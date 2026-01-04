"""
Backward compatibility shim for reminders module.

This module has been moved to spreadsheet_dl.domains.finance.reminders.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.reminders import (
    COMMON_BILLS,
    BillReminder,
    BillReminderManager,
    ReminderFrequency,
    ReminderStatus,
    create_bill_from_template,
    get_calendar_feed_url,
)

__all__ = [
    "COMMON_BILLS",
    "BillReminder",
    "BillReminderManager",
    "ReminderFrequency",
    "ReminderStatus",
    "create_bill_from_template",
    "get_calendar_feed_url",
]
