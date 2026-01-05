"""Charts and visualization support for SpreadsheetDL.

Implements:
    - FR-CHART-001: Chart Type Support
    - FR-CHART-002: Chart Configuration
    - FR-CHART-003: Sparklines
    - FR-CHART-004: Chart Styling
    - FR-CHART-005: Chart Data Ranges
    - FR-CHART-006: Chart Positioning
    - FR-CHART-007: Trendlines
    - FR-BUILDER-004: ChartBuilder

Provides a fluent API for creating charts with data series,
axis configuration, legends, and styling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Self

# ============================================================================
# Enums (FR-CHART-001)
# ============================================================================


class ChartType(Enum):
    """Chart type enumeration (FR-CHART-001)."""

    # Column charts
    COLUMN = auto()
    COLUMN_STACKED = auto()
    COLUMN_100_STACKED = auto()

    # Bar charts
    BAR = auto()
    BAR_STACKED = auto()
    BAR_100_STACKED = auto()

    # Line charts
    LINE = auto()
    LINE_MARKERS = auto()
    LINE_SMOOTH = auto()

    # Area charts
    AREA = auto()
    AREA_STACKED = auto()
    AREA_100_STACKED = auto()

    # Pie charts
    PIE = auto()
    DOUGHNUT = auto()

    # Other
    SCATTER = auto()
    SCATTER_LINES = auto()
    BUBBLE = auto()
    COMBO = auto()  # Column + Line combination


class LegendPosition(Enum):
    """Legend position options (FR-CHART-002)."""

    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"
    NONE = "none"


class AxisType(Enum):
    """Axis type enumeration (FR-CHART-002)."""

    CATEGORY = "category"  # X-axis typically
    VALUE = "value"  # Y-axis typically
    SECONDARY_VALUE = "secondary_value"  # Secondary Y-axis


class DataLabelPosition(Enum):
    """Data label position options (FR-CHART-002)."""

    INSIDE = "inside"
    OUTSIDE = "outside"
    CENTER = "center"
    ABOVE = "above"
    BELOW = "below"
    LEFT = "left"
    RIGHT = "right"


class TrendlineType(Enum):
    """Trendline type enumeration (FR-CHART-007)."""

    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    POLYNOMIAL = "polynomial"
    POWER = "power"
    MOVING_AVERAGE = "moving_average"


class SparklineType(Enum):
    """Sparkline type enumeration (FR-CHART-003)."""

    LINE = "line"
    COLUMN = "column"
    WIN_LOSS = "win_loss"


# ============================================================================
# Data Classes (FR-CHART-002)
# ============================================================================


@dataclass
class ChartTitle:
    """Chart title configuration (FR-CHART-002).

    Attributes:
        text: Title text
        font_family: Font family name
        font_size: Font size (e.g., "14pt")
        font_weight: Font weight (normal, bold)
        color: Text color (hex)
        position: Position (top, bottom, none)
    """

    text: str
    font_family: str | None = None
    font_size: str = "14pt"
    font_weight: str = "bold"
    color: str | None = None
    position: str = "top"


@dataclass(slots=True)
class AxisConfig:
    """Axis configuration for chart axes.

    Uses __slots__ for memory efficiency.

    Attributes:
        axis_type: Type of axis (category, value, secondary_value)
        title: Axis title text
        title_font_size: Title font size
        min_value: Minimum axis value (None for auto)
        max_value: Maximum axis value (None for auto)
        major_interval: Major gridline interval
        minor_interval: Minor gridline interval
        major_gridlines: Show major gridlines
        minor_gridlines: Show minor gridlines
        format_code: Number format code
        reversed: Reverse axis direction
        logarithmic: Use logarithmic scale
    """

    axis_type: AxisType = AxisType.VALUE
    title: str | None = None
    title_font_size: str = "11pt"
    min_value: float | None = None
    max_value: float | None = None
    major_interval: float | None = None
    minor_interval: float | None = None
    major_gridlines: bool = True
    minor_gridlines: bool = False
    format_code: str | None = None
    reversed: bool = False
    logarithmic: bool = False


@dataclass
class LegendConfig:
    """Legend configuration (FR-CHART-002).

    Attributes:
        position: Legend position
        visible: Whether legend is visible
        font_family: Font family
        font_size: Font size
        overlay: Whether legend overlays chart
    """

    position: LegendPosition = LegendPosition.BOTTOM
    visible: bool = True
    font_family: str | None = None
    font_size: str = "10pt"
    overlay: bool = False


@dataclass
class DataLabelConfig:
    """Data label configuration (FR-CHART-002).

    Attributes:
        show_value: Show value on label
        show_percentage: Show percentage (pie charts)
        show_category: Show category name
        show_series: Show series name
        position: Label position
        font_size: Font size
        format_code: Number format code
        separator: Separator between label parts
    """

    show_value: bool = False
    show_percentage: bool = False
    show_category: bool = False
    show_series: bool = False
    position: DataLabelPosition = DataLabelPosition.OUTSIDE
    font_size: str = "9pt"
    format_code: str | None = None
    separator: str = ", "


@dataclass
class Trendline:
    """Trendline configuration (FR-CHART-007).

    Attributes:
        type: Trendline type
        order: Polynomial order (for polynomial type)
        period: Moving average period
        forward_periods: Number of periods to forecast forward
        backward_periods: Number of periods to forecast backward
        intercept: Force intercept value
        display_equation: Show equation on chart
        display_r_squared: Show R-squared value
        color: Trendline color (hex)
        width: Line width
        dash_style: Line dash style
    """

    type: TrendlineType = TrendlineType.LINEAR
    order: int = 2  # For polynomial
    period: int = 2  # For moving average
    forward_periods: int = 0
    backward_periods: int = 0
    intercept: float | None = None
    display_equation: bool = False
    display_r_squared: bool = False
    color: str | None = None
    width: str = "1pt"
    dash_style: str = "solid"


@dataclass(slots=True)
class DataSeries:
    """Chart data series configuration.

    Uses __slots__ for memory efficiency.

    Attributes:
        name: Series name (for legend)
        values: Range reference for values (e.g., "Sheet.B2:B20")
        categories: Range reference for categories (optional)
        color: Series color (hex, None for auto)
        secondary_axis: Use secondary Y-axis
        chart_type: Override chart type for combo charts
        data_labels: Data label configuration
        trendline: Trendline configuration
        marker_style: Marker style for line/scatter
        line_width: Line width for line charts
        fill_opacity: Fill opacity for area charts
    """

    name: str
    values: str
    categories: str | None = None
    color: str | None = None
    secondary_axis: bool = False
    chart_type: ChartType | None = None  # For combo charts
    data_labels: DataLabelConfig | None = None
    trendline: Trendline | None = None
    marker_style: str | None = None
    line_width: str = "2pt"
    fill_opacity: float = 0.8


@dataclass
class ChartPosition:
    """Chart position configuration (FR-CHART-006).

    Attributes:
        cell: Anchor cell reference (e.g., "F2")
        offset_x: Horizontal offset in pixels
        offset_y: Vertical offset in pixels
        move_with_cells: Move chart when cells are resized
        size_with_cells: Size chart when cells are resized
        z_order: Z-order for overlapping charts
    """

    cell: str = "A1"
    offset_x: int = 0
    offset_y: int = 0
    move_with_cells: bool = True
    size_with_cells: bool = False
    z_order: int = 0


@dataclass
class ChartSize:
    """Chart size configuration (FR-CHART-006).

    Attributes:
        width: Width in pixels
        height: Height in pixels
    """

    width: int = 400
    height: int = 300


@dataclass
class PlotAreaStyle:
    """Plot area styling (FR-CHART-002).

    Attributes:
        background_color: Background color (hex)
        border_color: Border color (hex)
        border_width: Border width
    """

    background_color: str | None = None
    border_color: str | None = None
    border_width: str = "1pt"


# ============================================================================
# Sparklines (FR-CHART-003)
# ============================================================================


@dataclass
class SparklineMarkers:
    """Sparkline marker configuration (FR-CHART-003).

    Attributes:
        high: Color for highest point
        low: Color for lowest point
        first: Color for first point
        last: Color for last point
        negative: Color for negative values
    """

    high: str | None = None
    low: str | None = None
    first: str | None = None
    last: str | None = None
    negative: str | None = None


@dataclass
class Sparkline:
    """Sparkline configuration (FR-CHART-003).

    Attributes:
        type: Sparkline type (line, column, win_loss)
        data_range: Data range (can include {row} placeholder)
        color: Main sparkline color
        negative_color: Color for negative values
        markers: Marker configuration
        min_axis: Minimum axis value (None for auto)
        max_axis: Maximum axis value (None for auto)
        same_scale: Use same scale for group
        show_axis: Show horizontal axis
        right_to_left: Display right to left
    """

    type: SparklineType = SparklineType.LINE
    data_range: str = ""
    color: str = "#4472C4"
    negative_color: str = "#FF0000"
    markers: SparklineMarkers | None = None
    min_axis: float | None = None
    max_axis: float | None = None
    same_scale: bool = False
    show_axis: bool = False
    right_to_left: bool = False


# ============================================================================
# Chart Specification (FR-CHART-001)
# ============================================================================


@dataclass(slots=True)
class ChartSpec:
    """Complete chart specification.

    Uses __slots__ for memory efficiency. This is the output of ChartBuilder
    and contains all configuration needed to render a chart.

    Attributes:
        chart_type: Type of chart
        title: Chart title configuration
        series: List of data series
        categories: Default category range for all series
        legend: Legend configuration
        category_axis: Category (X) axis configuration
        value_axis: Value (Y) axis configuration
        secondary_axis: Secondary Y axis configuration
        position: Chart position
        size: Chart size
        plot_area: Plot area styling
        data_labels: Default data label configuration
        style_preset: Theme style preset name
        color_palette: Custom color palette
        threed: Enable 3D effects
    """

    chart_type: ChartType = ChartType.COLUMN
    title: ChartTitle | None = None
    series: list[DataSeries] = field(default_factory=list)
    categories: str | None = None
    legend: LegendConfig = field(default_factory=LegendConfig)
    category_axis: AxisConfig | None = None
    value_axis: AxisConfig | None = None
    secondary_axis: AxisConfig | None = None
    position: ChartPosition = field(default_factory=ChartPosition)
    size: ChartSize = field(default_factory=ChartSize)
    plot_area: PlotAreaStyle | None = None
    data_labels: DataLabelConfig | None = None
    style_preset: str | None = None
    color_palette: list[str] | None = None
    threed: bool = False


# ============================================================================
# ChartBuilder (FR-BUILDER-004)
# ============================================================================


class ChartBuilder:
    r"""Fluent builder for creating charts.

    Implements FR-BUILDER-004: ChartBuilder

    Provides a chainable API for building chart specifications
    with support for:
    - Multiple chart types
    - Data series configuration
    - Axis configuration
    - Legend and title
    - Positioning and sizing

    Examples:
        # Simple column chart
        chart = ChartBuilder() \\
            .column_chart() \\
            .title("Monthly Budget") \\
            .series("Budget", "Sheet.B2:B13") \\
            .series("Actual", "Sheet.C2:C13") \\
            .categories("Sheet.A2:A13") \\
            .legend(position="bottom") \\
            .position("F2") \\
            .size(400, 300) \\
            .build()

        # Pie chart with data labels
        pie = ChartBuilder() \\
            .pie_chart() \\
            .title("Spending by Category") \\
            .series("Amount", "Data.B2:B10") \\
            .categories("Data.A2:A10") \\
            .data_labels(show_percentage=True) \\
            .build()

        # Combo chart with secondary axis
        combo = ChartBuilder() \\
            .combo_chart() \\
            .series("Revenue", "Data.B:B", chart_type="column") \\
            .series("Growth Rate", "Data.C:C", chart_type="line", secondary_axis=True) \\
            .build()
    """

    def __init__(self) -> None:
        """Initialize chart builder."""
        self._spec = ChartSpec()
        self._current_series: DataSeries | None = None

    # =========================================================================
    # Chart Type Selection (FR-CHART-001 AC1-AC7)
    # =========================================================================

    def column_chart(self, stacked: bool = False, percent: bool = False) -> Self:
        """Set chart type to column.

        Args:
            stacked: Use stacked columns
            percent: Use 100% stacked (requires stacked=True)

        Returns:
            Self for chaining
        """
        if percent:
            self._spec.chart_type = ChartType.COLUMN_100_STACKED
        elif stacked:
            self._spec.chart_type = ChartType.COLUMN_STACKED
        else:
            self._spec.chart_type = ChartType.COLUMN
        return self

    def bar_chart(self, stacked: bool = False, percent: bool = False) -> Self:
        """Set chart type to bar (horizontal columns).

        Args:
            stacked: Use stacked bars
            percent: Use 100% stacked

        Returns:
            Self for chaining
        """
        if percent:
            self._spec.chart_type = ChartType.BAR_100_STACKED
        elif stacked:
            self._spec.chart_type = ChartType.BAR_STACKED
        else:
            self._spec.chart_type = ChartType.BAR
        return self

    def line_chart(self, markers: bool = False, smooth: bool = False) -> Self:
        """Set chart type to line.

        Args:
            markers: Show data point markers
            smooth: Use smooth/curved lines

        Returns:
            Self for chaining
        """
        if smooth:
            self._spec.chart_type = ChartType.LINE_SMOOTH
        elif markers:
            self._spec.chart_type = ChartType.LINE_MARKERS
        else:
            self._spec.chart_type = ChartType.LINE
        return self

    def area_chart(self, stacked: bool = False, percent: bool = False) -> Self:
        """Set chart type to area.

        Args:
            stacked: Use stacked areas
            percent: Use 100% stacked

        Returns:
            Self for chaining
        """
        if percent:
            self._spec.chart_type = ChartType.AREA_100_STACKED
        elif stacked:
            self._spec.chart_type = ChartType.AREA_STACKED
        else:
            self._spec.chart_type = ChartType.AREA
        return self

    def pie_chart(self, doughnut: bool = False) -> Self:
        """Set chart type to pie.

        Args:
            doughnut: Use doughnut style

        Returns:
            Self for chaining
        """
        if doughnut:
            self._spec.chart_type = ChartType.DOUGHNUT
        else:
            self._spec.chart_type = ChartType.PIE
        return self

    def scatter_chart(self, lines: bool = False) -> Self:
        """Set chart type to scatter.

        Args:
            lines: Connect points with lines

        Returns:
            Self for chaining
        """
        if lines:
            self._spec.chart_type = ChartType.SCATTER_LINES
        else:
            self._spec.chart_type = ChartType.SCATTER
        return self

    def bubble_chart(self) -> Self:
        """Set chart type to bubble."""
        self._spec.chart_type = ChartType.BUBBLE
        return self

    def combo_chart(self) -> Self:
        """Set chart type to combo (column + line)."""
        self._spec.chart_type = ChartType.COMBO
        return self

    # =========================================================================
    # Title and Labels (FR-CHART-002 AC1, AC4)
    # =========================================================================

    def title(
        self,
        text: str,
        *,
        font_size: str = "14pt",
        font_weight: str = "bold",
        color: str | None = None,
        position: str = "top",
    ) -> Self:
        """Set chart title.

        Args:
            text: Title text
            font_size: Font size
            font_weight: Font weight (normal, bold)
            color: Text color (hex)
            position: Position (top, bottom)

        Returns:
            Self for chaining
        """
        self._spec.title = ChartTitle(
            text=text,
            font_size=font_size,
            font_weight=font_weight,
            color=color,
            position=position,
        )
        return self

    def data_labels(
        self,
        *,
        show_value: bool = False,
        show_percentage: bool = False,
        show_category: bool = False,
        show_series: bool = False,
        position: str = "outside",
        font_size: str = "9pt",
        format_code: str | None = None,
    ) -> Self:
        """Configure data labels for all series.

        Args:
            show_value: Show value on label
            show_percentage: Show percentage
            show_category: Show category name
            show_series: Show series name
            position: Label position
            font_size: Font size
            format_code: Number format

        Returns:
            Self for chaining
        """
        pos_enum = (
            DataLabelPosition(position) if isinstance(position, str) else position
        )
        self._spec.data_labels = DataLabelConfig(
            show_value=show_value,
            show_percentage=show_percentage,
            show_category=show_category,
            show_series=show_series,
            position=pos_enum,
            font_size=font_size,
            format_code=format_code,
        )
        return self

    # =========================================================================
    # Data Series (FR-CHART-005 AC1-AC5)
    # =========================================================================

    def series(
        self,
        name: str,
        values: str,
        *,
        color: str | None = None,
        secondary_axis: bool = False,
        chart_type: str | ChartType | None = None,
        trendline: str | None = None,
    ) -> Self:
        """Add a data series.

        Args:
            name: Series name (for legend)
            values: Range reference for values (e.g., "Sheet.B2:B20")
            color: Series color (hex)
            secondary_axis: Use secondary Y-axis
            chart_type: Override chart type for combo charts
            trendline: Trendline type (linear, exponential, etc.)

        Returns:
            Self for chaining
        """
        # Parse chart_type if string
        ct = None
        if chart_type is not None:
            if isinstance(chart_type, str):
                chart_type_map = {
                    "column": ChartType.COLUMN,
                    "bar": ChartType.BAR,
                    "line": ChartType.LINE,
                    "area": ChartType.AREA,
                }
                ct = chart_type_map.get(chart_type.lower())
            else:
                ct = chart_type

        # Parse trendline if string
        trend = None
        if trendline:
            trend = Trendline(type=TrendlineType(trendline.lower()))

        series = DataSeries(
            name=name,
            values=values,
            color=color,
            secondary_axis=secondary_axis,
            chart_type=ct,
            trendline=trend,
        )
        self._spec.series.append(series)
        self._current_series = series
        return self

    def series_color(self, color: str) -> Self:
        """Set color for the last added series.

        Args:
            color: Hex color

        Returns:
            Self for chaining
        """
        if self._current_series:
            self._current_series.color = color
        return self

    def series_trendline(
        self,
        type: str = "linear",
        *,
        forward_periods: int = 0,
        backward_periods: int = 0,
        display_equation: bool = False,
        display_r_squared: bool = False,
    ) -> Self:
        """Add trendline to the last added series.

        Args:
            type: Trendline type
            forward_periods: Forecast forward
            backward_periods: Forecast backward
            display_equation: Show equation
            display_r_squared: Show R-squared

        Returns:
            Self for chaining
        """
        if self._current_series:
            self._current_series.trendline = Trendline(
                type=TrendlineType(type.lower()),
                forward_periods=forward_periods,
                backward_periods=backward_periods,
                display_equation=display_equation,
                display_r_squared=display_r_squared,
            )
        return self

    def categories(self, range_ref: str) -> Self:
        """Set category range for all series.

        Args:
            range_ref: Range reference (e.g., "Sheet.A2:A20")

        Returns:
            Self for chaining
        """
        self._spec.categories = range_ref
        return self

    # =========================================================================
    # Legend Configuration (FR-CHART-002 AC2)
    # =========================================================================

    def legend(
        self,
        *,
        position: str = "bottom",
        visible: bool = True,
        font_size: str = "10pt",
        overlay: bool = False,
    ) -> Self:
        """Configure chart legend.

        Args:
            position: Legend position (top, bottom, left, right, none)
            visible: Whether legend is visible
            font_size: Font size
            overlay: Whether legend overlays chart

        Returns:
            Self for chaining
        """
        pos_enum = (
            LegendPosition(position) if position != "none" else LegendPosition.NONE
        )
        self._spec.legend = LegendConfig(
            position=pos_enum,
            visible=visible and position != "none",
            font_size=font_size,
            overlay=overlay,
        )
        return self

    # =========================================================================
    # Axis Configuration (FR-CHART-002 AC3)
    # =========================================================================

    def axis(
        self,
        axis_type: str,
        *,
        title: str | None = None,
        min: float | None = None,
        max: float | None = None,
        interval: float | None = None,
        format_code: str | None = None,
        gridlines: bool = True,
        logarithmic: bool = False,
    ) -> Self:
        """Configure an axis.

        Args:
            axis_type: Axis type ("category", "value", "secondary")
            title: Axis title
            min: Minimum value
            max: Maximum value
            interval: Major gridline interval
            format_code: Number format
            gridlines: Show gridlines
            logarithmic: Use logarithmic scale

        Returns:
            Self for chaining
        """
        axis_config = AxisConfig(
            title=title,
            min_value=min,
            max_value=max,
            major_interval=interval,
            major_gridlines=gridlines,
            format_code=format_code,
            logarithmic=logarithmic,
        )

        if axis_type == "category":
            axis_config.axis_type = AxisType.CATEGORY
            self._spec.category_axis = axis_config
        elif axis_type == "value":
            axis_config.axis_type = AxisType.VALUE
            self._spec.value_axis = axis_config
        elif axis_type in ("secondary", "secondary_value"):
            axis_config.axis_type = AxisType.SECONDARY_VALUE
            self._spec.secondary_axis = axis_config

        return self

    def category_axis(
        self,
        *,
        title: str | None = None,
        format_code: str | None = None,
        reversed: bool = False,
    ) -> Self:
        """Configure category (X) axis.

        Args:
            title: Axis title
            format_code: Number/date format
            reversed: Reverse axis

        Returns:
            Self for chaining
        """
        self._spec.category_axis = AxisConfig(
            axis_type=AxisType.CATEGORY,
            title=title,
            format_code=format_code,
            reversed=reversed,
        )
        return self

    def value_axis(
        self,
        *,
        title: str | None = None,
        min: float | None = None,
        max: float | None = None,
        format_code: str | None = None,
        logarithmic: bool = False,
    ) -> Self:
        """Configure value (Y) axis.

        Args:
            title: Axis title
            min: Minimum value
            max: Maximum value
            format_code: Number format
            logarithmic: Use logarithmic scale

        Returns:
            Self for chaining
        """
        self._spec.value_axis = AxisConfig(
            axis_type=AxisType.VALUE,
            title=title,
            min_value=min,
            max_value=max,
            format_code=format_code,
            logarithmic=logarithmic,
        )
        return self

    # =========================================================================
    # Position and Size (FR-CHART-006 AC1-AC5)
    # =========================================================================

    def position(
        self,
        cell: str,
        *,
        offset_x: int = 0,
        offset_y: int = 0,
        move_with_cells: bool = True,
        size_with_cells: bool = False,
    ) -> Self:
        """Set chart position.

        Args:
            cell: Anchor cell (e.g., "F2")
            offset_x: Horizontal offset in pixels
            offset_y: Vertical offset in pixels
            move_with_cells: Move when cells resize
            size_with_cells: Size when cells resize

        Returns:
            Self for chaining
        """
        self._spec.position = ChartPosition(
            cell=cell,
            offset_x=offset_x,
            offset_y=offset_y,
            move_with_cells=move_with_cells,
            size_with_cells=size_with_cells,
        )
        return self

    def size(self, width: int, height: int) -> Self:
        """Set chart size.

        Args:
            width: Width in pixels
            height: Height in pixels

        Returns:
            Self for chaining
        """
        self._spec.size = ChartSize(width=width, height=height)
        return self

    # =========================================================================
    # Styling (FR-CHART-004 AC1-AC5)
    # =========================================================================

    def style(self, preset: str) -> Self:
        """Apply a style preset.

        Args:
            preset: Style preset name (e.g., "theme", "minimal", "colorful")

        Returns:
            Self for chaining
        """
        self._spec.style_preset = preset
        return self

    def colors(self, *colors: str) -> Self:
        """Set custom color palette.

        Args:
            *colors: Hex color values

        Returns:
            Self for chaining
        """
        self._spec.color_palette = list(colors)
        return self

    def plot_area(
        self,
        *,
        background: str | None = None,
        border_color: str | None = None,
        border_width: str = "1pt",
    ) -> Self:
        """Configure plot area styling.

        Args:
            background: Background color
            border_color: Border color
            border_width: Border width

        Returns:
            Self for chaining
        """
        self._spec.plot_area = PlotAreaStyle(
            background_color=background,
            border_color=border_color,
            border_width=border_width,
        )
        return self

    def threed(self, enabled: bool = True) -> Self:
        """Enable 3D effects.

        Args:
            enabled: Whether to enable 3D

        Returns:
            Self for chaining
        """
        self._spec.threed = enabled
        return self

    # =========================================================================
    # Build
    # =========================================================================

    def build(self) -> ChartSpec:
        """Build the chart specification.

        Returns:
            ChartSpec object
        """
        return self._spec


# ============================================================================
# Sparkline Builder (FR-CHART-003)
# ============================================================================


class SparklineBuilder:
    r"""Fluent builder for creating sparklines.

    Implements FR-CHART-003: Sparklines

    Examples:
        sparkline = SparklineBuilder() \\
            .line() \\
            .data("MonthlyData.B{row}:M{row}") \\
            .color("#4472C4") \\
            .markers(high="#00B050", low="#FF0000") \\
            .build()
    """

    def __init__(self) -> None:
        """Initialize sparkline builder."""
        self._sparkline = Sparkline()

    def line(self) -> Self:
        """Set sparkline type to line."""
        self._sparkline.type = SparklineType.LINE
        return self

    def column(self) -> Self:
        """Set sparkline type to column."""
        self._sparkline.type = SparklineType.COLUMN
        return self

    def win_loss(self) -> Self:
        """Set sparkline type to win/loss."""
        self._sparkline.type = SparklineType.WIN_LOSS
        return self

    def data(self, range_ref: str) -> Self:
        """Set data range.

        Args:
            range_ref: Range reference (can include {row} placeholder)

        Returns:
            Self for chaining
        """
        self._sparkline.data_range = range_ref
        return self

    def color(self, color: str) -> Self:
        """Set sparkline color.

        Args:
            color: Hex color

        Returns:
            Self for chaining
        """
        self._sparkline.color = color
        return self

    def negative_color(self, color: str) -> Self:
        """Set color for negative values.

        Args:
            color: Hex color

        Returns:
            Self for chaining
        """
        self._sparkline.negative_color = color
        return self

    def markers(
        self,
        *,
        high: str | None = None,
        low: str | None = None,
        first: str | None = None,
        last: str | None = None,
        negative: str | None = None,
    ) -> Self:
        """Configure marker colors.

        Args:
            high: Color for highest point
            low: Color for lowest point
            first: Color for first point
            last: Color for last point
            negative: Color for negative values

        Returns:
            Self for chaining
        """
        self._sparkline.markers = SparklineMarkers(
            high=high,
            low=low,
            first=first,
            last=last,
            negative=negative,
        )
        return self

    def axis_range(self, min: float | None = None, max: float | None = None) -> Self:
        """Set axis range.

        Args:
            min: Minimum value
            max: Maximum value

        Returns:
            Self for chaining
        """
        self._sparkline.min_axis = min
        self._sparkline.max_axis = max
        return self

    def same_scale(self, enabled: bool = True) -> Self:
        """Use same scale for group.

        Args:
            enabled: Whether to use same scale

        Returns:
            Self for chaining
        """
        self._sparkline.same_scale = enabled
        return self

    def show_axis(self, enabled: bool = True) -> Self:
        """Show horizontal axis.

        Args:
            enabled: Whether to show axis

        Returns:
            Self for chaining
        """
        self._sparkline.show_axis = enabled
        return self

    def build(self) -> Sparkline:
        """Build the sparkline specification.

        Returns:
            Sparkline object
        """
        return self._sparkline


# ============================================================================
# Convenience Functions
# ============================================================================


def chart() -> ChartBuilder:
    """Create a new chart builder.

    Returns:
        ChartBuilder instance
    """
    return ChartBuilder()


def sparkline() -> SparklineBuilder:
    """Create a new sparkline builder.

    Returns:
        SparklineBuilder instance
    """
    return SparklineBuilder()


# Pre-built chart configurations for common use cases


def budget_comparison_chart(
    categories: str,
    budget_values: str,
    actual_values: str,
    *,
    title: str = "Budget vs Actual",
    position: str = "F2",
) -> ChartSpec:
    """Create a budget comparison column chart.

    Args:
        categories: Category labels range
        budget_values: Budget values range
        actual_values: Actual values range
        title: Chart title
        position: Anchor cell

    Returns:
        ChartSpec for budget comparison
    """
    return (
        ChartBuilder()
        .column_chart()
        .title(title)
        .categories(categories)
        .series("Budget", budget_values, color="#4472C4")
        .series("Actual", actual_values, color="#ED7D31")
        .legend(position="bottom")
        .axis("value", title="Amount ($)", min=0)
        .position(position)
        .size(450, 300)
        .build()
    )


def spending_pie_chart(
    categories: str,
    values: str,
    *,
    title: str = "Spending by Category",
    position: str = "F2",
) -> ChartSpec:
    """Create a spending breakdown pie chart.

    Args:
        categories: Category labels range
        values: Values range
        title: Chart title
        position: Anchor cell

    Returns:
        ChartSpec for spending pie chart
    """
    return (
        ChartBuilder()
        .pie_chart()
        .title(title)
        .categories(categories)
        .series("Spending", values)
        .data_labels(show_percentage=True, show_category=True)
        .legend(position="right")
        .position(position)
        .size(400, 350)
        .build()
    )


def trend_line_chart(
    categories: str,
    values: str,
    *,
    title: str = "Trend Analysis",
    position: str = "F2",
    trendline: bool = True,
) -> ChartSpec:
    """Create a trend line chart.

    Args:
        categories: Category labels range (e.g., months)
        values: Values range
        title: Chart title
        position: Anchor cell
        trendline: Add linear trendline

    Returns:
        ChartSpec for trend chart
    """
    builder = (
        ChartBuilder()
        .line_chart(markers=True)
        .title(title)
        .categories(categories)
        .series("Values", values)
    )

    if trendline:
        builder.series_trendline("linear", display_equation=True)

    return (
        builder.legend(visible=False)
        .axis("value", gridlines=True)
        .position(position)
        .size(500, 300)
        .build()
    )
