# Module: cli

## Overview

Command-line interface for SpreadsheetDL finance tracker. Provides comprehensive CLI commands for generating budgets, analyzing spending, creating reports, managing finances, and extending functionality through plugins.

**New in v4.0.0:**

- FR-EXT-001: Plugin system framework (plugin command)
- FR-EXT-005: Custom category management (category command)

**New in v0.6.0 (Phase 3):**

- FR-CORE-004: Account management (account command)
- FR-CURR-001: Multi-currency support (currency command)
- FR-IMPORT-002: Extended bank formats (50+ supported)
- FR-REPORT-003: Interactive visualization (visualize command)
- FR-AI-001/003: Enhanced AI export with semantic tagging

**New in v0.5.0:**

- FR-UX-004: Confirmation prompts for destructive operations
- DR-STORE-002: Backup/restore functionality
- FR-EXPORT-001: Multi-format export (xlsx, csv, pdf)
- FR-DUAL-001/002: Dual export (ODS + JSON for AI)

## Key Functions

### main() -> int

Main entry point for the CLI application.

**Returns:**

- `int`: Exit code (0 for success, non-zero for error)

**Example:**

```python
import sys
from spreadsheet_dl.cli import main

sys.exit(main())
```

### Confirmation Utilities (FR-UX-004)

#### confirm_action(message, default=False, skip_confirm=False) -> bool

Prompt user for confirmation before destructive actions.

**Parameters:**

- `message` (str): Description of the action to confirm
- `default` (bool): Default response if user just presses Enter
- `skip_confirm` (bool): If True, skip confirmation and return True

**Returns:**

- `bool`: True if action is confirmed, False otherwise

**Example:**

```python
from spreadsheet_dl.cli import confirm_action

if confirm_action("Delete all backups?", default=False):
    # Proceed with deletion
    pass
```

#### confirm_overwrite(file_path, skip_confirm=False) -> bool

Confirm overwriting an existing file.

**Parameters:**

- `file_path` (Path): Path to the file that would be overwritten
- `skip_confirm` (bool): If True, skip confirmation

**Returns:**

- `bool`: True if overwrite is confirmed

**Example:**

```python
from pathlib import Path
from spreadsheet_dl.cli import confirm_overwrite

output = Path("budget.ods")
if not confirm_overwrite(output):
    print("Operation cancelled")
```

#### confirm_delete(file_path, skip_confirm=False) -> bool

Confirm deleting a file.

**Parameters:**

- `file_path` (Path): Path to the file to delete
- `skip_confirm` (bool): If True, skip confirmation

**Returns:**

- `bool`: True if deletion is confirmed

#### confirm_destructive_operation(operation, details=None, skip_confirm=False) -> bool

Confirm a potentially destructive operation.

**Parameters:**

- `operation` (str): Name of the operation
- `details` (str | None): Additional details about what will happen
- `skip_confirm` (bool): If True, skip confirmation

**Returns:**

- `bool`: True if operation is confirmed

### Validation Utilities

#### \_validate_amount(amount_str: str) -> Decimal

Validate and parse an amount string.

**Parameters:**

- `amount_str` (str): Amount string (may include $ and commas)

**Returns:**

- `Decimal`: Parsed Decimal amount

**Raises:**

- `InvalidAmountError`: If amount is invalid

**Example:**

```python
from spreadsheet_dl.cli import _validate_amount

amount = _validate_amount("$1,234.56")  # Returns Decimal('1234.56')
```

#### \_validate_date(date_str: str) -> date

Validate and parse a date string.

**Parameters:**

- `date_str` (str): Date string in YYYY-MM-DD format

**Returns:**

- `date`: Parsed date object

**Raises:**

- `InvalidDateError`: If date is invalid

## CLI Commands

### generate - Generate Budget Spreadsheet

Create a new budget tracking ODS spreadsheet.

**Usage:**

```bash
spreadsheet-dl generate [options]
```

**Options:**

- `-o, --output PATH`: Output directory or file path (default: current directory)
- `-m, --month MONTH`: Month number (1-12, default: current month)
- `-y, --year YEAR`: Year (default: current year)
- `-t, --template NAME`: Budget template (50_30_20, family, minimalist, zero_based, fire, high_income)
- `--theme THEME`: Visual theme (default, corporate, minimal, dark, high_contrast)
- `--empty-rows N`: Number of empty rows for data entry (default: 50)
- `--force`: Overwrite existing file without confirmation

**Examples:**

```bash
# Generate budget for current month
spreadsheet-dl generate -o output/

# Generate with specific template and theme
spreadsheet-dl generate -o output/ --template 50_30_20 --theme corporate

# Generate for specific month/year
spreadsheet-dl generate -o budget.ods -m 12 -y 2024
```

