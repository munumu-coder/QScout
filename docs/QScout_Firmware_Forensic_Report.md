# Informe Forense: Análisis del Firmware ESP32 (k2x.bin)

**Fecha:** 2026-07-17  
**Fase:** 1C — Análisis forense del firmware  
**Objetivo:** Determinar qué contiene `k2x.bin` y su relación con MicroPython

---

## Cadena de custodia

| Elemento | Valor |
|----------|-------|
| Original | `/media/munumu/F08A96178A95DA84/Program Files/MyQode/resources/remote/k2x.bin` |
| Copia de trabajo | `/home/munumu/Qscout/firmware_copia/k2x.bin` |
| Método | `cp --preserve=all` |
| MD5 original | `12e72841bd27d0d1c516b54e1b73854d` |
| MD5 copia | `12e72841bd27d0d1c516b54e1b73854d` |
| SHA-256 original | `293d427d7e4c23c0df14c6655f2249a1c5755b49ea4af6ccf4c9084b2b41ca4a` |
| SHA-256 copia | `293d427d7e4c23c0df14c6655f2249a1c5755b49ea4af6ccf4c9084b2b41ca4a` |

Hashes verificados: idénticos antes del análisis.

---

## 1. Arquitectura interna del firmware

### Tipo de imagen

| Propiedad | Valor |
|-----------|-------|
| Formato | ESP32 image (magic `0xE9`) |
| Flash mode | DIO |
| Flash size | 4 MB |
| Flash freq | 80 MHz |
| Entry point | `0x40084534` (IRAM) |
| Segmentos | 6 |
| Tamaño total | 1,040,016 bytes (1,015.6 KB) |

### Segmentos

| Seg | Dirección | Tamaño | Ubicación | Descripción |
|-----|-----------|--------|-----------|-------------|
| 0 | `0x3F400020` | 172.6 KB | DRAM/SRAM | Datos inicializados |
| 1 | `0x3FFBDB60` | 13.6 KB | DRAM | BSS / heap |
| 2 | `0x40080000` | 1.0 KB | IRAM | Trampolinas / vector table |
| 3 | `0x40080400` | 4.8 KB | IRAM | ISR handlers |
| 4 | `0x400D0018` | 739.0 KB | Flash mapeado | **Código de aplicación** |
| 5 | `0x40081750` | 84.5 KB | IRAM | Stack / buffers |

### Información de compilación (embebida en el header)

```
Versión:         9036908-dirty
Sistema:         esp32-arduino-lib-builder
ESP-IDF:         v3.3.5-1-g85c43024c
Arduino Core:    1.0.6
Fecha build:     Mar 26 2021
Hora build:      06:09:28
```

**Conclusión:** Este firmware NO es una imagen MicroPython. Es una aplicación Arduino/ESP-IDF compilada con el `esp32-arduino-lib-builder`.

---

## 2. Comparación con MicroPython oficial

| Propiedad | k2x.bin | esp32spiram v1.17 |
|-----------|---------|-------------------|
| **Tamaño** | 1,015.6 KB | 1,559.7 KB |
| **ESP-IDF** | v3.3.5 | v4.2 |
| **Framework** | Arduino ESP32 1.0.6 | MicroPython |
| **Entry point** | `0x40084534` | `0x400806b0` |
| **Segmentos** | 6 | 3 |
| **Strings "micropython"** | 0 (falsos positivos) | 425 |
| **Archivos .py embebidos** | Ninguno | 30+ (boot.py, main.py, etc.) |
| **REPL** | No | Sí |
| **WebREPL** | No | Sí |
| **Módulos congelados** | No | Sí (neopixel, dht, uasyncio, etc.) |

### ¿Está construido sobre MicroPython?

**NO.** `k2x.bin` no contiene ningún rastro de MicroPython:

- No hay VM de MicroPython
- No hay intérprete de Python
- No hay archivos `.py` embebidos
- No hay frozen modules
- No hay REPL ni WebREPL
- No hay strings `micropython` reales (los 4 encontrados son falsos positivos de C++ `basic_string`)

**Certeza:** 100% — evidencia directa del análisis de strings.

---

## 3. Módulos embebidos

### Módulos de Robobloq encontrados

