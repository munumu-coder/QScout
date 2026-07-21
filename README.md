# QScout SDK

Python SDK para control del robot **Robobloq Q-Scout RB-00002** desde Linux vía UART/USB.

## Requisitos

- Python ≥ 3.10
- Linux (probado en Ubuntu/Debian)
- pyserial

## Instalación

```bash
pip install -e .
```

## Uso rápido

```python
from qscout import QScout

with QScout("/dev/ttyUSB0") as robot:
    # LED rojo en puerto M4
    robot.led(-4, 255, 0, 0)

    # Mover robot
    robot.move(50, 50)

    # Leer sensor ultrasónico
    distance = robot.get_ultrasonic(1)
    print(f"Distancia: {distance} mm")

    # Buzzer
    robot.buzzer(440, 500)

    # Parar
    robot.stop()
```

### Comandos disponibles (confirmados experimentalmente)

| Método | Descripción | Tipo |
|--------|-------------|:----:|
| `robot.led(port, r, g, b)` | Color LED RGB | SET |
| `robot.motor(port, speed)` | Motor individual | SET |
| `robot.move(left, right)` | Movimiento dual motor | SET |
| `robot.stop()` | Parar ambos motores | SET |
| `robot.buzzer(freq, duration)` | Tono buzzer | SET |
| `robot.get_ultrasonic(port)` | Distancia ultrasónica (mm) | GET |

**Nota:** Solo comandos validados experimentalmente. Sensores/actuadores pendientes no están implementados.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quick Start (Bootstrap System)

```bash
# Full bootstrap — checks environment, loads state, shows dashboard
./start_project.sh

# Or use Make commands
make start      # Full bootstrap
make health     # Health check only
make dashboard  # Project dashboard
make validate   # Run all validators
make status     # Show current state
make dispatch   # Show next task
```

See [docs/BOOTSTRAP_SYSTEM.md](docs/BOOTSTRAP_SYSTEM.md) for full documentation.

## Arquitectura

```
┌──────────────────────┐
│  robot.led()          │  ← API de usuario (facade convenience)
│  robot.sensors.*      │
│  robot.actuators.*    │
└────────┬─────────────┘
         │
┌────────▼─────────────┐
│       QScout         │  ← Fachada (__init__.py)
│  + Connection,       │
│    Sensors,          │
│    Actuators,        │
│    OrderManager      │
└────────┬─────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────┐
│ Sensors │ │Actuators │  ← Capa de alto nivel
│.py      │ │.py       │
└───┬─────┘ └────┬─────┘
    │            │
    └─────┬──────┘
          ▼
┌──────────────────┐
│   protocol.py    │  ← Capa de protocolo RB
│ RBPacket, Action, │
│ Port, builders,   │
│ parsers, checksum │
└────────┬─────────┘
         │
┌────────▼─────────┐
│  connection.py   │  ← Transporte UART puro
└──────────────────┘
```

| Módulo | Capa | Responsabilidad |
|--------|------|-----------------|
| `connection.py` | SDK-01 | Transporte UART (send/receive) |
| `protocol.py` | SDK-01 | RBPacket, Action, Port, OrderManager, builders, parsers, checksum |
| `actuators.py` | SDK-01 | Actuator API de alto nivel (LED, motor, buzzer, matrix, etc.) |
| `sensors.py` | SDK-01 | Sensor API de alto nivel (ultrasonic, voltage, gyro, color, etc.) |
| `__init__.py` | SDK-01 | Fachada QScout + convenience methods |
| `exceptions.py` | SDK-01 | QScoutError, QScoutProtocolError, QScoutChecksumError, QScoutConnectionError |

## Estructura

```
src/qscout/
    __init__.py       # QScout facade + convenience methods
    connection.py     # UART transport (send/receive)
    protocol.py       # RBPacket, Action, Port, OrderManager, builders, parsers
    actuators.py      # Actuator high-level API
    sensors.py        # Sensor high-level API
    exceptions.py     # SDK exceptions
tests/
    __init__.py
    test_connection.py
    test_protocol.py
    test_checksum.py
    test_real_packets.py
    test_actuators.py
    test_sensors.py
    test_facade.py
```
