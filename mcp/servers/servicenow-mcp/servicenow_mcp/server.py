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


# Tool definitions
TOOLS = [
    {
        "name": "snow_configure",
        "description": "Configure ServiceNow instance. Call this before other snow_* tools. SSO login is handled via browser - a window will open for you to authenticate.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "instance": {
                    "type": "string",
                    "description": "ServiceNow instance (e.g., mycompany.service-now.com)"
                }
            },
            "required": ["instance"]
        }
    },
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
        "description": "Query CMDB configuration items with optional pagination. Returns records and metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "class": {
                    "type": "string",
                    "description": "CI class (cmdb_ci, cmdb_ci_server, cmdb_ci_app_server, cmdb_ci_database, cmdb_ci_business_app)"
                },
                "query": {
                    "type": "string",
                    "description": "Encoded query (e.g., 'operational_status=1^name LIKE prod')"
                },
                "filters": {
                    "type": "array",
                    "description": "Structured filters (alternative to query string). Each filter: {field, operator, value}",
                    "items": {
                        "type": "object",
                        "properties": {
                            "field": {"type": "string", "description": "Field name (e.g., 'u_lob', 'operational_status')"},
                            "operator": {"type": "string", "description": "Operator: =, !=, LIKE, STARTSWITH, IN, ISEMPTY, etc."},
                            "value": {"type": "string", "description": "Value to compare"}
                        },
                        "required": ["field", "operator"]
                    }
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum records (default: 50, ignored if fetch_all=true)"
                },
                "offset": {
                    "type": "integer",
                    "description": "Starting row for pagination (0-indexed)"
                },
                "fetch_all": {
                    "type": "boolean",
                    "description": "Auto-paginate to fetch all matching records"
                },
                "page_size": {
                    "type": "integer",
                    "description": "Records per page when fetch_all=true (default: 200)"
                },
                "max_records": {
                    "type": "integer",
                    "description": "Safety limit when fetch_all=true (default: 10000)"
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
        "description": "Query any ServiceNow table by name with optional pagination. Returns records and metadata.",
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
                "filters": {
                    "type": "array",
                    "description": "Structured filters (alternative to query string). Each filter: {field, operator, value}",
                    "items": {
                        "type": "object",
                        "properties": {
                            "field": {"type": "string", "description": "Field name"},
                            "operator": {"type": "string", "description": "Operator: =, !=, LIKE, STARTSWITH, IN, ISEMPTY, etc."},
                            "value": {"type": "string", "description": "Value to compare"}
                        },
                        "required": ["field", "operator"]
                    }
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum records (default: 50, ignored if fetch_all=true)"
                },
                "offset": {
                    "type": "integer",
                    "description": "Starting row for pagination (0-indexed)"
                },
                "fetch_all": {
                    "type": "boolean",
                    "description": "Auto-paginate to fetch all matching records"
                },
                "page_size": {
                    "type": "integer",
                    "description": "Records per page when fetch_all=true (default: 200)"
                },
                "max_records": {
                    "type": "integer",
                    "description": "Safety limit when fetch_all=true (default: 10000)"
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
        "name": "snow_describe_table",
        "description": "Get field information for a ServiceNow table. Use this to discover available fields, their types, and whether they're mandatory before querying.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "table": {
                    "type": "string",
                    "description": "Table name (e.g., 'incident', 'cmdb_ci_business_app')"
                }
            },
            "required": ["table"]
        }
    },
    {
        "name": "snow_build_query",
        "description": "Build an encoded query string from structured filters. Use this to construct complex queries without knowing ServiceNow query syntax.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filters": {
                    "type": "array",
                    "description": "List of filter conditions",
                    "items": {
                        "type": "object",
                        "properties": {
                            "field": {
                                "type": "string",
                                "description": "Field name (e.g., 'u_lob', 'operational_status', 'name')"
                            },
                            "operator": {
                                "type": "string",
                                "enum": ["=", "!=", ">", ">=", "<", "<=", "LIKE", "STARTSWITH", "ENDSWITH", "IN", "NOT IN", "ISEMPTY", "ISNOTEMPTY"],
                                "description": "Comparison operator"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value to compare (not needed for ISEMPTY/ISNOTEMPTY)"
                            }
                        },
                        "required": ["field", "operator"]
                    }
                },
                "operator": {
                    "type": "string",
                    "enum": ["AND", "OR"],
                    "description": "Logical operator between conditions (default: AND)"
                }
            },
            "required": ["filters"]
        }
    }
]

