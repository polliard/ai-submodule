# Severity Scale

> All personas must use this canonical severity scale when rating findings. Consistent classification enables meaningful panel consolidation.

## Ratings

| Severity | Definition | Action Required |
|----------|-----------|-----------------|
| **Critical** | Production-breaking, data loss, or active security exploitation risk | Must fix before any further progress |
| **High** | Significant degradation, security exposure, or reliability risk | Must fix before merge or deploy |
| **Medium** | Moderate quality, performance, or maintainability concern | Should fix in current cycle |
| **Low** | Minor improvement opportunity with no immediate risk | Consider fixing; document if deferred |

## Output Requirements

Every finding in a persona's output must include:

1. **Severity** — A rating from the table above
2. **Evidence** — Specific reference to the code, configuration, or system behavior that supports the finding
3. **Remediation** — A concrete recommendation for resolution

## Panel Consolidation

When consolidating findings across panel participants:

- A finding rated Critical by any participant remains Critical in the consolidated output
- Conflicting severity ratings must be resolved with documented rationale
- The consolidated output must group findings by severity, with Critical items first
