# LibreOffice MCP Server Integration

This guide covers setting up the LibreOffice MCP server for natural language
interaction with budget spreadsheets via Claude Code.

## Prerequisites

- Node.js 18+ installed
- LibreOffice installed (for ODS support)
- Claude Code (Claude Desktop or CLI)

## Installation

### 1. Install the MCP Server

```bash
npx -y @smithery/cli install @patrup/mcp-libre --client claude
```

This installs the LibreOffice MCP server and configures it for Claude.

### 2. Verify Configuration

Check your Claude configuration file:

**For Claude Desktop**: `~/.claude/claude_desktop_config.json`
**For Claude CLI**: `~/.claude.json` or project `.mcp.json`

Should contain:

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

### 3. Verify LibreOffice Path

Find your LibreOffice installation:

```bash
# Linux
which libreoffice
# Usually: /usr/bin/libreoffice

# macOS
ls /Applications/LibreOffice.app/Contents/MacOS/soffice

# Windows
where libreoffice
```

Update the `LIBREOFFICE_PATH` environment variable accordingly.

## Usage Examples

### Reading Budget Data

```
Claude: "Read my budget file at ~/Documents/budget_2025_01.ods"
```

### Analyzing Spending

```
Claude: "What categories have I spent the most in this month?"
```

### Getting Summaries

```
Claude: "Summarize my spending for January and compare to budget"
```

### Checking Alerts

```
Claude: "Am I over budget in any category?"
```

### Creating Visualizations

```
Claude: "Create a pie chart of my spending by category"
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
   uv run finance-tracker generate -o ./budgets/
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
   uv run finance-tracker report ./budgets/budget_2025_01.ods -f markdown
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
from finance_tracker.budget_analyzer import analyze_budget
from finance_tracker.report_generator import generate_monthly_report

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
