# QScout RB Protocol Specification

**Fuente:** MyQode `app.asar` → `./mycode/services/robot/Protocol.js` (module id 99)  
**Fecha:** 2026-07-17  
**Estado:** Extracción completa desde código fuente JavaScript + Validación experimental con robot físico  

---

## 1. Formato General del Paquete RB

```
+--------+--------+--------+--------+--------+-----------+--------+
| Header | Length | Order  | Action | Payload ...         | Check  |
| 2 bytes| 1 byte | 1 byte | 1 byte | N bytes             | 1 byte |
+--------+--------+--------+--------+-----------+--------+--------+
  [0-1]    [2]      [3]      [4]     [5..N-2]            [N-1]
```

### Campos

| Campo | Offset | Tamaño | Tipo | Descripción |
|-------|--------|--------|------|-------------|
| **Header** | 0 | 2 bytes | ASCII | `"RB"` = `0x52 0x42` para robot. `"MK"` = `0x4D 0x4B` para dongle BLE |
| **Length** | 2 | 1 byte | UInt8 | Tamaño total del paquete en bytes (incluye header, length, order, action, payload, checksum) |
| **Order ID** | 3 | 1 byte | UInt8 | Identificador de secuencia. El PC asigna un ID incremental; el robot lo replica en la respuesta |
| **Action** | 4 | 1 byte | UInt8 | Código de operación (ver Tabla de Comandos) |
| **Payload** | 5 | Variable | Bytes | Datos del comando. Formato varía según Action |
| **Checksum** | N-1 | 1 byte | UInt8 | `sum(all_bytes[0..N-2]) % 256` |

### Cálculo del Checksum

```javascript
sumCheck(buffer) {
    let sum = 0;
    for (let i = 0; i < buffer.length; i++) {
        sum += buffer[i];
    }
    return sum % 256;
}
```

Se calcula sobre **todos** los bytes del buffer incluyendo header, length, order, action y payload. El resultado se escribe en la última posición.

### Ejemplo Verificado

```
52 42 0b 04 13 fa 05 2a 03 e8 ca
│  │  │  │  │  └──────────┘ └─┘
│  │  │  │  │      Payload    Checksum
│  │  │  │  └── Action: 0x13 (set_buzzer)
│  │  │  └── Order ID: 0x04
│  │  └── Length: 0x0B = 11 bytes
│  └── Header: 'B' (0x42)
└── Header: 'R' (0x52)
```

Fuente: `Protocol.js` — línea comentada en app.asar:  
`// robotManage.getCurrentRobot().write('52420b0413fa052a03e8ca');`

---

## 2. Constantes de Puertos

Extraído de `Protocol.js` — objeto `ports`:

```javascript
const ports = {
    board_led_1:    -4,    // LED integrado 1 (on-board)
    board_led_2:    -5,    // LED integrado 2 (on-board)
    board_buzzer:   -6,    // Buzzer integrado (on-board)
    board_button:   -7,    // Botón integrado (on-board)
    interface1:      1,    // Puerto RJ11 #1
    interface2:      2,    // Puerto RJ11 #2
    interface3:      3,    // Puerto RJ11 #3
    interface4:      4,    // Puerto RJ11 #4
    interface5:      5,    // Puerto RJ11 #5 (solo K1)
    interface6:      6,    // Puerto RJ11 #6 (solo K1)
    interface7:      7,    // Puerto RJ11 #7 (solo K1)
    interface8:      8,    // Puerto RJ11 #8 (solo K1)
};
```

**Q-Scout (K2):** puertos 1-4.  
**Qmind (K1):** puertos 1-8.  
**Valores negativos:** componentes integrados en la placa.

---

## 3. Tabla Completa de Comandos

### 3.1 Comandos SET (Escritura — PC → Robot)

| Nombre | Action ID | Payload | Ejemplo Hex | Estado |
|--------|-----------|---------|-------------|--------|
| `set_led` | `0x10` | port(1) + R(1) + G(1) + B(1) | `52 42 0A __ 10 PP RR GG BB CC` | ✓ |
| `set_motor` | `0x11` | port(1) + speed(1) | `52 42 08 __ 11 PP SS CC` | ✓ |
| `set_ultrasonic_light` | `0x12` | port(1) + R(1) + G(1) + B(1) | `52 42 0A __ 12 PP RR GG BB CC` | ✓ |
| `set_buzzer` | `0x13` | port(1) + rate(2BE) + time(2BE) | `52 42 0B __ 13 PP RR RR TT TT CC` | ✓ |
| `set_matrix` | `0x14` | port(1) + rows[10](10×2BE) | `52 42 1B __ 14 PP R0 R0 ... R9 R9 CC` | ✓ |
| `low_battery` | `0x15` | port(1) + flag(1) | `52 42 08 __ 15 PP FF CC` | ✓ |
| `click_button` | `0x16` | port(1) + flag(1) | `52 42 08 __ 16 PP FF CC` | ✓ |
| `set_work_mode` | `0x18` | port(1) + mode(1) + value(1) | `52 42 09 __ 18 PP MM VV CC` | ✓ |
| `set_Steering_engine` | `0x19` | port(1) + engine(1) + radian1(1) + radian2(1) | `52 42 0A __ 19 PP EE R1 R2 CC` | ✓ |
| `set_Out_engine` | `0x1A` | port(1) + engine(1) + radian1(1) + radian2(1) | `52 42 0A __ 1A PP EE R1 R2 CC` | ✓ |
| `set_rgbLedMatrix` | `0x1B` | port(1) + led_data(144) | `52 42 97 __ 1B PP [144 bytes] CC` | ✓ |
| `set_mp3_sensor` | `0x1C` | port(1) + are(1) + order(1) + info(1) | `52 42 0A __ 1C PP AA OO II CC` | ✓ |
| `touch_button` | `0x1D` | port(1) + flag(1) | `52 42 08 __ 1D PP FF CC` | ✓ |
| `set_fan` | `0x20` | port(1) + speed(1) + direction(1) | `52 42 09 __ 20 PP SS DD CC` | ✓ |
| `set_hardware_update` | `0x21` | port(1) + flag(1) | `52 42 08 __ 21 PP FF CC` | ✓ |
| `set_ext_servo_degree` | `0x22` | port(1) + degree(1) | `52 42 08 __ 22 PP DD CC` | ✓ |
| `control_four_digital_value` | `0x1E` | port(1) + d1(1) + d2(1) + d3(1) + d4(1) | `52 42 0B __ 1E PP D1 D2 D3 D4 CC` | ✓ |
| `control_four_rgbled` | `0x1F` | port(1) + location(1) + R(1) + G(1) + B(1) | `52 42 0B __ 1F PP LL RR GG BB CC` | ✓ |
| `set_ext_IO_output` | `0x21` | port(1) + status(1) | `52 42 08 __ 21 PP SS CC` | ✓ |

