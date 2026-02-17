# ServiceNow MCP Server

Access ServiceNow CMDB, incidents, changes, problems, and other ITSM data directly from your AI assistant. Uses SSO authentication via browser.

## Installation

```bash
# Install from the servers directory
cd ~/.ai/mcp/servers/servicenow
pip install .

# Install Playwright browsers
playwright install chromium
```

## Configuration

Add to your `.vscode/mcp.json`:

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

### Environment Variables

| Variable              | Required | Description                                                  |
| --------------------- | -------- | ------------------------------------------------------------ |
| `SERVICENOW_INSTANCE` | ✓        | Your ServiceNow instance (e.g., `mycompany.service-now.com`) |

### SSO Authentication

When you first use a ServiceNow tool, a browser window will open for SSO login:

1. Complete your organization's SSO login in the browser
2. Once authenticated, the browser will close automatically
3. Your session is saved to `~/.config/servicenow-mcp/` for future use

Sessions are cached per-instance, so you won't need to log in again until the session expires.

### Runtime Configuration

If you don't set `SERVICENOW_INSTANCE` via environment, use the `snow_configure` tool:

```
Call snow_configure with instance="mycompany.service-now.com"
```

## Tools

### CMDB Tools

#### snow_cmdb_query

Query CMDB configuration items with filters.

**Parameters:**
| Name     | Type          | Required | Default                                              | Description                                                |
| -------- | ------------- | -------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| `class`  | string        | ✓        | —                                                    | CI class (e.g., `cmdb_ci_server`, `cmdb_ci_app_server`)    |
| `query`  | string        |          | —                                                    | Encoded query (e.g., `name=myserver^operational_status=1`) |
| `fields` | array[string] |          | `[name, sys_id, operational_status, sys_class_name]` | Fields to return                                           |
| `limit`  | integer       |          | `100`                                                | Maximum records                                            |

**Example prompts:**
- "Show me all production servers in the CMDB"
- "Find all databases with 'orders' in the name"
- "List application servers in the Finance business service"

**Example tool call:**
```json
{
  "class": "cmdb_ci_server",
  "query": "operational_status=1^install_status=1",
  "fields": ["name", "ip_address", "os", "location"],
  "limit": 50
}
```

---

#### snow_cmdb_get

Get a specific CI by sys_id or name.

**Parameters:**
| Name                | Type    | Required | Default | Description                               |
| ------------------- | ------- | -------- | ------- | ----------------------------------------- |
| `identifier`        | string  | ✓        | —       | sys_id or name of the CI                  |
| `class`             | string  |          | —       | CI class (searches all if not specified)  |
| `include_relations` | boolean |          | `false` | Include upstream/downstream relationships |

**Example prompts:**
- "Get details for server PRODWEB01"
- "Show me the CI relationships for the orders database"
- "What depends on the payment service?"

---

### Incident Tools

#### snow_incident_query

Query incidents with filters.

**Parameters:**
| Name               | Type    | Required | Default | Description                                                       |
| ------------------ | ------- | -------- | ------- | ----------------------------------------------------------------- |
| `query`            | string  |          | —       | Encoded query string                                              |
| `assignment_group` | string  |          | —       | Filter by assignment group                                        |
| `assigned_to`      | string  |          | —       | Filter by assigned user                                           |
| `state`            | string  |          | —       | `new`, `in_progress`, `on_hold`, `resolved`, `closed`, `canceled` |
| `priority`         | integer |          | —       | 1 (Critical) to 5 (Planning)                                      |
| `limit`            | integer |          | `50`    | Maximum records                                                   |

**Example prompts:**
- "Show me all P1 incidents"
- "What incidents are assigned to the Platform team?"
- "List my open incidents"
- "Find incidents related to the payment system"

**Example tool call:**
```json
{
  "priority": 1,
  "state": "in_progress",
  "assignment_group": "Platform Engineering",
  "limit": 20
}
```

---

#### snow_incident_get

Get incident details by number or sys_id.

**Parameters:**
| Name                | Type    | Required | Default | Description                            |
| ------------------- | ------- | -------- | ------- | -------------------------------------- |
| `identifier`        | string  | ✓        | —       | Incident number (INC0012345) or sys_id |
| `include_worknotes` | boolean |          | `false` | Include work notes and comments        |
| `include_related`   | boolean |          | `false` | Include related CIs, changes, problems |

**Example prompts:**
- "Get details for INC0012345"
- "Show me the work notes on that incident"
- "What CIs are affected by INC0098765?"

---

### Change Tools

#### snow_change_query

Query change requests with filters.

**Parameters:**
| Name                     | Type    | Required | Default | Description                                                                            |
| ------------------------ | ------- | -------- | ------- | -------------------------------------------------------------------------------------- |
| `query`                  | string  |          | —       | Encoded query string                                                                   |
| `type`                   | string  |          | —       | `standard`, `normal`, `emergency`                                                      |
| `state`                  | string  |          | —       | `new`, `assess`, `authorize`, `scheduled`, `implement`, `review`, `closed`, `canceled` |
| `assignment_group`       | string  |          | —       | Filter by assignment group                                                             |
| `scheduled_start_after`  | string  |          | —       | ISO date                                                                               |
| `scheduled_start_before` | string  |          | —       | ISO date                                                                               |
| `limit`                  | integer |          | `50`    | Maximum records                                                                        |

