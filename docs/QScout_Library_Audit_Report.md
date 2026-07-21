# QScout Library Audit Report

**Date:** 2026-07-17  
**Phase:** 3A.5 (Library Audit)  
**Status:** Complete — Ready for Phase 3B Physical Validation

---

## Executive Summary

The QScout Python library has been audited for correctness, robustness, and protocol compliance. All critical issues identified during the audit have been fixed. The library is now ready for physical validation with the Q-Scout robot.

---

## 1. Protocol Verification

### 1.1 Motor Speed Range

**Finding:** Motor speed range is **-100 to +100** (percentage of max PWM duty).

**Evidence:**
- Protocol.js `setMotor()` comment: `@param {any} speed 电机转速 (-100-100)`
- Arduino `QM_DCMOTORONBOARD.cpp`: `speed = constrain(speed, -100, 100);`
- JavaScript `gs_motion_move_base()`: Clamps to [-100, 100]

**Wire Encoding:** Signed Int8 (`writeInt8` in JS, `int8_t` semantics in C++)

**Fix Applied:** Added `_clamp_speed()` function that clamps to [-100, 100] (line 29).

### 1.2 Response Format

**Finding:** Response packets do NOT include the port byte. Data starts at offset 5.

**Evidence:**
- Protocol.js `parseUltrasonicValue()`: reads `buffer[5]` and `buffer[6]`
- Protocol.js `parseVoltage()`: reads `buffer[5]`
- Response format: `[RB 2B][length 1B][orderId 1B][action 1B][data N][checksum 1B]`

**Status:** Parsers were already correct. Test cases were fixed to match.

---

## 2. Code Quality Issues Fixed

### 2.1 protocol.py

| Issue | Status | Details |
|-------|--------|---------|
| `_clamp_signed8` defined after first use | **Fixed** | Moved to line 21 (before all uses) |
| Motor speed clamped to ±127 | **Fixed** | Now uses `_clamp_speed()` for ±100 |
| `build_set_out_engine` used inline clamping | **Fixed** | Now uses `_clamp_speed()` |

### 2.2 connection.py

| Issue | Status | Details |
|-------|--------|---------|
| Potential infinite loop in `receive()` | **Fixed** | Added `is_open` check and `SerialException` handling |
| No protection against serial disconnection | **Fixed** | Catches `SerialException` and `OSError` |
| Unbounded RX buffer growth | **Fixed** | Added `MAX_BUFFER_SIZE` (1024 bytes) limit |
| No error handling in `send()` | **Fixed** | Catches exceptions and raises `ConnectionError` |

---

## 3. Unit Tests

### 3.1 Test Coverage

Created 47 unit tests across two test files:

**test_protocol.py (36 tests):**
- Checksum calculation (4 tests)
- `_clamp_signed8` (2 tests)
- `_clamp_speed` (2 tests)
- Packet building (2 tests)
- Parse functions (6 tests)
- Packet extraction (4 tests)
- LED command building (2 tests)
- Motor command building (3 tests)
- Move command building (2 tests)
- Buzzer command building (1 test)
- Order manager (2 tests)
- Response parsing (5 tests)

**test_connection.py (11 tests):**
- Connection initialization (2 tests)
- Connection state management (5 tests)
- Receive functionality (2 tests)
- Port detection (2 tests)

### 3.2 Test Results

```
Ran 47 tests in 0.108s — OK
```

All tests pass. No failures or errors.

---

## 4. Architecture Review

### 4.1 Module Structure

```
qscout/
├── __init__.py      # QScout class, auto-detect, context manager
├── protocol.py      # RB protocol: Action enum, Port constants, builders, parsers
├── connection.py    # SerialConnection: open/close/send/receive/extract_packets
├── sensors.py       # Sensors class: 26 GET sensor methods
└── actuators.py     # Actuators class: 18 SET methods + convenience wrappers
```

### 4.2 Design Decisions

