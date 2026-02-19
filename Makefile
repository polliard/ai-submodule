.PHONY: help lint-md lint-md-fix setup sync-copilot sync-cursor release

# Default target - show help
help:
	@echo "Available targets:"
	@echo "  help         - Show this help message"
	@echo "  setup        - Configure git hooks"
	@echo "  lint-md      - Check markdown files for issues"
	@echo "  lint-md-fix  - Check and auto-fix markdown issues"
	@echo "  sync-copilot - Merge instructions.md into copilot-instructions.md"
	@echo "  sync-cursor  - Generate .cursor/rules/ from instructions.md"
	@echo "  release      - Infer bump, update .symver, commit, and tag"

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

# Merge instructions.md into copilot-instructions.md (section-level merge)
sync-copilot:
	@if [ ! -f .github/copilot-instructions.md ]; then \
		cp instructions.md .github/copilot-instructions.md; \
		printf '\n---\n\n## Project-Specific Instructions\n' >> .github/copilot-instructions.md; \
		echo "copilot-instructions.md created (first sync)."; \
	else \
		python3 .githooks/merge-instructions.py instructions.md .github/copilot-instructions.md \
			> .github/copilot-instructions.md.tmp; \
		mv .github/copilot-instructions.md.tmp .github/copilot-instructions.md; \
		echo "copilot-instructions.md merged."; \
	fi

# Generate Cursor rules from instructions.md
CURSOR_DIR := .cursor/rules
sync-cursor:
	@mkdir -p $(CURSOR_DIR)
	@echo '---' > $(CURSOR_DIR)/ai-instructions.mdc
	@echo 'description: Core AI instructions synced from instructions.md' >> $(CURSOR_DIR)/ai-instructions.mdc
	@echo 'globs: **/*' >> $(CURSOR_DIR)/ai-instructions.mdc
	@echo 'alwaysApply: true' >> $(CURSOR_DIR)/ai-instructions.mdc
	@echo '---' >> $(CURSOR_DIR)/ai-instructions.mdc
	@echo '' >> $(CURSOR_DIR)/ai-instructions.mdc
	@tail -n +2 instructions.md >> $(CURSOR_DIR)/ai-instructions.mdc
	@echo "Cursor rules generated at $(CURSOR_DIR)/ai-instructions.mdc"

release:
	./scripts/release/infer-and-tag.sh

