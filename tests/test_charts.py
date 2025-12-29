"""
Tests for charts module.

Implements tests for:
    - FR-CHART-001: Chart Type Support
    - FR-CHART-002: Chart Configuration
    - FR-CHART-003: Sparklines
    - FR-CHART-004: Chart Styling
    - FR-CHART-005: Chart Data Ranges
    - FR-CHART-006: Chart Positioning
    - FR-CHART-007: Trendlines
    - FR-BUILDER-004: ChartBuilder
"""


from finance_tracker.charts import (
    AxisConfig,
    ChartBuilder,
    ChartPosition,
    ChartSize,
    ChartTitle,
    ChartType,
    DataSeries,
    LegendConfig,
    LegendPosition,
    SparklineBuilder,
    SparklineType,
    Trendline,
    TrendlineType,
    budget_comparison_chart,
    chart,
    sparkline,
    spending_pie_chart,
    trend_line_chart,
)


class TestChartTypes:
    """Test chart type enums and selection (FR-CHART-001)."""

    def test_chart_type_enum_values(self) -> None:
        """Test ChartType enum has expected values."""
        assert ChartType.COLUMN is not None
        assert ChartType.COLUMN_STACKED is not None
        assert ChartType.BAR is not None
        assert ChartType.LINE is not None
        assert ChartType.PIE is not None
        assert ChartType.SCATTER is not None
        assert ChartType.COMBO is not None

    def test_column_chart_builder(self) -> None:
        """Test column chart creation."""
        spec = ChartBuilder().column_chart().build()
        assert spec.chart_type == ChartType.COLUMN

    def test_stacked_column_chart(self) -> None:
        """Test stacked column chart creation."""
        spec = ChartBuilder().column_chart(stacked=True).build()
        assert spec.chart_type == ChartType.COLUMN_STACKED

    def test_100_stacked_column_chart(self) -> None:
        """Test 100% stacked column chart creation."""
        spec = ChartBuilder().column_chart(stacked=True, percent=True).build()
        assert spec.chart_type == ChartType.COLUMN_100_STACKED

    def test_bar_chart_builder(self) -> None:
        """Test bar chart creation."""
        spec = ChartBuilder().bar_chart().build()
        assert spec.chart_type == ChartType.BAR

    def test_line_chart_builder(self) -> None:
        """Test line chart creation."""
        spec = ChartBuilder().line_chart().build()
        assert spec.chart_type == ChartType.LINE

    def test_line_chart_with_markers(self) -> None:
        """Test line chart with markers."""
        spec = ChartBuilder().line_chart(markers=True).build()
        assert spec.chart_type == ChartType.LINE_MARKERS

    def test_smooth_line_chart(self) -> None:
        """Test smooth line chart."""
        spec = ChartBuilder().line_chart(smooth=True).build()
        assert spec.chart_type == ChartType.LINE_SMOOTH

    def test_area_chart_builder(self) -> None:
        """Test area chart creation."""
        spec = ChartBuilder().area_chart().build()
        assert spec.chart_type == ChartType.AREA

    def test_pie_chart_builder(self) -> None:
        """Test pie chart creation."""
        spec = ChartBuilder().pie_chart().build()
        assert spec.chart_type == ChartType.PIE

    def test_doughnut_chart(self) -> None:
        """Test doughnut chart creation."""
        spec = ChartBuilder().pie_chart(doughnut=True).build()
        assert spec.chart_type == ChartType.DOUGHNUT

    def test_scatter_chart_builder(self) -> None:
        """Test scatter chart creation."""
        spec = ChartBuilder().scatter_chart().build()
        assert spec.chart_type == ChartType.SCATTER

    def test_combo_chart_builder(self) -> None:
        """Test combo chart creation."""
        spec = ChartBuilder().combo_chart().build()
        assert spec.chart_type == ChartType.COMBO


