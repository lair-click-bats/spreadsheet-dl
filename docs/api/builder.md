# Builder API Reference

Complete API reference for the spreadsheet builder system.

**Implements:** DOC-PROF-001 (Complete API Reference)

## Overview

The Builder API provides a fluent, chainable interface for constructing spreadsheets programmatically. It consists of three main components:

- **SpreadsheetBuilder**: Main builder for creating multi-sheet workbooks
- **FormulaBuilder**: Type-safe formula construction with ODF syntax
- **ChartBuilder**: Fluent chart creation (from charts module)

## SpreadsheetBuilder

### Class: `SpreadsheetBuilder`

Fluent builder for creating spreadsheets with theme support.

```python
from spreadsheet_dl.builder import SpreadsheetBuilder, create_spreadsheet

# Using class directly
builder = SpreadsheetBuilder(theme="corporate")

# Using convenience function
builder = create_spreadsheet(theme="default")
```

#### Constructor

```python
SpreadsheetBuilder(
    theme: str | Theme | None = "default",
    theme_dir: Path | str | None = None
)
```

**Parameters:**
- `theme`: Theme name (string), Theme object, or None for no theme
- `theme_dir`: Directory containing theme YAML files

### Workbook Properties

#### `workbook_properties()`

Set workbook-level metadata.

```python
builder.workbook_properties(
    title: str | None = None,
    author: str | None = None,
    subject: str | None = None,
    description: str | None = None,
    keywords: list[str] | None = None,
    **custom: str
) -> Self
```

**Example:**
```python
builder.workbook_properties(
    title="Monthly Budget Report",
    author="Finance Team",
    subject="Q4 2024 Budget Analysis",
    keywords=["budget", "finance", "2024"],
    department="Finance",  # Custom property
)
```

#### `named_range()`

Define a named range for use in formulas.

```python
builder.named_range(
    name: str,
    start: str,
    end: str,
    sheet: str | None = None
) -> Self
```

**Example:**
```python
builder.named_range("BudgetData", "B2", "B50", sheet="Budget")
```

### Sheet Operations

#### `sheet()`

Start a new sheet.

```python
builder.sheet(name: str) -> Self
```

**Example:**
```python
builder.sheet("Summary")
```

#### `freeze()`

Freeze rows and/or columns for scrolling.

```python
builder.freeze(
    *,
    rows: int = 0,
    cols: int = 0
) -> Self
```

**Example:**
```python
builder.sheet("Data").freeze(rows=1)  # Freeze header row
```

#### `print_area()`

Set the print area for the current sheet.

```python
builder.print_area(range_ref: str) -> Self
```

**Example:**
```python
builder.print_area("A1:D50")
```

#### `protect()`

Enable sheet protection.

```python
builder.protect(
    *,
    password: str | None = None,
    edit_cells: bool = False,
    edit_objects: bool = False
) -> Self
```

**Example:**
```python
builder.protect(password="secret123", edit_cells=True)
```

### Column Operations

#### `column()`

Add a column to the current sheet.

```python
builder.column(
    name: str,
    *,
    width: str = "2.5cm",
    type: str = "string",
    style: str | None = None,
    validation: str | None = None,
    hidden: bool = False
) -> Self
```

**Parameters:**
- `name`: Column header name
- `width`: Column width (e.g., "2.5cm", "100pt", "100px")
- `type`: Value type (string, currency, date, percentage)
- `style`: Default style for cells in this column
- `validation`: Data validation reference
- `hidden`: Whether column is hidden

**Example:**
```python
builder.sheet("Budget") \
    .column("Category", width="150pt", style="text") \
    .column("Budget", width="100pt", type="currency") \
    .column("Actual", width="100pt", type="currency") \
    .column("Variance", width="100pt", type="currency")
```

### Row Operations

#### `header_row()`

Add a header row using column names.

```python
builder.header_row(*, style: str = "header_primary") -> Self
```

**Example:**
```python
builder.header_row(style="header")
```

#### `row()`

Start a new data row.

```python
builder.row(
    *,
    style: str | None = None,
    height: str | None = None
) -> Self
```

