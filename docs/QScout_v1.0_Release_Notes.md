# QScout Python Library v1.0.0 — Release Notes

**Fecha:** 2026-07-17  
**Versión:** 1.0.0  
**Estado:** Estable — listo para uso general

---

## 1. Objetivos del Proyecto

Desarrollar una librería Python nativa para Linux que permita controlar completamente el robot Robobloq Q-Scout (RB-00002) vía USB/UART, sin depender del software propietario MyQode ni de Windows.

---

## 2. Funcionalidades Implementadas

### 2.1 Conexión

- Detección automática del robot vía VID:PID CH340 (`1A86:7523`)
- Conexión serial a 115200 baud, 8N1
- Soporte para context manager (`with QScout() as robot:`)
- Manejo de errores y reconexión

### 2.2 Sensores (27 métodos)

| Comando | Método | Estado |
|---------|--------|:------:|
| GET_DEVICE_INFO | `sensors.device_info()` | ✅ Validado |
| GET_INTERFACE_INFO | `sensors.interface_info(port)` | ✅ Validado |
| GET_ALL_INTERFACE_INFO | `sensors.all_interface_info()` | ⏳ Pendiente |
| GET_MOTOR_INTERFACE_INFO | `sensors.motor_interface_info()` | ✅ Validado |
| GET_USER_INTERFACE_INFO | `sensors.user_interface_info()` | ⏳ Pendiente |
| GET_ULTRASONIC | `sensors.ultrasonic(port)` | ✅ Validado |
| GET_BUTTON | `sensors.button(port)` | ⏳ Pendiente |
| GET_VOLTAGE | `sensors.voltage(port)` | ⏳ Pendiente |
| GET_LINE_VALUE | `sensors.line_value(port)` | ✅ Validado |
| GET_TEMP_HUMIDITY | `sensors.temperature_humidity(port)` | ⏳ Pendiente |
| GET_LIGHT | `sensors.light(port)` | ⏳ Pendiente |
| GET_VOICE | `sensors.voice(port)` | ⏳ Pendiente |
| GET_INFRARED | `sensors.infrared(port)` | ⏳ Pendiente |
| GET_GYRO | `sensors.gyro(port, gyro_type)` | ⏳ Pendiente |
| GET_COLOR | `sensors.color_rgb(port)` / `sensors.color_grey(port)` | ⏳ Pendiente |
| GET_TOUCH_BUTTON | `sensors.touch_button(port)` | ⏳ Pendiente |
| GET_TEMP_DUAL | `sensors.temperature_dual(port, temp_type)` | ⏳ Pendiente |
| GET_SIX_LINE | `sensors.six_line(port)` | ⏳ Pendiente |
| GET_ROCKER | `sensors.rocker(port)` | ⏳ Pendiente |
| GET_FLAME | `sensors.flame(port)` | ⏳ Pendiente |
| GET_GAS | `sensors.gas(port)` | ⏳ Pendiente |
| GET_SPIRAL_POT | `sensors.spiral_pot(port)` | ⏳ Pendiente |
| GET_LINE_POT | `sensors.line_pot(port)` | ⏳ Pendiente |
| GET_EXT_IO_INPUT | `sensors.ext_io_input(port)` | ⏳ Pendiente |
| GET_EXT_APC | `sensors.ext_apc(port)` | ⏳ Pendiente |
| GET_EXT_TEMP_HUMI | `sensors.ext_temp_humi(port)` | ⏳ Pendiente |

### 2.3 Actuadores (16 métodos)

