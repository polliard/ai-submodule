# ServiceNow MCP — Install Guide

## Prerequisites

- **Python 3.9+**

```bash
python3 --version   # 3.9 or higher
```

## Manual Install

```bash
cd mcp/servers/servicenow-mcp
pip install -e .
playwright install chromium
```

## Automated Install

```bash
# macOS / Linux
./install.sh

# Windows (PowerShell)
.\install.ps1
```

## Verify

```bash
servicenow-mcp --help
```

## Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SERVICENOW_INSTANCE` | Yes | Your ServiceNow instance hostname | `mycompany.service-now.com` |

### VS Code / Cursor

Add to `.vscode/mcp.json`:

```json
{
    "servers": {
        "servicenow": {
            "type": "stdio",
            "command": "servicenow-mcp",
            "args": ["serve"],
            "env": {
                "SERVICENOW_INSTANCE": "mycompany.service-now.com"
            }
        }
    }
}
```

### Authentication

Uses browser-based SSO — no passwords stored. A browser window opens for authentication on first use. Sessions are cached at `~/.config/servicenow-mcp/` with an 8-hour expiry.

See [README.md](README.md) for full tool documentation and troubleshooting.
