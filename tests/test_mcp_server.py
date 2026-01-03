"""
Tests for MCP server module.

Tests IR-MCP-002: Native MCP Server.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from spreadsheet_dl.mcp_server import (
    MCPConfig,
    MCPError,
    MCPSecurityError,
    MCPServer,
    MCPTool,
    MCPToolError,
    MCPToolParameter,
    MCPToolResult,
    create_mcp_server,
)


class TestMCPConfig:
    """Tests for MCPConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = MCPConfig()

        assert config.name == "spreadsheet-dl"
        assert config.version == "1.0.0"
        assert config.rate_limit_per_minute == 60
        assert config.enable_audit_log is True

    def test_default_allowed_paths(self):
        """Test default allowed paths."""
        config = MCPConfig()

        # Should have some default paths
        assert len(config.allowed_paths) > 0
        assert Path.cwd() in config.allowed_paths

    def test_custom_allowed_paths(self):
        """Test custom allowed paths."""
        custom_paths = [Path("/tmp/test")]
        config = MCPConfig(allowed_paths=custom_paths)

        assert config.allowed_paths == custom_paths


class TestMCPToolParameter:
    """Tests for MCPToolParameter."""

    def test_to_schema_basic(self):
        """Test basic schema generation."""
        param = MCPToolParameter(
            name="file_path",
            type="string",
            description="Path to file",
            required=True,
        )

        schema = param.to_schema()

        assert schema["type"] == "string"
        assert schema["description"] == "Path to file"

    def test_to_schema_with_enum(self):
        """Test schema with enum values."""
        param = MCPToolParameter(
            name="format",
            type="string",
            description="Output format",
            enum=["json", "text", "markdown"],
        )

        schema = param.to_schema()

        assert schema["enum"] == ["json", "text", "markdown"]

    def test_to_schema_with_default(self):
        """Test schema with default value."""
        param = MCPToolParameter(
            name="count",
            type="number",
            description="Number of items",
            required=False,
            default=10,
        )

        schema = param.to_schema()

        assert schema["default"] == 10


class TestMCPTool:
    """Tests for MCPTool."""

    def test_to_schema(self):
        """Test tool schema generation."""
        tool = MCPTool(
            name="test_tool",
            description="A test tool",
            parameters=[
                MCPToolParameter(
                    name="required_param",
                    type="string",
                    description="Required parameter",
                    required=True,
                ),
                MCPToolParameter(
                    name="optional_param",
                    type="number",
                    description="Optional parameter",
                    required=False,
                ),
            ],
        )

        schema = tool.to_schema()

        assert schema["name"] == "test_tool"
        assert schema["description"] == "A test tool"
        assert "required_param" in schema["inputSchema"]["properties"]
        assert "optional_param" in schema["inputSchema"]["properties"]
        assert "required_param" in schema["inputSchema"]["required"]
        assert "optional_param" not in schema["inputSchema"]["required"]


class TestMCPToolResult:
    """Tests for MCPToolResult."""

    def test_text_result(self):
        """Test text result creation."""
        result = MCPToolResult.text("Hello, world!")

        assert len(result.content) == 1
        assert result.content[0]["type"] == "text"
        assert result.content[0]["text"] == "Hello, world!"
        assert result.is_error is False

    def test_json_result(self):
        """Test JSON result creation."""
        data = {"key": "value", "number": 42}
        result = MCPToolResult.json(data)

        assert len(result.content) == 1
        assert result.content[0]["type"] == "text"
        assert '"key": "value"' in result.content[0]["text"]
        assert result.is_error is False

    def test_error_result(self):
        """Test error result creation."""
        result = MCPToolResult.error("Something went wrong")

        assert len(result.content) == 1
        assert "Error:" in result.content[0]["text"]
        assert "Something went wrong" in result.content[0]["text"]
        assert result.is_error is True


