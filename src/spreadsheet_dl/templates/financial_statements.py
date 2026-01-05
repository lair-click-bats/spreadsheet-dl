"""Backward compatibility shim for templates.financial_statements module.

This module has been moved to spreadsheet_dl.domains.finance.templates.financial_statements.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.templates.financial_statements import (
    BalanceSheetTemplate,
    CashFlowStatementTemplate,
    EquityStatementTemplate,
    IncomeStatementTemplate,
    get_financial_template,
    list_financial_templates,
)

__all__ = [
    "BalanceSheetTemplate",
    "CashFlowStatementTemplate",
    "EquityStatementTemplate",
    "IncomeStatementTemplate",
    "get_financial_template",
    "list_financial_templates",
]
