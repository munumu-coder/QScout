# AGENT_WORKFLOW.md — Agent Communication Protocol

**Last Updated:** 2026-07-18

---

## Overview

This document defines the official communication workflow for all future development in the Q-Scout project. All agents must follow this protocol.

---

## Official Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    1. COORDINATOR                           │
│  • Read PROJECT_STATE.md                                    │
│  • Read TASK_STATE.yaml                                     │
│  • Select next task from TASK_QUEUE.md                      │
│  • Assign to Programmer                                     │
│  • Update TASK_STATE.yaml                                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    2. PROGRAMMER                             │
│  • Receive task assignment                                  │
│  • Read relevant documentation                              │
│  • Implement changes in src/qscout/                         │
│  • Write unit tests                                         │
│  • Report completion to Coordinator                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    3. AUTOMATIC TESTS                        │
│  • Execute test suite                                       │
│  • Verify all tests pass                                    │
│  • Report results                                           │
│  • If FAIL → return to Step 2 (Programmer fixes)            │
│  • If PASS → proceed to Step 4                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    4. AUDITOR                                │
│  • Receive review request from Coordinator                  │
│  • Review code using docs/checklists/code_review.md         │
│  • Check test coverage                                      │
│  • Review documentation using docs/checklists/              │
│  • Report findings to Coordinator                           │
│  • If REVISION REQUIRED → return to Step 2                  │
│  • If APPROVED → proceed to Step 5                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    5. DOCUMENTATION UPDATE                   │
│  • Auditor updates documentation                            │
│  • Update CHANGELOG.md                                      │
│  • Update README.md (if public API changed)                 │
│  • Update relevant docs/ files                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    6. CURRENT_STATUS.yaml UPDATE             │
│  • Coordinator updates CURRENT_STATUS.yaml                  │
│  • Update test count                                        │
│  • Update last run date                                     │
│  • Update phase status                                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    7. TASK_STATE.yaml UPDATE                 │
│  • Coordinator updates TASK_STATE.yaml                      │
│  • Move task to completed_tasks                             │
│  • Update current_task to next task                         │
│  • Update pending_tasks                                     │
│  • Update last_completed                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    8. COORDINATOR APPROVAL                   │
│  • Review all updates                                       │
│  • Verify consistency                                       │
│  • Update PROJECT_STATE.md                                  │
│  • Mark task as completed in TASK_QUEUE.md                  │
│  • Task complete                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Transition Details

### Transition 1→2: Coordinator Assigns Task

**Trigger:** Task selected from TASK_QUEUE.md
**Action:** Coordinator assigns task to Programmer
**Documents Updated:** TASK_STATE.yaml
**Criteria:** Dependencies satisfied, task matches current phase

### Transition 2→3: Programmer Reports Completion

**Trigger:** Programmer finishes implementation
**Action:** Automatic test suite executes
**Command:**
```bash
cd /home/munumu/Qscout
PYTHONPATH=src python3 -m unittest discover -s tests
```
**Criteria:** All 119+ tests pass

### Transition 3→4: Tests Pass

**Trigger:** All tests pass
**Action:** Coordinator requests Auditor review
**Documents Updated:** TASK_STATE.yaml (status: review)
**Criteria:** Test results show 0 failures

### Transition 4→5: Auditor Approves

**Trigger:** Auditor approves code review
**Action:** Documentation update begins
**Documents Updated:** CHANGELOG.md, README.md, docs/
**Criteria:** No critical or major issues found

### Transition 5→6: Documentation Complete

**Trigger:** All documentation updated
**Action:** CURRENT_STATUS.yaml updated
**Documents Updated:** CURRENT_STATUS.yaml
**Criteria:** All documentation consistent

### Transition 6→7: Status Updated

**Trigger:** CURRENT_STATUS.yaml current
**Action:** TASK_STATE.yaml updated
**Documents Updated:** TASK_STATE.yaml
**Criteria:** All fields current

### Transition 7→8: State Updated

**Trigger:** TASK_STATE.yaml current
**Action:** Coordinator final approval
**Documents Updated:** PROJECT_STATE.md, TASK_QUEUE.md
**Criteria:** All updates consistent and complete

---

## Rollback Conditions

### Rollback from Step 3 to Step 2

**Condition:** Tests fail
**Action:** Programmer must fix before proceeding
**No documentation changes rolled back**

### Rollback from Step 4 to Step 2

**Condition:** Auditor finds critical or major issues
**Action:** Programmer must fix issues
**Documentation changes may need to be reverted**

### Rollback from Step 5 to Step 2

**Condition:** Documentation review reveals issues
**Action:** Programmer fixes code, documentation re-updated
**All documentation changes reverted**

### Full Rollback

**Condition:** Regression detected after task completion
**Action:**
1. Revert all code changes
2. Revert all documentation changes
3. Revert CURRENT_STATUS.yaml
4. Revert TASK_STATE.yaml
5. Revert PROJECT_STATE.md
6. Revert TASK_QUEUE.md
7. Reassign task with updated requirements

