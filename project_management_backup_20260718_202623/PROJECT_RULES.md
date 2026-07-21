# PROJECT_RULES.md — Permanent Project Rules

---

## Repository Rules

1. **One canonical repository:** `/home/munumu/Qscout`
2. **No duplicate repositories.** All work happens in the canonical repository.
3. **All agents must follow their assigned role.**

---

## Development Rules

4. **Every feature requires tests.** No code changes without corresponding test updates.
5. **Evidence-driven development.** Never implement undocumented behavior.
6. **Physical validation overrides assumptions.** Experimental results are authoritative.
7. **Protocol layer must remain transport-independent.**
8. **Transport layer must never know protocol details.**
9. **Checksum must always be validated before parsing.**
10. **Architecture is frozen.** Future work extends capabilities, not redesigns.

---

## Documentation Rules

11. **Documentation always follows implementation.** Code first, docs second.
12. **No undocumented architectural changes.** All changes must be documented.
13. **Every completed task updates PROJECT_STATE.md.**
14. **Every architectural decision updates DECISIONS.md.**
15. **Every code modification updates CHANGELOG.md.**
16. **Cross-references must be consistent.** No broken links between documents.

---

## Task Management Rules

17. **Only Coordinator assigns tasks.**
18. **Programmer only works on assigned tasks.**
19. **Auditor reviews completed tasks before marking done.**
20. **All task completions update TASK_QUEUE.md.**

---

## Quality Rules

21. **No regressions.** All existing tests must pass after changes.
22. **No secrets or keys in code.**
23. **No hardcoded paths.** Use auto-detection or configuration.
24. **No external dependencies without justification.**

---

## Communication Rules

25. **Responses are correlated exclusively by Order ID.**
26. **Action codes in responses are informational only.**
27. **Order ID 0 is reserved for unsolicited firmware reports.**

---

## Workflow Rules

28. **Follow AGENT_WORKFLOW.md** for all agent communication
29. **Use CURRENT_STATUS.yaml** for machine-readable state
30. **All agents must read PROJECT_STATE.md** before starting work

---

## Enforcement

These rules are enforced by the Coordinator agent. Violations must be reported to the Auditor for review.

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [START_HERE.md](START_HERE.md) | Entry point for new agents |
| [PROJECT_STATE.md](PROJECT_STATE.md) | Current project status |
| [TASK_STATE.yaml](TASK_STATE.yaml) | Live execution state |
| [ROADMAP.md](ROADMAP.md) | Complete project roadmap |
| [TASK_QUEUE.md](TASK_QUEUE.md) | Task queue with assignments |
| [DECISIONS.md](DECISIONS.md) | Architectural decisions |
| [CHANGELOG.md](CHANGELOG.md) | Project history |
| [AGENT_MANIFEST.md](AGENT_MANIFEST.md) | Agent definitions |
| [AGENT_WORKFLOW.md](AGENT_WORKFLOW.md) | Agent communication protocol |
| [CURRENT_STATUS.yaml](CURRENT_STATUS.yaml) | Machine-readable project state |
