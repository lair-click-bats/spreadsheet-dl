# Charts API Reference

Complete API reference for the chart and visualization system.

**Implements:** FR-CHART-001 through FR-CHART-007, FR-BUILDER-004

## Overview

The Charts API provides fluent, chainable interfaces for creating professional charts and sparklines in spreadsheets. It consists of:

- **ChartBuilder**: Main builder for creating charts with complete configuration
- **SparklineBuilder**: Builder for creating inline sparklines
- **ChartSpec and related dataclasses**: Complete chart specifications
- **Pre-built chart templates**: Common chart configurations

---

## ChartBuilder

### Class: `ChartBuilder`

Fluent builder for creating charts with comprehensive configuration options.

```python
from spreadsheet_dl.charts import ChartBuilder, chart

# Using class directly
builder = ChartBuilder()

# Using convenience function
builder = chart()
```

### Chart Type Selection

#### `column_chart()`

Create a column (vertical bar) chart.

```python
column_chart(stacked: bool = False, percent: bool = False) -> Self
```

**Parameters:**

- `stacked`: Use stacked columns (bars stack vertically)
- `percent`: Use 100% stacked (each bar shows percentage distribution)

**Examples:**

```python
# Simple column chart
chart = ChartBuilder().column_chart()

# Stacked column chart
chart = ChartBuilder().column_chart(stacked=True)

# 100% stacked
chart = ChartBuilder().column_chart(stacked=True, percent=True)
```

#### `bar_chart()`

Create a bar (horizontal bar) chart.

```python
bar_chart(stacked: bool = False, percent: bool = False) -> Self
```

**Parameters:**

- `stacked`: Use stacked bars (bars stack horizontally)
- `percent`: Use 100% stacked

**Example:**

```python
chart = ChartBuilder() \
    .bar_chart() \
    .title("Category Comparison") \
    .series("Q1", "Sheet.B2:B10")
```

#### `line_chart()`

Create a line chart.

```python
line_chart(markers: bool = False, smooth: bool = False) -> Self
```

**Parameters:**

- `markers`: Show data point markers on the line
- `smooth`: Use smooth/curved lines instead of straight segments

**Example:**

```python
# Line chart with markers
chart = ChartBuilder() \
    .line_chart(markers=True) \
    .title("Trend Over Time") \
    .series("Revenue", "Data.B2:B13")
```

#### `area_chart()`

Create an area chart.

```python
area_chart(stacked: bool = False, percent: bool = False) -> Self
```

**Parameters:**

- `stacked`: Stack multiple series
- `percent`: Use 100% stacked

**Example:**

```python
chart = ChartBuilder() \
    .area_chart(stacked=True) \
    .series("Product A", "Sheet.B:B") \
    .series("Product B", "Sheet.C:C")
```

#### `pie_chart()`

Create a pie or doughnut chart.

```python
pie_chart(doughnut: bool = False) -> Self
```

**Parameters:**

- `doughnut`: Use doughnut style (pie with center hole)

**Example:**

```python
chart = ChartBuilder() \
    .pie_chart() \
    .title("Market Share") \
    .series("Share", "Data.B2:B6") \
    .categories("Data.A2:A6") \
    .data_labels(show_percentage=True)
```

#### `scatter_chart()`

Create a scatter (XY) chart.

```python
scatter_chart(lines: bool = False) -> Self
```

**Parameters:**

- `lines`: Connect points with lines

**Example:**

```python
chart = ChartBuilder() \
    .scatter_chart() \
    .series("Correlation", "Data.B:C")
```

#### `bubble_chart()`

Create a bubble chart (3-dimensional scatter).

```python
bubble_chart() -> Self
```

**Example:**

```python
chart = ChartBuilder() \
    .bubble_chart() \
    .series("Sales Analysis", "Data.B:D")
```

#### `combo_chart()`

Create a combo chart (mix of column and line).

```python
combo_chart() -> Self
```

**Example:**

```python
chart = ChartBuilder() \
    .combo_chart() \
    .series("Revenue", "Data.B:B", chart_type="column") \
    .series("Growth", "Data.C:C", chart_type="line", secondary_axis=True)
```

### Title and Labels

#### `title()`

Set chart title with formatting.

```python
title(
    text: str,
    *,
    font_size: str = "14pt",
    font_weight: str = "bold",
    color: str | None = None,
    position: str = "top"
) -> Self
```

