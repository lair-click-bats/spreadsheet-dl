"""Tests for renderer module."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

import pytest

from spreadsheet_dl.builder import (
    CellSpec,
    ColumnSpec,
    RowSpec,
    SheetSpec,
    SpreadsheetBuilder,
)
from spreadsheet_dl.renderer import OdsRenderer, render_sheets

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
        from spreadsheet_dl.schema.loader import ThemeLoader

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


# =============================================================================
# Chart Rendering Tests (TASK-231)
# =============================================================================


class TestChartRendering:
    """Tests for chart rendering functionality (TASK-231).

    Implements validation for GAP-BUILDER-006: Charts defined but not rendered.
    """

    def test_render_with_chart_spec(self, tmp_path: Path) -> None:
        """Test rendering with chart specification."""
        from spreadsheet_dl.charts import ChartBuilder

        output = tmp_path / "with_chart.ods"
        sheets = [
            SheetSpec(
                name="Data",
                columns=[
                    ColumnSpec(name="Month"),
                    ColumnSpec(name="Value", type="float"),
                ],
                rows=[
                    RowSpec(cells=[CellSpec(value="Jan"), CellSpec(value=100)]),
                    RowSpec(cells=[CellSpec(value="Feb"), CellSpec(value=150)]),
                    RowSpec(cells=[CellSpec(value="Mar"), CellSpec(value=200)]),
                ],
            ),
        ]

        # Create a chart
        chart = (
            ChartBuilder()
            .column_chart()
            .title("Monthly Values")
            .series("Values", "Data.B1:B3")
            .categories("Data.A1:A3")
            .position("D1")
            .size(400, 300)
            .build()
        )

        renderer = OdsRenderer()
        path = renderer.render(sheets, output, charts=[chart])

        assert path.exists()
        assert path.stat().st_size > 0

    def test_render_line_chart(self, tmp_path: Path) -> None:
        """Test rendering line chart."""
        from spreadsheet_dl.charts import ChartBuilder

        output = tmp_path / "line_chart.ods"
        sheets = [SheetSpec(name="Data")]

        chart = (
            ChartBuilder()
            .line_chart(markers=True)
            .title("Trend Line")
            .series("Trend", "Data.B1:B12")
            .build()
        )

        renderer = OdsRenderer()
        path = renderer.render(sheets, output, charts=[chart])

        assert path.exists()

    def test_render_pie_chart(self, tmp_path: Path) -> None:
        """Test rendering pie chart."""
        from spreadsheet_dl.charts import ChartBuilder

        output = tmp_path / "pie_chart.ods"
        sheets = [SheetSpec(name="Data")]

        chart = (
            ChartBuilder()
            .pie_chart()
            .title("Distribution")
            .series("Values", "Data.B1:B5")
            .categories("Data.A1:A5")
            .data_labels(show_percentage=True)
            .build()
        )

        renderer = OdsRenderer()
        path = renderer.render(sheets, output, charts=[chart])

        assert path.exists()

    def test_render_bar_chart(self, tmp_path: Path) -> None:
        """Test rendering bar chart (horizontal)."""
        from spreadsheet_dl.charts import ChartBuilder

        output = tmp_path / "bar_chart.ods"
        sheets = [SheetSpec(name="Data")]

        chart = (
            ChartBuilder()
            .bar_chart()
            .title("Comparison")
            .series("Group A", "Data.B1:B5")
            .series("Group B", "Data.C1:C5")
            .legend(position="right")
            .build()
        )

        renderer = OdsRenderer()
        path = renderer.render(sheets, output, charts=[chart])

        assert path.exists()

    def test_render_area_chart(self, tmp_path: Path) -> None:
        """Test rendering area chart."""
        from spreadsheet_dl.charts import ChartBuilder

        output = tmp_path / "area_chart.ods"
        sheets = [SheetSpec(name="Data")]

        chart = (
            ChartBuilder()
            .area_chart(stacked=True)
            .title("Stacked Area")
            .series("Series 1", "Data.B1:B10")
            .series("Series 2", "Data.C1:C10")
            .build()
        )

        renderer = OdsRenderer()
        path = renderer.render(sheets, output, charts=[chart])

        assert path.exists()

    def test_render_chart_with_axis_config(self, tmp_path: Path) -> None:
        """Test rendering chart with axis configuration."""
        from spreadsheet_dl.charts import ChartBuilder

        output = tmp_path / "axis_config_chart.ods"
        sheets = [SheetSpec(name="Data")]

        chart = (
            ChartBuilder()
            .column_chart()
            .title("With Axis Config")
            .series("Values", "Data.B1:B10")
            .axis("category", title="Categories")
            .axis("value", title="Amount ($)", min=0, max=1000)
            .build()
        )

        renderer = OdsRenderer()
        path = renderer.render(sheets, output, charts=[chart])

        assert path.exists()

    def test_render_multiple_charts(self, tmp_path: Path) -> None:
        """Test rendering multiple charts on same sheet."""
        from spreadsheet_dl.charts import ChartBuilder

        output = tmp_path / "multiple_charts.ods"
        sheets = [SheetSpec(name="Data")]

        chart1 = (
            ChartBuilder()
            .column_chart()
            .title("Chart 1")
            .series("Values", "Data.B1:B5")
            .position("D1")
            .build()
        )

        chart2 = (
            ChartBuilder()
            .line_chart()
            .title("Chart 2")
            .series("Trend", "Data.C1:C5")
            .position("D15")
            .build()
        )

        renderer = OdsRenderer()
        path = renderer.render(sheets, output, charts=[chart1, chart2])

        assert path.exists()

    def test_render_chart_with_legend(self, tmp_path: Path) -> None:
        """Test chart with legend configuration."""
        from spreadsheet_dl.charts import ChartBuilder, LegendPosition

        output = tmp_path / "chart_legend.ods"
        sheets = [SheetSpec(name="Data")]

        chart = (
            ChartBuilder()
            .column_chart()
            .title("With Legend")
            .series("Budget", "Data.B1:B5")
            .series("Actual", "Data.C1:C5")
            .legend(position="bottom", visible=True)
            .build()
        )

        assert chart.legend.position == LegendPosition.BOTTOM
        assert chart.legend.visible is True

        renderer = OdsRenderer()
        path = renderer.render(sheets, output, charts=[chart])

        assert path.exists()

    def test_chart_type_mapping(self) -> None:
        """Test that chart types are correctly mapped to ODF classes."""
        from spreadsheet_dl.charts import ChartType

        renderer = OdsRenderer()

        # Test various chart type mappings
        assert renderer._get_odf_chart_class(ChartType.COLUMN) == "chart:bar"
        assert renderer._get_odf_chart_class(ChartType.LINE) == "chart:line"
        assert renderer._get_odf_chart_class(ChartType.PIE) == "chart:circle"
        assert renderer._get_odf_chart_class(ChartType.AREA) == "chart:area"
        assert renderer._get_odf_chart_class(ChartType.SCATTER) == "chart:scatter"
        assert renderer._get_odf_chart_class(ChartType.DOUGHNUT) == "chart:ring"

    def test_legend_position_mapping(self) -> None:
        """Test that legend positions are correctly mapped."""
        from spreadsheet_dl.charts import LegendPosition

        renderer = OdsRenderer()

        assert renderer._get_odf_legend_position(LegendPosition.TOP) == "top"
        assert renderer._get_odf_legend_position(LegendPosition.BOTTOM) == "bottom"
        assert renderer._get_odf_legend_position(LegendPosition.LEFT) == "start"
        assert renderer._get_odf_legend_position(LegendPosition.RIGHT) == "end"
        assert renderer._get_odf_legend_position(LegendPosition.NONE) == "none"


class TestConditionalFormatRendering:
    """Tests for conditional format rendering (TASK-211)."""

    def test_render_with_color_scale(self, tmp_path: Path) -> None:
        """Test rendering with color scale conditional format."""
        from spreadsheet_dl.schema.conditional import (
            ColorScale,
            ConditionalFormat,
            ConditionalRule,
            ConditionalRuleType,
        )

        output = tmp_path / "color_scale.ods"
        sheets = [SheetSpec(name="Data")]

        # Create color scale conditional format
        cf = ConditionalFormat(
            range="B2:B20",
            rules=[
                ConditionalRule(
                    type=ConditionalRuleType.COLOR_SCALE,
                    color_scale=ColorScale.red_yellow_green(),
                )
            ],
        )

        renderer = OdsRenderer()
        path = renderer.render(sheets, output, conditional_formats=[cf])

        assert path.exists()

    def test_render_with_data_bar(self, tmp_path: Path) -> None:
        """Test rendering with data bar conditional format."""
        from spreadsheet_dl.schema.conditional import (
            ConditionalFormat,
            ConditionalRule,
            ConditionalRuleType,
            DataBar,
        )

        output = tmp_path / "data_bar.ods"
        sheets = [SheetSpec(name="Data")]

        cf = ConditionalFormat(
            range="C2:C20",
            rules=[
                ConditionalRule(
                    type=ConditionalRuleType.DATA_BAR,
                    data_bar=DataBar.default(),
                )
            ],
        )

        renderer = OdsRenderer()
        path = renderer.render(sheets, output, conditional_formats=[cf])

        assert path.exists()


class TestDataValidationRendering:
    """Tests for data validation rendering (TASK-221)."""

    def test_render_with_list_validation(self, tmp_path: Path) -> None:
        """Test rendering with list validation."""
        from spreadsheet_dl.schema.data_validation import (
            DataValidation,
            ValidationConfig,
        )

        output = tmp_path / "list_validation.ods"
        sheets = [SheetSpec(name="Data")]

        validation = ValidationConfig(
            range="A2:A20",
            validation=DataValidation.list(
                items=["Option 1", "Option 2", "Option 3"],
            ),
        )

        renderer = OdsRenderer()
        path = renderer.render(sheets, output, validations=[validation])

        assert path.exists()

    def test_render_with_number_validation(self, tmp_path: Path) -> None:
        """Test rendering with number validation."""
        from spreadsheet_dl.schema.data_validation import (
            DataValidation,
            ValidationConfig,
        )

        output = tmp_path / "number_validation.ods"
        sheets = [SheetSpec(name="Data")]

        validation = ValidationConfig(
            range="B2:B20",
            validation=DataValidation.positive_number(),
        )

        renderer = OdsRenderer()
        path = renderer.render(sheets, output, validations=[validation])

        assert path.exists()
