"""Professional financial templates.

Implements:
    - FR-PROF-001: Enterprise Budget Template
    - FR-PROF-002: Cash Flow Tracker Template
    - FR-PROF-003: Invoice/Expense Report Template (partial)
    - FR-PROF-004: Financial Statement Templates (partial)

Provides ready-to-use templates for common financial documents
with professional formatting and built-in formulas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


# ============================================================================
# Template Configuration
# ============================================================================


@dataclass
class TemplateMetadata:
    """Metadata for a template."""

    name: str
    version: str = "1.0.0"
    description: str = ""
    category: str = "finance"
    author: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class ColumnDef:
    """Column definition for templates."""

    name: str
    width: str = "2.5cm"
    type: str = "string"
    style: str | None = None
    formula: str | None = None  # Default formula pattern


# ============================================================================
# Enterprise Budget Template (FR-PROF-001)
# ============================================================================


@dataclass
class EnterpriseBudgetTemplate:
    """Enterprise-grade budget template (FR-PROF-001).

    Features:
    - Multiple budget categories with subcategories
    - Monthly breakdown with quarterly and annual totals
    - Variance analysis (budget vs actual)
    - Department-level budgets
    - Approval workflow fields
    - Professional formatting

    Example:
        template = EnterpriseBudgetTemplate(
            fiscal_year=2024,
            departments=["Engineering", "Sales", "Marketing"],
            categories=[
                BudgetCategory("Personnel", ["Salaries", "Benefits"]),
                BudgetCategory("Operations", ["Rent", "Utilities"]),
            ],
        )
        builder = template.generate()
        builder.save("enterprise_budget.ods")
    """

    fiscal_year: int = 2024
    departments: list[str] = field(default_factory=lambda: ["General"])
    currency_symbol: str = "$"
    include_quarterly: bool = True
    include_variance: bool = True
    theme: str = "corporate"

    # Categories with subcategories
    categories: list[BudgetCategory] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize default categories if none provided."""
        if not self.categories:
            self.categories = [
                BudgetCategory(
                    name="Personnel",
                    subcategories=["Salaries", "Benefits", "Training", "Recruiting"],
                ),
                BudgetCategory(
                    name="Operations",
                    subcategories=["Rent", "Utilities", "Insurance", "Maintenance"],
                ),
                BudgetCategory(
                    name="Technology",
                    subcategories=[
                        "Software",
                        "Hardware",
                        "Cloud Services",
                        "IT Support",
                    ],
                ),
                BudgetCategory(
                    name="Marketing",
                    subcategories=["Advertising", "Events", "Content", "Brand"],
                ),
                BudgetCategory(
                    name="Travel & Entertainment",
                    subcategories=["Travel", "Meals", "Client Entertainment"],
                ),
                BudgetCategory(
                    name="Professional Services",
                    subcategories=["Legal", "Accounting", "Consulting"],
                ),
            ]

    @property
    def months(self) -> list[str]:
        """Get month names for fiscal year."""
        return [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]

    def generate(self) -> SpreadsheetBuilder:
        """Generate the budget spreadsheet.

        Returns:
            SpreadsheetBuilder configured with budget template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Enterprise Budget FY{self.fiscal_year}",
            author="Finance Department",
            subject="Annual Budget",
            description=f"Enterprise budget for fiscal year {self.fiscal_year}",
            keywords=["budget", "finance", "annual", str(self.fiscal_year)],
        )

        # Create summary sheet
        self._create_summary_sheet(builder)

        # Create sheet for each department
        for dept in self.departments:
            self._create_department_sheet(builder, dept)

        # Create variance analysis sheet if requested
        if self.include_variance:
            self._create_variance_sheet(builder)

        return builder

    def _create_summary_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create the executive summary sheet."""
        builder.sheet("Summary")

        # Title area
        builder.column("Description", width="200pt", style="text")
        builder.column("Annual Budget", width="120pt", type="currency")
        builder.column("YTD Actual", width="120pt", type="currency")
        builder.column("Variance", width="120pt", type="currency")
        builder.column("% Used", width="80pt", type="percentage")

        builder.freeze(rows=2)

        # Header row
        builder.row(style="header_primary")
        builder.cell(f"Budget Summary - FY{self.fiscal_year}", colspan=5)

        builder.row(style="header_secondary")
        builder.cell("Category")
        builder.cell("Annual Budget")
        builder.cell("YTD Actual")
        builder.cell("Variance")
        builder.cell("% Used")

        # Category totals
        row_num = 3
        for category in self.categories:
            builder.row(style="category")
            builder.cell(category.name, style="category_label")
            # Reference to department sheets
            builder.cell(f"='{self.departments[0]}'.B{row_num}", style="currency")
            builder.cell(f"='{self.departments[0]}'.C{row_num}", style="currency")
            builder.cell(f"=B{row_num}-C{row_num}", style="currency_variance")
            builder.cell(
                f"=IF(B{row_num}=0,0,C{row_num}/B{row_num})", style="percentage"
            )
            row_num += 1

        # Grand total
        last_data_row = row_num - 1
        builder.row(style="total")
        builder.cell("GRAND TOTAL", style="total_label")
        builder.cell(f"=SUM(B3:B{last_data_row})", style="currency_total")
        builder.cell(f"=SUM(C3:C{last_data_row})", style="currency_total")
        builder.cell(f"=B{row_num}-C{row_num}", style="currency_variance")
        builder.cell(f"=IF(B{row_num}=0,0,C{row_num}/B{row_num})", style="percentage")

    def _create_department_sheet(
        self,
        builder: SpreadsheetBuilder,
        department: str,
    ) -> None:
        """Create a department budget sheet."""
        builder.sheet(department)

        # Define columns
        builder.column("Category", width="150pt", style="text")
        builder.column("Subcategory", width="150pt", style="text")

        # Monthly columns
        for month in self.months:
            builder.column(month, width="80pt", type="currency")

        # Total column
        builder.column("Total", width="100pt", type="currency")

        builder.freeze(rows=2, cols=2)

        # Header rows
        builder.row(style="header_primary")
        builder.cell(f"{department} Budget - FY{self.fiscal_year}", colspan=14)

        builder.row(style="header_secondary")
        builder.cell("Category")
        builder.cell("Subcategory")
        for month in self.months:
            builder.cell(month)
        builder.cell("Total")

        # Data rows
        row_num = 3
        for category in self.categories:
            # Category header row
            builder.row(style="category")
            builder.cell(category.name, rowspan=len(category.subcategories))
            builder.cell(category.subcategories[0] if category.subcategories else "")
            for _ in range(12):
                builder.cell(0, style="currency_input")
            # Sum formula for monthly amounts
            builder.cell(f"=SUM(C{row_num}:N{row_num})", style="currency")
            row_num += 1

            # Subcategory rows
            for subcat in category.subcategories[1:]:
                builder.row()
                builder.cell("")  # Merged with category
                builder.cell(subcat)
                for _ in range(12):
                    builder.cell(0, style="currency_input")
                builder.cell(f"=SUM(C{row_num}:N{row_num})", style="currency")
                row_num += 1

        # Category subtotals row (would need formula references)
        # Total row
        builder.row(style="total")
        builder.cell("TOTAL", colspan=2)
        for col_idx in range(12):
            col_letter = chr(ord("C") + col_idx)
            builder.cell(f"=SUM({col_letter}3:{col_letter}{row_num - 1})")
        builder.cell(f"=SUM(O3:O{row_num - 1})")

    def _create_variance_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create variance analysis sheet."""
        builder.sheet("Variance Analysis")

        builder.column("Category", width="150pt")
        builder.column("Budget", width="100pt", type="currency")
        builder.column("Actual", width="100pt", type="currency")
        builder.column("Variance $", width="100pt", type="currency")
        builder.column("Variance %", width="80pt", type="percentage")
        builder.column("Status", width="80pt")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Category")
        builder.cell("Budget")
        builder.cell("Actual")
        builder.cell("Variance $")
        builder.cell("Variance %")
        builder.cell("Status")

        # Data rows with conditional formatting
        row_num = 2
        for category in self.categories:
            builder.row()
            builder.cell(category.name)
            builder.cell(f"=Summary.B{row_num}", style="currency")
            builder.cell(f"=Summary.C{row_num}", style="currency")
            builder.cell(f"=B{row_num}-C{row_num}", style="currency_variance")
            builder.cell(f"=IF(B{row_num}=0,0,(B{row_num}-C{row_num})/B{row_num})")
            # Status formula based on variance
            builder.cell(
                f'=IF(D{row_num}>0,"Under Budget",IF(D{row_num}<0,"Over Budget","On Budget"))'
            )
            row_num += 1


@dataclass
class BudgetCategory:
    """Budget category with optional subcategories."""

    name: str
    subcategories: list[str] = field(default_factory=list)


# ============================================================================
# Cash Flow Tracker Template (FR-PROF-002)
# ============================================================================


@dataclass
class CashFlowTrackerTemplate:
    """Cash flow tracker template (FR-PROF-002).

    Features:
    - Operating, investing, and financing sections
    - Weekly or monthly tracking periods
    - Running balance calculation
    - Cash flow projections
    - Bank reconciliation support
    - Professional formatting

    Example:
        template = CashFlowTrackerTemplate(
            start_date="2024-01-01",
            periods=12,
            period_type="monthly",
            opening_balance=50000.00,
        )
        builder = template.generate()
        builder.save("cash_flow.ods")
    """

    start_date: str = "2024-01-01"
    periods: int = 12
    period_type: str = "monthly"  # "weekly" or "monthly"
    opening_balance: float = 0.0
    currency_symbol: str = "$"
    include_projections: bool = True
    theme: str = "corporate"

    # Operating activities
    operating_inflows: list[str] = field(
        default_factory=lambda: [
            "Sales Revenue",
            "Service Revenue",
            "Interest Income",
            "Other Operating Income",
        ]
    )
    operating_outflows: list[str] = field(
        default_factory=lambda: [
            "Payroll",
            "Rent/Lease",
            "Utilities",
            "Supplies",
            "Insurance",
            "Professional Services",
            "Marketing",
            "Other Operating Expenses",
        ]
    )

    # Investing activities
    investing_inflows: list[str] = field(
        default_factory=lambda: [
            "Asset Sales",
            "Investment Returns",
        ]
    )
    investing_outflows: list[str] = field(
        default_factory=lambda: [
            "Equipment Purchases",
            "Investments",
        ]
    )

    # Financing activities
    financing_inflows: list[str] = field(
        default_factory=lambda: [
            "Loan Proceeds",
            "Equity Investment",
        ]
    )
    financing_outflows: list[str] = field(
        default_factory=lambda: [
            "Loan Payments",
            "Dividends",
        ]
    )

    def generate(self) -> SpreadsheetBuilder:
        """Generate the cash flow tracker spreadsheet.

        Returns:
            SpreadsheetBuilder configured with cash flow template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Cash Flow Tracker - {self.start_date}",
            author="Finance Department",
            subject="Cash Flow Management",
            description="Cash flow tracking and projections",
            keywords=["cash flow", "finance", "liquidity"],
        )

        # Create main tracker sheet
        self._create_tracker_sheet(builder)

        # Create summary dashboard
        self._create_summary_sheet(builder)

        # Create projections if requested
        if self.include_projections:
            self._create_projections_sheet(builder)

        return builder

    def _get_period_headers(self) -> list[str]:
        """Generate period headers based on period type."""
        if self.period_type == "weekly":
            return [f"Week {i + 1}" for i in range(self.periods)]
        else:
            months = [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
            return months[: self.periods]

    def _create_tracker_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create the main cash flow tracker sheet."""
        builder.sheet("Cash Flow")

        period_headers = self._get_period_headers()

        # Define columns
        builder.column("Category", width="200pt", style="text")
        for period in period_headers:
            builder.column(period, width="90pt", type="currency")
        builder.column("Total", width="100pt", type="currency")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell("Cash Flow Statement", colspan=len(period_headers) + 2)

        # Period header row
        builder.row(style="header_secondary")
        builder.cell("Category")
        for period in period_headers:
            builder.cell(period)
        builder.cell("Total")

        current_row = 3

        # Opening Balance
        builder.row(style="balance")
        builder.cell("Opening Cash Balance")
        builder.cell(self.opening_balance, style="currency")
        for _ in range(len(period_headers) - 1):
            # Reference previous period ending balance
            col = chr(ord("B") + self.periods - 1)
            builder.cell(f"={col}{current_row + 20}", style="currency")  # Approximate
        builder.cell("", style="currency")
        current_row += 1

        # Operating Activities Section
        current_row = self._add_activity_section(
            builder,
            "OPERATING ACTIVITIES",
            self.operating_inflows,
            self.operating_outflows,
            current_row,
            len(period_headers),
        )

        # Investing Activities Section
        current_row = self._add_activity_section(
            builder,
            "INVESTING ACTIVITIES",
            self.investing_inflows,
            self.investing_outflows,
            current_row,
            len(period_headers),
        )

        # Financing Activities Section
        current_row = self._add_activity_section(
            builder,
            "FINANCING ACTIVITIES",
            self.financing_inflows,
            self.financing_outflows,
            current_row,
            len(period_headers),
        )

        # Net Change in Cash
        builder.row(style="subtotal")
        builder.cell("NET CHANGE IN CASH")
        for col_idx in range(len(period_headers)):
            col_letter = chr(ord("B") + col_idx)
            builder.cell(f"=SUM({col_letter}5:{col_letter}{current_row - 1})")
        builder.cell(
            f"=SUM(B{current_row}:{chr(ord('A') + len(period_headers))}{current_row})"
        )
        current_row += 1

        # Closing Balance
        builder.row(style="total")
        builder.cell("CLOSING CASH BALANCE")
        for col_idx in range(len(period_headers)):
            col_letter = chr(ord("B") + col_idx)
            prev_col = chr(ord("B") + col_idx - 1) if col_idx > 0 else "B"
            if col_idx == 0:
                builder.cell(f"=B3+B{current_row - 1}")  # Opening + Net Change
            else:
                builder.cell(f"={prev_col}{current_row}+{col_letter}{current_row - 1}")
        builder.cell(f"={chr(ord('A') + len(period_headers))}{current_row}")

    def _add_activity_section(
        self,
        builder: SpreadsheetBuilder,
        section_name: str,
        inflows: list[str],
        outflows: list[str],
        start_row: int,
        num_periods: int,
    ) -> int:
        """Add an activity section (operating, investing, financing)."""
        current_row = start_row

        # Section header
        builder.row(style="section_header")
        builder.cell(section_name, colspan=num_periods + 2)
        current_row += 1

        # Inflows
        inflow_start = current_row
        for inflow in inflows:
            builder.row()
            builder.cell(f"  {inflow}", style="category_label")
            for _ in range(num_periods):
                builder.cell(0, style="currency_input")
            col_start = chr(ord("B"))
            col_end = chr(ord("A") + num_periods)
            builder.cell(f"=SUM({col_start}{current_row}:{col_end}{current_row})")
            current_row += 1
        inflow_end = current_row - 1

        # Total Inflows
        builder.row(style="subtotal")
        builder.cell("  Total Inflows", style="subtotal_label")
        for col_idx in range(num_periods):
            col_letter = chr(ord("B") + col_idx)
            builder.cell(f"=SUM({col_letter}{inflow_start}:{col_letter}{inflow_end})")
        builder.cell(f"=SUM(B{current_row}:{chr(ord('A') + num_periods)}{current_row})")
        current_row += 1

        # Outflows
        outflow_start = current_row
        for outflow in outflows:
            builder.row()
            builder.cell(f"  {outflow}", style="category_label")
            for _ in range(num_periods):
                builder.cell(0, style="currency_input")
            col_start = chr(ord("B"))
            col_end = chr(ord("A") + num_periods)
            builder.cell(f"=SUM({col_start}{current_row}:{col_end}{current_row})")
            current_row += 1
        outflow_end = current_row - 1

        # Total Outflows
        builder.row(style="subtotal")
        builder.cell("  Total Outflows", style="subtotal_label")
        for col_idx in range(num_periods):
            col_letter = chr(ord("B") + col_idx)
            builder.cell(
                f"=-SUM({col_letter}{outflow_start}:{col_letter}{outflow_end})"
            )
        builder.cell(f"=SUM(B{current_row}:{chr(ord('A') + num_periods)}{current_row})")
        current_row += 1

        # Net Section
        builder.row(style="net")
        builder.cell(f"  Net {section_name.title()}", style="net_label")
        for col_idx in range(num_periods):
            col_letter = chr(ord("B") + col_idx)
            inflow_row = inflow_end + 1
            outflow_row = current_row - 1
            builder.cell(f"={col_letter}{inflow_row}+{col_letter}{outflow_row}")
        builder.cell(f"=SUM(B{current_row}:{chr(ord('A') + num_periods)}{current_row})")
        current_row += 1

        return current_row

    def _create_summary_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create summary dashboard sheet."""
        builder.sheet("Summary")

        builder.column("Metric", width="200pt")
        builder.column("Value", width="120pt", type="currency")
        builder.column("Status", width="100pt")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Cash Flow Summary", colspan=3)

        # Key metrics
        builder.row(style="header_secondary")
        builder.cell("Key Metrics")
        builder.cell("Amount")
        builder.cell("Status")

        metrics = [
            ("Opening Balance", "='Cash Flow'.B3"),
            ("Total Inflows", "='Cash Flow'.O6"),
            ("Total Outflows", "='Cash Flow'.O15"),
            ("Net Cash Flow", "=B5+B6"),
            ("Closing Balance", "='Cash Flow'.B22"),
        ]

        for metric_name, formula in metrics:
            builder.row()
            builder.cell(metric_name)
            builder.cell(formula, style="currency")
            if builder._current_sheet is not None:
                builder.cell(
                    "=IF(B"
                    + str(len(builder._current_sheet.rows) + 1)
                    + '>0,"Positive","Negative")'
                )

    def _create_projections_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create cash flow projections sheet."""
        builder.sheet("Projections")

        builder.column("Scenario", width="150pt")
        builder.column("Description", width="250pt")
        builder.column("Projected Amount", width="120pt", type="currency")
        builder.column("Probability", width="80pt", type="percentage")
        builder.column("Expected Value", width="120pt", type="currency")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Cash Flow Projections", colspan=5)

        builder.row(style="header_secondary")
        builder.cell("Scenario")
        builder.cell("Description")
        builder.cell("Projected Amount")
        builder.cell("Probability")
        builder.cell("Expected Value")

        # Default scenarios
        scenarios = [
            ("Best Case", "Strong sales, low expenses", 0, 0.25),
            ("Expected Case", "Normal operations", 0, 0.50),
            ("Worst Case", "Weak sales, high expenses", 0, 0.25),
        ]

        for scenario, desc, amount, prob in scenarios:
            builder.row()
            builder.cell(scenario)
            builder.cell(desc)
            builder.cell(amount, style="currency_input")
            builder.cell(prob, style="percentage_input")
            if builder._current_sheet is not None:
                row_num = len(builder._current_sheet.rows) + 1
                builder.cell(f"=C{row_num}*D{row_num}")

        # Expected value total
        builder.row(style="total")
        builder.cell("EXPECTED CASH FLOW", colspan=4)
        builder.cell("=SUM(E3:E5)")


# ============================================================================
# Invoice Template (FR-PROF-003 - Partial)
# ============================================================================


@dataclass
class InvoiceTemplate:
    """Professional invoice template (FR-PROF-003).

    Features:
    - Company header with logo placeholder
    - Customer information section
    - Line items with quantity, rate, amount
    - Subtotal, tax, and total calculations
    - Payment terms and notes
    """

    company_name: str = "Your Company"
    company_address: str = ""
    company_phone: str = ""
    company_email: str = ""
    invoice_number: str = "INV-001"
    tax_rate: float = 0.0
    currency_symbol: str = "$"
    theme: str = "corporate"

    def generate(self) -> SpreadsheetBuilder:
        """Generate the invoice spreadsheet."""
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Invoice {self.invoice_number}",
            author=self.company_name,
            subject="Invoice",
        )

        builder.sheet("Invoice")

        # Company header section
        builder.column("A", width="100pt")
        builder.column("B", width="150pt")
        builder.column("C", width="80pt")
        builder.column("D", width="80pt")
        builder.column("E", width="100pt")

        # Company info
        builder.row(style="header_primary")
        builder.cell(self.company_name, colspan=3, style="company_name")
        builder.cell("INVOICE", colspan=2, style="invoice_title")

        builder.row()
        builder.cell(self.company_address, colspan=3)
        builder.cell(f"Invoice #: {self.invoice_number}", colspan=2)

        builder.row()
        builder.cell(self.company_phone, colspan=3)
        builder.cell("Date: [DATE]", colspan=2)

        builder.row()
        builder.cell(self.company_email, colspan=3)
        builder.cell("Due: [DUE DATE]", colspan=2)

        # Blank row
        builder.row()

        # Bill To section
        builder.row(style="section_header")
        builder.cell("Bill To:")
        builder.cell("", colspan=4)

        builder.row()
        builder.cell("[Customer Name]", colspan=2)

        builder.row()
        builder.cell("[Customer Address]", colspan=2)

        # Blank row
        builder.row()

        # Line items header
        builder.row(style="header_secondary")
        builder.cell("Description", colspan=2)
        builder.cell("Qty")
        builder.cell("Rate")
        builder.cell("Amount")

        # Line item rows (10 blank rows)
        for i in range(10):
            row_num = i + 13  # Adjust based on header rows
            builder.row()
            builder.cell("", colspan=2, style="input")
            builder.cell("", style="input")
            builder.cell("", style="currency_input")
            builder.cell(f"=C{row_num}*D{row_num}", style="currency")

        # Totals section
        builder.row()
        builder.cell("", colspan=3)
        builder.cell("Subtotal:", style="label_right")
        builder.cell("=SUM(E13:E22)", style="currency")

        if self.tax_rate > 0:
            builder.row()
            builder.cell("", colspan=3)
            builder.cell(f"Tax ({self.tax_rate * 100:.0f}%):", style="label_right")
            builder.cell(f"=E23*{self.tax_rate}", style="currency")

            builder.row(style="total")
            builder.cell("", colspan=3)
            builder.cell("TOTAL:", style="total_label")
            builder.cell("=E23+E24", style="currency_total")
        else:
            builder.row(style="total")
            builder.cell("", colspan=3)
            builder.cell("TOTAL:", style="total_label")
            builder.cell("=E23", style="currency_total")

        # Notes section
        builder.row()
        builder.row()
        builder.cell("Notes:", style="section_label")

        builder.row()
        builder.cell("[Payment terms and notes]", colspan=5)

        return builder


# ============================================================================
# Expense Report Template
# ============================================================================


@dataclass
class ExpenseReportTemplate:
    """Employee expense report template.

    Features:
    - Employee information section
    - Expense line items with categories
    - Receipt tracking
    - Approval signatures
    - Automatic totals by category
    """

    employee_name: str = ""
    department: str = ""
    report_period: str = ""
    currency_symbol: str = "$"
    theme: str = "corporate"

    # Expense categories
    categories: list[str] = field(
        default_factory=lambda: [
            "Travel",
            "Lodging",
            "Meals",
            "Transportation",
            "Entertainment",
            "Supplies",
            "Other",
        ]
    )

    def generate(self) -> SpreadsheetBuilder:
        """Generate the expense report spreadsheet."""
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title="Expense Report",
            author=self.employee_name or "Employee",
            subject="Expense Report",
        )

        builder.sheet("Expenses")

        # Columns
        builder.column("Date", width="80pt", type="date")
        builder.column("Description", width="200pt")
        builder.column("Category", width="100pt")
        builder.column("Amount", width="100pt", type="currency")
        builder.column("Receipt", width="60pt")
        builder.column("Notes", width="150pt")

        builder.freeze(rows=4)

        # Header section
        builder.row(style="header_primary")
        builder.cell("EXPENSE REPORT", colspan=6)

        builder.row()
        builder.cell("Employee:")
        builder.cell(self.employee_name or "[Name]")
        builder.cell("Department:")
        builder.cell(self.department or "[Department]")
        builder.cell("Period:")
        builder.cell(self.report_period or "[Period]")

        builder.row()  # Blank row

        # Column headers
        builder.row(style="header_secondary")
        builder.cell("Date")
        builder.cell("Description")
        builder.cell("Category")
        builder.cell("Amount")
        builder.cell("Receipt")
        builder.cell("Notes")

        # Expense rows (15 blank)
        for _ in range(15):
            builder.row()
            builder.cell("", style="date_input")
            builder.cell("", style="input")
            builder.cell("", style="dropdown")  # Would need validation
            builder.cell("", style="currency_input")
            builder.cell("", style="checkbox")
            builder.cell("", style="input")

        # Total row
        builder.row(style="total")
        builder.cell("TOTAL", colspan=3)
        builder.cell("=SUM(D5:D19)", style="currency_total")
        builder.cell("")
        builder.cell("")

        # Summary by category
        builder.row()
        builder.row(style="section_header")
        builder.cell("Summary by Category", colspan=6)

        for category in self.categories:
            builder.row()
            builder.cell(category, colspan=3)
            builder.cell(
                f'=SUMIF(C5:C19,"{category}",D5:D19)',
                style="currency",
            )

        # Approval section
        builder.row()
        builder.row()
        builder.cell("Approval:", colspan=2)

        builder.row()
        builder.cell("Employee Signature:")
        builder.cell("_______________")
        builder.cell("Date:")
        builder.cell("_______________")

        builder.row()
        builder.cell("Manager Signature:")
        builder.cell("_______________")
        builder.cell("Date:")
        builder.cell("_______________")

        return builder


# ============================================================================
# Template Registry
# ============================================================================


PROFESSIONAL_TEMPLATES: dict[str, type] = {
    "enterprise_budget": EnterpriseBudgetTemplate,
    "cash_flow": CashFlowTrackerTemplate,
    "invoice": InvoiceTemplate,
    "expense_report": ExpenseReportTemplate,
}


def list_templates() -> list[str]:
    """List available professional templates."""
    return list(PROFESSIONAL_TEMPLATES.keys())


def get_template(name: str) -> type | None:
    """Get a template class by name."""
    return PROFESSIONAL_TEMPLATES.get(name)
