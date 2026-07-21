# PROJECT_STATE.md — Single Source of Truth

**Last Update:** 2026-07-18

---

## Repository

| Field | Value |
|-------|-------|
| Canonical Repository | `/home/munumu/Qscout` |
| Current Branch | `main` (default) |
| Source Code | `src/qscout/` |
| Tests | `tests/` |
| Documentation | `docs/` |
| Evidence | `evidence/` |
| Project Management | `project_management/` |

---

## Project Identity

| Field | Value |
|-------|-------|
| Project | Q-Scout Native Linux SDK |
| Objective | Native Python SDK for controlling Robobloq Q-Scout (RB-00002) via USB/UART |
| Language | Python 3.10+ |
| OS | Linux (Ubuntu/Debian) |
| Hardware | Robobloq Q-Scout RB-00002 (ESP32, CH340 USB-UART) |
| Protocol | RB (Header: 0x52 0x42) |
| Baudrate | 115200, 8N1 |

---

## Current Milestone

| Field | Value |
|-------|-------|
| Current Phase | **SDK-02 Phase 2C — Expand Public API** |
| Previous Milestone | SDK-02 Phase 2B — Physical SDK Validation |
| Current Objective | Expand public API with additional documented commands |
| Next Milestone | SDK-03 — Full Coverage, CLI, Examples |

---

## Current Architecture

```
┌──────────────────┐
│   robot.led()    │  ← API de usuario
└────────┬─────────┘
         │
┌────────▼─────────┐
│      QScout      │  ← Fachada (SDK-02)
└────────┬─────────┘
         │
┌────────▼─────────┐
│  actuators.py    │  ← Construcción de payloads (SDK-02)
│  sensors.py      │
└────────┬─────────┘
         │
┌────────▼─────────┐
│    Command       │  ← Intención abstracta (SDK-02)
│  command_map.py  │
└────────┬─────────┘
         │
┌────────▼─────────┐
│  build_packet()  │  ← Protocolo RB genérico (SDK-01)
│  protocol.py     │
└────────┬─────────┘
         │
┌────────▼─────────┐
│ QScoutConnection │  ← Transporte UART (SDK-01)
│  connection.py   │
└──────────────────┘
```

| Module | Layer | Responsibility |
|--------|-------|----------------|
| `connection.py` | SDK-01 | UART transport with auto-detection |
| `protocol.py` | SDK-01 | RB protocol, Action enum, builders, parsers |
| `packet.py` | SDK-01 | RBPacket representation |
| `exceptions.py` | SDK-01 | SDK exceptions |
| `command_map.py` | SDK-02 | 42 CommandDef definitions, 41 unique action codes |
| `commands.py` | SDK-02 | Command abstraction |
| `actuators.py` | SDK-02 | Actuator payload builders |
| `sensors.py` | SDK-02 | Sensor payload builders and parsers |
| `__init__.py` | SDK-02 | QScout facade |

**Architecture Status:** Frozen (Decision D-009)

---

## Test Status

| Metric | Value |
|--------|-------|
| Total Tests | 119 |
| Passing | 119 |
| Failing | 0 |
| Last Run | 2026-07-18 |

| Test File | Tests | Coverage |
|-----------|-------|----------|
| `tests/test_protocol.py` | 36 | Protocol builders/parsers |
| `tests/test_connection.py` | 11 | Connection management |
| `tests/test_real_packets.py` | 23 | Regression with real captured packets |
| Other test files | 49 | Commands, actuators, sensors, facade |

**Run Tests:**
```bash
cd /home/munumu/Qscout
PYTHONPATH=src python3 -m unittest discover -s tests
```

---

## Physical Validation

| Command | Status | Date |
|---------|--------|------|
| SET_LED | PASS | 2026-07-17 |
| SET_MOTOR | PASS | 2026-07-17 |
| SET_MOVE | PASS | 2026-07-17 |
| SET_BUZZER | PASS | 2026-07-17 |
| GET_ULTRASONIC | PASS | 2026-07-17 |

**Key Findings:**
- Response action codes ≠ request action codes
- Response correlation by Order ID only
- SET_BUZZER returns ACK (not fire-and-forget)
- Only SET_MOVE variants are fire-and-forget

---

## Documentation Status

