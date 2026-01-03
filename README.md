# SpreadsheetDL

[![Version](https://img.shields.io/badge/version-4.0.0--alpha.1-blue.svg)](https://github.com/USER/spreadsheet-dl/releases)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-662%20passing-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-97%25-brightgreen.svg)](tests/)
[![MCP](https://img.shields.io/badge/MCP-native%20server-purple.svg)](docs/api/mcp_server.md)

**The Spreadsheet Definition Language for Python**

Define complex spreadsheets in Python or YAML, export to ODS/XLSX/PDF. Built-in domain plugins for finance, science, and engineering. Native MCP server for Claude integration.

---

## Overview

SpreadsheetDL is a universal spreadsheet definition language that lets you create professional spreadsheets programmatically using a declarative, high-level API.

**Key Features:**

- 📝 **Declarative API** - Define structure, formulas, and styling in code (not cell-by-cell imperative)
- 🎨 **Theme System** - 5 built-in themes (default, corporate, minimal, dark, high_contrast)
- 📊 **Chart Builder** - 60+ chart types with fluent API
- ⚡ **Type-Safe Formulas** - FormulaBuilder with circular reference detection
- 🔧 **Domain Plugins** - Pre-built templates for finance, science, engineering (more coming)
- 🌍 **Multi-Format Export** - ODS, XLSX, PDF from single definition
- 🤖 **MCP Server** - Native integration with Claude for AI-powered spreadsheet generation

### Why SpreadsheetDL?

**vs openpyxl/xlsxwriter** (imperative, Excel-only):

- ✅ Declarative (define what, not how)
- ✅ Multi-format (ODS, XLSX, PDF)
- ✅ Domain-aware (finance, science, engineering templates)
- ✅ Theme system (consistent styling)
- ✅ MCP server (AI integration)

**Use Cases Across Domains:**

- 💰 **Finance**: Budgets, financial statements, invoices, expense reports
- 🔬 **Data Science**: Experiment logs, dataset catalogs, analysis reports, A/B test results
- ⚙️ **Electrical Engineering**: BOMs, pin maps, power budgets, signal routing tables
- 🔧 **Mechanical Engineering**: Design calculations, tolerance stack-ups, material specs
- 🏭 **Manufacturing**: OEE dashboards, quality control charts, production schedules
- 🧬 **Biology**: Plate layouts (96/384-well), qPCR results, cell culture tracking
- 📚 **Education**: Gradebooks, attendance, rubrics

## Features

### Core Platform (v4.0.0)

- ✅ **Declarative Builder API** - Define spreadsheets using fluent, chainable methods
- ✅ **Type-Safe Formulas** - FormulaBuilder with 60+ functions, circular reference detection
- ✅ **Theme System** - YAML-based themes (5 built-in: default, corporate, minimal, dark, high_contrast)
- ✅ **Chart Builder** - 60+ chart types (column, bar, line, area, pie, scatter, combo, sparklines)
- ✅ **Multi-Format Export** - ODS (native), XLSX, PDF from single definition
- ✅ **Advanced Formatting** - Conditional formatting, data validation, named ranges, cell merging
- ✅ **Template Engine** - Schema-driven template system with component composition
- ✅ **MCP Server** - Native server with 8 tools (145+ planned), Claude Desktop integration
- ✅ **Streaming I/O** - Handle 100k+ row spreadsheets efficiently
- ✅ **Round-Trip Editing** - Read, modify, and write existing ODS files
- ✅ **CLI & Python API** - Both command-line and programmatic interfaces

### Domain Plugins (Official)

#### 💰 Finance Domain

- **Templates**: Monthly budget, financial statements (income, balance sheet, cash flow, equity), invoices, expense reports
- **Formulas**: NPV, IRR, PMT, PV, FV (financial functions)
- **Importers**: Bank CSV (50+ banks), Plaid API integration
- **Utils**: Account management, budget analytics, alerts, recurring expenses, goals tracking
- **Features**: WebDAV upload (Nextcloud), multi-currency support, auto-categorization

#### 🔬 Data Science Domain (Planned - Phase 1)

- **Templates**: Experiment log, dataset catalog, analysis report, A/B test results, model comparison
- **Formulas**: Statistical tests (TTEST, FTEST, ZTEST), ML metrics (confusion matrix, F1, precision, recall)
- **Importers**: Scientific CSV, MLflow experiment import
- **Utils**: Plotting helpers, statistical utilities

#### ⚙️ Engineering Domain (Planned - Phase 2)

- **Electrical**: BOM, pin mapping, power budget, signal routing
- **Mechanical**: Design calculations, tolerance stack-up, material properties
- **Civil**: Load calculations, construction schedules, cost estimates

#### 🏭 Manufacturing Domain (Planned - Phase 3)

- **Templates**: OEE dashboard, quality control charts (SPC), production schedules
- **Formulas**: OEE, Cpk, DPMO, control limits
- **Importers**: SCADA data connectors

See [Domain Analysis](.coordination/2026-01-03-comprehensive-domain-analysis.md) for full roadmap (12 domains planned).

## Documentation

### User Guides

- **[Getting Started](docs/getting-started.md)** - Installation through first budget
- **[User Guide](docs/user-guide.md)** - Complete user documentation
- **[CLI Reference](docs/cli.md)** - All command-line options
- **[Best Practices](docs/best-practices.md)** - Tips and recommendations

### Tutorials

Learn SpreadsheetDL step-by-step:

1. **[Create a Budget](docs/tutorials/01-create-budget.md)** - Set up your first monthly budget
2. **[Track Expenses](docs/tutorials/02-track-expenses.md)** - Daily expense tracking workflow
3. **[Import Bank Data](docs/tutorials/03-import-bank-data.md)** - Automate from CSV exports
4. **[Create Reports](docs/tutorials/04-create-reports.md)** - Generate comprehensive reports
5. **[Use MCP Tools](docs/tutorials/05-use-mcp-tools.md)** - AI-powered operations with Claude
6. **[Customize Themes](docs/tutorials/06-customize-themes.md)** - Create custom visual themes

### Technical Documentation

- **[Architecture](docs/ARCHITECTURE.md)** - System design and structure
- **[API Reference](docs/api/)** - Complete Python API docs
- **[MCP Integration](docs/MCP_INTEGRATION.md)** - Model Context Protocol setup
- **[Error Codes](docs/error-codes.md)** - Error handling reference

### Examples

Working code examples in the [`examples/`](examples/) directory:

- `example_budget.py` - Create a sample budget programmatically
- `example_import.py` - Import and process bank CSV
- `example_report.py` - Generate custom reports
- `example_chart.py` - Create charts programmatically
- `example_mcp.py` - Use MCP server from Python

## Quick Start

> **New to SpreadsheetDL?** Start with the [Getting Started Guide](docs/getting-started.md) for a beginner-friendly introduction!

### Installation

```bash
# Install from GitHub (PyPI coming soon)
pip install git+https://github.com/USER/spreadsheet-dl.git

# Or clone for development
git clone https://github.com/USER/spreadsheet-dl.git
cd spreadsheet-dl
uv sync --dev

# Install with specific domain plugins (when available)
pip install spreadsheet-dl[finance]         # Finance domain only
pip install spreadsheet-dl[science]         # Data science domain
pip install spreadsheet-dl[all]             # All official domains
```

**Next Steps:**

- 📖 **[Getting Started Guide](docs/getting-started.md)** - Your first budget in 5 minutes
- 🎓 **[Tutorials](docs/tutorials/)** - Step-by-step learning path
- 📚 **[Best Practices](docs/best-practices.md)** - Tips for effective use

### Quick Example (Universal Builder API)

```python
from spreadsheet_dl import create_spreadsheet, formula

# Create a simple spreadsheet
builder = create_spreadsheet(theme="default")

# Add a data sheet
builder.sheet("Sales Data") \
    .column("Month", width="3cm", type="text") \
    .column("Revenue", width="3cm", type="currency") \
    .column("Expenses", width="3cm", type="currency") \
    .column("Profit", width="3cm", type="currency") \
    .header_row(style="header_primary") \
    .row().cell("January").cell(15000).cell(8000).cell(formula=formula().subtract("B2", "C2")) \
    .row().cell("February").cell(18000).cell(9500).cell(formula=formula().subtract("B3", "C3")) \
    .row().cell("March").cell(22000).cell(11000).cell(formula=formula().subtract("B4", "C4"))

# Save to multiple formats
builder.save("sales_report.ods")     # Native ODS
builder.export("sales_report.xlsx")  # Excel format
builder.export("sales_report.pdf")   # PDF for distribution
```

### Finance Domain Example (CLI)

```bash
# Create a budget (with optional template and theme)
uv run spreadsheet-dl generate -o ./budgets/
uv run spreadsheet-dl generate -o ./budgets/ -t 50_30_20
uv run spreadsheet-dl generate -o ./budgets/ --theme corporate
uv run spreadsheet-dl generate -o ./budgets/ -t family --theme minimal

# List available themes
uv run spreadsheet-dl themes
uv run spreadsheet-dl themes --json

# Analyze a budget
uv run spreadsheet-dl analyze budget.ods
uv run spreadsheet-dl analyze budget.ods --json

# Generate reports
uv run spreadsheet-dl report budget.ods -f text
uv run spreadsheet-dl report budget.ods -f markdown -o report.md

# View analytics dashboard
uv run spreadsheet-dl dashboard budget.ods
uv run spreadsheet-dl dashboard budget.ods --json

# Check budget alerts
uv run spreadsheet-dl alerts budget.ods
uv run spreadsheet-dl alerts budget.ods --critical-only

# Import bank CSV
uv run spreadsheet-dl import transactions.csv --bank chase
uv run spreadsheet-dl import transactions.csv --preview
uv run spreadsheet-dl import transactions.csv --theme default

# Quick expense entry
uv run spreadsheet-dl expense 25.50 "Lunch at Chipotle"
uv run spreadsheet-dl expense 150 "Whole Foods" -c Groceries

# Upload to Nextcloud
uv run spreadsheet-dl upload budget.ods

# List available templates
uv run spreadsheet-dl templates
```

## Python API

### Basic Usage

```python
from decimal import Decimal
from datetime import date
from spreadsheet_dl import (
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

### Using Themes

```python
from spreadsheet_dl import OdsGenerator, create_monthly_budget

# Create budget with a theme
generator = OdsGenerator(theme="corporate")
generator.create_budget_spreadsheet("corporate_budget.ods")

# Or use convenience function
path = create_monthly_budget("./budgets", theme="minimal")
```

### Fluent Builder API

```python
from decimal import Decimal
from spreadsheet_dl import create_spreadsheet, formula

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
from spreadsheet_dl import formula

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
from spreadsheet_dl import get_template, OdsGenerator

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
from spreadsheet_dl import import_bank_csv, OdsGenerator

# Import from CSV (auto-detects bank format)
expenses = import_bank_csv("bank_export.csv", bank="auto")

# Create budget with imported expenses
generator = OdsGenerator()
generator.create_budget_spreadsheet("imported.ods", expenses=expenses)
```

### Analytics Dashboard

```python
from spreadsheet_dl import generate_dashboard

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
from spreadsheet_dl import check_budget_alerts, AlertConfig

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
from spreadsheet_dl import RecurringExpenseManager, RecurringExpense, RecurrenceFrequency
from spreadsheet_dl.recurring import create_common_recurring

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
from spreadsheet_dl import upload_budget, NextcloudConfig

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
spreadsheet-dl/
├── src/
│   └── spreadsheet_dl/
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
│       ├── builder.py            # Fluent builder API
│       ├── renderer.py           # Builder -> ODS renderer
│       ├── schema/               # Theme schema
│       │   ├── styles.py         # Style dataclasses
│       │   ├── loader.py         # YAML loader
│       │   └── validation.py     # Schema validation
│       └── themes/               # Theme YAML files
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
uv run spreadsheet-dl upload budget.ods
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

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup and workflow
- Coding standards and style guide
- Testing requirements
- Commit message format (conventional commits)
- **Branding guidelines** - See [BRANDING.md](BRANDING.md) for official naming, terminology, and brand voice

## License

MIT License - See LICENSE file

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

### Recent Releases

- **v4.0.0-alpha.1** (2026-01-03) - Universal spreadsheet definition language with MCP server, streaming I/O, 97% test coverage
- **v2.0.0** (2025-12-29) - Professional spreadsheet system with enterprise formatting
- **v0.4.1** (2025-12-15) - Expense append functionality and comprehensive error codes
- **v0.4.0** (2025-12-10) - Declarative DSL with themes and fluent builder API
