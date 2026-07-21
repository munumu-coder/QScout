# QUALITY_GATES.md — Mandatory Quality Gates

**Last Updated:** 2026-07-18

---

## Overview

No task may be marked complete until ALL quality gates pass. These gates are mandatory and cannot be bypassed.

---

## Gate 1: Programming Completed

**Owner:** Programmer
**Verification:** Self-declared

### Criteria

- [ ] All code changes implemented
- [ ] All unit tests written
- [ ] Code follows project conventions
- [ ] No known issues
- [ ] No debug code left in

### Verification

Programmer declares completion and provides:
- Files modified list
- Tests added/modified list
- Implementation notes

---

## Gate 2: Tests PASS

**Owner:** Validator
**Verification:** Automated

### Criteria

- [ ] All unit tests pass
- [ ] 0 failures
- [ ] Test count ≥ 119 (or increased)

### Verification

```bash
cd /home/munumu/Qscout
PYTHONPATH=src python3 -m unittest discover -s tests
```

**Result:** PASS or FAIL

---

## Gate 3: Validator PASS

**Owner:** Validator
**Verification:** Automated

### Criteria

- [ ] Unit tests PASS (Gate 2)
- [ ] Project structure valid
- [ ] YAML syntax valid
- [ ] Markdown syntax valid
- [ ] Documentation links valid
- [ ] State files consistent
- [ ] Repository consistent

### Verification

Validator executes all checks from `AGENT_VALIDATOR.md`

**Result:** PASS or FAIL

---

## Gate 4: Auditor PASS

**Owner:** Auditor
**Verification:** Manual review

### Criteria

- [ ] Code review checklist complete (docs/checklists/code_review.md)
- [ ] No critical issues
- [ ] No major issues (or approved with notes)
- [ ] Test coverage adequate
- [ ] Documentation accurate
- [ ] Conventions followed

### Verification

Auditor completes review and provides findings report

**Result:** APPROVED or REVISION REQUIRED

---

## Gate 5: Documentation Updated

**Owner:** Auditor / Coordinator
**Verification:** Manual review

### Criteria

- [ ] CHANGELOG.md updated
- [ ] README.md updated (if public API changed)
- [ ] All docs/ files current
- [ ] Cross-references valid
- [ ] No broken links

### Verification

Auditor completes documentation review from `docs/checklists/documentation_review.md`

**Result:** APPROVED or REVISION REQUIRED

---

## Gate 6: Coordinator Approval

**Owner:** Coordinator
**Verification:** Final approval

### Criteria

- [ ] Gate 1: Programming completed ✅
- [ ] Gate 2: Tests PASS ✅
- [ ] Gate 3: Validator PASS ✅
- [ ] Gate 4: Auditor PASS ✅
- [ ] Gate 5: Documentation updated ✅
- [ ] All state files updated
- [ ] No contradictions between documents

### Verification

Coordinator reviews all gates and approves

**Result:** APPROVED or REVISION REQUIRED

---

## Gate Flow

```
┌─────────────────────────────────────────────────────────────┐
│  GATE 1: Programming Completed                              │
│  Owner: Programmer                                          │
│  Status: [ ] Pending / [ ] Complete                         │
└─────────────────────┬─────────────────────────────────────┘
                      │ PASS
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  GATE 2: Tests PASS                                         │
│  Owner: Validator                                           │
│  Status: [ ] Pending / [ ] PASS / [ ] FAIL                  │
└─────────────────────┬─────────────────────────────────────┘
                      │ PASS
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  GATE 3: Validator PASS                                     │
│  Owner: Validator                                           │
│  Status: [ ] Pending / [ ] PASS / [ ] FAIL                  │
└─────────────────────┬─────────────────────────────────────┘
                      │ PASS
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  GATE 4: Auditor PASS                                       │
│  Owner: Auditor                                             │
│  Status: [ ] Pending / [ ] APPROVED / [ ] REVISION REQUIRED │
└─────────────────────┬─────────────────────────────────────┘
                      │ APPROVED
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  GATE 5: Documentation Updated                              │
│  Owner: Auditor / Coordinator                               │
│  Status: [ ] Pending / [ ] APPROVED / [ ] REVISION REQUIRED │
└─────────────────────┬─────────────────────────────────────┘
                      │ APPROVED
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  GATE 6: Coordinator Approval                               │
│  Owner: Coordinator                                         │
│  Status: [ ] Pending / [ ] APPROVED / [ ] REVISION REQUIRED │
└─────────────────────────────────────────────────────────────┘
                      │ APPROVED
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  TASK COMPLETE                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Failure Handling

### Gate 2 Failure (Tests FAIL)

1. Validator reports FAIL
2. Coordinator notifies Programmer
3. Programmer investigates and fixes
4. Return to Gate 2

### Gate 3 Failure (Validator FAIL)

1. Validator reports FAIL with details
2. Coordinator notifies Programmer
3. Programmer fixes issues
4. Return to Gate 2

### Gate 4 Failure (Auditor REVISION REQUIRED)

1. Auditor reports issues
2. Coordinator notifies Programmer
3. Programmer implements fixes
4. Return to Gate 2

### Gate 5 Failure (Documentation REVISION REQUIRED)

1. Auditor reports documentation issues
2. Auditor fixes documentation
3. Return to Gate 5

### Gate 6 Failure (Coordinator REVISION REQUIRED)

1. Coordinator identifies inconsistencies
2. Coordinator assigns fixes to appropriate agent
3. Return to relevant gate

---

## Gate Tracking

Track gate status in TASK_STATE.yaml:

```yaml
active_task:
  id: "T-2C-01"
  gates:
    gate_1_programming: "pending"
    gate_2_tests: "pending"
    gate_3_validator: "pending"
    gate_4_auditor: "pending"
    gate_5_documentation: "pending"
    gate_6_coordinator: "pending"
```

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [AGENT_VALIDATOR.md](AGENT_VALIDATOR.md) | Validator agent spec |
| [AGENT_WORKFLOW.md](AGENT_WORKFLOW.md) | Communication protocol |
| [PROJECT_OPERATING_SYSTEM.md](PROJECT_OPERATING_SYSTEM.md) | Operating procedures |
| [docs/checklists/code_review.md](docs/checklists/code_review.md) | Code review checklist |
| [docs/checklists/documentation_review.md](docs/checklists/documentation_review.md) | Documentation review checklist |