**Parameters:**

- `text`: Title text
- `font_size`: Font size (e.g., "14pt", "18pt")
- `font_weight`: Font weight ("normal" or "bold")
- `color`: Text color (hex format, e.g., "#FF0000")
- `position`: Title position ("top" or "bottom")

**Example:**

```python
builder.title(
    "Monthly Revenue Analysis",
    font_size="16pt",
    font_weight="bold",
    color="#2C3E50"
)
```

#### `data_labels()`

Configure data labels on chart elements.

```python
data_labels(
    *,
    show_value: bool = False,
    show_percentage: bool = False,
    show_category: bool = False,
    show_series: bool = False,
    position: str = "outside",
    font_size: str = "9pt",
    format_code: str | None = None
) -> Self
```

**Parameters:**

- `show_value`: Display actual values
- `show_percentage`: Display percentages (useful for pie charts)
- `show_category`: Display category names
- `show_series`: Display series names
- `position`: Label position ("inside", "outside", "center", "above", "below", "left", "right")
- `font_size`: Label font size
- `format_code`: Number format code (e.g., "#,##0.00")

**Examples:**

```python
# Pie chart with percentages
chart.data_labels(show_percentage=True, show_category=True, position="outside")

# Column chart with values
chart.data_labels(show_value=True, format_code="#,##0", position="above")
```

### Data Series

#### `series()`

Add a data series to the chart.

```python
series(
    name: str,
    values: str,
    *,
    color: str | None = None,
    secondary_axis: bool = False,
    chart_type: str | ChartType | None = None,
    trendline: str | None = None
) -> Self
```

**Parameters:**

- `name`: Series name (appears in legend)
- `values`: Range reference for data (e.g., "Sheet.B2:B20")
- `color`: Series color (hex format)
- `secondary_axis`: Plot on secondary Y-axis (for combo charts)
- `chart_type`: Override chart type for this series ("column", "bar", "line", "area")
- `trendline`: Add trendline ("linear", "exponential", "logarithmic", "polynomial", "power", "moving_average")

**Examples:**

```python
# Simple series
chart.series("Budget", "Budget.B2:B13")

# Series with custom color
chart.series("Actual", "Budget.C2:C13", color="#ED7D31")

# Series with trendline
chart.series("Sales", "Data.B:B", trendline="linear")

# Combo chart with mixed types
chart.series("Revenue", "Data.B:B", chart_type="column") \
     .series("Growth Rate", "Data.C:C", chart_type="line", secondary_axis=True)
```

#### `series_color()`

Set color for the last added series.

```python
series_color(color: str) -> Self
```

**Parameters:**

- `color`: Hex color code

**Example:**

```python
chart.series("Q1", "Data.B:B").series_color("#4472C4")
```

#### `series_trendline()`

Add trendline to the last added series.

```python
series_trendline(
    type: str = "linear",
    *,
    forward_periods: int = 0,
    backward_periods: int = 0,
    display_equation: bool = False,
    display_r_squared: bool = False
) -> Self
```

**Parameters:**

- `type`: Trendline type ("linear", "exponential", "logarithmic", "polynomial", "power", "moving_average")
- `forward_periods`: Number of periods to forecast forward
- `backward_periods`: Number of periods to forecast backward
- `display_equation`: Show trend equation on chart
- `display_r_squared`: Show R-squared value

**Example:**

```python
chart.series("Sales", "Data.B2:B13") \
     .series_trendline("linear", forward_periods=3, display_equation=True, display_r_squared=True)
```

#### `categories()`

Set category labels for all series.

```python
categories(range_ref: str) -> Self
```

**Parameters:**

- `range_ref`: Range reference for category labels (e.g., "Sheet.A2:A13")

**Example:**

```python
chart.categories("Budget.A2:A13")  # Month names or dates
```

### Legend Configuration

#### `legend()`

Configure chart legend.

```python
legend(
    *,
    position: str = "bottom",
    visible: bool = True,
    font_size: str = "10pt",
    overlay: bool = False
) -> Self
```

**Parameters:**

- `position`: Legend position ("top", "bottom", "left", "right", "top-left", "top-right", "bottom-left", "bottom-right", "none")
- `visible`: Whether legend is visible
- `font_size`: Legend font size
- `overlay`: Whether legend overlays the chart area

