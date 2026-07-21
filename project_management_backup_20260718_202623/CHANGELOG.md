# CHANGELOG.md — Chronological Project History

---

## Phase 0 — Initial Idea (Early July 2026)

### Features Implemented
- Project concept defined
- Feasibility assessment completed

### Tests
- N/A

### Physical Validation
- N/A

### Documentation
- Initial project plan

### Known Issues
- None

---

## Phase 1 — Robot Knowledge (Early July 2026)

### Features Implemented
- Hardware identification (ESP32, CH340, UART 115200)
- Communication interface analysis

### Tests
- N/A

### Physical Validation
- USB connection confirmed
- Serial port detection confirmed

### Documentation
- `QScout_Initial_Analysis_Report.md`
- `QScout_MyQode_Forensic_Report.md`

### Known Issues
- None

---

## Phase 1A — MyQode Forensic Analysis (Early July 2026)

### Features Implemented
- MyQode application reverse-engineered
- Protocol.js analyzed
- RB packet format extracted

### Tests
- N/A

### Physical Validation
- N/A

### Documentation
- `QScout_MyQode_Forensic_Report.md`

### Known Issues
- None

---

## Phase 1B — Architecture Verification (Early July 2026)

### Features Implemented
- Architecture assumptions verified
- MicroPython hypothesis discarded

### Tests
- N/A

### Physical Validation
- N/A

### Documentation
- `QScout_Initial_Analysis_Report.md` updated

### Known Issues
- None

---

## Phase 1C — Protocol Specification (Mid July 2026)

### Features Implemented
- Complete RB protocol specification documented
- Header, checksum, action codes, order ID defined

### Tests
- N/A

### Physical Validation
- N/A

### Documentation
- `QScout_RB_Protocol_Specification.md`

### Known Issues
- None

---

## Phase 2 — Protocol Validation (Mid July 2026)

### Features Implemented
- Protocol behavior validated experimentally

### Tests
- N/A

### Physical Validation
- Packet format confirmed
- Checksum calculation confirmed

### Documentation
- `QScout_Protocol_Validation_Report.md`

### Known Issues
- None

---

## Phase 3A — Firmware Analysis (Mid July 2026)

### Features Implemented
- Firmware identified as Arduino + ESP-IDF C++
- k2x.bin analyzed

### Tests
- N/A

### Physical Validation
- N/A

### Documentation
- `QScout_Firmware_Forensic_Report.md`

### Known Issues
- None

---

## Phase 3B — Protocol Consolidation (Mid July 2026)

### Features Implemented
- Response matching mechanism documented
- Observed differences documented
- Reference packets created

### Tests
- N/A

### Physical Validation
- N/A

### Documentation
- `QScout_Response_Matching_Mechanism.md`
- `QScout_Observed_Differences.md`
- `QScout_Reference_Packets.md`

### Known Issues
- None

---

## Phase 3C — Physical Validation (Mid July 2026)

### Features Implemented
- Physical robot validation completed
- Regression tests created

### Tests
- 23 regression tests with real captured packets

### Physical Validation
- LED: PASS
- Motor: PASS
- Move: PASS
- Buzzer: PASS
- Ultrasonic: PASS

### Documentation
- `physical_validation_report.md`
- `QScout_Physical_Validation_Report.md`

### Known Issues
- Response action codes differ from request action codes

---

## SDK-01 — Core SDK (Mid July 2026)

### Features Implemented
- `protocol.py` — RB protocol, Action enum, Port constants, 40+ builders, 20+ parsers
- `connection.py` — UART transport with VID:PID auto-detection
- `packet.py` — RBPacket representation
- `exceptions.py` — SDK exceptions
- `__init__.py` — QScout facade

### Tests
- 41 tests passing

### Physical Validation
- N/A

### Documentation
- `QScout_Library_Audit_Report.md`

### Known Issues
- None

---

## SDK-02 Phase 1 — Command Layer (Mid July 2026)

### Features Implemented
- `commands.py` — Command abstraction
- `command_map.py` — 42 CommandDef definitions, 41 unique action codes

### Tests
- Command metadata tests added

### Physical Validation
- N/A

### Documentation
- `QScout_API_Audit_Report.md`

### Known Issues
- Action 0x11 represents both SET_MOTOR and SET_MOVE (payload structure distinguishes)

---

## SDK-02 Phase 2A — Public API (Mid July 2026)

### Features Implemented
- `actuators.py` — LED, motor, move, buzzer payload builders
- `sensors.py` — Ultrasonic sensor payload and parser
- Public methods: `led()`, `motor()`, `move()`, `stop()`, `buzzer()`, `get_ultrasonic()`

### Tests
- Actuator tests added
- Sensor tests added
- Facade tests added

### Physical Validation
- N/A

### Documentation
- README.md updated with public API

### Known Issues
- None

---

## SDK-02 Phase 2B — Physical SDK Validation (Mid July 2026)

### Features Implemented
- SDK validated against physical robot

### Tests
- 119 tests passing (all suites)

### Physical Validation
- LED: PASS
- Motor: PASS
- Move: PASS
- Buzzer: PASS (returns ACK, not fire-and-forget)
- Ultrasonic: PASS (2500mm confirmed)

### Documentation
- `QScout_Project_Consolidation_Report.md`
- `QScout_v1.0_Release_Notes.md`
- `RB_Protocol_v1.0.md`

### Known Issues
- SET_BUZZER returns ACK (previously documented as fire-and-forget)
- Only SET_MOVE variants are fire-and-forget

---

## Documentation Consolidation (2026-07-18)

### Features Implemented
- All documentation synchronized with latest physical validation

### Tests
- N/A

### Physical Validation
- N/A

### Documentation
- `QScout_Response_Action_Code_Analysis.md`
- `QScout_Protocol_Coverage_Report.md`
- `QScout_Repository_Consolidation_Report.md`
- `QScout_API_Audit_Report.md` updated

### Known Issues
- None
