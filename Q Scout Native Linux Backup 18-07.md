# Q-Scout Native Linux SDK — Complete Project Backup & Handover

**Project:** Robobloq Q-Scout (RB-00002) Native Linux SDK

**Document Version:** 2.0

**Date:** July 2026

**Current Status:** SDK-02 Phase 2B Completed and Physically Validated

**Purpose**

This document is intended to provide a complete technical handover of the project so that another AI assistant or developer can immediately continue development without reconstructing previous work.

It summarizes the architecture, discoveries, implementation status, validation, roadmap and project history.

---

# 1. Project Objective

Develop a fully native Python SDK capable of controlling the Robobloq Q-Scout (RB-00002) robot from Ubuntu/Linux without requiring Windows or the proprietary MyQode software.

The SDK is intended to become the reference implementation of the Q-Scout communication protocol.

Long-term goals include:

* Native Python SDK
* Scratch support
* BLE backend
* ROS integration
* CLI utilities
* Diagnostic tools
* PyPI package

---

# 2. Reverse Engineering Status

The reverse engineering phase is considered **complete**.

The following has been experimentally confirmed.

## Hardware

Robot

Robobloq Q-Scout RB-00002

Main MCU

ESP32

USB Interface

CH340

VID:PID

1A86:7523

UART

115200 baud

8N1

Linux Device

/dev/ttyUSB0

---

## Firmware

Confirmed

* Native C++
* Arduino Core
* ESP-IDF v3.3.5

Discarded

* MicroPython
* Frozen modules
* REPL
* WebREPL
* OTA
* WiFi application layer

The firmware behaves as a deterministic command processor implementing the RB protocol.

---

# 3. Communication Architecture

```text
Linux Application
        │
        ▼
Native Python SDK
        │
        ▼
RB Protocol
        │
        ▼
USB / UART
        │
        ▼
ESP32 Firmware
        │
        ▼
Robot Hardware
```

BLE support exists in the official ecosystem but is outside the scope of the current SDK.

---

# 4. RB Protocol

Packet format

```text
Header
Length
Order ID
Action
Payload
Checksum
```

Header

```text
52 42
```

ASCII

```text
RB
```

Checksum

```text
sum(all bytes except checksum) % 256
```

Length represents the complete packet size.

---

# 5. Response Correlation

One of the most important discoveries.

Responses are **never matched using Action Codes.**

Responses are matched **only through Order ID.**

Example

Request

```text
Action A1
Order 09
```

Response

```text
Action 01
Order 09
```

This behaviour has been confirmed through:

* Protocol.js
* Arduino firmware
* Serial captures
* Physical robot validation

---

# 6. Physical Validation

The SDK successfully communicates with the real robot.

Validated commands

| Command        | Status |
| -------------- | ------ |
| SET_LED        | PASS   |
| SET_MOTOR      | PASS   |
| SET_MOVE       | PASS   |
| SET_BUZZER     | PASS   |
| GET_ULTRASONIC | PASS   |

Ultrasonic reading

2500 mm

Confirmed

* checksum
* packet parser
* payload decoding
* Order ID tracking
* big-endian values

---

# 7. Important Discovery

Previous documentation stated

SET_BUZZER was fire-and-forget.

Physical validation demonstrated this was incorrect.

Actual behaviour

SET_BUZZER returns an ACK response (Action 0x01).

Documentation has been updated.

Currently only SET_MOVE variants remain fire-and-forget according to the available evidence.

---

# 8. SDK Architecture

Project

```text
qscout-sdk/
```

Current structure

```text
qscout-sdk/

qscout/

    __init__.py
    connection.py
    protocol.py
    packet.py
    exceptions.py
    command_map.py
    commands.py
    actuators.py
    sensors.py

tests/

examples/

docs/

README.md

pyproject.toml
```

---

# 9. SDK-01 (Completed)

Implemented

* RBPacket
* Generic packet builder
* Generic packet parser
* Checksum
* UART connection
* Exceptions
* receive_packet()
* QScout facade

Status

Frozen

41 tests completed.

---

# 10. SDK-02 Phase 1 (Completed)

Implemented

* CommandDef
* CommandType
* Command abstraction
* Lookup tables
* Metadata layer

42 CommandDef definitions

41 unique Action Codes

Special case

Action 0x11 represents both

* SET_MOTOR
* SET_MOVE

The firmware distinguishes them through payload structure.

Architecture remains cleanly separated.

---

# 11. SDK-02 Phase 2A (Completed)

Implemented public API

```python
robot.led()

robot.motor()

robot.move()

robot.stop()

robot.buzzer()

robot.get_ultrasonic()
```

Implemented payload builders

* SET_LED
* SET_MOTOR
* SET_MOVE
* SET_BUZZER
* GET_ULTRASONIC

Order IDs

2 → 254 → 2

Order ID 0 remains reserved for unsolicited firmware reports.

---

# 12. SDK-02 Phase 2B (Completed)

Physical validation.

Real packets captured.

Validated

* LED
* Motor
* Move
* Buzzer
* Ultrasonic

Generated

physical_validation_report.md

SDK communicates reliably with the physical robot.

---

# 13. Command Coverage

Protocol

43 conceptual commands

41 unique Action Codes

Current SDK

42 CommandDef objects

Experimentally validated

10 commands

Pending validation

33 commands

Reason

