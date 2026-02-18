# Personas Index

Quick reference for all available personas and when to use them.

## Code Quality

| Persona              | File                                   | Use When                                                                    |
| -------------------- | -------------------------------------- | --------------------------------------------------------------------------- |
| Code Reviewer        | `code_quality/code-reviewer.md`        | Production-level review — correctness, security, concurrency, failure modes |
| Adversarial Reviewer | `code_quality/adversarial-reviewer.md` | Stress-testing a design — hidden assumptions, invariants, corruption paths  |

## Architecture

| Persona           | File                                | Use When                                                                  |
| ----------------- | ----------------------------------- | ------------------------------------------------------------------------- |
| Architect         | `architecture/architect.md`         | System design evaluation — components, boundaries, data flow              |
| API Designer      | `architecture/api-designer.md`      | REST/API contract review — versioning, compatibility, consumer experience |
| Systems Architect | `architecture/systems-architect.md` | Distributed systems — scalability, failure domains, state management      |

## Engineering

| Persona              | File                                  | Use When                                                          |
| -------------------- | ------------------------------------- | ----------------------------------------------------------------- |
| Test Engineer        | `engineering/test-engineer.md`        | Test strategy — coverage gaps, flaky tests, mock quality          |
| Performance Engineer | `engineering/performance-engineer.md` | Performance analysis — hot paths, allocations, bottlenecks        |
| Debugger             | `engineering/debugger.md`             | Root cause analysis — systematic isolation, hypothesis testing    |
| Minimalist Engineer  | `engineering/minimalist-engineer.md`  | Complexity reduction — unnecessary abstraction, framework overuse |
| UX Engineer          | `engineering/ux-engineer.md`          | Developer experience — ergonomics, configuration, error messages  |
| Refactor Specialist  | `engineering/refactor-specialist.md`  | Restructuring — incremental migration, responsibility cleanup     |

## Operations & Reliability

| Persona                 | File                                                | Use When                                                       |
| ----------------------- | --------------------------------------------------- | -------------------------------------------------------------- |
| SRE                     | `operations_reliability/sre.md`                     | Production stability — SLOs, error budgets, toil reduction     |
| DevOps Engineer         | `operations_reliability/devops-engineer.md`         | Build/deploy pipelines — reproducibility, artifact management  |
| Infrastructure Engineer | `operations_reliability/infrastructure-engineer.md` | Infrastructure security — IAM, network segmentation, TLS       |
| Observability Engineer  | `operations_reliability/observability-engineer.md`  | Monitoring — logging, metrics, tracing, alerting               |
| Failure Engineer        | `operations_reliability/failure-engineer.md`        | Failure modes — retry storms, partial failures, recovery paths |
| Cost Optimizer          | `operations_reliability/cost-optimizer.md`          | Cloud spend — right-sizing, reserved capacity, storage tiers   |
| Platform Engineer       | `operations_reliability/platform-engineer.md`       | Internal developer platforms — CI/CD abstractions, self-service tooling  |
| DBA                     | `operations_reliability/dba.md`                     | Database operations — replication, backup/restore, query tuning          |

## Domain Specific

| Persona           | File                                   | Use When                                                         |
| ----------------- | -------------------------------------- | ---------------------------------------------------------------- |
| Frontend Engineer | `domain_specific/frontend-engineer.md` | Client-side — components, state, bundle size, rendering          |
| Backend Engineer  | `domain_specific/backend-engineer.md`  | Server-side — API patterns, caching, service boundaries          |
| Data Architect    | `domain_specific/data-architect.md`    | Data layer — schema evolution, indexing, migrations              |
| ML Engineer       | `domain_specific/ml-engineer.md`       | Machine learning — training pipelines, model versioning, drift   |
| Mobile Engineer   | `domain_specific/mobile-engineer.md`   | Mobile — platform conventions, offline-first, battery efficiency |
| Data Engineer       | `domain_specific/data-engineer.md`       | Data pipelines — ETL/ELT, data quality, lineage, orchestration          |

## Compliance & Governance

| Persona                | File                                              | Use When                                                                           |
| ---------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Security Auditor       | `compliance_governance/security-auditor.md`       | Security assessment — injection, auth, secrets, insecure defaults                  |
| Compliance Officer     | `compliance_governance/compliance-officer.md`     | Regulatory — GDPR, SOC2, HIPAA, PCI-DSS, audit readiness                           |
| Accessibility Engineer | `compliance_governance/accessibility-engineer.md` | Accessibility — WCAG, screen readers, keyboard navigation                          |
| Red Team Engineer      | `compliance_governance/red-team-engineer.md`      | Offensive security — attack paths, exploitation chains, kill chain analysis        |
| Blue Team Engineer     | `compliance_governance/blue-team-engineer.md`     | Defensive security — detection coverage, response readiness, hardening             |
| Purple Team Engineer   | `compliance_governance/purple-team-engineer.md`   | Collaborative security — attack-defense alignment, TTP mapping, posture validation |
| Supply Chain Engineer  | `compliance_governance/supply-chain-engineer.md`  | Supply chain security — SBOM, dependency provenance, build attestation            |
| Privacy Engineer       | `compliance_governance/privacy-engineer.md`       | Data privacy — PII detection, data minimization, GDPR/CCPA compliance              |

## Process & People

