# Makefile — Q-Scout Project Operations

.PHONY: start health dashboard validate session status help sync ready consistency

PYTHON ?= python3
TOOLS = tools

# Default target
help:
	@echo "Q-Scout Project Operations"
	@echo "=========================="
	@echo ""
	@echo "Commands:"
	@echo "  make start       — Run full bootstrap sequence"
	@echo "  make health      — Run health check"
	@echo "  make ready       — Run project ready check"
	@echo "  make dashboard   — Display project dashboard"
	@echo "  make status      — Show concise status summary"
	@echo "  make sync        — Run state synchronization"
	@echo "  make validate    — Run all validators"
	@echo "  make consistency — Run task consistency validator"
	@echo "  make dispatch    — Run task dispatcher"
	@echo "  make agents      — Run agent selector"
	@echo "  make session     — Session manager (open|close|resume|status)"
	@echo "  make tests       — Run SDK test suite"
	@echo "  make help        — Show this help"
	@echo ""

# Full bootstrap sequence
start:
	@chmod +x start_project.sh
	@./start_project.sh

# Health check
health:
	@$(PYTHON) $(TOOLS)/health_check.py

# Project ready check
ready:
	@$(PYTHON) $(TOOLS)/project_ready.py

# Project dashboard
dashboard:
	@$(PYTHON) $(TOOLS)/project_dashboard.py

# Concise status summary
status:
	@$(PYTHON) $(TOOLS)/status.py

# State synchronization
sync:
	@$(PYTHON) $(TOOLS)/state_sync.py

# Task consistency validation
consistency:
	@$(PYTHON) $(TOOLS)/task_consistency_validator.py

# Run all validators
validate: validate-yaml validate-docs consistency
	@echo ""
	@echo "All validation complete"

validate-yaml:
	@echo "Validating YAML files..."
	@$(PYTHON) $(TOOLS)/validate_yaml.py

validate-docs:
	@echo "Validating documentation..."
	@$(PYTHON) $(TOOLS)/validate_docs.py

# Task dispatcher
dispatch:
	@$(PYTHON) $(TOOLS)/task_dispatcher.py

# Agent selector
agents:
	@$(PYTHON) $(TOOLS)/agent_selector.py

# Session manager
session:
	@if [ "$(ACTION)" = "open" ]; then \
		$(PYTHON) $(TOOLS)/session_manager.py open; \
	elif [ "$(ACTION)" = "close" ]; then \
		$(PYTHON) $(TOOLS)/session_manager.py close; \
	elif [ "$(ACTION)" = "resume" ]; then \
		$(PYTHON) $(TOOLS)/session_manager.py resume; \
	else \
		$(PYTHON) $(TOOLS)/session_manager.py status; \
	fi

# Run SDK tests
tests:
	@cd /home/munumu/Qscout && PYTHONPATH=src python3 -m unittest discover -s tests

# Open a session
session-open:
	@$(PYTHON) $(TOOLS)/session_manager.py open

# Close current session
session-close:
	@$(PYTHON) $(TOOLS)/session_manager.py close

# Resume a session
session-resume:
	@$(PYTHON) $(TOOLS)/session_manager.py resume
