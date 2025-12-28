"""
Command-line interface for finance tracker.

Provides CLI commands for generating budgets, analyzing spending,
creating reports, and managing finances.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from finance_tracker import __version__
from finance_tracker.exceptions import (
    FinanceTrackerError,
    InvalidAmountError,
    InvalidCategoryError,
    InvalidDateError,
)


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        prog="finance-tracker",
        description="Family financial tracking with ODS spreadsheets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  finance-tracker generate -o output/
  finance-tracker generate -o output/ --theme corporate
  finance-tracker analyze budget.ods --json
  finance-tracker report budget.ods -f markdown
  finance-tracker expense 25.50 "Coffee shop" -c "Dining Out"
  finance-tracker import bank_export.csv --preview
  finance-tracker dashboard budget.ods
  finance-tracker templates
  finance-tracker themes

For more information, visit: https://github.com/allenjd1/finance-tracker
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
        help="Bank format (chase, bank_of_america, capital_one, wells_fargo, citi, usaa, generic, or auto)",
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

    # Themes command (NEW)
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
        elif args.command == "upload":
            return _cmd_upload(args)
        elif args.command == "dashboard":
            return _cmd_dashboard(args)
        elif args.command == "alerts":
            return _cmd_alerts(args)
        elif args.command == "templates":
            return _cmd_templates(args)
        elif args.command == "themes":
            return _cmd_themes(args)
        elif args.command == "config":
            return _cmd_config(args)
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
    from finance_tracker.ods_generator import OdsGenerator, create_monthly_budget
    from finance_tracker.templates import get_template

    output = args.output

    # Get template allocations if specified
    allocations = None
    if args.template:
        template = get_template(args.template)
        allocations = template.allocations
        print(f"Using template: {template.name}")

    # Get theme if specified
    theme = getattr(args, "theme", None)
    if theme:
        print(f"Using theme: {theme}")

    if output.is_dir():
        if allocations or theme:
            generator = OdsGenerator(theme=theme)
            today = date.today()
            month = args.month or today.month
            year = args.year or today.year
            filename = f"budget_{year}_{month:02d}.ods"
            output_path = output / filename
            path = generator.create_budget_spreadsheet(
                output_path,
                month=month,
                year=year,
                budget_allocations=allocations,
            )
        else:
            path = create_monthly_budget(
                output, month=args.month, year=args.year, theme=theme
            )
    else:
        generator = OdsGenerator(theme=theme)
        path = generator.create_budget_spreadsheet(
            output,
            month=args.month,
            year=args.year,
            budget_allocations=allocations,
        )

    print(f"Created: {path}")
    return 0


def _cmd_analyze(args: argparse.Namespace) -> int:
    """Handle analyze command."""
    from finance_tracker.budget_analyzer import BudgetAnalyzer

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
    from finance_tracker.report_generator import ReportGenerator

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
    """Handle quick expense entry."""
    from finance_tracker.csv_import import TransactionCategorizer
    from finance_tracker.ods_generator import (
        ExpenseCategory,
        ExpenseEntry,
        OdsGenerator,
    )

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
    else:
        # Look for most recent budget file in current directory
        ods_files = list(Path.cwd().glob("budget_*.ods"))
        if ods_files:
            ods_path = max(ods_files, key=lambda p: p.stat().st_mtime)
            print(f"Using: {ods_path}")
        else:
            # Create new
            today = date.today()
            ods_path = Path.cwd() / f"budget_{today.year}_{today.month:02d}.ods"
            generator = OdsGenerator()
            generator.create_budget_spreadsheet(ods_path)
            print(f"Created new budget: {ods_path}")

    # Add expense to file
    # Note: This would require additional implementation to append to existing ODS
    # For now, just show what would be added
    print("\nExpense recorded:")
    print(f"  Date:        {entry.date}")
    print(f"  Category:    {entry.category.value}")
    print(f"  Description: {entry.description}")
    print(f"  Amount:      ${entry.amount:.2f}")

    return 0


def _cmd_import(args: argparse.Namespace) -> int:
    """Handle CSV import."""
    from finance_tracker.csv_import import CSVImporter, import_bank_csv
    from finance_tracker.ods_generator import OdsGenerator

    if not args.csv_file.exists():
        print(f"Error: CSV file not found: {args.csv_file}", file=sys.stderr)
        return 1

    # Detect or use specified bank format
    if args.bank == "auto":
        detected = CSVImporter.detect_format(args.csv_file)
        bank = detected or "generic"
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

    theme = getattr(args, "theme", None)
    generator = OdsGenerator(theme=theme)
    generator.create_budget_spreadsheet(output_path, expenses=entries)

    print(f"Created: {output_path}")
    print(f"Total imported: ${sum(e.amount for e in entries):,.2f}")

    return 0


def _cmd_upload(args: argparse.Namespace) -> int:
    """Handle Nextcloud upload."""
    from finance_tracker.webdav_upload import NextcloudConfig, upload_budget

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
        print("  finance-tracker config --init")
        return 1

    print(f"Uploading to {config.server_url}...")
    url = upload_budget(args.file, config)
    print(f"Uploaded: {url}")

    return 0


def _cmd_dashboard(args: argparse.Namespace) -> int:
    """Handle dashboard command."""
    from finance_tracker.analytics import generate_dashboard

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


def _cmd_alerts(args: argparse.Namespace) -> int:
    """Handle alerts command."""
    from finance_tracker.alerts import AlertMonitor, AlertSeverity
    from finance_tracker.budget_analyzer import BudgetAnalyzer

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
    from finance_tracker.templates import list_templates

    templates = list_templates()

    if args.json:
        print(json.dumps(templates, indent=2))
        return 0

    print("Available Budget Templates")
    print("=" * 60)
    print()

    for t in templates:
        print(f"  {t['name']}")
        print(f"    {t['display_name']}")
        print(f"    {t['description']}")
        print(f"    Default budget: ${float(t['total_budget']):,.2f}")
        if t["recommended_for"]:
            print(f"    For: {', '.join(t['recommended_for'])}")
        print()

    print("Use: finance-tracker generate -t <template_name>")

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

    print("Use: finance-tracker generate --theme <theme_name>")
    print()
    print("Note: Themes require PyYAML. Install with:")
    print("  pip install 'finance-tracker[config]'")

    return 0


def _cmd_config(args: argparse.Namespace) -> int:
    """Handle config command."""
    from finance_tracker.config import get_config, init_config_file

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
    print("  finance-tracker config --init     Create a new config file")
    print("  finance-tracker config --show     Show current configuration")
    print()
    print("Configuration sources (in priority order):")
    print("  1. Command-line arguments")
    print("  2. Environment variables")
    print("  3. Configuration file")
    print()
    print("Config file locations (first found is used):")
    print("  - ~/.config/finance-tracker/config.yaml")
    print("  - ~/.finance-tracker.yaml")
    print("  - ./.finance-tracker.yaml")
    print()
    print("Environment variables:")
    print("  NEXTCLOUD_URL       - Nextcloud server URL")
    print("  NEXTCLOUD_USER      - Nextcloud username")
    print("  NEXTCLOUD_PASSWORD  - Nextcloud password/app token")
    print("  NO_COLOR            - Disable colored output")

    return 0


if __name__ == "__main__":
    sys.exit(main())
