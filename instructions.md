# AI Instructions

<!-- Target: <1500 tokens for core rules. Offload reference material to linked files. -->

> Base instructions for AI assistants across all projects.
> Load this file before beginning any task in a repo.

## Quick Reference

Five core behaviors:

1. Be direct — prefer code over explanation.
2. Check `.ai/project.yaml` for project settings before starting.
3. Use American English.
4. Keep documentation in sync with code.
5. Use available MCP tools before generic alternatives.

## Core Behavior

- Be direct and concise. Default to showing code over narrating it.
- Infer intent and act. Ask only when intent is genuinely ambiguous
  and the answer materially changes your approach.
- Follow existing patterns before introducing new ones.
- Prefer iterative, scoped changes over large rewrites.
- Link to relevant files when their paths are known and the reference
  aids understanding.
- Before modifying code, read `project.yaml` and understand the
  project structure, key directories, and tech stack.

## Protected Files

The following files are managed by enterprise policy and must never be
modified, deleted, or recreated by AI assistants:

- `.github/workflows/jm-compliance.yml` — Enterprise JM Compliance
  workflow. Changes are blocked by an enterprise push ruleset and will
  cause pipeline failures.

## Security

- Never hardcode secrets, tokens, or credentials. Use environment
  variables or secret managers.
- Never commit `.env` files, private keys, or connection strings.
- Use parameterized queries for all database operations. Never
  concatenate user input into SQL strings.
- Sanitize all user input before passing to shell commands, file
  paths, or template engines.
- Never disable TLS/SSL verification in production code.
- Never use `eval()`, `exec()`, or equivalent on untrusted input.
- Never run destructive commands (`rm -rf`, `git push --force`,
  `DROP TABLE`, `docker system prune`) without explicit user
  confirmation.
- Prefer least-privilege access in IAM policies, service accounts,
  and file permissions.

## Agent Mode

When operating autonomously (Copilot agent mode, Claude Code,
Cursor Composer):

- **Verify changes**: run project tests and `make lint-md-fix`
  after edits before proceeding.
- **Scope changes**: only modify files directly related to the
  current task.
- **Incremental commits**: for multi-file changes, commit
  incrementally rather than in one massive commit.
- **Destructive-command guards**: never force-push, delete
  branches, drop databases, or run destructive commands without
  user confirmation.
- **Rollback on failure**: if tests fail after a change, revert
  and explain the failure before retrying.
- **File creation policy**: do not create summary, log, or
  report files unless explicitly requested.
- **Test preservation**: never delete or weaken existing tests.
  Only add or strengthen. If a test must change, explain why
  before modifying it.

## Conditional Behavior

- If MCP tools are available, prefer them over CLI alternatives.
  If not, fall back to CLI.
- If running in agent mode with terminal access, verify changes
  before committing. If in chat-only mode, provide commands for
  the user to run.
- If the project has no `project.yaml`, infer settings from
  workspace structure (lockfiles, configs, directory layout).

## Code Quality

- Write idiomatic code for the language in use.
- Include error handling.
- Write testable code.
- Write tests for code created with at least 80% coverage.
- Follow existing patterns in the codebase.

## Coding Languages

### Python

- Always use virtual environments `.venv`.
- If there are multiple projects within a repo, use `.venv` inside
  subdirectories to separate needed tooling.

### JavaScript and TypeScript

- Use `package-lock.json` or `yarn.lock` — always commit lockfiles.
- Prefer `npx` for one-shot CLI tool execution over global installs.
- Use project-local ESLint and Prettier configs; do not rely on global
  settings.
- Follow the existing code style (e.g., semicolons, quotes).
- Use existing linting and formatting tools (e.g., ESLint, Prettier).
- For new projects, use standard tools like ESLint with Airbnb config
  and Prettier.
- Use JSDoc for function documentation.

### Go

- Follow standard `go mod` for dependency management.
- Use `go vet` and `staticcheck` for static analysis.
- Keep module paths consistent with repository structure.

