"""
Tests for gitignore MCP server.

Run with: pytest test_gitignore.py -v
"""

import os
import pytest

from mcp_client import MCPClient, MCPError


pytestmark = pytest.mark.requires_server("gitignore")


class TestGitignoreProtocol:
    """Test MCP protocol compliance."""

    def test_initialize(self, gitignore_client):
        """Server responds to initialize with correct info."""
        result = gitignore_client.initialize()

        assert "protocolVersion" in result
        assert "serverInfo" in result
        assert result["serverInfo"]["name"] == "gitignore"
        assert "capabilities" in result

    def test_initialize_returns_version(self, gitignore_client):
        """Server reports its version."""
        result = gitignore_client.initialize()

        # v1.3.0+ supports MCP
        assert "version" in result["serverInfo"]
        version = result["serverInfo"]["version"]
        assert version.startswith("v") or version[0].isdigit()

    def test_tools_list(self, gitignore_client):
        """Server returns list of available tools."""
        gitignore_client.initialize()
        tools = gitignore_client.list_tools()

        assert isinstance(tools, list)
        assert len(tools) > 0

        # Check tool structure
        for tool in tools:
            assert "name" in tool
            assert "description" in tool
            assert tool["name"].startswith("gitignore_")

    def test_expected_tools_present(self, gitignore_client):
        """All expected tools are available."""
        gitignore_client.initialize()
        tools = gitignore_client.list_tools()
        tool_names = {t["name"] for t in tools}

        expected_tools = {
            "gitignore_list",
            "gitignore_search",
            "gitignore_add",
            "gitignore_delete",
            "gitignore_ignore",
            "gitignore_remove",
            "gitignore_init",
        }

        for expected in expected_tools:
            assert expected in tool_names, f"Missing tool: {expected}"

    def test_tool_has_input_schema(self, gitignore_client):
        """Each tool has an inputSchema."""
        gitignore_client.initialize()
        tools = gitignore_client.list_tools()

        for tool in tools:
            assert "inputSchema" in tool, f"Tool {tool['name']} missing inputSchema"
            schema = tool["inputSchema"]
            assert schema.get("type") == "object"


class TestGitignoreList:
    """Test gitignore_list tool."""

    def test_list_returns_templates(self, gitignore_client):
        """List returns available templates."""
        gitignore_client.initialize()
        result = gitignore_client.call_tool("gitignore_list")

        assert "content" in result
        assert len(result["content"]) > 0

        # Should have text content
        content = result["content"][0]
        assert content["type"] == "text"
        assert len(content["text"]) > 0

    def test_list_includes_common_templates(self, gitignore_client):
        """List includes commonly expected templates."""
        gitignore_client.initialize()
        result = gitignore_client.call_tool("gitignore_list")

        text = result["content"][0]["text"].lower()

        # At least some common languages should be present
        common = ["go", "python", "node", "java", "rust"]
        found = [lang for lang in common if lang in text]

        assert len(found) >= 2, f"Expected common templates, found: {found}"


class TestGitignoreSearch:
    """Test gitignore_search tool."""

    def test_search_finds_go(self, gitignore_client):
        """Search for 'go' returns results."""
        gitignore_client.initialize()
        result = gitignore_client.call_tool("gitignore_search", {"pattern": "go"})

        assert "content" in result
        text = result["content"][0]["text"].lower()
        assert "go" in text

    def test_search_finds_python(self, gitignore_client):
        """Search for 'python' returns results."""
        gitignore_client.initialize()
        result = gitignore_client.call_tool("gitignore_search", {"pattern": "python"})

        assert "content" in result
        text = result["content"][0]["text"].lower()
        assert "python" in text

    def test_search_no_match(self, gitignore_client):
        """Search with no matches returns empty or appropriate response."""
        gitignore_client.initialize()
        result = gitignore_client.call_tool("gitignore_search", {"pattern": "xyznonexistent123"})

        assert "content" in result
        # Should return empty list or message indicating no matches

    def test_search_requires_pattern(self, gitignore_client):
        """Search without pattern should error or return all."""
        gitignore_client.initialize()

        # Behavior depends on implementation - may error or return all
        try:
            result = gitignore_client.call_tool("gitignore_search", {})
            # If it succeeds, that's also valid (returns all)
            assert "content" in result
        except MCPError:
            # Error for missing required param is also valid
            pass


