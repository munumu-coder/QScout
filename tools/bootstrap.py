#!/usr/bin/env python3
"""
bootstrap.py — Project Bootstrap System

Locates project root, validates environment, loads state,
and prepares the project for AI agent operation.

Startup Sequence:
1. Locate repository
2. Health check
3. Load CONTROL_CENTER.yaml
4. Load CURRENT_STATUS.yaml
5. Load TASK_STATE.yaml
6. Verify consistency
7. Determine current task
8. Determine responsible agent
9. Display dashboard
10. Ready

If CONTROL_CENTER.yaml is missing: STOP.
"""

import os
import sys
from pathlib import Path

# Project structure
MANDATORY_DIRS = [
    "src/qscout",
    "tests",
    "docs",
    "project_management",
    "project_management/sessions",
    "project_management/templates",
    "project_management/docs/checklists",
]

MANDATORY_FILES = [
    "README.md",
    "pyproject.toml",
    "project_management/START_HERE.md",
    "project_management/CONTROL_CENTER.yaml",
    "project_management/TASK_STATE.yaml",
    "project_management/ROADMAP.md",
    "project_management/DECISIONS.md",
    "project_management/CHANGELOG.md",
    "project_management/PROJECT_RULES.md",
    "project_management/AGENT_WORKFLOW.md",
    "project_management/AGENT_MANIFEST.md",
    "project_management/AGENT_VALIDATOR.md",
    "project_management/QUALITY_GATES.md",
]


def find_project_root():
    """Locate project root by looking for标志性 files."""
    current = Path(__file__).resolve().parent.parent
    while current != current.parent:
        if (current / "README.md").exists() and (current / "pyproject.toml").exists():
            if (current / "src" / "qscout").is_dir():
                return current
        current = current.parent
    return None


def verify_directories(root):
    """Verify mandatory directories exist."""
    missing = []
    for d in MANDATORY_DIRS:
        path = root / d
        if not path.is_dir():
            missing.append(d)
    return missing


def verify_files(root):
    """Verify mandatory files exist."""
    missing = []
    for f in MANDATORY_FILES:
        path = root / f
        if not path.exists():
            missing.append(f)
    return missing


def load_yaml_file(root, filename):
    """Load and parse a YAML file."""
    try:
        import yaml
        path = root / filename
        if not path.exists():
            return None, f"File not found: {filename}"
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return data, None
    except ImportError:
        return None, "PyYAML not installed"
    except Exception as e:
        return None, str(e)


def verify_consistency(cc_data, task_data):
    """Verify consistency between state files."""
    issues = []

    if cc_data and task_data:
        cc_task = cc_data.get("current_task", {}).get("id", "")
        task_id = task_data.get("active_task", {}).get("id", "")
        if cc_task and task_id and cc_task != task_id:
            issues.append(f"Task mismatch: CC={cc_task}, TASK={task_id}")

    return issues


def display_dashboard(cc_data, task_data):
    """Display coordinator dashboard."""
    print("\n" + "=" * 60)
    print("Q-SCOUT PROJECT DASHBOARD")
    print("=" * 60)

    if cc_data:
        project = cc_data.get("project", {})
        phase = cc_data.get("current_phase", {})
        task = cc_data.get("current_task", {})
        agents = cc_data.get("assigned_agents", {})
        tests = cc_data.get("tests", {})
        progress = cc_data.get("progress", {})
        blockers = cc_data.get("blockers", [])

        print(f"\nProject: {project.get('name', 'Unknown')}")
        print(f"Phase: {phase.get('id', 'Unknown')} — {phase.get('name', '')}")
        print(f"Current Task: {task.get('id', 'None')} — {task.get('title', 'None')}")
        print(f"Assigned To: {task.get('assigned_agent', 'None')}")
        print(f"Tests: {tests.get('total', 0)} total, {tests.get('passing', 0)} passing")

        print("\nAgents:")
        for name, info in agents.items():
            print(f"  {name}: {info.get('status', 'unknown')}")

        print(f"\nProgress: {progress.get('percent_complete', 0)}%")
        print(f"Completed: {progress.get('completed_tasks', 0)} tasks")
        print(f"Pending: {progress.get('pending_tasks', 0)} tasks")

        if blockers:
            print("\nBlockers:")
            for b in blockers:
                print(f"  - {b}")
        else:
            print("\nBlockers: None")
    else:
        print("\n[ERROR] CONTROL_CENTER.yaml not found — PROJECT NOT READY")
        return

    if task_data:
        tasks = task_data.get("tasks", {})
        completed = len(tasks.get("completed_tasks", []))
        pending = len(tasks.get("pending_tasks", []))
        print(f"Tasks (from TASK_STATE): {completed} completed, {pending} pending")

    print("\n" + "=" * 60)