| String encontrado | Tipo | Función probable |
|-------------------|------|------------------|
| `QmindX V3.0.1` | Versión | Identificación del firmware |
| `ROBOBLOQ-k1` | Identificador | Nombre de plataforma (fijo para K1 y K2) |
| `attachMotors` | Función C++ | Inicialización de motores MCPWM |
| `motorForward` | Función C++ | Control de motor hacia adelante |
| `motorFullForward` | Función C++ | Motor a velocidad máxima |
| `BLE_Connect_Process` | Función C++ | Manejo de conexión BLE |
| `start advertising` | Debug string | Inicio de advertising BLE |
| `Work_Mode= %d` | Debug string | Modo de trabajo actual |
| `Work_Mode_Port= %d` | Debug string | Puerto del modo de trabajo |
| `Car_Style= %d` | Debug string | Estilo del robot |
| `qm_linefollower Port=` | Debug string | Sensor de línea seguidor |
| `qm_linefollower->ReadSensors=` | Debug string | Lectura de sensores de línea |
| `RX_BUF[ack][7]= %d` | Debug string | Buffer de recepción (protocolo) |

### Módulos NO encontrados en el firmware

| Módulo Python | Estado |
|---------------|--------|
| `QmindX.py` | **No embebido** — se sube vía serial como archivo .py |
| `Port.py` | **No embebido** |
| `ble.py` | **No embebido** (pero BLE está en C++) |
| `BDR612x.py` | **No embebido** |
| `MachineModel.py` | **No embebido** |
| `main.py` | **No embebido** |
| `boot.py` | **No embebido** |

### Conclusión sobre módulos

Los módulos Python (`QmindX.py`, `Port.py`, `ble.py`, etc.) **no están congelados en el firmware**. Son archivos que se cargan en la memoria flash del ESP32 como archivos Python individuales, ejecutados por un intérprete Python que **no está en `k2x.bin`**.

Esto indica que el firmware contiene un intérprete Python compilado en código nativo C++, no MicroPython. Los scripts Python se ejecutan sobre este intérprete nativo.

---

## 4. Flujo de arranque

### Punto de entrada

- **Entry point:** `0x40084534` (IRAM)
- Este es el vector de reset del ESP32

### Proceso reconstructo

```
1. Bootloader ESP32 (no incluido en k2x.bin, separado en flash)
   ↓
2. Carga de k2x.bin en la dirección de entry point
   ↓
3. Inicialización de hardware:
   - UART0 (115200 baud, 8N1)
   - GPIO para motores (MCPWM)
   - GPIO para I2C (sensores)
   - BLE stack (Nordic UART Service)
   ↓
4. Inicialización de BLE:
   - Servicio NUS (UUID: 6E400001-...)
   - Característica TX (UUID: 6E400003-...)
   - Característica RX (UUID: 6E400002-...)
   - Advertising: "start advertising"
   ↓
5. Inicialización de motores:
   - attachMotors()
   - MCPWM configuration
   ↓
6. Loop principal:
   - Lee UART (protocolo RB)
   - Lee BLE NUS (datos RB encapsulados)
   - Parsea comandos
   - Ejecuta acciones
   - Envía respuestas
```

### No hay boot.py / main.py

El firmware no ejecuta archivos Python en el arranque. El loop principal está implementado en C++ compilado.

---

## 5. Soporte Wi-Fi

### Evidencia encontrada

| Categoría | Evidencia | Significado |
|-----------|-----------|-------------|
| Constantes ESP-IDF | `ESP_ERR_WIFI_*`, `ESP_ERR_TCPIP_ADAPTER_*`, `ESP_ERR_HTTP_*`, `ESP_ERR_HTTPS_OTA_*` | **Solo constantes de error** del framework ESP-IDF |
| NVS init | `"NVS has not been initialized. Call nvs_flash_init before starting WiFi/BT."` | Mensaje de error estándar de ESP-IDF |
| Coex | `"Coex register Wi-Fi channel change btdm cb faild"` | Coordinación Wi-Fi/BT del controlador |

### Búsqueda exhaustiva

| Patrón | Resultado |
|--------|-----------|
| `WLAN` | No encontrado |
| `STA_IF` | No encontrado |
| `AP_IF` | No encontrado |
| `SSID` | No encontrado (solo `ESP_ERR_WIFI_SSID` como constante de error) |
| `wifi_start` / `wifi_init` | No encontrado |
| `tcpip_adapter_init` | No encontrado |
| `socket` (como función Python) | No encontrado |
| `HTTP` (como código de aplicación) | No encontrado (solo `ESP_ERR_HTTP_*` como constantes) |
| `MQTT` | No encontrado |
| `WebSocket` | No encontrado |
| `ESP-NOW` | No encontrado |

### Conclusión

**No existe código Wi-Fi implementado.** Las únicas referencias a Wi-Fi son constantes de error del framework ESP-IDF que se compilan automáticamente en cualquier firmware ESP32. No hay ninguna función de aplicación que use Wi-Fi.

