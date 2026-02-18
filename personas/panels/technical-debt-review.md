# Panel: Technical Debt Review

## Purpose

Assess and prioritize technical debt for strategic remediation.

## Participants

- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[Refactor Specialist](../engineering/refactor-specialist.md)** - Code structure, duplication, complexity
- **[Systems Architect](../architecture/systems-architect.md)** - Architectural debt, coupling, boundaries
- **[Test Engineer](../engineering/test-engineer.md)** - Test debt, coverage gaps, flaky tests
- **[Tech Lead](../process_people/tech-lead.md)** - Business impact, team velocity, priorities
- **[Minimalist Engineer](../engineering/minimalist-engineer.md)** - Over-engineering, unnecessary complexity

## Process

1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Inventory known technical debt
3. Each participant identifies debt from their perspective
4. Assess impact on velocity and reliability
5. Estimate remediation effort
6. Present findings using the [severity scale](../_shared/severity-scale.md)
7. Prioritize by ROI

## Output Format

### Per Participant

- Perspective name
- Debt items identified
- Impact assessment
- Remediation approach

### Consolidated

- Debt inventory with categories
- High-impact items
- Quick wins (low effort, high value)
- Strategic debt (accept with monitoring)
- Recommended roadmap

## Constraints

- Quantify impact where possible
- Consider compounding effects
- Balance remediation with feature work
- Identify debt that blocks future work

## Conflict Resolution

When participants produce conflicting recommendations:

1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
