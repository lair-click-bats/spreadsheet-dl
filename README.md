# Finance Tracker

Family financial tracking with ODS spreadsheets for Nextcloud and Collabora Office.

## Overview

This project provides Python tools for creating, analyzing, and reporting on family budget spreadsheets in ODS format. Designed for seamless integration with:

- **Nextcloud** - Self-hosted file sync and storage with WebDAV upload
- **Collabora Office** - Online document editing in Nextcloud
- **Mobile Editing** - iOS/Android via Nextcloud app
- **Claude Code** - Optional LLM integration via LibreOffice MCP

## Features

### Core (v0.1.0)

- Generate structured budget spreadsheets with formulas
- Analyze spending with pandas
- Generate reports in text, Markdown, or JSON
- Mobile-friendly ODS files
- CLI and Python API

### New in v0.2.0

- **WebDAV Upload** - Direct upload to Nextcloud
- **Bank CSV Import** - Import from Chase, Bank of America, Capital One, and more
- **Auto-Categorization** - Automatic transaction categorization with ML-like patterns
- **Analytics Dashboard** - Comprehensive budget analytics and insights
- **Alert System** - Configurable budget alerts and notifications
- **Recurring Expenses** - Track and auto-generate recurring payments
- **Budget Templates** - Pre-built templates (50/30/20, Family, FIRE, and more)
- **Quick Expense CLI** - Add expenses from command line

### New in v0.4.0 - Declarative DSL

- **YAML Theme System** - Define visual styles in YAML files
- **5 Built-in Themes** - default, corporate, minimal, dark, high_contrast
- **Fluent Builder API** - Chainable spreadsheet construction
- **FormulaBuilder** - Type-safe ODF formula generation
- **Theme Inheritance** - Extend and customize themes
- **CLI Theme Support** - `--theme` flag for all generation commands

## Quick Start

### Installation

```bash
# Clone the repository
cd ~/development/finance-tracker

# Set up Python environment with uv
uv sync

# Install dev dependencies
uv sync --dev

# Install with theme support (requires PyYAML)
uv sync --extra config
```

### CLI Commands

```bash
# Create a budget (with optional template and theme)
uv run finance-tracker generate -o ./budgets/
uv run finance-tracker generate -o ./budgets/ -t 50_30_20
uv run finance-tracker generate -o ./budgets/ --theme corporate
uv run finance-tracker generate -o ./budgets/ -t family --theme minimal

# List available themes
uv run finance-tracker themes
uv run finance-tracker themes --json

# Analyze a budget
uv run finance-tracker analyze budget.ods
uv run finance-tracker analyze budget.ods --json

# Generate reports
uv run finance-tracker report budget.ods -f text
uv run finance-tracker report budget.ods -f markdown -o report.md

# View analytics dashboard
uv run finance-tracker dashboard budget.ods
uv run finance-tracker dashboard budget.ods --json

# Check budget alerts
uv run finance-tracker alerts budget.ods
uv run finance-tracker alerts budget.ods --critical-only

# Import bank CSV
uv run finance-tracker import transactions.csv --bank chase
uv run finance-tracker import transactions.csv --preview
uv run finance-tracker import transactions.csv --theme default

# Quick expense entry
uv run finance-tracker expense 25.50 "Lunch at Chipotle"
uv run finance-tracker expense 150 "Whole Foods" -c Groceries

# Upload to Nextcloud
uv run finance-tracker upload budget.ods

# List available templates
uv run finance-tracker templates
```

## Python API

### Basic Usage

