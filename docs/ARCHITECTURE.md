# Architecture Overview

## Version 2.0.0 - Professional Spreadsheet System

This document describes the architecture of SpreadsheetDL v2.0.0, a comprehensive
professional spreadsheet system with enterprise-grade formatting capabilities.

## Project Structure

```
spreadsheet-dl/
├── src/
│   └── spreadsheet_dl/          # Main package
│       ├── __init__.py           # Package exports (250+ symbols)
│       ├── ods_generator.py      # ODS file creation
│       ├── budget_analyzer.py    # Pandas-based analysis
│       ├── report_generator.py   # Report generation
│       ├── cli.py                # Command-line interface
│       │
│       # v2.0.0 Professional Features
│       ├── charts.py             # Chart builder (FR-CHART-*)
│       ├── template_engine.py    # Template system (FR-TEMPLATE-*)
│       ├── builder.py            # Fluent builder API (FR-BUILDER-*)
│       ├── renderer.py           # ODS rendering engine
│       │
│       # Schema Extensions
│       ├── schema/
│       │   ├── typography.py     # Typography and fonts
│       │   ├── print_layout.py   # Print layout settings
│       │   ├── advanced.py       # Named ranges, comments, filters
│       │   ├── conditional.py    # Conditional formatting
│       │   ├── data_validation.py # Data validation rules
│       │   └── units.py          # Length/unit handling
│       │
│       # Professional Templates
│       ├── templates/
│       │   ├── professional.py   # Business templates
│       │   └── financial_statements.py # Financial report templates
│       │
│       # Integration Modules
│       ├── mcp_server.py         # MCP server for AI integration
│       ├── interactive.py        # Interactive ODS features
│       ├── security.py           # Encryption and credentials
│       ├── plaid_integration.py  # Bank API integration
│       │
│       # Export and Analysis
│       ├── export.py             # Multi-format export
│       ├── ai_export.py          # AI-friendly export
│       ├── ai_training.py        # Training data export
│       └── visualization.py      # Chart.js dashboards
│
├── tests/                        # Comprehensive test suite
├── examples/                     # Usage examples
├── templates/                    # YAML theme templates
└── docs/                         # Documentation
```

## Core Components

### 1. Template Engine System (NEW in v2.0.0)

The template engine provides declarative spreadsheet creation using YAML schemas.

**Key Classes:**

- `TemplateLoader` - Loads and validates YAML templates
- `TemplateRenderer` - Renders templates to ODS format
- `ComponentDefinition` - Reusable template components
- `TemplateVariable` - Dynamic variable handling

**Features:**

- YAML-based template definitions
- Variable interpolation
- Component reuse and inheritance
- Conditional sections
- Loop constructs for data arrays

### 2. Chart Builder (NEW in v2.0.0)

Comprehensive chart creation with all major chart types.

**Key Classes:**

- `ChartBuilder` - Fluent API for chart construction
- `ChartSpec` - Chart specification container
- `DataSeries` - Chart data series
- `SparklineBuilder` - Inline sparkline charts

**Supported Chart Types:**

- Column and Bar charts
- Line and Area charts
- Pie and Donut charts
- Scatter plots
- Combo charts (dual axis)
- Sparklines (line, bar, column)

**Chart Configuration:**

- `AxisConfig` - Axis formatting
- `LegendConfig` - Legend positioning
- `DataLabelConfig` - Data labels
- `Trendline` - Trend lines and projections

### 3. Professional Templates (NEW in v2.0.0)

Enterprise-ready document templates.

**Business Templates:**

- `EnterpriseBudgetTemplate` - Multi-department budgets
- `CashFlowTrackerTemplate` - Cash flow management
- `InvoiceTemplate` - Professional invoices
- `ExpenseReportTemplate` - Expense tracking

**Financial Statement Templates:**

- `IncomeStatementTemplate` - P&L statements
- `BalanceSheetTemplate` - Balance sheets
- `CashFlowStatementTemplate` - Statement of cash flows
- `EquityStatementTemplate` - Equity changes

### 4. Interactive ODS Features (NEW in v1.0.0)

Enhanced interactivity within ODS spreadsheets.

**Key Classes:**

- `InteractiveOdsBuilder` - Add interactive elements
- `DropdownList` - Cell dropdowns
- `ValidationRule` - Data validation
- `ConditionalFormat` - Conditional formatting
- `DashboardKPI` - KPI widgets

**Features:**

- Data validation with error messages
- Dropdown lists for categories
- Conditional formatting rules
- Dashboard views with KPIs
- Sparklines for trends

### 5. MCP Server Integration (NEW in v1.0.0)

Native Model Context Protocol server for AI integration.

**Key Classes:**

- `MCPServer` - Server implementation
- `MCPConfig` - Server configuration
- `MCPTool` - Tool definitions
- `MCPToolResult` - Tool results

**Capabilities:**

- Natural language budget queries
- Automated report generation
- Expense categorization
- Trend analysis