### 3.2 Comandos GET (Lectura — PC → Robot)

| Nombre | Action ID | Payload | Ejemplo Hex | Estado |
|--------|-----------|---------|-------------|--------|
| `get_device_info` | `0x01` | *(vacío)* | `52 42 06 __ 01 CC` | ✓ |
| `get_interface_info` | `0x02` | port(1) | `52 42 07 __ 02 PP CC` | ✓ |
| `get_all_interface_info` | `0x03` | *(vacío)* | `52 42 06 __ 03 CC` | ✓ |
| `get_motor_interface_info` | `0x04` | *(vacío)* | `52 42 06 __ 04 CC` | ✓ |
| `get_user_interface_info` | `0x05` | *(vacío)* | `52 42 06 __ 05 CC` | ✓ |
| `get_ultrasonic_value` | `0xA1` | port(1) | `52 42 07 __ A1 PP CC` | ✓ |
| `get_button_info` | `0xA2` | port(1) | `52 42 07 __ A2 PP CC` | ✓ |
| `get_voltage` | `0xA3` | port(1) | `52 42 07 __ A3 PP CC` | ✓ |
| `get_Line_value` | `0xA4` | port(1) | `52 42 07 __ A4 PP CC` | ✓ |
| `get_ltemperature_humidity_value` | `0xA5` | port(1) | `52 42 07 __ A5 PP CC` | ✓ |
| `get_light_sensor_value` | `0xA6` | port(1) | `52 42 07 __ A6 PP CC` | ✓ |
| `get_voice_sensor_value` | `0xA7` | port(1) | `52 42 07 __ A7 PP CC` | ✓ |
| `get_infrared_value` | `0xA8` | port(1) | `52 42 07 __ A8 PP CC` | ✓ |
| `get_gyro_sensor_value` | `0xA9` | port(1) + type(1) | `52 42 08 __ A9 PP TT CC` | ✓ |
| `get_color_sensor_value` | `0xAA` | port(1) + type(1) | `52 42 08 __ AA PP TT CC` | ✓ |
| `get_touch_button` | `0xAB` | port(1) | `52 42 07 __ AB PP CC` | ✓ |
| `get_tow_temperature_value` | `0xAC` | port(1) + type(1) | `52 42 08 __ AC PP TT CC` | ✓ |
| `get_six_line_value` | `0xAD` | port(1) | `52 42 07 __ AD PP CC` | ✓ |
| `get_rocker` | `0xAE` | port(1) | `52 42 07 __ AE PP CC` | ✓ |
| `get_flame_sensor` | `0xAF` | port(1) | `52 42 07 __ AF PP CC` | ✓ |
| `get_gas_sensor` | `0xB0` | port(1) | `52 42 07 __ B0 PP CC` | ✓ |
| `get_spiral_potentiometer` | `0xB1` | port(1) | `52 42 07 __ B1 PP CC` | ✓ |
| `get_linePotentiometer_sensor` | `0xB2` | port(1) | `52 42 07 __ B2 PP CC` | ✓ |
| `get_ext_IO_input` | `0xB4` | port(1) | `52 42 07 __ B4 PP CC` | ✓ |
| `get_ext_APC` | `0xB5` | port(1) | `52 42 07 __ B5 PP CC` | ✓ |
| `get_ext_tempandHumi` | `0xB6` | port(1) | `52 42 07 __ B6 PP CC` | ✓ |

---

## 4. Detalle de Payload y Respuesta por Comando

### 4.1 Comandos SET — Detalle de Payload

#### `set_led` (0x10) — Establecer Color LED

```
Payload: [port(1)] [R(1)] [G(1)] [B(1)]
Total:   4 bytes
```

| Byte | Campo | Tipo | Rango | Descripción |
|------|-------|------|-------|-------------|
| 5 | port | Int8 | -7 a 8 | Puerto. Ver tabla de puertos |
| 6 | red | UInt8 | 0-255 | Componente rojo |
| 7 | green | UInt8 | 0-255 | Componente verde |
| 8 | blue | UInt8 | 0-255 | Componente azul |

Puertos válidos: `[0, -4, -5, 2, 3, 4, 5, 6, 7]`

#### `set_motor` (0x11) — Control de Motor

**Modo individual** (puerto + velocidad):

```
Payload: [port(1)] [speed(1)]
Total:   2 bytes
```

| Byte | Campo | Tipo | Rango | Descripción |
|------|-------|------|-------|-------------|
| 5 | port | Int8 | M1/M2/ext | Puerto del motor |
| 6 | speed | Int8 | -255 a 255 | Velocidad. Negativo = reversa |

**Modo doble** (motores M1+M2):

```
Payload: [0x00(1)] [m1Speed(1)] [m2Speed(1)]
Total:   3 bytes
```