| Persona          | File                                 | Use When                                                                                           |
| ---------------- | ------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Tech Lead        | `process_people/tech-lead.md`        | Technical leadership — decisions, knowledge distribution, coordination                             |
| Product Manager  | `process_people/product-manager.md`  | Requirements — acceptance criteria, scope, success metrics                                         |
| Mentor           | `process_people/mentor.md`           | Teaching — concept explanation, guided examples, learning progression                              |
| Interviewer      | `process_people/interviewer.md`      | Hiring — skill assessment, evidence-based evaluation                                               |
| Business Analyst | `process_people/business-analyst.md` | Business analysis — requirements elicitation, process mapping, gap analysis, stakeholder alignment |
| Release Engineer     | `process_people/release-engineer.md`     | Release management — feature flags, rollback procedures, changelog                 |

## Special Purpose

| Persona              | File                                      | Use When                                                                   |
| -------------------- | ----------------------------------------- | -------------------------------------------------------------------------- |
| Code Archaeologist   | `special_purpose/code-archaeologist.md`   | Legacy systems — historical context, tribal knowledge, hidden dependencies |
| Incident Commander   | `special_purpose/incident-commander.md`   | Active incidents — impact assessment, coordination, communication          |
| Migration Specialist | `special_purpose/migration-specialist.md` | Data/system migrations — integrity, rollback, parallel running             |
| API Consumer         | `special_purpose/api-consumer.md`         | API evaluation — from the consumer's perspective, DX friction              |

## Documentation

| Persona               | File                                      | Use When                                                                    |
| --------------------- | ----------------------------------------- | --------------------------------------------------------------------------- |
| Documentation Reviewer | `documentation/documentation-reviewer.md` | Documentation accuracy — completeness, structure, correctness               |
| Documentation Writer   | `documentation/documentation-writer.md`   | Documentation authoring — clarity, examples, task orientation               |

## Panels

Multi-perspective reviews where several personas collaborate. See `panels/` for full details and `panels-personas.md` for human-readable descriptions.

| Panel                      | File                                    | Participants                                                                                          |
| -------------------------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Code Review                | `panels/code-review.md`                 | Code Reviewer, Security Auditor, Performance Engineer, Test Engineer, Refactor Specialist             |
| Architecture Review        | `panels/architecture-review.md`         | Systems Architect, Security Auditor, Failure Engineer, Infrastructure Engineer, API Designer          |
| Security Review            | `panels/security-review.md`             | Security Auditor, Infrastructure Engineer, Compliance Officer, Adversarial Reviewer, Backend Engineer |
| Performance Review         | `panels/performance-review.md`          | Performance Engineer, Backend Engineer, Frontend Engineer, Infrastructure Engineer, SRE               |
| Testing Review             | `panels/testing-review.md`              | Test Engineer, Failure Engineer, Performance Engineer, Security Auditor, Code Reviewer                |
| Production Readiness       | `panels/production-readiness-review.md` | SRE, Infrastructure Engineer, Observability Engineer, Failure Engineer, DevOps Engineer               |
| API Design Review          | `panels/api-design-review.md`           | API Designer, API Consumer, Security Auditor, Backend Engineer, Frontend Engineer                     |
| Data Design Review         | `panels/data-design-review.md`          | Data Architect, Backend Engineer, Performance Engineer, Security Auditor, Compliance Officer          |
| Documentation Review       | `panels/documentation-review.md`        | Documentation Reviewer, Documentation Writer, API Consumer, Mentor, UX Engineer                       |
| Technical Debt Review      | `panels/technical-debt-review.md`       | Refactor Specialist, Systems Architect, Test Engineer, Tech Lead, Minimalist Engineer                 |
| Migration Review           | `panels/migration-review.md`            | Migration Specialist, Data Architect, SRE, Failure Engineer, Tech Lead                                |
| Incident Post-Mortem       | `panels/incident-post-mortem.md`        | Incident Commander, SRE, Systems Architect, Failure Engineer, Observability Engineer, Debugger        |
| Adversarial Security Panel | `panels/adversarial-security-panel.md`  | Red Team Engineer, Blue Team Engineer, Purple Team Engineer, Security Auditor, Adversarial Reviewer   |
| Business Analysis Panel    | `panels/ba-business-analyst.md`         | Business Analyst, Product Manager, Tech Lead, Architect, Test Engineer, UX Engineer                   |
| Penetration Testing        | `panels/penetration-testing.md`         | Red Team Engineer, Security Auditor, Infrastructure Engineer, Backend Engineer, Compliance Officer    |
| Accessibility Review           | `panels/accessibility-review.md`           | Accessibility Engineer, Frontend Engineer, UX Engineer, Test Engineer, Documentation Writer        |
| Cost Review                    | `panels/cost-review.md`                    | Cost Optimizer, Infrastructure Engineer, SRE, Systems Architect, DevOps Engineer                   |
| Supply Chain Review            | `panels/supply-chain-review.md`            | Supply Chain Engineer, Security Auditor, Compliance Officer, DevOps Engineer, Backend Engineer     |
| ML/AI System Review            | `panels/ml-system-review.md`               | ML Engineer, Data Engineer, Data Architect, SRE, Security Auditor                                  |
| Developer Experience Review    | `panels/developer-experience-review.md`    | UX Engineer, Documentation Reviewer, API Consumer, Test Engineer, Platform Engineer               |
| Privacy Review                 | `panels/privacy-review.md`                 | Privacy Engineer, Security Auditor, Compliance Officer, Data Architect, Backend Engineer           |
| Release Review                 | `panels/release-review.md`                 | Release Engineer, SRE, Test Engineer, DevOps Engineer, Tech Lead                                   |
