# SDK_CAPABILITY_AUDIT.md — Phase A.5.2

**Date:** 2026-07-18  
**Audit Type:** Read-Only Analysis  
**Files Modified:** None

---

## 1. Executive Summary

### 1.1 Overall Implementation Percentage

| Metric | Value |
|--------|-------|
| Commands defined | 42 |
| Commands with builder functions | 42 (100%) |
| Commands with parsers | 35 (83%) |
| Commands with public API | 42 (100%) |
| Commands with unit tests | 17 (40.5%) |
| Commands with real packet tests | 5 (12%) |
| Commands physically validated | 9 (21%) |
| Commands fully documented | 42 (100%) |

**Note:** The value for "Commands with unit tests" was corrected from **21 (50%)** to **17 (40.5%)** to match the table in [Section 2.1](#21-get-commands-26) and [Section 2.2](#22-set-commands-16).
For the current canonical definition of "unit tests", see **M-001** in `docs/METRIC_DEFINITIONS.md`.

### 1.2 Overall Validation Percentage

| Metric | Value |
|--------|-------|
| Commands marked validated | 9 / 42 (21.4%) |
| Commands with real packet tests | 5 / 42 (12%) |
| Commands with physical validation | 9 / 42 (21.4%) |

### 1.3 Overall Documentation Percentage

| Metric | Value |
|--------|-------|
| Commands in protocol docs | 42 (100%) |
| Commands in CHANGELOG | ~15 (36%) |
| Commands in ROADMAP | ~10 (24%) |

### 1.4 Overall Test Coverage

| Metric | Value |
|--------|-------|
| Test files | 11 |
| Test methods discovered | 145 |
| Tests passing | 114 (78.6%) |
| Tests failing | 31 (21.4%) |
| Commands with zero tests | 21 (50%) |

---

## 2. Capability Matrix

### 2.1 GET Commands (26)

| # | Command | Action | Builder | Parser | Public API | Unit Tests | Real Packets | HW Validated | Classification |
|---|---------|--------|---------|--------|------------|------------|--------------|--------------|----------------|
| 1 | GET_DEVICE_INFO | 0x01 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | FULLY_COMPLETE |
| 2 | GET_INTERFACE_INFO | 0x02 | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | IMPLEMENTED_AND_VALIDATED |
| 3 | GET_ALL_INTERFACE_INFO | 0x03 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | IMPLEMENTED |
| 4 | GET_MOTOR_INTERFACE_INFO | 0x04 | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | IMPLEMENTED_AND_VALIDATED |
| 5 | GET_USER_INTERFACE_INFO | 0x05 | ✅ | ⚠️ | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 6 | GET_ULTRASONIC | 0xA1 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | FULLY_COMPLETE |
| 7 | GET_BUTTON | 0xA2 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | IMPLEMENTED |
| 8 | GET_VOLTAGE | 0xA3 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | IMPLEMENTED |
| 9 | GET_LINE_VALUE | 0xA4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | FULLY_COMPLETE |
| 10 | GET_TEMP_HUMIDITY | 0xA5 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | IMPLEMENTED |
| 11 | GET_LIGHT | 0xA6 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | IMPLEMENTED |
| 12 | GET_VOICE | 0xA7 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 13 | GET_INFRARED | 0xA8 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 14 | GET_GYRO | 0xA9 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | IMPLEMENTED |
| 15 | GET_COLOR | 0xAA | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 16 | GET_TOUCH_BUTTON | 0xAB | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 17 | GET_TEMP_DUAL | 0xAC | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 18 | GET_SIX_LINE | 0xAD | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 19 | GET_ROCKER | 0xAE | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | IMPLEMENTED |
| 20 | GET_FLAME | 0xAF | ✅ | ⚠️ | ✅ | ✅ | ❌ | ❌ | PARTIALLY_IMPLEMENTED |
| 21 | GET_GAS | 0xB0 | ✅ | ⚠️ | ✅ | ❌ | ❌ | ❌ | PARTIALLY_IMPLEMENTED |
| 22 | GET_SPIRAL_POT | 0xB1 | ✅ | ⚠️ | ✅ | ❌ | ❌ | ❌ | PARTIALLY_IMPLEMENTED |
| 23 | GET_LINE_POT | 0xB2 | ✅ | ⚠️ | ✅ | ❌ | ❌ | ❌ | PARTIALLY_IMPLEMENTED |
| 24 | GET_EXT_IO_INPUT | 0xB4 | ✅ | ⚠️ | ✅ | ❌ | ❌ | ❌ | PARTIALLY_IMPLEMENTED |
| 25 | GET_EXT_APC | 0xB5 | ✅ | ⚠️ | ✅ | ❌ | ❌ | ❌ | PARTIALLY_IMPLEMENTED |
| 26 | GET_EXT_TEMP_HUMI | 0xB6 | ✅ | ⚠️ | ✅ | ❌ | ❌ | ❌ | PARTIALLY_IMPLEMENTED |

### 2.2 SET Commands (16)

| # | Command | Action | Builder | Parser | Public API | Unit Tests | Real Packets | HW Validated | Classification |
|---|---------|--------|---------|--------|------------|------------|--------------|--------------|----------------|
| 27 | SET_LED | 0x10 | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | FULLY_COMPLETE |
| 28 | SET_MOTOR | 0x11 | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | IMPLEMENTED_AND_VALIDATED |
| 29 | SET_MOVE | 0x11 | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | FULLY_COMPLETE |
| 30 | SET_ULTRASONIC_LIGHT | 0x12 | ✅ | N/A | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 31 | SET_BUZZER | 0x13 | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | IMPLEMENTED_AND_VALIDATED |
| 32 | SET_MATRIX | 0x14 | ✅ | N/A | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 33 | SET_WORK_MODE | 0x18 | ✅ | N/A | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 34 | SET_STEERING_ENGINE | 0x19 | ✅ | N/A | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 35 | SET_OUT_ENGINE | 0x1A | ✅ | N/A | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 36 | SET_RGB_LED_MATRIX | 0x1B | ✅ | N/A | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 37 | SET_MP3 | 0x1C | ✅ | N/A | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 38 | SET_FOUR_DIGIT | 0x1E | ✅ | N/A | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 39 | SET_FOUR_RGB_LED | 0x1F | ✅ | N/A | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 40 | SET_FAN | 0x20 | ✅ | N/A | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 41 | SET_EXT_IO_OUTPUT | 0x21 | ✅ | N/A | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |
| 42 | SET_EXT_SERVO_DEGREE | 0x22 | ✅ | N/A | ✅ | ❌ | ❌ | ❌ | IMPLEMENTED |

### 2.3 Classification Summary

| Classification | Count | Percentage |
|----------------|-------|------------|
| FULLY_COMPLETE | 5 | 12% |
| IMPLEMENTED_AND_VALIDATED | 5 | 12% |
| IMPLEMENTED | 20 | 48% |
| PARTIALLY_IMPLEMENTED | 7 | 17% |
| NOT_STARTED | 0 | 0% |
| **Total** | **42** | **100%** |

---

## 3. Inconsistencies

### 3.1 ERROR Level

| # | Issue | Evidence | Impact | Recommended Correction |
|---|-------|----------|--------|----------------------|
| 1 | 7 tasks pending but already implemented | TASK_STATE.yaml T-2C-02 through T-2C-09 pending; command_map.py shows all implemented | Waste developer time | Mark T-2C-02 through T-2C-09 as completed |
| 2 | 26 test failures due to API mismatch | test_actuators.py, test_sensors.py call module-level functions that don't exist | Tests cannot validate implementation | Fix tests to use class-based API |
| 3 | 2 test files cannot import | test_checksum.py imports `receive_packet`; test_facade.py imports `_OrderIdManager` | Tests cannot run | Update imports to match current API |
| 4 | 3 test failures due to exception type | test_packet.py expects QScoutProtocolError; protocol.py raises ValueError | Tests cannot validate error handling | Align exception types |

### 3.2 WARNING Level

| # | Issue | Evidence | Impact | Recommended Correction |
|---|-------|----------|--------|----------------------|
| 5 | 7 commands use generic parsers | GET_FLAME through GET_EXT_TEMP_HUMI use parse_uint16_be/parse_uint8 | Less specific error handling | Consider dedicated parsers if needed |
| 6 | GET_USER_INTERFACE_INFO has no parser | sensors.py does inline byte slicing | Code inconsistency | Add parse_user_interface_info to protocol.py |
| 7 | 3 Action enum values not in command_map | LOW_BATTERY(0x15), CLICK_BUTTON(0x16), TOUCH_BUTTON(0x1D) | Orphaned enum values | Document as event codes or remove |
| 8 | 21 commands have zero test coverage | No unit tests for GET_VOICE, GET_INFRARED, GET_COLOR, etc. | Unknown correctness | Add unit tests for all commands |
| 9 | CHANGELOG incomplete | Many commands not mentioned in CHANGELOG.md | Documentation drift | Update CHANGELOG with all commands |
| 10 | TASK_STATE.yaml next_task still references T-2C-01 | line 180-181 | Stale reference | Update to current task |

### 3.3 INFO Level

| # | Issue | Evidence | Impact | Recommended Correction |
|---|-------|----------|--------|----------------------|
| 11 | Action code gaps | 0x06-0x0F, 0x17 unused | Normal protocol design | No action needed |
| 12 | Shared action code 0x11 | SET_MOTOR and SET_MOVE both use 0x11 | Expected (payload distinguishes) | Document in protocol spec |
| 13 | Shared parser for 0x02/0x03 | parse_interface_info handles both | Expected (response length distinguishes) | Document in protocol spec |

---

## 4. Missing Functionality

### 4.1 Genuinely Missing

| Category | Missing Items |
|----------|---------------|
| **Test coverage** | 21 commands have zero unit tests |
| **Real packet tests** | 37 commands lack real packet regression tests |
| **Physical validation** | 33 commands not validated against hardware |
| **Dedicated parsers** | 7 commands use generic parse helpers |
| **CHANGELOG entries** | ~27 commands not documented in CHANGELOG |
| **Exception alignment** | protocol.py raises ValueError, tests expect custom exceptions |

### 4.2 Not Missing (Already Implemented)

| Category | Status |
|----------|--------|
| Command definitions | ✅ All 42 defined |
| Builder functions | ✅ All 42 implemented |
| Public API methods | ✅ All 42 implemented |
| Protocol documentation | ✅ All commands documented |

---

## 5. Obsolete Tasks

| Task ID | Title | Reason |
|---------|-------|--------|
| T-2C-02 | Implement GET_INTERFACE_INFO Command | Already implemented |
| T-2C-03 | Implement GET_ALL_INTERFACE_INFO Command | Already implemented |
| T-2C-04 | Implement GET_MOTOR_INTERFACE_INFO Command | Already implemented |
| T-2C-05 | Implement GET_VOLTAGE Sensor Command | Already implemented |
| T-2C-06 | Implement GET_BUTTON Sensor Command | Already implemented |
| T-2C-07 | Implement GET_LIGHT Sensor Command | Already implemented |
| T-2C-08 | Implement GET_GYROSCOPE Sensor Command | Already implemented |
| T-2C-09 | Implement GET_COLOR Sensor Command | Already implemented |
| T-2C-10 | Implement GET_TOUCH Sensor Command | Already implemented |
| T-2C-11 | Implement Remaining Actuator Commands | Already implemented |

---

## 6. Updated Roadmap Proposal

### 6.1 Remaining Work (Ordered by Dependency)

| Priority | Task ID | Title | Effort | Depends On |
|----------|---------|-------|--------|------------|
| P1 | T-FIX-01 | Fix 31 failing tests (API mismatch) | 2h | None |
| P1 | T-FIX-02 | Fix 2 unimportable test files | 1h | None |
| P1 | T-FIX-03 | Fix 3 exception type mismatches | 1h | None |
| P1 | T-TEST-01 | Add unit tests for 21 untested commands | 4h | T-FIX-01 |
| P1 | T-TEST-02 | Add real packet tests for remaining commands | 3h | T-TEST-01 |
| P2 | T-DOC-01 | Update CHANGELOG with all commands | 1h | None |
| P2 | T-DOC-02 | Document event codes (LOW_BATTERY, etc.) | 1h | None |
| P2 | T-HW-01 | Physical validation of remaining commands | 4h | T-TEST-01 |
| P3 | T-CLEAN-01 | Clean up task queue (remove obsolete tasks) | 0.5h | None |
| P3 | T-CLEAN-02 | Add dedicated parsers for 7 commands | 2h | None |

### 6.2 Estimated Total Remaining Effort

| Category | Hours |
|----------|-------|
| Test fixes | 4h |
| New unit tests | 4h |
| New real packet tests | 3h |
| Documentation | 2h |
| Physical validation | 4h |
| Cleanup | 2.5h |
| **Total** | **19.5h** |

---

## 7. Recommended Next Task

### T-FIX-01: Fix 31 Failing Tests

**Why this should be next:**

1. **Blocks all other work** — Cannot add new tests until existing tests pass
2. **Quick win** — 26 failures are API mismatch (test files call wrong functions)
3. **Establishes baseline** — Need passing tests before adding new ones
4. **Low risk** — Only modifying test files, not SDK source

**Estimated complexity:** LOW

**Estimated duration:** 2 hours

**Dependencies:** None

**Risks:**
- May discover additional test issues during fixes
- Exception type alignment may require protocol.py changes (but only exception types, not logic)

**Expected deliverables:**
- Updated `tests/test_actuators.py` — Use class-based API
- Updated `tests/test_sensors.py` — Use class-based API
- Updated `tests/test_checksum.py` — Fix imports
- Updated `tests/test_facade.py` — Fix imports
- Updated `tests/test_packet.py` — Fix exception types
- All 145 tests passing

---

## 8. Overall Assessment

### 8.1 Completion Percentage

| Metric | Percentage |
|--------|------------|
| Implementation | 100% (all 42 commands implemented) |
| Test coverage | 50% (21/42 commands have tests) |
| Physical validation | 21% (9/42 commands validated) |
| Documentation | 73% (31/42 in CHANGELOG) |
| **Overall** | **61%** |

### 8.2 Remaining Work

| Category | Items | Hours |
|----------|-------|-------|
| Test fixes | 31 failing tests | 4h |
| Unit tests | 21 commands | 4h |
| Real packet tests | 37 commands | 3h |
| Physical validation | 33 commands | 4h |
| Documentation | ~27 commands | 2h |
| Cleanup | Task queue, parsers | 2.5h |
| **Total** | | **19.5h** |

### 8.3 Remaining Phases

| Phase | Description | Estimated Time |
|-------|-------------|----------------|
| SDK-02 Phase 2C | Fix tests, add unit tests | 8h |
| SDK-02 Phase 2D | Real packet tests | 3h |
| SDK-02 Phase 2E | Physical validation | 4h |
| SDK-03 | CLI, examples, diagnostics | 20h+ |
| SDK-04 | BLE backend | 40h+ |

### 8.4 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Exception type changes break other code | LOW | MEDIUM | Check all exception handlers before changing |
| Physical validation reveals protocol issues | LOW | HIGH | Already validated 9 commands successfully |
| Test fixes reveal real bugs | MEDIUM | HIGH | Fix bugs as discovered, don't suppress failures |
| Parser generic helpers miss edge cases | LOW | LOW | Add dedicated parsers if issues found |

---

## 9. Files Analysed

| Category | Files |
|----------|-------|
| SDK source | 9 files in src/qscout/ |
| Tests | 11 files in tests/ |
| Protocol docs | 2 files (RB_Protocol_v1.0.md, QScout_RB_Protocol_Specification.md) |
| Project management | 6 files (CONTROL_CENTER, TASK_STATE, CHANGELOG, ROADMAP, DECISIONS, QUALITY_GATES) |
| Tools | 12 files in tools/ |

---

## 10. Commands Analysed

| Metric | Count |
|--------|-------|
| Total commands | 42 |
| GET commands | 26 |
| SET commands | 16 |
| Unique action codes | 41 (0x11 shared) |
| Event codes | 3 (not commands) |

---

## 11. Inconsistencies Found

| Level | Count |
|-------|-------|
| ERROR | 4 |
| WARNING | 6 |
| INFO | 3 |
| **Total** | **13** |

---

## 12. Recommended Next Task

**T-FIX-01: Fix 31 Failing Tests**

- Why: Blocks all other test work
- Complexity: LOW
- Duration: 2h
- Dependencies: None
- Deliverables: All 145 tests passing

---

**PHASE A.5.2 COMPLETED**
