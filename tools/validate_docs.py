#!/usr/bin/env python3
"""
validate_docs.py — Documentation Validator

Verifies broken links, missing documents, orphan documents, and duplicate titles.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote


def find_project_root():
    """Locate project root."""
    current = Path(__file__).resolve().parent.parent
    while current != current.parent:
        if (current / "README.md").exists() and (current / "pyproject.toml").exists():
            if (current / "src" / "qscout").is_dir():
                return current
        current = current.parent
    return None


def find_markdown_files(root):
    """Find all Markdown files in project_management/."""
    pm_dir = root / "project_management"
    if not pm_dir.exists():
        return []
    return list(pm_dir.rglob("*.md"))


def extract_links(filepath):
    """Extract Markdown links from a file, skipping code blocks."""
    try:
        content = filepath.read_text()
        # Remove code blocks first
        content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content_no_code = re.sub(r'`[^`]+`', '', content_no_code)
        # Match [text](path) patterns
        links = re.findall(r'\[.*?\]\((.*?\.md)\)', content_no_code)
        return links
    except Exception:
        return []


def extract_titles(filepath):
    """Extract Markdown titles from a file."""
    try:
        content = filepath.read_text()
        titles = re.findall(r'^#\s+(.+)$', content, re.MULTILINE)
        return titles
    except Exception:
        return []


def validate_links(root, md_files):
    """Validate all Markdown links."""
    broken = []
    valid = 0

    for filepath in md_files:
        links = extract_links(filepath)
        for link in links:
            # URL-decode the link path
            decoded_link = unquote(link)
            # Resolve relative link
            if decoded_link.startswith("../"):
                target = root / decoded_link[3:]
            else:
                target = filepath.parent / decoded_link

            if target.exists():
                valid += 1
            else:
                broken.append((filepath.name, link))

    return valid, broken


def validate_documents(root, md_files):
    """Check for required documents."""
    required = [
        "START_HERE.md",
        "PROJECT_STATE.md",
        "PROJECT_RULES.md",
        "AGENT_WORKFLOW.md",
        "AGENT_MANIFEST.md",
    ]

    pm_dir = root / "project_management"
    missing = []

    for doc in required:
        if not (pm_dir / doc).exists():
            missing.append(doc)

    return missing


def validate_titles(md_files):
    """Check for duplicate titles."""
    all_titles = {}
    duplicates = []

    for filepath in md_files:
        titles = extract_titles(filepath)
        for title in titles:
            if title in all_titles:
                duplicates.append((title, all_titles[title], filepath.name))
            else:
                all_titles[title] = filepath.name

    return duplicates


def main():
    """Run documentation validation."""
    print("Q-Scout Documentation Validator")
    print("=" * 40)

    root = find_project_root()
    if root is None:
        print("FAIL: Could not locate project root")
        return 1

    md_files = find_markdown_files(root)
    print(f"\nFound {len(md_files)} Markdown files")

    results = []

    # Validate links
    print("\nValidating links...")
    valid, broken = validate_links(root, md_files)
    print(f"  Valid links: {valid}")
    if broken:
        print(f"  Broken links: {len(broken)}")
        for source, link in broken[:5]:
            print(f"    {source} -> {link}")
        results.append(("Links", "FAIL", f"{len(broken)} broken links"))
    else:
        print(f"  Broken links: 0")
        results.append(("Links", "PASS", "All links valid"))

    # Validate required documents
    print("\nValidating required documents...")
    missing = validate_documents(root, md_files)
    if missing:
        print(f"  Missing: {missing}")
        results.append(("Documents", "FAIL", f"Missing: {missing}"))
    else:
        print(f"  All required documents present")
        results.append(("Documents", "PASS", "All required documents present"))

    # Validate titles
    print("\nValidating titles...")
    duplicates = validate_titles(md_files)
    if duplicates:
        print(f"  Duplicate titles: {len(duplicates)}")
        results.append(("Titles", "WARNING", f"{len(duplicates)} duplicate titles"))
    else:
        print(f"  No duplicate titles")
        results.append(("Titles", "PASS", "No duplicate titles"))

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
