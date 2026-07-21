# PROJECT_OPERATING_SYSTEM.md — Project Brain

**Last Updated:** 2026-07-18

---

## Overview

This document describes HOW the Q-Scout project operates. It does NOT describe the SDK. It defines the operating procedures for autonomous multi-agent coordination.

---

## Project Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT START                             │
│  • Read START_HERE.md                                        │
│  • Load CURRENT_STATUS.yaml                                  │
│  • Load TASK_STATE.yaml                                      │
│  • Determine current phase                                   │
│  • Initialize agents                                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    PHASE EXECUTION                           │
│  • Execute task loop                                         │
│  • Complete all phase tasks                                  │
│  • Validate phase deliverables                              │
│  • Update documentation                                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    PHASE TRANSITION                          │
│  • Verify phase completion criteria                         │
│  • Update ROADMAP.md                                         │
│  • Update PROJECT_STATE.md                                   │
│  • Initialize next phase                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT COMPLETION                        │
│  • All phases completed                                      │
│  • Release preparation                                       │
│  • Final documentation                                       │
│  • Project archive                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Startup Sequence

When a new AI agent joins the project:

```
┌─────────────────────────────────────────────────────────────┐
│  1. READ START_HERE.md                                       │
│     • Understand project overview                            │
│     • Identify next steps                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  2. READ CURRENT_STATUS.yaml                                 │
│     • Load project state                                     │
│     • Identify current phase                                 │
│     • Check blockers                                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  3. READ TASK_STATE.yaml                                     │
│     • Load execution state                                   │
│     • Identify current task                                  │
│     • Check agent assignments                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  4. DETERMINE ROLE                                           │
│     • Read AGENT_MANIFEST.md                                 │
│     • Read role-specific document                            │
│     • Understand permissions                                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  5. BEGIN WORK                                               │
│     • Follow AGENT_WORKFLOW.md                               │
│     • Execute assigned tasks                                 │
│     • Update state files                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Shutdown Sequence

When an AI agent session ends:

```
┌─────────────────────────────────────────────────────────────┐
│  1. SAVE SESSION STATE                                       │
│     • Update sessions/CURRENT_SESSION.md                     │
│     • Record progress                                        │
│     • Note any blockers                                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  2. UPDATE STATE FILES                                       │
│     • Update TASK_STATE.yaml                                 │
│     • Update CURRENT_STATUS.yaml                             │
│     • Update sessions/SESSION_HISTORY.md                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  3. PREPARE HANDOVER                                         │
│     • Update sessions/NEXT_SESSION.md                        │
│     • Document current state                                 │
│     • List pending tasks                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  4. FINALIZE                                                 │
│     • Verify all updates are consistent                      │
│     • Run validation checks                                  │
│     • Report completion                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Task Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    TASK SELECTION                            │
│  Input: TASK_STATE.yaml                                      │
│  Process:                                                   │
│    • Read pending_tasks                                      │
│    • Check dependencies                                      │
│    • Select highest priority                                 │
│  Output: Selected task ID                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    TASK ASSIGNMENT                           │
│  Input: Selected task                                        │
│  Process:                                                   │
│    • Read TASK_QUEUE.md for details                          │
│    • Assign to appropriate agent                             │
│    • Update TASK_STATE.yaml                                  │
│  Output: Task assignment                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    TASK EXECUTION                            │
│  Input: Task assignment                                      │
│  Agent: Programmer                                           │
│  Process:                                                   │
│    • Read requirements                                       │
│    • Implement changes                                       │
│    • Write tests                                             │
│    • Run tests                                               │
│  Output: Completed implementation                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    TASK VALIDATION                           │
│  Input: Completed implementation                             │
│  Agent: Validator                                            │
│  Process:                                                   │
│    • Run test suite                                          │
│    • Verify YAML syntax                                      │
│    • Verify Markdown syntax                                  │
│    • Verify project structure                                │
│  Output: PASS or FAIL                                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    TASK REVIEW                               │
│  Input: Validation PASS                                       │
│  Agent: Auditor                                              │
│  Process:                                                   │
│    • Review code quality                                     │
│    • Check documentation                                     │
│    • Verify conventions                                      │
│  Output: APPROVED or REVISION REQUIRED                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    TASK COMPLETION                           │
│  Input: Auditor APPROVED                                     │
│  Agent: Coordinator                                          │
│  Process:                                                   │
│    • Update PROJECT_STATE.md                                 │
│    • Update TASK_QUEUE.md                                    │
│    • Update CHANGELOG.md                                     │
│    • Update CURRENT_STATUS.yaml                              │
│    • Update TASK_STATE.yaml                                  │
│  Output: Task marked complete                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Agent Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT INITIALIZATION                      │
│  • Read AGENT_MANIFEST.md                                    │
│  • Read role-specific document                               │
│  • Load relevant state files                                 │
│  • Understand permissions and boundaries                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT ACTIVATION                          │
│  • Receive task assignment                                   │
│  • Read task requirements                                    │
│  • Load relevant documentation                               │
│  • Begin work                                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT EXECUTION                           │
│  • Execute assigned tasks                                    │
│  • Follow workflow                                           │
│  • Update state files                                        │
│  • Report progress                                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT DEACTIVATION                        │
│  • Complete current task                                     │
│  • Save session state                                        │
│  • Prepare handover                                          │
│  • Report completion                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Review Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    REVIEW REQUEST                            │
│  Input: Programmer completion report                         │
│  Source: Coordinator                                         │
│  Destination: Auditor                                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    CODE REVIEW                               │
│  Agent: Auditor                                              │
│  Checklist: docs/checklists/code_review.md                   │
│  Process:                                                   │
│    • Review code quality                                     │
│    • Check test coverage                                     │
│    • Verify conventions                                      │
│    • Check architecture compliance                           │
│  Output: Findings report                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENTATION REVIEW                      │
│  Agent: Auditor                                              │
│  Checklist: docs/checklists/documentation_review.md          │
│  Process:                                                   │
│    • Review README                                           │
│    • Review CHANGELOG                                        │
│    • Check cross-references                                  │
│    • Verify consistency                                      │
│  Output: Documentation findings                              │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    REVIEW DECISION                           │
│  Agent: Coordinator                                          │
│  Process:                                                   │
│    • Review Auditor findings                                 │
│    • Decide: APPROVED / APPROVED WITH NOTES / REVISION REQUIRED
│    • If REVISION: return to Programmer                       │
│    • If APPROVED: proceed to completion                      │
│  Output: Review decision                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Documentation Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENTATION TRIGGER                     │
│  • Code change completed                                     │
│  • Task completed                                            │
│  • Phase completed                                           │
│  • Decision made                                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENTATION UPDATE                      │
│  Agent: Auditor (code docs) / Coordinator (state docs)       │
│  Process:                                                   │
│    • Update relevant documentation                           │
│    • Follow templates                                        │
│    • Maintain cross-references                               │
│  Output: Updated documentation                               │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENTATION REVIEW                      │
│  Agent: Auditor                                              │
│  Checklist: docs/checklists/documentation_review.md          │
│  Process:                                                   │
│    • Verify accuracy                                         │
│    • Check consistency                                       │
│    • Validate cross-references                               │
│  Output: Documentation approved                              │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENTATION PUBLICATION                 │
│  Agent: Coordinator                                          │
│  Process:                                                   │
│    • Update PROJECT_STATE.md                                 │
│    • Update CURRENT_STATUS.yaml                              │
│    • Update TASK_STATE.yaml                                  │
│  Output: Documentation current                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Validation Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    VALIDATION REQUEST                        │
│  Input: Code changes completed                               │
│  Source: Programmer                                          │
│  Destination: Validator                                      │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    UNIT TEST VALIDATION                      │
│  Agent: Validator                                            │
│  Command:                                                   │
│    cd /home/munumu/Qscout                                   │
│    PYTHONPATH=src python3 -m unittest discover -s tests     │
│  Output: PASS or FAIL                                        │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    STRUCTURE VALIDATION                      │
│  Agent: Validator                                            │
│  Process:                                                   │
│    • Verify project structure                                │
│    • Check file organization                                 │
│    • Validate naming conventions                             │
│  Output: PASS or FAIL                                        │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    SYNTAX VALIDATION                         │
│  Agent: Validator                                            │
│  Process:                                                   │
│    • Verify YAML syntax                                      │
│    • Verify Markdown syntax                                  │
│    • Check for syntax errors                                 │
│  Output: PASS or FAIL                                        │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    CONSISTENCY VALIDATION                    │
│  Agent: Validator                                            │
│  Process:                                                   │
│    • Verify documentation links                              │
│    • Check cross-references                                  │
│    • Validate state file consistency                         │
│  Output: PASS or FAIL                                        │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    VALIDATION RESULT                         │
│  If ALL PASS: Proceed to Auditor review                      │
│  If ANY FAIL: Return to Programmer for fixes                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Release Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    RELEASE PREPARATION                       │
│  Agent: Coordinator                                          │
│  Checklist: docs/checklists/release_checklist.md             │
│  Process:                                                   │
│    • Verify all phase tasks completed                        │
│    • Verify all tests pass                                   │
│    • Verify documentation complete                           │
│    • Verify physical validation complete                     │
│  Output: Release candidate                                   │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    RELEASE REVIEW                            │
│  Agent: Auditor                                              │
│  Process:                                                   │
│    • Final code review                                       │
│    • Final documentation review                              │
│    • Final consistency check                                 │
│  Output: Release approved                                    │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    RELEASE EXECUTION                         │
│  Agent: Coordinator                                          │
│  Process:                                                   │
│    • Update version numbers                                  │
│    • Update ROADMAP.md                                       │
│    • Update PROJECT_STATE.md                                 │
│    • Create release notes                                    │
│  Output: Release published                                   │
└─────────────────────┬─────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    POST-RELEASE                              │
│  Agent: Coordinator                                          │
│  Process:                                                   │
│    • Update TASK_STATE.yaml                                  │
│    • Initialize next phase                                   │
│    • Update CURRENT_STATUS.yaml                              │
│  Output: Next phase ready                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Document Reading Order

