# HANDOVER_PROTOCOL.md — New Agent Onboarding

---

## Purpose

This document describes how a new AI agent can join the Q-Scout project and safely continue development.

---

## Step 1: Read Project State

**First document to read:** `PROJECT_STATE.md`

This provides:
- Current phase
- Current task
- Test status
- Known issues
- Blockers
- Risks

---

## Step 2: Read Roadmap

**Second document:** `ROADMAP.md`

This provides:
- Complete project history
- Future plans
- Phase dependencies
- Completion criteria

---

## Step 3: Understand Your Role

Read the document matching your assigned role:

| Role | Document |
|------|----------|
| Coordinator | `AGENT_COORDINATOR.md` |
| Programmer | `AGENT_PROGRAMMER.md` |
| Auditor | `AGENT_AUDITOR.md` |

---

## Step 4: Read Project Rules

**Required reading:** `PROJECT_RULES.md`

These rules are mandatory and enforced by the Coordinator.

---

## Step 5: Review Task Queue

**Document:** `TASK_QUEUE.md`

This shows:
- Pending tasks
- Task priorities
- Task dependencies
- Assigned agents

---

## Step 6: Understand Decisions

**Document:** `DECISIONS.md`

This provides:
- Architectural decisions already made
- Alternatives considered
- Consequences of each decision

---

## Step 7: Review History

**Document:** `CHANGELOG.md`

This provides:
- Chronological project history
- Features implemented per phase
- Tests added per phase
- Known issues per phase

---

## Step 8: Understand Your Role Agent

Read your role-specific document:

### For Programmer
- Read `AGENT_PROGRAMMER.md`
- Understand code conventions
- Understand restrictions
- Understand quality standards

### For Auditor
- Read `AGENT_AUDITOR.md`
- Understand review process
- Understand documentation updates
- Understand quality metrics

### For Coordinator
- Read `AGENT_COORDINATOR.md`
- Understand workflow
- Understand decision authority
- Understand communication protocol

---

## Step 9: Review Existing Code

If you are a Programmer:
1. Read `src/qscout/` files
2. Understand the architecture
3. Review existing tests in `tests/`
4. Check documentation in `docs/`

If you are an Auditor:
1. Read `docs/` files
2. Review documentation consistency
3. Check cross-references
4. Identify gaps

---

## Step 10: Safely Continue Development

### For Programmer
1. Wait for task assignment from Coordinator
2. Read task requirements carefully
3. Implement changes
4. Write tests
5. Execute test suite
6. Report completion

### For Auditor
1. Wait for review request from Coordinator
2. Review code/documentation
3. Report findings
4. Update documentation if approved

### For Coordinator
1. Read PROJECT_STATE.md
2. Read TASK_QUEUE.md
3. Identify next task
4. Assign to appropriate agent
5. Monitor progress
6. Verify completion
7. Update documentation

---

## Step 11: Report Completed Work

### Programmer Reports

Include:
- Task ID
- Files modified
- Tests added/modified
- Test results (all passing)
- Any issues encountered

### Auditor Reports

Include:
- Review scope
- Findings (issues found)
- Recommendations
- Documentation updates made

### Coordinator Reports

Include:
- Tasks assigned
- Tasks completed
- Phase progress
- Updated PROJECT_STATE.md

---

## Step 12: Update Documentation

After completing work:

1. **Programmer:** Report to Coordinator
2. **Auditor:** Review and update documentation
3. **Coordinator:** Update PROJECT_STATE.md, TASK_QUEUE.md, CHANGELOG.md

---

## Emergency Contacts

If you encounter:
- **Blocker:** Report to Coordinator immediately
- **Architecture question:** Escalate to human
- **Rule violation:** Report to Auditor
- **Unclear requirements:** Ask Coordinator for clarification

---

## Quick Reference

| Document | Purpose |
|----------|---------|
| START_HERE.md | Entry point for new agents |
| PROJECT_STATE.md | Current project status |
| TASK_STATE.yaml | Live execution state |
| ROADMAP.md | Complete project plan |
| TASK_QUEUE.md | Task assignments |
| DECISIONS.md | Architectural decisions |
| CHANGELOG.md | Project history |
| PROJECT_RULES.md | Mandatory rules |
| AGENT_MANIFEST.md | Agent definitions |
| AGENT_WORKFLOW.md | Agent communication protocol |
| AGENT_COORDINATOR.md | Coordinator role |
| AGENT_PROGRAMMER.md | Programmer role |
| AGENT_AUDITOR.md | Auditor role |
| CURRENT_STATUS.yaml | Machine-readable state |

---

## For AI Agents

**Machine-readable state:** Read `CURRENT_STATUS.yaml` for structured project data.

**Workflow:** Follow `AGENT_WORKFLOW.md` for all communication.

**First file to read:** `PROJECT_STATE.md` or parse `CURRENT_STATUS.yaml`.

---

## Canonical Repository

**ALWAYS** use: `/home/munumu/Qscout`

**NEVER** use any other repository.
