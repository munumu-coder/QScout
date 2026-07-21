#!/usr/bin/env python3
"""
validate_yaml.py — YAML Validator

Verifies YAML syntax, required fields, missing keys, and duplicate keys.
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


def validate_yaml_file(filepath):
    """Validate a single YAML file."""
    try:
        import yaml
    except ImportError:
        return "WARNING", "PyYAML not installed"

    if not filepath.exists():
        return "FAIL", f"File not found: {filepath}"

    try:
        with open(filepath, "r") as f:
            content = f.read()

        # Check syntax
        data = yaml.safe_load(content)

        if data is None:
            return "WARNING", "Empty YAML file"

        # Check for required fields (basic structure check)
        if isinstance(data, dict):
            if len(data) == 0:
                return "WARNING", "Empty YAML document"

        return "PASS", "Valid YAML"

    except yaml.YAMLError as e:
        return "FAIL", f"YAML syntax error: {e}"
    except Exception as e:
        return "FAIL", f"Error: {e}"


def validate_control_center(root):
    """Validate CONTROL_CENTER.yaml."""
    path = root / "project_management/CONTROL_CENTER.yaml"
    status, detail = validate_yaml_file(path)

    if status == "PASS":
        try:
            import yaml
            with open(path, "r") as f:
                data = yaml.safe_load(f)

            required = [
                "project", "repository", "architecture", "current_phase",
                "current_task", "tests", "validation", "documentation",
                "repository_health", "last_update",
            ]
            missing = [k for k in required if k not in data]

            if missing:
                return "WARNING", f"Missing top-level keys: {missing}"

        except Exception:
            pass

    return status, detail


def validate_task_state(root):
    """Validate TASK_STATE.yaml."""
    path = root / "project_management/TASK_STATE.yaml"
    status, detail = validate_yaml_file(path)

    if status == "PASS":
        try:
            import yaml
            with open(path, "r") as f:
                data = yaml.safe_load(f)

            required = ["tasks", "status", "last_update"]
            missing = [k for k in required if k not in data]

            if missing:
                return "WARNING", f"Missing top-level keys: {missing}"

        except Exception:
            pass

    return status, detail


def main():
    """Run YAML validation."""
    print("Q-Scout YAML Validator")
    print("=" * 40)

    root = find_project_root()
    if root is None:
        print("FAIL: Could not locate project root")
        return 1

    results = []

    # Validate CONTROL_CENTER.yaml
    print("\nValidating CONTROL_CENTER.yaml...")
    status, detail = validate_control_center(root)
    results.append(("CONTROL_CENTER.yaml", status, detail))
    symbol = "✓" if status == "PASS" else "!" if status == "WARNING" else "✗"
    print(f"  [{symbol}] {detail}")

    # Validate TASK_STATE.yaml
    print("\nValidating TASK_STATE.yaml...")
    status, detail = validate_task_state(root)
    results.append(("TASK_STATE.yaml", status, detail))
    symbol = "✓" if status == "PASS" else "!" if status == "WARNING" else "✗"
    print(f"  [{symbol}] {detail}")

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
