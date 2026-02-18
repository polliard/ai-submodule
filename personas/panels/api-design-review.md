# Panel: API Design Review

## Purpose
Evaluate API design from provider and consumer perspectives.

## Participants
- **[API Designer](../architecture/api-designer.md)** - REST correctness, versioning, contracts
- **[API Consumer](../special_purpose/api-consumer.md)** - Usability, documentation, error messages
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Auth, rate limiting, input validation
- **[Backend Engineer](../domain_specific/backend-engineer.md)** - Implementation feasibility, performance
- **[Frontend Engineer](../domain_specific/frontend-engineer.md)** - Client integration, caching, offline support

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Review API contract and documentation
3. Each participant evaluates from their perspective
4. Identify breaking change risks
5. Test typical consumer workflows
6. Present findings using the [severity scale](../_shared/severity-scale.md)
7. Converge on design improvements

## Output Format
### Per Participant
- Perspective name
- Design concerns
- Usability issues
- Suggested changes

### Consolidated
- Contract issues requiring change
- Breaking change risks
- Documentation gaps
- Implementation concerns
- Versioning recommendations

## Constraints
- Prioritize backward compatibility
- Consider multiple client types
- Ensure consistent error semantics
- Design for evolution

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
