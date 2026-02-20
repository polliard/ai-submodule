# Round Table: MCP Server Review

## Purpose
Evaluate MCP server implementations for protocol compliance, security, usability, and integration quality.

## Participants
- **MCP Server Engineer** - Protocol compliance, schema correctness, transport design
- **AI Tooling Specialist** - Tool usability for LLM consumption, naming, descriptions
- **Security Auditor** - Credential handling, auth patterns, secret exposure
- **API Designer** - Contract design, naming conventions, versioning
- **API Consumer** - Developer experience, documentation quality, onboarding friction

## Process
1. Review server manifest and tool definitions
2. Each participant evaluates from their lens
3. Validate tool schemas against protocol spec
4. Assess developer and LLM interaction experience
5. Surface security and operational concerns
6. Converge on recommendations

## Output Format
### Per Participant
- Perspective name
- Findings and concerns
- Severity rating
- Recommended changes

### Consolidated
- Protocol compliance status
- Tool design quality assessment
- Security findings
- Developer experience gaps
- Prioritized improvements
- Ship/Iterate/Block recommendation

## Constraints
- Evaluate from both human developer and LLM consumer perspectives
- Validate all tool schemas for completeness and correctness
- Verify credential handling follows security best practices
- Ensure documentation supports self-service onboarding
