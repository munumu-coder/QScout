# Documentation Review Checklist

**Used by:** Auditor Agent
**When:** After code changes are completed and reviewed

---

## Pre-Review

- [ ] Receive review request from Coordinator
- [ ] Read changed files list
- [ ] Read Programmer's completion report

---

## README.md

- [ ] Public API methods listed correctly
- [ ] Usage examples are accurate
- [ ] Installation instructions current
- [ ] Test instructions current
- [ ] Architecture diagram matches implementation
- [ ] No outdated information

---

## CHANGELOG.md

- [ ] Entry added for completed task
- [ ] Features implemented listed
- [ ] Tests added/modified listed
- [ ] Physical validation results listed (if applicable)
- [ ] Known issues listed (if any)
- [ ] Date is correct
- [ ] Phase name is correct

---

## PROJECT_STATE.md

- [ ] Current phase is correct
- [ ] Test count is accurate
- [ ] Physical validation status is current
- [ ] Documentation status is current
- [ ] Known issues are current
- [ ] Blockers are current
- [ ] Related documents section is complete

---

## API Documentation

- [ ] New methods documented
- [ ] Parameters described
- [ ] Return values described
- [ ] Exceptions documented
- [ ] Examples provided

---

## Protocol Documentation

- [ ] Protocol specification updated (if behavior changed)
- [ ] Reference packets updated (if new patterns found)
- [ ] Response matching analysis updated (if applicable)
- [ ] Observed differences updated (if applicable)

---

## Cross-References

- [ ] All internal links work
- [ ] All document references are valid
- [ ] No broken references
- [ ] Consistent terminology used

---

## Machine-Readable Files

- [ ] CURRENT_STATUS.yaml updated
- [ ] TASK_STATE.yaml updated
- [ ] YAML syntax is valid
- [ ] All fields are current

---

## Findings

| Severity | Description | Document | Section |
|----------|-------------|----------|---------|
| | | | |

---

## Verdict

- [ ] **APPROVED** — Documentation is accurate and complete
- [ ] **APPROVED WITH NOTES** — Minor issues, non-blocking
- [ ] **REVISION REQUIRED** — Issues must be fixed

---

## Reviewer

- **Agent:** Auditor
- **Date:** ___________
- **Task ID:** ___________
