# Module: renderer

## Overview

The `renderer` module provides the core ODS rendering engine that converts builder specifications into ODS spreadsheet files. It bridges the builder API with the `odfpy` library, translating theme-based styles and sheet specifications into actual ODS documents.

This module implements several critical features including cell merging, named ranges, chart embedding, conditional formatting, and data validation.

**New in v4.0.0:**

- Chart rendering to ODS (TASK-231, GAP-BUILDER-006)
- Conditional format rendering (TASK-211, GAP-BUILDER-007)
- Data validation rendering (TASK-221, GAP-BUILDER-008)

## Key Classes

### OdsRenderer

Main class responsible for rendering sheet specifications to ODS files.

**Attributes:**

- `_theme` (Theme | None): Optional theme for styling
- `_doc` (OpenDocumentSpreadsheet | None): Current ODS document being built
- `_styles` (dict[str, Style]): Cache of created ODF styles
- `_style_counter` (int): Counter for generating unique style names
- `_merged_regions` (set[tuple[int, int]]): Tracks merged cell positions
- `_chart_counter` (int): Counter for generating unique chart IDs

**Methods:**

#### `__init__(theme: Theme | None = None) -> None`

Initialize renderer with optional theme.

**Parameters:**

- `theme` (Theme | None): Theme for styling. If None, uses default styles.

**Example:**

```python
from spreadsheet_dl.renderer import OdsRenderer
from spreadsheet_dl.schema.styles import Theme

# Create renderer with default styles
renderer = OdsRenderer()

# Create renderer with custom theme
theme = Theme.from_file("my_theme.yaml")
renderer = OdsRenderer(theme=theme)
```

#### `render(sheets, output_path, named_ranges=None, charts=None, conditional_formats=None, validations=None) -> Path`

Render sheets to an ODS file.

**Parameters:**

- `sheets` (list[SheetSpec]): List of sheet specifications to render
- `output_path` (Path): Output file path for the ODS file
- `named_ranges` (list[NamedRangeSpec] | None): Optional list of named ranges to export
- `charts` (list[ChartSpec] | None): Optional list of chart specifications to render
- `conditional_formats` (list[ConditionalFormat] | None): Optional conditional formats
- `validations` (list[ValidationConfig] | None): Optional data validations

**Returns:**

- `Path`: Path to the created ODS file

**Implements:**

- TASK-202: Named range export to ODS
- TASK-231: Chart rendering to ODS
- TASK-211: Conditional format rendering
- TASK-221: Data validation rendering

**Example:**

```python
from pathlib import Path
from spreadsheet_dl.builder import SheetBuilder
from spreadsheet_dl.renderer import OdsRenderer

# Create sheet specification
builder = SheetBuilder("Budget")
builder.add_row(["Month", "Income", "Expenses"])
builder.add_row(["January", 5000, 3000])
sheets = [builder.build()]

# Render to ODS
renderer = OdsRenderer()
output_path = renderer.render(
    sheets=sheets,
    output_path=Path("budget.ods")
)
print(f"Created: {output_path}")
```

#### `_create_default_styles() -> None`

Create default cell styles (header, currency, date, warning, success, normal, total).

**Styles Created:**

- `header` / `header_primary`: Blue headers with white bold text
- `currency` / `cell_currency`: Standard cell with 2pt padding
- `date` / `cell_date`: Date formatted cells
- `warning` / `cell_warning` / `cell_danger`: Red background for over-budget
- `good` / `cell_success`: Green background for under-budget
- `normal` / `cell_normal` / `default`: Standard cell
- `total` / `total_row`: Bold total row with blue background

#### `_create_theme_styles() -> None`

Create styles from theme definitions. Converts theme CellStyle objects to ODF Style objects.

#### `_render_sheet(sheet_spec: SheetSpec) -> None`

Render a single sheet with columns and rows. Implements cell merge rendering with covered cells (TASK-201).

**Parameters:**

- `sheet_spec` (SheetSpec): Sheet specification to render

#### `_render_cell(cell_spec, row_style, col_spec, row_idx, col_idx) -> TableCell`

Render a single cell with appropriate type, value, formula, and styling.

**Parameters:**

- `cell_spec` (CellSpec): Cell specification
- `row_style` (str | None): Default row style name
- `col_spec` (ColumnSpec | None): Column specification for type inference
- `row_idx` (int): Row index for merge tracking
- `col_idx` (int): Column index for merge tracking

**Returns:**

- `TableCell`: ODF table cell element

**Supports:**

- Cell merging (colspan/rowspan)
- Formulas
- Value types (string, currency, date, float, percentage)
- Custom styling

#### `_add_named_ranges(named_ranges: list[NamedRangeSpec]) -> None`

Add named ranges to the ODS document (TASK-202).

**Parameters:**

- `named_ranges` (list[NamedRangeSpec]): List of named range specifications

**Example:**

```python
from spreadsheet_dl.builder import NamedRange, CellRange

named_range = NamedRange(
    name="TotalIncome",
    range=CellRange(sheet="Budget", start="B2", end="B13")
)
renderer.render(sheets, output_path, named_ranges=[named_range])
```

#### `_add_charts(charts: list[ChartSpec], sheets: list[SheetSpec]) -> None`

Add charts to the ODS document (TASK-231).

**Parameters:**

- `charts` (list[ChartSpec]): List of chart specifications
- `sheets` (list[SheetSpec]): List of sheet specifications for lookup

