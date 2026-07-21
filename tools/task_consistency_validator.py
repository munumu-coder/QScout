#!/usr/bin/env python3
"""
task_consistency_validator.py — Automatic Task Consistency Validator

Detects obsolete, inconsistent, or duplicated tasks before development begins.
Helps the Coordinator avoid assigning work that has already been completed.

Phase A.5.1 — Multi-Agent Infrastructure Improvement
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple


class Finding:
    """A single validation finding."""

    def __init__(self, level: str, rule: str, description: str, evidence: str,
                 impact: str, recommendation: str):
        self.level = level.upper()
        self.rule = rule
        self.description = description
        self.evidence = evidence
        self.impact = impact
        self.recommendation = recommendation

    def to_markdown(self) -> str:
        return (
            f"#### [{self.level}] {self.rule}\n\n"
            f"**Description:** {self.description}\n\n"
            f"**Evidence:** {self.evidence}\n\n"
            f"**Impact:** {self.impact}\n\n"
            f"**Recommended Correction:** {self.recommendation}\n"
        )


class TaskConsistencyValidator:
    """Validates consistency between task definitions and actual state."""

    def __init__(self, root: Path):
        self.root = root
        self.findings: List[Finding] = []
        self.cc_data = None
        self.task_data = None
        self.changelog_content = ""
        self.roadmap_content = ""
        self.decisions_content = ""
        self.src_files: Set[str] = set()
        self.test_files: Set[str] = set()
        self.doc_files: Set[str] = set()

    def add_finding(self, level: str, rule: str, description: str,
                    evidence: str, impact: str, recommendation: str):
        """Add a finding."""
        self.findings.append(Finding(level, rule, description, evidence,
                                     impact, recommendation))

    def load_files(self):
        """Load all required files."""
        import yaml

        # Load CONTROL_CENTER.yaml
        cc_path = self.root / "project_management" / "CONTROL_CENTER.yaml"
        if cc_path.exists():
            with open(cc_path, "r") as f:
                self.cc_data = yaml.safe_load(f)

        # Load TASK_STATE.yaml
        task_path = self.root / "project_management" / "TASK_STATE.yaml"
        if task_path.exists():
            with open(task_path, "r") as f:
                self.task_data = yaml.safe_load(f)

        # Load markdown files
        for filename, attr in [
            ("CHANGELOG.md", "changelog_content"),
            ("ROADMAP.md", "roadmap_content"),
            ("DECISIONS.md", "decisions_content"),
        ]:
            path = self.root / "project_management" / filename
            if path.exists():
                setattr(self, attr, path.read_text())

        # Scan source files
        src_dir = self.root / "src" / "qscout"
        if src_dir.exists():
            for f in src_dir.glob("*.py"):
                self.src_files.add(f.stem)

        # Scan test files
        tests_dir = self.root / "tests"
        if tests_dir.exists():
            for f in tests_dir.glob("*.py"):
                if f.name != "__init__.py":
                    self.test_files.add(f.stem)

        # Scan doc files
        docs_dir = self.root / "docs"
        if docs_dir.exists():
            for f in docs_dir.glob("*.md"):
                self.doc_files.add(f.name)

    def extract_task_ids(self, text: str) -> Set[str]:
        """Extract task IDs from text."""
        pattern = r'(?:T-\d+[A-Z]?-\d+|T-\d+)'
        return set(re.findall(pattern, text))

    def extract_command_names(self, text: str) -> Set[str]:
        """Extract command names like GET_DEVICE_INFO from text."""
        pattern = r'GET_[A-Z_]+|SET_[A-Z_]+'
        return set(re.findall(pattern, text))

    def get_implemented_commands(self) -> Set[str]:
        """Get commands that are implemented in src/qscout/."""
        implemented = set()

        # Check command_map.py for all commands
        cmd_map = self.root / "src" / "qscout" / "command_map.py"
        if cmd_map.exists():
            content = cmd_map.read_text()
            # Find CommandDef definitions
            pattern = r'(\w+)\s*=\s*CommandDef\('
            for match in re.finditer(pattern, content):
                implemented.add(match.group(1))

        return implemented

    def get_pending_tasks(self) -> Dict[str, str]:
        """Get pending tasks from TASK_STATE.yaml."""
        tasks = {}
        if self.task_data:
            pending = self.task_data.get("tasks", {}).get("pending_tasks", [])
            for task in pending:
                tid = task.get("id", "")
                title = task.get("title", "")
                if tid:
                    tasks[tid] = title
        return tasks

    def get_completed_tasks(self) -> Dict[str, str]:
        """Get completed tasks from TASK_STATE.yaml."""
        tasks = {}
        if self.task_data:
            completed = self.task_data.get("tasks", {}).get("completed_tasks", [])
            for task in completed:
                tid = task.get("id", "")
                title = task.get("title", "")
                if tid:
                    tasks[tid] = title
        return tasks

    def rule_1_pending_but_implemented(self):
        """Rule 1: Task marked as pending but already implemented."""
        pending = self.get_pending_tasks()
        implemented = self.get_implemented_commands()

        for tid, title in pending.items():
            # Extract command name from title
            cmd_match = re.search(r'(?:GET|SET)_[A-Z_]+', title)
            if cmd_match:
                cmd_name = cmd_match.group()
                if cmd_name in implemented:
                    self.add_finding(
                        "ERROR",
                        "Rule 1: Pending but Implemented",
                        f"Task {tid} is pending but command {cmd_name} is already implemented.",
                        f"Task title: '{title}' | Command found in command_map.py",
                        "Would waste developer time reimplementing existing code.",
                        f"Mark task {tid} as completed or remove from pending queue."
                    )

    def rule_2_completed_but_not_implemented(self):
        """Rule 2: Task marked as completed but missing implementation."""
        completed = self.get_completed_tasks()
        implemented = self.get_implemented_commands()

        for tid, title in completed.items():
            cmd_match = re.search(r'(?:GET|SET)_[A-Z_]+', title)
            if cmd_match:
                cmd_name = cmd_match.group()
                if cmd_name not in implemented:
                    self.add_finding(
                        "WARNING",
                        "Rule 2: Completed but Not Implemented",
                        f"Task {tid} is marked completed but command {cmd_name} not found in code.",
                        f"Task title: '{title}' | Command not in command_map.py",
                        "Status tracking may be inaccurate.",
                        f"Verify if command {cmd_name} exists under different name or was removed."
                    )

    def rule_3_implemented_but_no_docs(self):
        """Rule 3: Task implemented but missing documentation."""
        implemented = self.get_implemented_commands()
        changelog_cmds = self.extract_command_names(self.changelog_content)
        roadmap_cmds = self.extract_command_names(self.roadmap_content)

        for cmd in implemented:
            if cmd not in changelog_cmds and cmd not in roadmap_cmds:
                self.add_finding(
                    "WARNING",
                    "Rule 3: Implemented but Not Documented",
                    f"Command {cmd} exists in code but not mentioned in CHANGELOG or ROADMAP.",
                    f"Found in src/qscout/command_map.py | Not found in project_management docs",
                    "Documentation drift may confuse future developers.",
                    f"Add {cmd} to CHANGELOG.md and/or ROADMAP.md."
                )

    def rule_4_docs_but_no_task(self):
        """Rule 4: Documentation exists but task never recorded."""
        all_tasks = {**self.get_pending_tasks(), **self.get_completed_tasks()}
        changelog_tasks = self.extract_task_ids(self.changelog_content)

        for tid in changelog_tasks:
            if tid not in all_tasks and tid != "T-A5-01":  # T-A5-01 is validation task
                self.add_finding(
                    "INFO",
                    "Rule 4: Documented but No Task Record",
                    f"Task {tid} mentioned in CHANGELOG but not in TASK_STATE.yaml.",
                    f"Found in CHANGELOG.md | Not in pending_tasks or completed_tasks",
                    "Minor documentation inconsistency.",
                    f"Add {tid} to appropriate task list in TASK_STATE.yaml."
                )

    def rule_5_duplicate_task_ids(self):
        """Rule 5: Duplicate task identifiers."""
        pending = self.get_pending_tasks()
        completed = self.get_completed_tasks()

        # Check for duplicates in pending
        pending_ids = list(pending.keys())
        if len(pending_ids) != len(set(pending_ids)):
            self.add_finding(
                "ERROR",
                "Rule 5: Duplicate Task IDs",
                "Duplicate task IDs found in pending_tasks.",
                f"IDs: {pending_ids}",
                "Could cause confusion about which task to execute.",
                "Remove duplicate entries and ensure unique IDs."
            )

        # Check for duplicates in completed
        completed_ids = list(completed.keys())
        if len(completed_ids) != len(set(completed_ids)):
            self.add_finding(
                "ERROR",
                "Rule 5: Duplicate Task IDs",
                "Duplicate task IDs found in completed_tasks.",
                f"IDs: {completed_ids}",
                "Could cause confusion about task history.",
                "Remove duplicate entries."
            )

        # Check task appears in both pending and completed
        overlap = set(pending.keys()) & set(completed.keys())
        if overlap:
            self.add_finding(
                "ERROR",
                "Rule 5: Duplicate Task IDs",
                f"Tasks appear in both pending and completed lists.",
                f"Overlap: {overlap}",
                "Contradictory state — task cannot be both pending and completed.",
                "Move tasks to correct list based on actual status."
            )

    def rule_6_missing_task_ids(self):
        """Rule 6: Missing task identifiers."""
        if self.cc_data:
            current_task = self.cc_data.get("current_task", {})
            if current_task:
                tid = current_task.get("id", "")
                title = current_task.get("title", "")
                if not tid:
                    self.add_finding(
                        "ERROR",
                        "Rule 6: Missing Task ID",
                        "Current task in CONTROL_CENTER.yaml has no ID.",
                        f"Task title: '{title}' | ID field empty or missing",
                        "Cannot track or reference this task.",
                        "Add unique task ID to current_task in CONTROL_CENTER.yaml."
                    )
                if not title:
                    self.add_finding(
                        "WARNING",
                        "Rule 6: Missing Task Title",
                        "Current task in CONTROL_CENTER.yaml has no title.",
                        f"Task ID: '{tid}' | Title field empty or missing",
                        "Task purpose unclear.",
                        "Add descriptive title to current_task."
                    )

    def rule_7_phase_mismatch(self):
        """Rule 7: Phase mismatch between state files."""
        if self.cc_data and self.task_data:
            cc_phase = self.cc_data.get("current_phase", {}).get("id", "")
            task_phase = self.task_data.get("active_phase", "")

            if cc_phase and task_phase and cc_phase != task_phase:
                self.add_finding(
                    "ERROR",
                    "Rule 7: Phase Mismatch",
                    "Current phase differs between CONTROL_CENTER.yaml and TASK_STATE.yaml.",
                    f"CONTROL_CENTER: '{cc_phase}' | TASK_STATE: '{task_phase}",
                    "Agents may be working on wrong phase.",
                    "Synchronize phase information across state files."
                )

    def rule_8_duplicate_info(self):
        """Rule 8: Duplicate information between state files."""
        if self.cc_data and self.task_data:
            # Compare test counts
            cc_tests = self.cc_data.get("tests", {})
            task_validation = self.task_data.get("last_validation", {})

            cc_passing = cc_tests.get("passing", 0)
            task_passing = task_validation.get("tests_passing", 0)

            if cc_passing != task_passing:
                self.add_finding(
                    "WARNING",
                    "Rule 8: Duplicate Info Mismatch",
                    "Test counts differ between state files.",
                    f"CONTROL_CENTER: {cc_passing} passing | TASK_STATE: {task_passing} passing",
                    "One file may have stale information.",
                    "Update both files to reflect current test status."
                )

    def rule_9_orphan_documents(self):
        """Rule 9: Orphan documents."""
        all_task_ids = set()
        if self.task_data:
            pending = self.task_data.get("tasks", {}).get("pending_tasks", [])
            completed = self.task_data.get("tasks", {}).get("completed_tasks", [])
            for task in pending + completed:
                tid = task.get("id", "")
                if tid:
                    all_task_ids.add(tid)

        # Check docs directory for orphan reports
        docs_dir = self.root / "docs"
        if docs_dir.exists():
            for f in docs_dir.glob("*.md"):
                content = f.read_text()
                # Check if document references tasks not in any list
                doc_tasks = self.extract_task_ids(content)
                for tid in doc_tasks:
                    if tid.startswith("T-") and tid not in all_task_ids and tid != "T-A5-01":
                        self.add_finding(
                            "INFO",
                            "Rule 9: Orphan Document Reference",
                            f"Document {f.name} references task {tid} not in task lists.",
                            f"File: docs/{f.name} | Task ID: {tid}",
                            "Minor documentation inconsistency.",
                            f"Add {tid} to task lists or update document reference."
                        )

    def rule_10_broken_references(self):
        """Rule 10: Broken references to archived tasks."""
        archive_dir = self.root / "project_management" / "archive"
        if not archive_dir.exists():
            return

        archived_files = {f.name for f in archive_dir.glob("*") if f.is_file()}

        # Check if any active files reference archived tasks
        active_files = [
            "project_management/CONTROL_CENTER.yaml",
            "project_management/TASK_STATE.yaml",
        ]

        for filepath in active_files:
            full_path = self.root / filepath
            if not full_path.exists():
                continue

            content = full_path.read_text()
            for archived in archived_files:
                if archived in content:
                    self.add_finding(
                        "WARNING",
                        "Rule 10: Broken Reference",
                        f"Active file {filepath} references archived file {archived}.",
                        f"Found reference to: {archived}",
                        "Reference may be stale or broken.",
                        f"Update {filepath} to remove or update reference to {archived}."
                    )

    def validate(self) -> List[Finding]:
        """Run all validation rules."""
        print("Loading files...")
        self.load_files()

        print("Running Rule 1: Pending but implemented...")
        self.rule_1_pending_but_implemented()

        print("Running Rule 2: Completed but not implemented...")
        self.rule_2_completed_but_not_implemented()

        print("Running Rule 3: Implemented but no docs...")
        self.rule_3_implemented_but_no_docs()

        print("Running Rule 4: Docs but no task...")
        self.rule_4_docs_but_no_task()

        print("Running Rule 5: Duplicate task IDs...")
        self.rule_5_duplicate_task_ids()

        print("Running Rule 6: Missing task IDs...")
        self.rule_6_missing_task_ids()

        print("Running Rule 7: Phase mismatch...")
        self.rule_7_phase_mismatch()

        print("Running Rule 8: Duplicate info...")
        self.rule_8_duplicate_info()

        print("Running Rule 9: Orphan documents...")
        self.rule_9_orphan_documents()

        print("Running Rule 10: Broken references...")
        self.rule_10_broken_references()

        return self.findings

    def generate_report(self) -> str:
        """Generate the validation report."""
        errors = [f for f in self.findings if f.level == "ERROR"]
        warnings = [f for f in self.findings if f.level == "WARNING"]
        infos = [f for f in self.findings if f.level == "INFO"]

        report = """# TASK_CONSISTENCY_REPORT.md — Automatic Task Validation

