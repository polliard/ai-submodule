# Personas Index

Quick reference for all available personas and when to use them.

## Code Quality

| Persona              | File                                   | Use When                                          |
| -------------------- | -------------------------------------- | ------------------------------------------------- |
| Code Reviewer        | `code_quality/code-reviewer.md`        | Correctness, security, concurrency, failure modes |
| Adversarial Reviewer | `code_quality/adversarial-reviewer.md` | Hidden assumptions, invariants, corruption paths  |

## Architecture

| Persona           | File                                | Use When                                       |
| ----------------- | ----------------------------------- | ---------------------------------------------- |
| Architect         | `architecture/architect.md`         | Components, boundaries, data flow              |
| API Designer      | `architecture/api-designer.md`      | REST/API contracts, versioning, compatibility  |
| Systems Architect | `architecture/systems-architect.md` | Scalability, failure domains, state management |

## Engineering

| Persona              | File                                  | Use When                                      |
| -------------------- | ------------------------------------- | --------------------------------------------- |
| Test Engineer        | `engineering/test-engineer.md`        | Coverage gaps, flaky tests, mock quality      |
| Performance Engineer | `engineering/performance-engineer.md` | Hot paths, allocations, bottlenecks           |
| Debugger             | `engineering/debugger.md`             | Root cause analysis, hypothesis testing       |
| Minimalist Engineer  | `engineering/minimalist-engineer.md`  | Unnecessary abstraction, framework overuse    |
| UX Engineer          | `engineering/ux-engineer.md`          | Ergonomics, configuration, error messages     |
| Refactor Specialist  | `engineering/refactor-specialist.md`  | Incremental migration, responsibility cleanup |

## Operations and Reliability

| Persona           | File                                                | Use When                                  |
| ----------------- | --------------------------------------------------- | ----------------------------------------- |
| SRE               | `operations_reliability/sre.md`                     | SLOs, error budgets, toil reduction       |
| DevOps Engineer   | `operations_reliability/devops-engineer.md`         | Build/deploy pipelines, reproducibility   |
| Infra Engineer    | `operations_reliability/infrastructure-engineer.md` | IAM, network segmentation, TLS            |
| Observability Eng | `operations_reliability/observability-engineer.md`  | Logging, metrics, tracing, alerting       |
| Failure Engineer  | `operations_reliability/failure-engineer.md`        | Retry storms, partial failures, recovery  |
| Cost Optimizer    | `operations_reliability/cost-optimizer.md`          | Right-sizing, reserved capacity, tiers    |
| Platform Engineer | `operations_reliability/platform-engineer.md`       | CI/CD abstractions, self-service tooling  |
| DBA               | `operations_reliability/dba.md`                     | Replication, backup/restore, query tuning |

## Domain Specific

| Persona           | File                                   | Use When                                     |
| ----------------- | -------------------------------------- | -------------------------------------------- |
| Frontend Engineer | `domain_specific/frontend-engineer.md` | Components, state, bundle size, rendering    |
| Backend Engineer  | `domain_specific/backend-engineer.md`  | API patterns, caching, service boundaries    |
| Data Architect    | `domain_specific/data-architect.md`    | Schema evolution, indexing, migrations       |
| ML Engineer       | `domain_specific/ml-engineer.md`       | Training pipelines, model versioning, drift  |
| Mobile Engineer   | `domain_specific/mobile-engineer.md`   | Platform conventions, offline-first, battery |
| Data Engineer     | `domain_specific/data-engineer.md`     | ETL/ELT, data quality, lineage               |
| LLM Analyst       | `domain_specific/llm-analyst.md`       | Instruction quality, model selection, tokens |
| LLM Engineer      | `domain_specific/llm-engineer.md`      | MCP configs, prompt pipelines, agent safety  |

## Compliance and Governance

| Persona            | File                                              | Use When                                    |
| ------------------ | ------------------------------------------------- | ------------------------------------------- |
| Security Auditor   | `compliance_governance/security-auditor.md`       | Injection, auth, secrets, insecure defaults |
| Compliance Officer | `compliance_governance/compliance-officer.md`     | GDPR, SOC2, HIPAA, PCI-DSS, audit readiness |
| Accessibility Eng  | `compliance_governance/accessibility-engineer.md` | WCAG, screen readers, keyboard navigation   |
| Red Team Engineer  | `compliance_governance/red-team-engineer.md`      | Attack paths, exploitation, kill chain      |
| Blue Team Engineer | `compliance_governance/blue-team-engineer.md`     | Detection coverage, response, hardening     |
| Purple Team Eng    | `compliance_governance/purple-team-engineer.md`   | Attack-defense alignment, TTP mapping       |
| Supply Chain Eng   | `compliance_governance/supply-chain-engineer.md`  | SBOM, dependency provenance, attestation    |
| Privacy Engineer   | `compliance_governance/privacy-engineer.md`       | PII detection, data minimization, GDPR/CCPA |
| MITRE Analyst      | `compliance_governance/mitre-analyst.md`          | STRIDE, ATT&CK mapping, threat profiling    |

