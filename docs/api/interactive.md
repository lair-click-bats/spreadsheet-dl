# Interactive Features API Reference

Interactive ODS features for enhanced spreadsheet interactivity.

**Implements:** FR-HUMAN-002 (Interactive Features), FR-HUMAN-003 (Dashboard View)

## Overview

The Interactive module provides interactive elements for ODS spreadsheets including dropdowns, data validation, conditional formatting, and dashboard generation.

Features:

- Dropdown lists for category selection
- Data validation rules for amounts and dates
- Conditional formatting for budget status
- Interactive dashboard with KPIs
- Sparklines for trend visualization
- Dashboard KPI metrics

## Enumerations

### ValidationRuleType

Types of data validation rules.

```python
from spreadsheet_dl.interactive import ValidationRuleType

ValidationRuleType.WHOLE_NUMBER    # Integer values
ValidationRuleType.DECIMAL         # Decimal numbers
ValidationRuleType.LIST            # List of values
ValidationRuleType.DATE            # Date values
ValidationRuleType.TIME            # Time values
ValidationRuleType.TEXT_LENGTH     # Text length limits
ValidationRuleType.CUSTOM          # Custom formula
```

---

### ComparisonOperator

Comparison operators for validation.

```python
from spreadsheet_dl.interactive import ComparisonOperator

ComparisonOperator.EQUAL
ComparisonOperator.NOT_EQUAL
ComparisonOperator.GREATER
ComparisonOperator.GREATER_OR_EQUAL
ComparisonOperator.LESS
ComparisonOperator.LESS_OR_EQUAL
ComparisonOperator.BETWEEN
ComparisonOperator.NOT_BETWEEN
```

---

### ConditionalFormatType

Types of conditional formatting.

```python
from spreadsheet_dl.interactive import ConditionalFormatType

ConditionalFormatType.CELL_VALUE       # Format based on cell value
ConditionalFormatType.FORMULA          # Format based on formula result
ConditionalFormatType.COLOR_SCALE      # Color gradient scale
ConditionalFormatType.DATA_BAR         # Data bar visualization
ConditionalFormatType.ICON_SET         # Icon set indicators
ConditionalFormatType.TOP_N            # Top N values
ConditionalFormatType.ABOVE_AVERAGE    # Above average values
ConditionalFormatType.DUPLICATE        # Duplicate detection
```

---

## Validation Rules

### ValidationRule

Data validation rule for spreadsheet cells.

```python
from spreadsheet_dl.interactive import ValidationRule, ValidationRuleType, ComparisonOperator

# Decimal number validation (>=0)
rule = ValidationRule(
    rule_type=ValidationRuleType.DECIMAL,
    operator=ComparisonOperator.GREATER_OR_EQUAL,
    value1=0,
    error_message="Amount must be positive"
)

# Date validation
rule = ValidationRule(
    rule_type=ValidationRuleType.DATE,
    error_message="Please enter a valid date"
)

# Text length validation (<=100 characters)
rule = ValidationRule(
    rule_type=ValidationRuleType.TEXT_LENGTH,
    operator=ComparisonOperator.LESS_OR_EQUAL,
    value1=100,
    error_message="Description must be 100 characters or less"
)
```

**Attributes:**

- `rule_type: ValidationRuleType` - Type of validation
- `operator: ComparisonOperator` - Comparison operator
- `value1: Any` - First comparison value
- `value2: Any` - Second value (for BETWEEN)
- `input_title: str` - Title for input prompt
- `input_message: str` - Message for input prompt
- `error_title: str` - Error dialog title
- `error_message: str` - Error message text
- `allow_blank: bool` - Whether blank cells are valid
- `show_dropdown: bool` - Show dropdown for list validation
- `values: list[str]` - List values for LIST type

---

### DropdownList

Dropdown list for cell selection.

```python
from spreadsheet_dl.interactive import DropdownList

# Create dropdown from list
dropdown = DropdownList(
    name="categories",
    values=["Housing", "Food", "Transportation", "Entertainment"],
    allow_custom=False
)

# Use predefined dropdowns
categories = DropdownList.categories()
account_types = DropdownList.account_types()
months = DropdownList.months()

# Convert to validation rule
rule = dropdown.to_validation_rule()
```

**Attributes:**

- `name: str` - Dropdown name
- `values: list[str]` - List of values
- `source_range: str | None` - Cell range as source
- `allow_custom: bool` - Allow custom values

**Class Methods:**

#### `categories() -> DropdownList`

Predefined dropdown for expense categories.

```python
dropdown = DropdownList.categories()
# Values from ExpenseCategory enum
```

#### `account_types() -> DropdownList`

