"""
Finance Tracker - Professional spreadsheet system with enterprise-grade formatting.

This package provides a comprehensive toolkit for creating professional-quality
ODS spreadsheets with complete formatting control, type-safe APIs, and
declarative YAML-based theming.

v2.0.0 - Professional Spreadsheet System (95/95 new requirements)
==================================================================

New in v2.0.0 (Professional Enhancement - ALL 95 REQUIREMENTS):
- FR-SCHEMA-*: Extended schema with Color, Font, Border, Typography, Print Layout
- FR-THEME-*: Enhanced theme system with inheritance and composition
- FR-FORMAT-*: Complete ODF formatting capabilities (cell, number, conditional)
- FR-COND-*: Conditional formatting engine with rules and criteria
- FR-VALID-*: Data validation system with type checking and constraints
- FR-CHART-*: Chart builder with all types (column, bar, line, area, pie, scatter, combo)
- FR-TEMPLATE-*: Template engine with schema, loader, renderer, component system
- FR-BUILDER-*: Enhanced builder API with charts, protection, freezing
- FR-PROF-*: Professional templates (enterprise budget, cash flow, invoice, expense report)
- FR-PRINT-*: Print layout optimization with page setup, headers/footers, breaks
- FR-ADV-*: Advanced features (named ranges, comments, filters, hyperlinks, images)
- DOC-PROF-*: Comprehensive guides (builder API, themes, templates, best practices)

New in v1.0.0 (Phase 5: Future Enhancements - FINAL):
- FR-IMPORT-003: Bank API Integration (Plaid)
- IR-MCP-002: Native MCP Server for AI integration
- FR-AI-010: AI training data export (anonymized)
- FR-HUMAN-002: Interactive features (dropdowns, validation)
- FR-HUMAN-003: Dashboard view in ODS

New in v0.7.0 (Phase 4: Advanced Features):
- FR-GOAL-001: Savings goals with progress tracking
- FR-GOAL-002: Debt payoff with snowball/avalanche methods
- FR-RECUR-002: Bill reminders with due date tracking
- IR-CAL-001: Calendar integration with ICS export
- IR-NOTIF-001: Notification system (email, ntfy.sh)
- FR-UX-009: Shell completions for Bash, Zsh, Fish

New in v0.6.0 (Phase 3: Enhanced Features):
- FR-CORE-004: Account management with balance tracking and transfers
- FR-CURR-001: Multi-currency support with 30+ currencies
- FR-IMPORT-002: Extended bank formats (50+ banks supported)
- FR-REPORT-003: Interactive visualization with Chart.js dashboards
- FR-AI-001: Enhanced AI export with cell relationships
- FR-AI-003: Semantic cell tagging for LLM integration

New in v0.5.0:
- DR-STORE-002: Backup/restore functionality with compression
- FR-DUAL-001/002: Dual export (ODS + AI-friendly JSON)
- FR-EXPORT-001: Multi-format export (XLSX, CSV, PDF)
- FR-UX-004: Confirmation prompts for destructive operations
- BackupManager for automatic and manual backups
- AIExporter for LLM-friendly JSON export
- MultiFormatExporter for XLSX/CSV/PDF export

New in v0.4.2:
- FR-SEC-001: Data encryption at rest (AES-256)
- Security module with FileEncryptor, CredentialStore
- Password strength checking and generation
- Security audit logging

New in v0.4.1:
- FR-CORE-003: Expense append functionality (fixes Gap G-02)
- FR-UX-003: Comprehensive error code system
- OdsEditor module for modifying existing ODS files
- CLI --dry-run flag for expense command

New in v0.4.0:
- Declarative DSL for themes and styling
- YAML-based theme definitions
- Fluent Builder API for spreadsheet construction
- Type-safe FormulaBuilder
- 5 built-in themes (default, corporate, minimal, dark, high_contrast)
- CLI --theme flag support
"""

__version__ = "2.0.0"
__author__ = "jallen"