### C#/DotNet

- Always use Xunit for testing.
- Always use playwright for UAT testing.
- Always document the code
- Always generate HTML documentation

### Dependencies

When adding dependencies to any language:

- Prefer standard library solutions before third-party packages.
- Check license compatibility before adding a dependency.
- Verify the package is actively maintained (recent commits, open
  issue triage).
- Pin versions in lockfiles. Avoid floating version ranges in
  production.

## Tools

- Read `.ai/project.yaml` for language, framework, test runner, linter,
  formatter, and other project settings. If the file does not exist,
  infer from workspace structure.
- Use available MCP tools first. Prefer project-specific tooling over
  generic CLI alternatives.
- MCP server configs live in `.ai/mcp/servers/`. Each server has a
  `mcp.json` with tool definitions.
  - `~/.ai/` — personal install, shared across all repos on the
    machine.
  - `<repo>/.ai/` — git submodule, shared with the team.
  - VS Code: symlink `mcp/vscode.json` → `.vscode/mcp.json`. See
    [`mcp/README.md`](mcp/README.md).
- Python: always `pip install` inside `.venv`.
- Node CLI tools: use `npx`; do not install globally.

## Documentation

- Always use markdown files for documentation unless specified.
- Always use mermaid diagrams for documentation within markdown files.

## Markdown Formatting

All markdown files must pass `markdownlint` with the project config
(`.markdownlint.json`). Run `make lint-md-fix` before committing.
See `.markdownlint.json` for the full ruleset.

## Paved Roads

For JM best practices, check repositories at
<https://github.com/JM-Paved-Roads> before introducing new patterns.

## Version Control

Before staging, run `git status --porcelain`, analyze paths, and group
changes by top-level directory and change intent. Each commit must
represent one logical change in one domain.

### Push

- After committing the code, always ask to push
- When pushing code, always check the CI state in the background
- if it fails
  - log a issue
  - create a branch with the issue number inside the users network-id and the
  type of issue it found.  Example itsfwcp/bug/issue-number
  - fix the code in a background thread using a moderator agent to manage
  communications.
  - Once complete, push and repeast until all issues are fixed.
- After pushing to a PR, check for Copilot review comments using
  `gh api repos/{owner}/{repo}/pulls/{number}/comments`. For each
  Copilot recommendation:
  - Create a GitHub issue with the appropriate priority and labels.
  - Fix the issue in the current branch.
  - Commit, push, and close the issue.

### Semantic Versioning

- Before committing, determine the version bump type (major, minor,
  patch, or none) from the user.
- Read the `.symver` file and increment the selected component by 1
  unless the choice is none.
- If `.symver` is modified, tag and push both tags and repo together
  when the user says push.

### Domain Groupings

| Path pattern                             | Domain         |
| ---------------------------------------- | -------------- |
| `src/`                                   | Application    |
| `docs/`                                  | Documentation  |
| `test/`, `__tests__/`                    | Tests          |
| `.github/`                               | CI/CD          |
| `infra/`, `bicep/`, `terraform/`         | Infrastructure |
| `scripts/`                               | Tooling        |
| `Makefile`, `Dockerfile`, `compose.yaml` | Build / env    |
| `package.json`, `go.mod`, `*.lock`       | Dependencies   |
| `*.md` outside `docs/`                   | Context docs   |

### Change Intents

`feature` · `refactor` · `bugfix` · `docs` · `deps` · `infra` ·
`chore`

### Commit Rules

- One commit = one domain + one intent. Grouping must consider both
  path and intent, not file extension alone.
- Source (`src/`) and docs: separate commits unless the docs change is
  a minimal inline API comment sync.
- Dependency files with source: same commit only if required for
  compilation; otherwise isolate.
- `src/` and `test/` when tests are directly related: same commit is
  allowed.
- Formatting-only: commit independently as `chore: format codebase`.
  Never combine with logic changes.
