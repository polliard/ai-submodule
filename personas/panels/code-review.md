# Panel: Code Review

## Purpose

Comprehensive code evaluation from multiple engineering perspectives.

## Participants

- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[Code Reviewer](../code_quality/code-reviewer.md)** - Correctness, edge cases, error handling
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Vulnerabilities, input validation, secrets
- **[Performance Engineer](../engineering/performance-engineer.md)** - Complexity, allocations, bottlenecks
- **[Test Engineer](../engineering/test-engineer.md)** - Testability, coverage gaps, mock quality
- **[Refactor Specialist](../engineering/refactor-specialist.md)** - Structure, duplication, maintainability

## Process

1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file.
   Install and verify all required tools, deduplicating across participants
2. Each participant reviews independently
3. Present findings using the [severity scale](../_shared/severity-scale.md)
4. Identify conflicting recommendations
5. Produce consolidated assessment

## Output Format

### Per Participant

- Perspective name
- Key concerns (bulleted)
- Risk level
- Suggested changes

### Consolidated

- Must-fix items
- Should-fix items
- Consider items
- Tradeoff summary
- Final recommendation (Approve/Request Changes/Reject)

## Constraints

- Focus on substantive issues, not style preferences
- Resolve conflicts explicitly with reasoning
- Provide concrete remediation for each issue

## Conflict Resolution

When participants produce conflicting recommendations:

1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
