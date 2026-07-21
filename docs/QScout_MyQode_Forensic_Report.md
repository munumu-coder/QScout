# QScout MyQode Forensic Report

**Fecha:** 2026-07-16  
**Fase:** 1A — Análisis forense de MyQode  
**Objetivo:** Determinar cómo MyQode se comunica con el Q-Scout  

---

## 1. Arquitectura MyQode

### Tipo de Aplicación

MyQode es una **aplicación Electron** (desktop, Windows) basada en **Scratch 3.0** para programación por bloques de robots educativos.

### Estructura

```
MyQode.exe (64.5 MB, PE32+ x86-64)
  └── resources/
        ├── app.asar (89 MB) — Código JavaScript de la aplicación
        │     ├── main.js — Entry point Electron
        │     ├── ./mycode/services/robot/Protocol.js — Parser RB (module 99)
        │     ├── ./mycode/services/robot/RobotManage.js — Gestión de robots (module 53)
        │     ├── ./mycode/services/robot/Robot.js — API de alto nivel
        │     ├── ./mycode/services/robot/RobotItem.js — Item de robot conectado
        │     ├── ./mycode/serial/SerialManage.js — Gestión serial (module 69)
        │     ├── ./mycode/serial/SerialNode.js — Operaciones serial (module 670)
        │     ├── ./mycode/order/OrderManager.js — Gestión de orderId (module 673)
        │     ├── ./myvm/blocks/gs_blocks.js — Bloques Scratch (dispatcher)
        │     ├── ./mycode/enums/ — Action codes y constants (module 145)
        │     ├── ./mycode/storey/localinfo.js — Info local (module 97)
        │     ├── scratch-vm — VM de Scratch
        │     ├── scratch-blocks — Blockly visual
        │     ├── react / react-dom / react-redux — UI
        │     └── serialport v6.2.2 — Comunicación serial
        ├── electron.asar (254 KB) — Runtime Electron
        ├── remote/ — Firmware, drivers, código fuente
        │     ├── sources/ — Código fuente de firmware y drivers
        │     │     ├── k2x-python/ — MicroPython para K2 (Q-Scout)
        │     │     ├── k1x-python/ — MicroPython para K1
        │     │     ├── k2x/ — Arduino C++ para K2
        │     │     ├── k1x/ — Arduino C++ para K1
        │     │     ├── uno/ — Arduino C++ para Uno
        │     │     ├── mega/ — Arduino C++ para Mega
        │     │     ├── qmind.py — Bridge HTTP client
        │     │     ├── qmind_socket.py — Bridge Socket client
        │     │     └── Python/ — CPython 2.x completo
        │     ├── k2x.bin — Firmware MicroPython K2
        │     ├── k1x.bin — Firmware MicroPython K1
        │     ├── k2.hex — Firmware AVR K2
        │     ├── k1.hex — Firmware AVR K1
        │     ├── esp32spiram-20210902-v1.17.bin — MicroPython base
        │     └── arduino/ — Toolchain Arduino completa
        └── drivers/ — Drivers USB
              ├── CP2102/ — CP210x USB-Serial
              └── CP210x_Win10/ — Win10 drivers
```

### Datos Clave

| Propiedad | Valor |
|-----------|-------|
| Tipo | Electron (Chromium + Node.js) |
| Entry point | `main.js` |
| Framework UI | Scratch 3.0 (React + Blockly) |
| Tamaño app.asar | 89 MB |
| serialport | v6.2.2 |
| Actualización | `https://static.robobloq.cn/apps/pc/` |

---

## 2. Componentes Encontrados

