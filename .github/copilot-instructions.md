# AI Instructions

> **Version**: 2.0 | **Last updated**: 2026-02-17

Base instructions for AI assistants across all projects.

## Core Principles

- Be concise and direct
- Show, don't tell - prefer code over explanations
- Follow project conventions (see project-specific instructions)
- Ask clarifying questions when requirements are ambiguous
- Prefer iterative changes over large rewrites
- Always keep documentation in sync with code.
- Use American English for spelling, naming conventions, and checks
- In repositories always use markdown files for documentation.

## Panels and Persona Reviews
- Use personas for focused analysis from specific expert perspectives (e.g. security, performance, maintainability)
- Use panels for comprehensive reviews that consolidate multiple perspectives into actionable recommendations
- Follow the activation protocol for loading personas, setting up tools, and executing evaluations
- Refer to shared policies for tool setup, severity ratings, credential handling, and scope constraints
- For custom panels, select relevant personas and follow the same activation and evaluation process
- Create data and reporting in the format specified in the panel's output requirements, ensuring clarity and actionable insights for developers and stakeholders.
- Store the outputs in markdown files in the `docs/panel-reports` directory, organized by panel type and date for easy reference.
- Ignore the docs/panel-reports directory when staging changes for commits, as these are generated outputs and not source files.

### Behavioral Rules

## Code Quality

- Write idiomatic code for the language
- Include error handling
- Write testable code
- Follow existing patterns in the codebase

## Communication

- Use markdown formatting
- Link to relevant files when discussing code
- Provide context for suggestions

## Tools

- Use available MCP tools when they exist
- Prefer project-specific tooling over generic approaches
- Check `.ai/project.yaml` for project configuration (language, framework, test runner, linter, formatter, and other project-specific settings)

### MCP Servers

MCP server configs live in `.ai/mcp/servers/`. This `.ai/` directory can be:

- **`~/.ai/`** — Personal install, shared across all repos on the machine
- **`<repo>/.ai/`** — Git submodule, shared with the team

Each server has a `mcp.json` with its tool definitions. For VS Code, symlink `mcp/vscode.json` → `.vscode/mcp.json`. See [mcp/README.md](mcp/README.md) for per-server install steps and available tools.

## Personas & Panels

- Personas are individual expert perspectives (see `personas/`)
- Panels are multi-persona collaborative reviews (see `personas/panels/`)
- Use panels when comprehensive evaluation from multiple perspectives is needed
- Panel output consolidates individual findings into actionable recommendations
- See `personas/panels-personas.md` for guidance on which panel to use

### Activation Protocol

When activating any persona or panel, follow this sequence before beginning analysis:

1. **Load the persona file** — Read the full persona definition from `personas/`
2. **Execute Tool Setup** — Run the `## Tool Setup` bootstrap in the persona file: check tool availability, install missing tools, verify installations, and document any constraints
3. **Begin analysis** — Proceed with the `## Evaluate For` criteria using the verified toolchain

For panels, execute Tool Setup across all participating personas before any participant begins their review. Deduplicate shared tools — install each tool only once even if multiple personas list it.

### Shared Policies

All persona-based analysis is governed by these shared policies:

- **[Tool Setup](personas/_shared/tool-setup.md)** — Standard bootstrap procedure for installing and verifying tools
- **[Base Tools](personas/_shared/base-tools.md)** — Shared tools available across all personas
- **[Severity Scale](personas/_shared/severity-scale.md)** — Canonical severity ratings for all findings
- **[Credential Policy](personas/_shared/credential-policy.md)** — Rules for handling authentication and secrets
- **[Scope Constraints](personas/_shared/scope-constraints.md)** — Mandatory requirements for offensive and chaos engineering personas

Tool isolation: All `pip install` commands must run inside a Python virtual environment. Use `npx` for Node.js CLI tools to avoid global installs.

### Choosing Between Similar Panels

- **Code Review** vs **Technical Debt Review**: Use Code Review for evaluating specific changes (PRs, new features). Use Technical Debt Review for assessing accumulated debt across the codebase and prioritizing remediation.
- **Architecture Review** vs **API Review**: Use Architecture Review for system-level design (boundaries, data models, infrastructure). Use API Review for contract design, developer experience, and consumer usability.
- **Launch Readiness Review** vs **Security Review**: Launch Readiness covers operational readiness across the board (deploy, monitor, rollback). Security Review focuses specifically on threat analysis, attack paths, and security posture.

