# Panel: Documentation Review

## Purpose

Evaluate documentation completeness, accuracy, and usability.

## Participants

- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[Documentation Reviewer](../documentation/documentation-reviewer.md)** - Accuracy, completeness, structure
- **[Documentation Writer](../documentation/documentation-writer.md)** - Clarity, examples, task orientation
- **[API Consumer](../special_purpose/api-consumer.md)** - Discoverability, onboarding experience
- **[Mentor](../process_people/mentor.md)** - Learning progression, concept explanation
- **[UX Engineer](../engineering/ux-engineer.md)** - Developer ergonomics, cognitive load

## Process

1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file.
   Install and verify all required tools, deduplicating across participants
2. Identify target audiences
3. Each participant evaluates from their perspective
4. Test documentation by following it
5. Identify gaps and inconsistencies
6. Present findings using the [severity scale](../_shared/severity-scale.md)
7. Prioritize improvements by user impact

## Output Format

### Per Participant

- Perspective name
- Gaps identified
- Usability issues
- Suggested improvements

### Consolidated

- Critical missing documentation
- Accuracy issues requiring immediate fix
- Structure improvements
- Example additions needed
- Maintenance recommendations

## Constraints

- Verify code examples actually work
- Test from newcomer perspective
- Ensure documentation matches current behavior
- Prioritize task completion over exhaustive reference

## Conflict Resolution

When participants produce conflicting recommendations:

1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
