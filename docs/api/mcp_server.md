# MCP Server API Reference

Complete API reference for the Model Context Protocol (MCP) server implementation.

**Implements:** IR-MCP-002 (Native MCP Server)

## Overview

The MCP Server provides a native implementation of the Model Context Protocol, exposing spreadsheet manipulation and budget analysis operations as tools for natural language interaction with Claude Desktop and other MCP-compatible clients.

**Features:**

- 96 tools across 8 categories
- Complete spreadsheet manipulation (cells, styles, structure)
- Advanced features (charts, validation, conditional formatting)
- Workbook operations, theme management, print layout
- Import/export across multiple formats
- Security controls (path restrictions, rate limiting, audit logging)

**Architecture Note**: Domain-specific functionality (budget analysis, account management, goal tracking, reporting) is available via Python APIs (BudgetAnalyzer, AccountManager, GoalManager, ReportGenerator), not as MCP tools.

---

## MCPServer

### Class: `MCPServer`

Main MCP server class implementing the Model Context Protocol.

```python
from spreadsheet_dl.mcp_server import MCPServer, MCPConfig

# Create with default config
server = MCPServer()

# Create with custom config
config = MCPConfig(
    allowed_paths=[Path("/path/to/budgets")],
    rate_limit_per_minute=60
)
server = MCPServer(config)
```

#### Constructor

```python
MCPServer(config: MCPConfig | None = None)
```

**Parameters:**

- `config`: Server configuration (uses defaults if not provided)

### Tool Categories

The server provides 96 universal spreadsheet tools organized into 8 categories:

1. **Cell Operations** (11 tools) - Read, write, and manipulate cells
2. **Style Operations** (11 tools) - Format and style cells
3. **Structure Operations** (11 tools) - Modify spreadsheet structure
4. **Advanced Operations** (8 tools) - Charts, validation, and queries
5. **Workbook Operations** (16 tools) - Workbook-level properties and analysis
6. **Theme Management** (12 tools) - Theme creation and application
7. **Print Layout** (10 tools) - Page setup and PDF export
8. **Import/Export** (17 tools) - Multi-format data exchange

**Note on Domain-Specific Operations:**

For budget analysis, account management, goal tracking, and reporting, use the Python APIs directly:

```python
from spreadsheet_dl.budget_analyzer import BudgetAnalyzer
from spreadsheet_dl.report_generator import ReportGenerator

# Analyze budget
analyzer = BudgetAnalyzer("/path/to/budget.ods")
analysis = analyzer.analyze()

# Generate report
generator = ReportGenerator("/path/to/budget.ods")
report = generator.generate_monthly_report(format="markdown")
```

---

## Cell Operation Tools

### cell_get

Get the value of a specific cell.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name
- `cell` (string, required): Cell reference (e.g., "A1", "B5")

**Returns:** JSON with cell value

**Example:**

```json
{
  "cell": "A1",
  "sheet": "Budget",
  "value": "Total"
}
```

### cell_set

Set the value of a specific cell.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name
- `cell` (string, required): Cell reference
- `value` (string, required): Value to set

**Returns:** JSON with success status

### cell_clear

Clear the value and formatting of a cell.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name
- `cell` (string, required): Cell reference

**Returns:** JSON with success status

### cell_copy

Copy a cell or range to another location.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name
- `source` (string, required): Source cell/range (e.g., "A1" or "A1:B5")
- `destination` (string, required): Destination cell/range

**Returns:** JSON with success status

### cell_move

Move a cell or range to another location.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name
- `source` (string, required): Source cell/range
- `destination` (string, required): Destination cell/range

**Returns:** JSON with success status

### cell_batch_get

Get values of multiple cells in a single operation.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name
- `cells` (string, required): Comma-separated cell references or range (e.g., "A1,B2,C3" or "A1:C3")

**Returns:** JSON with cell values

**Example:**

```json
{
  "cells": ["A1", "B2", "C3"],
  "sheet": "Data",
  "values": {
    "A1": "Name",
    "B2": 100,
    "C3": "Active"
  }
}
```

### cell_batch_set

