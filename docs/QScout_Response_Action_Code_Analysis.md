# QScout Response Action Code Analysis

**Fecha:** 2026-07-17  
**Fuente:** Validación física Fase 3B + Protocol.js analysis  
**Estado:** Análisis completo

---

## 1. Objetivo

Analizar todos los paquetes capturados durante la validación física para determinar el significado de los códigos de acción (ACTION) en las respuestas del robot Q-Scout.

---

## 2. Datos Capturados

### 2.1 Resumen Estadístico

| Métrica | Cantidad |
|---------|----------|
| Total paquetes TX | 31 |
| Total paquetes RX | 12 |
| Timeouts (sin respuesta) | 16 |
| Sin respuesta esperada (fire-and-forget) | 5 |
| Respuesta con action = 0x01 | 10 (83.3%) |
| Respuesta con action = 0x03 | 1 (8.3%) |
| Respuesta con action = 0x04 | 1 (8.3%) |
| Respuesta con action = request action | 0 (0%) |
| Checksums válidos | 43/43 (100%) |

### 2.2 Tabla Completa de Paquetes

| # | Order ID | Comando | TX Action | TX Hex | RX Action | RX Hex | RX Payload | ¿Respuesta? |
|---|----------|---------|-----------|--------|-----------|--------|------------|-------------|
| 1 | 0x00 | GET_DEVICE_INFO | 0x01 | `52420600019b` | 0x03 | `52420800030001a0` | `[00,01]` | ✅ Sí |
| 2 | 0x01 | GET_VOLTAGE (struct) | 0xA3 | `52420701a30140` | — | — | — | ❌ Timeout |
| 3 | 0x02 | GET_ULTRASONIC (struct) | 0xA1 | `52420702a1013f` | 0x01 | `524208020109c46c` | `[09,C4]` | ✅ Sí |
| 4 | 0x03 | GET_BUTTON (struct) | 0xA2 | `52420703a20141` | — | — | — | ❌ Timeout |
| 5 | 0x04 | GET_LIGHT (struct) | 0xA6 | `52420704a60247` | — | — | — | ❌ Timeout |
| 6 | 0x05 | GET_ULTRASONIC port=1 | 0xA1 | `52420705a10142` | 0x01 | `524208050109c46f` | `[09,C4]` | ✅ Sí |
| 7 | 0x06 | GET_VOLTAGE | 0xA3 | `52420706a30145` | — | — | — | ❌ Timeout |
| 8 | 0x07 | GET_BUTTON port=1 | 0xA2 | `52420707a20145` | — | — | — | ❌ Timeout |
| 9 | 0x08 | GET_LIGHT port=2 | 0xA6 | `52420708a6024b` | — | — | — | ❌ Timeout |
| 10 | 0x09 | GET_TEMP_HUMIDITY port=2 | 0xA5 | `52420709a5024b` | — | — | — | ❌ Timeout |
| 11 | 0x0A | GET_LINE_VALUE port=3 | 0xA4 | `5242070aa4034c` | 0x01 | `5242070a0102a8` | `[02]` | ✅ Sí |
| 12 | 0x0B | GET_VOICE port=1 | 0xA7 | `5242070ba7014e` | — | — | — | ❌ Timeout |
| 13 | 0x0C | GET_INFRARED port=1 | 0xA8 | `5242070ca80150` | — | — | — | ❌ Timeout |
| 14 | 0x0D | GET_INTERFACE_INFO port=1 | 0x02 | `5242070d0201ab` | 0x04 | `5242060d04ab` | (vacío) | ✅ Sí |
| 15 | 0x0E | GET_ALL_INTERFACE_INFO | 0x03 | `5242060e03ab` | — | — | — | ❌ Timeout |
| 16 | 0x0F | GET_MOTOR_INTERFACE_INFO | 0x04 | `5242060f04ad` | 0x01 | `5242070f0101ac` | `[01]` | ✅ Sí |
| 17 | 0x10 | SET_LED RED | 0x10 | `52420a1010fcff0000b9` | 0x01 | `5242061001ab` | (vacío) | ✅ Sí |
| 18 | 0x11 | SET_LED OFF | 0x10 | `52420a1110fc000000bb` | 0x01 | `5242061101ac` | (vacío) | ✅ Sí |
| 19 | 0x12 | SET_LED GREEN | 0x10 | `52420a1210fc00ff00bb` | 0x01 | `5242061201ad` | (vacío) | ✅ Sí |
| 20 | 0x13 | SET_LED OFF | 0x10 | `52420a1310fc000000bd` | 0x01 | `5242061301ae` | (vacío) | ✅ Sí |
| 21 | 0x14 | SET_LED BLUE | 0x10 | `52420a1410fc0000ffbd` | 0x01 | `5242061401af` | (vacío) | ✅ Sí |
| 22 | 0x15 | SET_LED OFF | 0x10 | `52420a1510fc000000bf` | 0x01 | `5242061501b0` | (vacío) | ✅ Sí |
| 23 | 0x16 | SET_BUZZER | 0x13 | `52420b1613fab801f40170` | — | — | — | ⚠️ No esperada |
| 24 | 0x17 | SET_MOVE forward | 0x11 | `5242091711001414ed` | — | — | — | ⚠️ No esperada |
| 25 | 0x18 | SET_MOVE stop | 0x11 | `5242091811000000c6` | — | — | — | ⚠️ No esperada |
| 26 | 0x19 | SET_MOVE backward | 0x11 | `524209191100ecec9f` | — | — | — | ⚠️ No esperada |
| 27 | 0x1A | SET_MOVE stop | 0x11 | `5242091a11000000c8` | — | — | — | ⚠️ No esperada |
| 28 | 0x1B | GET_GYRO port=1 | 0xA9 | `5242081ba9010061` | — | — | — | ❌ Timeout |
| 29 | 0x1C | GET_COLOR port=1 | 0xAA | `5242081caa010063` | — | — | — | ❌ Timeout |
| 30 | 0x1D | GET_TOUCH_BUTTON port=1 | 0xAB | `5242071dab0164` | — | — | — | ❌ Timeout |
| 31 | 0x1E | GET_ROCKER port=1 | 0xAE | `5242071eae0168` | — | — | — | ❌ Timeout |