```python
from decimal import Decimal
from datetime import date
from finance_tracker import (
    OdsGenerator, BudgetAnalyzer, ReportGenerator,
    ExpenseCategory, ExpenseEntry, BudgetAllocation,
)

# Create a budget
generator = OdsGenerator()
generator.create_budget_spreadsheet(
    "budget_2025_01.ods",
    month=1,
    year=2025,
    expenses=[
        ExpenseEntry(
            date=date(2025, 1, 5),
            category=ExpenseCategory.GROCERIES,
            description="Weekly groceries",
            amount=Decimal("125.50"),
        ),
    ],
    budget_allocations=[
        BudgetAllocation(ExpenseCategory.GROCERIES, Decimal("600")),
        BudgetAllocation(ExpenseCategory.UTILITIES, Decimal("200")),
    ],
)

# Analyze spending
analyzer = BudgetAnalyzer("budget_2025_01.ods")
summary = analyzer.get_summary()
print(f"Total spent: ${summary.total_spent}")
print(f"Budget used: {summary.percent_used:.1f}%")

# Generate report
report_gen = ReportGenerator("budget_2025_01.ods")
print(report_gen.generate_text_report())
```

### Using Themes (New in v0.4.0)

```python
from finance_tracker import OdsGenerator, create_monthly_budget

# Create budget with a theme
generator = OdsGenerator(theme="corporate")
generator.create_budget_spreadsheet("corporate_budget.ods")

# Or use convenience function
path = create_monthly_budget("./budgets", theme="minimal")
```

### Fluent Builder API (New in v0.4.0)

```python
from decimal import Decimal
from finance_tracker import create_spreadsheet, formula

# Build spreadsheet with fluent API
builder = create_spreadsheet(theme="default")

# Create Expense Log sheet
builder.sheet("Expense Log") \
    .column("Date", width="2.5cm", type="date") \
    .column("Category", width="3cm") \
    .column("Description", width="4cm") \
    .column("Amount", width="2.5cm", type="currency") \
    .column("Notes", width="4cm") \
    .header_row(style="header_primary") \
    .data_rows(50)

# Create Summary sheet with formulas
f = formula()
builder.sheet("Summary") \
    .column("Category", width="3cm") \
    .column("Budget", width="2.5cm", type="currency") \
    .column("Actual", width="2.5cm", type="currency") \
    .column("Remaining", width="2.5cm", type="currency") \
    .header_row() \
    .row() \
        .cell("Groceries") \
        .cell(Decimal("600")) \
        .cell(formula=f.sumif(
            f.sheet("Expense Log").col("B"),
            f.cell("A2"),
            f.sheet("Expense Log").col("D")
        )) \
        .cell(formula=f.subtract("B2", "C2"))

# Save
builder.save("my_budget.ods")
```

### FormulaBuilder API

```python
from finance_tracker import formula

f = formula()

# SUM formula
f.sum(f.range("A2", "A100"))
# -> "of:=SUM([.A2:A100])"

# Cross-sheet SUMIF
f.sumif(
    f.sheet("Expenses").col("B"),
    f.cell("A2"),
    f.sheet("Expenses").col("D"),
)
# -> "of:=SUMIF(['Expenses'.$B:$B];[.A2];['Expenses'.$D:$D])"

# VLOOKUP with exact match
f.vlookup(
    f.cell("A2"),
    f.range("A1", "B100"),
    2,
    exact=True,
)
# -> "of:=VLOOKUP([.A2];[.A1:B100];2;0)"

# Division with zero check
f.divide("B2", "C2")
# -> "of:=IF([.C2]>0;[.B2]/[.C2];0)"
```

### Using Templates

```python
from finance_tracker import get_template, OdsGenerator

# Get a predefined template
template = get_template("50_30_20")  # or "family", "fire", "minimalist", etc.

# Scale to your income
scaled_allocations = template.scale_to_income(Decimal("6000"))

# Create budget
generator = OdsGenerator()
generator.create_budget_spreadsheet(
    "my_budget.ods",
    budget_allocations=scaled_allocations,
)
```

### Import Bank Transactions

```python
from finance_tracker import import_bank_csv, OdsGenerator

# Import from CSV (auto-detects bank format)
expenses = import_bank_csv("bank_export.csv", bank="auto")

# Create budget with imported expenses
generator = OdsGenerator()
generator.create_budget_spreadsheet("imported.ods", expenses=expenses)
```

### Analytics Dashboard