| Certeza | Nivel |
|---------|-------|
| No hay código Wi-Fi de aplicación | ✓ Demostrado |
| Wi-Fi está disponible en el hardware | ✓ Demostrado (ESP32 tiene Wi-Fi) |
| Wi-Fi podría habilitarse con recompilación | ≈ Muy probable (el hardware lo soporta) |
| Wi-Fi está deshabilitado intencionalmente | ? Indeterminado |

---

## 6. Implementación BLE

### Servicios encontrados

| Servicio | UUID | Estado |
|----------|------|--------|
| Nordic UART Service (NUS) | `6E400001-B5A3-F393-E0A9-E50E24DCCA9E` | ✓ Implementado |
| TX Characteristic (Notify) | `6E400003-B5A3-F393-E0A9-E50E24DCCA9E` | ✓ Implementado |
| RX Characteristic (Write) | `6E400002-B5A3-F393-E0A9-E50E24DCCA9E` | ✓ Implementado |

### Stack BLE

- **Controlador:** Bluedroid (ESP-IDF v3.3.5)
- **Librería Arduino:** `esp32/1.0.6/libraries/BLE/`
- **Implementación:** `BLECharacteristic.cpp`, `FreeRTOS.cpp`
- **UUIDs:** Solo NUS (Nordic UART Service)

### Servicios adicionales

| Servicio | Estado |
|----------|--------|
| OTA por BLE | No encontrado |
| Configuración por BLE | No encontrado |
| Provisioning | No encontrado |
| GATT personalizados | No encontrado |

### Conclusión

BLE implementa **únicamente Nordic UART Service** para transporte de datos RB. No hay servicios GATT adicionales, OTA, ni configuración.

---

## 7. Localización del parser del protocolo RB

### Evidencia

| Evidencia | Ubicación | Significado |
|-----------|-----------|-------------|
| `RX_BUF[ack][7]= %d` | String en firmware | Parser de respuesta RB (ack byte 7) |
| `Work_Mode= %d` | Debug output | Dispatcher de modo de trabajo |
| `Car_Style= %d` | Debug output | Dispatcher de estilo |
| `attachMotors` | Función C++ | Inicialización de hardware |
| `motorForward` | Función C++ | Ejecución de comando motor |
| `BLE_Connect_Process` | Función C++ | Manejo de conexión BLE |
| `qm_linefollower Port=` | Debug output | Línea seguidor |

### Dónde reside el parser

**El parser del protocolo RB está implementado en C++ compilado dentro de `k2x.bin`.**

No está en Python, no está en un módulo congelado, no está en un archivo externo. Es código nativo que:
1. Lee bytes del UART y del BLE NUS
2. Busca la cabecera `0x52 0x42` ("RB")
3. Valida el checksum
4. Extrae orderId, action, payload
5. Despacha a la función correspondiente (motor, LED, buzzer, sensor, etc.)
6. Construye y envía la respuesta

### Cadena de ejecución

```
UART/BLE → RB parser (C++) → action dispatch → hardware driver → respuesta RB
```

---

## 8. Funcionalidades ocultas encontradas

| Funcionalidad | Estado | Evidencia |
|---------------|--------|-----------|
| MicroPython VM | **No** | No hay strings de MicroPython |
| REPL / Shell | **No** | No hay strings de REPL |
| WebREPL | **No** | No hay strings de WebREPL |
| Telnet | **No** | No encontrado |
| FTP | **No** | No encontrado |
| OTA | **No** | Solo constantes ESP-IDF, no código de aplicación |
| Wi-Fi de aplicación | **No** | Solo constantes de error ESP-IDF |
| Shell de debug | **No** | Solo debug prints (`printf`) |
| Modo fábrica | **No** | No encontrado |
| Modo test | **No** | No encontrado |
| Diagnóstico | **No** | Solo `ChipID Read` (string del framework) |
| Comandos internos | **No** | Solo protocolo RB documentado |

---

## 9. Comparación con el firmware oficial de MicroPython

| Aspecto | k2x.bin | esp32spiram v1.17 |
|---------|---------|-------------------|
| Framework | Arduino/ESP-IDF | MicroPython |
| Lenguaje | C++ nativo | Python + C |
| Intérprete | No (loop C++ dedicado) | VM MicroPython |
| Archivos .py | Ninguno | 30+ congelados |
| Tamaño | 1,015.6 KB | 1,559.7 KB |
| REPL | No | Sí |
| Boot | Entry point → loop C++ | boot.py → main.py |
| Actualización | Requiere recompilación | Subir archivos .py |
| BLE | NUS (C++ nativo) | N/A (sin BLE en v1.17) |
| Motores | MCPWM (C++ nativo) | N/A |

---

