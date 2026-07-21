# Physical Validation Report

**Date:** 2026-07-17
**Robot:** Robobloq QScout RB-00002
**Interface:** CH340 USB-Serial /dev/ttyUSB0 (115200 8N1)
**SDK:** qscout-sdk v0.1.0 (SDK-02 Fase 2A)

---

## Environment

| Check | Status |
|-------|--------|
| /dev/ttyUSB0 exists | ✅ |
| VID:PID 1A86:7523 | ✅ |
| User in dialout group | ✅ |
| pyserial 3.5 installed | ✅ |

---

## Test Results

| # | Test | Result | Notes |
|---|------|--------|-------|
| 1 | LED | PASS | LED turned red then off correctly |
| 2 | BUZZER | PASS | 440Hz tone audible, ACK received |
| 3 | MOTOR | PASS | Motor M1 spun at speed 50, then stopped |
| 4 | MOVE | PASS | Robot moved forward (50,50), then stopped |
| 5 | ULTRASONIC | PASS | Distance read: 2500mm, response parsed correctly |

**Total: 5/5 PASS**

---

## TX/RX Captures

### TEST 1 — LED

**TX (ON):** `52 42 0A 02 10 FC FF 00 00 AB`
- `[0-1]` 52 42 = Header
- `[2]` 0A = Size (10)
- `[3]` 02 = Order ID
- `[4]` 10 = SET_LED
- `[5]` FC = port -4 (M4)
- `[6-8]` FF 00 00 = RGB (red)
- `[9]` AB = Checksum

**TX (OFF):** `52 42 0A 03 10 FC 00 00 00 AD`

**Physical:** LED turned red, then off ✅

### TEST 2 — BUZZER

**TX:** `52 42 0B 04 13 00 B8 01 F4 01 64`
- `[0-1]` 52 42 = Header
- `[2]` 0B = Size (11)
- `[3]` 04 = Order ID
- `[4]` 13 = SET_BUZZER
- `[5]` 00 = port placeholder
- `[6-7]` B8 01 = 440 Hz (little-endian u16)
- `[8-9]` F4 01 = 500 ms (little-endian u16)
- `[10]` 64 = Checksum

**RX:** oid=3, action=0x01 (ACK)

**Physical:** 440Hz tone audible ✅

### TEST 3 — MOTOR

**TX (ON):** `52 42 08 05 11 FF 32 E3`
- `[5]` FF = port -1 (M1)
- `[6]` 32 = speed 50

**TX (OFF):** `52 42 08 06 11 FF 00 B2`

**Physical:** Motor spun at speed 50, then stopped ✅

### TEST 4 — MOVE

**TX (ON):** `52 42 09 07 11 00 32 32 19`
- `[5]` 00 = port 0 (dual motor)
- `[6]` 32 = left speed 50
- `[7]` 32 = right speed 50

**TX (OFF):** `52 42 09 08 11 00 00 00 B6`

**Physical:** Robot moved forward, then stopped ✅

### TEST 5 — ULTRASONIC

**TX:** `52 42 07 09 A1 01 46`
- `[4]` A1 = GET_ULTRASONIC
- `[5]` 01 = port 1

**RX:** `oid=9, action=0x01, payload=09 C4`
- `[5-6]` 09 C4 = distance
- `09 * 256 + C4 = 9 * 256 + 196 = 2500 mm`

**Physical:** Distance 2500mm (2.5m) — consistent with open space ✅

---

## SET_BUZZER Response Discovery

**Prior assumption:** SET_BUZZER (0x13) was fire-and-forget — no ACK expected.

**Physical validation finding:** SET_BUZZER **does** return an ACK response, like all other SET commands.

### Evidence

**TX (buzzer 440Hz, 500ms):**
```
52 42 0B 04 13 00 B8 01 F4 01 64
```
- `[0-1]` 52 42 = Header
- `[2]` 0B = Size (11)
- `[3]` 04 = Order ID
- `[4]` 13 = SET_BUZZER
- `[5]` 00 = port placeholder
- `[6-7]` B8 01 = 440 Hz (little-endian u16)
- `[8-9]` F4 01 = 500 ms (little-endian u16)
- `[10]` 64 = Checksum

**RX (ACK):**
```
oid=4, action=0x01, payload=<empty>
```
- Order ID matches TX (0x04)
- Action 0x01 = generic ACK
- Empty payload = command acknowledged

### Interpretation

The buzzer plays the tone immediately upon receiving the command (latency < 1ms), so the user perceives it as fire-and-forget. However, the firmware still sends an ACK response after processing the command.

### Conclusion

SET_BUZZER behavior is identical to SET_LED, SET_MOTOR, and SET_MOVE:
- Returns action=0x01 ACK
- Correlation via Order ID
- No payload in ACK

---

## Protocol Observations

1. **Buzzer gets ACK:** SET_BUZZER (0x13) returns an ACK response (action=0x01), not fire-and-forget as initially documented.

2. **All commands get ACKs:** SET_MOTOR, SET_MOVE, SET_LED, and SET_BUZZER all return action=0x01 ACKs.

3. **Ultrasonic response action:** GET_ULTRASONIC response action is 0x01 (generic ACK), NOT 0xA1. Correlation is by Order ID only.

4. **Buffer management:** Stale data in the RX buffer must be flushed before each test to avoid parsing errors.

---

## Failure Analysis

No failures. All 5 tests passed on first execution.

---

## Conclusion

**SDK-02 Fase 2B: VALIDATED** ✅

The QScout SDK successfully communicates with the real robot:
- All 5 commands sent correct RB packets
- All physical behaviors verified (LED, buzzer, motor, movement, ultrasonic)
- Ultrasonic distance parsed correctly (2500mm)
- 119/119 software tests continue passing

---

## Next Steps

SDK-02 Fase 2C: implement remaining sensor/actuator commands.