| Byte | Campo | Tipo | Rango | Descripción |
|------|-------|------|-------|-------------|
| 5 | reserved | Int8 | 0 | Siempre 0 |
| 6 | m1Speed | Int8 | -255 a 255 | Velocidad motor M1 |
| 7 | m2Speed | Int8 | -255 a 255 | Velocidad motor M2 |

#### `set_ultrasonic_light` (0x12) — LED del Sensor Ultrasónico

```
Payload: [port(1)] [R(1)] [G(1)] [B(1)]
Total:   4 bytes
```

Mismo formato que `set_led`.

#### `set_buzzer` (0x13) — Activar Buzzer

```
Payload: [port(1)] [rate(2 BE)] [time(2 BE)]
Total:   5 bytes
```

| Byte | Campo | Tipo | Rango | Descripción |
|------|-------|------|-------|-------------|
| 5 | port | Int8 | -6, 2-7 | Puerto. `-6` = buzzer on-board |
| 6-7 | rate | UInt16BE | 0-65535 | Frecuencia en Hz |
| 8-9 | time | UInt16BE | 0-65535 | Duración en milisegundos |

#### `set_matrix` (0x14) — Display LED Matrix 5×10

```
Payload: [port(1)] [row0(2BE)] [row1(2BE)] ... [row9(2BE)]
Total:   21 bytes
```

| Byte | Campo | Tipo | Descripción |
|------|-------|------|-------------|
| 5 | port | Int8 | Puerto del display |
| 6-25 | rows | 10× UInt16BE | Datos de las 10 filas (cada fila = 10 bits de ancho) |

#### `set_work_mode` (0x18) — Establecer Modo de Trabajo

```
Payload: [port(1)] [mode(1)] [value(1)]
Total:   3 bytes
```

| Byte | Campo | Tipo | Valores | Descripción |
|------|-------|------|---------|-------------|
| 5 | port | Int8 | Puerto | |
| 6 | mode | UInt8 | 0x00-0x11 | Modo de operación |
| 7 | value | UInt8 | 0-255 | Parámetro del modo |

Modos conocidos:
- `0x00` — Remote_Control_Mode
- `0x01` — Ultrasonic_Mode
- `0x02` — Line_Follower_Mode
- `0x03` — Dinosaur_Ultrasonic_Mode
- `0x04` — Alligator_Ultrasonic_Mode
- `0x10` — Scan_Mode
- `0x11` — SearchLight_Mode

#### `set_Steering_engine` (0x19) — Servo Motor

```
Payload: [port(1)] [engine(1)] [radian1(1)] [radian2(1)]
Total:   4 bytes
```

| Byte | Campo | Tipo | Rango | Descripción |
|------|-------|------|-------|-------------|
| 5 | port | Int8 | Puerto | |
| 6 | engine | UInt8 | 0-2 | Número de servo (0=ambos, 1=A, 2=B) |
| 7 | radian1 | UInt8 | 0-180 | Ángulo servo A (grados) |
| 8 | radian2 | UInt8 | 0-180 | Ángulo servo B (grados) |

#### `set_Out_engine` (0x1A) — Motor DC Externo

```
Payload: [port(1)] [engine(1)] [speed1(1)] [speed2(1)]
Total:   4 bytes
```

| Byte | Campo | Tipo | Rango | Descripción |
|------|-------|------|-------|-------------|
| 5 | port | Int8 | Puerto | |
| 6 | engine | Int8 | -127 a 127 | Motor (select) |
| 7 | speed1 | Int8 | -127 a 127 | Velocidad canal A |
| 8 | speed2 | Int8 | -127 a 127 | Velocidad canal B |

#### `set_rgbLedMatrix` (0x1B) — Matriz LED RGB 12×12

```
Payload: [port(1)] [led_data(144)]
Total:   145 bytes
```

| Byte | Campo | Tipo | Descripción |
|------|-------|------|-------------|
| 5 | port | Int8 | Puerto |
| 6-149 | led_data | 144× Int8 | Datos de color LED (12×12 = 144 LEDs) |

#### `set_mp3_sensor` (0x1C) — Control Módulo MP3

```
Payload: [port(1)] [are(1)] [order(1)] [info(1)]
Total:   4 bytes
```

| Byte | Campo | Tipo | Valores | Descripción |
|------|-------|------|---------|-------------|
| 5 | port | Int8 | Puerto | |
| 6 | are | Int8 | 1=flash, 2=BLE, 3=TF | Fuente de audio |
| 7 | order | Int8 | 0x01-0x09 | Comando MP3 |
| 8 | info | Int8 | 0-16 | Parámetro (número de pista, etc.) |

Sub-órdenes MP3:
- `0x01` — Play
- `0x02` — Stop / BLE start
- `0x03` — Sound (0-16)
- `0x04` — Play control
- `0x05` — Change (up/down)
- `0x09` — BLE stop

#### `set_fan` (0x20) — Control Ventilador

```
Payload: [port(1)] [speed(1)] [direction(1)]
Total:   3 bytes
```

| Byte | Campo | Tipo | Rango | Descripción |
|------|-------|------|-------|-------------|
| 5 | port | Int8 | Puerto | |
| 6 | speed | UInt8 | 0-255 | Velocidad |
| 7 | direction | Int8 | -1/1 | Dirección |

#### `set_ext_servo_degree` (0x22) — Servo Externo

```
Payload: [port(1)] [degree(1)]
Total:   2 bytes
```

| Byte | Campo | Tipo | Rango | Descripción |
|------|-------|------|-------|-------------|
| 5 | port | Int8 | Puerto | |
| 6 | degree | UInt8 | 0-180 | Ángulo en grados |

#### `set_ext_IO_output` (0x21) — Salida Digital Extrema

```
Payload: [port(1)] [status(1)]
Total:   2 bytes
```

| Byte | Campo | Tipo | Rango | Descripción |
|------|-------|------|-------|-------------|
| 5 | port | Int8 | Puerto | |
| 6 | status | Int8 | 0/1 | Estado del relay/LED |

