# AI Instructions

Base instructions for AI assistants across all projects.

## Core Principles

- Be concise and direct
- Show, don't tell - prefer code over explanations
- Follow project conventions (see project-specific instructions)
- Ask clarifying questions when requirements are ambiguous
- Prefer iterative changes over large rewrites
- Alaways keep documentation in sync with code.

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
- Check `.ai/project.yaml` for project configuration

## Personas & Panels

- Personas are individual expert perspectives (see `personas/`)
- Panels (also known as round tables) are multi-persona collaborative reviews
- Use panels when comprehensive evaluation from multiple perspectives is needed
- Panel output consolidates individual findings into actionable recommendations
- Terms "panel" and "round_table" are interchangeable

## Coding Languages

### Python

- Always use virtual environments .venv
- If there are multiple "projects" within a repo, Use .venv inside of the subdirectories to serprate needed tooling.

---

*This file is inherited by all projects. Project-specific instructions extend this.*