| Decision | Rationale |
|----------|-----------|
| Signed Int8 for port/speed | Matches Protocol.js `writeInt8` behavior |
| Speed clamped to ±100 | Matches firmware `constrain(speed, -100, 100)` |
| Port constants as negative values | Matches Protocol.js `ports` object |
| Buzzer port uses UInt8 (`B`) | Matches Protocol.js `writeUInt8` for buzzer port |
| Fire-and-forget for SET commands | Protocol does not send acknowledgments |
| Single-packet response assumption | GET commands always return one response |

---

## 5. Remaining Issues

### 5.1 Minor Issues (Non-blocking)

| Issue | Priority | Notes |
|-------|----------|-------|
| No integration tests | Low | Will be addressed in Phase 3B |
| No type hints for sensor return types | Low | Could improve IDE support |
| `tests/__init__.py` missing | Low | Not required for `unittest discover` |

### 5.2 Known Limitations

| Limitation | Impact |
|------------|--------|
| No reconnection logic | Must manually reconnect if serial drops |
| No thread safety | Not safe for concurrent access |
| No async support | Synchronous only |

---

## 6. Protocol Compliance Matrix

| Feature | Protocol.js | Our Library | Status |
|---------|-------------|-------------|--------|
| Header | `0x52 0x42` | `b'RB'` | ✅ Match |
| Checksum | `sum % 256` | `sum(data) % 256` | ✅ Match |
| Motor speed range | -100..100 | -100..100 | ✅ Match |
| Motor speed encoding | Int8 | Int8 | ✅ Match |
| Port encoding | Int8 | Int8 | ✅ Match |
| Buzzer port encoding | UInt8 | UInt8 | ✅ Match |
| Response format | No port in response | No port in response | ✅ Match |

---

## 7. Readiness Checklist

- [x] Motor speed range verified against Protocol.js
- [x] Motor speed range verified against Arduino firmware
- [x] Response format verified (no port byte in response)
- [x] `_clamp_signed8` moved before first use
- [x] `_clamp_speed` added for motor commands
- [x] `connection.py` infinite loop protection added
- [x] `connection.py` serial disconnection handling added
- [x] `connection.py` buffer size limit added
- [x] Unit tests created (47 tests, all passing)
- [x] Protocol compliance verified

---

## 8. Next Steps

1. **Phase 3B:** Physical validation with Q-Scout robot
   - Test motor control (forward, backward, turn)
   - Test sensor readings (ultrasonic, light, button)
   - Test LED and buzzer commands
   - Verify response parsing with real data

2. **Post-Phase 3B:**
   - Add integration tests
   - Add type hints for sensor return types
   - Consider async support if needed

---

## Appendix: Changes Made

### protocol.py

```python
# Added at line 21-29:
MAX_BUFFER_SIZE = 1024  # Prevent unbounded RX buffer growth

def _clamp_signed8(v: int) -> int:
    """Clamp *v* to the signed 8-bit range [-128, 127]."""
    return max(-128, min(127, v))

def _clamp_speed(v: int) -> int:
    """Clamp motor speed to [-100, 100] per protocol specification."""
    return max(-100, min(100, v))

# Updated motor functions to use _clamp_speed()
```

### connection.py

```python
# Updated receive() method:
def receive(self, timeout: float = 0.5) -> Optional[bytes]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            if not self.is_open:
                return None
            waiting = self._serial.in_waiting
            if waiting > 0:
                self._rx_buffer.extend(self._serial.read(waiting))
                if len(self._rx_buffer) > MAX_BUFFER_SIZE:
                    self._rx_buffer = self._rx_buffer[-MAX_BUFFER_SIZE:]
                packets, remaining = protocol.extract_packets(bytes(self._rx_buffer))
                self._rx_buffer = bytearray(remaining)
                if packets:
                    return packets[-1]
            else:
                time.sleep(0.005)
        except (serial.SerialException, OSError):
            self._serial = None
            return None
    return None

# Updated send() method:
def send(self, packet: bytes) -> None:
    try:
        self.write(packet)
    except (serial.SerialException, OSError):
        self._serial = None
        raise ConnectionError('Serial port disconnected during send')
```

### tests/test_protocol.py

- Created 36 unit tests covering checksum, clamping, packet building, parsing, extraction, and response parsing
- All tests pass

### tests/test_connection.py

- Created 11 unit tests covering initialization, state management, receive, and port detection
- All tests pass
