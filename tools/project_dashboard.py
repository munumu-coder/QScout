#!/usr/bin/env python3
"""
project_dashboard.py — Project Dashboard

Displays comprehensive project status from CONTROL_CENTER.yaml.
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


def display_dashboard(cc_data, task_data):
    """Display the project dashboard from CONTROL_CENTER.yaml."""
    print("\n" + "=" * 70)
    print("  Q-SCOUT PROJECT DASHBOARD")
    print("=" * 70)

    if not cc_data:
        print("\n  [ERROR] CONTROL_CENTER.yaml not loaded")
        print("  PROJECT NOT READY")
        return

    # Repository
    print("\n  REPOSITORY")
    print("  " + "-" * 40)
    repo = cc_data.get("repository", {})
    print(f"  Canonical: {repo.get('canonical', 'Unknown')}")
    print(f"  Branch: {repo.get('branch', 'Unknown')}")
    print(f"  Source: {repo.get('source', 'Unknown')}")

    # Architecture
    print("\n  ARCHITECTURE")
    print("  " + "-" * 40)
    arch = cc_data.get("architecture", {})
    print(f"  Status: {arch.get('status', 'Unknown')}")
    print(f"  Decision: {arch.get('decision', 'Unknown')}")
    layers = arch.get("layers", [])
    print(f"  Layers: {len(layers)}")

    # Current Phase
    print("\n  CURRENT PHASE")
    print("  " + "-" * 40)
    phase = cc_data.get("current_phase", {})
    print(f"  Phase: {phase.get('id', 'Unknown')}")
    print(f"  Name: {phase.get('name', '')}")
    print(f"  Next: {phase.get('next', 'Unknown')}")

    # Current Milestone
    print("\n  CURRENT MILESTONE")
    print("  " + "-" * 40)
    milestone = cc_data.get("current_milestone", {})
    print(f"  Milestone: {milestone.get('id', 'Unknown')}")
    print(f"  Name: {milestone.get('name', '')}")
    print(f"  Target: {milestone.get('target', 'Unknown')}")
    print(f"  Progress: {milestone.get('progress', 'Unknown')}")

    # Current Task
    print("\n  CURRENT TASK")
    print("  " + "-" * 40)
    task = cc_data.get("current_task", {})
    print(f"  ID: {task.get('id', 'None')}")
    print(f"  Title: {task.get('title', 'None')}")
    print(f"  Agent: {task.get('assigned_agent', 'None')}")
    print(f"  Status: {task.get('status', 'None')}")
    print(f"  Priority: {task.get('priority', 'Unknown')}")

    # Current Agent
    print("\n  CURRENT AGENT")
    print("  " + "-" * 40)
    agent = cc_data.get("current_agent", {})
    print(f"  Role: {agent.get('role', 'Unknown')}")
    print(f"  Status: {agent.get('status', 'Unknown')}")

    # Next Agent
    print("\n  NEXT AGENT")
    print("  " + "-" * 40)
    next_agent = cc_data.get("next_agent", {})
    print(f"  Role: {next_agent.get('role', 'Unknown')}")
    print(f"  Reason: {next_agent.get('reason', 'Unknown')}")

    # Assigned Agents
    print("\n  ASSIGNED AGENTS")
    print("  " + "-" * 40)
    agents = cc_data.get("assigned_agents", {})
    for name, info in agents.items():
        tasks = info.get("tasks_assigned", 0)
        print(f"  {name.capitalize()}: {info.get('status', 'unknown')} ({tasks} tasks)")

    # Tests
    print("\n  TESTS")
    print("  " + "-" * 40)
    tests = cc_data.get("tests", {})
    total = tests.get("total", 0)
    passing = tests.get("passing", 0)
    failing = tests.get("failing", 0)
    print(f"  Total: {total}")
    print(f"  Passing: {passing}")
    print(f"  Failing: {failing}")
    print(f"  Last Run: {tests.get('last_run', 'Unknown')}")
    if total > 0:
        pct = (passing / total) * 100
        print(f"  Pass Rate: {pct:.1f}%")

    # Validation
    print("\n  VALIDATION")
    print("  " + "-" * 40)
    validation = cc_data.get("validation", {})
    pv = validation.get("physical_validation", {})
    print(f"  Physical Validation: {pv.get('status', 'Unknown')}")
    print(f"  YAML Validation: {validation.get('yaml_validation', 'Unknown')}")
    print(f"  Docs Validation: {validation.get('docs_validation', 'Unknown')}")
    print(f"  Bootstrap Validation: {validation.get('bootstrap_validation', 'Unknown')}")

    # Documentation
    print("\n  DOCUMENTATION")
    print("  " + "-" * 40)
    doc = cc_data.get("documentation", {})
    print(f"  Version: {doc.get('version', 'Unknown')}")
    print(f"  Last Update: {doc.get('last_update', 'Unknown')}")
    print(f"  Total Files: {doc.get('total_files', 0)}")
    print(f"  Status: {doc.get('status', 'Unknown')}")

    # Repository Health
    print("\n  REPOSITORY HEALTH")
    print("  " + "-" * 40)
    health = cc_data.get("repository_health", {})
    print(f"  Status: {health.get('status', 'Unknown')}")
    print(f"  Python: {health.get('python_version', 'Unknown')}")
    print(f"  SDK Files Intact: {health.get('sdk_files_intact', 'Unknown')}")

    # Progress
    print("\n  OVERALL PROGRESS")
    print("  " + "-" * 40)
    progress = cc_data.get("progress", {})
    completed = progress.get("completed_tasks", 0)
    pending = progress.get("pending_tasks", 0)
    total_tasks = progress.get("total_tasks", 0)
    pct = progress.get("percent_complete", 0)
    if total_tasks > 0:
        bar_len = 30
        filled = int(bar_len * pct / 100)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"  [{bar}] {pct:.1f}%")
        print(f"  Completed: {completed} tasks")
        print(f"  Pending: {pending} tasks")
        print(f"  Blocked: {progress.get('blocked_tasks', 0)} tasks")

    # Blockers
    print("\n  BLOCKERS")
    print("  " + "-" * 40)
    blockers = cc_data.get("blockers", [])
    if blockers:
        for b in blockers:
            if isinstance(b, dict):
                print(f"  - [{b.get('severity', 'unknown')}] {b.get('description', b)}")
            else:
                print(f"  - {b}")
    else:
        print("  None")

    # Risks
    print("\n  RISKS")
    print("  " + "-" * 40)
    risks = cc_data.get("risks", [])
    if risks:
        for r in risks:
            if isinstance(r, dict):
                print(f"  - [{r.get('severity', 'unknown')}] {r.get('description', r)}")
            else:
                print(f"  - {r}")
    else:
        print("  None")

    # Next Actions
    print("\n  NEXT ACTIONS")
    print("  " + "-" * 40)
    actions = cc_data.get("next_actions", [])
    for action in actions[:3]:
        if isinstance(action, dict):
            print(f"  {action.get('order', '?')}. {action.get('action', 'Unknown')} ({action.get('agent', 'Unknown')})")

    # Release
    print("\n  RELEASE")
    print("  " + "-" * 40)
    release = cc_data.get("release", {})
    print(f"  Ready: {release.get('ready', 'Unknown')}")
    print(f"  Version: {release.get('version', 'Unknown')}")
    print(f"  Target: {release.get('target_date', 'Unknown')}")

    # Overall Readiness
    print("\n  OVERALL READINESS")
    print("  " + "-" * 40)
    readiness = "READY" if not blockers and health.get("status") == "healthy" else "NOT READY"
    print(f"  Status: {readiness}")

    print("\n" + "=" * 70)


def main():
    """Display project dashboard."""
    root = find_project_root()
    if root is None:
        print("FAIL: Could not locate project root")
        return 1

    cc_data, err = load_yaml(root, "project_management/CONTROL_CENTER.yaml")
    if err:
        print(f"FAIL: {err}")
        return 1

    task_data, _ = load_yaml(root, "project_management/TASK_STATE.yaml")

    display_dashboard(cc_data, task_data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
