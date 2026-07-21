# SDK-02 Phase 2C — Resumption Report

**Date:** 2026-07-18  
**Agent:** opencode (Programmer)  
**Status:** ANALYSIS COMPLETE — Ready for implementation

---

## 1. Executive Summary

SDK-02 Phase 2C ("Expand Public API") has been resumed after the multi-agent infrastructure completion and repository consolidation. The canonical repository is `/home/munumu/Qscout` with all modules merged from the archived `/home/munumu/qscout-sdk`.

**Current test status:** 145 tests run, **31 errors**, 0 failures  
**Root cause:** Architecture mismatch — migrated test files expect a function-based API; the canonical source uses a class-based API.

---

## 2. Repository Status

| Item | Status |
|------|--------|
| Canonical repo | `/home/munumu/Qscout` |
| Source modules | 9 modules in `src/qscout/` |
| Test files | 11 files in `tests/` |
| Documentation | 24 files in `docs/` |
| Git status | Not a git repo (pre-existing) |
| Python | 3.12.3 |
| Backups | `backups/Qscout_20260718_121744.tar.gz` (1.8MB) |

### Modules in `src/qscout/`

| Module | Architecture | Layer |
|--------|-------------|-------|
| `__init__.py` | Class-based `QScout` facade | SDK-02 |
| `connection.py` | Class-based `Connection` | SDK-01 |
| `protocol.py` | Monolith (626 lines) + compat aliases | SDK-01 |
| `packet.py` | Class-based `RBPacket` | SDK-01 |
| `command_map.py` | 42 `CommandDef` + lookup tables | SDK-02 |
| `commands.py` | `Command` abstraction | SDK-02 |
| `exceptions.py` | 4 typed exceptions | SDK-01 |
| `actuators.py` | Class-based `Actuators` | SDK-02 |
| `sensors.py` | Class-based `Sensors` | SDK-02 |

---

## 3. T-FIX-01 Analysis — 31 Errors

### 3.1 Error Breakdown