```python
from finance_tracker import generate_dashboard

# Get comprehensive analytics
data = generate_dashboard("budget.ods")

print(f"Status: {data['budget_status']}")
print(f"Days remaining: {data['days_remaining']}")
print(f"Daily budget: ${data['daily_budget_remaining']:.2f}")

for rec in data['recommendations']:
    print(f"- {rec}")
```

### Alert System

```python
from finance_tracker import check_budget_alerts, AlertConfig

# Check with custom thresholds
config = AlertConfig(
    budget_warning_threshold=75.0,
    large_transaction_threshold=150.0,
    watched_categories=["Dining Out", "Entertainment"],
)

alerts = check_budget_alerts("budget.ods", config)
for alert in alerts:
    print(f"[{alert.severity.value}] {alert.title}: {alert.message}")
```

### Recurring Expenses

```python
from finance_tracker import RecurringExpenseManager, RecurringExpense, RecurrenceFrequency
from finance_tracker.recurring import create_common_recurring

# Create manager
manager = RecurringExpenseManager("recurring.json")

# Add from template
manager.add(create_common_recurring("netflix", Decimal("15.99")))
manager.add(create_common_recurring("rent", Decimal("1500.00")))

# Add custom
manager.add(RecurringExpense(
    name="Gym Membership",
    category=ExpenseCategory.HEALTHCARE,
    amount=Decimal("49.99"),
    frequency=RecurrenceFrequency.MONTHLY,
    start_date=date(2025, 1, 1),
    day_of_month=15,
))

# Generate for a month
entries = manager.generate_for_month(1, 2025)
print(f"Monthly total: ${manager.calculate_monthly_total()}")
```

### WebDAV Upload

```python
from finance_tracker import upload_budget, NextcloudConfig

# Configure (or use environment variables)
config = NextcloudConfig(
    server_url="https://nextcloud.example.com",
    username="your_username",
    password="your_app_password",
    remote_path="/Finance",
)

# Upload
url = upload_budget("budget.ods", config)
print(f"Uploaded to: {url}")
```

Or set environment variables:

```bash
export NEXTCLOUD_URL=https://nextcloud.example.com
export NEXTCLOUD_USER=username
export NEXTCLOUD_PASSWORD=app-password
export NEXTCLOUD_PATH=/Finance
```

## Built-in Themes

| Theme           | Description               | Style                          |
| --------------- | ------------------------- | ------------------------------ |
| `default`       | Clean professional theme  | Blue headers, green/red status |
| `corporate`     | Business-focused styling  | Navy blue, brown accents       |
| `minimal`       | Distraction-free design   | Gray headers, subtle borders   |
| `dark`          | Dark mode for eye comfort | Dark backgrounds, light text   |
| `high_contrast` | Accessibility-focused     | Bold colors, large fonts       |

## Budget Templates

| Template      | Description                               | Use Case                       |
| ------------- | ----------------------------------------- | ------------------------------ |
| `50_30_20`    | Classic 50% needs, 30% wants, 20% savings | Beginners, general budgeting   |
| `family`      | Optimized for family of four              | Families with children         |
| `minimalist`  | Lean budget focused on high savings       | Single person, FIRE aspirants  |
| `zero_based`  | Every dollar assigned                     | Detail-oriented, tight budgets |
| `fire`        | 50%+ savings rate                         | Early retirement focus         |
| `high_income` | Balanced lifestyle for $200k+             | High earners                   |

## Project Structure

