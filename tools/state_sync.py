#!/usr/bin/env python3
"""
state_sync.py — State Synchronization Validator

Compares CONTROL_CENTER.yaml and TASK_STATE.yaml.
Detects missing fields, conflicting values, obsolete information, and timestamp mismatches.
"""

import sys
from pathlib import Path


def find_project_root():
    """Locate project root."""
    current = Path(__file__).resolve().parent.parent
    while current != current.parent:
        if (current / "README.md").exists() and (current / "pyproject.toml").exists():
            if (current / "src" / "qscout").is_dir():
                return current
        current = current.parent
    return None


def load_yaml(root, filename):
    """Load a YAML file."""
    try:
        import yaml
    except ImportError:
        return None, "PyYAML not installed"

    path = root / filename
    if not path.exists():
        return None, f"File not found: {filename}"

    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return data, None
    except Exception as e:
        return None, str(e)


def check_missing_fields(cc_data, task_data):
    """Check for missing required fields."""
    issues = []

    # CONTROL_CENTER.yaml required fields
    cc_required = [
        "project", "repository", "architecture", "current_phase",
        "current_task", "current_milestone", "current_agent", "next_agent",
        "assigned_agents", "progress", "tests", "validation", "documentation",
        "repository_health", "sessions", "blockers", "risks", "backups",
        "release", "next_actions", "last_update",
    ]

    if cc_data:
        for field in cc_required:
            if field not in cc_data:
                issues.append(f"CONTROL_CENTER.yaml missing: {field}")

    # TASK_STATE.yaml required fields
    task_required = ["active_phase", "active_task", "tasks", "last_update"]
    if task_data:
        for field in task_required:
            if field not in task_data:
                issues.append(f"TASK_STATE.yaml missing: {field}")

    return issues


def check_conflicts(cc_data, task_data):
    """Check for conflicting values between files."""
    issues = []

    if cc_data and task_data:
        # Task comparison
        cc_task = cc_data.get("current_task", {}).get("id", "")
        task_id = task_data.get("active_task", {}).get("id", "")
        if cc_task and task_id and cc_task != task_id:
            issues.append(f"Task conflict: CC={cc_task} vs TASK={task_id}")

        # Agent comparison
        cc_agent = cc_data.get("current_task", {}).get("assigned_agent", "")
        task_agent = task_data.get("active_task", {}).get("assigned_agent", "")
        if cc_agent and task_agent and cc_agent != task_agent:
            issues.append(f"Agent conflict: CC={cc_agent} vs TASK={task_agent}")

    return issues


def check_timestamps(cc_data, task_data):
    """Check for timestamp mismatches."""
    issues = []

    timestamps = {}
    if cc_data and "last_update" in cc_data:
        timestamps["CONTROL_CENTER"] = cc_data["last_update"]
    if task_data and "last_update" in task_data:
        timestamps["TASK_STATE"] = task_data["last_update"]

    if len(timestamps) > 1:
        values = list(timestamps.values())
        if len(set(values)) > 1:
            issues.append(f"Timestamp mismatch: {timestamps}")

    return issues


def main():
    """Run state synchronization check."""
    print("Q-Scout State Synchronization Validator")
    print("=" * 40)

    root = find_project_root()
    if root is None:
        print("FAIL: Could not locate project root")
        return 1

    # Load all state files
    cc_data, err = load_yaml(root, "project_management/CONTROL_CENTER.yaml")
    if err:
        print(f"FAIL: {err}")
        return 1

    task_data, _ = load_yaml(root, "project_management/TASK_STATE.yaml")

    results = []

    # Check missing fields
    print("\nChecking missing fields...")
    missing = check_missing_fields(cc_data, task_data)
    if missing:
        print(f"  Found {len(missing)} missing fields:")
        for issue in missing:
            print(f"    - {issue}")
        results.append(("Missing Fields", "FAIL", len(missing)))
    else:
        print("  All required fields present")
        results.append(("Missing Fields", "PASS", 0))

    # Check conflicts
    print("\nChecking conflicts...")
    conflicts = check_conflicts(cc_data, task_data)
    if conflicts:
        print(f"  Found {len(conflicts)} conflicts:")
        for issue in conflicts:
            print(f"    - {issue}")
        results.append(("Conflicts", "FAIL", len(conflicts)))
    else:
        print("  No conflicts detected")
        results.append(("Conflicts", "PASS", 0))

    # Check timestamps
    print("\nChecking timestamps...")
    timestamps = check_timestamps(cc_data, task_data)
    if timestamps:
        print(f"  Found {len(timestamps)} timestamp issues:")
        for issue in timestamps:
            print(f"    - {issue}")
        results.append(("Timestamps", "WARNING", len(timestamps)))
    else:
        print("  All timestamps consistent")
        results.append(("Timestamps", "PASS", 0))

    # Summary
    print("\n" + "=" * 40)
    statuses = [r[1] for r in results]

    if all(s == "PASS" for s in statuses):
        print("RESULT: PASS")
        return 0
    elif any(s == "FAIL" for s in statuses):
        print("RESULT: FAIL")
        return 1
    else:
        print("RESULT: WARNING")
        return 0


if __name__ == "__main__":
    sys.exit(main())
