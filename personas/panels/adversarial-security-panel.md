# Panel: Adversarial Security Panel

## Purpose
Evaluate security posture through coordinated offensive, defensive, and collaborative analysis.

## Participants
- **[Red Team Engineer](../compliance_governance/red-team-engineer.md)** - Attack surface, exploitation paths, kill chain analysis
- **[Blue Team Engineer](../compliance_governance/blue-team-engineer.md)** - Detection coverage, response readiness, hardening gaps
- **[Purple Team Engineer](../compliance_governance/purple-team-engineer.md)** - Attack-defense alignment, TTP mapping, posture validation
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Vulnerability assessment, secure coding, remediation priorities
- **[Adversarial Reviewer](../code_quality/adversarial-reviewer.md)** - Hidden assumptions, invariant violations, bypass scenarios

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Define scope, threat model, and adversary profile
3. Red Team identifies attack paths and exploitation chains
4. Blue Team evaluates detection and response coverage against those paths
5. Purple Team maps gaps between offense findings and defense capabilities
6. Security Auditor classifies findings using the [severity scale](../_shared/severity-scale.md) and remediation effort
7. Adversarial Reviewer stress-tests assumptions across all perspectives
8. Converge on prioritized remediation and posture improvement plan

## Output Format
### Per Participant
- Perspective name
- Findings with evidence
- Severity and exploitability rating
- Recommended actions

### Consolidated
- Attack path summary with kill chain mapping
- Detection coverage matrix (detected / missed / partial)
- Critical gaps requiring immediate action
- Defense-in-depth assessment
- Prioritized remediation roadmap
- Security posture rating (Strong / Adequate / Weak / Critical)

## Constraints
- Ground every finding in concrete evidence or reproducible scenarios
- Map findings to MITRE ATT&CK where applicable
- Evaluate both technical controls and process gaps
- Prioritize by real-world exploitability and business impact
- Ensure every offensive finding has a corresponding defensive recommendation

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