## Process and People

| Persona          | File                                 | Use When                                    |
| ---------------- | ------------------------------------ | ------------------------------------------- |
| Tech Lead        | `process_people/tech-lead.md`        | Decisions, knowledge distribution           |
| Product Manager  | `process_people/product-manager.md`  | Acceptance criteria, scope, success metrics |
| Mentor           | `process_people/mentor.md`           | Concept explanation, guided examples        |
| Interviewer      | `process_people/interviewer.md`      | Skill assessment, evidence-based evaluation |
| Business Analyst | `process_people/business-analyst.md` | Requirements, process mapping, gap analysis |
| Release Engineer | `process_people/release-engineer.md` | Feature flags, rollback, changelog          |
| Moderator        | `process_people/moderator.md`        | Turn order, severity, conflict resolution   |

## Special Purpose

| Persona              | File                                      | Use When                                   |
| -------------------- | ----------------------------------------- | ------------------------------------------ |
| Code Archaeologist   | `special_purpose/code-archaeologist.md`   | Historical context, hidden dependencies    |
| Incident Commander   | `special_purpose/incident-commander.md`   | Impact assessment, coordination            |
| Migration Specialist | `special_purpose/migration-specialist.md` | Data integrity, rollback, parallel running |
| API Consumer         | `special_purpose/api-consumer.md`         | Consumer perspective, DX friction          |

## Documentation

| Persona      | File                                      | Use When                            |
| ------------ | ----------------------------------------- | ----------------------------------- |
| Doc Reviewer | `documentation/documentation-reviewer.md` | Accuracy, completeness, structure   |
| Doc Writer   | `documentation/documentation-writer.md`   | Clarity, examples, task orientation |

## Panels

Multi-perspective reviews where several personas collaborate.
Every panel includes a Moderator for process facilitation.
See `panels/` for details and `panels-personas.md` for
human-readable descriptions.

| Panel            | File                                | Participants                                                    |
| ---------------- | ----------------------------------- | --------------------------------------------------------------- |
| Code Review      | `panels/code-review.md`             | Code Reviewer, Security, Perf, Test, Refactor                   |
| Architecture     | `panels/architecture-review.md`     | Systems Arch, Data Arch, Security, Failure, Infra, API, Perf    |
| Security         | `panels/security-review.md`         | Red/Blue/Purple Team, Security, Adversarial, Infra, Compliance  |
| Performance      | `panels/performance-review.md`      | Perf Eng, Backend, Frontend, Infra, SRE                         |
| Testing          | `panels/testing-review.md`          | Test Eng, Failure Eng, Perf Eng, Security, Code Reviewer        |
| Documentation    | `panels/documentation-review.md`    | Doc Reviewer, Doc Writer, API Consumer, Mentor, UX              |
| Tech Debt        | `panels/technical-debt-review.md`   | Refactor, Systems Arch, Test, Tech Lead, Minimalist             |
| Migration        | `panels/migration-review.md`        | Migration Specialist, Data Arch, SRE, Failure, Tech Lead        |
| Post-Mortem      | `panels/incident-post-mortem.md`    | Incident Cmdr, SRE, Systems Arch, Failure, Observability        |
| Launch Readiness | `panels/launch-readiness-review.md` | SRE, Infra, Observability, Failure, DevOps, Release, Test       |
| API Review       | `panels/api-review.md`              | API Designer, API Consumer, UX, Frontend, Backend, Doc Reviewer |
| Compliance       | `panels/compliance-review.md`       | Privacy, Supply Chain, Accessibility, Compliance, Security      |
| Threat Modeling  | `panels/threat-modeling-review.md`  | MITRE, Systems Arch, Red/Blue/Purple, Infra, Security           |
| AI Governance    | `panels/ai-governance-review.md`    | LLM Analyst, LLM Engineer, Doc Reviewer, Security, UX           |

## Resources and References

The personas and panels in this repository draw on the following
industry frameworks, standards, methodologies, and toolchains.

### Security Frameworks

- **MITRE ATT&CK** — Adversary tactics, techniques, and procedures
  (TTP) knowledge base. Used by Red/Blue/Purple Team, MITRE
  Analyst, and Security/Threat Modeling panels.
- **STRIDE / DREAD / PASTA** — Threat modeling methodologies used
  by the MITRE Analyst persona and Threat Modeling Review panel.