**Example prompts:**
- "What changes are scheduled for this week?"
- "Show me emergency changes from the last 30 days"
- "List changes waiting for approval"
- "Find changes affecting production databases"

**Example tool call:**
```json
{
  "type": "normal",
  "state": "scheduled",
  "scheduled_start_after": "2026-02-17",
  "scheduled_start_before": "2026-02-24"
}
```

---

#### snow_change_get

Get change request details.

**Parameters:**
| Name                   | Type    | Required | Default | Description                          |
| ---------------------- | ------- | -------- | ------- | ------------------------------------ |
| `identifier`           | string  | ✓        | —       | Change number (CHG0012345) or sys_id |
| `include_tasks`        | boolean |          | `false` | Include change tasks                 |
| `include_approvals`    | boolean |          | `false` | Include approval history             |
| `include_affected_cis` | boolean |          | `true`  | Include affected CIs                 |

**Example prompts:**
- "Get details for CHG0012345"
- "Show me the approval history for that change"
- "What tasks are left on CHG0098765?"

---

### Problem Tools

#### snow_problem_query

Query problems with filters.

**Parameters:**
| Name       | Type    | Required | Default | Description                                                                     |
| ---------- | ------- | -------- | ------- | ------------------------------------------------------------------------------- |
| `query`    | string  |          | —       | Encoded query string                                                            |
| `state`    | string  |          | —       | `new`, `assess`, `root_cause_analysis`, `fix_in_progress`, `resolved`, `closed` |
| `priority` | integer |          | —       | 1-5                                                                             |
| `limit`    | integer |          | `50`    | Maximum records                                                                 |

**Example prompts:**
- "Show me open problems"
- "What problems are in root cause analysis?"
- "List P1 problems from this month"

---

### User & Group Tools

#### snow_user_lookup

Look up a ServiceNow user.

**Parameters:**
| Name             | Type    | Required | Default | Description                |
| ---------------- | ------- | -------- | ------- | -------------------------- |
| `identifier`     | string  | ✓        | —       | Username, email, or sys_id |
| `include_groups` | boolean |          | `false` | Include group memberships  |

**Example prompts:**
- "Look up user john.smith"
- "What groups is jane.doe a member of?"

---

#### snow_group_members

List members of an assignment group.

**Parameters:**
| Name          | Type    | Required | Default | Description          |
| ------------- | ------- | -------- | ------- | -------------------- |
| `group`       | string  | ✓        | —       | Group name or sys_id |
| `active_only` | boolean |          | `true`  | Only active members  |

**Example prompts:**
- "Who is in the Platform Engineering group?"
- "List members of the CAB"

---

### Generic Query

#### snow_table_query

Query any ServiceNow table directly.

**Parameters:**
| Name     | Type          | Required | Default | Description                                   |
| -------- | ------------- | -------- | ------- | --------------------------------------------- |
| `table`  | string        | ✓        | —       | Table name (e.g., `sys_user`, `kb_knowledge`) |
| `query`  | string        |          | —       | Encoded query string                          |
| `fields` | array[string] |          | —       | Fields to return                              |
| `limit`  | integer       |          | `100`   | Maximum records                               |

**Example prompts:**
- "Search the knowledge base for articles about VPN"
- "List recent catalog requests"
- "Query the sys_audit table for changes to user records"

**Example tool call:**
```json
{
  "table": "kb_knowledge",
  "query": "textLIKEvpn^workflow_state=published",
  "fields": ["number", "short_description", "sys_updated_on"],
  "limit": 10
}
```

## Resources

| Resource            | URI                         | Description                      |
| ------------------- | --------------------------- | -------------------------------- |
| `instance_info`     | `servicenow://instance`     | Instance information and version |
| `cmdb_classes`      | `servicenow://cmdb/classes` | Available CMDB CI classes        |
| `assignment_groups` | `servicenow://groups`       | List of assignment groups        |

## Common Workflows

### Incident Investigation

1. "Show me P1 incidents from the last 24 hours"
2. "Get details for INC0012345 with work notes"
3. "What CIs are affected?"
4. "Are there related changes or problems?"

### Change Planning

1. "What changes are scheduled for this weekend?"
2. "Show me changes affecting the payment service"
3. "Get the approval status for CHG0012345"

### CMDB Exploration

1. "Find all servers in the orders application"
2. "Show me relationships for database ORDERSDB01"
3. "What depends on this CI?"

### On-Call Context

1. "What's assigned to me?"
2. "Show my team's open incidents"
3. "Any P1s I should know about?"

## ServiceNow Encoded Query Syntax

The `query` parameter uses ServiceNow's encoded query format:

| Operator     | Syntax                 | Example                      |
| ------------ | ---------------------- | ---------------------------- |
| Equals       | `field=value`          | `state=1`                    |
| Not equals   | `field!=value`         | `state!=7`                   |
| Contains     | `fieldLIKEvalue`       | `short_descriptionLIKEerror` |
| Starts with  | `fieldSTARTSWITHvalue` | `numberSTARTSWITHINC`        |
| Greater than | `field>value`          | `priority<3`                 |
| AND          | `^`                    | `state=1^priority=1`         |
| OR           | `^OR`                  | `state=1^ORstate=2`          |

Example: `priority=1^state!=7^assignment_group=Platform` (P1 incidents not closed, assigned to Platform)
