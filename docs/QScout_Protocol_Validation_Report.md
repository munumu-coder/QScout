# QScout Protocol Validation Report

**Fecha:** 2026-07-16  
**Fase:** 2 — Validación mínima del protocolo RB  

---

## 1. Comparación del Protocolo

| Elemento | Arduino (librería Robobloq) | MyQode (Protocol.js) | ¿Compatible? |
|----------|----------------------------|----------------------|--------------|
| **Header** | `0x52 0x42` ("RB") — identificado en análisis Fase 1A de `Robobloq-master/` | `0x52 0x42` ("RB") — `this.head = ['RB', 'MK']` en `Protocol.js` | ✓ Idéntico |
| **Length** | Byte 2, UInt8 — tamanho total del paquete | Byte 2, UInt8 — `buffer.writeUInt8(size, 2)` | ✓ Idéntico |
| **Order ID** | Byte 3, UInt8 — identificador de secuencia | Byte 3, UInt8 — `buffer.writeUInt8(order, 3)` | ✓ Idéntico |
| **Action** | Byte 4, UInt8 — codes 0x01-0x20 (SET), 0xA1-0xB2 (GET) — `k2x/QM_QMINDX.h:59-100` | Byte 4, UInt8 — `actions.set_*` / `actions.get_*` en `Protocol.js` | ✓ Idénticos |
| **Payload** | Variable, bytes 5..N-2 | Variable, bytes 5..N-2 | ✓ Idéntico |
| **Checksum** | `sum(all_bytes) % 256` — identificado en análisis Fase 1A | `sumCheck(buffer) { sum += buffer[i]; } return sum % 256;` | ✓ Idéntico |
| **Baudrate** | 115200 — `uno/RB_SERIAL_TASK.cpp:14-29` (registro AVR USART0) | 115200 — `se.open` → `"115200"` en app.asar | ✓ Idéntico |
| **Formato** | `[RB][size][orderId][action][payload...][checksum]` | `[RB][size][orderId][action][payload...][checksum]` | ✓ Idéntico |

---

## 2. Comparación de Tres Comandos

### Motor — ACTION 0x11

| Aspecto | Arduino | MyQode |
|---------|---------|--------|
| Action code | `0x11` — `MoterSpeed_SET` en `k2x/QM_QMINDX.h:63` | `0x11` — `set_motor: 0x11` en `Protocol.js` |
| Payload (individual) | port(1) + speed(1) | port(1, Int8) + speed(1, Int8) |
| Payload (dual) | — | `0x00`(1) + m1Speed(1, Int8) + m2Speed(1, Int8) |
| Paquete ejemplo | `[52 42 08 __ 11 PP SS CC]` | `[52 42 08 __ 11 PP SS CC]` |
| **Resultado** | ✓ Mismo action, mismo formato | |

### LED — ACTION 0x10

| Aspecto | Arduino | MyQode |
|---------|---------|--------|
| Action code | `0x10` — `Led_SET` en `k2x/QM_QMINDX.h:62` | `0x10` — `set_led: 0x10` en `Protocol.js` |
| Payload | port(1) + R(1) + G(1) + B(1) | port(1, Int8) + R(1, UInt8) + G(1, UInt8) + B(1, UInt8) |
| Paquete ejemplo | `[52 42 0A __ 10 PP RR GG BB CC]` | `[52 42 0A __ 10 PP RR GG BB CC]` |
| **Resultado** | ✓ Mismo action, mismo formato | |

### Buzzer — ACTION 0x13

| Aspecto | Arduino | MyQode |
|---------|---------|--------|
| Action code | `0x13` — `Buzzer_Set` en `k2x/QM_QMINDX.h:65` | `0x13` — `set_buzzer: 0x13` en `Protocol.js` |
| Payload | port(1) + frequency(2, UInt16BE) + duration(2, UInt16BE) | port(1, Int8) + rate(2, UInt16BE) + time(2, UInt16BE) |
| Paquete ejemplo | `[52 42 0B __ 13 PP RR RR TT TT CC]` | `[52 42 0B __ 13 PP RR RR TT TT CC]` |
| **Resultado** | ✓ Mismo action, mismo formato | |

---

## 3. Transporte

### UART

- **Datos transmitidos:** Paquete RB completo (`[RB][size][orderId][action][payload][checksum]`)
- **Envío directo:** `port.write(buffer)` → USB → ESP32 UART0
- **Implementación:** `serialport` v6.2.2 en MyQode; registro AVR UDR0 en Arduino
- **Velocidad:** 115200 baud, 8N1

### BLE

- **Datos transmitidos:** Paquete RB envuelto en paquete MK
- **Envoltura:** `Protocol.mkSetRobotData(mac, rbPacket)` → `[MK header][action 0x06][MAC 6B][rbPacket]`
- **Transporte final:** Dongle USB → BLE NUS (`6E400001-...`) → ESP32 `ble.py`
- **En ESP32:** `ble.py:104` → `gatts_write(21, data)` → callback → procesamiento

### Conclusión de transporte

| Transporte | Formato del payload RB | Envoltura |
|------------|----------------------|-----------|
| UART | RB directo | Ninguna |
| BLE | RB directo | envuelto en MK |

**Ambos transports utilizan el mismo paquete RB.** La única diferencia es que BLE añade una capa MK (header + MAC) alrededor del RB.

---

## 4. Conclusión Técnica

### **Opción A: El protocolo es el mismo.**

### Justificación

1. **Header idéntico:** `0x52 0x42` ("RB") — ambos lo utilizan.
2. **Estructura idéntica:** `[RB][size][orderId][action][payload][checksum]` — ambos lo siguen.
3. **Checksum idéntico:** `sum(all_bytes) % 256` — ambos lo implementan igual.
4. **Action codes idénticos:** 0x10, 0x11, 0x13, 0xA1, etc. — mismos valores en ambos.
5. **Payload idéntico:** Port, speed, R/G/B, frequency, duration — mismos campos, mismo orden, mismos tipos.
6. **Baudrate idéntico:** 115200 — ambos lo utilizan.
7. **Order ID:** Mismo mecanismo de correlación petición-respuesta.

### Limitación

La librería Arduino Robobloq es una **biblioteca de sensores** (no contiene el parser del protocolo). El parser real del Arduino está en el firmware compilado (`k1.hex`, `k2.hex`). Sin embargo, las action codes definidas en `QM_QMINDX.h` coinciden exactamente con las de `Protocol.js`, y la estructura del paquete es la misma.

MyQode es la **fuente primaria** del protocolo (contiene el parser completo en `Protocol.js`). La librería Arduino confirma las constantes y la estructura.

---

## 5. Respuesta a Preguntas de Cierre

### 1. ¿MyQode utiliza el protocolo RB?

**Sí.** El protocolo RB está implementado en `Protocol.js` dentro de `app.asar`. Header `0x52 0x42`, checksum `sum % 256`, action codes 0x01-0xB6.

### 2. ¿El protocolo es compatible con el de Arduino?

**Sí.** Son el mismo protocolo. Mismas action codes, misma estructura, mismo checksum, mismo baudrate. La librería Arduino define las constantes; MyQode implementa el parser completo.

### 3. ¿La documentación disponible permite implementar una librería Python Linux independiente?

**Sí.** La especificación completa está en `QScout_RB_Protocol_Specification.md`:
- Formato del paquete: documentado
- Todos los action codes: enumerados
- Todos los payloads: byte por byte
- Todos los parsers de respuesta: documentados
- Ejemplos reales de paquetes: verificados

**La Fase 2 se considera completada.** La Fase 3 (implementación de la librería Python) puede iniciarse.
