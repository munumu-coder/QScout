# Protocol.js Internal Mechanism Documentation

**Fecha:** 2026-07-17  
**Fuente:** Análisis de `lib.min.js` (Webpack bundle de MyQode)  
**Módulo:** Protocol (Webpack module 99)

---

## 1. Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                    APLICACIÓN (Robot class)                     │
│  getUltrasonicValue(port), setLed(r,g,b), moveForward(speed)... │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OrderManager (module 673)                    │
│  Genera Order ID único (2-254) para cada petición              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Protocol (module 99)                         │
│  Construye paquetes RB/MK, parsea respuestas                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RobotItem (module 668)                       │
│  Gestiona conexión, cola de callbacks (listBack), envío/recepción│
└───────────┬─────────────────────────────────┬───────────────────┘
            │                                 │
            ▼                                 ▼
    ┌───────────────┐                ┌───────────────────┐
    │  UART (RB)    │                │  BLE (MK + RB)    │
    │  Serial USB   │                │  Dongle + BLE     │
    └───────────────┘                └───────────────────┘
```

---

## 2. OrderManager — Generación de Order ID

**Ubicación:** `lib.min.js:305862-305907`

### 2.1 Definición

```javascript
class OrderManager {
    constructor() {
        this.index = 1;        // Contador monótono
        this.indexList = [];   // Código muerto (nunca se usa)
    }

    create() {
        let order = {};
        order.id = this.orderId();
        return order;
    }

    orderId() {
        this.index++;
        const maxId = 255;
        if (this.index >= maxId) {
            this.index = 2;   // Reinicia en 2 (0 y 1 reservados)
        }
        return this.index;
    }
}
```

### 2.2 Ciclo de Vida del Order ID

```
┌─────────────────────────────────────────────────────────────┐
│                    Order ID Lifecycle                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Inicialización:                                            │
│  ┌─────────┐                                                │
│  │ index=1 │                                                │
│  └────┬────┘                                                │
│       │                                                     │
│       ▼                                                     │
│  Primera petición:                                          │
│  ┌─────────────┐     ┌─────────────┐                        │
│  │ index=1→2   │────▶│ id=2        │  (primer ID válido)   │
│  └─────────────┘     └─────────────┘                        │
│                                                             │
│  Peticiones subsiguientes:                                  │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐               │
│  │ index=3 │────▶│ id=3    │     │ id=4    │ ...           │
│  └─────────┘     └─────────┘     └─────────┘               │
│                                                             │
│  Límite superior:                                           │
│  ┌─────────────┐     ┌─────────────┐                        │
│  │ index=254   │────▶│ id=254      │  (último ID válido)   │
│  └─────────────┘     └─────────────┘                        │
│                                                             │
│  Reinicio automático:                                       │
│  ┌─────────────┐     ┌─────────────┐                        │
│  │ index=255   │────▶│ index=2     │  (vuelve a empezar)   │
│  └─────────────┘     └─────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Valores Reservados

| Valor | Estado | Uso |
|-------|--------|-----|
| **0** | Reservado | Datos automáticos/reporte no solicitado |
| **1** | Reservado | No utilizado por OrderManager |
| **2-254** | Válidos | IDs generados por OrderManager |
| **255** | Techo | Cuando `index >= 255`, se reinicia a 2 |

### 2.4 Almacenamiento en el Paquete

El Order ID se almacena como `UInt8` en el **byte offset 3** de cada paquete:

```
RB Packet:
[0-1]  Header "RB"
[2]    Longitud total
[3]    ★ ORDER ID (UInt8) ★
[4]    Action code
[5-N]  Payload
[N+1]  Checksum
```

---

## 3. listBack — Cola de Callbacks

**Ubicación:** `lib.min.js:303879` (declaración), `lib.min.js:304010-304050` (registro)

### 3.1 Declaración

```javascript
// En RobotItem constructor
this.listBack = [];  // Cola de callbacks pendientes
```

