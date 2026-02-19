# Personas Index

Quick reference for all available personas and when to use them.

## Code Quality

| Persona | File | Use When |
| --- | --- | --- |
| Code Reviewer | `code_quality/code-reviewer.md` | Correctness, security, concurrency, failure modes |
| Adversarial Reviewer | `code_quality/adversarial-reviewer.md` | Hidden assumptions, invariants, corruption paths |

## Architecture

| Persona | File | Use When |
| --- | --- | --- |
| Architect | `architecture/architect.md` | Components, boundaries, data flow |
| API Designer | `architecture/api-designer.md` | REST/API contracts, versioning, compatibility |
| Systems Architect | `architecture/systems-architect.md` | Scalability, failure domains, state management |

## Engineering

| Persona | File | Use When |
| --- | --- | --- |
| Test Engineer | `engineering/test-engineer.md` | Coverage gaps, flaky tests, mock quality |
| Performance Engineer | `engineering/performance-engineer.md` | Hot paths, allocations, bottlenecks |
| Debugger | `engineering/debugger.md` | Root cause analysis, hypothesis testing |
| Minimalist Engineer | `engineering/minimalist-engineer.md` | Unnecessary abstraction, framework overuse |
| UX Engineer | `engineering/ux-engineer.md` | Ergonomics, configuration, error messages |
| Refactor Specialist | `engineering/refactor-specialist.md` | Incremental migration, responsibility cleanup |

## Operations and Reliability

| Persona | File | Use When |
| --- | --- | --- |
| SRE | `operations_reliability/sre.md` | SLOs, error budgets, toil reduction |
| DevOps Engineer | `operations_reliability/devops-engineer.md` | Build/deploy pipelines, reproducibility |
| Infra Engineer | `operations_reliability/infrastructure-engineer.md` | IAM, network segmentation, TLS |
| Observability Eng | `operations_reliability/observability-engineer.md` | Logging, metrics, tracing, alerting |
| Failure Engineer | `operations_reliability/failure-engineer.md` | Retry storms, partial failures, recovery |
| Cost Optimizer | `operations_reliability/cost-optimizer.md` | Right-sizing, reserved capacity, tiers |
| Platform Engineer | `operations_reliability/platform-engineer.md` | CI/CD abstractions, self-service tooling |
| DBA | `operations_reliability/dba.md` | Replication, backup/restore, query tuning |

## Domain Specific

| Persona | File | Use When |
| --- | --- | --- |
| Frontend Engineer | `domain_specific/frontend-engineer.md` | Components, state, bundle size, rendering |
| Backend Engineer | `domain_specific/backend-engineer.md` | API patterns, caching, service boundaries |
| Data Architect | `domain_specific/data-architect.md` | Schema evolution, indexing, migrations |
| ML Engineer | `domain_specific/ml-engineer.md` | Training pipelines, model versioning, drift |
| Mobile Engineer | `domain_specific/mobile-engineer.md` | Platform conventions, offline-first, battery |
| Data Engineer | `domain_specific/data-engineer.md` | ETL/ELT, data quality, lineage |
| LLM Analyst | `domain_specific/llm-analyst.md` | Instruction quality, model selection, tokens |
| LLM Engineer | `domain_specific/llm-engineer.md` | MCP configs, prompt pipelines, agent safety |

## Compliance and Governance

| Persona | File | Use When |
| --- | --- | --- |
| Security Auditor | `compliance_governance/security-auditor.md` | Injection, auth, secrets, insecure defaults |
| Compliance Officer | `compliance_governance/compliance-officer.md` | GDPR, SOC2, HIPAA, PCI-DSS, audit readiness |
| Accessibility Eng | `compliance_governance/accessibility-engineer.md` | WCAG, screen readers, keyboard navigation |
| Red Team Engineer | `compliance_governance/red-team-engineer.md` | Attack paths, exploitation, kill chain |
| Blue Team Engineer | `compliance_governance/blue-team-engineer.md` | Detection coverage, response, hardening |
| Purple Team Eng | `compliance_governance/purple-team-engineer.md` | Attack-defense alignment, TTP mapping |
| Supply Chain Eng | `compliance_governance/supply-chain-engineer.md` | SBOM, dependency provenance, attestation |
| Privacy Engineer | `compliance_governance/privacy-engineer.md` | PII detection, data minimization, GDPR/CCPA |
| MITRE Analyst | `compliance_governance/mitre-analyst.md` | STRIDE, ATT&CK mapping, threat profiling |

