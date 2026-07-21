# TASK_QUEUE.md — Project Task Queue

**Last Updated:** 2026-07-18

---

## Legend

| Priority | Meaning |
|----------|---------|
| P0 | Critical — Blocks other work |
| P1 | High — Next in line |
| P2 | Medium — Planned |
| P3 | Low — Nice to have |

| Status | Meaning |
|--------|---------|
| Pending | Not started |
| In Progress | Actively working |
| Blocked | Waiting on dependency |
| Review | Under audit review |
| Completed | Done and verified |

---

## Active Tasks (SDK-02 Phase 2C)

### T-2C-01: Implement GET_DEVICE_INFO Command

| Field | Value |
|-------|-------|
| ID | T-2C-01 |
| Title | Implement GET_DEVICE_INFO Command |
| Description | Add command to retrieve device information from the robot |
| Priority | P1 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | None |
| Estimated Effort | 2 hours |
| Required Verification | Unit tests, code review |
| Acceptance Criteria | Command implemented, tests passing, documentation updated |

---

### T-2C-02: Implement GET_INTERFACE_INFO Command

| Field | Value |
|-------|-------|
| ID | T-2C-02 |
| Title | Implement GET_INTERFACE_INFO Command |
| Description | Add command to retrieve interface information from the robot |
| Priority | P1 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | None |
| Estimated Effort | 2 hours |
| Required Verification | Unit tests, code review |
| Acceptance Criteria | Command implemented, tests passing, documentation updated |

---

### T-2C-03: Implement GET_ALL_INTERFACE_INFO Command

| Field | Value |
|-------|-------|
| ID | T-2C-03 |
| Title | Implement GET_ALL_INTERFACE_INFO Command |
| Description | Add command to retrieve all interface information from the robot |
| Priority | P1 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | None |
| Estimated Effort | 3 hours |
| Required Verification | Unit tests, code review |
| Acceptance Criteria | Command implemented, tests passing, documentation updated |

---

### T-2C-04: Implement GET_MOTOR_INTERFACE_INFO Command

| Field | Value |
|-------|-------|
| ID | T-2C-04 |
| Title | Implement GET_MOTOR_INTERFACE_INFO Command |
| Description | Add command to retrieve motor interface information from the robot |
| Priority | P1 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | None |
| Estimated Effort | 2 hours |
| Required Verification | Unit tests, code review |
| Acceptance Criteria | Command implemented, tests passing, documentation updated |

---

### T-2C-05: Implement GET_VOLTAGE Sensor Command

| Field | Value |
|-------|-------|
| ID | T-2C-05 |
| Title | Implement GET_VOLTAGE Sensor Command |
| Description | Add sensor command to read voltage from the robot |
| Priority | P1 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | None |
| Estimated Effort | 2 hours |
| Required Verification | Unit tests, code review |
| Acceptance Criteria | Command implemented, tests passing, documentation updated |

---

### T-2C-06: Implement GET_BUTTON Sensor Command

| Field | Value |
|-------|-------|
| ID | T-2C-06 |
| Title | Implement GET_BUTTON Sensor Command |
| Description | Add sensor command to read button state from the robot |
| Priority | P1 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | None |
| Estimated Effort | 2 hours |
| Required Verification | Unit tests, code review |
| Acceptance Criteria | Command implemented, tests passing, documentation updated |

---

### T-2C-07: Implement GET_LIGHT Sensor Command

| Field | Value |
|-------|-------|
| ID | T-2C-07 |
| Title | Implement GET_LIGHT Sensor Command |
| Description | Add sensor command to read light sensor from the robot |
| Priority | P1 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | None |
| Estimated Effort | 2 hours |
| Required Verification | Unit tests, code review |
| Acceptance Criteria | Command implemented, tests passing, documentation updated |

---

### T-2C-08: Implement GET_GYROSCOPE Sensor Command

| Field | Value |
|-------|-------|
| ID | T-2C-08 |
| Title | Implement GET_GYROSCOPE Sensor Command |
| Description | Add sensor command to read gyroscope data from the robot |
| Priority | P2 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | None |
| Estimated Effort | 3 hours |
| Required Verification | Unit tests, code review |
| Acceptance Criteria | Command implemented, tests passing, documentation updated |

---

### T-2C-09: Implement GET_COLOR Sensor Command