### 3.2 Estructura del Elemento

```javascript
{
    key: <orderId>,        // Number (2-254): Order ID a correlacionar
    callBack: <function>   // Function(buffer): resuelve la Promise pendiente
}
```

### 3.3 Registro de Callbacks

```javascript
// En RobotItem.request()
request(isWait, buffer) {
    return new Promise(function(resolve, reject) {
        that.writeBuffer(buffer);  // Enviar paquete

        if (!isWait) {
            resolve(1);  // Fire-and-forget
        } else {
            var orderId = buffer.readUInt8(3, false);  // byte[3] = order ID

            // Caso especial: paquetes Dongle relay
            if (orderId === 0) {
                var _head = buffer.toString('utf8', 0, 2);
                let actid = buffer.readUInt8(4, false);
                if (actid === 0x06 && _head === that.head[1]) {
                    orderId = buffer.readUInt8(14, false);  // byte[14] para MK relay
                }
            }

            if (orderId === 0) {
                resolve(1);  // orderId=0 no espera respuesta
            }

            var flag = 0;

            function backData(data) {  // Closure que resuelve la Promise
                if (flag === 0) {
                    flag = 1;
                    resolve(data);
                }
            }

            var item = {
                key: orderId,      // Order ID a buscar en respuestas
                callBack: backData  // Callback que resuelve la Promise
            };

            that.listBack.push(item);  // Añadir a la cola

            // Timeout de 4500ms
            that.wait(that.timeOutRequest).then(function(data) {
                if (flag === 0) {
                    flag = 2;
                    resolve(null);  // Timeout: resolver con null
                }
            });
        }
    });
}
```

### 3.4 Diagrama de la Cola

```
listBack = [
    ┌─────────────────────────────────────┐
    │ { key: 7, callBack: [Function] }   │  ← Petición ultrasonido
    ├─────────────────────────────────────┤
    │ { key: 8, callBack: [Function] }   │  ← Petición LED
    ├─────────────────────────────────────┤
    │ { key: 9, callBack: [Function] }   │  ← Petición buzzer
    └─────────────────────────────────────┘

Cuando llega respuesta con orderId=7:
    → Busca item.key === 7
    → Ejecuta item.callBack(buffer)
    → Promise se resuelve con el buffer
    → (Filtro elimina todos los items - ver §3.5)
```

### 3.5 Bug Conocido en la Limpieza

**Ubicación:** `lib.min.js:304122-304125`, `304143-304146`, `304192-304195`

```javascript
// BUG: Falta 'return' en el filtro
this.listBack = this.listBack.filter(function(item) {
    orderId !== item.key;  // ❌ Siempre retorna undefined (falsy)
});
```

**Consecuencia:** El filtro elimina **todos** los items de `listBack`, no solo el coincidente. Funciona porque las peticiones son secuenciales (delay de 20ms en `sendSingle`).

---

## 4. Proceso de Registro de Peticiones

### 4.1 Flujo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DE REGISTRO                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Robot.someMethod(port)                                      │
│     │                                                           │
│     │  order = this.orderManager.create()                       │
│     │  → { id: 7 }                                              │
│     │                                                           │
│     │  buffer = Protocol.someMethod(order.id, port)             │
│     │  → Buffer con orderId=7 en byte[3]                       │
│     │                                                           │
│     ▼                                                           │
│  2. Robot.request(isWait=true, order, buffer)                   │
│     │                                                           │
│     │  Delega a RobotManage.getCurrentRobot().request()         │
│     ▼                                                           │
│  3. RobotItem.request(isWait=true, buffer)                      │
│     │                                                           │
│     ├──→ writeBuffer(buffer)  ← ENVÍO POR SERIAL               │
│     │                                                           │
│     ├──→ orderId = buffer.readUInt8(3)  ← LEER ORDER ID        │
│     │                                                           │
│     ├──→ listBack.push({                                        │
│     │        key: orderId,                                      │
│     │        callBack: resolve                                  │
│     │    })  ← REGISTRAR EN COLA                               │
│     │                                                           │
│     └──→ setTimeout(4500ms, timeoutHandler)  ← INICIAR TIMER  │
│                                                                 │
│  ESTADO: Promise pendiente, esperando respuesta                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Caso Especial: Paquetes MK Relay

