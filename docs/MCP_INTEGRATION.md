# SpreadsheetDL MCP Server Integration (v4.0)

This guide covers the native SpreadsheetDL MCP server for natural language
interaction with spreadsheets via Claude Desktop, Claude CLI, and other
MCP-compatible clients.

**Version 4.0** introduces a comprehensive MCP server with 145+ tools for
complete spreadsheet manipulation through AI assistants.

## Prerequisites

- Python 3.12+ installed
- SpreadsheetDL v4.0+ installed (`pip install spreadsheet-dl`)
- Claude Desktop or Claude CLI (or any MCP-compatible client)

## Installation

### 1. Install SpreadsheetDL

```bash
pip install spreadsheet-dl
# or with uv
uv add spreadsheet-dl
```

### 2. Configure MCP Server

Add the SpreadsheetDL MCP server to your Claude configuration:

**For Claude Desktop**: `~/.claude/claude_desktop_config.json`
**For Claude CLI**: `~/.claude.json` or project `.mcp.json`

```json
{
  "mcpServers": {
    "spreadsheet-dl": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "spreadsheet_dl.mcp_server"],
      "env": {
        "SPREADSHEET_DL_ALLOWED_PATHS": "~/Documents,~/Downloads,."
      }
    }
  }
}
```

### 3. Verify Installation

Test the MCP server to ensure it's working:

```bash
# List all 145+ available tools
python -m spreadsheet_dl.mcp_server --list-tools

# Should output 13 categories with 145 total tools
```

### 4. Security Configuration

The MCP server enforces path restrictions for security. Configure allowed paths:

```bash
# Via environment variable
export SPREADSHEET_DL_ALLOWED_PATHS="/path/to/spreadsheets:/another/path"

# Via configuration file (~/.spreadsheet-dl/config.json)
{
  "mcp_server": {
    "allowed_paths": ["/path/to/spreadsheets", "/another/path"],
    "rate_limit_per_minute": 120,
    "enable_audit_log": true
  }
}
```

## Usage Examples

### Cell Operations

```
User: "Get the value from cell A1 in Sheet1 of report.ods"
Claude: Uses cell_get tool to retrieve value

User: "Set cell B5 in Sheet1 to the formula =SUM(B1:B4)"
Claude: Uses cell_set with type="formula"

User: "Find all cells containing 'Total' in the spreadsheet"
Claude: Uses cell_find to search across sheets
```

### Style Operations

```
User: "Make cells A1:E1 bold with dark blue background"
Claude: Uses cell_font to set bold, color_set_background for fill

User: "Apply the 'header' style to row 1"
Claude: Uses style_apply with range A1:Z1

User: "Create a new style called 'highlight' with yellow background and red text"
Claude: Uses style_create to define custom style
```

### Structure Operations

```
User: "Insert 3 rows above row 5"
Claude: Uses row_insert with position=5, count=3

User: "Hide columns D through F"
Claude: Uses column_hide with range D:F

User: "Freeze the first row and first column"
Claude: Uses freeze_set with rows=1, columns=1
```

### Charts and Visualizations

```
User: "Create a column chart of sales data in A1:B10"
Claude: Uses chart_create with type="column"

User: "Add a pie chart showing category breakdown"
Claude: Uses chart_create with appropriate data range

User: "Create sparklines in column E showing trends from columns A-D"
Claude: Uses sparkline_create for each row
```

### Data Analysis

```
User: "Sort the data by column B in descending order"
Claude: Uses query_sort with column=B, order=desc

User: "Find all values greater than 1000 in column C"
Claude: Uses query_filter with condition >1000

User: "Calculate the sum of all values in the Amount column"
Claude: Uses query_aggregate with function=SUM
```

### Multi-Format Operations

```
User: "Export this spreadsheet to Excel format"
Claude: Uses export_xlsx to convert

User: "Import data from data.csv into a new sheet"
Claude: Uses import_csv to load data

User: "Convert this ODS file to PDF"
Claude: Uses export_pdf for document export
```

## Advanced Configuration

### Project-Scoped Configuration

Create `.mcp.json` in your project root for project-specific settings:

```json
{
  "mcpServers": {
    "libreoffice": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@patrup/mcp-libre"],
      "env": {
        "LIBREOFFICE_PATH": "/usr/bin/libreoffice",
        "ALLOWED_PATHS": "/home/user/Documents/finances"
      }
    }
  }
}
```

### Restricting File Access

For security, limit which directories the MCP server can access:

```json
{
  "env": {
    "ALLOWED_PATHS": "/path/to/budget/files:/path/to/another/dir"
  }
}
```

## Workflow Integration

### Typical Workflow

1. **Generate Budget** (Python):

   ```bash
   uv run spreadsheet-dl generate -o ./budgets/
   ```

2. **Upload to Nextcloud** (manual or script):

   ```bash
   scp budgets/budget_2025_01.ods user@beelink:/nextcloud/data/
   ```

3. **Edit via Collabora** (browser/mobile):
   - Add expenses throughout the month
   - Collabora handles formulas and formatting

4. **Download Updated File**:

   ```bash
   scp user@beelink:/nextcloud/data/budget_2025_01.ods ./budgets/
   ```

5. **Analyze via Claude** (MCP):

   ```
   Claude: "Analyze my January budget and tell me if I'm on track"
   ```

6. **Generate Report** (Python):
   ```bash
   uv run spreadsheet-dl report ./budgets/budget_2025_01.ods -f markdown
   ```

## Troubleshooting

### MCP Server Not Found

```
Error: Cannot find MCP server 'libreoffice'
```

**Solution**: Reinstall the server:

```bash
npx -y @smithery/cli install @patrup/mcp-libre --client claude
```

### LibreOffice Not Found

```
Error: LibreOffice executable not found
```

**Solution**: Check `LIBREOFFICE_PATH` in config matches actual installation.

### Permission Denied

```
Error: Cannot read file
```

**Solution**:

- Check file permissions
- Verify `ALLOWED_PATHS` includes the file directory
- Run Claude with appropriate permissions

### File Format Error

```
Error: Unsupported file format
```

**Solution**: Ensure the file is a valid ODS file. Verify with:

```bash
file your_budget.ods
# Should show: OpenDocument Spreadsheet
```

## Security Best Practices

1. **Limit Paths**: Configure `ALLOWED_PATHS` to restrict access
2. **Don't Commit**: Never commit actual financial files to git
3. **Review Access**: Regularly check what files MCP can access
4. **Local Only**: MCP runs locally - no data sent to cloud
5. **Audit Logs**: Enable MCP logging to track file access

## Alternative: Direct Python Analysis

If MCP is not needed, use the Python API directly:

```python
from spreadsheet_dl.budget_analyzer import analyze_budget
from spreadsheet_dl.report_generator import generate_monthly_report

# Analyze
data = analyze_budget("budget_2025_01.ods")
print(f"Total spent: ${data['total_spent']:,.2f}")

# Report
report = generate_monthly_report("budget_2025_01.ods", format="text")
print(report)
```

This approach:

- Requires no additional configuration
- Works without Claude integration
- Can be automated via scripts
