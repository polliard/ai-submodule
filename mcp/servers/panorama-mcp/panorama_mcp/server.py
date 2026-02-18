"""
Panorama MCP Server — multi-instance Palo Alto Panorama management via MCP.

Supports multiple Panorama deployments with browser-based SSO authentication.
Configure via PANORAMA_URLS (comma-separated) or PANORAMA_URL (single).
"""

import argparse
import asyncio
import json
import os
import sys
from typing import Optional
from urllib.parse import urlparse

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .browser import (
    PanoramaSession,
    close_all_sessions,
    close_session,
    clear_saved_session,
    ensure_authenticated,
    get_session,
    is_session_valid,
    login_interactive_sync,
)
from .scraper import PanoramaScraper


# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------
server = Server("panorama-mcp")

# Configuration
HEADLESS = os.environ.get("PANORAMA_HEADLESS", "false").lower() == "true"


def _parse_urls() -> list[str]:
    """Parse configured Panorama URLs from environment."""
    raw = os.environ.get("PANORAMA_URLS", "")
    if raw:
        return [u.strip().rstrip("/") for u in raw.split(",") if u.strip()]

    single = os.environ.get("PANORAMA_URL", "").strip().rstrip("/")
    if single:
        return [single]

    return []


def _configured_urls() -> list[str]:
    urls = _parse_urls()
    if not urls:
        raise ValueError(
            "No Panorama instances configured. "
            "Set PANORAMA_URLS (comma-separated) or PANORAMA_URL."
        )
    return urls


def _resolve_instance(instance: Optional[str] = None) -> str:
    """
    Resolve an instance hint to a full URL.

    The hint can be a full URL, hostname, or partial hostname substring.
    If None, returns the first configured URL.
    """
    urls = _configured_urls()

    if not instance:
        return urls[0]

    # Exact match
    hint = instance.strip().rstrip("/")
    for url in urls:
        if url == hint or urlparse(url).hostname == hint:
            return url

    # Partial / substring match
    hint_lower = hint.lower()
    for url in urls:
        host = (urlparse(url).hostname or "").lower()
        if hint_lower in host:
            return url

    raise ValueError(
        f"Instance '{instance}' not found in configured URLs: "
        + ", ".join(urls)
    )


def _instance_description() -> str:
    """Build a description snippet for the instance param."""
    urls = _parse_urls()
    if len(urls) <= 1:
        return "Panorama instance (optional if only one configured)"
    names = [urlparse(u).hostname or u for u in urls]
    return f"Panorama instance — one of: {', '.join(names)}. Partial match OK."


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------
@server.list_tools()
async def list_tools() -> list[Tool]:
    inst_desc = _instance_description()

    return [
        # ---- Instance management ----
        Tool(
            name="panorama_list_instances",
            description="List configured Panorama instances and their session status",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="panorama_login",
            description=(
                "Open browser for SSO login to Panorama. "
                "Auth state is saved for future sessions (8-hour TTL)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                    "timeout_seconds": {
                        "type": "integer",
                        "description": "SSO timeout in seconds (default: 300)",
                        "default": 300,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="panorama_check_auth",
            description="Check authentication status for a Panorama instance",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                },
                "required": [],
            },
        ),
        Tool(
            name="panorama_logout",
            description="Clear saved authentication for a Panorama instance",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                },
                "required": [],
            },
        ),
        # ---- Policies ----
        Tool(
            name="panorama_get_security_policies",
            description="Get security policies from Panorama for a device group",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                    "device_group": {
                        "type": "string",
                        "description": "Device group name (default: shared)",
                        "default": "shared",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="panorama_get_nat_policies",
            description="Get NAT policies from Panorama for a device group",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                    "device_group": {
                        "type": "string",
                        "description": "Device group name (default: shared)",
                        "default": "shared",
                    },
                },
                "required": [],
            },
        ),
        # ---- Logs ----
        Tool(
            name="panorama_get_traffic_logs",
            description="Get traffic logs from Panorama with optional filter query",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                    "query": {
                        "type": "string",
                        "description": "Log filter query (e.g., 'addr.src in 10.0.0.0/8')",
                        "default": "",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max logs to return (default: 100)",
                        "default": 100,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="panorama_get_threat_logs",
            description="Get threat logs from Panorama with optional filter query",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                    "query": {"type": "string", "description": "Log filter query", "default": ""},
                    "limit": {"type": "integer", "description": "Max logs (default: 100)", "default": 100},
                },
                "required": [],
            },
        ),
        Tool(
            name="panorama_get_system_logs",
            description="Get system logs from Panorama",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                    "query": {"type": "string", "description": "Log filter query", "default": ""},
                    "limit": {"type": "integer", "description": "Max logs (default: 100)", "default": 100},
                },
                "required": [],
            },
        ),
        # ---- Devices ----
        Tool(
            name="panorama_get_device_groups",
            description="Get list of device groups in Panorama",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                },
                "required": [],
            },
        ),
        Tool(
            name="panorama_get_managed_devices",
            description="Get list of managed firewalls in Panorama",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                },
                "required": [],
            },
        ),
        # ---- Operations ----
        Tool(
            name="panorama_commit",
            description="Commit pending changes in Panorama",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                    "device_group": {
                        "type": "string",
                        "description": "Device group (optional for Panorama-only commit)",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="panorama_push",
            description="Push configuration to devices in a device group",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                    "device_group": {
                        "type": "string",
                        "description": "Device group to push to",
                    },
                },
                "required": ["device_group"],
            },
        ),
        # ---- Browser control ----
        Tool(
            name="panorama_screenshot",
            description="Take a screenshot of the current Panorama page",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                    "save_path": {"type": "string", "description": "Optional path to save screenshot"},
                },
                "required": [],
            },
        ),
        Tool(
            name="panorama_navigate",
            description="Navigate to a specific page in Panorama",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                    "path": {
                        "type": "string",
                        "description": "Page path (e.g., 'policies/security', 'monitor/logs/traffic')",
                    },
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="panorama_page_snapshot",
            description="Get accessibility snapshot of current Panorama page for AI analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance": {"type": "string", "description": inst_desc},
                },
                "required": [],
            },
        ),
    ]


