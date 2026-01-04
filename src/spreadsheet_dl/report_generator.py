"""
Backward compatibility shim for report_generator module.

This module has been moved to spreadsheet_dl.domains.finance.report_generator.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.report_generator import (
    ReportConfig,
    ReportGenerator,
    generate_monthly_report,
)

__all__ = [
    "ReportConfig",
    "ReportGenerator",
    "generate_monthly_report",
]
