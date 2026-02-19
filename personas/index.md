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

### Future Directions

Planned evolution paths based on industry trends:

- **Machine-readable metadata** — YAML frontmatter on persona
  files for automated indexing, selection, and validation
- **Trigger-based activation** — File pattern and keyword
  triggers for automatic persona/panel recommendation
- **Phased panel processes** — Multi-phase review where Phase 1
  findings inform Phase 2 specialist routing
- **Confidence scores** — Per-finding confidence levels to
  improve panel consolidation signal-to-noise
- **Finding deduplication** — Explicit protocol for merging
  semantically overlapping findings across panel participants
- **Persona composability** — Mixin patterns to combine
  evaluation criteria from multiple personas (e.g.,
  security-aware code review)
- **Output schema validation** — JSON Schema definitions for
  persona output formats enabling automated quality checks
- **Effectiveness benchmarks** — Sample inputs with expected
  outputs to measure and compare persona quality over time
- **Agent delegation** — Allow panel participants to request
  specialist input from other personas mid-review (inspired
  by CrewAI task delegation and OpenAI Swarm handoffs)

### External Sources

Resources consulted during persona and panel development.

**LLM and AI Integration:**

- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
  — System prompt design, instruction ordering, and behavioral
  steering patterns. Informed LLM Analyst and LLM Engineer.
- [OpenAI Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)
  — Tactics for clear instructions, reference text, and
  structured output. Informed prompt template evaluation
  criteria.
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
  — MCP server architecture, tool definitions, and JSON schema
  contracts. Foundational for LLM Engineer evaluation criteria.
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
  — Copilot configuration, instruction files, and extensions.
  Informed AI Governance panel and LLM Analyst.
