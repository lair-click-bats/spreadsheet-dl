"""Financial statement templates.

Implements:
    - FR-PROF-004: Financial Statement Templates

Provides templates for standard financial statements:
- Income Statement (P&L)
- Balance Sheet
- Cash Flow Statement
- Statement of Changes in Equity
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


# ============================================================================
# Income Statement Template
# ============================================================================


@dataclass
class IncomeStatementTemplate:
    """Income Statement (Profit & Loss) template (FR-PROF-004).

    Features:
    - Revenue section with multiple line items
    - Cost of goods sold
    - Operating expenses
    - Non-operating income/expenses
    - Tax calculations
    - Net income with comparative periods

    Examples:
        template = IncomeStatementTemplate(
            company_name="ACME Corp",
            period="Q1 2024",
            comparative=True,
        )
        builder = template.generate()
    """

    company_name: str = "Company Name"
    period: str = "Year Ended December 31, 2024"
    comparative: bool = True  # Include prior period comparison
    currency_symbol: str = "$"
    theme: str = "corporate"

    # Revenue items
    revenue_items: list[str] = field(
        default_factory=lambda: [
            "Product Sales",
            "Service Revenue",
            "Other Revenue",
        ]
    )

    # Cost of goods sold items
    cogs_items: list[str] = field(
        default_factory=lambda: [
            "Direct Materials",
            "Direct Labor",
            "Manufacturing Overhead",
        ]
    )

    # Operating expense items
    operating_expenses: list[str] = field(
        default_factory=lambda: [
            "Selling Expenses",
            "General & Administrative",
            "Research & Development",
            "Depreciation & Amortization",
        ]
    )

    # Non-operating items
    non_operating_items: list[str] = field(
        default_factory=lambda: [
            "Interest Income",
            "Interest Expense",
            "Other Income (Expense)",
        ]
    )

    def generate(self) -> SpreadsheetBuilder:
        """Generate the income statement spreadsheet."""
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Income Statement - {self.company_name}",
            author="Finance Department",
            subject="Income Statement",
        )

        builder.sheet("Income Statement")

        # Columns
        if self.comparative:
            builder.column("", width="250pt")  # Description
            builder.column("Current Period", width="120pt", type="currency")
            builder.column("Prior Period", width="120pt", type="currency")
            builder.column("Change", width="100pt", type="currency")
            builder.column("% Change", width="80pt", type="percentage")
        else:
            builder.column("", width="250pt")
            builder.column("Amount", width="120pt", type="currency")

        builder.freeze(rows=3)

        # Header section
        builder.row(style="company_header")
        builder.cell(self.company_name, colspan=5 if self.comparative else 2)

        builder.row(style="report_title")
        builder.cell("INCOME STATEMENT", colspan=5 if self.comparative else 2)

        builder.row(style="period")
        builder.cell(self.period, colspan=5 if self.comparative else 2)

        # Column headers
        builder.row(style="header_secondary")
        builder.cell("")
        if self.comparative:
            builder.cell("Current")
            builder.cell("Prior")
            builder.cell("Change")
            builder.cell("% Change")
        else:
            builder.cell("Amount")

        current_row = 5

        # Revenue Section - returns (next_row, total_row)
        current_row, revenue_total_row = self._add_section_with_total(
            builder, "REVENUE", self.revenue_items, current_row
        )

        # Cost of Goods Sold
        current_row, cogs_total_row = self._add_section_with_total(
            builder, "COST OF GOODS SOLD", self.cogs_items, current_row
        )

        # Gross Profit = Revenue - COGS
        builder.row(style="subtotal")
        builder.cell("GROSS PROFIT")
        builder.cell(f"=B{revenue_total_row}-B{cogs_total_row}")
        if self.comparative:
            builder.cell(f"=C{revenue_total_row}-C{cogs_total_row}")
            builder.cell(f"=B{current_row}-C{current_row}")
            builder.cell(
                f"=IF(C{current_row}=0,0,(B{current_row}-C{current_row})/ABS(C{current_row}))"
            )
        gross_profit_row = current_row
        current_row += 1

        # Operating Expenses
        current_row, opex_total_row = self._add_section_with_total(
            builder, "OPERATING EXPENSES", self.operating_expenses, current_row
        )

        # Operating Income = Gross Profit - Operating Expenses
        builder.row(style="subtotal")
        builder.cell("OPERATING INCOME")
        builder.cell(f"=B{gross_profit_row}-B{opex_total_row}")
        if self.comparative:
            builder.cell(f"=C{gross_profit_row}-C{opex_total_row}")
            builder.cell(f"=B{current_row}-C{current_row}")
            builder.cell(
                f"=IF(C{current_row}=0,0,(B{current_row}-C{current_row})/ABS(C{current_row}))"
            )
        operating_income_row = current_row
        current_row += 1

        # Non-Operating Items
        current_row, non_op_total_row = self._add_section_with_total(
            builder, "NON-OPERATING ITEMS", self.non_operating_items, current_row
        )

        # Income Before Taxes = Operating Income + Non-Operating Items
        builder.row(style="subtotal")
        builder.cell("INCOME BEFORE TAXES")
        builder.cell(f"=B{operating_income_row}+B{non_op_total_row}")
        if self.comparative:
            builder.cell(f"=C{operating_income_row}+C{non_op_total_row}")
            builder.cell(f"=B{current_row}-C{current_row}")
            builder.cell(
                f"=IF(C{current_row}=0,0,(B{current_row}-C{current_row})/ABS(C{current_row}))"
            )
        income_before_tax_row = current_row
        current_row += 1

        # Income Tax
        builder.row()
        builder.cell("  Income Tax Expense")
        builder.cell(0, style="currency_input")
        if self.comparative:
            builder.cell(0, style="currency_input")
            builder.cell(f"=B{current_row}-C{current_row}")
            builder.cell(
                f"=IF(C{current_row}=0,0,(B{current_row}-C{current_row})/ABS(C{current_row}))"
            )
        tax_row = current_row
        current_row += 1

        # Net Income = Income Before Taxes - Tax
        builder.row(style="total")
        builder.cell("NET INCOME")
        builder.cell(f"=B{income_before_tax_row}-B{tax_row}")
        if self.comparative:
            builder.cell(f"=C{income_before_tax_row}-C{tax_row}")
            builder.cell(f"=B{current_row}-C{current_row}")
            builder.cell(
                f"=IF(C{current_row}=0,0,(B{current_row}-C{current_row})/ABS(C{current_row}))"
            )

        return builder

    def _add_section_with_total(
        self,
        builder: SpreadsheetBuilder,
        section_name: str,
        items: list[str],
        start_row: int,
    ) -> tuple[int, int]:
        """Add a section with items. Returns (next_row, total_row)."""
        current_row = start_row

        # Section header
        builder.row(style="section_header")
        builder.cell(section_name)
        builder.cell("")
        if self.comparative:
            builder.cell("")
            builder.cell("")
            builder.cell("")
        current_row += 1

        # Line items
        item_start = current_row
        for item in items:
            builder.row()
            builder.cell(f"  {item}")
            builder.cell(0, style="currency_input")
            if self.comparative:
                builder.cell(0, style="currency_input")
                builder.cell(f"=B{current_row}-C{current_row}")
                builder.cell(
                    f"=IF(C{current_row}=0,0,(B{current_row}-C{current_row})/ABS(C{current_row}))"
                )
            current_row += 1
        item_end = current_row - 1

        # Section total
        builder.row(style="section_total")
        builder.cell(f"  Total {section_name.title()}")
        builder.cell(f"=SUM(B{item_start}:B{item_end})")
        if self.comparative:
            builder.cell(f"=SUM(C{item_start}:C{item_end})")
            builder.cell(f"=B{current_row}-C{current_row}")
            builder.cell(
                f"=IF(C{current_row}=0,0,(B{current_row}-C{current_row})/ABS(C{current_row}))"
            )
        total_row = current_row
        current_row += 1

        return current_row, total_row


# ============================================================================
# Balance Sheet Template
# ============================================================================


@dataclass
class BalanceSheetTemplate:
    """Balance Sheet template (FR-PROF-004).

    Features:
    - Assets section (current and non-current)
    - Liabilities section (current and non-current)
    - Equity section
    - Comparative periods
    - Accounting equation check

    Examples:
        template = BalanceSheetTemplate(
            company_name="ACME Corp",
            as_of_date="December 31, 2024",
        )
        builder = template.generate()
    """

    company_name: str = "Company Name"
    as_of_date: str = "December 31, 2024"
    comparative: bool = True
    currency_symbol: str = "$"
    theme: str = "corporate"

    # Current assets
    current_assets: list[str] = field(
        default_factory=lambda: [
            "Cash and Cash Equivalents",
            "Short-term Investments",
            "Accounts Receivable",
            "Inventory",
            "Prepaid Expenses",
        ]
    )

    # Non-current assets
    non_current_assets: list[str] = field(
        default_factory=lambda: [
            "Property, Plant & Equipment",
            "Accumulated Depreciation",
            "Intangible Assets",
            "Long-term Investments",
        ]
    )

    # Current liabilities
    current_liabilities: list[str] = field(
        default_factory=lambda: [
            "Accounts Payable",
            "Accrued Expenses",
            "Short-term Debt",
            "Current Portion of Long-term Debt",
        ]
    )

    # Non-current liabilities
    non_current_liabilities: list[str] = field(
        default_factory=lambda: [
            "Long-term Debt",
            "Deferred Tax Liabilities",
            "Other Long-term Liabilities",
        ]
    )

    # Equity items
    equity_items: list[str] = field(
        default_factory=lambda: [
            "Common Stock",
            "Additional Paid-in Capital",
            "Retained Earnings",
            "Treasury Stock",
        ]
    )

    def generate(self) -> SpreadsheetBuilder:
        """Generate the balance sheet spreadsheet."""
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Balance Sheet - {self.company_name}",
            author="Finance Department",
            subject="Balance Sheet",
        )

        builder.sheet("Balance Sheet")

        # Columns
        if self.comparative:
            builder.column("", width="250pt")
            builder.column("Current", width="120pt", type="currency")
            builder.column("Prior", width="120pt", type="currency")
        else:
            builder.column("", width="250pt")
            builder.column("Amount", width="120pt", type="currency")

        builder.freeze(rows=3)

        # Header
        builder.row(style="company_header")
        builder.cell(self.company_name, colspan=3 if self.comparative else 2)

        builder.row(style="report_title")
        builder.cell("BALANCE SHEET", colspan=3 if self.comparative else 2)

        builder.row(style="period")
        builder.cell(f"As of {self.as_of_date}", colspan=3 if self.comparative else 2)

        current_row = 4

        # ASSETS
        builder.row(style="major_section")
        builder.cell("ASSETS")
        current_row += 1

        # Current Assets
        current_row, ca_total_row = self._add_section(
            builder, "Current Assets", self.current_assets, current_row
        )

        # Non-Current Assets
        current_row, nca_total_row = self._add_section(
            builder, "Non-Current Assets", self.non_current_assets, current_row
        )

        # Total Assets
        builder.row(style="total")
        builder.cell("TOTAL ASSETS")
        builder.cell(f"=B{ca_total_row}+B{nca_total_row}")
        if self.comparative:
            builder.cell(f"=C{ca_total_row}+C{nca_total_row}")
        total_assets_row = current_row
        current_row += 1

        builder.row()  # Blank row
        current_row += 1

        # LIABILITIES & EQUITY
        builder.row(style="major_section")
        builder.cell("LIABILITIES & STOCKHOLDERS' EQUITY")
        current_row += 1

        # Current Liabilities
        current_row, cl_total_row = self._add_section(
            builder, "Current Liabilities", self.current_liabilities, current_row
        )

        # Non-Current Liabilities
        current_row, ncl_total_row = self._add_section(
            builder,
            "Non-Current Liabilities",
            self.non_current_liabilities,
            current_row,
        )

        # Total Liabilities
        builder.row(style="subtotal")
        builder.cell("Total Liabilities")
        builder.cell(f"=B{cl_total_row}+B{ncl_total_row}")
        if self.comparative:
            builder.cell(f"=C{cl_total_row}+C{ncl_total_row}")
        total_liab_row = current_row
        current_row += 1

        # Stockholders' Equity
        current_row, eq_total_row = self._add_section(
            builder, "Stockholders' Equity", self.equity_items, current_row
        )

        # Total Liabilities & Equity
        builder.row(style="total")
        builder.cell("TOTAL LIABILITIES & EQUITY")
        builder.cell(f"=B{total_liab_row}+B{eq_total_row}")
        if self.comparative:
            builder.cell(f"=C{total_liab_row}+C{eq_total_row}")
        current_row += 1

        # Balance check
        builder.row()
        current_row += 1
        builder.row(style="check")
        builder.cell("Balance Check (Assets = L+E)")
        builder.cell(f'=IF(B{total_assets_row}=B{current_row - 2},"OK","ERROR")')
        if self.comparative:
            builder.cell(f'=IF(C{total_assets_row}=C{current_row - 2},"OK","ERROR")')

        return builder

    def _add_section(
        self,
        builder: SpreadsheetBuilder,
        section_name: str,
        items: list[str],
        start_row: int,
    ) -> tuple[int, int]:
        """Add a section with items. Returns (next_row, total_row)."""
        current_row = start_row

        # Section header
        builder.row(style="section_header")
        builder.cell(f"  {section_name}")
        current_row += 1

        # Line items
        item_start = current_row
        for item in items:
            builder.row()
            builder.cell(f"    {item}")
            builder.cell(0, style="currency_input")
            if self.comparative:
                builder.cell(0, style="currency_input")
            current_row += 1
        item_end = current_row - 1

        # Section total
        builder.row(style="section_total")
        builder.cell(f"  Total {section_name}")
        builder.cell(f"=SUM(B{item_start}:B{item_end})")
        if self.comparative:
            builder.cell(f"=SUM(C{item_start}:C{item_end})")
        total_row = current_row
        current_row += 1

        return current_row, total_row


# ============================================================================
# Cash Flow Statement Template
# ============================================================================


@dataclass
class CashFlowStatementTemplate:
    """Statement of Cash Flows template (FR-PROF-004).

    Features:
    - Operating activities (indirect method)
    - Investing activities
    - Financing activities
    - Reconciliation to balance sheet

    Examples:
        template = CashFlowStatementTemplate(
            company_name="ACME Corp",
            period="Year Ended December 31, 2024",
        )
        builder = template.generate()
    """

    company_name: str = "Company Name"
    period: str = "Year Ended December 31, 2024"
    method: str = "indirect"  # "indirect" or "direct"
    comparative: bool = True
    currency_symbol: str = "$"
    theme: str = "corporate"

    # Operating adjustments (for indirect method)
    operating_adjustments: list[str] = field(
        default_factory=lambda: [
            "Depreciation & Amortization",
            "(Gain) Loss on Sale of Assets",
            "Changes in Accounts Receivable",
            "Changes in Inventory",
            "Changes in Prepaid Expenses",
            "Changes in Accounts Payable",
            "Changes in Accrued Liabilities",
        ]
    )

    # Investing activities
    investing_items: list[str] = field(
        default_factory=lambda: [
            "Purchase of Property & Equipment",
            "Proceeds from Sale of Assets",
            "Purchases of Investments",
            "Proceeds from Investments",
        ]
    )

    # Financing activities
    financing_items: list[str] = field(
        default_factory=lambda: [
            "Proceeds from Debt",
            "Repayment of Debt",
            "Proceeds from Stock Issuance",
            "Dividends Paid",
            "Share Repurchases",
        ]
    )

    def generate(self) -> SpreadsheetBuilder:
        """Generate the cash flow statement spreadsheet."""
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Cash Flow Statement - {self.company_name}",
            author="Finance Department",
            subject="Statement of Cash Flows",
        )

        builder.sheet("Cash Flow")

        # Columns
        if self.comparative:
            builder.column("", width="280pt")
            builder.column("Current", width="120pt", type="currency")
            builder.column("Prior", width="120pt", type="currency")
        else:
            builder.column("", width="280pt")
            builder.column("Amount", width="120pt", type="currency")

        builder.freeze(rows=3)

        # Header
        builder.row(style="company_header")
        builder.cell(self.company_name, colspan=3 if self.comparative else 2)

        builder.row(style="report_title")
        builder.cell("STATEMENT OF CASH FLOWS", colspan=3 if self.comparative else 2)

        builder.row(style="period")
        builder.cell(self.period, colspan=3 if self.comparative else 2)

        current_row = 4

        # Operating Activities
        builder.row(style="major_section")
        builder.cell("CASH FLOWS FROM OPERATING ACTIVITIES")
        current_row += 1

        # Net Income
        builder.row()
        builder.cell("  Net Income")
        builder.cell(0, style="currency_input")
        if self.comparative:
            builder.cell(0, style="currency_input")
        net_income_row = current_row
        current_row += 1

        # Adjustments header
        builder.row(style="subsection")
        builder.cell("  Adjustments to reconcile net income:")
        current_row += 1

        # Adjustment items
        adj_start = current_row
        for item in self.operating_adjustments:
            builder.row()
            builder.cell(f"    {item}")
            builder.cell(0, style="currency_input")
            if self.comparative:
                builder.cell(0, style="currency_input")
            current_row += 1
        adj_end = current_row - 1

        # Net Operating Cash Flow
        builder.row(style="subtotal")
        builder.cell("Net Cash from Operating Activities")
        builder.cell(f"=B{net_income_row}+SUM(B{adj_start}:B{adj_end})")
        if self.comparative:
            builder.cell(f"=C{net_income_row}+SUM(C{adj_start}:C{adj_end})")
        op_total_row = current_row
        current_row += 1

        builder.row()
        current_row += 1

        # Investing Activities
        builder.row(style="major_section")
        builder.cell("CASH FLOWS FROM INVESTING ACTIVITIES")
        current_row += 1

        inv_start = current_row
        for item in self.investing_items:
            builder.row()
            builder.cell(f"  {item}")
            builder.cell(0, style="currency_input")
            if self.comparative:
                builder.cell(0, style="currency_input")
            current_row += 1
        inv_end = current_row - 1

        builder.row(style="subtotal")
        builder.cell("Net Cash from Investing Activities")
        builder.cell(f"=SUM(B{inv_start}:B{inv_end})")
        if self.comparative:
            builder.cell(f"=SUM(C{inv_start}:C{inv_end})")
        inv_total_row = current_row
        current_row += 1

        builder.row()
        current_row += 1

        # Financing Activities
        builder.row(style="major_section")
        builder.cell("CASH FLOWS FROM FINANCING ACTIVITIES")
        current_row += 1

        fin_start = current_row
        for item in self.financing_items:
            builder.row()
            builder.cell(f"  {item}")
            builder.cell(0, style="currency_input")
            if self.comparative:
                builder.cell(0, style="currency_input")
            current_row += 1
        fin_end = current_row - 1

        builder.row(style="subtotal")
        builder.cell("Net Cash from Financing Activities")
        builder.cell(f"=SUM(B{fin_start}:B{fin_end})")
        if self.comparative:
            builder.cell(f"=SUM(C{fin_start}:C{fin_end})")
        fin_total_row = current_row
        current_row += 1

        builder.row()
        current_row += 1

        # Summary
        builder.row(style="total")
        builder.cell("NET CHANGE IN CASH")
        builder.cell(f"=B{op_total_row}+B{inv_total_row}+B{fin_total_row}")
        if self.comparative:
            builder.cell(f"=C{op_total_row}+C{inv_total_row}+C{fin_total_row}")
        net_change_row = current_row
        current_row += 1

        builder.row()
        builder.cell("Beginning Cash Balance")
        builder.cell(0, style="currency_input")
        if self.comparative:
            builder.cell(0, style="currency_input")
        begin_cash_row = current_row
        current_row += 1

        builder.row(style="total")
        builder.cell("ENDING CASH BALANCE")
        builder.cell(f"=B{net_change_row}+B{begin_cash_row}")
        if self.comparative:
            builder.cell(f"=C{net_change_row}+C{begin_cash_row}")

        return builder


# ============================================================================
# Statement of Changes in Equity Template
# ============================================================================


@dataclass
class EquityStatementTemplate:
    """Statement of Changes in Equity template (FR-PROF-004).

    Features:
    - Beginning balances
    - Comprehensive income
    - Dividends
    - Stock transactions
    - Ending balances

    Examples:
        template = EquityStatementTemplate(
            company_name="ACME Corp",
            period="Year Ended December 31, 2024",
        )
        builder = template.generate()
    """

    company_name: str = "Company Name"
    period: str = "Year Ended December 31, 2024"
    currency_symbol: str = "$"
    theme: str = "corporate"

    # Equity components
    equity_components: list[str] = field(
        default_factory=lambda: [
            "Common Stock",
            "Additional Paid-in Capital",
            "Retained Earnings",
            "Treasury Stock",
            "Accumulated OCI",
        ]
    )

    def generate(self) -> SpreadsheetBuilder:
        """Generate the equity statement spreadsheet."""
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Statement of Changes in Equity - {self.company_name}",
            author="Finance Department",
            subject="Statement of Changes in Equity",
        )

        builder.sheet("Changes in Equity")

        # Columns: Description + one per equity component + Total
        builder.column("", width="200pt")
        for comp in self.equity_components:
            builder.column(comp, width="100pt", type="currency")
        builder.column("Total", width="100pt", type="currency")

        builder.freeze(rows=4, cols=1)

        num_cols = len(self.equity_components) + 1

        # Header
        builder.row(style="company_header")
        builder.cell(self.company_name, colspan=num_cols + 1)

        builder.row(style="report_title")
        builder.cell(
            "STATEMENT OF CHANGES IN STOCKHOLDERS' EQUITY", colspan=num_cols + 1
        )

        builder.row(style="period")
        builder.cell(self.period, colspan=num_cols + 1)

        # Column headers
        builder.row(style="header_secondary")
        builder.cell("")
        for comp in self.equity_components:
            builder.cell(comp)
        builder.cell("Total")

        current_row = 5

        # Beginning balance
        builder.row(style="balance")
        builder.cell("Beginning Balance")
        for _i in range(len(self.equity_components)):
            builder.cell(0, style="currency_input")
        builder.cell(
            f"=SUM(B{current_row}:{chr(ord('A') + len(self.equity_components))}{current_row})"
        )
        begin_row = current_row
        current_row += 1

        # Transactions
        transactions = [
            "Net Income",
            "Other Comprehensive Income",
            "Dividends Declared",
            "Stock Issuance",
            "Stock Repurchases",
            "Stock Compensation",
        ]

        for trans in transactions:
            builder.row()
            builder.cell(f"  {trans}")
            for _i in range(len(self.equity_components)):
                builder.cell(0, style="currency_input")
            builder.cell(
                f"=SUM(B{current_row}:{chr(ord('A') + len(self.equity_components))}{current_row})"
            )
            current_row += 1

        # Ending balance
        builder.row(style="total")
        builder.cell("Ending Balance")
        for col_idx in range(len(self.equity_components)):
            col_letter = chr(ord("B") + col_idx)
            builder.cell(f"=SUM({col_letter}{begin_row}:{col_letter}{current_row - 1})")
        builder.cell(
            f"=SUM(B{current_row}:{chr(ord('A') + len(self.equity_components))}{current_row})"
        )

        return builder


# ============================================================================
# Template Registry
# ============================================================================


FINANCIAL_STATEMENT_TEMPLATES: dict[str, type] = {
    "income_statement": IncomeStatementTemplate,
    "balance_sheet": BalanceSheetTemplate,
    "cash_flow_statement": CashFlowStatementTemplate,
    "equity_statement": EquityStatementTemplate,
}


def list_financial_templates() -> list[str]:
    """List available financial statement templates."""
    return list(FINANCIAL_STATEMENT_TEMPLATES.keys())


def get_financial_template(name: str) -> type | None:
    """Get a financial statement template class by name."""
    return FINANCIAL_STATEMENT_TEMPLATES.get(name)