### analyze - Analyze Budget File

Analyze an existing budget ODS file and show spending summary.

**Usage:**

```bash
spreadsheet-dl analyze FILE [options]
```

**Options:**

- `--json`: Output as JSON
- `--category CATEGORY`: Filter by category
- `--start-date DATE`: Start date (YYYY-MM-DD)
- `--end-date DATE`: End date (YYYY-MM-DD)

**Examples:**

```bash
# Basic analysis
spreadsheet-dl analyze budget.ods

# Filter by category
spreadsheet-dl analyze budget.ods --category Groceries

# Date range analysis
spreadsheet-dl analyze budget.ods --start-date 2024-01-01 --end-date 2024-01-31

# JSON output
spreadsheet-dl analyze budget.ods --json
```

### expense - Quick Expense Entry

Add a quick expense entry to a budget file.

**Usage:**

```bash
spreadsheet-dl expense AMOUNT DESCRIPTION [options]
```

**Options:**

- `-c, --category CATEGORY`: Category (auto-detected if not specified)
- `-f, --file FILE`: ODS file to update (uses most recent if not specified)
- `-d, --date DATE`: Date (YYYY-MM-DD, defaults to today)
- `--dry-run`: Show what would be added without modifying the file

**Examples:**

```bash
# Quick expense with auto-categorization
spreadsheet-dl expense 25.50 "Coffee shop"

# Specify category
spreadsheet-dl expense 75.00 "Gas station" -c Transportation

# Specific file and date
spreadsheet-dl expense 120.00 "Restaurant" -f budget.ods -d 2024-01-15

# Dry run to preview
spreadsheet-dl expense 50.00 "Groceries" --dry-run
```

### import - Import Bank CSV

Import transactions from a bank CSV export.

**Usage:**

```bash
spreadsheet-dl import CSV_FILE [options]
```

**Options:**

- `-o, --output FILE`: Output ODS file
- `-b, --bank FORMAT`: Bank format (use 'banks --list' to see available formats)
- `--preview`: Preview import without writing
- `--theme THEME`: Visual theme for output file
- `--force`: Overwrite existing output file without confirmation

**Examples:**

```bash
# Auto-detect format and preview
spreadsheet-dl import bank_export.csv --preview

# Import with specific format
spreadsheet-dl import transactions.csv --bank chase_checking -o imported.ods

# Import with theme
spreadsheet-dl import export.csv -o budget.ods --theme corporate
```

### export - Export to Other Formats

Export ODS file to Excel, CSV, PDF, or JSON format.

**Usage:**

```bash
spreadsheet-dl export FILE -f FORMAT [options]
```

**Options:**

- `-o, --output FILE`: Output file path (default: same name with new extension)
- `-f, --format FORMAT`: Export format (xlsx, csv, pdf, json) [required]
- `--force`: Overwrite existing file without confirmation

**Examples:**

```bash
# Export to Excel
spreadsheet-dl export budget.ods -f xlsx

# Export to CSV
spreadsheet-dl export budget.ods -f csv -o expenses.csv

# Export to PDF
spreadsheet-dl export budget.ods -f pdf
```

### plugin - Manage Plugins (NEW in v4.0)

Manage SpreadsheetDL plugins for extensibility.

**Subcommands:**

- `list`: List all plugins
- `enable NAME`: Enable a plugin
- `disable NAME`: Disable a plugin
- `info NAME`: Show plugin information

**Options:**

- `--enabled-only`: Show only enabled plugins (for list)
- `--json`: Output as JSON (for list/info)
- `--config JSON`: Plugin configuration (for enable)

**Examples:**

```bash
# List all plugins
spreadsheet-dl plugin list

# List enabled plugins only
spreadsheet-dl plugin list --enabled-only

# Enable a plugin
spreadsheet-dl plugin enable my_plugin

# Enable with configuration
spreadsheet-dl plugin enable my_plugin --config '{"key":"value"}'

# Disable a plugin
spreadsheet-dl plugin disable my_plugin

# Show plugin info
spreadsheet-dl plugin info my_plugin
```

### category - Manage Categories (NEW in v4.0)

Add, edit, delete, and list expense categories.

**Subcommands:**

- `add NAME`: Add a custom category
- `list`: List all categories
- `update NAME`: Update a category
- `delete NAME`: Delete a custom category
- `search QUERY`: Search categories
- `suggest DESCRIPTION`: Suggest category for expense description

**Examples:**

```bash
# Add custom category
spreadsheet-dl category add "Pet Care" --color "#795548"

# List all categories
spreadsheet-dl category list

# List only custom categories
spreadsheet-dl category list --custom-only

# Update category
spreadsheet-dl category update "Pet Care" --color "#8B4513"

# Delete category
spreadsheet-dl category delete "Pet Care"

# Search categories
spreadsheet-dl category search pet

# Get suggestion
spreadsheet-dl category suggest "vet bill for dog"
```

