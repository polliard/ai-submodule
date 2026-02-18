.PHONY: lint-md lint-md-fix setup

# Setup git hooks
setup:
	git config core.hooksPath .githooks
	@echo "Git hooks configured."

# Markdown linting using markdownlint-cli
lint-md:
	@command -v markdownlint >/dev/null 2>&1 || { echo "Installing markdownlint-cli..."; npm install -g markdownlint-cli; }
	markdownlint '**/*.md' --ignore node_modules --ignore .venv

lint-md-fix:
	@command -v markdownlint >/dev/null 2>&1 || { echo "Installing markdownlint-cli..."; npm install -g markdownlint-cli; }
	markdownlint '**/*.md' --ignore node_modules --ignore .venv --fix