**Example:**
```python
builder.row(style="data", height="20pt")
```

#### `data_rows()`

Add multiple empty data entry rows with optional alternating styles.

```python
builder.data_rows(
    count: int,
    *,
    style: str | None = None,
    alternate_styles: list[str] | None = None
) -> Self
```

**Example:**
```python
# Zebra striping
builder.data_rows(20, alternate_styles=["row_even", "row_odd"])
```

#### `total_row()`

Add a total/summary row.

```python
builder.total_row(
    *,
    style: str | None = "total",
    values: Sequence[str | None] | None = None,
    formulas: Sequence[str | None] | None = None
) -> Self
```

**Example:**
```python
builder.total_row(
    style="total",
    formulas=["Total", "=SUM(B2:B21)", "=SUM(C2:C21)", "=B22-C22"]
)
```

#### `formula_row()`

Add a row with formulas.

```python
builder.formula_row(
    formulas: Sequence[str | None],
    *,
    style: str | None = None
) -> Self
```

### Cell Operations

#### `cell()`

Add a cell to the current row.

```python
builder.cell(
    value: Any = None,
    *,
    formula: str | None = None,
    style: str | None = None,
    colspan: int = 1,
    rowspan: int = 1,
    value_type: str | None = None
) -> Self
```

**Example:**
```python
builder.row() \
    .cell("Category Name", style="label") \
    .cell(1500.00, value_type="currency") \
    .cell(formula="=B2*0.1", style="calculated")
```

#### `cells()`

Add multiple cells to the current row.

```python
builder.cells(*values: Any, style: str | None = None) -> Self
```

**Example:**
```python
builder.row().cells("Jan", "Feb", "Mar", "Apr", style="header")
```

### Chart Operations

#### `chart()`

Add a chart to the current sheet.

```python
builder.chart(chart_spec: ChartSpec) -> Self
```

**Example:**
```python
from spreadsheet_dl.charts import ChartBuilder

chart = ChartBuilder() \
    .column_chart() \
    .title("Budget vs Actual") \
    .series("Budget", "B2:B13") \
    .series("Actual", "C2:C13") \
    .build()

builder.sheet("Summary").chart(chart)
```

### Build and Save

#### `build()`

Return the built sheet specifications.

```python
builder.build() -> list[SheetSpec]
```

#### `save()`

Generate and save the ODS file.

```python
builder.save(path: Path | str) -> Path
```

**Example:**
```python
output_path = builder.save("budget_report.ods")
print(f"Saved to: {output_path}")
```

---

## FormulaBuilder

### Class: `FormulaBuilder`

Type-safe formula builder for ODF formulas.

```python
from spreadsheet_dl.builder import FormulaBuilder, formula

# Using class directly
f = FormulaBuilder()

# Using convenience function
f = formula()
```

### Reference Creation

#### `cell()`

Create a cell reference.

```python
f.cell(ref: str) -> CellRef
```

**Example:**
```python
ref = f.cell("A1")
abs_ref = f.cell("A1").absolute()  # $A$1
```

#### `range()`

Create a range reference.

```python
f.range(start: str, end: str) -> RangeRef
```

**Example:**
```python
rng = f.range("A2", "A100")
```

#### `sheet()`

Create a sheet reference for cross-sheet formulas.

```python
f.sheet(name: str) -> SheetRef
```

**Example:**
```python
budget_sheet = f.sheet("Budget")
rng = budget_sheet.range("B2", "B50")
```

### Mathematical Functions

| Method | Formula | Example |
|--------|---------|---------|
| `sum(range)` | SUM | `f.sum(f.range("A1", "A10"))` |
| `sumif(cr, crit, sr)` | SUMIF | `f.sumif(f.range("A:A"), ">=100", f.range("B:B"))` |
| `abs(ref)` | ABS | `f.abs("A1")` |
| `round(ref, dec)` | ROUND | `f.round("A1", 2)` |
| `mod(num, div)` | MOD | `f.mod("A1", 12)` |
| `power(base, exp)` | POWER | `f.power("A1", 2)` |
| `sqrt(ref)` | SQRT | `f.sqrt("A1")` |

