#!/usr/bin/env python3
"""
agent_selector.py — Agent Selector

Selects the appropriate agent role based on task type.
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


# Agent selection rules
AGENT_RULES = {
    "programming": {
        "keywords": ["implement", "code", "fix", "bug", "feature", "modify", "write", "create", "add"],
        "role": "Programmer",
        "description": "Code implementation task",
    },
    "validation": {
        "keywords": ["validate", "verify", "test", "check", "run tests"],
        "role": "Validator",
        "description": "Validation task",
    },
    "documentation": {
        "keywords": ["document", "review", "audit", "checklist", "readme", "changelog"],
        "role": "Auditor",
        "description": "Documentation task",
    },
    "planning": {
        "keywords": ["plan", "assign", "coordinate", "schedule", "prioritize"],
        "role": "Coordinator",
        "description": "Planning task",
    },
}


def select_agent(task):
    """Select the appropriate agent for a task."""
    if not task:
        return "Coordinator", "No task specified"

    title = task.get("title", "").lower()
    assigned = task.get("assigned_agent", "")

    # If agent is already assigned, use that
    if assigned and assigned in ["Programmer", "Validator", "Auditor", "Coordinator"]:
        return assigned, f"Pre-assigned: {assigned}"

    # Match against rules
    for category, rules in AGENT_RULES.items():
        for keyword in rules["keywords"]:
            if keyword in title:
                return rules["role"], rules["description"]

    # Default to Programmer
    return "Programmer", "Default assignment"


def display_selection(task_data):
    """Display agent selection results."""
    if not task_data or "tasks" not in task_data:
        print("No task data available")
        return

    tasks = task_data["tasks"]
    current = tasks.get("current_task", {})
    pending = tasks.get("pending_tasks", [])

    print("\n" + "=" * 60)
    print("  AGENT SELECTOR")
    print("=" * 60)

    # Current task
    print("\n  CURRENT TASK")
    print("  " + "-" * 40)
    if current and current.get("id"):
        role, reason = select_agent(current)
        print(f"  Task: {current.get('id', 'None')} — {current.get('title', 'None')}")
        print(f"  Selected Agent: {role}")
        print(f"  Reason: {reason}")
    else:
        print("  No current task")

    # Next tasks
    print("\n  PENDING TASKS")
    print("  " + "-" * 40)
    for task in pending[:5]:  # Show first 5
        role, reason = select_agent(task)
        print(f"  {task.get('id', 'None')}: {role} — {task.get('title', 'None')}")

    if len(pending) > 5:
        print(f"  ... and {len(pending) - 5} more tasks")

    # Agent summary
    print("\n  AGENT SUMMARY")
    print("  " + "-" * 40)
    agent_counts = {}
    for task in pending:
        role, _ = select_agent(task)
        agent_counts[role] = agent_counts.get(role, 0) + 1

    for role, count in sorted(agent_counts.items()):
        print(f"  {role}: {count} tasks")

    print("\n" + "=" * 60)


def main():
    """Run agent selector."""
    print("Q-Scout Agent Selector")
    print("=" * 40)

    root = find_project_root()
    if root is None:
        print("FAIL: Could not locate project root")
        return 1

    task_data, err = load_yaml(root, "project_management/TASK_STATE.yaml")
    if err:
        print(f"ERROR: {err}")
        return 1

    display_selection(task_data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
