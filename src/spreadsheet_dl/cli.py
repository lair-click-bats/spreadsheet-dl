"""
Command-line interface for SpreadsheetDL.

PUBLIC API ENTRY POINT
----------------------
This module is the public API entry point for the CLI functionality.
Implementation is modularized in the _cli package:

    - _cli/utils.py: Validation, confirmation, and utility functions
    - _cli/commands.py: Command handler implementations
    - _cli/app.py: Main application setup and argument parsing

New in v4.0.0:
    - FR-EXT-001: Plugin system framework (plugin command)
    - FR-EXT-005: Custom category management (category command)

New in v0.6.0 (Phase 3: Enhanced Features):
    - FR-CORE-004: Account management (account command)
    - FR-CURR-001: Multi-currency support (currency command)
    - FR-IMPORT-002: Extended bank formats (50+ supported)
    - FR-REPORT-003: Interactive visualization (visualize command)
    - FR-AI-001/003: Enhanced AI export with semantic tagging

New in v0.5.0:
    - FR-UX-004: Confirmation prompts for destructive operations
    - DR-STORE-002: Backup/restore functionality
    - FR-EXPORT-001: Multi-format export (xlsx, csv, pdf)
    - FR-DUAL-001/002: Dual export (ODS + JSON for AI)
"""

from __future__ import annotations

import sys

# Re-export everything from the modularized _cli package
from spreadsheet_dl._cli import (
    confirm_action,
    confirm_delete,
    confirm_destructive_operation,
    confirm_overwrite,
    main,
    validate_amount,
    validate_date,
)

__all__ = [
    "confirm_action",
    "confirm_delete",
    "confirm_destructive_operation",
    "confirm_overwrite",
    "main",
    "validate_amount",
    "validate_date",
]


if __name__ == "__main__":
    sys.exit(main())
