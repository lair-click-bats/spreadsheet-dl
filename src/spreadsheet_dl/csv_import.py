"""
Backward compatibility shim for csv_import module.

This module has been moved to spreadsheet_dl.domains.finance.csv_import.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.csv_import import (
    BANK_FORMATS,
    DEFAULT_CATEGORY_RULES,
    BankFormat,
    CategoryRule,
    CSVImporter,
    TransactionCategorizer,
    import_bank_csv,
)

__all__ = [
    "BANK_FORMATS",
    "DEFAULT_CATEGORY_RULES",
    "BankFormat",
    "CSVImporter",
    "CategoryRule",
    "TransactionCategorizer",
    "import_bank_csv",
]
