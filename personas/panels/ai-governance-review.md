# Panel: AI Governance Review

## Purpose

Evaluate AI integration quality, instruction file effectiveness, MCP configuration correctness, and alignment between
  AI tooling and project conventions. Ensures AI-assisted workflows are reliable, efficient, safe, and maintainable.

## Participants

- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[LLM Analyst](../domain_specific/llm-analyst.md)** - Instruction quality, model selection, token efficiency, AI tool
  configuration
- **[LLM Engineer](../domain_specific/llm-engineer.md)** - MCP configs, prompt pipelines, agent safety, context
  management
- **[Documentation Reviewer](../documentation/documentation-reviewer.md)** - Accuracy and completeness of AI-related
  documentation
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Credential exposure in prompts, agent
  permission boundaries
- **[UX Engineer](../engineering/ux-engineer.md)** - Developer ergonomics of AI workflows, cognitive load of instruction
  files

## Process

1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file.
   Install and verify all required tools, deduplicating across participants
2. Inventory all AI instruction surfaces (.github/copilot-instructions.md, CLAUDE.md, .cursorrules, .ai/instructions.md)
3. Inventory MCP server configurations and tool definitions
4. Each participant evaluates from their perspective
5. Cross-reference instruction files for duplication and drift
6. Estimate token budgets and identify bloat
7. Present findings using the [severity scale](../_shared/severity-scale.md)
8. Prioritize improvements by impact on AI behavior accuracy

## Output Format

### Per Participant

- Perspective name
- Findings with evidence
- Severity rating
- Recommended remediation

### Consolidated

- Instruction file quality and token efficiency summary
- MCP configuration audit results
- Cross-surface duplication and drift report
- Agent safety boundary assessment
- Model-task alignment recommendations
- Prioritized improvement roadmap

## Constraints

- Test instructions by feeding them to multiple models and comparing behavior
- Verify MCP tool schemas match actual tool capabilities
- Check that instruction sync mechanisms (symlinks, merge scripts) are functional
- Measure token counts — do not estimate
- Evaluate from the perspective of a developer onboarding to the AI workflow for the first time

## Conflict Resolution

When participants produce conflicting recommendations:

1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., token efficiency vs. instruction clarity, safety vs. developer velocity)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
