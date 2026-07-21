# Q-Scout Project Backup
Fecha: 2026-07-16

## Estado del proyecto

Proyecto:
Desarrollo de una librería Python nativa para Linux que controle el robot Robobloq Q-Scout (RB-00002) mediante USB/UART, sin depender de MyQode.

### Fases completadas

✓ Fase 1 — Análisis inicial
✓ Fase 1A — Análisis forense de MyQode
✓ Fase 1B — Verificación de arquitectura y protocolo
✓ Fase 1C — Extracción de la especificación del protocolo
✓ Fase 2 — Validación del protocolo
✓ Fase 3A — Diseño e implementación inicial de la librería Python

### Conclusiones verificadas

- El protocolo RB utilizado por MyQode es el mismo que el documentado en la librería Arduino.
- Header: 0x52 0x42 ("RB")
- Checksum: suma de todos los bytes módulo 256.
- UART transmite paquetes RB directamente.
- BLE encapsula el mismo paquete RB dentro de paquetes MK.
- Baudrate: 115200.

### Estado de la librería

Ubicación:
/home/munumu/Qscout/

Estructura:

docs/
src/qscout/
tests/
examples/
pyproject.toml

La librería incluye:

- protocol.py
- connection.py
- sensors.py
- actuators.py

El protocolo implementado coincide con la especificación obtenida durante la ingeniería inversa.

### Documentación disponible

QScout_Initial_Analysis_Report.md
QScout_MyQode_Forensic_Report.md
QScout_RB_Protocol_Specification.md
QScout_Protocol_Validation_Report.md

### Próxima fase

Fase 3B

Objetivo:
Validar la librería sobre el robot físico.

Tareas previstas:

1. Detectar correctamente /dev/ttyUSB0.
2. Abrir comunicación a 115200 baudios.
3. Enviar un primer paquete RB.
4. Verificar ACK.
5. Probar LED, buzzer y motores.
6. Validar lectura de sensores.
7. Corregir únicamente las diferencias detectadas respecto al comportamiento real.

No modificar el protocolo salvo evidencia experimental.
