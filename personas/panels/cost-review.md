# Panel: Cost Review

## Purpose
Evaluate infrastructure costs, resource efficiency, and cloud spending optimization opportunities.

## Participants
- **[Cost Optimizer](../operations_reliability/cost-optimizer.md)** - Cloud spend analysis, right-sizing, reserved capacity
- **[Infrastructure Engineer](../operations_reliability/infrastructure-engineer.md)** - Resource provisioning, scaling policies, networking costs
- **[SRE](../operations_reliability/sre.md)** - Reliability vs. cost tradeoffs, capacity planning
- **[Systems Architect](../architecture/systems-architect.md)** - Architecture-level cost drivers, service decomposition economics
- **[DevOps Engineer](../operations_reliability/devops-engineer.md)** - CI/CD resource usage, environment proliferation, build costs

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Collect current cost data and resource utilization metrics
3. Each participant identifies cost drivers and waste from their perspective
4. Present findings using the [severity scale](../_shared/severity-scale.md)
5. Model cost impact of proposed optimizations
6. Prioritize by savings magnitude and implementation risk

## Output Format
### Per Participant
- Perspective name
- Cost concerns identified
- Estimated waste or over-provisioning
- Optimization recommendations

### Consolidated
- Total identified savings opportunity
- Quick wins (immediate cost reduction, low risk)
- Medium-term optimizations (require architecture or process changes)
- Cost vs. reliability tradeoffs requiring decision
- Recommended cost governance practices
- Monthly cost projection after optimizations

## Constraints
- Never sacrifice reliability for cost savings without explicit approval
- Quantify savings estimates with confidence ranges
- Consider total cost of ownership, not just compute
- Account for cost of implementing optimizations

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