Predefined dropdown for account types.

```python
dropdown = DropdownList.account_types()
# Values: checking, savings, credit_card, investment, loan, cash, other
```

#### `months() -> DropdownList`

Predefined dropdown for months.

```python
dropdown = DropdownList.months()
# Values: January, February, ..., December
```

---

## Conditional Formatting

### ConditionalFormat

Conditional formatting rule.

```python
from spreadsheet_dl.interactive import ConditionalFormat

# Red background for over-budget values
red_format = ConditionalFormat.over_budget_warning()

# Green background for under-budget values
green_format = ConditionalFormat.under_budget_success()

# Color scale (green to red gradient)
scale_format = ConditionalFormat.percentage_color_scale()

# Data bar for spending visualization
bar_format = ConditionalFormat.spending_data_bar()
```

**Attributes:**

- `format_type: ConditionalFormatType` - Type of formatting
- `operator: ComparisonOperator` - Comparison operator
- `value1: Any` - First comparison value
- `value2: Any` - Second value (for ranges)
- `formula: str | None` - Custom formula
- `style: dict[str, Any]` - Style settings (colors, fonts)
- `priority: int` - Rule priority

**Class Methods:**

#### `over_budget_warning() -> ConditionalFormat`

Red background for over-budget cells.

#### `under_budget_success() -> ConditionalFormat`

Green background for under-budget cells.

#### `percentage_color_scale() -> ConditionalFormat`

Color gradient from green (0%) to red (100%).

#### `spending_data_bar() -> ConditionalFormat`

Data bar visualization for spending amounts.

---

## Dashboard Components

### DashboardKPI

Key Performance Indicator for dashboard display.

```python
from spreadsheet_dl.interactive import DashboardKPI

kpi = DashboardKPI(
    name="Total Spent",
    value=2500.50,
    target=3000.00,
    unit="$",
    trend="up",  # up, down, stable
    status="warning"  # good, warning, critical
)

# Get formatted value
print(kpi.formatted_value)  # -> "$2,500.50"

# Get progress percentage
print(kpi.progress_percent)  # -> 83.35

# Convert to dictionary
data = kpi.to_dict()
```

**Attributes:**

- `name: str` - KPI display name
- `value: float` - Current value
- `target: float | None` - Target value
- `unit: str` - Unit of measurement (default: "$")
- `trend: str` - Trend direction (up, down, stable)
- `status: str` - Status (good, warning, critical)

**Properties:**

- `formatted_value: str` - Formatted value with unit
- `progress_percent: float` - Progress toward target (0-100)

---

### SparklineConfig

Configuration for sparkline visualization.

```python
from spreadsheet_dl.interactive import SparklineConfig

# Line sparkline showing spending trend
sparkline = SparklineConfig(
    data_range="A2:A30",
    sparkline_type="line",
    color="#2196F3",
    negative_color="#F44336",
    show_markers=False
)

# Column sparkline
sparkline = SparklineConfig(
    data_range="B2:B12",
    sparkline_type="column",
    color="#4CAF50"
)

# Get formula
formula = sparkline.to_formula()
```

**Attributes:**

- `data_range: str` - Cell range for data
- `sparkline_type: str` - Type (line, bar, column)
- `color: str` - Primary color (hex)
- `negative_color: str` - Color for negative values
- `show_markers: bool` - Show data point markers

---

### DashboardSection

Dashboard section configuration.

```python
from spreadsheet_dl.interactive import DashboardSection, DashboardKPI

section = DashboardSection(
    title="Budget Overview",
    kpis=[
        DashboardKPI("Total Budget", 5000, unit="$"),
        DashboardKPI("Total Spent", 3200, target=5000, unit="$"),
    ],
    chart_type="column",
    data_range="A2:B12",
    position=(1, 1),
    size=(4, 6)
)
```

**Attributes:**

- `title: str` - Section title
- `kpis: list[DashboardKPI]` - KPIs to display
- `chart_type: str | None` - Chart type (pie, bar, column, line)
- `data_range: str | None` - Data range for charts
- `position: tuple[int, int]` - Grid position (row, col)
- `size: tuple[int, int]` - Size in cells (rows, cols)

---

## Interactive ODS Builder

### InteractiveOdsBuilder

Builder for adding interactive features to ODS spreadsheets.

