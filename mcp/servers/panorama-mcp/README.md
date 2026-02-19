# Panorama MCP Server

**Read-only query tool** for Palo Alto Panorama. Provides structured, searchable access to policies, objects, logs,
  devices, and configuration — without modifying anything on the appliance.

Uses browser-based SSO authentication, multi-instance support, and Panorama's internal PanDirect RPC API for reliable
  structured data.

## Features

- **Read-Only Queries**: All tools fetch data — no configuration changes are made to Panorama
- **SSO Authentication**: Browser-based SSO via Playwright (Microsoft Edge) — no credentials in config
- **Auto-SSO**: Automatically clicks "Use Single Sign-On", fills SSO account, and handles IDP redirect
- **PanDirect API**: Uses Panorama's internal RPC API for reliable structured data (no DOM scraping)
- **Multi-Instance**: Query multiple Panorama deployments from a single server
- **Live Browser Session**: Browser stays alive for session persistence (Panorama uses session-only cookies)
- **36 MCP Tools**: Comprehensive read-only coverage of Panorama data
- **Policy Queries**: Security and NAT policies with pre/post rulebase support
- **Object Queries**: Address objects, service objects, address groups, service groups
- **Network Config**: Security zones, interfaces, routing
- **Log Queries**: Traffic, threat, system, URL, WildFire, and config logs
- **Device Info**: Device groups, managed firewalls, templates
- **Monitoring**: System resources, HA status, jobs, software versions
- **Power Tools**: Generic PanDirect RPC and API method discovery

## Installation

```bash
cd panorama-mcp
pip install -e .
playwright install chromium
```

## Quick Start

```bash
# 1. Set your Panorama instance(s)
export PANORAMA_URLS="https://panoramav2.corp.jmfamily.com"
export PANORAMA_SSO_ACCOUNT="user@company.com"

# 2. Start the MCP server (handles SSO on first tool call)
panorama-mcp serve
```

## CLI Commands

### `panorama-mcp serve`

Start the MCP server. Pre-authenticates all configured instances by default.

```bash
panorama-mcp serve              # pre-auth + start server
panorama-mcp serve --no-preauth # skip pre-auth, handle SSO on-demand
```

### `panorama-mcp login`

Standalone SSO login for testing. Note: Panorama uses session-only cookies, so the session only persists while the
  browser is open.

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

| Variable | Description | Example |
| ---------------------- | -------------------------------------------- | -------------------------------------------------------- |
| `PANORAMA_URLS` | Comma-separated Panorama URLs (multi-deploy) | `https://panoramav2.example.com,https://panoramav1.example.com` |
| `PANORAMA_URL` | Single Panorama URL (backward compat) | `https://panoramav2.example.com` |
| `PANORAMA_SSO_ACCOUNT` | SSO account for auto-fill on login page | `user@company.com` |
| `PANORAMA_HEADLESS` | Run browser in headless mode (default: false) | `false` |

