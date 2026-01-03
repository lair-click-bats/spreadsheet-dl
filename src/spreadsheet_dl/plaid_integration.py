"""
Backward compatibility shim for plaid_integration module.

This module has been moved to spreadsheet_dl.domains.finance.plaid_integration.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.plaid_integration import *  # noqa: F403
