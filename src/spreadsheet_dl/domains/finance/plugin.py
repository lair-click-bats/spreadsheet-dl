"""Finance Domain Plugin for SpreadsheetDL.

Implements:
    Finance domain plugin
    PHASE-C: Domain plugin implementations

Provides finance-specific functionality including:
- Enterprise budget tracking and analysis
- Cash flow tracking and forecasting
- Invoice generation
- Expense report management
- Financial statements (Income, Balance Sheet, Cash Flow, Equity)

Note: Finance templates use a standalone dataclass pattern for historical compatibility.
They provide a generate() method that returns a SpreadsheetBuilder.
"""

from __future__ import annotations

from typing import Any

from spreadsheet_dl.domains.base import BaseDomainPlugin, PluginMetadata

# Import templates
from spreadsheet_dl.domains.finance.templates.financial_statements import (
    BalanceSheetTemplate,
    CashFlowStatementTemplate,
    EquityStatementTemplate,
    IncomeStatementTemplate,
)
from spreadsheet_dl.domains.finance.templates.professional import (
    CashFlowTrackerTemplate,
    EnterpriseBudgetTemplate,
    ExpenseReportTemplate,
    InvoiceTemplate,
)


class FinanceDomainPlugin(BaseDomainPlugin):
    """Finance domain plugin.

    Implements:
        Complete Finance domain plugin
        PHASE-C: Domain plugin implementations

    Provides comprehensive finance functionality for SpreadsheetDL
    with professional templates for budgeting, invoicing, and financial statements.

    Note: Finance templates use a standalone dataclass pattern with generate() method.
    They don't extend BaseTemplate but provide equivalent functionality.

    Templates (8 total):
        Professional (4):
        - EnterpriseBudgetTemplate: Budget tracking with categories and variances
        - CashFlowTrackerTemplate: Cash flow tracking and forecasting
        - InvoiceTemplate: Professional invoice generation
        - ExpenseReportTemplate: Expense tracking and reimbursement

        Financial Statements (4):
        - IncomeStatementTemplate: Profit and loss statement
        - BalanceSheetTemplate: Assets, liabilities, and equity
        - CashFlowStatementTemplate: Operating, investing, financing activities
        - EquityStatementTemplate: Changes in stockholders' equity

    Example:
        >>> plugin = FinanceDomainPlugin()
        >>> plugin.initialize()
        >>> template_class = plugin.get_template("invoice")
        >>> template = template_class(company_name="Acme Corp")
        >>> builder = template.generate()
        >>> path = builder.save("invoice.ods")
    """

    def __init__(self) -> None:
        """Initialize finance domain plugin."""
        super().__init__()
        # Finance templates use standalone dataclass pattern (historical compatibility)
        self._finance_templates: dict[str, type[Any]] = {}

    @property
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata.

        Returns:
            PluginMetadata with finance plugin information

        Implements:
            Plugin metadata requirements
        """
        return PluginMetadata(
            name="finance",
            version="4.0.0",
            description="Finance templates for budgeting, invoicing, and financial statements",
            author="SpreadsheetDL Team",
            license="MIT",
            homepage="https://github.com/lair-click-bats/spreadsheet-dl",
            tags=(
                "finance",
                "budget",
                "invoice",
                "expense",
                "accounting",
                "financial-statements",
            ),
            min_spreadsheet_dl_version="4.0.0",
        )

    def initialize(self) -> None:
        """Initialize plugin resources.

        Registers all templates using finance-specific registration.

        Implements:
            Plugin initialization with all components

        Raises:
            Exception: If initialization fails
        """
        # Register professional templates (4)
        self._finance_templates["enterprise_budget"] = EnterpriseBudgetTemplate
        self._finance_templates["cash_flow"] = CashFlowTrackerTemplate
        self._finance_templates["invoice"] = InvoiceTemplate
        self._finance_templates["expense_report"] = ExpenseReportTemplate

        # Register financial statement templates (4)
        self._finance_templates["income_statement"] = IncomeStatementTemplate
        self._finance_templates["balance_sheet"] = BalanceSheetTemplate
        self._finance_templates["cash_flow_statement"] = CashFlowStatementTemplate
        self._finance_templates["equity_statement"] = EquityStatementTemplate

    def cleanup(self) -> None:
        """Cleanup plugin resources.

        No resources need explicit cleanup for this plugin.

        Implements:
            Plugin cleanup method
        """
        self._finance_templates.clear()

    def validate(self) -> bool:
        """Validate plugin configuration.

        Returns:
            True if plugin has required templates registered

        Implements:
            Plugin validation
        """
        required_templates = 8
        return len(self._finance_templates) >= required_templates

    def get_template(self, name: str) -> type[Any] | None:
        """Get a template class by name.

        Args:
            name: Template name

        Returns:
            Template class or None if not found

        Implements:
            Template retrieval for finance domain
        """
        return self._finance_templates.get(name)

    def list_templates(self) -> list[str]:
        """List all available template names.

        Returns:
            List of template names

        Implements:
            Template listing for finance domain
        """
        return list(self._finance_templates.keys())


__all__ = [
    "FinanceDomainPlugin",
]
