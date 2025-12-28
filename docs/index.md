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

## Features

### Core Functionality

- Generate structured budget spreadsheets with formulas
- Analyze spending patterns with pandas
- Generate reports in text, Markdown, or JSON
- Mobile-friendly ODS files
- CLI and Python API

### Integration Features

- **WebDAV Upload** - Direct upload to Nextcloud
- **Bank CSV Import** - Import from Chase, Bank of America, Capital One, and more
- **Auto-Categorization** - Automatic transaction categorization

### Advanced Features

- **Analytics Dashboard** - Comprehensive budget analytics
- **Alert System** - Configurable budget alerts
- **Recurring Expenses** - Track recurring payments
- **Budget Templates** - Pre-built templates (50/30/20, Family, FIRE, etc.)
- **Visual Themes** - 5 built-in themes for spreadsheet styling

## Version

Current version: **v0.4.1**

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
│   ├── ods_editor.py       # Modify existing ODS files (NEW)
│   ├── budget_analyzer.py  # Analyze budgets
│   ├── cli.py              # Command-line interface
│   ├── exceptions.py       # Comprehensive error hierarchy
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