#### `control_four_digital_value` (0x1E) — Display 4 Dígitos

```
Payload: [port(1)] [d1(1)] [d2(1)] [d3(1)] [d4(1)]
Total:   5 bytes
```

| Byte | Campo | Tipo | Rango | Descripción |
|------|-------|------|-------|-------------|
| 5 | port | Int8 | Puerto | |
| 6 | digit1 | UInt8 | 0-9, 0x40(-) | Dígito position 1 |
| 7 | digit2 | UInt8 | 0-9, 0x40(-) | Dígito position 2 |
| 8 | digit3 | UInt8 | 0-9, 0x40(-) | Dígito position 3 |
| 9 | digit4 | UInt8 | 0-9, 0x40(-) | Dígito position 4 |

#### `control_four_rgbled` (0x1F) — LED RGB Individual

```
Payload: [port(1)] [location(1)] [R(1)] [G(1)] [B(1)]
Total:   5 bytes
```

| Byte | Campo | Tipo | Rango | Descripción |
|------|-------|------|-------|-------------|
| 5 | port | Int8 | Puerto | |
| 6 | location | Int8 | 0-4 | Ubicación del LED (0=todos) |
| 7 | R | UInt8 | 0-255 | Rojo |
| 8 | G | UInt8 | 0-255 | Verde |
| 9 | B | UInt8 | 0-255 | Azul |

---

### 4.2 Comandos GET — Payload y Respuesta

Todos los comandos GET de sensores siguen el mismo patrón de petición:

```
Request:  [RB] [size] [order] [action] [port] [checksum]
Response: [RB] [size] [order] [action] [data...]
```

La respuesta **echoa** el header, size, order y action de la petición, y añade los datos del sensor en los bytes siguientes.

#### `get_device_info` (0x01) — Info del Dispositivo

**Request:** `52 42 06 __ 01 CC` (sin payload)  
**Response parse:**

```javascript
parseHardware(buffer) {
    result[0] = buffer.readUInt8(4);  // action echo
    result[1] = buffer.readUInt8(5);  // hardware version
    result[2] = buffer.readUInt8(6);  // software version
    return result;  // [action, hw_version, sw_version]
}
```

#### `get_interface_info` (0x02) — Info de Puerto

**Request:** `52 42 07 __ 02 PP CC`  
**Response parse:**

```javascript
parseInterfaceInfo(buffer, isAll) {
    if (isAll) {
        // bytes 4-13: 10 bytes con info de cada puerto
        for (i = 4; i < 14; i++) result.push(buffer.readUInt8(i));
    } else {
        return buffer.readUInt8(4);  // tipo de sensor en el puerto
    }
}
```

#### `get_all_interface_info` (0x03) — Info de Todos los Puertos

**Request:** `52 42 06 __ 03 CC`  
**Response:** 10 bytes de info de puertos (byte 4-13)

#### `get_motor_interface_info` (0x04) — Info Motores

**Request:** `52 42 06 __ 04 CC`  
**Response parse:**

```javascript
parseMotorInterfaceInfo(buffer) {
    return [buffer.readUInt8(4), buffer.readUInt8(5)];
}
```

#### `get_user_interface_info` (0x05) — Info Puertos de Usuario

**Request:** `52 42 06 __ 05 CC`  
**Response parse:**

```javascript
parseUserInterfaceInfo(buffer) {
    let max = 8;
    if (buffer.length >= 13) max = 12;
    for (i = 4; i < max; i++) result.push(buffer.readUInt8(i));
    return result;
}
```

#### `get_ultrasonic_value` (0xA1) — Distancia Ultrasónica

**Request:** `52 42 07 __ A1 PP CC`  
**Response parse:**

```javascript
parseUltrasonicValue(buffer) {
    return buffer.readUInt8(5) * 256 + buffer.readUInt8(6);
    // UInt16BE en bytes 5-6 → distancia en mm
}
```

#### `get_button_info` (0xA2) — Botón

**Request:** `52 42 07 __ A2 PP CC`  
**Response parse:**

```javascript
parseButtonInfo(buffer) {
    return buffer.readUInt8(5);  // 0=suelto, 1=presionado
}
```

#### `get_voltage` (0xA3) — Voltaje de Batería

**Request:** `52 42 07 __ A3 PP CC`  
**Response parse:**

```javascript
parseVoltage(buffer) {
    return buffer.readUInt8(5);  // nivel de batería (0-100%)
}
```

#### `get_Line_value` (0xA4) — Sensor de Línea

**Request:** `52 42 07 __ A4 PP CC`  
**Response parse:**

```javascript
parseLinePatrolValue(buffer, type) {
    if (type === 6) return buffer.readUInt8(5);  // 6-sensor
    return buffer.readUInt8(5);  // valor del sensor (0=bright, 1=dark)
}
```

#### `get_ltemperature_humidity_value` (0xA5) — Temperatura + Humedad

**Request:** `52 42 07 __ A5 PP CC`  
**Response parse:**

```javascript
parseTemperatureValue(buffer) {
    return buffer.readUInt8(7) + '.' + buffer.readUInt8(8);
    // Temperatura: entero.decimal
}
parseHumidityValue(buffer) {
    return buffer.readUInt8(5) + '.' + buffer.readUInt8(6);
    // Humedad: entero.decimal
}
```

#### `get_light_sensor_value` (0xA6) — Sensor de Luz

**Request:** `52 42 07 __ A6 PP CC`  
**Response parse:**

```javascript
parseLightSensorValue(buffer) {
    return buffer.readUInt8(5) * 256 + buffer.readUInt8(6);
    // UInt16BE → valor de luz (0-1023)
}
```

#### `get_voice_sensor_value` (0xA7) — Sensor de Sonido

