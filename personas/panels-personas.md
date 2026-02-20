# Panels Overview

Multi-persona collaborative reviews for comprehensive evaluation. Each
panel brings together specialists with different perspectives to surface
issues a single reviewer might miss. Every panel is facilitated by a
[Moderator](process_people/moderator.md) who manages turn order,
enforces the severity scale, and consolidates findings.

## Quick Start

Run `/panels` to see all available panel commands, or invoke a panel
directly:

```text
/code-review-panel src/auth/
/security-panel
/threat-panel path/to/system
```

## When to Use Panels

| Situation | Panel | Command |
| --- | --- | --- |
| Before launch | Launch Readiness Review | `/launch-readiness-panel` |
| Design phase | Architecture Review | `/architecture-panel` |
| Design phase | API Review | `/api-panel` |
| Ongoing maintenance | Code Review | `/code-review-panel` |
| Ongoing maintenance | Technical Debt Review | `/technical-debt-panel` |
| After incidents | Incident Post-Mortem | `/incident-post-mortem-panel` |
| System changes | Migration Review | `/migration-panel` |
| System changes | Testing Review | `/testing-panel` |
| Documentation updates | Documentation Review | `/documentation-panel` |
| Security assessments | Security Review | `/security-panel` |
| Threat modeling | Threat Modeling Review | `/threat-panel` |
| Privacy & compliance | Compliance Review | `/compliance-panel` |
| Performance concerns | Performance Review | `/performance-panel` |
| AI tooling review | AI Governance Review | `/ai-governance-panel` |

---

## Code Review

**Command**: `/code-review-panel`

**Purpose**: Comprehensive evaluation of code changes from quality,
security, performance, and maintainability perspectives.

**When to use**: Pull requests for critical paths, new features, or
complex refactors.

**What you get**: Consolidated assessment with must-fix, should-fix, and
consider items. Clear approve/reject recommendation with reasoning.

---

## Architecture Review

**Command**: `/architecture-panel`

**Purpose**: Evaluate system design and data architecture decisions from
structural, operational, security, and data-layer perspectives.

**When to use**: New services, major refactors, infrastructure changes,
schema changes, data migrations, or when design decisions have long-term
implications.

**What you get**: Go/no-go recommendation with identified risks, schema
assessment, required modifications, and documented tradeoffs.

---

## Security Review

**Command**: `/security-panel`

**Purpose**: Comprehensive security assessment combining vulnerability
analysis, adversarial attack simulation, penetration testing
methodology, and compliance evaluation from offensive, defensive, and
governance perspectives.

**When to use**: Before exposing new endpoints, handling sensitive data,
integrating third-party services, security assessments, penetration
testing, or defense validation.

**What you get**: Attack path narratives, detection coverage matrix,
vulnerability inventory by severity, prioritized remediation roadmap,
and security posture assessment.

---

## Performance Review

**Command**: `/performance-panel`

**Purpose**: Analyze system performance from frontend, backend, and
infrastructure perspectives.

**When to use**: Before scaling, after performance regressions, or when
optimizing critical paths.

**What you get**: Bottleneck identification, optimization
recommendations, and benchmarking strategy.

---

## Testing Review

**Command**: `/testing-panel`

**Purpose**: Evaluate test strategy, coverage, and quality from multiple
testing perspectives.

**When to use**: Before major releases, when test suites are flaky, or
establishing testing patterns for new projects.

**What you get**: Coverage gap analysis, test quality assessment, and
prioritized testing improvements.

---

## Documentation Review

**Command**: `/documentation-panel`

**Purpose**: Evaluate documentation completeness, accuracy, and
usability.

**When to use**: Before publishing docs, onboarding new team members, or
when docs are frequently misunderstood.

**What you get**: Documentation gaps, clarity improvements, and
structure recommendations.

---

## Technical Debt Review

**Command**: `/technical-debt-panel`

**Purpose**: Assess accumulated technical debt and prioritize
remediation efforts.

**When to use**: Sprint planning, before major features, or when
velocity is declining.

**What you get**: Debt inventory with impact analysis, payoff
recommendations, and incremental cleanup plan.

---

## Migration Review

**Command**: `/migration-panel`

**Purpose**: Evaluate migration plans for data integrity, rollback
capability, and operational safety.

**When to use**: Database migrations, service replacements, cloud
migrations, or major version upgrades.

**What you get**: Migration checklist, rollback procedures, validation
strategy, and risk mitigation plan.

---

## Incident Post-Mortem

**Command**: `/incident-post-mortem-panel`

**Purpose**: Analyze incidents to understand root causes and prevent
recurrence.

**When to use**: After production incidents, near-misses, or recurring
issues.

**What you get**: Root cause analysis, timeline reconstruction,
contributing factors, and actionable remediation items.

---

## Launch Readiness Review

**Command**: `/launch-readiness-panel`

**Purpose**: Assess whether a system is ready for production deployment,
covering operational readiness, release safety, rollback capability, and
ongoing operability.

**When to use**: Before initial launch, major feature releases, or
production deployments with breaking changes.

**What you get**: Launch checklist with SLO definitions, monitoring
requirements, runbooks, rollback verification, feature flag
configuration, and go/no-go recommendation.

---

## API Review

**Command**: `/api-panel`

**Purpose**: Evaluate API design, developer experience, and consumer
usability from provider, consumer, and documentation perspectives.

**When to use**: Designing new APIs, versioning existing APIs, exposing
internal services externally, or when developer onboarding is slow.

**What you get**: API contract assessment, consumer friction points,
documentation gaps, compatibility analysis, and developer satisfaction
assessment.

---

## Threat Modeling Review

**Command**: `/threat-panel`

**Purpose**: Systematic identification, classification, and
prioritization of threats using structured methodologies (STRIDE, MITRE
ATT&CK, attack trees) combined with architectural analysis and
offensive/defensive perspectives.

**When to use**: New system designs, before exposing new attack surfaces,
after significant architectural changes, or as a periodic security
posture assessment.

**What you get**: Data flow diagrams with trust boundaries, STRIDE threat
catalog, MITRE ATT&CK heat map, attack trees, threat actor profiles,
detection coverage matrix, and prioritized threat register with
mitigation roadmap.

---

## Compliance Review

**Command**: `/compliance-panel`

**Purpose**: Evaluate privacy practices, supply chain security,
accessibility compliance, and regulatory posture across the application
stack.

**When to use**: Before handling new PII categories, expanding to new
jurisdictions, before releases with dependency changes, launching
user-facing features, or for periodic compliance audits.

**What you get**: PII inventory, consent mechanism assessment, WCAG
conformance gaps, dependency health scorecard, license compliance report,
and prioritized remediation roadmap.

---

## AI Governance Review

**Command**: `/ai-governance-panel`

**Purpose**: Evaluate AI integration quality, instruction file
effectiveness, MCP configuration correctness, and alignment between AI
tooling and project conventions.

**When to use**: Setting up AI workflows, auditing instruction files,
reviewing MCP configurations, or when AI-assisted outputs are
inconsistent.

**What you get**: Instruction quality summary, MCP audit results,
cross-surface drift report, agent safety assessment, and prioritized
improvement roadmap.
