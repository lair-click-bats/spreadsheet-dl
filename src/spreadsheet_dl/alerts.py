"""
Backward compatibility shim for alerts module.

This module has been moved to spreadsheet_dl.domains.finance.alerts.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.alerts import *  # noqa: F403
