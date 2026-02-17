# .ai — Shared AI Configuration

Reusable AI instructions, prompts, personas, and templates designed to be added to any project as a git submodule.

## Contents

- **instructions.md** — Base instructions inherited by all projects
- **config.yaml** — Configuration for symlinks, defaults, and gitignore patterns
- **prompts/** — Reusable prompt templates (debug, refactor, code-review, workflows, etc.)
- **personas/** — Specialized AI personas for different roles and review types
- **templates/** — Language/framework-specific project scaffolding (Go, Python, Node, React, C#)
- **mcp/** — MCP server configurations for shared AI tooling (requires binaries installed locally)

## Why a Git Submodule?

There are several ways to share configuration across repos. A git submodule is the best fit here.

### Alternatives considered

| Approach                             | Drawback                                                                                                                                                                       |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Copy-paste**                       | Drifts immediately. No way to propagate updates across 10+ repos. You end up with N slightly different versions of the same instructions.                                      |
| **Package manager** (npm, pip, etc.) | Adds a runtime dependency and build step for static text files. Requires a registry, versioning toolchain, and a language-specific ecosystem — overkill for markdown and YAML. |
| **Monorepo / shared folder**         | Forces all projects into one repo or requires a separate sync script. Doesn't work when repos live in different orgs or on different hosts.                                    |
| **Template repo**                    | Good for bootstrapping, but one-time only. Changes to the template don't flow to repos that were created from it.                                                              |
| **Symlinks to a local path**         | Machine-specific. Breaks for every other developer who doesn't have the same filesystem layout.                                                                                |
| **Git subtree**                      | Merges history into the host repo, making it harder to cleanly update or remove. Subtree splits are error-prone and confusing for contributors.                                |

### Why submodules win for this use case

- **Version-pinned**: Each project locks to a specific commit. You update deliberately, not accidentally.
- **Single source of truth**: Fix a prompt or add a persona once, pull it into every project with one command.
- **No toolchain required**: Works with bare git — no package manager, no CI plugin, no custom scripts.
- **Clean separation**: The `.ai/` directory is its own repo with its own history. It doesn't pollute the host project's log, and removing it is a clean operation.
- **Works everywhere**: Any git host, any language, any CI system. No ecosystem lock-in.
- **Project-level overrides**: Local files (gitignored) let each project customize without forking the shared config.

The main tradeoff is that submodules require contributors to run `git submodule update` (or clone with `--recurse-submodules`). This is a well-understood git workflow and the commands are documented below.

## Adding to a Project

```bash
git submodule add git@github.com:SET-Apps/ai-submodule.git .ai
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
