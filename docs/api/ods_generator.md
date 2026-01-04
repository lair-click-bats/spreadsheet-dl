# ods_generator

Module for creating ODS spreadsheets for budget tracking.

## Module Contents

- [OdsGenerator](#odsgenerator) - Main class for creating ODS files
- [create_monthly_budget](#create_monthly_budget) - Convenience function
- [ExpenseCategory](#expensecategory) - Expense category enum
- [ExpenseEntry](#expenseentry) - Single expense data class
- [BudgetAllocation](#budgetallocation) - Budget allocation data class

---

## OdsGenerator

Generate ODS spreadsheets for family budget tracking.

### Constructor

```python
class OdsGenerator:
    def __init__(
        self,
        theme: str | Theme | None = None,
        theme_dir: Path | str | None = None,
    ) -> None:
        """
        Initialize the ODS generator.

        Args:
            theme: Theme name (e.g., "default", "corporate") or Theme object.
                   If None, uses legacy hardcoded styles.
            theme_dir: Directory containing theme YAML files.
        """
```

### Methods

#### create_budget_spreadsheet

```python
def create_budget_spreadsheet(
    self,
    output_path: Path | str,
    *,
    month: int | None = None,
    year: int | None = None,
    budget_allocations: Sequence[BudgetAllocation] | None = None,
    expenses: Sequence[ExpenseEntry] | None = None,
) -> Path:
    """
    Create a complete budget tracking spreadsheet.

    Args:
        output_path: Path to save the ODS file.
        month: Month number (1-12). Defaults to current month.
        year: Year. Defaults to current year.
        budget_allocations: List of budget allocations per category.
        expenses: List of expense entries to pre-populate.

    Returns:
        Path to the created ODS file.
    """
```

#### create_expense_template

```python
def create_expense_template(
    self,
    output_path: Path | str,
    *,
    categories: Sequence[ExpenseCategory] | None = None,
) -> Path:
    """
    Create a blank expense tracking template.

    Args:
        output_path: Path to save the ODS file.
        categories: Categories to include. Defaults to all.

    Returns:
        Path to the created ODS file.
    """
```

### Usage Examples

#### Basic Creation

```python
from spreadsheet_dl import OdsGenerator

generator = OdsGenerator()
path = generator.create_budget_spreadsheet("budget_2025_01.ods")
print(f"Created: {path}")
```

#### With Theme

```python
from spreadsheet_dl import OdsGenerator

generator = OdsGenerator(theme="corporate")
path = generator.create_budget_spreadsheet(
    "budget.ods",
    month=1,
    year=2025,
)
```

#### With Pre-populated Data

```python
from spreadsheet_dl import (
    OdsGenerator, ExpenseEntry, BudgetAllocation, ExpenseCategory
)
from decimal import Decimal
from datetime import date

generator = OdsGenerator()
path = generator.create_budget_spreadsheet(
    "budget.ods",
    expenses=[
        ExpenseEntry(
            date=date(2025, 1, 5),
            category=ExpenseCategory.GROCERIES,
            description="Weekly groceries",
            amount=Decimal("125.50"),
        ),
    ],
    budget_allocations=[
        BudgetAllocation(ExpenseCategory.GROCERIES, Decimal("600")),
        BudgetAllocation(ExpenseCategory.UTILITIES, Decimal("200")),
    ],
)
```

---

## create_monthly_budget

Convenience function to create a monthly budget spreadsheet.

```python
def create_monthly_budget(
    output_dir: Path | str,
    *,
    month: int | None = None,
    year: int | None = None,
    theme: str | None = None,
) -> Path:
    """
    Create a monthly budget spreadsheet.

    Args:
        output_dir: Directory to save the file.
        month: Month number (1-12). Defaults to current.
        year: Year. Defaults to current.
        theme: Optional theme name.

    Returns:
        Path to the created file (budget_YYYY_MM.ods).
    """
```

### Example

```python
from spreadsheet_dl import create_monthly_budget

# Creates budget_2025_01.ods in ./budgets/
path = create_monthly_budget("./budgets/", month=1, year=2025)
```

---

## ExpenseCategory

Enum of standard expense categories.

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

### Usage

```python
from spreadsheet_dl import ExpenseCategory

# By name
cat = ExpenseCategory.GROCERIES

# By value
cat = ExpenseCategory("Groceries")

# Get display value
print(cat.value)  # "Groceries"

# Iterate all
for cat in ExpenseCategory:
    print(f"{cat.name}: {cat.value}")
```

---

## ExpenseEntry

Data class for a single expense entry.

```python
@dataclass
class ExpenseEntry:
    date: date
    category: ExpenseCategory
    description: str
    amount: Decimal
    notes: str = ""
```

### Example

```python
from spreadsheet_dl import ExpenseEntry, ExpenseCategory
from decimal import Decimal
from datetime import date

expense = ExpenseEntry(
    date=date(2025, 1, 15),
    category=ExpenseCategory.GROCERIES,
    description="Costco shopping",
    amount=Decimal("245.50"),
    notes="Monthly bulk run",
)

print(f"${expense.amount} on {expense.date}")
```

---

## BudgetAllocation

Data class for budget allocation per category.

```python
@dataclass
class BudgetAllocation:
    category: ExpenseCategory
    monthly_budget: Decimal
    notes: str = ""
```

### Example

```python
from spreadsheet_dl import BudgetAllocation, ExpenseCategory
from decimal import Decimal

allocations = [
    BudgetAllocation(ExpenseCategory.HOUSING, Decimal("1500")),
    BudgetAllocation(ExpenseCategory.UTILITIES, Decimal("200")),
    BudgetAllocation(ExpenseCategory.GROCERIES, Decimal("600")),
]

total = sum(a.monthly_budget for a in allocations)
print(f"Total budget: ${total}")
```

---

## Spreadsheet Structure

Generated spreadsheets contain three sheets:

### Expense Log

| Date       | Category  | Description     | Amount  | Notes |
| ---------- | --------- | --------------- | ------- | ----- |
| 2025-01-15 | Groceries | Weekly shopping | $125.50 |       |

### Budget

| Category  | Monthly Budget | Notes |
| --------- | -------------- | ----- |
| Groceries | $600.00        |       |
| Utilities | $200.00        |       |

### Summary

| Category  | Budget  | Actual      | Remaining |
| --------- | ------- | ----------- | --------- |
| Groceries | $600.00 | =SUMIF(...) | =B2-C2    |

The Summary sheet uses formulas to automatically calculate totals.

---

## Available Themes

| Theme           | Description                        |
| --------------- | ---------------------------------- |
| `default`       | Blue headers, green/red indicators |
| `corporate`     | Navy blue, professional            |
| `minimal`       | Gray, subtle borders               |
| `dark`          | Dark backgrounds                   |
| `high_contrast` | Accessibility focused              |

See [themes](../themes.md) for details.
