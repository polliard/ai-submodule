# MCP Server Tests

Test suite for validating MCP server implementations.

## Quick Start

```bash
# Run all tests
./run_tests.sh

# Run specific server tests
./run_tests.sh gitignore
./run_tests.sh servicenow
```

## Setup

Tests use a Python virtual environment with pytest:

```bash
# Manual setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest -v
pytest test_gitignore.py -v
pytest test_servicenow.py -v
```

## Test Structure

| File                 | Purpose                                               |
| -------------------- | ----------------------------------------------------- |
| `mcp_client.py`      | Generic MCP client for testing any stdio-based server |
| `test_gitignore.py`  | Tests for gitignore MCP server                        |
| `test_servicenow.py` | Tests for servicenow MCP server                       |
| `conftest.py`        | Pytest fixtures and shared configuration              |

## Test Categories

### Protocol Tests

- Server initialization (JSON-RPC 2.0 handshake)
- tools/list response validation
- Error handling for invalid requests

### Tool Tests

- Each tool's input schema validation
- Tool execution and response format
- Error cases (missing required params, invalid values)

## Environment Variables

### ServiceNow Tests

ServiceNow tests require credentials:

```bash
export SERVICENOW_INSTANCE=mycompany.service-now.com
export SERVICENOW_USERNAME=admin
export SERVICENOW_PASSWORD=secret
```

Without credentials, ServiceNow tests are skipped.

## Adding New Server Tests

1. Create `test_<servername>.py`
2. Use `MCPClient` from `mcp_client.py`
3. Follow existing patterns for protocol and tool tests

```python
import pytest
from mcp_client import MCPClient

class TestMyServer:
    @pytest.fixture
    def client(self):
        client = MCPClient(["myserver", "serve"])
        yield client
        client.close()

    def test_initialize(self, client):
        result = client.initialize()
        assert result["serverInfo"]["name"] == "myserver"

    def test_tools_list(self, client):
        client.initialize()
        tools = client.list_tools()
        assert len(tools) > 0
```

## CI Integration

Tests exit with:

- `0` - All tests passed
- `1` - Test failures
- `5` - No tests collected (server binary missing)
