# Panorama MCP Server

An MCP (Model Context Protocol) server for interacting with Palo Alto Panorama using browser-based SSO authentication.

## Features

- **SSO Authentication**: Uses browser automation (Playwright) to handle SSO login flows
- **Session Persistence**: Saves authentication state for future sessions
- **Policy Management**: View security and NAT policies
- **Log Monitoring**: Query traffic, threat, and system logs
- **Device Management**: List device groups and managed firewalls
- **Operations**: Commit changes and push to devices

## Installation

### Prerequisites

- Python 3.10+
- Playwright browsers

### Install from source

```bash
# Clone and install
cd panorama_mcp
pip install -e .

# Install Playwright browsers
playwright install chromium
```

### Configure VS Code / Cursor

Add to your MCP settings (`~/.vscode/mcp.json` or workspace `.vscode/mcp.json`):

```json
{
  "servers": {
    "panorama": {
      "command": "panorama-mcp",
      "env": {
        "PANORAMA_URL": "https://your-panorama-server.example.com",
        "PANORAMA_HEADLESS": "false"
      }
    }
  }
}
```

Or using Python directly:

```json
{
  "servers": {
    "panorama": {
      "command": "python",
      "args": ["-m", "panorama_mcp.server"],
      "env": {
        "PANORAMA_URL": "https://your-panorama-server.example.com"
      }
    }
  }
}
```

## Usage

### Authentication

First, authenticate to Panorama using SSO:

```
Use panorama_login to authenticate
```

The browser will open and wait for you to complete your SSO login. Once authenticated, the session is saved for future use.

### Available Tools

#### Authentication
- `panorama_login` - Open browser for SSO login (interactive)
- `panorama_check_auth` - Check current authentication status
- `panorama_logout` - Clear saved authentication

#### Policy Management
- `panorama_get_security_policies` - Get security policies for a device group
- `panorama_get_nat_policies` - Get NAT policies for a device group

#### Log Monitoring
- `panorama_get_traffic_logs` - Query traffic logs with optional filters
- `panorama_get_threat_logs` - Query threat logs with optional filters
- `panorama_get_system_logs` - Query system logs

#### Device Management
- `panorama_get_device_groups` - List all device groups
- `panorama_get_managed_devices` - List managed firewalls

#### Operations
- `panorama_commit` - Commit pending changes
- `panorama_push` - Push configuration to devices

#### Browser Control
- `panorama_screenshot` - Capture current page screenshot
- `panorama_navigate` - Navigate to specific Panorama page
- `panorama_page_snapshot` - Get accessibility tree for AI analysis

### Example Queries

```
# Check if authenticated
panorama_check_auth

# Get security policies
panorama_get_security_policies with device_group="Production"

# Get recent traffic logs
panorama_get_traffic_logs with query="addr.src in 10.0.0.0/8" limit=50

# Get threat logs
panorama_get_threat_logs with query="severity eq critical"

# List managed devices
panorama_get_managed_devices
```

## Environment Variables

| Variable            | Description                  | Default    |
| ------------------- | ---------------------------- | ---------- |
| `PANORAMA_URL`      | Panorama server URL          | (required) |
| `PANORAMA_HEADLESS` | Run browser in headless mode | `false`    |

## How SSO Works

1. When `panorama_login` is called, a browser window opens
2. Navigate to your SSO provider and complete authentication
3. Once logged into Panorama, the session state is saved to `~/.panorama_mcp/auth_state.json`
4. Future sessions reuse the saved state (until it expires)
5. If the session expires, run `panorama_login` again

## Security Notes

- Authentication state is stored locally in `~/.panorama_mcp/`
- The server never handles your credentials directly - all authentication happens in your browser
- Use `panorama_logout` to clear saved authentication
- Consider your organization's security policies when using browser automation

## Troubleshooting

### Browser not opening
- Ensure Playwright browsers are installed: `playwright install chromium`
- Check that `PANORAMA_HEADLESS` is set to `false` for SSO login

### Authentication not persisting
- Verify the storage path `~/.panorama_mcp/auth_state.json` is writable
- Some SSO providers use short-lived tokens that require frequent re-authentication

### Scraping not working
- Panorama UI varies by version; you may need to adjust selectors in `scraper.py`
- Use `panorama_page_snapshot` to inspect page structure
- Check browser console for JavaScript errors

## License

MIT