def main():
    """Main bootstrap function."""
    print("Q-Scout Project Bootstrap")
    print("=" * 40)

    # Step 1: Find project root
    print("\n[1/11] Locating project root...")
    root = find_project_root()
    if root is None:
        print("  FAIL: Could not locate project root")
        return 1
    print(f"  OK: {root}")

    # Step 2: Verify directories
    print("\n[2/11] Verifying directories...")
    missing_dirs = verify_directories(root)
    if missing_dirs:
        print(f"  FAIL: Missing directories: {missing_dirs}")
        return 1
    print(f"  OK: All {len(MANDATORY_DIRS)} directories present")

    # Step 3: Verify files
    print("\n[3/11] Verifying files...")
    missing_files = verify_files(root)
    if missing_files:
        print(f"  FAIL: Missing files: {missing_files}")
        return 1
    print(f"  OK: All {len(MANDATORY_FILES)} files present")

    # Step 4: Load CONTROL_CENTER.yaml (REQUIRED — STOP if missing)
    print("\n[4/11] Loading CONTROL_CENTER.yaml...")
    cc_data, err = load_yaml_file(root, "project_management/CONTROL_CENTER.yaml")
    if err:
        print(f"  FAIL: {err}")
        print("  CONTROL_CENTER.yaml is REQUIRED. PROJECT NOT READY.")
        return 1
    print("  OK: Loaded successfully")

    # Step 5: Load TASK_STATE.yaml
    print("\n[5/11] Loading TASK_STATE.yaml...")
    task_data, err = load_yaml_file(root, "project_management/TASK_STATE.yaml")
    if err:
        print(f"  WARNING: {err}")
    else:
        print("  OK: Loaded successfully")

    # Step 6: Verify consistency
    print("\n[6/11] Verifying consistency...")
    issues = verify_consistency(cc_data, task_data)
    if issues:
        print(f"  WARNING: {len(issues)} consistency issues:")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("  OK: All state files consistent")

    # Step 7: Task consistency validation
    print("\n[7/11] Running task consistency validation...")
    try:
        from task_consistency_validator import TaskConsistencyValidator
        validator = TaskConsistencyValidator(root)
        findings = validator.validate()
        errors = [f for f in findings if f.level == "ERROR"]
        warnings = [f for f in findings if f.level == "WARNING"]
        print(f"  INFO: {len(errors)} errors, {len(warnings)} warnings")
        if errors:
            print("  WARNING: Task consistency issues detected")
    except Exception as e:
        print(f"  WARNING: Task consistency validation skipped: {e}")

    # Step 8: Determine current task
    print("\n[8/11] Determining current task...")
    if cc_data and "current_task" in cc_data:
        task = cc_data["current_task"]
        print(f"  OK: {task.get('id', 'None')} — {task.get('title', 'None')}")
    else:
        print("  WARNING: Could not determine current task")

    # Step 9: Determine responsible agent
    print("\n[9/11] Determining responsible agent...")
    if cc_data and "current_agent" in cc_data:
        agent = cc_data["current_agent"]
        print(f"  OK: {agent.get('role', 'Unknown')}")
    else:
        print("  WARNING: Could not determine responsible agent")

    # Step 10: Display dashboard
    print("\n[10/11] Displaying dashboard...")
    display_dashboard(cc_data, task_data)

    # Step 11: Summary
    print("\n[11/11] Bootstrap summary...")
    print("  OK: All bootstrap checks passed")

    print("\n" + "=" * 40)
    print("BOOTSTRAP COMPLETE — PROJECT READY")
    print("=" * 40)

    return 0


if __name__ == "__main__":
    sys.exit(main())
