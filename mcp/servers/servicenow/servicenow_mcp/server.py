"""
ServiceNow MCP Server.

Implements Model Context Protocol over stdio using web scraping.
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional

from .scraper import ServiceNowScraper, ServiceNowScraperError


PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "servicenow"
SERVER_VERSION = "0.1.0"


# Prompt definitions for configuration
PROMPTS = [
    {
        "name": "configure_servicenow",
        "description": "Configure ServiceNow instance. SSO login will be handled via browser.",
        "arguments": [
            {
                "name": "instance",
                "description": "ServiceNow instance URL (e.g., mycompany.service-now.com)",
                "required": True
            }
        ]
    }
]


# Tool definitions
TOOLS = [
    {
        "name": "snow_incident_query",
        "description": "Query incidents with filters. Returns list of incidents matching criteria.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Encoded query (e.g., 'priority=1^state!=7' for P1 non-closed)"
                },
                "assignment_group": {
                    "type": "string",
                    "description": "Filter by assignment group name"
                },
                "state": {
                    "type": "string",
                    "enum": ["new", "in_progress", "on_hold", "resolved", "closed"],
                    "description": "Filter by incident state"
                },
                "priority": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5,
                    "description": "Filter by priority (1=Critical, 5=Planning)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum records to return (default: 50)"
                }
            }
        }
    },
    {
        "name": "snow_incident_get",
        "description": "Get incident details by number or sys_id",
        "inputSchema": {
            "type": "object",
            "properties": {
                "identifier": {
                    "type": "string",
                    "description": "Incident number (INC0012345) or sys_id"
                }
            },
            "required": ["identifier"]
        }
    },
    {
        "name": "snow_change_query",
        "description": "Query change requests with filters",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Encoded query string"
                },
                "type": {
                    "type": "string",
                    "enum": ["standard", "normal", "emergency"],
                    "description": "Change type filter"
                },
                "state": {
                    "type": "string",
                    "description": "Change state filter"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum records (default: 50)"
                }
            }
        }
    },
    {
        "name": "snow_change_get",
        "description": "Get change request details by number or sys_id",
        "inputSchema": {
            "type": "object",
            "properties": {
                "identifier": {
                    "type": "string",
                    "description": "Change number (CHG0012345) or sys_id"
                }
            },
            "required": ["identifier"]
        }
    },
    {
        "name": "snow_cmdb_query",
        "description": "Query CMDB configuration items",
        "inputSchema": {
            "type": "object",
            "properties": {
                "class": {
                    "type": "string",
                    "description": "CI class (cmdb_ci, cmdb_ci_server, cmdb_ci_app_server, cmdb_ci_database)"
                },
                "query": {
                    "type": "string",
                    "description": "Encoded query (e.g., 'operational_status=1^name LIKE prod')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum records (default: 50)"
                }
            },
            "required": ["class"]
        }
    },
    {
        "name": "snow_cmdb_get",
        "description": "Get CI details by name or sys_id",
        "inputSchema": {
            "type": "object",
            "properties": {
                "identifier": {
                    "type": "string",
                    "description": "CI name or sys_id"
                },
                "class": {
                    "type": "string",
                    "description": "CI class (optional, defaults to cmdb_ci)"
                }
            },
            "required": ["identifier"]
        }
    },
    {
        "name": "snow_user_query",
        "description": "Query ServiceNow users",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Encoded query (e.g., 'active=true^department LIKE IT')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum records (default: 50)"
                }
            }
        }
    },
    {
        "name": "snow_group_query",
        "description": "Query ServiceNow groups",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Encoded query"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum records (default: 50)"
                }
            }
        }
    },
    {
        "name": "snow_table_query",
        "description": "Query any ServiceNow table by name",
        "inputSchema": {
            "type": "object",
            "properties": {
                "table": {
                    "type": "string",
                    "description": "Table name (e.g., 'incident', 'cmdb_ci_server', 'sys_user')"
                },
                "query": {
                    "type": "string",
                    "description": "Encoded query string"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum records (default: 50)"
                }
            },
            "required": ["table"]
        }
    },
    {
        "name": "snow_kb_search",
        "description": "Search the ServiceNow knowledge base",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search text"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results (default: 50)"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "snow_configure",
        "description": "Configure ServiceNow instance. Call this before other snow_* tools. SSO login is handled via browser - a window will open for you to authenticate.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "instance": {
                    "type": "string",
                    "description": "ServiceNow instance URL (e.g., mycompany.service-now.com)"
                }
            },
            "required": ["instance"]
        }
    }
]


class CredentialsNotConfiguredError(Exception):
    """Raised when ServiceNow credentials are not configured."""
    pass


class MCPServer:
    """ServiceNow MCP Server."""

    def __init__(self):
        self.scraper: Optional[ServiceNowScraper] = None
        self._initialized = False
        # Runtime instance config (override env var)
        self._instance: Optional[str] = None

    def _get_instance(self) -> str:
        """Get instance from runtime config or environment."""
        return self._instance or os.environ.get("SERVICENOW_INSTANCE", "")

    def _check_instance(self):
        """Check if instance is configured, raise helpful error if not."""
        instance = self._get_instance()
        if not instance:
            raise CredentialsNotConfiguredError(
                "ServiceNow instance not configured. "
                "Use the 'snow_configure' tool to set the instance URL."
            )

    def _get_scraper(self) -> ServiceNowScraper:
        """Get or create scraper instance."""
        self._check_instance()

        if self.scraper is None:
            self.scraper = ServiceNowScraper(instance=self._get_instance())
        return self.scraper

    def handle_initialize(self, params: Dict) -> Dict:
        """Handle initialize request."""
        self._initialized = True
        return {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {
                "tools": {"listChanged": True},
                "prompts": {"listChanged": True}
            },
            "serverInfo": {
                "name": SERVER_NAME,
                "version": SERVER_VERSION
            }
        }

    def handle_tools_list(self, params: Dict) -> Dict:
        """Handle tools/list request."""
        return {"tools": TOOLS}

    def handle_tools_call(self, params: Dict) -> Dict:
        """Handle tools/call request."""
        name = params.get("name", "")
        arguments = params.get("arguments", {})

        try:
            result = self._execute_tool(name, arguments)
            return {
                "content": [
                    {"type": "text", "text": json.dumps(result, indent=2)}
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {"type": "text", "text": f"Error: {e}"}
                ],
                "isError": True
            }

    def handle_prompts_list(self, params: Dict) -> Dict:
        """Handle prompts/list request."""
        return {"prompts": PROMPTS}

    def handle_prompts_get(self, params: Dict) -> Dict:
        """Handle prompts/get request."""
        name = params.get("name", "")
        arguments = params.get("arguments", {})

        # Find the prompt
        prompt = None
        for p in PROMPTS:
            if p["name"] == name:
                prompt = p
                break

        if not prompt:
            raise ValueError(f"Unknown prompt: {name}")

        if name == "configure_servicenow":
            # Generate a message that guides the AI to configure instance
            instance = arguments.get("instance", "")

            messages = []

            if instance:
                # Instance provided - return instruction to call the tool
                messages.append({
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Configure ServiceNow connection to {instance}."
                    }
                })
                messages.append({
                    "role": "assistant",
                    "content": {
                        "type": "text",
                        "text": f"I'll configure the ServiceNow connection. Call snow_configure with instance='{instance}'. SSO login will be handled via browser - a window will open for you to authenticate."
                    }
                })
            else:
                # Prompt for instance
                messages.append({
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I need to configure my ServiceNow connection."
                    }
                })
                messages.append({
                    "role": "assistant",
                    "content": {
                        "type": "text",
                        "text": "To configure ServiceNow, I'll need your instance URL (e.g., mycompany.service-now.com). SSO login will be handled via browser."
                    }
                })

            return {
                "description": prompt.get("description", ""),
                "messages": messages
            }

        raise ValueError(f"Prompt implementation not found: {name}")

    def _execute_tool(self, name: str, args: Dict) -> Any:
        """Execute a tool by name."""
        # snow_configure doesn't need scraper
        if name == "snow_configure":
            return self._configure_credentials(args)

        scraper = self._get_scraper()

        if name == "snow_incident_query":
            return self._incident_query(scraper, args)
        elif name == "snow_incident_get":
            return scraper.get_record("incident", args["identifier"])
        elif name == "snow_change_query":
            return self._change_query(scraper, args)
        elif name == "snow_change_get":
            return scraper.get_record("change_request", args["identifier"])
        elif name == "snow_cmdb_query":
            return scraper.query_table(
                args.get("class", "cmdb_ci"),
                args.get("query"),
                args.get("limit", 50)
            )
        elif name == "snow_cmdb_get":
            table = args.get("class", "cmdb_ci")
            return scraper.get_record(table, args["identifier"])
        elif name == "snow_user_query":
            return scraper.query_table(
                "sys_user",
                args.get("query"),
                args.get("limit", 50)
            )
        elif name == "snow_group_query":
            return scraper.query_table(
                "sys_user_group",
                args.get("query"),
                args.get("limit", 50)
            )
        elif name == "snow_table_query":
            return scraper.query_table(
                args["table"],
                args.get("query"),
                args.get("limit", 50)
            )
        elif name == "snow_kb_search":
            return scraper.search_knowledge(
                args["query"],
                args.get("limit", 50)
            )
        else:
            raise ValueError(f"Unknown tool: {name}")

    def _configure_credentials(self, args: Dict) -> Dict:
        """Configure ServiceNow instance at runtime."""
        self._instance = args["instance"]

        # Close existing scraper so it reconnects with new instance
        if self.scraper:
            self.scraper.close()
            self.scraper = None

        return {
            "status": "configured",
            "instance": self._instance,
            "message": f"ServiceNow instance configured: {self._instance}. SSO login will occur on first tool use - a browser window will open for authentication."
        }

    def _incident_query(self, scraper: ServiceNowScraper, args: Dict) -> List[Dict]:
        """Build and execute incident query."""
        query_parts = []

        if args.get("query"):
            query_parts.append(args["query"])
        if args.get("assignment_group"):
            query_parts.append(f"assignment_group.name={args['assignment_group']}")
        if args.get("state"):
            state_map = {
                "new": "1", "in_progress": "2", "on_hold": "3",
                "resolved": "6", "closed": "7"
            }
            state_val = state_map.get(args["state"], args["state"])
            query_parts.append(f"state={state_val}")
        if args.get("priority"):
            query_parts.append(f"priority={args['priority']}")

        query = "^".join(query_parts) if query_parts else None
        return scraper.query_table("incident", query, args.get("limit", 50))

    def _change_query(self, scraper: ServiceNowScraper, args: Dict) -> List[Dict]:
        """Build and execute change query."""
        query_parts = []

        if args.get("query"):
            query_parts.append(args["query"])
        if args.get("type"):
            query_parts.append(f"type={args['type']}")
        if args.get("state"):
            query_parts.append(f"state={args['state']}")

        query = "^".join(query_parts) if query_parts else None
        return scraper.query_table("change_request", query, args.get("limit", 50))

    def handle_request(self, request: Dict) -> Optional[Dict]:
        """Handle a JSON-RPC request."""
        method = request.get("method", "")
        params = request.get("params", {})
        req_id = request.get("id")

        # Notifications don't get responses
        if req_id is None:
            return None

        try:
            if method == "initialize":
                result = self.handle_initialize(params)
            elif method == "tools/list":
                result = self.handle_tools_list(params)
            elif method == "tools/call":
                result = self.handle_tools_call(params)
            elif method == "prompts/list":
                result = self.handle_prompts_list(params)
            elif method == "prompts/get":
                result = self.handle_prompts_get(params)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": result
            }

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }

    def run(self):
        """Run the MCP server (stdio mode)."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
                response = self.handle_request(request)

                if response:
                    print(json.dumps(response), flush=True)

            except json.JSONDecodeError as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {e}"
                    }
                }
                print(json.dumps(error_response), flush=True)

    def close(self):
        """Cleanup resources."""
        if self.scraper:
            self.scraper.close()
            self.scraper = None


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="ServiceNow MCP Server")
    parser.add_argument("command", choices=["serve"], help="Command to run")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    args = parser.parse_args()

    if args.command == "serve":
        server = MCPServer()
        try:
            server.run()
        finally:
            server.close()


if __name__ == "__main__":
    main()