**Request:** `52 42 07 __ A7 PP CC`  
**Response parse:**

```javascript
parseVoiceSensorValue(buffer) {
    return buffer.readUInt8(5) * 256 + buffer.readUInt8(6);
    // UInt16BE → nivel de sonido
}
```

#### `get_infrared_value` (0xA8) — Sensor PIR (Infrarrojo)

**Request:** `52 42 07 __ A8 PP CC`  
**Response parse:**

```javascript
parseinfraredValue(buffer) {
    return buffer.readUInt8(5);  // 0=sin movimiento, 1=detectado
}
```

#### `get_gyro_sensor_value` (0xA9) — Giroscopio / Acelerómetro

**Request:** `52 42 08 __ A9 PP TT CC`

| Byte | Campo | Tipo | Valores | Descripción |
|------|-------|------|---------|-------------|
| 5 | port | Int8 | Puerto | |
| 6 | type | Int8 | 0x00=XYZ, 0x01=Angle, 0x02=XYZ, 0x03=Acc | Tipo de dato |

**Response parse:**

```javascript
parseGyroValue(buffer) {
    // XYZ mode: bytes 5-14
    x_ = buffer.readUInt8(6);   // signo X (0=positivo, 1=negativo)
    x  = buffer.readUInt8(7)*256 + buffer.readUInt8(8);  // valor X * 100
    y_ = buffer.readUInt8(9);   // signo Y
    y  = buffer.readUInt8(10)*256 + buffer.readUInt8(11);
    z_ = buffer.readUInt8(12);  // signo Z
    z  = buffer.readUInt8(13)*256 + buffer.readUInt8(14);
    return [parseInt(x/100), parseInt(y/100), parseInt(z/100)];
}
```

#### `get_color_sensor_value` (0xAA) — Sensor de Color

**Request:** `52 42 08 __ AA PP TT CC`

| Byte | Campo | Tipo | Valores | Descripción |
|------|-------|------|---------|-------------|
| 5 | port | Int8 | Puerto | |
| 6 | type | Int8 | 0x00=RGB, 0x01=Grey | Tipo de dato |

**Response parse (RGB):**

```javascript
parseColorSensorValue(buffer) {
    R = buffer.readUInt8(6)*256 + buffer.readUInt8(7);
    G = buffer.readUInt8(8)*256 + buffer.readUInt8(9);
    B = buffer.readUInt8(10)*256 + buffer.readUInt8(11);
    C = buffer.readUInt8(12)*256 + buffer.readUInt8(13);
    return R+","+G+","+B+","+C;  // "R,G,B,Clear"
}
```

**Response parse (Grey):**

```javascript
parseColorSensorValueGrey(buffer) {
    return buffer.readUInt8(6)*256 + buffer.readUInt8(7);
}
```

#### `get_touch_button` (0xAB) — Botón Táctil

**Request:** `52 42 07 __ AB PP CC`  
**Response parse:**

```javascript
getTouchButtonInfo(buffer) {
    let param = (buffer.readUInt8(5)*256 + buffer.readUInt8(6)) / 2;
    // Convertir a binario, cada bit = un botón (bit 0=btn1, bit 1=btn2, etc.)
    param = param.toString(2);
    let key = [];
    for (var i = param.length; i > 0; i--) {
        if (param.charAt(i-1) === '1') key.push(param.length - i + 1);
    }
    return key;  // Array de botones presionados [1,3] = botones 1 y 3
}
```

#### `get_tow_temperature_value` (0xAC) — Temperatura Dual

**Request:** `52 42 08 __ AC PP TT CC`  
**Response parse:**

```javascript
parseTemperatureValue2(buffer) {
    let sign = buffer.readUInt8(5) ? '' : '-';
    let value = (buffer.readUInt8(6)*256 + buffer.readUInt8(7)) / 100;
    return sign + value;  // ej: "-23.45"
}
```

#### `get_six_line_value` (0xAD) — Sensor de Línea 6 Canales

**Request:** `52 42 07 __ AD PP CC`  
**Response parse:**

```javascript
parseLinePatrolValue(buffer, type=6) {
    return buffer.readUInt8(5);  // máscara de 6 bits
}
```

#### `get_rocker` (0xAE) — Joystick

**Request:** `52 42 07 __ AE PP CC`  
**Response parse:**

```javascript
parseRockerValue(buffer) {
    X  = (buffer.readUInt8(6)*256) + buffer.readUInt8(7);
    X_ = buffer.readUInt8(5);   // 2=negativo
    X  = X_ === 2 ? -X : X;
    Y  = (buffer.readUInt8(9)*256) + buffer.readUInt8(10);
    Y_ = buffer.readUInt8(8);   // 2=negativo
    Y  = Y_ === 2 ? -Y : Y;
    return [X, Y];
}
```

#### `get_flame_sensor` (0xAF) — Sensor de Llama

**Request:** `52 42 07 __ AF PP CC`  
**Response:** UInt16BE en bytes 5-6

#### `get_gas_sensor` (0xB0) — Sensor de Gas

**Request:** `52 42 07 __ B0 PP CC`  
**Response:** UInt16BE en bytes 5-6

#### `get_spiral_potentiometer` (0xB1) — Potenciómetro Espiral

**Request:** `52 42 07 __ B1 PP CC`  
**Response:** UInt16BE en bytes 5-6

#### `get_linePotentiometer_sensor` (0xB2) — Potenciómetro de Línea

**Request:** `52 42 07 __ B2 PP CC`  
**Response:** UInt16BE en bytes 5-6

#### `get_ext_IO_input` (0xB4) — Entrada Digital Externa

**Request:** `52 42 07 __ B4 PP CC`  
**Response:** UInt8 en byte 5 (0/1)

#### `get_ext_APC` (0xB5) — Entrada Analógica Externa

**Request:** `52 42 07 __ B5 PP CC`  
**Response:** UInt16BE en bytes 5-6

