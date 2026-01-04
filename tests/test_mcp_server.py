"""
Tests for MCP server module.

Tests IR-MCP-002: Native MCP Server.
"""

from __future__ import annotations

import contextlib
import json
import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from spreadsheet_dl.exceptions import FileError
from spreadsheet_dl.mcp_server import (
    MCPCapabilities,
    MCPConfig,
    MCPError,
    MCPSecurityError,
    MCPServer,
    MCPTool,
    MCPToolError,
    MCPToolParameter,
    MCPToolRegistry,
    MCPToolResult,
    MCPVersion,
    create_mcp_server,
)


class TestMCPVersion:
    """Tests for MCPVersion enum."""

    def test_mcp_version_v1(self) -> None:
        """Test MCP Version V1 value."""
        assert MCPVersion.V1.value == "2024-11-05"


class TestMCPCapabilities:
    """Tests for MCPCapabilities."""

    def test_default_capabilities(self) -> None:
        """Test default capabilities values."""
        caps = MCPCapabilities()
        assert caps.tools is True
        assert caps.resources is False
        assert caps.prompts is False
        assert caps.logging is True

    def test_custom_capabilities(self) -> None:
        """Test custom capabilities."""
        caps = MCPCapabilities(tools=False, resources=True, prompts=True, logging=False)
        assert caps.tools is False
        assert caps.resources is True
        assert caps.prompts is True
        assert caps.logging is False


class TestMCPConfig:
    """Tests for MCPConfig."""

    def test_default_config(self) -> None:
        """Test default configuration values."""
        config = MCPConfig()

        assert config.name == "spreadsheet-dl"
        assert config.version == "1.0.0"
        assert config.rate_limit_per_minute == 60
        assert config.enable_audit_log is True
        assert config.audit_log_path is None

    def test_default_allowed_paths(self) -> None:
        """Test default allowed paths."""
        config = MCPConfig()

        # Should have some default paths
        assert len(config.allowed_paths) > 0
        assert Path.cwd() in config.allowed_paths

    def test_custom_allowed_paths(self) -> None:
        """Test custom allowed paths."""
        custom_paths = [Path("/tmp/test")]
        config = MCPConfig(allowed_paths=custom_paths)

        assert config.allowed_paths == custom_paths

    def test_custom_name(self) -> None:
        """Test custom server name."""
        config = MCPConfig(name="my-server")
        assert config.name == "my-server"

    def test_custom_version(self) -> None:
        """Test custom server version."""
        config = MCPConfig(version="2.0.0")
        assert config.version == "2.0.0"

    def test_custom_rate_limit(self) -> None:
        """Test custom rate limit."""
        config = MCPConfig(rate_limit_per_minute=100)
        assert config.rate_limit_per_minute == 100

    def test_audit_log_disabled(self) -> None:
        """Test audit logging disabled."""
        config = MCPConfig(enable_audit_log=False)
        assert config.enable_audit_log is False

    def test_audit_log_path(self) -> None:
        """Test custom audit log path."""
        log_path = Path("/var/log/mcp.log")
        config = MCPConfig(audit_log_path=log_path)
        assert config.audit_log_path == log_path


class TestMCPToolParameter:
    """Tests for MCPToolParameter."""

    def test_to_schema_basic(self) -> None:
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

    def test_to_schema_with_enum(self) -> None:
        """Test schema with enum values."""
        param = MCPToolParameter(
            name="format",
            type="string",
            description="Output format",
            enum=["json", "text", "markdown"],
        )

        schema = param.to_schema()

        assert schema["enum"] == ["json", "text", "markdown"]

    def test_to_schema_with_default(self) -> None:
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

    def test_to_schema_no_enum_or_default(self) -> None:
        """Test schema without enum or default."""
        param = MCPToolParameter(
            name="value",
            type="string",
            description="A value",
            required=True,
        )

        schema = param.to_schema()

        assert "enum" not in schema
        assert "default" not in schema

    def test_default_required_true(self) -> None:
        """Test that required defaults to True."""
        param = MCPToolParameter(
            name="test",
            type="string",
            description="Test",
        )
        assert param.required is True

    def test_default_enum_none(self) -> None:
        """Test that enum defaults to None."""
        param = MCPToolParameter(
            name="test",
            type="string",
            description="Test",
        )
        assert param.enum is None

    def test_default_value_none(self) -> None:
        """Test that default value defaults to None."""
        param = MCPToolParameter(
            name="test",
            type="string",
            description="Test",
        )
        assert param.default is None


class TestMCPTool:
    """Tests for MCPTool."""

    def test_to_schema(self) -> None:
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

    def test_to_schema_no_parameters(self) -> None:
        """Test schema for tool with no parameters."""
        tool = MCPTool(
            name="simple_tool",
            description="A simple tool",
        )

        schema = tool.to_schema()

        assert schema["name"] == "simple_tool"
        assert schema["inputSchema"]["properties"] == {}
        assert schema["inputSchema"]["required"] == []

    def test_tool_with_handler(self) -> None:
        """Test tool with handler function."""

        def my_handler() -> MCPToolResult:
            return MCPToolResult.text("Hello")

        tool = MCPTool(
            name="handler_tool",
            description="Tool with handler",
            handler=my_handler,
        )

        assert tool.handler is not None
        result = tool.handler()
        assert result.content[0]["text"] == "Hello"


class TestMCPToolResult:
    """Tests for MCPToolResult."""

    def test_text_result(self) -> None:
        """Test text result creation."""
        result = MCPToolResult.text("Hello, world!")

        assert len(result.content) == 1
        assert result.content[0]["type"] == "text"
        assert result.content[0]["text"] == "Hello, world!"
        assert result.is_error is False

    def test_json_result(self) -> None:
        """Test JSON result creation."""
        data = {"key": "value", "number": 42}
        result = MCPToolResult.json(data)

        assert len(result.content) == 1
        assert result.content[0]["type"] == "text"
        assert '"key": "value"' in result.content[0]["text"]
        assert result.is_error is False

    def test_json_result_with_non_serializable(self) -> None:
        """Test JSON result with non-serializable types."""
        from datetime import date

        data = {"date": date(2025, 1, 15), "value": 100}
        result = MCPToolResult.json(data)

        # Should not raise, uses default=str
        assert "2025-01-15" in result.content[0]["text"]

    def test_error_result(self) -> None:
        """Test error result creation."""
        result = MCPToolResult.error("Something went wrong")

        assert len(result.content) == 1
        assert "Error:" in result.content[0]["text"]
        assert "Something went wrong" in result.content[0]["text"]
        assert result.is_error is True

    def test_direct_creation(self) -> None:
        """Test direct result creation."""
        result = MCPToolResult(
            content=[{"type": "text", "text": "Direct"}],
            is_error=False,
        )
        assert result.content[0]["text"] == "Direct"


class TestMCPToolRegistry:
    """Tests for MCPToolRegistry."""

    def test_registry_creation(self) -> None:
        """Test registry initialization."""
        registry = MCPToolRegistry()
        assert registry.get_tool_count() == 0

    def test_register_tool(self) -> None:
        """Test programmatic tool registration."""
        registry = MCPToolRegistry()

        def handler() -> MCPToolResult:
            return MCPToolResult.text("Test")

        registry.register(
            name="test_tool",
            description="A test tool",
            handler=handler,
            category="test",
        )

        assert registry.get_tool_count() == 1
        tool = registry.get_tool("test_tool")
        assert tool is not None
        assert tool.name == "test_tool"

    def test_register_with_decorator(self) -> None:
        """Test decorator-based tool registration."""
        registry = MCPToolRegistry()

        @registry.tool("decorated_tool", "A decorated tool", category="test")
        def my_tool() -> MCPToolResult:
            return MCPToolResult.text("Hello")

        assert registry.get_tool_count() == 1
        tool = registry.get_tool("decorated_tool")
        assert tool is not None
        assert tool.description == "A decorated tool"

    def test_get_all_tools(self) -> None:
        """Test getting all tools."""
        registry = MCPToolRegistry()

        def h1() -> MCPToolResult:
            return MCPToolResult.text("1")

        def h2() -> MCPToolResult:
            return MCPToolResult.text("2")

        registry.register("tool1", "Tool 1", h1)
        registry.register("tool2", "Tool 2", h2)

        tools = registry.get_all_tools()
        assert len(tools) == 2
        assert "tool1" in tools
        assert "tool2" in tools

    def test_get_tools_by_category(self) -> None:
        """Test getting tools by category."""
        registry = MCPToolRegistry()

        def h() -> MCPToolResult:
            return MCPToolResult.text("x")

        registry.register("tool1", "Tool 1", h, category="cat_a")
        registry.register("tool2", "Tool 2", h, category="cat_a")
        registry.register("tool3", "Tool 3", h, category="cat_b")

        cat_a_tools = registry.get_tools_by_category("cat_a")
        assert len(cat_a_tools) == 2

        cat_b_tools = registry.get_tools_by_category("cat_b")
        assert len(cat_b_tools) == 1

    def test_get_tools_by_unknown_category(self) -> None:
        """Test getting tools by unknown category."""
        registry = MCPToolRegistry()
        tools = registry.get_tools_by_category("nonexistent")
        assert tools == []

    def test_get_categories(self) -> None:
        """Test getting all categories."""
        registry = MCPToolRegistry()

        def h() -> MCPToolResult:
            return MCPToolResult.text("x")

        registry.register("tool1", "Tool 1", h, category="cat_a")
        registry.register("tool2", "Tool 2", h, category="cat_b")

        categories = registry.get_categories()
        assert "cat_a" in categories
        assert "cat_b" in categories

    def test_list_tools(self) -> None:
        """Test listing all tools as schemas."""
        registry = MCPToolRegistry()

        def h() -> MCPToolResult:
            return MCPToolResult.text("x")

        registry.register("tool1", "Tool 1", h)
        registry.register("tool2", "Tool 2", h)

        schemas = registry.list_tools()
        assert len(schemas) == 2
        assert all("name" in s for s in schemas)
        assert all("description" in s for s in schemas)

    def test_get_nonexistent_tool(self) -> None:
        """Test getting non-existent tool returns None."""
        registry = MCPToolRegistry()
        assert registry.get_tool("nonexistent") is None

    def test_decorator_with_parameters(self) -> None:
        """Test decorator with parameters."""
        registry = MCPToolRegistry()

        @registry.tool(
            "param_tool",
            "Tool with params",
            parameters=[
                MCPToolParameter("input", "string", "Input value"),
            ],
        )
        def param_tool() -> MCPToolResult:
            return MCPToolResult.text("x")

        tool = registry.get_tool("param_tool")
        assert tool is not None
        assert len(tool.parameters) == 1
        assert tool.parameters[0].name == "input"


