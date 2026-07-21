# PROJECT_INDEX.md — Master Index

**Last Updated:** 2026-07-18

---

## Project

| Document | Purpose |
|----------|---------|
| [START_HERE.md](START_HERE.md) | Entry point for all AI agents |
| [PROJECT_STATE.md](PROJECT_STATE.md) | Single source of truth |
| [README.md](../README.md) | Project overview and usage |

---

## Architecture

| Document | Purpose |
|----------|---------|
| [DECISIONS.md](DECISIONS.md) | Architectural decision log |
| [docs/QScout_RB_Protocol_Specification.md](../docs/QScout_RB_Protocol_Specification.md) | RB protocol specification |
| [docs/QScout_Response_Matching_Mechanism.md](../docs/QScout_Response_Matching_Mechanism.md) | Response correlation analysis |
| [docs/QScout_Firmware_Forensic_Report.md](../docs/QScout_Firmware_Forensic_Report.md) | Firmware analysis |
| [docs/QScout_Observed_Differences.md](../docs/QScout_Observed_Differences.md) | Experimental findings |
| [docs/QScout_Reference_Packets.md](../docs/QScout_Reference_Packets.md) | Real packet examples |

---

## Workflow

| Document | Purpose |
|----------|---------|
| [AGENT_WORKFLOW.md](AGENT_WORKFLOW.md) | Agent communication protocol |
| [PROJECT_OPERATING_SYSTEM.md](PROJECT_OPERATING_SYSTEM.md) | Operating procedures |
| [QUALITY_GATES.md](QUALITY_GATES.md) | Mandatory quality gates |
| [AUTONOMY_GUIDE.md](AUTONOMY_GUIDE.md) | Autonomy improvements |

---

## Agents

| Document | Purpose |
|----------|---------|
| [AGENT_MANIFEST.md](AGENT_MANIFEST.md) | Agent definitions and boundaries |
| [AGENT_COORDINATOR.md](AGENT_COORDINATOR.md) | Coordinator agent spec |
| [AGENT_PROGRAMMER.md](AGENT_PROGRAMMER.md) | Programmer agent spec |
| [AGENT_AUDITOR.md](AGENT_AUDITOR.md) | Auditor agent spec |
| [AGENT_VALIDATOR.md](AGENT_VALIDATOR.md) | Validator agent spec |

---

## Templates

| Document | Purpose |
|----------|---------|
| [templates/task_template.md](templates/task_template.md) | Standard task format |
| [templates/audit_template.md](templates/audit_template.md) | Standard audit format |
| [templates/decision_template.md](templates/decision_template.md) | Standard decision format |
| [templates/handover_template.md](templates/handover_template.md) | Standard handover format |

---

## Checklists

| Document | Purpose |
|----------|---------|
| [docs/checklists/code_review.md](docs/checklists/code_review.md) | Code review checklist |
| [docs/checklists/documentation_review.md](docs/checklists/documentation_review.md) | Documentation review checklist |
| [docs/checklists/physical_validation.md](docs/checklists/physical_validation.md) | Physical validation checklist |
| [docs/checklists/release_checklist.md](docs/checklists/release_checklist.md) | Release checklist |

---

## Sessions

| Document | Purpose |
|----------|---------|
| [sessions/CURRENT_SESSION.md](sessions/CURRENT_SESSION.md) | Active session state |
| [sessions/NEXT_SESSION.md](sessions/NEXT_SESSION.md) | Next session preparation |
| [sessions/BLOCKERS.md](sessions/BLOCKERS.md) | Active blockers |
| [sessions/SESSION_HISTORY.md](sessions/SESSION_HISTORY.md) | Session history log |

---

## Documentation

| Document | Purpose |
|----------|---------|
| [docs/QScout_Physical_Validation_Report.md](../docs/QScout_Physical_Validation_Report.md) | Physical validation results |
| [docs/QScout_Library_Audit_Report.md](../docs/QScout_Library_Audit_Report.md) | Library audit findings |
| [docs/QScout_API_Audit_Report.md](../docs/QScout_API_Audit_Report.md) | API audit findings |
| [docs/QScout_Project_Consolidation_Report.md](../docs/QScout_Project_Consolidation_Report.md) | Consolidation summary |
| [docs/QScout_Protocol_Coverage_Report.md](../docs/QScout_Protocol_Coverage_Report.md) | Protocol coverage |
| [docs/QScout_Response_Action_Code_Analysis.md](../docs/QScout_Response_Action_Code_Analysis.md) | Response action code analysis |
| [docs/QScout_v1.0_Release_Notes.md](../docs/QScout_v1.0_Release_Notes.md) | Release notes |
| [docs/RB_Protocol_v1.0.md](../docs/RB_Protocol_v1.0.md) | Protocol v1.0 |
| [docs/physical_validation_report.md](../docs/physical_validation_report.md) | Physical validation report |
| [docs/QScout_Repository_Consolidation_Report.md](../docs/QScout_Repository_Consolidation_Report.md) | Repository consolidation |

---

## Evidence

| Directory | Purpose |
|-----------|---------|
| [evidence/captures/](../evidence/captures/) | Serial captures |
| [evidence/logs/](../evidence/logs/) | Validation logs |
| [evidence/packets/](../evidence/packets/) | Packet captures |

---

## Roadmap

| Document | Purpose |
|----------|---------|
| [ROADMAP.md](ROADMAP.md) | Complete project roadmap |

---

## State

| Document | Purpose |
|----------|---------|
| [CURRENT_STATUS.yaml](CURRENT_STATUS.yaml) | Machine-readable project state |
| [TASK_STATE.yaml](TASK_STATE.yaml) | Live execution state |

---

## Rules

| Document | Purpose |
|----------|---------|
| [PROJECT_RULES.md](PROJECT_RULES.md) | Permanent project rules |

---

## Backups

| Document | Purpose |
|----------|---------|
| [../2026-07-16 Project Backup.md](../2026-07-16%20Project%20Backup.md) | Project backup (2026-07-16) |
| [../2026-07-17 Backup.md](../2026-07-17%20Backup.md) | Project backup (2026-07-17) |
| [../Q Scout Native Linux Backup 18-07.md](../Q%20Scout%20Native%20Linux%20Backup%2018-07.md) | Complete project backup |

---

## Quick Reference

### For New Agents

1. Read `START_HERE.md`
2. Read `CURRENT_STATUS.yaml`
3. Read `TASK_STATE.yaml`
4. Read `AGENT_MANIFEST.md`
5. Read `AGENT_WORKFLOW.md`

### For Task Execution

1. Read `TASK_STATE.yaml`
2. Read `TASK_QUEUE.md`
3. Read relevant source code
4. Execute task
5. Update state files

### For Review

1. Read completion report
2. Use `docs/checklists/code_review.md`
3. Use `docs/checklists/documentation_review.md`
4. Produce findings report

### For Coordination

1. Read `COORDINATOR_DASHBOARD.md`
2. Read `TASK_STATE.yaml`
3. Assign next task
4. Monitor progress
5. Update state files

---

## File Count

| Category | Count |
|----------|-------|
| Operational Documents | 12 |
| Agent Documents | 5 |
| Templates | 4 |
| Checklists | 4 |
| Session Files | 4 |
| State Files | 2 |
| **Total Project Management** | **31** |
| Technical Documentation | 12 |
| Evidence Files | Multiple |
| **Total Repository Files** | **50+** |
