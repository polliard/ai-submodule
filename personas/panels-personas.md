# Panels Overview

Multi-persona collaborative reviews for comprehensive evaluation. Each panel brings together specialists with different perspectives to surface issues a single reviewer might miss.

## When to Use Panels

- **Before launch** — Production Readiness, Security Review, Release Review
- **Design phase** — Architecture Review, API Design Review, Data Design Review
- **Ongoing maintenance** — Code Review, Technical Debt Review, Cost Review
- **After incidents** — Incident Post-Mortem
- **System changes** — Migration Review, Testing Review
- **Documentation updates** — Documentation Review
- **Business alignment** — Business Analysis Panel
- **Security assessments** — Adversarial Security Panel, Penetration Testing
- **Accessibility** — Accessibility Review
- **ML/AI systems** — ML/AI System Review
- **Privacy & compliance** — Privacy Review, Supply Chain Review
- **Developer productivity** — Developer Experience Review

---

## Code Review

**Purpose**: Comprehensive evaluation of code changes from quality, security, performance, and maintainability perspectives.

**When to use**: Pull requests for critical paths, new features, or complex refactors.

**What you get**: Consolidated assessment with must-fix, should-fix, and consider items. Clear approve/reject recommendation with reasoning.

---

## Architecture Review

**Purpose**: Evaluate system design decisions for scalability, resilience, security, and operational concerns.

**When to use**: New services, major refactors, infrastructure changes, or when design decisions have long-term implications.

**What you get**: Go/no-go recommendation with identified risks, required modifications, and documented tradeoffs.

---

## Security Review

**Purpose**: Identify vulnerabilities, attack surfaces, and compliance gaps from multiple security perspectives.

**When to use**: Before exposing new endpoints, handling sensitive data, or integrating third-party services.

**What you get**: Threat assessment with prioritized remediation steps and compliance checklist.

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

## Production Readiness

**Purpose**: Verify a system is ready for production deployment and ongoing operation.

**When to use**: Before initial launch or major feature releases.

**What you get**: Launch checklist with SLO definitions, monitoring requirements, runbooks, and rollback procedures.

---

## API Design Review

**Purpose**: Evaluate API contracts from provider and consumer perspectives for usability, compatibility, and security.

**When to use**: Designing new APIs, versioning existing APIs, or exposing internal services externally.

**What you get**: API contract assessment with consumer friction points, compatibility analysis, and improvement recommendations.

---

## Data Design Review

**Purpose**: Evaluate data models, storage choices, and data flow for correctness, performance, and compliance.

**When to use**: New databases, schema changes, data migrations, or when handling regulated data.

**What you get**: Schema assessment, indexing recommendations, migration strategy, and compliance verification.

---

## Documentation Review

**Purpose**: Evaluate documentation quality from author and consumer perspectives.

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

## Adversarial Security Panel

**Purpose**: Attack-defense simulation from red, blue, and purple team perspectives.

**When to use**: Security assessments, penetration testing preparation, or defense validation.

**What you get**: Attack paths, detection gaps, defense recommendations, and TTP coverage analysis.

---

## Business Analysis Panel

**Purpose**: Align technical solutions with business requirements and stakeholder needs.

**When to use**: New projects, feature planning, or when business and technical teams need alignment.

**What you get**: Requirements validation, gap analysis, acceptance criteria, and stakeholder communication plan.

---

## Penetration Testing

**Purpose**: Structured penetration test engagement simulating real-world attack methodology from reconnaissance through exploitation.

**When to use**: Pre-launch security validation, periodic security assessments, after significant infrastructure or application changes, or compliance-driven testing requirements.

**What you get**: Attack path narratives, vulnerability inventory by severity, exploitation proof-of-concepts, prioritized remediation roadmap, and compliance impact assessment.

---

## Accessibility Review

**Purpose**: Evaluate accessibility compliance, inclusive design, and assistive technology compatibility.

**When to use**: Before launch for user-facing features, when adding new UI components, or for periodic accessibility audits.

**What you get**: WCAG conformance assessment, assistive technology compatibility report, and prioritized remediation plan.

---

## Cost Review

**Purpose**: Analyze infrastructure costs, resource efficiency, and cloud spending optimization opportunities.

**When to use**: Before scaling, during budget planning, or when cloud bills increase unexpectedly.

**What you get**: Savings opportunities, right-sizing recommendations, cost vs. reliability tradeoff analysis, and governance practices.

---

## Dependency & Supply Chain Review

**Purpose**: Evaluate software supply chain security, dependency health, and build pipeline integrity.

**When to use**: Before releases, after dependency updates, or when establishing supply chain security practices.

**What you get**: Dependency audit, SBOM coverage assessment, license compliance report, and supply chain risk scorecard.

---

## ML/AI System Review

**Purpose**: Evaluate ML system design, model lifecycle management, and operational readiness for AI workloads.

**When to use**: Before deploying ML models to production, when establishing MLOps practices, or after model performance degradation.

**What you get**: Model lifecycle gap analysis, data quality assessment, serving infrastructure review, and MLOps maturity evaluation.

---

## Developer Experience Review

**Purpose**: Evaluate developer-facing tools, APIs, documentation, and workflows for usability and productivity.

**When to use**: When onboarding is slow, developer satisfaction is low, or launching new developer-facing APIs or SDKs.

**What you get**: Friction point inventory, onboarding gap analysis, tooling improvement recommendations, and DX satisfaction assessment.

---

## Privacy Review

**Purpose**: Evaluate data privacy practices, PII handling, and regulatory compliance across the application stack.

**When to use**: Before handling new PII categories, when expanding to new jurisdictions, or for periodic privacy assessments.

**What you get**: PII inventory, consent mechanism assessment, regulatory risk analysis, and privacy improvement roadmap.

---

## Release Review

**Purpose**: Evaluate release readiness, deployment safety, and rollback capability before shipping to production.

**When to use**: Before production releases, especially for major features or breaking changes.

**What you get**: Release readiness checklist, rollback verification, monitoring readiness assessment, and go/no-go recommendation.