```
finance-tracker/
├── src/
│   └── finance_tracker/
│       ├── __init__.py           # Package exports
│       ├── ods_generator.py      # ODS file creation
│       ├── budget_analyzer.py    # Pandas-based analysis
│       ├── report_generator.py   # Report generation
│       ├── cli.py                # Command-line interface
│       ├── csv_import.py         # Bank CSV import
│       ├── webdav_upload.py      # Nextcloud WebDAV
│       ├── analytics.py          # Dashboard analytics
│       ├── alerts.py             # Alert system
│       ├── recurring.py          # Recurring expenses
│       ├── templates.py          # Budget templates
│       ├── builder.py            # Fluent builder API (NEW)
│       ├── renderer.py           # Builder -> ODS renderer (NEW)
│       ├── schema/               # Theme schema (NEW)
│       │   ├── styles.py         # Style dataclasses
│       │   ├── loader.py         # YAML loader
│       │   └── validation.py     # Schema validation
│       └── themes/               # Theme YAML files (NEW)
│           ├── default.yaml
│           ├── corporate.yaml
│           ├── minimal.yaml
│           ├── dark.yaml
│           └── high_contrast.yaml
├── tests/                        # Test suite (250+ tests)
├── examples/                     # Usage examples
├── docs/                         # Documentation
├── pyproject.toml               # Project configuration
└── README.md
```

## Nextcloud Integration

### Upload to Nextcloud (CLI)

```bash
# Set credentials
export NEXTCLOUD_URL=https://your-nextcloud.com
export NEXTCLOUD_USER=username
export NEXTCLOUD_PASSWORD=app-password

# Upload
uv run finance-tracker upload budget.ods
```

### Edit with Collabora

1. Open Nextcloud in browser
2. Navigate to the ODS file
3. Click to open in Collabora Office
4. Edit and save - changes sync automatically

### Mobile Editing

1. Install Nextcloud iOS/Android app
2. Connect to your Nextcloud instance
3. Open ODS file - Collabora editor loads
4. Edit expenses on the go

## Development

### Running Tests

```bash
uv run pytest
uv run pytest -v  # Verbose
uv run pytest --cov  # With coverage
```

### Code Quality

```bash
# Linting
uv run ruff check src/ tests/

# Formatting
uv run ruff format src/ tests/

# Type checking
uv run mypy src/
```

## Configuration

### Environment Variables

| Variable             | Description             | Default               |
| -------------------- | ----------------------- | --------------------- |
| `NEXTCLOUD_URL`      | Nextcloud server URL    | (required for upload) |
| `NEXTCLOUD_USER`     | Nextcloud username      | (required for upload) |
| `NEXTCLOUD_PASSWORD` | Nextcloud app password  | (required for upload) |
| `NEXTCLOUD_PATH`     | Remote path for budgets | `/Finance`            |

## Dependencies

### Core

- **odfpy** - ODS file creation and manipulation
- **pandas** - Data analysis
- **pyexcel-ods3** - Reliable ODS reading
- **requests** - WebDAV HTTP client

### Optional

- **pyyaml** - YAML theme loading (install with `[config]` extra)

### Development

- **pytest** - Testing framework
- **ruff** - Linting and formatting
- **mypy** - Type checking

## Security Notes

- Never commit actual financial files to git
- Use `.gitignore` patterns for personal data
- Use Nextcloud app passwords, not main password
- Keep ODS files in encrypted storage when possible

## License

MIT License - See LICENSE file

## Changelog

### v0.4.0 (2025-12-10)

- Added declarative DSL for themes and styling
- Added YAML-based theme definitions (5 built-in themes)
- Added fluent SpreadsheetBuilder API
- Added type-safe FormulaBuilder
- Added OdsRenderer for builder-to-ODS conversion
- Added CLI `--theme` flag for generation commands
- Added CLI `themes` command to list available themes
- Maintained full backward compatibility with v0.3.0
- All 250+ tests passing

### v0.3.0 (2025-12-10)

- Added configuration management
- Added exceptions module
- Performance improvements

### v0.2.0 (2025-12-10)

- Added WebDAV upload to Nextcloud
- Added bank CSV import with auto-detection
- Added transaction auto-categorization
- Added analytics dashboard
- Added configurable alert system
- Added recurring expense management
- Added budget templates (50/30/20, Family, FIRE, etc.)
- Added quick expense CLI command
- Fixed pandas ODS reading issues using pyexcel_ods3
- All 35+ tests passing

### v0.1.0 (2025-12-09)

- Initial release
- ODS budget generation with formulas
- Budget analysis with pandas
- Report generation (text, Markdown, JSON)
- CLI interface