Missing external hardware modules.

---

# 14. Separation of Responsibilities

connection.py

UART transport only.

protocol.py

Generic RB protocol only.

packet.py

Packet representation.

command_map.py

Command metadata.

commands.py

Command abstraction.

actuators.py

Payload builders for actuator commands.

sensors.py

Payload builders and response parsers.

**init**.py

Facade exposed to users.

Architecture follows strict separation of concerns.

---

# 15. Tests

Current result

119 tests

All passing.

Coverage

* checksum
* parser
* packet builder
* connection
* commands
* metadata
* actuators
* sensors
* facade

---

# 16. Documentation

Current documentation includes

* Architecture Reference Manual
* RB Protocol Specification
* Firmware Forensic Report
* Physical Validation Report
* Coverage Report
* Response Matching Analysis
* Reference Packets
* Release Notes

All documentation has been synchronized with the latest physical validation.

---

# 17. Current Project Status

Reverse Engineering

Completed

Protocol Reconstruction

Completed

Firmware Analysis

Completed

Architecture Reconstruction

Completed

Python SDK Core

Completed

Initial Public API

Completed

Physical Validation

Completed

Documentation

Completed

---

# 18. Next Recommended Phase

SDK-02 Phase 2C

Objective

Expand the public API by implementing additional commands already documented in the protocol.

Suggested order

Information commands

* GET_DEVICE_INFO
* GET_INTERFACE_INFO
* GET_ALL_INTERFACE_INFO
* GET_MOTOR_INTERFACE_INFO

Sensors

* Voltage
* Button
* Light
* Gyroscope
* Colour
* Touch

Remaining actuators

No architectural redesign should be performed.

Only SDK capabilities should be expanded.

---

# 19. Long-Term Roadmap

SDK-03

Complete protocol coverage

CLI

Examples

Diagnostics

SDK-04

BLE backend

Async API

SDK-05

Scratch backend

Visual programming

SDK-06

ROS integration

SDK-07

Version 1.0

PyPI publication

Complete developer documentation

---

# 20. Engineering Rules

The following rules govern the entire project.

1.

Evidence-driven development.

Never implement undocumented behaviour.

2.

Physical validation always overrides assumptions.

3.

Protocol layer must remain transport-independent.

4.

Transport layer must never know protocol details.

5.

Responses are correlated exclusively by Order ID.

6.

Checksum must always be validated before parsing.

7.

Packet header is always

```text
52 42
```

8.

The SDK architecture is considered stable.

Future work should extend capabilities, not redesign the core.

---

# 21. Final State

The project has successfully transitioned from reverse engineering to platform development.

The robot architecture has been reconstructed with high confidence.

The protocol has been documented, implemented and physically validated.

The SDK is capable of controlling the real robot from Ubuntu using native Python.

Future work should focus on expanding functionality rather than discovering protocol behaviour.

---

# Appendix A — Project Timeline

| Approximate Date | Phase                                         | Status      | Main Result                                                                                                  |
| ---------------- | --------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------ |
| Early July 2026  | **Phase 0 — Initial Idea**                    | ✅ Completed | Decision to control Q-Scout from Ubuntu without Windows or MyQode.                                           |
| Early July 2026  | **Phase 1 — Robot Knowledge**                 | ✅ Completed | Hardware identification (ESP32, CH340, UART), communication analysis, MyQode investigation.                  |
| Mid July 2026    | **Phase 2 — Reverse Engineering**             | ✅ Completed | RB protocol reconstructed, packet format, checksum, Action Codes, Order ID mechanism documented.             |
| Mid July 2026    | **Phase 3A — Firmware Analysis**              | ✅ Completed | Firmware identified as native Arduino + ESP-IDF; MicroPython hypothesis discarded.                           |
| Mid July 2026    | **Phase 3B — Protocol Consolidation**         | ✅ Completed | Protocol documentation, response matching analysis, reference packets and forensic reports completed.        |
| Mid July 2026    | **Phase 3C — Physical Validation**            | ✅ Completed | Real robot validation confirmed protocol behaviour and corrected undocumented assumptions.                   |
| Mid July 2026    | **SDK-01 — Core SDK**                         | ✅ Completed | Core library implemented (packet, protocol, connection, exceptions, facade). Frozen after review (41 tests). |
| Mid July 2026    | **SDK-02 Phase 1 — Command Layer**            | ✅ Completed | Command metadata layer implemented (CommandDef, Command abstraction, lookup tables).                         |
| Mid July 2026    | **SDK-02 Phase 2A — Public API**              | ✅ Completed | First public robot API: LED, motor, move, buzzer and ultrasonic sensor.                                      |
| Mid July 2026    | **SDK-02 Phase 2B — Physical SDK Validation** | ✅ Completed | SDK successfully controlled the physical robot. 119/119 tests passing.                                       |
| Mid July 2026    | **Documentation Update**                      | ✅ Completed | Documentation corrected after discovering that SET_BUZZER returns ACK instead of being fire-and-forget.      |

---

# Appendix B — Current Development Starting Point

A new developer or AI should assume the following:

* Reverse engineering is finished.
* The protocol is considered stable.
* The architecture is frozen.
* The SDK core is production-quality.
* Physical communication has been validated.
* The next development task is **SDK-02 Phase 2C**, expanding the public API with additional documented commands while preserving the existing architecture.