| Archivo | Función | Importancia |
|---------|---------|-------------|
| `app.asar` → `Protocol.js` (module 99) | Construcción y parsing de paquetes RB/MK | **Crítico** |
| `app.asar` → `RobotManage.js` (module 53) | Gestión de robots conectados, dispatch de datos | **Crítico** |
| `app.asar` → `Robot.js` | API de alto nivel: getMkVersion, setMkConnectRobot, etc. | **Crítico** |
| `app.asar` → `SerialManage.js` (module 69) | Listado y E/S de puertos serie | **Alto** |
| `app.asar` → `SerialNode.js` (module 670) | Operaciones serial de bajo nivel, upload firmware | **Alto** |
| `app.asar` → `OrderManager.js` (module 673) | Generación incremental de orderId | **Alto** |
| `app.asar` → `gs_blocks.js` | Dispatcher de bloques Scratch → comandos robot | **Medio** |
| `app.asar` → `enums` (module 145) | Action codes, port constants, event types | **Alto** |
| `app.asar` → `localinfo.js` (module 97) | Info persistente: MAC, BLE name, connect type | **Medio** |
| `resources/remote/sources/k2x-python/ble.py` | BLE UART Service (NUS) en ESP32 | **Crítico** |
| `resources/remote/sources/k2x-python/QmindX.py` | Driver de hardware MicroPython (731 líneas) | **Alto** |
| `resources/remote/sources/k2x-python/Port.py` | Driver de puertos RJ11, detección de sensores | **Alto** |
| `resources/remote/sources/k2x-python/BDR612x.py` | Driver de motor (L298N, 57 líneas) | **Alto** |
| `resources/remote/sources/qmind.py` | Bridge HTTP → `127.0.0.1:12345` | **Medio** |
| `resources/remote/sources/qmind_socket.py` | Bridge Socket → `127.0.0.1:12345` | **Medio** |
| `resources/remote/sources/k2x/QM_QMINDX.h` | Action codes Arduino (0x01-0xB3) | **Alto** |
| `resources/remote/sources/k2x/QM_PORT.cpp` | Mux I2C, detección de sensores (Arduino) | **Medio** |
| `resources/remote/sources/uno/RB_SERIAL_TASK.cpp` | Driver UART AVR (register-level) | **Alto** |
| `resources/remote/k2x.bin` | Firmware MicroPython K2 compilado | **Alto** |
| `resources/remote/k2.hex` | Firmware AVR K2 compilado | **Medio** |

---

## 3. Flujo Completo de Comunicación

### USB/Serial

```
┌──────────────────────────────────────────────────────────┐
│                    MyQode Electron                        │
│                                                          │
│  Usuario presiona bloque "motor forward"                 │
│         ↓                                                │
│  gs_blocks.js → GsBlocks.blockCallBack()                │
│         ↓                                                │
│  Robot.setMotor(orderId, port, speed)                    │
│         ↓                                                │
│  Protocol.setMotor(order, port, speed)                   │
│    → Buffer.alloc(8)                                     │
│    → write('RB', 0, 2)    ← HEADER                      │
│    → writeUInt8(size, 2)  ← LENGTH                      │
│    → writeUInt8(order, 3) ← ORDER ID                    │
│    → writeUInt8(0x11, 4)  ← ACTION (set_motor)          │
│    → writeInt8(port, 5)   ← PAYLOAD                     │
│    → writeInt8(speed, 6)  ← PAYLOAD                     │
│    → writeUInt8(sum, 7)   ← CHECKSUM                    │
│         ↓                                                │
│  RobotItem.writeBuffer(buffer)                           │
│    → hex = buffer.toString('hex')                        │
│    → this.write(hex)                                     │
│         ↓                                                │
│  SerialManage.write(port, hexData)                       │
│    → new Buffer(hexData, "hex")                          │
│    → port.write(buffer)  ← serialport.write()            │
│         ↓                                                │
│  USB-Serial (CH340, 115200 baud)                         │
└──────────────────────────────────────────────────────────┘
         ↓
┌──────────────────────────────────────────────────────────┐
│               ESP32 (Q-Scout Robot)                      │
│                                                          │
│  UART0 RX (ISR) → RX_BUF[200]                           │
│    → Parser (firmware compilado)                         │
│    → Action dispatch (0x11 → Motor)                      │
│    → Motor.forward(speed)                                │
│    → Respuesta RB → UART0 TX                             │
└──────────────────────────────────────────────────────────┘
```

### BLE (Dongle USB)

