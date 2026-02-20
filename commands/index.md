# Commands

Slash commands provide one-step access to structured workflows. Type
`/<command-name>` in any AI assistant that loads this `.ai/` submodule.

## Available Commands

### Panels

Multi-persona review panels. Each panel assembles specialist personas
to evaluate a target from multiple perspectives. Run `/panels` for a
quick reference with situational guidance. Panel reports are written to
`.panels/` (gitignored). Plans are written to `.plans/` (gitignored).

| Command | Description |
| --- | --- |
| `/panels` | List all panel commands with usage guidance |
| `/code-review-panel` | Correctness, security, performance, and maintainability review |
| `/architecture-panel` | System design, data architecture, and operational readiness |
| `/security-panel` | Offensive, defensive, and compliance security assessment |
| `/api-panel` | API design, developer experience, and consumer usability |
| `/technical-debt-panel` | Technical debt assessment and remediation prioritization |
| `/launch-readiness-panel` | Production deployment go/no-go assessment |
| `/compliance-panel` | Privacy, accessibility, and supply chain compliance |
| `/documentation-panel` | Documentation accuracy, completeness, and usability |
| `/incident-post-mortem-panel` | Root cause analysis and systemic improvements |
| `/migration-panel` | Data integrity, rollback capability, and migration safety |
| `/performance-panel` | Bottleneck identification and optimization strategy |
| `/testing-panel` | Test coverage, quality, and testing strategy |
| `/threat-panel` | STRIDE + MITRE ATT&CK threat modeling with attack trees |
| `/ai-governance-panel` | AI instruction quality, MCP config, and agent safety |

## How Commands Work

Each command is a markdown file in this directory with YAML frontmatter:

```yaml
---
description: "Short description shown in help"
argument-hint: "<what the command expects>"
allowed-tools:
  - Read
  - Glob
  - Bash
---
```

- **`description`** — Displayed when listing available commands.
- **`argument-hint`** — Shows the user what to pass as an argument.
- **`allowed-tools`** — Tools the command is permitted to use.

The body of the file contains the instructions the AI follows when the
command is invoked.

## Adding a New Command

1. Create a new `.md` file in this directory.
2. Add YAML frontmatter with `description`, `argument-hint`, and
   `allowed-tools`.
3. Write the command body with setup steps, execution process, and
   output expectations.
4. Add the command to this index.
5. Run `make lint-md-fix` before committing.
