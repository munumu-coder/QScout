# QScout API Audit Report

**Fecha:** 2026-07-17  
**Fase:** 3D — Cierre y certificación  
**Estado:** Completo

---

## 1. Resumen Ejecutivo

| Criterio | Estado |
|----------|:------:|
| Consistencia de nombres | ✅ Buena |
| Coherencia entre métodos | ✅ Buena |
| Facilidad de uso | ✅ Buena |
| Simetría GET/SET | ✅ Buena |
| Claridad de parámetros | ✅ Buena |
| Valores por defecto | ⚠️ Mejorable |
| Documentación | ✅ Completa |
| Manejo de errores | ⚠️ Inconsistente |

**Calificación global:** La API es estable, coherente y usable. Las mejoras identificadas son menores y no justifican cambios incompatibles en v1.0.

---

## 2. Análisis por Clase

### 2.1 QScout (clase principal)

| Método | Firma | Docstring | Estado |
|--------|-------|-----------|:------:|
| `__init__(port, baudrate)` | `port: str \| None = None, baudrate: int = 115200` | ✅ Completo | ✅ |
| `connect()` | `() -> None` | ✅ Completo | ✅ |
| `disconnect()` | `() -> None` | ✅ Completo | ✅ |
| `is_connected()` | `() -> bool` | ✅ Completo | ✅ |
| `connection` (property) | `-> Connection` | ✅ Completo | ✅ |
| `__enter__` / `__exit__` | Context manager | ✅ Correcto | ✅ |

**Observaciones:**
- Auto-detección del puerto es una buena decisión ergonómica
- `ConnectionError` claro cuando no se encuentra el robot
- Context manager funciona correctamente

### 2.2 Sensors (lectura de sensores)

**Patrón consistente:** Todos los métodos siguen el mismo patrón:
```python
def sensor(self, port: int) -> ReturnType | None:
    oid = self._conn.next_order_id()
    pkt = protocol.build_get_*(oid, port)
    resp = self._conn.send_receive(pkt)
    return protocol.parse_*(resp) if resp else None
```

