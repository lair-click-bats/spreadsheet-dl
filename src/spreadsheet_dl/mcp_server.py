"""
MCP (Model Context Protocol) server for finance tracker.

Provides a native MCP server exposing finance operations as tools,
enabling natural language interaction with budgets via Claude and
other MCP-compatible LLM clients.

Requirements implemented:
    - IR-MCP-002: Native MCP Server (Gap G-AI-05)

Features:
    - Budget analysis tools
    - Natural language expense entry
    - Report generation on request
    - Spending trend analysis
    - Period comparison
    - Real-time budget queries

Security:
    - File access restrictions (configurable paths)
    - Rate limiting
    - Audit logging
"""

from __future__ import annotations

import contextlib
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any

from spreadsheet_dl.exceptions import (
    FileError,
    FinanceTrackerError,
)

if TYPE_CHECKING:
    from collections.abc import Callable


class MCPError(FinanceTrackerError):
    """Base exception for MCP server errors."""

    error_code = "FT-MCP-1900"


class MCPToolError(MCPError):
    """Raised when a tool execution fails."""

    error_code = "FT-MCP-1901"


class MCPSecurityError(MCPError):
    """Raised when a security violation occurs."""

    error_code = "FT-MCP-1902"


class MCPVersion(Enum):
    """MCP protocol versions."""

    V1 = "2024-11-05"  # Current stable version


@dataclass
class MCPCapabilities:
    """Server capabilities declaration."""

    tools: bool = True
    resources: bool = False
    prompts: bool = False
    logging: bool = True


@dataclass
class MCPToolParameter:
    """Definition of a tool parameter."""

    name: str
    type: str
    description: str
    required: bool = True
    enum: list[str] | None = None
    default: Any = None

    def to_schema(self) -> dict[str, Any]:
        """Convert to JSON Schema format."""
        schema: dict[str, Any] = {
            "type": self.type,
            "description": self.description,
        }
        if self.enum:
            schema["enum"] = self.enum
        if self.default is not None:
            schema["default"] = self.default
        return schema


@dataclass
class MCPTool:
    """Definition of an MCP tool."""

    name: str
    description: str
    parameters: list[MCPToolParameter] = field(default_factory=list)
    handler: Callable[..., Any] | None = None

    def to_schema(self) -> dict[str, Any]:
        """Convert to MCP tool schema format."""
        properties = {}
        required = []

        for param in self.parameters:
            properties[param.name] = param.to_schema()
            if param.required:
                required.append(param.name)

        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        }


@dataclass
class MCPToolResult:
    """Result of a tool execution."""

    content: list[dict[str, Any]]
    is_error: bool = False

    @classmethod
    def text(cls, text: str) -> MCPToolResult:
        """Create a text result."""
        return cls(content=[{"type": "text", "text": text}])

    @classmethod
    def json(cls, data: Any) -> MCPToolResult:
        """Create a JSON result."""
        return cls(
            content=[
                {
                    "type": "text",
                    "text": json.dumps(data, indent=2, default=str),
                }
            ]
        )

    @classmethod
    def error(cls, message: str) -> MCPToolResult:
        """Create an error result."""
        return cls(
            content=[{"type": "text", "text": f"Error: {message}"}],
            is_error=True,
        )


@dataclass
class MCPConfig:
    """Configuration for MCP server."""

    name: str = "spreadsheet-dl"
    version: str = "1.0.0"
    allowed_paths: list[Path] = field(default_factory=list)
    rate_limit_per_minute: int = 60
    enable_audit_log: bool = True
    audit_log_path: Path | None = None

    def __post_init__(self) -> None:
        """Set default allowed paths."""
        if not self.allowed_paths:
            # Default to common budget locations
            self.allowed_paths = [
                Path.cwd(),
                Path.home() / "Documents",
                Path.home() / "Finance",
            ]


class MCPToolRegistry:
    """
    Registry for MCP tools with decorator-based registration.

    Implements:
        - TASK-301: MCPToolRegistry with decorator registration
        - GAP-MCP: Tool discovery system

    Features:
        - Decorator-based tool registration
        - Automatic tool discovery
        - Tool metadata management
        - Category-based organization

    Example:
        >>> registry = MCPToolRegistry()
        >>> @registry.tool("cell_get", "Get cell value")
        >>> def get_cell(sheet: str, cell: str) -> str:
        ...     return "value"
    """

    def __init__(self) -> None:
        """Initialize the tool registry."""
        self._tools: dict[str, MCPTool] = {}
        self._categories: dict[str, list[str]] = {}

    def tool(
        self,
        name: str,
        description: str,
        category: str = "general",
        parameters: list[MCPToolParameter] | None = None,
    ) -> Callable[[Callable[..., MCPToolResult]], Callable[..., MCPToolResult]]:
        """
        Decorator to register a tool.

        Args:
            name: Tool name (unique identifier)
            description: Human-readable description
            category: Tool category for organization
            parameters: List of tool parameters

        Returns:
            Decorated function
        """

        def decorator(
            func: Callable[..., MCPToolResult],
        ) -> Callable[..., MCPToolResult]:
            # Create tool with handler
            tool = MCPTool(
                name=name,
                description=description,
                parameters=parameters or [],
                handler=func,
            )

            # Register tool
            self._tools[name] = tool

            # Add to category
            if category not in self._categories:
                self._categories[category] = []
            self._categories[category].append(name)

            return func

        return decorator

    def register(
        self,
        name: str,
        description: str,
        handler: Callable[..., MCPToolResult],
        parameters: list[MCPToolParameter] | None = None,
        category: str = "general",
    ) -> None:
        """
        Register a tool programmatically.

        Args:
            name: Tool name
            description: Tool description
            handler: Tool handler function
            parameters: Tool parameters
            category: Tool category
        """
        tool = MCPTool(
            name=name,
            description=description,
            parameters=parameters or [],
            handler=handler,
        )
        self._tools[name] = tool

        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(name)

    def get_tool(self, name: str) -> MCPTool | None:
        """Get a tool by name."""
        return self._tools.get(name)

    def get_all_tools(self) -> dict[str, MCPTool]:
        """Get all registered tools."""
        return self._tools.copy()

    def get_tools_by_category(self, category: str) -> list[MCPTool]:
        """Get all tools in a category."""
        tool_names = self._categories.get(category, [])
        return [self._tools[name] for name in tool_names if name in self._tools]

    def get_categories(self) -> list[str]:
        """Get all available categories."""
        return list(self._categories.keys())

    def list_tools(self) -> list[dict[str, Any]]:
        """
        List all tools with metadata.

        Returns:
            List of tool schemas
        """
        return [tool.to_schema() for tool in self._tools.values()]

    def get_tool_count(self) -> int:
        """Get total number of registered tools."""
        return len(self._tools)


