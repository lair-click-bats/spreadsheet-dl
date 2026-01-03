"""
Backward compatibility shim for csv_import module.

This module has been moved to spreadsheet_dl.domains.finance.csv_import.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.csv_import import *  # noqa: F403, F401