| Método | Puerto | Default | Retorno | Docstring | Estado |
|--------|:------:|:-------:|---------|-----------|:------:|
| `device_info()` | — | N/A | `dict \| None` | ✅ | ✅ |
| `interface_info(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `all_interface_info()` | — | N/A | `list \| None` | ✅ | ✅ |
| `motor_interface_info()` | — | N/A | `dict \| None` | ✅ | ✅ |
| `user_interface_info()` | — | N/A | `list \| None` | ✅ | ⚠️ |
| `voltage(port)` | `int` | **1** | `int \| None` | ✅ | ⚠️ |
| `ultrasonic(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `button(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `line_value(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `temperature_humidity(port)` | `int` | requerido | `dict \| None` | ✅ | ✅ |
| `light(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `voice(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `infrared(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `gyro(port, gyro_type)` | `int` | requerido | `list \| None` | ✅ | ✅ |
| `color_rgb(port)` | `int` | requerido | `dict \| None` | ✅ | ✅ |
| `color_grey(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `touch_button(port)` | `int` | requerido | `list` | ✅ | ⚠️ |
| `temperature_dual(port, temp_type)` | `int` | requerido | `str \| None` | ✅ | ⚠️ |
| `six_line(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `rocker(port)` | `int` | requerido | `list \| None` | ✅ | ✅ |
| `flame(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `gas(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `spiral_pot(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `line_pot(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `ext_io_input(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `ext_apc(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |
| `ext_temp_humi(port)` | `int` | requerido | `int \| None` | ✅ | ✅ |

### 2.3 Actuators (control de actuadores)

| Método | Parámetros | Default | Retorno | Docstring | Estado |
|--------|-----------|:-------:|---------|-----------|:------:|
| `led(port, r, g, b)` | port, r, g, b | — | None | ✅ | ✅ |
| `motor(port, speed)` | port, speed | — | None | ✅ | ✅ |
| `move(m1_speed, m2_speed)` | m1, m2 | — | None | ✅ | ✅ |
| `forward(speed)` | speed | **150** | None | ✅ | ⚠️ |
| `backward(speed)` | speed | **150** | None | ✅ | ⚠️ |
| `turn_left(speed)` | speed | **150** | None | ✅ | ⚠️ |
| `turn_right(speed)` | speed | **150** | None | ✅ | ⚠️ |
| `stop()` | — | — | None | ✅ | ✅ |
| `ultrasonic_light(port, r, g, b)` | port, r, g, b | — | None | ✅ | ✅ |
| `buzzer(frequency, duration_ms, port)` | freq, dur, port | port=-6 | None | ✅ | ⚠️ |
| `beep(frequency, duration_ms)` | freq, dur | 440, 200 | None | ✅ | ✅ |
| `matrix(port, rows)` | port, rows | — | None | ✅ | ✅ |
| `work_mode(port, mode, value)` | port, mode, value | value=0 | None | ✅ | ✅ |
| `steering_engine(port, engine, a, b)` | port, engine, a, b | b=90 | None | ✅ | ✅ |
| `out_engine(port, engine, spd_a, spd_b)` | port, engine, spd_a, spd_b | spd_b=0 | None | ✅ | ✅ |
| `rgb_led_matrix(port, led_data)` | port, led_data | — | None | ✅ | ✅ |
| `mp3(port, source, command, param)` | port, src, cmd, param | param=0 | None | ✅ | ✅ |
| `fan(port, speed, direction)` | port, speed, direction | direction=1 | None | ✅ | ✅ |
| `ext_servo_degree(port, degree)` | port, degree | — | None | ✅ | ✅ |
| `ext_io_output(port, status)` | port, status | — | None | ✅ | ✅ |
| `four_digit(port, d1–d4)` | port, d1–d4 | — | None | ✅ | ✅ |
| `four_rgb_led(port, loc, r, g, b)` | port, loc, r, g, b | — | None | ✅ | ✅ |

---

## 3. Problemas Identificados

### 3.1 Inconsistencia de Tipado (MENOR)

| Archivo | Estilo usado |
|---------|-------------|
| `__init__.py` | `str \| None` (PEP 604) |
| `sensors.py` | `dict \| None` (PEP 604) |
| `connection.py` | `Optional[str]` (typing module) |
| `protocol.py` | Mixto: `int \| None` y `List[bytes]` |

**Impacto:** Cosmético. No afecta funcionalidad.  
**Recomendación:** Unificar a PEP 604 en v2.0.

### 3.2 `touch_button()` retorna `[]` en vez de `None` (MENOR)

```python
# Actual (sensors.py:146)
return protocol.parse_touch_button(resp) if resp else []

# Convención documentada en la clase:
# "All methods... return None if no response is received"
```

**Impacto:** Rompe la convención documentada. El usuario debe verificar `if result is not None` en vez de `if result`.  
**Recomendación:** Cambiar a `return None` en v2.0.

### 3.3 `temperature_dual()` retorna `str` (MENOR)

```python
# Actual: retorna string como "-23.45"
# Esperado: retornar float o dict con valores numéricos
```

**Impacto:** El usuario debe parsear el string para hacer cálculos.  
**Recomendación:** Retornar `dict | None` con `{'temperature': float, 'sign': int}` en v2.0.

### 3.4 `user_interface_info()` tiene parsing inline (MENOR)

```python
# Actual (sensors.py:58-62): parsing manual de bytes
# Patrón normal: delegar a protocol.parse_*()
```

**Impacto:** Inconsistencia arquitectónica. No afecta funcionalidad.  
**Recomendación:** Extraer a `parse_user_interface_info()` en protocol.py en v2.0.

### 3.5 `forward(speed=150)` excede rango (MENOR)

```python
# forward() usa speed=150 por defecto
# protocol._clamp_speed() limita a [-100, 100]
# Resultado: speed se silencamente limita a 100
```

**Impacto:** El usuario cree que el robot se mueve a 150, pero en realidad se mueve a 100.  
**Recomendación:** Cambiar default a `100` en v2.0.

### 3.6 `buzzer()` tiene port como tercer parámetro (MENOR)

```python
# buzzer(frequency, duration_ms, port=-6)
# Todos los demás métodos: port es el primer parámetro
```

**Impacto:** Inconsistencia de orden de parámetros.  
**Recomendación:** Reordenar a `buzzer(port, frequency, duration_ms)` en v2.0 (breaking change).

### 3.7 `Connection` no tiene context manager (MENOR)

```python
# QScout: ✅ __enter__ / __exit__
# Connection: ❌ no tiene
```

**Impacto:** Los usuarios que usan Connection directamente deben cerrar manualmente.  
**Recomendación:** Añadir soporte en v2.0.

### 3.8 Inconsistencia en error handling (MENOR)

| Método | Comportamiento en error |
|--------|------------------------|
| `Connection.send()` | Lanza `ConnectionError` |
| `Connection.receive()` | Retorna `None` silenciosamente |
| `Connection.send_receive()` | Retorna `None` (no distingue timeout de desconexión) |

**Impacto:** No se puede distinguir "timeout" de "desconexión" al usar `send_receive()`.  
**Recomendación:** Añadir excepción o flag en v2.0.

---

## 4. Recomendaciones para v2.0

Estas mejoras romperían compatibilidad y deben documentarse únicamente, no implementarse en v1.0:

| # | Mejora | Breaking Change | Prioridad |
|---|--------|:---------------:|:---------:|
| 1 | Unificar tipado a PEP 604 | No | Baja |
| 2 | `touch_button()` retorna `None` | Sí | Media |
| 3 | `temperature_dual()` retorna `float` | Sí | Media |
| 4 | Extraer `parse_user_interface_info` | No | Baja |
| 5 | Default speed = 100 en `forward()` | Sí | Baja |
| 6 | Reordenar parámetros de `buzzer()` | Sí | Baja |
| 7 | Añadir context manager a `Connection` | No | Baja |
| 8 | Unificar error handling | Sí | Media |

---

## 5. Conclusión

La API pública es **estable y coherente** para v1.0. Los problemas identificados son menores y no afectan la funcionalidad core. Las mejoras recomendadas son candidatas para v2.0.

**Estado:** ✅ Aprobado para v1.0.0

---

*Generado el 2026-07-17 como parte de la Fase 3D de cierre.*
