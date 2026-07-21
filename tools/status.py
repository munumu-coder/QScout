#!/usr/bin/env python3
"""
status.py — Concise Status Summary

Prints a concise summary of the project status from CONTROL_CENTER.yaml.
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


def main():
    """Display concise status summary."""
    root = find_project_root()
    if root is None:
        print("FAIL: Could not locate project root")
        return 1

    cc_data, err = load_yaml(root, "project_management/CONTROL_CENTER.yaml")
    if err:
        print(f"FAIL: {err}")
        return 1

    print("")
    print("-" * 50)
    print("  Q-Scout SDK")
    print("-" * 50)

    # Repository
    repo = cc_data.get("repository", {})
    print(f"  Repository:       {repo.get('canonical', 'Unknown')}")

    # SDK Phase
    phase = cc_data.get("current_phase", {})
    print(f"  SDK Phase:        {phase.get('id', 'Unknown')}")

    # Current Task
    task = cc_data.get("current_task", {})
    print(f"  Current Task:     {task.get('title', 'Unknown')}")

    # Current Agent
    agent = cc_data.get("current_agent", {})
    print(f"  Current Agent:    {agent.get('role', 'Unknown')}")

    # Next Agent
    next_agent = cc_data.get("next_agent", {})
    print(f"  Next Agent:       {next_agent.get('role', 'Unknown')}")

    # Tests
    tests = cc_data.get("tests", {})
    total = tests.get("total", 0)
    passing = tests.get("passing", 0)
    failing = tests.get("failing", 0)
    if failing == 0:
        print(f"  Tests:            {total} PASS")
    else:
        print(f"  Tests:            {passing} PASS, {failing} FAIL")

    # Repository Health
    health = cc_data.get("repository_health", {})
    print(f"  Repository:       {health.get('status', 'Unknown').capitalize()}")

    # Documentation
    doc = cc_data.get("documentation", {})
    print(f"  Documentation:    {doc.get('status', 'Unknown').capitalize()}")

    # Blockers
    blockers = cc_data.get("blockers", [])
    if blockers:
        print(f"  Blockers:         {len(blockers)}")
        for b in blockers:
            if isinstance(b, dict):
                print(f"    - {b.get('description', b)}")
            else:
                print(f"    - {b}")
    else:
        print(f"  Blockers:         None")

    # Next Action
    actions = cc_data.get("next_actions", [])
    if actions:
        first = actions[0]
        if isinstance(first, dict):
            print(f"  Next Action:      {first.get('action', 'Unknown')}")

    # Release
    release = cc_data.get("release", {})
    print(f"  Release Ready:    {release.get('ready', 'Unknown')}")

    print("-" * 50)
    print("")

    return 0


if __name__ == "__main__":
    sys.exit(main())
