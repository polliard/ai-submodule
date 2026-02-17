# MCP Servers

Shareable MCP server configurations for extending AI capabilities.

## Overview

This directory contains [Model Context Protocol](https://modelcontextprotocol.io) server definitions that can be imported into any project using this submodule. MCP servers let AI assistants (VS Code Copilot, Claude, etc.) call tools directly via JSON-RPC over stdio.

## Structure

```
mcp/
├── README.md            # This file
├── vscode.json          # VS Code mcp.json template
└── servers/
    ├── gitignore.json   # MCP server definition
    ├── gitignore.md     # Documentation & usage examples
    ├── servicenow.json  # MCP server definition
    └── servicenow.md    # Documentation & usage examples
```

Each server has two files:

- **`.json`** — Machine-readable config defining tools and input schemas
- **`.md`** — Human-readable docs with examples, prompts, and workflows

## Setup

### VS Code / GitHub Copilot

1. Copy or symlink the template to your project:

```bash
# Option 1: Symlink (auto-updates with submodule)
mkdir -p .vscode
ln -s ../.ai/mcp/vscode.json .vscode/mcp.json

# Option 2: Copy (manual updates)
cp .ai/mcp/vscode.json .vscode/mcp.json
```

1. Ensure required binaries are installed (see individual server docs below)

2. Reload VS Code window

### Other Clients

Server definitions in `servers/` use a portable JSON format. Adapt to your client's configuration as needed.

## Available Servers

### gitignore

Manage `.gitignore` files using templates from multiple sources (GitHub, Toptal, local).

**Binary:** `gitignore` (v1.3.0+)
**Repository:** [github.com/polliard/gitignore](https://github.com/polliard/gitignore)

**Installation:**

```bash
# From source (Go 1.23+ required)
go install github.com/polliard/gitignore/src/cmd/gitignore@latest

# Or download from releases
curl -L https://github.com/polliard/gitignore/releases/latest/download/gitignore-darwin-arm64.tar.gz | tar xz
sudo mv gitignore /usr/local/bin/
```

**Tools provided:**

- `gitignore_list` — List all available templates
- `gitignore_search` — Search templates by name pattern
- `gitignore_add` — Add a template to `.gitignore`
- `gitignore_delete` — Remove a template section
- `gitignore_ignore` — Add patterns directly
- `gitignore_remove` — Remove patterns
- `gitignore_init` — Initialize with configured defaults

See [servers/gitignore.md](servers/gitignore.md) for full documentation.

### servicenow

Access ServiceNow CMDB, incidents, changes, problems, and other ITSM data.

**Binary:** `servicenow-mcp` (requires MCP server implementation)

**Required Environment Variables:**

- `SERVICENOW_INSTANCE` — Instance URL (e.g., `mycompany.service-now.com`)
- `SERVICENOW_USERNAME` — ServiceNow username with API access
- `SERVICENOW_PASSWORD` — ServiceNow password or API token

**Tools provided:**

- `snow_cmdb_query` — Query CMDB configuration items by class with filters
- `snow_cmdb_get` — Get CI details including relationships
- `snow_incident_query` — Query incidents with priority/state/assignment filters
- `snow_incident_get` — Get incident details with work notes and related records
- `snow_change_query` — Query change requests by type, state, schedule
- `snow_change_get` — Get change details including tasks and approvals
- `snow_problem_query` — Query problems
- `snow_user_lookup` — Look up users by username/email
- `snow_group_members` — List assignment group members
- `snow_table_query` — Generic query for any ServiceNow table

See [servers/servicenow.md](servers/servicenow.md) for full documentation.

## Adding New Tools

1. Create `.json` and `.md` files in `servers/`
2. For MCP servers: add entry to `vscode.json`
3. For CLI tools: document commands and usage in the `.md`
4. Update this README with a summary
5. Commit and push — all projects using the submodule can now opt-in

## Binary Distribution

Configs are portable text files. Binaries are **not** included. Distribution options:

- **Go:** `go install github.com/org/tool@latest`
- **Releases:** GitHub releases with prebuilt binaries
- **Homebrew:** `brew install org/tap/tool`
- **Internal:** Corporate artifact repository

Users without the binary simply won't have the tools available — no errors, just missing capabilities.