# Account Management (NEW in v0.6.0 - Phase 3)
from finance_tracker.accounts import (
    Account,
    AccountManager,
    AccountTransaction,
    AccountType,
    NetWorth,
    Transfer,
    get_default_accounts,
)

# AI Export (Enhanced in v0.6.0)
from finance_tracker.ai_export import (
    AIExporter,
    CellRelationship,
    SemanticCell,
    SemanticCellType,
    SemanticSheet,
    SemanticTag,
    export_dual,
    export_for_ai,
)

# AI Training Data Export (NEW in v1.0.0 - Phase 5)
from finance_tracker.ai_training import (
    AnonymizationConfig,
    AnonymizationLevel,
    DataAnonymizer,
    PIIDetector,
    TrainingDataExporter,
    TrainingDataset,
    export_training_data,
)
from finance_tracker.alerts import (
    Alert,
    AlertConfig,
    AlertMonitor,
    check_budget_alerts,
)
from finance_tracker.analytics import (
    AnalyticsDashboard,
    generate_dashboard,
)

# Backup (NEW in v0.5.0)
from finance_tracker.backup import (
    BackupManager,
    BackupReason,
    auto_backup,
)

# Extended Bank Formats (NEW in v0.6.0 - Phase 3)
from finance_tracker.bank_formats import (
    BUILTIN_FORMATS,
    BankFormatDefinition,
    BankFormatRegistry,
    FormatBuilder,
    count_formats,
    detect_format,
    get_format,
    list_formats,
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

# ============================================================================
# v2.0.0 Professional Spreadsheet System (95 new requirements)
# ============================================================================
# Charts (NEW in v2.0.0 - FR-CHART-*)
from finance_tracker.charts import (
    AxisConfig,
    AxisType,
    ChartBuilder,
    ChartPosition,
    ChartSize,
    ChartSpec,
    ChartTitle,
    ChartType,
    DataLabelConfig,
    DataLabelPosition,
    DataSeries,
    LegendConfig,
    LegendPosition,
    PlotAreaStyle,
    Sparkline,
    SparklineBuilder,
    SparklineMarkers,
    SparklineType,
    Trendline,
    TrendlineType,
    budget_comparison_chart,
    chart,
    sparkline,
    spending_pie_chart,
    trend_line_chart,
)

# Shell Completions (NEW in v0.7.0 - Phase 4)
from finance_tracker.completions import (
    detect_shell,
    generate_bash_completions,
    generate_fish_completions,
    generate_zsh_completions,
    install_completions,
    print_completion_script,
)
from finance_tracker.config import (
    Config,
    get_config,
    init_config_file,
)
from finance_tracker.csv_import import (
    CSVImporter,
    TransactionCategorizer,
    import_bank_csv,
)

# Multi-Currency Support (NEW in v0.6.0 - Phase 3)
from finance_tracker.currency import (
    CURRENCIES,
    Currency,
    CurrencyCode,
    CurrencyConverter,
    ExchangeRate,
    ExchangeRateProvider,
    MoneyAmount,
    convert,
    format_currency,
    get_currency,
    list_currencies,
    money,
)
from finance_tracker.exceptions import (
    ConfigurationError,
    CSVImportError,
    DecryptionError,
    EncryptionError,
    FileError,
    FinanceTrackerError,
    IntegrityError,
    OdsError,
    OperationCancelledError,
    TemplateError,
    ValidationError,
    WebDAVError,
)

# Multi-format Export (NEW in v0.5.0)
from finance_tracker.export import (
    ExportFormat,
    ExportOptions,
    MultiFormatExporter,
    export_to_csv,
    export_to_pdf,
    export_to_xlsx,
)

# Goals and Debt Payoff (NEW in v0.7.0 - Phase 4)
from finance_tracker.goals import (
    Debt,
    DebtPayoffMethod,
    DebtPayoffPlan,
    GoalCategory,
    GoalManager,
    GoalStatus,
    SavingsGoal,
    compare_payoff_methods,
    create_debt_payoff_plan,
    create_emergency_fund,
)

# Interactive ODS Features (NEW in v1.0.0 - Phase 5)
from finance_tracker.interactive import (
    ConditionalFormat,
    DashboardKPI,
    DropdownList,
    InteractiveOdsBuilder,
    ValidationRule,
    add_interactive_features,
    generate_budget_dashboard,
)
from finance_tracker.interactive import (
    DashboardGenerator as OdsDashboardGenerator,
)

# MCP Server (NEW in v1.0.0 - Phase 5)
from finance_tracker.mcp_server import (
    MCPConfig,
    MCPServer,
    MCPTool,
    MCPToolResult,
    create_mcp_server,
)

# Notifications (NEW in v0.7.0 - Phase 4)
from finance_tracker.notifications import (
    EmailChannel,
    EmailConfig,
    Notification,
    NotificationManager,
    NotificationPriority,
    NotificationTemplates,
    NotificationType,
    NtfyChannel,
    NtfyConfig,
)

# ODS Editor (NEW in v0.4.1)
from finance_tracker.ods_editor import (
    OdsEditor,
    append_expense_to_file,
)
from finance_tracker.ods_generator import (
    BudgetAllocation,
    ExpenseCategory,
    ExpenseEntry,
    OdsGenerator,
    create_monthly_budget,
)

# Plaid Integration (NEW in v1.0.0 - Phase 5)
from finance_tracker.plaid_integration import (
    PlaidAccount,
    PlaidClient,
    PlaidConfig,
    PlaidSyncManager,
    PlaidTransaction,
    SyncResult,
)

# Recurring expenses (Enhanced in Phase 4)
from finance_tracker.recurring import (
    RecurrenceFrequency,
    RecurringExpense,
    RecurringExpenseManager,
)

# Bill Reminders (NEW in v0.7.0 - Phase 4)
from finance_tracker.reminders import (
    BillReminder,
    BillReminderManager,
    ReminderFrequency,
    ReminderStatus,
    create_bill_from_template,
)

# Renderer (NEW in v0.4.0)
from finance_tracker.renderer import (
    OdsRenderer,
    render_sheets,
)
from finance_tracker.report_generator import ReportGenerator

# Schema Extensions (NEW in v2.0.0 - FR-SCHEMA-*, FR-FORMAT-*, FR-ADV-*)
from finance_tracker.schema.advanced import (
    AutoFilter,
    CellComment,
    DataTable,
    FilterCriteria,
    HiddenRowsColumns,
    Hyperlink,
    Image,
    NamedRange,
    OutlineGroup,
    OutlineSettings,
    Shape,
)
from finance_tracker.schema.conditional import (
    ConditionalFormat,
    ConditionalRule,
)
from finance_tracker.schema.data_validation import (
    DataValidation,
    ValidationType,
)
from finance_tracker.schema.print_layout import (
    HeaderFooter,
    HeaderFooterContent,
    PageBreak,
    PageMargins,
    PageOrientation,
    PageSetup,
    PageSetupBuilder,
    PageSize,
    PrintPresets,
    PrintQuality,
    PrintScale,
    RepeatConfig,
)
from finance_tracker.schema.typography import (
    FontPairing,
    Typography,
)
from finance_tracker.schema.units import (
    Length,
    LengthUnit,
)

# Security (NEW in v0.4.2)
from finance_tracker.security import (
    CredentialStore,
    EncryptionMetadata,
    FileEncryptor,
    SecurityAuditLog,
    check_password_strength,
    generate_password,
)

# Template Engine (NEW in v2.0.0 - FR-TEMPLATE-*)
from finance_tracker.template_engine import (
    ComponentDefinition,
    TemplateLoader,
    TemplateRenderer,
    TemplateVariable,
)
from finance_tracker.templates import (
    get_template,
    list_templates,
)

# Financial Statement Templates (NEW in v2.0.0 - FR-PROF-*)
from finance_tracker.templates.financial_statements import (
    BalanceSheetTemplate,
    CashFlowStatementTemplate,
    EquityStatementTemplate,
    IncomeStatementTemplate,
)

# Professional Templates (NEW in v2.0.0 - FR-PROF-*)
from finance_tracker.templates.professional import (
    CashFlowTrackerTemplate,
    EnterpriseBudgetTemplate,
    ExpenseReportTemplate,
    InvoiceTemplate,
)

# Interactive Visualization (NEW in v0.6.0 - Phase 3)
from finance_tracker.visualization import (
    CATEGORY_COLORS,
    ChartConfig,
    ChartDataPoint,
    ChartGenerator,
    ChartSeries,
    ChartType,
    DashboardGenerator,
    create_budget_dashboard,
    create_spending_pie_chart,
)
from finance_tracker.webdav_upload import (
    NextcloudConfig,
    WebDAVClient,
    upload_budget,
)

__all__ = [
    "BUILTIN_FORMATS",
    # Visualization (v0.6.0)
    "CATEGORY_COLORS",
    # Multi-Currency (v0.6.0)
    "CURRENCIES",
    # AI Export (v0.6.0)
    "AIExporter",
    # Account Management (v0.6.0)
    "Account",
    "AccountManager",
    "AccountTransaction",
    "AccountType",
    "Alert",
    "AlertConfig",
    "AlertMonitor",
    "AnalyticsDashboard",
    # v2.0.0 Professional Spreadsheet System
    # AI Training (v1.0.0)
    "AnonymizationConfig",
    "AnonymizationLevel",
    "AutoFilter",
    "AxisConfig",
    "AxisType",
    # Backup (v0.5.0)
    "BackupManager",
    "BackupReason",
    "BalanceSheetTemplate",
    # Bank Formats (v0.6.0)
    "BankFormatDefinition",
    "BankFormatRegistry",
    # Bill Reminders (v0.7.0)
    "BillReminder",
    "BillReminderManager",
    "BudgetAllocation",
    "BudgetAnalyzer",
    "CSVImportError",
    "CSVImporter",
    "CashFlowStatementTemplate",
    "CashFlowTrackerTemplate",
    "CellComment",
    # Builder API (v0.4.0)
    "CellRef",
    "CellRelationship",
    "CellSpec",
    "ChartBuilder",
    "ChartConfig",
    "ChartDataPoint",
    "ChartGenerator",
    "ChartPosition",
    "ChartSeries",
    "ChartSize",
    "ChartSpec",
    "ChartTitle",
    "ChartType",
    "ColumnSpec",
    # Interactive ODS (v1.0.0)
    "ConditionalFormat",
    "ConditionalRule",
    "Config",
    "ConfigurationError",
    "CredentialStore",
    "Currency",
    "CurrencyCode",
    "CurrencyConverter",
    "DashboardGenerator",
    "DashboardKPI",
    "DataAnonymizer",
    "DataLabelConfig",
    "DataLabelPosition",
    "DataSeries",
    "DataTable",
    "DataValidation",
    # Goals (v0.7.0)
    "Debt",
    "DebtPayoffMethod",
    "DebtPayoffPlan",
    "DecryptionError",
    "DropdownList",
    # Notifications (v0.7.0)
    "EmailChannel",
    "EmailConfig",
    "EncryptionError",
    "EncryptionMetadata",
    "EnterpriseBudgetTemplate",
    "EquityStatementTemplate",
    "ExchangeRate",
    "ExchangeRateProvider",
    "ExpenseCategory",
    "ExpenseEntry",
    "ExpenseReportTemplate",
    # Export (v0.5.0)
    "ExportFormat",
    "ExportOptions",
    "FileEncryptor",
    "FileError",
    "FilterCriteria",
    "FinanceTrackerError",
    "FontPairing",
    "FormatBuilder",
    "FormulaBuilder",
    "GoalCategory",
    "GoalManager",
    "GoalStatus",
    "HeaderFooter",
    "HeaderFooterContent",
    "HiddenRowsColumns",
    "Hyperlink",
    "Image",
    "IncomeStatementTemplate",
    "IntegrityError",
    "InteractiveOdsBuilder",
    "InvoiceTemplate",
    "LegendConfig",
    "LegendPosition",
    "Length",
    "LengthUnit",
    # MCP Server (v1.0.0)
    "MCPConfig",
    "MCPServer",
    "MCPTool",
    "MCPToolResult",
    "MoneyAmount",
    "MultiFormatExporter",
    "NamedRange",
    "NetWorth",
    "NextcloudConfig",
    "Notification",
    "NotificationManager",
    "NotificationPriority",
    "NotificationTemplates",
    "NotificationType",
    "NtfyChannel",
    "NtfyConfig",
    "OdsDashboardGenerator",
    "OdsEditor",
    "OdsError",
    "OdsGenerator",
    "OdsRenderer",
    "OperationCancelledError",
    "OutlineGroup",
    "OutlineSettings",
    "PIIDetector",
    "PageBreak",
    "PageMargins",
    "PageOrientation",
    "PageSetup",
    "PageSetupBuilder",
    "PageSize",
    # Plaid (v1.0.0)
    "PlaidAccount",
    "PlaidClient",
    "PlaidConfig",
    "PlaidSyncManager",
    "PlaidTransaction",
    "PlotAreaStyle",
    "PrintPresets",
    "PrintQuality",
    "PrintScale",
    "RangeRef",
    "RecurrenceFrequency",
    "RecurringExpense",
    "RecurringExpenseManager",
    "ReminderFrequency",
    "ReminderStatus",
    "RepeatConfig",
    "ReportGenerator",
    "RowSpec",
    "SavingsGoal",
    "SecurityAuditLog",
    "SemanticCell",
    "SemanticCellType",
    "SemanticSheet",
    "SemanticTag",
    "Shape",
    "SheetRef",
    "SheetSpec",
    "Sparkline",
    "SparklineBuilder",
    "SparklineMarkers",
    "SparklineType",
    "SpreadsheetBuilder",
    "SyncResult",
    "ComponentDefinition",
    "TemplateError",
    "TemplateLoader",
    "TemplateRenderer",
    "TemplateVariable",
    "TrainingDataExporter",
    "TrainingDataset",
    "TransactionCategorizer",
    "Transfer",
    "Trendline",
    "TrendlineType",
    "Typography",
    "ValidationError",
    "ValidationRule",
    "ValidationType",
    "WebDAVClient",
    "WebDAVError",
    "__author__",
    "__version__",
    "add_interactive_features",
    "append_expense_to_file",
    "auto_backup",
    "budget_comparison_chart",
    "chart",
    "check_budget_alerts",
    "check_password_strength",
    "compare_payoff_methods",
    "convert",
    "count_formats",
    "create_bill_from_template",
    "create_budget_dashboard",
    "create_debt_payoff_plan",
    "create_emergency_fund",
    "create_mcp_server",
    "create_monthly_budget",
    "create_spending_pie_chart",
    "create_spreadsheet",
    "detect_format",
    "detect_shell",
    "export_dual",
    "export_for_ai",
    "export_to_csv",
    "export_to_pdf",
    "export_to_xlsx",
    "export_training_data",
    "format_currency",
    "formula",
    "generate_bash_completions",
    "generate_budget_dashboard",
    "generate_dashboard",
    "generate_fish_completions",
    "generate_password",
    "generate_zsh_completions",
    "get_config",
    "get_currency",
    "get_default_accounts",
    "get_format",
    "get_template",
    "import_bank_csv",
    "init_config_file",
    "install_completions",
    "list_currencies",
    "list_formats",
    "list_templates",
    "money",
    "print_completion_script",
    "render_sheets",
    "sparkline",
    "spending_pie_chart",
    "trend_line_chart",
    "upload_budget",
]
