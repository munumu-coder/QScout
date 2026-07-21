# ROADMAP.md — Complete Project Roadmap

---

## Phase 0 — Initial Idea

- **Objective:** Decide to control Q-Scout from Ubuntu without Windows or MyQode
- **Dependencies:** None
- **Deliverables:** Project concept, initial research plan
- **Completion Criteria:** Feasibility assessment complete
- **Status:** ✅ Completed

---

## Phase 1 — Robot Knowledge

- **Objective:** Understand the robot hardware and communication interface
- **Dependencies:** Phase 0
- **Deliverables:** Hardware identification report, communication analysis
- **Completion Criteria:** ESP32, CH340, UART 115200 confirmed
- **Status:** ✅ Completed

### Phase 1A — MyQode Forensic Analysis

- **Objective:** Reverse-engineer the MyQode application to extract protocol details
- **Dependencies:** Phase 1
- **Deliverables:** `QScout_MyQode_Forensic_Report.md`
- **Completion Criteria:** Protocol.js analyzed, RB packet format understood
- **Status:** ✅ Completed

### Phase 1B — Architecture & Protocol Verification

- **Objective:** Verify architecture assumptions and protocol behavior
- **Dependencies:** Phase 1A
- **Deliverables:** `QScout_Initial_Analysis_Report.md`
- **Completion Criteria:** Arduino firmware hypothesis formed, MicroPython discarded
- **Status:** ✅ Completed

### Phase 1C — Protocol Specification Extraction

- **Objective:** Extract complete RB protocol specification
- **Dependencies:** Phase 1B
- **Deliverables:** `QScout_RB_Protocol_Specification.md`
- **Completion Criteria:** Header, checksum, action codes, order ID documented
- **Status:** ✅ Completed

---

## Phase 2 — Protocol Validation

- **Objective:** Validate protocol specification against real robot behavior
- **Dependencies:** Phase 1C
- **Deliverables:** `QScout_Protocol_Validation_Report.md`
- **Completion Criteria:** Protocol behavior confirmed experimentally
- **Status:** ✅ Completed

---

## Phase 3 — Analysis & Consolidation

### Phase 3A — Firmware Analysis

- **Objective:** Analyze robot firmware to confirm architecture
- **Dependencies:** Phase 2
- **Deliverables:** `QScout_Firmware_Forensic_Report.md`
- **Completion Criteria:** Firmware identified as Arduino + ESP-IDF C++
- **Status:** ✅ Completed

### Phase 3B — Protocol Consolidation

- **Objective:** Consolidate all protocol knowledge into definitive documentation
- **Dependencies:** Phase 3A
- **Deliverables:** Response matching analysis, reference packets, observed differences
- **Completion Criteria:** All protocol documentation complete and consistent
- **Status:** ✅ Completed

### Phase 3C — Physical Validation

- **Objective:** Validate SDK behavior against physical robot
- **Dependencies:** Phase 3B
- **Deliverables:** `physical_validation_report.md`, regression tests
- **Completion Criteria:** LED, motor, move, buzzer, ultrasonic validated
- **Status:** ✅ Completed

---

## SDK-01 — Core SDK

- **Objective:** Implement core protocol and transport layers
- **Dependencies:** Phase 3C
- **Deliverables:**
  - `protocol.py` — RB protocol, Action enum, Port constants, 40+ builders, 20+ parsers
  - `connection.py` — UART transport with auto-detection
  - `packet.py` — RBPacket representation
  - `exceptions.py` — SDK exceptions
  - `__init__.py` — QScout facade
- **Completion Criteria:** 41 tests passing, architecture frozen
- **Status:** ✅ Completed (Frozen)

---

## SDK-02 Phase 1 — Command Layer

- **Objective:** Implement command abstraction and metadata layer
- **Dependencies:** SDK-01
- **Deliverables:**
  - `commands.py` — Command abstraction
  - `command_map.py` — 42 CommandDef definitions, 41 unique action codes
- **Completion Criteria:** Metadata layer complete, lookup tables functional
- **Status:** ✅ Completed

---

## SDK-02 Phase 2A — Public API

- **Objective:** Implement first public API methods
- **Dependencies:** SDK-02 Phase 1
- **Deliverables:**
  - `actuators.py` — LED, motor, move, buzzer payloads
  - `sensors.py` — Ultrasonic sensor payload and parser
  - Public methods: `led()`, `motor()`, `move()`, `stop()`, `buzzer()`, `get_ultrasonic()`
- **Completion Criteria:** First public API methods functional
- **Status:** ✅ Completed

---

## SDK-02 Phase 2B — Physical SDK Validation

- **Objective:** Validate SDK against physical robot
- **Dependencies:** SDK-02 Phase 2A
- **Deliverables:** Physical validation report, 119 tests passing
- **Completion Criteria:** All public API methods validated on real robot
- **Status:** ✅ Completed

---

## SDK-02 Phase 2C — Expand Public API

- **Objective:** Expand public API with additional documented commands
- **Dependencies:** SDK-02 Phase 2B
- **Deliverables:**
  - Information commands: GET_DEVICE_INFO, GET_INTERFACE_INFO, GET_ALL_INTERFACE_INFO, GET_MOTOR_INTERFACE_INFO
  - Sensor commands: Voltage, Button, Light, Gyroscope, Colour, Touch
  - Remaining actuator commands
- **Completion Criteria:** Additional commands implemented and tested
- **Status:** 🔄 In Progress

---

## SDK-03 — Full Coverage, CLI, Examples

- **Objective:** Complete protocol coverage, CLI interface, comprehensive examples
- **Dependencies:** SDK-02 Phase 2C
- **Deliverables:**
  - Complete command coverage
  - CLI tool for robot control
  - Comprehensive examples
  - Diagnostic tools
- **Completion Criteria:** All 43 protocol commands implemented, CLI functional
- **Status:** ⏳ Pending

---

## SDK-04 — BLE Backend

- **Objective:** Add Bluetooth Low Energy connectivity
- **Dependencies:** SDK-03
- **Deliverables:**
  - BLE transport layer
  - Async API
  - Connection management
- **Completion Criteria:** Robot controllable via BLE from Linux
- **Status:** ⏳ Pending

---

## SDK-05 — Scratch Backend

- **Objective:** Enable Scratch visual programming integration
- **Dependencies:** SDK-04
- **Deliverables:**
  - Scratch backend
  - Visual programming interface
- **Completion Criteria:** Robot controllable from Scratch
- **Status:** ⏳ Pending

---

## SDK-06 — ROS Integration

- **Objective:** Integrate with Robot Operating System
- **Dependencies:** SDK-05
- **Deliverables:**
  - ROS nodes
  - ROS messages/services
- **Completion Criteria:** Robot accessible as ROS node
- **Status:** ⏳ Pending

---

## SDK-07 — Version 1.0 / PyPI

- **Objective:** Release stable version 1.0 on PyPI
- **Dependencies:** SDK-06
- **Deliverables:**
  - PyPI package
  - Complete developer documentation
  - Installation guide
  - API reference
- **Completion Criteria:** `pip install qscout` works, documentation complete
- **Status:** ⏳ Pending

---

## Future Improvements (Post 1.0)

- Wi-Fi backend (if firmware allows)
- Multi-robot support
- Simulation environment
- Advanced motion planning
- Plugin architecture