---

## Failure Handling

### Test Failure (Step 3)

1. Test suite reports failures
2. Programmer receives failure report
3. Programmer investigates and fixes
4. Return to Step 3 (re-run tests)
5. Repeat until tests pass

### Review Failure (Step 4)

1. Auditor finds issues
2. Auditor reports to Coordinator
3. Coordinator assigns fixes to Programmer
4. Programmer implements fixes
5. Return to Step 3 (re-run tests)
6. Auditor re-reviews
7. Repeat until approved

### Documentation Failure (Step 5)

1. Documentation review finds issues
2. Auditor fixes documentation
3. Verify documentation consistency
4. Proceed to Step 6

### Blocker (Any Step)

1. Agent reports blocker to Coordinator
2. Coordinator assesses impact
3. If resolvable: Coordinator provides guidance
4. If not resolvable: Escalate to human
5. Task marked as blocked in TASK_STATE.yaml

---

## Approval Criteria

### Programmer Completion (Step 2→3)

- [ ] All code changes implemented
- [ ] All unit tests written
- [ ] Code follows project conventions
- [ ] No known issues

### Test Pass (Step 3→4)

- [ ] All tests pass
- [ ] No regressions
- [ ] Test count ≥ 119

### Auditor Approval (Step 4→5)

- [ ] Code review checklist complete
- [ ] No critical issues
- [ ] No major issues (or approved with notes)
- [ ] Test coverage adequate
- [ ] Documentation accurate

### Documentation Complete (Step 5→6)

- [ ] CHANGELOG.md updated
- [ ] README.md updated (if needed)
- [ ] All docs/ files current
- [ ] Cross-references valid

### Status Update (Step 6→7)

- [ ] CURRENT_STATUS.yaml current
- [ ] All fields accurate
- [ ] YAML syntax valid

### State Update (Step 7→8)

- [ ] TASK_STATE.yaml current
- [ ] Task moved to completed
- [ ] Next task identified

### Final Approval (Step 8)

- [ ] PROJECT_STATE.md updated
- [ ] TASK_QUEUE.md updated
- [ ] All documents consistent
- [ ] No contradictions

---

## Escalation Procedure

Escalate to human when:

1. Architecture change is requested
2. Blocker cannot be resolved by agents
3. Risk materializes (see PROJECT_STATE.md)
4. Rule violation detected
5. Conflict between agents cannot be resolved
6. Decision requires human judgment

**Escalation Format:**
```
ESCALATION
- Issue: [description]
- Impact: [what is affected]
- Step: [current workflow step]
- Attempted solutions: [what was tried]
- Recommendation: [suggested resolution]
- Urgency: [P0/P1/P2/P3]
```

---

## Document References

| Document | Role in Workflow |
|----------|------------------|
| [START_HERE.md](START_HERE.md) | Entry point for new agents |
| [PROJECT_STATE.md](PROJECT_STATE.md) | Current status (read by all) |
| [PROJECT_OPERATING_SYSTEM.md](PROJECT_OPERATING_SYSTEM.md) | Operating procedures |
| [TASK_QUEUE.md](TASK_QUEUE.md) | Task assignments (managed by Coordinator) |
| [DECISIONS.md](DECISIONS.md) | Architecture decisions (read by all) |
| [CHANGELOG.md](CHANGELOG.md) | History (updated at Step 5) |
| [PROJECT_RULES.md](PROJECT_RULES.md) | Rules (enforced by Coordinator) |
| [AGENT_MANIFEST.md](AGENT_MANIFEST.md) | Agent definitions and boundaries |
| [AGENT_COORDINATOR.md](AGENT_COORDINATOR.md) | Coordinator detailed spec |
| [AGENT_PROGRAMMER.md](AGENT_PROGRAMMER.md) | Programmer detailed spec |
| [AGENT_AUDITOR.md](AGENT_AUDITOR.md) | Auditor detailed spec |
| [AGENT_VALIDATOR.md](AGENT_VALIDATOR.md) | Validator detailed spec |
| [CURRENT_STATUS.yaml](CURRENT_STATUS.yaml) | Machine-readable state (updated at Step 6) |
| [TASK_STATE.yaml](TASK_STATE.yaml) | Live execution state (updated at Step 7) |
| [HANDOVER_PROTOCOL.md](HANDOVER_PROTOCOL.md) | New agent onboarding |
| [QUALITY_GATES.md](QUALITY_GATES.md) | Mandatory quality gates |
| [COORDINATOR_DASHBOARD.md](COORDINATOR_DASHBOARD.md) | Daily dashboard |
| [PROJECT_INDEX.md](PROJECT_INDEX.md) | Master index |
| [docs/checklists/](docs/checklists/) | Review checklists for Auditor |
| [templates/](templates/) | Document templates |
| [sessions/](sessions/) | Session management |
