# ARCHITECTURE_CLEANUP_PLAN.md — Multi-Agent System Cleanup

**Created:** 2026-07-18
**Based on:** MULTI_AGENT_ARCHITECTURE_AUDIT.md
**Scope:** All 34 project management files (6,070 lines)

---

## 1. Document Classification

### 1.1 Active Documents (Keep As-Is)

| File | Lines | Reason |
|------|-------|--------|
| `PROJECT_RULES.md` | 89 | Permanent rules, never changes |
| `QUALITY_GATES.md` | 261 | Gate definitions, stable |
| `ROADMAP.md` | 221 | Historical record, append-only |
| `CHANGELOG.md` | 306 | Change log, append-only |
| `DECISIONS.md` | 133 | Decision log, append-only |
| `AGENT_VALIDATOR.md` | 236 | Detailed validation checks |
| `AGENT_WORKFLOW.md` | 325 | Canonical communication protocol |
| `sessions/CURRENT_SESSION.md` | 70 | Active session snapshot |
| `sessions/NEXT_SESSION.md` | 58 | Next session prep |
| `sessions/BLOCKERS.md` | 61 | Active blocker tracking |
| `sessions/SESSION_HISTORY.md` | 92 | Session log |
| `docs/checklists/` (4 files) | 450 | Review checklists |
| `templates/` (4 files) | 400 | Document templates |
| **Subtotal** | **2,552** | |

### 1.2 Active Documents (Modify)

| File | Lines | Change |
|------|-------|--------|
| `START_HERE.md` | 125 | Absorb HANDOVER_PROTOCOL.md |
| `AGENT_MANIFEST.md` | 264 | Absorb AGENT_COORDINATOR/PROGRAMMER/AUDITOR.md |
| `AGENT_WORKFLOW.md` | 325 | Absorb PROJECT_OPERATING_SYSTEM.md + AUTONOMY_GUIDE.md |
| `CONTROL_CENTER.yaml` | 242 | Absorb CURRENT_STATUS.yaml fields |
| `TASK_STATE.yaml` | 189 | Remove fields already in CC |
| **Subtotal** | **1,145** | |

### 1.3 Deprecate (Delete)

| File | Lines | Reason |
|------|-------|--------|
| `PROJECT_STATE.md` | 234 | Replaced by CONTROL_CENTER.yaml |
| `CURRENT_STATUS.yaml` | 128 | Merged into CONTROL_CENTER.yaml |
| `TASK_QUEUE.md` | 355 | Replaced by TASK_STATE.yaml + CC |
| `COORDINATOR_DASHBOARD.md` | 146 | Replaced by `make dashboard` |
| `PROJECT_INDEX.md` | 196 | Tools find files automatically |
| `AGENT_COORDINATOR.md` | 109 | Merged into AGENT_MANIFEST.md |
| `AGENT_PROGRAMMER.md` | 118 | Merged into AGENT_MANIFEST.md |
| `AGENT_AUDITOR.md` | 139 | Merged into AGENT_MANIFEST.md |
| `HANDOVER_PROTOCOL.md` | 243 | Merged into START_HERE.md |
| `AUTONOMY_GUIDE.md` | 264 | Merged into AGENT_WORKFLOW.md |
| `PROJECT_OPERATING_SYSTEM.md` | 616 | Merged into AGENT_WORKFLOW.md |
| **Subtotal** | **2,548** | |

---

## 2. Source of Truth Design

### 2.1 State Hierarchy

```
CONTROL_CENTER.yaml          ← Authoritative for ALL operational state
├── TASK_STATE.yaml          ← Task execution details
├── sessions/                ← Session-specific state
├── CHANGELOG.md             ← Append-only history
├── ROADMAP.md               ← Append-only roadmap
└── DECISIONS.md             ← Append-only decisions
```

### 2.2 Single Source of Truth: CONTROL_CENTER.yaml

| Data Point | Before (Files) | After (Only Here) |
|------------|----------------|-------------------|
| Current phase | 7 files | CC only |
| Current task | 4 files | CC + TASK_STATE.yaml |
| Test count | 5 files | CC only |
| Architecture status | 4 files | CC + DECISIONS.md |
| Blockers | 3 files | CC + sessions/BLOCKERS.md |
| Risks | 3 files | CC only |
| Release status | 2 files | CC only |
| Agent status | 3 files | CC only |
| Documentation version | 2 files | CC only |
| Physical validation | 3 files | CC only |
| Repository health | 1 file | CC only |

### 2.3 Read-Only Documents (Never Change)