```
┌──────────────────────────────────────────────────────────┐
│                    MyQode Electron                        │
│                                                          │
│  Protocol.mkSetRobotData(mac, rbPacket)                  │
│    → Construye paquete MK con header MK + MAC + rbData  │
│         ↓                                                │
│  SerialManage.write(dongle_port, mkPacket)               │
│    → Dongle USB transmite vía BLE NUS                    │
└──────────────────────────────────────────────────────────┘
         ↓ BLE (Nordic UART Service)
┌──────────────────────────────────────────────────────────┐
│               ESP32 (Q-Scout Robot)                      │
│                                                          │
│  ble.py: BLESimplePeripheral                             │
│    → _irq() → _IRQ_GATTS_WRITE                          │
│    → value = gatts_read(value_handle)                    │
│    → _write_callback(value)  ← datos RB                  │
│    → Parser (firmware compilado)                         │
│    → Action dispatch                                     │
│    → Respuesta → gatts_notify(conn_handle, 21, data)     │
└──────────────────────────────────────────────────────────┘
```

---

## 4. Transporte Utilizado

### USB/Serial

| Aspecto | Evidencia | Ubicación |
|---------|-----------|-----------|
| Librería | `serialport` v6.2.2 (Node.js) | `app.asar` → `require('serialport')` |
| Puerto | `/dev/ttyUSB0` (Linux), `COMx` (Windows) | Convención CH340 |
| Velocidad | 115200 baud | `se.open` → `"115200"` en app.asar |
| Formato | 8N1 | `RB_SERIAL_TASK.cpp:14-29` (AVR) |
| Envío | `port.write(buffer)` | `SerialManage.write()` |
| Recepción | ISR USART0_RX_vect (AVR) | `RB_SERIAL_TASK.cpp` — RX interrupt habilitado |
| Paquete | `[RB][size][orderId][action][payload][checksum]` | `Protocol.js` |

### BLE

| Aspecto | Evidencia | Ubicación |
|---------|-----------|-----------|
| UUID Servicio | `6E400001-B5A3-F393-E0A9-E50E24DCCA9E` | `ble.py:26` |
| TX | `6E400003-...` (Notify) | `ble.py:28` |
| RX | `6E400002-...` (Write/WriteNoResponse) | `ble.py:33` |
| Implementación ESP32 | `bluetooth.BLE()` + `gatts_register_services()` | `ble.py:71-83` |
| Envío ESP32 | `gatts_write(21, data)` / `gatts_notify(conn, 21, data)` | `ble.py:104,108` |
| Recepción ESP32 | `_IRQ_GATTS_WRITE` → `_write_callback(value)` | `ble.py:96-100` |
| Envoltura PC | RB envuelto en MK (dongle) | `Protocol.mkSetRobotData()` |

### HTTP/Socket Bridge

| Aspecto | Evidencia | Ubicación |
|---------|-----------|-----------|
| Dirección | `127.0.0.1:12345` | `qmind.py:7`, `qmind_socket.py:7` |
| HTTP | POST URL-encoded → `/set_motor_type`, `/get_ultrasonic`, etc. | `qmind.py:9-15` |
| Socket | TCP raw JSON → `{"event": "...", "data": {...}}` | `qmind_socket.py:6-10` |
| Función | API alternativa para control del robot | Clientes Python 2 |

---

## 5. Protocolo Localizado

### Implementación Principal

**Archivo:** `app.asar` → `./mycode/services/robot/Protocol.js` (module id 99)

### Funciones del Protocolo