- **OWASP Top 10 / ZAP / Threat Dragon** — Web application
  security risks and tooling. Referenced by Security Auditor,
  Security Review panel, and Threat Modeling Review panel.
- **CVSS** (Common Vulnerability Scoring System) — Severity
  scoring for vulnerabilities in security-related panels.
- **Kill Chain / Attack Trees** — Adversary progression models
  used by Red Team Engineer and MITRE Analyst.
- **OpenSSF Scorecard** — Open-source project security health
  scoring. Used by Supply Chain Engineer.
- **SLSA** (Supply-chain Levels for Software Artifacts) — Build
  attestation levels for Supply Chain Engineer.
- **Sigstore / cosign** — Container image signing and
  attestation for supply chain provenance.

### Compliance and Regulatory Standards

- **GDPR** — EU data protection regulation. Referenced by
  Compliance Officer and Privacy Engineer.
- **SOC 2** — Service organization controls for security,
  availability, and confidentiality.
- **HIPAA** — US healthcare data protection. Referenced by
  Compliance Officer and Compliance Review panel.
- **PCI-DSS** — Payment card industry data security standard.
- **CCPA** — California consumer privacy act. Referenced by
  Privacy Engineer.
- **NIST Cybersecurity Framework / OSCAL** — Federal security
  controls and machine-readable assessment language.
- **WCAG 2.1** — Web content accessibility guidelines (levels
  A/AA/AAA). Used by Accessibility Engineer.
- **CIS Benchmarks** — Security configuration baselines used
  by Compliance Officer and Infrastructure Engineer.

### Methodologies

- **Site Reliability Engineering (SRE)** — SLOs/SLIs, error
  budgets, toil reduction, on-call practices. Foundational to
  the SRE persona and Launch Readiness panel. Draws from
  the Google SRE body of work.
- **Chaos Engineering** — Fault injection, blast radius limits,
  abort criteria. Core to the Failure Engineer persona.
  Influenced by Netflix Principles of Chaos Engineering.
- **Adversary Emulation / TTP Mapping** — Purple Team Engineer
  and Red Team Engineer use MITRE Caldera and Atomic Red Team.
- **Defense-in-Depth / Assume-Breach** — Layered security
  strategy used by Blue Team and Infrastructure Engineer.
- **Mutation Testing** — Test adequacy measurement via code
  mutation (mutmut, Stryker). Used by Test Engineer.
- **Property-Based Testing** — Generative test input via
  Hypothesis. Used by Test Engineer.
- **Blameless Post-Mortems** — Focus on systems not individuals.
  Core principle of the Incident Post-Mortem panel.
- **Policy-as-Code** — Compliance automation via OPA and Regula.
  Used by Compliance Officer.
- **Privacy by Design / Data Minimization** — Privacy-first
  architecture principles for Privacy Engineer.
- **Architecture Decision Records (ADRs)** — Lightweight decision
  documentation via adr-tools.

### Design Philosophy

Each persona and panel follows a consistent structural template:

**Persona structure:**

- **Role** — Single-paragraph expert identity with explicit scope
  boundaries distinguishing it from adjacent personas
- **Allowed Tools** — Required and supplementary tools with
  install commands
- **Tool Setup** — Links to the standardized bootstrap procedure
  in `_shared/tool-setup.md`
- **Evaluate For** — Checklist of specific evaluation criteria
  (the "lens" the persona applies)
- **Output Format** — Structured deliverables expected
- **Principles** — 3-4 guiding decision heuristics
- **Anti-patterns** — 3-4 explicit behaviors to avoid

**Panel structure:**

- **Purpose** — One-paragraph scope statement
- **Participants** — 6-9 personas with linked files; always
  includes a Moderator
- **Process** — Numbered steps from "bootstrap tooling" through
  convergence
- **Output Format** — Per-participant findings and consolidated
  assessment
- **Conflict Resolution** — Standard 4-step protocol (present
  positions, identify tradeoff, recommend resolution, escalate)

**Shared infrastructure:**

- `_shared/severity-scale.md` — Canonical 4-level severity scale
  (Critical / High / Medium / Low)
- `_shared/base-tools.md` — 8 shared tools installed once per
  session (jq, Semgrep, k6, cloc, Trivy, Madge, Lighthouse,
  Mermaid CLI)
- `_shared/tool-setup.md` — 5-step bootstrap: Check, Install,
  Verify, Adapt, Report
- `_shared/scope-constraints.md` — Mandatory rules for offensive
  and chaos personas (explicit targets, human approval, rules of
  engagement, non-production default, reversibility, logging)
- `_shared/credential-policy.md` — Secret hygiene rules
- `tools.yaml` — Central registry mapping every tool to install
  commands, categories, and consuming personas
