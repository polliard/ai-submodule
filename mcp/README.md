# MCP Servers

Shareable MCP server configurations for extending AI capabilities.

## Overview

This directory contains [Model Context Protocol](https://modelcontextprotocol.io) server definitions that can be
  imported into any project using this submodule. MCP servers let AI assistants (VS Code Copilot, Claude, etc.) call
  tools directly via JSON-RPC over stdio.

## Structure

```text
mcp/
├── README.md            # This file
├── mcp-install          # Unified installer (macOS/Linux)
├── mcp-install.ps1      # Unified installer (Windows)
└── servers/
    ├── azure-devops-mcp/
    │   ├── mcp.json     # Server definition
    │   ├── install.md   # Install guide
    │   ├── install.sh   # Installer (macOS/Linux)
    │   └── install.ps1  # Installer (Windows)
    ├── gitignore-mcp/
    │   ├── mcp.json     # Server definition
    │   ├── README.md    # Documentation
    │   ├── install.md   # Install guide
    │   ├── install.sh   # Installer (macOS/Linux)
    │   └── install.ps1  # Installer (Windows)
    ├── panorama-mcp/
    │   ├── pyproject.toml
    │   ├── README.md    # Documentation
    │   ├── install.md   # Install guide
    │   ├── install.sh   # Installer (macOS/Linux)
    │   └── install.ps1  # Installer (Windows)
    └── servicenow-mcp/
        ├── mcp.json     # Server definition
        ├── README.md    # Documentation
        ├── install.md   # Install guide
        ├── install.sh   # Installer (macOS/Linux)
        ├── install.ps1  # Installer (Windows)
        └── pyproject.toml
```

Each server directory contains:

- **`mcp.json`** — Machine-readable config defining tools and input schemas
- **`README.md`** — Human-readable docs with examples, prompts, and workflows
- **`install.md`** — Prerequisites, manual install steps, configuration
- **`install.sh`** / **`install.ps1`** — Automated installers for macOS/Linux and Windows

## Installation

The `.ai/` directory can live in two places:

| Location | Use case |
| --- | --- |
| `~/.ai/` | Personal machine — shared across all repos |
| `<repo>/.ai/` (submodule) | Team-shared — checked into the project |

### Quick install

Use the unified installer at the root of `mcp/`. It handles prerequisites, prompts for required configuration, runs
  the server-specific installer, and prints the VS Code config snippet with your values filled in.

```bash
# macOS / Linux
./mcp-install                          # list available servers
./mcp-install azure-devops-mcp         # interactive — prompts for org name
./mcp-install servicenow-mcp --instance mycompany.service-now.com

# Windows (PowerShell)
.\mcp-install.ps1                                    # list available servers
.\mcp-install.ps1 panorama-mcp -Urls https://pan.example.com
```

### Per-server setup

Each server has different prerequisites and install methods. See the table below for details, or run `./mcp-install`
  for an interactive guide.

| Server | Type | Prerequisites | Install guide | Automated install |
| -------- | ------ | --------------- | --------------- | ------------------- |
| [azure-devops-mcp](servers/azure-devops-mcp/) | npx (no local install) | Node.js 18+ | [install.md](servers/azure-devops-mcp/install.md) | `install.sh` / `install.ps1` |
| [gitignore-mcp](servers/gitignore-mcp/) | Go binary | Go 1.23+ or curl | [install.md](servers/gitignore-mcp/install.md) | `install.sh` / `install.ps1` |
| [panorama-mcp](servers/panorama-mcp/) | Python venv + Playwright | Python 3.10+, Edge | [install.md](servers/panorama-mcp/install.md) | `install.sh` / `install.ps1` |
| [servicenow-mcp](servers/servicenow-mcp/) | Python + Playwright | Python 3.9+ | [install.md](servers/servicenow-mcp/install.md) | `install.sh` / `install.ps1` |

### VS Code / GitHub Copilot

Each server's [install.md](servers/) includes a VS Code config snippet. To configure a server, add its entry to
  `.vscode/mcp.json`.

Start with an empty skeleton:

```json
{
    "servers": {},
    "inputs": []
}
```

Then merge in the `servers` entry (and any `inputs`) from each server's install guide. For example, to add
  **gitignore** and **ado**:

```json
{
    "servers": {
        "ado": {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@azure-devops/mcp", "${input:ado_org}"]
        },
        "gitignore": {
            "type": "stdio",
            "command": "gitignore",
            "args": ["serve"]
        }
    },
    "inputs": [
        {
            "id": "ado_org",
            "type": "promptString",
            "description": "Azure DevOps organization name (e.g. 'contoso')"
        }
    ]
}
```

Save as `.vscode/mcp.json` and reload VS Code.

### Claude Code

Claude Code reads `mcp.json` files from server directories automatically when configured. See [Claude Code MCP
  docs](https://docs.anthropic.com/en/docs/claude-code/mcp) for config details.

### Other Clients

Server definitions in `servers/` use a portable JSON format. Adapt to your client's configuration as needed.

## Available Servers

### azure-devops-mcp

Query Azure DevOps work items, repos, pipelines, and pull requests.

**Transport:** npx (no local install needed)
**Package:** `@azure-devops/mcp`

**Required inputs:** Azure DevOps organization name (prompted on first use).

See [install.md](servers/azure-devops-mcp/install.md) for setup and [mcp.json](servers/azure-devops-mcp/mcp.json) for
  config.

### gitignore

Manage `.gitignore` files using templates from multiple sources (GitHub, Toptal, local).

**Binary:** `gitignore` (v1.3.0+)
**Repository:** [github.com/polliard/gitignore](https://github.com/polliard/gitignore)

**Tools:** `gitignore_list`, `gitignore_search`, `gitignore_add`, `gitignore_delete`, `gitignore_ignore`,
  `gitignore_remove`, `gitignore_init`

See [install.md](servers/gitignore-mcp/install.md) for setup and [README.md](servers/gitignore-mcp/README.md) for full
  documentation.

### panorama-mcp

MCP server for Palo Alto Panorama with browser-based SSO authentication, multi-instance support, and PanDirect API
  integration.

**Binary:** `panorama-mcp` (Python, pip-installable)
**Required env:** `PANORAMA_URLS`, optionally `PANORAMA_SSO_ACCOUNT`

**Tools:** 34 tools covering device management, policy, objects, network, logs, monitoring, operations, and browser
  control.

See [install.md](servers/panorama-mcp/install.md) for setup and [README.md](servers/panorama-mcp/README.md) for full
  documentation.

### servicenow-mcp

Access ServiceNow CMDB, incidents, changes, and other ITSM data via SSO authentication.

**Binary:** `servicenow-mcp` (Python, pip-installable)
**Required env:** `SERVICENOW_INSTANCE`
**Auth:** Browser-based SSO — no passwords stored. Sessions cached 8 hours.

**Tools:** `snow_configure`, `snow_incident_query`, `snow_incident_get`, `snow_change_query`, `snow_change_get`,
  `snow_cmdb_query`, `snow_cmdb_get`, `snow_user_query`, `snow_group_query`, `snow_table_query`, `snow_kb_search`,
  `snow_describe_table`, `snow_build_query`

See [install.md](servers/servicenow-mcp/install.md) for setup and [README.md](servers/servicenow-mcp/README.md) for
  full documentation.

## Adding New Servers

1. Create a directory under `servers/<name>/` with at least `mcp.json`
2. Add a `README.md` with tool descriptions and workflows
3. Add `install.md`, `install.sh`, and `install.ps1`
4. Update this README
5. Commit and push — all projects using the submodule can opt-in
