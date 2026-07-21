# CONTROL_CENTER.md — Control Center Documentation

**Last Updated:** 2026-07-18

---

## Purpose

The Control Center is the **single source of truth** for all AI agent operations. Every tool, every agent, and every decision reads from `CONTROL_CENTER.yaml` to determine the complete project status.

---

## Architecture

```
CONTROL_CENTER.yaml
        │
        ├──► bootstrap.py (loads first, stops if missing)
        ├──► project_dashboard.py (reads for display)
        ├──► status.py (reads for summary)
        ├──► state_sync.py (validates consistency)
        ├──► task_dispatcher.py (reads for task assignment)
        ├──► agent_selector.py (reads for agent selection)
        └──► session_manager.py (reads for session state)
```

---

## Fields

### project
```yaml
project:
  name: "Q-Scout Native Linux SDK"
  objective: "Native Python SDK for controlling Robobloq Q-Scout (RB-00002) via USB/UART"
  version: "0.2.0"
  status: "active"
  started: "2026-07-01"
```

**Purpose:** Basic project identification.

---

### repository
```yaml
repository:
  canonical: "/home/munumu/Qscout"
  branch: "main"
  source: "src/qscout/"
  tests: "tests/"
  docs: "docs/"
  evidence: "evidence/"
  project_management: "project_management/"
  tools: "tools/"
```

**Purpose:** File system locations for all project components.

---

### architecture
```yaml
architecture:
  status: "frozen"
  decision: "D-009"
  layers:
    - name: "Transport"
      module: "connection.py"
      layer: "SDK-01"
      status: "stable"
```

**Purpose:** Architecture status and layer definitions.

---

### current_phase
```yaml
current_phase:
  id: "SDK-02 Phase 2C"
  name: "Expand Public API"
  description: "Implement remaining sensor and actuator commands"
  previous: "SDK-02 Phase 2B — Physical SDK Validation"
  next: "SDK-03 — Full Coverage, CLI, Examples"
  started: "2026-07-18"
```

**Purpose:** Current SDK development phase.

---

### current_task
```yaml
current_task:
  id: "T-2C-01"
  title: "Implement GET_DEVICE_INFO Command"
  status: "pending"
  assigned_agent: "Programmer"
  priority: "P1"
  dependencies: []
```

**Purpose:** Currently active task.

---

### current_milestone
```yaml
current_milestone:
  id: "M-02C"
  name: "Public API Completion"
  target: "2026-07-25"
  progress: "0%"
```

**Purpose:** Current milestone target.

---

### current_agent
```yaml
current_agent:
  role: "Programmer"
  document: "AGENT_PROGRAMMER.md"
  status: "available"
```

**Purpose:** Agent currently responsible for the active task.

---

### next_agent
```yaml
next_agent:
  role: "Validator"
  document: "AGENT_VALIDATOR.md"
  reason: "After implementation, commands must be validated"
```

**Purpose:** Agent that will act next.

---

### assigned_agents
```yaml
assigned_agents:
  coordinator:
    role: "Coordinator"
    document: "AGENT_COORDINATOR.md"
    status: "available"
    tasks_assigned: 0
  programmer:
    role: "Programmer"
    document: "AGENT_PROGRAMMER.md"
    status: "available"
    tasks_assigned: 13
  auditor:
    role: "Auditor"
    document: "AGENT_AUDITOR.md"
    status: "available"
    tasks_assigned: 1
  validator:
    role: "Validator"
    document: "AGENT_VALIDATOR.md"
    status: "available"
    tasks_assigned: 0
```

**Purpose:** All agent roles and their current status.

---

### progress
```yaml
progress:
  total_tasks: 30
  completed_tasks: 16
  pending_tasks: 14
  blocked_tasks: 0
  percent_complete: 53.3
  phases_completed:
    - "Phase 0 — Initial idea and feasibility"
```

**Purpose:** Overall project progress metrics.

---

### tests
```yaml
tests:
  total: 119
  passing: 119
  failing: 0
  last_run: "2026-07-18"
  pass_rate: 100.0
  command: "PYTHONPATH=src python3 -m unittest discover -s tests"
```

**Purpose:** Test suite status.

---

### validation
```yaml
validation:
  physical_validation:
    status: "completed"
    date: "2026-07-17"
    commands:
      - name: "SET_LED"
        status: "PASS"
  yaml_validation: "PASS"
  docs_validation: "PASS"
  bootstrap_validation: "PASS"
```

**Purpose:** All validation results.

---

### documentation
```yaml
documentation:
  version: "2.0"
  last_update: "2026-07-18"
  total_files: 31
  status: "current"
```

**Purpose:** Documentation status.

---

### repository_health
```yaml
repository_health:
  status: "healthy"
  python_version: "3.12.3"
  pyyaml_installed: true
  sdk_files_intact: true
  all_directories_present: true
  all_required_files_present: true
  last_check: "2026-07-18"
```

**Purpose:** Repository health metrics.

---

### sessions
```yaml
sessions:
  active: false
  current_session: null
  last_session: null
  total_sessions: 0
```

