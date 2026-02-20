---
description: "List all available panel review commands"
allowed-tools: []
---

# Available Panel Commands

Run any panel by typing its slash command. Each panel brings together
multiple specialist personas for a comprehensive review.

| Command | Description |
| --- | --- |
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

## Usage

Each command accepts a target argument:

```text
/code-review-panel src/auth/
/security-panel https://github.com/org/repo
/threat-panel path/to/system
```

If no argument is provided, the panel analyzes the current working
directory.

## When to Use Which Panel

| Situation | Panel |
| --- | --- |
| Before launch | `/launch-readiness-panel` |
| Design phase | `/architecture-panel`, `/api-panel` |
| Ongoing maintenance | `/code-review-panel`, `/technical-debt-panel` |
| After incidents | `/incident-post-mortem-panel` |
| System changes | `/migration-panel`, `/testing-panel` |
| Documentation updates | `/documentation-panel` |
| Security assessments | `/security-panel` |
| Threat modeling | `/threat-panel` |
| Privacy & compliance | `/compliance-panel` |
| Performance concerns | `/performance-panel` |
| AI tooling review | `/ai-governance-panel` |

For detailed guidance on panel selection, see
`~/.ai/personas/panels-personas.md`.
