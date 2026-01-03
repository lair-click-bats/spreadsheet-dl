"""
Backward compatibility shim for ods_generator module.

This module has been moved to spreadsheet_dl.domains.finance.ods_generator.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.ods_generator import *  # noqa: F403

__all__ = [
    "BudgetAllocation",
    "ExpenseCategory",
    "ExpenseEntry",
    "OdsGenerator",
    "create_monthly_budget",
]