### For New AI Agents

```
START_HERE.md
    │
    ▼
CURRENT_STATUS.yaml
    │
    ▼
TASK_STATE.yaml
    │
    ▼
Determine Role
    │
    ├──► Coordinator → AGENT_COORDINATOR.md
    ├──► Programmer → AGENT_PROGRAMMER.md
    ├──► Auditor → AGENT_AUDITOR.md
    └──► Validator → AGENT_VALIDATOR.md
    │
    ▼
AGENT_WORKFLOW.md
    │
    ▼
Begin Work
```

### For Task Execution

```
TASK_STATE.yaml
    │
    ▼
Identify Current Task
    │
    ▼
TASK_QUEUE.md (task details)
    │
    ▼
PROJECT_STATE.md (context)
    │
    ▼
Relevant Source Code
    │
    ▼
Execute Task
```

### For Review

```
Programmer Completion Report
    │
    ▼
docs/checklists/code_review.md
    │
    ▼
Changed Files
    │
    ▼
docs/checklists/documentation_review.md
    │
    ▼
Findings Report
```

---

## State File Updates

### TASK_STATE.yaml

Updated by: Coordinator
When: Task status changes
Fields: current_task, completed_tasks, pending_tasks, status

### CURRENT_STATUS.yaml

Updated by: Coordinator
When: Phase changes, test results change, validation completes
Fields: tests, physical_validation, status, last_update

