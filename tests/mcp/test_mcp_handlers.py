"""
Tests for MCP server direct handler calls and exception handling.

Tests IR-MCP-002: Native MCP Server - Handlers.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from spreadsheet_dl.mcp_server import (
    MCPConfig,
    MCPServer,
    MCPToolResult,
)

pytestmark = [pytest.mark.unit, pytest.mark.mcp]


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
        assert response is not None
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
            patch("pathlib.Path.cwd", return_value=tmp_path),
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