Set values of multiple cells in a single operation.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name
- `values` (string, required): JSON object mapping cell references to values

**Example:**

```javascript
{
  "name": "cell_batch_set",
  "arguments": {
    "file_path": "/path/to/file.ods",
    "sheet": "Data",
    "values": "{\"A1\": \"Name\", \"B1\": \"Value\", \"C1\": \"Status\"}"
  }
}
```

**Returns:** JSON with success status

### cell_find

Find cells containing specific text or matching a pattern.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name
- `search_text` (string, required): Text to search for
- `match_case` (boolean, optional): Whether to match case
  - Default: false

**Returns:** JSON with matching cell references

**Example:**

```json
{
  "search_text": "Total",
  "sheet": "Budget",
  "match_case": false,
  "matches": ["A1", "A15", "D20"]
}
```

### cell_replace

Find and replace text in cells.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name
- `search_text` (string, required): Text to search for
- `replace_text` (string, required): Replacement text
- `match_case` (boolean, optional): Whether to match case
  - Default: false

**Returns:** JSON with replacement count

### cell_merge

Merge a range of cells.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name
- `range` (string, required): Cell range to merge (e.g., "A1:B5")

**Returns:** JSON with success status

### cell_unmerge

Unmerge a previously merged cell range.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name
- `cell` (string, required): Any cell in the merged range

**Returns:** JSON with success status

---

## Style Operation Tools

### style_list

List all available styles in a spreadsheet.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, optional): Sheet name

**Returns:** JSON with style list

### style_get

Get details of a specific style.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, optional): Sheet name

**Returns:** JSON with style details

### style_create

Create a new style definition.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, optional): Sheet name

**Returns:** JSON with success status

### style_update

Update an existing style.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, optional): Sheet name

**Returns:** JSON with success status

### style_delete

Delete a style.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, optional): Sheet name

**Returns:** JSON with success status

### style_apply

Apply a style to a cell or range.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### format_cells

Format cells with specific styling.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### format_number

Format cells as numbers with specific format.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### format_font

Apply font formatting to cells.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### format_fill

Apply fill/background color to cells.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### format_border

Apply borders to cells.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

---

## Structure Operation Tools

### row_insert

Insert a new row at a specified position.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### row_delete

Delete a row.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### row_hide

Hide a row.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### column_insert

Insert a new column at a specified position.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### column_delete

Delete a column.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### column_hide

Hide a column.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### freeze_set

Set freeze panes at a specified position.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### freeze_clear

Clear freeze panes.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### sheet_create

Create a new sheet.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### sheet_delete

Delete a sheet.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### sheet_copy

Copy a sheet.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

---

## Advanced Operation Tools

### chart_create

Create a new chart.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### chart_update

Update an existing chart.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### validation_create

Create data validation rules.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### cf_create

Create conditional formatting rules.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### named_range_create

Create a named range.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### table_create

Create a table from a range.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with success status

### query_select

Query and select data based on criteria.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with query results

### query_find

Find data matching specific conditions.

**Parameters:**

- `file_path` (string, required): Path to spreadsheet file
- `sheet` (string, required): Sheet name

**Returns:** JSON with found data

---

## Configuration Classes

### MCPConfig

Server configuration.

```python
@dataclass
class MCPConfig:
    name: str = "spreadsheet-dl"
    version: str = "1.0.0"
    allowed_paths: list[Path] = field(default_factory=list)
    rate_limit_per_minute: int = 60
    enable_audit_log: bool = True
    audit_log_path: Path | None = None
```

**Attributes:**

- `name`: Server name
- `version`: Server version
- `allowed_paths`: List of allowed file paths (security control)
- `rate_limit_per_minute`: Maximum requests per minute
- `enable_audit_log`: Enable audit logging
- `audit_log_path`: Path for audit log file

**Example:**

```python
config = MCPConfig(
    name="my-spreadsheet-server",
    allowed_paths=[
        Path("/home/user/Documents"),
        Path("/home/user/Finance")
    ],
    rate_limit_per_minute=100,
    enable_audit_log=True,
    audit_log_path=Path("/var/log/mcp-audit.log")
)
```