class TestChartConfiguration:
    """Test chart configuration options (FR-CHART-002)."""

    def test_chart_title(self) -> None:
        """Test setting chart title."""
        spec = (
            ChartBuilder()
            .column_chart()
            .title("Monthly Budget", font_size="16pt", font_weight="bold")
            .build()
        )
        assert spec.title is not None
        assert spec.title.text == "Monthly Budget"
        assert spec.title.font_size == "16pt"
        assert spec.title.font_weight == "bold"

    def test_chart_title_with_color(self) -> None:
        """Test title with custom color."""
        spec = (
            ChartBuilder()
            .column_chart()
            .title("Budget", color="#1A3A5C")
            .build()
        )
        assert spec.title is not None
        assert spec.title.color == "#1A3A5C"

    def test_legend_configuration(self) -> None:
        """Test legend configuration."""
        spec = (
            ChartBuilder()
            .column_chart()
            .legend(position="bottom", visible=True)
            .build()
        )
        assert spec.legend.position == LegendPosition.BOTTOM
        assert spec.legend.visible is True

    def test_legend_none(self) -> None:
        """Test hiding legend."""
        spec = (
            ChartBuilder()
            .column_chart()
            .legend(position="none")
            .build()
        )
        assert spec.legend.position == LegendPosition.NONE
        assert spec.legend.visible is False

    def test_value_axis_configuration(self) -> None:
        """Test value axis configuration."""
        spec = (
            ChartBuilder()
            .column_chart()
            .axis("value", title="Amount ($)", min=0, max=1000)
            .build()
        )
        assert spec.value_axis is not None
        assert spec.value_axis.title == "Amount ($)"
        assert spec.value_axis.min_value == 0
        assert spec.value_axis.max_value == 1000

    def test_category_axis_configuration(self) -> None:
        """Test category axis configuration."""
        spec = (
            ChartBuilder()
            .column_chart()
            .category_axis(title="Months")
            .build()
        )
        assert spec.category_axis is not None
        assert spec.category_axis.title == "Months"

    def test_data_labels(self) -> None:
        """Test data label configuration."""
        spec = (
            ChartBuilder()
            .pie_chart()
            .data_labels(show_value=True, show_percentage=True)
            .build()
        )
        assert spec.data_labels is not None
        assert spec.data_labels.show_value is True
        assert spec.data_labels.show_percentage is True


class TestDataSeries:
    """Test data series configuration (FR-CHART-005)."""

    def test_add_series(self) -> None:
        """Test adding a data series."""
        spec = (
            ChartBuilder()
            .column_chart()
            .series("Budget", "Sheet.B2:B13")
            .build()
        )
        assert len(spec.series) == 1
        assert spec.series[0].name == "Budget"
        assert spec.series[0].values == "Sheet.B2:B13"

    def test_multiple_series(self) -> None:
        """Test adding multiple data series."""
        spec = (
            ChartBuilder()
            .column_chart()
            .series("Budget", "Sheet.B2:B13")
            .series("Actual", "Sheet.C2:C13")
            .build()
        )
        assert len(spec.series) == 2
        assert spec.series[0].name == "Budget"
        assert spec.series[1].name == "Actual"

    def test_series_with_color(self) -> None:
        """Test series with custom color."""
        spec = (
            ChartBuilder()
            .column_chart()
            .series("Budget", "Sheet.B2:B13", color="#4472C4")
            .build()
        )
        assert spec.series[0].color == "#4472C4"

    def test_series_secondary_axis(self) -> None:
        """Test series on secondary axis."""
        spec = (
            ChartBuilder()
            .combo_chart()
            .series("Revenue", "Sheet.B2:B13")
            .series("Growth", "Sheet.C2:C13", secondary_axis=True)
            .build()
        )
        assert spec.series[0].secondary_axis is False
        assert spec.series[1].secondary_axis is True

    def test_categories(self) -> None:
        """Test setting category range."""
        spec = (
            ChartBuilder()
            .column_chart()
            .categories("Sheet.A2:A13")
            .series("Budget", "Sheet.B2:B13")
            .build()
        )
        assert spec.categories == "Sheet.A2:A13"


