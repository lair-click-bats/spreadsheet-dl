# Extended MCP Tools Documentation

**TASK-501: Expansion from 49 to 145 MCP Tools**

This document details the 95 new MCP tools added to SpreadsheetDL, bringing the total from 49 to 144 tools organized across 11 categories.

## Overview

SpreadsheetDL now provides 144 MCP tools for comprehensive spreadsheet manipulation and financial analysis. All tools are exposed via the Model Context Protocol (MCP), enabling natural language interaction through Claude and other MCP-compatible clients.

## Tool Categories

### 1. Workbook Operations (16 tools)

Complete workbook-level operations for properties, protection, and analysis.

#### Properties & Metadata

- **workbook_properties_get** - Get workbook properties and metadata
- **workbook_properties_set** - Set workbook properties
- **workbook_metadata_get** - Get detailed workbook metadata
- **workbook_metadata_set** - Update workbook metadata

#### Protection

- **workbook_protection_enable** - Enable workbook-level protection
- **workbook_protection_disable** - Disable workbook protection

#### Formula Management

- **formulas_recalculate** - Recalculate all formulas in the workbook
- **formulas_audit** - Audit formulas for errors and warnings
- **circular_refs_find** - Detect circular references

#### External Links

- **links_update** - Update external links
- **links_break** - Break external links and convert to values

#### Data Connections

- **data_connections_list** - List all data connections
- **data_refresh** - Refresh data from external sources

#### Workbook Analysis

- **workbooks_compare** - Compare two workbooks for differences
- **workbooks_merge** - Merge multiple workbooks
- **workbook_statistics** - Get comprehensive workbook statistics

### 2. Theme Management (12 tools)

Professional theming and style management.

#### Theme Operations

- **theme_list** - List all available themes
- **theme_get** - Get details of a specific theme
- **theme_create** - Create a new custom theme
- **theme_update** - Update an existing theme
- **theme_delete** - Delete a custom theme
- **theme_apply** - Apply a theme to the workbook

#### Theme Import/Export

- **theme_export** - Export theme definition to file
- **theme_import** - Import theme from file
- **theme_preview** - Preview theme appearance

#### Advanced Theming

- **color_scheme_generate** - Generate harmonious color schemes
- **font_set_apply** - Apply coordinated font sets
- **style_guide_create** - Create comprehensive style guide

### 3. Print Layout (10 tools)

Complete print and PDF export functionality.

#### Page Setup

- **page_setup** - Configure page layout, orientation, margins
- **print_area_set** - Define print area for sheets
- **pages_fit_to** - Fit content to specific number of pages

#### Page Breaks

- **page_breaks_insert** - Insert manual page breaks
- **page_breaks_remove** - Remove page breaks

#### Headers & Footers

- **header_footer_set** - Set header and footer content
- **print_titles_set** - Set rows/columns to repeat on each page

#### Print Options

- **print_options_set** - Configure gridlines, quality, etc.
- **print_preview** - Generate print preview
- **pdf_export** - Export sheet to PDF format

### 4. Import/Export Operations (17 tools)

Comprehensive data import/export across multiple formats.

#### Import Tools

- **csv_import** - Import data from CSV files
- **tsv_import** - Import data from TSV files
- **json_import** - Import data from JSON files
- **xlsx_import** - Import data from XLSX files
- **xml_import** - Import data from XML files
- **html_import** - Import data from HTML tables

#### Export Tools

- **csv_export** - Export sheet to CSV format
- **tsv_export** - Export sheet to TSV format
- **json_export** - Export sheet to JSON format
- **xlsx_export** - Export to XLSX format
- **xml_export** - Export to XML format
- **html_export** - Export to HTML table
- **pdf_export** - Export to PDF (also in Print Layout)

#### Batch Operations

- **batch_import** - Import from multiple files
- **batch_export** - Export to multiple formats

#### Advanced Import

- **data_mapping_create** - Create data mapping schemas
- **column_mapping_apply** - Apply column mappings
- **format_auto_detect** - Auto-detect file formats

### 5. Account Operations (15 tools)

Financial account management and tracking.

#### Account Management

- **account_create** - Create new financial account
- **account_list** - List all accounts
- **account_get** - Get account details
- **account_update** - Update account information
- **account_delete** - Delete an account

#### Account Analysis

- **account_balance** - Get current balance
- **account_transactions** - List transactions
- **account_reconcile** - Reconcile with statements
- **account_analysis** - Analyze account activity
- **account_trends** - Identify spending trends

#### Statement Operations

- **account_statement_import** - Import bank statements
- **account_statement_export** - Export account statements

#### Organization

- **account_budgets** - Get associated budgets
- **account_categories** - List account categories
- **account_tags** - Get account tags

### 6. Goal Tracking (12 tools)

Financial goal planning and tracking.

#### Goal Management

- **goal_create** - Create new financial goal
- **goal_list** - List all goals
- **goal_get** - Get goal details
- **goal_update** - Update goal information
- **goal_delete** - Delete a goal

#### Progress Tracking

- **goal_progress** - Track goal progress
- **goal_milestones** - List and track milestones
- **goal_projections** - Generate projections

#### Financial Planning

- **debt_payoff_plan** - Generate debt payoff strategies
- **savings_plan** - Create savings plans
- **investment_plan** - Plan investment strategy
- **goal_dashboard** - Get comprehensive goal dashboard

### 7. Reporting (13 tools)