**Examples:**

```python
# Bottom legend (default)
chart.legend(position="bottom")

# Right-side legend
chart.legend(position="right", font_size="9pt")

# Hide legend
chart.legend(visible=False)
```

### Axis Configuration

#### `axis()`

Configure a chart axis.

```python
axis(
    axis_type: str,
    *,
    title: str | None = None,
    min: float | None = None,
    max: float | None = None,
    interval: float | None = None,
    format_code: str | None = None,
    gridlines: bool = True,
    logarithmic: bool = False
) -> Self
```

**Parameters:**

- `axis_type`: Axis type ("category", "value", "secondary")
- `title`: Axis title text
- `min`: Minimum axis value (None for auto)
- `max`: Maximum axis value (None for auto)
- `interval`: Major gridline interval
- `format_code`: Number format code
- `gridlines`: Show major gridlines
- `logarithmic`: Use logarithmic scale

**Example:**

```python
chart.axis("value", title="Revenue ($)", min=0, max=100000, format_code="#,##0")
```

#### `category_axis()`

Configure the category (X) axis.

```python
category_axis(
    *,
    title: str | None = None,
    format_code: str | None = None,
    reversed: bool = False
) -> Self
```

**Parameters:**

- `title`: Axis title
- `format_code`: Format for axis labels
- `reversed`: Reverse axis direction

**Example:**

```python
chart.category_axis(title="Month", format_code="MMM YYYY")
```

#### `value_axis()`

Configure the value (Y) axis.

```python
value_axis(
    *,
    title: str | None = None,
    min: float | None = None,
    max: float | None = None,
    format_code: str | None = None,
    logarithmic: bool = False
) -> Self
```

**Parameters:**

- `title`: Axis title
- `min`: Minimum value
- `max`: Maximum value
- `format_code`: Number format
- `logarithmic`: Use logarithmic scale

**Example:**

```python
chart.value_axis(title="Amount ($)", min=0, format_code="$#,##0")
```

### Position and Size

#### `position()`

Set chart position on the sheet.

```python
position(
    cell: str,
    *,
    offset_x: int = 0,
    offset_y: int = 0,
    move_with_cells: bool = True,
    size_with_cells: bool = False
) -> Self
```

**Parameters:**

- `cell`: Anchor cell reference (e.g., "F2")
- `offset_x`: Horizontal offset in pixels from anchor
- `offset_y`: Vertical offset in pixels from anchor
- `move_with_cells`: Move chart when cells are inserted/deleted
- `size_with_cells`: Resize chart when cells are resized

**Example:**

```python
chart.position("F2", offset_x=10, offset_y=5)
```

#### `size()`

Set chart dimensions.

```python
size(width: int, height: int) -> Self
```

**Parameters:**

- `width`: Width in pixels
- `height`: Height in pixels

**Example:**

```python
chart.size(500, 350)
```

### Styling

#### `style()`

Apply a style preset.

```python
style(preset: str) -> Self
```

**Parameters:**

- `preset`: Style preset name (e.g., "theme", "minimal", "colorful")

**Example:**

```python
chart.style("minimal")
```

#### `colors()`

Set custom color palette for series.

```python
colors(*colors: str) -> Self
```

**Parameters:**

- `*colors`: Hex color values for each series

**Example:**

```python
chart.colors("#4472C4", "#ED7D31", "#A5A5A5", "#FFC000", "#5B9BD5")
```

#### `plot_area()`

Configure plot area styling.

```python
plot_area(
    *,
    background: str | None = None,
    border_color: str | None = None,
    border_width: str = "1pt"
) -> Self
```

**Parameters:**

- `background`: Background color (hex)
- `border_color`: Border color (hex)
- `border_width`: Border width

**Example:**

```python
chart.plot_area(background="#F9F9F9", border_color="#CCCCCC")
```

#### `threed()`

Enable 3D effects.

```python
threed(enabled: bool = True) -> Self
```

**Parameters:**

- `enabled`: Enable 3D rendering

**Example:**

```python
chart.pie_chart().threed()
```

### Build

#### `build()`

Build the final ChartSpec.

```python
build() -> ChartSpec
```

**Returns:** `ChartSpec` object ready for use with SpreadsheetBuilder

**Example:**

