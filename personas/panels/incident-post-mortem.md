# Panel: Incident Post-Mortem

## Purpose
Analyze incident for root cause and systemic improvements.

## Participants
- **[Incident Commander](../special_purpose/incident-commander.md)** - Timeline accuracy, response effectiveness
- **[SRE](../operations_reliability/sre.md)** - Detection gaps, SLO impact, operational failures
- **[Systems Architect](../architecture/systems-architect.md)** - Architectural contributing factors
- **[Failure Engineer](../operations_reliability/failure-engineer.md)** - Resilience gaps, recovery effectiveness
- **[Observability Engineer](../operations_reliability/observability-engineer.md)** - Monitoring blind spots, alert quality
- **[Debugger](../engineering/debugger.md)** - Root cause analysis, code-level fault tracing, reproduction steps

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Reconstruct incident timeline
3. Each participant analyzes from their perspective
4. Identify contributing factors (not blame)
5. Distinguish symptoms from root causes
6. Present findings using the [severity scale](../_shared/severity-scale.md)
7. Prioritize preventive actions

## Output Format
### Per Participant
- Perspective name
- Contributing factors identified
- Gaps in their domain
- Recommended improvements

### Consolidated
- Incident summary
- Root cause(s)
- Contributing factors
- What went well
- Action items with owners and deadlines
- Systemic improvements needed

## Constraints
- Focus on systems, not individuals
- Seek multiple contributing factors
- Prioritize prevention over detection
- Ensure actions are specific and measurable

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