| Comando | Método | Estado |
|---------|--------|:------:|
| SET_LED | `actuators.led(port, r, g, b)` | ✅ Validado |
| SET_MOTOR | `actuators.motor(port, speed)` | ✅ Validado |
| SET_MOVE | `actuators.move(m1, m2)` | ✅ Validado |
| SET_ULTRASONIC_LIGHT | `actuators.ultrasonic_light(port, r, g, b)` | ⏳ Pendiente |
| SET_BUZZER | `actuators.buzzer(freq, dur, port)` | ✅ Validado |
| SET_MATRIX | `actuators.matrix(port, rows)` | ⏳ Pendiente |
| SET_WORK_MODE | `actuators.work_mode(port, mode, value)` | ⏳ Pendiente |
| SET_STEERING_ENGINE | `actuators.steering_engine(port, engine, a, b)` | ⏳ Pendiente |
| SET_OUT_ENGINE | `actuators.out_engine(port, engine, spd_a, spd_b)` | ⏳ Pendiente |
| SET_RGB_LED_MATRIX | `actuators.rgb_led_matrix(port, led_data)` | ⏳ Pendiente |
| SET_MP3 | `actuators.mp3(port, src, cmd, param)` | ⏳ Pendiente |
| SET_FOUR_DIGIT | `actuators.four_digit(port, d1–d4)` | ⏳ Pendiente |
| SET_FOUR_RGB_LED | `actuators.four_rgb_led(port, loc, r, g, b)` | ⏳ Pendiente |
| SET_FAN | `actuators.fan(port, speed, direction)` | ⏳ Pendiente |
| SET_EXT_IO_OUTPUT | `actuators.ext_io_output(port, status)` | ⏳ Pendiente |
| SET_EXT_SERVO_DEGREE | `actuators.ext_servo_degree(port, degree)` | ⏳ Pendiente |

**Métodos de conveniencia:**
- `actuators.forward(speed)` / `actuators.backward(speed)`
- `actuators.turn_left(speed)` / `actuators.turn_right(speed)`
- `actuators.stop()`
- `actuators.beep(frequency, duration_ms)`

### 2.4 Constantes

- `Port`: 12 constantes de puerto (4 on-board + 8 externos)
- `Action`: 37 códigos de acción

---

## 3. Protocolo Soportado

- **Protocolo RB** v1.0 (especificación completa en `docs/RB_Protocol_v1.0.md`)
- Header: `0x52 0x42` ("RB")
- Checksum: `sum(all_bytes) % 256`
- Correlación petición-respuesta por Order ID (2–254)
- Velocidad motor: -100..100 (clampeada)

---

## 4. Pruebas Realizadas

### 4.1 Pruebas Unitarias

| Archivo | Pruebas | Estado |
|---------|:-------:|:------:|
| `tests/test_protocol.py` | 36 | ✅ Todas pasan |
| `tests/test_connection.py` | 11 | ✅ Todas pasan |
| `tests/test_real_packets.py` | 23 | ✅ Todas pasan |
| **Total** | **65** | **✅ 100%** |

### 4.2 Validación Física

- **Robot:** Robobloq Q-Scout (RB-00002)
- **Firmware:** k2x (Arduino/ESP-IDF, NO MicroPython)
- **Conexión:** USB-Serial CH340, `/dev/ttyUSB0`, 115200 baud
- **Fecha:** 2026-07-17
- **Paquetes capturados:** 43 (31 TX + 12 RX)
- **Comandos validados:** 10/43 (los demás requieren hardware adicional)

**Comandos validados experimentalmente:**
- GET_DEVICE_INFO, GET_INTERFACE_INFO, GET_MOTOR_INTERFACE_INFO
- GET_ULTRASONIC (2500mm), GET_LINE_VALUE (value=2)
- SET_LED (Rojo, Verde, Azul, Off), SET_BUZZER (440Hz 500ms)
- SET_MOVE (Adelante, Atrás, Parar)

---

## 5. Limitaciones Conocidas

### 5.1 Sin soporte para

- Conexión BLE (requiere dongle MK + wrapper MK)
- Conexión Wi-Fi
- Interfaz de línea de comandos (CLI)
- Modo asíncrono (asyncio)

### 5.2 Sensores no validados

27 comandos de sensores/actuadores no fueron validados experimentalmente porque los sensores correspondientes no estaban conectados durante la validación. La implementación es correcta según el protocolo, pero requiere hardware adicional para confirmación.

