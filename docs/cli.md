# CLI Reference

Command-line interface documentation for Finance Tracker.

## Usage

```bash
finance-tracker [OPTIONS] COMMAND [ARGS]...
```

Or with uv:

```bash
uv run finance-tracker [OPTIONS] COMMAND [ARGS]...
```

## Global Options

| Option | Description |
|--------|-------------|
| `-V, --version` | Show version and exit |
| `--config FILE` | Path to configuration file |
| `--no-color` | Disable colored output |
| `--help` | Show help message |

---

## Commands

### generate

Create a new budget spreadsheet.

```bash
finance-tracker generate [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output PATH` | Output directory or file | Current directory |
| `-m, --month MONTH` | Month number (1-12) | Current month |
| `-y, --year YEAR` | Year | Current year |
| `-t, --template NAME` | Budget template | None |
| `--theme NAME` | Visual theme | None |
| `--empty-rows N` | Empty rows for data entry | 50 |

**Examples:**

```bash
# Basic creation
finance-tracker generate -o ./budgets/

# Specific month/year
finance-tracker generate -m 6 -y 2025

# With template and theme
finance-tracker generate -t family --theme corporate -o ./budgets/
```

---

### expense

Add a quick expense entry to a budget file.

**New in v0.4.1**: Now actually writes to ODS files!

```bash
finance-tracker expense AMOUNT DESCRIPTION [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `AMOUNT` | Expense amount (e.g., 25.50 or $25.50) |
| `DESCRIPTION` | Expense description |

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `-c, --category CAT` | Category name | Auto-detected |
| `-f, --file PATH` | ODS file to update | Most recent budget_*.ods |
| `-d, --date DATE` | Date (YYYY-MM-DD) | Today |
| `--dry-run` | Preview without modifying | False |

**Examples:**

```bash
# Basic expense (auto-categorized)
finance-tracker expense 25.50 "Walmart groceries"

# Specify category
finance-tracker expense 45.00 "Gas station" -c Transportation

# Specify date
finance-tracker expense 150.00 "Electric bill" -c Utilities -d 2025-01-15

# Specify file
finance-tracker expense 12.99 "Netflix" -f budget_2025_01.ods -c Subscriptions

# Preview without writing
finance-tracker expense 100.00 "Test" --dry-run
```

**Valid Categories:**
- Housing, Utilities, Groceries, Transportation
- Healthcare, Insurance, Entertainment, Dining Out
- Clothing, Personal Care, Education, Savings
- Debt Payment, Gifts, Subscriptions, Miscellaneous

---

### analyze

Analyze a budget file and show spending summary.

```bash
finance-tracker analyze FILE [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON |
| `--category CAT` | Filter by category |
| `--start-date DATE` | Start date (YYYY-MM-DD) |
| `--end-date DATE` | End date (YYYY-MM-DD) |

**Examples:**

```bash
# Basic analysis
finance-tracker analyze budget.ods

# JSON output
finance-tracker analyze budget.ods --json

# Filter by category
finance-tracker analyze budget.ods --category Groceries

# Filter by date range
finance-tracker analyze budget.ods --start-date 2025-01-01 --end-date 2025-01-31
```

---

### report

Generate a formatted report from a budget file.

```bash
finance-tracker report FILE [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output PATH` | Output file path | stdout |
| `-f, --format FMT` | Format (text, markdown, json) | markdown |

**Examples:**

```bash
# Markdown to stdout
finance-tracker report budget.ods

# Text format
finance-tracker report budget.ods -f text

# Save to file
finance-tracker report budget.ods -f markdown -o report.md
```

---

### dashboard

Display an analytics dashboard for a budget file.

```bash
finance-tracker dashboard FILE [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON |

**Example Output:**

```
============================================================
BUDGET DASHBOARD
============================================================

Status: [OK] Budget is healthy

SUMMARY
----------------------------------------
  Total Budget:     $    4,825.00
  Total Spent:      $    1,245.50
  Remaining:        $    3,579.50
  Budget Used:              25.8%
  Days Remaining:             16
  Daily Budget:     $      223.72

TOP SPENDING
----------------------------------------
  1. Groceries            $   275.50
  2. Housing              $   250.00
  3. Dining Out           $   125.00
```

---

### alerts

Check for budget alerts and warnings.

```bash
finance-tracker alerts FILE [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON |
| `--critical-only` | Show only critical alerts |

---

### import

Import transactions from a bank CSV export.

```bash
finance-tracker import CSV_FILE [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output PATH` | Output ODS file | imported_YYYYMMDD.ods |
| `-b, --bank BANK` | Bank format | auto |
| `--preview` | Preview without writing | False |
| `--theme NAME` | Visual theme | None |

**Supported Banks:**
- chase, bank_of_america, capital_one
- wells_fargo, citi, usaa, generic

**Examples:**

```bash
# Auto-detect bank format
finance-tracker import transactions.csv

# Specify bank
finance-tracker import transactions.csv --bank chase

# Preview first
finance-tracker import transactions.csv --preview
```

---

### upload

Upload a budget file to Nextcloud via WebDAV.

```bash
finance-tracker upload FILE [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `-p, --path PATH` | Remote path on Nextcloud |

**Required Environment Variables:**
- `NEXTCLOUD_URL` - Server URL
- `NEXTCLOUD_USER` - Username
- `NEXTCLOUD_PASSWORD` - App password

---

### templates

List available budget templates.

```bash
finance-tracker templates [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON |

---

### themes

List available visual themes.

```bash
finance-tracker themes [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON |

---

### config

Manage configuration.

```bash
finance-tracker config [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--init` | Create a new config file |
| `--show` | Show current configuration |
| `--path PATH` | Path for config file |

---

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | General error |
| 130 | Interrupted (Ctrl+C) |

## Error Codes

Errors include machine-readable codes:

```
Error [INVALID_AMOUNT]: Invalid amount 'abc': Not a valid number
Error [INVALID_DATE]: Invalid date 'bad': Expected format: YYYY-MM-DD
Error [INVALID_CATEGORY]: Invalid category 'Unknown'. Valid: Housing, Utilities, ...
Error [FILE_NOT_FOUND]: File not found: budget.ods
Error [SHEET_NOT_FOUND]: Sheet 'Expenses' not found. Available: Expense Log, Budget
```
