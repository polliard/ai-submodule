# .ai — Shared AI Configuration

Reusable AI instructions, prompts, personas, and templates designed to be added to any project as a git submodule.

## Contents

- **instructions.md** — Base instructions inherited by all projects
- **config.yaml** — Configuration for symlinks, defaults, and gitignore patterns
- **prompts/** — Reusable prompt templates (debug, refactor, code-review, workflows, etc.)
- **personas/** — Specialized AI personas for different roles and review types
- **templates/** — Language/framework-specific project scaffolding (Go, Python, Node, React, C#)

## Adding to a Project

```bash
git submodule add <YOUR_REMOTE_URL> .ai
git commit -m "Add .ai submodule"
```

This clones the `.ai` repo into your project at the `.ai/` path.

## Cloning a Project That Uses This Submodule

When cloning a repo that already includes this submodule:

```bash
# Option 1: Clone with submodules in one step
git clone --recurse-submodules <PROJECT_URL>

# Option 2: Initialize after cloning
git clone <PROJECT_URL>
cd <project>
git submodule init
git submodule update
```

## Updating the Submodule

To pull the latest changes from this repo into your project:

```bash
# From the project root
git submodule update --remote .ai
git add .ai
git commit -m "Update .ai submodule"
```

Or enter the submodule directory directly:

```bash
cd .ai
git pull origin main
cd ..
git add .ai
git commit -m "Update .ai submodule"
```

## Pinning a Specific Version

Submodules track a specific commit. To pin to a tag or commit:

```bash
cd .ai
git checkout v1.0.0   # or a specific commit hash
cd ..
git add .ai
git commit -m "Pin .ai submodule to v1.0.0"
```

## Project-Specific Overrides

The submodule provides shared defaults. To customize per-project:

1. **Create a `project.yaml`** in `.ai/` (gitignored via `*.local.*` patterns) or at the project root
2. **Add project-specific instructions** that extend the base `instructions.md`
3. **Use `config.yaml` symlinks** to map instructions to tool-specific files:
   - `.github/copilot-instructions.md`
   - `CLAUDE.md`
   - `.cursorrules`

## Removing the Submodule

```bash
git submodule deinit -f .ai
git rm -f .ai
rm -rf .git/modules/.ai
git commit -m "Remove .ai submodule"
```
