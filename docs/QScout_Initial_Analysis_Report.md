# QScout Initial Analysis Report

**Fecha:** 2026-07-16 (actualizado 2026-07-17)  
**Fase:** 1 — Análisis inicial  
**Robot:** Robobloq Q-Scout (RB-00002)

---

**Nota importante (2026-07-17):** Este informe fue generado antes del análisis forense del firmware. El firmware `k2x.bin` NO es MicroPython, sino una aplicación Arduino/ESP-IDF C++ compilada. Ver `QScout_Firmware_Forensic_Report.md` para detalles.

---

## 1. Arquitectura General

```
┌─────────────┐     USB/Serial      ┌──────────────┐
│   PC Linux  │ ◄─────────────────► │  Q-Scout     │
│  (Python)   │     115200 baud     │  ESP32       │
└─────────────┘                     │  (Arduino)   │
                                    └──────┬───────┘
                                           │ BLE NUS
                                    ┌──────┴───────┐
                                    │  App Móvil   │
                                    │  (Android)   │
                                    └──────────────┘
```

**Flujo de control:**
- **USB/Serial:** PC envía paquetes RB directamente al ESP32 vía puerto serie (`/dev/ttyUSB0`, CH340)
- **BLE:** App móvil se conecta vía Nordic UART Service (NUS) UUID `6E400001-B5A3-F393-E0A9-E50E24DCCA9E`
- **MyQode (Windows):** App Electron que usa `serialport` v6.2.2 para enviar paquetes RB por USB

---

## 2. Componentes Encontrados

### Hardware

| Componente | Evidencia | Ubicación |
|------------|-----------|-----------|
| ESP32 (con SPIRAM) | Firmware `esp32spiram-20210902-v1.17.bin` | `MyQode/resources/remote/` |
| CH340 USB-Serial | Driver incluido en MyQode | `MyQode/resources/drivers/` |
| Motor DC dual (L298N) | `BDR612x.py` — Motor class, pins 12/13/27/14/33 | `k2x-python/BDR612x.py` |
| Sensor ultrasónico | `QM_ULTRASONIC.h` en Arduino | `k2x/QM_ULTRASONIC.h` |
| Sensor de línea | `QM_LINEFOLLOWER.h` | `k2x/QM_LINEFOLLOWER.h` |
| Sensor de luz | `QM_LIGHTSENSOR.h` | `k2x/QM_LIGHTSENSOR.h` |
| Sensor de sonido | `QM_SOUNDSENSOR.h` | `k2x/QM_SOUNDSENSOR.h` |
| Sensor PIR | `QM_PIRSENSOR.h` | `k2x/QM_PIRSENSOR.h` |
| Temp+Humedad (DHT11) | `dht.DHT11(machine.Pin(18))` en QmindX.py | `k2x-python/QmindX.py:36` |
| Giroscopio (MPU6050/ICM42605) | `mpu6050.py`, `icm42605.py` | `k2x-python/` |
| Sensor de color (TCS34725) | `tcs34725.py` | `k2x-python/tcs34725.py` |
| LED NeoPixel (WS2812) | `neopixel.NeoPixel(machine.Pin(25), 2)` | `k2x-python/QmindX.py:33` |
| Display LED matrix | `BlueLEDMatrixPanel.py` (TM1680) | `k2x-python/BlueLEDMatrixPanel.py` |
| Display 4 dígitos | `FourDigitDisplay.py` (TM1650) | `k2x-python/FourDigitDisplay.py` |
| Buzzer piezo | `QM_BUZZER.h` | `k2x/QM_BUZZER.h` |
| Botón on-board | Pin 34 (`pin34 = machine.Pin(34, machine.Pin.IN)`) | `k2x-python/QmindX.py:30` |
| Puerto RJ11 ×4 (K2) | `Port.py` — 4 puertos con mux I2C (pins 23/22/21) | `k2x-python/Port.py:54-56` |
| Mux I2C 3-bit | SEL_I2C_A/B/C en pins 23/22/21 | `k2x-python/Port.py:54-56` |

### Variantes Hardware

