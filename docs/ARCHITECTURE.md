# Architecture Overview

## Project Structure

```
finance-tracker/
├── src/
│   └── finance_tracker/          # Main package
│       ├── __init__.py           # Package exports
│       ├── ods_generator.py      # ODS file creation
│       ├── budget_analyzer.py    # Pandas-based analysis
│       ├── report_generator.py   # Report generation
│       └── cli.py                # Command-line interface
├── tests/                        # Test suite
├── examples/                     # Usage examples
├── templates/                    # ODS templates
└── docs/                         # Documentation
```

## Core Components

### ODS Generator (`ods_generator.py`)

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

### Budget Analyzer (`budget_analyzer.py`)

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

### Report Generator (`report_generator.py`)

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
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│                 │     │                  │     │                 │
│  ODS Generator  │────>│   ODS File       │────>│ Budget Analyzer │
│                 │     │  (Nextcloud)     │     │                 │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          v
                                                 ┌─────────────────┐
                                                 │                 │
                                                 │ Report Generator│
                                                 │                 │
                                                 └─────────────────┘
```

## Integration Points

### Nextcloud + Collabora

ODS files are designed for seamless Collabora Office editing:

1. Generate ODS file locally
2. Upload to Nextcloud (manually or via WebDAV)
3. Edit in browser (Collabora) or mobile (Nextcloud iOS/Android)
4. Download and analyze locally

### LibreOffice MCP Server

Optional integration with Claude Code via MCP:

```json
{
  "mcpServers": {
    "libreoffice": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@patrup/mcp-libre"],
      "env": {
        "LIBREOFFICE_PATH": "/usr/bin/libreoffice"
      }
    }
  }
}
```

Enables natural language queries:

- "Analyze my January budget"
- "What category has the highest spending?"
- "Am I over budget this month?"

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

## Security Considerations

1. **Local Processing**: All analysis runs locally
2. **No Cloud Dependencies**: Works offline
3. **File-Based**: No database or network requirements
4. **Minimal Permissions**: Only needs file read/write access

For sensitive financial data:

- Keep ODS files in encrypted storage
- Use Nextcloud's encryption features
- Restrict MCP server file access paths
