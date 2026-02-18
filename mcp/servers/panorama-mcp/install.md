# Panorama MCP — Install Guide

## Prerequisites

- **Python 3.10+**
- **Microsoft Edge** (used for SSO authentication via Playwright)

```bash
python3 --version   # 3.10 or higher
```

## Automated Install (Recommended)

```bash
# macOS / Linux
cd mcp/servers/panorama-mcp
bash install.sh

# Windows (PowerShell)
cd mcp\servers\panorama-mcp
.\install.ps1
```

The installer will:
1. Check Python version (3.10+)
2. Create a `.venv` virtual environment (or recreate if stale)
3. Install the package and dependencies into the venv
4. Install Playwright Chromium browser
5. Verify the installation works

## Manual Install

```bash
cd mcp/servers/panorama-mcp
python3 -m venv .venv
.venv/bin/pip install -e .           # Windows: .venv\Scripts\pip install -e .
.venv/bin/playwright install chromium
```

> **Note:** Always use `.venv/bin/pip` (not bare `pip`) to avoid macOS
> "externally-managed-environment" errors and ensure packages go into the venv.

## Verify

```bash
.venv/bin/panorama-mcp --help
```

## Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `PANORAMA_URLS` | Yes | Comma-separated Panorama URLs | `https://panoramav2.example.com` |
| `PANORAMA_SSO_ACCOUNT` | No | SSO account for auto-fill on login page | `user@company.com` |
| `PANORAMA_HEADLESS` | No | Run browser in headless mode (default: false) | `false` |

### VS Code / Copilot

Add to `.vscode/mcp.json` in your workspace root:

```json
{
    "servers": {
        "panorama": {
            "type": "stdio",
            "command": "/absolute/path/to/panorama-mcp/.venv/bin/python",
            "args": ["-m", "panorama_mcp", "serve", "--no-preauth"],
            "env": {
                "PANORAMA_URLS": "https://panoramav2.corp.example.com",
                "PANORAMA_SSO_ACCOUNT": "user@company.com",
                "PANORAMA_HEADLESS": "false"
            }
        }
    }
}
```

> **Important:** Use the full absolute path to `.venv/bin/python` so VS Code
> finds the correct interpreter with all dependencies installed. The installer
> prints the exact path after a successful install.

### Claude Code

Add to `~/.claude/settings.json` or project `.claude/settings.json`:

```json
{
    "mcpServers": {
        "panorama": {
            "command": "/absolute/path/to/panorama-mcp/.venv/bin/python",
            "args": ["-m", "panorama_mcp", "serve", "--no-preauth"],
            "env": {
                "PANORAMA_URLS": "https://panoramav2.corp.example.com",
                "PANORAMA_SSO_ACCOUNT": "user@company.com",
                "PANORAMA_HEADLESS": "false"
            }
        }
    }
}
```

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

See [README.md](README.md) for full tool documentation, multi-instance usage, and troubleshooting.
