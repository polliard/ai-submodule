# Panel: Performance Review

## Purpose
Comprehensive performance analysis from multiple perspectives.

## Participants
- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[Performance Engineer](../engineering/performance-engineer.md)** - Algorithms, hot paths, profiling
- **[Backend Engineer](../domain_specific/backend-engineer.md)** - Database queries, caching, async patterns
- **[Frontend Engineer](../domain_specific/frontend-engineer.md)** - Rendering, bundle size, perceived performance
- **[Infrastructure Engineer](../operations_reliability/infrastructure-engineer.md)** - Resource allocation, scaling limits
- **[SRE](../operations_reliability/sre.md)** - Production metrics, capacity planning

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Review performance requirements and SLOs
3. Analyze current metrics and bottlenecks
4. Each participant identifies issues from their perspective
5. Prioritize by user impact
6. Present findings using the [severity scale](../_shared/severity-scale.md)
7. Define measurement strategy

## Output Format
### Per Participant
- Perspective name
- Bottlenecks identified
- Optimization opportunities
- Measurement recommendations

### Consolidated
- Critical performance issues
- Quick wins
- Longer-term optimizations
- Capacity risks
- Performance testing recommendations

## Constraints
- Measure before optimizing
- Focus on user-perceived performance
- Consider cost of optimization
- Require benchmarks for changes

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
