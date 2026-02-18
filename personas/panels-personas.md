# Panels Overview

Multi-persona collaborative reviews for comprehensive evaluation. Each panel brings together specialists with different perspectives to surface issues a single reviewer might miss. Every panel is facilitated by a [Moderator](process_people/moderator.md) who manages turn order, enforces the severity scale, and consolidates findings.

## When to Use Panels

- **Before launch** — Launch Readiness Review
- **Design phase** — Architecture Review, API Review
- **Ongoing maintenance** — Code Review, Technical Debt Review
- **After incidents** — Incident Post-Mortem
- **System changes** — Migration Review, Testing Review
- **Documentation updates** — Documentation Review
- **Security assessments** — Security Review
- **Threat modeling** — Threat Modeling Review
- **Privacy, accessibility & compliance** — Compliance Review
- **Performance concerns** — Performance Review

---

## Code Review

**Purpose**: Comprehensive evaluation of code changes from quality, security, performance, and maintainability perspectives.

**When to use**: Pull requests for critical paths, new features, or complex refactors.

**What you get**: Consolidated assessment with must-fix, should-fix, and consider items. Clear approve/reject recommendation with reasoning.

---

## Architecture Review

**Purpose**: Evaluate system design and data architecture decisions from structural, operational, security, and data-layer perspectives.

**When to use**: New services, major refactors, infrastructure changes, schema changes, data migrations, or when design decisions have long-term implications.

**What you get**: Go/no-go recommendation with identified risks, schema assessment, required modifications, and documented tradeoffs.

---

## Security Review

**Purpose**: Comprehensive security assessment combining vulnerability analysis, adversarial attack simulation, penetration testing methodology, and compliance evaluation from offensive, defensive, and governance perspectives.

**When to use**: Before exposing new endpoints, handling sensitive data, integrating third-party services, security assessments, penetration testing, or defense validation.

**What you get**: Attack path narratives, detection coverage matrix, vulnerability inventory by severity, prioritized remediation roadmap, and security posture assessment.

---

## Performance Review

**Purpose**: Analyze system performance from frontend, backend, and infrastructure perspectives.

**When to use**: Before scaling, after performance regressions, or when optimizing critical paths.

**What you get**: Bottleneck identification, optimization recommendations, and benchmarking strategy.

---

## Testing Review

**Purpose**: Evaluate test strategy, coverage, and quality from multiple testing perspectives.

**When to use**: Before major releases, when test suites are flaky, or establishing testing patterns for new projects.

**What you get**: Coverage gap analysis, test quality assessment, and prioritized testing improvements.

---

## Documentation Review

**Purpose**: Evaluate documentation completeness, accuracy, and usability.

**When to use**: Before publishing docs, onboarding new team members, or when docs are frequently misunderstood.

**What you get**: Documentation gaps, clarity improvements, and structure recommendations.

---

## Technical Debt Review

**Purpose**: Assess accumulated technical debt and prioritize remediation efforts.

**When to use**: Sprint planning, before major features, or when velocity is declining.

**What you get**: Debt inventory with impact analysis, payoff recommendations, and incremental cleanup plan.

---

## Migration Review

**Purpose**: Evaluate migration plans for data integrity, rollback capability, and operational safety.

**When to use**: Database migrations, service replacements, cloud migrations, or major version upgrades.

**What you get**: Migration checklist, rollback procedures, validation strategy, and risk mitigation plan.

---

## Incident Post-Mortem

**Purpose**: Analyze incidents to understand root causes and prevent recurrence.

**When to use**: After production incidents, near-misses, or recurring issues.

**What you get**: Root cause analysis, timeline reconstruction, contributing factors, and actionable remediation items.

---

## Launch Readiness Review

**Purpose**: Assess whether a system is ready for production deployment, covering operational readiness, release safety, rollback capability, and ongoing operability.

**When to use**: Before initial launch, major feature releases, or production deployments with breaking changes.

**What you get**: Launch checklist with SLO definitions, monitoring requirements, runbooks, rollback verification, feature flag configuration, and go/no-go recommendation.

---

## API Review

**Purpose**: Evaluate API design, developer experience, and consumer usability from provider, consumer, and documentation perspectives.

**When to use**: Designing new APIs, versioning existing APIs, exposing internal services externally, or when developer onboarding is slow.

**What you get**: API contract assessment, consumer friction points, documentation gaps, compatibility analysis, and developer satisfaction assessment.

---

## Threat Modeling Review

**Purpose**: Systematic identification, classification, and prioritization of threats using structured methodologies (STRIDE, MITRE ATT&CK, attack trees) combined with architectural analysis and offensive/defensive perspectives.

**When to use**: New system designs, before exposing new attack surfaces, after significant architectural changes, or as a periodic security posture assessment.

**What you get**: Data flow diagrams with trust boundaries, STRIDE threat catalog, MITRE ATT&CK heat map, attack trees, threat actor profiles, detection coverage matrix, and prioritized threat register with mitigation roadmap.

---

## Compliance Review

**Purpose**: Evaluate privacy practices, supply chain security, accessibility compliance, and regulatory posture across the application stack.

**When to use**: Before handling new PII categories, expanding to new jurisdictions, before releases with dependency changes, launching user-facing features, or for periodic compliance audits.

**What you get**: PII inventory, consent mechanism assessment, WCAG conformance gaps, dependency health scorecard, license compliance report, and prioritized remediation roadmap.
