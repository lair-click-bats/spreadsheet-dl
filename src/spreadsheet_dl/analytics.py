"""
Backward compatibility shim for analytics module.

This module has been moved to spreadsheet_dl.domains.finance.analytics.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.analytics import (
    AnalyticsDashboard,
    CategoryInsight,
    DashboardData,
    TrendData,
    generate_dashboard,
)

__all__ = [
    "AnalyticsDashboard",
    "CategoryInsight",
    "DashboardData",
    "TrendData",
    "generate_dashboard",
]
