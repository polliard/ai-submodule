"""
MCP Client for testing stdio-based MCP servers.

Implements the Model Context Protocol (JSON-RPC 2.0 over stdio) for testing purposes.
"""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any, Dict, List, Optional


class MCPError(Exception):
    """MCP protocol error."""
    def __init__(self, code: int, message: str, data: Any = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"MCP Error {code}: {message}")


class MCPClient:
    """
    MCP client for testing stdio-based servers.

    Usage:
        client = MCPClient(["gitignore", "serve"])
        result = client.initialize()
        tools = client.list_tools()
        result = client.call_tool("gitignore_search", {"pattern": "go"})
        client.close()
    """

    PROTOCOL_VERSION = "2024-11-05"

    def __init__(self, command: List[str], env: Optional[Dict[str, str]] = None, cwd: Optional[str] = None):
        """
        Start an MCP server process.

        Args:
            command: Command and args to start server (e.g., ["gitignore", "serve"])
            env: Optional environment variables for the server process
            cwd: Working directory for the server process (default: current dir)
        """
        self.command = command
        self._request_id = 0
        self._initialized = False

        # Merge with current environment
        process_env = dict(__import__("os").environ)
        if env:
            process_env.update(env)

        try:
            self.process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=process_env,
                cwd=cwd,
                text=True,
            )
        except FileNotFoundError:
            raise FileNotFoundError(f"MCP server binary not found: {command[0]}")

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _send(self, method: str, params: Optional[Dict] = None, is_notification: bool = False) -> Optional[Dict]:
        """Send a JSON-RPC request/notification and optionally wait for response."""
        if is_notification:
            message = {
                "jsonrpc": "2.0",
                "method": method,
            }
            if params:
                message["params"] = params
        else:
            message = {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": method,
            }
            if params:
                message["params"] = params

        line = json.dumps(message) + "\n"
        self.process.stdin.write(line)
        self.process.stdin.flush()

        if is_notification:
            return None

        # Read response
        response_line = self.process.stdout.readline()
        if not response_line:
            stderr = self.process.stderr.read()
            raise MCPError(-32603, f"Server closed connection. stderr: {stderr}")

        response = json.loads(response_line)

        if "error" in response:
            err = response["error"]
            raise MCPError(err.get("code", -1), err.get("message", "Unknown error"), err.get("data"))

        return response.get("result")

    def initialize(
        self,
        client_name: str = "mcp-test-client",
        client_version: str = "1.0.0",
    ) -> dict:
        """
        Initialize the MCP connection.

        Returns:
            Server capabilities and info
        """
        result = self._send("initialize", {
            "protocolVersion": self.PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {
                "name": client_name,
                "version": client_version,
            },
        })

        # Send initialized notification
        self._send("notifications/initialized", is_notification=True)
        self._initialized = True

        return result

    def list_tools(self) -> List[Dict]:
        """
        List available tools from the server.

        Returns:
            List of tool definitions with name, description, inputSchema
        """
        if not self._initialized:
            raise MCPError(-32002, "Client not initialized. Call initialize() first.")

        result = self._send("tools/list")
        return result.get("tools", [])

    def call_tool(self, name: str, arguments: Optional[Dict] = None) -> Any:
        """
        Call a tool on the server.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            Tool result content
        """
        if not self._initialized:
            raise MCPError(-32002, "Client not initialized. Call initialize() first.")

        params = {"name": name}
        if arguments:
            params["arguments"] = arguments

        result = self._send("tools/call", params)
        return result

    def close(self):
        """Close the server connection."""
        if self.process:
            self.process.stdin.close()
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


def check_server_available(command: List[str]) -> bool:
    """Check if a server binary is available."""
    import shutil
    return shutil.which(command[0]) is not None


if __name__ == "__main__":
    # Quick test
    if len(sys.argv) < 2:
        print("Usage: python mcp_client.py <command> [args...]")
        print("Example: python mcp_client.py gitignore serve")
        sys.exit(1)

    command = sys.argv[1:]

    try:
        with MCPClient(command) as client:
            print(f"Connecting to: {' '.join(command)}")

            result = client.initialize()
            print(f"\n✓ Initialize: {result['serverInfo']['name']} v{result['serverInfo'].get('version', 'unknown')}")

            tools = client.list_tools()
            print(f"\n✓ Tools ({len(tools)}):")
            for tool in tools:
                print(f"  - {tool['name']}: {tool.get('description', '')[:60]}")

            print("\n✓ Server is working correctly!")
    except FileNotFoundError as e:
        print(f"✗ {e}")
        sys.exit(1)
    except MCPError as e:
        print(f"✗ MCP Error: {e}")
        sys.exit(1)