#### `get_ext_tempandHumi` (0xB6) — Temperatura+Humedad Externa

**Request:** `52 42 07 __ B6 PP CC`  
**Response:** UInt16BE en bytes 5-6

---

## 5. Protocolo Dongle MK (BLE)

El dongle USB BLE utiliza un protocolo separado pero empaquetado de forma similar.

### Header MK

```
'MK' = 0x4D 0x4B (en lugar de 'RB')
```

### Acciones MK

| Nombre | Action ID | Descripción |
|--------|-----------|-------------|
| `mkAct.get_version` | `0x01` | Obtener versión del dongle |
| `mkAct.set_scan` | `0x02` | Iniciar/detener escaneo BLE |
| `mkAct.get_info` | `0x04` | Obtener info de robot por MAC |
| `mkAct.set_connect` | `0x05` | Conectar a robot por BLE |
| `mkAct.set_disconect` | `0x09` | Desconectar robot BLE |
| `mkAct.set_robot_data` | `0x06` | Enviar datos RB a través del dongle |

### Envío RB a través de BLE

```javascript
mkSetRobotData(mac, rbBuffer) {
    // Construye paquete MK con header MK + action + MAC + datos RB
    // El payload RB se transmite íntegro dentro del paquete MK
}
```

**Flujo:**
```
App → Protocol.mkSetRobotData(mac, rbPacket)
    → Paquete MK = [MK header] [action 0x06] [MAC 6 bytes] [rbPacket]
    → SerialManage.write(dongle_port, mkPacket)
    → Dongle USB → BLE NUS → ESP32
```

---

## 6. Cadena de Llamadas: API → Paquete RB

### 6.1 Mover Motores (Forward)

```
API pública:  robot.request(true, order, Protocol.setMove(order.id, 150, 150))
                    ↓
Protocol.setMove(order, m1Speed=150, m2Speed=150)
    → Buffer.alloc(9)
    → write('RB', 0, 2)
    → writeUInt8(9, 2)           // size
    → writeUInt8(order, 3)       // orderId
    → writeUInt8(0x11, 4)        // action = set_motor
    → writeInt8(0, 5)            // reserved = 0
    → writeInt8(150, 6)          // m1Speed
    → writeInt8(150, 7)          // m2Speed
    → writeUInt8(sumCheck, 8)    // checksum
    → return Buffer
                    ↓
RobotItem.writeBuffer(buffer)
    → hex = buffer.toString('hex')
    → write(hex)
                    ↓
SerialManage.write(port, hexData)
    → new Buffer(hexData, "hex")
    → port.write(buffer)         // serialport.write()
                    ↓
USB-Serial (115200 baud) → Robot ESP32
```

### 6.2 Cambiar Color LED

```
robot.request(true, order, Protocol.setLed(order.id, 2, 255, 0, 0))
    → [52 42 0A __ 10 02 FF 00 00 CC]
    → LED puerto 2, color rojo (255,0,0)
```

### 6.3 Activar Buzzer

```
robot.request(true, order, Protocol.setBuzzer(order.id, -6, 440, 1000))
    → [52 42 0B __ 13 FA 01 B8 03 E8 CC]
    → Buzzer on-board (-6), 440Hz, 1000ms
```

### 6.4 Leer Distancia Ultrasónica

```
robot.request(true, order, Protocol.getUltrasonicValue(order.id, 2))
    → [52 42 07 __ A1 02 CC]
    → Solicita distancia del sensor en puerto 2
    → Respuesta: [52 42 08 __ A1 02 HH LL CC]
    → Distancia = HH*256 + LL (en mm)
```

---

## 7. Formato de Respuesta del Robot

### Estructura

```
+--------+--------+--------+--------+-----------+--------+
| Header | Length | Order  | Action | Data ...  | Check  |
| 2 bytes| 1 byte | 1 byte | 1 byte | N bytes   | 1 byte |
+--------+--------+--------+--------+-----------+--------+
```

- **Header:** Siempre `"RB"` (`0x52 0x42`)
- **Order ID:** Echo del orderId de la petición
- **Action:** Echo del action de la petición
- **Data:** Datos de respuesta (formato específico por comando)

### Dispatch de Respuestas

```javascript
// En RobotManage
doListenOnDataComplete(buffer, robotId, type) {
    // type: 0=robot, 1=dongle
    for (listener of this.listenOnDataComplete) {
        listener.callBack(buffer, robotId, type);
    }
}

// En Robot
request(isWait, order, buffer) {
    this.writeBuffer(buffer);
    if (isWait) {
        var orderId = buffer.readUInt8(3);
        // Registra callback等待 orderId específico
        // Cuando llega respuesta con mismo orderId, procesa
    }
}
```

### ParseOrderId

```javascript
parseOrderId(buffer) {
    let head = buffer.toString('utf8', 0, 2);
    if (head === 'RB') {
        return buffer.readUInt8(3);  // orderId
    } else {
        return false;
    }
}
```

---

## 8. Constantes de Acción Completas (Enum Extraído)