Cuando se envía un paquete MK para relay (action 0x06), el Order ID real está en **byte[14]**, no en byte[3]:

```javascript
// En RobotItem.request()
if (orderId === 0) {
    var _head = buffer.toString('utf8', 0, 2);
    let actid = buffer.readUInt8(4, false);
    if (actid === 0x06 && _head === that.head[1]) {
        orderId = buffer.readUInt8(14, false);  // ← Order ID real en byte[14]
    }
}
```

**Estructura del paquete MK relay:**

```
MK Packet (set_robot_data):
[0-1]   "MK"
[2]     Total size
[3]     0x00 (orderId siempre 0 para relay)
[4]     0x06 (set_robot_data)
[5-10]  MAC address (6 bytes)
[11-12] "RB" (header del paquete interno)
[13]    RB size
[14]    ★ RB ORDER ID (el que se usa para correlación) ★
[15]    RB action
[...]   RB payload
[last]  RB checksum
[last]  MK checksum
```

---

## 5. Correlación Petición-Respuesta

### 5.1 Mecanismo UART (backWork_RB)

**Ubicación:** `lib.min.js:304100-304125`

```javascript
backWork_RB(buffer) {
    let orderId = buffer.readUInt8(3, false);  // byte[3] del paquete RB

    // orderId === 0: Reporte no solicitado
    if (orderId === 0) {
        RobotManage.doListenOnDataComplete(buffer, orderId, 1);
        return;
    }

    // Verificar checksum
    let check = buffer.readUInt8(buffer.length - 1, false);
    let checkTrue = this.sumCheck(buffer.slice(0, buffer.length - 1));
    if (check !== checkTrue) {
        console.error('packet checksum error');
        return false;
    }

    // Buscar en listBack
    for (let i = 0; i < this.listBack.length; i++) {
        let key = this.listBack[i].key;
        if (key === orderId) {
            this.listBack[i].callBack(buffer);  // ← RESOLVER PROMISE
            // Filtro (con bug)
            return true;
        }
    }
}
```

### 5.2 Mecanismo BLE (backWork_MK)

**Ubicación:** `lib.min.js:304133-304200`

```javascript
backWork_MK(buffer) {
    var orderId = buffer.readUInt8(3, false);   // byte[3] MK
    var actionId = buffer.readUInt8(4, false);  // byte[4] MK

    // Caso 1: Respuesta directa del Dongle (orderId >= 2)
    if (orderId >= 2) {
        for (var i = 0; i < this.listBack.length; i++) {
            var key = this.listBack[i].key;
            if (key === orderId) {
                this.listBack[i].callBack(buffer);  // ← RESOLVER
                return true;
            }
        }
    }

    // Caso 2: Desconexión BLE (orderId=0, actionId=8)
    if (orderId === 0 && actionId === 8) {
        RobotManage.doListenOnDataComplete(buffer, this.port, 10);
        return;
    }

    // Caso 3: Resultado de escaneo (orderId=0, actionId=3)
    if (orderId === 0 && actionId === 3) {
        if (this.dongle.scanFun) this.dongle.scanFun(buffer);
        return;
    }

    // Caso 4: Robot data relay (orderId=0, actionId=7)
    if (orderId === 0 && actionId === 7) {
        let rbOrderId = buffer.readUInt8(14, false);  // ← ORDER ID REAL en byte[14]

        // Reporte no solicitado del robot
        if (rbOrderId === 0) {
            let rb_buffer = Protocol.parseMkRobotBackData(buffer);
            RobotManage.doListenOnDataComplete(rb_buffer, rbOrderId, 1);
            return;
        }

        // Respuesta interactiva: correlacionar por rbOrderId
        for (var i = 0; i < this.listBack.length; i++) {
            var key = this.listBack[i].key;
            if (key === rbOrderId) {
                this.listBack[i].callBack(buffer);  // ← RESOLVER
                return true;
            }
        }
    }
}
```