### MCPToolRegistry

Tool registry with decorator-based registration.

```python
class MCPToolRegistry:
    def tool(
        self,
        name: str,
        description: str,
        category: str = "general",
        parameters: list[MCPToolParameter] | None = None
    ) -> Callable
```

**Example:**

```python
registry = MCPToolRegistry()

@registry.tool(
    name="custom_operation",
    description="Perform custom operation",
    category="custom",
    parameters=[
        MCPToolParameter("file_path", "string", "Path to file", required=True),
        MCPToolParameter("option", "string", "Operation option", required=False)
    ]
)
def handle_custom_operation(file_path: str, option: str = "default") -> MCPToolResult:
    # Implementation
    return MCPToolResult.text("Operation complete")
```

### MCPTool

Tool definition.

```python
@dataclass
class MCPTool:
    name: str
    description: str
    parameters: list[MCPToolParameter]
    handler: Callable[..., Any] | None
```

### MCPToolParameter

Tool parameter definition.

```python
@dataclass
class MCPToolParameter:
    name: str
    type: str
    description: str
    required: bool = True
    enum: list[str] | None = None
    default: Any = None
```

### MCPToolResult

Tool execution result.

```python
@dataclass
class MCPToolResult:
    content: list[dict[str, Any]]
    is_error: bool = False

    @classmethod
    def text(cls, text: str) -> MCPToolResult:
        """Create a text result."""

    @classmethod
    def json(cls, data: Any) -> MCPToolResult:
        """Create a JSON result."""

    @classmethod
    def error(cls, message: str) -> MCPToolResult:
        """Create an error result."""
```

---

## Server Methods

### run()

Run the MCP server in stdio mode.

```python
def run(self) -> None
```

Reads JSON-RPC messages from stdin and writes responses to stdout.

**Example:**

```python
server = MCPServer()
server.run()  # Blocks until stopped
```

### handle_message()

Handle an incoming MCP message.

```python
def handle_message(self, message: dict[str, Any]) -> dict[str, Any] | None
```

**Parameters:**

- `message`: JSON-RPC message

**Returns:** JSON-RPC response or None for notifications

---

## Security Features

### Path Restrictions

Control which file paths the server can access.

```python
config = MCPConfig(
    allowed_paths=[
        Path("/home/user/Documents"),
        Path("/home/user/Finance")
    ]
)
```

Any attempt to access files outside these paths will raise `MCPSecurityError`.

### Rate Limiting

Limit requests per minute to prevent abuse.

```python
config = MCPConfig(
    rate_limit_per_minute=60  # Max 60 requests/minute
)
```

### Audit Logging

Log all tool invocations for audit trails.

```python
config = MCPConfig(
    enable_audit_log=True,
    audit_log_path=Path("/var/log/mcp-audit.log")
)
```

**Audit log format:**

```json
{
  "timestamp": "2024-12-15T10:30:45",
  "tool": "add_expense",
  "params": { "file_path": "/path/to/budget.ods", "amount": "125.50" },
  "success": true
}
```

---

## Exception Classes

### MCPError

Base exception for MCP server errors.

```python
class MCPError(SpreadsheetDLError):
    error_code = "FT-MCP-1900"
```

### MCPToolError

Raised when a tool execution fails.

```python
class MCPToolError(MCPError):
    error_code = "FT-MCP-1901"
```

### MCPSecurityError

Raised when a security violation occurs.

```python
class MCPSecurityError(MCPError):
    error_code = "FT-MCP-1902"
```

---

## Convenience Functions

### create_mcp_server()

Create an MCP server with optional path restrictions.

```python
def create_mcp_server(
    allowed_paths: list[str | Path] | None = None
) -> MCPServer
```

**Example:**

```python
from spreadsheet_dl.mcp_server import create_mcp_server

server = create_mcp_server(["/home/user/Documents"])
server.run()
```

### main()

Entry point for MCP server CLI.

```python
def main() -> None
```

**Usage:**

```bash
python -m spreadsheet_dl.mcp_server --allowed-paths /path/to/budgets --debug
```

**CLI Arguments:**

