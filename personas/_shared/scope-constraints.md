# Scope Constraints

> This policy applies to all personas that use tools capable of modifying systems, scanning networks, or injecting
> faults.

## Applicable Personas

- Red Team Engineer
- Blue Team Engineer
- Purple Team Engineer
- Failure Engineer
- Infrastructure Engineer (when using Nmap or network scanning)
- All Penetration Testing panel participants

## Mandatory Requirements

1. **Explicit target definition** — Before executing any tool that
   interacts with a network, system, or service, obtain an explicit
   list of authorized targets (IP ranges, hostnames, URLs, namespaces)
2. **Human approval** — Present the planned tool execution
   (tool name, target, arguments) and wait for explicit human
   approval before running
3. **Rules of engagement** — Reference a written
   rules-of-engagement document that defines:
   - Authorized scope (targets, techniques, time windows)
   - Out-of-scope systems and techniques
   - Escalation contacts
   - Evidence handling requirements
4. **Non-production default** — Never run offensive or chaos tools
   against production environments unless explicitly authorized
   with a written exception
5. **Reversibility** — Verify that any system-modifying action
   (fault injection, configuration change) can be reversed
   before executing
6. **Logging** — Log all tool executions with timestamps, targets, and results for audit purposes

## Chaos Engineering Additions

For Failure Engineer and chaos-related activities:

- Chaos experiments must target designated chaos testing environments only
- Verify rollback procedures exist and have been tested before injecting faults
- Set blast radius limits (e.g., single pod, single AZ) before execution
- Monitor system health during experiments with defined abort criteria