### VS Code / Cursor

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "panorama": {
      "command": "panorama-mcp",
      "args": ["serve", "--no-preauth"],
      "env": {
        "PANORAMA_URLS": "https://panoramav2.corp.jmfamily.com",
        "PANORAMA_SSO_ACCOUNT": "user@company.com",
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

## Available Tools (36)

### Instance Management (4)

- `panorama_list_instances` — List configured instances and session status
- `panorama_login` — Open browser for SSO login
- `panorama_check_auth` — Check authentication status
- `panorama_logout` — Clear saved authentication

### System / Dashboard (3)

- `panorama_get_system_info` — Hostname, IP, PAN-OS version, serial, uptime
- `panorama_get_device_summary` — Connected/disconnected counts, version distribution
- `panorama_get_system_resources` — CPU, memory, disk utilization

### Configuration (2)

- `panorama_get_templates` — Templates, template stacks, and associations
- `panorama_get_commit_history` — Config commit audit trail (who, when, what)

### Policy Queries (2)

- `panorama_get_security_policies` — Security policies for a device group (`position`: `pre`, `post`, or `both`)
- `panorama_get_nat_policies` — NAT policies for a device group (`position`: `pre`, `post`, or `both`)

### Objects (4)

- `panorama_get_address_objects` — IP/FQDN/range objects with search filter
- `panorama_get_service_objects` — Protocol/port objects with search filter
- `panorama_get_address_groups` — Address group objects (collections of addresses) with search filter
- `panorama_get_service_groups` — Service group objects (collections of services) with search filter

### Network (3)

- `panorama_get_security_zones` — Security zones (template-scoped)
- `panorama_get_interfaces` — Network interfaces (template-scoped)
- `panorama_get_routing` — Routing info / virtual routers (template-scoped)

### Log Monitoring (6)

- `panorama_get_traffic_logs` — Query traffic logs with optional filters
- `panorama_get_threat_logs` — Query threat logs with optional filters
- `panorama_get_system_logs` — Query system logs
- `panorama_get_url_logs` — URL filtering logs
- `panorama_get_wildfire_logs` — WildFire submission logs
- `panorama_get_config_logs` — Configuration change logs

### Device Management (2)

- `panorama_get_device_groups` — List all device groups with device counts
- `panorama_get_managed_devices` — List managed firewalls with full details

### Operations (2)

- `panorama_commit` — Commit pending changes
- `panorama_push` — Push configuration to devices

### Monitoring (3)

- `panorama_get_jobs` — Async job status (commits, pushes, upgrades)
- `panorama_get_ha_status` — High availability pair status
- `panorama_get_software_info` — Installed PAN-OS + content versions

### Browser Control (3)

- `panorama_screenshot` — Capture current page screenshot
- `panorama_navigate` — Navigate to specific Panorama page
- `panorama_page_snapshot` — Get accessibility tree for AI analysis

### Power Tools (2)

- `panorama_run_direct` — Call any PanDirect RPC method directly (escape hatch for power users)
- `panorama_discover_methods` — Enumerate available PanDirect namespaces and methods via JS introspection

## How It Works

### Architecture

```text
MCP Client (VS Code, CLI)
    │
    ▼
Panorama MCP Server (Python, stdio)
    │
    ▼
Playwright Browser (Microsoft Edge, visible mode)
    │
    ├── SSO via Azure AD / Okta (auto-click + auto-fill)
    ├── Panos.direct.run() — Internal RPC API (36 tools)
    │     ├── DashboardDirect.*        (system info, resources, HA)
    │     ├── DeviceDirect.*           (managed devices)
    │     ├── PanoramaScalability.*    (templates, stacks)
    │     ├── ConfigAudit.*            (commit history)
    │     ├── Policies.*               (security, NAT rules)
    │     ├── ObjectDirect.*           (address, service objects)
    │     ├── ZoneDirect.*             (security zones)
    │     ├── InterfaceDirect.*        (network interfaces)
    │     ├── RoutingDirect.*          (virtual routers, routes)
    │     ├── LogDirect.*              (traffic, threat, system, URL, WildFire, config)
    │     ├── JobDirect.*              (async job tracking)
    │     ├── SoftwareDirect.*         (PAN-OS versions)
    │     └── (discover more with panorama_discover_methods)
    └── Session-only cookies (live browser required)
```

### SSO Authentication

Panorama restricts server-side authentication — only browser-based SSO with cookies is supported.

1. **On first tool call** (or `serve` with pre-auth):
   - A Microsoft Edge browser opens and navigates to Panorama
   - Auto-clicks "Use Single Sign-On"
   - Auto-fills SSO account from `PANORAMA_SSO_ACCOUNT`
   - Clicks Continue to redirect to your IDP (Azure AD, Okta, etc.)
   - User completes MFA if prompted
   - Browser stays open for the server lifetime

2. **During MCP operation**:
   - All data access uses `Panos.direct.run()` — Panorama's internal RPC API
   - CSRF tokens are handled automatically by the framework
   - Returns structured JSON (no DOM scraping)

3. **Session lifecycle**:
   - Panorama uses session-only cookies — they exist only while the browser is open
   - The browser stays alive for the MCP server's lifetime
   - If the session expires (~8 hours), auto-SSO re-authenticates

### Why Not Headless?

Corporate SSO (Azure AD, Okta) typically requires visible browser mode:

- SSL certificate validation needs the system browser's cert store
- MFA prompts (push notifications, TOTP) need user interaction
- Some IDPs detect and block headless browsers

The server uses `channel="msedge"` to leverage the system Microsoft Edge installation, which has access to corporate
  certificates and proxy configuration.

## Validation

Test SSO login and data collection against a real instance:

```bash
export PANORAMA_URLS="https://panoramav2.corp.jmfamily.com"
export PANORAMA_SSO_ACCOUNT="user@company.com"
python validate.py
```

This will:

1. Launch browser and navigate to Panorama
2. Auto-SSO if session expired (wait for MFA if needed)
3. Verify authentication works
4. Query device groups via PanDirect API
5. Query managed devices via PanDirect API
6. Test screenshot capture
7. Report pass/fail for each check

## Troubleshooting

### "Not authenticated" errors

- The browser may have been closed (session-only cookies lost)
- SSO session expired — the server will auto-SSO on next tool call
- Check if `PANORAMA_SSO_ACCOUNT` is set correctly

### Browser not opening

- Ensure Playwright is installed: `playwright install chromium`
- Microsoft Edge must be installed (`channel="msedge"`)
- `PANORAMA_HEADLESS` must be `false` (default) for SSO

### "Panos.direct.run timed out"

- Panorama may be slow to respond — increase timeout
- The browser page may have navigated away — use `panorama_check_auth`
- Check if the Panorama instance is accessible

### Auto-SSO not working

- Set `PANORAMA_SSO_ACCOUNT` to your AD username (e.g., `user@company.com`)
- The SSO Account field on Panorama's login page must match
- Some IDPs require MFA on every login — user interaction is needed

## License

MIT