### account - Manage Accounts (NEW in v0.6.0)

Manage financial accounts, balances, and transfers.

**Subcommands:**

- `add NAME`: Add a new account
- `list`: List accounts
- `balance [NAME]`: Show account balance(s)
- `transfer FROM TO AMOUNT`: Transfer between accounts
- `net-worth`: Calculate net worth

**Examples:**

```bash
# Add checking account
spreadsheet-dl account add "Primary Checking" --type checking --balance 1000

# List all accounts
spreadsheet-dl account list

# Show specific account balance
spreadsheet-dl account balance "Primary Checking"

# Transfer funds
spreadsheet-dl account transfer "Checking" "Savings" 500

# Calculate net worth
spreadsheet-dl account net-worth
```

### visualize - Generate Interactive Charts (NEW in v0.6.0)

Generate interactive HTML charts and dashboards.

**Usage:**

```bash
spreadsheet-dl visualize FILE [options]
```

**Options:**

- `-o, --output FILE`: Output HTML file (default: budget_dashboard.html)
- `-t, --type TYPE`: Chart type (dashboard, pie, bar, trend)
- `--theme THEME`: Visual theme (default, dark)

**Examples:**

```bash
# Generate full dashboard
spreadsheet-dl visualize budget.ods

# Generate pie chart
spreadsheet-dl visualize budget.ods -t pie -o expenses_pie.html

# Generate with dark theme
spreadsheet-dl visualize budget.ods --theme dark
```

### backup - Backup Budget Files

Create, restore, and manage backups.

**Usage:**

```bash
spreadsheet-dl backup FILE [options]
```

**Options:**

- `--list`: List available backups for this file
- `--restore BACKUP_FILE`: Restore from a specific backup file
- `--cleanup`: Remove backups older than retention period
- `--days N`: Retention period in days (default: 30)
- `--dry-run`: Show what would be done without making changes
- `--force`: Skip confirmation for restore/cleanup

**Examples:**

```bash
# Create backup
spreadsheet-dl backup budget.ods

# List backups
spreadsheet-dl backup budget.ods --list

# Restore from backup
spreadsheet-dl backup budget.ods --restore backup_20240115.ods

# Cleanup old backups
spreadsheet-dl backup budget.ods --cleanup --days 30
```

## Usage Examples

### Complete Workflow Example

```bash
# 1. Generate a new budget
spreadsheet-dl generate -o monthly/ --template family --theme corporate

# 2. Add some quick expenses
spreadsheet-dl expense 125.50 "Grocery store" -c Groceries
spreadsheet-dl expense 45.00 "Gas station" -c Transportation

# 3. Import bank transactions
spreadsheet-dl import bank_export.csv --bank chase_checking -o monthly/imported.ods

# 4. Analyze spending
spreadsheet-dl analyze monthly/budget_2024_01.ods

# 5. Create backup before modifications
spreadsheet-dl backup monthly/budget_2024_01.ods

# 6. Generate visual dashboard
spreadsheet-dl visualize monthly/budget_2024_01.ods -o dashboard.html

# 7. Export to Excel for sharing
spreadsheet-dl export monthly/budget_2024_01.ods -f xlsx
```

### Plugin Development Example

```python
# Create custom plugin (plugins/my_plugin.py)
from spreadsheet_dl.plugins import PluginInterface

class MyPlugin(PluginInterface):
    @property
    def name(self) -> str:
        return "my_plugin"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "My custom plugin"

    def initialize(self, config=None):
        print(f"Plugin {self.name} initialized")

    def shutdown(self):
        print(f"Plugin {self.name} shutdown")

# Enable the plugin
# $ spreadsheet-dl plugin enable my_plugin
```

## Error Handling

All commands use structured exceptions from `spreadsheet_dl.exceptions`:

```python
try:
    # CLI operation
    result = _cmd_generate(args)
except OperationCancelledError:
    print("Operation cancelled.", file=sys.stderr)
    sys.exit(1)
except FinanceTrackerError as e:
    print(f"Error [{e.error_code}]: {e.message}", file=sys.stderr)
    sys.exit(1)
except KeyboardInterrupt:
    print("\nOperation cancelled.", file=sys.stderr)
    sys.exit(130)
```

## See Also

- [plugins](plugins.md) - Plugin system framework
- [exceptions](exceptions.md) - Exception hierarchy
- [config](config.md) - Configuration management
- [backup](backup.md) - Backup/restore functionality
- [export](export.md) - Multi-format export
