# Panel: Release Review

## Purpose
Evaluate release readiness, deployment safety, and rollback capability before shipping to production.

## Participants
- **[Release Engineer](../process_people/release-engineer.md)** - Release process, feature flags, rollback procedures, changelog
- **[SRE](../operations_reliability/sre.md)** - SLO impact, operational readiness, monitoring coverage
- **[Test Engineer](../engineering/test-engineer.md)** - Test coverage, regression risk, release validation
- **[DevOps Engineer](../operations_reliability/devops-engineer.md)** - CI/CD pipeline health, deployment automation, artifact integrity
- **[Tech Lead](../process_people/tech-lead.md)** - Scope validation, risk assessment, stakeholder communication

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Review release scope and changelog
3. Each participant evaluates readiness from their perspective
4. Verify rollback procedures and feature flag configuration
5. Present findings using the [severity scale](../_shared/severity-scale.md)
6. Determine release blockers vs. accepted risks

## Output Format
### Per Participant
- Perspective name
- Readiness concerns
- Risk level
- Required actions before release

### Consolidated
- Release blockers (must fix before ship)
- Accepted risks (with mitigation plan)
- Rollback verification status
- Monitoring and alerting readiness
- Go/No-Go recommendation

## Constraints
- Verify rollback has been tested, not just documented
- Ensure feature flags are configured for gradual rollout
- Validate that monitoring covers new functionality
- Confirm changelog accurately reflects all changes

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