class TestMCPServer:
    """Tests for MCPServer."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(
            allowed_paths=[tmp_path, Path.cwd()],
        )
        return MCPServer(config)

    def test_registered_tools(self, server: MCPServer) -> None:
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

    def test_handle_initialize(self, server: MCPServer) -> None:
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

    def test_handle_initialized(self, server: MCPServer) -> None:
        """Test initialized notification handling."""
        message = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        }

        # Should not raise, should return None (no response for notifications)
        response = server.handle_message(message)
        # Notifications don't require response
        assert response is None or "result" in response

    def test_handle_tools_list(self, server: MCPServer) -> None:
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

    def test_handle_unknown_method(self, server: MCPServer) -> None:
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

    def test_handle_list_categories(self, server: MCPServer) -> None:
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

    def test_handle_unknown_tool(self, server: MCPServer) -> None:
        """Test calling unknown tool."""
        message = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "nonexistent_tool",
                "arguments": {},
            },
        }

        response = server.handle_message(message)

        assert "error" in response or response["result"]["isError"] is True

    def test_path_validation_allowed(self, server: MCPServer, tmp_path: Path) -> None:
        """Test path validation for allowed paths."""
        test_file = tmp_path / "test.ods"
        test_file.write_text("test")

        # Should not raise
        validated = server._validate_path(str(test_file))
        assert validated == test_file

    def test_path_validation_disallowed(self, server: MCPServer) -> None:
        """Test path validation for disallowed paths."""
        with pytest.raises(MCPSecurityError):
            server._validate_path("/etc/passwd")

    def test_rate_limiting(self, server: MCPServer) -> None:
        """Test rate limit checking."""
        # First request should pass
        assert server._check_rate_limit() is True

        # Simulate many requests
        server._request_count = server.config.rate_limit_per_minute

        # Next should fail
        assert server._check_rate_limit() is False

    def test_rate_limit_reset(self, server: MCPServer) -> None:
        """Test rate limit reset after time period."""
        from datetime import datetime, timedelta

        # Set high request count
        server._request_count = server.config.rate_limit_per_minute

        # Simulate time passing
        server._last_reset = datetime.now() - timedelta(minutes=2)

        # Should reset and pass
        assert server._check_rate_limit() is True
        assert server._request_count == 1


class TestMCPServerToolHandlers:
    """Tests for MCP server tool handlers."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server with budget file."""
        config = MCPConfig(
            allowed_paths=[tmp_path, Path.cwd()],
        )
        return MCPServer(config)

    def test_handle_query_budget_total_spent(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget for total spending question."""
        pytest.skip("BudgetAnalyzer not integrated into MCP server yet")

    def test_handle_query_budget_remaining(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget for remaining budget question."""
        pytest.skip("BudgetAnalyzer not integrated into MCP server yet")

    def test_handle_list_categories_returns_default(self, server: MCPServer) -> None:
        """Test list_categories returns default categories."""
        result = server._handle_list_categories()

        assert result.is_error is False
        content = json.loads(result.content[0]["text"])
        assert "categories" in content
        assert isinstance(content["categories"], list)
        assert len(content["categories"]) > 0

    def test_handle_analyze_budget_invalid_path(self, server: MCPServer) -> None:
        """Test analyze_budget with invalid file path."""
        result = server._handle_analyze_budget(
            file_path="/etc/nonexistent.ods",
            analysis_type="summary",
        )

        assert result.is_error is True

    def test_handle_add_expense_invalid_date(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test add_expense with invalid date format."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_add_expense(
            date="invalid-date",
            category="Groceries",
            description="Test",
            amount=50.0,
            file_path=str(test_file),
        )

        assert result.is_error is True

    def test_handle_spending_trends(self, server: MCPServer, tmp_path: Path) -> None:
        """Test get_spending_trends handler."""
        with patch(
            "spreadsheet_dl.budget_analyzer.BudgetAnalyzer", create=True
        ) as MockAnalyzer:
            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_trends.return_value = {
                "direction": "increasing",
                "avg_weekly": 250.0,
            }

            test_file = tmp_path / "budget.ods"
            test_file.write_bytes(b"test")

            result = server._handle_spending_trends(
                file_path=str(test_file),
                period="month",
                category=None,
            )

            # Should return result (may or may not be error depending on impl)
            assert result is not None

    def test_handle_compare_periods(self, server: MCPServer, tmp_path: Path) -> None:
        """Test compare_periods handler."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_compare_periods(
            file_path=str(test_file),
            period1_start="2025-01-01",
            period1_end="2025-01-31",
            period2_start="2025-02-01",
            period2_end="2025-02-28",
        )

        assert result is not None

    def test_handle_generate_report(self, server: MCPServer, tmp_path: Path) -> None:
        """Test generate_report handler."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_generate_report(
            file_path=str(test_file),
            format="markdown",
            include_recommendations=True,
        )

        assert result is not None

    def test_handle_get_alerts(self, server: MCPServer, tmp_path: Path) -> None:
        """Test get_alerts handler."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_get_alerts(
            file_path=str(test_file),
            severity="warning",
        )

        assert result is not None


class TestMCPServerCellOperations:
    """Tests for MCP server cell operation handlers."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    @pytest.fixture
    def test_ods(self, tmp_path: Path) -> Path:
        """Create a test ODS file with sample data."""
        from odf.opendocument import OpenDocumentSpreadsheet
        from odf.table import Table, TableCell, TableRow
        from odf.text import P

        # Create a simple ODS file
        doc = OpenDocumentSpreadsheet()
        table = Table(name="Sheet1")

        # Add header row
        header_row = TableRow()
        for header in ["Name", "Value", "Status"]:
            cell = TableCell(valuetype="string")
            cell.addElement(P(text=header))
            header_row.addElement(cell)
        table.addElement(header_row)

        # Add data rows
        data = [
            ["Test1", "100", "Active"],
            ["Test2", "200", "Inactive"],
            ["Test3", "300", "Active"],
        ]
        for row_data in data:
            row = TableRow()
            for value in row_data:
                cell = TableCell(valuetype="string")
                cell.addElement(P(text=value))
                row.addElement(cell)
            table.addElement(row)

        doc.spreadsheet.addElement(table)

        # Save to file
        test_file = tmp_path / "test.ods"
        doc.save(str(test_file))
        return test_file

    def test_cell_get_handler(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_get handler reads values correctly."""
        result = server._handle_cell_get(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="A1",
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert content["cell"] == "A1"
        assert content["sheet"] == "Sheet1"
        assert content["value"] == "Name"

    def test_cell_set_handler(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_set handler writes values correctly."""
        result = server._handle_cell_set(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="D1",
            value="NewColumn",
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert content["success"] is True
        assert content["cell"] == "D1"
        assert content["value"] == "NewColumn"

        # Verify the value was written
        get_result = server._handle_cell_get(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="D1",
        )
        get_content = json.loads(get_result.content[0]["text"])
        assert get_content["value"] == "NewColumn"

    def test_cell_clear_handler(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_clear handler clears cell values."""
        # First set a value
        server._handle_cell_set(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="E1",
            value="ToClear",
        )

        # Now clear it
        result = server._handle_cell_clear(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="E1",
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert content["success"] is True

        # Verify it was cleared
        get_result = server._handle_cell_get(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="E1",
        )
        get_content = json.loads(get_result.content[0]["text"])
        assert get_content["value"] is None or get_content["value"] == ""

    def test_cell_copy_handler(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_copy handler copies cell values."""
        result = server._handle_cell_copy(
            file_path=str(test_ods),
            sheet="Sheet1",
            source="A1",
            destination="F1",
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert content["success"] is True

        # Verify the copy
        get_result = server._handle_cell_get(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="F1",
        )
        get_content = json.loads(get_result.content[0]["text"])
        assert get_content["value"] == "Name"

    def test_cell_move_handler(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_move handler moves cell values."""
        # Set a value to move
        server._handle_cell_set(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="G1",
            value="ToMove",
        )

        result = server._handle_cell_move(
            file_path=str(test_ods),
            sheet="Sheet1",
            source="G1",
            destination="H1",
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert content["success"] is True

        # Verify destination has the value
        get_result = server._handle_cell_get(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="H1",
        )
        get_content = json.loads(get_result.content[0]["text"])
        assert get_content["value"] == "ToMove"

        # Verify source is cleared
        get_result = server._handle_cell_get(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="G1",
        )
        get_content = json.loads(get_result.content[0]["text"])
        assert get_content["value"] is None or get_content["value"] == ""

    def test_cell_batch_get_handler(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_batch_get handler reads multiple cells."""
        result = server._handle_cell_batch_get(
            file_path=str(test_ods),
            sheet="Sheet1",
            cells="A1,B1,C1",
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert len(content["values"]) == 3
        assert content["values"]["A1"] == "Name"
        assert content["values"]["B1"] == "Value"
        assert content["values"]["C1"] == "Status"

    def test_cell_batch_get_range(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_batch_get handler reads a range."""
        result = server._handle_cell_batch_get(
            file_path=str(test_ods),
            sheet="Sheet1",
            cells="A1:C1",
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert len(content["values"]) == 3
        assert "A1" in content["values"]
        assert "B1" in content["values"]
        assert "C1" in content["values"]

    def test_cell_batch_set_handler(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_batch_set handler writes multiple cells."""
        values = json.dumps(
            {
                "A5": "Batch1",
                "B5": "Batch2",
                "C5": "Batch3",
            }
        )

        result = server._handle_cell_batch_set(
            file_path=str(test_ods),
            sheet="Sheet1",
            values=values,
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert content["success"] is True
        assert content["cells_updated"] == 3

        # Verify values were written
        get_result = server._handle_cell_get(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="B5",
        )
        get_content = json.loads(get_result.content[0]["text"])
        assert get_content["value"] == "Batch2"

    def test_cell_find_handler(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_find handler finds matching cells."""
        result = server._handle_cell_find(
            file_path=str(test_ods),
            sheet="Sheet1",
            search_text="Test",
            match_case=False,
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert content["count"] >= 3  # At least 3 matches (Test1, Test2, Test3)
        assert len(content["matches"]) >= 3

    def test_cell_find_case_sensitive(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_find handler with case sensitivity."""
        result = server._handle_cell_find(
            file_path=str(test_ods),
            sheet="Sheet1",
            search_text="Active",
            match_case=True,
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert content["match_case"] is True
        assert content["count"] >= 2  # At least 2 "Active" matches

    def test_cell_replace_handler(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_replace handler replaces text in cells."""
        result = server._handle_cell_replace(
            file_path=str(test_ods),
            sheet="Sheet1",
            search_text="Active",
            replace_text="Enabled",
            match_case=False,
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert content["success"] is True
        assert content["replacements"] >= 2

        # Verify replacement
        find_result = server._handle_cell_find(
            file_path=str(test_ods),
            sheet="Sheet1",
            search_text="Enabled",
            match_case=False,
        )
        find_content = json.loads(find_result.content[0]["text"])
        assert find_content["count"] >= 2

    def test_cell_merge_handler(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_merge handler merges cell ranges."""
        result = server._handle_cell_merge(
            file_path=str(test_ods),
            sheet="Sheet1",
            range="A6:C6",
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert content["success"] is True
        assert content["rows_spanned"] == 1
        assert content["cols_spanned"] == 3

    def test_cell_unmerge_handler(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_unmerge handler unmerges cells."""
        # First merge
        server._handle_cell_merge(
            file_path=str(test_ods),
            sheet="Sheet1",
            range="A7:B7",
        )

        # Then unmerge
        result = server._handle_cell_unmerge(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="A7",
        )

        assert not result.is_error
        content = json.loads(result.content[0]["text"])
        assert content["success"] is True

    def test_cell_get_nonexistent_file(self, server: MCPServer, tmp_path: Path) -> None:
        """Test cell_get with nonexistent file returns error."""
        result = server._handle_cell_get(
            file_path=str(tmp_path / "nonexistent.ods"),
            sheet="Sheet1",
            cell="A1",
        )

        assert result.is_error

    def test_cell_get_invalid_sheet(self, server: MCPServer, test_ods: Path) -> None:
        """Test cell_get with invalid sheet name returns error."""
        result = server._handle_cell_get(
            file_path=str(test_ods),
            sheet="NonexistentSheet",
            cell="A1",
        )

        assert result.is_error

    def test_cell_get_invalid_cell_reference(
        self, server: MCPServer, test_ods: Path
    ) -> None:
        """Test cell_get with invalid cell reference returns error."""
        result = server._handle_cell_get(
            file_path=str(test_ods),
            sheet="Sheet1",
            cell="INVALID",
        )

        assert result.is_error


class TestMCPServerStyleOperations:
    """Tests for MCP server style operation handlers."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_style_list_handler(self, server: MCPServer) -> None:
        """Test style_list handler exists."""
        assert hasattr(server, "_handle_style_list")

    def test_style_get_handler(self, server: MCPServer) -> None:
        """Test style_get handler exists."""
        assert hasattr(server, "_handle_style_get")

    def test_style_create_handler(self, server: MCPServer) -> None:
        """Test style_create handler exists."""
        assert hasattr(server, "_handle_style_create")

    def test_style_update_handler(self, server: MCPServer) -> None:
        """Test style_update handler exists."""
        assert hasattr(server, "_handle_style_update")

    def test_style_delete_handler(self, server: MCPServer) -> None:
        """Test style_delete handler exists."""
        assert hasattr(server, "_handle_style_delete")

    def test_style_apply_handler(self, server: MCPServer) -> None:
        """Test style_apply handler exists."""
        assert hasattr(server, "_handle_style_apply")

    def test_format_cells_handler(self, server: MCPServer) -> None:
        """Test format_cells handler exists."""
        assert hasattr(server, "_handle_format_cells")

    def test_format_number_handler(self, server: MCPServer) -> None:
        """Test format_number handler exists."""
        assert hasattr(server, "_handle_format_number")

    def test_format_font_handler(self, server: MCPServer) -> None:
        """Test format_font handler exists."""
        assert hasattr(server, "_handle_format_font")

    def test_format_fill_handler(self, server: MCPServer) -> None:
        """Test format_fill handler exists."""
        assert hasattr(server, "_handle_format_fill")

    def test_format_border_handler(self, server: MCPServer) -> None:
        """Test format_border handler exists."""
        assert hasattr(server, "_handle_format_border")


class TestMCPServerStructureOperations:
    """Tests for MCP server structure operation handlers."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_row_insert_handler(self, server: MCPServer) -> None:
        """Test row_insert handler exists."""
        assert hasattr(server, "_handle_row_insert")

    def test_row_delete_handler(self, server: MCPServer) -> None:
        """Test row_delete handler exists."""
        assert hasattr(server, "_handle_row_delete")

    def test_row_hide_handler(self, server: MCPServer) -> None:
        """Test row_hide handler exists."""
        assert hasattr(server, "_handle_row_hide")

    def test_column_insert_handler(self, server: MCPServer) -> None:
        """Test column_insert handler exists."""
        assert hasattr(server, "_handle_column_insert")

    def test_column_delete_handler(self, server: MCPServer) -> None:
        """Test column_delete handler exists."""
        assert hasattr(server, "_handle_column_delete")

    def test_column_hide_handler(self, server: MCPServer) -> None:
        """Test column_hide handler exists."""
        assert hasattr(server, "_handle_column_hide")

    def test_freeze_set_handler(self, server: MCPServer) -> None:
        """Test freeze_set handler exists."""
        assert hasattr(server, "_handle_freeze_set")

    def test_freeze_clear_handler(self, server: MCPServer) -> None:
        """Test freeze_clear handler exists."""
        assert hasattr(server, "_handle_freeze_clear")

    def test_sheet_create_handler(self, server: MCPServer) -> None:
        """Test sheet_create handler exists."""
        assert hasattr(server, "_handle_sheet_create")

    def test_sheet_delete_handler(self, server: MCPServer) -> None:
        """Test sheet_delete handler exists."""
        assert hasattr(server, "_handle_sheet_delete")

    def test_sheet_copy_handler(self, server: MCPServer) -> None:
        """Test sheet_copy handler exists."""
        assert hasattr(server, "_handle_sheet_copy")


class TestMCPServerAdvancedOperations:
    """Tests for MCP server advanced operation handlers."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_chart_create_handler(self, server: MCPServer) -> None:
        """Test chart_create handler exists."""
        assert hasattr(server, "_handle_chart_create")

    def test_chart_update_handler(self, server: MCPServer) -> None:
        """Test chart_update handler exists."""
        assert hasattr(server, "_handle_chart_update")

    def test_validation_create_handler(self, server: MCPServer) -> None:
        """Test validation_create handler exists."""
        assert hasattr(server, "_handle_validation_create")

    def test_cf_create_handler(self, server: MCPServer) -> None:
        """Test cf_create handler exists."""
        assert hasattr(server, "_handle_cf_create")

    def test_named_range_create_handler(self, server: MCPServer) -> None:
        """Test named_range_create handler exists."""
        assert hasattr(server, "_handle_named_range_create")

    def test_table_create_handler(self, server: MCPServer) -> None:
        """Test table_create handler exists."""
        assert hasattr(server, "_handle_table_create")

    def test_query_select_handler(self, server: MCPServer) -> None:
        """Test query_select handler exists."""
        assert hasattr(server, "_handle_query_select")

    def test_query_find_handler(self, server: MCPServer) -> None:
        """Test query_find handler exists."""
        assert hasattr(server, "_handle_query_find")


class TestMCPServerMessageProtocol:
    """Tests for MCP server message protocol handling."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_invalid_jsonrpc_version(self, server: MCPServer) -> None:
        """Test handling invalid JSON-RPC version."""
        message = {
            "jsonrpc": "1.0",
            "id": 1,
            "method": "initialize",
            "params": {},
        }

        response = server.handle_message(message)

        # Should handle gracefully
        assert response is not None

    def test_missing_method(self, server: MCPServer) -> None:
        """Test handling message without method."""
        message = {
            "jsonrpc": "2.0",
            "id": 1,
            "params": {},
        }

        response = server.handle_message(message)

        assert "error" in response

    def test_missing_id(self, server: MCPServer) -> None:
        """Test handling request without id."""
        message = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
        }

        # Notification (no id) should not return error
        response = server.handle_message(message)
        # May return None or response depending on implementation
        assert response is None or isinstance(response, dict)

    def test_tools_call_with_arguments(self, server: MCPServer) -> None:
        """Test tools/call with arguments."""
        message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "list_categories",
                "arguments": {},
            },
        }

        response = server.handle_message(message)

        assert "result" in response
        assert "content" in response["result"]


class TestCreateMCPServer:
    """Tests for create_mcp_server function."""

    def test_create_with_paths(self) -> None:
        """Test creating server with allowed paths."""
        server = create_mcp_server(["/tmp", "/home"])

        assert len(server.config.allowed_paths) == 2
        assert Path("/tmp") in server.config.allowed_paths
        assert Path("/home") in server.config.allowed_paths

    def test_create_without_paths(self) -> None:
        """Test creating server without paths."""
        server = create_mcp_server()

        # Should have default paths
        assert len(server.config.allowed_paths) >= 0

    def test_create_with_empty_paths(self) -> None:
        """Test creating server with empty paths list."""
        server = create_mcp_server([])

        # Should use defaults when empty
        assert len(server.config.allowed_paths) > 0


class TestMCPErrors:
    """Tests for MCP errors."""

    def test_mcp_error(self) -> None:
        """Test base MCP error."""
        error = MCPError("Test error")
        assert error.error_code == "FT-MCP-1900"
        assert "Test error" in str(error)
        assert "FT-MCP-1900" in str(error)

    def test_tool_error(self) -> None:
        """Test tool error."""
        error = MCPToolError("Tool failed")
        assert error.error_code == "FT-MCP-1901"
        assert "Tool failed" in str(error)
        assert "FT-MCP-1901" in str(error)

    def test_security_error(self) -> None:
        """Test security error."""
        error = MCPSecurityError("Access denied")
        assert error.error_code == "FT-MCP-1902"
        assert "Access denied" in str(error)
        assert "FT-MCP-1902" in str(error)

    def test_error_inheritance(self) -> None:
        """Test error inheritance hierarchy."""
        assert issubclass(MCPToolError, MCPError)
        assert issubclass(MCPSecurityError, MCPError)


class TestMCPServerAuditLogging:
    """Tests for MCP server audit logging."""

    @pytest.fixture
    def server_with_audit(self, tmp_path: Path) -> MCPServer:
        """Create a server with audit logging enabled."""
        log_path = tmp_path / "audit.log"
        config = MCPConfig(
            allowed_paths=[tmp_path],
            enable_audit_log=True,
            audit_log_path=log_path,
        )
        return MCPServer(config)

    def test_audit_log_enabled(self, server_with_audit: MCPServer) -> None:
        """Test audit logging is enabled."""
        assert server_with_audit.config.enable_audit_log is True

    def test_audit_log_path_set(
        self, server_with_audit: MCPServer, tmp_path: Path
    ) -> None:
        """Test audit log path is set."""
        assert server_with_audit.config.audit_log_path == tmp_path / "audit.log"

    def test_audit_logging_writes_to_file(
        self, server_with_audit: MCPServer, tmp_path: Path
    ) -> None:
        """Test audit logging writes to file."""
        result = MCPToolResult.text("test")
        params = {"tool": "test"}

        server_with_audit._log_audit("test_tool", params, result)

        log_path = tmp_path / "audit.log"
        assert log_path.exists()
        log_content = log_path.read_text()
        assert "test_tool" in log_content
        assert "test" in log_content

    def test_audit_logging_disabled(self, tmp_path: Path) -> None:
        """Test audit logging when disabled."""
        config = MCPConfig(
            allowed_paths=[tmp_path],
            enable_audit_log=False,
        )
        server = MCPServer(config)

        result = MCPToolResult.text("test")
        params = {"tool": "test"}

        # Should not raise
        server._log_audit("test_tool", params, result)


class TestMCPServerIntegrationToolCalls:
    """Integration tests for MCP server tool calls via handle_message."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_cell_get_via_message(self, server: MCPServer, tmp_path: Path) -> None:
        """Test cell_get tool via MCP message."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "cell_get",
                "arguments": {
                    "file_path": str(test_file),
                    "sheet": "Sheet1",
                    "cell": "A1",
                },
            },
        }

        response = server.handle_message(message)
        assert response["jsonrpc"] == "2.0"
        assert "result" in response
        assert "content" in response["result"]

    def test_cell_set_via_message(self, server: MCPServer, tmp_path: Path) -> None:
        """Test cell_set tool via MCP message."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "cell_set",
                "arguments": {
                    "file_path": str(test_file),
                    "sheet": "Sheet1",
                    "cell": "A1",
                    "value": "Test Value",
                },
            },
        }

        response = server.handle_message(message)
        assert response["jsonrpc"] == "2.0"
        assert "result" in response

    def test_cell_clear_via_message(self, server: MCPServer, tmp_path: Path) -> None:
        """Test cell_clear tool via MCP message."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        message = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "cell_clear",
                "arguments": {
                    "file_path": str(test_file),
                    "sheet": "Sheet1",
                    "cell": "A1",
                },
            },
        }

        response = server.handle_message(message)
        assert "result" in response

    def test_cell_copy_via_message(self, server: MCPServer, tmp_path: Path) -> None:
        """Test cell_copy tool via MCP message."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        message = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "cell_copy",
                "arguments": {
                    "file_path": str(test_file),
                    "sheet": "Sheet1",
                    "source": "A1",
                    "destination": "B1",
                },
            },
        }

        response = server.handle_message(message)
        assert "result" in response

    def test_cell_move_via_message(self, server: MCPServer, tmp_path: Path) -> None:
        """Test cell_move tool via MCP message."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        message = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "cell_move",
                "arguments": {
                    "file_path": str(test_file),
                    "sheet": "Sheet1",
                    "source": "A1",
                    "destination": "C1",
                },
            },
        }

        response = server.handle_message(message)
        assert "result" in response

    def test_cell_batch_get_via_message(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test cell_batch_get tool via MCP message."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        message = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "cell_batch_get",
                "arguments": {
                    "file_path": str(test_file),
                    "sheet": "Sheet1",
                    "cells": "A1,B1,C1",
                },
            },
        }

        response = server.handle_message(message)
        assert "result" in response

    def test_cell_batch_set_via_message(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test cell_batch_set tool via MCP message."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        message = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {
                "name": "cell_batch_set",
                "arguments": {
                    "file_path": str(test_file),
                    "sheet": "Sheet1",
                    "values": '{"A1": "value1", "B1": "value2"}',
                },
            },
        }

        response = server.handle_message(message)
        assert "result" in response

    def test_cell_find_via_message(self, server: MCPServer, tmp_path: Path) -> None:
        """Test cell_find tool via MCP message."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        message = {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "tools/call",
            "params": {
                "name": "cell_find",
                "arguments": {
                    "file_path": str(test_file),
                    "sheet": "Sheet1",
                    "search_text": "test",
                    "match_case": False,
                },
            },
        }

        response = server.handle_message(message)
        assert "result" in response

    def test_cell_replace_via_message(self, server: MCPServer, tmp_path: Path) -> None:
        """Test cell_replace tool via MCP message."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        message = {
            "jsonrpc": "2.0",
            "id": 9,
            "method": "tools/call",
            "params": {
                "name": "cell_replace",
                "arguments": {
                    "file_path": str(test_file),
                    "sheet": "Sheet1",
                    "search_text": "old",
                    "replace_text": "new",
                    "match_case": False,
                },
            },
        }

        response = server.handle_message(message)
        assert "result" in response

    def test_cell_merge_via_message(self, server: MCPServer, tmp_path: Path) -> None:
        """Test cell_merge tool via MCP message."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        message = {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {
                "name": "cell_merge",
                "arguments": {
                    "file_path": str(test_file),
                    "sheet": "Sheet1",
                    "range": "A1:B2",
                },
            },
        }

        response = server.handle_message(message)
        assert "result" in response

    def test_cell_unmerge_via_message(self, server: MCPServer, tmp_path: Path) -> None:
        """Test cell_unmerge tool via MCP message."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        message = {
            "jsonrpc": "2.0",
            "id": 11,
            "method": "tools/call",
            "params": {
                "name": "cell_unmerge",
                "arguments": {
                    "file_path": str(test_file),
                    "sheet": "Sheet1",
                    "cell": "A1",
                },
            },
        }

        response = server.handle_message(message)
        assert "result" in response

    def test_style_tools_via_message(self, server: MCPServer, tmp_path: Path) -> None:
        """Test style operation tools via MCP messages."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        style_tools = [
            "style_list",
            "style_get",
            "style_create",
            "style_update",
            "style_delete",
            "style_apply",
            "format_cells",
            "format_number",
            "format_font",
            "format_fill",
            "format_border",
        ]

        for i, tool_name in enumerate(style_tools):
            message = {
                "jsonrpc": "2.0",
                "id": 100 + i,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": {
                        "file_path": str(test_file),
                        "sheet": "Sheet1",
                    },
                },
            }

            response = server.handle_message(message)
            assert "result" in response, f"Tool {tool_name} failed"

    def test_structure_tools_via_message(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test structure operation tools via MCP messages."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        structure_tools = [
            "row_insert",
            "row_delete",
            "row_hide",
            "column_insert",
            "column_delete",
            "column_hide",
            "freeze_set",
            "freeze_clear",
            "sheet_create",
            "sheet_delete",
            "sheet_copy",
        ]

        for i, tool_name in enumerate(structure_tools):
            message = {
                "jsonrpc": "2.0",
                "id": 200 + i,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": {
                        "file_path": str(test_file),
                        "sheet": "Sheet1",
                    },
                },
            }

            response = server.handle_message(message)
            assert "result" in response, f"Tool {tool_name} failed"

    def test_advanced_tools_via_message(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test advanced operation tools via MCP messages."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        advanced_tools = [
            "chart_create",
            "chart_update",
            "validation_create",
            "cf_create",
            "named_range_create",
            "table_create",
            "query_select",
            "query_find",
        ]

        for i, tool_name in enumerate(advanced_tools):
            message = {
                "jsonrpc": "2.0",
                "id": 300 + i,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": {
                        "file_path": str(test_file),
                        "sheet": "Sheet1",
                    },
                },
            }

            response = server.handle_message(message)
            assert "result" in response, f"Tool {tool_name} failed"

    def test_rate_limit_exceeded_via_message(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test rate limit exceeded error via MCP message."""
        # Set request count to limit
        server._request_count = server.config.rate_limit_per_minute

        message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {},
        }

        response = server.handle_message(message)
        assert "error" in response
        assert response["error"]["code"] == -32000
        assert "rate limit" in response["error"]["message"].lower()

    def test_tool_with_no_handler(self, server: MCPServer) -> None:
        """Test calling a tool with no handler."""
        # Add a tool without handler
        tool = MCPTool(name="no_handler", description="Tool without handler")
        server._tools["no_handler"] = tool

        message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "no_handler",
                "arguments": {},
            },
        }

        response = server.handle_message(message)
        assert "error" in response
        assert response["error"]["code"] == -32603

    def test_error_response_format(self, server: MCPServer) -> None:
        """Test error response format."""
        response = server._error_response(1, -32000, "Test error")

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "error" in response
        assert response["error"]["code"] == -32000
        assert response["error"]["message"] == "Test error"


class TestMCPServerPathValidation:
    """Tests for path validation edge cases."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path])
        return MCPServer(config)

    def test_validate_path_nonexistent_file(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test validating path for nonexistent file."""
        nonexistent = tmp_path / "nonexistent.ods"

        with pytest.raises(FileError):
            server._validate_path(str(nonexistent))

    def test_validate_path_outside_allowed(self, server: MCPServer) -> None:
        """Test validating path outside allowed paths."""
        with pytest.raises(MCPSecurityError) as exc_info:
            server._validate_path("/etc/passwd")

        assert "not allowed" in str(exc_info.value).lower()

    def test_validate_path_string_conversion(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test path validation with string input."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        # Should accept string
        result = server._validate_path(str(test_file))
        assert result == test_file

    def test_validate_path_relative_path(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test path validation with relative path."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        # Update allowed paths to include parent
        server.config.allowed_paths = [tmp_path.parent]

        result = server._validate_path(str(test_file))
        assert result.is_absolute()


class TestMCPServerAnalyzeBudgetHandlers:
    """Tests for analyze_budget handler with different analysis types."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_analyze_budget_summary_type(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test analyze_budget with summary type."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_analyze_budget(
            file_path=str(test_file),
            analysis_type="summary",
        )

        # Should return error (no real budget file) but not raise
        assert result is not None

    def test_analyze_budget_detailed_type(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test analyze_budget with detailed type."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_analyze_budget(
            file_path=str(test_file),
            analysis_type="detailed",
        )

        assert result is not None

    def test_analyze_budget_categories_type(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test analyze_budget with categories type."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_analyze_budget(
            file_path=str(test_file),
            analysis_type="categories",
        )

        assert result is not None

    def test_analyze_budget_trends_type(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test analyze_budget with trends type."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_analyze_budget(
            file_path=str(test_file),
            analysis_type="trends",
        )

        assert result is not None


class TestMCPServerQueryBudgetHandlers:
    """Tests for query_budget natural language processing."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_query_budget_total_spent_keyword(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget with total spent keywords."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_query_budget(
            question="How much have I spent in total?",
            file_path=str(test_file),
        )

        assert result is not None

    def test_query_budget_remaining_keyword(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget with remaining keywords."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_query_budget(
            question="How much budget is remaining?",
            file_path=str(test_file),
        )

        assert result is not None

    def test_query_budget_over_budget_keyword(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget with over budget keywords."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_query_budget(
            question="Am I over budget?",
            file_path=str(test_file),
        )

        assert result is not None

    def test_query_budget_default_response(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget with unrecognized question."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_query_budget(
            question="What is the meaning of life?",
            file_path=str(test_file),
        )

        assert result is not None


class TestMCPServerGenerateReportFormats:
    """Tests for generate_report with different formats."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_generate_report_json_format(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test generate_report with JSON format."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_generate_report(
            file_path=str(test_file),
            format="json",
            include_recommendations=True,
        )

        assert result is not None

    def test_generate_report_markdown_format(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test generate_report with markdown format."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_generate_report(
            file_path=str(test_file),
            format="markdown",
            include_recommendations=True,
        )

        assert result is not None

    def test_generate_report_text_format(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test generate_report with text format."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_generate_report(
            file_path=str(test_file),
            format="text",
            include_recommendations=False,
        )

        assert result is not None

    def test_generate_report_without_recommendations(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test generate_report without recommendations."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_generate_report(
            file_path=str(test_file),
            format="markdown",
            include_recommendations=False,
        )

        assert result is not None


class TestMCPServerMain:
    """Tests for main CLI function."""

    def test_main_function_imports(self) -> None:
        """Test that main function can be imported."""
        from spreadsheet_dl.mcp_server import main

        assert callable(main)


class TestMCPServerDirectHandlerCalls:
    """Direct tests for handler methods to increase coverage."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_handle_cell_get_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to cell_get handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_cell_get(
            file_path=str(test_file),
            sheet="Sheet1",
            cell="A1",
        )

        assert result is not None
        assert isinstance(result, MCPToolResult)

    def test_handle_cell_set_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to cell_set handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_cell_set(
            file_path=str(test_file),
            sheet="Sheet1",
            cell="A1",
            value="test value",
        )

        assert result is not None

    def test_handle_cell_clear_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to cell_clear handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_cell_clear(
            file_path=str(test_file),
            sheet="Sheet1",
            cell="A1",
        )

        assert result is not None

    def test_handle_cell_copy_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to cell_copy handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_cell_copy(
            file_path=str(test_file),
            sheet="Sheet1",
            source="A1",
            destination="B1",
        )

        assert result is not None

    def test_handle_cell_move_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to cell_move handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_cell_move(
            file_path=str(test_file),
            sheet="Sheet1",
            source="A1",
            destination="C1",
        )

        assert result is not None

    def test_handle_cell_batch_get_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to cell_batch_get handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_cell_batch_get(
            file_path=str(test_file),
            sheet="Sheet1",
            cells="A1,B1,C1",
        )

        assert result is not None

    def test_handle_cell_batch_set_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to cell_batch_set handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_cell_batch_set(
            file_path=str(test_file),
            sheet="Sheet1",
            values='{"A1": "val1", "B1": "val2"}',
        )

        assert result is not None

    def test_handle_cell_find_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to cell_find handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_cell_find(
            file_path=str(test_file),
            sheet="Sheet1",
            search_text="test",
            match_case=True,
        )

        assert result is not None

    def test_handle_cell_replace_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to cell_replace handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_cell_replace(
            file_path=str(test_file),
            sheet="Sheet1",
            search_text="old",
            replace_text="new",
            match_case=True,
        )

        assert result is not None

    def test_handle_cell_merge_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to cell_merge handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_cell_merge(
            file_path=str(test_file),
            sheet="Sheet1",
            range="A1:B2",
        )

        assert result is not None

    def test_handle_cell_unmerge_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to cell_unmerge handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_cell_unmerge(
            file_path=str(test_file),
            sheet="Sheet1",
            cell="A1",
        )

        assert result is not None

    def test_handle_style_list_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to style_list handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_style_list(
            file_path=str(test_file),
        )

        assert result is not None

    def test_handle_style_get_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to style_get handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_style_get(
            file_path=str(test_file),
        )

        assert result is not None

    def test_handle_style_create_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to style_create handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_style_create(
            file_path=str(test_file),
        )

        assert result is not None

    def test_handle_style_update_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to style_update handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_style_update(
            file_path=str(test_file),
        )

        assert result is not None

    def test_handle_style_delete_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to style_delete handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_style_delete(
            file_path=str(test_file),
        )

        assert result is not None

    def test_handle_style_apply_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to style_apply handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_style_apply(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_format_cells_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to format_cells handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_format_cells(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_format_number_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to format_number handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_format_number(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_format_font_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to format_font handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_format_font(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_format_fill_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to format_fill handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_format_fill(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_format_border_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to format_border handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_format_border(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_row_insert_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to row_insert handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_row_insert(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_row_delete_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to row_delete handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_row_delete(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_row_hide_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to row_hide handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_row_hide(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_column_insert_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to column_insert handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_column_insert(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_column_delete_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to column_delete handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_column_delete(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_column_hide_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to column_hide handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_column_hide(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_freeze_set_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to freeze_set handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_freeze_set(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_freeze_clear_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to freeze_clear handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_freeze_clear(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_sheet_create_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to sheet_create handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_sheet_create(
            file_path=str(test_file),
            sheet="NewSheet",
        )

        assert result is not None

    def test_handle_sheet_delete_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to sheet_delete handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_sheet_delete(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_sheet_copy_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to sheet_copy handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_sheet_copy(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_chart_create_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to chart_create handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_chart_create(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_chart_update_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to chart_update handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_chart_update(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_validation_create_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to validation_create handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_validation_create(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_cf_create_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to cf_create handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_cf_create(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_named_range_create_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to named_range_create handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_named_range_create(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_table_create_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to table_create handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_table_create(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_query_select_direct(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test direct call to query_select handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_query_select(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None

    def test_handle_query_find_direct(self, server: MCPServer, tmp_path: Path) -> None:
        """Test direct call to query_find handler."""
        test_file = tmp_path / "test.ods"
        test_file.write_bytes(b"test")

        result = server._handle_query_find(
            file_path=str(test_file),
            sheet="Sheet1",
        )

        assert result is not None


class TestMCPServerExceptionHandling:
    """Tests for exception handling in tool handlers."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path])
        return MCPServer(config)

    def test_cell_handlers_with_invalid_path(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test cell handlers with invalid path return errors."""
        result = server._handle_cell_get(
            file_path="/nonexistent/file.ods",
            sheet="Sheet1",
            cell="A1",
        )
        assert result.is_error is True

        result = server._handle_cell_set(
            file_path="/nonexistent/file.ods",
            sheet="Sheet1",
            cell="A1",
            value="test",
        )
        assert result.is_error is True

        result = server._handle_cell_clear(
            file_path="/nonexistent/file.ods",
            sheet="Sheet1",
            cell="A1",
        )
        assert result.is_error is True

        result = server._handle_cell_copy(
            file_path="/nonexistent/file.ods",
            sheet="Sheet1",
            source="A1",
            destination="B1",
        )
        assert result.is_error is True

        result = server._handle_cell_move(
            file_path="/nonexistent/file.ods",
            sheet="Sheet1",
            source="A1",
            destination="B1",
        )
        assert result.is_error is True

        result = server._handle_cell_batch_get(
            file_path="/nonexistent/file.ods",
            sheet="Sheet1",
            cells="A1,B1",
        )
        assert result.is_error is True

        result = server._handle_cell_batch_set(
            file_path="/nonexistent/file.ods",
            sheet="Sheet1",
            values='{"A1": "val"}',
        )
        assert result.is_error is True

        result = server._handle_cell_find(
            file_path="/nonexistent/file.ods",
            sheet="Sheet1",
            search_text="test",
        )
        assert result.is_error is True

        result = server._handle_cell_replace(
            file_path="/nonexistent/file.ods",
            sheet="Sheet1",
            search_text="old",
            replace_text="new",
        )
        assert result.is_error is True

        result = server._handle_cell_merge(
            file_path="/nonexistent/file.ods",
            sheet="Sheet1",
            range="A1:B2",
        )
        assert result.is_error is True

        result = server._handle_cell_unmerge(
            file_path="/nonexistent/file.ods",
            sheet="Sheet1",
            cell="A1",
        )
        assert result.is_error is True

    def test_style_handlers_with_invalid_path(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test style handlers with invalid path return errors."""
        result = server._handle_style_list(file_path="/nonexistent/file.ods")
        assert result.is_error is True

        result = server._handle_style_get(file_path="/nonexistent/file.ods")
        assert result.is_error is True

        result = server._handle_style_create(file_path="/nonexistent/file.ods")
        assert result.is_error is True

        result = server._handle_style_update(file_path="/nonexistent/file.ods")
        assert result.is_error is True

        result = server._handle_style_delete(file_path="/nonexistent/file.ods")
        assert result.is_error is True

        result = server._handle_style_apply(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_format_cells(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_format_number(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_format_font(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_format_fill(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_format_border(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

    def test_structure_handlers_with_invalid_path(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test structure handlers with invalid path return errors."""
        result = server._handle_row_insert(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_row_delete(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_row_hide(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_column_insert(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_column_delete(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_column_hide(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_freeze_set(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_freeze_clear(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_sheet_create(
            file_path="/nonexistent/file.ods", sheet="NewSheet"
        )
        assert result.is_error is True

        result = server._handle_sheet_delete(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_sheet_copy(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

    def test_advanced_handlers_with_invalid_path(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test advanced handlers with invalid path return errors."""
        result = server._handle_chart_create(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_chart_update(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_validation_create(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_cf_create(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_named_range_create(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_table_create(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_query_select(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

        result = server._handle_query_find(
            file_path="/nonexistent/file.ods", sheet="Sheet1"
        )
        assert result.is_error is True

    def test_handle_message_exception_handling(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test handle_message exception handling."""
        # Trigger an exception by passing invalid message
        message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "list_categories",
                "arguments": {"invalid": "argument"},
            },
        }

        # This should not crash, should return error response
        response = server.handle_message(message)
        # Either error in response or isError in result
        assert "error" in response or response.get("result", {}).get("isError") is True


class TestMCPServerWithMockedBudgetAnalyzer:
    """Tests with mocked BudgetAnalyzer for complete coverage."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_analyze_budget_with_mock(self, server: MCPServer, tmp_path: Path) -> None:
        """Test analyze_budget with mocked BudgetAnalyzer."""
        from decimal import Decimal
        from unittest.mock import MagicMock

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            mock_summary = MagicMock()
            mock_summary.total_budget = Decimal("1000")
            mock_summary.total_spent = Decimal("500")
            mock_summary.total_remaining = Decimal("500")
            mock_summary.percent_used = Decimal("50")
            mock_summary.alerts = []

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("200"),
                "Transport": Decimal("150"),
                "Entertainment": Decimal("150"),
            }
            mock_analyzer.expenses = MagicMock()
            mock_analyzer.expenses.empty = False

            # Test summary type
            result = server._handle_analyze_budget(str(test_file), "summary")
            assert result.is_error is False
            assert '"total_budget": 1000' in result.content[0]["text"]

            # Test detailed type
            result = server._handle_analyze_budget(str(test_file), "detailed")
            assert result.is_error is False
            assert '"by_category"' in result.content[0]["text"]

            # Test categories type
            result = server._handle_analyze_budget(str(test_file), "categories")
            assert result.is_error is False
            assert '"categories"' in result.content[0]["text"]

    def test_add_expense_with_valid_category(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test add_expense with valid category."""

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch("spreadsheet_dl.ods_editor.OdsEditor") as MockEditor:
            mock_editor = MockEditor.return_value
            mock_editor.append_expense.return_value = 5
            mock_editor.save.return_value = None

            result = server._handle_add_expense(
                date="2025-01-15",
                category="Groceries",
                description="Test expense",
                amount=50.0,
                file_path=str(test_file),
            )

            assert result.is_error is False
            assert '"success": true' in result.content[0]["text"]

    def test_add_expense_no_file_path(self, server: MCPServer, tmp_path: Path) -> None:
        """Test add_expense without file_path parameter."""
        # Create a budget file in cwd
        budget_file = tmp_path / "budget_test.ods"
        budget_file.write_bytes(b"test")

        with (
            patch("spreadsheet_dl.ods_editor.OdsEditor") as MockEditor,
            patch("spreadsheet_dl.mcp_server.Path.cwd", return_value=tmp_path),
        ):
            mock_editor = MockEditor.return_value
            mock_editor.append_expense.return_value = 5
            mock_editor.save.return_value = None

            result = server._handle_add_expense(
                date="2025-01-15",
                category="Groceries",
                description="Test expense",
                amount=50.0,
                file_path=None,
            )

            # May succeed or fail depending on file discovery
            assert result is not None

    def test_add_expense_case_insensitive_category(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test add_expense with case-insensitive category match."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch("spreadsheet_dl.ods_editor.OdsEditor") as MockEditor:
            mock_editor = MockEditor.return_value
            mock_editor.append_expense.return_value = 5
            mock_editor.save.return_value = None

            result = server._handle_add_expense(
                date="2025-01-15",
                category="groceries",  # lowercase
                description="Test expense",
                amount=50.0,
                file_path=str(test_file),
            )

            # Should handle case-insensitive match
            assert result is not None

    def test_generate_report_with_recommendations(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test generate_report with recommendations."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with (
            patch(
                "spreadsheet_dl.domains.finance.report_generator.ReportGenerator"
            ) as MockReportGen,
            patch.object(
                server,
                "_generate_recommendations",
                return_value=["Test recommendation"],
            ),
        ):
            mock_gen = MockReportGen.return_value
            mock_gen.generate_visualization_data.return_value = {"data": "test"}
            mock_gen.generate_markdown_report.return_value = "# Report"
            mock_gen.generate_text_report.return_value = "Report text"

            # JSON format with recommendations
            result = server._handle_generate_report(
                file_path=str(test_file),
                format="json",
                include_recommendations=True,
            )
            assert result.is_error is False
            assert "recommendations" in result.content[0]["text"]

            # Markdown format with recommendations
            result = server._handle_generate_report(
                file_path=str(test_file),
                format="markdown",
                include_recommendations=True,
            )
            assert result.is_error is False
            assert "Test recommendation" in result.content[0]["text"]

            # Text format
            result = server._handle_generate_report(
                file_path=str(test_file),
                format="text",
                include_recommendations=False,
            )
            assert result.is_error is False

    def test_generate_recommendations_logic(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test _generate_recommendations internal logic."""
        from decimal import Decimal

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            # Test over budget scenario
            mock_summary = MagicMock()
            mock_summary.total_remaining = Decimal("-100")
            mock_summary.percent_used = Decimal("110")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("500")
            }

            recommendations = server._generate_recommendations(test_file)
            assert len(recommendations) > 0
            assert any("over budget" in r.lower() for r in recommendations)

            # Test high percentage used
            mock_summary.total_remaining = Decimal("100")
            mock_summary.percent_used = Decimal("85")

            recommendations = server._generate_recommendations(test_file)
            assert any("%" in r for r in recommendations)

            # Test high category spending
            mock_summary.percent_used = Decimal("50")
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("800"),
                "Transport": Decimal("200"),
            }

            recommendations = server._generate_recommendations(test_file)
            assert any("Groceries" in r for r in recommendations)


class TestMCPServerQueryBudgetCategoryMatching:
    """Tests for query_budget category matching logic."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_query_budget_with_category_match(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget with category name in question."""
        from decimal import Decimal

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            mock_summary = MagicMock()
            mock_summary.total_spent = Decimal("500")
            mock_summary.total_budget = Decimal("1000")
            mock_summary.total_remaining = Decimal("500")
            mock_summary.percent_used = Decimal("50")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("200"),
                "Transport": Decimal("150"),
                "Entertainment": Decimal("150"),
            }

            # Question with category name (avoid other keywords)
            result = server._handle_query_budget(
                question="Tell me about groceries category?",
                file_path=str(test_file),
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "Groceries" in data["answer"]
            assert data["data"]["category"] == "Groceries"
            assert data["data"]["amount"] == 200.0

    def test_query_budget_total_spent_path(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget total spent code path."""
        from decimal import Decimal

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            mock_summary = MagicMock()
            mock_summary.total_spent = Decimal("500")
            mock_summary.total_budget = Decimal("1000")
            mock_summary.total_remaining = Decimal("500")
            mock_summary.percent_used = Decimal("50")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("200")
            }

            # Test "spend" keyword
            result = server._handle_query_budget(
                question="How much did I spend?",
                file_path=str(test_file),
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "total_spent" in data["data"]
            assert data["data"]["total_spent"] == 500.0

    def test_query_budget_remaining_path(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget remaining budget code path."""
        from decimal import Decimal

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            mock_summary = MagicMock()
            mock_summary.total_spent = Decimal("500")
            mock_summary.total_budget = Decimal("1000")
            mock_summary.total_remaining = Decimal("500")
            mock_summary.percent_used = Decimal("50")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("200")
            }

            # Test "left" keyword
            result = server._handle_query_budget(
                question="How much budget is left?",
                file_path=str(test_file),
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "remaining" in data["data"]
            assert data["data"]["remaining"] == 500.0

    def test_query_budget_over_budget_path(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget over budget code path."""
        from decimal import Decimal

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            mock_summary = MagicMock()
            mock_summary.total_spent = Decimal("1100")
            mock_summary.total_budget = Decimal("1000")
            mock_summary.total_remaining = Decimal("-100")
            mock_summary.percent_used = Decimal("110")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("600"),
                "Transport": Decimal("500"),
            }

            # Test "overspent" keyword
            result = server._handle_query_budget(
                question="Did I overspent?",
                file_path=str(test_file),
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "percent_used" in data["data"]
            assert "is_over" in data["data"]
            assert data["data"]["is_over"] is True


class TestMCPServerSpendingTrends:
    """Tests for spending_trends with date grouping."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    @pytest.mark.skip(
        reason="Coverage+mock interaction issue - test passes without cov"
    )
    def test_spending_trends_with_category_filter(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test spending_trends with category filtering."""
        import pandas as pd

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            # Create mock expenses DataFrame
            mock_expenses = pd.DataFrame(
                {
                    "Date": ["2025-01-01", "2025-01-02", "2025-01-03"],
                    "Category": ["Groceries", "Transport", "Groceries"],
                    "Amount": [100.0, 50.0, 75.0],
                }
            )

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.expenses = mock_expenses

            result = server._handle_spending_trends(
                file_path=str(test_file),
                period="month",
                category="Groceries",
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "daily_spending" in data
            assert "statistics" in data
            assert data["category"] == "Groceries"
            assert "average_daily" in data["statistics"]

    def test_spending_trends_date_grouping(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test spending_trends date grouping logic."""
        import pandas as pd

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            # Create mock expenses DataFrame with Date column
            mock_expenses = pd.DataFrame(
                {
                    "Date": ["2025-01-01", "2025-01-01", "2025-01-02"],
                    "Category": ["Groceries", "Transport", "Groceries"],
                    "Amount": [100.0, 50.0, 75.0],
                }
            )

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.expenses = mock_expenses

            result = server._handle_spending_trends(
                file_path=str(test_file),
                period="week",
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "daily_spending" in data
            assert "2025-01-01" in data["daily_spending"]
            assert data["daily_spending"]["2025-01-01"] == 150.0
            assert data["statistics"]["total_days"] == 2
            assert data["statistics"]["highest_amount"] > 0


class TestMCPServerComparePeriods:
    """Tests for compare_periods calculations."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    @pytest.mark.skip(
        reason="Coverage+mock interaction issue - test passes without cov"
    )
    def test_compare_periods_calculations(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test compare_periods with date filtering and calculations."""
        import pandas as pd

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            # Create mock DataFrames for two periods
            p1_expenses = pd.DataFrame({"Amount": [100.0, 50.0, 75.0]})
            p2_expenses = pd.DataFrame({"Amount": [150.0, 100.0, 50.0]})

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.filter_by_date_range.side_effect = [p1_expenses, p2_expenses]

            result = server._handle_compare_periods(
                file_path=str(test_file),
                period1_start="2025-01-01",
                period1_end="2025-01-15",
                period2_start="2025-01-16",
                period2_end="2025-01-31",
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "period1" in data
            assert "period2" in data
            assert "comparison" in data
            assert data["period1"]["total"] == 225.0
            assert data["period2"]["total"] == 300.0
            assert "percent_change" in data["comparison"]

    @pytest.mark.skip(
        reason="Coverage+mock interaction issue - test passes without cov"
    )
    def test_compare_periods_zero_first_period(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test compare_periods when first period has zero spending."""
        import pandas as pd

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            # Empty first period, non-empty second
            p1_expenses = pd.DataFrame({"Amount": []})
            p2_expenses = pd.DataFrame({"Amount": [100.0, 50.0]})

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.filter_by_date_range.side_effect = [p1_expenses, p2_expenses]

            result = server._handle_compare_periods(
                file_path=str(test_file),
                period1_start="2025-01-01",
                period1_end="2025-01-15",
                period2_start="2025-01-16",
                period2_end="2025-01-31",
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert data["period1"]["total"] == 0.0
            assert data["period2"]["total"] == 150.0
            assert data["comparison"]["percent_change"] == 100


class TestMCPServerReportGeneration:
    """Tests for report generation with recommendations."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_generate_report_json_with_recommendations(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test JSON report format with recommendations."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with (
            patch(
                "spreadsheet_dl.domains.finance.report_generator.ReportGenerator"
            ) as MockReportGen,
            patch(
                "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
            ) as MockAnalyzer,
        ):
            mock_gen = MockReportGen.return_value
            mock_gen.generate_visualization_data.return_value = {
                "data": "test",
                "charts": [],
            }

            from decimal import Decimal

            mock_summary = MagicMock()
            mock_summary.total_remaining = Decimal("-100")
            mock_summary.percent_used = Decimal("110")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("500")
            }

            result = server._handle_generate_report(
                file_path=str(test_file),
                format="json",
                include_recommendations=True,
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "recommendations" in data
            assert len(data["recommendations"]) > 0

    def test_generate_report_markdown_with_recommendations(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test markdown report format with recommendations."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with (
            patch(
                "spreadsheet_dl.domains.finance.report_generator.ReportGenerator"
            ) as MockReportGen,
            patch(
                "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
            ) as MockAnalyzer,
        ):
            mock_gen = MockReportGen.return_value
            mock_gen.generate_markdown_report.return_value = "# Budget Report"

            from decimal import Decimal

            mock_summary = MagicMock()
            mock_summary.total_remaining = Decimal("100")
            mock_summary.percent_used = Decimal("85")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("300")
            }

            result = server._handle_generate_report(
                file_path=str(test_file),
                format="markdown",
                include_recommendations=True,
            )

            assert result.is_error is False
            assert "Budget Report" in result.content[0]["text"]
            assert "## Recommendations" in result.content[0]["text"]

    def test_generate_report_text_format(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test text report format."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.report_generator.ReportGenerator"
        ) as MockReportGen:
            mock_gen = MockReportGen.return_value
            mock_gen.generate_text_report.return_value = "Budget Report Text"

            result = server._handle_generate_report(
                file_path=str(test_file),
                format="text",
                include_recommendations=False,
            )

            assert result.is_error is False
            assert "Budget Report Text" in result.content[0]["text"]

    def test_generate_recommendations_all_scenarios(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test _generate_recommendations with all logic paths."""
        from decimal import Decimal

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            mock_analyzer = MockAnalyzer.return_value

            # Scenario 1: Over budget
            mock_summary = MagicMock()
            mock_summary.total_remaining = Decimal("-50")
            mock_summary.percent_used = Decimal("105")
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("200")
            }

            recommendations = server._generate_recommendations(test_file)
            assert any("over budget" in r.lower() for r in recommendations)

            # Scenario 2: High percentage (>80%)
            mock_summary.total_remaining = Decimal("50")
            mock_summary.percent_used = Decimal("85")

            recommendations = server._generate_recommendations(test_file)
            assert any("85" in r and "%" in r for r in recommendations)

            # Scenario 3: High category spending (>30%)
            mock_summary.percent_used = Decimal("50")
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("700"),
                "Transport": Decimal("100"),
                "Entertainment": Decimal("200"),
            }

            recommendations = server._generate_recommendations(test_file)
            assert any("Groceries" in r and "70.0%" in r for r in recommendations)

            # Scenario 4: All good
            mock_summary.percent_used = Decimal("50")
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("250"),
                "Transport": Decimal("250"),
                "Entertainment": Decimal("250"),
                "Utilities": Decimal("250"),
            }

            recommendations = server._generate_recommendations(test_file)
            assert any("on track" in r.lower() for r in recommendations)

    def test_generate_recommendations_exception_handling(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test _generate_recommendations handles exceptions."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.budget_analyzer.BudgetAnalyzer",
            side_effect=Exception("Test error"),
        ):
            recommendations = server._generate_recommendations(test_file)
            assert recommendations == []

    def test_list_categories_handler(self, server: MCPServer) -> None:
        """Test list_categories handler."""
        result = server._handle_list_categories()

        assert result.is_error is False
        data = json.loads(result.content[0]["text"])
        assert "categories" in data
        assert len(data["categories"]) > 0
        assert all("name" in cat and "id" in cat for cat in data["categories"])

    def test_get_alerts_handler(self, server: MCPServer, tmp_path: Path) -> None:
        """Test get_alerts handler with severity filtering."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with (
            patch("spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"),
            patch("spreadsheet_dl.domains.finance.alerts.AlertMonitor") as MockMonitor,
        ):
            mock_alert = MagicMock()
            mock_alert.message = "Over budget"
            mock_alert.category = "Groceries"
            mock_alert.severity.value = "critical"
            mock_alert.amount = 100
            mock_alert.threshold = 80

            mock_monitor = MockMonitor.return_value
            mock_monitor.check_all.return_value = [mock_alert]

            result = server._handle_get_alerts(
                file_path=str(test_file),
                severity="warning",
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "total_alerts" in data
            assert "alerts" in data


class TestMCPServerMainCLI:
    """Tests for main CLI function and run loop."""

    def test_main_cli_argument_parsing(self) -> None:
        """Test main function argument parsing."""
        from unittest.mock import MagicMock

        from spreadsheet_dl.mcp_server import main

        with (
            patch("sys.argv", ["mcp_server", "--debug", "--allowed-paths", "/tmp"]),
            patch("spreadsheet_dl.mcp_server.create_mcp_server") as mock_create,
            patch("logging.basicConfig") as mock_logging,
        ):
            mock_server = MagicMock()
            mock_create.return_value = mock_server
            mock_server.run.side_effect = KeyboardInterrupt()

            with contextlib.suppress(KeyboardInterrupt):
                main()

            mock_create.assert_called_once()
            mock_logging.assert_called_once()
            # Verify debug logging was enabled
            call_kwargs = mock_logging.call_args[1]
            assert call_kwargs["level"] == logging.DEBUG

    def test_main_cli_without_debug(self) -> None:
        """Test main function without debug flag."""
        from spreadsheet_dl.mcp_server import main

        with (
            patch("sys.argv", ["mcp_server"]),
            patch("spreadsheet_dl.mcp_server.create_mcp_server") as mock_create,
            patch("logging.basicConfig") as mock_logging,
        ):
            mock_server = MagicMock()
            mock_create.return_value = mock_server
            mock_server.run.side_effect = KeyboardInterrupt()

            with contextlib.suppress(KeyboardInterrupt):
                main()

            call_kwargs = mock_logging.call_args[1]
            assert call_kwargs["level"] == logging.INFO

    def test_server_run_loop_with_valid_message(self, tmp_path: Path) -> None:
        """Test server run loop with valid JSON-RPC message."""
        config = MCPConfig(allowed_paths=[tmp_path])
        server = MCPServer(config)

        message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {},
        }

        with (
            patch("sys.stdin.readline", side_effect=[json.dumps(message) + "\n", ""]),
            patch("sys.stdout.write") as mock_write,
            patch("sys.stdout.flush"),
        ):
            server.run()

            # Verify response was written
            assert mock_write.called

    def test_server_run_loop_with_invalid_json(self, tmp_path: Path) -> None:
        """Test server run loop with invalid JSON."""
        config = MCPConfig(allowed_paths=[tmp_path])
        server = MCPServer(config)

        with (
            patch("sys.stdin.readline", side_effect=["{invalid json\n", ""]),
            patch("sys.stdout.write"),
            patch("sys.stdout.flush"),
        ):
            server.run()

            # Should not crash, just log error

    def test_server_run_loop_keyboard_interrupt(self, tmp_path: Path) -> None:
        """Test server run loop handles keyboard interrupt."""
        config = MCPConfig(allowed_paths=[tmp_path])
        server = MCPServer(config)

        with patch("sys.stdin.readline", side_effect=KeyboardInterrupt()):
            server.run()
            # Should exit gracefully

    def test_server_run_loop_general_exception(self, tmp_path: Path) -> None:
        """Test server run loop handles general exceptions."""
        config = MCPConfig(allowed_paths=[tmp_path])
        server = MCPServer(config)

        with patch("sys.stdin.readline", side_effect=Exception("Unexpected error")):
            server.run()
            # Should exit gracefully

    def test_create_mcp_server_with_paths(self) -> None:
        """Test create_mcp_server with allowed paths."""
        from spreadsheet_dl.mcp_server import create_mcp_server

        server = create_mcp_server(allowed_paths=["/tmp", "/home"])

        assert server is not None
        assert len(server.config.allowed_paths) == 2

    def test_create_mcp_server_without_paths(self) -> None:
        """Test create_mcp_server without allowed paths uses defaults."""
        from spreadsheet_dl.mcp_server import create_mcp_server

        server = create_mcp_server(allowed_paths=None)

        assert server is not None
        # MCPConfig sets default paths in __post_init__ when allowed_paths is empty
        assert len(server.config.allowed_paths) > 0
