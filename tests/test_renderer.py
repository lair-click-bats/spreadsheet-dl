"""Tests for renderer module."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

import pytest

from finance_tracker.builder import (
    CellSpec,
    ColumnSpec,
    RowSpec,
    SheetSpec,
    SpreadsheetBuilder,
)
from finance_tracker.renderer import OdsRenderer, render_sheets

if TYPE_CHECKING:
    from pathlib import Path

    pass


class TestOdsRenderer:
    """Tests for OdsRenderer class."""

    def test_render_empty_sheet(self, tmp_path: Path) -> None:
        """Test rendering empty sheet."""
        output = tmp_path / "empty.ods"
        sheets = [SheetSpec(name="Empty")]

        renderer = OdsRenderer()
        path = renderer.render(sheets, output)

        assert path.exists()
        assert path.stat().st_size > 0

    def test_render_sheet_with_columns(self, tmp_path: Path) -> None:
        """Test rendering sheet with columns."""
        output = tmp_path / "columns.ods"
        sheets = [
            SheetSpec(
                name="Test",
                columns=[
                    ColumnSpec(name="Date", width="2.5cm", type="date"),
                    ColumnSpec(name="Category", width="3cm"),
                    ColumnSpec(name="Amount", width="2cm", type="currency"),
                ],
            ),
        ]

        renderer = OdsRenderer()
        path = renderer.render(sheets, output)

        assert path.exists()

    def test_render_sheet_with_rows(self, tmp_path: Path) -> None:
        """Test rendering sheet with data rows."""
        output = tmp_path / "rows.ods"
        sheets = [
            SheetSpec(
                name="Test",
                columns=[
                    ColumnSpec(name="A"),
                    ColumnSpec(name="B"),
                ],
                rows=[
                    RowSpec(cells=[CellSpec(value="A"), CellSpec(value="B")]),
                    RowSpec(cells=[CellSpec(value="1"), CellSpec(value="2")]),
                ],
            ),
        ]

        renderer = OdsRenderer()
        path = renderer.render(sheets, output)

        assert path.exists()

    def test_render_with_formulas(self, tmp_path: Path) -> None:
        """Test rendering sheet with formulas."""
        output = tmp_path / "formulas.ods"
        sheets = [
            SheetSpec(
                name="Test",
                columns=[
                    ColumnSpec(name="Values", type="float"),
                    ColumnSpec(name="Sum", type="float"),
                ],
                rows=[
                    RowSpec(cells=[CellSpec(value=10), CellSpec()]),
                    RowSpec(cells=[CellSpec(value=20), CellSpec()]),
                    RowSpec(
                        cells=[
                            CellSpec(value="Total"),
                            CellSpec(formula="of:=SUM([.A1:A2])"),
                        ]
                    ),
                ],
            ),
        ]

        renderer = OdsRenderer()
        path = renderer.render(sheets, output)

        assert path.exists()

    def test_render_multi_sheet(self, tmp_path: Path) -> None:
        """Test rendering multiple sheets."""
        output = tmp_path / "multi.ods"
        sheets = [
            SheetSpec(name="Sheet1", columns=[ColumnSpec(name="A")]),
            SheetSpec(name="Sheet2", columns=[ColumnSpec(name="B")]),
            SheetSpec(name="Sheet3", columns=[ColumnSpec(name="C")]),
        ]

        renderer = OdsRenderer()
        path = renderer.render(sheets, output)

        assert path.exists()

    def test_render_with_dates(self, tmp_path: Path) -> None:
        """Test rendering dates."""
        output = tmp_path / "dates.ods"
        sheets = [
            SheetSpec(
                name="Dates",
                columns=[ColumnSpec(name="Date", type="date")],
                rows=[
                    RowSpec(cells=[CellSpec(value=date(2025, 1, 15))]),
                    RowSpec(cells=[CellSpec(value=date(2025, 1, 16))]),
                ],
            ),
        ]

        renderer = OdsRenderer()
        path = renderer.render(sheets, output)

        assert path.exists()

    def test_render_with_decimals(self, tmp_path: Path) -> None:
        """Test rendering Decimal values."""
        output = tmp_path / "decimals.ods"
        sheets = [
            SheetSpec(
                name="Currency",
                columns=[ColumnSpec(name="Amount", type="currency")],
                rows=[
                    RowSpec(cells=[CellSpec(value=Decimal("123.45"))]),
                    RowSpec(cells=[CellSpec(value=Decimal("678.90"))]),
                ],
            ),
        ]

        renderer = OdsRenderer()
        path = renderer.render(sheets, output)

        assert path.exists()

    def test_render_with_styles(self, tmp_path: Path) -> None:
        """Test rendering with style names."""
        output = tmp_path / "styled.ods"
        sheets = [
            SheetSpec(
                name="Styled",
                columns=[ColumnSpec(name="A")],
                rows=[
                    RowSpec(
                        cells=[CellSpec(value="Header", style="header")],
                        style="header",
                    ),
                    RowSpec(
                        cells=[CellSpec(value="100", style="currency")],
                    ),
                ],
            ),
        ]

        renderer = OdsRenderer()
        path = renderer.render(sheets, output)

        assert path.exists()


# Check if pyyaml is available
try:
    import yaml  # noqa: F401

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@pytest.mark.skipif(not HAS_YAML, reason="PyYAML not installed")
class TestOdsRendererWithTheme:
    """Tests for OdsRenderer with theme support."""

    def test_render_with_theme(self, tmp_path: Path) -> None:
        """Test rendering with theme."""
        from finance_tracker.schema.loader import ThemeLoader

        output = tmp_path / "themed.ods"
        loader = ThemeLoader()
        theme = loader.load("default")

        sheets = [
            SheetSpec(
                name="Themed",
                columns=[ColumnSpec(name="A")],
                rows=[
                    RowSpec(
                        cells=[CellSpec(value="Header", style="header_primary")],
                    ),
                ],
            ),
        ]

        renderer = OdsRenderer(theme=theme)
        path = renderer.render(sheets, output)

        assert path.exists()


class TestRenderSheetsFunction:
    """Tests for render_sheets convenience function."""

    def test_render_sheets_basic(self, tmp_path: Path) -> None:
        """Test render_sheets convenience function."""
        output = tmp_path / "basic.ods"
        sheets = [SheetSpec(name="Test", columns=[ColumnSpec(name="A")])]

        path = render_sheets(sheets, output)

        assert path.exists()

    def test_render_sheets_with_string_path(self, tmp_path: Path) -> None:
        """Test render_sheets with string path."""
        output = str(tmp_path / "string_path.ods")
        sheets = [SheetSpec(name="Test")]

        path = render_sheets(sheets, output)

        assert path.exists()


class TestRendererIntegration:
    """Integration tests for renderer with builder."""

    def test_builder_save_uses_renderer(self, tmp_path: Path) -> None:
        """Test that SpreadsheetBuilder.save uses renderer."""
        output = tmp_path / "builder_save.ods"

        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").column("B").header_row().data_rows(10)

        path = builder.save(output)

        assert path.exists()
        assert path.stat().st_size > 0

    def test_complete_budget_workflow(self, tmp_path: Path) -> None:
        """Test complete budget spreadsheet workflow."""
        output = tmp_path / "complete_budget.ods"

        builder = SpreadsheetBuilder(theme=None)

        # Expense Log sheet
        builder.sheet("Expense Log").column("Date", width="2.5cm", type="date").column(
            "Category", width="3cm"
        ).column("Description", width="4cm").column(
            "Amount", width="2.5cm", type="currency"
        ).column("Notes", width="4cm").header_row(style="header").data_rows(50)

        # Budget sheet
        builder.sheet("Budget").column("Category", width="3cm").column(
            "Monthly Budget", width="3cm", type="currency"
        ).header_row(style="header")

        # Add sample budget rows
        categories = ["Groceries", "Utilities", "Entertainment"]
        for cat in categories:
            builder.row().cell(cat).cell(Decimal("500"))

        path = builder.save(output)

        assert path.exists()
        assert path.stat().st_size > 0
