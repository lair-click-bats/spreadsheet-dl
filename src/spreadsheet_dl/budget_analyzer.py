"""
Backward compatibility shim for budget_analyzer module.

This module has been moved to spreadsheet_dl.domains.finance.budget_analyzer.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.budget_analyzer import *  # noqa: F403
