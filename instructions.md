# AI Instructions

> **Version**: 2.0 | **Last updated**: 2026-02-17

Base instructions for AI assistants across all projects.

## Core Principles

- Be concise and direct
- Show, don't tell - prefer code over explanations
- Follow project conventions (see project-specific instructions)
- Ask clarifying questions when requirements are ambiguous
- Prefer iterative changes over large rewrites
- Always keep documentation in sync with code.

## Code Quality

- Write idiomatic code for the language
- Include error handling
- Write testable code
- Follow existing patterns in the codebase

## Communication

- Use markdown formatting
- Link to relevant files when discussing code
- Provide context for suggestions

## Tools

- Use available MCP tools when they exist
- Prefer project-specific tooling over generic approaches
- Check `.ai/project.yaml` for project configuration (language, framework, test runner, linter, formatter, and other project-specific settings)

## Personas & Panels

- Personas are individual expert perspectives (see `personas/`)
- Panels are multi-persona collaborative reviews (see `personas/panels/`)
- Use panels when comprehensive evaluation from multiple perspectives is needed
- Panel output consolidates individual findings into actionable recommendations
- See `personas/panels-personas.md` for guidance on which panel to use

### Activation Protocol

When activating any persona or panel, follow this sequence before beginning analysis:

1. **Load the persona file** — Read the full persona definition from `personas/`
2. **Execute Tool Setup** — Run the `## Tool Setup` bootstrap in the persona file: check tool availability, install missing tools, verify installations, and document any constraints
3. **Begin analysis** — Proceed with the `## Evaluate For` criteria using the verified toolchain

For panels, execute Tool Setup across all participating personas before any participant begins their review. Deduplicate shared tools — install each tool only once even if multiple personas list it.

### Shared Policies

All persona-based analysis is governed by these shared policies:

- **[Tool Setup](personas/_shared/tool-setup.md)** — Standard bootstrap procedure for installing and verifying tools
- **[Base Tools](personas/_shared/base-tools.md)** — Shared tools available across all personas
- **[Severity Scale](personas/_shared/severity-scale.md)** — Canonical severity ratings for all findings
- **[Credential Policy](personas/_shared/credential-policy.md)** — Rules for handling authentication and secrets
- **[Scope Constraints](personas/_shared/scope-constraints.md)** — Mandatory requirements for offensive and chaos engineering personas

Tool isolation: All `pip install` commands must run inside a Python virtual environment. Use `npx` for Node.js CLI tools to avoid global installs.

### Choosing Between Similar Panels

Some panels have overlapping scope. Use these guidelines:

- **Security Review** vs **Adversarial Security Panel** vs **Penetration Testing**: Use Security Review for general vulnerability assessment and compliance. Use Adversarial Security for red/blue/purple team coordination and detection coverage validation. Use Penetration Testing for structured exploit-driven assessments with kill chain analysis.
- **Code Review** vs **Technical Debt Review**: Use Code Review for evaluating specific changes (PRs, new features). Use Technical Debt Review for assessing accumulated debt across the codebase and prioritizing remediation.

### Custom Panels

For situations that don't fit a predefined panel, compose an ad-hoc panel by selecting 4-6 personas from `personas/index.md`. Follow the same activation protocol: load all persona files, deduplicate and bootstrap tools, then have each persona evaluate independently before consolidating findings.

## Coding Languages

### Python

- Always use virtual environments .venv
- If there are multiple "projects" within a repo, use .venv inside of the subdirectories to separate needed tooling.

### JavaScript / TypeScript

- Use `package-lock.json` or `yarn.lock` — always commit lockfiles
- Prefer `npx` for one-shot CLI tool execution over global installs
- Use project-local ESLint and Prettier configs; do not rely on global settings

### Go

- Follow standard `go mod` for dependency management
- Use `go vet` and `staticcheck` for static analysis
- Keep module paths consistent with repository structure

---

*This file is inherited by all projects. Project-specific instructions extend this.*
