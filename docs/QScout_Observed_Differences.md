# QScout Observed Differences

**Fecha:** 2026-07-17  
**Estado:** Documentado experimentalmente

---

## 1. Resumen

Este documento documenta las diferencias observadas entre el comportamiento esperado (según la especificación del protocolo) y el comportamiento real del robot Q-Scout.

---

## 2. Diferencias Críticas

### 2.1 Código de Acción de la Respuesta

**Comportamiento Esperado:**
La respuesta debería "ecoar" el código de acción de la petición.

**Comportamiento Real:**
El código de acción de la respuesta NO coincide con el de la petición.

| Petición | Action Esperada | Action Real | Diferencia |
|----------|-----------------|-------------|------------|
| GET_DEVICE_INFO (0x01) | 0x01 | 0x03 | +2 |
| GET_ULTRASONIC (0xA1) | 0xA1 | 0x01 | -0xA0 |
| GET_LINE_VALUE (0xA4) | 0xA4 | 0x01 | -0xA3 |
| SET_LED (0x10) | 0x10 | 0x01 | -0x0F |

**Evidencia:**
```
TX: 52420600019b  (GET_DEVICE_INFO, action=0x01)
RX: 52420800030001a0  (action=0x03, NO 0x01)

TX: 52420701a1013e  (GET_ULTRASONIC, action=0xA1)
RX: 524208010109c46b  (action=0x01, NO 0xA1)
```

**Hipótesis:**
El firmware del robot utilza el código de acción de la respuesta para indicar el tipo de respuesta, no para echoar la petición. Los valores 0x01 y 0x03 podrían ser códigos de estado.

**Estado:** ✅ Confirmado experimentalmente

---

### 2.2 ACK Genéricos

**Comportamiento Esperado:**
Cada comando tendría una respuesta específica con el mismo código de acción.

**Comportamiento Real:**
Los comandos SET parecen recibir un ACK genérico con acción 0x01.

**Evidencia:**
```
TX: 52420a0210fcff0000ab  (SET_LED, action=0x10)
RX: 52420602019d  (action=0x01, payload vacío)
```

**Hipótesis:**
El firmware envía un ACK genérico (acción 0x01) para todos los comandos SET exitosos.

**Estado:** ✅ Confirmado para SET_LED

---

### 2.3 Respuestas con Acción 0x03

**Comportamiento Esperado:**
Todas las respuestas deberían tener acción 0x01 (ACK).

**Comportamiento Real:**
GET_DEVICE_INFO retorna acción 0x03.

**Evidencia:**
```
TX: 52420600019b  (GET_DEVICE_INFO, action=0x01)
RX: 52420800030001a0  (action=0x03)
```

**Hipótesis:**
El código 0x03 podría indicar "información de dispositivo" o "respuesta a consulta de información".

**Estado:** ⚠️ Requiere más investigación

---

## 3. Diferencias Menores

### 3.1 Auto-Detection

**Comportamiento Esperado:**
`find_qscout()` debería detectar el robot por descripción "CH340".

**Comportamiento Real:**
La descripción del puerto es "USB Serial", no "CH340".

**Evidencia:**
```python
>>> Connection.list_ports()
['/dev/ttyS31', ..., '/dev/ttyUSB0']

>>> for p in serial.tools.list_ports.comports():
...     if 'USB' in p.device:
...         print(p.description)
USB Serial
```

**Hipótesis:**
El driver CH340 en Linux puede reportar una descripción diferente.

**Estado:** ✅ Confirmado, requiere corrección

---

### 3.2 Longitud de Respuesta

**Comportamiento Esperado:**
La longitud indicada en el byte 2 debería coincidir con la longitud real del paquete.

**Comportamiento Real:**
Coincide correctamente.

**Evidencia:**
```
RX: 52420800030001a0
     ↑
     Length = 8
     Longitud real = 8 bytes ✓
```

**Estado:** ✅ Confirmado correcto

---

### 3.3 Checksum

**Comportamiento Esperado:**
El checksum debería ser `sum(all_bytes) % 256`.

**Comportamiento Real:**
El checksum es correcto en todas las respuestas.

**Evidencia:**
```
RX: 524208010109c46b
Checksum recibido: 0x6B = 107
Checksum calculado: (0x52+0x42+0x08+0x01+0x01+0x09+0xC4) % 256 = 107 ✓
```

**Estado:** ✅ Confirmado correcto

---

## 4. Comportamientos No Confirmados

### 4.1 Significado de los Códigos de Acción de Respuesta

**Pregunta:** ¿Qué significan los códigos 0x01 y 0x03 en las respuestas?

**Hipótesis:**
- 0x01: ACK genérico / respuesta estándar
- 0x03: Respuesta de información de dispositivo

**Estado:** ⚠️ No confirmado

### 4.2 Comportamiento con Sensores No Conectados

**Pregunta:** ¿Qué respuesta envía el robot cuando un sensor no está conectado?

**Observación:** No se recibe respuesta (timeout).

**Hipótesis:** El robot no envía respuesta si el sensor no está detectado.

**Estado:** ⚠️ No confirmado (requiere sensor desconectado)

### 4.3 Auto-Reports

**Pregunta:** ¿Envía el robot auto-reports con Order ID = 0?

**Observación:** No se observaron auto-reports durante las pruebas.

**Hipótesis:** Los auto-reports podrían enviarse en ciertas condiciones (ej: cambio de estado de sensor).

**Estado:** ⚠️ No confirmado

---

## 5. Diferencias con Implementación Convencional

### 5.1 Protocolo Convencional vs. Real

| Aspecto | Convencional | Real (Q-Scout) |
|---------|--------------|----------------|
| Echo de Action | Sí | No |
| Correlación por Order ID | Sí | Sí |
| ACK genérico | No | Sí (acción 0x01) |
| Auto-reports | No | Posible |

### 5.2 Implicaciones para la Librería

1. **No verificar Action en respuestas:** La librería NO debe utilizar el código de acción para identificar respuestas.

2. **Usar Order ID para correlación:** La correlación petición-respuesta debe basarse EXCLUSIVAMENTE en el Order ID.

3. **No asumir Echo:** No se debe asumir que la respuesta tiene el mismo código de acción que la petición.

---

## 6. Conclusiones

1. **La diferencia más crítica es el código de acción de la respuesta.** Esto confirma que la correlación se realiza por Order ID.

2. **Los ACK genéricos son el comportamiento estándar** para comandos SET.

3. **La auto-detection requiere corrección** para funcionar en Linux.

4. **Nuestra implementación es correcta** porque:
   - Usa Order ID para correlación
   - No verifica código de acción en respuestas
   - Maneja correctamente el buffer de recepción

---

## 7. Recomendaciones

1. **Actualizar documentación** para reflejar que el Action de respuesta NO es echo.

2. **Corregir `find_qscout()`** para detectar por VID:PID en lugar de descripción.

3. **Investigar significado** de los códigos 0x01 y 0x03 en respuestas.

4. **Probar auto-reports** si se conectan sensores que generen eventos.

---

## 8. Referencias

- Validación experimental: Fase 3B (2026-07-17)
- Paquetes de referencia: `docs/QScout_Reference_Packets.md`
- Log completo: `logs/validation_20260717_135131.log`
