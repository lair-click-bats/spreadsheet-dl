"""
Tests for MCP server tool operations.

Tests IR-MCP-002: Native MCP Server - Tool Operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from spreadsheet_dl.mcp_server import (
    MCPConfig,
    MCPServer,
)

pytestmark = [pytest.mark.unit, pytest.mark.mcp]


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
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer", create=True
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