### 5.3 Diagrama de Correlación

```
┌─────────────────────────────────────────────────────────────────┐
│              CORRELACIÓN PETICIÓN-RESPUESTA                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  UART (RB directo):                                             │
│  ┌──────────┐          ┌──────────┐                             │
│  │ TX: orderId=7       │ RX: orderId=7   ← MATCH              │
│  │ byte[3]=0x07        │ byte[3]=0x07     (mismo byte)        │
│  └──────────┘          └──────────┘                             │
│                                                                 │
│  BLE (MK relay):                                                │
│  ┌──────────┐          ┌──────────┐                             │
│  │ TX: MK orderId=0    │ RX: MK orderId=0                      │
│  │ byte[3]=0x00        │ byte[3]=0x00                          │
│  │ RB orderId=7        │ RB orderId=7   ← MATCH               │
│  │ byte[14]=0x07       │ byte[14]=0x07   (byte diferente)     │
│  └──────────┘          └──────────┘                             │
│                                                                 │
│  BLE (MK directo - Dongle):                                     │
│  ┌──────────┐          ┌──────────┐                             │
│  │ TX: MK orderId=5    │ RX: MK orderId=5  ← MATCH            │
│  │ byte[3]=0x05        │ byte[3]=0x05   (mismo byte)          │
│  └──────────┘          └──────────┘                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Diferencias UART vs BLE

### 6.1 Tabla Comparativa

| Aspecto | UART (RB) | BLE (MK + RB) |
|---------|-----------|---------------|
| **Header** | `"RB"` (0x52, 0x42) | `"MK"` (0x4D, 0x4B) envolviendo `"RB"` |
| **Order ID location** | byte[3] | byte[3] (MK) + byte[14] (RB interno) |
| **Order ID relay** | N/A | byte[3] siempre 0x00 |
| **Action codes** | RB actions (0x01-0xB6) | MK actions (0x01-0x09) |
| **Routing** | `backWork_RB()` | `backWork_MK()` |
| **Correlación** | byte[3] del paquete RB | byte[14] del paquete MK (action 0x07) |
| **Desempaquetado** | No necesario | `parseMkRobotBackData()` extrae RB interno |

### 6.2 Flujo UART

```
PC                           Robot
│                             │
│  ┌─────────────────────┐    │
│  │ RB [orderId] [act]  │────│  TX: Paquete RB directo
│  └─────────────────────┘    │
│                             │
│  ┌─────────────────────┐    │
│  │ RB [orderId] [resp] │←───│  RX: Respuesta RB
│  └─────────────────────┘    │
│                             │
│  backWork_RB(buffer):       │
│  - orderId = byte[3]        │
│  - match listBack[i].key   │
│  - callBack(buffer)         │
```

### 6.3 Flujo BLE

```
PC                     Dongle                    Robot
│                        │                        │
│  ┌───────────────┐     │                        │
│  │ MK [orderId=0]│     │                        │
│  │ action=0x06   │─────│  TX: MK relay          │
│  │ [MAC] [RB...] │     │  (orderId=0 en MK)    │
│  └───────────────┘     │                        │
│                        │  ┌───────────────┐     │
│                        │  │ RB [orderId]  │─────│  Forward RB
│                        │  └───────────────┘     │
│                        │                        │
│                        │  ┌───────────────┐     │
│                        │←─│ RB [orderId]  │     │  Respuesta RB
│                        │  └───────────────┘     │
│  ┌───────────────┐     │                        │
│  │ MK [orderId=0]│     │                        │
│  │ action=0x07   │←────│  RX: MK relay back    │
│  │ [MAC] [RB...] │     │  (action 0x07)        │
│  └───────────────┘     │                        │
│                        │                        │
│  backWork_MK(buffer):  │                        │
│  - MK orderId=0        │                        │
│  - actionId=0x07       │                        │
│  - rbOrderId=byte[14]  │  ← Order ID real       │
│  - match listBack[i].key│                       │
│  - callBack(buffer)    │                        │
```

---

## 7. Extracción del Order ID desde Paquete MK

### 7.1 Paquete MK Relay (action 0x07)

```
Offset  Tamaño  Campo                    Descripción
─────────────────────────────────────────────────────────
[0-1]   2B      Header "MK"              0x4D, 0x4B
[2]     1B      Total size               Longitud total del paquete
[3]     1B      MK orderId               Siempre 0x00 para relay
[4]     1B      MK action                0x07 (back_robot_data)
[5-10]  6B      MAC address              Dirección MAC del robot
[11]    1B      RB header                0x52 ("R")
[12]    1B      RB header                0x42 ("B")
[13]    1B      RB size                  Longitud del paquete RB
[14]    1B      ★ RB ORDER ID ★         ID real para correlación
[15]    1B      RB action                Código de acción RB
[...]   NB      RB payload               Datos de respuesta
[last]  1B      RB checksum              Suma verificación RB
[last]  1B      MK checksum              Suma verificación MK
```

### 7.2 Código de Extracción

```javascript
// En backWork_MK()
if (orderId === 0 && actionId === 7) {
    let rbOrderId = buffer.readUInt8(14, false);  // ← BYTE 14
    // ...
}
```

### 7.3 Ejemplo Real

```
Paquete MK relay recibido:
Hex:  4D 4B 12 00 07 A1 B2 C3 D4 E5 F6 52 42 06 07 03 01 09 C0 8E
      ── ── ── ── ── ─────────────────── ── ── ── ── ── ────── ── ──
      M  K  sz id act MAC(6 bytes)       R  B  sz id act data chk chk

