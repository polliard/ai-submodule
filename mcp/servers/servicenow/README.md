# ServiceNow MCP Server

MCP server for ServiceNow with SSO authentication via Playwright web scraping.

## Features

- **SSO Authentication**: Browser-based SSO login (Okta, Azure AD, ADFS, Ping, etc.)
- **Auto Pre-authentication**: Automatically prompts for SSO if no valid session exists
- **Session Caching**: Sessions cached for 8 hours at `~/.config/servicenow-mcp/`
- **Secure Storage**: Session files have restrictive permissions (0600)
- **11 Tools**: Query incidents, changes, CMDB, users, groups, KB articles
- **3 Prompts**: Configure, incident triage, change review

## Installation

```bash
cd mcp/servers/servicenow
pip install -e .
playwright install chromium
```

## Configuration

Set the ServiceNow instance:

```bash
export SERVICENOW_INSTANCE=mycompany.service-now.com
```

## Usage

### Start the MCP server (default with auto pre-auth)

```bash
servicenow-mcp serve
```

If no valid session exists, a browser window opens for SSO login. Complete the login and press ENTER. The session is saved for 8 hours.

### Skip pre-authentication

To handle SSO on-demand instead (old behavior):

```bash
servicenow-mcp serve --no-preauth
```

### Manual login (separate from serve)

```bash
servicenow-mcp login --instance mycompany.service-now.com
```

### VS Code MCP Configuration

Add to your MCP settings:

```json
{
  "servers": {
    "servicenow": {
      "command": "servicenow-mcp",
      "args": ["serve"],
      "env": {
        "SERVICENOW_INSTANCE": "mycompany.service-now.com"
      }
    }
  }
}
```

## Authentication Flow

### Default: Auto Pre-authentication

1. Run `servicenow-mcp serve`
2. If no valid session, browser opens automatically
3. Complete SSO login, press ENTER
4. Session saved for 8 hours
5. MCP server starts

### Alternative: On-demand with `--no-preauth`

1. Run `servicenow-mcp serve --no-preauth`
2. First tool call opens browser
3. Complete SSO login (10 minute timeout)
4. Session cached automatically

**Supported Identity Providers**: Okta, Azure AD, ADFS, Ping Identity, Auth0, OneLogin, Duo, Google

## Data Format

Query tools return JSON arrays with data scraped from ServiceNow list views:

```json
[
  {
    "sys_id": "00abed1a138c17405852d3228144b01c",
    "Name": "My Application",
    "Operational status": "Operational",
    "Business criticality": "High",
    "Owned by": "John Smith (jsmith)",
    "Managed by": "Jane Doe (jdoe)",
    "Description": "Application description..."
  }
]
```

Column names match the ServiceNow list view headers.

## Tools

### snow_configure

Configure the ServiceNow instance. Call this first if not set via environment variable.

```json
{"instance": "mycompany.service-now.com"}
```

### snow_incident_query

Query incidents with filters.

```json
{
  "query": "priority=1^state!=7",
  "assignment_group": "IT Support",
  "state": "in_progress",
  "priority": 1,
  "limit": 50
}
```

### snow_incident_get

Get incident details by number or sys_id.

```json
{"identifier": "INC0012345"}
```

### snow_change_query

Query change requests.

```json
{
  "type": "normal",
  "state": "scheduled",
  "limit": 50
}
```

### snow_change_get

Get change request details.

```json
{"identifier": "CHG0012345"}
```

### snow_cmdb_query

Query CMDB configuration items.

```json
{
  "class": "cmdb_ci_business_app",
  "query": "operational_status=1",
  "limit": 50
}
```

Common CMDB classes:

- `cmdb_ci_business_app` - Business applications
- `cmdb_ci_server` - Servers
- `cmdb_ci_app_server` - Application servers
- `cmdb_ci_database` - Databases

### snow_cmdb_get

Get CI details.

```json
{
  "identifier": "prod-web-01",
  "class": "cmdb_ci_server"
}
```

### snow_user_query

Query users.

```json
{
  "query": "active=true^department LIKE IT",
  "limit": 50
}
```

### snow_group_query

Query groups.

```json
{
  "query": "active=true",
  "limit": 50
}
```

### snow_table_query

Query any ServiceNow table.

```json
{
  "table": "sc_request",
  "query": "state=2",
  "limit": 50
}
```

### snow_kb_search

Search knowledge base.

```json
{
  "query": "password reset",
  "limit": 50
}
```

## Prompts

### configure

Start ServiceNow configuration workflow.

### incident_triage

Analyze open incidents and provide triage recommendations.

### change_review

Review pending change requests for risk assessment.

## CLI Commands

```bash
# Start MCP server (auto pre-auth if no session)
servicenow-mcp serve

# Start MCP server without pre-auth (handle SSO on-demand)
servicenow-mcp serve --no-preauth

# Manual login (saves session for later)
servicenow-mcp login --instance mycompany.service-now.com
```

## Troubleshooting

### SSO Redirects Away Before Login Completes

The default `serve` command now handles this by using interactive pre-authentication.
If you still have issues, use the standalone login:

```bash
servicenow-mcp login
```

This lets you complete SSO at your own pace, then press ENTER when done.

### Session Expired

Sessions auto-expire after 8 hours. Just run `serve` again - it will automatically prompt for re-authentication.

### Clear All Sessions

```bash
rm -rf ~/.config/servicenow-mcp/
```

### Playwright Not Installed

```bash
pip install playwright
playwright install chromium
```

## Security

- **No passwords stored** - SSO-only authentication
- **Session files** stored with 0600 permissions (owner read/write only)
- **Sessions expire** after 8 hours
- **Session directory**: `~/.config/servicenow-mcp/`
- **Browser visible** during authentication for security (you see what's happening)