| File | Purpose |
|------|---------|
| `PROJECT_RULES.md` | Permanent rules |
| `QUALITY_GATES.md` | Quality thresholds |
| `templates/*` | Document templates |

---

## 3. Document Responsibility Model

### 3.1 Responsibility Matrix

| Document | Owner | Read | Write | Append | Source of Truth? |
|----------|-------|------|-------|--------|-----------------|
| `CONTROL_CENTER.yaml` | Coordinator | All | Coordinator | — | YES (operational) |
| `TASK_STATE.yaml` | Coordinator | All | Coordinator | — | YES (execution) |
| `START_HERE.md` | Coordinator | All | Coordinator | — | Entry point |
| `PROJECT_RULES.md` | Human | All | Human | — | YES (rules) |
| `QUALITY_GATES.md` | Coordinator | All | Auditor | — | YES (gates) |
| `AGENT_MANIFEST.md` | Coordinator | All | Coordinator | — | Agent definitions |
| `AGENT_VALIDATOR.md` | Validator | Validator | Auditor | — | Validation checks |
| `AGENT_WORKFLOW.md` | All | All | Coordinator | — | Communication protocol |
| `ROADMAP.md` | All | All | Coordinator | — | NO (historical) |
| `CHANGELOG.md` | All | All | Auditor | Coordinator | NO (append-only) |
| `DECISIONS.md` | All | All | Human | — | NO (log) |
| `sessions/*` | Active agent | All | Active agent | — | NO (session data) |
| `docs/checklists/*` | Auditor | Auditor | Human | — | Reusable checklists |
| `templates/*` | All | All | Human | — | Reusable templates |

### 3.2 Documentation Ownership Rules