byte[3]  = 0x00 (MK orderId - ignorado para correlación)
byte[14] = 0x07 (RB orderId - usado para correlación)
```

---

## 8. parseMkRobotBackData() — Desempaquetado MK

**Ubicación:** `lib.min.js:81800`

### 8.1 Función

```javascript
parseMkRobotBackData(buffer) {
    if (!buffer || buffer.length <= 2) return undefined;

    var _head = buffer.toString('utf8', 0, 2);

    if (_head === this.head[1]) {  // head[1] = 'MK'
        // Extraer RB interno: desde byte[11] hasta byte[length-2]
        // (omite header MK[0-4], MAC[5-10], elimina checksum[last])
        const newbuffer = buffer.slice(11, buffer.length - 1);
        return newbuffer;
    }

    return buffer;  // Ya es RB, retornar tal cual
}
```

### 8.2 Diagrama de Desempaquetado

```
ENTRADA (paquete MK relay):
┌──────────────────────────────────────────────────────────────┐
│ MK │ sz │ id=0 │ act=07 │ MAC(6B) │ RB header │ RB... │ chk │
│ 0  │ 1  │ 2    │ 3      │ 4-9     │ 10-11     │ 12-N  │ N+1 │
└──────────────────────────────────────────────────────────────┘
                                                    ▲
                                                    │
                                            parseMkRobotBackData()
                                                    │
                                                    ▼
SALIDA (paquete RB interno):
┌──────────────────────────────────────┐
│ RB │ sz │ id │ act │ payload │ chk   │
│ 0  │ 1  │ 2  │ 3   │ 4-N     │ N+1   │
└──────────────────────────────────────┘
```

### 8.3 Transformación de Bytes

```
Entrada: buffer.slice(11, buffer.length - 1)

Antes: [11][12][13][14][15]...[N-1][N]
        RB  sz  id  act payload  chk MK-chk

