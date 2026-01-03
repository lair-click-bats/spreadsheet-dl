# Best Practices

Comprehensive guide to using SpreadsheetDL effectively for budget management and financial tracking.

## Table of Contents

- [File Organization](#file-organization)
- [Category Management](#category-management)
- [Import Workflow](#import-workflow)
- [Performance Tips](#performance-tips)
- [Security Recommendations](#security-recommendations)
- [Troubleshooting](#troubleshooting)

## File Organization

### Directory Structure

Organize your budgets and related files systematically:

```
~/budgets/
├── 2026/
│   ├── budget_2026_01.ods
│   ├── budget_2026_02.ods
│   └── ...
├── 2025/
│   ├── budget_2025_01.ods
│   └── ...
├── reports/
│   ├── 2026/
│   │   ├── report_2026_01.md
│   │   └── report_2026_01.html
│   └── 2025/
├── imports/
│   ├── raw/
│   │   ├── chase_2026_01.csv
│   │   └── ...
│   └── processed/
└── templates/
    ├── my_custom_budget.ods
    └── monthly_template.ods
```

### Naming Conventions

**Budget files:**

- Format: `budget_YYYY_MM.ods`
- Example: `budget_2026_01.ods`
- Consistent naming enables automated processing

**Report files:**

- Format: `report_YYYY_MM.{format}`
- Example: `report_2026_01.md`, `report_2026_01.html`

**Import files:**

- Format: `{bank}_{YYYY_MM}.csv`
- Example: `chase_2026_01.csv`
- Keep raw CSVs for reference

### Automation Script

```python
#!/usr/bin/env python3
"""Organize budget files automatically."""

from pathlib import Path
import shutil
from datetime import date

def organize_budgets():
    """Move budgets to year-based directories."""
    budget_dir = Path.home() / "budgets"

    # Find all budget files in root
    for budget_file in budget_dir.glob("budget_*.ods"):
        # Extract year from filename
        parts = budget_file.stem.split("_")
        if len(parts) >= 2:
            year = parts[1]

            # Create year directory
            year_dir = budget_dir / year
            year_dir.mkdir(exist_ok=True)

            # Move file
            new_path = year_dir / budget_file.name
            if not new_path.exists():
                shutil.move(budget_file, new_path)
                print(f"Moved: {budget_file.name} → {year}/{budget_file.name}")

if __name__ == "__main__":
    organize_budgets()
```

## Category Management

### Standard Categories

Use standard categories consistently:

**Essential (Needs):**

- Housing
- Groceries
- Utilities
- Transportation
- Healthcare
- Insurance

**Discretionary (Wants):**

- Dining Out
- Entertainment
- Shopping
- Personal Care
- Hobbies

**Financial:**

- Savings
- Debt Payment
- Investment
- Emergency Fund

### Custom Categories

Create custom categories for specialized tracking:

```bash
# Add pet-related category
spreadsheet-dl category add "Pet Care" --color "#795548" --budget 150

# Add subcategory
spreadsheet-dl category add "Pet Medical" --parent "Pet Care" --budget 50

# Add hobby category
spreadsheet-dl category add "Photography" --color "#9C27B0" --budget 100
```

### Category Strategies

**1. Granular Tracking**

- Break broad categories into subcategories
- Example: "Transportation" → "Gas", "Car Payment", "Maintenance", "Insurance"
- Benefit: Identify specific spending patterns

**2. Goal-Based Categories**

- Create categories aligned with financial goals
- Example: "Vacation Fund", "House Down Payment", "Car Replacement"
- Benefit: Track progress toward specific objectives

**3. Time-Based Categories**

- Separate recurring vs. one-time expenses
- Example: "Monthly Bills" vs. "Irregular Expenses"
- Benefit: Better cash flow planning

## Import Workflow

### Monthly Import Routine

Best practices for importing bank data:

**1. Export from Bank (Monthly)**

```bash
# Export on the same day each month (e.g., last day)
# Download to consistent location
~/Downloads/chase_2026_01.csv
```

**2. Preview Before Import**

```bash
# Always preview first
spreadsheet-dl import ~/Downloads/chase_2026_01.csv --preview

# Check:
# - Correct date range
# - No duplicate transactions
# - Categories look reasonable
```

**3. Import to Budget**

```bash
# Import with theme
spreadsheet-dl import ~/Downloads/chase_2026_01.csv \
  -o ~/budgets/2026/budget_2026_01.ods \
  --theme default
```

**4. Review Categorization**

```bash
# Analyze imported data
spreadsheet-dl analyze ~/budgets/2026/budget_2026_01.ods

# Check categories needing adjustment
```

**5. Archive CSV**

```bash
# Move to imports archive
mv ~/Downloads/chase_2026_01.csv ~/budgets/imports/raw/
```

### Multi-Account Import

Consolidate transactions from multiple accounts:

```python
#!/usr/bin/env python3
"""Import from multiple accounts."""

from pathlib import Path
from datetime import date
from spreadsheet_dl import import_bank_csv, OdsGenerator

def import_all_accounts():
    """Import from all accounts."""
    downloads = Path.home() / "Downloads"
    budget_dir = Path.home() / "budgets" / str(date.today().year)

    # Import from each account
    all_transactions = []

    # Checking account
    if (downloads / "chase_checking.csv").exists():
        checking = import_bank_csv(downloads / "chase_checking.csv")
        all_transactions.extend(checking)
        print(f"Imported {len(checking)} checking transactions")

    # Savings account
    if (downloads / "chase_savings.csv").exists():
        savings = import_bank_csv(downloads / "chase_savings.csv")
        all_transactions.extend(savings)
        print(f"Imported {len(savings)} savings transactions")

    # Credit card
    if (downloads / "chase_credit.csv").exists():
        credit = import_bank_csv(downloads / "chase_credit.csv")
        all_transactions.extend(credit)
        print(f"Imported {len(credit)} credit transactions")

    # Sort by date
    all_transactions.sort(key=lambda t: t.date)

    # Create consolidated budget
    today = date.today()
    output_file = budget_dir / f"budget_{today.year}_{today.month:02d}.ods"

    generator = OdsGenerator()
    generator.create_budget_spreadsheet(
        output_file,
        expenses=all_transactions,
        month=today.month,
        year=today.year
    )

    print(f"\nConsolidated budget: {output_file}")
    print(f"Total transactions: {len(all_transactions)}")
    print(f"Total amount: ${sum(t.amount for t in all_transactions):,.2f}")

if __name__ == "__main__":
    import_all_accounts()
```

## Performance Tips

### Large Datasets

Optimize for budgets with 1000+ transactions:

**1. Use Streaming I/O**

```python
from spreadsheet_dl import stream_read, stream_write

# Read large file efficiently
for row in stream_read("large_budget.ods", sheet="Expenses"):
    # Process row by row
    process_transaction(row)
```

**2. Enable Caching**

```python
from spreadsheet_dl import FileCache

# Cache parsed data
cache = FileCache(max_size_mb=100)
analyzer = BudgetAnalyzer("budget.ods", cache=cache)
```

**3. Batch Operations**

```python
from spreadsheet_dl import BatchProcessor, OdsEditor

# Add multiple expenses efficiently
editor = OdsEditor("budget.ods")
batch = BatchProcessor(editor)

# Add in batch
for expense in expense_list:
    batch.add_expense(expense)

# Commit all at once
batch.commit()
editor.save()
```

### Formula Optimization

Avoid circular references and complex formulas:

**Bad:**

```python
# Creates circular dependency
f.sum(f.range("A1", "A100"))  # If used in column A
```

**Good:**

```python
# Use separate summary sheet
builder.sheet("Summary")
# Reference Expense Log, not self
```

## Security Recommendations

### Protect Sensitive Data

**1. Never Commit Financial Files**

```bash
# .gitignore
*.ods
*.xlsx
budgets/
reports/
imports/
*.csv

# Only commit
examples/
scripts/
README.md
```

**2. Use Encryption**

```python
from spreadsheet_dl import FileEncryptor

# Encrypt budget file
encryptor = FileEncryptor()
encryptor.encrypt_file(
    "budget_2026_01.ods",
    "budget_2026_01.ods.enc",
    password="strong-password"
)

# Decrypt when needed
encryptor.decrypt_file(
    "budget_2026_01.ods.enc",
    "budget_2026_01.ods",
    password="strong-password"
)
```

**3. Backup Regularly**

```bash
# Automated backup
spreadsheet-dl backup budget.ods

# List backups
spreadsheet-dl backup budget.ods --list

# Cleanup old backups (keep 30 days)
spreadsheet-dl backup budget.ods --cleanup --days 30
```

**4. Secure Cloud Storage**

```bash
# Upload to Nextcloud (encrypted transit)
export NEXTCLOUD_URL=https://cloud.example.com
export NEXTCLOUD_USER=username
export NEXTCLOUD_PASSWORD=app-password

spreadsheet-dl upload budget.ods
```

### Access Control

**Set file permissions:**

```bash
# Make budgets private
chmod 600 ~/budgets/*.ods

# Only you can read/write
ls -l ~/budgets/
# -rw------- 1 user user 45678 Jan 15 budget_2026_01.ods
```

## Troubleshooting

### Common Issues

**1. Formulas Not Calculating**

_Problem:_ Summary sheet shows #REF or #VALUE errors

_Solution:_

- Open in LibreOffice Calc (better ODS support than Excel)
- Check sheet names match exactly
- Verify cell ranges are correct
- Enable automatic calculation: Tools → Cell Contents → AutoCalculate

**2. Import Categories Wrong**

_Problem:_ Auto-categorization is inaccurate

_Solution:_

```python
# Customize categorization
from spreadsheet_dl import TransactionCategorizer

categorizer = TransactionCategorizer()
categorizer.add_pattern("MY GYM", ExpenseCategory.HEALTHCARE)
categorizer.add_pattern("PET STORE", "Pet Care")  # Custom category

# Use for imports
import_bank_csv("transactions.csv", categorizer=categorizer)
```

**3. File Corruption**

_Problem:_ Cannot open ODS file

_Solution:_

```bash
# Try to repair
libreoffice --headless --convert-to ods budget_2026_01.ods

# Or restore from backup
spreadsheet-dl backup budget_2026_01.ods --list
spreadsheet-dl backup budget_2026_01.ods --restore backup_file.ods.gz
```

**4. Performance Issues**

_Problem:_ Slow analysis on large budgets

_Solution:_

```python
# Use sampling for quick analysis
from spreadsheet_dl import BudgetAnalyzer

analyzer = BudgetAnalyzer("large_budget.ods")

# Analyze recent data only
recent = analyzer.filter_by_date_range(
    start_date=date(2026, 1, 1),
    end_date=date.today()
)
```

### Getting Help

**Check logs:**

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run your operation
# Logs will show detailed information
```

**Report issues:**

1. Check existing issues on GitHub
2. Provide minimal reproduction example
3. Include version info: `spreadsheet-dl --version`
4. Share error messages and logs

## Advanced Workflows

### Automated Monthly Close

```python
#!/usr/bin/env python3
"""End-of-month automation."""

from pathlib import Path
from datetime import date
from spreadsheet_dl import (
    import_bank_csv,
    OdsGenerator,
    ReportGenerator,
    create_budget_dashboard,
    BackupManager,
)

def month_end_close():
    """Complete month-end workflow."""
    today = date.today()
    budget_dir = Path.home() / "budgets" / str(today.year)
    budget_file = budget_dir / f"budget_{today.year}_{today.month:02d}.ods"

    # 1. Import latest transactions
    print("1. Importing transactions...")
    latest_csv = Path.home() / "Downloads" / f"bank_{today.year}_{today.month:02d}.csv"
    if latest_csv.exists():
        transactions = import_bank_csv(latest_csv)
        generator = OdsGenerator()
        generator.create_budget_spreadsheet(budget_file, expenses=transactions)

    # 2. Generate reports
    print("2. Generating reports...")
    report_dir = budget_dir / "reports"
    report_dir.mkdir(exist_ok=True)

    gen = ReportGenerator(budget_file)
    gen.save_report(report_dir / f"report_{today.year}_{today.month:02d}.md", "markdown")
    create_budget_dashboard(budget_file, report_dir / f"dashboard_{today.year}_{today.month:02d}.html")

    # 3. Backup
    print("3. Creating backup...")
    backup_mgr = BackupManager()
    backup_mgr.create_backup(budget_file)

    # 4. Analyze
    print("4. Analyzing budget...")
    analyzer = BudgetAnalyzer(budget_file)
    summary = analyzer.get_summary()

    print("\n" + "="*50)
    print("MONTH-END SUMMARY")
    print("="*50)
    print(f"Total Spent: ${summary.total_spent:,.2f}")
    print(f"Budget Used: {summary.percent_used:.1f}%")
    print(f"Savings: ${summary.total_budget - summary.total_spent:,.2f}")
    print("="*50)

if __name__ == "__main__":
    month_end_close()
```

## Summary

**Key Takeaways:**

1. **Organization** - Use consistent file structure and naming
2. **Categories** - Start with standards, customize as needed
3. **Imports** - Preview first, archive raw data
4. **Performance** - Use streaming for large datasets
5. **Security** - Encrypt sensitive files, regular backups
6. **Automation** - Script repetitive workflows

**Next Steps:**

- Review [tutorials](tutorials/) for detailed walkthroughs
- Explore [API documentation](api/) for advanced usage
- Check [examples](../examples/) for working code

## Additional Resources

- [Installation Guide](installation.md)
- [CLI Reference](cli.md)
- [API Reference](api/)
- [GitHub Issues](https://github.com/USER/spreadsheet-dl/issues)
