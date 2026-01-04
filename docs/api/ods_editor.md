# ods_editor

Module for editing existing ODS spreadsheets.

**Feature**: Implements FR-CORE-003 - expense append functionality (stable in v4.0.0).

## Module Contents

- [OdsEditor](#odseditor) - Main class for editing ODS files
- [append_expense_to_file](#append_expense_to_file) - Convenience function

---

## OdsEditor

Edit existing ODS spreadsheets safely.

### Constructor

```python
class OdsEditor:
    def __init__(self, file_path: Path | str) -> None:
        """
        Initialize editor with an existing ODS file.

        Args:
            file_path: Path to the ODS file to edit.

        Raises:
            OdsReadError: If file cannot be read or is invalid.
        """
```

### Methods

#### get_sheet_names

```python
def get_sheet_names(self) -> list[str]:
    """
    Get list of sheet names in the document.

    Returns:
        List of sheet names.
    """
```

#### get_sheet

```python
def get_sheet(self, name: str) -> Table:
    """
    Get a sheet by name.

    Args:
        name: Sheet name to find.

    Returns:
        Table element for the sheet.

    Raises:
        SheetNotFoundError: If sheet not found.
    """
```

#### find_next_empty_row

```python
def find_next_empty_row(self, sheet_name: str) -> int:
    """
    Find the index of the next empty row in a sheet.

    Scans from row 1 (after header) looking for first row where
    the first cell is empty.

    Args:
        sheet_name: Name of the sheet to scan.

    Returns:
        Row index (0-based) of the next empty row.
    """
```

#### append_expense

```python
def append_expense(
    self,
    expense: ExpenseEntry,
    sheet_name: str = "Expense Log"
) -> int:
    """
    Append an expense entry to the expense sheet.

    Args:
        expense: ExpenseEntry to append.
        sheet_name: Name of the expense sheet (default: "Expense Log").

    Returns:
        Row number where expense was added (1-based).

    Raises:
        SheetNotFoundError: If expense sheet not found.
        OdsWriteError: If append fails.
    """
```

#### save

```python
def save(self, output_path: Path | str | None = None) -> Path:
    """
    Save the modified document.

    Args:
        output_path: Optional path to save to. If None, overwrites original.

    Returns:
        Path where file was saved.

    Raises:
        OdsWriteError: If save fails.
    """
```

### Usage Example

```python
from spreadsheet_dl import OdsEditor, ExpenseEntry, ExpenseCategory
from decimal import Decimal
from datetime import date

# Open existing budget file
editor = OdsEditor("budget_2025_01.ods")

# Check available sheets
print(editor.get_sheet_names())
# Output: ['Expense Log', 'Budget', 'Summary - January 2025']

# Create expense entry
expense = ExpenseEntry(
    date=date(2025, 1, 15),
    category=ExpenseCategory.GROCERIES,
    description="Costco run",
    amount=Decimal("245.50"),
    notes="Monthly bulk shopping",
)

# Append expense
row_num = editor.append_expense(expense)
print(f"Added expense at row {row_num}")

# Save changes
editor.save()

# Or save to new file
editor.save("budget_2025_01_updated.ods")
```

### Adding Multiple Expenses

```python
expenses = [
    ExpenseEntry(
        date=date(2025, 1, 1),
        category=ExpenseCategory.HOUSING,
        description="Rent",
        amount=Decimal("1500.00"),
    ),
    ExpenseEntry(
        date=date(2025, 1, 5),
        category=ExpenseCategory.UTILITIES,
        description="Electric bill",
        amount=Decimal("95.00"),
    ),
]

editor = OdsEditor("budget.ods")
for expense in expenses:
    row = editor.append_expense(expense)
    print(f"Added {expense.description} at row {row}")
editor.save()
```

---

## append_expense_to_file

Convenience function for single expense additions.

### Signature

```python
def append_expense_to_file(
    file_path: Path | str,
    expense: ExpenseEntry,
    sheet_name: str = "Expense Log",
) -> tuple[Path, int]:
    """
    Append a single expense to an ODS file.

    Args:
        file_path: Path to the ODS file.
        expense: ExpenseEntry to append.
        sheet_name: Name of the expense sheet.

    Returns:
        Tuple of (file path, row number where added).
    """
```

### Usage Example

```python
from spreadsheet_dl import append_expense_to_file, ExpenseEntry, ExpenseCategory
from decimal import Decimal
from datetime import date

expense = ExpenseEntry(
    date=date.today(),
    category=ExpenseCategory.DINING_OUT,
    description="Lunch meeting",
    amount=Decimal("45.00"),
)

path, row = append_expense_to_file("budget.ods", expense)
print(f"Added to {path} at row {row}")
```

---

## Error Handling

```python
from spreadsheet_dl import OdsEditor
from spreadsheet_dl.exceptions import OdsReadError, SheetNotFoundError, OdsWriteError

try:
    editor = OdsEditor("budget.ods")
except OdsReadError as e:
    print(f"Cannot read file: {e.message}")
    print(f"Error code: {e.error_code}")

try:
    editor.append_expense(expense, sheet_name="Wrong Sheet")
except SheetNotFoundError as e:
    print(f"Sheet not found: {e.sheet_name}")
    print(f"Available: {e.available_sheets}")

try:
    editor.save()
except OdsWriteError as e:
    print(f"Cannot save: {e.message}")
```

---

## Implementation Notes

### Thread Safety

OdsEditor is NOT thread-safe. Use separate instances for concurrent access.

### Memory Usage

The entire ODS file is loaded into memory. For very large files, consider:

- Processing in batches
- Using the low-level odfpy API

### Preserving Formatting

OdsEditor preserves:

- Existing cell styles
- Formulas
- Sheet structure

It does NOT preserve:

- Conditional formatting rules (partially)
- Complex cell validation

### Performance

For bulk additions, use a single editor instance:

```python
# Good - one load/save cycle
editor = OdsEditor("budget.ods")
for expense in expenses:
    editor.append_expense(expense)
editor.save()

# Bad - many load/save cycles
for expense in expenses:
    append_expense_to_file("budget.ods", expense)
```
