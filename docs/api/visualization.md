# Visualization API Reference

Interactive charts and dashboards for budget visualization.

**Implements:** FR-REPORT-003 (Interactive Visualization)

## Overview

The visualization module provides:

- Pie charts for category breakdown
- Bar charts for spending trends
- Line charts for budget tracking over time
- Stacked bar charts for multi-category analysis
- Complete HTML dashboards with Chart.js
- Theme support (light/dark)

## Classes

### ChartGenerator

Generate interactive charts using Chart.js.

```python
from spreadsheet_dl.visualization import ChartGenerator, ChartConfig, ChartDataPoint, ChartType

generator = ChartGenerator(theme="default")

# Create pie chart
data = [
    ChartDataPoint("Food", 500, category="Groceries"),
    ChartDataPoint("Housing", 1500, category="Housing"),
    ChartDataPoint("Transport", 300, category="Transportation"),
]

config = ChartConfig(title="Monthly Spending", chart_type=ChartType.PIE)
html = generator.create_pie_chart(data, config)

# Save to file
with open("chart.html", "w") as f:
    f.write(html)
```

#### Constructor

```python
ChartGenerator(
    theme: str = "default",     # "default" or "dark"
    colors: list[str] | None = None  # Custom color palette
)
```

#### Methods

##### `create_pie_chart()`

Create a pie or doughnut chart.

```python
html = generator.create_pie_chart(
    data: Sequence[ChartDataPoint],
    config: ChartConfig | None = None
)
```

##### `create_bar_chart()`

Create a bar chart (vertical or horizontal).

```python
html = generator.create_bar_chart(
    data: Sequence[ChartDataPoint],
    config: ChartConfig | None = None
)
```

##### `create_line_chart()`

Create a line or area chart.

```python
from spreadsheet_dl.visualization import ChartSeries

html = generator.create_line_chart(
    labels: Sequence[str],  # X-axis labels
    series: Sequence[ChartSeries],
    config: ChartConfig | None = None
)
```

##### `create_stacked_bar_chart()`

Create a stacked bar chart.

```python
html = generator.create_stacked_bar_chart(
    labels: Sequence[str],
    series: Sequence[ChartSeries],
    config: ChartConfig | None = None
)
```

---

### DashboardGenerator

Generate complete HTML dashboards.

```python
from spreadsheet_dl.visualization import DashboardGenerator
from spreadsheet_dl.budget_analyzer import BudgetAnalyzer

# From budget analyzer
analyzer = BudgetAnalyzer("budget.ods")
dashboard = DashboardGenerator(analyzer=analyzer, theme="default")
html = dashboard.generate()
dashboard.save("dashboard.html")

# Demo mode (no analyzer)
dashboard = DashboardGenerator(theme="dark")
html = dashboard.generate()  # Uses demo data
```

#### Constructor

```python
DashboardGenerator(
    analyzer: Any = None,  # BudgetAnalyzer instance
    theme: str = "default"  # "default" or "dark"
)
```

#### Methods

##### `generate()`

Generate complete dashboard HTML.

```python
html = dashboard.generate()
```

##### `save()`

Generate and save dashboard to file.

```python
path = dashboard.save("output/dashboard.html")
```

---

### ChartConfig

Configuration for chart generation.

```python
from spreadsheet_dl.visualization import ChartConfig, ChartType

config = ChartConfig(
    title="Budget vs Actual",
    chart_type=ChartType.BAR,
    width=600,
    height=400,
    show_legend=True,
    show_labels=True,
    animation=True,
    responsive=True,
    colors=None,  # Use default palette
    cutout=60,    # Doughnut chart cutout %
    stacked=False,
    tension=0.3   # Line chart smoothing
)
```

#### Attributes

| Attribute     | Type        | Default  | Description            |
| ------------- | ----------- | -------- | ---------------------- |
| `title`       | `str`       | Required | Chart title            |
| `chart_type`  | `ChartType` | Required | Type of chart          |
| `width`       | `int`       | 600      | Chart width in pixels  |
| `height`      | `int`       | 400      | Chart height in pixels |
| `show_legend` | `bool`      | True     | Show legend            |
| `show_labels` | `bool`      | True     | Show data labels       |
| `animation`   | `bool`      | True     | Enable animations      |
| `responsive`  | `bool`      | True     | Responsive sizing      |
| `colors`      | `list[str]` | None     | Custom color palette   |
| `cutout`      | `int`       | 0        | Doughnut cutout %      |
| `stacked`     | `bool`      | False    | Stack bars             |
| `tension`     | `float`     | 0.0      | Line smoothing (0-1)   |

---

### ChartType

Enum of available chart types.

```python
from spreadsheet_dl.visualization import ChartType

ChartType.PIE            # Pie chart
ChartType.BAR            # Vertical bar chart
ChartType.LINE           # Line chart
ChartType.DOUGHNUT       # Doughnut (pie with hole)
ChartType.STACKED_BAR    # Stacked bar chart
ChartType.AREA           # Area chart (filled line)
ChartType.HORIZONTAL_BAR # Horizontal bar chart
```