Después: [0] [1] [2] [3]  [4]  ...[N-2]
         RB  sz  id  act payload  chk
```

---

## 9. Proceso Completo: Petición → Respuesta

### 9.1 Flujo UART Completo

```
┌─────────────────────────────────────────────────────────────────┐
│           FLUJO COMPLETO UART (RB)                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  APLICACIÓN                                                    │
│  ══════════                                                    │
│  1. Robot.getUltrasonicValue(port)                              │
│  2. order = orderManager.create()  → { id: 7 }                 │
│  3. buffer = Protocol.getUltrasonicValue(7, port)               │
│     → [52 42 06 07 A1 02 00 09] (ejemplo)                     │
│                                                                 │
│  TRANSPORTE                                                     │
│  ══════════                                                     │
│  4. RobotItem.request(true, buffer)                             │
│  5. writeBuffer(buffer) → SerialManage → serial port write      │
│  6. listBack.push({ key: 7, callBack: resolve })               │
│  7. setTimeout(4500ms, timeoutHandler)                          │
│                                                                 │
│  [ESPERANDO RESPUESTA...]                                       │
│                                                                 │
│  RECEPCIÓN                                                      │
│  ══════════                                                     │
│  8. Serial port 'data' event → RobotItem.read(buffer)          │
│  9. backWork(buffer) → BufferCache.handle(buffer)               │
│  10. BufferCache: cacheData → doListData → bufferConcat         │
│      → cachePackage → doPackage → completeData                  │
│  11. doBackWorkOnDataComplete(buffer)                           │
│  12. head = "RB" → backWork_RB(buffer)                          │
│                                                                 │
│  CORRELACIÓN                                                    │
│  ══════════                                                     │
│  13. orderId = buffer.readUInt8(3) → 7                          │
│  14. Verificar checksum                                         │
│  15. Buscar listBack[i].key === 7                               │
│  16. listBack[i].callBack(buffer) → resolve(buffer)            │
│                                                                 │
│  PROCESAMIENTO                                                  │
│  ══════════                                                     │
│  17. backBuffer = new Buffer(data)                              │
│  18. result = Protocol.parseUltrasonicValue(backBuffer)         │
│      → lee buf[5]*256 + buf[6] = 2500mm                       │
│  19. return result                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Flujo BLE Completo

