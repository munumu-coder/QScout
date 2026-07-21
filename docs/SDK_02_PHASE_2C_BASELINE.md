# SDK-02 Phase 2C Baseline

**Date:** 2026-07-18  
**Status:** FROZEN  
**Baseline ID:** BL-2026-07-18-001

---

## 1. Baseline Summary

This baseline formally registers the stable state of the Q-Scout Native Linux SDK after the completion of T-FIX-01 (API compatibility restoration). The project has achieved a significant stability milestone:

- **Multi-Agent Infrastructure:** COMPLETED
- **Repository Consolidation:** COMPLETED (single canonical repo at `/home/munumu/Qscout`)
- **Protocol Documentation:** COMPLETED (RB Protocol v1.0 spec)
- **Physical Validation:** COMPLETED (5 commands validated against real robot)
- **SDK Compatibility Fixes:** COMPLETED (T-FIX-01, T-FIX-02, T-FIX-03)
- **Test Suite:** 184 tests, 0 failures, 0 errors

The project is considered stable because:
1. All migrated tests pass against the canonical codebase
2. The physically validated commands remain unchanged
3. Both class-based and function-based APIs are operational
4. The architecture is frozen (Decision D-009)
5. No blockers or critical risks remain

---

## 2. Repository Status

| Item | Value |
|------|-------|
| Canonical repository | `/home/munumu/Qscout` |
| Archived repository | `/home/munumu/qscout-sdk` (DO NOT USE) |
| Source layout | `src/qscout/` (pyproject.toml `where = ["src"]`) |
| Test directory | `tests/` |
| Documentation | `docs/` (24+ files) |
| Evidence | `evidence/logs/` |
| Project management | `project_management/` |
| Tools | `tools/` (13 validation/management scripts) |
| Backups | `backups/` (pre-consolidation archives) |
| Python version | 3.12.3 |
| Git status | Not a git repository |

### Source Modules (9 files)

| Module | Lines | Layer | Status |
|--------|-------|-------|--------|
| `__init__.py` | ~130 | SDK-02 | Facade with class + function APIs |
| `connection.py` | ~161 | SDK-01 | UART transport, CH340 auto-detect |
| `protocol.py` | ~660 | SDK-01 | RB protocol, 42 builders, 20+ parsers |
| `packet.py` | ~57 | SDK-01 | RBPacket representation |
| `command_map.py` | ~430 | SDK-02 | 42 CommandDef definitions |
| `commands.py` | ~88 | SDK-02 | Command abstraction |
| `exceptions.py` | ~17 | SDK-01 | 4 typed exceptions |
| `actuators.py` | ~210 | SDK-02 | Class + 4 module-level functions |
| `sensors.py` | ~230 | SDK-02 | Class + 2 module-level functions |

### Test Files (10 files)

| File | Tests | Status |
|------|-------|--------|
| `test_protocol.py` | 36 | PASS |
| `test_connection.py` | 11 | PASS |
| `test_real_packets.py` | 23 | PASS |
| `test_checksum.py` | 30 | PASS |
| `test_facade.py` | 12 | PASS |
| `test_actuators.py` | 19 | PASS |
| `test_sensors.py` | 7 | PASS |
| `test_packet.py` | 12 | PASS |
| `test_command_map.py` | 20 | PASS |
| `test_commands.py` | 14 | PASS |
| **Total** | **184** | **ALL PASS** |

---

## 3. SDK Architecture Status

### 3.1 Current Modules

The SDK uses a layered architecture with 7 architectural layers:

```
┌─────────────────────────────────────┐
│  Facade (__init__.py)               │  SDK-02
├─────────────────────────────────────┤
│  Actuators (actuators.py)           │  SDK-02
│  Sensors (sensors.py)               │  SDK-02
├─────────────────────────────────────┤
│  Commands (commands.py)             │  SDK-02
│  Command Map (command_map.py)       │  SDK-02
├─────────────────────────────────────┤
│  Packet (packet.py)                 │  SDK-01
├─────────────────────────────────────┤
│  Protocol (protocol.py)             │  SDK-01
├─────────────────────────────────────┤
│  Connection (connection.py)         │  SDK-01
│  Exceptions (exceptions.py)         │  SDK-01
└─────────────────────────────────────┘
```

### 3.2 Public API Status

**Dual API approach** (Option B from T-FIX-01):

| API Style | Location | Use Case |
|-----------|----------|----------|
| Class-based | `Actuators(conn)`, `Sensors(conn)` | Live robot control |
| Function-based | `actuators.led(...)`, `sensors.get_ultrasonic(...)` | Offline command construction |
| Facade | `QScout.port, r, g, b)` | Simplified integration |