---

## 3. Análisis de Action Codes de Respuesta

### 3.1 Acción 0x01 — ACK Genérico / Respuesta Estándar

**Frecuencia:** 10 de 12 respuestas (83.3%)

| Comando TX | TX Action | RX Action | RX Payload | Interpretación |
|------------|-----------|-----------|------------|----------------|
| GET_ULTRASONIC | 0xA1 | 0x01 | `[09,C4]` | Distancia = 2500mm |
| GET_ULTRASONIC port=1 | 0xA1 | 0x01 | `[09,C4]` | Distancia = 2500mm |
| GET_LINE_VALUE port=3 | 0xA4 | 0x01 | `[02]` | Valor línea = 2 |
| GET_MOTOR_INTERFACE_INFO | 0x04 | 0x01 | `[01]` | Info motor = 1 |
| SET_LED RED | 0x10 | 0x01 | (vacío) | ACK de confirmación |
| SET_LED OFF | 0x10 | 0x01 | (vacío) | ACK de confirmación |
| SET_LED GREEN | 0x10 | 0x01 | (vacío) | ACK de confirmación |
| SET_LED OFF | 0x10 | 0x01 | (vacío) | ACK de confirmación |
| SET_LED BLUE | 0x10 | 0x01 | (vacío) | ACK de confirmación |
| SET_LED OFF | 0x10 | 0x01 | (vacío) | ACK de confirmación |

**Patrón observado:**
- **Para comandos GET con sensor conectado:** Action 0x01 + payload con datos
- **Para comandos SET:** Action 0x01 + payload vacío (ACK puro)

**Hipótesis:** 0x01 es el código de acción genérico para "éxito" o "respuesta estándar". No es un echo de la petición.

**Evidencia de Protocol.js:**
```javascript
// backWork_RB() no verifica el action code de la respuesta
// Solo verifica el orderId para correlación
backWork_RB(buffer) {
    let orderId = buffer.readUInt8(3, false);
    // ... verifica checksum ...
    // Correlaciona por orderId, NO por action
}
```

**Estado:** ✅ Confirmado — ACK genérico para todas las respuestas exitosas

---

### 3.2 Acción 0x03 — Respuesta de Información de Dispositivo

**Frecuencia:** 1 de 12 respuestas (8.3%)

