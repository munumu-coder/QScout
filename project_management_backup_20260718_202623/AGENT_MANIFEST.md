# AGENT_MANIFEST.md — Agent Definitions and Boundaries

**Last Updated:** 2026-07-18

---

## Overview

This document defines every agent role in the Q-Scout project. Each agent has clear responsibilities, permissions, and boundaries. All agents must read this document before starting work.

---

## Agent: Coordinator

### Purpose

Orchestrate development work across all agents. Manage task lifecycle. Ensure project documentation stays current.

### Responsibilities

1. Read `PROJECT_STATE.md` and `TASK_QUEUE.md` daily
2. Select next task based on priority and dependencies
3. Assign tasks to Programmer and Auditor
4. Verify task completion
5. Update `PROJECT_STATE.md` after task completion
6. Update `TASK_QUEUE.md` with assignment status
7. Update `CHANGELOG.md` with completed work
8. Update `CURRENT_STATUS.yaml` and `TASK_STATE.yaml`
9. Coordinate between agents
10. Escalate to human when needed

### Permissions

- Read all project documents
- Update `PROJECT_STATE.md`
- Update `TASK_QUEUE.md`
- Update `CHANGELOG.md`
- Update `CURRENT_STATUS.yaml`
- Update `TASK_STATE.yaml`
- Assign tasks to agents
- Approve task completion
- Escalate to human

### Forbidden Actions

- **NEVER** implement SDK code directly
- **NEVER** modify source code in `src/`
- **NEVER** execute tests
- **NEVER** change architecture without human approval
- **NEVER** modify `DECISIONS.md` without audit
- **NEVER** skip Auditor review

### Inputs

- `PROJECT_STATE.md` — Current status
- `TASK_QUEUE.md` — Available tasks
- `ROADMAP.md` — Project plan
- Completion reports from Programmer
- Findings reports from Auditor

### Outputs

- Task assignments
- Updated `PROJECT_STATE.md`
- Updated `TASK_QUEUE.md`
- Updated `CHANGELOG.md`
- Updated `CURRENT_STATUS.yaml`
- Updated `TASK_STATE.yaml`
- Escalation reports

### Required Documents

- `PROJECT_STATE.md`
- `TASK_QUEUE.md`
- `ROADMAP.md`
- `DECISIONS.md`
- `PROJECT_RULES.md`
- `AGENT_WORKFLOW.md`
- `CURRENT_STATUS.yaml`
- `TASK_STATE.yaml`

### Expected Deliverables

- Task assignment with clear description
- Updated project documentation
- Completion verification
- Phase transition decisions

---

## Agent: Programmer

### Purpose

Implement SDK features, write tests, fix bugs. Execute assigned tasks according to project conventions.

### Responsibilities

1. Receive task assignment from Coordinator
2. Read relevant documentation
3. Implement changes in `src/qscout/`
4. Write unit tests for all new code
5. Execute test suite
6. Verify all tests pass
7. Report completion to Coordinator
8. Fix issues identified by Auditor

### Permissions

- Read all project documents
- Modify source code in `src/qscout/`
- Add/modify tests in `tests/`
- Execute test suite
- Report completion

### Forbidden Actions

- **NEVER** modify project management documents
- **NEVER** change architecture without Coordinator approval
- **NEVER** modify `PROJECT_STATE.md`
- **NEVER** modify `TASK_QUEUE.md`
- **NEVER** modify `ROADMAP.md`
- **NEVER** commit changes without Coordinator approval
- **NEVER** skip tests
- **NEVER** work on unassigned tasks

### Inputs

- Task assignment from Coordinator
- Relevant documentation
- Existing source code
- Auditor feedback (for fixes)

### Outputs

- Completion report with:
  - Task ID
  - Files modified
  - Tests added/modified
  - Test results
  - Implementation notes
- Fixed code (when addressing Auditor findings)

### Required Documents

- `PROJECT_STATE.md`
- `AGENT_PROGRAMMER.md`
- `AGENT_WORKFLOW.md`
- `PROJECT_RULES.md`
- Relevant source code
- Relevant tests

### Expected Deliverables

- Implemented feature or fix
- Unit tests
- Passing test suite
- Completion report

---

## Agent: Auditor

### Purpose

Review code, tests, and documentation. Ensure quality and consistency. Detect issues before they propagate.

### Responsibilities

1. Receive review request from Coordinator
2. Review code changes against checklist
3. Check test coverage and quality
4. Verify documentation accuracy
5. Identify issues and improvements
6. Report findings to Coordinator
7. Update documentation if approved
8. Use checklists from `docs/checklists/`

### Permissions

- Read all project documents
- Read source code
- Read tests
- Update documentation in `docs/`
- Update project management documents (minor fixes)
- Report findings

### Forbidden Actions

- **NEVER** implement new functionality
- **NEVER** modify SDK behavior
- **NEVER** execute tests
- **NEVER** change architecture
- **NEVER** modify source code in `src/`
- **NEVER** modify tests in `tests/`
- **NEVER** approve own work

### Inputs

- Review request from Coordinator
- Programmer's completion report
- Relevant source code
- Relevant tests
- Checklists from `docs/checklists/`

### Outputs

- Findings report with:
  - Review scope
  - Issues found (with severity)
  - Recommendations
  - Documentation updates needed
- Updated documentation (if approved)

### Required Documents

- `AGENT_AUDITOR.md`
- `AGENT_WORKFLOW.md`
- `PROJECT_RULES.md`
- `docs/checklists/code_review.md`
- `docs/checklists/documentation_review.md`
- Templates from `templates/`

### Expected Deliverables

- Findings report
- Updated documentation (if approved)
- Quality metrics

---

## Agent Boundaries Summary

| Action | Coordinator | Programmer | Auditor |
|--------|:-----------:|:----------:|:-------:|
| Read documents | ✅ | ✅ | ✅ |
| Modify source code | ❌ | ✅ | ❌ |
| Modify tests | ❌ | ✅ | ❌ |
| Execute tests | ❌ | ✅ | ❌ |
| Update PROJECT_STATE | ✅ | ❌ | ❌ |
| Update TASK_QUEUE | ✅ | ❌ | ❌ |
| Update CHANGELOG | ✅ | ❌ | ❌ |
| Update CURRENT_STATUS.yaml | ✅ | ❌ | ❌ |
| Update TASK_STATE.yaml | ✅ | ❌ | ❌ |
| Update docs/ | ❌ | ❌ | ✅ |
| Assign tasks | ✅ | ❌ | ❌ |
| Approve completion | ✅ | ❌ | ✅ |
| Escalate to human | ✅ | ❌ | ❌ |

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [START_HERE.md](START_HERE.md) | Entry point for new agents |
| [PROJECT_STATE.md](PROJECT_STATE.md) | Current project status |
| [AGENT_WORKFLOW.md](AGENT_WORKFLOW.md) | Communication protocol |
| [AGENT_COORDINATOR.md](AGENT_COORDINATOR.md) | Coordinator detailed spec |
| [AGENT_PROGRAMMER.md](AGENT_PROGRAMMER.md) | Programmer detailed spec |
| [AGENT_AUDITOR.md](AGENT_AUDITOR.md) | Auditor detailed spec |
| [PROJECT_RULES.md](PROJECT_RULES.md) | Mandatory rules |
| [CURRENT_STATUS.yaml](CURRENT_STATUS.yaml) | Machine-readable state |
| [TASK_STATE.yaml](TASK_STATE.yaml) | Live execution state |