1. **Coordinator** updates: CONTROL_CENTER.yaml, TASK_STATE.yaml, START_HERE.md, AGENT_MANIFEST.md
2. **Auditor** updates: CHANGELOG.md, docs/checklists/*, QUALITY_GATES.md
3. **Validator** reads: AGENT_VALIDATOR.md, QUALITY_GATES.md, sessions/BLOCKERS.md
4. **Programmer** reads: AGENT_WORKFLOW.md, CONTROL_CENTER.yaml
5. **Human** updates: PROJECT_RULES.md, DECISIONS.md, templates/*, docs/checklists/*
6. **No agent** updates: ROADMAP.md (append-only by Coordinator with human approval)

---

## 4. Agent Responsibility Model

### 4.1 Updated Agent Boundaries

| Agent | Primary Responsibility | Documents It Reads | Documents It Writes |
|-------|----------------------|-------------------|---------------------|
| **Coordinator** | Orchestrate work, maintain state | CC, TASK_STATE, AGENT_WORKFLOW, START_HERE | CC, TASK_STATE, START_HERE, AGENT_MANIFEST |
| **Programmer** | Implement code, write tests | CC, AGENT_WORKFLOW, TASK_STATE | Code files, test files |
| **Auditor** | Review code, update docs | CC, AGENT_WORKFLOW, AGENT_MANIFEST, checklists | CHANGELOG, docs/checklists, QUALITY_GATES |
| **Validator** | Validate code, test execution | CC, AGENT_VALIDATOR, QUALITY_GATES, TASK_STATE | sessions/BLOCKERS |

### 4.2 Responsibility Conflict Resolution

| Conflict | Before | After |
|----------|--------|-------|
| Who updates PROJECT_STATE.md? | Coordinator + Auditor | DEPRECATED — CC is source |
| Who updates CURRENT_STATUS.yaml? | Coordinator | DEPRECATED — merged into CC |
| Who updates TASK_QUEUE.md? | Coordinator | DEPRECATED — TASK_STATE.yaml |
| Who updates test count? | 5 files | CC only |
| Who updates phase status? | 8 files | CC only |

### 4.3 Workflow Update (After Cleanup)

```
Step 1: Coordinator reads CC, assigns task → updates TASK_STATE.yaml
Step 2: Programmer implements → writes code/tests
Step 3: Tests run automatically → Validator checks
Step 4: Auditor reviews → updates CHANGELOG, docs
Step 5: Coordinator updates CC (single state change)
```

**Before:** 8 files updated per phase change
**After:** 2 files updated (CC + TASK_STATE.yaml)

---

## 5. Automatic Generation Plan

### 5.1 Generated Documents

| Document | Generator | Trigger | Source Data |
|----------|-----------|---------|-------------|
| `COORDINATOR_DASHBOARD.md` | `make dashboard` | On demand | CC + TASK_STATE |
| `PROJECT_INDEX.md` | `make index` | On demand | File system scan |
| Session summary | `tools/session_manager.py` | Session end | CC + TASK_STATE |
| Status report | `tools/status.py` | On demand | CC |
| Project ready check | `tools/project_ready.py` | Before work | CC + TASK_STATE |

### 5.2 State Synchronization

| Source | Target | Script | Trigger |
|--------|--------|--------|---------|
| CC | TASK_STATE.yaml | `tools/state_sync.py` | After CC update |
| CC | sessions/BLOCKERS.md | `tools/state_sync.py` | After CC update |
| CC | START_HERE.md (phase) | Manual | Phase transition |
| CC | AGENT_WORKFLOW.md (references) | Manual | Document reference change |

### 5.3 Validation Scripts

| Script | What It Validates | Frequency |
|--------|------------------|-----------|
| `tools/validate_yaml.py` | YAML syntax + CC schema | Every CC update |
| `tools/validate_docs.py` | Doc links + consistency | Every doc update |
| `tools/health_check.py` | Repository health | Every session start |
| `tools/bootstrap.py` | Project readiness | Before work |

---

## 6. Future Directory Structure

### 6.1 Before (34 files, 6,070 lines)

```
project_management/
├── AGENT_AUDITOR.md              (139)
├── AGENT_COORDINATOR.md          (109)
├── AGENT_MANIFEST.md             (264)
├── AGENT_PROGRAMMER.md           (118)
├── AGENT_VALIDATOR.md            (236)
├── AGENT_WORKFLOW.md             (325)
├── AUTONOMY_GUIDE.md             (264)
├── CHANGELOG.md                  (306)
├── CONTROL_CENTER.yaml           (242)
├── COORDINATOR_DASHBOARD.md      (146)
├── CURRENT_STATUS.yaml           (128)
├── DECISIONS.md                  (133)
├── HANDOVER_PROTOCOL.md          (243)
├── PROJECT_INDEX.md              (196)
├── PROJECT_OPERATING_SYSTEM.md   (616)
├── PROJECT_RULES.md              (89)
├── PROJECT_STATE.md              (234)
├── QUALITY_GATES.md              (261)
├── ROADMAP.md                    (221)
├── START_HERE.md                 (125)
├── TASK_QUEUE.md                 (355)
├── TASK_STATE.yaml               (189)
├── docs/
│   └── checklists/
│       ├── code_review.md        (105)
│       ├── documentation_review.md (108)
│       ├── physical_validation.md (127)
│       └── release_checklist.md  (110)
├── sessions/
│   ├── BLOCKERS.md               (61)
│   ├── CURRENT_SESSION.md        (70)
│   ├── NEXT_SESSION.md           (58)
│   └── SESSION_HISTORY.md        (92)
└── templates/
    ├── audit_template.md         (107)
    ├── decision_template.md      (103)
    ├── handover_template.md      (134)
    └── task_template.md          (56)
```

### 6.2 After (18 files, ~3,200 lines)

```
project_management/
├── START_HERE.md                 (~200)  ← absorbed HANDOVER_PROTOCOL
├── CONTROL_CENTER.yaml           (~370)  ← absorbed CURRENT_STATUS
├── TASK_STATE.yaml               (~189)  ← reduced duplication
├── AGENT_MANIFEST.md             (~450)  ← absorbed role-specific docs
├── AGENT_VALIDATOR.md            (236)   ← kept as-is
├── AGENT_WORKFLOW.md             (~500)  ← absorbed POS + AUTONOMY
├── PROJECT_RULES.md              (89)    ← kept as-is
├── QUALITY_GATES.md              (261)   ← kept as-is
├── ROADMAP.md                    (221)   ← kept as-is
├── CHANGELOG.md                  (306)   ← kept as-is
├── DECISIONS.md                  (133)   ← kept as-is
├── docs/
│   └── checklists/               (450)   ← kept as-is
├── sessions/                     (281)   ← kept as-is
└── templates/                    (400)   ← kept as-is
```

### 6.3 Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total files | 34 | 18 | **-16 files (-47%)** |
| Total lines | 6,070 | ~3,200 | **-2,870 lines (-47%)** |
| Files per phase change | 8 | 2 | **-75%** |
| Data duplication instances | 12 | 0 | **-100%** |
| Agent confusion points | 5 | 0 | **-100%** |

---

## 7. Migration Strategy

### 7.1 Migration Order

| Phase | Action | Files Affected | Risk |
|-------|--------|----------------|------|
| **1** | Merge CURRENT_STATUS.yaml → CONTROL_CENTER.yaml | 2 | LOW |
| **2** | Merge role-specific agent docs → AGENT_MANIFEST.md | 4 | LOW |
| **3** | Merge HANDOVER_PROTOCOL → START_HERE.md | 2 | LOW |
| **4** | Merge AUTONOMY_GUIDE + POS → AGENT_WORKFLOW.md | 3 | MEDIUM |
| **5** | Remove duplicated fields from TASK_STATE.yaml | 1 | LOW |
| **6** | Deprecate PROJECT_STATE.md | 1 | LOW |
| **7** | Deprecate TASK_QUEUE.md | 1 | LOW |
| **8** | Deprecate COORDINATOR_DASHBOARD.md | 1 | LOW |
| **9** | Deprecate PROJECT_INDEX.md | 1 | LOW |
| **10** | Update AGENT_WORKFLOW.md references | 1 | LOW |
| **11** | Update tools to read from new sources | 7 | MEDIUM |

### 7.2 Migration Rules

1. **Read before delete:** Always read source file before merging
2. **Preserve unique content:** Never discard unique information
3. **Update references:** Fix all cross-references after merge
4. **Verify tools:** Run `make health` after each phase
5. **Backup first:** Create backup before each phase
6. **One phase at a time:** Complete and verify before next phase

### 7.3 Rollback Plan

Each phase has a rollback:
1. **Restore from backup:** Revert file changes
2. **Update references:** Restore cross-references
3. **Verify tools:** Run `make health`
4. **Document rollback:** Record in CHANGELOG.md

---

## 8. Risk Analysis

### 8.1 Migration Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Data loss during merge | HIGH | LOW | Read before delete, backup first |
| Broken cross-references | MEDIUM | HIGH | Update all references after each phase |
| Tool failures | MEDIUM | MEDIUM | Run `make health` after each phase |
| Agent confusion during transition | LOW | MEDIUM | Clear deprecation markers |
| Human confusion | LOW | LOW | Document changes in CHANGELOG.md |

### 8.2 Post-Migration Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| CC becomes bottleneck | LOW | LOW | CC is designed for single-source |
| Over-simplification | LOW | LOW | Keep detailed docs (VALIDATOR, WORKFLOW) |
| Missing historical data | LOW | LOW | ROADMAP + CHANGELOG preserve history |

### 8.3 Risk Acceptance

- **Accepted:** 16 files will be deleted (content preserved in merged files)
- **Accepted:** 2,548 lines will be removed (unique content preserved)
- **Accepted:** Some cross-references will need manual update
- **Accepted:** Tools may need minor updates after migration

---

## 9. File Count and Size Metrics

### 9.1 Current State

| Category | Files | Lines | % of Total |
|----------|-------|-------|------------|
| Operational Documents | 12 | 2,941 | 48% |
| Agent Documents | 5 | 866 | 14% |
| Workflow Documents | 2 | 568 | 9% |
| State Files | 3 | 559 | 9% |
| Checklists | 4 | 450 | 7% |
| Templates | 4 | 400 | 7% |
| Sessions | 4 | 281 | 5% |
| **Total** | **34** | **6,070** | **100%** |

### 9.2 Target State

| Category | Files | Lines | % of Total |
|----------|-------|-------|------------|
| Entry Point | 1 | ~200 | 6% |
| State Files | 2 | ~559 | 18% |
| Agent Documents | 2 | ~686 | 21% |
| Workflow Documents | 1 | ~500 | 16% |
| Reference Documents | 4 | ~942 | 29% |
| Supporting Files | 8 | ~313 | 10% |
| **Total** | **18** | **~3,200** | **100%** |

### 9.3 Comparison

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total files | 34 | 18 | -47% |
| Total lines | 6,070 | ~3,200 | -47% |
| Max files to update per change | 8 | 2 | -75% |
| Data duplication instances | 12 | 0 | -100% |
| Agent confusion points | 5 | 0 | -100% |
| Maintenance burden | HIGH | LOW | -80% |
| Architecture score | 5/10 | 8/10 | +60% |

---

## 10. Expected Improvements

### 10.1 Quantitative Improvements

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Files | 34 | 18 | **-47%** |
| Lines | 6,070 | ~3,200 | **-47%** |
| Phase change updates | 8 files | 2 files | **-75%** |
| Data duplication | 12 instances | 0 | **-100%** |
| Agent confusion | 5 points | 0 | **-100%** |
| Maintenance burden | HIGH | LOW | **-80%** |

### 10.2 Qualitative Improvements

| Aspect | Before | After |
|--------|--------|-------|
| Source of truth | Ambiguous (7 files) | Clear (1 file) |
| Agent responsibilities | Overlapping | Distinct |
| Document purpose | Unclear | Well-defined |
| Tool integration | Partial | Complete |
| Onboarding speed | Slow (34 files) | Fast (18 files) |
| State consistency | Manual | Automated |

### 10.3 Developer Experience

| Scenario | Before | After |
|----------|--------|-------|
| New agent onboarding | Read 34 files | Read START_HERE → CC → WORKFLOW |
| Phase transition | Update 8 files | Update CC (1 file) |
| Status check | Read 5 files | Run `make status` |
| Task assignment | Read CC + TASK_STATE + TASK_QUEUE | Read CC + TASK_STATE |
| Blocker reporting | Update CC + TASK_STATE + BLOCKERS | Update CC (auto-sync) |

---

## 11. Implementation Phases

### 11.1 Phase 1: Core State Consolidation

**Duration:** 30 minutes
**Risk:** LOW

1. Read CURRENT_STATUS.yaml
2. Merge unique fields into CONTROL_CENTER.yaml
3. Update TASK_STATE.yaml references
4. Delete CURRENT_STATUS.yaml
5. Run `make validate`

### 11.2 Phase 2: Agent Document Merge

**Duration:** 45 minutes
**Risk:** LOW

1. Read AGENT_COORDINATOR.md, AGENT_PROGRAMMER.md, AGENT_AUDITOR.md
2. Merge role-specific content into AGENT_MANIFEST.md
3. Update CONTROL_CENTER.yaml references
4. Delete role-specific files
5. Run `make validate`

### 11.3 Phase 3: Entry Point Consolidation

**Duration:** 30 minutes
**Risk:** LOW

1. Read HANDOVER_PROTOCOL.md
2. Merge onboarding content into START_HERE.md
3. Update cross-references
4. Delete HANDOVER_PROTOCOL.md
5. Run `make validate`

### 11.4 Phase 4: Workflow Consolidation

**Duration:** 45 minutes
**Risk:** MEDIUM

1. Read PROJECT_OPERATING_SYSTEM.md, AUTONOMY_GUIDE.md
2. Merge into AGENT_WORKFLOW.md
3. Update all references
4. Delete source files
5. Run `make validate`

### 11.5 Phase 5: Deprecation

**Duration:** 30 minutes
**Risk:** LOW

1. Delete PROJECT_STATE.md
2. Delete TASK_QUEUE.md
3. Delete COORDINATOR_DASHBOARD.md
4. Delete PROJECT_INDEX.md
5. Update remaining references
6. Run `make validate`

### 11.6 Phase 6: Tool Updates

**Duration:** 30 minutes
**Risk:** MEDIUM

1. Update bootstrap.py references
2. Update project_dashboard.py references
3. Update health_check.py references
4. Update validate_yaml.py references
5. Run `make health`

---

## 12. Verification Criteria

### 12.1 Success Criteria

| Criterion | Target | Verification |
|-----------|--------|--------------|
| File count | ≤ 18 | `ls project_management/*.md project_management/*.yaml \| wc -l` |
| Total lines | ≤ 3,200 | `wc -l project_management/**/*.md project_management/**/*.yaml` |
| Data duplication | 0 instances | Manual review |
| Tool functionality | All pass | `make health` |
| YAML validation | All pass | `make validate` |
| Documentation links | All valid | `make validate-docs` |
| Cross-references | All updated | Manual review |
| No data loss | Confirmed | Manual comparison |

### 12.2 Final Verification Checklist

- [ ] All 34 original files reviewed
- [ ] 16 files deleted (content preserved in merged files)
- [ ] 5 files modified (content merged)
- [ ] 13 files unchanged
- [ ] All cross-references updated
- [ ] All tools updated to read from new sources
- [ ] `make health` passes
- [ ] `make validate` passes
- [ ] No data duplication detected
- [ ] All agent responsibilities clearly defined
- [ ] CONTROL_CENTER.yaml is single source of truth
- [ ] Architecture score improved from 5/10 to 8/10

### 12.3 Architecture Score Improvement

| Category | Before | After |
|----------|--------|-------|
| Functional completeness | 8/10 | 8/10 |
| Information architecture | 4/10 | 8/10 |
| Maintainability | 3/10 | 8/10 |
| Documentation weight | 3/10 | 7/10 |
| Agent clarity | 7/10 | 9/10 |
| Git readiness | 6/10 | 6/10 |
| Automation potential | 5/10 | 8/10 |
| **Overall** | **5/10** | **8/10** |

---

**ARCHITECTURE CLEANUP PLAN COMPLETED**
