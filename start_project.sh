#!/bin/bash
# start_project.sh — Q-Scout Project Bootstrap Runner
# Runs all bootstrap utilities in sequence.
# Execution order:
#   1. health_check.py
#   2. project_ready.py
#   3. bootstrap.py
#   4. state_sync.py
#   5. task_consistency_validator.py
#   6. project_dashboard.py
#   7. status.py
#   8. task_dispatcher.py
#   9. agent_selector.py
#   10. session_manager.py

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="$SCRIPT_DIR/tools"
PYTHON="${PYTHON:-python3}"

echo "============================================================"
echo "  Q-SCOUT PROJECT BOOTSTRAP"
echo "============================================================"
echo ""

# Check Python
if ! command -v $PYTHON &> /dev/null; then
    echo "ERROR: Python3 not found"
    exit 1
fi

# Check PyYAML
if ! $PYTHON -c "import yaml" 2>/dev/null; then
    echo "WARNING: PyYAML not installed. Installing..."
    $PYTHON -m pip install pyyaml --quiet 2>/dev/null || true
fi

# Step 1: Health Check
echo "============================================================"
echo "  STEP 1: HEALTH CHECK"
echo "============================================================"
$PYTHON "$TOOLS_DIR/health_check.py"
HEALTH_EXIT=$?
echo ""

if [ $HEALTH_EXIT -ne 0 ]; then
    echo "PROJECT NOT READY — Health check failed"
    exit 1
fi

# Step 2: Project Ready Check
echo "============================================================"
echo "  STEP 2: PROJECT READY CHECK"
echo "============================================================"
$PYTHON "$TOOLS_DIR/project_ready.py"
READY_EXIT=$?
echo ""

if [ $READY_EXIT -ne 0 ]; then
    echo "PROJECT NOT READY — Project ready check failed"
    exit 1
fi

# Step 3: Bootstrap
echo "============================================================"
echo "  STEP 3: BOOTSTRAP"
echo "============================================================"
$PYTHON "$TOOLS_DIR/bootstrap.py"
BOOTSTRAP_EXIT=$?
echo ""

if [ $BOOTSTRAP_EXIT -ne 0 ]; then
    echo "PROJECT NOT READY — Bootstrap failed"
    exit 1
fi

# Step 4: State Synchronization
echo "============================================================"
echo "  STEP 4: STATE SYNCHRONIZATION"
echo "============================================================"
$PYTHON "$TOOLS_DIR/state_sync.py"
SYNC_EXIT=$?
echo ""

if [ $SYNC_EXIT -ne 0 ]; then
    echo "PROJECT NOT READY — State synchronization failed"
    exit 1
fi

# Step 5: Task Consistency Validation
echo "============================================================"
echo "  STEP 5: TASK CONSISTENCY VALIDATION"
echo "============================================================"
$PYTHON "$TOOLS_DIR/task_consistency_validator.py"
CONSISTENCY_EXIT=$?
echo ""

if [ $CONSISTENCY_EXIT -ne 0 ]; then
    echo "WARNING: Task consistency issues detected"
    echo "Continuing with bootstrap (ERROR level issues found)"
fi

# Step 6: Dashboard
echo "============================================================"
echo "  STEP 6: PROJECT DASHBOARD"
echo "============================================================"
$PYTHON "$TOOLS_DIR/project_dashboard.py"
echo ""

# Step 7: Status Summary
echo "============================================================"
echo "  STEP 7: STATUS SUMMARY"
echo "============================================================"
$PYTHON "$TOOLS_DIR/status.py"
echo ""

# Step 8: Task Dispatcher
echo "============================================================"
echo "  STEP 8: TASK DISPATCHER"
echo "============================================================"
$PYTHON "$TOOLS_DIR/task_dispatcher.py"
echo ""

# Step 9: Agent Selector
echo "============================================================"
echo "  STEP 9: AGENT SELECTOR"
echo "============================================================"
$PYTHON "$TOOLS_DIR/agent_selector.py"
echo ""

# Step 10: Session Manager
echo "============================================================"
echo "  STEP 10: SESSION MANAGER"
echo "============================================================"
$PYTHON "$TOOLS_DIR/session_manager.py" status
echo ""

# Final
echo "============================================================"
echo "  PROJECT READY"
echo "============================================================"
echo ""
echo "All bootstrap checks passed."
echo "The project is ready for AI agent operation."
echo ""
echo "Quick commands:"
echo "  make dashboard    — View project dashboard"
echo "  make health       — Run health check"
echo "  make validate     — Run all validators"
echo "  make start        — Run full bootstrap"
echo "  make status       — Show concise status"
echo "  make sync         — Run state synchronization"
echo "  make consistency  — Run task consistency validator"
echo ""

exit 0