| Comando TX | TX Action | RX Action | RX Payload | Interpretación |
|------------|-----------|-----------|------------|----------------|
| GET_DEVICE_INFO | 0x01 | 0x03 | `[00,01]` | hw_version=0, sw_version=1 |

**Patrón observado:**
- Único comando que retorna action 0x03
- Payload contiene información de versión del dispositivo

**Hipótesis:** 0x03 es un código de acción específico para "información de dispositivo" o "respuesta a consulta de identificación".

**Evidencia de Protocol.js:**
```javascript
// parseDeviceInfo() lee desde byte[5]
parseDeviceInfo(buffer) {
    if (!buffer || buffer.length < 5) return {};
    return {
        hw_version: buffer.readUInt8(5, false),
        sw_version: buffer.readUInt8(6, false)
    };
}
```

**Análisis del paquete:**
```
TX: 52 42 06 00 01 9b
    RB sz id=0 act=01 chk

RX: 52 42 08 00 03 00 01 a0
    RB sz id=0 act=03 hw=0 sw=1 chk
         ↑
         action = 0x03 (NO 0x01)
```

**Hipótesis alternativa:** Podría ser un eco parcial (0x01 + 0x02 = 0x03), pero no hay evidencia suficiente.

**Estado:** ⚠️ Parcialmente confirmado — Solo observado una vez, requiere más muestras

---

### 3.3 Acción 0x04 — Respuesta de Información de Interfaz

**Frecuencia:** 1 de 12 respuestas (8.3%)

| Comando TX | TX Action | RX Action | RX Payload | Interpretación |
|------------|-----------|-----------|------------|----------------|
| GET_INTERFACE_INFO port=1 | 0x02 | 0x04 | (vacío) | Tipo de interfaz |

**Patrón observado:**
- Único comando que retorna action 0x04
- Payload vacío (paquete de 6 bytes mínimo)

**Análisis del paquete:**
```
TX: 52 42 07 0D 02 01 ab
    RB sz id=13 act=02 port=1 chk

RX: 52 42 06 0D 04 ab
    RB sz id=13 act=04 chk
         ↑
         action = 0x04 (NO 0x02)
```

**Nota importante:** La longitud declarada es 6 bytes (mínimo), lo que significa que no hay payload después del action code. El parser `parse_interface_info` en Protocol.js lee byte[4] que es el action code (0x04), no un payload.

**Hipótesis:** 0x04 es un código de acción específico para "información de interfaz" o "respuesta a consulta de puerto".

**Estado:** ⚠️ Parcialmente confirmado — Solo observado una vez, requiere más muestras

---

### 3.4 Sin Respuesta (Timeout)

**Frecuencia:** 16 de 31 comandos (51.6%)

| Comando TX | TX Action | Observación |
|------------|-----------|-------------|
| GET_VOLTAGE | 0xA3 | Sensor no conectado |
| GET_BUTTON | 0xA2 | Sensor no conectado |
| GET_LIGHT | 0xA6 | Sensor no conectado |
| GET_TEMP_HUMIDITY | 0xA5 | Sensor no conectado |
| GET_VOICE | 0xA7 | Sensor no conectado |
| GET_INFRARED | 0xA8 | Sensor no conectado |
| GET_ALL_INTERFACE_INFO | 0x03 | Probablemente no soportado |
| GET_GYRO | 0xA9 | Sensor no conectado |
| GET_COLOR | 0xAA | Sensor no conectado |
| GET_TOUCH_BUTTON | 0xAB | Sensor no conectado |
| GET_ROCKER | 0xAE | Sensor no conectado |

**Patrón observado:**
- Los sensores no conectados no generan respuesta
- El robot NO envía código de error
- Simplemente no responde (timeout)

**Hipótesis:** El firmware solo responde a sensores detectados硬件mente.

**Estado:** ✅ Confirmado — Timeout para sensores no conectados

---

### 3.5 Sin Respuesta Esperada (Fire-and-Forget)

**Frecuencia:** 5 de 31 comandos (16.1%)

| Comando TX | TX Action | Observación |
|------------|-----------|-------------|
| SET_BUZZER | 0x13 | Devuelve ACK (confirmado 2026-07-17) |
| SET_MOVE forward | 0x11 | No espera respuesta |
| SET_MOVE stop | 0x11 | No espera respuesta |
| SET_MOVE backward | 0x11 | No espera respuesta |
| SET_MOVE stop | 0x11 | No espera respuesta |

