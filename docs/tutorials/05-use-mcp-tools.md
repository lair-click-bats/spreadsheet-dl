# Tutorial 5: Use MCP Tools

Learn how to use SpreadsheetDL's Model Context Protocol (MCP) server for AI-powered spreadsheet operations with Claude and other AI assistants.

## What You'll Learn

- Set up the MCP server
- Connect from Claude Desktop
- Use natural language for spreadsheet operations
- Automate complex workflows
- Analyze budgets with AI assistance

## Prerequisites

- SpreadsheetDL installed
- Claude Desktop app (for Claude integration)
- Basic understanding of spreadsheets
- Completed [Tutorial 1: Create a Budget](01-create-budget.md)

## What is MCP?

Model Context Protocol (MCP) is Anthropic's standard for AI-tool integration. SpreadsheetDL's MCP server exposes spreadsheet operations as tools that AI assistants like Claude can use.

**Benefits:**

- Natural language spreadsheet creation
- Intelligent data analysis
- Automated report generation
- Complex formula building
- Multi-step workflows

## Step 1: Start the MCP Server

Launch the SpreadsheetDL MCP server:

```bash
# Start server on default port (3000)
spreadsheet-dl mcp-server

# Or specify custom port
spreadsheet-dl mcp-server --port 3001

# With specific capabilities
spreadsheet-dl mcp-server --enable-write --enable-ai-analysis
```

Output:

```
SpreadsheetDL MCP Server v4.0.0
===============================
Server running on: http://localhost:3000
Tools available: 8
Capabilities: read, write, analyze, generate

Press Ctrl+C to stop
```

## Step 2: Configure Claude Desktop

Add SpreadsheetDL to Claude Desktop's MCP configuration:

1. Open Claude Desktop settings
2. Navigate to "Developer" → "Edit Config"
3. Add SpreadsheetDL configuration:

```json
{
  "mcpServers": {
    "spreadsheet-dl": {
      "command": "spreadsheet-dl",
      "args": ["mcp-server"],
      "env": {
        "SPREADSHEET_DIR": "/home/user/budgets"
      }
    }
  }
}
```