- [Cursor Rules Documentation](https://docs.cursor.com/context/rules-for-ai)
  — `.cursorrules` format and project-level AI instruction
  patterns. Informed cross-surface duplication analysis.
- [Microsoft Responsible AI Standard](https://www.microsoft.com/en-us/ai/responsible-ai)
  — Fairness, reliability, safety, privacy, inclusiveness,
  transparency, and accountability principles. Informed AI
  Governance panel constraints.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
  — Prompt injection, insecure output handling, and model
  denial of service. Informed Security Auditor's AI-specific
  evaluation criteria.

**Site Reliability and Operations:**

- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
  — SLOs, SLIs, error budgets, toil reduction, on-call
  practices. Foundational for SRE persona.
- [Google SRE Workbook](https://sre.google/workbook/table-of-contents/)
  — Practical implementation of SRE principles. Informed
  Launch Readiness and Incident Post-Mortem panels.
- [Principles of Chaos Engineering](https://principlesofchaos.org/)
  — Steady-state hypotheses, fault injection, and abort
  criteria. Foundational for Failure Engineer.
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
  — Distributed tracing, metrics, and logging standards.
  Informed Observability Engineer evaluation criteria.

**Security and Threat Modeling:**

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
  — Adversary tactics and techniques knowledge base. Core
  to Red/Blue/Purple Team and MITRE Analyst personas.
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
  — Web application security testing methodology. Informed
  Security Auditor evaluation criteria.
- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
  — STRIDE, attack trees, and data flow diagram methodology.
  Informed Threat Modeling Review panel.
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
  — Identify, Protect, Detect, Respond, Recover functions.
  Informed Compliance Officer and security-related panels.
- [OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/)
  — Open-source project security criteria and scorecard.
  Informed Supply Chain Engineer.
- [SLSA Framework](https://slsa.dev/)
  — Supply-chain integrity levels and build attestation.
  Informed Supply Chain Engineer.

**Compliance and Privacy:**

- [GDPR Official Text](https://gdpr-info.eu/)
  — EU data protection regulation articles. Informed Privacy
  Engineer and Compliance Officer.
- [WCAG 2.1 Specification](https://www.w3.org/TR/WCAG21/)
  — Web content accessibility guidelines. Informed
  Accessibility Engineer.
- [SOC 2 Trust Service Criteria](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2)
  — Security, availability, processing integrity, and
  confidentiality controls. Informed Compliance Officer.

**Testing and Code Quality:**

- [Mutation Testing Literature](https://pitest.org/quickstart/mutators/)
  — Mutation operator design and adequacy metrics. Informed
  Test Engineer mutation testing criteria.
- [Property-Based Testing (Hypothesis)](https://hypothesis.readthedocs.io/)
  — Generative test strategies and shrinking. Informed Test
  Engineer evaluation criteria.
- [Chaos Toolkit Documentation](https://chaostoolkit.org/)
  — Experiment definition, probes, actions, and rollback.
  Informed Failure Engineer toolchain.

**Architecture and API Design:**

- [Spectral (Stoplight) Documentation](https://stoplight.io/open-source/spectral)
  — OpenAPI linting rules and custom rulesets. Informed
  API Designer toolchain.
- [Architecture Decision Records](https://adr.github.io/)
  — Lightweight decision documentation format. Informed
  Tech Lead persona.
- [The Twelve-Factor App](https://12factor.net/)
  — Cloud-native application design principles. Informed
  Backend Engineer and DevOps Engineer evaluation criteria.
- [C4 Model](https://c4model.com/)
  — Software architecture visualization at four
  abstraction levels (Context, Container, Component,
  Code). Referenced by Architect and Systems Architect
  for diagram standards.
- [Pact Contract Testing](https://pact.io/)
  — Consumer-driven contract testing framework.
  Referenced by API Designer and Test Engineer for
  contract verification criteria.

**Multi-Agent Frameworks:**

- [CrewAI Documentation](https://docs.crewai.com/)
  — Multi-agent orchestration with role/goal/backstory
  patterns and task delegation. Primary reference for
  multi-persona review patterns.
- [Microsoft AutoGen](https://microsoft.github.io/autogen/)
  — Multi-agent conversation patterns with group chat
  and dynamic speaker selection. Informed panel
  moderation and routing patterns.
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
  — State graph agent orchestration with checkpointing
  and human-in-the-loop. Alternative architecture for
  phased panel processes.
- [PydanticAI Documentation](https://ai.pydantic.dev/)
  — Typed agent output with structured validation.
  Reference for output format standardization.
- [Fabric Patterns](https://github.com/danielmiessler/fabric)
  — Community library of reusable AI analysis patterns.
  Complementary task-oriented approach to role-oriented
  personas.
- [OpenAI Swarm](https://github.com/openai/swarm)
  — Lightweight agent handoff patterns for multi-agent
  delegation workflows.

**AI Governance and Risk:**

- [NIST AI Risk Management Framework](https://www.nist.gov/artificial-intelligence/ai-risk-management-framework)
  — Federal AI risk governance standard. Foundational
  for AI Governance panel risk assessment criteria.
- [EU AI Act](https://artificialintelligenceact.eu/)
  — EU regulation on AI system classification, risk
  levels, and compliance requirements. Relevant to
  Compliance Officer for AI-integrated systems.
- [ISO/IEC 42001](https://www.iso.org/standard/81230.html)
  — AI management system standard for organizational
  AI governance. Informed AI Governance panel structure.
- [OWASP AI Security and Privacy Guide](https://owasp.org/www-project-ai-security-and-privacy-guide/)
  — Comprehensive AI security lifecycle beyond
  LLM-specific risks. Extends Security Auditor AI
  evaluation criteria.

**Engineering Metrics and Practices:**

- [DORA Metrics](https://dora.dev/)
  — Deployment frequency, lead time, MTTR, and change
  failure rate. Informed DevOps Engineer, Release
  Engineer, and SRE evaluation criteria.
- [FinOps Foundation](https://www.finops.org/)
  — Cloud financial operations framework. Foundational
  for Cost Optimizer persona.
- [Team Topologies](https://teamtopologies.com/)
  — Team interaction patterns and cognitive load
  management. Informed Platform Engineer and Tech Lead
  organizational awareness criteria.

**Software Supply Chain:**

- [OpenSSF GUAC](https://guac.sh/)
  — Graph for Understanding Artifact Composition.
  Emerging supply chain visibility tool for Supply
  Chain Engineer.
- [in-toto Framework](https://in-toto.io/)
  — Software supply chain layout and verification.
  Complements SLSA for Supply Chain Engineer.