class TestChartPositioning:
    """Test chart positioning (FR-CHART-006)."""

    def test_chart_position(self) -> None:
        """Test setting chart position."""
        spec = (
            ChartBuilder()
            .column_chart()
            .position("F2", offset_x=10, offset_y=5)
            .build()
        )
        assert spec.position.cell == "F2"
        assert spec.position.offset_x == 10
        assert spec.position.offset_y == 5

    def test_chart_size(self) -> None:
        """Test setting chart size."""
        spec = (
            ChartBuilder()
            .column_chart()
            .size(500, 350)
            .build()
        )
        assert spec.size.width == 500
        assert spec.size.height == 350

    def test_position_with_cells(self) -> None:
        """Test move/size with cells options."""
        spec = (
            ChartBuilder()
            .column_chart()
            .position("F2", move_with_cells=True, size_with_cells=True)
            .build()
        )
        assert spec.position.move_with_cells is True
        assert spec.position.size_with_cells is True


class TestChartStyling:
    """Test chart styling options (FR-CHART-004)."""

    def test_style_preset(self) -> None:
        """Test applying style preset."""
        spec = (
            ChartBuilder()
            .column_chart()
            .style("theme")
            .build()
        )
        assert spec.style_preset == "theme"

    def test_custom_colors(self) -> None:
        """Test custom color palette."""
        spec = (
            ChartBuilder()
            .column_chart()
            .colors("#4472C4", "#ED7D31", "#A5A5A5")
            .build()
        )
        assert spec.color_palette == ["#4472C4", "#ED7D31", "#A5A5A5"]

    def test_plot_area_styling(self) -> None:
        """Test plot area styling."""
        spec = (
            ChartBuilder()
            .column_chart()
            .plot_area(background="#F5F5F5", border_color="#CCCCCC")
            .build()
        )
        assert spec.plot_area is not None
        assert spec.plot_area.background_color == "#F5F5F5"
        assert spec.plot_area.border_color == "#CCCCCC"

    def test_3d_effects(self) -> None:
        """Test 3D effects."""
        spec = (
            ChartBuilder()
            .column_chart()
            .threed(True)
            .build()
        )
        assert spec.threed is True


class TestTrendlines:
    """Test trendline configuration (FR-CHART-007)."""

    def test_series_trendline(self) -> None:
        """Test adding trendline to series."""
        spec = (
            ChartBuilder()
            .scatter_chart()
            .series("Data", "Sheet.B2:B100")
            .series_trendline("linear")
            .build()
        )
        assert spec.series[0].trendline is not None
        assert spec.series[0].trendline.type == TrendlineType.LINEAR

    def test_trendline_with_forecast(self) -> None:
        """Test trendline with forecast periods."""
        spec = (
            ChartBuilder()
            .scatter_chart()
            .series("Data", "Sheet.B2:B100")
            .series_trendline("linear", forward_periods=3)
            .build()
        )
        assert spec.series[0].trendline.forward_periods == 3

    def test_trendline_display_options(self) -> None:
        """Test trendline display options."""
        spec = (
            ChartBuilder()
            .scatter_chart()
            .series("Data", "Sheet.B2:B100")
            .series_trendline(
                "linear",
                display_equation=True,
                display_r_squared=True
            )
            .build()
        )
        assert spec.series[0].trendline.display_equation is True
        assert spec.series[0].trendline.display_r_squared is True