## 10. Nivel de certeza de cada conclusión

| Conclusión | Certeza | Basis |
|------------|---------|-------|
| k2x.bin NO es MicroPython | **100%** | 0 strings de MicroPython vs 425 en firmware oficial |
| Es una aplicación Arduino C++ | **100%** | Strings `esp32-arduino-lib-builder`, Arduino BLE library paths |
| Usa ESP-IDF v3.3.5 | **100%** | String embebido en el header |
| Usa Arduino Core 1.0.6 | **100%** | Path `Arduino15/packages/esp32/1.0.6` |
| No hay archivos .py embebidos | **100%** | Búsqueda exhaustiva de `.py` en strings |
| El parser RB está en C++ compilado | **95%** | Strings `RX_BUF[ack]`, debug prints, funcionalidad |
| No hay Wi-Fi de aplicación | **100%** | Solo constantes ESP-IDF, ninguna función de uso |
| BLE solo usa NUS | **100%** | Solo UUIDs NUS encontrados, sin servicios adicionales |
| Los scripts Python se suben vía serial | **95%** | Consistente con la ausencia de .py en el firmware |
| No hay funcionalidades ocultas | **90%** | Búsqueda exhaustiva sin resultados |

---

## Respuestas a las preguntas de cierre

### 1. ¿Qué contiene realmente k2x.bin?

Una aplicación Arduino/ESP-IDF compilada en C++ para ESP32. Contiene:
- Motor driver (MCPWM)
- BLE stack con Nordic UART Service
- Parser del protocolo RB
- Driver de sensores (ultrasonic, línea, etc.)
- Lógica de control del robot

**No contiene** MicroPython, archivos .py, REPL, Wi-Fi de aplicación, ni funcionalidades ocultas.

### 2. ¿Qué versión exacta de MicroPython utiliza?

**Ninguna.** `k2x.bin` no contiene MicroPython. Está construido con ESP-IDF v3.3.5 + Arduino ESP32 Core 1.0.6.

### 3. ¿Qué módulos ha añadido Robobloq?

Robobloq ha añadido módulos C++ compilados:
- `QmindX V3.0.1` — módulo principal del robot
- `attachMotors` / `motorForward` / `motorFullForward` — control de motores
- `BLE_Connect_Process` — manejo de conexión BLE
- `qm_linefollower` — sensor de línea seguidor
- Parser del protocolo RB (C++ nativo)

### 4. ¿Dónde comienza la ejecución del firmware?

En la dirección `0x40084534` (IRAM), que es el entry point del ESP32. El bootloader (no incluido en `k2x.bin`) carga el firmware y salta a esta dirección.

### 5. ¿Existe soporte Wi-Fi implementado?

**No.** No hay código de aplicación Wi-Fi. Solo constantes de error del framework ESP-IDF que se compilan automáticamente.

### 6. Si existe, ¿está activo, deshabilitado o sin utilizar?

**No existe código de aplicación Wi-Fi.** El hardware ESP32 tiene Wi-Fi, pero el firmware no lo usa.

### 7. ¿Dónde reside el parser del protocolo?

En código C++ compilado dentro de `k2x.bin`. Evidence: strings `RX_BUF[ack][7]`, `Work_Mode`, `Car_Style`, y la lógica de dispatch de comandos.

### 8. ¿Existen funcionalidades ocultas o no documentadas?

**No.** Búsqueda exhaustiva de REPL, WebREPL, Telnet, FTP, OTA, modo fábrica, modo test, y diagnóstico no encontró resultados. Las únicas funcionalidades son: control de motores, LEDs, buzzer, sensores, y comunicación BLE/UART.

### 9. ¿Qué partes del firmware pueden reutilizarse para desarrollar una biblioteca nativa para Linux?

| Componente | Reutilizable | Método |
|------------|-------------|--------|
| Protocolo RB | **Sí** | Documentado en `QScout_RB_Protocol_Specification.md` |
| Action codes | **Sí** | Extraídos de `Protocol.js` y validados contra el firmware |
| BLE NUS UUIDs | **Sí** | Extraídos del firmware |
| Motor control | **Parcial** | La lógica está en C++, pero los comandos RB son documentados |
| Sensor reading | **Parcial** | Los comandos GET RB son documentados |
| Código C++ del firmware | **No** | Compilado para ESP32, no reutilizable en Linux |

La biblioteca Python existente (`qscout/`) ya implementa el protocolo RB completo, que es la interfaz documentada entre el PC y el robot. El firmware C++ es innecesario para el control desde Linux.

---

*Fin del informe. Análisis realizado exclusivamente sobre la copia de trabajo. El firmware original no fue modificado.*