```python
chart_spec = ChartBuilder() \
    .column_chart() \
    .title("Sales by Quarter") \
    .series("Sales", "Data.B2:B5") \
    .categories("Data.A2:A5") \
    .build()

# Use with SpreadsheetBuilder
builder.chart(chart_spec)
```

---

## SparklineBuilder

### Class: `SparklineBuilder`

Fluent builder for creating inline sparklines.

```python
from spreadsheet_dl.charts import SparklineBuilder, sparkline

# Using class directly
builder = SparklineBuilder()

# Using convenience function
builder = sparkline()
```

### Sparkline Types

#### `line()`

Create a line sparkline.

```python
line() -> Self
```

**Example:**

```python
spark = SparklineBuilder().line()
```

#### `column()`

Create a column sparkline.

```python
column() -> Self
```

**Example:**

```python
spark = SparklineBuilder().column()
```

#### `win_loss()`

Create a win/loss sparkline.

```python
win_loss() -> Self
```

**Example:**

```python
spark = SparklineBuilder().win_loss()
```

### Configuration

#### `data()`

Set the data range for the sparkline.

```python
data(range_ref: str) -> Self
```

**Parameters:**

- `range_ref`: Data range (can include `{row}` placeholder for dynamic ranges)

**Examples:**

```python
# Static range
spark.data("MonthlyData.B2:M2")

# Dynamic range using row placeholder
spark.data("MonthlyData.B{row}:M{row}")
```

#### `color()`

Set sparkline color.

```python
color(color: str) -> Self
```

**Parameters:**

- `color`: Hex color code

**Example:**

```python
spark.color("#4472C4")
```

#### `negative_color()`

Set color for negative values.

```python
negative_color(color: str) -> Self
```

**Parameters:**

- `color`: Hex color code for negative values

**Example:**

```python
spark.negative_color("#FF0000")
```

#### `markers()`

Configure marker colors for special points.

```python
markers(
    *,
    high: str | None = None,
    low: str | None = None,
    first: str | None = None,
    last: str | None = None,
    negative: str | None = None
) -> Self
```

**Parameters:**

- `high`: Color for highest point
- `low`: Color for lowest point
- `first`: Color for first point
- `last`: Color for last point
- `negative`: Color for negative values

**Example:**

```python
spark.markers(
    high="#00B050",
    low="#FF0000",
    first="#0070C0",
    last="#FFC000"
)
```

#### `axis_range()`

Set axis range.

```python
axis_range(min: float | None = None, max: float | None = None) -> Self
```

**Parameters:**

- `min`: Minimum axis value (None for auto)
- `max`: Maximum axis value (None for auto)

**Example:**

```python
spark.axis_range(min=0, max=100)
```

#### `same_scale()`

Use same scale across sparkline group.

```python
same_scale(enabled: bool = True) -> Self
```

**Parameters:**

- `enabled`: Use consistent scale

**Example:**

```python
spark.same_scale(True)
```

#### `show_axis()`

Show horizontal axis.

```python
show_axis(enabled: bool = True) -> Self
```

**Parameters:**

- `enabled`: Show axis line

**Example:**

```python
spark.show_axis(True)
```

#### `build()`

Build the final Sparkline spec.

```python
build() -> Sparkline
```

**Returns:** `Sparkline` object

---

## Data Classes

### ChartSpec

Complete chart specification.

```python
@dataclass
class ChartSpec:
    chart_type: ChartType
    title: ChartTitle | None
    series: list[DataSeries]
    categories: str | None
    legend: LegendConfig
    category_axis: AxisConfig | None
    value_axis: AxisConfig | None
    secondary_axis: AxisConfig | None
    position: ChartPosition
    size: ChartSize
    plot_area: PlotAreaStyle | None
    data_labels: DataLabelConfig | None
    style_preset: str | None
    color_palette: list[str] | None
    threed: bool
```

### DataSeries

Chart data series specification.

```python
@dataclass
class DataSeries:
    name: str
    values: str
    categories: str | None = None
    color: str | None = None
    secondary_axis: bool = False
    chart_type: ChartType | None = None
    data_labels: DataLabelConfig | None = None
    trendline: Trendline | None = None
    marker_style: str | None = None
    line_width: str = "2pt"
    fill_opacity: float = 0.8
```

### ChartPosition

Chart position configuration.