### Statistical Functions

| Method | Formula | Example |
|--------|---------|---------|
| `average(range)` | AVERAGE | `f.average(f.range("A1", "A10"))` |
| `count(range)` | COUNT | `f.count(f.range("A:A"))` |
| `counta(range)` | COUNTA | `f.counta(f.range("A:A"))` |
| `countif(cr, crit)` | COUNTIF | `f.countif(f.range("A:A"), ">0")` |
| `max(range)` | MAX | `f.max(f.range("A:A"))` |
| `min(range)` | MIN | `f.min(f.range("A:A"))` |
| `median(range)` | MEDIAN | `f.median(f.range("A:A"))` |
| `stdev(range)` | STDEV | `f.stdev(f.range("A:A"))` |

### Financial Functions

| Method | Formula | Description |
|--------|---------|-------------|
| `pmt(rate, nper, pv)` | PMT | Periodic payment |
| `pv(rate, nper, pmt)` | PV | Present value |
| `fv(rate, nper, pmt)` | FV | Future value |
| `npv(rate, values)` | NPV | Net present value |
| `irr(values, guess)` | IRR | Internal rate of return |
| `nper(rate, pmt, pv)` | NPER | Number of periods |
| `rate(nper, pmt, pv)` | RATE | Interest rate |

**Example:**
```python
# Monthly mortgage payment
payment = f.pmt(
    rate="B1/12",      # Annual rate / 12 months
    nper="B2*12",      # Years * 12 months
    pv="B3"            # Loan amount
)
# -> "of:=PMT([.B1]/12;[.B2]*12;[.B3];0;0)"
```

### Date/Time Functions

| Method | Formula | Example |
|--------|---------|---------|
| `today()` | TODAY | `f.today()` |
| `now()` | NOW | `f.now()` |
| `date(y, m, d)` | DATE | `f.date(2024, 12, 31)` |
| `year(ref)` | YEAR | `f.year("A1")` |
| `month(ref)` | MONTH | `f.month("A1")` |
| `day(ref)` | DAY | `f.day("A1")` |
| `eomonth(date, m)` | EOMONTH | `f.eomonth("A1", 1)` |
| `datedif(s, e, u)` | DATEDIF | `f.datedif("A1", "B1", "D")` |

### Lookup Functions

| Method | Formula | Example |
|--------|---------|---------|
| `vlookup(val, tbl, col)` | VLOOKUP | `f.vlookup("A1", f.range("D:F"), 2)` |
| `hlookup(val, tbl, row)` | HLOOKUP | `f.hlookup("A1", f.range("A1:Z1"), 2)` |
| `index(arr, row, col)` | INDEX | `f.index(f.range("A:C"), 5, 2)` |
| `match(val, arr, type)` | MATCH | `f.match("A1", f.range("B:B"), 0)` |
| `offset(ref, r, c, h, w)` | OFFSET | `f.offset("A1", 5, 2)` |
| `indirect(ref)` | INDIRECT | `f.indirect("A1")` |

**INDEX/MATCH Example:**
```python
# More flexible than VLOOKUP
lookup = f.index_match(
    f.range("C:C"),  # Return column
    f.match("A2", f.range("B:B"))
)
```

### Text Functions

| Method | Formula | Example |
|--------|---------|---------|
| `concatenate(*vals)` | CONCATENATE | `f.concatenate("A1", "B1")` |
| `text(val, fmt)` | TEXT | `f.text("A1", "0.00%")` |
| `left(txt, n)` | LEFT | `f.left("A1", 5)` |
| `right(txt, n)` | RIGHT | `f.right("A1", 3)` |
| `mid(txt, s, n)` | MID | `f.mid("A1", 2, 5)` |
| `len(txt)` | LEN | `f.len("A1")` |
| `trim(txt)` | TRIM | `f.trim("A1")` |
| `upper(txt)` | UPPER | `f.upper("A1")` |
| `lower(txt)` | LOWER | `f.lower("A1")` |
| `substitute(t, o, n)` | SUBSTITUTE | `f.substitute("A1", "x", "y")` |