**Generated:** Phase A.5.1
**Validator:** tools/task_consistency_validator.py
**Result:** {result}

---

## Summary

| Level | Count |
|-------|-------|
| ERROR | {errors} |
| WARNING | {warnings} |
| INFO | {infos} |
| **Total** | **{total}** |

---

## Validation Rules

1. Task marked as pending but already implemented
2. Task marked as completed but missing implementation
3. Task implemented but missing documentation
4. Documentation exists but task never recorded
5. Duplicate task identifiers
6. Missing task identifiers
7. Phase mismatch
8. Duplicate information between state files
9. Orphan documents
10. Broken references to archived tasks

---

""".format(
            result="PASS" if not errors else "FAIL",
            errors=len(errors),
            warnings=len(warnings),
            infos=len(infos),
            total=len(self.findings)
        )

        if self.findings:
            report += "## Findings\n\n"
            for i, finding in enumerate(self.findings, 1):
                report += f"### Finding {i}\n\n"
                report += finding.to_markdown()
                report += "\n---\n\n"
        else:
            report += "## Findings\n\nNo issues detected. All tasks are consistent.\n"

        report += """
## Recommendations

"""
        if errors:
            report += "### Critical (ERROR)\n\n"
            report += "The following issues must be resolved before development:\n\n"
            for f in errors:
                report += f"- {f.rule}: {f.description}\n"
            report += "\n"

        if warnings:
            report += "### Important (WARNING)\n\n"
            report += "The following issues should be reviewed:\n\n"
            for f in warnings:
                report += f"- {f.rule}: {f.description}\n"
            report += "\n"

        if infos:
            report += "### Informational (INFO)\n\n"
            report += "The following are minor inconsistencies:\n\n"
            for f in infos:
                report += f"- {f.rule}: {f.description}\n"
            report += "\n"

        if not self.findings:
            report += "No recommendations. All tasks are consistent.\n"

        report += """
