# Threat Model

Generate a comprehensive threat model for an agentic AI system using a **5-round adversarial panel review** methodology.

## Methodology

**STRIDE + MITRE ATT&CK + Attack Trees**, executed through 5 iterative rounds where independent reviewer personas analyze the codebase, challenge each other's findings, and harden the output with each pass.

## Panel Composition

All 5 review tracks run **simultaneously in parallel**. Each track is led by a **Sub-Moderator** who coordinates 1-3 specialist reviewers within that domain. One **Overall Moderator** orchestrates the sub-moderators, performs cross-domain correlation, and produces the final integrated report.

All reviewers analyze the **actual source code** — not abstract descriptions.

### Moderator Hierarchy

| Role                   | Responsibility                                                                                                                                                    |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Overall Moderator**  | Coordinates all 5 sub-moderators; performs cross-domain deduplication, compound attack chain construction, severity arbitration, and final report assembly        |
| **Sub-Moderator (×5)** | Leads one review track; aggregates findings within their domain; escalates cross-cutting concerns to the Overall Moderator; ensures risk validation rules are met |

### Review Tracks (Parallel)

| Track | Sub-Moderator Persona                   | Focus                                                                                                                                    |
| ----- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | **Infrastructure Security Engineer**    | Deployment, containers, Helm, Kubernetes, cloud config, network segmentation, TLS, secrets storage                                       |
| 2     | **Supply Chain Security Specialist**    | Dependencies, CI/CD pipeline integrity, package publishing, version pinning, lockfiles, image provenance                                 |
| 3     | **Application Security Engineer**       | MCP/tool protocol, input validation, injection, caching, authentication, authorization, data access controls                             |
| 4     | **DevSecOps & AI Safety Engineer**      | Workflow security, agentic automation, prompt injection, tool privilege, `--allow-all-tools` flags, token exposure, GITHUB_ENV poisoning |
| 5     | **Data Privacy & Information Security** | GDPR/HIPAA compliance, credential exposure, data leakage paths, PII in results, cross-context contamination                              |

## The 5-Track Parallel Process

### Phase 1: Parallel Independent Analysis (All 5 Tracks Simultaneously)

All 5 tracks execute **at the same time**. Each Sub-Moderator coordinates their reviewers to produce:
- **Threats found** (STRIDE-classified, with severity and likelihood)
- **Specific file and line references** for every finding
- **Concrete attack narratives** — not hypotheticals, but step-by-step exploits you could actually execute
- **Proposed mitigations** with implementation specifics
- **Cross-domain flags** — any finding that touches another track's domain, tagged for the Overall Moderator

Each Sub-Moderator validates findings within their track against the **Risk Validation Rules** before escalating.

### Phase 2: Sub-Moderator Aggregation (Per-Track)

Each Sub-Moderator independently:
1. Deduplicates findings within their track
2. Assigns preliminary severity ratings with justification
3. Identifies findings that span multiple tracks (cross-cutting concerns)
4. Prepares a **track summary** with ranked findings and cross-domain flags
5. Submits their track summary to the Overall Moderator

### Phase 3: Overall Moderator Integration

The **Overall Moderator** receives all 5 track summaries simultaneously and:
1. **Cross-references** all tracks — flags duplicates, contradictions, and coverage gaps
2. **Challenges weak findings** via sub-moderators: "Could an attacker actually exploit this? Under what conditions?"
3. **Escalates convergent findings** where multiple tracks independently identified the same issue
4. **Constructs compound attack chains** — where findings from different tracks combine into multi-stage attacks
5. **Arbitrates severity** — resolves disagreements between tracks using CVSS evidence and attack feasibility
6. **Identifies blind spots** — areas no track addressed, and assigns follow-up to the most relevant sub-moderator

### Phase 4: Hardening Pass (5 Rounds of Iterative Refinement)

The Overall Moderator drives **5 rounds** of cross-track hardening:

| Round | Activity                                                                                                       |
| ----- | -------------------------------------------------------------------------------------------------------------- |
| 1     | Sub-moderators review each other's findings; challenge severity ratings and attack feasibility                 |
| 2     | Sub-moderators test proposed mitigations against findings from other tracks — do they create new gaps?         |
| 3     | Overall Moderator presents compound attack chains; sub-moderators validate or refute from their domain's lens  |
| 4     | Sub-moderators refine mitigations to address cross-domain dependencies; Overall Moderator checks for conflicts |
| 5     | Final validation: every Critical/High finding must have consensus from ≥3 tracks or explicit justification     |

### Phase 5: Final Report Assembly

The Overall Moderator produces the final report by:
- Deduplicating across all 5 tracks with authoritative severity based on cross-track consensus
- Building cross-cutting concern narratives (e.g., "3 of 5 tracks flagged content integrity")
- Constructing compound attack trees from individual findings across tracks
- Ensuring every finding meets Risk Validation Rules (concrete, referenced, reproducible, justified, actionable)
- Including dissenting opinions where sub-moderators disagreed on severity

## Output Requirements

### Template
Use the template at `~/.ai/templates/threat-model.md` as the structural foundation.

### Diagrams
**ALL diagrams MUST use Mermaid syntax.** No ASCII art, no PlantUML, no images.