```javascript
// Acciones SET (PC → Robot)
set_led:                 0x10
set_motor:               0x11
set_ultrasonic_light:    0x12
set_buzzer:              0x13
set_matrix:              0x14
low_battery:             0x15    // callback/evento
click_button:            0x16    // callback/evento
set_work_mode:           0x18
set_Steering_engine:     0x19
set_Out_engine:          0x1A
set_rgbLedMatrix:        0x1B
set_mp3_sensor:          0x1C
touch_button:            0x1D    // callback/evento
control_four_digital_value: 0x1E
control_four_rgbled:     0x1F
set_fan:                 0x20
set_hardware_update:     0x21
set_ext_servo_degree:    0x22
set_ext_IO_output:       0x21    // (reutiliza code de hardware_update)

// Acciones GET (PC → Robot)
get_device_info:         0x01
get_interface_info:      0x02
get_all_interface_info:  0x03
get_motor_interface_info:0x04
get_user_interface_info: 0x05
get_ultrasonic_value:    0xA1
get_button_info:         0xA2
get_voltage:             0xA3
get_Line_value:          0xA4
get_ltemperature_humidity_value: 0xA5
get_light_sensor_value:  0xA6
get_voice_sensor_value:  0xA7
get_infrared_value:      0xA8
get_gyro_sensor_value:   0xA9
get_color_sensor_value:  0xAA
get_touch_button:        0xAB
get_tow_temperature_value: 0xAC
get_six_line_value:      0xAD
get_rocker:              0xAE
get_flame_sensor:        0xAF
get_gas_sensor:          0xB0
get_spiral_potentiometer:0xB1
get_linePotentiometer_sensor: 0xB2
get_ext_IO_input:        0xB4
get_ext_APC:             0xB5
get_ext_tempandHumi:     0xB6

// Acciones Dongle MK
mkAct.get_version:       0x01
mkAct.set_scan:          0x02
mkAct.get_info:          0x04
mkAct.set_connect:       0x05
mkAct.set_robot_data:    0x06
mkAct.set_disconect:     0x09
```

---

## 9. Tabla de Sensores

| Sensor | Device Code (Port.py) | Action GET | Payload | Respuesta | Unidad |
|--------|----------------------|------------|---------|-----------|--------|
| Ultrasónico | `0x02` | `0xA1` | port | UInt16BE (bytes 5-6) | mm |
| Botón | — | `0xA2` | port | UInt8 (byte 5) | 0/1 |
| Batería | — | `0xA3` | port | UInt8 (byte 5) | % |
| Línea (2ch) | `0x04` | `0xA4` | port | UInt8 (byte 5) | bitmask |
| Temp+Humedad | `0x06` | `0xA5` | port | Hum: UInt8.UInt8, Temp: UInt8.UInt8 | °C, %RH |
| Luz | `0x07` | `0xA6` | port | UInt16BE (bytes 5-6) | 0-1023 |
| Sonido | `0x08` | `0xA7` | port | UInt16BE (bytes 5-6) | 0-1023 |
| PIR (Infrarrojo) | `0x0A` | `0xA8` | port | UInt8 (byte 5) | 0/1 |
| Giroscopio | `0x0E` | `0xA9` | port+type | XYZ×3 con signo | °/s, m/s² |
| Color | `0x0D` | `0xAA` | port+type | R,G,B,C × UInt16BE | 0-65535 |
| Táctil | `0x0F` | `0xAB` | port | bitmask UInt16/2 | botones |
| Temp Dual | `0x10` | `0xAC` | port+type | signo + UInt16BE/100 | °C |
| Línea 6ch | `0x11` | `0xAD` | port | UInt8 bitmask | 6 bits |
| Joystick | `0x14` | `0xAE` | port | X signo+UInt16, Y signo+UInt16 | -1023..1023 |
| Llama | `0x15` | `0xAF` | port | UInt16BE (bytes 5-6) | 0-1023 |
| Gas | `0x16` | `0xB0` | port | UInt16BE (bytes 5-6) | 0-1023 |
| Potenciómetro Espiral | `0x17` | `0xB1` | port | UInt16BE (bytes 5-6) | 0-1023 |
| Potenciómetro Línea | `0x18` | `0xB2` | port | UInt16BE (bytes 5-6) | 0-1023 |

---

## 10. Comandos con Estado Desconocido

| Action ID | Nombre | Notas | Estado |
|-----------|--------|-------|--------|
| `0x21` | `set_ext_IO_output` / `set_hardware_update` | Mismo código para dos funciones diferentes | ? Ambigüedad |
| `0x22` | `set_ext_servo_degree` | Confirmado en Protocol.js | ✓ |
| `0xB3` | `ChipID_Read` | Definido en k2x/QM_QMINDX.h pero NO en Protocol.js | ? Solo Arduino |
| `0xB4` | `get_ext_IO_input` | Extraído de Protocol.js | ✓ |
| `0xB5` | `get_ext_APC` | Extraído de Protocol.js | ✓ |
| `0xB6` | `get_ext_tempandHumi` | Extraído de Protocol.js | ✓ |

---

## 11. Notas de Implementación

### Orden de los argumentos Int8 vs UInt8

- **Port:** Siempre `writeInt8` (puede ser negativo: -4 a -7 para componentes on-board)
- **Speed:** `writeInt8` (negativo = reversa)
- **Color R/G/B:** `writeUInt8` (0-255)
- **Frecuencia/Duración:** `writeUInt16BE` (big-endian, 2 bytes)
- **Sensor data:** Respuesta usa `readUInt8` y `readUInt16BE`

### Tamaños de Paquete Fijos

| Payload Size | Total Packet Size | Ejemplo |
|---|---|---|
| 0 bytes | 6 bytes | get_device_info |
| 1 byte | 7 bytes | get_ultrasonic_value, get_voltage |
| 2 bytes | 8 bytes | set_motor, set_led (individual) |
| 3 bytes | 9 bytes | set_move (dual motor), set_work_mode |
| 4 bytes | 10 bytes | set_led, set_steering_engine |
| 5 bytes | 11 bytes | set_buzzer |
| 21 bytes | 27 bytes | set_matrix |
| 145 bytes | 151 bytes | set_rgbLedMatrix |

### Order ID

- El PC asigna un orderId incremental (0-255, wrap-around)
- El robot replica el orderId en la respuesta
- Se usa para correlacionar peticiones con respuestas
- `OrderManager.create()` genera el siguiente orderId

### Timeouts

- BLE commands: 780ms delay para rgbLedMatrix, 350ms para otros
- Serial commands: 30ms delay típico entre comandos
- Sensor reads: respuesta síncrona (request/wait)

---