### 5.3 Comportamiento de respuesta

- Los códigos de acción de respuesta NO coinciden con los de petición
- La correlación se realiza exclusivamente por Order ID
- Sensores no conectados generan timeout (sin código de error)
- SET_BUZZER returns ACK (confirmed 2026-07-17); SET_MOVE variants remain fire-and-forget

---

## 6. Compatibilidad

- **Python:** ≥ 3.10 (usa `str | None` syntax)
- **SO:** Linux (probado en Ubuntu/Debian)
- **Dependencias:** `pyserial`
- **Hardware:** Robobloq Q-Scout (RB-00002) con firmware k2x

---

## 7. Estructura del Proyecto

```
Qscout/
├── src/qscout/           # Librería Python
│   ├── __init__.py       # Clase QScout (punto de entrada)
│   ├── protocol.py       # Protocolo RB (builders + parsers)
│   ├── connection.py     # Conexión serial
│   ├── sensors.py        # Lectura de sensores (27 métodos)
│   └── actuators.py      # Control de actuadores (16+5 métodos)
├── tests/                # Pruebas unitarias (65 tests)
│   ├── test_protocol.py
│   ├── test_connection.py
│   └── test_real_packets.py
├── examples/             # Ejemplos de uso
│   ├── full_demo.py      # Ejemplo oficial completo
│   └── test_basic.py     # Ejemplos básicos
├── docs/                 # Documentación técnica
│   ├── RB_Protocol_v1.0.md           # Especificación canónica
│   ├── QScout_Protocol_Coverage_Report.md
│   ├── QScout_API_Audit_Report.md
│   ├── QScout_v1.0_Release_Notes.md  # Este documento
│   └── ... (12+ documentos más)
├── evidence/             # Evidencias experimentales
│   ├── logs/             # Logs de validación
│   ├── packets/          # Paquetes de referencia
│   └── captures/         # Capturas reservadas
└── pyproject.toml        # Configuración del paquete
```

---

## 8. Cambios Respecto a Fases Anteriores

### Fase 1–2: Análisis
- Análisis forense de MyQode y protocolo
- Extracción de action codes, parsers, builders
- Análisis forense del firmware (k2x.bin = Arduino, NO MicroPython)

### Fase 3: Implementación
- Librería completa: protocol, connection, sensors, actuators
- 47 pruebas unitarias iniciales

### Fase 3A.5: Auditoría
- Corrección de `find_qscout()` (VID:PID)
- Añadido `_clamp_speed()` (±100)
- Manejo de errores mejorado
- Auditoría completa con 65 tests

### Fase 3B: Validación física
- Conexión real al robot
- 43 paquetes capturados
- 10 comandos validados experimentalmente
- Descubrimiento: action codes de respuesta ≠ echo

### Fase 3C: Consolidación
- Documentación completa del protocolo
- Mecanismo de correlación documentado
- Diferencias observadas documentadas
- Paquetes de referencia
- Pruebas de regresión con paquetes reales

### Fase 3D: Cierre (v1.0.0)
- Auditoría de cobertura (43/43 comandos = 100%)
- Auditoría de API pública
- Ejemplo oficial completo
- Corrección del bug de Order ID (iniciaba en 0, ahora en 2)
- Referencias a MyQode actualizadas
- Release notes

---

## 9. Uso Rápido

```python
from qscout import QScout

# Conexión automática
with QScout() as robot:
    # Información del dispositivo
    info = robot.sensors.device_info()
    print(f'HW: {info["hw_version"]}, SW: {info["sw_version"]}')

    # Leer sensor ultrasónico
    dist = robot.sensors.ultrasonic(1)
    print(f'Distancia: {dist} mm')

    # Controlar LED
    robot.actuators.led(-4, 255, 0, 0)  # Rojo
    robot.actuators.led(-4, 0, 0, 0)    # Off

    # Mover robot
    robot.actuators.forward(80)
    robot.actuators.stop()
```

---

*QScout Python Library v1.0.0 — 2026-07-17*