# ---------------------------------------------------------------------------
# Tool execution
# ---------------------------------------------------------------------------
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        result = await _execute_tool(name, arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]


async def _get_session_for(arguments: dict) -> PanoramaSession:
    """Resolve instance from arguments and return an authenticated session.

    Uses ensure_authenticated which handles SSO re-auth if the session
    has expired.  The browser is kept alive — Panorama uses session-only
    cookies that are lost when the browser closes.
    """
    url = _resolve_instance(arguments.get("instance"))
    session = await ensure_authenticated(url, headless=HEADLESS)
    if not session.is_authenticated:
        raise RuntimeError(
            f"Not authenticated to {session.instance_name}. "
            "Run 'panorama-mcp login' in a terminal or use the panorama_login tool."
        )
    return session


async def _execute_tool(name: str, arguments: dict) -> dict:

    # ---- Instance management ----
    if name == "panorama_list_instances":
        urls = _parse_urls()
        instances = []
        for url in urls:
            host = urlparse(url).hostname or url
            instances.append({
                "url": url,
                "hostname": host,
                "session_valid": is_session_valid(url),
            })
        return {"instances": instances, "count": len(instances)}

    if name == "panorama_login":
        url = _resolve_instance(arguments.get("instance"))
        timeout = arguments.get("timeout_seconds", 300)
        session = await get_session(url, headless=False)  # always visible for SSO
        return await session.wait_for_sso_login(timeout_seconds=timeout)

    if name == "panorama_check_auth":
        url = _resolve_instance(arguments.get("instance"))
        session = await get_session(url, headless=HEADLESS)
        is_authed = await session.check_login_status()
        return {
            "authenticated": is_authed,
            "panorama_url": url,
            "instance": session.instance_name,
            "session_valid": is_session_valid(url),
        }

    if name == "panorama_logout":
        url = _resolve_instance(arguments.get("instance"))
        await close_session(url)
        clear_saved_session(url)
        return {
            "success": True,
            "message": f"Logged out and cleared session for {urlparse(url).hostname}",
        }

    # ---- Policy tools ----
    if name == "panorama_get_security_policies":
        session = await _get_session_for(arguments)
        scraper = PanoramaScraper(session)
        dg = arguments.get("device_group", "shared")
        return {"device_group": dg, "policies": await scraper.get_security_policies(dg)}

    if name == "panorama_get_nat_policies":
        session = await _get_session_for(arguments)
        scraper = PanoramaScraper(session)
        dg = arguments.get("device_group", "shared")
        return {"device_group": dg, "nat_policies": await scraper.get_nat_policies(dg)}

    # ---- Log tools ----
    if name == "panorama_get_traffic_logs":
        session = await _get_session_for(arguments)
        scraper = PanoramaScraper(session)
        q, lim = arguments.get("query", ""), arguments.get("limit", 100)
        logs = await scraper.get_traffic_logs(q, lim)
        return {"query": q, "logs": logs, "count": len(logs)}

    if name == "panorama_get_threat_logs":
        session = await _get_session_for(arguments)
        scraper = PanoramaScraper(session)
        q, lim = arguments.get("query", ""), arguments.get("limit", 100)
        logs = await scraper.get_threat_logs(q, lim)
        return {"query": q, "logs": logs, "count": len(logs)}

    if name == "panorama_get_system_logs":
        session = await _get_session_for(arguments)
        scraper = PanoramaScraper(session)
        q, lim = arguments.get("query", ""), arguments.get("limit", 100)
        logs = await scraper.get_system_logs(q, lim)
        return {"query": q, "logs": logs, "count": len(logs)}

    # ---- Device tools ----
    if name == "panorama_get_device_groups":
        session = await _get_session_for(arguments)
        scraper = PanoramaScraper(session)
        return {"device_groups": await scraper.get_device_groups()}

    if name == "panorama_get_managed_devices":
        session = await _get_session_for(arguments)
        scraper = PanoramaScraper(session)
        return {"devices": await scraper.get_managed_devices()}

    # ---- Operations ----
    if name == "panorama_commit":
        session = await _get_session_for(arguments)
        scraper = PanoramaScraper(session)
        return await scraper.commit_changes(arguments.get("device_group"))

    if name == "panorama_push":
        session = await _get_session_for(arguments)
        scraper = PanoramaScraper(session)
        return await scraper.push_to_devices(arguments["device_group"])

    # ---- Browser control ----
    if name == "panorama_screenshot":
        session = await _get_session_for(arguments)
        save_path = arguments.get("save_path")
        if save_path:
            await session.take_screenshot(save_path)
            return {"success": True, "saved_to": save_path}
        import base64
        data = await session.take_screenshot()
        return {"success": True, "image_base64": base64.b64encode(data).decode()}

    if name == "panorama_navigate":
        session = await _get_session_for(arguments)
        path = arguments["path"]
        full_url = f"{session.panorama_url.rstrip('/')}/#" + path.lstrip("#/")
        await session.page.goto(full_url, wait_until="networkidle")
        return await session.get_page_info()

    if name == "panorama_page_snapshot":
        session = await _get_session_for(arguments)
        snapshot = await session.get_page_snapshot()
        return {"snapshot": snapshot, "url": session.page.url if session.page else ""}

    return {"error": f"Unknown tool: {name}"}


