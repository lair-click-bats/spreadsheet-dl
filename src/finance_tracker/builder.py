"""
Fluent builder API for spreadsheet construction.

Implements:
    - FR-BUILDER-001: Extended SpreadsheetBuilder
    - FR-BUILDER-004: ChartBuilder (via charts module)
    - FR-BUILDER-005: Formula Builder Enhancement

Provides a declarative, chainable API for building spreadsheets:
- SpreadsheetBuilder: Main builder for creating sheets
- SheetBuilder: Builder for individual sheets
- FormulaBuilder: Type-safe formula construction
- ChartBuilder: Fluent chart creation (from charts module)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from collections.abc import Sequence

    from finance_tracker.charts import ChartSpec
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
        validation: Data validation reference
        conditional_format: Conditional format reference
    """

    value: Any = None
    formula: str | None = None
    style: str | None = None
    colspan: int = 1
    rowspan: int = 1
    value_type: str | None = None
    validation: str | None = None
    conditional_format: str | None = None

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
        validation: Data validation reference
        hidden: Whether column is hidden
        sparkline: Optional sparkline specification
    """

    name: str
    width: str = "2.5cm"
    type: str = "string"
    style: str | None = None
    validation: str | None = None
    hidden: bool = False
    sparkline: Any = None  # Sparkline from charts module


@dataclass
class SheetSpec:
    """
    Specification for a sheet.

    Implements FR-BUILDER-001: Extended sheet properties

    Attributes:
        name: Sheet name
        columns: Column specifications
        rows: Row specifications
        freeze_rows: Number of rows to freeze
        freeze_cols: Number of columns to freeze
        print_area: Print area range
        protection: Sheet protection settings
        conditional_formats: List of conditional format references
        validations: List of validation references
        charts: List of chart specifications (FR-BUILDER-004)
    """

    name: str
    columns: list[ColumnSpec] = field(default_factory=list)
    rows: list[RowSpec] = field(default_factory=list)
    freeze_rows: int = 0
    freeze_cols: int = 0
    print_area: str | None = None
    protection: dict[str, Any] = field(default_factory=dict)
    conditional_formats: list[str] = field(default_factory=list)
    validations: list[str] = field(default_factory=list)
    charts: list[Any] = field(default_factory=list)  # List of ChartSpec


@dataclass
class WorkbookProperties:
    """
    Workbook-level properties.

    Implements FR-BUILDER-001: Workbook-level properties

    Attributes:
        title: Document title
        author: Document author
        subject: Document subject
        description: Document description
        keywords: Document keywords
        created: Creation date
        modified: Last modified date
        custom: Custom properties
    """

    title: str = ""
    author: str = ""
    subject: str = ""
    description: str = ""
    keywords: list[str] = field(default_factory=list)
    created: str | None = None
    modified: str | None = None
    custom: dict[str, str] = field(default_factory=dict)


# ============================================================================
# Formula Builder (FR-BUILDER-005)
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
class NamedRange:
    """
    Named range for use in formulas.

    Implements FR-BUILDER-005: Named range support

    Attributes:
        name: Range name
        range: The range reference
        scope: Scope ("workbook" or sheet name)
    """

    name: str
    range: RangeRef
    scope: str = "workbook"


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

    Implements FR-BUILDER-005: Formula Builder Enhancement

    Provides methods for common spreadsheet functions with
    proper ODF syntax generation, including:
    - Mathematical functions
    - Statistical functions
    - Financial functions (PMT, PV, FV, NPV, IRR)
    - Date/time functions
    - Lookup functions (VLOOKUP, HLOOKUP, INDEX, MATCH)
    - Text functions
    - Array formula support

    Examples:
        f = FormulaBuilder()

        # Simple SUM
        formula = f.sum(f.range("A2", "A100"))
        # -> "of:=SUM([.A2:A100])"

        # Financial: Monthly payment
        formula = f.pmt(f.cell("B1"), f.cell("B2"), f.cell("B3"))
        # -> "of:=PMT([.B1];[.B2];[.B3])"

        # Lookup
        formula = f.index_match(
            f.range("B:B", "B:B"),
            f.match(f.cell("A2"), f.range("A:A", "A:A")),
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

    def _format_value(self, val: CellRef | RangeRef | str | float | int) -> str:
        """Format a value (reference or literal) for formula use."""
        if isinstance(val, (CellRef, RangeRef)):
            return self._format_ref(val)
        elif isinstance(val, str) and (val[0].isalpha() or val[0] == "$"):
            # Looks like a cell reference
            return f"[.{val}]"
        else:
            return str(val)

    # =========================================================================
    # Mathematical Functions
    # =========================================================================

    def sum(self, ref: RangeRef | str) -> str:
        """Create SUM formula."""
        return f"{self.PREFIX}SUM({self._format_ref(ref)})"

    def sumif(
        self,
        criteria_range: RangeRef | str,
        criteria: CellRef | str,
        sum_range: RangeRef | str,
    ) -> str:
        """Create SUMIF formula."""
        cr = self._format_ref(criteria_range)
        crit = self._format_value(criteria)
        sr = self._format_ref(sum_range)
        return f"{self.PREFIX}SUMIF({cr};{crit};{sr})"

    def sumifs(
        self,
        sum_range: RangeRef | str,
        *criteria_pairs: tuple[RangeRef | str, CellRef | str],
    ) -> str:
        """
        Create SUMIFS formula (multiple criteria).

        Args:
            sum_range: Range to sum
            criteria_pairs: Pairs of (criteria_range, criteria)

        Returns:
            ODF formula string
        """
        sr = self._format_ref(sum_range)
        parts = [sr]
        for criteria_range, criteria in criteria_pairs:
            parts.append(self._format_ref(criteria_range))
            parts.append(self._format_value(criteria))
        return f"{self.PREFIX}SUMIFS({';'.join(parts)})"

    def subtract(self, cell1: str, cell2: str) -> str:
        """Create subtraction formula."""
        return f"{self.PREFIX}[.{cell1}]-[.{cell2}]"

    def multiply(self, cell1: str, cell2: str) -> str:
        """Create multiplication formula."""
        return f"{self.PREFIX}[.{cell1}]*[.{cell2}]"

    def divide(self, cell1: str, cell2: str, default: str = "0") -> str:
        """Create division formula with zero check."""
        return f"{self.PREFIX}IF([.{cell2}]<>0;[.{cell1}]/[.{cell2}];{default})"

    def abs(self, ref: CellRef | str) -> str:
        """Create ABS formula."""
        return f"{self.PREFIX}ABS({self._format_value(ref)})"

    def round(self, ref: CellRef | str, decimals: int = 0) -> str:
        """Create ROUND formula."""
        return f"{self.PREFIX}ROUND({self._format_value(ref)};{decimals})"

    def roundup(self, ref: CellRef | str, decimals: int = 0) -> str:
        """Create ROUNDUP formula."""
        return f"{self.PREFIX}ROUNDUP({self._format_value(ref)};{decimals})"

    def rounddown(self, ref: CellRef | str, decimals: int = 0) -> str:
        """Create ROUNDDOWN formula."""
        return f"{self.PREFIX}ROUNDDOWN({self._format_value(ref)};{decimals})"

    def mod(self, number: CellRef | str, divisor: CellRef | str | int) -> str:
        """Create MOD formula."""
        return f"{self.PREFIX}MOD({self._format_value(number)};{self._format_value(divisor)})"

    def power(self, base: CellRef | str, exponent: CellRef | str | float) -> str:
        """Create POWER formula."""
        return f"{self.PREFIX}POWER({self._format_value(base)};{self._format_value(exponent)})"

    def sqrt(self, ref: CellRef | str) -> str:
        """Create SQRT formula."""
        return f"{self.PREFIX}SQRT({self._format_value(ref)})"

    # =========================================================================
    # Statistical Functions
    # =========================================================================

    def average(self, ref: RangeRef | str) -> str:
        """Create AVERAGE formula."""
        return f"{self.PREFIX}AVERAGE({self._format_ref(ref)})"

    def averageif(
        self,
        criteria_range: RangeRef | str,
        criteria: CellRef | str,
        average_range: RangeRef | str | None = None,
    ) -> str:
        """Create AVERAGEIF formula."""
        cr = self._format_ref(criteria_range)
        crit = self._format_value(criteria)
        if average_range:
            ar = self._format_ref(average_range)
            return f"{self.PREFIX}AVERAGEIF({cr};{crit};{ar})"
        return f"{self.PREFIX}AVERAGEIF({cr};{crit})"

    def count(self, ref: RangeRef | str) -> str:
        """Create COUNT formula (count numbers)."""
        return f"{self.PREFIX}COUNT({self._format_ref(ref)})"

    def counta(self, ref: RangeRef | str) -> str:
        """Create COUNTA formula (count non-empty)."""
        return f"{self.PREFIX}COUNTA({self._format_ref(ref)})"

    def countblank(self, ref: RangeRef | str) -> str:
        """Create COUNTBLANK formula."""
        return f"{self.PREFIX}COUNTBLANK({self._format_ref(ref)})"

    def countif(
        self,
        criteria_range: RangeRef | str,
        criteria: CellRef | str,
    ) -> str:
        """Create COUNTIF formula."""
        cr = self._format_ref(criteria_range)
        crit = self._format_value(criteria)
        return f"{self.PREFIX}COUNTIF({cr};{crit})"

    def countifs(
        self,
        *criteria_pairs: tuple[RangeRef | str, CellRef | str],
    ) -> str:
        """Create COUNTIFS formula (multiple criteria)."""
        parts = []
        for criteria_range, criteria in criteria_pairs:
            parts.append(self._format_ref(criteria_range))
            parts.append(self._format_value(criteria))
        return f"{self.PREFIX}COUNTIFS({';'.join(parts)})"

    def max(self, ref: RangeRef | str) -> str:
        """Create MAX formula."""
        return f"{self.PREFIX}MAX({self._format_ref(ref)})"

    def min(self, ref: RangeRef | str) -> str:
        """Create MIN formula."""
        return f"{self.PREFIX}MIN({self._format_ref(ref)})"

    def median(self, ref: RangeRef | str) -> str:
        """Create MEDIAN formula."""
        return f"{self.PREFIX}MEDIAN({self._format_ref(ref)})"

    def stdev(self, ref: RangeRef | str) -> str:
        """Create STDEV formula (sample standard deviation)."""
        return f"{self.PREFIX}STDEV({self._format_ref(ref)})"

    def stdevp(self, ref: RangeRef | str) -> str:
        """Create STDEVP formula (population standard deviation)."""
        return f"{self.PREFIX}STDEVP({self._format_ref(ref)})"

    def var(self, ref: RangeRef | str) -> str:
        """Create VAR formula (sample variance)."""
        return f"{self.PREFIX}VAR({self._format_ref(ref)})"

    def percentile(self, ref: RangeRef | str, k: float) -> str:
        """Create PERCENTILE formula."""
        return f"{self.PREFIX}PERCENTILE({self._format_ref(ref)};{k})"

    # =========================================================================
    # Financial Functions (FR-BUILDER-005)
    # =========================================================================

    def pmt(
        self,
        rate: CellRef | str | float,
        nper: CellRef | str | int,
        pv: CellRef | str | float,
        fv: CellRef | str | float = 0,
        payment_type: int = 0,
    ) -> str:
        """
        Create PMT formula (periodic payment).

        Args:
            rate: Interest rate per period
            nper: Total number of payment periods
            pv: Present value (loan amount)
            fv: Future value (default 0)
            payment_type: 0=end of period, 1=beginning

        Returns:
            ODF formula string
        """
        return f"{self.PREFIX}PMT({self._format_value(rate)};{self._format_value(nper)};{self._format_value(pv)};{self._format_value(fv)};{payment_type})"

    def pv(
        self,
        rate: CellRef | str | float,
        nper: CellRef | str | int,
        pmt: CellRef | str | float,
        fv: CellRef | str | float = 0,
        payment_type: int = 0,
    ) -> str:
        """
        Create PV formula (present value).

        Args:
            rate: Interest rate per period
            nper: Total number of payment periods
            pmt: Payment per period
            fv: Future value (default 0)
            payment_type: 0=end of period, 1=beginning

        Returns:
            ODF formula string
        """
        return f"{self.PREFIX}PV({self._format_value(rate)};{self._format_value(nper)};{self._format_value(pmt)};{self._format_value(fv)};{payment_type})"

    def fv(
        self,
        rate: CellRef | str | float,
        nper: CellRef | str | int,
        pmt: CellRef | str | float,
        pv: CellRef | str | float = 0,
        payment_type: int = 0,
    ) -> str:
        """
        Create FV formula (future value).

        Args:
            rate: Interest rate per period
            nper: Total number of payment periods
            pmt: Payment per period
            pv: Present value (default 0)
            payment_type: 0=end of period, 1=beginning

        Returns:
            ODF formula string
        """
        return f"{self.PREFIX}FV({self._format_value(rate)};{self._format_value(nper)};{self._format_value(pmt)};{self._format_value(pv)};{payment_type})"

    def npv(
        self,
        rate: CellRef | str | float,
        values: RangeRef | str,
    ) -> str:
        """
        Create NPV formula (net present value).

        Args:
            rate: Discount rate
            values: Range of cash flow values

        Returns:
            ODF formula string
        """
        return f"{self.PREFIX}NPV({self._format_value(rate)};{self._format_ref(values)})"

    def irr(
        self,
        values: RangeRef | str,
        guess: float = 0.1,
    ) -> str:
        """
        Create IRR formula (internal rate of return).

        Args:
            values: Range of cash flow values
            guess: Initial guess (default 0.1 = 10%)

        Returns:
            ODF formula string
        """
        return f"{self.PREFIX}IRR({self._format_ref(values)};{guess})"

    def nper(
        self,
        rate: CellRef | str | float,
        pmt: CellRef | str | float,
        pv: CellRef | str | float,
        fv: CellRef | str | float = 0,
        payment_type: int = 0,
    ) -> str:
        """
        Create NPER formula (number of periods).

        Args:
            rate: Interest rate per period
            pmt: Payment per period
            pv: Present value
            fv: Future value (default 0)
            payment_type: 0=end of period, 1=beginning

        Returns:
            ODF formula string
        """
        return f"{self.PREFIX}NPER({self._format_value(rate)};{self._format_value(pmt)};{self._format_value(pv)};{self._format_value(fv)};{payment_type})"

    def rate(
        self,
        nper: CellRef | str | int,
        pmt: CellRef | str | float,
        pv: CellRef | str | float,
        fv: CellRef | str | float = 0,
        payment_type: int = 0,
        guess: float = 0.1,
    ) -> str:
        """
        Create RATE formula (interest rate per period).

        Args:
            nper: Number of periods
            pmt: Payment per period
            pv: Present value
            fv: Future value (default 0)
            payment_type: 0=end of period, 1=beginning
            guess: Initial guess (default 0.1)

        Returns:
            ODF formula string
        """
        return f"{self.PREFIX}RATE({self._format_value(nper)};{self._format_value(pmt)};{self._format_value(pv)};{self._format_value(fv)};{payment_type};{guess})"

    # =========================================================================
    # Date/Time Functions (FR-BUILDER-005)
    # =========================================================================

    def today(self) -> str:
        """Create TODAY formula."""
        return f"{self.PREFIX}TODAY()"

    def now(self) -> str:
        """Create NOW formula."""
        return f"{self.PREFIX}NOW()"

    def date(
        self,
        year: CellRef | str | int,
        month: CellRef | str | int,
        day: CellRef | str | int,
    ) -> str:
        """Create DATE formula."""
        return f"{self.PREFIX}DATE({self._format_value(year)};{self._format_value(month)};{self._format_value(day)})"

    def year(self, ref: CellRef | str) -> str:
        """Create YEAR formula."""
        return f"{self.PREFIX}YEAR({self._format_value(ref)})"

    def month(self, ref: CellRef | str) -> str:
        """Create MONTH formula."""
        return f"{self.PREFIX}MONTH({self._format_value(ref)})"

    def day(self, ref: CellRef | str) -> str:
        """Create DAY formula."""
        return f"{self.PREFIX}DAY({self._format_value(ref)})"

    def weekday(self, ref: CellRef | str, type: int = 1) -> str:
        """Create WEEKDAY formula (1=Sunday-Saturday, 2=Monday-Sunday)."""
        return f"{self.PREFIX}WEEKDAY({self._format_value(ref)};{type})"

    def weeknum(self, ref: CellRef | str, type: int = 1) -> str:
        """Create WEEKNUM formula."""
        return f"{self.PREFIX}WEEKNUM({self._format_value(ref)};{type})"

    def eomonth(self, start_date: CellRef | str, months: CellRef | str | int) -> str:
        """Create EOMONTH formula (end of month)."""
        return f"{self.PREFIX}EOMONTH({self._format_value(start_date)};{self._format_value(months)})"

    def datedif(
        self,
        start_date: CellRef | str,
        end_date: CellRef | str,
        unit: str = "D",
    ) -> str:
        """
        Create DATEDIF formula.

        Args:
            start_date: Start date
            end_date: End date
            unit: "Y", "M", "D", "YM", "MD", "YD"

        Returns:
            ODF formula string
        """
        return f'{self.PREFIX}DATEDIF({self._format_value(start_date)};{self._format_value(end_date)};"{unit}")'

    # =========================================================================
    # Lookup Functions (FR-BUILDER-005)
    # =========================================================================

    def vlookup(
        self,
        lookup_value: CellRef | str,
        table: RangeRef | str,
        col_index: int,
        *,
        exact: bool = True,
    ) -> str:
        """Create VLOOKUP formula."""
        val = self._format_value(lookup_value)
        tbl = self._format_ref(table)
        match = "0" if exact else "1"
        return f"{self.PREFIX}VLOOKUP({val};{tbl};{col_index};{match})"

    def hlookup(
        self,
        lookup_value: CellRef | str,
        table: RangeRef | str,
        row_index: int,
        *,
        exact: bool = True,
    ) -> str:
        """Create HLOOKUP formula."""
        val = self._format_value(lookup_value)
        tbl = self._format_ref(table)
        match = "0" if exact else "1"
        return f"{self.PREFIX}HLOOKUP({val};{tbl};{row_index};{match})"

    def index(
        self,
        array: RangeRef | str,
        row_num: CellRef | str | int,
        col_num: CellRef | str | int | None = None,
    ) -> str:
        """Create INDEX formula."""
        arr = self._format_ref(array)
        row = self._format_value(row_num)
        if col_num is not None:
            col = self._format_value(col_num)
            return f"{self.PREFIX}INDEX({arr};{row};{col})"
        return f"{self.PREFIX}INDEX({arr};{row})"

    def match(
        self,
        lookup_value: CellRef | str,
        lookup_array: RangeRef | str,
        match_type: int = 0,
    ) -> str:
        """
        Create MATCH formula.

        Args:
            lookup_value: Value to find
            lookup_array: Range to search
            match_type: 0=exact, 1=less than, -1=greater than

        Returns:
            ODF formula string
        """
        val = self._format_value(lookup_value)
        arr = self._format_ref(lookup_array)
        return f"{self.PREFIX}MATCH({val};{arr};{match_type})"

    def index_match(
        self,
        return_range: RangeRef | str,
        match_formula: str,
    ) -> str:
        """
        Create INDEX/MATCH combination.

        Args:
            return_range: Range to return value from
            match_formula: MATCH formula (without prefix)

        Returns:
            ODF formula string
        """
        # Strip prefix from match_formula if present
        if match_formula.startswith(self.PREFIX):
            match_formula = match_formula[len(self.PREFIX):]
        return f"{self.PREFIX}INDEX({self._format_ref(return_range)};{match_formula})"

    def offset(
        self,
        reference: CellRef | str,
        rows: CellRef | str | int,
        cols: CellRef | str | int,
        height: CellRef | str | int | None = None,
        width: CellRef | str | int | None = None,
    ) -> str:
        """Create OFFSET formula."""
        ref = self._format_value(reference)
        r = self._format_value(rows)
        c = self._format_value(cols)
        parts = [ref, r, c]
        if height is not None:
            parts.append(self._format_value(height))
            if width is not None:
                parts.append(self._format_value(width))
        return f"{self.PREFIX}OFFSET({';'.join(parts)})"

    def indirect(self, ref_text: CellRef | str) -> str:
        """Create INDIRECT formula."""
        return f"{self.PREFIX}INDIRECT({self._format_value(ref_text)})"

    # =========================================================================
    # Text Functions (FR-BUILDER-005)
    # =========================================================================

    def concatenate(self, *values: CellRef | str) -> str:
        """Create CONCATENATE formula."""
        parts = [self._format_value(v) for v in values]
        return f"{self.PREFIX}CONCATENATE({';'.join(parts)})"

    def concat(self, *values: CellRef | str) -> str:
        """Create CONCAT formula (alias for CONCATENATE)."""
        return self.concatenate(*values)

    def text(self, value: CellRef | str, format_text: str) -> str:
        """Create TEXT formula."""
        return f'{self.PREFIX}TEXT({self._format_value(value)};"{format_text}")'

    def left(self, text: CellRef | str, num_chars: int = 1) -> str:
        """Create LEFT formula."""
        return f"{self.PREFIX}LEFT({self._format_value(text)};{num_chars})"

    def right(self, text: CellRef | str, num_chars: int = 1) -> str:
        """Create RIGHT formula."""
        return f"{self.PREFIX}RIGHT({self._format_value(text)};{num_chars})"

    def mid(self, text: CellRef | str, start_num: int, num_chars: int) -> str:
        """Create MID formula."""
        return f"{self.PREFIX}MID({self._format_value(text)};{start_num};{num_chars})"

    def len(self, text: CellRef | str) -> str:
        """Create LEN formula."""
        return f"{self.PREFIX}LEN({self._format_value(text)})"

    def trim(self, text: CellRef | str) -> str:
        """Create TRIM formula."""
        return f"{self.PREFIX}TRIM({self._format_value(text)})"

    def upper(self, text: CellRef | str) -> str:
        """Create UPPER formula."""
        return f"{self.PREFIX}UPPER({self._format_value(text)})"

    def lower(self, text: CellRef | str) -> str:
        """Create LOWER formula."""
        return f"{self.PREFIX}LOWER({self._format_value(text)})"

    def proper(self, text: CellRef | str) -> str:
        """Create PROPER formula (title case)."""
        return f"{self.PREFIX}PROPER({self._format_value(text)})"

    def find(self, find_text: str, within_text: CellRef | str, start_num: int = 1) -> str:
        """Create FIND formula (case-sensitive)."""
        return f'{self.PREFIX}FIND("{find_text}";{self._format_value(within_text)};{start_num})'

    def search(self, find_text: str, within_text: CellRef | str, start_num: int = 1) -> str:
        """Create SEARCH formula (case-insensitive)."""
        return f'{self.PREFIX}SEARCH("{find_text}";{self._format_value(within_text)};{start_num})'

    def substitute(
        self,
        text: CellRef | str,
        old_text: str,
        new_text: str,
        instance_num: int | None = None,
    ) -> str:
        """Create SUBSTITUTE formula."""
        parts = [self._format_value(text), f'"{old_text}"', f'"{new_text}"']
        if instance_num is not None:
            parts.append(str(instance_num))
        return f"{self.PREFIX}SUBSTITUTE({';'.join(parts)})"

    # =========================================================================
    # Logical Functions
    # =========================================================================

    def if_expr(
        self,
        condition: str,
        true_value: str | CellRef,
        false_value: str | CellRef,
    ) -> str:
        """Create IF formula."""
        tv = str(true_value) if isinstance(true_value, CellRef) else true_value
        fv = str(false_value) if isinstance(false_value, CellRef) else false_value
        return f"{self.PREFIX}IF({condition};{tv};{fv})"

    def iferror(
        self,
        value: CellRef | str,
        value_if_error: CellRef | str | float | int,
    ) -> str:
        """Create IFERROR formula."""
        return f"{self.PREFIX}IFERROR({self._format_value(value)};{self._format_value(value_if_error)})"

    def ifna(
        self,
        value: CellRef | str,
        value_if_na: CellRef | str | float | int,
    ) -> str:
        """Create IFNA formula."""
        return f"{self.PREFIX}IFNA({self._format_value(value)};{self._format_value(value_if_na)})"

    def and_expr(self, *conditions: str) -> str:
        """Create AND formula."""
        return f"{self.PREFIX}AND({';'.join(conditions)})"

    def or_expr(self, *conditions: str) -> str:
        """Create OR formula."""
        return f"{self.PREFIX}OR({';'.join(conditions)})"

    def not_expr(self, condition: str) -> str:
        """Create NOT formula."""
        return f"{self.PREFIX}NOT({condition})"

    def isblank(self, ref: CellRef | str) -> str:
        """Create ISBLANK formula."""
        return f"{self.PREFIX}ISBLANK({self._format_value(ref)})"

    def iserror(self, ref: CellRef | str) -> str:
        """Create ISERROR formula."""
        return f"{self.PREFIX}ISERROR({self._format_value(ref)})"

    def isnumber(self, ref: CellRef | str) -> str:
        """Create ISNUMBER formula."""
        return f"{self.PREFIX}ISNUMBER({self._format_value(ref)})"

    def istext(self, ref: CellRef | str) -> str:
        """Create ISTEXT formula."""
        return f"{self.PREFIX}ISTEXT({self._format_value(ref)})"

    # =========================================================================
    # Array Formulas (FR-BUILDER-005)
    # =========================================================================

    def array(self, formula: str) -> str:
        """
        Wrap formula as array formula.

        Note: In ODF, array formulas need special handling during rendering.

        Args:
            formula: Formula to wrap

        Returns:
            Array formula string
        """
        # Remove existing prefix if present
        if formula.startswith(self.PREFIX):
            formula = formula[len(self.PREFIX):]
        return f"{self.PREFIX}{{{formula}}}"


# ============================================================================
# Spreadsheet Builder (FR-BUILDER-001)
# ============================================================================


class SpreadsheetBuilder:
    """
    Fluent builder for creating spreadsheets.

    Implements FR-BUILDER-001: Extended SpreadsheetBuilder

    Provides a chainable API for building multi-sheet spreadsheets
    with theme support, including:
    - Workbook-level properties
    - Sheet freezing and protection
    - Alternating row styles
    - Total row formulas
    - Conditional formats and validations
    - Charts (FR-BUILDER-004)

    Examples:
        builder = SpreadsheetBuilder(theme="corporate")

        builder.workbook_properties(
            title="Monthly Budget",
            author="Finance Team",
        )

        builder.sheet("Budget") \\
            .column("Category", width="150pt", style="text") \\
            .column("Budget", width="100pt", type="currency") \\
            .column("Actual", width="100pt", type="currency") \\
            .freeze(rows=1) \\
            .header_row(style="header") \\
            .data_rows(20, alternate_styles=["row_even", "row_odd"]) \\
            .total_row(style="total", formulas=["Total", "=SUM(B2:B21)", "=SUM(C2:C21)"])

        # Add a chart
        from finance_tracker.charts import ChartBuilder
        chart = ChartBuilder() \\
            .column_chart() \\
            .title("Budget vs Actual") \\
            .series("Budget", "Budget.B2:B21") \\
            .series("Actual", "Budget.C2:C21") \\
            .build()
        builder.chart(chart)

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
            else:
                self._theme = theme

        self._theme_dir = Path(theme_dir) if theme_dir else None
        self._sheets: list[SheetSpec] = []
        self._current_sheet: SheetSpec | None = None
        self._current_row: RowSpec | None = None
        self._workbook_properties = WorkbookProperties()
        self._named_ranges: list[NamedRange] = []

    def _get_theme(self) -> Theme | None:
        """Get or load the theme."""
        if self._theme is None and self._theme_name is not None:
            from finance_tracker.schema.loader import ThemeLoader

            loader = ThemeLoader(self._theme_dir)
            self._theme = loader.load(self._theme_name)
        return self._theme

    # =========================================================================
    # Workbook-Level Properties (FR-BUILDER-001)
    # =========================================================================

    def workbook_properties(
        self,
        *,
        title: str | None = None,
        author: str | None = None,
        subject: str | None = None,
        description: str | None = None,
        keywords: list[str] | None = None,
        **custom: str,
    ) -> Self:
        """
        Set workbook-level properties.

        Args:
            title: Document title
            author: Document author
            subject: Document subject
            description: Document description
            keywords: Document keywords
            **custom: Custom properties

        Returns:
            Self for chaining
        """
        if title:
            self._workbook_properties.title = title
        if author:
            self._workbook_properties.author = author
        if subject:
            self._workbook_properties.subject = subject
        if description:
            self._workbook_properties.description = description
        if keywords:
            self._workbook_properties.keywords = keywords
        for key, value in custom.items():
            self._workbook_properties.custom[key] = value
        return self

    def named_range(
        self,
        name: str,
        start: str,
        end: str,
        sheet: str | None = None,
    ) -> Self:
        """
        Define a named range.

        Args:
            name: Range name
            start: Start cell reference
            end: End cell reference
            sheet: Sheet name (None for current sheet)

        Returns:
            Self for chaining
        """
        sheet_name = sheet or (self._current_sheet.name if self._current_sheet else None)
        self._named_ranges.append(
            NamedRange(
                name=name,
                range=RangeRef(start, end, sheet_name),
                scope="workbook" if sheet is None else sheet_name or "workbook",
            )
        )
        return self

    # =========================================================================
    # Sheet Operations
    # =========================================================================

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

    def freeze(self, *, rows: int = 0, cols: int = 0) -> Self:
        """
        Freeze rows and/or columns.

        Args:
            rows: Number of rows to freeze
            cols: Number of columns to freeze

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected. Call .sheet() first.")
        self._current_sheet.freeze_rows = rows
        self._current_sheet.freeze_cols = cols
        return self

    def print_area(self, range_ref: str) -> Self:
        """
        Set print area.

        Args:
            range_ref: Range reference (e.g., "A1:D50")

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected.")
        self._current_sheet.print_area = range_ref
        return self

    def protect(
        self,
        *,
        password: str | None = None,
        edit_cells: bool = False,
        edit_objects: bool = False,
    ) -> Self:
        """
        Enable sheet protection.

        Args:
            password: Protection password
            edit_cells: Allow editing unlocked cells
            edit_objects: Allow editing objects

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected.")
        self._current_sheet.protection = {
            "enabled": True,
            "password": password,
            "edit_cells": edit_cells,
            "edit_objects": edit_objects,
        }
        return self

    # =========================================================================
    # Column Operations
    # =========================================================================

    def column(
        self,
        name: str,
        *,
        width: str = "2.5cm",
        type: str = "string",
        style: str | None = None,
        validation: str | None = None,
        hidden: bool = False,
    ) -> Self:
        """
        Add a column to current sheet.

        Args:
            name: Column header name
            width: Column width (e.g., "2.5cm", "100px", "100pt")
            type: Value type (string, currency, date, percentage)
            style: Default style for cells
            validation: Data validation reference
            hidden: Whether column is hidden

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected. Call .sheet() first.")

        self._current_sheet.columns.append(
            ColumnSpec(
                name=name,
                width=width,
                type=type,
                style=style,
                validation=validation,
                hidden=hidden,
            )
        )
        return self

    # =========================================================================
    # Row Operations
    # =========================================================================

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

    def row(self, *, style: str | None = None, height: str | None = None) -> Self:
        """
        Start a new row.

        Args:
            style: Default style for cells in this row
            height: Row height (e.g., "20pt")

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected.")

        self._current_row = RowSpec(style=style, height=height)
        self._current_sheet.rows.append(self._current_row)
        return self

    def data_rows(
        self,
        count: int,
        *,
        style: str | None = None,
        alternate_styles: list[str] | None = None,
    ) -> Self:
        """
        Add empty data entry rows with optional alternating styles.

        Args:
            count: Number of rows to add
            style: Style for cells (used if alternate_styles not provided)
            alternate_styles: List of styles to alternate (e.g., ["row_even", "row_odd"])

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected.")

        col_count = len(self._current_sheet.columns)
        for i in range(count):
            # Determine row style
            if alternate_styles:
                row_style = alternate_styles[i % len(alternate_styles)]
            else:
                row_style = style

            row = RowSpec(style=row_style)
            row.cells = [CellSpec(style=row_style) for _ in range(col_count)]
            self._current_sheet.rows.append(row)

        self._current_row = None
        return self

    def total_row(
        self,
        *,
        style: str | None = "total",
        values: Sequence[str | None] | None = None,
        formulas: Sequence[str | None] | None = None,
    ) -> Self:
        """
        Add a total/summary row.

        Args:
            style: Style for total row cells
            values: List of static values (None for empty)
            formulas: List of formula strings (None for empty)

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected.")

        row = RowSpec(style=style)

        if values:
            for value in values:
                row.cells.append(CellSpec(value=value, style=style))
        elif formulas:
            for formula in formulas:
                if formula and not formula.startswith("=") and not formula.startswith("of:"):
                    # Treat as value, not formula
                    row.cells.append(CellSpec(value=formula, style=style))
                else:
                    row.cells.append(CellSpec(formula=formula, style=style))
        else:
            # Empty total row
            col_count = len(self._current_sheet.columns)
            row.cells = [CellSpec(style=style) for _ in range(col_count)]

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

    # =========================================================================
    # Cell Operations
    # =========================================================================

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

    # =========================================================================
    # Conditional Format and Validation
    # =========================================================================

    def conditional_format(self, format_ref: str) -> Self:
        """
        Add a conditional format reference to current sheet.

        Args:
            format_ref: Conditional format reference name

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected.")
        self._current_sheet.conditional_formats.append(format_ref)
        return self

    def validation(self, validation_ref: str) -> Self:
        """
        Add a data validation reference to current sheet.

        Args:
            validation_ref: Validation reference name

        Returns:
            Self for chaining
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected.")
        self._current_sheet.validations.append(validation_ref)
        return self

    # =========================================================================
    # Charts (FR-BUILDER-004)
    # =========================================================================

    def chart(self, chart_spec: ChartSpec) -> Self:
        """
        Add a chart to current sheet.

        Args:
            chart_spec: ChartSpec from ChartBuilder.build()

        Returns:
            Self for chaining

        Examples:
            from finance_tracker.charts import ChartBuilder

            chart = ChartBuilder() \\
                .column_chart() \\
                .title("Budget vs Actual") \\
                .series("Budget", "B2:B20") \\
                .series("Actual", "C2:C20") \\
                .build()

            builder.sheet("Summary").chart(chart)
        """
        if self._current_sheet is None:
            raise ValueError("No sheet selected.")
        self._current_sheet.charts.append(chart_spec)
        return self

    # =========================================================================
    # Build and Save
    # =========================================================================

    def build(self) -> list[SheetSpec]:
        """
        Return the built sheet specifications.

        Returns:
            List of SheetSpec objects
        """
        return self._sheets

    def get_properties(self) -> WorkbookProperties:
        """
        Get workbook properties.

        Returns:
            WorkbookProperties object
        """
        return self._workbook_properties

    def get_named_ranges(self) -> list[NamedRange]:
        """
        Get named ranges.

        Returns:
            List of NamedRange objects
        """
        return self._named_ranges

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