### 3.3 Compatibility Layer

| Module | Compatibility Addition |
|--------|----------------------|
| `protocol.py` | `HEADER` alias for `HEADER_RB`, `calculate_checksum` alias for `sum_check`, `parse_packet()` compat function, `validate_checksum()` compat function |
| `actuators.py` | `led()`, `motor()`, `move()`, `buzzer()` module-level functions returning `Command` |
| `sensors.py` | `get_ultrasonic()`, `parse_ultrasonic_response()` module-level functions |
| `__init__.py` | `_OrderIdManager` class, facade methods (`led`, `motor`, `move`, `stop`, `buzzer`, `get_ultrasonic`) |

### 3.4 Preserved Class API

The class-based API is fully preserved and operational:

```python
from qscout import QScout

robot = QScout()
robot.connect()
robot.actuators.led(-4, 255, 0, 0)
robot.actuators.motor(-1, 80)
distance = robot.sensors.ultrasonic(1)
robot.actuators.stop()
robot.disconnect()
```

---

## 4. Protocol Status

### 4.1 RB Protocol

| Property | Value |
|----------|-------|
| Status | FROZEN |
| Header | `0x52 0x42` ("RB") |
| Checksum | `sum(all_bytes_except_checksum) % 256` |
| Packet format | `[header 2B][length 1B][orderId 1B][action 1B][payload N][checksum 1B]` |
| Order ID range | 2-254 (cycling, 0 reserved for unsolicited reports) |
| Baud rate | 115200, 8N1 |

### 4.2 Command Map

- **Total CommandDef definitions:** 42
- **Unique action codes:** 41 (0x11 shared by SET_MOTOR and SET_MOVE)
- **Validated commands:** 9 (LED, MOTOR, MOVE, BUZZER, ULTRASONIC, DEVICE_INFO, INTERFACE_INFO, ALL_INTERFACE_INFO, LINE_VALUE)
- **Pending commands:** 33 (awaiting physical validation)

### 4.3 Response Matching

- Response action codes do NOT match request action codes
- Correlation is by Order ID only
- SET_BUZZER returns ACK (action=0x01), confirmed by physical validation

---

## 5. Test Baseline

### 5.1 Before T-FIX-01

```
Ran 145 tests in 0.121s
FAILED (errors=31)
```

- 31 errors across 5 test files
- Root cause: architecture mismatch between migrated tests (function-based) and canonical source (class-based)

### 5.2 After T-FIX-01

```
Ran 184 tests in 0.143s
OK
```

- 0 failures, 0 errors
- 100% pass rate
- 39 additional tests from previously unimportable modules

### 5.3 What Was Fixed

| Fix | Tests Resolved | Method |
|-----|---------------|--------|
| Module-level functions in actuators.py | 19 | Added `led()`, `motor()`, `move()`, `buzzer()` |
| Module-level functions in sensors.py | 7 | Added `get_ultrasonic()`, `parse_ultrasonic_response()` |
| Exception types in parse_packet | 3 | Changed from `ValueError` to `QScoutProtocolError` / `QScoutChecksumError` |
| Missing receive_packet | 1 (import) | Added `receive_packet()` to protocol.py |
| Missing _OrderIdManager | 1 (import) | Added `_OrderIdManager` to __init__.py |
| build_packet validation | 4 | Added range checks for order_id and action |

---

## 6. Physical Validation Status

### 6.1 Validated Commands

| Command | Action Code | Status | Date |
|---------|-------------|--------|------|
| SET_LED | 0x10 | PASS | 2026-07-17 |
| SET_MOTOR | 0x11 | PASS | 2026-07-17 |
| SET_MOVE | 0x11 | PASS | 2026-07-17 |
| SET_BUZZER | 0x13 | PASS | 2026-07-17 |
| GET_ULTRASONIC | 0xA1 | PASS | 2026-07-17 |

### 6.2 Physical Validation Preservation

T-FIX-01 did NOT modify:
- Packet format for any validated command
- Checksum calculation
- Serial communication behavior
- Order ID management
- Command encoding

All 5 physically validated commands produce identical byte sequences before and after T-FIX-01.

---

## 7. Files Modified During T-FIX-01

### 7.1 `src/qscout/protocol.py`

| Change | Lines Affected |
|--------|---------------|
| `parse_packet` raises `QScoutProtocolError`/`QScoutChecksumError` instead of `ValueError` | ~139-150 |
| Added `receive_packet(connection)` function | ~167-200 |
| Added range/type validation to `build_packet` | ~154-175 |
| Added `calculate_checksum` alias for `sum_check` | ~129 (already existed) |

