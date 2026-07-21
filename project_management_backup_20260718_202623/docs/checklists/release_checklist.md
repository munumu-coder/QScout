# Release Checklist

**Used by:** Coordinator Agent
**When:** Preparing a new release or phase transition

---

## Pre-Release

- [ ] All tasks in current phase completed
- [ ] All tests passing:
  ```bash
  cd /home/munumu/Qscout
  PYTHONPATH=src python3 -m unittest discover -s tests
  ```
- [ ] No failing tests
- [ ] No regressions introduced

---

## Code Quality

- [ ] All code reviewed by Auditor
- [ ] No known bugs in new code
- [ ] Code follows project conventions
- [ ] Architecture integrity maintained
- [ ] No unauthorized changes

---

## Documentation

- [ ] README.md updated
- [ ] CHANGELOG.md updated with phase summary
- [ ] PROJECT_STATE.md updated
- [ ] ROADMAP.md updated (if new phase)
- [ ] API documentation current
- [ ] All cross-references valid

---

## Physical Validation

- [ ] All public API commands validated on robot
- [ ] Validation evidence captured
- [ ] Validation report updated
- [ ] Known limitations documented

---

## Machine-Readable Files

- [ ] CURRENT_STATUS.yaml updated
- [ ] TASK_STATE.yaml updated
- [ ] YAML syntax valid
- [ ] All fields current

---

## Task Management

- [ ] All tasks marked completed in TASK_QUEUE.md
- [ ] Next phase tasks identified
- [ ] Backlog updated
- [ ] Dependencies documented

---

## Decision Log

- [ ] All architectural decisions documented in DECISIONS.md
- [ ] Decision status current
- [ ] Alternatives documented
- [ ] Consequences documented

---

## Risk Assessment

- [ ] Known issues documented in PROJECT_STATE.md
- [ ] Risks documented in PROJECT_STATE.md
- [ ] Blockers documented
- [ ] Mitigation plans in place

---

## Final Verification

- [ ] No contradictions between documents
- [ ] Consistent terminology used
- [ ] All documents reference each other correctly
- [ ] Canonical repository path correct: `/home/munumu/Qscout`

---

## Release Approval

- [ ] Auditor has reviewed all changes
- [ ] All checklists pass
- [ ] Coordinator approves release
- [ ] Human notified (if required)

---

## Release Information

- **Release Version:** ___________
- **Release Date:** ___________
- **Phase Completed:** ___________
- **Approved By:** ___________
