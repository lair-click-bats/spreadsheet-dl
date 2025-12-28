# Finance Tracker Documentation

Family financial tracking with ODS spreadsheets for Nextcloud and Collabora Office.

## Overview

Finance Tracker provides Python tools for creating, analyzing, and reporting on family budget spreadsheets in ODS format. Designed for seamless integration with self-hosted infrastructure.

## Quick Links

- [Installation Guide](installation.md) - Get started quickly
- [User Guide](user-guide.md) - Comprehensive usage instructions
- [API Reference](api/index.md) - Complete API documentation
- [CLI Reference](cli.md) - Command-line interface documentation
- [Examples](examples/index.md) - Practical usage examples
- [Error Codes](error-codes.md) - Error code reference

## Guides

- [Builder API Reference](api/builder.md) - Fluent API for spreadsheet construction
- [Theme Creation Guide](guides/theme-creation.md) - Create custom visual themes
- [Template Creation Guide](guides/template-creation.md) - Build reusable templates

## Features

### Core Functionality

- Generate structured budget spreadsheets with formulas
- Analyze spending patterns with pandas
- Generate reports in text, Markdown, or JSON
- Mobile-friendly ODS files
- CLI and Python API

### v2.0 Professional Features

- **Template Engine** - YAML-based templates with variable substitution
- **Theme System** - Comprehensive color palettes, font pairings, and typography
- **ChartBuilder** - Fluent API for creating charts and sparklines
- **FormulaBuilder** - Type-safe formula construction with 60+ functions
- **Component Library** - Pre-built components for financial documents

### Integration Features

- **WebDAV Upload** - Direct upload to Nextcloud
- **Bank CSV Import** - Import from Chase, Bank of America, Capital One, and more
- **Auto-Categorization** - Automatic transaction categorization

### Advanced Features

- **Analytics Dashboard** - Comprehensive budget analytics
- **Alert System** - Configurable budget alerts
- **Recurring Expenses** - Track recurring payments
- **Budget Templates** - Pre-built templates (50/30/20, Family, FIRE, etc.)
- **Visual Themes** - Professional themes for spreadsheet styling

## Version

Current version: **v1.0.0** (v2.0.0 in development)

### What's New in v2.0 (Development)

- **Template Engine** - Define spreadsheets declaratively in YAML
  - Variable substitution with `${...}` syntax
  - Built-in functions (month_name, format_currency, etc.)
  - Conditional content rendering
  - Reusable components

- **Enhanced Theme System**
  - Color palette management with accessibility checking
  - Font pairing system with pre-built pairings
  - Typography hierarchy with type scales

- **ChartBuilder** - Fluent API for charts
  - Column, bar, line, area, pie, scatter charts
  - Sparklines for inline visualizations
  - Trendlines with forecasting
  - Full styling and positioning control

- **Extended Builder API**
  - Workbook properties (title, author, etc.)
  - Named ranges
  - Sheet freezing and protection
  - Alternating row styles
  - Chart integration

- **FormulaBuilder Enhancement**
  - Financial functions (PMT, PV, FV, NPV, IRR)
  - Date/time functions
  - Lookup functions (VLOOKUP, INDEX/MATCH)
  - Text and statistical functions
  - Array formula support

### What's New in v0.4.1

- **FR-CORE-003**: Expense append functionality - the `expense` command now actually writes to ODS files
- **OdsEditor module**: New module for modifying existing ODS files
- **--dry-run flag**: Preview expense additions without modifying files
- **FR-UX-003**: Comprehensive error code system (FT-xxx-nnn format)
  - Structured error messages with error codes, details, and suggestions
  - Error code reference documentation
  - 50+ specific exception classes with actionable guidance

### What's New in v0.4.0

- Declarative DSL for themes and styling
- YAML-based theme definitions
- Fluent Builder API for spreadsheet construction
- Type-safe FormulaBuilder

## Installation

```bash
# Using uv (recommended)
cd ~/development/finance-tracker
uv sync

# Install with theme support
uv sync --extra config
```

## Basic Usage

```python
from finance_tracker import OdsGenerator, BudgetAnalyzer

# Create a budget
generator = OdsGenerator()
generator.create_budget_spreadsheet("budget_2025_01.ods")

# Analyze spending
analyzer = BudgetAnalyzer("budget_2025_01.ods")
summary = analyzer.get_summary()
print(f"Total spent: ${summary.total_spent}")
```

### Using the Builder API

```python
from finance_tracker.builder import SpreadsheetBuilder, formula
from finance_tracker.charts import ChartBuilder

# Create spreadsheet with fluent API
builder = SpreadsheetBuilder(theme="professional")

builder.sheet("Budget") \
    .column("Category", width="150pt") \
    .column("Budget", width="100pt", type="currency") \
    .column("Actual", width="100pt", type="currency") \
    .freeze(rows=1) \
    .header_row() \
    .data_rows(10, alternate_styles=["row_even", "row_odd"]) \
    .total_row(formulas=["Total", "=SUM(B2:B11)", "=SUM(C2:C11)"])

# Add a chart
chart = ChartBuilder() \
    .column_chart() \
    .title("Budget vs Actual") \
    .series("Budget", "B2:B11") \
    .series("Actual", "C2:C11") \
    .position("E2") \
    .build()

builder.chart(chart)
builder.save("budget.ods")
```

## CLI Quick Start

```bash
# Generate budget
uv run finance-tracker generate -o ./budgets/

# Add expense (NEW in v0.4.1 - actually writes to file!)
uv run finance-tracker expense 25.50 "Lunch" -c "Dining Out"

# Analyze budget
uv run finance-tracker analyze budget.ods

# View dashboard
uv run finance-tracker dashboard budget.ods
```

## Architecture

```
finance-tracker/
├── src/finance_tracker/
│   ├── ods_generator.py    # Create ODS files
│   ├── ods_editor.py       # Modify existing ODS files
│   ├── budget_analyzer.py  # Analyze budgets
│   ├── builder.py          # Fluent builder API
│   ├── charts.py           # Chart builder (NEW)
│   ├── cli.py              # Command-line interface
│   ├── exceptions.py       # Comprehensive error hierarchy
│   ├── schema/             # Data classes and styles
│   ├── template_engine/    # Template system (NEW)
│   │   ├── schema.py       # Template data structures
│   │   ├── loader.py       # YAML template loading
│   │   ├── renderer.py     # Template rendering
│   │   └── components.py   # Pre-built components
│   └── ...
├── tests/                  # Test suite (260+ tests)
└── docs/                   # Documentation
```

## Error Handling

Finance Tracker uses structured error codes for programmatic error handling:

```python
from finance_tracker.exceptions import InvalidAmountError

try:
    # Process expense
    ...
except InvalidAmountError as e:
    print(f"Error [{e.error_code}]: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    # Output:
    # Error [FT-VAL-401]: Invalid amount 'abc': Not a valid number
    # Suggestion: Enter a numeric value without letters (e.g., 99.99 or 99).
```

See [Error Codes Reference](error-codes.md) for complete documentation.

## License

MIT License - See LICENSE file for details.
