# Round Table: Adversarial Security Panel

## Purpose
Evaluate security posture through coordinated offensive, defensive, and collaborative analysis.

## Participants
- **Red Team Engineer** - Attack surface, exploitation paths, kill chain analysis
- **Blue Team Engineer** - Detection coverage, response readiness, hardening gaps
- **Purple Team Engineer** - Attack-defense alignment, TTP mapping, posture validation
- **Security Auditor** - Vulnerability assessment, secure coding, remediation priorities
- **Adversarial Reviewer** - Hidden assumptions, invariant violations, bypass scenarios

## Process
1. Define scope, threat model, and adversary profile
2. Red Team identifies attack paths and exploitation chains
3. Blue Team evaluates detection and response coverage against those paths
4. Purple Team maps gaps between offense findings and defense capabilities
5. Security Auditor classifies findings by severity and remediation effort
6. Adversarial Reviewer stress-tests assumptions across all perspectives
7. Converge on prioritized remediation and posture improvement plan

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