### PROJECT_STATE.md

Updated by: Coordinator
When: Significant project changes
Sections: Current Phase, Test Status, Known Issues, Blockers

### CHANGELOG.md

Updated by: Coordinator
When: Tasks completed, phases completed
Format: Chronological entries

---

## Error Recovery

### Test Failure

1. Validator reports FAIL
2. Coordinator notifies Programmer
3. Programmer investigates and fixes
4. Return to validation

### Review Failure

1. Auditor reports REVISION REQUIRED
2. Coordinator notifies Programmer
3. Programmer implements fixes
4. Return to validation

### Blocker

1. Agent reports blocker
2. Coordinator assesses impact
3. If resolvable: provide guidance
4. If not: escalate to human
5. Update sessions/BLOCKERS.md

### Session Interruption

1. Save current state to sessions/CURRENT_SESSION.md
2. Update TASK_STATE.yaml
3. Update CURRENT_STATUS.yaml
4. Next session reads sessions/NEXT_SESSION.md

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [START_HERE.md](START_HERE.md) | Entry point |
| [PROJECT_STATE.md](PROJECT_STATE.md) | Current status |
| [CURRENT_STATUS.yaml](CURRENT_STATUS.yaml) | Machine state |
| [TASK_STATE.yaml](TASK_STATE.yaml) | Execution state |
| [AGENT_WORKFLOW.md](AGENT_WORKFLOW.md) | Communication protocol |
| [AGENT_MANIFEST.md](AGENT_MANIFEST.md) | Agent definitions |
| [QUALITY_GATES.md](QUALITY_GATES.md) | Mandatory gates |
| [AUTONOMY_GUIDE.md](AUTONOMY_GUIDE.md) | Autonomy improvements |
| [COORDINATOR_DASHBOARD.md](COORDINATOR_DASHBOARD.md) | Daily dashboard |