### Logical Functions

| Method | Formula | Example |
|--------|---------|---------|
| `if_expr(cond, t, f)` | IF | `f.if_expr("[.A1]>0", "Positive", "Negative")` |
| `iferror(val, err)` | IFERROR | `f.iferror("A1/B1", 0)` |
| `and_expr(*conds)` | AND | `f.and_expr("[.A1]>0", "[.B1]>0")` |
| `or_expr(*conds)` | OR | `f.or_expr("[.A1]=1", "[.A1]=2")` |
| `not_expr(cond)` | NOT | `f.not_expr("[.A1]=0")` |
| `isblank(ref)` | ISBLANK | `f.isblank("A1")` |
| `iserror(ref)` | ISERROR | `f.iserror("A1")` |

### Array Formulas

#### `array()`

Wrap a formula as an array formula.

```python
f.array(formula: str) -> str
```

**Example:**
```python
arr_formula = f.array(f.sum(f.range("A1", "A10")))
# -> "of:={SUM([.A1:A10])}"
```

---

## Data Classes

### CellSpec

Specification for a single cell.

```python
@dataclass
class CellSpec:
    value: Any = None
    formula: str | None = None
    style: str | None = None
    colspan: int = 1
    rowspan: int = 1
    value_type: str | None = None
    validation: str | None = None
    conditional_format: str | None = None
```

### RowSpec

Specification for a row.

```python
@dataclass
class RowSpec:
    cells: list[CellSpec] = field(default_factory=list)
    style: str | None = None
    height: str | None = None
```

### ColumnSpec

Specification for a column.

```python
@dataclass
class ColumnSpec:
    name: str
    width: str = "2.5cm"
    type: str = "string"
    style: str | None = None
    validation: str | None = None
    hidden: bool = False
```

### SheetSpec

Specification for a sheet.

```python
@dataclass
class SheetSpec:
    name: str
    columns: list[ColumnSpec] = field(default_factory=list)
    rows: list[RowSpec] = field(default_factory=list)
    freeze_rows: int = 0
    freeze_cols: int = 0
    print_area: str | None = None
    protection: dict[str, Any] = field(default_factory=dict)
    conditional_formats: list[str] = field(default_factory=list)
    validations: list[str] = field(default_factory=list)
    charts: list[ChartSpec] = field(default_factory=list)
```

### WorkbookProperties

Workbook-level properties.

```python
@dataclass
class WorkbookProperties:
    title: str = ""
    author: str = ""
    subject: str = ""
    description: str = ""
    keywords: list[str] = field(default_factory=list)
    created: str | None = None
    modified: str | None = None
    custom: dict[str, str] = field(default_factory=dict)
```

---

## Complete Example

```python
from spreadsheet_dl.builder import SpreadsheetBuilder, formula
from spreadsheet_dl.charts import ChartBuilder

# Create builder with theme
builder = SpreadsheetBuilder(theme="professional")

# Set workbook properties
builder.workbook_properties(
    title="Monthly Budget Report",
    author="Finance Team",
    keywords=["budget", "monthly", "2024"],
)

# Create Budget sheet
builder.sheet("Budget") \
    .column("Category", width="150pt") \
    .column("Budget", width="100pt", type="currency") \
    .column("Actual", width="100pt", type="currency") \
    .column("Variance", width="100pt", type="currency") \
    .freeze(rows=1) \
    .header_row(style="header") \
    .data_rows(15, alternate_styles=["row_even", "row_odd"]) \
    .total_row(
        formulas=[
            "Total",
            "=SUM(B2:B16)",
            "=SUM(C2:C16)",
            "=B17-C17"
        ]
    )

# Add chart
chart = ChartBuilder() \
    .column_chart() \
    .title("Budget vs Actual") \
    .categories("Budget.A2:A16") \
    .series("Budget", "Budget.B2:B16", color="#4472C4") \
    .series("Actual", "Budget.C2:C16", color="#ED7D31") \
    .legend(position="bottom") \
    .position("F2") \
    .size(450, 300) \
    .build()

builder.chart(chart)

# Save
builder.save("budget_report.ods")
```