---

### ChartDataPoint

Single data point for charts.

```python
from spreadsheet_dl.visualization import ChartDataPoint

point = ChartDataPoint(
    label="Groceries",
    value=450.50,
    color="#27ae60",     # Optional custom color
    category="Groceries"  # For auto-coloring
)
```

---

### ChartSeries

Series of data for multi-series charts.

```python
from spreadsheet_dl.visualization import ChartSeries

series = ChartSeries(
    name="Budget",
    data=[5000, 5000, 5200, 5200],
    color="#4472C4"  # Optional
)
```

---

## Module Functions

### `create_spending_pie_chart()`

Create a pie chart from category spending data.

```python
from spreadsheet_dl.visualization import create_spending_pie_chart

html = create_spending_pie_chart(
    categories={
        "Groceries": 450,
        "Housing": 1500,
        "Transportation": 300,
    },
    title="Monthly Spending",
    output_path="spending.html"  # Optional save path
)
```

### `create_budget_dashboard()`

Create a complete budget dashboard.

```python
from spreadsheet_dl.visualization import create_budget_dashboard
from spreadsheet_dl.budget_analyzer import BudgetAnalyzer

analyzer = BudgetAnalyzer("budget.ods")

html = create_budget_dashboard(
    analyzer=analyzer,
    output_path="dashboard.html",
    theme="dark"
)
```

---

## Constants

### `CATEGORY_COLORS`

Pre-defined colors for budget categories.

```python
from spreadsheet_dl.visualization import CATEGORY_COLORS

CATEGORY_COLORS = {
    "Housing": "#2c3e50",
    "Utilities": "#3498db",
    "Groceries": "#27ae60",
    "Transportation": "#e67e22",
    "Healthcare": "#e74c3c",
    "Insurance": "#9b59b6",
    "Entertainment": "#f39c12",
    "Dining Out": "#1abc9c",
    "Clothing": "#d35400",
    "Personal Care": "#c0392b",
    "Education": "#2980b9",
    "Savings": "#16a085",
    "Debt Payment": "#8e44ad",
    "Gifts": "#f1c40f",
    "Subscriptions": "#34495e",
    "Miscellaneous": "#7f8c8d",
}
```

### `DEFAULT_COLORS`

Default color palette for charts.

```python
from spreadsheet_dl.visualization import DEFAULT_COLORS

# 15 colors suitable for data visualization
DEFAULT_COLORS = [
    "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
    "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac",
    "#86bcb6", "#8cd17d", "#b6992d", "#499894", "#d4a6c8"
]
```

---

## Complete Example

```python
from spreadsheet_dl.visualization import (
    ChartGenerator,
    DashboardGenerator,
    ChartConfig,
    ChartDataPoint,
    ChartSeries,
    ChartType,
    create_spending_pie_chart,
)
from pathlib import Path

# Create output directory
output_dir = Path("./reports")
output_dir.mkdir(exist_ok=True)

# 1. Simple Pie Chart
spending = {
    "Groceries": 450,
    "Housing": 1500,
    "Transportation": 300,
    "Utilities": 180,
    "Entertainment": 120,
}

create_spending_pie_chart(
    spending,
    title="January Spending",
    output_path=output_dir / "pie_chart.html"
)

# 2. Custom Bar Chart
generator = ChartGenerator(theme="default")

data = [
    ChartDataPoint(label=cat, value=amt, category=cat)
    for cat, amt in spending.items()
]

config = ChartConfig(
    title="Spending by Category",
    chart_type=ChartType.HORIZONTAL_BAR,
    height=300
)

bar_html = generator.create_bar_chart(data, config)
(output_dir / "bar_chart.html").write_text(bar_html)

# 3. Multi-Series Line Chart
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
budget_series = ChartSeries(
    name="Budget",
    data=[5000, 5000, 5000, 5200, 5200, 5200]
)
actual_series = ChartSeries(
    name="Actual",
    data=[4800, 5100, 4600, 5300, 4900, 4400]
)

line_config = ChartConfig(
    title="Budget vs Actual Trend",
    chart_type=ChartType.LINE,
    tension=0.3  # Smooth curves
)

line_html = generator.create_line_chart(
    months,
    [budget_series, actual_series],
    line_config
)
(output_dir / "trend_chart.html").write_text(line_html)

# 4. Complete Dashboard (Dark Theme)
dashboard = DashboardGenerator(theme="dark")
dashboard.save(output_dir / "dashboard.html")

print(f"Charts saved to {output_dir}/")
```

### Dashboard Output Features

The generated dashboard includes:

- **Summary Cards**: Total budget, spent, remaining, percentage used
- **Progress Bar**: Visual budget usage with color coding
- **Pie/Doughnut Chart**: Category breakdown with tooltips
- **Horizontal Bar Chart**: Side-by-side category comparison
- **Category List**: Detailed breakdown with color indicators
- **Trend Chart**: Budget vs spending over time (if data available)
- **Responsive Design**: Works on desktop and mobile
- **Theme Support**: Light and dark modes