class TestSparklines:
    """Test sparkline configuration (FR-CHART-003)."""

    def test_line_sparkline(self) -> None:
        """Test line sparkline creation."""
        spark = SparklineBuilder().line().data("B1:M1").build()
        assert spark.type == SparklineType.LINE
        assert spark.data_range == "B1:M1"

    def test_column_sparkline(self) -> None:
        """Test column sparkline creation."""
        spark = SparklineBuilder().column().data("B1:M1").build()
        assert spark.type == SparklineType.COLUMN

    def test_win_loss_sparkline(self) -> None:
        """Test win/loss sparkline creation."""
        spark = SparklineBuilder().win_loss().data("B1:M1").build()
        assert spark.type == SparklineType.WIN_LOSS

    def test_sparkline_color(self) -> None:
        """Test sparkline color setting."""
        spark = (
            SparklineBuilder()
            .line()
            .data("B1:M1")
            .color("#4472C4")
            .build()
        )
        assert spark.color == "#4472C4"

    def test_sparkline_markers(self) -> None:
        """Test sparkline marker colors."""
        spark = (
            SparklineBuilder()
            .line()
            .data("B1:M1")
            .markers(high="#00B050", low="#FF0000")
            .build()
        )
        assert spark.markers is not None
        assert spark.markers.high == "#00B050"
        assert spark.markers.low == "#FF0000"

    def test_sparkline_axis_range(self) -> None:
        """Test sparkline axis range."""
        spark = (
            SparklineBuilder()
            .line()
            .data("B1:M1")
            .axis_range(min=0, max=100)
            .build()
        )
        assert spark.min_axis == 0
        assert spark.max_axis == 100


class TestConvenienceFunctions:
    """Test convenience functions for chart creation."""

    def test_chart_function(self) -> None:
        """Test chart() convenience function."""
        builder = chart()
        assert isinstance(builder, ChartBuilder)

    def test_sparkline_function(self) -> None:
        """Test sparkline() convenience function."""
        builder = sparkline()
        assert isinstance(builder, SparklineBuilder)

    def test_budget_comparison_chart(self) -> None:
        """Test pre-built budget comparison chart."""
        spec = budget_comparison_chart(
            categories="Sheet.A2:A13",
            budget_values="Sheet.B2:B13",
            actual_values="Sheet.C2:C13",
        )
        assert spec.chart_type == ChartType.COLUMN
        assert len(spec.series) == 2
        assert spec.series[0].name == "Budget"
        assert spec.series[1].name == "Actual"

    def test_spending_pie_chart(self) -> None:
        """Test pre-built spending pie chart."""
        spec = spending_pie_chart(
            categories="Data.A2:A10",
            values="Data.B2:B10",
        )
        assert spec.chart_type == ChartType.PIE
        assert spec.data_labels is not None
        assert spec.data_labels.show_percentage is True

    def test_trend_line_chart(self) -> None:
        """Test pre-built trend line chart."""
        spec = trend_line_chart(
            categories="Data.A2:A24",
            values="Data.B2:B24",
            trendline=True,
        )
        assert spec.chart_type == ChartType.LINE_MARKERS
        assert len(spec.series) == 1
        assert spec.series[0].trendline is not None


class TestChartDataClasses:
    """Test chart data class creation and defaults."""

    def test_chart_title_defaults(self) -> None:
        """Test ChartTitle default values."""
        title = ChartTitle(text="Test")
        assert title.font_size == "14pt"
        assert title.font_weight == "bold"
        assert title.position == "top"

    def test_axis_config_defaults(self) -> None:
        """Test AxisConfig default values."""
        axis = AxisConfig()
        assert axis.major_gridlines is True
        assert axis.minor_gridlines is False
        assert axis.logarithmic is False

    def test_legend_config_defaults(self) -> None:
        """Test LegendConfig default values."""
        legend = LegendConfig()
        assert legend.position == LegendPosition.BOTTOM
        assert legend.visible is True

    def test_data_series_defaults(self) -> None:
        """Test DataSeries default values."""
        series = DataSeries(name="Test", values="A1:A10")
        assert series.secondary_axis is False
        assert series.chart_type is None
        assert series.line_width == "2pt"

    def test_chart_position_defaults(self) -> None:
        """Test ChartPosition default values."""
        pos = ChartPosition()
        assert pos.cell == "A1"
        assert pos.offset_x == 0
        assert pos.move_with_cells is True

    def test_chart_size_defaults(self) -> None:
        """Test ChartSize default values."""
        size = ChartSize()
        assert size.width == 400
        assert size.height == 300

    def test_trendline_defaults(self) -> None:
        """Test Trendline default values."""
        trend = Trendline()
        assert trend.type == TrendlineType.LINEAR
        assert trend.forward_periods == 0
        assert trend.display_equation is False