```python
@dataclass
class ChartPosition:
    cell: str = "A1"
    offset_x: int = 0
    offset_y: int = 0
    move_with_cells: bool = True
    size_with_cells: bool = False
    z_order: int = 0
```

### ChartSize

Chart size configuration.

```python
@dataclass
class ChartSize:
    width: int = 400
    height: int = 300
```

### Trendline

Trendline configuration.

```python
@dataclass
class Trendline:
    type: TrendlineType
    order: int = 2
    period: int = 2
    forward_periods: int = 0
    backward_periods: int = 0
    intercept: float | None = None
    display_equation: bool = False
    display_r_squared: bool = False
    color: str | None = None
    width: str = "1pt"
    dash_style: str = "solid"
```

---

## Pre-built Chart Templates

Convenience functions for common chart types.

### `budget_comparison_chart()`

Create a budget vs actual comparison chart.

```python
budget_comparison_chart(
    categories: str,
    budget_values: str,
    actual_values: str,
    *,
    title: str = "Budget vs Actual",
    position: str = "F2"
) -> ChartSpec
```

**Example:**

```python
from spreadsheet_dl.charts import budget_comparison_chart

chart = budget_comparison_chart(
    categories="Budget.A2:A13",
    budget_values="Budget.B2:B13",
    actual_values="Budget.C2:C13",
    title="2024 Budget vs Actual",
    position="F2"
)
```

### `spending_pie_chart()`

Create a spending breakdown pie chart.

```python
spending_pie_chart(
    categories: str,
    values: str,
    *,
    title: str = "Spending by Category",
    position: str = "F2"
) -> ChartSpec
```

**Example:**

```python
from spreadsheet_dl.charts import spending_pie_chart

chart = spending_pie_chart(
    categories="Summary.A2:A10",
    values="Summary.B2:B10",
    title="Monthly Spending Distribution"
)
```

### `trend_line_chart()`

Create a trend analysis line chart.

```python
trend_line_chart(
    categories: str,
    values: str,
    *,
    title: str = "Trend Analysis",
    position: str = "F2",
    trendline: bool = True
) -> ChartSpec
```

**Example:**

```python
from spreadsheet_dl.charts import trend_line_chart

chart = trend_line_chart(
    categories="Data.A2:A13",
    values="Data.B2:B13",
    title="Revenue Trend",
    trendline=True
)
```

---

## Complete Examples

### Example 1: Budget Comparison Column Chart

```python
from spreadsheet_dl.builder import SpreadsheetBuilder
from spreadsheet_dl.charts import ChartBuilder

builder = SpreadsheetBuilder(theme="corporate")

# Create sheet with data
builder.sheet("Budget") \
    .column("Month", width="2cm") \
    .column("Budget", width="3cm", type="currency") \
    .column("Actual", width="3cm", type="currency") \
    .header_row() \
    .data_rows(12)

# Create chart
chart = ChartBuilder() \
    .column_chart() \
    .title("Monthly Budget vs Actual", font_size="16pt") \
    .categories("Budget.A2:A13") \
    .series("Budget", "Budget.B2:B13", color="#4472C4") \
    .series("Actual", "Budget.C2:C13", color="#ED7D31") \
    .legend(position="bottom") \
    .value_axis(title="Amount ($)", min=0, format_code="$#,##0") \
    .position("E2") \
    .size(450, 300) \
    .build()

builder.chart(chart)
builder.save("budget_report.ods")
```

### Example 2: Pie Chart with Data Labels

```python
from spreadsheet_dl.charts import ChartBuilder

chart = ChartBuilder() \
    .pie_chart() \
    .title("Expense Distribution") \
    .categories("Expenses.A2:A8") \
    .series("Amount", "Expenses.B2:B8") \
    .data_labels(
        show_category=True,
        show_percentage=True,
        position="outside",
        font_size="10pt"
    ) \
    .legend(position="right") \
    .colors("#4472C4", "#ED7D31", "#A5A5A5", "#FFC000", "#5B9BD5", "#70AD47", "#9E480E") \
    .position("E2") \
    .size(400, 350) \
    .build()
```

### Example 3: Combo Chart with Secondary Axis

