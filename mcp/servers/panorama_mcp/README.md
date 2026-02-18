# Panorama MCP Server

MCP server for Palo Alto Panorama with browser-based SSO authentication and multi-instance support.

## Features

- **SSO Authentication**: Browser-based SSO via Playwright — no credentials in config
- **Multi-Instance**: Manage multiple Panorama deployments from a single server
- **Session Persistence**: 8-hour TTL, per-instance session files with 0600 permissions
- **Pre-Authentication**: CLI login before server starts — no auth prompts during MCP use
- **Policy Management**: View security and NAT policies
- **Log Monitoring**: Query traffic, threat, and system logs
- **Device Management**: List device groups and managed firewalls
- **Operations**: Commit changes and push to devices

## Installation

```bash
cd panorama_mcp
pip install -e .
playwright install chromium
```

## Quick Start

```bash
# 1. Set your Panorama instance(s)
export PANORAMA_URLS="https://panoramav2.corp.jmfamily.com"

# 2. Authenticate via SSO (opens browser, press ENTER when done)
panorama-mcp login

# 3. Start the MCP server
panorama-mcp serve
```

## CLI Commands

### `panorama-mcp serve`

Start the MCP server. Pre-authenticates any instances without a valid session.

```bash
panorama-mcp serve              # pre-auth + start server
panorama-mcp serve --no-preauth # skip pre-auth, handle SSO on-demand
```

### `panorama-mcp login`

Standalone SSO login. Opens a browser, waits for you to complete SSO, saves the session.

```bash
panorama-mcp login                          # login to first configured instance
panorama-mcp login --instance panoramav2    # login to specific instance (partial match)
```

### `panorama-mcp status`

Show session status for all configured instances.

```bash
panorama-mcp status
#   panoramav2.corp.jmfamily.com: VALID
#   panoramav1.corp.jmfamily.com: EXPIRED / MISSING
```

## Configuration

### Environment Variables

| Variable            | Description                                  | Example                                                  |
| ------------------- | -------------------------------------------- | -------------------------------------------------------- |
| `PANORAMA_URLS`     | Comma-separated Panorama URLs (multi-deploy) | `https://panoramav2.example.com,https://panoramav1.example.com` |
| `PANORAMA_URL`      | Single Panorama URL (backward compat)        | `https://panoramav2.example.com`                         |
| `PANORAMA_HEADLESS` | Run browser in headless mode                 | `false` (default)                                        |

### VS Code / Cursor

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "panorama": {
      "command": "panorama-mcp",
      "args": ["serve", "--no-preauth"],
      "env": {
        "PANORAMA_URLS": "https://panoramav2.corp.jmfamily.com,https://panoramav1.corp.jmfamily.com",
        "PANORAMA_HEADLESS": "false"
      }
    }
  }
}
```

## Multi-Instance Usage

When multiple Panorama instances are configured, every tool accepts an optional `instance` parameter. You can pass:

- A full URL: `https://panoramav2.corp.jmfamily.com`
- A hostname: `panoramav2.corp.jmfamily.com`
- A partial match: `panoramav2` or `v2`

If omitted, the first configured instance is used.

```
# List configured instances
panorama_list_instances

# Query specific instance
panorama_get_device_groups with instance="panoramav2"

# Default to first instance
panorama_get_security_policies with device_group="Production"
```

## Available Tools

### Instance Management
- `panorama_list_instances` — List configured instances and session status
- `panorama_login` — Open browser for SSO login
- `panorama_check_auth` — Check authentication status
- `panorama_logout` — Clear saved authentication

### Policy Management
- `panorama_get_security_policies` — Get security policies for a device group
- `panorama_get_nat_policies` — Get NAT policies for a device group

### Log Monitoring
- `panorama_get_traffic_logs` — Query traffic logs with optional filters
- `panorama_get_threat_logs` — Query threat logs with optional filters
- `panorama_get_system_logs` — Query system logs

### Device Management
- `panorama_get_device_groups` — List all device groups
- `panorama_get_managed_devices` — List managed firewalls

### Operations
- `panorama_commit` — Commit pending changes
- `panorama_push` — Push configuration to devices

### Browser Control
- `panorama_screenshot` — Capture current page screenshot
- `panorama_navigate` — Navigate to specific Panorama page
- `panorama_page_snapshot` — Get accessibility tree for AI analysis

## How SSO Authentication Works

Panorama restricts server-side authentication — only browser-based SSO with cookies is supported.

1. **Pre-auth** (`panorama-mcp login` or `panorama-mcp serve`):
   - A Chromium browser opens and navigates to Panorama
   - Panorama redirects to your identity provider (Okta, Azure AD, etc.)
   - You complete SSO in the browser
   - Press ENTER in the terminal when done
   - Cookies/session are saved to `~/.config/panorama-mcp/`

2. **During MCP operation**:
   - Tools load the saved session (cookies) into a headless browser
   - The headless browser uses cookies to access Panorama pages
   - Sessions are valid for 8 hours, then require re-authentication

3. **Session storage**:
   - Location: `~/.config/panorama-mcp/{hostname}_session.json`
   - Permissions: `0600` (owner read/write only)
   - TTL: 8 hours from last save

## Validation

Test SSO login and data collection against a real instance:

```bash
python validate.py https://panoramav2.corp.jmfamily.com
```

This will:
1. Check for existing session
2. Login via SSO if needed
3. Verify authentication works
4. Test device group and managed device queries
5. Test screenshot capture
6. Report pass/fail for each check

## Troubleshooting

### "Not authenticated" errors
- Run `panorama-mcp login` to re-authenticate
- Check `panorama-mcp status` to see session validity
- Sessions expire after 8 hours

### Browser not opening
- Ensure Playwright is installed: `playwright install chromium`
- Set `PANORAMA_HEADLESS=false` for SSO login

### Session not persisting
- Check permissions on `~/.config/panorama-mcp/`
- Some SSO providers issue very short-lived tokens

### Scraping not working
- Panorama UI varies by version; selectors in `scraper.py` may need adjustment
- Use `panorama_page_snapshot` to inspect page structure

## License

MIT