class MCPServer:
    """
    MCP server for spreadsheet-dl.

    Exposes spreadsheet manipulation and budget analysis tools via MCP protocol,
    enabling natural language interaction with Claude Desktop and
    other MCP-compatible clients.

    Tools provided:
        Budget Analysis (8 tools):
            - analyze_budget: Analyze a budget file
            - add_expense: Add a new expense
            - query_budget: Answer natural language budget questions
            - get_spending_trends: Analyze spending patterns
            - compare_periods: Compare two time periods
            - generate_report: Generate formatted reports
            - list_categories: List expense categories
            - get_alerts: Check budget alerts

        Cell Operations (TASK-302):
            - cell_get, cell_set, cell_clear
            - cell_copy, cell_move
            - cell_batch_get, cell_batch_set
            - cell_find, cell_replace
            - cell_merge, cell_unmerge

        Style Operations (TASK-303):
            - style_list, style_get, style_create
            - style_update, style_delete, style_apply
            - format_cells, format_number
            - format_font, format_fill, format_border

        Structure Operations (TASK-304):
            - row_insert, row_delete, row_hide
            - column_insert, column_delete, column_hide
            - freeze_set, freeze_clear
            - sheet_create, sheet_delete, sheet_copy

        Advanced Tools (TASK-305):
            - chart_create, chart_update
            - validation_create, cf_create
            - named_range_create, table_create
            - query_select, query_find

    Example:
        >>> server = MCPServer()
        >>> server.run()  # Starts stdio-based MCP server
    """

    def __init__(
        self,
        config: MCPConfig | None = None,
    ) -> None:
        """
        Initialize MCP server.

        Args:
            config: Server configuration. Uses defaults if not provided.
        """
        self.config = config or MCPConfig()
        self.logger = logging.getLogger("spreadsheet-dl-mcp")
        self._registry = MCPToolRegistry()
        self._tools: dict[str, MCPTool] = {}
        self._request_count = 0
        self._last_reset = datetime.now()
        self._register_tools()

    def _register_tools(self) -> None:
        """Register all available tools."""
        # analyze_budget tool
        self._tools["analyze_budget"] = MCPTool(
            name="analyze_budget",
            description="Analyze a budget file and return spending summary with category breakdowns",
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to the ODS budget file",
                ),
                MCPToolParameter(
                    name="analysis_type",
                    type="string",
                    description="Type of analysis to perform",
                    required=False,
                    enum=["summary", "detailed", "trends", "categories"],
                    default="summary",
                ),
            ],
            handler=self._handle_analyze_budget,
        )

        # add_expense tool
        self._tools["add_expense"] = MCPTool(
            name="add_expense",
            description="Add a new expense to the budget file",
            parameters=[
                MCPToolParameter(
                    name="date",
                    type="string",
                    description="Expense date (YYYY-MM-DD format)",
                ),
                MCPToolParameter(
                    name="category",
                    type="string",
                    description="Expense category",
                ),
                MCPToolParameter(
                    name="description",
                    type="string",
                    description="Description of the expense",
                ),
                MCPToolParameter(
                    name="amount",
                    type="number",
                    description="Expense amount",
                ),
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to budget file (optional, uses most recent)",
                    required=False,
                ),
            ],
            handler=self._handle_add_expense,
        )

        # query_budget tool
        self._tools["query_budget"] = MCPTool(
            name="query_budget",
            description="Answer natural language questions about budget data",
            parameters=[
                MCPToolParameter(
                    name="question",
                    type="string",
                    description="Natural language question about the budget",
                ),
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to budget file",
                ),
            ],
            handler=self._handle_query_budget,
        )

        # get_spending_trends tool
        self._tools["get_spending_trends"] = MCPTool(
            name="get_spending_trends",
            description="Analyze spending trends over time",
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to budget file",
                ),
                MCPToolParameter(
                    name="period",
                    type="string",
                    description="Time period for trend analysis",
                    required=False,
                    enum=["week", "month", "quarter", "year"],
                    default="month",
                ),
                MCPToolParameter(
                    name="category",
                    type="string",
                    description="Specific category to analyze (optional)",
                    required=False,
                ),
            ],
            handler=self._handle_spending_trends,
        )

        # compare_periods tool
        self._tools["compare_periods"] = MCPTool(
            name="compare_periods",
            description="Compare spending between two time periods",
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to budget file",
                ),
                MCPToolParameter(
                    name="period1_start",
                    type="string",
                    description="Start date of first period (YYYY-MM-DD)",
                ),
                MCPToolParameter(
                    name="period1_end",
                    type="string",
                    description="End date of first period (YYYY-MM-DD)",
                ),
                MCPToolParameter(
                    name="period2_start",
                    type="string",
                    description="Start date of second period (YYYY-MM-DD)",
                ),
                MCPToolParameter(
                    name="period2_end",
                    type="string",
                    description="End date of second period (YYYY-MM-DD)",
                ),
            ],
            handler=self._handle_compare_periods,
        )

        # generate_report tool
        self._tools["generate_report"] = MCPTool(
            name="generate_report",
            description="Generate a formatted budget report",
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to budget file",
                ),
                MCPToolParameter(
                    name="format",
                    type="string",
                    description="Report format",
                    required=False,
                    enum=["text", "markdown", "json"],
                    default="markdown",
                ),
                MCPToolParameter(
                    name="include_recommendations",
                    type="boolean",
                    description="Include spending recommendations",
                    required=False,
                    default=True,
                ),
            ],
            handler=self._handle_generate_report,
        )

        # list_categories tool
        self._tools["list_categories"] = MCPTool(
            name="list_categories",
            description="List available expense categories",
            parameters=[],
            handler=self._handle_list_categories,
        )

        # get_alerts tool
        self._tools["get_alerts"] = MCPTool(
            name="get_alerts",
            description="Get budget alerts and warnings",
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to budget file",
                ),
                MCPToolParameter(
                    name="severity",
                    type="string",
                    description="Minimum alert severity",
                    required=False,
                    enum=["info", "warning", "critical"],
                    default="warning",
                ),
            ],
            handler=self._handle_get_alerts,
        )

        # =====================================================================
        # Cell Operation Tools (TASK-302)
        # =====================================================================

        # cell_get tool
        self._registry.register(
            name="cell_get",
            description="Get the value of a specific cell",
            handler=self._handle_cell_get,
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to the spreadsheet file",
                ),
                MCPToolParameter(
                    name="sheet",
                    type="string",
                    description="Sheet name",
                ),
                MCPToolParameter(
                    name="cell",
                    type="string",
                    description="Cell reference (e.g., 'A1', 'B5')",
                ),
            ],
            category="cell_operations",
        )

        # cell_set tool
        self._registry.register(
            name="cell_set",
            description="Set the value of a specific cell",
            handler=self._handle_cell_set,
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to the spreadsheet file",
                ),
                MCPToolParameter(
                    name="sheet",
                    type="string",
                    description="Sheet name",
                ),
                MCPToolParameter(
                    name="cell",
                    type="string",
                    description="Cell reference (e.g., 'A1', 'B5')",
                ),
                MCPToolParameter(
                    name="value",
                    type="string",
                    description="Value to set",
                ),
            ],
            category="cell_operations",
        )

        # cell_clear tool
        self._registry.register(
            name="cell_clear",
            description="Clear the value and formatting of a cell",
            handler=self._handle_cell_clear,
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to the spreadsheet file",
                ),
                MCPToolParameter(
                    name="sheet",
                    type="string",
                    description="Sheet name",
                ),
                MCPToolParameter(
                    name="cell",
                    type="string",
                    description="Cell reference (e.g., 'A1', 'B5')",
                ),
            ],
            category="cell_operations",
        )

        # cell_copy tool
        self._registry.register(
            name="cell_copy",
            description="Copy a cell or range to another location",
            handler=self._handle_cell_copy,
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to the spreadsheet file",
                ),
                MCPToolParameter(
                    name="sheet",
                    type="string",
                    description="Sheet name",
                ),
                MCPToolParameter(
                    name="source",
                    type="string",
                    description="Source cell/range (e.g., 'A1' or 'A1:B5')",
                ),
                MCPToolParameter(
                    name="destination",
                    type="string",
                    description="Destination cell/range",
                ),
            ],
            category="cell_operations",
        )

        # cell_move tool
        self._registry.register(
            name="cell_move",
            description="Move a cell or range to another location",
            handler=self._handle_cell_move,
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to the spreadsheet file",
                ),
                MCPToolParameter(
                    name="sheet",
                    type="string",
                    description="Sheet name",
                ),
                MCPToolParameter(
                    name="source",
                    type="string",
                    description="Source cell/range",
                ),
                MCPToolParameter(
                    name="destination",
                    type="string",
                    description="Destination cell/range",
                ),
            ],
            category="cell_operations",
        )

        # cell_batch_get tool
        self._registry.register(
            name="cell_batch_get",
            description="Get values of multiple cells in a single operation",
            handler=self._handle_cell_batch_get,
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to the spreadsheet file",
                ),
                MCPToolParameter(
                    name="sheet",
                    type="string",
                    description="Sheet name",
                ),
                MCPToolParameter(
                    name="cells",
                    type="string",
                    description="Comma-separated cell references or range (e.g., 'A1,B2,C3' or 'A1:C3')",
                ),
            ],
            category="cell_operations",
        )

        # cell_batch_set tool
        self._registry.register(
            name="cell_batch_set",
            description="Set values of multiple cells in a single operation",
            handler=self._handle_cell_batch_set,
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to the spreadsheet file",
                ),
                MCPToolParameter(
                    name="sheet",
                    type="string",
                    description="Sheet name",
                ),
                MCPToolParameter(
                    name="values",
                    type="string",
                    description="JSON object mapping cell references to values",
                ),
            ],
            category="cell_operations",
        )

        # cell_find tool
        self._registry.register(
            name="cell_find",
            description="Find cells containing specific text or matching a pattern",
            handler=self._handle_cell_find,
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to the spreadsheet file",
                ),
                MCPToolParameter(
                    name="sheet",
                    type="string",
                    description="Sheet name",
                ),
                MCPToolParameter(
                    name="search_text",
                    type="string",
                    description="Text to search for",
                ),
                MCPToolParameter(
                    name="match_case",
                    type="boolean",
                    description="Whether to match case",
                    required=False,
                    default=False,
                ),
            ],
            category="cell_operations",
        )

        # cell_replace tool
        self._registry.register(
            name="cell_replace",
            description="Find and replace text in cells",
            handler=self._handle_cell_replace,
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to the spreadsheet file",
                ),
                MCPToolParameter(
                    name="sheet",
                    type="string",
                    description="Sheet name",
                ),
                MCPToolParameter(
                    name="search_text",
                    type="string",
                    description="Text to search for",
                ),
                MCPToolParameter(
                    name="replace_text",
                    type="string",
                    description="Replacement text",
                ),
                MCPToolParameter(
                    name="match_case",
                    type="boolean",
                    description="Whether to match case",
                    required=False,
                    default=False,
                ),
            ],
            category="cell_operations",
        )

        # cell_merge tool
        self._registry.register(
            name="cell_merge",
            description="Merge a range of cells",
            handler=self._handle_cell_merge,
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to the spreadsheet file",
                ),
                MCPToolParameter(
                    name="sheet",
                    type="string",
                    description="Sheet name",
                ),
                MCPToolParameter(
                    name="range",
                    type="string",
                    description="Cell range to merge (e.g., 'A1:B5')",
                ),
            ],
            category="cell_operations",
        )

        # cell_unmerge tool
        self._registry.register(
            name="cell_unmerge",
            description="Unmerge a previously merged cell range",
            handler=self._handle_cell_unmerge,
            parameters=[
                MCPToolParameter(
                    name="file_path",
                    type="string",
                    description="Path to the spreadsheet file",
                ),
                MCPToolParameter(
                    name="sheet",
                    type="string",
                    description="Sheet name",
                ),
                MCPToolParameter(
                    name="cell",
                    type="string",
                    description="Any cell in the merged range",
                ),
            ],
            category="cell_operations",
        )

        # =====================================================================
        # Style Operation Tools (TASK-303)
        # =====================================================================

        style_tools = [
            ("style_list", "List all available styles in a spreadsheet"),
            ("style_get", "Get details of a specific style"),
            ("style_create", "Create a new style definition"),
            ("style_update", "Update an existing style"),
            ("style_delete", "Delete a style"),
            ("style_apply", "Apply a style to a cell or range"),
            ("format_cells", "Format cells with specific styling"),
            ("format_number", "Format cells as numbers with specific format"),
            ("format_font", "Apply font formatting to cells"),
            ("format_fill", "Apply fill/background color to cells"),
            ("format_border", "Apply borders to cells"),
        ]

        for tool_name, tool_desc in style_tools:
            self._registry.register(
                name=tool_name,
                description=tool_desc,
                handler=getattr(self, f"_handle_{tool_name}"),
                parameters=[
                    MCPToolParameter(
                        name="file_path",
                        type="string",
                        description="Path to the spreadsheet file",
                    ),
                    MCPToolParameter(
                        name="sheet",
                        type="string",
                        description="Sheet name",
                        required=tool_name
                        not in [
                            "style_list",
                            "style_get",
                            "style_create",
                            "style_update",
                            "style_delete",
                        ],
                    ),
                ],
                category="style_operations",
            )

        # =====================================================================
        # Structure Operation Tools (TASK-304)
        # =====================================================================

        structure_tools = [
            ("row_insert", "Insert a new row at a specified position"),
            ("row_delete", "Delete a row"),
            ("row_hide", "Hide a row"),
            ("column_insert", "Insert a new column at a specified position"),
            ("column_delete", "Delete a column"),
            ("column_hide", "Hide a column"),
            ("freeze_set", "Set freeze panes at a specified position"),
            ("freeze_clear", "Clear freeze panes"),
            ("sheet_create", "Create a new sheet"),
            ("sheet_delete", "Delete a sheet"),
            ("sheet_copy", "Copy a sheet"),
        ]

        for tool_name, tool_desc in structure_tools:
            self._registry.register(
                name=tool_name,
                description=tool_desc,
                handler=getattr(self, f"_handle_{tool_name}"),
                parameters=[
                    MCPToolParameter(
                        name="file_path",
                        type="string",
                        description="Path to the spreadsheet file",
                    ),
                    MCPToolParameter(
                        name="sheet",
                        type="string",
                        description="Sheet name",
                    ),
                ],
                category="structure_operations",
            )

        # =====================================================================
        # Advanced MCP Tools (TASK-305)
        # =====================================================================

        advanced_tools = [
            ("chart_create", "Create a new chart"),
            ("chart_update", "Update an existing chart"),
            ("validation_create", "Create data validation rules"),
            ("cf_create", "Create conditional formatting rules"),
            ("named_range_create", "Create a named range"),
            ("table_create", "Create a table from a range"),
            ("query_select", "Query and select data based on criteria"),
            ("query_find", "Find data matching specific conditions"),
        ]

        for tool_name, tool_desc in advanced_tools:
            self._registry.register(
                name=tool_name,
                description=tool_desc,
                handler=getattr(self, f"_handle_{tool_name}"),
                parameters=[
                    MCPToolParameter(
                        name="file_path",
                        type="string",
                        description="Path to the spreadsheet file",
                    ),
                    MCPToolParameter(
                        name="sheet",
                        type="string",
                        description="Sheet name",
                    ),
                ],
                category="advanced_operations",
            )

        # =====================================================================
        # Workbook Operation Tools (TASK-501)
        # =====================================================================

        workbook_tools = [
            ("workbook_properties_get", "Get workbook properties and metadata"),
            ("workbook_properties_set", "Set workbook properties"),
            ("workbook_metadata_get", "Get workbook metadata"),
            ("workbook_metadata_set", "Update workbook metadata"),
            ("workbook_protection_enable", "Enable workbook protection"),
            ("workbook_protection_disable", "Disable workbook protection"),
            ("formulas_recalculate", "Recalculate all formulas in workbook"),
            ("links_update", "Update external links"),
            ("links_break", "Break external links"),
            ("data_connections_list", "List data connections"),
            ("data_refresh", "Refresh data from external sources"),
            ("workbooks_compare", "Compare two workbooks"),
            ("workbooks_merge", "Merge multiple workbooks"),
            ("workbook_statistics", "Get workbook statistics"),
            ("formulas_audit", "Audit formulas for errors"),
            ("circular_refs_find", "Find circular references"),
        ]

        for tool_name, tool_desc in workbook_tools:
            self._registry.register(
                name=tool_name,
                description=tool_desc,
                handler=getattr(self, f"_handle_{tool_name}"),
                parameters=[
                    MCPToolParameter(
                        name="file_path",
                        type="string",
                        description="Path to the spreadsheet file",
                    ),
                ],
                category="workbook_operations",
            )

        # =====================================================================
        # Theme Management Tools (TASK-501)
        # =====================================================================

        theme_tools = [
            ("theme_list", "List all available themes"),
            ("theme_get", "Get details of a specific theme"),
            ("theme_create", "Create a new custom theme"),
            ("theme_update", "Update an existing theme"),
            ("theme_delete", "Delete a custom theme"),
            ("theme_apply", "Apply a theme to the workbook"),
            ("theme_export", "Export theme definition"),
            ("theme_import", "Import theme from file"),
            ("theme_preview", "Preview theme appearance"),
            ("color_scheme_generate", "Generate color scheme from base colors"),
            ("font_set_apply", "Apply font set to workbook"),
            ("style_guide_create", "Create comprehensive style guide"),
        ]

        for tool_name, tool_desc in theme_tools:
            self._registry.register(
                name=tool_name,
                description=tool_desc,
                handler=getattr(self, f"_handle_{tool_name}"),
                parameters=[
                    MCPToolParameter(
                        name="file_path",
                        type="string",
                        description="Path to the spreadsheet file",
                    ),
                ],
                category="theme_management",
            )

        # =====================================================================
        # Print Layout Tools (TASK-501)
        # =====================================================================

        print_tools = [
            ("page_setup", "Configure page setup and layout"),
            ("print_area_set", "Set print area for a sheet"),
            ("page_breaks_insert", "Insert manual page breaks"),
            ("page_breaks_remove", "Remove page breaks"),
            ("header_footer_set", "Set header and footer content"),
            ("print_titles_set", "Set rows/columns to repeat on each page"),
            ("print_options_set", "Configure print options"),
            ("pages_fit_to", "Fit content to specific number of pages"),
            ("print_preview", "Generate print preview"),
            ("pdf_export", "Export sheet to PDF"),
        ]

        for tool_name, tool_desc in print_tools:
            self._registry.register(
                name=tool_name,
                description=tool_desc,
                handler=getattr(self, f"_handle_{tool_name}"),
                parameters=[
                    MCPToolParameter(
                        name="file_path",
                        type="string",
                        description="Path to the spreadsheet file",
                    ),
                    MCPToolParameter(
                        name="sheet",
                        type="string",
                        description="Sheet name",
                    ),
                ],
                category="print_layout",
            )

        # =====================================================================
        # Import/Export Operation Tools (TASK-501)
        # =====================================================================

        import_export_tools = [
            ("csv_import", "Import data from CSV file"),
            ("tsv_import", "Import data from TSV file"),
            ("json_import", "Import data from JSON file"),
            ("xlsx_import", "Import data from XLSX file"),
            ("xml_import", "Import data from XML file"),
            ("html_import", "Import data from HTML table"),
            ("csv_export", "Export sheet to CSV format"),
            ("tsv_export", "Export sheet to TSV format"),
            ("json_export", "Export sheet to JSON format"),
            ("xlsx_export", "Export to XLSX format"),
            ("xml_export", "Export to XML format"),
            ("html_export", "Export to HTML table"),
            ("batch_import", "Batch import from multiple files"),
            ("batch_export", "Batch export to multiple formats"),
            ("data_mapping_create", "Create data mapping schema"),
            ("column_mapping_apply", "Apply column mapping during import"),
            ("format_auto_detect", "Auto-detect file format"),
        ]

        for tool_name, tool_desc in import_export_tools:
            self._registry.register(
                name=tool_name,
                description=tool_desc,
                handler=getattr(self, f"_handle_{tool_name}"),
                parameters=[
                    MCPToolParameter(
                        name="file_path",
                        type="string",
                        description="Path to the file",
                    ),
                ],
                category="import_export",
            )

        # =====================================================================
        # Account Operation Tools (TASK-501)
        # =====================================================================

        account_tools = [
            ("account_create", "Create a new financial account"),
            ("account_list", "List all accounts"),
            ("account_get", "Get account details"),
            ("account_update", "Update account information"),
            ("account_delete", "Delete an account"),
            ("account_balance", "Get current account balance"),
            ("account_transactions", "List account transactions"),
            ("account_reconcile", "Reconcile account with statement"),
            ("account_statement_import", "Import account statement"),
            ("account_statement_export", "Export account statement"),
            ("account_budgets", "Get budgets for account"),
            ("account_analysis", "Analyze account activity"),
            ("account_trends", "Get account spending trends"),
            ("account_categories", "List account categories"),
            ("account_tags", "Get account tags"),
        ]

        for tool_name, tool_desc in account_tools:
            self._registry.register(
                name=tool_name,
                description=tool_desc,
                handler=getattr(self, f"_handle_{tool_name}"),
                parameters=[
                    MCPToolParameter(
                        name="file_path",
                        type="string",
                        description="Path to the budget file",
                    ),
                ],
                category="account_operations",
            )

        # =====================================================================
        # Goal Tracking Tools (TASK-501)
        # =====================================================================

        goal_tools = [
            ("goal_create", "Create a new financial goal"),
            ("goal_list", "List all goals"),
            ("goal_get", "Get goal details"),
            ("goal_update", "Update goal information"),
            ("goal_delete", "Delete a goal"),
            ("goal_progress", "Get goal progress"),
            ("goal_milestones", "List goal milestones"),
            ("goal_projections", "Get goal projections"),
            ("debt_payoff_plan", "Generate debt payoff plan"),
            ("savings_plan", "Create savings plan"),
            ("investment_plan", "Create investment plan"),
            ("goal_dashboard", "Get goal tracking dashboard"),
        ]

        for tool_name, tool_desc in goal_tools:
            self._registry.register(
                name=tool_name,
                description=tool_desc,
                handler=getattr(self, f"_handle_{tool_name}"),
                parameters=[
                    MCPToolParameter(
                        name="file_path",
                        type="string",
                        description="Path to the budget file",
                    ),
                ],
                category="goal_tracking",
            )

        # =====================================================================
        # Reporting Tools (TASK-501)
        # =====================================================================

        reporting_tools = [
            # Note: "generate_report" already exists as a budget analysis tool
            ("report_schedule", "Schedule report generation"),
            ("report_list", "List available reports"),
            ("report_templates", "List report templates"),
            ("cash_flow_report", "Generate cash flow report"),
            ("income_statement", "Generate income statement"),
            ("balance_sheet", "Generate balance sheet"),
            ("budget_variance", "Generate budget variance report"),
            ("category_breakdown", "Generate category breakdown"),
            ("trend_analysis", "Perform trend analysis"),
            ("forecast", "Generate financial forecast"),
            ("what_if_analysis", "Perform what-if analysis"),
            ("report_export", "Export report to file"),
            ("report_email", "Email report to recipients"),
        ]

        for tool_name, tool_desc in reporting_tools:
            self._registry.register(
                name=tool_name,
                description=tool_desc,
                handler=getattr(self, f"_handle_{tool_name}"),
                parameters=[
                    MCPToolParameter(
                        name="file_path",
                        type="string",
                        description="Path to the budget file",
                    ),
                ],
                category="reporting",
            )

        # Update _tools from registry
        self._tools.update(self._registry.get_all_tools())

    def _validate_path(self, path: str | Path) -> Path:
        """
        Validate and resolve a file path.

        Args:
            path: Path to validate.

        Returns:
            Resolved Path object.

        Raises:
            MCPSecurityError: If path is not allowed.
            FileError: If file doesn't exist.
        """
        resolved = Path(path).resolve()

        # Check against allowed paths
        allowed = False
        for allowed_path in self.config.allowed_paths:
            try:
                resolved.relative_to(allowed_path.resolve())
                allowed = True
                break
            except ValueError:
                continue

        if not allowed:
            raise MCPSecurityError(
                f"Path not allowed: {path}. "
                f"Allowed paths: {[str(p) for p in self.config.allowed_paths]}"
            )

        if not resolved.exists():
            raise FileError(f"File not found: {resolved}")

        return resolved

    def _check_rate_limit(self) -> bool:
        """Check if rate limit is exceeded."""
        now = datetime.now()
        if (now - self._last_reset).seconds >= 60:
            self._request_count = 0
            self._last_reset = now

        self._request_count += 1
        return self._request_count <= self.config.rate_limit_per_minute

    def _log_audit(
        self,
        tool: str,
        params: dict[str, Any],
        result: MCPToolResult,
    ) -> None:
        """Log tool invocation for audit."""
        if not self.config.enable_audit_log:
            return

        entry = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool,
            "params": {k: str(v) for k, v in params.items()},
            "success": not result.is_error,
        }

        self.logger.info(json.dumps(entry))

        if self.config.audit_log_path:
            with open(self.config.audit_log_path, "a") as f:
                f.write(json.dumps(entry) + "\n")

    # =========================================================================
    # Tool Handlers
    # =========================================================================

    def _handle_analyze_budget(
        self,
        file_path: str,
        analysis_type: str = "summary",
    ) -> MCPToolResult:
        """Handle analyze_budget tool."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.domains.finance.budget_analyzer import BudgetAnalyzer

            analyzer = BudgetAnalyzer(path)
            summary = analyzer.get_summary()

            if analysis_type == "summary":
                return MCPToolResult.json(
                    {
                        "total_budget": float(summary.total_budget),
                        "total_spent": float(summary.total_spent),
                        "remaining": float(summary.total_remaining),
                        "percent_used": float(summary.percent_used),
                        "status": "under_budget"
                        if summary.total_remaining >= 0
                        else "over_budget",
                        "alerts": summary.alerts,
                    }
                )

            elif analysis_type == "detailed":
                by_category = analyzer.get_category_breakdown()
                return MCPToolResult.json(
                    {
                        "summary": {
                            "total_budget": float(summary.total_budget),
                            "total_spent": float(summary.total_spent),
                            "remaining": float(summary.total_remaining),
                            "percent_used": float(summary.percent_used),
                        },
                        "by_category": {
                            cat: float(amt) for cat, amt in by_category.items()
                        },
                        "transaction_count": len(analyzer.expenses),
                        "alerts": summary.alerts,
                    }
                )

            elif analysis_type == "categories":
                by_category = analyzer.get_category_breakdown()
                total = sum(by_category.values())
                return MCPToolResult.json(
                    {
                        "categories": [
                            {
                                "name": cat,
                                "amount": float(amt),
                                "percentage": float(amt / total * 100)
                                if total > 0
                                else 0,
                            }
                            for cat, amt in sorted(
                                by_category.items(),
                                key=lambda x: x[1],
                                reverse=True,
                            )
                        ]
                    }
                )

            else:
                return MCPToolResult.json(analyzer.to_dict())

        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_add_expense(
        self,
        date: str,
        category: str,
        description: str,
        amount: float,
        file_path: str | None = None,
    ) -> MCPToolResult:
        """Handle add_expense tool."""
        try:
            from datetime import date as date_type

            from spreadsheet_dl.ods_editor import OdsEditor
            from spreadsheet_dl.domains.finance.ods_generator import (
                ExpenseCategory,
                ExpenseEntry,
            )

            # Find or validate budget file
            if file_path:
                path = self._validate_path(file_path)
            else:
                # Find most recent budget file
                ods_files = list(Path.cwd().glob("budget_*.ods"))
                if not ods_files:
                    return MCPToolResult.error(
                        "No budget file found. Please specify file_path."
                    )
                path = max(ods_files, key=lambda p: p.stat().st_mtime)

            # Parse date
            expense_date = date_type.fromisoformat(date)

            # Parse category
            try:
                expense_category = ExpenseCategory(category)
            except ValueError:
                # Try case-insensitive match
                for cat in ExpenseCategory:
                    if cat.value.lower() == category.lower():
                        expense_category = cat
                        break
                else:
                    return MCPToolResult.error(
                        f"Invalid category: {category}. "
                        f"Valid: {[c.value for c in ExpenseCategory]}"
                    )

            # Create expense entry
            entry = ExpenseEntry(
                date=expense_date,
                category=expense_category,
                description=description,
                amount=Decimal(str(amount)),
            )

            # Append to file
            editor = OdsEditor(path)
            row_num = editor.append_expense(entry)
            editor.save()

            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "row": row_num,
                    "expense": {
                        "date": entry.date.isoformat(),
                        "category": entry.category.value,
                        "description": entry.description,
                        "amount": float(entry.amount),
                    },
                }
            )

        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_query_budget(
        self,
        question: str,
        file_path: str,
    ) -> MCPToolResult:
        """Handle query_budget tool with natural language questions."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.domains.finance.budget_analyzer import BudgetAnalyzer

            analyzer = BudgetAnalyzer(path)
            summary = analyzer.get_summary()
            by_category = analyzer.get_category_breakdown()

            # Parse question intent
            question_lower = question.lower()

            # Total spending questions
            if any(
                kw in question_lower
                for kw in ["total spent", "spend", "total spending"]
            ):
                return MCPToolResult.json(
                    {
                        "question": question,
                        "answer": f"Total spending is ${float(summary.total_spent):,.2f}",
                        "data": {"total_spent": float(summary.total_spent)},
                    }
                )

            # Remaining budget questions
            if any(kw in question_lower for kw in ["remaining", "left", "have left"]):
                return MCPToolResult.json(
                    {
                        "question": question,
                        "answer": f"Remaining budget is ${float(summary.total_remaining):,.2f}",
                        "data": {"remaining": float(summary.total_remaining)},
                    }
                )

            # Over budget questions
            if any(
                kw in question_lower for kw in ["over budget", "overspent", "exceeded"]
            ):
                [
                    cat
                    for cat, amt in by_category.items()
                    if amt > 0  # Simplified check
                ]
                return MCPToolResult.json(
                    {
                        "question": question,
                        "answer": f"Budget status: {summary.percent_used:.1f}% used",
                        "data": {
                            "percent_used": float(summary.percent_used),
                            "is_over": summary.total_remaining < 0,
                        },
                    }
                )

            # Category-specific questions
            for cat_name, cat_amount in by_category.items():
                if cat_name.lower() in question_lower:
                    return MCPToolResult.json(
                        {
                            "question": question,
                            "answer": f"Spending on {cat_name}: ${float(cat_amount):,.2f}",
                            "data": {
                                "category": cat_name,
                                "amount": float(cat_amount),
                            },
                        }
                    )

            # Default: return summary
            return MCPToolResult.json(
                {
                    "question": question,
                    "answer": (
                        f"Budget summary: ${float(summary.total_spent):,.2f} spent "
                        f"of ${float(summary.total_budget):,.2f} budget "
                        f"({summary.percent_used:.1f}% used)"
                    ),
                    "data": {
                        "total_budget": float(summary.total_budget),
                        "total_spent": float(summary.total_spent),
                        "remaining": float(summary.total_remaining),
                        "percent_used": float(summary.percent_used),
                    },
                }
            )

        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_spending_trends(
        self,
        file_path: str,
        period: str = "month",
        category: str | None = None,
    ) -> MCPToolResult:
        """Handle get_spending_trends tool."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.domains.finance.budget_analyzer import BudgetAnalyzer

            analyzer = BudgetAnalyzer(path)
            expenses = analyzer.expenses

            if expenses.empty:
                return MCPToolResult.json(
                    {
                        "message": "No expenses found",
                        "trends": [],
                    }
                )

            # Filter by category if specified
            if category:
                expenses = expenses[
                    expenses["Category"].str.lower() == category.lower()
                ]

            # Group by date
            if "Date" in expenses.columns:
                expenses["Date"] = expenses["Date"].astype(str)

            # Calculate trends
            daily_totals = expenses.groupby("Date")["Amount"].sum().to_dict()

            # Calculate statistics
            amounts = list(daily_totals.values())
            avg_daily = sum(amounts) / len(amounts) if amounts else 0
            max_day = (
                max(daily_totals.items(), key=lambda x: x[1])
                if daily_totals
                else (None, 0)
            )

            return MCPToolResult.json(
                {
                    "period": period,
                    "category": category,
                    "daily_spending": {
                        str(k): float(v) for k, v in daily_totals.items()
                    },
                    "statistics": {
                        "average_daily": float(avg_daily),
                        "highest_day": str(max_day[0]),
                        "highest_amount": float(max_day[1]),
                        "total_days": len(daily_totals),
                    },
                }
            )

        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_compare_periods(
        self,
        file_path: str,
        period1_start: str,
        period1_end: str,
        period2_start: str,
        period2_end: str,
    ) -> MCPToolResult:
        """Handle compare_periods tool."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.domains.finance.budget_analyzer import BudgetAnalyzer

            analyzer = BudgetAnalyzer(path)

            # Parse dates
            p1_start = date.fromisoformat(period1_start)
            p1_end = date.fromisoformat(period1_end)
            p2_start = date.fromisoformat(period2_start)
            p2_end = date.fromisoformat(period2_end)

            # Filter expenses for each period
            p1_expenses = analyzer.filter_by_date_range(p1_start, p1_end)
            p2_expenses = analyzer.filter_by_date_range(p2_start, p2_end)

            p1_total = (
                float(p1_expenses["Amount"].sum()) if not p1_expenses.empty else 0
            )
            p2_total = (
                float(p2_expenses["Amount"].sum()) if not p2_expenses.empty else 0
            )

            # Calculate change
            if p1_total > 0:
                change_pct = ((p2_total - p1_total) / p1_total) * 100
            else:
                change_pct = 100 if p2_total > 0 else 0

            return MCPToolResult.json(
                {
                    "period1": {
                        "start": period1_start,
                        "end": period1_end,
                        "total": p1_total,
                        "transaction_count": len(p1_expenses),
                    },
                    "period2": {
                        "start": period2_start,
                        "end": period2_end,
                        "total": p2_total,
                        "transaction_count": len(p2_expenses),
                    },
                    "comparison": {
                        "difference": p2_total - p1_total,
                        "percent_change": change_pct,
                        "trend": "increased"
                        if p2_total > p1_total
                        else "decreased"
                        if p2_total < p1_total
                        else "unchanged",
                    },
                }
            )

        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_generate_report(
        self,
        file_path: str,
        format: str = "markdown",
        include_recommendations: bool = True,
    ) -> MCPToolResult:
        """Handle generate_report tool."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.domains.finance.report_generator import ReportGenerator

            generator = ReportGenerator(path)

            if format == "json":
                data = generator.generate_visualization_data()
                if include_recommendations:
                    data["recommendations"] = self._generate_recommendations(path)
                return MCPToolResult.json(data)

            elif format == "markdown":
                report = generator.generate_markdown_report()
                if include_recommendations:
                    recs = self._generate_recommendations(path)
                    report += "\n\n## Recommendations\n\n"
                    for rec in recs:
                        report += f"- {rec}\n"
                return MCPToolResult.text(report)

            else:  # text
                report = generator.generate_text_report()
                return MCPToolResult.text(report)

        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_list_categories(self) -> MCPToolResult:
        """Handle list_categories tool."""
        try:
            from spreadsheet_dl.domains.finance.ods_generator import ExpenseCategory

            categories = [
                {"name": cat.value, "id": cat.name} for cat in ExpenseCategory
            ]
            return MCPToolResult.json({"categories": categories})

        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_get_alerts(
        self,
        file_path: str,
        severity: str = "warning",
    ) -> MCPToolResult:
        """Handle get_alerts tool."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.domains.finance.alerts import AlertMonitor
            from spreadsheet_dl.domains.finance.budget_analyzer import BudgetAnalyzer

            analyzer = BudgetAnalyzer(path)
            monitor = AlertMonitor(analyzer)
            alerts = monitor.check_all()

            # Filter by severity
            severity_order = ["info", "warning", "critical"]
            min_severity_idx = severity_order.index(severity.lower())

            filtered_alerts = [
                {
                    "message": a.message,
                    "category": a.category,
                    "severity": a.severity.value,
                    "value": float(a.amount) if a.amount else None,
                    "threshold": float(a.threshold) if a.threshold else None,
                }
                for a in alerts
                if severity_order.index(a.severity.value) >= min_severity_idx
            ]

            return MCPToolResult.json(
                {
                    "total_alerts": len(filtered_alerts),
                    "alerts": filtered_alerts,
                }
            )

        except Exception as e:
            return MCPToolResult.error(str(e))

    def _generate_recommendations(self, path: Path) -> list[str]:
        """Generate spending recommendations."""
        try:
            from spreadsheet_dl.domains.finance.budget_analyzer import BudgetAnalyzer

            analyzer = BudgetAnalyzer(path)
            summary = analyzer.get_summary()
            by_category = analyzer.get_category_breakdown()

            recommendations = []

            # Check if over budget
            if summary.total_remaining < 0:
                recommendations.append(
                    f"You are ${abs(float(summary.total_remaining)):,.2f} over budget. "
                    "Consider reducing discretionary spending."
                )

            # Check percentage used
            if summary.percent_used > 80:
                recommendations.append(
                    f"You've used {summary.percent_used:.1f}% of your budget. "
                    "Be cautious with remaining spending."
                )

            # Find highest spending category
            if by_category:
                highest_cat = max(by_category.items(), key=lambda x: x[1])
                total = sum(by_category.values())
                pct = (highest_cat[1] / total * 100) if total > 0 else 0
                if pct > 30:
                    recommendations.append(
                        f"{highest_cat[0]} represents {pct:.1f}% of your spending. "
                        "Consider reviewing expenses in this category."
                    )

            if not recommendations:
                recommendations.append(
                    "Your spending appears to be on track. Keep it up!"
                )

            return recommendations

        except Exception:
            return []

    # =========================================================================
    # Cell Operation Handlers (TASK-302)
    # =========================================================================

    def _handle_cell_get(
        self,
        file_path: str,
        sheet: str,
        cell: str,
    ) -> MCPToolResult:
        """Get the value of a specific cell."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.ods_editor import OdsEditor

            editor = OdsEditor(path)
            value = editor.get_cell_value(sheet, cell)

            return MCPToolResult.json(
                {
                    "cell": cell,
                    "sheet": sheet,
                    "value": value,
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_cell_set(
        self,
        file_path: str,
        sheet: str,
        cell: str,
        value: str,
    ) -> MCPToolResult:
        """Set the value of a specific cell."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.ods_editor import OdsEditor

            editor = OdsEditor(path)
            editor.set_cell_value(sheet, cell, value)
            editor.save()

            return MCPToolResult.json(
                {
                    "success": True,
                    "cell": cell,
                    "sheet": sheet,
                    "value": value,
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_cell_clear(
        self,
        file_path: str,
        sheet: str,
        cell: str,
    ) -> MCPToolResult:
        """Clear the value and formatting of a cell."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.ods_editor import OdsEditor

            editor = OdsEditor(path)
            editor.clear_cell(sheet, cell)
            editor.save()

            return MCPToolResult.json(
                {
                    "success": True,
                    "cell": cell,
                    "sheet": sheet,
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_cell_copy(
        self,
        file_path: str,
        sheet: str,
        source: str,
        destination: str,
    ) -> MCPToolResult:
        """Copy a cell or range to another location."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.ods_editor import OdsEditor

            editor = OdsEditor(path)
            editor.copy_cells(sheet, source, destination)
            editor.save()

            return MCPToolResult.json(
                {
                    "success": True,
                    "source": source,
                    "destination": destination,
                    "sheet": sheet,
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_cell_move(
        self,
        file_path: str,
        sheet: str,
        source: str,
        destination: str,
    ) -> MCPToolResult:
        """Move a cell or range to another location."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.ods_editor import OdsEditor

            editor = OdsEditor(path)
            editor.move_cells(sheet, source, destination)
            editor.save()

            return MCPToolResult.json(
                {
                    "success": True,
                    "source": source,
                    "destination": destination,
                    "sheet": sheet,
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_cell_batch_get(
        self,
        file_path: str,
        sheet: str,
        cells: str,
    ) -> MCPToolResult:
        """Get values of multiple cells in a single operation."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.ods_editor import OdsEditor

            editor = OdsEditor(path)

            # Parse cells - can be comma-separated cells or a range
            if ":" in cells:
                # It's a range
                start, end = editor._parse_range(cells)
                cell_list = []
                for row in range(start[0], end[0] + 1):
                    for col in range(start[1], end[1] + 1):
                        col_letter = editor._col_index_to_letter(col)
                        cell_list.append(f"{col_letter}{row + 1}")
            else:
                # Comma-separated cells
                cell_list = [c.strip() for c in cells.split(",")]

            # Get values for all cells
            values = {}
            for cell_ref in cell_list:
                value = editor.get_cell_value(sheet, cell_ref)
                values[cell_ref] = value

            return MCPToolResult.json(
                {
                    "cells": cell_list,
                    "sheet": sheet,
                    "values": values,
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_cell_batch_set(
        self,
        file_path: str,
        sheet: str,
        values: str,
    ) -> MCPToolResult:
        """Set values of multiple cells in a single operation."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.ods_editor import OdsEditor

            editor = OdsEditor(path)
            values_dict = json.loads(values)

            # Set each cell value
            for cell_ref, value in values_dict.items():
                editor.set_cell_value(sheet, cell_ref, value)

            editor.save()

            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "cells_updated": len(values_dict),
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_cell_find(
        self,
        file_path: str,
        sheet: str,
        search_text: str,
        match_case: bool = False,
    ) -> MCPToolResult:
        """Find cells containing specific text or matching a pattern."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.ods_editor import OdsEditor

            editor = OdsEditor(path)
            matches = editor.find_cells(sheet, search_text, match_case)

            # Convert matches to JSON-serializable format
            match_list = [
                {"cell": cell_ref, "value": value} for cell_ref, value in matches
            ]

            return MCPToolResult.json(
                {
                    "search_text": search_text,
                    "sheet": sheet,
                    "match_case": match_case,
                    "matches": match_list,
                    "count": len(match_list),
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_cell_replace(
        self,
        file_path: str,
        sheet: str,
        search_text: str,
        replace_text: str,
        match_case: bool = False,
    ) -> MCPToolResult:
        """Find and replace text in cells."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.ods_editor import OdsEditor

            editor = OdsEditor(path)
            count = editor.replace_cells(sheet, search_text, replace_text, match_case)
            editor.save()

            return MCPToolResult.json(
                {
                    "success": True,
                    "search_text": search_text,
                    "replace_text": replace_text,
                    "sheet": sheet,
                    "match_case": match_case,
                    "replacements": count,
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_cell_merge(
        self,
        file_path: str,
        sheet: str,
        range: str,
    ) -> MCPToolResult:
        """Merge a range of cells."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.ods_editor import OdsEditor

            editor = OdsEditor(path)
            sheet_obj = editor.get_sheet(sheet)

            # Parse range
            start, end = editor._parse_range(range)
            rows_to_span = end[0] - start[0] + 1
            cols_to_span = end[1] - start[1] + 1

            # Ensure the cell exists by setting an empty value if needed
            cell = editor._get_cell(sheet_obj, start[0], start[1])
            if cell is None:
                # Create the cell by setting an empty value
                editor._set_cell_value(sheet_obj, start[0], start[1], "")
                cell = editor._get_cell(sheet_obj, start[0], start[1])

            if cell is not None:
                # Set merge attributes
                if rows_to_span > 1:
                    cell.setAttribute("numberrowsspanned", str(rows_to_span))
                if cols_to_span > 1:
                    cell.setAttribute("numbercolumnsspanned", str(cols_to_span))

                editor.save()

                return MCPToolResult.json(
                    {
                        "success": True,
                        "range": range,
                        "sheet": sheet,
                        "rows_spanned": rows_to_span,
                        "cols_spanned": cols_to_span,
                    }
                )
            else:
                return MCPToolResult.error(f"Cell not found at range start: {range}")

        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_cell_unmerge(
        self,
        file_path: str,
        sheet: str,
        cell: str,
    ) -> MCPToolResult:
        """Unmerge a previously merged cell range."""
        try:
            path = self._validate_path(file_path)

            from spreadsheet_dl.ods_editor import OdsEditor

            editor = OdsEditor(path)
            sheet_obj = editor.get_sheet(sheet)

            # Parse cell reference
            row, col = editor._parse_cell_reference(cell)

            # Get the cell
            cell_obj = editor._get_cell(sheet_obj, row, col)

            if cell_obj is not None:
                # Remove merge attributes (suppress exception if they don't exist)
                with contextlib.suppress(Exception):
                    cell_obj.removeAttribute("numberrowsspanned")
                with contextlib.suppress(Exception):
                    cell_obj.removeAttribute("numbercolumnsspanned")

                editor.save()

                return MCPToolResult.json(
                    {
                        "success": True,
                        "cell": cell,
                        "sheet": sheet,
                    }
                )
            else:
                return MCPToolResult.error(f"Cell not found: {cell}")

        except Exception as e:
            return MCPToolResult.error(str(e))

    # =========================================================================
    # Style Operation Handlers (TASK-303)
    # =========================================================================

    def _handle_style_list(
        self, file_path: str, sheet: str | None = None
    ) -> MCPToolResult:
        """List all available styles."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {"styles": [], "message": "Style listing not yet implemented"}
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_style_get(
        self, file_path: str, sheet: str | None = None
    ) -> MCPToolResult:
        """Get details of a specific style."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {"style": {}, "message": "Style retrieval not yet implemented"}
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_style_create(
        self, file_path: str, sheet: str | None = None
    ) -> MCPToolResult:
        """Create a new style definition."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {"success": True, "message": "Style creation not yet implemented"}
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_style_update(
        self, file_path: str, sheet: str | None = None
    ) -> MCPToolResult:
        """Update an existing style."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {"success": True, "message": "Style update not yet implemented"}
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_style_delete(
        self, file_path: str, sheet: str | None = None
    ) -> MCPToolResult:
        """Delete a style."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {"success": True, "message": "Style deletion not yet implemented"}
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_style_apply(self, file_path: str, sheet: str) -> MCPToolResult:
        """Apply a style to a cell or range."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Style application not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_format_cells(self, file_path: str, sheet: str) -> MCPToolResult:
        """Format cells with specific styling."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Cell formatting not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_format_number(self, file_path: str, sheet: str) -> MCPToolResult:
        """Format cells as numbers with specific format."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Number formatting not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_format_font(self, file_path: str, sheet: str) -> MCPToolResult:
        """Apply font formatting to cells."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Font formatting not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_format_fill(self, file_path: str, sheet: str) -> MCPToolResult:
        """Apply fill/background color to cells."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Fill formatting not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_format_border(self, file_path: str, sheet: str) -> MCPToolResult:
        """Apply borders to cells."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Border formatting not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    # =========================================================================
    # Structure Operation Handlers (TASK-304)
    # =========================================================================

    def _handle_row_insert(self, file_path: str, sheet: str) -> MCPToolResult:
        """Insert a new row at a specified position."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Row insertion not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_row_delete(self, file_path: str, sheet: str) -> MCPToolResult:
        """Delete a row."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Row deletion not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_row_hide(self, file_path: str, sheet: str) -> MCPToolResult:
        """Hide a row."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Row hiding not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_column_insert(self, file_path: str, sheet: str) -> MCPToolResult:
        """Insert a new column at a specified position."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Column insertion not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_column_delete(self, file_path: str, sheet: str) -> MCPToolResult:
        """Delete a column."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Column deletion not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_column_hide(self, file_path: str, sheet: str) -> MCPToolResult:
        """Hide a column."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Column hiding not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_freeze_set(self, file_path: str, sheet: str) -> MCPToolResult:
        """Set freeze panes at a specified position."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Freeze panes not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_freeze_clear(self, file_path: str, sheet: str) -> MCPToolResult:
        """Clear freeze panes."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Freeze clear not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_sheet_create(self, file_path: str, sheet: str) -> MCPToolResult:
        """Create a new sheet."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Sheet creation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_sheet_delete(self, file_path: str, sheet: str) -> MCPToolResult:
        """Delete a sheet."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Sheet deletion not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_sheet_copy(self, file_path: str, sheet: str) -> MCPToolResult:
        """Copy a sheet."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Sheet copying not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    # =========================================================================
    # Advanced Operation Handlers (TASK-305)
    # =========================================================================

    def _handle_chart_create(self, file_path: str, sheet: str) -> MCPToolResult:
        """Create a new chart."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Chart creation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_chart_update(self, file_path: str, sheet: str) -> MCPToolResult:
        """Update an existing chart."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Chart update not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_validation_create(self, file_path: str, sheet: str) -> MCPToolResult:
        """Create data validation rules."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Validation creation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_cf_create(self, file_path: str, sheet: str) -> MCPToolResult:
        """Create conditional formatting rules."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Conditional formatting not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_named_range_create(self, file_path: str, sheet: str) -> MCPToolResult:
        """Create a named range."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Named range creation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_table_create(self, file_path: str, sheet: str) -> MCPToolResult:
        """Create a table from a range."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "success": True,
                    "sheet": sheet,
                    "message": "Table creation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_query_select(self, file_path: str, sheet: str) -> MCPToolResult:
        """Query and select data based on criteria."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "results": [],
                    "sheet": sheet,
                    "message": "Query select not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_query_find(self, file_path: str, sheet: str) -> MCPToolResult:
        """Find data matching specific conditions."""
        try:
            path = self._validate_path(file_path)  # noqa: F841
            return MCPToolResult.json(
                {
                    "results": [],
                    "sheet": sheet,
                    "message": "Query find not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    # =========================================================================
    # Workbook Operation Handlers (TASK-501)
    # =========================================================================

    def _handle_workbook_properties_get(self, file_path: str) -> MCPToolResult:
        """
        Get workbook properties and metadata.

        TASK-501: Stub implementation.
        Returns schema for workbook properties.

        Args:
            file_path: Path to spreadsheet file

        Returns:
            Workbook properties
        """
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "properties": {
                        "title": "Untitled",
                        "author": "",
                        "created": "",
                        "modified": "",
                    },
                    "message": "Stub: Full implementation pending",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_workbook_properties_set(self, file_path: str) -> MCPToolResult:
        """Set workbook properties. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "message": "Stub: Property setting not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_workbook_metadata_get(self, file_path: str) -> MCPToolResult:
        """Get workbook metadata. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "metadata": {},
                    "message": "Stub: Metadata retrieval not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_workbook_metadata_set(self, file_path: str) -> MCPToolResult:
        """Update workbook metadata. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "message": "Stub: Metadata update not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_workbook_protection_enable(self, file_path: str) -> MCPToolResult:
        """Enable workbook protection. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "protected": True,
                    "message": "Stub: Protection not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_workbook_protection_disable(self, file_path: str) -> MCPToolResult:
        """Disable workbook protection. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "protected": False,
                    "message": "Stub: Protection removal not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_formulas_recalculate(self, file_path: str) -> MCPToolResult:
        """Recalculate all formulas. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "formulas_recalculated": 0,
                    "message": "Stub: Formula recalculation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_links_update(self, file_path: str) -> MCPToolResult:
        """Update external links. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "links_updated": 0,
                    "message": "Stub: Link update not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_links_break(self, file_path: str) -> MCPToolResult:
        """Break external links. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "links_broken": 0,
                    "message": "Stub: Link breaking not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_data_connections_list(self, file_path: str) -> MCPToolResult:
        """List data connections. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "connections": [],
                    "message": "Stub: Connection listing not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_data_refresh(self, file_path: str) -> MCPToolResult:
        """Refresh data from external sources. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "refreshed": 0,
                    "message": "Stub: Data refresh not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_workbooks_compare(self, file_path: str) -> MCPToolResult:
        """Compare two workbooks. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "differences": [],
                    "message": "Stub: Workbook comparison not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_workbooks_merge(self, file_path: str) -> MCPToolResult:
        """Merge multiple workbooks. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "merged_count": 0,
                    "message": "Stub: Workbook merging not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_workbook_statistics(self, file_path: str) -> MCPToolResult:
        """Get workbook statistics. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "statistics": {
                        "sheets": 0,
                        "cells": 0,
                        "formulas": 0,
                    },
                    "message": "Stub: Statistics calculation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_formulas_audit(self, file_path: str) -> MCPToolResult:
        """Audit formulas for errors. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "errors": [],
                    "warnings": [],
                    "message": "Stub: Formula auditing not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_circular_refs_find(self, file_path: str) -> MCPToolResult:
        """Find circular references. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "circular_refs": [],
                    "message": "Stub: Circular reference detection not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    # =========================================================================
    # Theme Management Handlers (TASK-501)
    # =========================================================================

    def _handle_theme_list(self, file_path: str) -> MCPToolResult:
        """List all available themes. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "themes": ["Default", "Office", "Modern"],
                    "message": "Stub: Theme listing not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_theme_get(self, file_path: str) -> MCPToolResult:
        """Get theme details. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "theme": {},
                    "message": "Stub: Theme retrieval not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_theme_create(self, file_path: str) -> MCPToolResult:
        """Create a new custom theme. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "theme_id": "custom_1",
                    "message": "Stub: Theme creation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_theme_update(self, file_path: str) -> MCPToolResult:
        """Update an existing theme. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "message": "Stub: Theme update not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_theme_delete(self, file_path: str) -> MCPToolResult:
        """Delete a custom theme. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "message": "Stub: Theme deletion not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_theme_apply(self, file_path: str) -> MCPToolResult:
        """Apply a theme to the workbook. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "message": "Stub: Theme application not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_theme_export(self, file_path: str) -> MCPToolResult:
        """Export theme definition. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "export_path": "",
                    "message": "Stub: Theme export not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_theme_import(self, file_path: str) -> MCPToolResult:
        """Import theme from file. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "theme_id": "",
                    "message": "Stub: Theme import not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_theme_preview(self, file_path: str) -> MCPToolResult:
        """Preview theme appearance. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "preview": {},
                    "message": "Stub: Theme preview not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_color_scheme_generate(self, file_path: str) -> MCPToolResult:
        """Generate color scheme from base colors. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "color_scheme": {},
                    "message": "Stub: Color scheme generation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_font_set_apply(self, file_path: str) -> MCPToolResult:
        """Apply font set to workbook. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "message": "Stub: Font set application not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_style_guide_create(self, file_path: str) -> MCPToolResult:
        """Create comprehensive style guide. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "style_guide": {},
                    "message": "Stub: Style guide creation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    # =========================================================================
    # Print Layout Handlers (TASK-501)
    # =========================================================================

    def _handle_page_setup(self, file_path: str, sheet: str) -> MCPToolResult:
        """Configure page setup and layout. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "sheet": sheet,
                    "message": "Stub: Page setup not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_print_area_set(self, file_path: str, sheet: str) -> MCPToolResult:
        """Set print area for a sheet. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "sheet": sheet,
                    "message": "Stub: Print area setting not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_page_breaks_insert(self, file_path: str, sheet: str) -> MCPToolResult:
        """Insert manual page breaks. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "sheet": sheet,
                    "message": "Stub: Page break insertion not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_page_breaks_remove(self, file_path: str, sheet: str) -> MCPToolResult:
        """Remove page breaks. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "sheet": sheet,
                    "message": "Stub: Page break removal not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_header_footer_set(self, file_path: str, sheet: str) -> MCPToolResult:
        """Set header and footer content. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "sheet": sheet,
                    "message": "Stub: Header/footer setting not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_print_titles_set(self, file_path: str, sheet: str) -> MCPToolResult:
        """Set rows/columns to repeat on each page. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "sheet": sheet,
                    "message": "Stub: Print titles not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_print_options_set(self, file_path: str, sheet: str) -> MCPToolResult:
        """Configure print options. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "sheet": sheet,
                    "message": "Stub: Print options not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_pages_fit_to(self, file_path: str, sheet: str) -> MCPToolResult:
        """Fit content to specific number of pages. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "sheet": sheet,
                    "message": "Stub: Fit to pages not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_print_preview(self, file_path: str, sheet: str) -> MCPToolResult:
        """Generate print preview. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "sheet": sheet,
                    "preview": {},
                    "message": "Stub: Print preview not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_pdf_export(self, file_path: str, sheet: str) -> MCPToolResult:
        """Export sheet to PDF. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "sheet": sheet,
                    "pdf_path": "",
                    "message": "Stub: PDF export not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    # =========================================================================
    # Import/Export Handlers (TASK-501)
    # =========================================================================

    def _handle_csv_import(self, file_path: str) -> MCPToolResult:
        """Import data from CSV file. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "rows_imported": 0,
                    "message": "Stub: CSV import not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_tsv_import(self, file_path: str) -> MCPToolResult:
        """Import data from TSV file. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "rows_imported": 0,
                    "message": "Stub: TSV import not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_json_import(self, file_path: str) -> MCPToolResult:
        """Import data from JSON file. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "records_imported": 0,
                    "message": "Stub: JSON import not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_xlsx_import(self, file_path: str) -> MCPToolResult:
        """Import data from XLSX file. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "sheets_imported": 0,
                    "message": "Stub: XLSX import not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_xml_import(self, file_path: str) -> MCPToolResult:
        """Import data from XML file. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "records_imported": 0,
                    "message": "Stub: XML import not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_html_import(self, file_path: str) -> MCPToolResult:
        """Import data from HTML table. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "tables_imported": 0,
                    "message": "Stub: HTML import not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_csv_export(self, file_path: str) -> MCPToolResult:
        """Export sheet to CSV format. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "export_path": "",
                    "message": "Stub: CSV export not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_tsv_export(self, file_path: str) -> MCPToolResult:
        """Export sheet to TSV format. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "export_path": "",
                    "message": "Stub: TSV export not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_json_export(self, file_path: str) -> MCPToolResult:
        """Export sheet to JSON format. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "export_path": "",
                    "message": "Stub: JSON export not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_xlsx_export(self, file_path: str) -> MCPToolResult:
        """Export to XLSX format. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "export_path": "",
                    "message": "Stub: XLSX export not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_xml_export(self, file_path: str) -> MCPToolResult:
        """Export to XML format. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "export_path": "",
                    "message": "Stub: XML export not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_html_export(self, file_path: str) -> MCPToolResult:
        """Export to HTML table. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "export_path": "",
                    "message": "Stub: HTML export not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_batch_import(self, file_path: str) -> MCPToolResult:
        """Batch import from multiple files. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "files_imported": 0,
                    "message": "Stub: Batch import not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_batch_export(self, file_path: str) -> MCPToolResult:
        """Batch export to multiple formats. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "files_exported": 0,
                    "message": "Stub: Batch export not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_data_mapping_create(self, file_path: str) -> MCPToolResult:
        """Create data mapping schema. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "mapping": {},
                    "message": "Stub: Data mapping not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_column_mapping_apply(self, file_path: str) -> MCPToolResult:
        """Apply column mapping during import. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "message": "Stub: Column mapping not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_format_auto_detect(self, file_path: str) -> MCPToolResult:
        """Auto-detect file format. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "detected_format": "unknown",
                    "message": "Stub: Format detection not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    # =========================================================================
    # Account Operation Handlers (TASK-501)
    # =========================================================================

    def _handle_account_create(self, file_path: str) -> MCPToolResult:
        """Create a new financial account. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "account_id": "acc_1",
                    "message": "Stub: Account creation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_list(self, file_path: str) -> MCPToolResult:
        """List all accounts. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "accounts": [],
                    "message": "Stub: Account listing not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_get(self, file_path: str) -> MCPToolResult:
        """Get account details. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "account": {},
                    "message": "Stub: Account retrieval not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_update(self, file_path: str) -> MCPToolResult:
        """Update account information. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "message": "Stub: Account update not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_delete(self, file_path: str) -> MCPToolResult:
        """Delete an account. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "message": "Stub: Account deletion not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_balance(self, file_path: str) -> MCPToolResult:
        """Get current account balance. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "balance": 0.0,
                    "message": "Stub: Balance calculation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_transactions(self, file_path: str) -> MCPToolResult:
        """List account transactions. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "transactions": [],
                    "message": "Stub: Transaction listing not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_reconcile(self, file_path: str) -> MCPToolResult:
        """Reconcile account with statement. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "reconciled": False,
                    "message": "Stub: Account reconciliation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_statement_import(self, file_path: str) -> MCPToolResult:
        """Import account statement. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "transactions_imported": 0,
                    "message": "Stub: Statement import not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_statement_export(self, file_path: str) -> MCPToolResult:
        """Export account statement. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "export_path": "",
                    "message": "Stub: Statement export not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_budgets(self, file_path: str) -> MCPToolResult:
        """Get budgets for account. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "budgets": [],
                    "message": "Stub: Account budgets not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_analysis(self, file_path: str) -> MCPToolResult:
        """Analyze account activity. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "analysis": {},
                    "message": "Stub: Account analysis not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_trends(self, file_path: str) -> MCPToolResult:
        """Get account spending trends. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "trends": {},
                    "message": "Stub: Account trends not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_categories(self, file_path: str) -> MCPToolResult:
        """List account categories. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "categories": [],
                    "message": "Stub: Category listing not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_account_tags(self, file_path: str) -> MCPToolResult:
        """Get account tags. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "tags": [],
                    "message": "Stub: Tag listing not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    # =========================================================================
    # Goal Tracking Handlers (TASK-501)
    # =========================================================================

    def _handle_goal_create(self, file_path: str) -> MCPToolResult:
        """Create a new financial goal. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "goal_id": "goal_1",
                    "message": "Stub: Goal creation not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_goal_list(self, file_path: str) -> MCPToolResult:
        """List all goals. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "goals": [],
                    "message": "Stub: Goal listing not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_goal_get(self, file_path: str) -> MCPToolResult:
        """Get goal details. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "goal": {},
                    "message": "Stub: Goal retrieval not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_goal_update(self, file_path: str) -> MCPToolResult:
        """Update goal information. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "message": "Stub: Goal update not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_goal_delete(self, file_path: str) -> MCPToolResult:
        """Delete a goal. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "message": "Stub: Goal deletion not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_goal_progress(self, file_path: str) -> MCPToolResult:
        """Get goal progress. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "progress": 0.0,
                    "message": "Stub: Goal progress tracking not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_goal_milestones(self, file_path: str) -> MCPToolResult:
        """List goal milestones. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "milestones": [],
                    "message": "Stub: Goal milestones not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_goal_projections(self, file_path: str) -> MCPToolResult:
        """Get goal projections. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "projections": {},
                    "message": "Stub: Goal projections not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_debt_payoff_plan(self, file_path: str) -> MCPToolResult:
        """Generate debt payoff plan. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "plan": {},
                    "message": "Stub: Debt payoff planning not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_savings_plan(self, file_path: str) -> MCPToolResult:
        """Create savings plan. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "plan": {},
                    "message": "Stub: Savings planning not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_investment_plan(self, file_path: str) -> MCPToolResult:
        """Create investment plan. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "plan": {},
                    "message": "Stub: Investment planning not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_goal_dashboard(self, file_path: str) -> MCPToolResult:
        """Get goal tracking dashboard. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "dashboard": {},
                    "message": "Stub: Goal dashboard not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    # =========================================================================
    # Reporting Handlers (TASK-501)
    # =========================================================================

    def _handle_report_schedule(self, file_path: str) -> MCPToolResult:
        """Schedule report generation. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "schedule_id": "sched_1",
                    "message": "Stub: Report scheduling not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_report_list(self, file_path: str) -> MCPToolResult:
        """List available reports. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "reports": [],
                    "message": "Stub: Report listing not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_report_templates(self, file_path: str) -> MCPToolResult:
        """List report templates. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "templates": [],
                    "message": "Stub: Report templates not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_cash_flow_report(self, file_path: str) -> MCPToolResult:
        """Generate cash flow report. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "report": {},
                    "message": "Stub: Cash flow report not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_income_statement(self, file_path: str) -> MCPToolResult:
        """Generate income statement. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "statement": {},
                    "message": "Stub: Income statement not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_balance_sheet(self, file_path: str) -> MCPToolResult:
        """Generate balance sheet. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "balance_sheet": {},
                    "message": "Stub: Balance sheet not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_budget_variance(self, file_path: str) -> MCPToolResult:
        """Generate budget variance report. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "variance": {},
                    "message": "Stub: Budget variance not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_category_breakdown(self, file_path: str) -> MCPToolResult:
        """Generate category breakdown. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "breakdown": {},
                    "message": "Stub: Category breakdown not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_trend_analysis(self, file_path: str) -> MCPToolResult:
        """Perform trend analysis. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "trends": {},
                    "message": "Stub: Trend analysis not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_forecast(self, file_path: str) -> MCPToolResult:
        """Generate financial forecast. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "forecast": {},
                    "message": "Stub: Financial forecasting not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_what_if_analysis(self, file_path: str) -> MCPToolResult:
        """Perform what-if analysis. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "scenarios": {},
                    "message": "Stub: What-if analysis not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_report_export(self, file_path: str) -> MCPToolResult:
        """Export report to file. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "export_path": "",
                    "message": "Stub: Report export not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    def _handle_report_email(self, file_path: str) -> MCPToolResult:
        """Email report to recipients. TASK-501: Stub implementation."""
        try:
            path = self._validate_path(file_path)
            return MCPToolResult.json(
                {
                    "success": True,
                    "file": str(path),
                    "sent": False,
                    "message": "Stub: Report emailing not yet implemented",
                }
            )
        except Exception as e:
            return MCPToolResult.error(str(e))

    # =========================================================================
    # MCP Protocol Methods
    # =========================================================================

    def handle_message(self, message: dict[str, Any]) -> dict[str, Any] | None:
        """
        Handle an incoming MCP message.

        Args:
            message: JSON-RPC message.

        Returns:
            JSON-RPC response or None for notifications.
        """
        msg_id = message.get("id")
        method = message.get("method", "")
        params = message.get("params", {})

        try:
            # Rate limiting
            if not self._check_rate_limit():
                return self._error_response(
                    msg_id,
                    -32000,
                    "Rate limit exceeded",
                )

            # Route method
            if method == "initialize":
                return self._handle_initialize(msg_id, params)
            elif method == "tools/list":
                return self._handle_tools_list(msg_id)
            elif method == "tools/call":
                return self._handle_tools_call(msg_id, params)
            elif method == "notifications/initialized":
                return None  # No response for notifications
            else:
                return self._error_response(
                    msg_id,
                    -32601,
                    f"Method not found: {method}",
                )

        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
            return self._error_response(msg_id, -32603, str(e))

    def _handle_initialize(
        self,
        msg_id: Any,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Handle initialize request."""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": MCPVersion.V1.value,
                "serverInfo": {
                    "name": self.config.name,
                    "version": self.config.version,
                },
                "capabilities": {
                    "tools": {},
                    "logging": {},
                },
            },
        }

    def _handle_tools_list(self, msg_id: Any) -> dict[str, Any]:
        """Handle tools/list request."""
        tools = [tool.to_schema() for tool in self._tools.values()]
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": tools},
        }

    def _handle_tools_call(
        self,
        msg_id: Any,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Handle tools/call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name not in self._tools:
            return self._error_response(
                msg_id,
                -32602,
                f"Unknown tool: {tool_name}",
            )

        tool = self._tools[tool_name]
        if tool.handler is None:
            return self._error_response(
                msg_id,
                -32603,
                f"Tool has no handler: {tool_name}",
            )

        # Execute tool
        result = tool.handler(**arguments)

        # Audit log
        self._log_audit(tool_name, arguments, result)

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": result.content,
                "isError": result.is_error,
            },
        }

    def _error_response(
        self,
        msg_id: Any,
        code: int,
        message: str,
    ) -> dict[str, Any]:
        """Create an error response."""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": code,
                "message": message,
            },
        }

    def run(self) -> None:
        """
        Run the MCP server in stdio mode.

        Reads JSON-RPC messages from stdin and writes responses to stdout.
        """
        self.logger.info(f"Starting MCP server: {self.config.name}")

        while True:
            try:
                # Read message length
                line = sys.stdin.readline()
                if not line:
                    break

                # Parse JSON-RPC message
                message = json.loads(line)

                # Handle message
                response = self.handle_message(message)

                # Send response (if not a notification)
                if response is not None:
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()

            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON: {e}")
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"Server error: {e}")
                break

        self.logger.info("MCP server stopped")


def create_mcp_server(
    allowed_paths: list[str | Path] | None = None,
) -> MCPServer:
    """
    Create an MCP server with optional path restrictions.

    Args:
        allowed_paths: List of paths the server can access.

    Returns:
        Configured MCPServer instance.
    """
    config = MCPConfig(
        allowed_paths=[Path(p) for p in allowed_paths] if allowed_paths else [],
    )
    return MCPServer(config)


def main() -> None:
    """Entry point for MCP server CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description="SpreadsheetDL MCP Server",
    )
    parser.add_argument(
        "--allowed-paths",
        nargs="*",
        help="Allowed file paths",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    # Configure logging
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stderr,
    )

    # Create and run server
    server = create_mcp_server(args.allowed_paths)
    server.run()


if __name__ == "__main__":
    main()
