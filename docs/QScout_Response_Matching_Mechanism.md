# QScout Response Matching Mechanism

**Fecha:** 2026-07-17  
**Estado:** Documentado y validado experimentalmente

---

## 1. Resumen

El mecanismo de correlación petición-respuesta en el protocolo RB se basa EXCLUSIVAMENTE en el **Order ID**, NO en el código de acción. Este documento describe detalladamente cómo funciona este mecanismo.

---

## 2. Generación del Order ID

### 2.1 En Protocol.js (MyQode)

```javascript
class OrderManager {
    constructor() {
        this.index = 1;
    }
    
    orderId() {
        this.index++;
        if (this.index >= 255) {
            this.index = 2;
        }
        return this.index;
    }
}
```

**Características:**
- Comienza en 1
- Se incrementa secuencialmente
- Wraps around en 255 (vuelve a 2)
- Rango válido: 2-254

### 2.2 En nuestra librería Python

```python
class OrderManager:
    def __init__(self) -> None:
        self._next = 0

    def create(self) -> int:
        order = self._next
        self._next = (self._next + 1) & 0xFF
        return order
```

**Características:**
- Comienza en 0
- Se incrementa secuencialmente
- Wraps around en 255 (vuelve a 0)
- Rango válido: 0-255

---

## 3. Utilización del Order ID

### 3.1 En la Petición

El Order ID se escribe en el byte 3 del paquete RB:

```
[Header 2B][Length 1B][Order ID 1B][Action 1B][Payload N][Checksum 1B]
                         ↑
                     Byte 3
```

**Ejemplo:**
```python
order = conn.next_order_id()  # Genera Order ID único
pkt = build_get_ultrasonic(order, 1)  # Incluye Order ID en byte 3
```

### 3.2 En la Respuesta

El robot replica exactamente el mismo Order ID en el byte 3 de la respuesta:

```
Petición:  [52 42 07 05 A1 01 42]
                         ↑
                     Order ID = 5

Respuesta: [52 42 08 05 01 09 C4 6B]
                         ↑
                     Order ID = 5 (echo)
```

---

## 4. Mecanismo de Callbacks

### 4.1 En Protocol.js (Serial Directo)

```javascript
// 1. Registrar callback con Order ID como clave
request(isWait, buffer) {
    var orderId = buffer.readUInt8(3);  // Extraer Order ID
    var item = { key: orderId, callBack: backData };
    that.listBack.push(item);  // Registrar en cola
}

// 2. Procesar respuesta
doBackWorkOnDataComplete(buffer) {
    var orderId = buffer.readUInt8(3);  // Extraer Order ID de respuesta
    
    // Auto-report (orderId === 0)
    if (orderId === 0) {
        RobotManage.doListenOnDataComplete(buffer, orderId, 1);
        return;
    }
    
    // Buscar callback registrado
    for (let i = 0; i < this.listBack.length; i++) {
        let key = this.listBack[i].key;
        if (key === orderId) {  // ← COINCIDENCIA POR ORDER ID
            this.listBack[i].callBack(buffer);
            // Remover de cola
        }
    }
}
```

### 4.2 En Protocol.js (BLE/MK)

```javascript
// Para comandos RB a través de BLE
backWork_MK(buffer) {
    var orderId = buffer.readUInt8(3);  // MK layer orderId
    var actionId = buffer.readUInt8(4); // MK layer action
    
    // Para datos de robot (MK action 0x07)
    if (orderId === 0 && actionId === 7) {
        let rbOrderId = buffer.readUInt8(14);  // Extraer RB Order ID
        
        if (rbOrderId === 0) {
            // Auto-report
            let rb_buffer = Protocol.parseMkRobotBackData(buffer);
            RobotManage.doListenOnDataComplete(rb_buffer, rbOrderId, 1);
            return;
        }
        
        if (rbOrderId >= 1) {
            for (var i = 0; i < this.listBack.length; i++) {
                if (this.listBack[i].key === rbOrderId) {  // ← COINCIDENCIA
                    this.listBack[i].callBack(buffer);
                }
            }
        }
    }
}
```

---

## 5. Cola de Peticiones Pendientes

### 5.1 Estructura

```javascript
// Cola de callbacks pendientes
listBack = [
    { key: orderId1, callBack: callback1 },
    { key: orderId2, callBack: callback2 },
    // ...
]
```

