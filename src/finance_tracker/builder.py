"""
Fluent builder API for spreadsheet construction.

Provides a declarative, chainable API for building spreadsheets:
- SpreadsheetBuilder: Main builder for creating sheets
- SheetBuilder: Builder for individual sheets
- FormulaBuilder: Type-safe formula construction
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from collections.abc import Sequence

    from finance_tracker.schema.styles import Theme


# ============================================================================
# Data Specifications
# ============================================================================


@dataclass
class CellSpec:
    """
    Specification for a single cell.

    Attributes:
        value: Cell value (string, number, date, etc.)
        formula: ODF formula string
        style: Style name from theme
        colspan: Number of columns to span
        rowspan: Number of rows to span
        value_type: ODF value type (string, currency, date, float, percentage)
    """

    value: Any = None
    formula: str | None = None
    style: str | None = None
    colspan: int = 1
    rowspan: int = 1
    value_type: str | None = None

    def is_empty(self) -> bool:
        """Check if cell has no content."""
        return self.value is None and self.formula is None


@dataclass
class RowSpec:
    """
    Specification for a row.

    Attributes:
        cells: List of cell specifications
        style: Default style for cells in this row
        height: Row height (optional)
    """

    cells: list[CellSpec] = field(default_factory=list)
    style: str | None = None
    height: str | None = None


@dataclass
class ColumnSpec:
    """
    Specification for a column.

    Attributes:
        name: Column header name
        width: Column width (e.g., "2.5cm")
        type: Value type (string, currency, date, percentage)
        style: Default style for cells in this column
    """

    name: str
    width: str = "2.5cm"
    type: str = "string"
    style: str | None = None


@dataclass
class SheetSpec:
    """
    Specification for a sheet.

    Attributes:
        name: Sheet name
        columns: Column specifications
        rows: Row specifications
    """

    name: str
    columns: list[ColumnSpec] = field(default_factory=list)
    rows: list[RowSpec] = field(default_factory=list)


# ============================================================================
# Formula Builder
# ============================================================================


@dataclass
class CellRef:
    """
    Cell reference for formulas.

    Attributes:
        ref: Cell reference (e.g., "A2")
        absolute_col: If True, column is absolute ($A)
        absolute_row: If True, row is absolute ($2)
    """

    ref: str
    absolute_col: bool = False
    absolute_row: bool = False

    def __str__(self) -> str:
        """Convert to ODF cell reference."""
        # Parse column and row from ref
        col = ""
        row = ""
        for i, c in enumerate(self.ref):
            if c.isalpha():
                col += c
            else:
                row = self.ref[i:]
                break

        # Build reference
        result = ""
        if self.absolute_col:
            result += f"${col}"
        else:
            result += col
        if self.absolute_row:
            result += f"${row}"
        else:
            result += row

        return result

    def absolute(self) -> CellRef:
        """Return absolute reference ($A$1)."""
        return CellRef(self.ref, absolute_col=True, absolute_row=True)

    def abs_col(self) -> CellRef:
        """Return reference with absolute column ($A1)."""
        return CellRef(self.ref, absolute_col=True, absolute_row=False)

    def abs_row(self) -> CellRef:
        """Return reference with absolute row (A$1)."""
        return CellRef(self.ref, absolute_col=False, absolute_row=True)


@dataclass
class RangeRef:
    """
    Range reference for formulas.

    Attributes:
        start: Start cell (e.g., "A2")
        end: End cell (e.g., "A100")
        sheet: Optional sheet name for cross-sheet references
    """

    start: str
    end: str
    sheet: str | None = None

    def __str__(self) -> str:
        """Convert to ODF range reference."""
        range_str = f"{self.start}:{self.end}"
        if self.sheet:
            # Quote sheet names that need it
            if " " in self.sheet or "'" in self.sheet:
                sheet_name = f"'{self.sheet}'"
            else:
                sheet_name = self.sheet
            return f"[{sheet_name}.${range_str}]"
        return f"[.{range_str}]"


@dataclass
class SheetRef:
    """
    Sheet reference for cross-sheet formulas.

    Attributes:
        name: Sheet name
    """

    name: str

    def col(self, col: str) -> RangeRef:
        """Reference to entire column."""
        return RangeRef(f"${col}", f"${col}", self.name)

    def range(self, start: str, end: str) -> RangeRef:
        """Range within this sheet."""
        return RangeRef(start, end, self.name)

    def cell(self, ref: str) -> str:
        """Cell reference within this sheet."""
        if " " in self.name or "'" in self.name:
            sheet_name = f"'{self.name}'"
        else:
            sheet_name = self.name
        return f"[{sheet_name}.{ref}]"


class FormulaBuilder:
    """
    Type-safe formula builder for ODF formulas.

    Provides methods for common spreadsheet functions with
    proper ODF syntax generation.

    Examples:
        f = FormulaBuilder()

        # Simple SUM
        formula = f.sum(f.range("A2", "A100"))
        # -> "of:=SUM([.A2:A100])"

        # Cross-sheet SUMIF
        formula = f.sumif(
            f.sheet("Expenses").col("B"),
            f.cell("A2"),
            f.sheet("Expenses").col("D"),
        )
        # -> "of:=SUMIF(['Expenses'.$B:$B];[.A2];['Expenses'.$D:$D])"

        # VLOOKUP
        formula = f.vlookup(
            f.cell("A2"),
            f.sheet("Budget").range("A:B", "A:B"),
            2,
            exact=True,
        )
    """

    # ODF formula prefix
    PREFIX = "of:="

    def cell(self, ref: str) -> CellRef:
        """Create cell reference."""
        return CellRef(ref)

    def range(self, start: str, end: str) -> RangeRef:
        """Create range reference (same sheet)."""
        return RangeRef(start, end)

    def sheet(self, name: str) -> SheetRef:
        """Create sheet reference for cross-sheet formulas."""
        return SheetRef(name)

    def _format_ref(self, ref: CellRef | RangeRef | str) -> str:
        """Format a reference for formula use."""
        if isinstance(ref, (str, CellRef)):
            return f"[.{ref}]"
        else:
            return str(ref)

    def sum(self, ref: RangeRef | str) -> str:
        """
        Create SUM formula.

        Args:
            ref: Range reference

        Returns:
            ODF formula string
        """
        return f"{self.PREFIX}SUM({self._format_ref(ref)})"

    def sumif(
        self,
        criteria_range: RangeRef | str,
        criteria: CellRef | str,
        sum_range: RangeRef | str,
    ) -> str:
        """
        Create SUMIF formula.

        Args:
            criteria_range: Range to check criteria against
            criteria: Criteria value or cell reference
            sum_range: Range to sum

        Returns:
            ODF formula string
        """
        cr = self._format_ref(criteria_range)
        crit = (
            self._format_ref(criteria)
            if isinstance(criteria, (CellRef, RangeRef))
            else f"[.{criteria}]"
        )
        sr = self._format_ref(sum_range)
        return f"{self.PREFIX}SUMIF({cr};{crit};{sr})"

    def vlookup(
        self,
        lookup_value: CellRef | str,
        table: RangeRef | str,
        col_index: int,
        *,
        exact: bool = True,
    ) -> str:
        """
        Create VLOOKUP formula.

        Args:
            lookup_value: Value to look up
            table: Table range
            col_index: Column to return (1-based)
            exact: If True, require exact match

        Returns:
            ODF formula string
        """
        val = (
            self._format_ref(lookup_value)
            if isinstance(lookup_value, CellRef)
            else f"[.{lookup_value}]"
        )
        tbl = self._format_ref(table)
        match = "0" if exact else "1"
        return f"{self.PREFIX}VLOOKUP({val};{tbl};{col_index};{match})"

    def if_expr(
        self,
        condition: str,
        true_value: str | CellRef,
        false_value: str | CellRef,
    ) -> str:
        """
        Create IF formula.

        Args:
            condition: Condition expression
            true_value: Value if true
            false_value: Value if false

        Returns:
            ODF formula string
        """
        tv = str(true_value) if isinstance(true_value, CellRef) else true_value
        fv = str(false_value) if isinstance(false_value, CellRef) else false_value
        return f"{self.PREFIX}IF({condition};{tv};{fv})"

    def subtract(self, cell1: str, cell2: str) -> str:
        """
        Create subtraction formula.

        Args:
            cell1: First cell reference
            cell2: Second cell reference

        Returns:
            ODF formula string
        """
        return f"{self.PREFIX}[.{cell1}]-[.{cell2}]"

    def divide(self, cell1: str, cell2: str, default: str = "0") -> str:
        """
        Create division formula with zero check.

        Args:
            cell1: Numerator cell
            cell2: Denominator cell
            default: Default value if denominator is zero

        Returns:
            ODF formula string
        """
        return f"{self.PREFIX}IF([.{cell2}]>0;[.{cell1}]/[.{cell2}];{default})"

    def average(self, ref: RangeRef | str) -> str:
        """Create AVERAGE formula."""
        return f"{self.PREFIX}AVERAGE({self._format_ref(ref)})"

    def count(self, ref: RangeRef | str) -> str:
        """Create COUNT formula."""
        return f"{self.PREFIX}COUNT({self._format_ref(ref)})"

    def counta(self, ref: RangeRef | str) -> str:
        """Create COUNTA formula (count non-empty)."""
        return f"{self.PREFIX}COUNTA({self._format_ref(ref)})"

    def max(self, ref: RangeRef | str) -> str:
        """Create MAX formula."""
        return f"{self.PREFIX}MAX({self._format_ref(ref)})"

    def min(self, ref: RangeRef | str) -> str:
        """Create MIN formula."""
        return f"{self.PREFIX}MIN({self._format_ref(ref)})"


# ============================================================================
# Spreadsheet Builder
# ============================================================================


class SpreadsheetBuilder:
    """
    Fluent builder for creating spreadsheets.

    Provides a chainable API for building multi-sheet spreadsheets
    with theme support.

    Examples:
        builder = SpreadsheetBuilder(theme="default")

        builder.sheet("Expenses") \\
            .column("Date", width="2.5cm", type="date") \\
            .column("Category", width="3cm") \\
            .column("Amount", width="2.5cm", type="currency") \\
            .header_row(style="header_primary") \\
            .data_rows(50)

        builder.sheet("Summary") \\
            .column("Category") \\
            .column("Budget") \\
            .column("Actual") \\
            .header_row() \\
            .row() \\
                .cell("Groceries") \\
                .cell(formula="=VLOOKUP(A2, Budget.A:B, 2, FALSE)") \\
                .cell(formula="=SUMIF(Expenses.B:B, A2, Expenses.C:C)")

        builder.save("budget.ods")
    """

    def __init__(
        self,
        theme: str | Theme | None = "default",
        theme_dir: Path | str | None = None,
    ) -> None:
        """
        Initialize builder with theme.

        Args:
            theme: Theme name, Theme object, or None for no theme
            theme_dir: Directory containing theme files
        """
        self._theme: Theme | None = None
        self._theme_name: str | None = None

        if theme is not None:
            if isinstance(theme, str):
                self._theme_name = theme
                # Lazy load theme when needed
            else:
                self._theme = theme

        self._theme_dir = Path(theme_dir) if theme_dir else None
        self._sheets: list[SheetSpec] = []
        self._current_sheet: SheetSpec | None = None
        self._current_row: RowSpec | None = None

    def _get_theme(self) -> Theme | None:
        """Get or load the theme."""
        if self._theme is None and self._theme_name is not None:
            from finance_tracker.schema.loader import ThemeLoader

            loader = ThemeLoader(self._theme_dir)
            self._theme = loader.load(self._theme_name)
        return self._theme

    def sheet(self, name: str) -> Self:
        """
        Start a new sheet.

        Args:
            name: Sheet name

        Returns:
            Self for chaining
        """
        self._current_sheet = SheetSpec(name=name)
        self._sheets.append(self._current_sheet)
        self._current_row = None
        return self

    def column(
        self,
        name: str,
        *,
        width: str = "2.5cm",
        type: str = "string",
        style: str | None = None,
    ) -> Self:
        """
        Add a column to current sheet.

        Args:
            name: Column header name
            width: Column width (e.g., "2.5cm", "100px")
            type: Value type (string, currency, date, percentage)
            style: Default style for cells

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected. Call .sheet() first.")

        self._current_sheet.columns.append(
            ColumnSpec(name=name, width=width, type=type, style=style)
        )
        return self

    def header_row(self, *, style: str = "header_primary") -> Self:
        """
        Add header row with column names.

        Args:
            style: Style for header cells

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected.")

        row = RowSpec(style=style)
        for col in self._current_sheet.columns:
            row.cells.append(CellSpec(value=col.name, style=style))

        self._current_sheet.rows.append(row)
        self._current_row = None
        return self

    def row(self, *, style: str | None = None) -> Self:
        """
        Start a new row.

        Args:
            style: Default style for cells in this row

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected.")

        self._current_row = RowSpec(style=style)
        self._current_sheet.rows.append(self._current_row)
        return self

    def cell(
        self,
        value: Any = None,
        *,
        formula: str | None = None,
        style: str | None = None,
        colspan: int = 1,
        rowspan: int = 1,
        value_type: str | None = None,
    ) -> Self:
        """
        Add a cell to current row.

        Args:
            value: Cell value
            formula: ODF formula
            style: Style name
            colspan: Columns to span
            rowspan: Rows to span
            value_type: ODF value type

        Returns:
            Self for chaining
        """
        if self._current_row is None:
            raise ValueError("No row selected. Call .row() first.")

        self._current_row.cells.append(
            CellSpec(
                value=value,
                formula=formula,
                style=style,
                colspan=colspan,
                rowspan=rowspan,
                value_type=value_type,
            )
        )
        return self

    def cells(self, *values: Any, style: str | None = None) -> Self:
        """
        Add multiple cells to current row.

        Args:
            *values: Cell values
            style: Style for all cells

        Returns:
            Self for chaining
        """
        if self._current_row is None:
            raise ValueError("No row selected. Call .row() first.")

        for value in values:
            self._current_row.cells.append(CellSpec(value=value, style=style))
        return self

    def data_rows(self, count: int, *, style: str | None = None) -> Self:
        """
        Add empty data entry rows.

        Args:
            count: Number of rows to add
            style: Style for empty cells

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected.")

        col_count = len(self._current_sheet.columns)
        for _ in range(count):
            row = RowSpec(style=style)
            row.cells = [CellSpec() for _ in range(col_count)]
            self._current_sheet.rows.append(row)

        self._current_row = None
        return self

    def formula_row(
        self,
        formulas: Sequence[str | None],
        *,
        style: str | None = None,
    ) -> Self:
        """
        Add a row with formulas.

        Args:
            formulas: List of formula strings (None for empty cells)
            style: Style for cells

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected.")

        row = RowSpec(style=style)
        for formula in formulas:
            row.cells.append(CellSpec(formula=formula, style=style))

        self._current_sheet.rows.append(row)
        self._current_row = None
        return self

    def build(self) -> list[SheetSpec]:
        """
        Return the built sheet specifications.

        Returns:
            List of SheetSpec objects
        """
        return self._sheets

    def save(self, path: Path | str) -> Path:
        """
        Generate and save the ODS file.

        Args:
            path: Output file path

        Returns:
            Path to saved file
        """
        from finance_tracker.renderer import OdsRenderer

        renderer = OdsRenderer(self._get_theme())
        return renderer.render(self._sheets, Path(path))


# ============================================================================
# Convenience Functions
# ============================================================================


def create_spreadsheet(theme: str = "default") -> SpreadsheetBuilder:
    """
    Create a new spreadsheet builder.

    Args:
        theme: Theme name to use

    Returns:
        SpreadsheetBuilder instance
    """
    return SpreadsheetBuilder(theme=theme)


def formula() -> FormulaBuilder:
    """
    Create a formula builder.

    Returns:
        FormulaBuilder instance
    """
    return FormulaBuilder()
