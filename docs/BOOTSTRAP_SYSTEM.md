# BOOTSTRAP_SYSTEM.md — Bootstrap System Documentation

**Last Updated:** 2026-07-18

---

## Overview

The Bootstrap System allows any AI agent to start working on the Q-Scout project automatically with minimal human intervention. It inspects the repository, validates the environment, loads project state, and prepares the project for operation.

---

## Architecture

```
start_project.sh
    │
    ├──► health_check.py
    │       • Verify repository structure
    │       • Check required files
    │       • Validate Python version
    │       • Check YAML files
    │       • Check Markdown files
    │
    ├──► bootstrap.py
    │       • Locate project root
    │       • Verify directories
    │       • Verify files
    │       • Load state files
    │       • Determine phase and task
    │       • Display dashboard
    │
    ├──► project_dashboard.py
    │       • Display comprehensive status
    │       • Show progress
    │       • Show blockers
    │
    ├──► task_dispatcher.py
    │       • Analyze current task
    │       • Check dependencies
    │       • Determine responsible agent
    │       • Recommend next action
    │
    ├──► agent_selector.py
    │       • Select agent based on task type
    │       • Apply selection rules
    │       • Display agent assignments
    │
    └──► session_manager.py
            • Check session status
            • Manage session lifecycle
```

---

## Execution Order

1. **health_check.py** — Verify environment is healthy
2. **bootstrap.py** — Load project state and prepare
3. **project_dashboard.py** — Display current status
4. **task_dispatcher.py** — Determine next task
5. **agent_selector.py** — Select appropriate agent
6. **session_manager.py** — Manage session state

---

## Utilities

### bootstrap.py

**Purpose:** Main bootstrap utility that locates project root, validates environment, and loads state.

**Responsibilities:**
1. Locate project root automatically
2. Verify mandatory directories exist
3. Verify mandatory documents exist
4. Verify YAML files
5. Verify Markdown files
6. Load CURRENT_STATUS.yaml
7. Load TASK_STATE.yaml
8. Determine current phase
9. Determine current task
10. Determine assigned agent
11. Display coordinator dashboard
12. Exit with appropriate return code

**Usage:**
```bash
python3 tools/bootstrap.py
```

**Exit Codes:**
- `0`: Success
- `1`: Failure

---

### health_check.py

**Purpose:** Verify repository health including structure, files, Python version, and consistency.

**Checks:**
- Python version (requires ≥ 3.10)
- Required directories
- Required files
- YAML file validity
- Markdown file presence
- SDK source files
- Test files

**Output:**
- `PASS` — All checks passed
- `WARNING` — Some checks have warnings
- `FAIL` — One or more checks failed

**Usage:**
```bash
python3 tools/health_check.py
```

---

### project_dashboard.py

**Purpose:** Display comprehensive project status in human-readable format.

**Displays:**
- Repository information
- Current phase and task
- Agent assignments
- Test status
- Documentation status
- Physical validation status
- Overall progress
- Blockers

**Usage:**
```bash
python3 tools/project_dashboard.py
```

---

### task_dispatcher.py

**Purpose:** Read TASK_STATE.yaml and determine current task, responsible agent, and next action.

**Analyzes:**
- Current task and its status
- Dependencies and prerequisites
- Completion status
- Next ready-to-execute task
- Responsible agent

**Usage:**
```bash
python3 tools/task_dispatcher.py
```

---

### agent_selector.py

**Purpose:** Select the appropriate agent role based on task type.

**Selection Rules:**
| Task Type | Agent |
|-----------|-------|
| Programming (implement, code, fix) | Programmer |
| Validation (validate, verify, test) | Validator |
| Documentation (document, review, audit) | Auditor |
| Planning (plan, assign, coordinate) | Coordinator |

**Usage:**
```bash
python3 tools/agent_selector.py
```

---

### session_manager.py

**Purpose:** Manage AI agent sessions: open, close, resume, and maintain history.

**Actions:**
- `open` — Open a new session
- `close` — Close current session
- `resume` — Resume a previous session
- `status` — Check session status

**Usage:**
```bash
python3 tools/session_manager.py open
python3 tools/session_manager.py close
python3 tools/session_manager.py resume
python3 tools/session_manager.py status
```

---

### validate_yaml.py

**Purpose:** Verify YAML syntax, required fields, missing keys, and duplicate keys.

**Validates:**
- CURRENT_STATUS.yaml
- TASK_STATE.yaml

**Output:**
- `PASS` — Valid YAML
- `WARNING` — Minor issues
- `FAIL` — Syntax errors or missing fields

**Usage:**
```bash
python3 tools/validate_yaml.py
```

---

### validate_docs.py

**Purpose:** Verify documentation integrity including links, required documents, and titles.

**Validates:**
- Broken links
- Missing required documents
- Orphan documents
- Duplicate titles

**Output:**
- `PASS` — All validations passed
- `WARNING` — Minor issues
- `FAIL` — Critical issues found

**Usage:**
```bash
python3 tools/validate_docs.py
```

---

### load_state.py

**Purpose:** Load and display project state from YAML files.

**Loads:**
- CURRENT_STATUS.yaml
- TASK_STATE.yaml

**Displays:**
- Current phase
- Current task
- Test status
- Agent status

**Usage:**
```bash
python3 tools/load_state.py
```

---

## Commands

### Quick Start

```bash
./start_project.sh
```

### Individual Commands

```bash
make health       # Run health check
make dashboard    # Display dashboard
make validate     # Run all validators
make status       # Load project state
make dispatch     # Run task dispatcher
make agents       # Run agent selector
make tests        # Run SDK tests
make session-open # Open a new session
make session-close # Close current session
```

---

## Troubleshooting

### Python Not Found

```bash
ERROR: Python3 not found
```

**Solution:** Ensure Python 3.10+ is installed and in PATH.

### PyYAML Not Installed

```bash
WARNING: PyYAML not installed
```

**Solution:**
```bash
pip install pyyaml
```

### Health Check Fails

```bash
RESULT: FAIL
```

**Solution:** Check the specific failure message and fix the issue (missing files, invalid YAML, etc.).

### Bootstrap Fails

```bash
FAIL: Could not locate project root
```

**Solution:** Ensure you are running from the project root directory.

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [START_HERE.md](START_HERE.md) | Entry point for new agents |
| [PROJECT_STATE.md](PROJECT_STATE.md) | Current project status |
| [PROJECT_OPERATING_SYSTEM.md](PROJECT_OPERATING_SYSTEM.md) | Operating procedures |
| [QUALITY_GATES.md](QUALITY_GATES.md) | Quality gates |
| [PROJECT_INDEX.md](PROJECT_INDEX.md) | Master index |
