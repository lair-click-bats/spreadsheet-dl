"""
Backward compatibility shim for templates.professional module.

This module has been moved to spreadsheet_dl.domains.finance.templates.professional.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.templates.professional import (
    PROFESSIONAL_TEMPLATES,
    BudgetCategory,
    CashFlowTrackerTemplate,
    ColumnDef,
    EnterpriseBudgetTemplate,
    ExpenseReportTemplate,
    InvoiceTemplate,
    TemplateMetadata,
    get_template,
    list_templates,
)

__all__ = [
    "PROFESSIONAL_TEMPLATES",
    "BudgetCategory",
    "CashFlowTrackerTemplate",
    "ColumnDef",
    "EnterpriseBudgetTemplate",
    "ExpenseReportTemplate",
    "InvoiceTemplate",
    "TemplateMetadata",
    "get_template",
    "list_templates",
]