- Multiple intents detected: do not auto-commit. Present a categorized
  grouping proposal and wait for confirmation. In agentic contexts with
  no user interaction, abort and explain why.
- Never commit directly to `main` or `master`. Create feature branches
  for changes.

### Commit Message Format

Follow conventional commits with scope:

```text
feat(api): add user endpoint
fix(auth): correct token expiry logic
docs(readme): clarify setup steps
infra(bicep): add private endpoint
chore(deps): bump az cli version
```

## Panels and Personas

Use **personas** for focused single-perspective analysis. Use **panels**
for multi-perspective reviews that consolidate into actionable
recommendations.

- Personas: `personas/`
- Panels: `personas/panels/`
- Selection guidance: `personas/panels-personas.md`

### Activation Protocol

Apply to every persona or panel before analysis begins:

1. Load the full persona definition file from `personas/`.
2. Execute `## Tool Setup` from the persona file: check availability,
   install missing tools, verify, document constraints.
3. For panels: run Tool Setup across all personas, deduplicating shared
   tools — each tool installed once only.
4. Proceed with `## Evaluate For` using the verified toolchain.

### Moderator

Every panel includes the Moderator persona. The Moderator orchestrates
turn order, enforces the severity scale, surfaces conflicts, and
consolidates all participant findings into the final output. The
Moderator contributes no domain findings.

### Panel Selection

| If you need                                    | Use                     |
| ---------------------------------------------- | ----------------------- |
| Review of specific changes (PR, new feature)   | Code Review             |
| Accumulated debt assessment and prioritization | Technical Debt Review   |
| System-level design (boundaries, data, infra)  | Architecture Review     |
| Contract design and developer experience       | API Review              |
| Operational go/no-go before deploy             | Launch Readiness Review |
| Threat analysis and attack paths               | Security Review         |

For situations not covered by a predefined panel, compose a custom
panel: select 4-6 personas from `personas/index.md` plus the Moderator.
Follow the same activation protocol.

### Output Requirements

- Store panel reports in `.panels/` organized by panel type and date.
  This directory is gitignored — generated output, not source.
- Store plans in `.plans/`. This directory is gitignored.
- Create GitHub issues for actionable findings:
  - Severity label matching the finding: `critical`, `high`, `medium`,
    or `low`.
  - Include finding ID, description, recommended remediation, and a
    link to the report.
  - Add relevant labels (e.g., `security`, `performance`,
    `technical-debt`).

### Gitignore Management

Manage `.gitignore` using `~/bin/gitignore`. Before running, check the
existing `.gitignore` in the target path to avoid duplicates.

```bash
# Check current .gitignore first
cat .gitignore
# Then add patterns
~/bin/gitignore ignore .panels/
~/bin/gitignore ignore .plans/
```

Both `.panels/` and `.plans/` must be present in every project
`.gitignore`. Verify before committing.

### Shared Policies

All persona analysis is governed by these shared policy files:

| Policy                                  | Purpose                       |
| --------------------------------------- | ----------------------------- |
| [`_shared/tool-setup.md`][tool-setup]   | Standard bootstrap for tools  |
| [`_shared/base-tools.md`][base-tools]   | Tools across all personas     |
| [`_shared/severity-scale.md`][severity] | Canonical severity ratings    |
| [`_shared/credential-policy.md`][creds] | Secrets and auth handling     |
| [`_shared/scope-constraints.md`][scope] | Offensive/chaos persona rules |

[tool-setup]: personas/_shared/tool-setup.md
[base-tools]: personas/_shared/base-tools.md
[severity]: personas/_shared/severity-scale.md
[creds]: personas/_shared/credential-policy.md
[scope]: personas/_shared/scope-constraints.md

## Reference Files

Load these when relevant — they extend or override these instructions:

- `.ai/project.yaml` — project-specific settings
- `personas/index.md` — full persona index
- `personas/panels-personas.md` — panel selection guidance
- `mcp/README.md` — MCP server install steps and available tools