```
┌─────────────────────────────────────────────────────────────────┐
│           FLUJO COMPLETO BLE (MK + RB)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  APLICACIÓN                                                    │
│  ══════════                                                    │
│  1. Robot.getUltrasonicValue(port)                              │
│  2. order = orderManager.create()  → { id: 7 }                 │
│  3. buffer = Protocol.getUltrasonicValue(7, port)               │
│     → RB packet: [52 42 06 07 A1 02 00 09]                    │
│                                                                 │
│  ENVOLVER EN MK                                                 │
│  ══════════════                                                 │
│  4. mkBuffer = Protocol.mkSetRobotData(mac, rbBuffer)          │
│     → [4D 4B 12 00 06 A1 B2 C3 D4 E5 F6 52 42 06 07 A1 02 00 ...]
│                                                                 │
│  TRANSPORTE                                                     │
│  ══════════                                                     │
│  5. RobotItem.request(true, mkBuffer)                           │
│  6. writeBuffer(mkBuffer) → SerialManage → serial port write   │
│  7. orderId = 0 (byte[3] del MK)                               │
│  8. Detecta MK relay: orderId = byte[14] = 7                   │
│  9. listBack.push({ key: 7, callBack: resolve })               │
│  10. setTimeout(4500ms, timeoutHandler)                         │
│                                                                 │
│  [DONGLE REENVÍA A ROBOT VÍA BLE...]                           │
│  [ROBOT RESPONDE, DONGLE RELAISA DE VUELTA...]                  │
│                                                                 │
│  RECEPCIÓN                                                      │
│  ══════════                                                     │
│  11. Serial port 'data' event → RobotItem.read(buffer)         │
│  12. backWork(buffer) → BufferCache.handle(buffer)              │
│  13. BufferCache: reensambla paquete MK completo               │
│  14. doBackWorkOnDataComplete(buffer)                           │
│  15. head = "MK" → backWork_MK(buffer)                         │
│                                                                 │
│  CORRELACIÓN                                                    │
│  ══════════                                                     │
│  16. MK orderId = byte[3] = 0                                  │
│  17. actionId = byte[4] = 0x07 (back_robot_data)              │
│  18. rbOrderId = byte[14] = 7                                  │
│  19. Buscar listBack[i].key === 7                               │
│  20. listBack[i].callBack(buffer) → resolve(buffer)           │
│                                                                 │
│  DESEMPAQUETADO                                                 │
│  ══════════════                                                 │
│  21. backBuffer = new Buffer(data)                              │
│  22. rbBuffer = Protocol.parseMkRobotBackData(backBuffer)       │
│      → Extrae RB interno desde byte[11]                         │
│  23. result = Protocol.parseUltrasonicValue(rbBuffer)           │
│      → lee buf[5]*256 + buf[6] = 2500mm                       │
│  24. return result                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Manejo de Respuestas No Solicitadas

### 10.1 Detección

```javascript
// En backWork_RB() o backWork_MK()
if (orderId === 0) {
    // Reporte no solicitado del robot
    RobotManage.doListenOnDataComplete(buffer, orderId, 1);
    return;
}
```

### 10.2 Tipos de Respuesta No Solicitada

| Condición | Descripción | Manejo |
|-----------|-------------|--------|
| UART, orderId=0 | Reporte automático del robot | `doListenOnDataComplete(buffer, 0, 1)` |
| BLE, orderId=0, actionId=8 | Desconexión BLE | `doListenOnDataComplete(buffer, port, 10)` |
| BLE, orderId=0, actionId=3 | Resultado de escaneo | `dongle.scanFun(buffer)` |
| BLE, orderId=0, actionId=7, rbOrderId=0 | Reporte robot vía BLE | `doListenOnDataComplete(rb_buffer, 0, 1)` |

### 10.3 Diagrama de Decisión

```
¿orderId === 0?
    │
    ├─── SÍ ──→ ¿Es UART (RB)?
    │               │
    │               ├─── SÍ ──→ doListenOnDataComplete() [reporte]
    │               │
    │               └─── NO (MK) ──→ ¿actionId?
    │                                   │
    │                                   ├─── 0x03 ──→ scanFun() [escaneo]
    │                                   │
    │                                   ├─── 0x08 ──→ doListenOnDataComplete() [desconexión]
    │                                   │
    │                                   └─── 0x07 ──→ ¿rbOrderId?
    │                                                   │
    │                                                   ├─── 0 ──→ unwrap + doListenOnDataComplete()
    │                                                   │
    │                                                   └─── >0 ──→ match listBack (respuesta)
    │
    └─── NO ──→ ¿Es UART (RB)?
                    │
                    ├─── SÍ ──→ match listBack por byte[3]
                    │
                    └─── NO (MK) ──→ match listBack por byte[3] (MK directo)
