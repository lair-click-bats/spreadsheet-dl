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
        return cls(content=[{
            "type": "text",
            "text": json.dumps(data, indent=2, default=str),
        }])

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


class MCPServer:
    """
    MCP server for spreadsheet-dl.

    Exposes budget analysis and management tools via MCP protocol,
    enabling natural language interaction with Claude Desktop and
    other MCP-compatible clients.

    Tools provided:
        - analyze_budget: Analyze a budget file
        - add_expense: Add a new expense
        - query_budget: Answer natural language budget questions
        - get_spending_trends: Analyze spending patterns
        - compare_periods: Compare two time periods
        - generate_report: Generate formatted reports
        - list_categories: List expense categories
        - get_alerts: Check budget alerts

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

            from spreadsheet_dl.budget_analyzer import BudgetAnalyzer

            analyzer = BudgetAnalyzer(path)
            summary = analyzer.get_summary()

            if analysis_type == "summary":
                return MCPToolResult.json({
                    "total_budget": float(summary.total_budget),
                    "total_spent": float(summary.total_spent),
                    "remaining": float(summary.total_remaining),
                    "percent_used": float(summary.percent_used),
                    "status": "under_budget" if summary.total_remaining >= 0 else "over_budget",
                    "alerts": summary.alerts,
                })

            elif analysis_type == "detailed":
                by_category = analyzer.by_category()
                return MCPToolResult.json({
                    "summary": {
                        "total_budget": float(summary.total_budget),
                        "total_spent": float(summary.total_spent),
                        "remaining": float(summary.total_remaining),
                        "percent_used": float(summary.percent_used),
                    },
                    "by_category": {
                        cat: float(amt) for cat, amt in by_category.items()
                    },
                    "transaction_count": len(analyzer.get_expenses()),
                    "alerts": summary.alerts,
                })

            elif analysis_type == "categories":
                by_category = analyzer.by_category()
                total = sum(by_category.values())
                return MCPToolResult.json({
                    "categories": [
                        {
                            "name": cat,
                            "amount": float(amt),
                            "percentage": float(amt / total * 100) if total > 0 else 0,
                        }
                        for cat, amt in sorted(
                            by_category.items(),
                            key=lambda x: x[1],
                            reverse=True,
                        )
                    ]
                })

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
            from spreadsheet_dl.ods_generator import ExpenseCategory, ExpenseEntry

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

            return MCPToolResult.json({
                "success": True,
                "file": str(path),
                "row": row_num,
                "expense": {
                    "date": entry.date.isoformat(),
                    "category": entry.category.value,
                    "description": entry.description,
                    "amount": float(entry.amount),
                },
            })

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

            from spreadsheet_dl.budget_analyzer import BudgetAnalyzer

            analyzer = BudgetAnalyzer(path)
            summary = analyzer.get_summary()
            by_category = analyzer.by_category()

            # Parse question intent
            question_lower = question.lower()

            # Total spending questions
            if any(kw in question_lower for kw in ["total spent", "spend", "total spending"]):
                return MCPToolResult.json({
                    "question": question,
                    "answer": f"Total spending is ${float(summary.total_spent):,.2f}",
                    "data": {"total_spent": float(summary.total_spent)},
                })

            # Remaining budget questions
            if any(kw in question_lower for kw in ["remaining", "left", "have left"]):
                return MCPToolResult.json({
                    "question": question,
                    "answer": f"Remaining budget is ${float(summary.total_remaining):,.2f}",
                    "data": {"remaining": float(summary.total_remaining)},
                })

            # Over budget questions
            if any(kw in question_lower for kw in ["over budget", "overspent", "exceeded"]):
                [
                    cat for cat, amt in by_category.items()
                    if amt > 0  # Simplified check
                ]
                return MCPToolResult.json({
                    "question": question,
                    "answer": f"Budget status: {summary.percent_used:.1f}% used",
                    "data": {
                        "percent_used": float(summary.percent_used),
                        "is_over": summary.total_remaining < 0,
                    },
                })

            # Category-specific questions
            for cat_name, cat_amount in by_category.items():
                if cat_name.lower() in question_lower:
                    return MCPToolResult.json({
                        "question": question,
                        "answer": f"Spending on {cat_name}: ${float(cat_amount):,.2f}",
                        "data": {
                            "category": cat_name,
                            "amount": float(cat_amount),
                        },
                    })

            # Default: return summary
            return MCPToolResult.json({
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
            })

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

            from spreadsheet_dl.budget_analyzer import BudgetAnalyzer

            analyzer = BudgetAnalyzer(path)
            expenses = analyzer.get_expenses()

            if expenses.empty:
                return MCPToolResult.json({
                    "message": "No expenses found",
                    "trends": [],
                })

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
            max_day = max(daily_totals.items(), key=lambda x: x[1]) if daily_totals else (None, 0)

            return MCPToolResult.json({
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
            })

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

            from spreadsheet_dl.budget_analyzer import BudgetAnalyzer

            analyzer = BudgetAnalyzer(path)

            # Parse dates
            p1_start = date.fromisoformat(period1_start)
            p1_end = date.fromisoformat(period1_end)
            p2_start = date.fromisoformat(period2_start)
            p2_end = date.fromisoformat(period2_end)

            # Filter expenses for each period
            p1_expenses = analyzer.filter_by_date_range(p1_start, p1_end)
            p2_expenses = analyzer.filter_by_date_range(p2_start, p2_end)

            p1_total = float(p1_expenses["Amount"].sum()) if not p1_expenses.empty else 0
            p2_total = float(p2_expenses["Amount"].sum()) if not p2_expenses.empty else 0

            # Calculate change
            if p1_total > 0:
                change_pct = ((p2_total - p1_total) / p1_total) * 100
            else:
                change_pct = 100 if p2_total > 0 else 0

            return MCPToolResult.json({
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
                    "trend": "increased" if p2_total > p1_total else "decreased" if p2_total < p1_total else "unchanged",
                },
            })

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

            from spreadsheet_dl.report_generator import ReportGenerator

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
            from spreadsheet_dl.ods_generator import ExpenseCategory

            categories = [
                {"name": cat.value, "id": cat.name}
                for cat in ExpenseCategory
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

            from spreadsheet_dl.alerts import AlertMonitor
            from spreadsheet_dl.budget_analyzer import BudgetAnalyzer

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
                    "value": float(a.current_value) if a.current_value else None,
                    "threshold": float(a.threshold) if a.threshold else None,
                }
                for a in alerts
                if severity_order.index(a.severity.value) >= min_severity_idx
            ]

            return MCPToolResult.json({
                "total_alerts": len(filtered_alerts),
                "alerts": filtered_alerts,
            })

        except Exception as e:
            return MCPToolResult.error(str(e))

    def _generate_recommendations(self, path: Path) -> list[str]:
        """Generate spending recommendations."""
        try:
            from spreadsheet_dl.budget_analyzer import BudgetAnalyzer

            analyzer = BudgetAnalyzer(path)
            summary = analyzer.get_summary()
            by_category = analyzer.by_category()

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
                recommendations.append("Your spending appears to be on track. Keep it up!")

            return recommendations

        except Exception:
            return []

    # =========================================================================
    # MCP Protocol Methods
    # =========================================================================

    def handle_message(self, message: dict[str, Any]) -> dict[str, Any]:
        """
        Handle an incoming MCP message.

        Args:
            message: JSON-RPC message.

        Returns:
            JSON-RPC response.
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