**Supports:**

- Column, bar, line, pie, area, scatter, bubble charts
- Chart positioning by cell reference
- Chart sizing (width/height)
- Titles, legends, and axis configuration
- Multiple data series with colors

**Example:**

```python
from spreadsheet_dl.charts import ChartBuilder, ChartType

chart = (ChartBuilder()
    .set_type(ChartType.COLUMN)
    .set_title("Monthly Expenses")
    .add_series(name="Expenses", values="Budget.C2:C13")
    .set_position(cell="E2", width=400, height=300)
    .build())

renderer.render(sheets, output_path, charts=[chart])
```

#### `_add_conditional_formats(conditional_formats: list[ConditionalFormat]) -> None`

Add conditional formatting to the ODS document (TASK-211).

**Parameters:**

- `conditional_formats` (list[ConditionalFormat]): List of conditional format configurations

**Supports:**

- Color scales (2-color and 3-color)
- Data bars
- Icon sets
- Cell value rules
- Formula-based rules

#### `_add_data_validations(validations: list[ValidationConfig]) -> None`

Add data validations to the ODS document (TASK-221).

**Parameters:**

- `validations` (list[ValidationConfig]): List of validation configurations

**Supports:**

- List validation with dropdowns
- Number range validation
- Date range validation
- Custom formula validation
- Input messages and error alerts

## Key Functions

### render_sheets(sheets, output_path, theme=None, named_ranges=None, charts=None, conditional_formats=None, validations=None) -> Path

Convenience function to render sheets to ODS file.

**Parameters:**

- `sheets` (list[SheetSpec]): Sheet specifications
- `output_path` (Path | str): Output file path
- `theme` (Theme | None): Optional theme
- `named_ranges` (list[NamedRangeSpec] | None): Optional named ranges
- `charts` (list[ChartSpec] | None): Optional chart specifications
- `conditional_formats` (list[ConditionalFormat] | None): Optional conditional formats
- `validations` (list[ValidationConfig] | None): Optional data validations

**Returns:**

- `Path`: Path to created file

**Example:**

```python
from spreadsheet_dl.renderer import render_sheets
from spreadsheet_dl.builder import SheetBuilder

builder = SheetBuilder("Sheet1")
builder.add_row(["A", "B", "C"])
sheets = [builder.build()]

output = render_sheets(
    sheets=sheets,
    output_path="output.ods",
    theme=None
)
```

## Usage Examples

### Basic Sheet Rendering

```python
from pathlib import Path
from spreadsheet_dl.builder import SheetBuilder
from spreadsheet_dl.renderer import OdsRenderer

# Build a sheet
builder = SheetBuilder("Expenses")
builder.add_column("Date", width="3cm")
builder.add_column("Category", width="4cm")
builder.add_column("Amount", width="3cm", type="currency")

# Add header row
builder.add_row(["Date", "Category", "Amount"], style="header")

# Add data rows
builder.add_row(["2024-01-15", "Groceries", 125.50])
builder.add_row(["2024-01-16", "Gas", 45.00])

# Render to ODS
renderer = OdsRenderer()
output = renderer.render(
    sheets=[builder.build()],
    output_path=Path("expenses.ods")
)
```

### Sheet with Formulas and Merging

```python
from spreadsheet_dl.builder import SheetBuilder, CellSpec

builder = SheetBuilder("Budget")

# Header with merged cells
builder.add_row([
    CellSpec(value="2024 Budget", colspan=3, style="header")
])

# Column headers
builder.add_row(["Category", "Budgeted", "Actual"])

# Data with formulas
builder.add_row(["Groceries", 500, 475])
builder.add_row(["Utilities", 200, 210])
builder.add_row([
    "Total",
    CellSpec(formula="=SUM(B3:B4)", value_type="currency"),
    CellSpec(formula="=SUM(C3:C4)", value_type="currency")
])

# Render
renderer = OdsRenderer()
renderer.render([builder.build()], Path("budget.ods"))
```

### Using Themes

```python
from spreadsheet_dl.renderer import OdsRenderer
from spreadsheet_dl.schema.styles import Theme

# Load custom theme
theme = Theme.from_file("corporate_theme.yaml")

# Create renderer with theme
renderer = OdsRenderer(theme=theme)

# Render with themed styles
renderer.render(sheets, Path("themed_budget.ods"))
```

### Adding Charts

```python
from spreadsheet_dl.renderer import OdsRenderer
from spreadsheet_dl.charts import ChartBuilder, ChartType

# Create chart specification
chart = (ChartBuilder()
    .set_type(ChartType.PIE)
    .set_title("Expense Breakdown")
    .add_series(
        name="Categories",
        values="Expenses.C2:C10",
        categories="Expenses.B2:B10"
    )
    .set_position(cell="E2", width=500, height=400)
    .show_legend(position="right")
    .build())

# Render with charts
renderer = OdsRenderer()
renderer.render(
    sheets=sheets,
    output_path=Path("budget_with_chart.ods"),
    charts=[chart]
)
```

## See Also

- [builder](builder.md) - Building sheet specifications
- [charts](charts.md) - Creating chart specifications
- [schema/styles](schema/styles.md) - Theme and style system
- [schema/conditional](schema/conditional.md) - Conditional formatting
- [schema/data_validation](schema/data_validation.md) - Data validation rules
