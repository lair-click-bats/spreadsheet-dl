# API Reference

Complete API documentation for SpreadsheetDL.

## Module Overview

| Module | Description |
|--------|-------------|
| [ods_generator](ods_generator.md) | Create ODS spreadsheets |
| [ods_editor](ods_editor.md) | Modify existing ODS files |
| [budget_analyzer](budget_analyzer.md) | Analyze budget data |
| [report_generator](report_generator.md) | Generate reports |
| [csv_import](csv_import.md) | Import bank CSV files |
| [analytics](analytics.md) | Dashboard analytics |
| [alerts](alerts.md) | Budget alert system |
| [recurring](recurring.md) | Recurring expenses |
| [templates](templates.md) | Budget templates |
| [builder](builder.md) | Fluent builder API |
| [webdav_upload](webdav_upload.md) | Nextcloud WebDAV |
| [config](config.md) | Configuration management |
| [exceptions](exceptions.md) | Exception classes |

## Quick Reference

### Creating Budgets

```python
from spreadsheet_dl import OdsGenerator, create_monthly_budget

# Simple creation
path = create_monthly_budget("./budgets")

# With options
generator = OdsGenerator(theme="corporate")
generator.create_budget_spreadsheet(
    "budget.ods",
    month=1,
    year=2025,
)
```

### Adding Expenses

```python
from spreadsheet_dl import OdsEditor, ExpenseEntry, ExpenseCategory
from decimal import Decimal
from datetime import date

# Edit existing file
editor = OdsEditor("budget.ods")
editor.append_expense(ExpenseEntry(
    date=date.today(),
    category=ExpenseCategory.GROCERIES,
    description="Weekly shopping",
    amount=Decimal("125.50"),
))
editor.save()
```

### Analyzing Data

```python
from spreadsheet_dl import BudgetAnalyzer

analyzer = BudgetAnalyzer("budget.ods")
summary = analyzer.get_summary()

print(f"Budget: ${summary.total_budget}")
print(f"Spent: ${summary.total_spent}")
print(f"Used: {summary.percent_used}%")
```

### Generating Reports

```python
from spreadsheet_dl import ReportGenerator

generator = ReportGenerator("budget.ods")
print(generator.generate_markdown_report())
```

### Importing CSV

```python
from spreadsheet_dl import import_bank_csv, OdsGenerator

expenses = import_bank_csv("transactions.csv", bank="chase")
generator = OdsGenerator()
generator.create_budget_spreadsheet("imported.ods", expenses=expenses)
```

## Core Classes

### OdsGenerator

Creates new ODS spreadsheets.

```python
class OdsGenerator:
    def __init__(
        self,
        theme: str | Theme | None = None,
        theme_dir: Path | str | None = None,
    ) -> None: ...

    def create_budget_spreadsheet(
        self,
        output_path: Path | str,
        *,
        month: int | None = None,
        year: int | None = None,
        budget_allocations: Sequence[BudgetAllocation] | None = None,
        expenses: Sequence[ExpenseEntry] | None = None,
    ) -> Path: ...
```

### OdsEditor

Modifies existing ODS files.

```python
class OdsEditor:
    def __init__(self, file_path: Path | str) -> None: ...

    def append_expense(
        self,
        expense: ExpenseEntry,
        sheet_name: str = "Expense Log",
    ) -> int: ...

    def save(self, output_path: Path | str | None = None) -> Path: ...
```

### BudgetAnalyzer

Analyzes budget data.

```python
class BudgetAnalyzer:
    def __init__(self, file_path: Path | str) -> None: ...

    def get_summary(self) -> BudgetSummary: ...
    def filter_by_category(self, category: str) -> pd.DataFrame: ...
    def filter_by_date_range(self, start: date, end: date) -> pd.DataFrame: ...
```

## Data Classes

### ExpenseEntry

```python
@dataclass
class ExpenseEntry:
    date: date
    category: ExpenseCategory
    description: str
    amount: Decimal
    notes: str = ""
```

### BudgetAllocation

```python
@dataclass
class BudgetAllocation:
    category: ExpenseCategory
    monthly_budget: Decimal
    notes: str = ""
```

### ExpenseCategory

```python
class ExpenseCategory(Enum):
    HOUSING = "Housing"
    UTILITIES = "Utilities"
    GROCERIES = "Groceries"
    TRANSPORTATION = "Transportation"
    HEALTHCARE = "Healthcare"
    INSURANCE = "Insurance"
    ENTERTAINMENT = "Entertainment"
    DINING_OUT = "Dining Out"
    CLOTHING = "Clothing"
    PERSONAL = "Personal Care"
    EDUCATION = "Education"
    SAVINGS = "Savings"
    DEBT_PAYMENT = "Debt Payment"
    GIFTS = "Gifts"
    SUBSCRIPTIONS = "Subscriptions"
    MISCELLANEOUS = "Miscellaneous"
```

## Exceptions

All exceptions inherit from `SpreadsheetDLError`:

```python
class SpreadsheetDLError(Exception):
    message: str
    error_code: str

class OdsError(SpreadsheetDLError): ...
class OdsReadError(OdsError): ...
class OdsWriteError(OdsError): ...
class SheetNotFoundError(OdsError): ...

class ValidationError(SpreadsheetDLError): ...
class InvalidAmountError(ValidationError): ...
class InvalidDateError(ValidationError): ...
class InvalidCategoryError(ValidationError): ...
```

## Type Hints

The library is fully typed. Common type aliases:

```python
from pathlib import Path
from decimal import Decimal
from datetime import date
from typing import Sequence

# Path can be string or Path object
def func(path: Path | str) -> Path: ...

# Sequences accept lists, tuples, etc.
def func(items: Sequence[ExpenseEntry]) -> None: ...
```
