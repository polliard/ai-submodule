"""
Panorama MCP Server - Main server implementation.

This server provides tools for managing Palo Alto Panorama through
browser-based SSO authentication.
"""

import asyncio
import os
from typing import Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .browser import get_session, close_session, PanoramaSession
from .scraper import PanoramaScraper


# Server instance
server = Server("panorama-mcp")

# Configuration from environment
PANORAMA_URL = os.environ.get("PANORAMA_URL", "")
HEADLESS = os.environ.get("PANORAMA_HEADLESS", "false").lower() == "true"


def get_panorama_url() -> str:
    """Get configured Panorama URL."""
    if not PANORAMA_URL:
        raise ValueError("PANORAMA_URL environment variable not set")
    return PANORAMA_URL


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available Panorama tools."""
    return [
        # Authentication
        Tool(
            name="panorama_login",
            description="Open browser for SSO login to Panorama. The browser will open and wait for you to complete the SSO authentication flow. Auth state is saved for future sessions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "panorama_url": {
                        "type": "string",
                        "description": "Panorama URL (optional if PANORAMA_URL env var is set)"
                    },
                    "timeout_seconds": {
                        "type": "integer",
                        "description": "Timeout waiting for SSO login completion (default: 300)",
                        "default": 300
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="panorama_check_auth",
            description="Check if currently authenticated to Panorama",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="panorama_logout",
            description="Close browser session and clear saved authentication",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),

        # Policy Management
        Tool(
            name="panorama_get_security_policies",
            description="Get security policies from Panorama for a device group",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_group": {
                        "type": "string",
                        "description": "Device group name (default: shared)",
                        "default": "shared"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="panorama_get_nat_policies",
            description="Get NAT policies from Panorama for a device group",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_group": {
                        "type": "string",
                        "description": "Device group name (default: shared)",
                        "default": "shared"
                    }
                },
                "required": []
            }
        ),

        # Log Monitoring
        Tool(
            name="panorama_get_traffic_logs",
            description="Get traffic logs from Panorama with optional filter query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Log filter query (e.g., 'addr.src in 10.0.0.0/8')",
                        "default": ""
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of logs to return (default: 100)",
                        "default": 100
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="panorama_get_threat_logs",
            description="Get threat logs from Panorama with optional filter query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Log filter query",
                        "default": ""
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of logs to return (default: 100)",
                        "default": 100
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="panorama_get_system_logs",
            description="Get system logs from Panorama",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Log filter query",
                        "default": ""
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of logs to return (default: 100)",
                        "default": 100
                    }
                },
                "required": []
            }
        ),

        # Device Management
        Tool(
            name="panorama_get_device_groups",
            description="Get list of device groups in Panorama",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="panorama_get_managed_devices",
            description="Get list of managed firewalls in Panorama",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),

        # Operations
        Tool(
            name="panorama_commit",
            description="Commit pending changes in Panorama",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_group": {
                        "type": "string",
                        "description": "Device group to commit (optional for Panorama-only commit)"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="panorama_push",
            description="Push configuration to devices in a device group",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_group": {
                        "type": "string",
                        "description": "Device group to push to"
                    }
                },
                "required": ["device_group"]
            }
        ),

        # Browser Control
        Tool(
            name="panorama_screenshot",
            description="Take a screenshot of the current Panorama page",
            inputSchema={
                "type": "object",
                "properties": {
                    "save_path": {
                        "type": "string",
                        "description": "Optional path to save screenshot"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="panorama_navigate",
            description="Navigate to a specific page in Panorama",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Page path (e.g., 'policies/security', 'monitor/logs/traffic', 'panorama/device_groups')"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="panorama_page_snapshot",
            description="Get accessibility snapshot of current Panorama page for AI analysis",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    import json

    try:
        result = await _execute_tool(name, arguments)
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, default=str)
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2)
        )]


async def _execute_tool(name: str, arguments: dict) -> dict:
    """Execute the specified tool."""

    # Authentication tools
    if name == "panorama_login":
        url = arguments.get("panorama_url") or get_panorama_url()
        timeout = arguments.get("timeout_seconds", 300)

        session = await get_session(url, headless=False)  # Always non-headless for SSO
        return await session.wait_for_sso_login(timeout_seconds=timeout)

    elif name == "panorama_check_auth":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        is_authenticated = await session.check_login_status()
        return {
            "authenticated": is_authenticated,
            "panorama_url": url,
            "has_saved_state": session.storage_path.exists()
        }

    elif name == "panorama_logout":
        await close_session()
        from pathlib import Path
        storage_path = Path.home() / ".panorama_mcp" / "auth_state.json"
        if storage_path.exists():
            storage_path.unlink()
        return {"success": True, "message": "Logged out and cleared saved authentication"}

    # Policy tools
    elif name == "panorama_get_security_policies":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        scraper = PanoramaScraper(session)
        device_group = arguments.get("device_group", "shared")
        policies = await scraper.get_security_policies(device_group)
        return {"device_group": device_group, "policies": policies}

    elif name == "panorama_get_nat_policies":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        scraper = PanoramaScraper(session)
        device_group = arguments.get("device_group", "shared")
        policies = await scraper.get_nat_policies(device_group)
        return {"device_group": device_group, "nat_policies": policies}

    # Log monitoring tools
    elif name == "panorama_get_traffic_logs":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        scraper = PanoramaScraper(session)
        query = arguments.get("query", "")
        limit = arguments.get("limit", 100)
        logs = await scraper.get_traffic_logs(query, limit)
        return {"query": query, "logs": logs, "count": len(logs)}

    elif name == "panorama_get_threat_logs":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        scraper = PanoramaScraper(session)
        query = arguments.get("query", "")
        limit = arguments.get("limit", 100)
        logs = await scraper.get_threat_logs(query, limit)
        return {"query": query, "logs": logs, "count": len(logs)}

    elif name == "panorama_get_system_logs":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        scraper = PanoramaScraper(session)
        query = arguments.get("query", "")
        limit = arguments.get("limit", 100)
        logs = await scraper.get_system_logs(query, limit)
        return {"query": query, "logs": logs, "count": len(logs)}

    # Device management tools
    elif name == "panorama_get_device_groups":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        scraper = PanoramaScraper(session)
        groups = await scraper.get_device_groups()
        return {"device_groups": groups}

    elif name == "panorama_get_managed_devices":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        scraper = PanoramaScraper(session)
        devices = await scraper.get_managed_devices()
        return {"devices": devices}

    # Operations
    elif name == "panorama_commit":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        scraper = PanoramaScraper(session)
        device_group = arguments.get("device_group")
        return await scraper.commit_changes(device_group)

    elif name == "panorama_push":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        scraper = PanoramaScraper(session)
        device_group = arguments["device_group"]
        return await scraper.push_to_devices(device_group)

    # Browser control
    elif name == "panorama_screenshot":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        save_path = arguments.get("save_path")

        if save_path:
            await session.take_screenshot(save_path)
            return {"success": True, "saved_to": save_path}
        else:
            import base64
            screenshot = await session.take_screenshot()
            return {
                "success": True,
                "image_base64": base64.b64encode(screenshot).decode()
            }

    elif name == "panorama_navigate":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        path = arguments["path"]

        full_url = f"{url.rstrip('/')}/#" + path.lstrip('#/')
        await session.page.goto(full_url, wait_until="networkidle")
        return await session.get_page_info()

    elif name == "panorama_page_snapshot":
        url = get_panorama_url()
        session = await get_session(url, headless=HEADLESS)
        snapshot = await session.get_page_snapshot()
        return {"snapshot": snapshot, "url": session.page.url if session.page else ""}

    else:
        return {"error": f"Unknown tool: {name}"}


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


def run():
    """Entry point for the server."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