| Variante | Modelo | Puertos RJ11 | MachineType | DeviceType |
|----------|--------|---------------|-------------|------------|
| K1 (Qmind) | `k1x` | 8 | 1 | 4 |
| K2 (Qmind Plus / Q-Scout) | `k2x` | 4 | 2 | 3 |

**Nuestro robot es K2 (Q-Scout).**

### Software

| Componente | Tecnología | Ubicación |
|------------|-----------|-----------|
| MyQode (desktop) | Electron + JavaScript | `MyQode/MyQode.exe` (64.5 MB) |
| Firmware ESP32 | Arduino/ESP-IDF C++ (NO MicroPython) | `k2x.bin` (1.04 MB) |
| Firmware AVR | Arduino C++ (compilado) | `k2.hex` (87 KB) |
| Drivers de sensores | MicroPython (subidos al robot) | `k2x-python/*.py` (15 archivos) |
| Drivers de sensores | Arduino C++ | `k2x/*.cpp,*.h` (65 archivos) |
| Bridge HTTP | Python 2 | `qmind.py` (271 líneas) |
| Bridge Socket | Python 2 | `qmind_socket.py` (185 líneas) |
| BLE Service | MicroPython (subido al robot) | `ble.py` (119 líneas) |
| Protocol parser | JavaScript (webpack) | `app.asar` → `Protocol.js` |

---

## 3. Firmware Localizado

| Archivo | Tamaño | Ubicación | Descripción |
|---------|--------|-----------|-------------|
| `k2x.bin` | 1,040,016 B | `resources/remote/` | Firmware Arduino/ESP-IDF para K2 (Q-Scout) |
| `k1x.bin` | 1,040,400 B | `resources/remote/` | Firmware Arduino/ESP-IDF para K1 (Qmind) |
| `esp32spiram-20210902-v1.17.bin` | 1,597,136 B | `resources/remote/` | MicroPython base ESP32 SPIRAM v1.17 (referencia) |
| `esp32-20220618-v1.19.1.bin` | 1,560,976 B | `resources/remote/` | MicroPython base ESP32 v1.19.1 (referencia) |
| `esp32-20210902-v1.17-k16.bin` | 1,527,504 B | `resources/remote/` | MicroPython base ESP32 v1.17 (k16) (referencia) |
| `k2.hex` | 87,514 B | `resources/remote/` | Firmware AVR compilado para K2 |
| `k1.hex` | 131,307 B | `resources/remote/` | Firmware AVR compilado para K1 |
| `k5.hex` | 70,504 B | `resources/remote/` | Firmware AVR compilado para K5 |
| `k6.hex` | 74,677 B | `resources/remote/` | Firmware AVR compilado para K6 |
| `QM_FactoryFirmware.ino.bootloader.bin` | 18,592 B | `resources/remote/` | Bootloader factory ESP32 |
| `QM_FactoryFirmware.ino.partitions.bin` | 3,072 B | `resources/remote/` | Tabla de particiones factory |
| `HZK12.bin` | 333,556 B | `resources/remote/` | Fuente de caracteres chinos |

---

## 4. Tecnologías Identificadas

| Tecnología | Uso | Archivos |
|------------|-----|----------|
| **Electron** | App de escritorio MyQode (Windows) | `MyQode.exe`, `app.asar` |
| **JavaScript (Node.js)** | Protocol parser, serial communication | `app.asar` → `Protocol.js`, `SerialManage.js` |
| **React/Redux** | UI de programación por bloques (Scratch 3.0) | `app.asar` |
| **MicroPython** | Firmware del ESP32, drivers de hardware | `k2x-python/*.py` |
| **Arduino C++** | Drivers de sensores (AVR), firmware compilado | `k2x/*.cpp,*.h`, `k2.hex` |
| **Python 2** | Bridge HTTP/Socket para control | `qmind.py`, `qmind_socket.py` |
| **serialport (npm)** | Comunicación serial USB desde Node.js | `app.asar` (v6.2.2) |
| **BLE NUS** | Comunicación inalámbrica | `ble.py`, app Android |
| **CH340** | Puente USB-Serial | Drivers en `resources/drivers/` |
| **CP2102** | Puente USB-Serial (dongle BLE) | Drivers en `resources/drivers/CP2102/` |

