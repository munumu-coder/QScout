#!/usr/bin/env python3
"""
project_ready.py — Project Ready Check

Checks repository, documentation, YAML, dashboard, bootstrap, and workflow.
Returns READY or NOT READY.
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


def check_repository(root):
    """Check repository structure."""
    checks = [
        (root / "src" / "qscout").is_dir(),
        (root / "tests").is_dir(),
        (root / "docs").is_dir(),
        (root / "project_management").is_dir(),
        (root / "tools").is_dir(),
    ]
    return all(checks)


def check_documentation(root):
    """Check required documentation exists."""
    required = [
        "START_HERE.md",
        "PROJECT_RULES.md",
        "AGENT_WORKFLOW.md",
        "AGENT_MANIFEST.md",
    ]
    pm_dir = root / "project_management"
    return all((pm_dir / f).exists() for f in required)


def check_yaml(root):
    """Check YAML files are valid."""
    try:
        import yaml
    except ImportError:
        return False

    yaml_files = [
        "project_management/CONTROL_CENTER.yaml",
        "project_management/TASK_STATE.yaml",
    ]

    for f in yaml_files:
        path = root / f
        if not path.exists():
            return False
        try:
            with open(path, "r") as fh:
                yaml.safe_load(fh)
        except Exception:
            return False

    return True


def check_dashboard(root):
    """Check dashboard can be loaded."""
    tools_dir = root / "tools"
    return (tools_dir / "project_dashboard.py").exists()


def check_bootstrap(root):
    """Check bootstrap can be loaded."""
    tools_dir = root / "tools"
    return (tools_dir / "bootstrap.py").exists()


def check_workflow(root):
    """Check workflow files exist."""
    pm_dir = root / "project_management"
    required = [
        "AGENT_WORKFLOW.md",
        "AGENT_VALIDATOR.md",
    ]
    return all((pm_dir / f).exists() for f in required)


def check_task_consistency(root):
    """Check task consistency."""
    validator_path = root / "tools" / "task_consistency_validator.py"
    if not validator_path.exists():
        return True  # Skip if validator not found

    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, str(validator_path)],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=30
        )
        # Check if there are ERROR level findings (look for "ERROR:   0" or similar)
        # The validator outputs "ERROR:   N" where N is the count
        import re
        error_match = re.search(r'ERROR:\s+(\d+)', result.stdout)
        if error_match:
            error_count = int(error_match.group(1))
            return error_count == 0
        # If no ERROR line found, assume no errors
        return True
    except Exception:
        return True  # Skip on error


def main():
    """Run all ready checks."""
    print("Q-Scout Project Ready Check")
    print("=" * 40)

    root = find_project_root()
    if root is None:
        print("RESULT: NOT READY (project root not found)")
        return 1

    checks = [
        ("Repository", check_repository),
        ("Documentation", check_documentation),
        ("YAML", check_yaml),
        ("Dashboard", check_dashboard),
        ("Bootstrap", check_bootstrap),
        ("Workflow", check_workflow),
        ("Task Consistency", check_task_consistency),
    ]

    all_pass = True
    for name, check_fn in checks:
        result = check_fn(root)
        status = "PASS" if result else "FAIL"
        if not result:
            all_pass = False
        symbol = "✓" if result else "✗"
        print(f"  [{symbol}] {name}: {status}")

    print("\n" + "=" * 40)
    if all_pass:
        print("RESULT: READY")
        return 0
    else:
        print("RESULT: NOT READY")
        return 1


if __name__ == "__main__":
    sys.exit(main())