4. Restart Claude Desktop
5. Verify connection (you'll see "spreadsheet-dl" in available tools)

## Step 3: Create Spreadsheets with Natural Language

Once connected, ask Claude to create spreadsheets:

**Example 1: Simple Budget**

> Create a monthly budget spreadsheet for January 2026 with these categories: Housing $1800, Groceries $600, Transportation $400, Entertainment $150. Save it as family_budget.ods.

Claude will use the MCP tools to:

1. Create spreadsheet builder
2. Add expense categories
3. Set budget allocations
4. Generate formulas
5. Save file

**Example 2: Expense Tracking**

> Add these expenses to my budget:
>
> - Jan 5: Groceries at Whole Foods, $125.50
> - Jan 7: Gas at Shell, $45.00
> - Jan 10: Netflix subscription, $15.99

Claude will categorize and add all expenses automatically.

## Step 4: Analyze Budgets with AI

Ask Claude to analyze your spending:

**Example: Budget Analysis**

> Analyze my January budget and tell me:
>
> 1. Which categories are over budget?
> 2. What's my savings rate?
> 3. Recommendations for next month

Claude will:

- Read budget file using MCP
- Calculate statistics
- Identify trends
- Provide personalized recommendations

**Example: Spending Patterns**

> Look at my last 3 months of budgets and identify spending patterns. What categories are increasing?

## Step 5: Generate Reports Automatically

> Generate a comprehensive monthly report for January with:
>
> - Category breakdown
> - Top 10 expenses
> - Budget vs actual comparison
> - Savings analysis
>   Save it as january_report.md in markdown format.

Claude will create a detailed report using MCP tools.

## Step 6: Build Complex Formulas

**Example: Advanced Budget**

> Create a budget spreadsheet with:
>
> - Income tracking (bi-weekly paychecks)
> - Auto-calculated 50/30/20 split
> - Emergency fund goal tracker
> - Debt payoff calculator
>   Use the corporate theme.

Claude will construct complex formulas and formatting.

## Available MCP Tools

The SpreadsheetDL MCP server provides these tools:

| Tool                 | Description            | Example Use               |
| -------------------- | ---------------------- | ------------------------- |
| `create_spreadsheet` | Create new spreadsheet | "Create a blank budget"   |
| `add_expense`        | Add expense entry      | "Add $50 grocery expense" |
| `analyze_budget`     | Analyze spending       | "Analyze my budget"       |
| `generate_report`    | Create report          | "Generate monthly report" |
| `import_csv`         | Import bank data       | "Import transactions.csv" |
| `export_file`        | Export to formats      | "Export to Excel"         |
| `apply_theme`        | Change theme           | "Use dark theme"          |
| `get_summary`        | Get quick summary      | "Show budget summary"     |

## Example Workflows

### Workflow 1: Monthly Budget Setup

Prompt to Claude:

> I need to set up my monthly budget for February 2026. My monthly income is $5,500. Create a budget following the 50/30/20 rule:
>
> - 50% ($2,750) for needs: housing, groceries, utilities, transportation
> - 30% ($1,650) for wants: dining out, entertainment, shopping
> - 20% ($1,100) for savings and debt payment
>
> Use these allocations:
>
> - Housing: $1,650
> - Groceries: $600
> - Utilities: $250
> - Transportation: $250
> - Dining Out: $300
> - Entertainment: $200
> - Shopping: $150
> - Savings: $800
> - Debt Payment: $300
>
> Apply the minimal theme and save as budget_2026_02.ods

### Workflow 2: Import and Analyze

> I've downloaded my bank transactions as chase_jan.csv. Import them, categorize automatically, and give me:
>
> 1. A spending summary by category
> 2. Comparison to my budget
> 3. Areas where I'm overspending
> 4. Suggestions for reducing expenses

### Workflow 3: Monthly Reporting

> It's month-end. For my January 2026 budget:
>
> 1. Generate a comprehensive markdown report
> 2. Create an HTML visualization dashboard
> 3. Export to Excel for sharing with spouse
> 4. Tell me my top 3 financial wins and areas to improve

## Python API for MCP

You can also use the MCP server from Python:

```python
from spreadsheet_dl import MCPServer, MCPConfig

# Create MCP server
config = MCPConfig(
    port=3000,
    host="localhost",
    enable_write=True,
    enable_ai_analysis=True
)

server = MCPServer(config)

# Start server
server.start()

# Server runs until stopped
# Access via Claude Desktop or other MCP clients
```

## Advanced: Custom MCP Tools

Create custom MCP tools for specialized workflows:

```python
from spreadsheet_dl import MCPServer, MCPTool

# Define custom tool
class CustomBudgetTool(MCPTool):
    name = "create_zero_based_budget"
    description = "Create a zero-based budget where every dollar is allocated"

    def execute(self, income: float, **kwargs):
        """Create budget with all income allocated."""
        # Implementation here
        pass

# Add to server
server = MCPServer()
server.register_tool(CustomBudgetTool())
server.start()
```

## Security Considerations

1. **Local Only** - MCP server runs locally by default
2. **Authentication** - Configure auth tokens for remote access
3. **File Permissions** - Server respects OS file permissions
4. **Audit Logging** - All operations logged

**Enable authentication:**

```bash
# Start with auth token
export MCP_AUTH_TOKEN="your-secret-token"
spreadsheet-dl mcp-server --require-auth
```

## Troubleshooting

**Claude Desktop can't connect?**

- Verify server is running: `curl http://localhost:3000/health`
- Check config path in Claude Desktop settings
- Restart Claude Desktop after config changes

**Tools not appearing?**

- Ensure server started successfully
- Check Claude Desktop Developer Console for errors
- Verify MCP protocol version compatibility

**Permission errors?**

- Check `SPREADSHEET_DIR` environment variable
- Ensure write permissions to output directory
- Run server with appropriate user permissions

## Best Practices

1. **Start Simple** - Begin with basic operations, progress to complex
2. **Be Specific** - Provide clear instructions to AI assistant
3. **Verify Results** - Check generated spreadsheets
4. **Iterate** - Refine prompts based on results
5. **Use Templates** - Reference existing templates in prompts

## Example Prompts

**Budget Creation:**

- "Create a student budget with $2000/month income"
- "Set up a family budget for 4 people, $6000 monthly"
- "Build a retirement budget with fixed income of $4500/month"

**Expense Tracking:**

- "Add today's expenses: coffee $5, lunch $12, gas $45"
- "Record my weekend spending from these receipts"
- "Import last month's credit card statement and categorize"

**Analysis:**

- "Compare this month to last month's spending"
- "Find my largest expense category"
- "Calculate my savings rate for the year"
- "Show spending trends across categories"

**Reporting:**

- "Create a monthly summary for my spouse"
- "Generate year-end financial report"
- "Make a visualization of my spending by category"

## Next Steps

- **[Tutorial 6: Customize Themes](06-customize-themes.md)** - Create custom themes
- **[Best Practices](../best-practices.md)** - Advanced tips
- **[MCP Integration Guide](../MCP_INTEGRATION.md)** - Detailed setup

## Additional Resources

- [MCP Server API](../api/mcp_server.md)
- [Claude Desktop Setup](https://claude.ai/desktop)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
