"""
Tests for extended MCP tool categories.

Tests TASK-501: Expansion from 49 to 145 MCP tools.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from spreadsheet_dl.mcp_server import MCPServer, MCPToolResult


@pytest.fixture
def mcp_server(tmp_path: Path) -> MCPServer:
    """Create a test MCP server with temporary path allowed."""
    from spreadsheet_dl.mcp_server import MCPConfig

    config = MCPConfig(allowed_paths=[tmp_path])
    return MCPServer(config)


@pytest.fixture
def test_file(tmp_path: Path) -> Path:
    """Create a test file."""
    file_path = tmp_path / "test.ods"
    file_path.touch()
    return file_path


class TestWorkbookOperations:
    """Tests for workbook operation tools (TASK-501)."""

    def test_workbook_tools_registered(self, mcp_server: MCPServer) -> None:
        """Test that all workbook operation tools are registered."""
        expected_tools = [
            "workbook_properties_get",
            "workbook_properties_set",
            "workbook_metadata_get",
            "workbook_metadata_set",
            "workbook_protection_enable",
            "workbook_protection_disable",
            "formulas_recalculate",
            "links_update",
            "links_break",
            "data_connections_list",
            "data_refresh",
            "workbooks_compare",
            "workbooks_merge",
            "workbook_statistics",
            "formulas_audit",
            "circular_refs_find",
        ]

        for tool_name in expected_tools:
            assert tool_name in mcp_server._tools, f"Tool {tool_name} not registered"
            tool = mcp_server._tools[tool_name]
            assert tool.handler is not None, f"Tool {tool_name} has no handler"

    def test_workbook_properties_get(
        self, mcp_server: MCPServer, test_file: Path
    ) -> None:
        """Test workbook properties retrieval."""
        result = mcp_server._handle_workbook_properties_get(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error
        # Stub implementation returns JSON with properties
        assert len(result.content) > 0

    def test_workbook_statistics(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test workbook statistics."""
        result = mcp_server._handle_workbook_statistics(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error


class TestThemeManagement:
    """Tests for theme management tools (TASK-501)."""

    def test_theme_tools_registered(self, mcp_server: MCPServer) -> None:
        """Test that all theme management tools are registered."""
        expected_tools = [
            "theme_list",
            "theme_get",
            "theme_create",
            "theme_update",
            "theme_delete",
            "theme_apply",
            "theme_export",
            "theme_import",
            "theme_preview",
            "color_scheme_generate",
            "font_set_apply",
            "style_guide_create",
        ]

        for tool_name in expected_tools:
            assert tool_name in mcp_server._tools, f"Tool {tool_name} not registered"

    def test_theme_list(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test theme listing."""
        result = mcp_server._handle_theme_list(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error

    def test_theme_create(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test theme creation."""
        result = mcp_server._handle_theme_create(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error


class TestPrintLayout:
    """Tests for print layout tools (TASK-501)."""

    def test_print_tools_registered(self, mcp_server: MCPServer) -> None:
        """Test that all print layout tools are registered."""
        expected_tools = [
            "page_setup",
            "print_area_set",
            "page_breaks_insert",
            "page_breaks_remove",
            "header_footer_set",
            "print_titles_set",
            "print_options_set",
            "pages_fit_to",
            "print_preview",
            "pdf_export",
        ]

        for tool_name in expected_tools:
            assert tool_name in mcp_server._tools, f"Tool {tool_name} not registered"

    def test_page_setup(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test page setup."""
        result = mcp_server._handle_page_setup(str(test_file), "Sheet1")
        assert isinstance(result, MCPToolResult)
        assert not result.is_error

    def test_pdf_export(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test PDF export."""
        result = mcp_server._handle_pdf_export(str(test_file), "Sheet1")
        assert isinstance(result, MCPToolResult)
        assert not result.is_error


class TestImportExport:
    """Tests for import/export tools (TASK-501)."""

    def test_import_export_tools_registered(self, mcp_server: MCPServer) -> None:
        """Test that all import/export tools are registered."""
        expected_tools = [
            "csv_import",
            "tsv_import",
            "json_import",
            "xlsx_import",
            "xml_import",
            "html_import",
            "csv_export",
            "tsv_export",
            "json_export",
            "xlsx_export",
            "xml_export",
            "html_export",
            "batch_import",
            "batch_export",
            "data_mapping_create",
            "column_mapping_apply",
            "format_auto_detect",
        ]

        for tool_name in expected_tools:
            assert tool_name in mcp_server._tools, f"Tool {tool_name} not registered"

    def test_csv_import(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test CSV import."""
        result = mcp_server._handle_csv_import(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error

    def test_json_export(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test JSON export."""
        result = mcp_server._handle_json_export(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error

    def test_format_auto_detect(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test format auto-detection."""
        result = mcp_server._handle_format_auto_detect(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error


class TestAccountOperations:
    """Tests for account operation tools (TASK-501)."""

    def test_account_tools_registered(self, mcp_server: MCPServer) -> None:
        """Test that all account operation tools are registered."""
        expected_tools = [
            "account_create",
            "account_list",
            "account_get",
            "account_update",
            "account_delete",
            "account_balance",
            "account_transactions",
            "account_reconcile",
            "account_statement_import",
            "account_statement_export",
            "account_budgets",
            "account_analysis",
            "account_trends",
            "account_categories",
            "account_tags",
        ]

        for tool_name in expected_tools:
            assert tool_name in mcp_server._tools, f"Tool {tool_name} not registered"

    def test_account_create(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test account creation."""
        result = mcp_server._handle_account_create(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error

    def test_account_balance(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test account balance retrieval."""
        result = mcp_server._handle_account_balance(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error

    def test_account_analysis(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test account analysis."""
        result = mcp_server._handle_account_analysis(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error


class TestGoalTracking:
    """Tests for goal tracking tools (TASK-501)."""

    def test_goal_tools_registered(self, mcp_server: MCPServer) -> None:
        """Test that all goal tracking tools are registered."""
        expected_tools = [
            "goal_create",
            "goal_list",
            "goal_get",
            "goal_update",
            "goal_delete",
            "goal_progress",
            "goal_milestones",
            "goal_projections",
            "debt_payoff_plan",
            "savings_plan",
            "investment_plan",
            "goal_dashboard",
        ]

        for tool_name in expected_tools:
            assert tool_name in mcp_server._tools, f"Tool {tool_name} not registered"

    def test_goal_create(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test goal creation."""
        result = mcp_server._handle_goal_create(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error

    def test_goal_progress(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test goal progress tracking."""
        result = mcp_server._handle_goal_progress(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error

    def test_debt_payoff_plan(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test debt payoff plan generation."""
        result = mcp_server._handle_debt_payoff_plan(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error


class TestReporting:
    """Tests for reporting tools (TASK-501)."""

    def test_reporting_tools_registered(self, mcp_server: MCPServer) -> None:
        """Test that all reporting tools are registered."""
        expected_tools = [
            # "report_generate" is excluded (already exists as "generate_report")
            "report_schedule",
            "report_list",
            "report_templates",
            "cash_flow_report",
            "income_statement",
            "balance_sheet",
            "budget_variance",
            "category_breakdown",
            "trend_analysis",
            "forecast",
            "what_if_analysis",
            "report_export",
            "report_email",
        ]

        for tool_name in expected_tools:
            assert tool_name in mcp_server._tools, f"Tool {tool_name} not registered"

    def test_cash_flow_report(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test cash flow report generation."""
        result = mcp_server._handle_cash_flow_report(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error

    def test_forecast(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test financial forecasting."""
        result = mcp_server._handle_forecast(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error

    def test_what_if_analysis(self, mcp_server: MCPServer, test_file: Path) -> None:
        """Test what-if analysis."""
        result = mcp_server._handle_what_if_analysis(str(test_file))
        assert isinstance(result, MCPToolResult)
        assert not result.is_error


class TestToolCountsAndCategories:
    """Tests for overall tool organization (TASK-501)."""

    def test_total_tool_count(self, mcp_server: MCPServer) -> None:
        """Test that we have 144+ tools (49 original + 95 new)."""
        total_tools = len(mcp_server._tools)
        assert total_tools >= 144, f"Expected at least 144 tools, got {total_tools}"

    def test_category_count(self, mcp_server: MCPServer) -> None:
        """Test that we have all expected categories."""
        categories = mcp_server._registry.get_categories()
        expected_categories = [
            "cell_operations",
            "style_operations",
            "structure_operations",
            "advanced_operations",
            "workbook_operations",
            "theme_management",
            "print_layout",
            "import_export",
            "account_operations",
            "goal_tracking",
            "reporting",
        ]

        for cat in expected_categories:
            assert cat in categories, f"Category {cat} not found"

    def test_workbook_category_count(self, mcp_server: MCPServer) -> None:
        """Test workbook operations category has 16 tools."""
        tools = mcp_server._registry.get_tools_by_category("workbook_operations")
        assert len(tools) == 16

    def test_theme_category_count(self, mcp_server: MCPServer) -> None:
        """Test theme management category has 12 tools."""
        tools = mcp_server._registry.get_tools_by_category("theme_management")
        assert len(tools) == 12

    def test_print_category_count(self, mcp_server: MCPServer) -> None:
        """Test print layout category has 10 tools."""
        tools = mcp_server._registry.get_tools_by_category("print_layout")
        assert len(tools) == 10

    def test_import_export_category_count(self, mcp_server: MCPServer) -> None:
        """Test import/export category has 17 tools."""
        tools = mcp_server._registry.get_tools_by_category("import_export")
        assert len(tools) == 17

    def test_account_category_count(self, mcp_server: MCPServer) -> None:
        """Test account operations category has 15 tools."""
        tools = mcp_server._registry.get_tools_by_category("account_operations")
        assert len(tools) == 15

    def test_goal_category_count(self, mcp_server: MCPServer) -> None:
        """Test goal tracking category has 12 tools."""
        tools = mcp_server._registry.get_tools_by_category("goal_tracking")
        assert len(tools) == 12

    def test_reporting_category_count(self, mcp_server: MCPServer) -> None:
        """Test reporting category has 13 tools."""
        tools = mcp_server._registry.get_tools_by_category("reporting")
        assert len(tools) == 13

    def test_all_tools_have_handlers(self, mcp_server: MCPServer) -> None:
        """Test that all tools have valid handlers."""
        for name, tool in mcp_server._tools.items():
            assert tool.handler is not None, f"Tool {name} has no handler"
            assert callable(tool.handler), f"Tool {name} handler is not callable"

    def test_stub_tools_return_success(
        self, mcp_server: MCPServer, test_file: Path
    ) -> None:
        """Test that stub implementations return success."""
        # Test a sample from each category
        stub_handlers = [
            ("_handle_workbook_properties_get", (str(test_file),)),
            ("_handle_theme_list", (str(test_file),)),
            ("_handle_page_setup", (str(test_file), "Sheet1")),
            ("_handle_csv_import", (str(test_file),)),
            ("_handle_account_create", (str(test_file),)),
            ("_handle_goal_create", (str(test_file),)),
            ("_handle_cash_flow_report", (str(test_file),)),
        ]

        for handler_name, args in stub_handlers:
            handler = getattr(mcp_server, handler_name)
            result = handler(*args)
            assert isinstance(result, MCPToolResult)
            assert not result.is_error, f"{handler_name} returned error"