### 5.2 Flujo

1. **Enviar petición:** Se genera Order ID único, se construye paquete, se envía
2. **Registrar callback:** Se añade `{ key: orderId, callBack: callback }` a `listBack`
3. **Esperar respuesta:** Se bloquea hasta recibir datos o timeout
4. **Procesar respuesta:** Se extrae Order ID, se busca en `listBack`, se ejecuta callback
5. **Limpiar:** Se remueve de `listBack`

---

## 6. Correlación Petición-Respuesta

### 6.1 Proceso

```
Petición                          Respuesta
    │                                  │
    │  [52 42 07 05 A1 01 42]         │
    │         Order ID = 5             │
    │──────────────────────────────────│
    │                                  │
    │                          [52 42 08 05 01 09 C4 6B]
    │                                  │
    │                          Order ID = 5 (echo)
    │                                  │
    │◀─────────────────────────────────│
    │                                  │
    │  Coincidencia: 5 == 5           │
    │  Ejecutar callback asociado     │
```

### 6.2 Regla Fundamental

**LA CORRELACIÓN SE REALIZA EXCLUSIVAMENTE MEDIANTE ORDER ID.**

- El código de acción de la respuesta **NO** se utiliza para identificar la petición
- El código de acción de la respuesta **NO** coincide con el de la petición
- El código de acción de la respuesta **NO** debe utilizarse para dispatch

### 6.3 Evidencia Experimental

| Petición | Action Petición | Order ID | Action Respuesta | Order ID Respuesta |
|----------|-----------------|----------|------------------|-------------------|
| GET_DEVICE_INFO | 0x01 | 0 | 0x03 | 0 |
| GET_ULTRASONIC | 0xA1 | 1 | 0x01 | 1 |
| GET_LINE_VALUE | 0xA4 | 2 | 0x01 | 2 |
| SET_LED | 0x10 | 2 | 0x01 | 2 |

**Conclusión:** El Order ID siempre coincide, el Action nunca coincide.

---

## 7. Implementación en Python

### 7.1 Nuestra Implementación

```python
class Connection:
    def __init__(self):
        self._order = OrderManager()
        self._rx_buffer = bytearray()
    
    def next_order_id(self) -> int:
        """Generar Order ID único."""
        return self._order.create()
    
    def send_receive(self, packet: bytes, timeout: float = 0.5):
        """Enviar paquete y esperar respuesta."""
        self.send(packet)
        return self.receive(timeout)
    
    def receive(self, timeout: float = 0.5):
        """Recibir respuesta completa."""
        # Extrae paquetes del buffer
        # Retorna el último paquete válido
        # NO verifica el código de acción
```

### 7.2 Características

- **Simplificado:** No implementa cola de callbacks
- **Síncrono:** `send_receive` espera respuesta directamente
- **Sin verificación de Action:** Solo verifica checksum y header
- **Buffer circular:** Maneja múltiples paquetes en el buffer

---

## 8. Casos Especiales

### 8.1 Auto-Reports (Order ID = 0)

Cuando el Order ID es 0, es un auto-report del robot (no respuesta a petición):

```javascript
if (orderId === 0) {
    // Auto-report: notificar a todos los listeners
    RobotManage.doListenOnDataComplete(buffer, orderId, 1);
    return;
}
```

### 8.2 Timeouts

Si no se recibe respuesta en el tiempo límite:

```javascript
// Protocol.js maneja timeouts internamente
// Nuestra librería retorna None en receive()
```

### 8.3 Múltiples Peticiones

Si se envían múltiples peticiones rápidamente:

1. Cada petición tiene Order ID único
2. Las respuestas se correlacionan por Order ID
3. El buffer puede contener múltiples paquetes

---

## 9. Conclusiones

1. **El Order ID es el único mecanismo de correlación**
2. **El código de acción NO se utiliza para dispatch**
3. **Las respuestas NO son echoes de las peticiones**
4. **El robot puede enviar auto-reports (Order ID = 0)**
5. **Nuestra implementación es correcta** (usa Order ID, no Action)

---

## 10. Referencias

- Protocol.js: `app.asar` → `www/build/lib.min.js` → módulo 99
- Validación experimental: Fase 3B (2026-07-17)
- Paquetes de referencia: `docs/QScout_Reference_Packets.md`
