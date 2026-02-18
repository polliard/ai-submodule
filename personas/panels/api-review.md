# Panel: API Review

## Purpose

Evaluate API design, developer experience, and consumer usability from provider, consumer, and documentation perspectives.

## Participants

- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[API Designer](../architecture/api-designer.md)** - REST correctness, versioning, contracts
- **[API Consumer](../special_purpose/api-consumer.md)** - Usability, onboarding experience, error message quality
- **[UX Engineer](../engineering/ux-engineer.md)** - API ergonomics, CLI usability, developer workflow friction
- **[Frontend Engineer](../domain_specific/frontend-engineer.md)** - Client integration, caching, offline support
- **[Backend Engineer](../domain_specific/backend-engineer.md)** - Implementation feasibility, performance
- **[Documentation Reviewer](../documentation/documentation-reviewer.md)** - Accuracy, completeness, discoverability of developer docs

## Process

1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Review API contract, documentation, and SDK surface
3. Define developer personas and key workflows
4. Each participant evaluates from their perspective
5. Perform hands-on testing of key consumer journeys
6. Identify breaking change risks
7. Present findings using the [severity scale](../_shared/severity-scale.md)
8. Prioritize by developer friction and frequency of impact
9. Converge on design and experience improvements

## Output Format

### Per Participant

- Perspective name
- Design or usability concerns
- Impact on developer productivity
- Suggested changes

### Consolidated

- Contract issues requiring change
- Breaking change risks
- Critical developer experience blockers
- High-friction workflows needing simplification
- Documentation gaps affecting onboarding
- Versioning recommendations
- Developer satisfaction assessment (Strong / Adequate / Needs Work / Poor)

## Constraints

- Prioritize backward compatibility
- Consider multiple client types
- Ensure consistent error semantics
- Design for evolution
- Test from a newcomer perspective, not expert familiarity
- Measure time-to-first-success for key workflows
- Evaluate error messages and failure modes, not just happy paths

## Conflict Resolution

When participants produce conflicting recommendations:

1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
