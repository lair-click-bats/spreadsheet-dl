"""
Backward compatibility shim for categories module.

This module has been moved to spreadsheet_dl.domains.finance.categories.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.categories import (
    CATEGORY_COLORS,
    Category,
    CategoryManager,
    StandardCategory,
    category_from_string,
    get_category_manager,
)

__all__ = [
    "CATEGORY_COLORS",
    "Category",
    "CategoryManager",
    "StandardCategory",
    "category_from_string",
    "get_category_manager",
]
