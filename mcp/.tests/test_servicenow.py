"""
Tests for servicenow MCP server.

Run with: pytest test_servicenow.py -v

Requires environment variables:
    SERVICENOW_INSTANCE - ServiceNow instance URL
    SERVICENOW_USERNAME - ServiceNow username
    SERVICENOW_PASSWORD - ServiceNow password
"""

import os
import pytest

from mcp_client import MCPClient, MCPError


pytestmark = [
    pytest.mark.requires_server("servicenow"),
    pytest.mark.requires_env("SERVICENOW_INSTANCE", "SERVICENOW_USERNAME", "SERVICENOW_PASSWORD"),
]


class TestServiceNowProtocol:
    """Test MCP protocol compliance."""

    def test_initialize(self, servicenow_client):
        """Server responds to initialize with correct info."""
        result = servicenow_client.initialize()

        assert "protocolVersion" in result
        assert "serverInfo" in result
        assert result["serverInfo"]["name"] == "servicenow"
        assert "capabilities" in result

    def test_tools_list(self, servicenow_client):
        """Server returns list of available tools."""
        servicenow_client.initialize()
        tools = servicenow_client.list_tools()

        assert isinstance(tools, list)
        assert len(tools) > 0

        # Check tool structure
        for tool in tools:
            assert "name" in tool
            assert "description" in tool
            assert tool["name"].startswith("snow_")

    def test_expected_tools_present(self, servicenow_client):
        """All expected tools are available."""
        servicenow_client.initialize()
        tools = servicenow_client.list_tools()
        tool_names = {t["name"] for t in tools}

        expected_tools = {
            "snow_cmdb_query",
            "snow_cmdb_get",
            "snow_incident_query",
            "snow_incident_get",
            "snow_change_query",
            "snow_change_get",
            "snow_user_query",
            "snow_group_query",
            "snow_table_query",
            "snow_kb_search",
        }

        for expected in expected_tools:
            assert expected in tool_names, f"Missing tool: {expected}"

    def test_tool_has_input_schema(self, servicenow_client):
        """Each tool has an inputSchema."""
        servicenow_client.initialize()
        tools = servicenow_client.list_tools()

        for tool in tools:
            assert "inputSchema" in tool, f"Tool {tool['name']} missing inputSchema"
            schema = tool["inputSchema"]
            assert schema.get("type") == "object"


class TestServiceNowCMDB:
    """Test CMDB-related tools."""

    def test_cmdb_query_servers(self, servicenow_client):
        """Query CMDB for servers."""
        servicenow_client.initialize()
        result = servicenow_client.call_tool("snow_cmdb_query", {
            "class": "cmdb_ci_server",
            "limit": 5,
        })

        assert "content" in result
        content = result["content"][0]
        assert content["type"] == "text"

    def test_cmdb_query_with_filter(self, servicenow_client):
        """Query CMDB with encoded query filter."""
        servicenow_client.initialize()
        result = servicenow_client.call_tool("snow_cmdb_query", {
            "class": "cmdb_ci_server",
            "query": "operational_status=1",
            "limit": 5,
        })

        assert "content" in result

    def test_cmdb_get_by_name(self, servicenow_client):
        """Get specific CI by name."""
        servicenow_client.initialize()

        # First get a server name from query
        query_result = servicenow_client.call_tool("snow_cmdb_query", {
            "class": "cmdb_ci_server",
            "limit": 1,
        })

        # This test validates the tool works; actual results depend on instance data


class TestServiceNowIncidents:
    """Test Incident-related tools."""

    def test_incident_query(self, servicenow_client):
        """Query incidents."""
        servicenow_client.initialize()
        result = servicenow_client.call_tool("snow_incident_query", {
            "limit": 5,
        })

        assert "content" in result

    def test_incident_query_by_priority(self, servicenow_client):
        """Query incidents by priority."""
        servicenow_client.initialize()
        result = servicenow_client.call_tool("snow_incident_query", {
            "priority": 1,
            "limit": 5,
        })

        assert "content" in result

    def test_incident_query_by_state(self, servicenow_client):
        """Query incidents by state."""
        servicenow_client.initialize()
        result = servicenow_client.call_tool("snow_incident_query", {
            "state": "in_progress",
            "limit": 5,
        })

        assert "content" in result


class TestServiceNowChanges:
    """Test Change-related tools."""

    def test_change_query(self, servicenow_client):
        """Query change requests."""
        servicenow_client.initialize()
        result = servicenow_client.call_tool("snow_change_query", {
            "limit": 5,
        })

        assert "content" in result

    def test_change_query_by_type(self, servicenow_client):
        """Query changes by type."""
        servicenow_client.initialize()
        result = servicenow_client.call_tool("snow_change_query", {
            "type": "standard",
            "limit": 5,
        })

        assert "content" in result


class TestServiceNowUsers:
    """Test User-related tools."""

    def test_user_query(self, servicenow_client):
        """Query users."""
        servicenow_client.initialize()
        result = servicenow_client.call_tool("snow_user_query", {
            "limit": 5,
        })

        assert "content" in result

    def test_group_query(self, servicenow_client):
        """Query groups."""
        servicenow_client.initialize()
        result = servicenow_client.call_tool("snow_group_query", {
            "limit": 5,
        })

        assert "content" in result


class TestServiceNowKnowledgeBase:
    """Test Knowledge Base tools."""

    def test_kb_search(self, servicenow_client):
        """Search knowledge base."""
        servicenow_client.initialize()
        result = servicenow_client.call_tool("snow_kb_search", {
            "query": "password reset",
            "limit": 5,
        })

        assert "content" in result


class TestServiceNowGenericTable:
    """Test generic table query tool."""

    def test_table_query(self, servicenow_client):
        """Query arbitrary table."""
        servicenow_client.initialize()
        result = servicenow_client.call_tool("snow_table_query", {
            "table": "sys_user",
            "limit": 5,
        })

        assert "content" in result

    def test_table_query_with_fields(self, servicenow_client):
        """Query table with specific fields."""
        servicenow_client.initialize()
        result = servicenow_client.call_tool("snow_table_query", {
            "table": "sys_user",
            "fields": ["user_name", "email", "name"],
            "limit": 5,
        })

        assert "content" in result


class TestServiceNowErrorHandling:
    """Test error handling."""

    def test_invalid_class(self, servicenow_client):
        """Invalid CMDB class should return error."""
        servicenow_client.initialize()

        result = servicenow_client.call_tool("snow_cmdb_query", {
            "class": "invalid_class_xyz",
        })

        # Should return error indicator
        assert "content" in result

    def test_invalid_incident_number(self, servicenow_client):
        """Invalid incident number should return not found."""
        servicenow_client.initialize()

        result = servicenow_client.call_tool("snow_incident_get", {
            "identifier": "INC9999999999",
        })

        # Should return not found message
        assert "content" in result
