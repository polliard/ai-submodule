# ServiceNow MCP — Install Guide

## Prerequisites

- **Python 3.9+**

```bash
python3 --version   # 3.9 or higher
```

## Automated Install (Recommended)

```bash
# macOS / Linux
cd mcp/servers/servicenow-mcp
bash install.sh

# Windows (PowerShell)
cd mcp\servers\servicenow-mcp
.\install.ps1
```

The installer will:
1. Check Python version (3.9+)
2. Create a `.venv` virtual environment (or recreate if stale)
3. Install the package and dependencies into the venv
4. Install Playwright Chromium browser
5. Verify the installation works

## Manual Install

```bash
cd mcp/servers/servicenow-mcp
python3 -m venv .venv
.venv/bin/pip install -e .           # Windows: .venv\Scripts\pip install -e .
.venv/bin/playwright install chromium
```

> **Note:** Always use `.venv/bin/pip` (not bare `pip`) to avoid macOS
> "externally-managed-environment" errors and ensure packages go into the venv.

## Verify

```bash
.venv/bin/servicenow-mcp --help
```

## Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SERVICENOW_INSTANCE` | Yes | Your ServiceNow instance hostname | `mycompany.service-now.com` |

### VS Code / Copilot

Add to `.vscode/mcp.json` in your workspace root:

```json
{
    "servers": {
        "servicenow": {
            "type": "stdio",
            "command": "/absolute/path/to/servicenow-mcp/.venv/bin/servicenow-mcp",
            "args": ["serve", "--no-preauth"],
            "env": {
                "SERVICENOW_INSTANCE": "mycompany.service-now.com"
            }
        }
    }
}
```

> **Important:** Use the full absolute path to the venv's `servicenow-mcp`
> binary so VS Code finds the correct interpreter with all dependencies.
> The installer prints the exact path after a successful install.

### Claude Code

Add to `~/.claude/settings.json` or project `.claude/settings.json`:

```json
{
    "mcpServers": {
        "servicenow": {
            "command": "/absolute/path/to/servicenow-mcp/.venv/bin/servicenow-mcp",
            "args": ["serve", "--no-preauth"],
            "env": {
                "SERVICENOW_INSTANCE": "mycompany.service-now.com"
            }
        }
    }
}
```

### Authentication

Uses browser-based SSO — no passwords stored. A browser window opens for
authentication on first use. Sessions are cached at `~/.config/servicenow-mcp/`
with an 8-hour expiry.

## Troubleshooting

### "externally-managed-environment" error
Your system Python is managed by Homebrew/OS. The installer handles this by
using a virtual environment. If running manually, always use `.venv/bin/pip`
instead of bare `pip` or `pip3`.

### Stale venv / "bad interpreter" error
If you moved the project directory, the venv's Python symlinks break. Fix:
```bash
rm -rf .venv
bash install.sh
```

### Playwright browser not found
Re-run: `.venv/bin/playwright install chromium`

See [README.md](README.md) for full tool documentation and troubleshooting.