- `--allowed-paths`: Space-separated list of allowed paths
- `--debug`: Enable debug logging

---

## Complete Examples

### Example 1: Running MCP Server

```python
from spreadsheet_dl.mcp_server import MCPServer, MCPConfig
from pathlib import Path

# Configure server
config = MCPConfig(
    name="my-budget-server",
    allowed_paths=[Path.home() / "Documents" / "Budgets"],
    rate_limit_per_minute=100,
    enable_audit_log=True
)

# Create and run server
server = MCPServer(config)
server.run()  # Starts stdio-based MCP server
```

### Example 2: Working with Cells

**Via Claude Desktop:**

> "Get the value from cell B5 in my budget file"

**Tool Call:**

```json
{
  "name": "cell_get",
  "arguments": {
    "file_path": "/home/user/Documents/budget.ods",
    "sheet": "Budget",
    "cell": "B5"
  }
}
```

**Response:**

```json
{
  "cell": "B5",
  "sheet": "Budget",
  "value": 450.25
}
```

### Example 3: Applying Styles

**User:** "Make the first row of my spreadsheet bold with a blue background"

**Tool Call:**

```json
{
  "name": "style_apply",
  "arguments": {
    "file_path": "/path/to/budget.ods",
    "sheet": "Budget",
    "range": "A1:Z1",
    "style_name": "header"
  }
}
```

### Example 4: Creating Charts

**User:** "Create a bar chart from the data in A1:D10"

**Tool Call:**

```json
{
  "name": "chart_create",
  "arguments": {
    "file_path": "/path/to/budget.ods",
    "sheet": "Budget",
    "range": "A1:D10",
    "chart_type": "bar"
  }
}
```

### Example 5: Custom Tool Registration

```python
from spreadsheet_dl.mcp_server import MCPServer, MCPToolParameter, MCPToolResult

server = MCPServer()
registry = server._registry

# Register custom tool
@registry.tool(
    name="export_to_pdf",
    description="Export spreadsheet to PDF",
    category="export",
    parameters=[
        MCPToolParameter("file_path", "string", "Spreadsheet path", required=True),
        MCPToolParameter("output_path", "string", "PDF output path", required=True)
    ]
)
def handle_export_pdf(file_path: str, output_path: str) -> MCPToolResult:
    # Implementation
    return MCPToolResult.json({
        "success": True,
        "output": output_path
    })

# Tool is now available to MCP clients
```

---

## Best Practices

### 1. Configure Appropriate Path Restrictions

```python
# Don't allow entire filesystem
# Bad:
config = MCPConfig(allowed_paths=[Path("/")])

# Good: Restrict to specific directories
config = MCPConfig(allowed_paths=[
    Path.home() / "Documents" / "Budgets",
    Path.home() / "Finance"
])
```

### 2. Enable Audit Logging for Production

```python
config = MCPConfig(
    enable_audit_log=True,
    audit_log_path=Path("/var/log/spreadsheet-mcp-audit.log")
)
```

### 3. Set Appropriate Rate Limits

```python
# For interactive use
config = MCPConfig(rate_limit_per_minute=60)

# For automated systems (higher)
config = MCPConfig(rate_limit_per_minute=300)
```

### 4. Handle Errors Gracefully

```python
try:
    server = MCPServer(config)
    server.run()
except MCPSecurityError as e:
    logger.error(f"Security violation: {e}")
except MCPError as e:
    logger.error(f"MCP error: {e}")
```

### 5. Use Structured Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr  # MCP uses stdout for protocol
)
```

---

## MCP Protocol Details

### JSON-RPC Messages

The server communicates using JSON-RPC 2.0 over stdio.

**Request Format:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "analyze_budget",
    "arguments": {
      "file_path": "/path/to/budget.ods"
    }
  }
}
```

**Response Format:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"total_budget\": 5000.00, ...}"
      }
    ],
    "isError": false
  }
}
```

### Supported Methods

- `initialize`: Initialize protocol connection
- `tools/list`: List available tools
- `tools/call`: Execute a tool
- `notifications/initialized`: Notification after initialization

### Protocol Version

- Protocol version: `2024-11-05` (MCP v1)
