# Panel: Migration Review

## Purpose

Evaluate migration plan safety, completeness, and risk mitigation.

## Participants

- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[Migration Specialist](../special_purpose/migration-specialist.md)** - Plan completeness, rollback capability
- **[Data Architect](../domain_specific/data-architect.md)** - Data integrity, transformation correctness
- **[SRE](../operations_reliability/sre.md)** - Operational readiness, monitoring during migration
- **[Failure Engineer](../operations_reliability/failure-engineer.md)** - Failure scenarios, recovery procedures
- **[Tech Lead](../process_people/tech-lead.md)** - Timeline, resource allocation, communication

## Process

1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file.
   Install and verify all required tools, deduplicating across participants
2. Review migration plan and timeline
3. Each participant assesses from their perspective
4. Identify rollback gaps
5. Stress-test failure scenarios
6. Present findings using the [severity scale](../_shared/severity-scale.md)
7. Validate communication plan

## Output Format

### Per Participant

- Perspective name
- Plan gaps
- Risk concerns
- Required additions

### Consolidated

- Migration blockers
- Risk mitigations required
- Rollback verification checklist
- Monitoring requirements
- Go/No-Go recommendation

## Constraints

- Require tested rollback at every step
- Validate data integrity continuously
- Plan for extended migration states
- Ensure clear abort criteria

## Conflict Resolution

When participants produce conflicting recommendations:

1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