### 6. Security Module

Data protection and credential management.

**Key Classes:**

- `FileEncryptor` - AES-256-GCM encryption
- `CredentialStore` - Secure credential storage
- `SecurityAuditLog` - Audit logging

**Features:**

- AES-256 encryption at rest
- PBKDF2-SHA256 key derivation
- Secure password generation
- Audit trail logging

### 7. Print Layout System (NEW in v2.0.0)

Professional print output configuration.

**Key Classes:**

- `PageSetup` - Page configuration
- `PageSetupBuilder` - Fluent setup API
- `HeaderFooter` - Headers and footers
- `PrintPresets` - Common print configurations

**Features:**

- Page size and orientation
- Margins and scaling
- Headers/footers with variables
- Page breaks
- Repeat rows/columns

### 8. Schema Extensions (NEW in v2.0.0)

Enhanced data types and structures.

**Advanced Features (`schema/advanced.py`):**

- `NamedRange` - Named cell ranges
- `CellComment` - Cell annotations
- `AutoFilter` - Data filtering
- `Hyperlink` - Clickable links
- `Image` - Embedded images

**Typography (`schema/typography.py`):**

- `Typography` - Font settings
- `FontPairing` - Font combinations

**Units (`schema/units.py`):**

- `Length` - Measurement values
- `LengthUnit` - Unit types (pt, cm, in, etc.)

### 9. ODS Generator (`ods_generator.py`)

Creates ODS spreadsheets using the `odfpy` library.

**Key Classes:**

- `OdsGenerator` - Main generator class
- `ExpenseCategory` - Enum of spending categories
- `ExpenseEntry` - Data class for expense records
- `BudgetAllocation` - Data class for budget amounts

**Features:**

- Creates multi-sheet workbooks (Expense Log, Budget, Summary)
- Formula support (SUM, SUMIF, VLOOKUP)
- Cell styling and formatting
- Conditional formatting for over-budget alerts
- Mobile-friendly structure (works in Collabora Office)

### 10. Budget Analyzer (`budget_analyzer.py`)

Analyzes budget data using pandas with ODF engine.

**Key Classes:**

- `BudgetAnalyzer` - Main analyzer class
- `BudgetSummary` - Analysis results container
- `CategorySpending` - Per-category breakdown
- `SpendingTrend` - Time-series data

**Features:**

- Load expenses and budgets from ODS files
- Calculate totals and percentages
- Filter by category or date range
- Generate alerts for budget overruns
- Export analysis as JSON

### 11. Report Generator (`report_generator.py`)

Creates formatted reports from analysis data.

**Key Classes:**

- `ReportGenerator` - Main report class
- `ReportConfig` - Configuration options

**Output Formats:**

- Plain text (console-friendly)
- Markdown (documentation/sharing)
- JSON (visualization data)

## Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           INPUT SOURCES                                  │
├─────────────────┬─────────────────┬─────────────────┬──────────────────┤
│  YAML Templates │   Bank CSVs     │   Plaid API     │  Manual Entry    │
│  (templates/)   │   (csv_import)  │ (plaid_int...)  │  (CLI/ODS)       │
└────────┬────────┴────────┬────────┴────────┬────────┴─────────┬────────┘
         │                 │                 │                  │
         v                 v                 v                  v
┌─────────────────────────────────────────────────────────────────────────┐
│                        PROCESSING LAYER                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  Template Engine ──> Builder API ──> Renderer ──> ODS Generator         │
│                                                                          │
│  Budget Analyzer <── Analysis Engine <── Data Validation                │
└─────────────────────────────────────────────────────────────────────────┘
         │                                                     │
         v                                                     v
┌─────────────────────────────────────────────────────────────────────────┐
│                        OUTPUT FORMATS                                    │
├─────────────────┬─────────────────┬─────────────────┬──────────────────┤
│   ODS Files     │   Excel XLSX    │   PDF Reports   │  AI/JSON Export  │
│   (odfpy)       │   (openpyxl)    │   (reportlab)   │  (semantic)      │
└────────┬────────┴────────┬────────┴────────┬────────┴─────────┬────────┘
         │                 │                 │                  │
         v                 v                 v                  v
┌─────────────────────────────────────────────────────────────────────────┐
│                        INTEGRATION LAYER                                 │
├─────────────────┬─────────────────┬─────────────────┬──────────────────┤
│   Nextcloud     │   MCP Server    │   Visualization │  Notifications   │
│   (WebDAV)      │   (AI/Claude)   │   (Chart.js)    │  (email/ntfy)    │
└─────────────────┴─────────────────┴─────────────────┴──────────────────┘
```

## Integration Points

### Nextcloud + Collabora

ODS files designed for seamless Collabora Office editing:

1. Generate ODS file locally via CLI or API
2. Upload to Nextcloud (WebDAV or manual)
3. Edit in browser (Collabora) or mobile apps
4. Sync and analyze locally

### MCP Server Integration

Native MCP server for Claude Code integration:

```json
{
  "mcpServers": {
    "spreadsheet-dl": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "spreadsheet-dl-mcp"],
      "env": {
        "FINANCE_DATA_DIR": "~/Documents/Finance"
      }
    }
  }
}
```

**Available Tools:**

- `analyze_budget` - Analyze budget files
- `create_budget` - Generate new budgets
- `import_transactions` - Import bank data
- `generate_report` - Create reports
- `query_spending` - Natural language queries

### Plaid Bank Integration

Automatic transaction import from banks:

```python
from spreadsheet_dl import PlaidClient, PlaidSyncManager

