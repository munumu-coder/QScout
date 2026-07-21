# NEXT_SESSION.md — Next Session Preparation

**Last Updated:** 2026-07-20

---

## Next Task

| Field | Value |
|-------|-------|
| Task ID | T-FIX-04 |
| Title | Fix 3 failing tests (1 failure, 2 errors) |
| Priority | P1 |
| Assigned Agent | Programmer |

---

## Prerequisites

- [ ] Read START_HERE.md
- [ ] Read CONTROL_CENTER.yaml
- [ ] Read TASK_STATE.yaml
- [ ] Read DECISIONS.md
- [ ] Run test suite to reproduce failures

---

## Expected Deliverables

1. All 143 tests passing (0 failures, 0 errors)
2. No changes to protocol or production code behavior
3. Test suite command: `PYTHONPATH=src python3 -m unittest discover -s tests`

---

## Relevant Documents

| Document | Purpose |
|----------|---------|
| CONTROL_CENTER.yaml | Project context |
| TASK_STATE.yaml | Task details |
| START_HERE.md | Project overview |
| DECISIONS.md | Architectural decisions |

---

## Context

The project is in SDK-03 — Full Coverage. All sensor and actuator commands are already implemented. The immediate priority is fixing the 3 test failures before adding new tests.

---

## Notes

SDK-02 Phase 2C is complete. Do NOT recreate deleted modules (packet.py, commands.py, command_map.py).
