# SpreadsheetDL

[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](https://github.com/lair-click-bats/spreadsheet-dl/releases)
[![First Release](https://img.shields.io/badge/🎉-first%20public%20release-gold.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-high-brightgreen.svg)](tests/)
[![MCP](https://img.shields.io/badge/MCP-server-purple.svg)](docs/api/mcp_server.md)

> **🎉 First Public Release (v4.0.0)** - Production-ready with comprehensive testing, complete documentation, and extensive domain plugin library.

**The Spreadsheet Definition Language for Python**

Define complex spreadsheets in Python or YAML, export to ODS/XLSX/PDF. Built-in domain plugins for science, engineering, and data analysis. Native MCP server for Claude integration.

---

## Overview

SpreadsheetDL is a universal spreadsheet definition language that lets you create professional spreadsheets programmatically using a declarative, high-level API.

**Key Features:**

- 📝 **Declarative API** - Define structure, formulas, and styling in code (not cell-by-cell imperative)
- 🎨 **Theme System** - 5 built-in themes (default, corporate, minimal, dark, high_contrast)
- 📊 **Chart Builder** - Extensive chart types with fluent API
- ⚡ **Type-Safe Formulas** - FormulaBuilder with circular reference detection
- 🔧 **Domain Plugins** - Specialized formulas and importers for science, engineering, data analysis
- 🌍 **Multi-Format Export** - ODS, XLSX, PDF from single definition
- 🤖 **MCP Server** - Native integration with Claude for AI-powered spreadsheet generation

### Why SpreadsheetDL?

**vs openpyxl/xlsxwriter** (imperative, Excel-only):

- ✅ Declarative (define what, not how)
- ✅ Multi-format (ODS, XLSX, PDF)
- ✅ Domain-aware (science, engineering, data analysis formulas)
- ✅ Theme system (consistent styling)
- ✅ MCP server (AI integration)

**Use Cases Across Domains:**

- ⚛️ **Physics**: Mechanics, electromagnetism, optics, quantum mechanics calculations
- 🔬 **Data Science**: Experiment logs, dataset catalogs, analysis reports, A/B test results, ML metrics
- ⚙️ **Electrical Engineering**: BOMs, pin maps, power budgets, signal routing tables, digital circuits, filter design
- 🔧 **Mechanical Engineering**: Design calculations, tolerance stack-ups, material specs, fluid dynamics, thermal analysis
- 🧪 **Chemistry**: Thermodynamics calculations, solution chemistry, reaction kinetics, equilibrium constants
- 🧬 **Biology**: Plate layouts (96/384-well), qPCR results, cell culture tracking, pharmacokinetics, genetics
- 🏗️ **Civil Engineering**: Structural analysis, foundation design, transportation planning
- 🌍 **Environmental**: Climate modeling, renewable energy analysis, air/water quality monitoring
- 🏭 **Manufacturing**: OEE dashboards, quality control charts, production schedules, lean metrics, six sigma analysis
- 📚 **Education**: Gradebooks, attendance, rubrics, assessment analytics, learning metrics
- 💰 **Finance**: Budgets, financial statements, invoices, expense reports, risk analysis, options pricing

## Philosophy: Universal Tools, Not Templates

SpreadsheetDL is built on a fundamental principle: **provide universal building blocks, not rigid templates**.

### What You Get

**Composable primitives** that work for ANY use case:

- **Formulas**: Comprehensive domain-specific formula library (physics, data science, electrical/mechanical/civil engineering, chemistry, biology, environmental, manufacturing, education, finance)
- **Styles**: Theme system with unlimited customization
- **Formats**: ODS, XLSX, PDF from single definition
- **Charts**: Extensive chart types with fluent builder API
- **Data validation**: Rules, conditional formatting, named ranges

These primitives combine in infinite ways. You're not locked into pre-built templates.

### What You Don't Get

We deliberately **don't** provide:

- ❌ Rigid pre-built templates ("budget template", "invoice template")
- ❌ One-size-fits-all layouts
- ❌ Opinionated business logic
- ❌ Template configuration hell

### Why This Matters

**Templates** are brittle. They assume your budget has exactly these categories, your invoice has exactly these fields, your gradebook uses exactly this grading scale.

**Tools** are flexible. Want a budget? Use `OdsGenerator`, add your categories, apply formulas, style with themes. Want an invoice? Same tools, different structure. Want a custom manufacturing dashboard? Same tools, manufacturing domain formulas.

### Declarative Over Imperative

You define **what** you want, not **how** to build it:

```python
# NOT: "Set cell A1 to 'Data', make it bold, set font size 14..."
# YES: "Create spreadsheet with structure and theme"
builder.sheet("Data") \
    .column("Name", width="3cm") \
    .column("Value", width="3cm") \
    .header_row() \
    .theme("corporate")
```

### Extensibility

Don't see your domain? **Create a plugin**. SpreadsheetDL's plugin architecture lets you extend formulas, importers, and utilities without forking the codebase.

All official domain plugins started as custom plugins. Yours can too.

## Features

### Core Platform (v4.0.0)

- ✅ **Declarative Builder API** - Define spreadsheets using fluent, chainable methods
- ✅ **Type-Safe Formulas** - FormulaBuilder with extensive functions, circular reference detection
- ✅ **Theme System** - YAML-based themes (5 built-in: default, corporate, minimal, dark, high_contrast)
- ✅ **Chart Builder** - Comprehensive chart types (column, bar, line, area, pie, scatter, combo, sparklines)
- ✅ **Multi-Format Export** - ODS (native), XLSX, PDF from single definition
- ✅ **Advanced Formatting** - Conditional formatting, data validation, named ranges, cell merging
- ✅ **Template Engine** - Schema-driven template system with component composition
- ✅ **MCP Server** - Native server with tools for spreadsheet and budget operations, Claude Desktop integration
- ✅ **Streaming I/O** - Handle large spreadsheets efficiently
- ✅ **Round-Trip Editing** - Read, modify, and write existing ODS files
- ✅ **CLI & Python API** - Both command-line and programmatic interfaces

### Domain Plugins (Official)

#### ⚛️ Physics Domain

- **Formulas**: Mechanics (kinematics, dynamics, energy), electromagnetism (Coulomb, Lorentz, circuits), optics (thin lens, diffraction), quantum mechanics (wave functions, uncertainty)
- **Importers**: Experimental data, sensor readings
- **Utils**: Unit conversions, physical constants

#### 🔬 Data Science Domain

- **Formulas**: Statistical tests (TTEST, FTEST, ZTEST), ML metrics (confusion matrix, F1, precision, recall, AUC-ROC), time series analysis, clustering metrics
- **Importers**: Scientific CSV, MLflow experiment import, Jupyter notebook
- **Utils**: Plotting helpers, statistical utilities, feature engineering

#### ⚙️ Engineering Domains

- **Electrical**: Pin mapping, power budgets, digital circuits, filter design, signal processing
- **Mechanical**: Stress analysis, tolerance calculations, fluid mechanics, thermal analysis, material properties
- **Civil**: Load calculations, structural analysis, concrete mix, foundation design, transportation planning
- **Environmental**: Climate modeling, renewable energy metrics, air/water quality, carbon footprint

#### 🧪 Chemistry Domain

- **Formulas**: Thermodynamics (enthalpy, entropy, Gibbs free energy), solution chemistry (molarity, dilution, pH), reaction kinetics (rate laws, Arrhenius equation)
- **Importers**: Spectroscopy data, lab results
- **Utils**: Unit conversions, chemical calculations

#### 🧬 Biology Domain

- **Formulas**: Pharmacokinetics (half-life, clearance, AUC), genetics (Hardy-Weinberg, linkage, allele frequency)
- **Importers**: Plate readers, qPCR data, cell culture tracking
- **Utils**: Plate layout generators, concentration calculators

#### 🏭 Manufacturing Domain

- **Formulas**: Lean metrics (CycleTime, TaktTime, Throughput), Six Sigma (ProcessCapability, ControlLimits, DefectRate), Supply Chain (EOQ, ReorderPoint, SafetyStock)
- **Importers**: MES Data, ERP Data, Sensor Data
- **Utils**: OEE calculators, quality metrics, inventory optimization

#### 📚 Education Domain

- **Formulas**: Assessment theory (KR20, KR21, Cronbach's alpha), grading (curves, GPA, percentiles), learning analytics (mastery, forgetting curves)
- **Importers**: LMS data, gradebook exports, assessment results
- **Utils**: Grade calculators, attendance tracking, rubric scoring

#### 💰 Finance Domain

- **Formulas**: Financial functions (NPV, IRR, PMT, PV, FV), bond pricing, options pricing (Black-Scholes), risk metrics (VaR, Sharpe ratio, beta)
- **Importers**: Bank CSV (major banks), Plaid API integration
- **Utils**: Account management, budget analytics, alerts, recurring expenses, goals tracking
- **Features**: WebDAV upload (Nextcloud), multi-currency support, auto-categorization

## Documentation

### User Guides

- **[Getting Started](docs/getting-started.md)** - Installation and quick start
- **[User Guide](docs/user-guide.md)** - Complete user documentation
- **[CLI Reference](docs/cli.md)** - All command-line options
- **[Best Practices](docs/guides/best-practices.md)** - Tips and recommendations

### Tutorials

Learn SpreadsheetDL step-by-step with the beginner tutorial series:

1. **[Getting Started](docs/tutorials/01-create-budget.md)** - Build your first spreadsheet
2. **[Working with Data](docs/tutorials/02-track-expenses.md)** - Load and organize data
3. **[Domain Plugins](docs/tutorials/03-import-bank-data.md)** - Use specialized formulas
4. **[Generate Reports](docs/tutorials/04-create-reports.md)** - Create comprehensive reports
5. **[MCP Integration](docs/tutorials/05-use-mcp-tools.md)** - AI-powered operations with Claude
6. **[Custom Themes](docs/tutorials/06-customize-themes.md)** - Design custom visual themes

### Technical Documentation

- **[Architecture](docs/ARCHITECTURE.md)** - System design and structure
- **[API Reference](docs/api/)** - Complete Python API docs
- **[MCP Integration](docs/MCP_INTEGRATION.md)** - Model Context Protocol setup
- **[Error Codes](docs/error-codes.md)** - Error handling reference

### Examples

Working code examples in the [`examples/`](examples/) directory:

- `example_basic.py` - Create structured spreadsheets programmatically
- `example_import.py` - Import and process CSV/external data
- `example_report.py` - Generate reports from spreadsheet data
- `example_chart.py` - Build charts with fluent API
- `example_mcp.py` - Integrate with MCP server from Python

## Known Limitations

### ODS Format Advanced Features

Some advanced conditional formatting features are not yet implemented for ODS export:

- Color scale conditional formatting
- Data bar conditional formatting
- Icon set conditional formatting
- Advanced cell value rules

These features will raise `NotImplementedError` with clear error messages. They are planned for future releases and work correctly in XLSX export.

### MCP Server Tools

The MCP server provides tools for spreadsheet operations across all domains. See [MCP Integration](docs/MCP_INTEGRATION.md) for detailed documentation.

## Quick Start

> **New to SpreadsheetDL?** Start with the [Getting Started Guide](docs/getting-started.md) for a beginner-friendly introduction!

### Installation

```bash
# Install from GitHub (PyPI coming soon)
pip install git+https://github.com/lair-click-bats/spreadsheet-dl.git

# Or clone for development
git clone https://github.com/lair-click-bats/spreadsheet-dl.git
cd spreadsheet-dl
uv sync --dev

# Install with specific domain plugins (when available)
pip install spreadsheet-dl[finance]         # Finance domain only
pip install spreadsheet-dl[science]         # Data science domain
pip install spreadsheet-dl[all]             # All official domains
```

**Next Steps:**

- 📖 **[Getting Started Guide](docs/getting-started.md)** - Your first spreadsheet in 5 minutes
- 🎓 **[Tutorials](docs/tutorials/)** - Step-by-step learning path
- 📚 **[Best Practices](docs/guides/best-practices.md)** - Tips for effective use

### Quick Example (Universal Builder API)

```python
from spreadsheet_dl import create_spreadsheet, formula

# Create experiment data spreadsheet
builder = create_spreadsheet(theme="default")

# Add data sheet with formulas
builder.sheet("Experiment Results") \
    .column("Trial", width="2cm", type="integer") \
    .column("Voltage (V)", width="3cm", type="number") \
    .column("Current (A)", width="3cm", type="number") \
    .column("Power (W)", width="3cm", type="number") \
    .column("Efficiency (%)", width="3cm", type="percent") \
    .header_row(style="header_primary") \
    .row().cell(1).cell(5.0).cell(0.5).cell(formula=formula().multiply("B2", "C2")).cell(formula=formula().divide("D2", "E2")) \
    .row().cell(2).cell(10.0).cell(1.0).cell(formula=formula().multiply("B3", "C3")).cell(formula=formula().divide("D3", "E3")) \
    .row().cell(3).cell(15.0).cell(1.5).cell(formula=formula().multiply("B4", "C4")).cell(formula=formula().divide("D4", "E4"))

# Save to multiple formats
builder.save("experiment_data.ods")    # Native ODS
builder.export("experiment_data.xlsx") # Excel format
builder.export("experiment_data.pdf")  # PDF for distribution
```

### CLI Examples

```bash
# List available themes
uv run spreadsheet-dl themes
uv run spreadsheet-dl themes --json

# Generate spreadsheet with theme
uv run spreadsheet-dl generate -o ./output/ --theme corporate
uv run spreadsheet-dl generate -o ./output/ --theme minimal

# Generate reports
uv run spreadsheet-dl report data.ods -f text
uv run spreadsheet-dl report data.ods -f markdown -o report.md

# Upload to Nextcloud
uv run spreadsheet-dl upload data.ods
```

**Finance Domain Commands:**

```bash
# Budget-specific operations
uv run spreadsheet-dl analyze budget.ods --json
uv run spreadsheet-dl dashboard budget.ods
uv run spreadsheet-dl alerts budget.ods --critical-only
uv run spreadsheet-dl import transactions.csv --bank chase
uv run spreadsheet-dl expense 25.50 "Description" -c Category
```

## Python API

### Universal Builder API (All Domains)

Create spreadsheets for any domain using the fluent builder API:

```python
from spreadsheet_dl import create_spreadsheet, formula

# Build spreadsheet with fluent API
builder = create_spreadsheet(theme="default")

# Create data sheet
builder.sheet("Experiment Data") \
    .column("Trial", width="2cm", type="integer") \
    .column("Temperature (K)", width="3cm", type="number") \
    .column("Pressure (Pa)", width="3cm", type="number") \
    .column("Volume (m³)", width="3cm", type="number") \
    .header_row(style="header_primary") \
    .data_rows(50)

# Create analysis sheet with formulas
f = formula()
builder.sheet("Analysis") \
    .column("Metric", width="4cm") \
    .column("Value", width="3cm", type="number") \
    .header_row() \
    .row() \
        .cell("Mean Temperature") \
        .cell(formula=f.average(f.sheet("Experiment Data").range("B2", "B51"))) \
    .row() \
        .cell("Std Dev Pressure") \
        .cell(formula=f.stdev(f.sheet("Experiment Data").range("C2", "C51")))

# Save to multiple formats
builder.save("experiment.ods")
builder.export("experiment.xlsx")
builder.export("experiment.pdf")
```

### FormulaBuilder API

```python
from spreadsheet_dl import formula

f = formula()

# SUM formula
f.sum(f.range("A2", "A100"))
# -> "of:=SUM([.A2:A100])"

# Cross-sheet references
f.sumif(
    f.sheet("Data").col("B"),
    f.cell("A2"),
    f.sheet("Data").col("D"),
)
# -> "of:=SUMIF(['Data'.$B:$B];[.A2];['Data'.$D:$D])"

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

### Domain-Specific APIs

SpreadsheetDL provides specialized APIs for each domain plugin. Examples below show the Finance domain, which has the most extensive API surface.

## Finance Domain API

The Finance domain includes comprehensive budget management, transaction tracking, and analysis tools:

### Basic Budget Operations

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

### Budget Themes

```python
from spreadsheet_dl import OdsGenerator, create_monthly_budget

# Create budget with a theme
generator = OdsGenerator(theme="corporate")
generator.create_budget_spreadsheet("corporate_budget.ods")

# Or use convenience function
path = create_monthly_budget("./budgets", theme="minimal")
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

## Project Structure

```
spreadsheet-dl/
├── docs/                        # Complete documentation
├── examples/                    # Usage examples
├── src/
│   └── spreadsheet_dl/
│       ├── _builder/            # Builder implementation
│       │   ├── core.py          # SheetBuilder, RowBuilder
│       │   ├── formulas.py      # FormulaBuilder
│       │   ├── models.py        # Data models
│       │   └── references.py    # Cell reference handling
│       ├── _cli/                # CLI implementation
│       │   ├── app.py           # Click application
│       │   └── commands.py      # CLI commands
│       ├── _mcp/                # MCP server
│       │   └── server.py        # MCP tools
│       ├── domains/             # Domain plugins
│       │   ├── biology/         # Biology formulas, plate readers
│       │   ├── chemistry/       # Chemistry formulas, lab data
│       │   ├── civil_engineering/       # Civil engineering formulas
│       │   ├── data_science/    # Statistical formulas, ML metrics
│       │   ├── education/       # Education formulas, LMS importers
│       │   ├── electrical_engineering/  # Electrical engineering formulas
│       │   ├── environmental/   # Environmental formulas
│       │   ├── finance/         # Financial formulas, importers
│       │   ├── manufacturing/   # Manufacturing formulas, MES importers
│       │   ├── mechanical_engineering/  # Mechanical engineering formulas
│       │   └── physics/         # Physics formulas, experimental data
│       ├── schema/              # Theme schema
│       │   ├── loader.py        # YAML loader
│       │   ├── styles.py        # Style dataclasses
│       │   └── validation.py    # Schema validation
│       ├── template_engine/     # Template engine
│       │   ├── renderer.py      # Template renderer
│       │   └── schema.py        # Template schema
│       ├── themes/              # Theme YAML files (5 built-in)
│       ├── __init__.py          # Package exports
│       ├── adapters.py          # Multi-format adapters (ODS/XLSX/CSV/HTML)
│       ├── builder.py           # Fluent builder API entry point
│       ├── charts.py            # Chart builder
│       ├── exceptions.py        # Exception hierarchy
│       ├── export.py            # Multi-format export
│       ├── plugins.py           # Plugin system framework
│       ├── renderer.py          # Builder -> ODS renderer
│       ├── security.py          # Encryption (AES-256-GCM)
│       └── streaming.py         # Streaming I/O for large files
├── tests/                       # Comprehensive test suite
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

- **v4.0.0** (2026-01-04) - First public release: Universal spreadsheet definition language with MCP server and comprehensive domain plugin library
- **v2.0.0** (2025-12-29) - Professional spreadsheet system with enterprise formatting
- **v0.4.1** (2025-12-15) - Expense append functionality and comprehensive error codes
- **v0.4.0** (2025-12-10) - Declarative DSL with themes and fluent builder API
