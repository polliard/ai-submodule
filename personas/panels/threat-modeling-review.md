# Panel: Threat Modeling Review

## Purpose

Systematic identification, classification, and prioritization of threats against a system using structured
  methodologies (STRIDE, MITRE ATT&CK, attack trees). Combines architectural analysis with offensive, defensive, and
  intelligence perspectives to produce a prioritized threat register and actionable mitigation roadmap.

## Participants

- **[Moderator](../process_people/moderator.md)** - Process facilitation, conflict resolution, finding consolidation
- **[MITRE Analyst](../compliance_governance/mitre-analyst.md)** - Threat modeling lead: STRIDE analysis, ATT&CK
  mapping, attack trees, threat actor profiling
- **[Systems Architect](../architecture/systems-architect.md)** - Trust boundaries, data flow diagrams, component
  interactions, blast radius
- **[Red Team Engineer](../compliance_governance/red-team-engineer.md)** - Attack path validation, exploitation chains,
  adversary simulation
- **[Blue Team Engineer](../compliance_governance/blue-team-engineer.md)** - Detection coverage, existing controls
  assessment, response readiness
- **[Purple Team Engineer](../compliance_governance/purple-team-engineer.md)** - TTP coverage validation, attack-defense
  gap analysis
- **[Infrastructure Engineer](../operations_reliability/infrastructure-engineer.md)** - Network segmentation, IAM, cloud
  configuration, encryption boundaries
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Vulnerability classification, OWASP/CVE
  mapping, severity assessment
- **[Compliance Officer](../compliance_governance/compliance-officer.md)** - Regulatory impact of identified threats,
  risk acceptance criteria

## Process

1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file.
   Install and verify all required tools, deduplicating across participants
2. Systems Architect presents the architecture: components, data flows, trust boundaries, and external dependencies
3. MITRE Analyst constructs data flow diagrams and identifies all trust boundary crossings
4. MITRE Analyst applies STRIDE to each boundary crossing to generate the initial threat catalog
5. Red Team Engineer validates threats with realistic attack paths and exploitation chains
6. Infrastructure Engineer assesses network, IAM, and cloud configuration against identified threats
7. Blue Team Engineer evaluates existing detection and response coverage for each threat
8. Purple Team Engineer maps gaps between identified threats and defensive capabilities using ATT&CK
9. Security Auditor classifies all findings using the [severity scale](../_shared/severity-scale.md) and CVSS scoring
10. MITRE Analyst profiles relevant threat actors (capability, intent, opportunity) and maps them to attack scenarios
11. MITRE Analyst constructs attack trees for the highest-priority threats with likelihood and impact scoring
12. Compliance Officer assesses regulatory implications and risk acceptance thresholds
13. Converge on prioritized threat register and mitigation roadmap

## Output Format

### Per Participant

- Perspective name
- Findings with evidence
- Severity and likelihood rating
- Recommended mitigations or controls

### Consolidated

- Executive summary with overall threat posture
- Data flow diagrams with annotated trust boundaries
- STRIDE threat catalog per component and boundary
- MITRE ATT&CK heat map of applicable techniques
- Attack trees for top threats with probability and impact
- Threat actor profiles with motivation and capability assessment
- Detection coverage matrix (covered / partial / gap)
- Existing controls assessment (effective / degraded / missing)
- Prioritized threat register with risk ratings (likelihood x impact)
- Mitigation roadmap with owner assignments
- Residual risk summary after proposed mitigations
- Threat posture assessment (Strong / Adequate / Weak / Critical)

## Constraints

- Ground every threat in architectural context — no abstract threat lists
- Every threat must trace to a specific data flow, trust boundary, or component
- Validate threats with realistic attack paths, not theoretical speculation
- Map findings to MITRE ATT&CK techniques for consistent communication
- Assess existing controls before recommending new ones
- Prioritize by exploitability and business impact, not by count
- Provide specific, actionable mitigations with clear ownership
- Treat the threat model as a living artifact, not a point-in-time document

## Conflict Resolution

When participants produce conflicting threat assessments or mitigations:

1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, cost vs. coverage)
3. Recommend a resolution with explicit justification and residual risk acknowledgment
4. If no resolution is possible, escalate to the user with a clear summary of options
