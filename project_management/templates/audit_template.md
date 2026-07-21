# Audit Template

Use this template when creating audit findings reports.

---

## Audit Report: [TASK_ID] — [Task Title]

| Field | Value |
|-------|-------|
| Task ID | [TASK_ID] |
| Task Title | [Task Title] |
| Auditor | [Agent Name] |
| Date | [YYYY-MM-DD] |
| Status | [APPROVED/APPROVED WITH NOTES/REVISION REQUIRED] |

---

## Review Scope

[Describe what was reviewed:]

- Files reviewed: [list files]
- Tests reviewed: [list test files]
- Documentation reviewed: [list docs]

---

## Findings

### Critical Issues

[List any critical issues that must be fixed:]

1. **[Issue Title]**
   - File: [filename]
   - Line: [line number]
   - Description: [what is wrong]
   - Impact: [what could go wrong]
   - Recommendation: [how to fix]

### Major Issues

[List any major issues that should be fixed:]

1. **[Issue Title]**
   - File: [filename]
   - Line: [line number]
   - Description: [what is wrong]
   - Impact: [what could go wrong]
   - Recommendation: [how to fix]

### Minor Issues

[List any minor issues or improvements:]

1. **[Issue Title]**
   - File: [filename]
   - Line: [line number]
   - Description: [what is wrong]
   - Recommendation: [how to fix]

---

## Test Coverage

- [ ] All new code has tests
- [ ] Tests cover normal cases
- [ ] Tests cover edge cases
- [ ] Tests cover error cases
- [ ] All tests pass

---

## Documentation

- [ ] README updated (if needed)
- [ ] CHANGELOG entry prepared
- [ ] API documentation current
- [ ] Cross-references valid

---

## Verdict

[Select one:]

- [ ] **APPROVED** — No issues found
- [ ] **APPROVED WITH NOTES** — Minor issues, non-blocking
- [ ] **REVISION REQUIRED** — Issues must be fixed before approval

---

## Recommendations

[List any recommendations for future work:]

1. [Recommendation 1]
2. [Recommendation 2]

---

## Sign-Off

- **Auditor:** [Agent Name]
- **Date:** [YYYY-MM-DD]
- **Task ID:** [TASK_ID]
