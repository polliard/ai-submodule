# Panorama MCP — Install Guide

## Prerequisites

- **Python 3.10+**
- **Microsoft Edge** (used for SSO authentication via Playwright)

```bash
python3 --version   # 3.10 or higher
```

## Manual Install

```bash
cd mcp/servers/panorama-mcp
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
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
panorama-mcp --help
```

## Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `PANORAMA_URLS` | Yes | Comma-separated Panorama URLs | `https://panoramav2.example.com,https://panoramav1.example.com` |
| `PANORAMA_URL` | No | Single Panorama URL (backward compat) | `https://panoramav2.example.com` |
| `PANORAMA_SSO_ACCOUNT` | No | SSO account for auto-fill on login page | `user@company.com` |
| `PANORAMA_HEADLESS` | No | Run browser in headless mode (default: false) | `false` |

### VS Code / Cursor

Add to `.vscode/mcp.json`:

```json
{
    "servers": {
        "panorama": {
            "command": "panorama-mcp",
            "args": ["serve", "--no-preauth"],
            "env": {
                "PANORAMA_URLS": "https://panoramav2.corp.example.com",
                "PANORAMA_SSO_ACCOUNT": "user@company.com",
                "PANORAMA_HEADLESS": "false"
            }
        }
    }
}
```

See [README.md](README.md) for full tool documentation, multi-instance usage, and troubleshooting.