## Process and People

| Persona | File | Use When |
| --- | --- | --- |
| Tech Lead | `process_people/tech-lead.md` | Decisions, knowledge distribution |
| Product Manager | `process_people/product-manager.md` | Acceptance criteria, scope, success metrics |
| Mentor | `process_people/mentor.md` | Concept explanation, guided examples |
| Interviewer | `process_people/interviewer.md` | Skill assessment, evidence-based evaluation |
| Business Analyst | `process_people/business-analyst.md` | Requirements, process mapping, gap analysis |
| Release Engineer | `process_people/release-engineer.md` | Feature flags, rollback, changelog |
| Moderator | `process_people/moderator.md` | Turn order, severity, conflict resolution |

## Special Purpose

| Persona | File | Use When |
| --- | --- | --- |
| Code Archaeologist | `special_purpose/code-archaeologist.md` | Historical context, hidden dependencies |
| Incident Commander | `special_purpose/incident-commander.md` | Impact assessment, coordination |
| Migration Specialist | `special_purpose/migration-specialist.md` | Data integrity, rollback, parallel running |
| API Consumer | `special_purpose/api-consumer.md` | Consumer perspective, DX friction |

## Documentation

| Persona | File | Use When |
| --- | --- | --- |
| Doc Reviewer | `documentation/documentation-reviewer.md` | Accuracy, completeness, structure |
| Doc Writer | `documentation/documentation-writer.md` | Clarity, examples, task orientation |

## Panels

Multi-perspective reviews where several personas collaborate.
Every panel includes a Moderator for process facilitation.
See `panels/` for details and `panels-personas.md` for
human-readable descriptions.

| Panel | File | Participants |
| --- | --- | --- |
| Code Review | `panels/code-review.md` | Code Reviewer, Security, Perf, Test, Refactor |
| Architecture | `panels/architecture-review.md` | Systems Arch, Data Arch, Security, Failure, Infra, API, Perf |
| Security | `panels/security-review.md` | Red/Blue/Purple Team, Security, Adversarial, Infra, Compliance |
| Performance | `panels/performance-review.md` | Perf Eng, Backend, Frontend, Infra, SRE |
| Testing | `panels/testing-review.md` | Test Eng, Failure Eng, Perf Eng, Security, Code Reviewer |
| Documentation | `panels/documentation-review.md` | Doc Reviewer, Doc Writer, API Consumer, Mentor, UX |
| Tech Debt | `panels/technical-debt-review.md` | Refactor, Systems Arch, Test, Tech Lead, Minimalist |
| Migration | `panels/migration-review.md` | Migration Specialist, Data Arch, SRE, Failure, Tech Lead |
| Post-Mortem | `panels/incident-post-mortem.md` | Incident Cmdr, SRE, Systems Arch, Failure, Observability |
| Launch Readiness | `panels/launch-readiness-review.md` | SRE, Infra, Observability, Failure, DevOps, Release, Test |
| API Review | `panels/api-review.md` | API Designer, API Consumer, UX, Frontend, Backend, Doc Reviewer |
| Compliance | `panels/compliance-review.md` | Privacy, Supply Chain, Accessibility, Compliance, Security |
| Threat Modeling | `panels/threat-modeling-review.md` | MITRE, Systems Arch, Red/Blue/Purple, Infra, Security |
| AI Governance | `panels/ai-governance-review.md` | LLM Analyst, LLM Engineer, Doc Reviewer, Security, UX |
