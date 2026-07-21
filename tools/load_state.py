#!/usr/bin/env python3
"""
load_state.py — State Loader

Loads and parses project state files for AI agents.
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


def load_control_center(root):
    """Load CONTROL_CENTER.yaml."""
    return load_yaml(root, "project_management/CONTROL_CENTER.yaml")


def load_task_state(root):
    """Load TASK_STATE.yaml."""
    return load_yaml(root, "project_management/TASK_STATE.yaml")


def get_current_phase(cc_data):
    """Extract current phase from control center data."""
    if cc_data and "current_phase" in cc_data:
        phase = cc_data["current_phase"]
        return {
            "phase": phase.get("id", "Unknown"),
            "phase_name": phase.get("name", ""),
            "previous_phase": phase.get("previous", ""),
            "next_phase": phase.get("next", ""),
        }
    return None


def get_current_task(task_data):
    """Extract current task from task data."""
    if task_data and "tasks" in task_data:
        tasks = task_data["tasks"]
        return {
            "current_task": tasks.get("current_task", {}),
            "next_task": tasks.get("next_task", {}),
            "pending_count": len(tasks.get("pending_tasks", [])),
            "completed_count": len(tasks.get("completed_tasks", [])),
            "blocked_count": len(tasks.get("blocked_tasks", [])),
        }
    return None


def get_test_status(cc_data):
    """Extract test status from control center data."""
    if cc_data and "tests" in cc_data:
        tests = cc_data["tests"]
        return {
            "total": tests.get("total", 0),
            "passing": tests.get("passing", 0),
            "failing": tests.get("failing", 0),
            "last_run": tests.get("last_run", "Unknown"),
        }
    return None


def get_agent_status(cc_data):
    """Extract agent status from control center data."""
    if cc_data and "assigned_agents" in cc_data:
        return cc_data["assigned_agents"]
    return None


def main():
    """Load and display project state."""
    print("Q-Scout State Loader")
    print("=" * 40)

    root = find_project_root()
    if root is None:
        print("FAIL: Could not locate project root")
        return 1

    # Load control center
    cc_data, err = load_control_center(root)
    if err:
        print(f"WARNING: {err}")

    # Load task state
    task_data, err = load_task_state(root)
    if err:
        print(f"WARNING: {err}")

    # Display phase
    phase = get_current_phase(cc_data)
    if phase:
        print(f"\nCurrent Phase: {phase['phase']} — {phase['phase_name']}")
        print(f"Next Phase: {phase['next_phase']}")

    # Display task
    task = get_current_task(task_data)
    if task:
        ct = task["current_task"]
        print(f"\nCurrent Task: {ct.get('id', 'None')} — {ct.get('title', 'None')}")
        print(f"Assigned To: {ct.get('assigned_agent', 'None')}")
        print(f"Pending Tasks: {task['pending_count']}")
        print(f"Completed Tasks: {task['completed_count']}")

    # Display tests
    tests = get_test_status(cc_data)
    if tests:
        print(f"\nTests: {tests['passing']}/{tests['total']} passing")
        print(f"Last Run: {tests['last_run']}")

    # Display agents
    agents = get_agent_status(cc_data)
    if agents:
        print("\nAgents:")
        for name, info in agents.items():
            print(f"  {name}: {info.get('status', 'unknown')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
