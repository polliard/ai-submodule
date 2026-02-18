# Panel: Developer Experience Review

## Purpose
Evaluate developer-facing tools, APIs, documentation, and workflows for usability, ergonomics, and productivity.

## Participants
- **[UX Engineer](../engineering/ux-engineer.md)** - API ergonomics, CLI usability, developer workflow friction
- **[Documentation Reviewer](../documentation/documentation-reviewer.md)** - Accuracy, completeness, discoverability of developer docs
- **[API Consumer](../special_purpose/api-consumer.md)** - SDK usability, onboarding experience, error message quality
- **[Test Engineer](../engineering/test-engineer.md)** - Test tooling usability, debugging experience, CI feedback loops
- **[Platform Engineer](../operations_reliability/platform-engineer.md)** - Internal developer platform quality, self-service capabilities

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Define developer personas and key workflows
3. Each participant evaluates from their perspective
4. Perform hands-on testing of key developer journeys
5. Present findings using the [severity scale](../_shared/severity-scale.md)
6. Prioritize by developer friction and frequency of impact

## Output Format
### Per Participant
- Perspective name
- Friction points identified
- Impact on developer productivity
- Recommended improvements

### Consolidated
- Critical developer experience blockers
- High-friction workflows needing simplification
- Documentation gaps affecting onboarding
- Tooling improvements with highest leverage
- Developer satisfaction assessment (Strong / Adequate / Needs Work / Poor)

## Constraints
- Test from a newcomer perspective, not expert familiarity
- Measure time-to-first-success for key workflows
- Evaluate error messages and failure modes, not just happy paths
- Consider diverse developer environments and skill levels

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
