#!/usr/bin/env python3
"""
task_dispatcher.py — Task Dispatcher

Reads TASK_STATE.yaml and determines current task, responsible agent,
dependencies, prerequisites, and completion status.
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


def analyze_task(task_data):
    """Analyze current task and dependencies."""
    if not task_data or "tasks" not in task_data:
        return None

    tasks = task_data["tasks"]
    current = tasks.get("current_task", {})
    pending = tasks.get("pending_tasks", [])
    completed = tasks.get("completed_tasks", [])
    blocked = tasks.get("blocked_tasks", [])

    # Find next task with satisfied dependencies
    completed_ids = {t["id"] for t in completed}
    next_task = None

    for task in pending:
        deps = task.get("depends_on", [])
        if all(d in completed_ids for d in deps):
            next_task = task
            break

    return {
        "current_task": current,
        "next_task": next_task,
        "pending_tasks": pending,
        "completed_tasks": completed,
        "blocked_tasks": blocked,
        "completed_count": len(completed),
        "pending_count": len(pending),
        "blocked_count": len(blocked),
    }


def determine_agent(task):
    """Determine which agent should handle a task."""
    if not task:
        return "None"

    title = task.get("title", "").lower()
    assigned = task.get("assigned_agent", "")

    if assigned:
        return assigned

    if "test" in title or "validate" in title:
        return "Validator"
    elif "document" in title or "review" in title:
        return "Auditor"
    elif "implement" in title or "code" in title or "fix" in title:
        return "Programmer"
    elif "plan" in title or "assign" in title:
        return "Coordinator"

    return "Programmer"


def check_dependencies(task, completed_ids):
    """Check if task dependencies are satisfied."""
    deps = task.get("depends_on", [])
    if not deps:
        return True, []

    unsatisfied = [d for d in deps if d not in completed_ids]
    return len(unsatisfied) == 0, unsatisfied


def display_dispatch(analysis):
    """Display task dispatch information."""
    if not analysis:
        print("No task data available")
        return

    print("\n" + "=" * 60)
    print("  TASK DISPATCHER")
    print("=" * 60)

    # Current task
    current = analysis["current_task"]
    print("\n  CURRENT TASK")
    print("  " + "-" * 40)
    if current and current.get("id"):
        print(f"  ID: {current.get('id', 'None')}")
        print(f"  Title: {current.get('title', 'None')}")
        print(f"  Agent: {current.get('assigned_agent', 'None')}")
        print(f"  Status: {current.get('status', 'None')}")
    else:
        print("  No current task")

    # Next task
    next_task = analysis["next_task"]
    print("\n  NEXT TASK (Ready to Execute)")
    print("  " + "-" * 40)
    if next_task:
        print(f"  ID: {next_task.get('id', 'None')}")
        print(f"  Title: {next_task.get('title', 'None')}")
        print(f"  Priority: {next_task.get('priority', 'None')}")
        agent = determine_agent(next_task)
        print(f"  Assigned Agent: {agent}")
        deps = next_task.get("depends_on", [])
        if deps:
            print(f"  Dependencies: {', '.join(deps)}")
        else:
            print(f"  Dependencies: None")
    else:
        print("  No task ready to execute")

    # Summary
    print("\n  SUMMARY")
    print("  " + "-" * 40)
    print(f"  Completed: {analysis['completed_count']} tasks")
    print(f"  Pending: {analysis['pending_count']} tasks")
    print(f"  Blocked: {analysis['blocked_count']} tasks")

    # Progress
    total = analysis["completed_count"] + analysis["pending_count"]
    if total > 0:
        pct = (analysis["completed_count"] / total) * 100
        print(f"  Progress: {pct:.1f}%")

    print("\n" + "=" * 60)


def main():
    """Run task dispatcher."""
    print("Q-Scout Task Dispatcher")
    print("=" * 40)

    root = find_project_root()
    if root is None:
        print("FAIL: Could not locate project root")
        return 1

    task_data, err = load_yaml(root, "project_management/TASK_STATE.yaml")
    if err:
        print(f"ERROR: {err}")
        return 1

    analysis = analyze_task(task_data)
    display_dispatch(analysis)

    return 0


if __name__ == "__main__":
    sys.exit(main())
