"""
Command-line interface for finance tracker.

Provides CLI commands for generating budgets, analyzing spending,
creating reports, and managing finances.

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

import argparse
import json
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from spreadsheet_dl import __version__
from spreadsheet_dl.exceptions import (
    FinanceTrackerError,
    InvalidAmountError,
    InvalidCategoryError,
    InvalidDateError,
    OperationCancelledError,
)

# =============================================================================
# Confirmation Prompt Utilities (FR-UX-004)
# =============================================================================


def confirm_action(
    message: str,
    *,
    default: bool = False,
    skip_confirm: bool = False,
) -> bool:
    """
    Prompt user for confirmation before destructive actions.

    Args:
        message: Description of the action to confirm.
        default: Default response if user just presses Enter.
        skip_confirm: If True, skip confirmation and return True.

    Returns:
        True if action is confirmed, False otherwise.

    Implements:
        FR-UX-004: Confirmation prompts for destructive operations.
    """
    if skip_confirm:
        return True

    # Non-interactive mode check
    if not sys.stdin.isatty():
        return default

    prompt_suffix = " [Y/n]" if default else " [y/N]"
    full_prompt = f"{message}{prompt_suffix}: "

    try:
        response = input(full_prompt).strip().lower()
        if not response:
            return default
        return response in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        print()
        return False


def confirm_overwrite(file_path: Path, *, skip_confirm: bool = False) -> bool:
    """
    Confirm overwriting an existing file.

    Args:
        file_path: Path to the file that would be overwritten.
        skip_confirm: If True, skip confirmation.

    Returns:
        True if overwrite is confirmed.
    """
    if not file_path.exists():
        return True

    return confirm_action(
        f"File '{file_path}' already exists. Overwrite?",
        default=False,
        skip_confirm=skip_confirm,
    )


def confirm_delete(file_path: Path, *, skip_confirm: bool = False) -> bool:
    """
    Confirm deleting a file.

    Args:
        file_path: Path to the file to delete.
        skip_confirm: If True, skip confirmation.

    Returns:
        True if deletion is confirmed.
    """
    return confirm_action(
        f"Delete '{file_path}'? This cannot be undone.",
        default=False,
        skip_confirm=skip_confirm,
    )


def confirm_destructive_operation(
    operation: str,
    details: str | None = None,
    *,
    skip_confirm: bool = False,
) -> bool:
    """
    Confirm a potentially destructive operation.

    Args:
        operation: Name of the operation.
        details: Additional details about what will happen.
        skip_confirm: If True, skip confirmation.

    Returns:
        True if operation is confirmed.
    """
    message = f"Proceed with {operation}?"
    if details:
        print(f"\n{details}")
    return confirm_action(message, default=False, skip_confirm=skip_confirm)


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        prog="spreadsheet-dl",
        description="Family financial tracking with ODS spreadsheets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  spreadsheet-dl generate -o output/
  spreadsheet-dl generate -o output/ --theme corporate
  spreadsheet-dl analyze budget.ods --json
  spreadsheet-dl report budget.ods -f markdown
  spreadsheet-dl expense 25.50 "Coffee shop" -c "Dining Out"
  spreadsheet-dl import bank_export.csv --preview
  spreadsheet-dl export budget.ods -f xlsx
  spreadsheet-dl backup budget.ods
  spreadsheet-dl dashboard budget.ods
  spreadsheet-dl visualize budget.ods -o dashboard.html
  spreadsheet-dl account add "Primary Checking" --type checking
  spreadsheet-dl account list
  spreadsheet-dl category add "Pet Care" --color "#795548"
  spreadsheet-dl category list
  spreadsheet-dl plugin list
  spreadsheet-dl plugin enable my_plugin
  spreadsheet-dl banks --list
  spreadsheet-dl templates
  spreadsheet-dl themes

For more information, visit: https://github.com/lair-click-bats/spreadsheet-dl
""",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program version and exit",
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file",
        metavar="FILE",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    # Global confirmation skip flag
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip confirmation prompts (answer yes to all)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    gen_parser = subparsers.add_parser(
        "generate",
        help="Generate budget spreadsheet",
        description="Create a new budget tracking ODS spreadsheet.",
    )
    gen_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path.cwd(),
        help="Output directory or file path (default: current directory)",
    )
    gen_parser.add_argument(
        "-m",
        "--month",
        type=int,
        choices=range(1, 13),
        metavar="MONTH",
        help="Month number (1-12, default: current month)",
    )
    gen_parser.add_argument(
        "-y",
        "--year",
        type=int,
        help="Year (default: current year)",
    )
    gen_parser.add_argument(
        "-t",
        "--template",
        type=str,
        help="Budget template (50_30_20, family, minimalist, zero_based, fire, high_income)",
    )
    gen_parser.add_argument(
        "--theme",
        type=str,
        help="Visual theme (default, corporate, minimal, dark, high_contrast)",
    )
    gen_parser.add_argument(
        "--empty-rows",
        type=int,
        default=50,
        help="Number of empty rows for data entry (default: 50)",
    )
    gen_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing file without confirmation",
    )

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze budget file",
        description="Analyze an existing budget ODS file and show spending summary.",
    )
    analyze_parser.add_argument(
        "file",
        type=Path,
        help="Path to ODS budget file",
    )
    analyze_parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )
    analyze_parser.add_argument(
        "--category",
        type=str,
        help="Filter by category",
    )
    analyze_parser.add_argument(
        "--start-date",
        type=str,
        help="Start date (YYYY-MM-DD)",
    )
    analyze_parser.add_argument(
        "--end-date",
        type=str,
        help="End date (YYYY-MM-DD)",
    )

    # Report command
    report_parser = subparsers.add_parser(
        "report",
        help="Generate report",
        description="Generate a formatted report from a budget file.",
    )
    report_parser.add_argument(
        "file",
        type=Path,
        help="Path to ODS budget file",
    )
    report_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file path (optional, prints to stdout if not specified)",
    )
    report_parser.add_argument(
        "-f",
        "--format",
        choices=["text", "markdown", "json"],
        default="markdown",
        help="Report format (default: markdown)",
    )

    # Quick expense command
    expense_parser = subparsers.add_parser(
        "expense",
        help="Quick expense entry",
        description="Add a quick expense entry to a budget file.",
    )
    expense_parser.add_argument(
        "amount",
        type=str,
        help="Expense amount (e.g., 25.50 or $25.50)",
    )
    expense_parser.add_argument(
        "description",
        type=str,
        help="Expense description",
    )
    expense_parser.add_argument(
        "-c",
        "--category",
        type=str,
        help="Category (auto-detected if not specified)",
    )
    expense_parser.add_argument(
        "-f",
        "--file",
        type=Path,
        help="ODS file to update (uses most recent if not specified)",
    )
    expense_parser.add_argument(
        "-d",
        "--date",
        type=str,
        help="Date (YYYY-MM-DD, defaults to today)",
    )
    expense_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be added without modifying the file",
    )

    # Import CSV command
    import_parser = subparsers.add_parser(
        "import",
        help="Import bank CSV",
        description="Import transactions from a bank CSV export.",
    )
    import_parser.add_argument(
        "csv_file",
        type=Path,
        help="Path to CSV file",
    )
    import_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output ODS file",
    )
    import_parser.add_argument(
        "-b",
        "--bank",
        type=str,
        default="auto",
        help="Bank format (use 'banks --list' to see available formats)",
    )
    import_parser.add_argument(
        "--preview",
        action="store_true",
        help="Preview import without writing",
    )
    import_parser.add_argument(
        "--theme",
        type=str,
        help="Visual theme for output file",
    )
    import_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing output file without confirmation",
    )

    # Export command (FR-EXPORT-001)
    export_parser = subparsers.add_parser(
        "export",
        help="Export to other formats",
        description="Export ODS file to Excel, CSV, PDF, or JSON format.",
    )
    export_parser.add_argument(
        "file",
        type=Path,
        help="Path to ODS budget file",
    )
    export_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file path (default: same name with new extension)",
    )
    export_parser.add_argument(
        "-f",
        "--format",
        choices=["xlsx", "csv", "pdf", "json"],
        required=True,
        help="Export format",
    )
    export_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing file without confirmation",
    )

    # Export-dual command (FR-DUAL-001/002)
    export_dual_parser = subparsers.add_parser(
        "export-dual",
        help="Export to ODS + AI-friendly JSON",
        description="Export to both ODS copy and AI-readable JSON for LLM integration.",
    )
    export_dual_parser.add_argument(
        "file",
        type=Path,
        help="Path to ODS budget file",
    )
    export_dual_parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Output directory (default: same as source)",
    )

    # Backup command (DR-STORE-002)
    backup_parser = subparsers.add_parser(
        "backup",
        help="Backup budget files",
        description="Create a backup of a budget file.",
    )
    backup_parser.add_argument(
        "file",
        type=Path,
        help="Path to file to backup",
    )
    backup_parser.add_argument(
        "--list",
        action="store_true",
        help="List available backups for this file",
    )
    backup_parser.add_argument(
        "--restore",
        type=Path,
        metavar="BACKUP_FILE",
        help="Restore from a specific backup file",
    )
    backup_parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Remove backups older than retention period",
    )
    backup_parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Retention period in days (default: 30)",
    )
    backup_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    backup_parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation for restore/cleanup",
    )

    # Upload command
    upload_parser = subparsers.add_parser(
        "upload",
        help="Upload to Nextcloud",
        description="Upload a budget file to Nextcloud via WebDAV.",
    )
    upload_parser.add_argument(
        "file",
        type=Path,
        help="File to upload",
    )
    upload_parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Remote path on Nextcloud",
    )

    # Dashboard command
    dashboard_parser = subparsers.add_parser(
        "dashboard",
        help="Analytics dashboard",
        description="Display an analytics dashboard for a budget file.",
    )
    dashboard_parser.add_argument(
        "file",
        type=Path,
        help="Path to ODS budget file",
    )
    dashboard_parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    # Visualize command (NEW - Phase 3 FR-REPORT-003)
    visualize_parser = subparsers.add_parser(
        "visualize",
        help="Generate interactive charts",
        description="Generate interactive HTML charts and dashboards.",
    )
    visualize_parser.add_argument(
        "file",
        type=Path,
        help="Path to ODS budget file",
    )
    visualize_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output HTML file (default: budget_dashboard.html)",
    )
    visualize_parser.add_argument(
        "-t",
        "--type",
        choices=["dashboard", "pie", "bar", "trend"],
        default="dashboard",
        help="Chart type (default: dashboard)",
    )
    visualize_parser.add_argument(
        "--theme",
        choices=["default", "dark"],
        default="default",
        help="Visual theme (default: default)",
    )

    # Account command (NEW - Phase 3 FR-CORE-004)
    account_parser = subparsers.add_parser(
        "account",
        help="Manage financial accounts",
        description="Manage accounts, balances, and transfers.",
    )
    account_subparsers = account_parser.add_subparsers(dest="account_action")

    # Account add
    account_add = account_subparsers.add_parser("add", help="Add a new account")
    account_add.add_argument("name", help="Account name")
    account_add.add_argument(
        "--type",
        choices=["checking", "savings", "credit", "investment", "cash", "retirement"],
        default="checking",
        help="Account type",
    )
    account_add.add_argument("--institution", help="Financial institution")
    account_add.add_argument("--balance", type=float, default=0, help="Initial balance")
    account_add.add_argument("--currency", default="USD", help="Currency code")

    # Account list
    account_list = account_subparsers.add_parser("list", help="List accounts")
    account_list.add_argument("--type", help="Filter by account type")
    account_list.add_argument("--json", action="store_true", help="Output as JSON")

    # Account balance
    account_balance = account_subparsers.add_parser(
        "balance", help="Show account balance"
    )
    account_balance.add_argument("name", nargs="?", help="Account name (or all)")

    # Account transfer
    account_transfer = account_subparsers.add_parser(
        "transfer", help="Transfer between accounts"
    )
    account_transfer.add_argument("from_account", help="Source account name")
    account_transfer.add_argument("to_account", help="Destination account name")
    account_transfer.add_argument("amount", type=float, help="Amount to transfer")

    # Account net-worth
    account_networth = account_subparsers.add_parser(
        "net-worth", help="Calculate net worth"
    )
    account_networth.add_argument("--json", action="store_true", help="Output as JSON")

    # Category command (NEW - v4.0 FR-EXT-005)
    category_parser = subparsers.add_parser(
        "category",
        help="Manage expense categories",
        description="Add, edit, delete, and list expense categories.",
    )
    category_subparsers = category_parser.add_subparsers(dest="category_action")

    # Category add
    category_add = category_subparsers.add_parser("add", help="Add a custom category")
    category_add.add_argument("name", help="Category name")
    category_add.add_argument("--color", default="#6B7280", help="Color (hex code)")
    category_add.add_argument("--icon", help="Icon name or emoji")
    category_add.add_argument("--description", help="Category description")
    category_add.add_argument("--parent", help="Parent category name")
    category_add.add_argument(
        "--budget", type=float, default=0, help="Default monthly budget"
    )

    # Category list
    category_list = category_subparsers.add_parser("list", help="List all categories")
    category_list.add_argument(
        "--custom-only", action="store_true", help="Show only custom categories"
    )
    category_list.add_argument(
        "--include-hidden", action="store_true", help="Include hidden categories"
    )
    category_list.add_argument("--json", action="store_true", help="Output as JSON")

    # Category update
    category_update = category_subparsers.add_parser("update", help="Update a category")
    category_update.add_argument("name", help="Category name to update")
    category_update.add_argument("--color", help="New color (hex code)")
    category_update.add_argument("--icon", help="New icon")
    category_update.add_argument("--description", help="New description")
    category_update.add_argument("--rename", help="Rename category to this name")
    category_update.add_argument(
        "--hide", action="store_true", help="Hide category from lists"
    )
    category_update.add_argument(
        "--unhide", action="store_true", help="Unhide category"
    )
    category_update.add_argument("--budget", type=float, help="New default budget")

    # Category delete
    category_delete = category_subparsers.add_parser(
        "delete", help="Delete a custom category"
    )
    category_delete.add_argument("name", help="Category name to delete")
    category_delete.add_argument(
        "--force", action="store_true", help="Force delete even if has sub-categories"
    )

    # Category search
    category_search = category_subparsers.add_parser("search", help="Search categories")
    category_search.add_argument("query", help="Search query")
    category_search.add_argument("--json", action="store_true", help="Output as JSON")

    # Category suggest
    category_suggest = category_subparsers.add_parser(
        "suggest", help="Suggest category for expense description"
    )
    category_suggest.add_argument("description", help="Expense description")

    # Banks command (NEW - Phase 3 FR-IMPORT-002)
    banks_parser = subparsers.add_parser(
        "banks",
        help="List supported bank formats",
        description="List and manage bank CSV format definitions.",
    )
    banks_parser.add_argument(
        "--list",
        action="store_true",
        help="List all supported bank formats",
    )
    banks_parser.add_argument(
        "--search",
        type=str,
        help="Search for banks by name",
    )
    banks_parser.add_argument(
        "--type",
        choices=["checking", "credit", "savings", "investment"],
        help="Filter by account type",
    )
    banks_parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )
    banks_parser.add_argument(
        "--detect",
        type=Path,
        help="Detect format from CSV file",
    )

    # Currency command (NEW - Phase 3 FR-CURR-001)
    currency_parser = subparsers.add_parser(
        "currency",
        help="Currency conversion utilities",
        description="Convert between currencies and view exchange rates.",
    )
    currency_parser.add_argument(
        "amount",
        type=float,
        nargs="?",
        help="Amount to convert",
    )
    currency_parser.add_argument(
        "--from",
        dest="from_currency",
        default="USD",
        help="Source currency (default: USD)",
    )
    currency_parser.add_argument(
        "--to",
        dest="to_currency",
        help="Target currency",
    )
    currency_parser.add_argument(
        "--list",
        action="store_true",
        help="List supported currencies",
    )
    currency_parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    # Alerts command
    alerts_parser = subparsers.add_parser(
        "alerts",
        help="Check budget alerts",
        description="Check for budget alerts and warnings.",
    )
    alerts_parser.add_argument(
        "file",
        type=Path,
        help="Path to ODS budget file",
    )
    alerts_parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )
    alerts_parser.add_argument(
        "--critical-only",
        action="store_true",
        help="Show only critical alerts",
    )

    # Templates command
    templates_parser = subparsers.add_parser(
        "templates",
        help="List budget templates",
        description="List available budget templates.",
    )
    templates_parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    # Themes command
    themes_parser = subparsers.add_parser(
        "themes",
        help="List visual themes",
        description="List available visual themes for spreadsheets.",
    )
    themes_parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    # Config command
    config_parser = subparsers.add_parser(
        "config",
        help="Manage configuration",
        description="View or initialize configuration.",
    )
    config_parser.add_argument(
        "--init",
        action="store_true",
        help="Initialize a new configuration file",
    )
    config_parser.add_argument(
        "--show",
        action="store_true",
        help="Show current configuration",
    )
    config_parser.add_argument(
        "--path",
        type=Path,
        help="Path for configuration file",
    )

    # Plugin command (NEW - v4.0 FR-EXT-001)
    plugin_parser = subparsers.add_parser(
        "plugin",
        help="Manage plugins",
        description="Manage SpreadsheetDL plugins for extensibility.",
    )
    plugin_subparsers = plugin_parser.add_subparsers(dest="plugin_action")

    # Plugin list
    plugin_list = plugin_subparsers.add_parser("list", help="List all plugins")
    plugin_list.add_argument(
        "--enabled-only", action="store_true", help="Show only enabled plugins"
    )
    plugin_list.add_argument("--json", action="store_true", help="Output as JSON")

    # Plugin enable
    plugin_enable = plugin_subparsers.add_parser("enable", help="Enable a plugin")
    plugin_enable.add_argument("name", help="Plugin name to enable")
    plugin_enable.add_argument(
        "--config", type=str, help="Plugin configuration (JSON string)"
    )

    # Plugin disable
    plugin_disable = plugin_subparsers.add_parser("disable", help="Disable a plugin")
    plugin_disable.add_argument("name", help="Plugin name to disable")

    # Plugin info
    plugin_info = plugin_subparsers.add_parser("info", help="Show plugin information")
    plugin_info.add_argument("name", help="Plugin name")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    try:
        if args.command == "generate":
            return _cmd_generate(args)
        elif args.command == "analyze":
            return _cmd_analyze(args)
        elif args.command == "report":
            return _cmd_report(args)
        elif args.command == "expense":
            return _cmd_expense(args)
        elif args.command == "import":
            return _cmd_import(args)
        elif args.command == "export":
            return _cmd_export(args)
        elif args.command == "export-dual":
            return _cmd_export_dual(args)
        elif args.command == "backup":
            return _cmd_backup(args)
        elif args.command == "upload":
            return _cmd_upload(args)
        elif args.command == "dashboard":
            return _cmd_dashboard(args)
        elif args.command == "visualize":
            return _cmd_visualize(args)
        elif args.command == "account":
            return _cmd_account(args)
        elif args.command == "category":
            return _cmd_category(args)
        elif args.command == "banks":
            return _cmd_banks(args)
        elif args.command == "currency":
            return _cmd_currency(args)
        elif args.command == "alerts":
            return _cmd_alerts(args)
        elif args.command == "templates":
            return _cmd_templates(args)
        elif args.command == "themes":
            return _cmd_themes(args)
        elif args.command == "config":
            return _cmd_config(args)
        elif args.command == "plugin":
            return _cmd_plugin(args)
    except OperationCancelledError:
        print("Operation cancelled.", file=sys.stderr)
        return 1
    except FinanceTrackerError as e:
        print(f"Error [{e.error_code}]: {e.message}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except PermissionError as e:
        print(f"Error: Permission denied - {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


def _validate_amount(amount_str: str) -> Decimal:
    """
    Validate and parse an amount string.

    Args:
        amount_str: Amount string (may include $ and commas)

    Returns:
        Parsed Decimal amount

    Raises:
        InvalidAmountError: If amount is invalid
    """
    cleaned = amount_str.replace("$", "").replace(",", "").strip()

    if not cleaned:
        raise InvalidAmountError(amount_str, "Empty value")

    try:
        amount = Decimal(cleaned)
    except InvalidOperation as e:
        raise InvalidAmountError(amount_str, "Not a valid number") from e

    if amount < 0:
        raise InvalidAmountError(amount_str, "Amount cannot be negative")

    return amount


def _validate_date(date_str: str) -> date:
    """
    Validate and parse a date string.

    Args:
        date_str: Date string in YYYY-MM-DD format

    Returns:
        Parsed date object

    Raises:
        InvalidDateError: If date is invalid
    """
    try:
        return date.fromisoformat(date_str)
    except ValueError as e:
        raise InvalidDateError(date_str) from e


def _cmd_generate(args: argparse.Namespace) -> int:
    """Handle generate command."""
    from spreadsheet_dl.domains.finance.ods_generator import (
        OdsGenerator,
        create_monthly_budget,
    )
    from spreadsheet_dl.templates.professional import (
        get_template,
    )
    from spreadsheet_dl.templates.professional import (
        list_templates as list_professional_templates,
    )

    output = args.output
    skip_confirm = getattr(args, "yes", False) or getattr(args, "force", False)

    # Handle professional templates - they generate complete spreadsheets
    if args.template:
        available = list_professional_templates()
        if args.template not in available:
            print(f"Error: Unknown template '{args.template}'", file=sys.stderr)
            print(f"Available templates: {', '.join(available)}", file=sys.stderr)
            return 1
        template_cls = get_template(args.template)
        if template_cls is None:
            print(f"Error: Template '{args.template}' not found", file=sys.stderr)
            return 1
        theme = getattr(args, "theme", None)
        template = template_cls(theme=theme) if theme else template_cls()
        print(f"Using professional template: {args.template}")

        if output.is_dir():
            today = date.today()
            filename = f"{args.template}_{today.year}_{today.month:02d}.ods"
            output_path = output / filename
        else:
            output_path = output

        if not confirm_overwrite(output_path, skip_confirm=skip_confirm):
            raise OperationCancelledError("File generation")

        builder = template.generate()
        builder.save(output_path)
        print(f"Created: {output_path}")
        return 0

    # Standard budget generation (no template)
    allocations = None

    # Get theme if specified
    theme = getattr(args, "theme", None)
    if theme:
        print(f"Using theme: {theme}")

    if output.is_dir():
        today = date.today()
        month = args.month or today.month
        year = getattr(args, "year", None) or today.year
        filename = f"budget_{year}_{month:02d}.ods"
        output_path = output / filename
    else:
        output_path = output

    # Check for existing file (FR-UX-004)
    if not confirm_overwrite(output_path, skip_confirm=skip_confirm):
        raise OperationCancelledError("File generation")

    if output.is_dir():
        if allocations or theme:
            generator = OdsGenerator(theme=theme)
            today = date.today()
            month = args.month or today.month
            year = getattr(args, "year", None) or today.year
            path = generator.create_budget_spreadsheet(
                output_path,
                month=month,
                year=year,
                budget_allocations=allocations,
            )
        else:
            path = create_monthly_budget(
                output, month=args.month, year=getattr(args, "year", None), theme=theme
            )
    else:
        generator = OdsGenerator(theme=theme)
        path = generator.create_budget_spreadsheet(
            output,
            month=args.month,
            year=getattr(args, "year", None),
            budget_allocations=allocations,
        )

    print(f"Created: {path}")
    return 0


def _cmd_analyze(args: argparse.Namespace) -> int:
    """Handle analyze command."""
    from spreadsheet_dl.domains.finance.budget_analyzer import BudgetAnalyzer

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    analyzer = BudgetAnalyzer(args.file)

    # Apply filters if specified
    if args.category:
        filtered = analyzer.filter_by_category(args.category)
        if filtered.empty:
            print(f"No expenses found for category: {args.category}")
            return 0
        print(f"Category: {args.category}")
        print(f"Total: ${filtered['Amount'].sum():,.2f}")
        print(f"Transactions: {len(filtered)}")
        return 0

    if args.start_date or args.end_date:
        start = _validate_date(args.start_date) if args.start_date else date(1900, 1, 1)
        end = _validate_date(args.end_date) if args.end_date else date(2100, 12, 31)
        filtered = analyzer.filter_by_date_range(start, end)
        if filtered.empty:
            print("No expenses found in date range")
            return 0
        print(f"Date Range: {start} to {end}")
        print(f"Total: ${filtered['Amount'].sum():,.2f}")
        print(f"Transactions: {len(filtered)}")
        return 0

    data = analyzer.to_dict()

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        summary = analyzer.get_summary()
        print(f"Budget Analysis: {args.file}")
        print("-" * 40)
        print(f"Total Budget:  ${summary.total_budget:,.2f}")
        print(f"Total Spent:   ${summary.total_spent:,.2f}")
        print(f"Remaining:     ${summary.total_remaining:,.2f}")
        print(f"Used:          {summary.percent_used:.1f}%")
        print()
        if summary.alerts:
            print("Alerts:")
            for alert in summary.alerts:
                print(f"  - {alert}")

    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    """Handle report command."""
    from spreadsheet_dl.domains.finance.report_generator import ReportGenerator

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    generator = ReportGenerator(args.file)

    if args.output:
        path = generator.save_report(args.output, format=args.format)
        print(f"Report saved: {path}")
    else:
        if args.format == "text":
            print(generator.generate_text_report())
        elif args.format == "markdown":
            print(generator.generate_markdown_report())
        elif args.format == "json":
            print(json.dumps(generator.generate_visualization_data(), indent=2))

    return 0


def _cmd_expense(args: argparse.Namespace) -> int:
    """
    Handle quick expense entry.

    Implements:
        - FR-CORE-003: Expense append functionality (fixes Gap G-02)
    """
    from spreadsheet_dl.domains.finance.csv_import import TransactionCategorizer
    from spreadsheet_dl.domains.finance.ods_generator import (
        ExpenseCategory,
        ExpenseEntry,
        OdsGenerator,
    )
    from spreadsheet_dl.ods_editor import OdsEditor

    # Parse amount with validation
    amount = _validate_amount(args.amount)

    # Parse date with validation
    expense_date = _validate_date(args.date) if args.date else date.today()

    # Determine category
    if args.category:
        try:
            category = ExpenseCategory(args.category)
        except ValueError:
            # Try to find by name (case-insensitive)
            category_lower = args.category.lower().replace(" ", "_")
            for cat in ExpenseCategory:
                if (
                    cat.name.lower() == category_lower
                    or cat.value.lower() == args.category.lower()
                ):
                    category = cat
                    break
            else:
                valid_categories = [cat.value for cat in ExpenseCategory]
                raise InvalidCategoryError(args.category, valid_categories)
    else:
        # Auto-categorize
        categorizer = TransactionCategorizer()
        category = categorizer.categorize(args.description)
        print(f"Auto-categorized as: {category.value}")

    entry = ExpenseEntry(
        date=expense_date,
        category=category,
        description=args.description,
        amount=amount,
    )

    # Find or create ODS file
    if args.file:
        ods_path = args.file
        if not ods_path.exists():
            print(f"Error: File not found: {ods_path}", file=sys.stderr)
            return 1
        file_existed = True
    else:
        # Look for most recent budget file in current directory
        ods_files = list(Path.cwd().glob("budget_*.ods"))
        if ods_files:
            ods_path = max(ods_files, key=lambda p: p.stat().st_mtime)
            print(f"Using: {ods_path}")
            file_existed = True
        else:
            # Create new
            today = date.today()
            ods_path = Path.cwd() / f"budget_{today.year}_{today.month:02d}.ods"
            file_existed = False

    # Handle dry-run mode
    dry_run = getattr(args, "dry_run", False)

    if dry_run:
        print("\n[DRY RUN] Would add expense:")
        print(f"  File:        {ods_path}")
        print(f"  Date:        {entry.date}")
        print(f"  Category:    {entry.category.value}")
        print(f"  Description: {entry.description}")
        print(f"  Amount:      ${entry.amount:.2f}")
        return 0

    # Create file if needed
    if not file_existed:
        generator = OdsGenerator()
        generator.create_budget_spreadsheet(ods_path)
        print(f"Created new budget: {ods_path}")

    # Append expense to file (FR-CORE-003 implementation)
    try:
        editor = OdsEditor(ods_path)
        row_num = editor.append_expense(entry)
        editor.save()

        print("\nExpense added successfully:")
        print(f"  File:        {ods_path}")
        print(f"  Row:         {row_num}")
        print(f"  Date:        {entry.date}")
        print(f"  Category:    {entry.category.value}")
        print(f"  Description: {entry.description}")
        print(f"  Amount:      ${entry.amount:.2f}")

    except Exception as e:
        print(f"Error adding expense: {e}", file=sys.stderr)
        return 1

    return 0


def _cmd_import(args: argparse.Namespace) -> int:
    """Handle CSV import."""
    from spreadsheet_dl.domains.finance.bank_formats import BankFormatRegistry
    from spreadsheet_dl.domains.finance.csv_import import import_bank_csv
    from spreadsheet_dl.domains.finance.ods_generator import OdsGenerator

    skip_confirm = getattr(args, "yes", False) or getattr(args, "force", False)

    if not args.csv_file.exists():
        print(f"Error: CSV file not found: {args.csv_file}", file=sys.stderr)
        return 1

    # Detect or use specified bank format
    if args.bank == "auto":
        registry = BankFormatRegistry()
        detected_fmt = registry.detect_format(args.csv_file)
        bank = detected_fmt.id if detected_fmt else "generic"
        print(f"Detected format: {bank}")
    else:
        bank = args.bank

    # Import transactions
    entries = import_bank_csv(args.csv_file, bank)

    if not entries:
        print("No expenses found in CSV file")
        return 0

    print(f"Found {len(entries)} expenses")

    if args.preview:
        print("\nPreview (first 10):")
        for entry in entries[:10]:
            print(
                f"  {entry.date} | {entry.category.value:15} | "
                f"${entry.amount:>8.2f} | {entry.description[:30]}"
            )
        if len(entries) > 10:
            print(f"  ... and {len(entries) - 10} more")
        return 0

    # Create ODS file
    if args.output:
        output_path = args.output
    else:
        today = date.today()
        output_path = Path.cwd() / f"imported_{today.strftime('%Y%m%d')}.ods"

    # Confirm overwrite (FR-UX-004)
    if not confirm_overwrite(output_path, skip_confirm=skip_confirm):
        raise OperationCancelledError("CSV import")

    theme = getattr(args, "theme", None)
    generator = OdsGenerator(theme=theme)
    generator.create_budget_spreadsheet(output_path, expenses=entries)

    print(f"Created: {output_path}")
    print(f"Total imported: ${sum(e.amount for e in entries):,.2f}")

    return 0


def _cmd_export(args: argparse.Namespace) -> int:
    """
    Handle export command.

    Implements:
        FR-EXPORT-001: Multi-format export (xlsx, csv, pdf)
    """
    from spreadsheet_dl.export import MultiFormatExporter

    skip_confirm = getattr(args, "yes", False) or getattr(args, "force", False)

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    # Determine output path
    output_path = args.output or args.file.with_suffix(f".{args.format}")

    # Confirm overwrite (FR-UX-004)
    if not confirm_overwrite(output_path, skip_confirm=skip_confirm):
        raise OperationCancelledError("Export")

    exporter = MultiFormatExporter()
    result = exporter.export(args.file, output_path, args.format)

    print(f"Exported: {result}")
    return 0


def _cmd_export_dual(args: argparse.Namespace) -> int:
    """
    Handle dual export command.

    Implements:
        FR-DUAL-001/002: Dual export (ODS + AI-friendly JSON)
    """
    from spreadsheet_dl.ai_export import AIExporter

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    output_dir = args.output_dir or args.file.parent

    exporter = AIExporter()
    ods_path, json_path = exporter.export_dual(args.file, output_dir)

    print("Exported:")
    print(f"  ODS:  {ods_path}")
    print(f"  JSON: {json_path}")
    print("\nThe JSON file is formatted for AI/LLM consumption with semantic metadata.")

    return 0


def _cmd_backup(args: argparse.Namespace) -> int:
    """
    Handle backup command.

    Implements:
        DR-STORE-002: Backup/restore functionality
    """
    from spreadsheet_dl.backup import BackupManager, BackupReason

    skip_confirm = getattr(args, "yes", False) or getattr(args, "force", False)
    dry_run = getattr(args, "dry_run", False)

    manager = BackupManager(retention_days=args.days)

    # List backups
    if args.list:
        backups = manager.list_backups(args.file)
        if not backups:
            print(f"No backups found for: {args.file}")
            return 0

        print(f"Backups for: {args.file}")
        print("-" * 60)
        for backup in backups:
            size_kb = (
                backup.backup_path.stat().st_size / 1024
                if backup.backup_path.exists()
                else 0
            )
            print(
                f"  {backup.created.strftime('%Y-%m-%d %H:%M')}  "
                f"{size_kb:>8.1f} KB  {backup.metadata.reason}"
            )
            print(f"    Path: {backup.backup_path}")
        return 0

    # Cleanup old backups
    if args.cleanup:
        if not confirm_destructive_operation(
            "backup cleanup",
            f"This will remove backups older than {args.days} days.",
            skip_confirm=skip_confirm,
        ):
            raise OperationCancelledError("Backup cleanup")

        deleted = manager.cleanup_old_backups(args.days, dry_run=dry_run)

        if dry_run:
            print(f"[DRY RUN] Would delete {len(deleted)} backup(s)")
        else:
            print(f"Deleted {len(deleted)} old backup(s)")
        return 0

    # Restore from backup
    if args.restore:
        if not args.restore.exists():
            print(f"Error: Backup file not found: {args.restore}", file=sys.stderr)
            return 1

        target = args.file
        if target.exists() and not confirm_overwrite(target, skip_confirm=skip_confirm):
            raise OperationCancelledError("Backup restore")

        if dry_run:
            print(f"[DRY RUN] Would restore {args.restore} to {target}")
            return 0

        restored = manager.restore_backup(args.restore, target, overwrite=True)
        print(f"Restored: {restored}")
        return 0

    # Create backup (default action)
    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    backup_info = manager.create_backup(args.file, BackupReason.MANUAL)
    print(f"Backup created: {backup_info.backup_path}")
    print(f"  Original: {args.file}")
    print(f"  Hash: {backup_info.metadata.content_hash[:16]}...")

    return 0


def _cmd_upload(args: argparse.Namespace) -> int:
    """Handle Nextcloud upload."""
    from spreadsheet_dl.webdav_upload import NextcloudConfig, upload_budget

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    try:
        config = NextcloudConfig.from_env()
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        print("\nSet these environment variables:")
        print("  NEXTCLOUD_URL=https://your-nextcloud.com")
        print("  NEXTCLOUD_USER=username")
        print("  NEXTCLOUD_PASSWORD=app-password")
        print("\nOr create a configuration file:")
        print("  spreadsheet-dl config --init")
        return 1

    print(f"Uploading to {config.server_url}...")
    url = upload_budget(args.file, config)
    print(f"Uploaded: {url}")

    return 0


def _cmd_dashboard(args: argparse.Namespace) -> int:
    """Handle dashboard command."""
    from spreadsheet_dl.domains.finance.analytics import generate_dashboard

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    data = generate_dashboard(args.file)

    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    # Pretty print dashboard
    print("=" * 60)
    print("BUDGET DASHBOARD")
    print("=" * 60)
    print()

    # Status
    status_icons = {
        "healthy": "[OK]",
        "caution": "[!]",
        "warning": "[!!]",
        "critical": "[!!!]",
    }
    print(
        f"Status: {status_icons.get(data['budget_status'], '[?]')} {data['status_message']}"
    )
    print()

    # Summary
    print("SUMMARY")
    print("-" * 40)
    print(f"  Total Budget:     ${data['total_budget']:>12,.2f}")
    print(f"  Total Spent:      ${data['total_spent']:>12,.2f}")
    print(f"  Remaining:        ${data['total_remaining']:>12,.2f}")
    print(f"  Budget Used:      {data['percent_used']:>12.1f}%")
    print(f"  Days Remaining:   {data['days_remaining']:>12}")
    print(f"  Daily Budget:     ${data['daily_budget_remaining']:>12,.2f}")
    print()

    # Top spending
    print("TOP SPENDING")
    print("-" * 40)
    for i, (cat, amount) in enumerate(data["top_spending"][:5], 1):
        print(f"  {i}. {cat:<20} ${amount:>10,.2f}")
    print()

    # Alerts
    if data["alerts"]:
        print("ALERTS")
        print("-" * 40)
        for alert in data["alerts"]:
            print(f"  ! {alert}")
        print()

    # Recommendations
    if data["recommendations"]:
        print("RECOMMENDATIONS")
        print("-" * 40)
        for rec in data["recommendations"]:
            print(f"  - {rec}")
        print()

    print("=" * 60)

    return 0


def _cmd_visualize(args: argparse.Namespace) -> int:
    """
    Handle visualize command.

    Implements:
        FR-REPORT-003: Interactive visualization
    """
    from spreadsheet_dl.visualization import (
        ChartConfig,
        ChartDataPoint,
        ChartGenerator,
        ChartType,
        create_budget_dashboard,
    )

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = args.file.with_suffix(".html")
        output_path = output_path.with_stem(f"{output_path.stem}_dashboard")

    # Generate visualization
    if args.type == "dashboard":
        html = create_budget_dashboard(
            output_path=output_path,
            theme=args.theme,
        )
        print(f"Dashboard created: {output_path}")
    else:
        # For specific chart types, we'd need budget data
        from spreadsheet_dl.domains.finance.budget_analyzer import BudgetAnalyzer

        analyzer = BudgetAnalyzer(args.file)
        by_category = analyzer.get_category_breakdown()

        generator = ChartGenerator(theme=args.theme)
        data = [
            ChartDataPoint(label=cat, value=float(amt), category=cat)
            for cat, amt in by_category.items()
            if amt > 0
        ]

        if args.type == "pie":
            config = ChartConfig(
                title="Spending by Category", chart_type=ChartType.PIE, cutout=60
            )
            html = generator.create_pie_chart(data, config)
        elif args.type == "bar":
            config = ChartConfig(title="Spending by Category", chart_type=ChartType.BAR)
            html = generator.create_bar_chart(data, config)
        else:
            config = ChartConfig(title="Spending Trend", chart_type=ChartType.LINE)
            # Would need time series data for trend
            html = generator.create_bar_chart(data, config)

        with open(output_path, "w") as f:
            f.write(html)
        print(f"Chart created: {output_path}")

    print("\nOpen the HTML file in a browser to view interactive charts.")
    return 0


def _cmd_account(args: argparse.Namespace) -> int:
    """
    Handle account command.

    Implements:
        FR-CORE-004: Account Management
    """
    from decimal import Decimal

    from spreadsheet_dl.domains.finance.accounts import AccountManager, AccountType

    # Get data file path
    config_dir = Path.home() / ".config" / "spreadsheet-dl"
    config_dir.mkdir(parents=True, exist_ok=True)
    data_file = config_dir / "accounts.json"

    manager = AccountManager(data_file=data_file)

    if args.account_action == "add":
        # Map string to AccountType
        type_map = {
            "checking": AccountType.CHECKING,
            "savings": AccountType.SAVINGS,
            "credit": AccountType.CREDIT,
            "investment": AccountType.INVESTMENT,
            "cash": AccountType.CASH,
            "retirement": AccountType.RETIREMENT,
        }
        account_type = type_map.get(args.type, AccountType.CHECKING)

        account = manager.add_account(
            name=args.name,
            account_type=account_type,
            institution=args.institution or "",
            balance=Decimal(str(args.balance)),
            currency=args.currency,
        )
        print(f"Account created: {account.name}")
        print(f"  ID: {account.id}")
        print(f"  Type: {account.account_type.value}")
        print(f"  Balance: ${account.balance:,.2f}")
        return 0

    elif args.account_action == "list":
        accounts = manager.list_accounts()

        if not accounts:
            print("No accounts found. Add one with: spreadsheet-dl account add <name>")
            return 0

        if getattr(args, "json", False):
            print(json.dumps([a.to_dict() for a in accounts], indent=2))
            return 0

        print("Accounts")
        print("=" * 60)
        for acc in accounts:
            status = "(active)" if acc.is_active else "(inactive)"
            print(f"  {acc.name} {status}")
            print(f"    Type: {acc.account_type.value}")
            print(f"    Balance: ${acc.balance:,.2f} {acc.currency}")
            if acc.institution:
                print(f"    Institution: {acc.institution}")
            print()
        return 0

    elif args.account_action == "balance":
        if args.name:
            found_account = manager.get_account_by_name(args.name)
            if found_account is None:
                print(f"Account not found: {args.name}", file=sys.stderr)
                return 1
            print(f"{found_account.name}: ${found_account.balance:,.2f}")
        else:
            accounts = manager.list_accounts()
            total = sum(a.balance for a in accounts)
            for acc in accounts:
                print(f"  {acc.name}: ${acc.balance:,.2f}")
            print("-" * 40)
            print(f"  Total: ${total:,.2f}")
        return 0

    elif args.account_action == "transfer":
        from_acc = manager.get_account_by_name(args.from_account)
        to_acc = manager.get_account_by_name(args.to_account)

        if not from_acc:
            print(f"Source account not found: {args.from_account}", file=sys.stderr)
            return 1
        if not to_acc:
            print(f"Destination account not found: {args.to_account}", file=sys.stderr)
            return 1

        transfer = manager.transfer(
            from_acc.id,
            to_acc.id,
            Decimal(str(args.amount)),
        )

        if transfer:
            print("Transfer complete:")
            print(f"  From: {from_acc.name} -> ${from_acc.balance:,.2f}")
            print(f"  To: {to_acc.name} -> ${to_acc.balance:,.2f}")
        else:
            print("Transfer failed", file=sys.stderr)
            return 1
        return 0

    elif args.account_action == "net-worth":
        net_worth = manager.calculate_net_worth()

        if getattr(args, "json", False):
            print(json.dumps(net_worth.to_dict(), indent=2))
            return 0

        print("Net Worth Summary")
        print("=" * 40)
        print(f"  Total Assets:      ${net_worth.total_assets:>12,.2f}")
        print(f"  Total Liabilities: ${net_worth.total_liabilities:>12,.2f}")
        print("-" * 40)
        print(f"  Net Worth:         ${net_worth.net_worth:>12,.2f}")

        if net_worth.assets_by_type:
            print("\nAssets by Type:")
            for atype, amount in net_worth.assets_by_type.items():
                print(f"  {atype.value}: ${amount:,.2f}")

        if net_worth.liabilities_by_type:
            print("\nLiabilities by Type:")
            for ltype, amount in net_worth.liabilities_by_type.items():
                print(f"  {ltype.value}: ${amount:,.2f}")

        return 0

    else:
        print("Usage: spreadsheet-dl account <add|list|balance|transfer|net-worth>")
        print("\nManage financial accounts, balances, and transfers.")
        print("\nExamples:")
        print(
            "  spreadsheet-dl account add 'Primary Checking' --type checking --balance 1000"
        )
        print("  spreadsheet-dl account list")
        print("  spreadsheet-dl account balance")
        print("  spreadsheet-dl account transfer 'Checking' 'Savings' 500")
        print("  spreadsheet-dl account net-worth")
        return 0


def _cmd_category(args: argparse.Namespace) -> int:
    """
    Handle category command.

    Implements:
        FR-EXT-005: Custom Category Support
    """
    from spreadsheet_dl.domains.finance.categories import Category, CategoryManager

    manager = CategoryManager()

    if args.category_action == "add":
        try:
            cat = Category(
                name=args.name,
                color=args.color,
                icon=args.icon or "",
                description=args.description or "",
                parent=args.parent,
                budget_default=args.budget,
            )
            manager.add_category(cat)
            manager.save()

            print(f"Category created: {cat.name}")
            print(f"  Color: {cat.color}")
            if cat.parent:
                print(f"  Parent: {cat.parent}")
            if cat.budget_default:
                print(f"  Default budget: ${cat.budget_default:,.2f}")
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.category_action == "list":
        categories = manager.list_categories(
            include_hidden=getattr(args, "include_hidden", False),
            custom_only=getattr(args, "custom_only", False),
        )

        if getattr(args, "json", False):
            print(json.dumps([c.to_dict() for c in categories], indent=2))
            return 0

        print("Expense Categories")
        print("=" * 60)

        custom = [c for c in categories if c.is_custom]
        standard = [c for c in categories if not c.is_custom]

        if standard:
            print("\nStandard Categories:")
            print("-" * 40)
            for cat in standard:
                hidden = " (hidden)" if cat.is_hidden else ""
                print(f"  {cat.name}{hidden}")
                print(f"    Color: {cat.color}")

        if custom:
            print("\nCustom Categories:")
            print("-" * 40)
            for cat in custom:
                hidden = " (hidden)" if cat.is_hidden else ""
                print(f"  {cat.name}{hidden}")
                print(f"    Color: {cat.color}")
                if cat.description:
                    print(f"    Description: {cat.description}")
                if cat.parent:
                    print(f"    Parent: {cat.parent}")

        print()
        print(f"Total: {len(categories)} categories")
        return 0

    elif args.category_action == "update":
        try:
            is_hidden = None
            if getattr(args, "hide", False):
                is_hidden = True
            elif getattr(args, "unhide", False):
                is_hidden = False

            cat = manager.update_category(
                args.name,
                color=args.color,
                icon=args.icon,
                description=args.description,
                new_name=args.rename,
                is_hidden=is_hidden,
                budget_default=args.budget,
            )
            manager.save()

            print(f"Category updated: {cat.name}")
            return 0
        except (KeyError, ValueError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.category_action == "delete":
        try:
            skip_confirm = getattr(args, "force", False)
            if not skip_confirm and not confirm_action(
                f"Delete category '{args.name}'?", default=False
            ):
                raise OperationCancelledError("Category deletion")

            result = manager.delete_category(
                args.name, force=getattr(args, "force", False)
            )
            if result:
                manager.save()
                print(f"Category deleted: {args.name}")
            else:
                print(f"Category not found: {args.name}")
                return 1
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.category_action == "search":
        results = manager.search_categories(args.query)

        if getattr(args, "json", False):
            print(json.dumps([c.to_dict() for c in results], indent=2))
            return 0

        if not results:
            print(f"No categories found matching: {args.query}")
            return 0

        print(f"Categories matching '{args.query}':")
        for cat in results:
            custom_label = " (custom)" if cat.is_custom else ""
            print(f"  {cat.name}{custom_label}")
        return 0

    elif args.category_action == "suggest":
        suggested_cat: Category | None = manager.suggest_category(args.description)
        if suggested_cat is not None:
            print(f"Suggested category: {suggested_cat.name}")
            print(f"  Color: {suggested_cat.color}")
        else:
            print("No suggestion available")
        return 0

    else:
        print("Usage: spreadsheet-dl category <add|list|update|delete|search|suggest>")
        print("\nManage expense categories.")
        print("\nExamples:")
        print("  spreadsheet-dl category add 'Pet Care' --color '#795548'")
        print("  spreadsheet-dl category list")
        print("  spreadsheet-dl category list --custom-only")
        print("  spreadsheet-dl category update 'Pet Care' --color '#8B4513'")
        print("  spreadsheet-dl category delete 'Pet Care'")
        print("  spreadsheet-dl category search pet")
        print("  spreadsheet-dl category suggest 'vet bill for dog'")
        return 0


def _cmd_banks(args: argparse.Namespace) -> int:
    """
    Handle banks command.

    Implements:
        FR-IMPORT-002: Extended bank formats
    """
    from spreadsheet_dl.domains.finance.bank_formats import (
        BankFormatRegistry,
        count_formats,
    )

    registry = BankFormatRegistry()

    # Detect format from file
    if args.detect:
        if not args.detect.exists():
            print(f"Error: File not found: {args.detect}", file=sys.stderr)
            return 1

        detected = registry.detect_format(args.detect)
        if detected:
            print(f"Detected format: {detected.name}")
            print(f"  ID: {detected.id}")
            print(f"  Institution: {detected.institution}")
            print(f"  Type: {detected.format_type}")
        else:
            print("Could not auto-detect format. Try specifying with --bank option.")
        return 0

    # List or search formats
    formats = registry.list_formats(
        institution=args.search,
        format_type=args.type,
    )

    if args.json:
        print(json.dumps([f.to_dict() for f in formats], indent=2))
        return 0

    print(f"Supported Bank Formats ({count_formats()} total)")
    print("=" * 60)

    if args.search:
        print(f"Filtered by: {args.search}")
    if args.type:
        print(f"Type: {args.type}")
    print()

    # Group by institution
    by_institution: dict[str, list[Any]] = {}
    for fmt in formats:
        inst = fmt.institution or "Other"
        by_institution.setdefault(inst, []).append(fmt)

    for institution in sorted(by_institution.keys()):
        print(f"{institution}")
        for fmt in by_institution[institution]:
            print(f"  - {fmt.id}: {fmt.name} ({fmt.format_type})")
        print()

    print("Use with: spreadsheet-dl import data.csv --bank <format_id>")
    return 0


def _cmd_currency(args: argparse.Namespace) -> int:
    """
    Handle currency command.

    Implements:
        FR-CURR-001: Multi-currency support
    """
    from spreadsheet_dl.domains.finance.currency import (
        CurrencyConverter,
        get_currency,
        list_currencies,
    )

    # List currencies
    if args.list:
        currencies = list_currencies()

        if args.json:
            print(
                json.dumps(
                    [
                        {"code": c.code, "name": c.name, "symbol": c.symbol}
                        for c in currencies
                    ],
                    indent=2,
                )
            )
            return 0

        print("Supported Currencies")
        print("=" * 60)
        for curr in currencies:
            print(f"  {curr.code}  {curr.symbol:>4}  {curr.name}")
        return 0

    # Convert currency
    if args.amount and args.to_currency:
        from decimal import Decimal

        converter = CurrencyConverter()
        result = converter.convert(
            Decimal(str(args.amount)),
            args.from_currency,
            args.to_currency,
        )

        from_curr = get_currency(args.from_currency)
        to_curr = get_currency(args.to_currency)

        if args.json:
            print(
                json.dumps(
                    {
                        "from": {"amount": args.amount, "currency": args.from_currency},
                        "to": {"amount": float(result), "currency": args.to_currency},
                    },
                    indent=2,
                )
            )
        else:
            from_formatted = from_curr.format(Decimal(str(args.amount)))
            to_formatted = to_curr.format(result)
            print(f"{from_formatted} = {to_formatted}")

        return 0

    # Show help
    print("Currency Conversion")
    print("=" * 40)
    print("\nUsage:")
    print("  spreadsheet-dl currency --list")
    print("  spreadsheet-dl currency 100 --from USD --to EUR")
    print()
    print("Examples:")
    print("  spreadsheet-dl currency 1000 --to EUR")
    print("  spreadsheet-dl currency 50 --from GBP --to USD")

    return 0


def _cmd_alerts(args: argparse.Namespace) -> int:
    """Handle alerts command."""
    from spreadsheet_dl.domains.finance.alerts import AlertMonitor, AlertSeverity
    from spreadsheet_dl.domains.finance.budget_analyzer import BudgetAnalyzer

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    analyzer = BudgetAnalyzer(args.file)
    monitor = AlertMonitor(analyzer)
    alerts = monitor.check_all()

    if args.critical_only:
        alerts = [a for a in alerts if a.severity == AlertSeverity.CRITICAL]

    if args.json:
        print(monitor.to_json())
        return 0

    if not alerts:
        print("No alerts at this time.")
        return 0

    print(monitor.format_text())

    return 0


def _cmd_templates(args: argparse.Namespace) -> int:
    """Handle templates command."""
    from spreadsheet_dl.templates import list_financial_templates, list_templates

    # Build template info for display
    template_info = []

    # Professional templates
    professional_descriptions = {
        "enterprise_budget": "Multi-department enterprise budget planning",
        "cash_flow": "Track incoming and outgoing cash flows",
        "invoice": "Professional invoice generation",
        "expense_report": "Employee expense tracking and reimbursement",
    }
    for name in list_templates():
        template_info.append(
            {
                "name": name,
                "category": "Professional",
                "description": professional_descriptions.get(
                    name, "Professional template"
                ),
            }
        )

    # Financial statement templates
    financial_descriptions = {
        "income_statement": "Statement of revenues and expenses",
        "balance_sheet": "Assets, liabilities, and equity snapshot",
        "cash_flow_statement": "Statement of cash flows",
        "equity_statement": "Statement of changes in equity",
    }
    for name in list_financial_templates():
        template_info.append(
            {
                "name": name,
                "category": "Financial Statement",
                "description": financial_descriptions.get(
                    name, "Financial statement template"
                ),
            }
        )

    if args.json:
        print(json.dumps(template_info, indent=2))
        return 0

    print("Available Templates")
    print("=" * 60)
    print()

    current_category = None
    for t in template_info:
        if t["category"] != current_category:
            current_category = t["category"]
            print(f"{current_category} Templates:")
            print("-" * 40)

        print(f"  {t['name']}")
        print(f"    {t['description']}")
        print()

    print("Use: spreadsheet-dl generate -t <template_name>")

    return 0


def _cmd_themes(args: argparse.Namespace) -> int:
    """Handle themes command."""
    # Built-in themes with descriptions
    themes_info = [
        {
            "name": "default",
            "display_name": "Default Finance Theme",
            "description": "Clean professional theme for budget spreadsheets",
            "colors": "Blue headers, green/red status indicators",
        },
        {
            "name": "corporate",
            "display_name": "Corporate Theme",
            "description": "Professional corporate styling for business use",
            "colors": "Navy blue headers, brown accents",
        },
        {
            "name": "minimal",
            "display_name": "Minimal Theme",
            "description": "Clean minimal design for focused work",
            "colors": "Gray headers, subtle borders, muted colors",
        },
        {
            "name": "dark",
            "display_name": "Dark Theme",
            "description": "Dark mode theme for reduced eye strain",
            "colors": "Dark backgrounds, light text, blue accents",
        },
        {
            "name": "high_contrast",
            "display_name": "High Contrast Theme",
            "description": "High contrast theme for accessibility",
            "colors": "Bold colors, large fonts, strong borders",
        },
    ]

    if args.json:
        print(json.dumps(themes_info, indent=2))
        return 0

    print("Available Visual Themes")
    print("=" * 60)
    print()

    for t in themes_info:
        print(f"  {t['name']}")
        print(f"    {t['display_name']}")
        print(f"    {t['description']}")
        print(f"    Style: {t['colors']}")
        print()

    print("Use: spreadsheet-dl generate --theme <theme_name>")
    print()
    print("Note: Themes require PyYAML. Install with:")
    print("  pip install 'spreadsheet-dl[config]'")

    return 0


def _cmd_config(args: argparse.Namespace) -> int:
    """Handle config command."""
    from spreadsheet_dl.config import get_config, init_config_file

    if args.init:
        path = init_config_file(args.path)
        print(f"Configuration file created: {path}")
        print("\nEdit this file to customize settings.")
        print("Note: For security, set NEXTCLOUD_PASSWORD as an environment variable.")
        return 0

    if args.show:
        config = get_config()
        print(json.dumps(config.to_dict(), indent=2))
        return 0

    # Default: show help
    print("Configuration Management")
    print("=" * 60)
    print()
    print("Commands:")
    print("  spreadsheet-dl config --init     Create a new config file")
    print("  spreadsheet-dl config --show     Show current configuration")
    print()
    print("Configuration sources (in priority order):")
    print("  1. Command-line arguments")
    print("  2. Environment variables")
    print("  3. Configuration file")
    print()
    print("Config file locations (first found is used):")
    print("  - ~/.config/spreadsheet-dl/config.yaml")
    print("  - ~/.spreadsheet-dl.yaml")
    print("  - ./.spreadsheet-dl.yaml")
    print()
    print("Environment variables:")
    print("  NEXTCLOUD_URL       - Nextcloud server URL")
    print("  NEXTCLOUD_USER      - Nextcloud username")
    print("  NEXTCLOUD_PASSWORD  - Nextcloud password/app token")
    print("  NO_COLOR            - Disable colored output")

    return 0


def _cmd_plugin(args: argparse.Namespace) -> int:
    """
    Handle plugin command.

    Implements:
        FR-EXT-001: Plugin management CLI
    """
    from spreadsheet_dl.plugins import get_plugin_manager

    manager = get_plugin_manager()

    if args.plugin_action == "list":
        plugins = manager.list_plugins(
            enabled_only=getattr(args, "enabled_only", False)
        )

        if getattr(args, "json", False):
            print(json.dumps(plugins, indent=2))
            return 0

        if not plugins:
            print("No plugins found.")
            print("\nTo add plugins:")
            print("  1. Create a plugin implementing PluginInterface")
            print("  2. Place it in ~/.spreadsheet-dl/plugins/ or ./plugins/")
            print("  3. Run: spreadsheet-dl plugin list")
            return 0

        print("SpreadsheetDL Plugins")
        print("=" * 60)
        print()

        enabled_plugins = [p for p in plugins if p["enabled"]]
        disabled_plugins = [p for p in plugins if not p["enabled"]]

        if enabled_plugins:
            print("Enabled Plugins:")
            print("-" * 40)
            for p in enabled_plugins:
                print(f"  ✓ {p['name']} v{p['version']}")
                if p["description"]:
                    print(f"    {p['description']}")
                if p["author"]:
                    print(f"    Author: {p['author']}")
                print()

        if disabled_plugins:
            print("Disabled Plugins:")
            print("-" * 40)
            for p in disabled_plugins:
                print(f"    {p['name']} v{p['version']}")
                if p["description"]:
                    print(f"    {p['description']}")
                if p["author"]:
                    print(f"    Author: {p['author']}")
                print()

        print(f"Total: {len(plugins)} plugin(s)")
        return 0

    elif args.plugin_action == "enable":
        try:
            # Parse config if provided
            config = None
            if hasattr(args, "config") and args.config:
                config = json.loads(args.config)

            manager.enable(args.name, config)
            print(f"Enabled plugin: {args.name}")
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON config: {e}", file=sys.stderr)
            return 1

    elif args.plugin_action == "disable":
        manager.disable(args.name)
        print(f"Disabled plugin: {args.name}")
        return 0

    elif args.plugin_action == "info":
        plugin = manager.get_plugin(args.name)
        if plugin:
            enabled_plugin_names: list[str] = [
                p["name"] for p in manager.list_plugins(enabled_only=True)
            ]
            is_enabled = plugin.name in enabled_plugin_names

            print(f"Plugin: {plugin.name}")
            print("=" * 40)
            print(f"  Version:     {plugin.version}")
            print(f"  Author:      {plugin.author or 'N/A'}")
            print(f"  Description: {plugin.description or 'N/A'}")
            print(f"  Status:      {'Enabled' if is_enabled else 'Disabled'}")
        else:
            print(f"Plugin not found: {args.name}", file=sys.stderr)
            return 1
        return 0

    else:
        print("Usage: spreadsheet-dl plugin <list|enable|disable|info>")
        print("\nManage plugins for extending SpreadsheetDL.")
        print("\nExamples:")
        print("  spreadsheet-dl plugin list")
        print("  spreadsheet-dl plugin list --enabled-only")
        print("  spreadsheet-dl plugin enable my_plugin")
        print('  spreadsheet-dl plugin enable my_plugin --config \'{"key":"value"}\'')
        print("  spreadsheet-dl plugin disable my_plugin")
        print("  spreadsheet-dl plugin info my_plugin")
        return 0


if __name__ == "__main__":
    sys.exit(main())