**Purpose:** AI agent session state.

---

### blockers
```yaml
blockers: []
```

**Purpose:** Active blockers preventing progress.

---

### risks
```yaml
risks:
  - id: "R-001"
    description: "Some tests reference APIs not yet implemented"
    severity: "low"
    mitigation: "Tests will pass once Phase 2C is complete"
    status: "accepted"
```

**Purpose:** Identified risks and mitigations.

---

### backups
```yaml
backups:
  - name: "2026-07-16 Project Backup.md"
    date: "2026-07-16"
    location: "/home/munumu/Qscout/2026-07-16 Project Backup.md"
```

**Purpose:** Available project backups.

---

### release
```yaml
release:
  ready: false
  reason: "Phase SDK-02 Phase 2C in progress"
  version: "0.2.0"
  target_date: "2026-07-25"
```

**Purpose:** Release readiness status.

---

### next_actions
```yaml
next_actions:
  - order: 1
    action: "Implement GET_DEVICE_INFO Command"
    agent: "Programmer"
    task_id: "T-2C-01"
  - order: 2
    action: "Implement GET_INTERFACE_INFO Command"
    agent: "Programmer"
    task_id: "T-2C-02"
```

**Purpose:** Ordered list of next actions.

---

### last_update
```yaml
last_update: "2026-07-18T00:00:00"
```

**Purpose:** Timestamp of last update.

---

## Responsibilities

| File | Responsibility |
|------|---------------|
| CONTROL_CENTER.yaml | Master operational state (single source of truth) |
| CURRENT_STATUS.yaml | Technical SDK status (architecture, tests, validation) |
| TASK_STATE.yaml | Task execution state (completed, pending, blocked) |

---

## Synchronization

All three state files must be kept in sync:

1. **CONTROL_CENTER.yaml** is authoritative for operational decisions
2. **CURRENT_STATUS.yaml** provides technical SDK details
3. **TASK_STATE.yaml** tracks task execution

### Sync Rules

- When a task completes: Update all three files
- When tests change: Update CURRENT_STATUS.yaml and CONTROL_CENTER.yaml
- When architecture changes: Update CURRENT_STATUS.yaml and CONTROL_CENTER.yaml
- When blockers arise: Update CONTROL_CENTER.yaml

---

## Lifecycle

1. **Bootstrap:** Load CONTROL_CENTER.yaml (REQUIRED)
2. **Operation:** Read from CONTROL_CENTER.yaml
3. **Updates:** Modify all three files as needed
4. **Validation:** Run state_sync.py to verify consistency

---

## Recovery

If CONTROL_CENTER.yaml becomes corrupted:

1. **Determine source:** Check CURRENT_STATUS.yaml and TASK_STATE.yaml
2. **Rebuild:** Use information from the two secondary files
3. **Verify:** Run state_sync.py to confirm consistency
4. **Resume:** Continue operations

See [Recovery Strategy](#recovery-strategy) below.

---

## Recovery Strategy

### Priority Order

1. **CONTROL_CENTER.yaml** — Authoritative (rebuild first)
2. **CURRENT_STATUS.yaml** — Technical details (secondary source)
3. **TASK_STATE.yaml** — Execution state (tertiary source)

### Recovery Steps

1. If CONTROL_CENTER.yaml is missing or corrupted:
   - Read CURRENT_STATUS.yaml for technical details
   - Read TASK_STATE.yaml for task state
   - Rebuild CONTROL_CENTER.yaml from these sources

2. If CURRENT_STATUS.yaml is missing or corrupted:
   - Read CONTROL_CENTER.yaml for technical details
   - Rebuild CURRENT_STATUS.yaml

3. If TASK_STATE.yaml is missing or corrupted:
   - Read CONTROL_CENTER.yaml for task state
   - Rebuild TASK_STATE.yaml

### Verification

After any recovery:
```bash
python3 tools/state_sync.py
```

---

## Examples

### Reading Project Status

```python
import yaml

with open("project_management/CONTROL_CENTER.yaml") as f:
    cc = yaml.safe_load(f)

phase = cc["current_phase"]["id"]
task = cc["current_task"]["title"]
agent = cc["current_agent"]["role"]
```

### Updating Task Status

```python
import yaml
from datetime import datetime

with open("project_management/CONTROL_CENTER.yaml") as f:
    cc = yaml.safe_load(f)

cc["current_task"]["status"] = "completed"
cc["last_update"] = datetime.now().isoformat()

with open("project_management/CONTROL_CENTER.yaml", "w") as f:
    yaml.dump(cc, f, default_flow_style=False)
```

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [BOOTSTRAP_SYSTEM.md](BOOTSTRAP_SYSTEM.md) | Bootstrap system documentation |
| [PROJECT_STATE.md](PROJECT_STATE.md) | Project state overview |
| [PROJECT_OPERATING_SYSTEM.md](PROJECT_OPERATING_SYSTEM.md) | Operating procedures |
| [QUALITY_GATES.md](QUALITY_GATES.md) | Quality gates |