### 7.2 `src/qscout/actuators.py`

| Change | Lines Affected |
|--------|---------------|
| Added imports: `struct`, `Command`, `SET_LED`, `SET_MOTOR`, `SET_MOVE`, `SET_BUZZER` | Top of file |
| Added `_clamp_signed8()` and `_clamp_speed()` helper functions | ~30-40 |
| Added `led(port, r, g, b) -> Command` | ~50-70 |
| Added `motor(port, speed) -> Command` | ~73-82 |
| Added `move(left_speed, right_speed) -> Command` | ~85-94 |
| Added `buzzer(frequency, duration_ms, port=0) -> Command` | ~97-115 |

### 7.3 `src/qscout/sensors.py`

| Change | Lines Affected |
|--------|---------------|
| Added imports: `struct`, `Command`, `GET_ULTRASONIC` | Top of file |
| Added `_clamp_signed8()` helper | ~30-35 |
| Added `get_ultrasonic(port) -> Command` | ~40-52 |
| Added `parse_ultrasonic_response(raw) -> int` | ~55-68 |

### 7.4 `src/qscout/__init__.py`

| Change | Lines Affected |
|--------|---------------|
| Added imports: `build_set_led`, `build_set_motor`, `build_set_move`, `build_set_buzzer`, `Command`, `GET_ULTRASONIC` | Top of file |
| Added `_OrderIdManager` class with `.next()` method | ~30-45 |
| Added facade methods: `led`, `motor`, `move`, `stop`, `buzzer`, `get_ultrasonic` | ~80-105 |
| Renamed `_conn` to `_connection` throughout | All references |

--- 

## 8. Metric Definitions Used in This Document

**Note:** This baseline uses **non-canonical** definitions for backward compatibility.
For current canonical definitions, see `docs/METRIC_DEFINITIONS.md`.

| Metric | Definition | Note |
|--------|------------|------|
| "Unit Test" | Includes only `test_actuators.py` and `test_sensors.py` (module-level functions) | Differs from canonical **M-001** (Dedicated Unit Test) |
| "Untested Commands" | Commands without tests in `test_actuators.py` or `test_sensors.py` | Excludes indirect tests (e.g., `test_real_packets.py`) |

---

## 9. Current Limitations

1. **21 commands have zero test coverage** — Only 9 of 42 CommandDef definitions have dedicated unit tests (according to the **non-canonical** definition above). The remaining 33 commands are tested only through the command_map metadata tests or indirect tests.

2. **5 of 42 commands physically validated** — SET_LED, SET_MOTOR, SET_MOVE, SET_BUZZER, GET_ULTRASONIC have been tested against real hardware. The remaining 37 commands have not.

3. **No CLI interface** — The SDK is library-only. No command-line tool for direct robot control.

4. **No example scripts** — The `src/qscout/examples/` directory exists but is empty.

5. **Not a git repository** — The canonical repo has no version control. Backup archives exist but no commit history.

6. **protocol.py is a monolith** — At 660 lines, protocol.py contains builders, parsers, validators, and compatibility aliases. Refactoring is recommended but not critical.

---

## 9. Next Development Phase

### Next Task: T-TEST-01

**Objective:** Add unit tests for 21 untested commands.

**Commands requiring tests:**

| Category | Commands |
|----------|----------|
| Actuators | SET_ULTRASONIC_LIGHT, SET_MATRIX, SET_WORK_MODE, SET_STEERING_ENGINE, SET_OUT_ENGINE, SET_RGB_LED_MATRIX, SET_MP3, SET_FAN, SET_EXT_SERVO_DEGREE, SET_EXT_IO_OUTPUT, SET_FOUR_DIGIT, SET_FOUR_RGB_LED |
| Sensors | GET_BUTTON, GET_VOLTAGE, GET_TEMP_HUMIDITY, GET_LIGHT, GET_VOICE, GET_INFRARED, GET_GYRO, GET_COLOR, GET_TOUCH_BUTTON |

**Testing strategy (must be designed before implementation):**
1. Use module-level functions in `actuators.py` and `sensors.py` for offline command construction
2. Verify payload format matches protocol specification
3. Verify Command object metadata (action, definition, payload)
4. Use existing `build_*` functions in `protocol.py` for packet construction verification
5. Create real packet tests against captured byte sequences

**Dependencies:** None (T-FIX-01/02/03 all resolved)

**Estimated effort:** Medium (21 test functions + helper infrastructure)
