# Panel: Accessibility Review

## Purpose
Evaluate application accessibility compliance, inclusive design patterns, and assistive technology compatibility.

## Participants
- **[Accessibility Engineer](../compliance_governance/accessibility-engineer.md)** - WCAG compliance, ARIA patterns, assistive technology compatibility
- **[Frontend Engineer](../domain_specific/frontend-engineer.md)** - Semantic HTML, focus management, responsive design
- **[UX Engineer](../engineering/ux-engineer.md)** - Developer experience of accessible components, API ergonomics
- **[Test Engineer](../engineering/test-engineer.md)** - Accessibility test coverage, automated a11y testing
- **[Documentation Writer](../documentation/documentation-writer.md)** - Accessibility documentation, usage guidelines

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Define target WCAG conformance level and user profiles
3. Each participant evaluates from their perspective
4. Test with assistive technologies (screen readers, keyboard navigation)
5. Present findings using the [severity scale](../_shared/severity-scale.md)
6. Prioritize by user impact and compliance requirement

## Output Format
### Per Participant
- Perspective name
- Accessibility issues identified
- WCAG criteria affected
- Recommended remediation

### Consolidated
- WCAG conformance gaps by level (A/AA/AAA)
- Critical barriers to access
- Assistive technology compatibility issues
- Quick wins and low-effort fixes
- Remediation roadmap with priority

## Constraints
- Test with actual assistive technologies, not just automated tools
- Prioritize barriers that prevent task completion
- Consider cognitive and motor accessibility, not just visual
- Ensure fixes don't regress other accessibility features

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
