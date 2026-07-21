# START_HERE.md — Entry Point for All AI Agents

**Last Updated:** 2026-07-18

---

## What Is This Project?

Native Python SDK for controlling the Robobloq Q-Scout (RB-00002) robot from Linux via USB/UART.

## Official Repository

`/home/munumu/Qscout`

## Current SDK Phase

**SDK-02 Phase 2C — Expand Public API**

## Current Milestone

Expand public API with additional documented commands (GET_DEVICE_INFO, GET_VOLTAGE, etc.)

---

## Reading Order for New AI Agents

| Order | Document | Purpose |
|-------|----------|---------|
| 1 | **This file** | Understand project and next steps |
| 2 | `PROJECT_STATE.md` | Current project status (source of truth) |
| 3 | `CURRENT_STATUS.yaml` | Machine-readable state |
| 4 | `ROADMAP.md` | Complete project history and future plan |
| 5 | `TASK_QUEUE.md` | Current task assignments |
| 6 | `DECISIONS.md` | Architectural decisions already made |
| 7 | `PROJECT_RULES.md` | Mandatory rules |
| 8 | `AGENT_MANIFEST.md` | Your role and boundaries |
| 9 | `AGENT_WORKFLOW.md` | How agents communicate |
| 10 | `HANDOVER_PROTOCOL.md` | How to safely continue work |

---

## What Should an AI Agent Do Immediately?

1. Read this file (you are here)
2. Read `PROJECT_STATE.md` to understand current status
3. Read `CURRENT_STATUS.yaml` for machine-readable state
4. Read `AGENT_MANIFEST.md` to understand your role
5. Read `AGENT_WORKFLOW.md` to understand the workflow
6. If Coordinator: read `TASK_QUEUE.md` and assign next task
7. If Programmer: wait for task assignment
8. If Auditor: wait for review request

---

## What Must NEVER Be Done

1. **NEVER** modify Python source code without task assignment
2. **NEVER** change architecture without human approval
3. **NEVER** modify tests without following workflow
4. **NEVER** skip the Auditor review step
5. **NEVER** update PROJECT_STATE.md directly (Coordinator only)
6. **NEVER** use any repository other than `/home/munumu/Qscout`
7. **NEVER** implement undocumented behavior
8. **NEVER** bypass the task assignment process

---

## Quick Reference

| Need | Document |
|------|----------|
| Current status | `PROJECT_STATE.md` |
| Machine state | `CURRENT_STATUS.yaml` |
| Task queue | `TASK_QUEUE.md` |
| Roadmap | `ROADMAP.md` |
| My role | `AGENT_MANIFEST.md` |
| Workflow | `AGENT_WORKFLOW.md` |
| Rules | `PROJECT_RULES.md` |
| Decisions | `DECISIONS.md` |
| History | `CHANGELOG.md` |
| Onboarding | `HANDOVER_PROTOCOL.md` |

---

## All Project Management Documents

```
project_management/
├── START_HERE.md              ← You are here
├── PROJECT_STATE.md           ← Single source of truth
├── PROJECT_OPERATING_SYSTEM.md ← Operating procedures
├── CURRENT_STATUS.yaml        ← Machine-readable state
├── TASK_STATE.yaml            ← Live execution state
├── ROADMAP.md                 ← Complete project plan
├── TASK_QUEUE.md              ← Task assignments
├── DECISIONS.md               ← Architectural decisions
├── CHANGELOG.md               ← Project history
├── PROJECT_RULES.md           ← Mandatory rules
├── PROJECT_INDEX.md           ← Master index
├── COORDINATOR_DASHBOARD.md   ← Daily dashboard
├── QUALITY_GATES.md           ← Quality gates
├── AUTONOMY_GUIDE.md          ← Autonomy improvements
├── AGENT_MANIFEST.md          ← Agent definitions
├── AGENT_WORKFLOW.md          ← Communication protocol
├── AGENT_COORDINATOR.md       ← Coordinator spec
├── AGENT_PROGRAMMER.md        ← Programmer spec
├── AGENT_AUDITOR.md           ← Auditor spec
├── AGENT_VALIDATOR.md         ← Validator spec
├── HANDOVER_PROTOCOL.md       ← New agent onboarding
├── docs/checklists/           ← Review checklists
│   ├── code_review.md
│   ├── documentation_review.md
│   ├── physical_validation.md
│   └── release_checklist.md
├── templates/                 ← Document templates
│   ├── task_template.md
│   ├── audit_template.md
│   ├── decision_template.md
│   └── handover_template.md
└── sessions/                  ← Session management
    ├── CURRENT_SESSION.md
    ├── NEXT_SESSION.md
    ├── BLOCKERS.md
    └── SESSION_HISTORY.md
```
