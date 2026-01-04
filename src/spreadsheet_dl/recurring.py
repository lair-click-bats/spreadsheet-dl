"""
Backward compatibility shim for recurring module.

This module has been moved to spreadsheet_dl.domains.finance.recurring.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export from the new location
from spreadsheet_dl.domains.finance.recurring import (
    RecurrenceFrequency,
    RecurringExpense,
    RecurringExpenseManager,
    create_common_recurring,
)

__all__ = [
    "RecurrenceFrequency",
    "RecurringExpense",
    "RecurringExpenseManager",
    "create_common_recurring",
]