| Función | Tipo | Acción | Descripción |
|---------|------|--------|-------------|
| `getHardware(orderId)` | GET | `0x01` | Consultar info del dispositivo |
| `getInterfaceInfo(orderId, port)` | GET | `0x02` | Consultar info de puerto |
| `getAllInterfaceInfo(orderId)` | GET | `0x03` | Consultar todos los puertos |
| `getMotorInterfaceInfo(orderId)` | GET | `0x04` | Consultar info de motores |
| `getUserInterfaceInfo(orderId)` | GET | `0x05` | Consultar puertos de usuario |
| `setLed(order, port, R, G, B)` | SET | `0x10` | Establecer color LED |
| `setMotor(order, port, speed)` | SET | `0x11` | Controlar motor individual |
| `setMove(order, m1, m2)` | SET | `0x11` | Controlar motores duales |
| `setUltrasonicLight(order, port, R, G, B)` | SET | `0x12` | LED sensor ultrasónico |
| `setBuzzer(order, port, rate, time)` | SET | `0x13` | Activar buzzer |
| `setMatrix(order, port, rows)` | SET | `0x14` | Display LED matrix |
| `setWorkMode(order, port, mode, value)` | SET | `0x18` | Modo de trabajo |
| `setSteeringEngine(order, port, engine, r1, r2)` | SET | `0x19` | Servo motor |
| `setExternalMotor(order, port, engine, s1, s2)` | SET | `0x1A` | Motor DC externo |
| `setRGBLedMatrix(order, port, rows)` | SET | `0x1B` | Matriz LED RGB |
| `setMp3(order, port, are, order, info)` | SET | `0x1C` | Control MP3 |
| `setFan(order, port, direction, speed)` | SET | `0x20` | Ventilador |
| `setExtRelay(order, port, status)` | SET | `0x21` | Relay externo |
| `setExtservoDegree(order, port, degree)` | SET | `0x22` | Servo externo |
| `getUltrasonicValue(order, port)` | GET | `0xA1` | Leer distancia |
| `getButtonInfo(order, port)` | GET | `0xA2` | Leer botón |
| `getVoltage(orderId, port)` | GET | `0xA3` | Leer batería |
| `getLinePatrolValue(order, port)` | GET | `0xA4` | Leer sensor línea |
| `getTemperatureHumidityValue(order, port)` | GET | `0xA5` | Leer temp+humedad |
| `getLightSensorValue(order, port)` | GET | `0xA6` | Leer sensor luz |
| `getVoiceSensorValue(order, port)` | GET | `0xA7` | Leer sensor sonido |
| `getinfraredValue(order, port)` | GET | `0xA8` | Leer PIR |
| `getGyroValue(order, type, port)` | GET | `0xA9` | Leer giroscopio |
| `getColorValue(order, port, type)` | GET | `0xAA` | Leer sensor color |
| `getTouchButtonValue(orderId, port)` | GET | `0xAB` | Leer botón táctil |
| `getTowtemperatureValue(order, port, type)` | GET | `0xAC` | Leer temp dual |
| `getSixLinePatrolValue(order, port)` | GET | `0xAD` | Leer línea 6ch |
| `getRockerValue(orderId, port)` | GET | `0xAE` | Leer joystick |
| `getFlameSensor(orderId, port)` | GET | `0xAF` | Leer llama |
| `getGasSensorValue(orderId, port)` | GET | `0xB0` | Leer gas |
| `getSpiralPotentiometer(orderId, port)` | GET | `0xB1` | Leer potenciómetro |
| `getLinePotentiometerSensor(orderId, port)` | GET | `0xB2` | Leer potenciómetro línea |
| `mkGetVersion(orderId)` | MK | `0x01` | Versión dongle |
| `mkSetRobotScanAction(orderId, act)` | MK | `0x02` | Escaneo BLE |
| `mkConnectRobot(orderId, mac)` | MK | `0x05` | Conectar BLE |
| `mkDisconnectRobot(orderId, mac)` | MK | `0x09` | Desconectar BLE |
| `mkSetRobotData(mac, rbPacket)` | MK | `0x06` | Enviar datos RB por BLE |

### Funciones de Parsing de Respuestas

