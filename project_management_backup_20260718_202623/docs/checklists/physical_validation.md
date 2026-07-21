# Physical Validation Checklist

**Used by:** Programmer Agent
**When:** Validating SDK commands against physical robot

---

## Pre-Validation

- [ ] Robot connected via USB
- [ ] Serial port detected (`/dev/ttyUSB0`)
- [ ] Connection established at 115200 baud
- [ ] Auto-detection working (VID:PID 1A86:7523)

---

## Command Validation

For each command, verify:

### SET Commands

- [ ] Command sends correct packet format
- [ ] Header is `0x52 0x42`
- [ ] Checksum is correct
- [ ] Order ID is assigned correctly
- [ ] Robot responds with ACK (Action 0x01)
- [ ] Response Order ID matches request

### GET Commands

- [ ] Command sends correct packet format
- [ ] Header is `0x52 0x42`
- [ ] Checksum is correct
- [ ] Order ID is assigned correctly
- [ ] Robot responds with data
- [ ] Response Order ID matches request
- [ ] Payload is parsed correctly
- [ ] Values are in expected range

---

## Specific Command Validation

### LED

- [ ] LED turns on with correct color
- [ ] LED turns off correctly
- [ ] Port parameter works correctly
- [ ] RGB values are clamped (0-255)

### Motor

- [ ] Motor spins in correct direction
- [ ] Speed is clamped to ±100
- [ ] Port parameter works correctly
- [ ] Both motors work independently

### Move

- [ ] Robot moves forward
- [ ] Robot moves backward
- [ ] Robot turns left
- [ ] Robot turns right
- [ ] Left and right speeds are independent

### Buzzer

- [ ] Buzzer produces sound
- [ ] Frequency is correct
- [ ] Duration is correct
- [ ] Returns ACK (not fire-and-forget)

### Ultrasonic

- [ ] Distance reading is reasonable
- [ ] Units are millimeters
- [ ] Response is parsed correctly
- [ ] Big-endian values handled correctly

---

## Response Correlation

- [ ] Order ID tracking works
- [ ] Response matched to correct request
- [ ] Timeout handling works
- [ ] No stale responses

---

## Error Handling

- [ ] Invalid port handled gracefully
- [ ] Connection loss handled
- [ ] Timeout handled
- [ ] Invalid response handled

---

## Evidence Capture

- [ ] Log file saved
- [ ] Packets captured
- [ ] Screenshots/video taken (if applicable)
- [ ] Evidence stored in `evidence/` directory

---

## Validation Results

| Command | Status | Notes |
|---------|--------|-------|
| SET_LED | | |
| SET_MOTOR | | |
| SET_MOVE | | |
| SET_BUZZER | | |
| GET_ULTRASONIC | | |

---

## Validator

- **Agent:** Programmer
- **Date:** ___________
- **Task ID:** ___________
- **Robot Serial:** ___________