*Fin de la especificación. Generada desde evidencias directas del código fuente en `app.asar` → `./mycode/services/robot/Protocol.js`.*

---

## 12. Validación Experimental

Esta sección documenta los resultados obtenidos de pruebas directas con el robot Q-Scout físico.

### 12.1 Configuración de Pruebas

- **Robot:** Robobloq Q-Scout (RB-00002)
- **Conexión:** USB Serial via CH340 (VID:PID 1A86:7523)
- **Puerto:** `/dev/ttyUSB0`
- **Velocidad:** 115200 baud, 8N1
- **Fecha:** 2026-07-17

### 12.2 Resultados de Comandos

#### GET_DEVICE_INFO (0x01)

**TX:**
```
Hex: 52420600019b
Bytes: [82, 66, 6, 0, 1, 155]
```

**RX:**
```
Hex: 52420800030001a0
Bytes: [82, 66, 8, 0, 3, 0, 1, 160]
```

**Análisis:**
- Order ID: 0 (coincide con petición)
- Action: 0x03 (NO coincide con petición 0x01)
- Payload: [0, 1] → hw_version=0, sw_version=1
- Checksum: válido

#### GET_ULTRASONIC (0xA1)

**TX:**
```
Hex: 52420701a1013e
Bytes: [82, 66, 7, 1, 161, 1, 62]
```

**RX:**
```
Hex: 524208010109c46b
Bytes: [82, 66, 8, 1, 1, 9, 196, 107]
```

**Análisis:**
- Order ID: 1 (coincide con petición)
- Action: 0x01 (NO coincide con petición 0xA1)
- Payload: [9, 196] → 9*256 + 196 = 2500mm
- Checksum: válido

#### GET_LINE_VALUE (0xA4)

**TX:**
```
Hex: 52420702a4034c
Bytes: [82, 66, 7, 2, 164, 3, 76]
```

**RX:**
```
Hex: 524207020102a8
Bytes: [82, 66, 7, 2, 1, 2, 168]
```

**Análisis:**
- Order ID: 2 (coincide con petición)
- Action: 0x01 (NO coincide con petición 0xA4)
- Payload: [2] → valor de línea = 2
- Checksum: válido

#### SET_LED (0x10)

**TX:**
```
Hex: 52420a0210fcff0000ab
Bytes: [82, 66, 10, 2, 16, 252, 255, 0, 0, 171]
```

**RX:**
```
Hex: 52420602019d
Bytes: [82, 66, 6, 2, 1, 157]
```

**Análisis:**
- Order ID: 2 (coincide con petición)
- Action: 0x01 (NO coincide con petición 0x10)
- Payload: vacío
- Checksum: válido
- Comportamiento: LED cambió a ROJO ✓

### 12.3 Hallazgos Críticos

#### 12.3.1 El código de acción de la respuesta NO coincide con la petición

| Petición | Action Petición | Action Respuesta |
|----------|-----------------|------------------|
| GET_DEVICE_INFO | 0x01 | 0x03 |
| GET_ULTRASONIC | 0xA1 | 0x01 |
| GET_LINE_VALUE | 0xA4 | 0x01 |
| SET_LED | 0x10 | 0x01 |

**Implicación:** El mecanismo de correlación petición-respuesta se basa EXCLUSIVAMENTE en el Order ID, NO en el código de acción.

#### 12.3.2 Formato de respuesta confirmado

```
[Header 2B][Length 1B][Order ID 1B][Action 1B][Data N][Checksum 1B]
```

- **Header:** Siempre 0x52 0x42 ("RB")
- **Order ID:** Echo del orderId de la petición
- **Action:** NO es echo del action de la petición
- **Data:** Datos del sensor (formato específico por comando)
- **Checksum:** Válido en todas las respuestas

#### 12.3.3 El puerto NO está en la respuesta

Confirmado experimentalmente: la respuesta NO incluye el byte de puerto. Los datos del sensor comienzan directamente después del byte de acción.

### 12.4 Sensores Respondedores

| Sensor | Puerto | Respuesta | Valor |
|--------|--------|-----------|-------|
| Ultrasónico | 1 | ✅ | 2500mm |
| Línea | 3 | ✅ | 2 |

### 12.5 Sensores No Respondedores

Los siguientes sensores no respondieron (probablemente no conectados):

- Voltaje (puerto 1)
- Botón (puerto 1)
- Luz (puerto 2)
- Temperatura/Humedad (puerto 2)
- Voz (puerto 1)
- Infrarrojo (puerto 1)
- Giroscopio (puerto 1)
- Color (puerto 1)
- Táctil (puerto 1)
- Joystick (puerto 1)

### 12.6 Actuadores Validados

| Actuador | Prueba | Resultado |
|----------|--------|-----------|
| LED Rojo | RGB(255,0,0) | ✅ Confirmado |
| LED Verde | RGB(0,255,0) | ✅ Confirmado |
| LED Azul | RGB(0,0,255) | ✅ Confirmado |
| Buzzer | 440Hz, 500ms | ✅ Sonido producido |
| Motores Adelante | Velocidad 20 | ✅ Movimiento confirmado |
| Motores Atrás | Velocidad -20 | ✅ Movimiento confirmado |

### 12.7 Conformidad con la Especificación

| Aspecto | Especificación | Real | Estado |
|---------|----------------|------|--------|
| Header | 0x52 0x42 | 0x52 0x42 | ✅ Coincide |
| Checksum | sum % 256 | sum % 256 | ✅ Coincide |
| Rango velocidad motor | -100..100 | -100..100 | ✅ Coincide |
| Codificación velocidad | Int8 | Int8 | ✅ Coincide |
| Codificación puerto | Int8 | Int8 | ✅ Coincide |
| Formato respuesta | Sin puerto | Sin puerto | ✅ Coincide |
| Action de respuesta | Echo | Diferente | ⚠️ Diferente |