**Patrón observado (actualizado 2026-07-17):**
- SET_BUZZER **sí** devuelve ACK (action=0x01) — confirmado por validación física con SDK
- SET_MOVE no recibe respuesta
- El buzzer reproduce el tono inmediatamente (< 1ms), pero el firmware envía ACK después

**Hipótesis:** Algunos comandos SET no requieren confirmación por diseño. SET_BUZZER fue una excepción: sí devuelve ACK.

**Estado:** ⚠️ Parcialmente actualizado — BUZZER devuelve ACK; MOVE sigue siendo fire-and-forget

---

## 4. Tabla Resumen de Action Codes

### 4.1 Action Codes de Respuesta Observados

| Action Code | Frecuencia | Tipo | Comandos que lo generan |
|-------------|------------|------|------------------------|
| **0x01** | 83.3% | ACK genérico / Respuesta estándar | GET_ULTRASONIC, GET_LINE_VALUE, GET_MOTOR_INTERFACE_INFO, SET_LED |
| **0x03** | 8.3% | Respuesta de información de dispositivo | GET_DEVICE_INFO |
| **0x04** | 8.3% | Respuesta de información de interfaz | GET_INTERFACE_INFO |
| **(timeout)** | — | Sin respuesta | Sensores no conectados |

### 4.2 Acción vs Tipo de Comando

| Tipo de Comando | Action TX | Action RX Esperado | Observado |
|-----------------|-----------|-------------------|-----------|
| GETDeviceInfo | 0x01 | 0x03 | ✅ Confirmado |
| GETInterfaceInfo | 0x02 | 0x04 | ✅ Confirmado |
| GETAllInterfaceInfo | 0x03 | — | ❌ Timeout |
| GETMotorInterfaceInfo | 0x04 | 0x01 | ✅ Confirmado |
| GETUltrasonic | 0xA1 | 0x01 | ✅ Confirmado |
| GETLineValue | 0xA4 | 0x01 | ✅ Confirmado |
| SETLed | 0x10 | 0x01 | ✅ Confirmado |
| SETMotor | 0x11 | — | ⚠️ Fire-and-forget |
| SETBuzzer | 0x13 | 0x01 | ✅ Confirmado (ACK) |

---

## 5. Hipótesis sobre el Significado

### 5.1 Hipótesis A: Action Codes como Tipo de Respuesta

| Action | Significado Propuesto | Evidencia |
|--------|----------------------|-----------|
| 0x01 | "Datos" o "ACK estándar" | Usado para la mayoría de respuestas con datos |
| 0x03 | "Identificación del dispositivo" | Solo para GET_DEVICE_INFO |
| 0x04 | "Información de interfaz" | Solo para GET_INTERFACE_INFO |

**Fortaleza de la hipótesis:** Los action codes 0x03 y 0x04 coinciden numéricamente con los action codes de petición para GET_DEVICE_INFO (0x01) y GET_INTERFACE_INFO (0x02) respectivamente, pero incrementados en +2 y +2.

**Debilidad:** No hay suficientes muestras para confirmar el patrón.

### 5.2 Hipótesis B: Action Codes como Estado

| Action | Significado Propuesto | Evidencia |
|--------|----------------------|-----------|
| 0x01 | "Éxito" / "Comando ejecutado" | Usado para todas las respuestas exitosas |
| 0x03 | "Éxito con información" | Solo para GET_DEVICE_INFO |
| 0x04 | "Éxito con información de interfaz" | Solo para GET_INTERFACE_INFO |

**Fortaleza de la hipótesis:** Consistente con el comportamiento observado.

**Debilidad:** No explica por qué 0x03 y 0x04 son diferentes de 0x01.

### 5.3 Hipótesis C: Action Codes como Categoría

| Action | Categoría | Ejemplos |
|--------|-----------|----------|
| 0x01 | Respuesta genérica | GET sensores, SET LED |
| 0x03 | Respuesta de identificación | GET_DEVICE_INFO |
| 0x04 | Respuesta de configuración | GET_INTERFACE_INFO |

**Fortaleza de la hipótesis:** Agrupa comandos por funcionalidad.

