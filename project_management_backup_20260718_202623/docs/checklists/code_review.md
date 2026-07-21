# Code Review Checklist

**Used by:** Auditor Agent
**When:** After Programmer reports task completion

---

## Pre-Review

- [ ] Receive review request from Coordinator
- [ ] Read task description from TASK_QUEUE.md
- [ ] Read Programmer's completion report
- [ ] Identify changed files

---

## Code Quality

- [ ] Code follows existing conventions (snake_case, PascalCase, etc.)
- [ ] No hardcoded values (use constants or configuration)
- [ ] Proper error handling (try/except where appropriate)
- [ ] No debug code or print statements left in
- [ ] No commented-out code blocks
- [ ] Meaningful variable and function names
- [ ] Appropriate comments (only where necessary)

---

## Architecture Compliance

- [ ] Layer separation maintained
- [ ] Protocol layer not mixed with transport layer
- [ ] No circular imports
- [ ] Follows existing module structure
- [ ] Uses existing utilities and helpers
- [ ] Does not introduce new dependencies without justification

---

## SDK-Specific Checks

- [ ] Checksum validation present (if modifying protocol)
- [ ] Order ID correlation correct (if modifying response handling)
- [ ] Motor speeds clamped to ±100
- [ ] Auto-detection uses VID:PID 1A86:7523
- [ ] Transport layer does not know protocol details
- [ ] Protocol layer does not know transport details

---

## Test Quality

- [ ] New code has corresponding tests
- [ ] Tests cover normal cases
- [ ] Tests cover edge cases
- [ ] Tests cover error cases
- [ ] Test names are descriptive
- [ ] Tests are independent (no shared state)
- [ ] All tests pass:
  ```bash
  cd /home/munumu/Qscout
  PYTHONPATH=src python3 -m unittest discover -s tests
  ```

---

## Documentation

- [ ] README updated (if public API changed)
- [ ] Docstrings added/updated
- [ ] CHANGELOG.md entry prepared
- [ ] No broken cross-references

---

## Security

- [ ] No secrets or keys in code
- [ ] No hardcoded file paths (use auto-detection)
- [ ] No external network calls without justification
- [ ] Input validation present

---

## Findings

| Severity | Description | File | Line |
|----------|-------------|------|------|
| | | | |

---

## Verdict

- [ ] **APPROVED** — No issues found
- [ ] **APPROVED WITH NOTES** — Minor issues, non-blocking
- [ ] **REVISION REQUIRED** — Issues must be fixed before approval

---

## Reviewer

- **Agent:** Auditor
- **Date:** ___________
- **Task ID:** ___________