# ---------------------------------------------------------------------------
# MCP server entry point
# ---------------------------------------------------------------------------
async def _run_server(preauth: bool = False):
    """Run the MCP server over stdio.

    If preauth is True, authenticates all configured instances before
    starting the server.  The sessions stay alive for the server lifetime
    (Panorama uses session-only cookies that die with the browser).
    """
    if preauth:
        import sys as _sys
        urls = _parse_urls()
        for url in urls:
            host = urlparse(url).hostname
            print(f"  Authenticating {host}...", file=_sys.stderr)
            try:
                session = await ensure_authenticated(url, headless=HEADLESS)
                if session.is_authenticated:
                    print(f"  {host}: authenticated", file=_sys.stderr)
                else:
                    print(f"  {host}: auth failed — will retry on first tool call", file=_sys.stderr)
            except Exception as e:
                print(f"  {host}: error — {e}", file=_sys.stderr)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    """CLI entry point: serve, login, status."""
    parser = argparse.ArgumentParser(
        prog="panorama-mcp",
        description="Panorama MCP Server — Palo Alto Panorama management via MCP",
    )
    sub = parser.add_subparsers(dest="command")

    # --- serve ---
    serve_p = sub.add_parser("serve", help="Start the MCP server (default)")
    serve_p.add_argument(
        "--no-preauth",
        action="store_true",
        help="Skip pre-authentication; handle SSO on-demand during tool calls",
    )

    # --- login ---
    login_p = sub.add_parser("login", help="Interactive SSO login (saves session)")
    login_p.add_argument(
        "--instance",
        help="Panorama URL or hostname to authenticate to",
    )

    # --- status ---
    sub.add_parser("status", help="Show session status for all configured instances")

    args = parser.parse_args()
    command = args.command or "serve"

    if command == "serve":
        preauth = not getattr(args, "no_preauth", False)
        asyncio.run(_run_server(preauth=preauth))

    elif command == "login":
        instance_hint = args.instance
        urls = _parse_urls()

        if instance_hint:
            try:
                url = _resolve_instance(instance_hint)
            except ValueError:
                # Treat as a raw URL if not in configured list
                url = instance_hint.strip().rstrip("/")
                if not url.startswith("http"):
                    url = f"https://{url}"
        elif urls:
            url = urls[0]
        else:
            print("Error: --instance required or set PANORAMA_URLS / PANORAMA_URL")
            sys.exit(1)

        host = urlparse(url).hostname
        print(f"\nLogging into {host}...")
        print("Complete SSO in the browser.\n")
        print("NOTE: Panorama uses session-only cookies. The MCP server must be")
        print("started with 'serve' (not --no-preauth) to keep the session alive.\n")

        try:
            login_interactive_sync(url)
            print(f"\nSSO login completed for {host}.")
            print("Start the MCP server with: panorama-mcp serve")
        except Exception as e:
            print(f"\nLogin failed: {e}")
            sys.exit(1)

    elif command == "status":
        urls = _parse_urls()
        if not urls:
            print("No instances configured. Set PANORAMA_URLS or PANORAMA_URL.")
            sys.exit(0)

        for url in urls:
            host = urlparse(url).hostname
            valid = is_session_valid(url)
            status = "VALID" if valid else "EXPIRED / MISSING"
            print(f"  {host}: {status}")


def run():
    """Legacy entry point (backward compat)."""
    main()


if __name__ == "__main__":
    main()
