# DECISIONS.md — Architectural Decision Log

---

## D-001: Native Python SDK

- **Date:** 2026-07-01
- **Description:** Develop a native Python SDK instead of using existing tools
- **Motivation:** MyQode requires Windows; need Linux-native solution
- **Alternatives Considered:**
  - Use Wine to run MyQode on Linux
  - Use existing Arduino libraries via serial
  - Develop native Python SDK
- **Consequences:** Full control over protocol implementation, no dependency on proprietary software
- **Status:** Accepted and implemented

---

## D-002: RB Protocol Direct Implementation

- **Date:** 2026-07-07
- **Description:** Implement RB protocol directly rather than emulating MyQode behavior
- **Motivation:** RB protocol is well-documented and simple; direct implementation is cleaner
- **Alternatives Considered:**
  - Emulate MyQode serial traffic
  - Implement RB protocol directly
- **Consequences:** Cleaner architecture, easier maintenance, protocol-level control
- **Status:** Accepted and implemented

---

## D-003: Arduino/ESP-IDF Firmware (Not MicroPython)

- **Date:** 2026-07-09
- **Description:** Firmware is native C++ Arduino, not MicroPython
- **Motivation:** Evidence from firmware analysis (k2x.bin) showed Arduino Core + ESP-IDF
- **Alternatives Considered:**
  - MicroPython with frozen modules
  - Native Arduino/ESP-IDF C++
- **Consequences:** No REPL access, no runtime introspection, deterministic command processing
- **Status:** Accepted (evidence-based)

---

## D-004: Strict Layer Separation

- **Date:** 2026-07-13
- **Description:** Maintain strict separation between protocol, transport, and application layers
- **Motivation:** Clean architecture, testability, transport independence
- **Alternatives Considered:**
  - Monolithic design
  - Strict layer separation
- **Consequences:** More files, but each module has single responsibility; easier to test and maintain
- **Status:** Accepted and enforced

---

## D-005: Order ID for Response Correlation

- **Date:** 2026-07-17
- **Description:** Responses are correlated exclusively by Order ID, not by Action Code
- **Motivation:** Physical validation showed request action codes differ from response action codes
- **Alternatives Considered:**
  - Match responses by action code
  - Match responses by order ID
- **Consequences:** All response handling must track order IDs; action codes in responses are informational only
- **Status:** Accepted (experimentally confirmed)

---

## D-006: Checksum Before Parsing

- **Date:** 2026-07-13
- **Description:** Always validate checksum before parsing packet content
- **Motivation:** Prevent processing corrupted data
- **Alternatives Considered:**
  - Parse first, validate later
  - Validate checksum before parsing
- **Consequences:** Failed checksums result in packet rejection; no partial parsing
- **Status:** Accepted and enforced

---

## D-007: Auto-Detection via VID:PID

- **Date:** 2026-07-15
- **Description:** Auto-detect robot connection using CH340 VID:PID (1A86:7523)
- **Motivation:** User should not need to specify port manually
- **Alternatives Considered:**
  - Require explicit port specification
  - Auto-detect via VID:PID with description fallback
- **Consequences:** Plug-and-play experience; fallback to description matching if VID:PID unavailable
- **Status:** Accepted and implemented

---

## D-008: Fire-and-Forget for SET_MOVE Only

- **Date:** 2026-07-17
- **Description:** Only SET_MOVE variants are fire-and-forget; SET_BUZZER returns ACK
- **Motivation:** Physical validation corrected previous assumption
- **Alternatives Considered:**
  - All SET commands are fire-and-forget
  - SET_BUZZER is fire-and-forget
  - Only SET_MOVE is fire-and-forget
- **Consequences:** SET_BUZZER must wait for response; SET_MOVE does not
- **Status:** Accepted (experimentally confirmed)

---

## D-009: Architecture Frozen at SDK-01

- **Date:** 2026-07-13
- **Description:** Core architecture is frozen; future work extends capabilities, not redesigns
- **Motivation:** Architecture is clean, tested, and validated
- **Alternatives Considered:**
  - Allow architecture evolution
  - Freeze architecture
- **Consequences:** All future work must fit within existing layer structure
- **Status:** Accepted and enforced

---

## D-010: Evidence-Driven Development

- **Date:** 2026-07-01
- **Description:** Never implement undocumented behavior; physical validation overrides assumptions
- **Motivation:** Prevent incorrect implementations based on incomplete information
- **Alternatives Considered:**
  - Implement based on documentation only
  - Evidence-driven development
- **Consequences:** Slower but more reliable; all assumptions must be validated
- **Status:** Accepted and enforced