| Field | Value |
|-------|-------|
| ID | T-2C-09 |
| Title | Implement GET_COLOR Sensor Command |
| Description | Add sensor command to read color sensor from the robot |
| Priority | P2 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | None |
| Estimated Effort | 3 hours |
| Required Verification | Unit tests, code review |
| Acceptance Criteria | Command implemented, tests passing, documentation updated |

---

### T-2C-10: Implement GET_TOUCH Sensor Command

| Field | Value |
|-------|-------|
| ID | T-2C-10 |
| Title | Implement GET_TOUCH Sensor Command |
| Description | Add sensor command to read touch sensor from the robot |
| Priority | P2 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | None |
| Estimated Effort | 2 hours |
| Required Verification | Unit tests, code review |
| Acceptance Criteria | Command implemented, tests passing, documentation updated |

---

### T-2C-11: Implement Remaining Actuator Commands

| Field | Value |
|-------|-------|
| ID | T-2C-11 |
| Title | Implement Remaining Actuator Commands |
| Description | Add remaining actuator commands documented in the protocol |
| Priority | P2 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | None |
| Estimated Effort | 4 hours |
| Required Verification | Unit tests, code review |
| Acceptance Criteria | All actuator commands implemented, tests passing, documentation updated |

---

### T-2C-12: Add Unit Tests for New Commands

| Field | Value |
|-------|-------|
| ID | T-2C-12 |
| Title | Add Unit Tests for New Commands |
| Description | Write comprehensive unit tests for all new commands |
| Priority | P1 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | T-2C-01, T-2C-02, T-2C-03, T-2C-04, T-2C-05, T-2C-06, T-2C-07, T-2C-08, T-2C-09, T-2C-10, T-2C-11 |
| Estimated Effort | 6 hours |
| Required Verification | All tests passing, coverage report |
| Acceptance Criteria | All new commands have tests, all tests pass, coverage ≥ 90% |

---

### T-2C-13: Update Documentation for New API Methods

| Field | Value |
|-------|-------|
| ID | T-2C-13 |
| Title | Update Documentation for New API Methods |
| Description | Update README, CHANGELOG, and API documentation |
| Priority | P1 |
| Status | Pending |
| Assigned Agent | Auditor |
| Dependencies | T-2C-12 |
| Estimated Effort | 3 hours |
| Required Verification | Documentation review |
| Acceptance Criteria | README updated, CHANGELOG updated, API docs complete |

---

### T-2C-14: Physical Validation of New Commands

| Field | Value |
|-------|-------|
| ID | T-2C-14 |
| Title | Physical Validation of New Commands |
| Description | Validate new commands against physical robot (if hardware available) |
| Priority | P2 |
| Status | Pending |
| Assigned Agent | Programmer |
| Dependencies | T-2C-12 |
| Estimated Effort | 4 hours |
| Required Validation | Physical robot test |
| Acceptance Criteria | All new commands validated on real robot, evidence captured |

---

## Summary Table (Active Tasks)

| ID | Title | Priority | Agent | Status | Effort |
|----|-------|----------|-------|--------|--------|
| T-2C-01 | GET_DEVICE_INFO | P1 | Programmer | Pending | 2h |
| T-2C-02 | GET_INTERFACE_INFO | P1 | Programmer | Pending | 2h |
| T-2C-03 | GET_ALL_INTERFACE_INFO | P1 | Programmer | Pending | 3h |
| T-2C-04 | GET_MOTOR_INTERFACE_INFO | P1 | Programmer | Pending | 2h |
| T-2C-05 | GET_VOLTAGE | P1 | Programmer | Pending | 2h |
| T-2C-06 | GET_BUTTON | P1 | Programmer | Pending | 2h |
| T-2C-07 | GET_LIGHT | P1 | Programmer | Pending | 2h |
| T-2C-08 | GET_GYROSCOPE | P2 | Programmer | Pending | 3h |
| T-2C-09 | GET_COLOR | P2 | Programmer | Pending | 3h |
| T-2C-10 | GET_TOUCH | P2 | Programmer | Pending | 2h |
| T-2C-11 | Remaining Actuators | P2 | Programmer | Pending | 4h |
| T-2C-12 | Unit Tests | P1 | Programmer | Pending | 6h |
| T-2C-13 | Documentation Update | P1 | Auditor | Pending | 3h |
| T-2C-14 | Physical Validation | P2 | Programmer | Pending | 4h |

**Total Estimated Effort:** 40 hours

---

## Completed Tasks