```python
from spreadsheet_dl.interactive import (
    InteractiveOdsBuilder,
    DropdownList,
    ValidationRule,
    ConditionalFormat,
    SparklineConfig
)

builder = InteractiveOdsBuilder()

# Add category dropdown to column B
builder.add_dropdown("B2:B100", DropdownList.categories())

# Add amount validation to column D
builder.add_validation(
    "D2:D100",
    ValidationRule(
        rule_type=ValidationRuleType.DECIMAL,
        operator=ComparisonOperator.GREATER_OR_EQUAL,
        value1=0,
        error_message="Amount must be positive"
    )
)

# Add conditional formatting
builder.add_conditional_format("E2:E100", ConditionalFormat.over_budget_warning())

# Add sparkline to cell F1
builder.add_sparkline("F1", SparklineConfig(data_range="D2:D30"))

# Apply to ODS document
builder.apply_to_document(doc)
```

**Methods:**

#### `add_dropdown(cell_range: str, dropdown: DropdownList) -> Self`

Add dropdown to cell range.

#### `add_validation(cell_range: str, rule: ValidationRule) -> Self`

Add validation rule to cell range.

#### `add_conditional_format(cell_range: str, format: ConditionalFormat) -> Self`

Add conditional formatting to cell range.

#### `add_sparkline(cell: str, config: SparklineConfig) -> Self`

Add sparkline to a cell.

#### `add_dashboard_section(section: DashboardSection) -> Self`

Add dashboard section.

#### `apply_to_document(doc: Any) -> None`

Apply all interactive features to ODS document.

---

## Dashboard Generator

### DashboardGenerator

Generate dashboard views in ODS spreadsheets.

```python
from spreadsheet_dl.interactive import DashboardGenerator
from pathlib import Path

generator = DashboardGenerator()

# Generate dashboard from budget file
dashboard_path = generator.generate_dashboard(
    budget_path=Path("budget.ods"),
    output_path=Path("budget_dashboard.ods")
)

print(f"Dashboard created: {dashboard_path}")
```

**Methods:**

#### `generate_dashboard(budget_path: Path, output_path: Path | None = None) -> Path`

Generate dashboard ODS file from budget data.

```python
output = generator.generate_dashboard(
    budget_path=Path("my_budget.ods"),
    output_path=Path("dashboard.ods")
)
# Default output: my_budget_dashboard.ods
```

**Returns:** Path to generated dashboard file

---

## Convenience Functions

### add_interactive_features(ods_path: Path, output_path: Path | None = None) -> Path

Add interactive features to existing ODS file.

```python
from spreadsheet_dl.interactive import add_interactive_features
from pathlib import Path

# Add features in-place
output = add_interactive_features(Path("budget.ods"))

# Save to new file
output = add_interactive_features(
    Path("budget.ods"),
    output_path=Path("budget_interactive.ods")
)
```

Adds:

- Category dropdown to column B
- Amount validation to column D
- Date validation to column A
- Conditional formatting for budget status

---

### generate_budget_dashboard(budget_path: Path, output_path: Path | None = None) -> Path

Generate dashboard from budget file.

```python
from spreadsheet_dl.interactive import generate_budget_dashboard
from pathlib import Path

dashboard = generate_budget_dashboard(
    budget_path=Path("budget.ods"),
    output_path=Path("dashboard.ods")
)

print(f"Dashboard: {dashboard}")
```

---

## Complete Example

```python
from spreadsheet_dl.interactive import (
    InteractiveOdsBuilder,
    DashboardGenerator,
    DropdownList,
    ValidationRule,
    ValidationRuleType,
    ComparisonOperator,
    ConditionalFormat,
    DashboardKPI,
    SparklineConfig,
)
from pathlib import Path

# Load existing ODS
from odf.opendocument import load

doc = load("budget.ods")

# Create builder
builder = InteractiveOdsBuilder()

# Add dropdowns for categories
builder.add_dropdown("B2:B100", DropdownList.categories())

# Add validation for amounts
builder.add_validation(
    "D2:D100",
    ValidationRule(
        rule_type=ValidationRuleType.DECIMAL,
        operator=ComparisonOperator.GREATER_OR_EQUAL,
        value1=0,
        error_message="Amount must be positive"
    )
)

# Add conditional formatting
builder.add_conditional_format("E2:E100", ConditionalFormat.over_budget_warning())
builder.add_conditional_format("E2:E100", ConditionalFormat.under_budget_success())

# Apply to document
builder.apply_to_document(doc)

# Save enhanced file
doc.save("budget_interactive.ods")

# Generate dashboard
generator = DashboardGenerator()
dashboard_path = generator.generate_dashboard(Path("budget.ods"))
print(f"Dashboard created: {dashboard_path}")
```

---

## Supported Spreadsheet Applications

The interactive features work with:

- LibreOffice Calc
- Apache OpenOffice Calc
- Microsoft Excel (after conversion from ODS)

Note: Some advanced features (conditional formatting, sparklines) may require additional implementation depending on the ODS library used.
