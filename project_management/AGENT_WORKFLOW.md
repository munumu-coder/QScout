# AGENT_WORKFLOW.md — Agent Communication Protocol (ARCHIVED)

**Last Updated:** 2026-07-18

> **NOTE:** The multi-agent project management infrastructure has been **archived**. This document is preserved for reference only.
>
> **For the current project state, read `START_HERE.md`** instead of following this workflow.
>
> **Single-agent workflow:**
> 1. Read `START_HERE.md`
> 2. Read `CONTROL_CENTER.yaml`
> 3. Read `TASK_STATE.yaml`
> 4. Read relevant source code
> 5. Implement changes
> 6. Run tests: `PYTHONPATH=src python3 -m unittest discover -s tests`
> 7. Report results

---

## Overview (Historical)

This document originally defined the official communication workflow for multi-agent development in the Q-Scout project.

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

## Project Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT START                             │
│  • Read START_HERE.md                                        │
│  • Load CONTROL_CENTER.yaml                                  │
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
│  • Update CONTROL_CENTER.yaml                                │
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
│  2. READ CONTROL_CENTER.yaml                                 │
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
│     • Read role-specific section                             │
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
│     • Update CONTROL_CENTER.yaml                             │
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
│    • Read CONTROL_CENTER.yaml for details                    │
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
│    • Update CONTROL_CENTER.yaml                              │
│    • Update TASK_STATE.yaml                                  │
│    • Update CHANGELOG.md                                     │
│  Output: Task marked complete                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Agent Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT INITIALIZATION                      │
│  • Read AGENT_MANIFEST.md                                    │
│  • Read role-specific section                                │
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
│    • Update CONTROL_CENTER.yaml                              │
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
│    • Update CONTROL_CENTER.yaml                              │
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
CONTROL_CENTER.yaml
    │
    ▼
TASK_STATE.yaml
    │
    ▼
Determine Role
    │
    ├──► Coordinator → AGENT_MANIFEST.md (Coordinator section)
    ├──► Programmer → AGENT_MANIFEST.md (Programmer section)
    ├──► Auditor → AGENT_MANIFEST.md (Auditor section)
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
CONTROL_CENTER.yaml (context)
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

### CONTROL_CENTER.yaml

Updated by: Coordinator
When: Phase changes, test results change, validation completes
Fields: tests, physical_validation, status, last_update

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
3. Update CONTROL_CENTER.yaml
4. Next session reads sessions/NEXT_SESSION.md

---

## Automatic Context Loading

### How It Works

When a new AI agent joins the project:

1. Read `START_HERE.md` — Get project overview
2. Parse `CONTROL_CENTER.yaml` — Load project state
3. Parse `TASK_STATE.yaml` — Load execution state
4. Read `AGENT_MANIFEST.md` — Understand role
5. Read `AGENT_WORKFLOW.md` — Understand workflow
6. Begin work

### What's Automatic

- Project state loading
- Role determination
- Task identification
- Document navigation

### What Requires Human

- Initial agent deployment
- Role assignment (first time)

---

## Automatic Task Assignment

### How It Works

1. Coordinator reads `TASK_STATE.yaml`
2. Identifies next pending task
3. Checks dependencies are satisfied
4. Assigns to appropriate agent
5. Updates `TASK_STATE.yaml`

### What's Automatic

- Task selection based on priority
- Dependency checking
- Agent assignment
- State file updates

### What Requires Human

- Defining new tasks
- Resolving priority conflicts
- Approving phase transitions

---

## Automatic Document Updates

### How It Works

When a task completes:

1. Coordinator updates `CONTROL_CENTER.yaml`
2. Coordinator updates `TASK_STATE.yaml`
3. Coordinator updates `CHANGELOG.md`
4. Coordinator updates `sessions/SESSION_HISTORY.md`

### What's Automatic

- State file synchronization
- History logging
- Status updates
- Cross-reference maintenance

### What Requires Human

- Approving architectural changes
- Resolving contradictions
- Defining new phases

---

## Automatic Validation

### How It Works

After code changes:

