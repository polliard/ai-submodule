# Panel: BA - Business Analyst

## Purpose
Cross-functional requirements and solution review ensuring business needs are accurately captured, technically feasible, testable, and well-communicated.

## Participants
- **[Business Analyst](../process_people/business-analyst.md)** - Requirements completeness, process gaps, stakeholder alignment, business rules
- **[Product Manager](../process_people/product-manager.md)** - User value, acceptance criteria, scope, success metrics
- **[Tech Lead](../process_people/tech-lead.md)** - Technical feasibility, delivery risk, architectural fit, team impact
- **[Architect](../architecture/architect.md)** - System design alignment, integration points, scalability implications
- **[Test Engineer](../engineering/test-engineer.md)** - Testability, coverage gaps, edge cases, validation strategy
- **[UX Engineer](../engineering/ux-engineer.md)** - User experience, workflow ergonomics, developer experience

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Business Analyst presents requirements, process flows, and business rules
3. Each participant reviews from their perspective
4. Present findings using the [severity scale](../_shared/severity-scale.md)
5. Identify conflicting recommendations and unresolved ambiguities
6. Produce consolidated assessment with action items

## Output Format
### Per Participant
- Perspective name
- Key concerns (bulleted)
- Risk level
- Suggested changes or clarifying questions

### Consolidated
- Must-resolve items (blockers to proceed)
- Should-resolve items (significant gaps)
- Consider items (improvements)
- Open questions requiring stakeholder input
- Tradeoff summary
- Final recommendation (Approve/Request Changes/Reject)

## Constraints
- Focus on requirement quality and solution alignment, not implementation details
- Resolve conflicts explicitly with reasoning and traceoffs
- Flag assumptions that need stakeholder validation
- Ensure every requirement has clear acceptance criteria before approval

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