Required diagrams:
1. **Data Flow Diagram** — `graph LR` with color-coded trust boundary subgraphs
2. **STRIDE Mindmap** — `mindmap` showing all 6 categories with subcategories
3. **Attack Trees** — `graph TD` for each primary attack goal
4. **MITRE ATT&CK Heat Map** — `block-beta` diagram with color-coded technique coverage:
   - 🔴 Red (`fill:#e74c3c`) = GAP — no detection
   - 🟡 Amber (`fill:#f39c12`) = PARTIAL — some detection
   - 🟢 Green (`fill:#27ae60`) = COVERED — validated detection
5. **STRIDE Risk Quadrant** — `quadrantChart` plotting category × severity × likelihood
6. **Mitigation Roadmap** — `gantt` chart with phased remediation timeline
7. **Detection Gap Visualization** — `graph` showing coverage status per capability
8. **Agentic Threat Pattern Tree** — `graph TD` showing the 19 common agentic patterns organized by category

### Risk Validation Rules

Every finding MUST meet these criteria or be rejected:

1. **Concrete, not theoretical** — "An attacker COULD do X" is insufficient. Describe the exact steps, prerequisites, and code paths.
2. **File and line references** — Every vulnerability must cite the specific source file and function. No hand-waving.
3. **Reproducible** — Could a red team engineer execute this attack with the information provided? If not, strengthen it or demote it.
4. **Severity is justified** — CVSS score must match the narrative. A "Critical" finding with a vague attack path gets downgraded.
5. **Mitigations are actionable** — "Improve security" is rejected. Specify the exact code change, configuration, or architectural fix.

### Agentic-Specific Patterns (Evaluate All 19)

| ID   | Pattern                            | Key Question                                                                           |
| ---- | ---------------------------------- | -------------------------------------------------------------------------------------- |
| P-01 | Prompt Injection → Tool Params     | Can crafted input cause the agent to invoke tools with attacker-controlled parameters? |
| P-02 | Indirect Prompt Injection via Data | Can data returned by a tool influence the agent to take unintended actions?            |
| P-03 | Configuration Redirect             | Can a tool call redirect the agent's backend to an attacker-controlled server?         |
| P-04 | Query/API Injection                | Are user-supplied values sanitized before embedding in queries or URLs?                |
| P-05 | No Transport Authentication        | Can any process on the host invoke the tool server without authentication?             |
| P-06 | Unrestricted Tool Access           | Are all tools available to all callers regardless of intent or authorization?          |
| P-07 | Unrestricted Data Scope            | Can the agent access any table/resource, including sensitive system resources?         |
| P-08 | Over-Privileged Tokens             | Do CI/CD tokens or agent credentials have broader scope than needed?                   |
| P-09 | Bulk Data Exfiltration             | Can `fetch_all` or equivalent extract unlimited records with no rate limit?            |
| P-10 | PII Exposure in Results            | Are sensitive fields returned unfiltered to the LLM context?                           |
| P-11 | Cross-Context Leakage              | Can data from one session/user leak into another?                                      |
| P-12 | Credential Persistence             | Are tokens/sessions stored in plaintext at known paths?                                |
| P-13 | Mutable Dependencies               | Are packages, images, and actions pinned to immutable references (SHA, not tags)?      |
| P-14 | Content Integrity                  | Are remotely-fetched prompts/resources hash-validated and fail-closed?                 |
| P-15 | CI/CD Supply Chain                 | Are GitHub Actions pinned to SHA digests? Is the CLI version-pinned?                   |
| P-16 | No Audit Logging                   | Is there a structured log of all tool invocations with params, timestamps, caller?     |
| P-17 | No Rate Limiting                   | Can an attacker exhaust backend resources through unlimited tool calls?                |
| P-18 | Silent Error Swallowing            | Do bare `except:` clauses mask security-relevant failures?                             |
| P-19 | No Kill Switch                     | Is there a mechanism to halt a runaway agent immediately?                              |

### Compliance Frameworks (Evaluate Applicable)

- **SOC 2 Type II** — CC6.1, CC6.3, CC7.1, CC7.2, CC7.3, CC8.1
- **GDPR** — Art. 5 (minimization), Art. 15/17 (access/erasure), Art. 30 (records), Art. 35 (DPIA), Ch. V (transfers)
- **NIST 800-53** — AC, AU, IA, SC, SI, CM control families
- **HIPAA** — §164.312(a)(b)(c) if health data is possible
- **PCI DSS** — Req 3, 7, 10 if cardholder data is possible

### Detection Artifacts

Include in appendices:
- **Sigma detection rules** for sensitive resource access, bulk extraction, credential anomalies
- **Purple team exercises** with ATT&CK technique, procedure, and expected detection
- **Incident response procedures** — session revocation, agent containment, forensic reconstruction

## When to Use

- Before deploying any MCP server, agent tool, or LLM-integrated system
- Before any system that grants an AI agent access to tools, APIs, data sources, or file systems
- When reviewing CI/CD pipelines that invoke AI agents (Copilot CLI, agentic loops)
- After architectural changes to an existing agentic system
- Periodically (quarterly) for deployed agentic systems handling sensitive data