1. Validator executes test suite
2. Validator verifies project structure
3. Validator verifies YAML syntax
4. Validator verifies Markdown syntax
5. Validator verifies documentation links
6. Validator produces PASS or FAIL

### What's Automatic

- Test execution
- Structure validation
- Syntax validation
- Link validation
- Consistency checking

### What Requires Human

- Interpreting complex failures
- Deciding on edge cases
- Approving physical validation

---

## Automatic Handover

### How It Works

When a session ends:

1. Agent saves state to `sessions/CURRENT_SESSION.md`
2. Agent updates `sessions/NEXT_SESSION.md`
3. Agent updates `TASK_STATE.yaml`
4. Agent updates `CONTROL_CENTER.yaml`
5. Next session reads these files and continues

### What's Automatic

- State preservation
- Session continuity
- Progress tracking
- Context loading

### What Requires Human

- Resolving complex blockers
- Deciding on major direction changes

---

## Automatic Progress Tracking

### How It Works

Progress is tracked through:

1. `TASK_STATE.yaml` — Task completion status
2. `CONTROL_CENTER.yaml` — Project status
3. `ROADMAP.md` — Phase completion

### What's Automatic

- Task completion tracking
- Phase progress calculation
- History maintenance

### What Requires Human

- Defining success criteria
- Approving milestone completion
- Celebrating achievements

---

## Automatic Recovery After Interruption

### How It Works

When a session is interrupted:

1. Current state saved to `sessions/CURRENT_SESSION.md`
2. `TASK_STATE.yaml` updated with current state
3. `CONTROL_CENTER.yaml` updated
4. Next session reads `sessions/NEXT_SESSION.md`
5. Work continues from last saved state

### What's Automatic

- State preservation
- Session recovery
- Progress continuity
- Context restoration

### What Requires Human

- Resolving root cause of interruption
- Deciding on priority changes
- Approving recovery plan

---

## What Still Requires Human Approval

### Always Requires Human

1. **Architecture changes** — Any modification to frozen architecture
2. **Phase transitions** — Moving to next major phase
3. **Rule changes** — Modifying project rules
4. **New dependencies** — Adding external dependencies
5. **Release approval** — Final release sign-off
6. **Escalated issues** — Issues agents cannot resolve

### Sometimes Requires Human

1. **Priority conflicts** — When agents disagree on priority
2. **Edge cases** — When behavior is ambiguous
3. **Complex blockers** — When technical issues are complex
4. **Strategic decisions** — When direction needs human judgment

### Never Requires Human

1. **Routine tasks** — Standard implementation tasks
2. **Test execution** — Running test suites
3. **Validation** — Automated validation checks
4. **Documentation updates** — Standard doc updates
5. **State file updates** — Routine state maintenance

---

## Autonomy Levels

### Level 1: Full Autonomy

- Routine task execution
- Test running
- Validation
- State updates
- Documentation updates

### Level 2: Guided Autonomy

- Task selection (within defined parameters)
- Agent assignment
- Phase progression (within planned phases)
- Release preparation

### Level 3: Human Oversight

- Architecture decisions
- Phase transitions
- Rule changes
- Complex problem resolution
- Strategic direction

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
| [CONTROL_CENTER.yaml](CONTROL_CENTER.yaml) | Current status (read by all) |
| [TASK_STATE.yaml](TASK_STATE.yaml) | Live execution state (updated at Step 7) |
| [DECISIONS.md](DECISIONS.md) | Architecture decisions (read by all) |
| [CHANGELOG.md](CHANGELOG.md) | History (updated at Step 5) |
| [PROJECT_RULES.md](PROJECT_RULES.md) | Rules (enforced by Coordinator) |
| [AGENT_MANIFEST.md](AGENT_MANIFEST.md) | Agent definitions and boundaries |
| [AGENT_VALIDATOR.md](AGENT_VALIDATOR.md) | Validator detailed spec |
| [QUALITY_GATES.md](QUALITY_GATES.md) | Mandatory quality gates |
| [docs/checklists/](docs/checklists/) | Review checklists for Auditor |
| [templates/](templates/) | Document templates |
| [sessions/](sessions/) | Session management |