| File | Errors | Root Cause |
|------|--------|------------|
| `test_actuators.py` | 19 | Calls `actuators.led()`, `actuators.motor()`, `actuators.move()`, `actuators.buzzer()` — module has no such functions |
| `test_sensors.py` | 7 | Calls `sensors.get_ultrasonic()`, `sensors.parse_ultrasonic_response()` — module has no such functions |
| `test_packet.py` | 3 | `RBPacket.from_bytes()` doesn't validate header; `parse_packet` exception types differ |
| `test_checksum.py` | 1 (import) | Imports `calculate_checksum` (doesn't exist, `sum_check` exists) and `receive_packet` (doesn't exist) |
| `test_facade.py` | 1 (import) | Imports `_OrderIdManager` from `qscout.__init__` (doesn't exist) |

### 3.2 Architecture Mismatch Detail

The **migrated tests** (from SDK repo) expect a **function-based API** where:

```python
# Expected by tests:
from qscout import actuators
cmd = actuators.led(port=-4, r=255, g=0, b=0)  # returns Command
cmd = actuators.motor(port=-1, speed=80)         # returns Command
cmd = actuators.move(left_speed=50, right_speed=50)  # returns Command
cmd = actuators.buzzer(frequency=440, duration_ms=500)  # returns Command
```

The **actual source** has a **class-based API** where:

```python
# Actual implementation:
from qscout.actuators import Actuators
a = Actuators(connection)
a.led(port=-4, r=255, g=0, b=0)     # returns None (sends directly)
a.motor(port=-1, speed=80)           # returns None (sends directly)
```

**Key differences:**
1. Tests expect **module-level functions** returning `Command` objects; source has **class methods** returning `None`
2. Tests expect **no connection required**; source requires an open `Connection`
3. Tests expect **validation in the function** (e.g., `ValueError` for out-of-range); source validates at send-time
4. `sensors.get_ultrasonic()` returns `Command`; `Sensors.ultrasonic()` returns `int | None`

### 3.3 Recommended Fix Strategy

The tests represent the **target public API** (function-based, Command-returning). Two approaches:

**Option A — Rewrite tests to match current class-based API** (Recommended)
- Pros: Preserves the working class-based architecture
- Cons: Loses the Command abstraction tests; tests become integration-only
- Effort: Low (straightforward adaptation)

**Option B — Add function-based wrappers to modules**
- Add module-level functions like `get_ultrasonic(port=1) -> Command` that create Command objects
- Pros: Preserves both APIs; tests work as-is
- Cons: Adds complexity; two APIs to maintain
- Effort: Medium (add ~20 wrapper functions + `parse_ultrasonic_response`)

**Option C — Refactor to function-based architecture**
- Rewrite `sensors.py` and `actuators.py` as pure function modules
- Pros: Matches test expectations exactly
- Cons: Loses the class-based architecture that was physically validated; breaks the `QScout` facade
- Effort: High (major refactor)

---

## 4. Additional Issues Found

### 4.1 Missing Functions in `protocol.py`

`test_checksum.py` imports functions that don't exist:
- `calculate_checksum` — protocol.py has `sum_check` instead (the SDK repo used `calculate_checksum`)
- `receive_packet` — not defined in protocol.py

### 4.2 Missing `_OrderIdManager`

`test_facade.py` imports `_OrderIdManager` from `qscout.__init__` — this class doesn't exist. The facade uses `OrderManager` from `protocol.py`.

### 4.3 `RBPacket.from_bytes` Validation Gap

`test_packet.py:39-41` expects `QScoutProtocolError` for invalid headers, but `RBPacket.from_bytes` doesn't validate headers — it delegates to `parse_packet` which only checks length and checksum.

---

## 5. Pending Task Queue

| ID | Title | Priority | Depends On | Status |
|----|-------|----------|------------|--------|
| T-FIX-01 | Fix 31 failing tests (API mismatch) | P1 | — | Pending |
| T-FIX-02 | Fix 2 unimportable test files | P1 | — | Pending |
| T-FIX-03 | Fix 3 exception type mismatches | P1 | T-FIX-01 | Pending |
| T-TEST-01 | Add unit tests for 21 untested commands | P1 | T-FIX-01/02/03 | Pending |
| T-TEST-02 | Add real packet tests for remaining commands | P1 | T-TEST-01 | Pending |
| T-DOC-01 | Update CHANGELOG with all commands | P2 | — | Pending |
| T-HW-01 | Physical validation of remaining commands | P2 | T-TEST-01 | Pending |

### Recommended Execution Order

1. **T-FIX-01 + T-FIX-02 + T-FIX-03** — Consolidate into a single fix session
   - Decide on Option A/B/C above
   - Fix import errors (test_checksum, test_facade)
   - Fix exception type mismatches
2. **T-TEST-01** — Add unit tests for remaining commands
3. **T-TEST-02** — Add real packet tests
4. **T-DOC-01** — Update CHANGELOG
5. **T-HW-01** — Physical validation

---

## 6. Risk Assessment

| Risk | Severity | Likelihood | Impact |
|------|----------|------------|--------|
| API mismatch fix breaks physically-validated commands | High | Low | Option A/B preserve existing validated code |
| `protocol.py` refactor introduces regressions | Medium | Medium | 114 existing tests provide safety net |
| Missing functions cause cascading import errors | Low | High | Already contained in 2 test files |
| Physical validation invalidated by code changes | High | Low | Only if Option C chosen; avoid this |

---

## 7. Conclusion

The SDK-02 Phase 2C resumption is well-defined. The 31 errors are all caused by a single architecture mismatch between migrated tests (function-based) and canonical source (class-based). The fix is straightforward once the API strategy is decided.

**Recommendation:** Adopt **Option B** (add function-based wrappers) to preserve both APIs and make the migrated tests pass without rewriting them. This also aligns with the project's stated goal of providing a public API for the SDK.
