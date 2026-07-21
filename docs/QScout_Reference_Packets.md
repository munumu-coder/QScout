# QScout Reference Packets

**Fecha:** 2026-07-17  
**Fuente:** Validación experimental Fase 3B  
**Estado:** Paquetes reales capturados del robot

---

## 1. Paquetes de Petición (TX)

### GET_DEVICE_INFO (0x01)

```
Hex: 52420600019b
Bytes: [82, 66, 6, 0, 1, 155]
Length: 6
Order ID: 0
Action: 0x01
Checksum: 155
```

### GET_ULTRASONIC (0xA1) - Puerto 1

```
Hex: 52420701a1013e
Bytes: [82, 66, 7, 1, 161, 1, 62]
Length: 7
Order ID: 1
Action: 0xA1
Payload: [1] (port)
Checksum: 62
```

### GET_LINE_VALUE (0xA4) - Puerto 3

```
Hex: 52420702a4034c
Bytes: [82, 66, 7, 2, 164, 3, 76]
Length: 7
Order ID: 2
Action: 0xA4
Payload: [3] (port)
Checksum: 76
```

### SET_LED (0x10) - Puerto -4, Rojo

```
Hex: 52420a0210fcff0000ab
Bytes: [82, 66, 10, 2, 16, 252, 255, 0, 0, 171]
Length: 10
Order ID: 2
Action: 0x10
Payload: [252, 255, 0, 0] (port=-4, R=255, G=0, B=0)
Checksum: 171
```

### SET_LED (0x10) - Puerto -4, Verde

```
Hex: 52420a1210fc00ff00bb
Bytes: [82, 66, 10, 18, 16, 252, 0, 255, 0, 187]
Length: 10
Order ID: 18
Action: 0x10
Payload: [252, 0, 255, 0] (port=-4, R=0, G=255, B=0)
Checksum: 187
```

### SET_LED (0x10) - Puerto -4, Azul

```
Hex: 52420a1410fc0000ffbd
Bytes: [82, 66, 10, 20, 16, 252, 0, 0, 255, 189]
Length: 10
Order ID: 20
Action: 0x10
Payload: [252, 0, 0, 255] (port=-4, R=0, G=0, B=255)
Checksum: 189
```

### SET_LED (0x10) - Puerto -4, Apagado

```
Hex: 52420a1510fc000000bf
Bytes: [82, 66, 10, 21, 16, 252, 0, 0, 0, 191]
Length: 10
Order ID: 21
Action: 0x10
Payload: [252, 0, 0, 0] (port=-4, R=0, G=0, B=0)
Checksum: 191
```

### SET_BUZZER (0x13) - 440Hz, 500ms

```
Hex: 52420b1613fab801f40170
Bytes: [82, 66, 11, 22, 19, 250, 184, 1, 244, 1, 112]
Length: 11
Order ID: 22
Action: 0x13
Payload: [250, 184, 1, 244, 1] (port=-6, freq=440, dur=500)
Checksum: 112
```

### SET_MOVE (0x11) - Adelante, Velocidad 20

```
Hex: 5242091711001414ed
Bytes: [82, 66, 9, 23, 17, 0, 20, 20, 237]
Length: 9
Order ID: 23
Action: 0x11
Payload: [0, 20, 20] (reserved=0, m1=20, m2=20)
Checksum: 237
```

### SET_MOVE (0x11) - Atrás, Velocidad -20

```
Hex: 524209191100ecec9f
Bytes: [82, 66, 9, 25, 17, 0, 236, 236, 159]
Length: 9
Order ID: 25
Action: 0x11
Payload: [0, 236, 236] (reserved=0, m1=-20, m2=-20)
Checksum: 159
```

### SET_MOVE (0x11) - Parar

```
Hex: 5242091a11000000c8
Bytes: [82, 66, 9, 26, 17, 0, 0, 0, 200]
Length: 9
Order ID: 26
Action: 0x11
Payload: [0, 0, 0] (reserved=0, m1=0, m2=0)
Checksum: 200
```

---

## 2. Paquetes de Respuesta (RX)

### GET_DEVICE_INFO Response

```
Hex: 52420800030001a0
Bytes: [82, 66, 8, 0, 3, 0, 1, 160]
Length: 8
Order ID: 0
Action: 0x03 (NO coincide con petición 0x01)
Payload: [0, 1] (hw_version=0, sw_version=1)
Checksum: 160
```

### GET_ULTRASONIC Response

```
Hex: 524208010109c46b
Bytes: [82, 66, 8, 1, 1, 9, 196, 107]
Length: 8
Order ID: 1
Action: 0x01 (NO coincide con petición 0xA1)
Payload: [9, 196] (distance=2500mm)
Checksum: 107
```

### GET_LINE_VALUE Response

```
Hex: 524207020102a8
Bytes: [82, 66, 7, 2, 1, 2, 168]
Length: 7
Order ID: 2
Action: 0x01 (NO coincide con petición 0xA4)
Payload: [2] (line_value=2)
Checksum: 168
```

### SET_LED Response (Rojo)

```
Hex: 52420602019d
Bytes: [82, 66, 6, 2, 1, 157]
Length: 6
Order ID: 2
Action: 0x01 (NO coincide con petición 0x10)
Payload: [] (vacío)
Checksum: 157
```

### SET_LED Response (Verde)

```
Hex: 5242061201ad
Bytes: [82, 66, 6, 18, 1, 173]
Length: 6
Order ID: 18
Action: 0x01
Payload: [] (vacío)
Checksum: 173
```

### SET_LED Response (Azul)

```
Hex: 5242061401af
Bytes: [82, 66, 6, 20, 1, 175]
Length: 6
Order ID: 20
Action: 0x01
Payload: [] (vacío)
Checksum: 175
```

### SET_LED Response (Apagado)

```
Hex: 5242061501b0
Bytes: [82, 66, 6, 21, 1, 176]
Length: 6
Order ID: 21
Action: 0x01
Payload: [] (vacío)
Checksum: 176
```

---

## 3. Análisis de Checksums

### Verificación de Checksums

| Paquete | Checksum Recibido | Checksum Calculado | Válido |
|---------|-------------------|-------------------|--------|
| GET_DEVICE_INFO TX | 155 | 155 | ✅ |
| GET_DEVICE_INFO RX | 160 | 160 | ✅ |
| GET_ULTRASONIC TX | 62 | 62 | ✅ |
| GET_ULTRASONIC RX | 107 | 107 | ✅ |
| GET_LINE_VALUE TX | 76 | 76 | ✅ |
| GET_LINE_VALUE RX | 168 | 168 | ✅ |
| SET_LED TX (Rojo) | 171 | 171 | ✅ |
| SET_LED RX (Rojo) | 157 | 157 | ✅ |

### Fórmula de Verificación

```python
def verify_checksum(packet: bytes) -> bool:
    """Verificar checksum de un paquete RB."""
    if len(packet) < 6:
        return False
    return sum(packet[:-1]) % 256 == packet[-1]
```

---

## 4. Observaciones

### 4.1 Order ID

- El Order ID de la respuesta SIEMPRE coincide con el de la petición
- Esto confirma que la correlación se realiza por Order ID

### 4.2 Action Code

- El Action code de la respuesta NUNCA coincide con el de la petición
- Esto confirma que NO se debe utilizar Action para correlación

### 4.3 Payload

- Las respuestas SET no tienen payload (solo ACK)
- Las respuestas GET tienen payload con los datos del sensor

### 4.4 Checksum

- Todos los checksums son válidos
- La fórmula `sum(all_bytes) % 256` es correcta
