# AI Instructions

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

## Markdown Formatting

All markdown files must pass `markdownlint` with the project config
(`.markdownlint.json`). Run `make lint-md-fix` before committing.
Key rules:

- **Line length**: max 120 characters per line (MD013). Break long
  sentences, table rows, and URLs onto continuation lines.
- **Headings**: ATX style only (`# H1`, `## H2`). No underline-style
  headings (MD003).
- **Lists**: use `-` for unordered lists (MD004). Indent nested lists
  by 2 spaces (MD007).
- **Blank lines**: leave one blank line before and after headings,
  fenced code blocks, and block-level elements.
- **Fenced code blocks**: always specify a language tag
  (e.g., `` ```yaml ``, `` ```bash ``). Never leave a bare `` ``` ``.
- **First line**: every markdown file must start with a top-level `#`
  heading (MD041).
- **Duplicate headings**: no duplicate heading text among sibling
  headings (MD024). Different nesting levels may reuse text.
- **Inline HTML**: allowed when markdown cannot express the structure.

## Code Quality

- Write idiomatic code for the language in use.
- Include error handling.
- Write testable code.
- Write tests for code created with at least 80% coverage.
- Follow existing patterns in the codebase.

## Tools

- Read `.ai/project.yaml` for language, framework, test runner, linter,
  formatter, and other project settings. If the file does not exist,
  infer from workspace structure.
- Use available MCP tools first. Prefer project-specific tooling over
  generic CLI alternatives.
- MCP servers configs live in `.ai/mcp/servers/`. Each server has a
  `mcp.json` with tool definitions.
  - `~/.ai/` — personal install, shared across all repos on the machine.
  - `<repo>/.ai/` — git submodule, shared with the team.
  - VS Code: symlink `mcp/vscode.json` → `.vscode/mcp.json`. See
    [`mcp/README.md`](mcp/README.md).
- Python: always `pip install` inside `.venv`.
- Node CLI tools: use `npx`; do not install globally.
- Documentation: use Markdown. Use Mermaid syntax for all diagrams —
  never ASCII art.

## Paved Roads

For JM best practices, check repositories at
<https://github.com/JM-Paved-Roads> before introducing new patterns.

## Version Control

Before staging, run `git status --porcelain`, analyze paths, and group
changes by top-level directory and change intent. Each commit must
represent one logical change in one domain.

**Domain groupings:**

| Path pattern | Domain |
| ---------------------------------------- | -------------- |
| `src/` | Application |
| `docs/` | Documentation |
| `test/`, `__tests__/` | Tests |
| `.github/` | CI/CD |
| `infra/`, `bicep/`, `terraform/` | Infrastructure |
| `scripts/` | Tooling |
| `Makefile`, `Dockerfile`, `compose.yaml` | Build / env |
| `package.json`, `go.mod`, `*.lock` | Dependencies |
| `*.md` outside `docs/` | Context docs |

**Change intents:** `feature` · `refactor` · `bugfix` · `docs` ·
`deps` · `infra` · `chore`

**Commit rules:**

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

**Commit message format** — follow conventional commits with scope:

```text
feat(api): add user endpoint
fix(auth): correct token expiry logic
docs(readme): clarify setup steps
infra(bicep): add private endpoint
chore(deps): bump az cli version
```

## Panels & Personas

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

| If you need… | Use |
| ---------------------------------------------- | ----------------------- |
| Review of specific changes (PR, new feature) | Code Review |
| Accumulated debt assessment and prioritization | Technical Debt Review |
| System-level design (boundaries, data, infra) | Architecture Review |
| Contract design and developer experience | API Review |
| Operational go/no-go before deploy | Launch Readiness Review |
| Threat analysis and attack paths | Security Review |

For situations not covered by a predefined panel, compose a custom
panel: select 4–6 personas from `personas/index.md` plus the Moderator.
Follow the same activation protocol.

### Output Requirements

- Store reports in `docs/panel-reports/` organized by panel type and
  date.
- Create GitHub issues for actionable findings:
  - Severity label matching the finding: `critical`, `high`, `medium`,
    or `low`.
  - Include finding ID, description, recommended remediation, and a
    link to the report.
  - Add relevant labels (e.g., `security`, `performance`,
    `technical-debt`).
- Exclude `docs/panel-reports/` from git staging — generated output,
  not source.

### Shared Policies

All persona analysis is governed by these shared policy files:

| Policy | Purpose |
| ----------------------------------------------------------------------- | --------------------------------------- |
| [`_shared/tool-setup.md`](personas/_shared/tool-setup.md) | Standard bootstrap for tools |
| [`_shared/base-tools.md`](personas/_shared/base-tools.md) | Tools available across all personas |
| [`_shared/severity-scale.md`](personas/_shared/severity-scale.md) | Canonical severity ratings for findings |
| [`_shared/credential-policy.md`](personas/_shared/credential-policy.md) | Secrets and auth handling rules |
| [`_shared/scope-constraints.md`](personas/_shared/scope-constraints.md) | Rules for offensive/chaos personas |

## Reference Files

Load these when relevant — they extend or override these instructions:

- `.ai/project.yaml` — project-specific settings
- `personas/index.md` — full persona index
- `personas/panels-personas.md` — panel selection guidance
- `mcp/README.md` — MCP server install steps and available tools