---

## 5. Comunicación Encontrada

### USB/Serial

| Aspecto | Evidencia | Ubicación |
|---------|-----------|-----------|
| Velocidad | 115200 baud | `RB_SERIAL_TASK.cpp:14-29` (AVR), app.asar `se.open` |
| Formato | 8N1 | `RB_SERIAL_TASK.cpp` (UCSZ01 + UCSZ00) |
| Puerto | `/dev/ttyUSB0` (Linux) | Convención CH340 |
| Paquete | `[RB][size][orderId][action][payload][checksum]` | `Protocol.js` en `app.asar` |
| Header | `0x52 0x42` ("RB") | `Protocol.js`: `this.head = ['RB', 'MK']` |
| Checksum | `sum(all_bytes) % 256` | `Protocol.js`: `sumCheck(buffer)` |

### BLE (Bluetooth Low Energy)

| Aspecto | Evidencia | Ubicación |
|---------|-----------|-----------|
| UUID Servicio | `6E400001-B5A3-F393-E0A9-E50E24DCCA9E` | `ble.py:26` |
| TX Characteristic | `6E400003-B5A3-F393-E0A9-E50E24DCCA9E` (Notify) | `ble.py:28` |
| RX Characteristic | `6E400002-B5A3-F393-E0A9-E50E24DCCA9E` (Write) | `ble.py:33` |
| Nombre | `RB-E4346E` (ejemplo) | App Android |
| Transporte | Nordic UART Service (NUS) | `ble.py` completo |
| Envoltura | RB envuelto en MK (dongle) | `Protocol.js`: `mkSetRobotData()` |

### HTTP/Socket (MyQode bridge)

| Aspecto | Evidencia | Ubicación |
|---------|-----------|-----------|
| Dirección | `127.0.0.1:12345` | `qmind.py:7`, `qmind_socket.py:7` |
| Protocolo HTTP | POST con URL-encoded data | `qmind.py:9-15` |
| Protocolo Socket | TCP raw con JSON | `qmind_socket.py:6-10` |
| Formato envío | `{"event": "...", "data": {...}}` (socket), `key=value` (HTTP) | `qmind_socket.py`, `qmind.py` |

---

## 6. Localización del Protocolo RB

### Ubicación principal

| Componente | Archivo | Estado |
|------------|---------|--------|
| **Parser completo** | `app.asar` → `./mycode/services/robot/Protocol.js` (module 99) | ✓ Extraído |
| **Action codes** | `k2x/QM_QMINDX.h:59-100` (Arduino) | ✓ Documentados |
| **Serial driver** | `uno/RB_SERIAL_TASK.cpp` (AVR register-level) | ✓ Analizado |
| **BLE service** | `k2x-python/ble.py` (MicroPython NUS) | ✓ Analizado |
| **Bridge HTTP** | `qmind.py` (Python 2 client) | ✓ Analizado |

### Action Codes Identificados

**SET (PC → Robot):** 0x10-0x22  
**GET (PC → Robot):** 0x01-0x05, 0xA1-0xB6  
**MK (Dongle):** 0x01-0x09  

### Documentación Generada

| Documento | Contenido |
|-----------|-----------|
| `QScout_RB_Protocol_Specification.md` | Especificación completa del protocolo (action codes, payloads, parsers) |
| `QScout_Protocol_Validation_Report.md` | Validación cruzada Arduino ↔ MyQode |

---

## 7. Próximos Pasos Recomendados

La Fase 1 está completada. Los análisis profundos ya se realizaron en sub-fases:

- **Fase 1B:** Verificación de arquitectura y protocolo ✓
- **Fase 1C:** Extracción completa del protocolo RB ✓
- **Fase 2:** Validación cruzada del protocolo ✓

**Documentos disponibles para Fase 3:**
1. `Informe Fase 1B` — Arquitectura completa del sistema
2. `QScout_RB_Protocol_Specification.md` — Especificación del protocolo (action codes, payloads, parsers)
3. `QScout_Protocol_Validation_Report.md` — Confirmación de compatibilidad

**La Fase 3 (implementación de la librería Python para Linux) puede iniciarse con la documentación existente.**