| Función | Lee | Descripción |
|---------|-----|-------------|
| `parseHardware(buffer)` | bytes 4-6 | [action, hw_version, sw_version] |
| `parseVoltage(buffer)` | byte 5 | Nivel batería (0-100%) |
| `parseInterfaceInfo(buffer)` | bytes 4-13 | Info de puertos |
| `parseUltrasonicValue(buffer)` | bytes 5-6 | UInt16BE → distancia mm |
| `parseLightSensorValue(buffer)` | bytes 5-6 | UInt16BE → luz (0-1023) |
| `parseVoiceSensorValue(buffer)` | bytes 5-6 | UInt16BE → sonido |
| `parseinfraredValue(buffer)` | byte 5 | 0/1 (detectado) |
| `parseGyroValue(buffer)` | bytes 5-14 | XYZ con signo, /100 |
| `parseColorSensorValue(buffer)` | bytes 6-13 | R,G,B,C UInt16BE |
| `parseTemperatureValue(buffer)` | bytes 7-8 | entero.decimal °C |
| `parseHumidityValue(buffer)` | bytes 5-6 | entero.decimal %RH |
| `parseTemperatureValue2(buffer)` | bytes 5-7 | signo + UInt16BE/100 |
| `parseRockerValue(buffer)` | bytes 5-10 | X,Y con signo |
| `parseLinePatrolValue(buffer)` | byte 5 | 0=bright, 1=dark |
| `getTouchButtonInfo(buffer)` | bytes 5-6 | bitmask → array botones |
| `getSensorInfo(buffer)` | bytes 5-12 | Array de 8 bytes |

---

## 6. Archivos Importantes para Siguientes Fases

### Prioridad Crítica (implementación directa)

1. **`Protocol.js`** (app.asar, module 99) — Parser RB completo. **Ya extraído.**
2. **`QScout_RB_Protocol_Specification.md`** — Especificación completa del protocolo. **Ya generado.**
3. **`ble.py`** (k2x-python/) — BLE NUS para ESP32. **Ya analizado.**

### Prioridad Alta (referencia)

4. **`QM_QMINDX.h`** (k2x/) — Action codes Arduino. **Ya analizado.**
5. **`RB_SERIAL_TASK.cpp`** (uno/) — UART AVR register-level. **Ya analizado.**
6. **`QmindX.py`** (k2x-python/) — Driver hardware MicroPython. **Ya analizado.**
7. **`Port.py`** (k2x-python/) — Port detection, device codes. **Ya analizado.**
8. **`BDR612x.py`** (k2x-python/) — Motor driver. **Ya analizado.**

### Prioridad Media (complemento)

9. **`qmind.py`** — Bridge HTTP client. **Ya analizado.**
10. **`qmind_socket.py`** — Bridge Socket client. **Ya analizado.**
11. **`k2x.bin`** — Firmware compilado (requiere ingeniería inversa para más detalle).
12. **`RobotManage.js`** (app.asar) — Gestión de robots. **Ya extraído.**

---

## Respuestas a Preguntas de Cierre

### 1. ¿Qué tipo de aplicación es MyQode?

**Aplicación Electron** (desktop, Windows) con interfaz Scratch 3.0 para programación por bloques de robots. Usa `serialport` v6.2.2 para comunicación USB y dongle BLE para comunicación inalámbrica.

### 2. ¿Dónde está la lógica de comunicación?

En **`Protocol.js`** (app.asar, module 99). Contiene todas las funciones de construcción de paquetes RB/MK y parsing de respuestas. El envío se realiza desde `SerialManage.js` (module 69) vía `serialport.write()`.

### 3. ¿Cómo llega una orden desde MyQode hasta el robot?

```
Bloque Scratch → GsBlocks.blockCallBack()
  → Robot.setMotor() / Robot.setLed() / etc.
    → Protocol.setMotor() / Protocol.setLed() / etc.
      → Buffer con [RB][size][orderId][action][payload][checksum]
        → RobotItem.writeBuffer()
          → SerialManage.write(port, hex)
            → serialport.write(buffer)
              → USB-Serial → ESP32
```

### 4. ¿Qué módulos controlan UART y BLE?

- **UART:** `SerialManage.js` → `serialport` (Node.js) → USB-Serial
- **BLE:** `Protocol.mkSetRobotData()` → `SerialManage.js` → dongle USB → BLE NUS → ESP32 `ble.py`

### 5. ¿Dónde se encuentra el protocolo RB?

En **`app.asar` → `./mycode/services/robot/Protocol.js`** (module id 99). Contiene 40+ métodos de construcción y parsing. La especificación completa está en `QScout_RB_Protocol_Specification.md`.