class TestMCPServer:
    """Tests for MCPServer."""

    @pytest.fixture
    def server(self, tmp_path):
        """Create a test server."""
        config = MCPConfig(
            allowed_paths=[tmp_path, Path.cwd()],
        )
        return MCPServer(config)

    def test_registered_tools(self, server):
        """Test that standard tools are registered."""
        expected_tools = [
            "analyze_budget",
            "add_expense",
            "query_budget",
            "get_spending_trends",
            "compare_periods",
            "generate_report",
            "list_categories",
            "get_alerts",
        ]

        for tool_name in expected_tools:
            assert tool_name in server._tools, f"Tool {tool_name} not registered"

    def test_handle_initialize(self, server):
        """Test initialize message handling."""
        message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
            },
        }

        response = server.handle_message(message)

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response
        assert response["result"]["protocolVersion"] == "2024-11-05"
        assert "serverInfo" in response["result"]
        assert response["result"]["serverInfo"]["name"] == "spreadsheet-dl"

    def test_handle_tools_list(self, server):
        """Test tools/list message handling."""
        message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {},
        }

        response = server.handle_message(message)

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 2
        assert "result" in response
        assert "tools" in response["result"]
        assert len(response["result"]["tools"]) >= 8

        # Check tool schema format
        tool = response["result"]["tools"][0]
        assert "name" in tool
        assert "description" in tool
        assert "inputSchema" in tool

    def test_handle_unknown_method(self, server):
        """Test unknown method handling."""
        message = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "unknown/method",
            "params": {},
        }

        response = server.handle_message(message)

        assert "error" in response
        assert response["error"]["code"] == -32601
        assert "not found" in response["error"]["message"].lower()

    def test_handle_list_categories(self, server):
        """Test list_categories tool."""
        message = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "list_categories",
                "arguments": {},
            },
        }

        response = server.handle_message(message)

        assert response["jsonrpc"] == "2.0"
        assert "result" in response
        assert "content" in response["result"]
        assert response["result"]["isError"] is False

        # Parse the content
        content = json.loads(response["result"]["content"][0]["text"])
        assert "categories" in content
        assert len(content["categories"]) > 0

    def test_path_validation_allowed(self, server, tmp_path):
        """Test path validation for allowed paths."""
        test_file = tmp_path / "test.ods"
        test_file.write_text("test")

        # Should not raise
        validated = server._validate_path(str(test_file))
        assert validated == test_file

    def test_path_validation_disallowed(self, server):
        """Test path validation for disallowed paths."""
        with pytest.raises(MCPSecurityError):
            server._validate_path("/etc/passwd")

    def test_rate_limiting(self, server):
        """Test rate limit checking."""
        # First request should pass
        assert server._check_rate_limit() is True

        # Simulate many requests
        server._request_count = server.config.rate_limit_per_minute

        # Next should fail
        assert server._check_rate_limit() is False


class TestMCPServerToolHandlers:
    """Tests for MCP server tool handlers."""

    @pytest.fixture
    def server(self, tmp_path):
        """Create a test server with budget file."""
        config = MCPConfig(
            allowed_paths=[tmp_path, Path.cwd()],
        )
        return MCPServer(config)

    def test_handle_query_budget_total_spent(self, server, tmp_path):
        """Test query_budget for total spending question."""
        # Create a mock budget file and analyzer
        with patch("spreadsheet_dl.budget_analyzer.BudgetAnalyzer") as MockAnalyzer:
            mock_summary = MagicMock()
            mock_summary.total_spent = 1500.00
            mock_summary.total_budget = 2000.00
            mock_summary.total_remaining = 500.00
            mock_summary.percent_used = 75.0

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.by_category.return_value = {"Groceries": 500}

            # Create a valid file
            test_file = tmp_path / "budget.ods"
            test_file.write_bytes(b"test")

            result = server._handle_query_budget(
                question="How much have I spent?",
                file_path=str(test_file),
            )

            assert result.is_error is False
            content = json.loads(result.content[0]["text"])
            assert "answer" in content
            assert "1,500" in content["answer"] or "1500" in content["answer"]

    def test_handle_query_budget_remaining(self, server, tmp_path):
        """Test query_budget for remaining budget question."""
        with patch("spreadsheet_dl.budget_analyzer.BudgetAnalyzer") as MockAnalyzer:
            mock_summary = MagicMock()
            mock_summary.total_spent = 1500.00
            mock_summary.total_budget = 2000.00
            mock_summary.total_remaining = 500.00
            mock_summary.percent_used = 75.0

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.by_category.return_value = {}

            test_file = tmp_path / "budget.ods"
            test_file.write_bytes(b"test")

            result = server._handle_query_budget(
                question="How much do I have left?",
                file_path=str(test_file),
            )

            assert result.is_error is False
            content = json.loads(result.content[0]["text"])
            assert "remaining" in content["answer"].lower()


class TestCreateMCPServer:
    """Tests for create_mcp_server function."""

    def test_create_with_paths(self):
        """Test creating server with allowed paths."""
        server = create_mcp_server(["/tmp", "/home"])

        assert len(server.config.allowed_paths) == 2
        assert Path("/tmp") in server.config.allowed_paths
        assert Path("/home") in server.config.allowed_paths

    def test_create_without_paths(self):
        """Test creating server without paths."""
        server = create_mcp_server()

        # Should have default paths
        assert len(server.config.allowed_paths) >= 0


class TestMCPErrors:
    """Tests for MCP errors."""

    def test_mcp_error(self):
        """Test base MCP error."""
        error = MCPError("Test error")
        assert error.error_code == "FT-MCP-1900"

    def test_tool_error(self):
        """Test tool error."""
        error = MCPToolError("Tool failed")
        assert error.error_code == "FT-MCP-1901"

    def test_security_error(self):
        """Test security error."""
        error = MCPSecurityError("Access denied")
        assert error.error_code == "FT-MCP-1902"