```python
from spreadsheet_dl.charts import ChartBuilder

chart = ChartBuilder() \
    .combo_chart() \
    .title("Revenue and Growth Rate") \
    .categories("Data.A2:A13") \
    .series("Revenue", "Data.B2:B13", chart_type="column", color="#4472C4") \
    .series("Growth %", "Data.C2:C13", chart_type="line", secondary_axis=True, color="#ED7D31") \
    .value_axis(title="Revenue ($)", min=0, format_code="$#,##0") \
    .axis("secondary", title="Growth (%)", min=-10, max=50, format_code="0%") \
    .legend(position="bottom") \
    .position("E2") \
    .size(500, 350) \
    .build()
```

### Example 4: Line Chart with Trendline

```python
from spreadsheet_dl.charts import ChartBuilder

chart = ChartBuilder() \
    .line_chart(markers=True) \
    .title("Sales Trend with Forecast") \
    .categories("Sales.A2:A25") \
    .series("Sales", "Sales.B2:B25", color="#4472C4") \
    .series_trendline(
        "linear",
        forward_periods=6,
        display_equation=True,
        display_r_squared=True
    ) \
    .value_axis(title="Sales ($)", min=0) \
    .legend(visible=False) \
    .position("D2") \
    .size(600, 300) \
    .build()
```

### Example 5: Sparklines in Table

```python
from spreadsheet_dl.builder import SpreadsheetBuilder
from spreadsheet_dl.charts import SparklineBuilder

builder = SpreadsheetBuilder()

# Create sparkline spec
sparkline_spec = SparklineBuilder() \
    .line() \
    .data("MonthlyData.B{row}:M{row}") \
    .color("#4472C4") \
    .markers(high="#00B050", low="#FF0000", last="#FFC000") \
    .axis_range(min=0) \
    .build()

# Use in table
builder.sheet("Dashboard") \
    .column("Product", width="4cm") \
    .column("Trend", width="8cm")  # Sparkline column
# ... add sparkline to cells
```

---

## Enumerations

### ChartType

Chart type options.

```python
class ChartType(Enum):
    COLUMN = auto()
    COLUMN_STACKED = auto()
    COLUMN_100_STACKED = auto()
    BAR = auto()
    BAR_STACKED = auto()
    BAR_100_STACKED = auto()
    LINE = auto()
    LINE_MARKERS = auto()
    LINE_SMOOTH = auto()
    AREA = auto()
    AREA_STACKED = auto()
    AREA_100_STACKED = auto()
    PIE = auto()
    DOUGHNUT = auto()
    SCATTER = auto()
    SCATTER_LINES = auto()
    BUBBLE = auto()
    COMBO = auto()
```

### LegendPosition

Legend position options.

```python
class LegendPosition(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"
    NONE = "none"
```

### TrendlineType

Trendline type options.

```python
class TrendlineType(Enum):
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    POLYNOMIAL = "polynomial"
    POWER = "power"
    MOVING_AVERAGE = "moving_average"
```

---

## Best Practices

### 1. Use Appropriate Chart Types

```python
# Column/Bar: Comparisons across categories
chart.column_chart().series("Sales", "Data.B:B")

# Line: Trends over time
chart.line_chart().series("Revenue", "Data.B:B")

# Pie: Part-to-whole relationships
chart.pie_chart().series("Share", "Data.B:B")

# Scatter: Correlations
chart.scatter_chart().series("Correlation", "Data.B:C")
```

### 2. Configure Axes Appropriately

```python
# Always set minimums for value axes showing amounts
chart.value_axis(title="Revenue ($)", min=0, format_code="$#,##0")

# Use appropriate formats for different data types
chart.category_axis(format_code="MMM YYYY")  # Dates
chart.value_axis(format_code="0.0%")  # Percentages
```

### 3. Use Colors Effectively

```python
# Use theme-consistent colors
chart.colors("#4472C4", "#ED7D31", "#A5A5A5")

# Highlight specific series
chart.series("Budget", "Data.B:B", color="#CCCCCC") \
     .series("Actual", "Data.C:C", color="#FF0000")  # Red for emphasis
```

### 4. Position Charts Strategically

```python
# Place charts next to data
chart.position("F2")  # Right of columns A-E

# Leave space between data and chart
chart.position("F2", offset_x=20)
```

### 5. Size for Readability

```python
# Standard sizes
chart.size(400, 300)  # Small
chart.size(500, 350)  # Medium
chart.size(600, 400)  # Large

# Wide charts for time series
chart.size(700, 300)
```