```

---

## 11. Constantes y Enums

### 11.1 Protocol Headers

```javascript
head: ["RB", "MK"]  // robot_head[0]="RB", robot_head[1]="MK"
```

### 11.2 MK Action Codes (mkAction)

| Código | Nombre | Descripción |
|--------|--------|-------------|
| 0x01 | `get_version` | Obtener versión del dongle |
| 0x02 | `set_scan` | Iniciar/detener escaneo BLE |
| 0x03 | `get_list` | Solicitar lista de dispositivos BLE |
| 0x04 | `get_info` | Solicitar RSSI de un dispositivo |
| 0x05 | `set_connect` | Conectar a robot BLE |
| 0x06 | `set_robot_data` | Enviar datos al robot vía dongle |
| 0x07 | `back_robot_data` | Robot reenvía datos vía dongle |
| 0x08 | `back_dongle` | Notificación del dongle (desconexión) |
| 0x09 | `set_disconect` | Desconectar robot BLE |

### 11.3 RB Action Codes (actions)

| Código | Nombre | Descripción |
|--------|--------|-------------|
| 0x01 | `get_device_info` | Consultar información del dispositivo |
| 0x02 | `get_interface_info` | Consultar información de un puerto |
| 0x03 | `get_all_interface_info` | Consultar todos los puertos |
| 0x10 | `set_led` | Establecer color LED |
| 0x11 | `set_motor` | Establecer velocidad motor |
| 0x13 | `set_buzzer` | Establecer buzzer |
| 0x14 | `set_matrix` | Establecer matriz LED |
| 0xA1 | `get_ultrasonic_value` | Leer sensor ultrasónico |
| 0xA2 | `get_button_info` | Leer estado del botón |
| 0xA3 | `get_voltage` | Leer voltaje de batería |
| 0xA6 | `get_light_sensor_value` | Leer sensor de luz |
| 0xAA | `get_color_sensor_value` | Leer sensor de color |

### 11.4 Sum Check Algorithm

```javascript
sumCheck(buffer) {
    let sum = 0;
    for (let i = 0; i < buffer.length; i++) {
        sum += buffer[i];
    }
    return sum % 256;
}
```

---

## 12. Variables Clave Resumen

| Variable | Ubicación | Propósito |
|----------|-----------|-----------|
| `this.index` | OrderManager:305874 | Contador de Order ID (1-254, cíclico) |
| `this.indexList` | OrderManager:305875 | **Código muerto** (declarado, nunca usado) |
| `order.id` | OrderManager:305883 | ID UInt8 en byte[3] de paquetes |
| `this.listBack` | RobotItem:303879 | Cola `{key, callBack}` de respuestas pendientes |
| `this.head` | RobotItem:303881 | `["RB", "MK"]` constantes de header |
| `this.timeOutRequest` | RobotItem:303883 | Timeout 4500ms para respuestas |
| `this.connectType` | RobotItem:303874 | 0=desconocido, 1=UART, 2=BLE |
| `this.listenOnData` | RobotItem:303886 | Listener raw (escape hatch) |
| `this.dongle.mac` | RobotItem:303862 | MAC del robot BLE conectado |
| `this.bufferCacheList` | BufferCache:305699 | Fragmentos incompletos en reensamblaje |
| `this.bufferCacheList2` | BufferCache:305705 | Cola de datos crudos entrantes |

---

## 13. Notas Arquitectónicas

1. **Singletons:** `Protocol`, `BufferCache` y `RobotManage` se instancian como singletons al cargar el módulo.

2. **listBack se limpia completamente:** El bug en el filtro (falta `return`) significa que cada respuesta elimina todos los items pendientes. Funciona porque las peticiones son secuenciales (delay de 20ms en `sendSingle`).

3. **MK layer es transparente:** El código de alto nivel (`Robot` class) construye paquetes RB de la misma manera para ambos paths. La única diferencia es que para BLE, el paquete RB se envuelve adicionalmente en MK via `mkSetRobotData`, y la respuesta se desempaqueta via `parseMkRobotBackData`.

4. **Correlación diferente por path:**
   - **UART (RB):** Order ID en **byte[3]** de la respuesta
   - **BLE directo (MK orderId ≥ 2):** Order ID en **byte[3]** de la respuesta MK
   - **BLE relay (MK action 0x07):** Order ID interno RB en **byte[14]** de la respuesta MK

5. **`listenOnData`** es un escape hatch para monitoreo de paquetes crudos, llamado antes de cualquier despacho de protocolo en `doBackWorkOnDataComplete`.

---

*Documento generado el 2026-07-17 basado en análisis de Protocol.js (Webpack module 99) del bundle `lib.min.js` de MyQode.*
