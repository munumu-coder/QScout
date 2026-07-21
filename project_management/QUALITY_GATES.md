# QUALITY_GATES.md — Mandatory Quality Gates

**Last Updated:** 2026-07-19

---

## Overview

No task may be marked complete until ALL quality gates pass. These gates are mandatory and cannot be bypassed.

---

## CORE ENGINEERING RULES

### RULE M-001: Metric Comparison Rule (MANDATORY)
> **NEVER compare numerical values until BOTH values have been proven to use EXACTLY the same metric definition.**
> Violating this rule invalidates the analysis.

**Workflow:**
1. Locate the canonical definition in `docs/METRIC_DEFINITIONS.md`.
2. Verify that both values use the **same definition**.
3. If definitions differ, **DO NOT COMPARE**. Classify as "Different Metric Definitions".
4. Only compare if definitions are **identical**.

**Violation Consequence:**
- Any report comparing metrics without verifying definitions is **invalid** and must be rejected.

---

## PERMANENT VALIDATION WORKFLOW

Every inconsistency analysis **MUST** execute this workflow:

### STEP 1: Identify the Metric
- Extract the exact wording from the document.

### STEP 2: Locate Its Canonical Definition
- Check `docs/METRIC_DEFINITIONS.md` for the metric.
- If the metric is undefined, **STOP** and propose a definition first.

### STEP 3: Verify Definitions Match
- Compare the document's definition with the canonical definition.
- If definitions differ:
  - **STOP**. Do NOT compare values.
  - Classify as **B) Different Metric Definitions**.

### STEP 4: Recompute the Metric from Repository
- Apply the **canonical definition** to the current repository.

### STEP 5: Compare Values (Only if Definitions Match)
- If the documented value **matches** the recomputed value → **Consistent**.
- If the documented value **differs** → Proceed to Step 6.

### STEP 6: Classify the Inconsistency
Use **exactly one** of these categories:

| **Category** | **Description** | **Example** |
|--------------|-----------------|-------------|
| **A) Real Repository Error** | The documented value is **factually incorrect** under the canonical definition. | Document says 21 commands have Dedicated Unit Tests, but recomputed value is 12. |
| **B) Different Metric Definitions** | The document uses a **different definition** than the canonical one. | Document includes `test_real_packets.py` as "Unit Tests". |
| **C) Historical Metric** | The metric refers to a **past state** of the repository. | Document from 2026-07-18 reports 145 tests (before T-FIX-01). |
| **D) Documentation Obsolete After Repository Evolution** | The documentation was correct **at the time of writing**, but the repository has since changed. | Document says 21 commands lack tests, but new tests were added. |
| **E) Intentional Difference** | The repository **intentionally** differs from a frozen baseline. | Baseline says architecture is frozen, but a justified improvement was approved. |

### STEP 7: Recommend Action
- **Category A**: Update the documentation to match the canonical metric.
- **Category B**: **DO NOT UPDATE**. Add a note clarifying the definition used.
- **Category C**: **DO NOT UPDATE**. Mark as "Historical Metric".
- **Category D**: Update the documentation **only if the metric is still relevant**.
- **Category E**: **DO NOT UPDATE**. Document the intentional difference.

---

## MANDATORY REPORT FORMAT

Every engineering report **MUST** include the following fields:

```markdown
# [Report Title] — Verification Report

**Date:** YYYY-MM-DD
**Analyst:** [Agent Role]
**Status:** [Draft/Final]
**Metric Under Analysis:** [e.g., M-010: Command Coverage (Dedicated Unit Test)]

---

## Definition Analysis

| **Field**               | **Value**                                                                 |
|-------------------------|---------------------------------------------------------------------------|
| Canonical Definition    | [Link to METRIC_DEFINITIONS.md section, e.g., M-010]                     |
| Document's Definition   | [Extract exact wording or infer from context]                            |
| Definitions Match?      | ✅ Yes / ❌ No                                                             |

---

## Repository Evidence

| **Field**               | **Value**                                                                 |
|-------------------------|---------------------------------------------------------------------------|
| Included Elements        | [List files/functions included in the metric]                           |
| Excluded Elements        | [List files/functions excluded]                                         |
| Calculation Method       | [Describe how the metric was computed]                                   |
| Computed Value          | [e.g., "12 (28.6%)"]                                                     |

---

## Consistency Classification

- **Category:** [A / B / C / D / E]
- **Justification:** [Explain why this category applies]

---

## Required Action

- **Action:** [Update Documentation / No Action / Add Clarification / Mark as Historical]
- **Files to Modify:** [List files, if applicable]
- **Priority:** [P1 / P2 / P3]
- **Evidence References:** [List repository files/lines used as evidence]
```

---

## METRIC REPORTING RULES

1. **All percentages must include their definition.**
   - ❌ Invalid: "Coverage is 50%."
   - ✅ Valid: "Command Coverage (Dedicated Unit Test) is 28.6% (12/42 commands with Dedicated Unit Tests)."

2. **All metrics must reference `METRIC_DEFINITIONS.md`.**

3. **Historical metrics must be marked explicitly.**
   - Example: "Historical Metric (2026-07-18): 145 tests (before T-FIX-01)."

---

## DOCUMENT HIERARCHY

Order of authority (highest to lowest):

1. **Repository source code** (`src/qscout/*.py`)
2. **Repository metadata** (`pyproject.toml`, `setup.cfg`, etc.)
3. **`docs/METRIC_DEFINITIONS.md`** (Canonical metric definitions)
4. **`project_management/QUALITY_GATES.md`** (This document)
5. **`project_management/CONTROL_CENTER.yaml`**
6. **`project_management/TASK_STATE.yaml`**
7. **Phase reports** (e.g., `docs/SDK_02_PHASE_2C_BASELINE.md`)
8. **Historical reports** (e.g., `docs/SDK_CAPABILITY_AUDIT.md`)

**Rule:** Lower levels **cannot** redefine metrics defined in higher levels.

---

## HISTORICAL METRIC RULES

1. **Historical documents are snapshots.**
   - They represent the state of the repository **at a specific point in time**.
   - They are **NOT bugs** simply because the repository has evolved.

2. **Preservation Rule:**
   - Historical documents **MUST NOT** be rewritten to match newer definitions.
   - Instead, mark them explicitly as:
     - `Historical Metric (YYYY-MM-DD)`
     - `Historical Snapshot (Phase X)`

3. **Clarification Rule:**
   - If a historical document uses a non-canonical definition, add a note:
     ```markdown
     **Note:** This metric uses a historical definition.
     See [M-XXX](#) in `docs/METRIC_DEFINITIONS.md` for the current canonical definition.
     ```

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
| [docs/checklists/code_review.md](docs/checklists/code_review.md) | Code review checklist |
| [docs/checklists/documentation_review.md](docs/checklists/documentation_review.md) | Documentation review checklist |