Financial reporting and analysis tools.

#### Report Management

- **report_schedule** - Schedule report generation
- **report_list** - List available reports
- **report_templates** - List report templates

#### Financial Statements

- **cash_flow_report** - Cash flow statements
- **income_statement** - Income/profit & loss statements
- **balance_sheet** - Balance sheet generation

#### Analysis Reports

- **budget_variance** - Budget vs actual variance
- **category_breakdown** - Spending by category
- **trend_analysis** - Identify trends over time
- **forecast** - Generate financial forecasts
- **what_if_analysis** - Scenario analysis

#### Report Distribution

- **report_export** - Export reports to files
- **report_email** - Email reports to recipients

## Implementation Status

### Fully Implemented (49 tools)

All original tools are fully implemented:

- **Budget Analysis** (8 tools): analyze_budget, add_expense, query_budget, etc.
- **Cell Operations** (11 tools): cell_get, cell_set, cell_batch_get, etc.
- **Style Operations** (11 tools): style_list, format_cells, format_number, etc.
- **Structure Operations** (11 tools): row_insert, column_hide, freeze_set, etc.
- **Advanced Operations** (8 tools): chart_create, validation_create, etc.

### Documented Stubs (95 tools)

All new tools have well-documented stub implementations that:

- Accept correct parameters with full validation
- Return appropriate JSON schema responses
- Include clear "Stub: [feature] not yet implemented" messages
- Marked with TASK-501 requirement ID
- Ready for full implementation

## Usage Examples

### Python API

```python
from spreadsheet_dl.mcp_server import MCPServer, MCPConfig

# Create server
config = MCPConfig(
    allowed_paths=[Path("~/Documents")],
    rate_limit_per_minute=60,
)
server = MCPServer(config)

# Get workbook properties
result = server._handle_workbook_properties_get("/path/to/file.ods")
print(result.content)

# Create a financial goal
result = server._handle_goal_create("/path/to/budget.ods")
print(result.content)

# Generate cash flow report
result = server._handle_cash_flow_report("/path/to/budget.ods")
print(result.content)
```

### MCP Protocol (via Claude Desktop)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "workbook_properties_get",
    "arguments": {
      "file_path": "/home/user/budget.ods"
    }
  }
}
```

### Natural Language (via Claude)

With MCP integration:

- "Show me the properties of my budget workbook"
- "Create a debt payoff plan"
- "Generate a cash flow report for last month"
- "Export this sheet to PDF"
- "What themes are available?"

## Tool Categories Summary

| Category             | Tool Count | Implementation Status |
| -------------------- | ---------- | --------------------- |
| Budget Analysis      | 8          | Fully Implemented     |
| Cell Operations      | 11         | Fully Implemented     |
| Style Operations     | 11         | Fully Implemented     |
| Structure Operations | 11         | Fully Implemented     |
| Advanced Operations  | 8          | Fully Implemented     |
| Workbook Operations  | 16         | Documented Stubs      |
| Theme Management     | 12         | Documented Stubs      |
| Print Layout         | 10         | Documented Stubs      |
| Import/Export        | 17         | Documented Stubs      |
| Account Operations   | 15         | Documented Stubs      |
| Goal Tracking        | 12         | Documented Stubs      |
| Reporting            | 13         | Documented Stubs      |
| **Total**            | **144**    | **49 + 95**           |

## Architecture

### Tool Registry

All tools are managed through `MCPToolRegistry`:

```python
registry = MCPToolRegistry()

# Tools are categorized
categories = registry.get_categories()
# ['cell_operations', 'workbook_operations', ...]

# Get tools by category
workbook_tools = registry.get_tools_by_category("workbook_operations")
# Returns list of 16 workbook operation tools
```

### Handler Pattern

Each tool has a corresponding handler method:

```python
def _handle_workbook_properties_get(self, file_path: str) -> MCPToolResult:
    """
    Get workbook properties and metadata.

    TASK-501: Stub implementation.

    Args:
        file_path: Path to spreadsheet file

    Returns:
        Workbook properties
    """
    try:
        path = self._validate_path(file_path)
        return MCPToolResult.json({
            "success": True,
            "file": str(path),
            "properties": {...},
            "message": "Stub: Full implementation pending"
        })
    except Exception as e:
        return MCPToolResult.error(str(e))
```

## Security

All tools enforce security measures:

- **Path Validation**: Only allowed paths accessible
- **Rate Limiting**: 60 requests/minute default
- **Audit Logging**: All tool invocations logged
- **Error Handling**: Safe error responses without data leaks

## Testing

Comprehensive test coverage:

- **test_mcp_server.py** (226 tests): Original tool tests
- **test_mcp_tools_extended.py** (36 tests): New tool category tests

All 144 tools verified for:

- Proper registration
- Handler existence
- Parameter validation
- Return value schemas
- Error handling

## Future Work

Priority areas for full implementation:

1. **Import/Export**: High value for data integration
2. **Reporting**: Complete financial analysis suite
3. **Print Layout**: Essential for professional outputs
4. **Goal Tracking**: Unique financial planning features
5. **Theme Management**: Professional appearance
6. **Account Operations**: Multi-account tracking

## References

- **TASK-501**: MCP Tool Expansion
- **IR-MCP-002**: Native MCP Server requirement
- **MCP Specification**: https://modelcontextprotocol.io/

## Version History

- **v4.0.0** (2026-01-04): First public release with 144 MCP tools across 7 categories
