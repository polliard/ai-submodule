"""
Pytest configuration and shared fixtures for MCP server tests.
"""

import os
import shutil
import sys
import pytest

from mcp_client import MCPClient, check_server_available


# Get the venv path for servicenow-mcp
_VENV_BIN = os.path.join(os.path.dirname(__file__), ".venv", "bin")

# Server configurations
SERVERS = {
    "gitignore": {
        "command": ["gitignore", "serve"],
        "env": None,
    },
    "servicenow": {
        # Use venv's servicenow-mcp to ensure we get the latest installed version
        # Use --no-preauth to handle SSO on-demand during tests
        "command": [os.path.join(_VENV_BIN, "servicenow-mcp"), "serve", "--no-preauth"],
        "env": {
            "SERVICENOW_INSTANCE": os.environ.get("SERVICENOW_INSTANCE", ""),
        },
    },
}


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "requires_server(name): skip if server binary is not available"
    )
    config.addinivalue_line(
        "markers", "requires_env(*vars): skip if environment variables are not set"
    )


def pytest_collection_modifyitems(config, items):
    """Apply skip markers based on server availability."""
    for item in items:
        # Check requires_server marker
        for marker in item.iter_markers(name="requires_server"):
            server_name = marker.args[0]
            if server_name in SERVERS:
                command = SERVERS[server_name]["command"]
                if not check_server_available(command):
                    item.add_marker(
                        pytest.mark.skip(
                            reason=f"Server binary not found: {command[0]}"
                        )
                    )

        # Check requires_env marker
        for marker in item.iter_markers(name="requires_env"):
            for var in marker.args:
                if not os.environ.get(var):
                    item.add_marker(
                        pytest.mark.skip(
                            reason=f"Environment variable not set: {var}"
                        )
                    )


@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for tests that modify files."""
    yield tmp_path


@pytest.fixture
def gitignore_client_factory():
    """Factory fixture for creating gitignore clients with custom cwd."""
    clients = []

    def _create(cwd=None):
        config = SERVERS["gitignore"]
        client = MCPClient(config["command"], config["env"], cwd=str(cwd) if cwd else None)
        clients.append(client)
        return client

    yield _create

    for client in clients:
        client.close()


@pytest.fixture
def gitignore_client(gitignore_client_factory):
    """Create a gitignore MCP client (default working directory)."""
    return gitignore_client_factory()


@pytest.fixture
def servicenow_client():
    """Create a servicenow MCP client."""
    config = SERVERS["servicenow"]
    client = MCPClient(config["command"], config["env"])
    yield client
    client.close()