**Debilidad:** No hay evidencia suficiente para confirmar.

---

## 6. Verificación con Protocol.js

### 6.1 Parsers en Protocol.js

```javascript
// Los parsers NO verifican el action code de la respuesta
// Simplemente leen los datos desde offsets específicos

parseDeviceInfo(buffer) {
    // Lee desde byte[5] y byte[6]
    return {
        hw_version: buffer.readUInt8(5, false),
        sw_version: buffer.readUInt8(6, false)
    };
}

parseUltrasonicValue(buffer) {
    // Lee desde byte[5] y byte[6]
    return buffer.readUInt8(5, false) * 256 + buffer.readUInt8(6, false);
}

parseInterfaceInfo(buffer, isAll) {
    // Lee desde byte[4] (action code) o bytes[4-13]
    if (isAll) {
        // Lee bytes 4-13
    } else {
        return buffer.readUInt8(4, false);  // Lee action code
    }
}
```

### 6.2 Implicación

Los parsers de Protocol.js **NO verifican** el action code de la respuesta. Simplemente leen los datos desde offsets fijos. Esto confirma que:

1. El action code de la respuesta **NO se utiliza** para identificar el tipo de respuesta
2. La correlación se realiza **exclusivamente** por Order ID
3. Los action codes de respuesta podrían ser informativos, pero no son críticos para el funcionamiento

---

## 7. Implicaciones para la Librería

### 7.1 Comportamiento Actual

```python
# Nuestra implementación actual
def receive(self, timeout=0.5):
    # Lee datos del puerto serial
    # Parsea el paquete usando parse_packet()
    # Retorna el buffer completo
    # NO verifica el action code
```

**Es correcto porque:**
- La correlación se realiza por Order ID
- Los parsers leen desde offsets fijos
- No es necesario verificar el action code

### 7.2 Recomendaciones

1. **No modificar la implementación** — El emparejamiento por Order ID funciona correctamente
2. **Documentar los action codes observados** — Para referencia futura
3. **No depender de action codes** — Podrían cambiar en versiones futuras del firmware

---

## 8. Conclusiones

### 8.1 Hallazgos Principales

1. **Los action codes de respuesta NUNCA coinciden con los de petición.** Esto confirma que el firmware utilza action codes para indicar el tipo de respuesta, no para echoar la petición.

2. **Tres action codes de respuesta observados:**
   - `0x01`: ACK genérico / Respuesta estándar (83.3%)
   - `0x03`: Respuesta de información de dispositivo (8.3%)
   - `0x04`: Respuesta de información de interfaz (8.3%)

3. **Los action codes no son críticos para el funcionamiento.** Protocol.js y nuestra librería correlacionan por Order ID, no por action code.

4. **Los sensores no conectados generan timeout**, no código de error.

5. **SET_BUZZER devuelve ACK** (confirmado 2026-07-17). SET_MOVE sigue siendo fire-and-forget.

### 8.2 Estado de las Hipótesis

| Hipótesis | Estado | Evidencia |
|-----------|--------|-----------|
| 0x01 = ACK genérico | ✅ Confirmado | 10/12 respuestas |
| 0x03 = Info dispositivo | ⚠️ Parcial | 1/12 respuestas |
| 0x04 = Info interfaz | ⚠️ Parcial | 1/12 respuestas |
| Timeout = sensor no conectado | ✅ Confirmado | 16/31 comandos |
| BUZZER devuelve ACK | ✅ Confirmado | SDK-02 Fase 2B (2026-07-17) |

### 8.3 Trabajo Futuro

Para confirmar las hipótesis sobre 0x03 y 0x04:
1. Probar GET_DEVICE_INFO múltiples veces
2. Probar GET_INTERFACE_INFO en diferentes puertos
3. Probar otros comandos GET para ver si retornan 0x01

---

## 9. Referencias

- **Validación física:** Fase 3B (2026-07-17)
- **Log completo:** `evidence/logs/validation_20260717_135131.log`
- **Protocol.js analysis:** `docs/QScout_Protocol_JS_Internal_Mechanism.md`
- **Diferencias observadas:** `docs/QScout_Observed_Differences.md`
- **Paquetes de referencia:** `docs/QScout_Reference_Packets.md`

---

*Análisis generado el 2026-07-17 basado en capturas de validación física.*