### Custom Panels

For situations that don't fit a predefined panel, compose an ad-hoc panel by selecting 4-6 personas from `personas/index.md`. Follow the same activation protocol: load all persona files, deduplicate and bootstrap tools, then have each persona evaluate independently before consolidating findings.

## Coding Languages

### Python

- Always use virtual environments .venv
- If there are multiple "projects" within a repo, use .venv inside of the subdirectories to separate needed tooling.

### JavaScript / TypeScript

- Use `package-lock.json` or `yarn.lock` — always commit lockfiles
- Prefer `npx` for one-shot CLI tool execution over global installs
- Use project-local ESLint and Prettier configs; do not rely on global settings
- Follow the existing code style (e.g. semicolons, quotes)
- Use existing linting and formatting tools (e.g. ESLint, Prettier)
- For new projects, use standard tools like ESLint with Airbnb config and Prettier
- Use JSDoc for function documentation

### Go

- Follow standard `go mod` for dependency management
- Use `go vet` and `staticcheck` for static analysis
- Keep module paths consistent with repository structure

### Markdown

- Use consistent heading levels
- Use bullet points for lists
- Use code blocks for code snippets
- Link to relevant files and documentation
- Use tables for structured data when appropriate
- Use mermaid for diagrams
- For new projects, use a standard markdown linter like markdownlint

### Version Control

#### Filesystem-Aware Grouping

Before staging any changes:

- Inspect git status --porcelain
- Analyze full file paths
- Categorize files by top-level domain and functional purpose

Group by:

- src/ → application source code
docs/ → documentation only
test/ or **tests**/ → tests
- .github/ → CI/CD workflows
- infra/, bicep/, terraform/ → infrastructure
- scripts/ → operational tooling
- Root config files → build/toolchain config
- Makefile, Dockerfile, compose.yaml → environment/build system
- *.md outside docs → contextual documentation
- Dependency files (package.json, go.mod, etc.) → dependency management

Do not infer grouping by file extension alone.
Grouping must consider both path and intent.

#### Commit Isolation Rules

A single commit MUST:

- Modify only one logical domain
- Represent one conceptual change
- Be reversible without affecting unrelated systems

A commit MUST NOT:

- Mix documentation and source changes (unless doc strictly explains that change)
- Mix infra and app logic
- Mix dependency updates with feature code
- Mix formatting-only changes with behavioral changes

#### Intent Evaluation

Before committing determine whether changes are:

- Feature
- Refactor
- Bugfix
- Documentation
- Dependency update
- Infrastructure change
- Formatting-only

If multiple intents exist → create separate commits.

#### Structural Heuristics

If multiple directories changed:

- If changes share a common parent directory → may group.
- If changes span unrelated roots → must split.
- If change touches both src/ and test/ and tests are directly related → allow same commit.
- If change touches src/ and docs/ → split unless docs are minimal API comment sync.

#### Dependency Edge Case

If src/ change requires go.mod / package.json change:

- Allow in same commit if directly required for compilation.
- Otherwise → isolate.

#### Formatting and Linting

If formatting touches many files but no logic changed:

- Separate commit titled chore: format codebase.
- Never mix formatting with feature logic.

#### Commit Message Enforcement

Each commit must:

- Follow conventional commits (if repo uses them)
- Be scoped:
- feat(api): add user endpoint
- docs(readme): clarify setup steps
- infra(bicep): add private endpoint
- test(auth): add token validation tests
- chore(deps): bump az cli version

#### Refusal Behavior

If logical separation cannot be determined:

- Do not auto-commit.
- Present categorized grouping proposal.
- Require confirmation before staging.

---

## Project-Specific Instructions

### Pre-Commit Checks

Before committing any changes that include markdown files, run the markdown linter:

```bash
make lint-md-fix
```

This will check and auto-fix common markdown issues. If issues remain after auto-fix, resolve them manually before committing.

For check-only (no auto-fix):

```bash
make lint-md
```
