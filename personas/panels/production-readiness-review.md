# Panel: Production Readiness Review

## Purpose


Assess whether a system is ready for production deployment.


## Participants

- **[SRE](../operations_reliability/sre.md)** - SLOs, runbooks, on-call readiness
- **[Infrastructure Engineer](../operations_reliability/infrastructure-engineer.md)** - Deployment, security, networking
- **[Observability Engineer](../operations_reliability/observability-engineer.md)** - Logging, metrics, alerting
- **[Failure Engineer](../operations_reliability/failure-engineer.md)** - Recovery, rollback, graceful degradation
- **[DevOps Engineer](../operations_reliability/devops-engineer.md)** - CI/CD, artifact management, environments


## Process

1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Review deployment architecture
3. Each participant assesses operational readiness
4. Identify gaps in observability and recovery
5. Evaluate incident response capability
6. Present findings using the [severity scale](../_shared/severity-scale.md)
7. Determine launch blockers vs follow-ups


## Output Format

### Per Participant

- Perspective name

- Readiness gaps
- Risk level
- Required before launch

### Consolidated

- Launch blockers (must fix)

- Launch risks (accepted with mitigation)
- Post-launch requirements
- Operational runbook status
- Go/No-Go recommendation

## Constraints

- Ensure rollback capability exists
- Verify alerting covers critical paths
- Require runbooks for known failure modes
- Document accepted risks explicitly

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
