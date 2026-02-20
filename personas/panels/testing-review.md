# Panel: Testing Strategy Review

## Purpose

Evaluate test coverage, quality, and testing approach comprehensively.

## Participants

- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[Test Engineer](../engineering/test-engineer.md)** - Coverage, isolation, determinism
- **[Failure Engineer](../operations_reliability/failure-engineer.md)** - Failure scenario coverage, chaos testing
- **[Performance Engineer](../engineering/performance-engineer.md)** - Load testing, benchmarks
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Security test coverage, penetration testing
- **[Code Reviewer](../code_quality/code-reviewer.md)** - Test code quality, maintainability

## Process

1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file.
   Install and verify all required tools, deduplicating across participants
2. Review current test portfolio
3. Each participant identifies gaps from their perspective
4. Assess test reliability and maintenance burden
5. Present findings using the [severity scale](../_shared/severity-scale.md)
6. Prioritize improvements by risk reduction

## Output Format

### Per Participant

- Perspective name
- Coverage gaps identified
- Quality concerns
- Recommended additions

### Consolidated

- Critical untested paths
- Flaky test risks
- Testing infrastructure needs
- Prioritized test backlog
- Confidence assessment (High/Medium/Low)

## Constraints

- Prefer integration tests for critical paths
- Balance coverage with maintenance cost
- Ensure tests document expected behavior
- Avoid testing implementation details

## Conflict Resolution

When participants produce conflicting recommendations:

1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