class TestChartBuilderChaining:
    """Test ChartBuilder method chaining."""

    def test_full_chart_configuration(self) -> None:
        """Test complete chart configuration with all options."""
        spec = (
            ChartBuilder()
            .column_chart()
            .title("Monthly Budget vs Actual", font_size="16pt")
            .categories("Budget.A2:A13")
            .series("Budget", "Budget.B2:B13", color="#4472C4")
            .series("Actual", "Budget.C2:C13", color="#ED7D31")
            .legend(position="bottom")
            .axis("value", title="Amount ($)", min=0)
            .axis("category", title="Month")
            .position("F2")
            .size(500, 350)
            .colors("#4472C4", "#ED7D31", "#A5A5A5")
            .style("theme")
            .build()
        )

        # Verify all settings
        assert spec.chart_type == ChartType.COLUMN
        assert spec.title.text == "Monthly Budget vs Actual"
        assert spec.categories == "Budget.A2:A13"
        assert len(spec.series) == 2
        assert spec.legend.position == LegendPosition.BOTTOM
        assert spec.value_axis.title == "Amount ($)"
        assert spec.position.cell == "F2"
        assert spec.size.width == 500
        assert spec.style_preset == "theme"

    def test_builder_returns_self(self) -> None:
        """Test that all builder methods return self for chaining."""
        builder = ChartBuilder()

        # All methods should return the same builder instance
        assert builder.column_chart() is builder
        assert builder.title("Test") is builder
        assert builder.series("Test", "A1:A10") is builder
        assert builder.categories("B1:B10") is builder
        assert builder.legend() is builder
        assert builder.axis("value") is builder
        assert builder.position("A1") is builder
        assert builder.size(400, 300) is builder
        assert builder.style("theme") is builder
        assert builder.colors("#000") is builder
        assert builder.plot_area() is builder
        assert builder.threed() is builder
        assert builder.data_labels() is builder


class TestSparklineBuilderChaining:
    """Test SparklineBuilder method chaining."""

    def test_full_sparkline_configuration(self) -> None:
        """Test complete sparkline configuration."""
        spark = (
            SparklineBuilder()
            .line()
            .data("MonthlyData.B{row}:M{row}")
            .color("#4472C4")
            .negative_color("#FF0000")
            .markers(high="#00B050", low="#C00000", first="#FFC000", last="#FFC000")
            .axis_range(min=0, max=100)
            .same_scale(True)
            .show_axis(True)
            .build()
        )

        assert spark.type == SparklineType.LINE
        assert spark.color == "#4472C4"
        assert spark.negative_color == "#FF0000"
        assert spark.markers.high == "#00B050"
        assert spark.min_axis == 0
        assert spark.same_scale is True
        assert spark.show_axis is True

    def test_sparkline_builder_returns_self(self) -> None:
        """Test that all sparkline builder methods return self."""
        builder = SparklineBuilder()

        assert builder.line() is builder
        assert builder.column() is builder
        assert builder.data("A1:Z1") is builder
        assert builder.color("#000") is builder
        assert builder.negative_color("#F00") is builder
        assert builder.markers() is builder
        assert builder.axis_range() is builder
        assert builder.same_scale() is builder
        assert builder.show_axis() is builder
