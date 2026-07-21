#!/usr/bin/env python3
"""
health_check.py — Project Health Check

Verifies repository structure, required files, Python version,
YAML validity, Markdown presence, and project consistency.
"""

import os
import sys
from pathlib import Path

# Health check items
REQUIRED_DIRS = [
    "src/qscout",
    "tests",
    "docs",
    "project_management",
]

REQUIRED_FILES = [
    "README.md",
    "pyproject.toml",
    "project_management/START_HERE.md",
    "project_management/CONTROL_CENTER.yaml",
    "project_management/TASK_STATE.yaml",
    "project_management/PROJECT_RULES.md",
    "project_management/AGENT_WORKFLOW.md",
]

REQUIRED_PYTHON = (3, 10)


def find_project_root():
    """Locate project root."""
    current = Path(__file__).resolve().parent.parent
    while current != current.parent:
        if (current / "README.md").exists() and (current / "pyproject.toml").exists():
            if (current / "src" / "qscout").is_dir():
                return current
        current = current.parent
    return None


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version >= REQUIRED_PYTHON:
        return "PASS", f"Python {version.major}.{version.minor}.{version.micro}"
    return "FAIL", f"Python {version.major}.{version.minor} (requires >= {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]})"


def check_directories(root):
    """Check required directories."""
    missing = []
    for d in REQUIRED_DIRS:
        if not (root / d).is_dir():
            missing.append(d)
    if missing:
        return "FAIL", f"Missing: {', '.join(missing)}"
    return "PASS", f"All {len(REQUIRED_DIRS)} directories present"


def check_files(root):
    """Check required files."""
    missing = []
    for f in REQUIRED_FILES:
        if not (root / f).exists():
            missing.append(f)
    if missing:
        return "FAIL", f"Missing: {', '.join(missing)}"
    return "PASS", f"All {len(REQUIRED_FILES)} files present"


def check_yaml_files(root):
    """Check YAML file validity."""
    try:
        import yaml
    except ImportError:
        return "WARNING", "PyYAML not installed — cannot validate YAML"

    yaml_files = [
        "project_management/CONTROL_CENTER.yaml",
        "project_management/TASK_STATE.yaml",
    ]

    errors = []
    for f in yaml_files:
        path = root / f
        if not path.exists():
            errors.append(f"{f}: not found")
            continue
        try:
            with open(path, "r") as fh:
                yaml.safe_load(fh)
        except Exception as e:
            errors.append(f"{f}: {e}")

    if errors:
        return "FAIL", "; ".join(errors)
    return "PASS", f"All {len(yaml_files)} YAML files valid"


def check_markdown_files(root):
    """Check Markdown file presence."""
    pm_dir = root / "project_management"
    if not pm_dir.exists():
        return "FAIL", "project_management/ directory not found"

    md_files = list(pm_dir.glob("*.md"))
    if len(md_files) < 10:
        return "WARNING", f"Only {len(md_files)} Markdown files found"
    return "PASS", f"{len(md_files)} Markdown files found"


def check_sdk_files(root):
    """Check SDK source files exist but are not modified."""
    src_dir = root / "src" / "qscout"
    if not src_dir.exists():
        return "FAIL", "src/qscout/ directory not found"

    expected_files = [
        "__init__.py",
        "connection.py",
        "protocol.py",
        "packet.py",
        "commands.py",
        "command_map.py",
        "actuators.py",
        "sensors.py",
        "exceptions.py",
    ]

    missing = []
    for f in expected_files:
        if not (src_dir / f).exists():
            missing.append(f)

    if missing:
        return "FAIL", f"Missing SDK files: {', '.join(missing)}"
    return "PASS", f"All {len(expected_files)} SDK files present"


def check_tests(root):
    """Check test files exist."""
    tests_dir = root / "tests"
    if not tests_dir.exists():
        return "FAIL", "tests/ directory not found"

    test_files = list(tests_dir.glob("test_*.py"))
    if len(test_files) < 3:
        return "WARNING", f"Only {len(test_files)} test files found"
    return "PASS", f"{len(test_files)} test files found"


def main():
    """Run all health checks."""
    print("Q-Scout Project Health Check")
    print("=" * 40)

    results = []

    # Find project root
    root = find_project_root()
    if root is None:
        print("FAIL: Could not locate project root")
        return 1

    print(f"Project Root: {root}\n")

    # Run checks
    checks = [
        ("Python Version", check_python_version),
        ("Directories", lambda r: check_directories(r)),
        ("Required Files", lambda r: check_files(r)),
        ("YAML Files", lambda r: check_yaml_files(r)),
        ("Markdown Files", lambda r: check_markdown_files(r)),
        ("SDK Files", lambda r: check_sdk_files(r)),
        ("Test Files", lambda r: check_tests(root)),
    ]

    for name, check_fn in checks:
        if name == "Python Version":
            status, detail = check_fn()
        else:
            status, detail = check_fn(root)
        results.append((name, status, detail))
        symbol = "✓" if status == "PASS" else "!" if status == "WARNING" else "✗"
        print(f"  [{symbol}] {name}: {detail}")

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