client = PlaidClient(config)
sync_manager = PlaidSyncManager(client)
result = sync_manager.sync_all_accounts()
```

## Technology Stack

### Core Dependencies

| Library  | Purpose           | Version |
| -------- | ----------------- | ------- |
| odfpy    | ODS file creation | ^1.4.1  |
| pandas   | Data analysis     | ^2.0.0  |
| pyyaml   | Configuration     | ^6.0    |
| typer    | CLI framework     | ^0.9.0  |
| requests | HTTP client       | ^2.31.0 |

### Optional Dependencies

| Library      | Purpose             | Install      |
| ------------ | ------------------- | ------------ |
| openpyxl     | Excel export        | `[xlsx]`     |
| reportlab    | PDF export          | `[pdf]`      |
| plaid-python | Bank integration    | `[plaid]`    |
| cryptography | Enhanced encryption | `[security]` |

### Development Dependencies

```bash
uv add --dev ruff mypy pytest pytest-cov
```

## Technology Choices

### Why ODS (not Excel)?

- Native format for Collabora Office
- No conversion needed in Nextcloud stack
- Open Document Format (ISO standard)
- Works on all platforms

### Why odfpy?

- Full ODS feature support
- Formula creation and preservation
- Style and formatting control
- Active maintenance
- Python native

### Why pandas?

- Powerful data analysis
- Built-in ODF engine support
- Familiar API for data manipulation
- Statistical functions

## Security Architecture

### Encryption

- **Algorithm**: AES-256-GCM (authenticated encryption)
- **Key Derivation**: PBKDF2-SHA256 (600K iterations)
- **Salt**: 256-bit random
- **Nonce**: 96-bit random per encryption

### Credential Storage

```
~/.config/spreadsheet-dl/
├── credentials.enc    # Encrypted credential store
├── security_audit.log # Audit trail
└── config.yaml        # Application config (no secrets)
```

### Audit Logging

All security operations logged:

- Encryption/decryption events
- Credential access
- Authentication attempts
- File access patterns

### Security Considerations

1. **Local Processing**: All analysis runs locally
2. **No Cloud Dependencies**: Works offline
3. **File-Based**: No database or network requirements
4. **Minimal Permissions**: Only needs file read/write access

For sensitive financial data:

- Keep ODS files in encrypted storage
- Use Nextcloud's encryption features
- Restrict MCP server file access paths

## Performance Considerations

### Large Files

- Streaming ODS parsing for memory efficiency
- Chunked export for large datasets
- Lazy loading of analysis data

### Caching

- Template compilation cached
- Exchange rates cached (24h)
- Parsed ODS data cached per session

### Optimization Tips

1. Use `active_sheet_only=True` for single-sheet analysis
2. Limit date ranges for large expense logs
3. Use JSON export for programmatic processing
4. Enable gzip compression for backups

## Extension Points

### Custom Templates

Create custom YAML templates in `templates/`:

```yaml
name: my_custom_template
version: '1.0'
sheets:
  - name: Data
    columns:
      - name: Date
        type: date
      - name: Value
        type: currency
```

### Custom Export Formats

Extend `MultiFormatExporter`:

```python
class CustomExporter(MultiFormatExporter):
    def _export_custom(self, sheets, output_path):
        # Custom export logic
        pass
```

### Custom Validators

Add validation rules:

```python
from spreadsheet_dl import ValidationRule, ValidationRuleType

custom_rule = ValidationRule(
    rule_type=ValidationRuleType.CUSTOM,
    formula="=AND(A1>0,A1<10000)",
    error_message="Value must be between 0 and 10,000"
)
```

## Versioning

SpreadsheetDL follows semantic versioning:

- **v2.0.0**: Professional Spreadsheet System (95 requirements)
- **v1.0.0**: Phase 5 - Future Enhancements
- **v0.7.0**: Phase 4 - Advanced Features
- **v0.6.0**: Phase 3 - Enhanced Features
- **v0.5.0**: Backup/Export Features
- **v0.4.x**: Builder API and Security

## Related Documentation

- [API Reference](./API.md)
- [Template Guide](./TEMPLATES.md)
- [Theme System](./THEMES.md)
- [Security Guide](./SECURITY.md)
- [CLI Reference](./CLI.md)
