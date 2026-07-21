# START_HERE.md — Entry Point for Any New Agent

**Last Updated:** 2026-07-20

---

## What Is This Project?

**QScout SDK** — Native Python library for controlling the **Robobloq Q-Scout (RB-00002)** robot from Linux via USB/UART at 115200 baud. The library provides:

- Motor, LED, buzzer, servo, and other actuator control
- Sensor reading (ultrasonic, voltage, gyroscope, color, light, temperature, etc.)
- UART auto-detection via CH340 VID:PID
- RB protocol implementation (checksum, packet building/parsing, order-ID correlation)

**Version:** 1.0.0 (per pyproject.toml)  
**Repository:** `/home/munumu/Qscout`

---

## Architecture (Definitive)

```
QScout (facade)
 ├── connection.Connection   — UART send/receive (transport only)
 ├── sensors.Sensors         — High-level sensor reads
 ├── actuators.Actuators     — High-level actuator commands
 ├── protocol.OrderManager   — Order ID generation (2-254)
 └── protocol.RBPacket       — RB packet value object
```

**Key points:**
- All protocol logic (builders, parsers, Action enum, Port constants, checksum) is in `protocol.py`
- No separate `packet.py`, `commands.py`, or `command_map.py` — those were consolidated into `protocol.py`
- `OrderManager` (not `_OrderIdManager`) handles incremental order IDs
- Architecture is **frozen** (decision D-009) — extend capabilities, don't redesign

---

## What Is Completed

| Phase | Status |
|-------|--------|
| Phase 0-3: Research, protocol extraction, analysis, physical validation | ✅ COMPLETED |
| SDK-01: protocol.py, connection.py, exceptions.py, RBPacket | ✅ COMPLETED |
| SDK-02 Phase 2A: actuators.py, sensors.py, facade methods | ✅ COMPLETED |
| SDK-02 Phase 2B: Physical validation of LED, motor, move, buzzer, ultrasonic | ✅ COMPLETED |
| SDK-02 Phase 2C: All remaining sensor/actuator commands implemented | ✅ COMPLETED |
| T-FIX-01: 31 failing tests fixed (API mismatch) | ✅ COMPLETED |
| T-FIX-02/03: Exception type mismatches fixed | ✅ COMPLETED |
| Documentation audit and sync | ✅ COMPLETED |

---

## What Is Pending

| Task | Priority | Notes |
|------|----------|-------|
| **T-FIX-04: Fix 3 failing tests** | **P1** | 1 failure + 2 errors in current test suite |
| T-TEST-01: Add unit tests for untested commands | P2 | Low coverage on newer sensor/actuator methods |
| T-HW-01: Physical validation of remaining commands | P3 | Only 5 commands validated on real robot so far |

---

## Source Modules

| File | What It Contains |
|------|-----------------|
| `src/qscout/__init__.py` | QScout facade + convenience methods (led, motor, move, buzzer, get_ultrasonic) |
| `src/qscout/protocol.py` | RBPacket, Action enum, Port constants, OrderManager, 25+ builders, 20+ parsers, checksum |
| `src/qscout/connection.py` | UART Connection with auto-detect via VID:PID |
| `src/qscout/actuators.py` | Actuators class: led, motor, move, buzzer, matrix, steering, fan, etc. |
| `src/qscout/sensors.py` | Sensors class: device_info, voltage, ultrasonic, gyro, color, light, etc. |
| `src/qscout/exceptions.py` | QScoutError, QScoutProtocolError, QScoutChecksumError, QScoutConnectionError |

**Modules that DO NOT exist** (deleted/consolidated, do NOT recreate):
- `packet.py` — RBPacket moved to protocol.py
- `commands.py` — removed (no Command abstraction layer)
- `command_map.py` — removed (Action enum in protocol.py)
- `test_packet.py` — removed
- `test_command_map.py` — removed
- `test_commands.py` — removed

---

## Test State

- **Total tests:** 143 (across 7 test files)
- **Passing:** 140
- **Failing:** 3 (1 failure + 2 errors)
- **Test files:** `test_connection.py`, `test_protocol.py`, `test_checksum.py`, `test_real_packets.py`, `test_actuators.py`, `test_sensors.py`, `test_facade.py`
- **Run command:** `PYTHONPATH=src python3 -m unittest discover -s tests`

---

## Key Documents

| Document | Purpose |
|----------|---------|
| `CONTROL_CENTER.yaml` | Current project state (source of truth) |
| `TASK_STATE.yaml` | Task tracking |
| `ROADMAP.md` | Phase history and future plans |
| `DECISIONS.md` | Architectural decisions |
| `PROJECT_RULES.md` | Mandatory rules |
| `CHANGELOG.md` | Chronological history |
| `docs/METRIC_DEFINITIONS.md` | Canonical metric definitions |
| `docs/QScout_RB_Protocol_Specification.md` | RB protocol spec |
| `docs/RB_Protocol_v1.0.md` | Protocol v1.0 document |

---

## Known Issues

1. **3 failing tests** — Need investigation and fix (T-FIX-04)
2. **Low test coverage** — Many sensor/actuator methods lack dedicated tests
3. **37 commands not physically validated** — Only LED, motor, move, buzzer, ultrasonic verified on real robot
4. **No CLI interface** — SDK-03 would add this
5. **No git repository** — Not version-controlled

---

## Architectural Decisions (Mandatory)

1. **D-004: Strict layer separation** — Connection never knows protocol details, protocol never knows transport
2. **D-005: Order ID correlation** — Responses matched by Order ID, NOT by action code
3. **D-006: Checksum before parsing** — Always validate checksum before interpreting packet data
4. **D-007: Auto-detection via VID:PID** — CH340 USB detected automatically (fallback: description)
5. **D-008: SET_MOVE is fire-and-forget** — Other SET commands may return ACK
6. **D-009: Architecture frozen** — No redesigns; only capability extensions

---

## Next Steps for a New Agent

1. Read `CONTROL_CENTER.yaml` for full current state
2. Read `TASK_STATE.yaml` for pending tasks
3. Read `ROADMAP.md` for context
4. Read `DECISIONS.md` for architectural constraints
5. Fix the 3 failing tests (T-FIX-04) or start on T-TEST-01
6. **Never** recreate deleted modules (packet.py, commands.py, command_map.py)
7. **Never** modify architecture without human approval

---

## What Must NEVER Be Done

1. **Never** recreate deleted files: `packet.py`, `commands.py`, `command_map.py`, `test_packet.py`, `test_command_map.py`, `test_commands.py`
2. **Never** modify frozen architecture (layers in protocol.py/connection.py/actuators.py/sensors.py)
3. **Never** modify `pyproject.toml` without justification
4. **Never** implement undocumented protocol behavior
5. **Never** add external dependencies without approval
