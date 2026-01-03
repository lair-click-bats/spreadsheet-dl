"""
SpreadsheetDL - Universal spreadsheet definition language with LLM-optimized MCP server.

This package provides a comprehensive toolkit for creating professional-quality
spreadsheets (ODS, XLSX, CSV) with complete formatting control, type-safe APIs,
declarative YAML-based theming, and an MCP server for AI integration.

v4.0.0 - SpreadsheetDL (Universal Spreadsheet Definition Language)
===================================================================

New in v4.0.0:
- Universal spreadsheet definition format (SpreadsheetDL)
- LLM-optimized MCP server with 145+ tools
- Multi-format support (ODS, XLSX, CSV, PDF)
- Theme variants (light, dark, high-contrast)
- Streaming I/O for 100k+ rows (TASK-401)
- Round-trip serialization (TASK-402)
- Format adapters (TASK-403)
- Chart rendering to ODS (TASK-231)
- 34 core model types with frozen dataclasses

Legacy Features (from v2.0.0):
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

__version__ = "4.0.0"
__author__ = "jallen"

# Account Management (NEW in v0.6.0 - Phase 3)
from spreadsheet_dl.accounts import (
    Account,
    AccountManager,
    AccountTransaction,
    AccountType,
    NetWorth,
    Transfer,
    get_default_accounts,
)

# Format Adapters (NEW in v4.0.0 - TASK-403)
from spreadsheet_dl.adapters import (
    AdapterOptions,
    AdapterRegistry,
    CsvAdapter,
    ExportFormat,
    FormatAdapter,
    HtmlAdapter,
    ImportFormat,
    JsonAdapter,
    OdsAdapter,
    TsvAdapter,
    export_to,
    import_from,
)

# AI Export (Enhanced in v0.6.0)
from spreadsheet_dl.ai_export import (
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
from spreadsheet_dl.ai_training import (
    AnonymizationConfig,
    AnonymizationLevel,
    DataAnonymizer,
    PIIDetector,
    TrainingDataExporter,
    TrainingDataset,
    export_training_data,
)
from spreadsheet_dl.alerts import (
    Alert,
    AlertConfig,
    AlertMonitor,
    check_budget_alerts,
)
from spreadsheet_dl.analytics import (
    AnalyticsDashboard,
    generate_dashboard,
)

# Backup (NEW in v0.5.0)
from spreadsheet_dl.backup import (
    BackupManager,
    BackupReason,
    auto_backup,
)

# Extended Bank Formats (NEW in v0.6.0 - Phase 3)
from spreadsheet_dl.bank_formats import (
    BUILTIN_FORMATS,
    BankFormatDefinition,
    BankFormatRegistry,
    FormatBuilder,
    count_formats,
    detect_format,
    get_format,
    list_formats,
)
from spreadsheet_dl.budget_analyzer import BudgetAnalyzer

# Builder API (NEW in v0.4.0)
from spreadsheet_dl.builder import (
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
from spreadsheet_dl.charts import (
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
from spreadsheet_dl.completions import (
    detect_shell,
    generate_bash_completions,
    generate_fish_completions,
    generate_zsh_completions,
    install_completions,
    print_completion_script,
)
from spreadsheet_dl.config import (
    Config,
    get_config,
    init_config_file,
)
from spreadsheet_dl.csv_import import (
    CSVImporter,
    TransactionCategorizer,
    import_bank_csv,
)

# Multi-Currency Support (NEW in v0.6.0 - Phase 3)
from spreadsheet_dl.currency import (
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
from spreadsheet_dl.exceptions import (
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
from spreadsheet_dl.export import (
    ExportOptions,
    MultiFormatExporter,
    export_to_csv,
    export_to_pdf,
    export_to_xlsx,
)

# Goals and Debt Payoff (NEW in v0.7.0 - Phase 4)
from spreadsheet_dl.goals import (
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
from spreadsheet_dl.interactive import (
    DashboardGenerator as OdsDashboardGenerator,
)

# Interactive ODS Features (NEW in v1.0.0 - Phase 5)
from spreadsheet_dl.interactive import (
    DashboardKPI,
    DropdownList,
    InteractiveOdsBuilder,
    ValidationRule,
    add_interactive_features,
    generate_budget_dashboard,
)

# MCP Server (NEW in v1.0.0 - Phase 5)
from spreadsheet_dl.mcp_server import (
    MCPConfig,
    MCPServer,
    MCPTool,
    MCPToolResult,
    create_mcp_server,
)

# Notifications (NEW in v0.7.0 - Phase 4)
from spreadsheet_dl.notifications import (
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
from spreadsheet_dl.ods_editor import (
    OdsEditor,
    append_expense_to_file,
)
from spreadsheet_dl.ods_generator import (
    BudgetAllocation,
    ExpenseCategory,
    ExpenseEntry,
    OdsGenerator,
    create_monthly_budget,
)

# Plaid Integration (NEW in v1.0.0 - Phase 5)
from spreadsheet_dl.plaid_integration import (
    PlaidAccount,
    PlaidClient,
    PlaidConfig,
    PlaidSyncManager,
    PlaidTransaction,
    SyncResult,
)

# Recurring expenses (Enhanced in Phase 4)
from spreadsheet_dl.recurring import (
    RecurrenceFrequency,
    RecurringExpense,
    RecurringExpenseManager,
)

# Bill Reminders (NEW in v0.7.0 - Phase 4)
from spreadsheet_dl.reminders import (
    BillReminder,
    BillReminderManager,
    ReminderFrequency,
    ReminderStatus,
    create_bill_from_template,
)

# Renderer (NEW in v0.4.0)
from spreadsheet_dl.renderer import (
    OdsRenderer,
    render_sheets,
)
from spreadsheet_dl.report_generator import ReportGenerator

# Schema Extensions (NEW in v2.0.0 - FR-SCHEMA-*, FR-FORMAT-*, FR-ADV-*)
from spreadsheet_dl.schema.advanced import (
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
from spreadsheet_dl.schema.conditional import (
    ConditionalFormat,
    ConditionalRule,
)
from spreadsheet_dl.schema.data_validation import (
    DataValidation,
    ValidationType,
)
from spreadsheet_dl.schema.print_layout import (
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
from spreadsheet_dl.schema.typography import (
    FontPairing,
    Typography,
)
from spreadsheet_dl.schema.units import (
    Length,
    LengthUnit,
)

# Security (NEW in v0.4.2)
from spreadsheet_dl.security import (
    CredentialStore,
    EncryptionMetadata,
    FileEncryptor,
    SecurityAuditLog,
    check_password_strength,
    generate_password,
)

# Serialization (NEW in v4.0.0 - TASK-402)
from spreadsheet_dl.serialization import (
    DefinitionFormat,
    Serializer,
    SpreadsheetDecoder,
    SpreadsheetEncoder,
    load_definition,
    save_definition,
)

# Streaming I/O (NEW in v4.0.0 - TASK-401)
from spreadsheet_dl.streaming import (
    StreamingCell,
    StreamingReader,
    StreamingRow,
    StreamingWriter,
    stream_read,
    stream_write,
)

# Template Engine (NEW in v2.0.0 - FR-TEMPLATE-*)
from spreadsheet_dl.template_engine import (
    ComponentDefinition,
    TemplateLoader,
    TemplateRenderer,
    TemplateVariable,
)
from spreadsheet_dl.templates import (
    get_template,
    list_templates,
)

# Financial Statement Templates (NEW in v2.0.0 - FR-PROF-*)
from spreadsheet_dl.templates.financial_statements import (
    BalanceSheetTemplate,
    CashFlowStatementTemplate,
    EquityStatementTemplate,
    IncomeStatementTemplate,
)

# Professional Templates (NEW in v2.0.0 - FR-PROF-*)
from spreadsheet_dl.templates.professional import (
    CashFlowTrackerTemplate,
    EnterpriseBudgetTemplate,
    ExpenseReportTemplate,
    InvoiceTemplate,
)

# Interactive Visualization (NEW in v0.6.0 - Phase 3)
from spreadsheet_dl.visualization import (
    CATEGORY_COLORS,
    ChartConfig,
    ChartDataPoint,
    ChartGenerator,
    ChartSeries,
    DashboardGenerator,
    create_budget_dashboard,
    create_spending_pie_chart,
)
from spreadsheet_dl.webdav_upload import (
    NextcloudConfig,
    WebDAVClient,
    upload_budget,
)

__all__ = [
    # Constants (uppercase first)
    "BUILTIN_FORMATS",
    "CATEGORY_COLORS",
    "CURRENCIES",
    # Classes (alphabetical)
    "AIExporter",
    "Account",
    "AccountManager",
    "AccountTransaction",
    "AccountType",
    "AdapterOptions",
    "AdapterRegistry",
    "Alert",
    "AlertConfig",
    "AlertMonitor",
    "AnalyticsDashboard",
    "AnonymizationConfig",
    "AnonymizationLevel",
    "AutoFilter",
    "AxisConfig",
    "AxisType",
    "BackupManager",
    "BackupReason",
    "BalanceSheetTemplate",
    "BankFormatDefinition",
    "BankFormatRegistry",
    "BillReminder",
    "BillReminderManager",
    "BudgetAllocation",
    "BudgetAnalyzer",
    "CSVImportError",
    "CSVImporter",
    "CashFlowStatementTemplate",
    "CashFlowTrackerTemplate",
    "CellComment",
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
    "ComponentDefinition",
    "ConditionalFormat",
    "ConditionalRule",
    "Config",
    "ConfigurationError",
    "CredentialStore",
    "CsvAdapter",
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
    "Debt",
    "DebtPayoffMethod",
    "DebtPayoffPlan",
    "DecryptionError",
    "DefinitionFormat",
    "DropdownList",
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
    "ExportFormat",
    "ExportOptions",
    "FileEncryptor",
    "FileError",
    "FilterCriteria",
    "FinanceTrackerError",
    "FontPairing",
    "FormatAdapter",
    "FormatBuilder",
    "FormulaBuilder",
    "GoalCategory",
    "GoalManager",
    "GoalStatus",
    "HeaderFooter",
    "HeaderFooterContent",
    "HiddenRowsColumns",
    "HtmlAdapter",
    "Hyperlink",
    "Image",
    "ImportFormat",
    "IncomeStatementTemplate",
    "IntegrityError",
    "InteractiveOdsBuilder",
    "InvoiceTemplate",
    "JsonAdapter",
    "LegendConfig",
    "LegendPosition",
    "Length",
    "LengthUnit",
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
    "OdsAdapter",
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
    "Serializer",
    "Shape",
    "SheetRef",
    "SheetSpec",
    "Sparkline",
    "SparklineBuilder",
    "SparklineMarkers",
    "SparklineType",
    "SpreadsheetBuilder",
    "SpreadsheetDecoder",
    "SpreadsheetEncoder",
    "StreamingCell",
    "StreamingReader",
    "StreamingRow",
    "StreamingWriter",
    "SyncResult",
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
    "TsvAdapter",
    "Typography",
    "ValidationError",
    "ValidationRule",
    "ValidationType",
    "WebDAVClient",
    "WebDAVError",
    # Dunder attributes
    "__author__",
    "__version__",
    # Functions (alphabetical)
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
    "export_to",
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
    "import_from",
    "init_config_file",
    "install_completions",
    "list_currencies",
    "list_formats",
    "list_templates",
    "load_definition",
    "money",
    "print_completion_script",
    "render_sheets",
    "save_definition",
    "sparkline",
    "spending_pie_chart",
    "stream_read",
    "stream_write",
    "trend_line_chart",
    "upload_budget",
]