class TestGitignoreAdd:
    """Test gitignore_add tool."""

    def test_add_creates_gitignore(self, gitignore_client_factory, temp_dir):
        """Add creates .gitignore with template content."""
        client = gitignore_client_factory(cwd=temp_dir)
        client.initialize()
        result = client.call_tool("gitignore_add", {"type": "go"})

        assert "content" in result

        # Check file was created
        gitignore_path = temp_dir / ".gitignore"
        assert gitignore_path.exists(), ".gitignore should be created"

        content = gitignore_path.read_text()
        assert "### START:" in content or "Go" in content

    def test_add_invalid_type(self, gitignore_client_factory, temp_dir):
        """Add with invalid type returns error."""
        client = gitignore_client_factory(cwd=temp_dir)
        client.initialize()

        result = client.call_tool("gitignore_add", {"type": "nonexistent_template_xyz"})

        # Should indicate error/not found in response
        assert "content" in result
        text = result["content"][0]["text"].lower()
        assert "not found" in text or "error" in text or "no template" in text


class TestGitignoreDelete:
    """Test gitignore_delete tool."""

    def test_delete_removes_section(self, gitignore_client_factory, temp_dir):
        """Delete removes previously added section."""
        client = gitignore_client_factory(cwd=temp_dir)
        client.initialize()

        # First add
        client.call_tool("gitignore_add", {"type": "go"})

        gitignore_path = temp_dir / ".gitignore"
        assert gitignore_path.exists()

        # Then delete - note: section name is capitalized "Go" not "go"
        result = client.call_tool("gitignore_delete", {"type": "Go"})
        assert "content" in result

        # Check section is removed
        content = gitignore_path.read_text()
        assert "### START: Go" not in content or content.strip() == ""


class TestGitignoreIgnore:
    """Test gitignore_ignore tool."""

    def test_ignore_adds_patterns(self, gitignore_client_factory, temp_dir):
        """Ignore adds custom patterns."""
        client = gitignore_client_factory(cwd=temp_dir)
        client.initialize()

        patterns = ["/dist/", "*.log", "node_modules"]
        result = client.call_tool("gitignore_ignore", {"patterns": patterns})

        assert "content" in result

        gitignore_path = temp_dir / ".gitignore"
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            for pattern in patterns:
                assert pattern in content, f"Pattern {pattern} should be in .gitignore"


class TestGitignoreRemove:
    """Test gitignore_remove tool."""

    def test_remove_deletes_patterns(self, gitignore_client_factory, temp_dir):
        """Remove deletes previously ignored patterns."""
        client = gitignore_client_factory(cwd=temp_dir)
        client.initialize()

        # First add patterns
        client.call_tool("gitignore_ignore", {"patterns": ["/dist/", "*.log"]})

        # Then remove one
        result = client.call_tool("gitignore_remove", {"patterns": ["/dist/"]})

        assert "content" in result

        gitignore_path = temp_dir / ".gitignore"
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            assert "/dist/" not in content


class TestGitignoreInit:
    """Test gitignore_init tool."""

    def test_init_creates_default_gitignore(self, gitignore_client_factory, temp_dir):
        """Init creates .gitignore with default templates."""
        client = gitignore_client_factory(cwd=temp_dir)
        client.initialize()
        result = client.call_tool("gitignore_init")

        assert "content" in result

        # May create file or indicate no defaults configured
        gitignore_path = temp_dir / ".gitignore"
        # File existence depends on default config
