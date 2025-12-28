"""
Finance Tracker - Family financial tracking with ODS spreadsheets.

This package provides tools for creating, reading, and analyzing ODS
spreadsheets for family budget tracking, integrated with Nextcloud
and Collabora Office.

New in v0.4.0:
- Declarative DSL for themes and styling
- YAML-based theme definitions
- Fluent Builder API for spreadsheet construction
- Type-safe FormulaBuilder
- 5 built-in themes (default, corporate, minimal, dark, high_contrast)
- CLI --theme flag support
"""

__version__ = "0.4.0"
__author__ = "jallen"

from finance_tracker.alerts import (
    Alert,
    AlertConfig,
    AlertMonitor,
    check_budget_alerts,
)

# Phase 3 modules
from finance_tracker.analytics import (
    AnalyticsDashboard,
    generate_dashboard,
)
from finance_tracker.budget_analyzer import BudgetAnalyzer

# Builder API (NEW in v0.4.0)
from finance_tracker.builder import (
    CellRef,
    CellSpec,
    ColumnSpec,
    FormulaBuilder,
    RangeRef,
    RowSpec,
    SheetRef,
    SheetSpec,
    SpreadsheetBuilder,
    create_spreadsheet,
    formula,
)

# Phase 5 modules
from finance_tracker.config import (
    Config,
    get_config,
    init_config_file,
)

# Phase 2 modules
from finance_tracker.csv_import import (
    CSVImporter,
    TransactionCategorizer,
    import_bank_csv,
)
from finance_tracker.exceptions import (
    ConfigurationError,
    CSVImportError,
    FileError,
    FinanceTrackerError,
    OdsError,
    TemplateError,
    ValidationError,
    WebDAVError,
)
from finance_tracker.ods_generator import (
    BudgetAllocation,
    ExpenseCategory,
    ExpenseEntry,
    OdsGenerator,
    create_monthly_budget,
)

# Phase 4 modules
from finance_tracker.recurring import (
    RecurrenceFrequency,
    RecurringExpense,
    RecurringExpenseManager,
)

# Renderer (NEW in v0.4.0)
from finance_tracker.renderer import (
    OdsRenderer,
    render_sheets,
)
from finance_tracker.report_generator import ReportGenerator
from finance_tracker.templates import (
    BudgetTemplate,
    get_template,
    list_templates,
)
from finance_tracker.webdav_upload import (
    NextcloudConfig,
    WebDAVClient,
    upload_budget,
)

__all__ = [
    "Alert",
    "AlertConfig",
    # Alerts
    "AlertMonitor",
    # Analytics
    "AnalyticsDashboard",
    "BudgetAllocation",
    # Core
    "BudgetAnalyzer",
    # Templates
    "BudgetTemplate",
    "CSVImportError",
    # CSV Import
    "CSVImporter",
    # Builder API (NEW)
    "CellRef",
    "CellSpec",
    "ColumnSpec",
    # Configuration
    "Config",
    "ConfigurationError",
    "ExpenseCategory",
    "ExpenseEntry",
    "FileError",
    # Exceptions
    "FinanceTrackerError",
    "FormulaBuilder",
    "NextcloudConfig",
    "OdsError",
    "OdsGenerator",
    # Renderer (NEW)
    "OdsRenderer",
    "RangeRef",
    "RecurrenceFrequency",
    # Recurring
    "RecurringExpense",
    "RecurringExpenseManager",
    "ReportGenerator",
    "RowSpec",
    "SheetRef",
    "SheetSpec",
    "SpreadsheetBuilder",
    "TemplateError",
    "TransactionCategorizer",
    "ValidationError",
    # WebDAV
    "WebDAVClient",
    "WebDAVError",
    "__author__",
    # Version info
    "__version__",
    "check_budget_alerts",
    "create_monthly_budget",
    "create_spreadsheet",
    "formula",
    "generate_dashboard",
    "get_config",
    "get_template",
    "import_bank_csv",
    "init_config_file",
    "list_templates",
    "render_sheets",
    "upload_budget",
]
