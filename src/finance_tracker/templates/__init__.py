"""
Templates package - Professional financial document templates.

Implements:
    - FR-PROF-001: Enterprise Budget Template
    - FR-PROF-002: Cash Flow Tracker Template
    - FR-PROF-003: Invoice/Expense Report Template
    - FR-PROF-004: Financial Statement Templates

Provides ready-to-use templates for common financial documents
with professional formatting, built-in formulas, and validation.
"""

from finance_tracker.templates.professional import (
    BudgetCategory,
    CashFlowTrackerTemplate,
    EnterpriseBudgetTemplate,
    ExpenseReportTemplate,
    InvoiceTemplate,
    PROFESSIONAL_TEMPLATES,
    TemplateMetadata,
    get_template,
    list_templates,
)

from finance_tracker.templates.financial_statements import (
    BalanceSheetTemplate,
    CashFlowStatementTemplate,
    EquityStatementTemplate,
    FINANCIAL_STATEMENT_TEMPLATES,
    get_financial_template,
    IncomeStatementTemplate,
    list_financial_templates,
)

__all__ = [
    # Professional Templates (FR-PROF-001, FR-PROF-002, FR-PROF-003)
    "EnterpriseBudgetTemplate",
    "CashFlowTrackerTemplate",
    "InvoiceTemplate",
    "ExpenseReportTemplate",
    # Financial Statement Templates (FR-PROF-004)
    "IncomeStatementTemplate",
    "BalanceSheetTemplate",
    "CashFlowStatementTemplate",
    "EquityStatementTemplate",
    # Supporting classes
    "BudgetCategory",
    "TemplateMetadata",
    # Professional Registry
    "PROFESSIONAL_TEMPLATES",
    "list_templates",
    "get_template",
    # Financial Statement Registry
    "FINANCIAL_STATEMENT_TEMPLATES",
    "list_financial_templates",
    "get_financial_template",
]
