#!/usr/bin/env python3
"""
session_manager.py — Session Manager

Manages AI agent sessions: open, close, resume, and maintain history.
"""

import os
import sys
from datetime import datetime
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


def save_yaml(root, filename, data):
    """Save a YAML file."""
    try:
        import yaml
    except ImportError:
        return "PyYAML not installed"

    path = root / filename
    try:
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        return None
    except Exception as e:
        return str(e)


def open_session(root):
    """Open a new session."""
    now = datetime.now()
    session_id = f"SESSION-{now.strftime('%Y-%m-%d-%H%M')}"

    session_data = {
        "session_id": session_id,
        "started": now.isoformat(),
        "agent": "TBD",
        "role": "TBD",
        "status": "active",
    }

    # Save current session
    err = save_yaml(root, "project_management/sessions/current_session.yaml", session_data)
    if err:
        return None, err

    # Update CURRENT_SESSION.md
    md_path = root / "project_management/sessions/CURRENT_SESSION.md"
    md_content = f"""# CURRENT_SESSION.md — Active Session State

**Last Updated:** {now.strftime('%Y-%m-%d')}

---

## Session Information

| Field | Value |
|-------|-------|
| Session ID | {session_id} |
| Started | {now.strftime('%Y-%m-%d %H:%M')} |
| Agent | TBD |
| Role | TBD |

---

## Current Task

| Field | Value |
|-------|-------|
| Task ID | TBD |
| Title | TBD |
| Status | Pending |
| Assigned To | TBD |

---

## Progress

- [ ] Session opened
- [ ] Task assigned
- [ ] Work started
- [ ] Work completed
- [ ] Session closed

---

## Notes

[Add session notes here]
"""

    with open(md_path, "w") as f:
        f.write(md_content)

    return session_id, None


def close_session(root):
    """Close the current session."""
    now = datetime.now()

    # Update CURRENT_SESSION.md
    md_path = root / "project_management/sessions/CURRENT_SESSION.md"
    if md_path.exists():
        content = md_path.read_text()
        content = content.replace("- [ ] Session closed", "- [x] Session closed")
        content += f"\n\n---\n\n**Session Closed:** {now.strftime('%Y-%m-%d %H:%M')}\n"
        with open(md_path, "w") as f:
            f.write(content)

    # Append to SESSION_HISTORY.md
    history_path = root / "project_management/sessions/SESSION_HISTORY.md"
    if history_path.exists():
        content = history_path.read_text()
        new_entry = f"""
### Session Closed: {now.strftime('%Y-%m-%d %H:%M')}

| Field | Value |
|-------|-------|
| Date | {now.strftime('%Y-%m-%d')} |
| Time | {now.strftime('%H:%M')} |
| Status | Closed |

"""
        # Insert after the first "---" following the title
        lines = content.split("\n")
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.strip() == "---" and i > 2:
                insert_idx = i + 1
                break

        lines.insert(insert_idx, new_entry)
        with open(history_path, "w") as f:
            f.write("\n".join(lines))

    return None


def resume_session(root):
    """Resume a previous session."""
    # Check for current session
    session_path = root / "project_management/sessions/current_session.yaml"
    if session_path.exists():
        data, err = load_yaml(root, "project_management/sessions/current_session.yaml")
        if data:
            return data.get("session_id", "Unknown"), None

    return None, "No active session found"


def main():
    """Run session manager."""
    print("Q-Scout Session Manager")
    print("=" * 40)

    root = find_project_root()
    if root is None:
        print("FAIL: Could not locate project root")
        return 1

    if len(sys.argv) < 2:
        print("Usage: session_manager.py [open|close|resume|status]")
        return 1

    action = sys.argv[1].lower()

    if action == "open":
        session_id, err = open_session(root)
        if err:
            print(f"ERROR: {err}")
            return 1
        print(f"Session opened: {session_id}")

    elif action == "close":
        err = close_session(root)
        if err:
            print(f"ERROR: {err}")
            return 1
        print("Session closed")

    elif action == "resume":
        session_id, err = resume_session(root)
        if err:
            print(f"ERROR: {err}")
            return 1
        print(f"Resuming session: {session_id}")

    elif action == "status":
        session_id, err = resume_session(root)
        if err:
            print("No active session")
        else:
            print(f"Active session: {session_id}")

    else:
        print(f"Unknown action: {action}")
        print("Usage: session_manager.py [open|close|resume|status]")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
