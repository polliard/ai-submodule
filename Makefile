.PHONY: help lint-md lint-md-fix setup

# Default target - show help
help:
	@echo "Available targets:"
	@echo "  help        - Show this help message"
	@echo "  setup       - Configure git hooks"
	@echo "  lint-md     - Check markdown files for issues"
	@echo "  lint-md-fix - Check and auto-fix markdown issues"

# Setup git hooks (idempotent - checks if already configured)
setup:
	@CURRENT=$$(git config --get core.hooksPath 2>/dev/null || echo ""); \
	if [ "$$CURRENT" = ".githooks" ]; then \
		echo "Git hooks already configured."; \
	else \
		git config core.hooksPath .githooks; \
		echo "Git hooks configured."; \
	fi

# Markdown linting using markdownlint-cli
lint-md:
	@command -v markdownlint >/dev/null 2>&1 || { echo "Installing markdownlint-cli..."; npm install -g markdownlint-cli; }
	markdownlint '**/*.md' --ignore node_modules --ignore .venv

lint-md-fix:
	@command -v markdownlint >/dev/null 2>&1 || { echo "Installing markdownlint-cli..."; npm install -g markdownlint-cli; }
	markdownlint '**/*.md' --ignore node_modules --ignore .venv --fix