| Document | Location | Status |
|----------|----------|--------|
| RB Protocol Specification | `docs/QScout_RB_Protocol_Specification.md` | Updated |
| Response Matching Mechanism | `docs/QScout_Response_Matching_Mechanism.md` | Completed |
| Observed Differences | `docs/QScout_Observed_Differences.md` | Completed |
| Reference Packets | `docs/QScout_Reference_Packets.md` | Completed |
| Physical Validation Report | `docs/physical_validation_report.md` | Completed |
| Library Audit Report | `docs/QScout_Library_Audit_Report.md` | Completed |
| Firmware Forensic Report | `docs/QScout_Firmware_Forensic_Report.md` | Completed |
| Consolidation Report | `docs/QScout_Project_Consolidation_Report.md` | Completed |
| Coverage Report | `docs/QScout_Protocol_Coverage_Report.md` | Completed |
| Release Notes v1.0 | `docs/QScout_v1.0_Release_Notes.md` | Completed |
| API Audit Report | `docs/QScout_API_Audit_Report.md` | Updated |
| Response Action Code Analysis | `docs/QScout_Response_Action_Code_Analysis.md` | Completed |

**Last Documentation Update:** 2026-07-18

---

## Project Team (AI Agents)

| Role | Agent | Document |
|------|-------|----------|
| Coordinator | TBD | `AGENT_COORDINATOR.md` |
| Programmer | TBD | `AGENT_PROGRAMMER.md` |
| Auditor | TBD | `AGENT_AUDITOR.md` |

**Last Audit:** 2026-07-18 (Phase A.1)

---

## Phase Progress

| Phase | Status |
|-------|--------|
| Phase 0 — Initial Idea | Completed |
| Phase 1 — Robot Knowledge | Completed |
| Phase 1A — MyQode Forensic Analysis | Completed |
| Phase 1B — Architecture & Protocol Verification | Completed |
| Phase 1C — Protocol Specification Extraction | Completed |
| Phase 2 — Protocol Validation | Completed |
| Phase 3A — Firmware Analysis | Completed |
| Phase 3B — Protocol Consolidation | Completed |
| Phase 3C — Physical Validation | Completed |
| SDK-01 — Core SDK | Completed (Frozen) |
| SDK-02 Phase 1 — Command Layer | Completed |
| SDK-02 Phase 2A — Public API | Completed |
| SDK-02 Phase 2B — Physical Validation | Completed |
| SDK-02 Phase 2C — Expand Public API | **IN PROGRESS** |
| SDK-03 — Full Coverage, CLI, Examples | Pending |
| SDK-04 — BLE Backend | Pending |
| SDK-05 — Scratch Backend | Pending |
| SDK-06 — ROS Integration | Pending |
| SDK-07 — Version 1.0 / PyPI | Pending |

---

## Known Issues

1. Response action codes 0x01 and 0x03 exact meaning not fully understood
2. Whether robot sends auto-reports unknown
3. Optimal timeout values for different operations not characterized

---

## Blockers

None currently.

---

## Risks

1. Missing external hardware modules limits physical validation of 33 untested commands
2. BLE and Wi-Fi backends require additional reverse engineering
3. No CI/CD pipeline yet

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [START_HERE.md](START_HERE.md) | Entry point for new agents |
| [ROADMAP.md](ROADMAP.md) | Complete project roadmap |
| [TASK_QUEUE.md](TASK_QUEUE.md) | Task queue with assignments |
| [TASK_STATE.yaml](TASK_STATE.yaml) | Live execution state |
| [DECISIONS.md](DECISIONS.md) | Architectural decision log |
| [CHANGELOG.md](CHANGELOG.md) | Chronological project history |
| [PROJECT_RULES.md](PROJECT_RULES.md) | Permanent project rules |
| [AGENT_MANIFEST.md](AGENT_MANIFEST.md) | Agent definitions |
| [AGENT_WORKFLOW.md](AGENT_WORKFLOW.md) | Agent communication protocol |
| [CURRENT_STATUS.yaml](CURRENT_STATUS.yaml) | Machine-readable project state |
| [PROJECT_OPERATING_SYSTEM.md](PROJECT_OPERATING_SYSTEM.md) | Operating procedures |
| [QUALITY_GATES.md](QUALITY_GATES.md) | Quality gates |
| [COORDINATOR_DASHBOARD.md](COORDINATOR_DASHBOARD.md) | Daily dashboard |
| [PROJECT_INDEX.md](PROJECT_INDEX.md) | Master index |
