# Panel: Launch Readiness Review

## Purpose

Assess whether a system is ready for production deployment, covering operational readiness, release safety, rollback capability, and ongoing operability.

## Participants

- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[SRE](../operations_reliability/sre.md)** - SLOs, runbooks, on-call readiness, SLO impact
- **[Infrastructure Engineer](../operations_reliability/infrastructure-engineer.md)** - Deployment, security, networking
- **[Observability Engineer](../operations_reliability/observability-engineer.md)** - Logging, metrics, alerting
- **[Failure Engineer](../operations_reliability/failure-engineer.md)** - Recovery, rollback, graceful degradation
- **[DevOps Engineer](../operations_reliability/devops-engineer.md)** - CI/CD pipeline health, artifact management, environments
- **[Release Engineer](../process_people/release-engineer.md)** - Release process, feature flags, rollback procedures, changelog
- **[Test Engineer](../engineering/test-engineer.md)** - Test coverage, regression risk, release validation
- **[Tech Lead](../process_people/tech-lead.md)** - Scope validation, risk assessment, stakeholder communication

## Process

1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Review deployment architecture and release scope
3. Each participant assesses readiness from their perspective
4. Identify gaps in observability, recovery, and release safety
5. Verify rollback procedures and feature flag configuration
6. Evaluate incident response capability
7. Present findings using the [severity scale](../_shared/severity-scale.md)
8. Determine launch blockers vs. accepted risks vs. post-launch follow-ups

## Output Format

### Per Participant

- Perspective name
- Readiness gaps
- Risk level
- Required actions before launch

### Consolidated

- Launch blockers (must fix before ship)
- Launch risks (accepted with mitigation plan)
- Post-launch requirements
- Rollback verification status
- Operational runbook status
- Monitoring and alerting readiness
- Go/No-Go recommendation

## Constraints

- Ensure rollback capability exists and has been tested
- Verify alerting covers critical paths
- Require runbooks for known failure modes
- Ensure feature flags are configured for gradual rollout
- Validate that monitoring covers new functionality
- Confirm changelog accurately reflects all changes
- Document accepted risks explicitly

## Conflict Resolution

When participants produce conflicting recommendations:

1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
