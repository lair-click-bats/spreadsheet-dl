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

from spreadsheet_dl.templates.financial_statements import (
    FINANCIAL_STATEMENT_TEMPLATES,
    BalanceSheetTemplate,
    CashFlowStatementTemplate,
    EquityStatementTemplate,
    IncomeStatementTemplate,
    get_financial_template,
    list_financial_templates,
)
from spreadsheet_dl.templates.professional import (
    PROFESSIONAL_TEMPLATES,
    BudgetCategory,
    CashFlowTrackerTemplate,
    EnterpriseBudgetTemplate,
    ExpenseReportTemplate,
    InvoiceTemplate,
    TemplateMetadata,
    get_template,
    list_templates,
)

__all__ = [
    # Financial Statement Registry
    "FINANCIAL_STATEMENT_TEMPLATES",
    # Professional Registry
    "PROFESSIONAL_TEMPLATES",
    "BalanceSheetTemplate",
    # Supporting classes
    "BudgetCategory",
    "CashFlowStatementTemplate",
    "CashFlowTrackerTemplate",
    # Professional Templates (FR-PROF-001, FR-PROF-002, FR-PROF-003)
    "EnterpriseBudgetTemplate",
    "EquityStatementTemplate",
    "ExpenseReportTemplate",
    # Financial Statement Templates (FR-PROF-004)
    "IncomeStatementTemplate",
    "InvoiceTemplate",
    "TemplateMetadata",
    "get_financial_template",
    "get_template",
    "list_financial_templates",
    "list_templates",
]