| ID | Title | Priority | Agent | Status | Completion Date |
|----|-------|----------|-------|--------|-----------------|
| T-001 | Phase 0 — Initial idea and feasibility | P0 | — | Completed | 2026-07-01 |
| T-002 | Phase 1 — Robot hardware identification | P0 | — | Completed | 2026-07-03 |
| T-003 | Phase 1A — MyQode forensic analysis | P0 | — | Completed | 2026-07-05 |
| T-004 | Phase 1B — Architecture verification | P0 | — | Completed | 2026-07-06 |
| T-005 | Phase 1C — Protocol specification extraction | P0 | — | Completed | 2026-07-07 |
| T-006 | Phase 2 — Protocol validation | P0 | — | Completed | 2026-07-08 |
| T-007 | Phase 3A — Firmware analysis | P0 | — | Completed | 2026-07-09 |
| T-008 | Phase 3B — Protocol consolidation | P0 | — | Completed | 2026-07-10 |
| T-009 | Phase 3C — Physical validation | P0 | — | Completed | 2026-07-11 |
| T-010 | SDK-01 — Core SDK implementation | P0 | Programmer | Completed | 2026-07-13 |
| T-011 | SDK-01 — Core SDK tests (41 tests) | P0 | Programmer | Completed | 2026-07-13 |
| T-012 | SDK-02 Phase 1 — Command layer | P0 | Programmer | Completed | 2026-07-14 |
| T-013 | SDK-02 Phase 2A — Public API | P0 | Programmer | Completed | 2026-07-15 |
| T-014 | SDK-02 Phase 2B — Physical validation | P0 | Programmer | Completed | 2026-07-17 |
| T-015 | SDK-02 Phase 2B — Test expansion (119 tests) | P0 | Programmer | Completed | 2026-07-17 |
| T-016 | Documentation consolidation | P1 | Auditor | Completed | 2026-07-18 |

---

## Backlog (SDK-03+)

| ID | Title | Priority | Phase | Status |
|----|-------|----------|-------|--------|
| T-030 | CLI interface implementation | P1 | SDK-03 | Backlog |
| T-031 | Complete command coverage | P1 | SDK-03 | Backlog |
| T-032 | Comprehensive examples | P2 | SDK-03 | Backlog |
| T-033 | Diagnostic tools | P2 | SDK-03 | Backlog |
| T-040 | BLE transport layer | P1 | SDK-04 | Backlog |
| T-041 | Async API | P2 | SDK-04 | Backlog |
| T-050 | Scratch backend | P2 | SDK-05 | Backlog |
| T-060 | ROS integration | P3 | SDK-06 | Backlog |
| T-070 | PyPI package | P1 | SDK-07 | Backlog |
| T-071 | Developer documentation | P1 | SDK-07 | Backlog |

---

## Task Assignment Rules

1. Only Coordinator assigns tasks (see [AGENT_COORDINATOR.md](AGENT_COORDINATOR.md))
2. Programmer only works on assigned tasks (see [AGENT_PROGRAMMER.md](AGENT_PROGRAMMER.md))
3. Auditor reviews completed tasks (see [AGENT_AUDITOR.md](AGENT_AUDITOR.md))
4. All task completions update [PROJECT_STATE.md](PROJECT_STATE.md)
5. All task completions update [CHANGELOG.md](CHANGELOG.md)
6. Workflow details in [AGENT_WORKFLOW.md](AGENT_WORKFLOW.md)

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [START_HERE.md](START_HERE.md) | Entry point for new agents |
| [PROJECT_STATE.md](PROJECT_STATE.md) | Current project status |
| [TASK_STATE.yaml](TASK_STATE.yaml) | Live execution state |
| [ROADMAP.md](ROADMAP.md) | Complete project roadmap |
| [DECISIONS.md](DECISIONS.md) | Architectural decisions |
| [CHANGELOG.md](CHANGELOG.md) | Project history |
| [AGENT_MANIFEST.md](AGENT_MANIFEST.md) | Agent definitions |
| [AGENT_WORKFLOW.md](AGENT_WORKFLOW.md) | Agent communication protocol |
| [CURRENT_STATUS.yaml](CURRENT_STATUS.yaml) | Machine-readable state |
| [PROJECT_OPERATING_SYSTEM.md](PROJECT_OPERATING_SYSTEM.md) | Operating procedures |
| [COORDINATOR_DASHBOARD.md](COORDINATOR_DASHBOARD.md) | Daily dashboard |
| [PROJECT_INDEX.md](PROJECT_INDEX.md) | Master index |