---

**Validator:** tools/task_consistency_validator.py
**Phase:** A.5.1
"""
        return report

    def print_summary(self):
        """Print summary to console."""
        errors = [f for f in self.findings if f.level == "ERROR"]
        warnings = [f for f in self.findings if f.level == "WARNING"]
        infos = [f for f in self.findings if f.level == "INFO"]

        print("\n" + "=" * 60)
        print("TASK CONSISTENCY VALIDATION RESULTS")
        print("=" * 60)
        print(f"\n  ERROR:   {len(errors)}")
        print(f"  WARNING: {len(warnings)}")
        print(f"  INFO:    {len(infos)}")
        print(f"  Total:   {len(self.findings)}")

        if errors:
            print("\n  CRITICAL ISSUES:")
            for f in errors:
                print(f"    - [{f.rule}] {f.description}")

        if warnings:
            print("\n  WARNINGS:")
            for f in warnings:
                print(f"    - [{f.rule}] {f.description}")

        print("\n" + "=" * 60)

        if errors:
            print("RESULT: FAIL (ERROR level issues found)")
        else:
            print("RESULT: PASS (no ERROR level issues)")


def main():
    """Main entry point."""
    # Find project root
    current = Path(__file__).resolve().parent.parent
    while current != current.parent:
        if (current / "README.md").exists() and (current / "pyproject.toml").exists():
            if (current / "src" / "qscout").is_dir():
                break
        current = current.parent
    else:
        print("ERROR: Could not locate project root")
        return 1

    root = current
    print(f"Project root: {root}")

    # Create validator
    validator = TaskConsistencyValidator(root)

    # Run validation
    findings = validator.validate()

    # Generate report
    report = validator.generate_report()
    report_path = root / "docs" / "TASK_CONSISTENCY_REPORT.md"
    report_path.write_text(report)
    print(f"\nReport written to: {report_path}")

    # Print summary
    validator.print_summary()

    # Return exit code
    errors = [f for f in findings if f.level == "ERROR"]
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
