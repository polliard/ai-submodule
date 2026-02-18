# Azure DevOps MCP — Install Guide

## Prerequisites

- **Node.js 18+** with npm/npx

```bash
node --version   # v18.x or higher
npx --version
```

## Manual Install

No local installation required. The server runs via `npx`, which downloads the package on demand:

```bash
npx -y @azure-devops/mcp <your-org-name>
```

Replace `<your-org-name>` with your Azure DevOps organization (e.g. `contoso`).

## Automated Install

```bash
# macOS / Linux
./install.sh

# Windows (PowerShell)
.\install.ps1
```

These scripts verify Node.js/npx are available and confirm the package downloads correctly.

## Verify

```bash
npx -y @azure-devops/mcp --help
```

## Configuration

### VS Code / Cursor

Add to `.vscode/mcp.json`:

```json
{
    "servers": {
        "ado": {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@azure-devops/mcp", "${input:ado_org}"]
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

### Environment

No environment variables required. The organization name is passed as a CLI argument.

Azure DevOps authentication uses your existing browser session / Azure CLI credentials.
