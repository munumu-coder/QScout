# AUTONOMY_GUIDE.md — Minimizing Human Intervention

**Last Updated:** 2026-07-18

---

## Overview

This document explains how the Q-Scout project minimizes human intervention while maintaining quality and safety.

---

## Automatic Context Loading

### How It Works

When a new AI agent joins the project:

1. Read `START_HERE.md` — Get project overview
2. Parse `CURRENT_STATUS.yaml` — Load project state
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

1. Coordinator updates `PROJECT_STATE.md`
2. Coordinator updates `TASK_QUEUE.md`
3. Coordinator updates `CHANGELOG.md`
4. Coordinator updates `CURRENT_STATUS.yaml`
5. Coordinator updates `TASK_STATE.yaml`
6. Coordinator updates `sessions/SESSION_HISTORY.md`

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
4. Agent updates `CURRENT_STATUS.yaml`
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
2. `CURRENT_STATUS.yaml` — Project status
3. `COORDINATOR_DASHBOARD.md` — Visual progress
4. `ROADMAP.md` — Phase completion

### What's Automatic

- Task completion tracking
- Phase progress calculation
- Dashboard updates
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
3. `CURRENT_STATUS.yaml` updated
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

## Related Documents

| Document | Purpose |
|----------|---------|
| [PROJECT_OPERATING_SYSTEM.md](PROJECT_OPERATING_SYSTEM.md) | Operating procedures |
| [AGENT_WORKFLOW.md](AGENT_WORKFLOW.md) | Communication protocol |
| [QUALITY_GATES.md](QUALITY_GATES.md) | Mandatory quality gates |
| [AGENT_MANIFEST.md](AGENT_MANIFEST.md) | Agent definitions |
| [sessions/](sessions/) | Session management |