# Prompts
PROMPTS = [
    {
        "name": "configure",
        "description": "Configure ServiceNow connection with SSO authentication",
        "arguments": [
            {
                "name": "instance",
                "description": "ServiceNow instance (e.g., mycompany.service-now.com)",
                "required": True
            }
        ]
    },
    {
        "name": "incident_triage",
        "description": "Analyze and triage incidents",
        "arguments": [
            {
                "name": "priority",
                "description": "Priority level (1-5)",
                "required": False
            }
        ]
    },
    {
        "name": "change_review",
        "description": "Review pending change requests",
        "arguments": []
    }
]


class MCPServer:
    """ServiceNow MCP Server."""

    def __init__(self):
        self.scraper: Optional[ServiceNowScraper] = None
        self._initialized = False
        self._instance: Optional[str] = None

    def _get_scraper(self) -> ServiceNowScraper:
        """Get or create scraper instance."""
        if self.scraper is None:
            self.scraper = ServiceNowScraper(instance=self._instance)
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

    def handle_prompts_list(self, params: Dict) -> Dict:
        """Handle prompts/list request."""
        return {"prompts": PROMPTS}

    def handle_prompts_get(self, params: Dict) -> Dict:
        """Handle prompts/get request."""
        name = params.get("name", "")
        arguments = params.get("arguments", {})

        if name == "configure":
            instance = arguments.get("instance", "your-instance.service-now.com")
            return {
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "type": "text",
                            "text": f"Configure ServiceNow connection to {instance}. Use SSO authentication - a browser window will open for you to complete the login."
                        }
                    }
                ]
            }
        elif name == "incident_triage":
            priority = arguments.get("priority", "")
            priority_filter = f" with priority {priority}" if priority else ""
            return {
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "type": "text",
                            "text": f"Query open incidents{priority_filter} and provide triage recommendations. For each incident, assess urgency and suggest next steps."
                        }
                    }
                ]
            }
        elif name == "change_review":
            return {
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "type": "text",
                            "text": "Review pending change requests. Analyze each for risk, completeness, and provide approval recommendations."
                        }
                    }
                ]
            }
        else:
            raise ValueError(f"Unknown prompt: {name}")

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

    def _execute_tool(self, name: str, args: Dict) -> Any:
        """Execute a tool by name."""
        if name == "snow_configure":
            return self._configure(args)

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
            return self._query_with_pagination(
                scraper,
                args.get("class", "cmdb_ci"),
                args
            )
        elif name == "snow_cmdb_get":
            table = args.get("class", "cmdb_ci")
            return scraper.get_record(table, args["identifier"])
        elif name == "snow_user_query":
            return self._query_with_pagination(scraper, "sys_user", args)
        elif name == "snow_group_query":
            return self._query_with_pagination(scraper, "sys_user_group", args)
        elif name == "snow_table_query":
            return self._query_with_pagination(scraper, args["table"], args)
        elif name == "snow_kb_search":
            return scraper.search_knowledge(
                args["query"],
                args.get("limit", 50)
            )
        elif name == "snow_describe_table":
            return scraper.describe_table(args["table"])
        elif name == "snow_build_query":
            return {
                "query": ServiceNowScraper.build_query(
                    args["filters"],
                    args.get("operator", "AND")
                )
            }
        else:
            raise ValueError(f"Unknown tool: {name}")

    def _query_with_pagination(
        self, scraper: ServiceNowScraper, table: str, args: Dict
    ) -> Dict:
        """Execute a query with pagination support."""
        # Build query from filters if provided
        query = args.get("query")
        if args.get("filters"):
            query = ServiceNowScraper.build_query(args["filters"])

        return scraper.query_table(
            table=table,
            query=query,
            limit=args.get("limit", 50),
            offset=args.get("offset", 0),
            fetch_all=args.get("fetch_all", False),
            page_size=args.get("page_size", 200),
            max_records=args.get("max_records", 10000),
        )

    def _configure(self, args: Dict) -> Dict:
        """Configure ServiceNow instance."""
        instance = args.get("instance", "")
        if not instance:
            raise ValueError("instance is required")

        # Close existing scraper if instance changed
        if self.scraper and self._instance != instance:
            self.scraper.close()
            self.scraper = None

        self._instance = instance

        # Test connection by getting scraper (triggers SSO if needed)
        scraper = self._get_scraper()

        return {
            "status": "configured",
            "instance": instance,
            "message": f"Connected to {instance}. SSO session active."
        }

    def _incident_query(self, scraper: ServiceNowScraper, args: Dict) -> Dict:
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
        return scraper.query_table(
            table="incident",
            query=query,
            limit=args.get("limit", 50),
        )

    def _change_query(self, scraper: ServiceNowScraper, args: Dict) -> Dict:
        """Build and execute change query."""
        query_parts = []

        if args.get("query"):
            query_parts.append(args["query"])
        if args.get("type"):
            query_parts.append(f"type={args['type']}")
        if args.get("state"):
            query_parts.append(f"state={args['state']}")

        query = "^".join(query_parts) if query_parts else None
        return scraper.query_table(
            table="change_request",
            query=query,
            limit=args.get("limit", 50),
        )

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
    parser.add_argument("command", choices=["serve", "login"], help="Command to run")
    parser.add_argument("--instance", help="ServiceNow instance")
    parser.add_argument("--no-preauth", action="store_true",
                        help="Skip pre-authentication check (handle SSO on-demand)")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    args = parser.parse_args()

    if args.command == "serve":
        instance = args.instance or os.environ.get("SERVICENOW_INSTANCE", "")

        # Pre-authenticate if no valid session exists (default behavior)
        if instance and not args.no_preauth:
            scraper = ServiceNowScraper(instance=instance, headless=False)
            try:
                if not scraper._is_session_valid():
                    # Use stderr for messages - stdout is for JSON-RPC
                    print(f"\nNo valid session for {instance}. Starting pre-authentication...", file=sys.stderr)
                    print("Complete SSO in the browser, then press ENTER.\n", file=sys.stderr)
                    scraper.login_interactive()
                    print("\nSession saved! Starting MCP server...\n", file=sys.stderr)
            except Exception as e:
                print(f"\nPre-authentication failed: {e}", file=sys.stderr)
                print("Starting server anyway - will prompt for SSO on first query.\n", file=sys.stderr)
            finally:
                scraper.close()

        server = MCPServer()
        try:
            server.run()
        finally:
            server.close()

    elif args.command == "login":
        # Standalone login - authenticate and save session for later use
        instance = args.instance or os.environ.get("SERVICENOW_INSTANCE", "")
        if not instance:
            print("Error: --instance required or set SERVICENOW_INSTANCE")
            sys.exit(1)

        print(f"\nLogging into {instance}...")
        print("Complete SSO in the browser. Session will be saved for reuse.\n")

        scraper = ServiceNowScraper(instance=instance, headless=False)
        try:
            scraper.login_interactive()
            print("\nSession saved! You can now run MCP queries without re-authenticating.")
        except Exception as e:
            print(f"\nLogin failed: {e}")
            sys.exit(1)
        finally:
            scraper.close()


if __name__ == "__main__":
    main()
