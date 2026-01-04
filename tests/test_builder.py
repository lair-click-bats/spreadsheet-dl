"""Tests for builder module - SpreadsheetBuilder and FormulaBuilder."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import pytest

from spreadsheet_dl.builder import (
    CellRef,
    CellSpec,
    ColumnSpec,
    FormulaBuilder,
    FormulaDependencyGraph,
    NamedRange,
    NoRowSelectedError,
    NoSheetSelectedError,
    RangeRef,
    RowSpec,
    SheetRef,
    SheetSpec,
    SpreadsheetBuilder,
    WorkbookProperties,
    create_spreadsheet,
    formula,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestCellRef:
    """Tests for CellRef class."""

    def test_basic_ref(self) -> None:
        """Test basic cell reference."""
        ref = CellRef("A1")
        assert str(ref) == "A1"

    def test_absolute_ref(self) -> None:
        """Test absolute cell reference."""
        ref = CellRef("A1").absolute()
        assert str(ref) == "$A$1"

    def test_abs_col(self) -> None:
        """Test absolute column reference."""
        ref = CellRef("A1").abs_col()
        assert str(ref) == "$A1"

    def test_abs_row(self) -> None:
        """Test absolute row reference."""
        ref = CellRef("A1").abs_row()
        assert str(ref) == "A$1"

    def test_ref_with_multiple_letters(self) -> None:
        """Test cell reference with multi-letter column."""
        ref = CellRef("AA100")
        assert str(ref) == "AA100"

    def test_absolute_ref_multi_letter(self) -> None:
        """Test absolute reference with multi-letter column."""
        ref = CellRef("AB25").absolute()
        assert str(ref) == "$AB$25"

    def test_abs_col_multi_letter(self) -> None:
        """Test absolute column with multi-letter column."""
        ref = CellRef("ZZ999").abs_col()
        assert str(ref) == "$ZZ999"

    def test_abs_row_large_number(self) -> None:
        """Test absolute row with large row number."""
        ref = CellRef("B100000").abs_row()
        assert str(ref) == "B$100000"

    def test_cell_ref_equality(self) -> None:
        """Test CellRef equality based on string representation."""
        ref1 = CellRef("A1")
        ref2 = CellRef("A1")
        assert str(ref1) == str(ref2)

    def test_cell_ref_no_row_number(self) -> None:
        """Test CellRef with only letters (edge case, lines 199-207)."""
        # This tests the edge case where ref has only letters
        ref = CellRef("ABC")
        # The loop will consume all letters, leaving row empty
        result = str(ref)
        # Should output just the column letters since row is empty
        assert "ABC" in result


class TestRangeRef:
    """Tests for RangeRef class."""

    def test_basic_range(self) -> None:
        """Test basic range reference."""
        ref = RangeRef("A1", "A10")
        assert str(ref) == "[.A1:A10]"

    def test_range_with_sheet(self) -> None:
        """Test range with sheet reference."""
        ref = RangeRef("A1", "A10", "Expenses")
        assert str(ref) == "[Expenses.$A1:A10]"

    def test_range_with_space_in_sheet(self) -> None:
        """Test range with space in sheet name."""
        ref = RangeRef("A1", "A10", "Expense Log")
        assert str(ref) == "['Expense Log'.$A1:A10]"

    def test_range_with_quote_in_sheet(self) -> None:
        """Test range with quote in sheet name."""
        ref = RangeRef("A1", "B10", "John's Data")
        assert "'" in str(ref)

    def test_range_large_area(self) -> None:
        """Test range covering large area."""
        ref = RangeRef("A1", "ZZ1000")
        assert str(ref) == "[.A1:ZZ1000]"

    def test_range_single_column(self) -> None:
        """Test range for entire column."""
        ref = RangeRef("A:A", "A:A")
        assert "A:A" in str(ref)


class TestSheetRef:
    """Tests for SheetRef class."""

    def test_col_reference(self) -> None:
        """Test column reference from sheet."""
        sheet = SheetRef("Expenses")
        ref = sheet.col("B")
        assert ref.start == "$B"
        assert ref.sheet == "Expenses"

    def test_range_reference(self) -> None:
        """Test range reference from sheet."""
        sheet = SheetRef("Expenses")
        ref = sheet.range("A1", "B10")
        assert ref.start == "A1"
        assert ref.end == "B10"
        assert ref.sheet == "Expenses"

    def test_cell_reference(self) -> None:
        """Test cell reference from sheet."""
        sheet = SheetRef("Expenses")
        ref = sheet.cell("A2")
        assert ref == "[Expenses.A2]"

    def test_cell_reference_with_space(self) -> None:
        """Test cell reference with space in sheet name."""
        sheet = SheetRef("My Sheet")
        ref = sheet.cell("B5")
        assert "'" in ref

    def test_cell_reference_with_quote(self) -> None:
        """Test cell reference with quote in sheet name."""
        sheet = SheetRef("John's Sheet")
        ref = sheet.cell("C10")
        assert "'" in ref


class TestNamedRange:
    """Tests for NamedRange class."""

    def test_basic_named_range(self) -> None:
        """Test basic named range."""
        nr = NamedRange(
            name="MyRange",
            range=RangeRef("A1", "B10", "Data"),
        )
        assert nr.name == "MyRange"
        assert nr.scope == "workbook"

    def test_named_range_sheet_scope(self) -> None:
        """Test named range with sheet scope."""
        nr = NamedRange(
            name="LocalRange",
            range=RangeRef("A1", "A10"),
            scope="Sheet1",
        )
        assert nr.scope == "Sheet1"


class TestWorkbookProperties:
    """Tests for WorkbookProperties class."""

    def test_default_properties(self) -> None:
        """Test default workbook properties."""
        props = WorkbookProperties()
        assert props.title == ""
        assert props.author == ""
        assert props.subject == ""
        assert props.description == ""
        assert props.keywords == []
        assert props.created is None
        assert props.modified is None
        assert props.custom == {}

    def test_custom_properties(self) -> None:
        """Test custom workbook properties."""
        props = WorkbookProperties(
            title="My Budget",
            author="John Doe",
            subject="Finance",
            description="Personal budget tracker",
            keywords=["budget", "finance", "tracking"],
        )
        assert props.title == "My Budget"
        assert props.author == "John Doe"
        assert len(props.keywords) == 3


class TestFormulaBuilder:
    """Tests for FormulaBuilder class."""

    def test_sum_formula(self) -> None:
        """Test SUM formula generation."""
        f = FormulaBuilder()
        formula_str = f.sum(f.range("A2", "A100"))
        assert formula_str == "of:=SUM([.A2:A100])"

    def test_sumif_formula(self) -> None:
        """Test SUMIF formula generation."""
        f = FormulaBuilder()
        formula_str = f.sumif(
            f.sheet("Expenses").col("B"),
            f.cell("A2"),
            f.sheet("Expenses").col("D"),
        )
        assert "SUMIF" in formula_str
        assert "Expenses" in formula_str

    def test_sumifs_formula(self) -> None:
        """Test SUMIFS formula generation."""
        f = FormulaBuilder()
        formula_str = f.sumifs(
            f.range("D2", "D100"),
            (f.range("A2", "A100"), f.cell("E1")),
            (f.range("B2", "B100"), f.cell("F1")),
        )
        assert "SUMIFS" in formula_str

    def test_vlookup_formula(self) -> None:
        """Test VLOOKUP formula generation."""
        f = FormulaBuilder()
        formula_str = f.vlookup(
            f.cell("A2"),
            f.range("A1", "B10"),
            2,
            exact=True,
        )
        assert "VLOOKUP" in formula_str
        assert "2" in formula_str
        assert "0" in formula_str  # exact match

    def test_vlookup_approximate(self) -> None:
        """Test VLOOKUP with approximate match."""
        f = FormulaBuilder()
        formula_str = f.vlookup(
            f.cell("A2"),
            f.range("A1", "B10"),
            2,
            exact=False,
        )
        assert "1" in formula_str  # approximate match

    def test_hlookup_formula(self) -> None:
        """Test HLOOKUP formula generation."""
        f = FormulaBuilder()
        formula_str = f.hlookup(
            f.cell("A1"),
            f.range("A1", "Z10"),
            5,
            exact=True,
        )
        assert "HLOOKUP" in formula_str

    def test_index_formula(self) -> None:
        """Test INDEX formula generation."""
        f = FormulaBuilder()
        formula_str = f.index(f.range("A1", "D10"), 2, 3)
        assert "INDEX" in formula_str

    def test_match_formula(self) -> None:
        """Test MATCH formula generation."""
        f = FormulaBuilder()
        formula_str = f.match(f.cell("A1"), f.range("B1", "B100"))
        assert "MATCH" in formula_str

    def test_index_match_formula(self) -> None:
        """Test INDEX/MATCH combination."""
        f = FormulaBuilder()
        formula_str = f.index_match(
            f.range("B1", "B100"),
            f.match(f.cell("A1"), f.range("A1", "A100")),
        )
        assert "INDEX" in formula_str
        assert "MATCH" in formula_str

    def test_if_formula(self) -> None:
        """Test IF formula generation."""
        f = FormulaBuilder()
        formula_str = f.if_expr("[.B2]>0", '"Yes"', '"No"')
        assert formula_str == 'of:=IF([.B2]>0;"Yes";"No")'

    def test_subtract_formula(self) -> None:
        """Test subtraction formula."""
        f = FormulaBuilder()
        formula_str = f.subtract("B2", "C2")
        assert formula_str == "of:=[.B2]-[.C2]"

    def test_multiply_formula(self) -> None:
        """Test multiplication formula."""
        f = FormulaBuilder()
        formula_str = f.multiply("B2", "C2")
        assert "*" in formula_str

    def test_divide_formula(self) -> None:
        """Test division formula with zero check."""
        f = FormulaBuilder()
        formula_str = f.divide("B2", "C2")
        assert "IF" in formula_str
        assert ">0" in formula_str or "<>0" in formula_str

    def test_average_formula(self) -> None:
        """Test AVERAGE formula."""
        f = FormulaBuilder()
        formula_str = f.average(f.range("A1", "A10"))
        assert formula_str == "of:=AVERAGE([.A1:A10])"

    def test_averageif_formula(self) -> None:
        """Test AVERAGEIF formula."""
        f = FormulaBuilder()
        formula_str = f.averageif(
            f.range("A1", "A100"),
            ">0",
            f.range("B1", "B100"),
        )
        assert "AVERAGEIF" in formula_str

    def test_averageif_no_average_range(self) -> None:
        """Test AVERAGEIF without separate average range."""
        f = FormulaBuilder()
        formula_str = f.averageif(
            f.range("A1", "A100"),
            ">0",
        )
        assert "AVERAGEIF" in formula_str

    def test_count_formula(self) -> None:
        """Test COUNT formula."""
        f = FormulaBuilder()
        formula_str = f.count(f.range("A1", "A10"))
        assert formula_str == "of:=COUNT([.A1:A10])"

    def test_counta_formula(self) -> None:
        """Test COUNTA formula."""
        f = FormulaBuilder()
        formula_str = f.counta(f.range("A1", "A10"))
        assert formula_str == "of:=COUNTA([.A1:A10])"

    def test_countblank_formula(self) -> None:
        """Test COUNTBLANK formula."""
        f = FormulaBuilder()
        formula_str = f.countblank(f.range("A1", "A10"))
        assert "COUNTBLANK" in formula_str

    def test_countif_formula(self) -> None:
        """Test COUNTIF formula."""
        f = FormulaBuilder()
        formula_str = f.countif(f.range("A1", "A100"), ">50")
        assert "COUNTIF" in formula_str

    def test_countifs_formula(self) -> None:
        """Test COUNTIFS formula."""
        f = FormulaBuilder()
        formula_str = f.countifs(
            (f.range("A1", "A100"), ">0"),
            (f.range("B1", "B100"), "<100"),
        )
        assert "COUNTIFS" in formula_str

    def test_max_formula(self) -> None:
        """Test MAX formula."""
        f = FormulaBuilder()
        formula_str = f.max(f.range("A1", "A10"))
        assert formula_str == "of:=MAX([.A1:A10])"

    def test_min_formula(self) -> None:
        """Test MIN formula."""
        f = FormulaBuilder()
        formula_str = f.min(f.range("A1", "A10"))
        assert formula_str == "of:=MIN([.A1:A10])"

    def test_median_formula(self) -> None:
        """Test MEDIAN formula."""
        f = FormulaBuilder()
        formula_str = f.median(f.range("A1", "A100"))
        assert "MEDIAN" in formula_str

    def test_stdev_formula(self) -> None:
        """Test STDEV formula."""
        f = FormulaBuilder()
        formula_str = f.stdev(f.range("A1", "A100"))
        assert "STDEV" in formula_str

    def test_stdevp_formula(self) -> None:
        """Test STDEVP formula."""
        f = FormulaBuilder()
        formula_str = f.stdevp(f.range("A1", "A100"))
        assert "STDEVP" in formula_str

    def test_var_formula(self) -> None:
        """Test VAR formula."""
        f = FormulaBuilder()
        formula_str = f.var(f.range("A1", "A100"))
        assert "VAR" in formula_str

    def test_percentile_formula(self) -> None:
        """Test PERCENTILE formula."""
        f = FormulaBuilder()
        formula_str = f.percentile(f.range("A1", "A100"), 0.9)
        assert "PERCENTILE" in formula_str

    def test_abs_formula(self) -> None:
        """Test ABS formula."""
        f = FormulaBuilder()
        formula_str = f.abs(f.cell("A1"))
        assert "ABS" in formula_str

    def test_round_formula(self) -> None:
        """Test ROUND formula."""
        f = FormulaBuilder()
        formula_str = f.round(f.cell("A1"), 2)
        assert "ROUND" in formula_str

    def test_roundup_formula(self) -> None:
        """Test ROUNDUP formula."""
        f = FormulaBuilder()
        formula_str = f.roundup(f.cell("A1"), 0)
        assert "ROUNDUP" in formula_str

    def test_rounddown_formula(self) -> None:
        """Test ROUNDDOWN formula."""
        f = FormulaBuilder()
        formula_str = f.rounddown(f.cell("A1"), 0)
        assert "ROUNDDOWN" in formula_str

    def test_mod_formula(self) -> None:
        """Test MOD formula."""
        f = FormulaBuilder()
        formula_str = f.mod(f.cell("A1"), 3)
        assert "MOD" in formula_str

    def test_power_formula(self) -> None:
        """Test POWER formula."""
        f = FormulaBuilder()
        formula_str = f.power(f.cell("A1"), 2)
        assert "POWER" in formula_str

    def test_sqrt_formula(self) -> None:
        """Test SQRT formula."""
        f = FormulaBuilder()
        formula_str = f.sqrt(f.cell("A1"))
        assert "SQRT" in formula_str

    def test_named_range_formula(self) -> None:
        """Test named range in formula."""
        f = FormulaBuilder()
        ref = f.named_range("MyRange")
        assert ref == "[MyRange]"


class TestFormulaBuilderFinancial:
    """Tests for FormulaBuilder financial functions."""

    def test_pmt_formula(self) -> None:
        """Test PMT formula."""
        f = FormulaBuilder()
        formula_str = f.pmt(0.05 / 12, 360, -200000)
        assert "PMT" in formula_str

    def test_pmt_formula_with_cells(self) -> None:
        """Test PMT formula with cell references."""
        f = FormulaBuilder()
        formula_str = f.pmt(f.cell("B1"), f.cell("B2"), f.cell("B3"))
        assert "PMT" in formula_str

    def test_pv_formula(self) -> None:
        """Test PV formula."""
        f = FormulaBuilder()
        formula_str = f.pv(0.05, 10, -1000)
        assert "PV" in formula_str

    def test_fv_formula(self) -> None:
        """Test FV formula."""
        f = FormulaBuilder()
        formula_str = f.fv(0.05 / 12, 120, -100, -1000)
        assert "FV" in formula_str

    def test_npv_formula(self) -> None:
        """Test NPV formula."""
        f = FormulaBuilder()
        formula_str = f.npv(0.1, f.range("A1", "A10"))
        assert "NPV" in formula_str

    def test_irr_formula(self) -> None:
        """Test IRR formula."""
        f = FormulaBuilder()
        formula_str = f.irr(f.range("A1", "A10"))
        assert "IRR" in formula_str

    def test_nper_formula(self) -> None:
        """Test NPER formula."""
        f = FormulaBuilder()
        formula_str = f.nper(0.05 / 12, -500, 10000)
        assert "NPER" in formula_str

    def test_rate_formula(self) -> None:
        """Test RATE formula."""
        f = FormulaBuilder()
        formula_str = f.rate(120, -500, 50000)
        assert "RATE" in formula_str


class TestFormulaBuilderDateTimeFunctions:
    """Tests for FormulaBuilder date/time functions."""

    def test_today_formula(self) -> None:
        """Test TODAY formula."""
        f = FormulaBuilder()
        formula_str = f.today()
        assert formula_str == "of:=TODAY()"

    def test_now_formula(self) -> None:
        """Test NOW formula."""
        f = FormulaBuilder()
        formula_str = f.now()
        assert formula_str == "of:=NOW()"

    def test_date_formula(self) -> None:
        """Test DATE formula."""
        f = FormulaBuilder()
        formula_str = f.date(2025, 1, 15)
        assert "DATE" in formula_str

    def test_year_formula(self) -> None:
        """Test YEAR formula."""
        f = FormulaBuilder()
        formula_str = f.year(f.cell("A1"))
        assert "YEAR" in formula_str

    def test_month_formula(self) -> None:
        """Test MONTH formula."""
        f = FormulaBuilder()
        formula_str = f.month(f.cell("A1"))
        assert "MONTH" in formula_str

    def test_day_formula(self) -> None:
        """Test DAY formula."""
        f = FormulaBuilder()
        formula_str = f.day(f.cell("A1"))
        assert "DAY" in formula_str

    def test_edate_formula(self) -> None:
        """Test EDATE formula."""
        f = FormulaBuilder()
        formula_str = f.edate(f.cell("A1"), 3)
        assert "EDATE" in formula_str
        assert "[.A1]" in formula_str
        assert ";3" in formula_str

    def test_eomonth_formula(self) -> None:
        """Test EOMONTH formula."""
        f = FormulaBuilder()
        formula_str = f.eomonth(f.cell("A1"), 0)
        assert "EOMONTH" in formula_str

    def test_datedif_formula(self) -> None:
        """Test DATEDIF formula."""
        f = FormulaBuilder()
        formula_str = f.datedif(f.cell("A1"), f.cell("B1"), "M")
        assert "DATEDIF" in formula_str


class TestFormulaBuilderTextFunctions:
    """Tests for FormulaBuilder text functions."""

    def test_concatenate_formula(self) -> None:
        """Test CONCATENATE formula."""
        f = FormulaBuilder()
        formula_str = f.concatenate(f.cell("A1"), '" "', f.cell("B1"))
        assert "CONCATENATE" in formula_str

    def test_left_formula(self) -> None:
        """Test LEFT formula."""
        f = FormulaBuilder()
        formula_str = f.left(f.cell("A1"), 5)
        assert "LEFT" in formula_str

    def test_right_formula(self) -> None:
        """Test RIGHT formula."""
        f = FormulaBuilder()
        formula_str = f.right(f.cell("A1"), 5)
        assert "RIGHT" in formula_str

    def test_mid_formula(self) -> None:
        """Test MID formula."""
        f = FormulaBuilder()
        formula_str = f.mid(f.cell("A1"), 2, 5)
        assert "MID" in formula_str

    def test_len_formula(self) -> None:
        """Test LEN formula."""
        f = FormulaBuilder()
        formula_str = f.len(f.cell("A1"))
        assert "LEN" in formula_str

    def test_trim_formula(self) -> None:
        """Test TRIM formula."""
        f = FormulaBuilder()
        formula_str = f.trim(f.cell("A1"))
        assert "TRIM" in formula_str

    def test_upper_formula(self) -> None:
        """Test UPPER formula."""
        f = FormulaBuilder()
        formula_str = f.upper(f.cell("A1"))
        assert "UPPER" in formula_str

    def test_lower_formula(self) -> None:
        """Test LOWER formula."""
        f = FormulaBuilder()
        formula_str = f.lower(f.cell("A1"))
        assert "LOWER" in formula_str

    def test_proper_formula(self) -> None:
        """Test PROPER formula."""
        f = FormulaBuilder()
        formula_str = f.proper(f.cell("A1"))
        assert "PROPER" in formula_str

    def test_text_formula(self) -> None:
        """Test TEXT formula."""
        f = FormulaBuilder()
        formula_str = f.text(f.cell("A1"), '"$#,##0.00"')
        assert "TEXT" in formula_str


class TestFormulaBuilderLogicalFunctions:
    """Tests for FormulaBuilder logical functions."""

    def test_and_formula(self) -> None:
        """Test AND formula."""
        f = FormulaBuilder()
        formula_str = f.and_expr("[.A1]>0", "[.B1]<100")
        assert "AND" in formula_str

    def test_or_formula(self) -> None:
        """Test OR formula."""
        f = FormulaBuilder()
        formula_str = f.or_expr("[.A1]>0", "[.B1]>0")
        assert "OR" in formula_str

    def test_not_formula(self) -> None:
        """Test NOT formula."""
        f = FormulaBuilder()
        formula_str = f.not_expr("[.A1]=0")
        assert "NOT" in formula_str

    def test_iferror_formula(self) -> None:
        """Test IFERROR formula."""
        f = FormulaBuilder()
        formula_str = f.iferror(f.divide("A1", "B1"), "0")
        assert "IFERROR" in formula_str

    def test_isblank_formula(self) -> None:
        """Test ISBLANK formula."""
        f = FormulaBuilder()
        formula_str = f.isblank(f.cell("A1"))
        assert "ISBLANK" in formula_str


class TestCellSpec:
    """Tests for CellSpec class."""

    def test_empty_cell(self) -> None:
        """Test empty cell specification."""
        cell = CellSpec()
        assert cell.is_empty()

    def test_cell_with_value(self) -> None:
        """Test cell with value."""
        cell = CellSpec(value="Hello")
        assert not cell.is_empty()
        assert cell.value == "Hello"

    def test_cell_with_formula(self) -> None:
        """Test cell with formula."""
        cell = CellSpec(formula="of:=SUM([.A1:A10])")
        assert not cell.is_empty()
        assert cell.formula == "of:=SUM([.A1:A10])"

    def test_cell_with_style(self) -> None:
        """Test cell with style."""
        cell = CellSpec(value="Styled", style="header")
        assert cell.style == "header"

    def test_cell_with_colspan(self) -> None:
        """Test cell with column span."""
        cell = CellSpec(value="Merged", colspan=3)
        assert cell.colspan == 3

    def test_cell_with_rowspan(self) -> None:
        """Test cell with row span."""
        cell = CellSpec(value="Merged", rowspan=2)
        assert cell.rowspan == 2

    def test_cell_with_value_type(self) -> None:
        """Test cell with explicit value type."""
        cell = CellSpec(value=100, value_type="currency")
        assert cell.value_type == "currency"

    def test_cell_with_validation(self) -> None:
        """Test cell with validation reference."""
        cell = CellSpec(value="", validation="list_validation")
        assert cell.validation == "list_validation"

    def test_cell_with_decimal_value(self) -> None:
        """Test cell with Decimal value."""
        cell = CellSpec(value=Decimal("123.45"))
        assert cell.value == Decimal("123.45")


class TestColumnSpec:
    """Tests for ColumnSpec class."""

    def test_default_column(self) -> None:
        """Test default column specification."""
        col = ColumnSpec(name="Amount")
        assert col.name == "Amount"
        assert col.width == "2.5cm"
        assert col.type == "string"

    def test_currency_column(self) -> None:
        """Test currency column specification."""
        col = ColumnSpec(name="Amount", type="currency", width="3cm")
        assert col.type == "currency"
        assert col.width == "3cm"

    def test_date_column(self) -> None:
        """Test date column specification."""
        col = ColumnSpec(name="Date", type="date", width="2.5cm")
        assert col.type == "date"

    def test_percentage_column(self) -> None:
        """Test percentage column specification."""
        col = ColumnSpec(name="Rate", type="percentage")
        assert col.type == "percentage"

    def test_hidden_column(self) -> None:
        """Test hidden column specification."""
        col = ColumnSpec(name="ID", hidden=True)
        assert col.hidden is True

    def test_column_with_validation(self) -> None:
        """Test column with validation reference."""
        col = ColumnSpec(name="Category", validation="category_list")
        assert col.validation == "category_list"


class TestRowSpec:
    """Tests for RowSpec class."""

    def test_empty_row(self) -> None:
        """Test empty row specification."""
        row = RowSpec()
        assert len(row.cells) == 0

    def test_row_with_cells(self) -> None:
        """Test row with cells."""
        row = RowSpec(cells=[CellSpec(value="A"), CellSpec(value="B")])
        assert len(row.cells) == 2

    def test_row_with_style(self) -> None:
        """Test row with style."""
        row = RowSpec(style="header")
        assert row.style == "header"

    def test_row_with_height(self) -> None:
        """Test row with custom height."""
        row = RowSpec(height="1cm")
        assert row.height == "1cm"


class TestSheetSpec:
    """Tests for SheetSpec class."""

    def test_empty_sheet(self) -> None:
        """Test empty sheet specification."""
        sheet = SheetSpec(name="Test")
        assert sheet.name == "Test"
        assert len(sheet.columns) == 0
        assert len(sheet.rows) == 0

    def test_sheet_with_freeze(self) -> None:
        """Test sheet with frozen rows/columns."""
        sheet = SheetSpec(name="Test", freeze_rows=1, freeze_cols=2)
        assert sheet.freeze_rows == 1
        assert sheet.freeze_cols == 2

    def test_sheet_with_print_area(self) -> None:
        """Test sheet with print area."""
        sheet = SheetSpec(name="Test", print_area="A1:D50")
        assert sheet.print_area == "A1:D50"

    def test_sheet_with_protection(self) -> None:
        """Test sheet with protection settings."""
        sheet = SheetSpec(
            name="Test",
            protection={"protected": True, "password": "secret"},
        )
        assert sheet.protection["protected"] is True


class TestSpreadsheetBuilder:
    """Tests for SpreadsheetBuilder class."""

    def test_create_builder_no_theme(self) -> None:
        """Test creating builder without theme."""
        builder = SpreadsheetBuilder(theme=None)
        assert builder._theme is None

    def test_create_builder_with_theme_name(self) -> None:
        """Test creating builder with theme name."""
        builder = SpreadsheetBuilder(theme="default")
        assert builder._theme_name == "default"

    def test_create_builder_with_theme_object(self) -> None:
        """Test creating builder with Theme object (line 1106)."""
        from spreadsheet_dl.schema.styles import Theme, ThemeSchema

        meta = ThemeSchema(name="test", version="1.0")
        theme = Theme(meta=meta)
        builder = SpreadsheetBuilder(theme=theme)
        assert builder._theme is theme
        assert builder._theme_name is None

    def test_get_theme_loads_theme(self, tmp_path: Path) -> None:
        """Test _get_theme loads theme from theme_name (lines 1118-1121)."""
        # Create a builder with theme name
        builder = SpreadsheetBuilder(theme="default")
        # First call should load the theme
        theme = builder._get_theme()
        assert theme is not None
        # Second call should return cached theme
        theme2 = builder._get_theme()
        assert theme2 is theme

    def test_get_theme_returns_none_for_no_theme(self) -> None:
        """Test _get_theme returns None when no theme."""
        builder = SpreadsheetBuilder(theme=None)
        theme = builder._get_theme()
        assert theme is None

    def test_add_sheet(self) -> None:
        """Test adding a sheet."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test Sheet")
        assert len(builder._sheets) == 1
        assert builder._sheets[0].name == "Test Sheet"

    def test_add_multiple_sheets(self) -> None:
        """Test adding multiple sheets."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Sheet1").sheet("Sheet2").sheet("Sheet3")
        assert len(builder._sheets) == 3

    def test_add_column(self) -> None:
        """Test adding columns."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("Date", width="2.5cm", type="date")
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.columns) == 1
        assert builder._current_sheet is not None
        assert builder._current_sheet.columns[0].name == "Date"

    def test_add_column_without_sheet_raises(self) -> None:
        """Test adding column without sheet raises error."""
        builder = SpreadsheetBuilder(theme=None)
        with pytest.raises(NoSheetSelectedError):
            builder.column("Test")

    def test_add_columns(self) -> None:
        """Test adding multiple columns."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test")
        builder.column("Date", width="2.5cm", type="date")
        builder.column("Amount", width="3cm", type="currency")
        builder.column("Notes", width="5cm", type="string")
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.columns) == 3

    def test_header_row(self) -> None:
        """Test adding header row."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").column("B").header_row()
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.rows) == 1
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.rows[0].cells) == 2

    def test_header_row_with_style(self) -> None:
        """Test adding header row with style."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").column("B").header_row(style="header_primary")
        assert builder._current_sheet is not None
        assert builder._current_sheet.rows[0].style == "header_primary"

    def test_data_rows(self) -> None:
        """Test adding empty data rows."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").column("B").data_rows(5)
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.rows) == 5

    def test_add_row(self) -> None:
        """Test adding a row."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").row()
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.rows) == 1

    def test_add_row_with_style(self) -> None:
        """Test adding a row with style."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").row(style="total_row")
        assert builder._current_sheet is not None
        assert builder._current_sheet.rows[0].style == "total_row"

    def test_add_cell(self) -> None:
        """Test adding a cell."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").row().cell("Value")
        assert builder._current_row is not None
        assert len(builder._current_row.cells) == 1
        assert builder._current_row is not None
        assert builder._current_row.cells[0].value == "Value"

    def test_add_cell_without_row_raises(self) -> None:
        """Test adding cell without row raises error."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test")
        with pytest.raises(NoRowSelectedError):
            builder.cell("Value")

    def test_add_cell_with_formula(self) -> None:
        """Test adding cell with formula."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").row().cell(formula="of:=SUM([.A1:A10])")
        assert builder._current_row is not None
        assert builder._current_row.cells[0].formula == "of:=SUM([.A1:A10])"

    def test_add_cell_with_style(self) -> None:
        """Test adding cell with style."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").row().cell("Header", style="header")
        assert builder._current_row is not None
        assert builder._current_row.cells[0].style == "header"

    def test_add_cells(self) -> None:
        """Test adding multiple cells."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").row().cells("A", "B", "C")
        assert builder._current_row is not None
        assert len(builder._current_row.cells) == 3

    def test_formula_row(self) -> None:
        """Test adding formula row."""
        builder = SpreadsheetBuilder(theme=None)
        formulas = ["of:=SUM([.A1:A10])", None, "of:=COUNT([.C1:C10])"]
        builder.sheet("Test").column("A").column("B").column("C").formula_row(formulas)
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.rows) == 1
        assert builder._current_sheet is not None
        assert builder._current_sheet.rows[0].cells[0].formula == formulas[0]

    def test_total_row(self) -> None:
        """Test adding total row."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test")
        builder.column("Item").column("Amount", type="currency")
        builder.header_row()
        builder.total_row(formulas=[None, "of:=SUM([.B2:B100])"])
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.rows) == 2

    def test_freeze(self) -> None:
        """Test setting freeze panes."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").freeze(rows=1, cols=2)
        assert builder._current_sheet is not None
        assert builder._current_sheet.freeze_rows == 1
        assert builder._current_sheet is not None
        assert builder._current_sheet.freeze_cols == 2

    def test_build(self) -> None:
        """Test building sheet specifications."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Sheet1").column("A")
        builder.sheet("Sheet2").column("B")
        specs = builder.build()
        assert len(specs) == 2
        assert specs[0].name == "Sheet1"
        assert specs[1].name == "Sheet2"

    def test_chaining(self) -> None:
        """Test fluent chaining."""
        builder = (
            SpreadsheetBuilder(theme=None)
            .sheet("Expenses")
            .column("Date", type="date")
            .column("Category")
            .column("Amount", type="currency")
            .header_row()
            .data_rows(10)
        )
        assert len(builder._sheets) == 1
        assert len(builder._sheets[0].columns) == 3
        assert len(builder._sheets[0].rows) == 11  # header + 10 data


class TestSpreadsheetBuilderAdvanced:
    """Tests for advanced SpreadsheetBuilder features."""

    def test_workbook_properties(self) -> None:
        """Test setting workbook properties."""
        builder = SpreadsheetBuilder(theme=None)
        builder.workbook_properties(
            title="My Budget",
            author="John Doe",
        )
        props = builder.get_properties()
        assert props.title == "My Budget"
        assert props.author == "John Doe"

    def test_workbook_properties_all_fields(self) -> None:
        """Test setting all workbook properties fields (lines 1152-1163)."""
        builder = SpreadsheetBuilder(theme=None)
        builder.workbook_properties(
            title="Test Title",
            author="Test Author",
            subject="Test Subject",
            description="Test Description",
            keywords=["key1", "key2"],
            custom_field="custom_value",
        )
        props = builder.get_properties()
        assert props.title == "Test Title"
        assert props.author == "Test Author"
        assert props.subject == "Test Subject"
        assert props.description == "Test Description"
        assert props.keywords == ["key1", "key2"]
        assert props.custom["custom_field"] == "custom_value"

    def test_workbook_properties_none_values(self) -> None:
        """Test workbook properties with None values (conditional paths)."""
        builder = SpreadsheetBuilder(theme=None)
        # Call with None values - should not update
        builder.workbook_properties(
            title=None,
            author=None,
            subject=None,
            description=None,
            keywords=None,
        )
        props = builder.get_properties()
        assert props.title == ""
        assert props.author == ""

    def test_add_named_range(self) -> None:
        """Test adding named range."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Data")
        builder.named_range("MyRange", "A1", "B10")
        assert len(builder._named_ranges) == 1

    def test_named_range_with_explicit_sheet(self) -> None:
        """Test named range with explicit sheet name."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Data")
        builder.named_range("MyRange", "A1", "B10", sheet="OtherSheet")
        assert len(builder._named_ranges) == 1
        assert builder._named_ranges[0].scope == "OtherSheet"

    def test_get_named_ranges(self) -> None:
        """Test get_named_ranges method (line 1627)."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Data")
        builder.named_range("Range1", "A1", "A10")
        builder.named_range("Range2", "B1", "B10")
        ranges = builder.get_named_ranges()
        assert len(ranges) == 2
        assert ranges[0].name == "Range1"
        assert ranges[1].name == "Range2"

    def test_add_chart(self) -> None:
        """Test adding chart to sheet."""
        from spreadsheet_dl.charts import ChartBuilder

        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Data")
        chart = (
            ChartBuilder()
            .column_chart()
            .title("Test Chart")
            .series("Values", "Data.B1:B10")
            .build()
        )
        builder.chart(chart)
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.charts) == 1

    def test_chart_without_sheet_raises(self) -> None:
        """Test adding chart without sheet raises error (line 1594)."""
        from spreadsheet_dl.charts import ChartBuilder

        builder = SpreadsheetBuilder(theme=None)
        chart = ChartBuilder().column_chart().build()
        with pytest.raises(NoSheetSelectedError):
            builder.chart(chart)

    def test_freeze_without_sheet_raises(self) -> None:
        """Test freeze without sheet raises error (line 1228)."""
        builder = SpreadsheetBuilder(theme=None)
        with pytest.raises(NoSheetSelectedError):
            builder.freeze(rows=1)

    def test_print_area_without_sheet_raises(self) -> None:
        """Test print_area without sheet raises error (lines 1243-1246)."""
        builder = SpreadsheetBuilder(theme=None)
        with pytest.raises(NoSheetSelectedError):
            builder.print_area("A1:D50")

    def test_print_area(self) -> None:
        """Test setting print area (lines 1245-1246)."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test")
        builder.print_area("A1:D50")
        assert builder._current_sheet is not None
        assert builder._current_sheet.print_area == "A1:D50"

    def test_protect_without_sheet_raises(self) -> None:
        """Test protect without sheet raises error (lines 1266-1274)."""
        builder = SpreadsheetBuilder(theme=None)
        with pytest.raises(NoSheetSelectedError):
            builder.protect(password="secret")

    def test_protect_with_all_options(self) -> None:
        """Test protect with all options (lines 1266-1274)."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test")
        builder.protect(password="secret", edit_cells=True, edit_objects=True)
        assert builder._current_sheet is not None
        assert builder._current_sheet.protection["enabled"] is True
        assert builder._current_sheet is not None
        assert builder._current_sheet.protection["password"] == "secret"
        assert builder._current_sheet is not None
        assert builder._current_sheet.protection["edit_cells"] is True
        assert builder._current_sheet is not None
        assert builder._current_sheet.protection["edit_objects"] is True

    def test_header_row_without_sheet_raises(self) -> None:
        """Test header_row without sheet raises error (line 1334)."""
        builder = SpreadsheetBuilder(theme=None)
        with pytest.raises(NoSheetSelectedError):
            builder.header_row()

    def test_row_without_sheet_raises(self) -> None:
        """Test row without sheet raises error (line 1356)."""
        builder = SpreadsheetBuilder(theme=None)
        with pytest.raises(NoSheetSelectedError):
            builder.row()

    def test_data_rows_without_sheet_raises(self) -> None:
        """Test data_rows without sheet raises error (line 1381)."""
        builder = SpreadsheetBuilder(theme=None)
        with pytest.raises(NoSheetSelectedError):
            builder.data_rows(5)

    def test_data_rows_with_alternate_styles(self) -> None:
        """Test data_rows with alternating styles (line 1388)."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").column("B")
        builder.data_rows(5, alternate_styles=["even", "odd"])
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.rows) == 5
        assert builder._current_sheet is not None
        assert builder._current_sheet.rows[0].style == "even"
        assert builder._current_sheet is not None
        assert builder._current_sheet.rows[1].style == "odd"
        assert builder._current_sheet is not None
        assert builder._current_sheet.rows[2].style == "even"

    def test_total_row_without_sheet_raises(self) -> None:
        """Test total_row without sheet raises error (line 1418)."""
        builder = SpreadsheetBuilder(theme=None)
        with pytest.raises(NoSheetSelectedError):
            builder.total_row()

    def test_total_row_with_values(self) -> None:
        """Test total_row with values (lines 1422-1424)."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").column("B").column("C")
        builder.total_row(values=["Total", 100, 200])
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.rows) == 1
        assert builder._current_sheet is not None
        assert builder._current_sheet.rows[0].cells[0].value == "Total"
        assert builder._current_sheet is not None
        assert builder._current_sheet.rows[0].cells[1].value == 100

    def test_total_row_with_text_in_formulas(self) -> None:
        """Test total_row with text values in formulas list (lines 1427-1433)."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").column("B")
        builder.total_row(formulas=["Total", "of:=SUM([.B2:B10])"])
        # First item is text (no = or of: prefix), second is formula
        assert builder._current_sheet is not None
        assert builder._current_sheet.rows[0].cells[0].value == "Total"
        assert builder._current_sheet is not None
        assert builder._current_sheet.rows[0].cells[1].formula == "of:=SUM([.B2:B10])"

    def test_total_row_empty(self) -> None:
        """Test total_row with no values or formulas (lines 1437-1439)."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").column("B").column("C")
        builder.total_row()
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.rows) == 1
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.rows[0].cells) == 3

    def test_formula_row_without_sheet_raises(self) -> None:
        """Test formula_row without sheet raises error (line 1462)."""
        builder = SpreadsheetBuilder(theme=None)
        with pytest.raises(NoSheetSelectedError):
            builder.formula_row(["of:=SUM([.A1:A10])"])

    def test_cells_without_row_raises(self) -> None:
        """Test cells without row raises error (line 1527)."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test")
        with pytest.raises(NoRowSelectedError):
            builder.cells("A", "B", "C")

    def test_conditional_format_without_sheet_raises(self) -> None:
        """Test conditional_format without sheet raises error (lines 1547-1550)."""
        builder = SpreadsheetBuilder(theme=None)
        with pytest.raises(NoSheetSelectedError):
            builder.conditional_format("format1")

    def test_conditional_format(self) -> None:
        """Test adding conditional format."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test")
        builder.conditional_format("highlight_red")
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.conditional_formats) == 1
        assert builder._current_sheet is not None
        assert builder._current_sheet.conditional_formats[0] == "highlight_red"

    def test_validation_without_sheet_raises(self) -> None:
        """Test validation without sheet raises error (lines 1562-1565)."""
        builder = SpreadsheetBuilder(theme=None)
        with pytest.raises(NoSheetSelectedError):
            builder.validation("val1")

    def test_validation(self) -> None:
        """Test adding validation."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test")
        builder.validation("list_validation")
        assert builder._current_sheet is not None
        assert len(builder._current_sheet.validations) == 1
        assert builder._current_sheet is not None
        assert builder._current_sheet.validations[0] == "list_validation"


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_create_spreadsheet(self) -> None:
        """Test create_spreadsheet function."""
        builder = create_spreadsheet(theme="default")
        assert isinstance(builder, SpreadsheetBuilder)
        assert builder._theme_name == "default"

    def test_create_spreadsheet_no_theme(self) -> None:
        """Test create_spreadsheet without theme."""
        builder = create_spreadsheet(theme=None)
        assert builder._theme is None

    def test_formula_function(self) -> None:
        """Test formula function."""
        f = formula()
        assert isinstance(f, FormulaBuilder)


class TestSpreadsheetBuilderSave:
    """Tests for SpreadsheetBuilder.save method."""

    def test_save_creates_file(self, tmp_path: Path) -> None:
        """Test saving spreadsheet creates file."""
        output = tmp_path / "test.ods"

        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").column("B").header_row().data_rows(5)
        path = builder.save(output)

        assert path.exists()
        assert path.stat().st_size > 0

    def test_save_multi_sheet(self, tmp_path: Path) -> None:
        """Test saving multi-sheet spreadsheet."""
        output = tmp_path / "multi_sheet.ods"

        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Sheet1").column("A").header_row()
        builder.sheet("Sheet2").column("B").header_row()
        path = builder.save(output)

        assert path.exists()

    def test_save_with_formulas(self, tmp_path: Path) -> None:
        """Test saving spreadsheet with formulas."""
        output = tmp_path / "formulas.ods"

        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").column("B")
        builder.row().cell(10).cell(20)
        builder.row().cell(formula="of:=SUM([.A1:A1])").cell(
            formula="of:=SUM([.B1:B1])"
        )
        path = builder.save(output)

        assert path.exists()

    def test_save_with_string_path(self, tmp_path: Path) -> None:
        """Test saving with string path."""
        output = str(tmp_path / "string_path.ods")

        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").header_row()
        path = builder.save(output)

        assert path.exists()

    def test_save_creates_directories(self, tmp_path: Path) -> None:
        """Test saving creates nested directories."""
        output = tmp_path / "nested" / "dir" / "test.ods"

        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").header_row()
        path = builder.save(output)

        assert path.exists()
        assert path.parent.exists()


class TestFormulaDependencyGraph:
    """Tests for FormulaDependencyGraph - circular reference detection."""

    def test_no_circular_reference(self) -> None:
        """Test detecting no circular reference."""
        graph = FormulaDependencyGraph()
        graph.add_cell("B1", "of:=[.A1]")
        graph.add_cell("C1", "of:=[.B1]")
        graph.add_cell("D1", "of:=[.C1]")
        refs = graph.detect_circular_references()
        assert len(refs) == 0

    def test_circular_reference_detected(self) -> None:
        """Test detecting circular reference."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=[.B1]")
        graph.add_cell("B1", "of:=[.C1]")
        graph.add_cell("C1", "of:=[.A1]")
        refs = graph.detect_circular_references()
        assert len(refs) > 0

    def test_self_reference(self) -> None:
        """Test detecting self-reference."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=[.A1]")
        refs = graph.detect_circular_references()
        assert len(refs) > 0

    def test_complex_circular(self) -> None:
        """Test detecting complex circular reference."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=[.B1]+[.C1]")
        graph.add_cell("B1", "of:=[.D1]")
        graph.add_cell("C1", "of:=[.E1]")
        graph.add_cell("E1", "of:=[.A1]")  # Creates cycle
        refs = graph.detect_circular_references()
        assert len(refs) > 0

    def test_multiple_dependencies(self) -> None:
        """Test cell with multiple dependencies."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=[.B1]+[.C1]+[.D1]")
        refs = graph.detect_circular_references()
        assert len(refs) == 0

    def test_find_cycle(self) -> None:
        """Test finding the cycle path."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=[.B1]")
        graph.add_cell("B1", "of:=[.C1]")
        graph.add_cell("C1", "of:=[.A1]")
        refs = graph.detect_circular_references()
        assert len(refs) > 0
        _cell, cycle = refs[0]
        assert any("A1" in c for c in cycle)

    def test_clear_graph(self) -> None:
        """Test clearing the dependency graph."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=[.B1]")
        # Clear by creating new graph
        graph = FormulaDependencyGraph()
        refs = graph.detect_circular_references()
        assert len(refs) == 0

    def test_add_cell_no_formula(self) -> None:
        """Test adding cell without formula (line 1734)."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", None)
        assert "Sheet1.A1" in graph._dependencies
        assert len(graph._dependencies["Sheet1.A1"]) == 0

    def test_add_cell_with_custom_sheet(self) -> None:
        """Test adding cell with custom sheet name (line 1737)."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=[.B1]", sheet="MySheet")
        deps = graph.get_dependencies("A1", sheet="MySheet")
        assert "MySheet.B1" in deps

    def test_extract_cross_sheet_references(self) -> None:
        """Test extracting cross-sheet references (lines 1762-1765)."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=[Sheet2.B5]+[OtherSheet.C10]", sheet="Sheet1")
        deps = graph.get_dependencies("A1", sheet="Sheet1")
        assert "Sheet2.B5" in deps
        assert "OtherSheet.C10" in deps

    def test_extract_cross_sheet_with_quotes(self) -> None:
        """Test cross-sheet references with quoted sheet names (line 1763)."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=['My Sheet'.B5]", sheet="Sheet1")
        deps = graph.get_dependencies("A1", sheet="Sheet1")
        assert "My Sheet.B5" in deps

    def test_validate_raises_on_circular(self) -> None:
        """Test validate() raises CircularReferenceError (lines 1826-1829)."""
        from spreadsheet_dl.builder import CircularReferenceError

        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=[.B1]")
        graph.add_cell("B1", "of:=[.A1]")
        with pytest.raises(CircularReferenceError):
            graph.validate()

    def test_validate_succeeds_without_circular(self) -> None:
        """Test validate() succeeds without circular references."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=[.B1]")
        graph.add_cell("B1", "of:=[.C1]")
        graph.validate()  # Should not raise

    def test_get_dependencies(self) -> None:
        """Test get_dependencies method (lines 1842-1843)."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=[.B1]+[.C1]")
        deps = graph.get_dependencies("A1")
        assert "Sheet1.B1" in deps
        assert "Sheet1.C1" in deps

    def test_get_dependents(self) -> None:
        """Test get_dependents method (lines 1856-1863)."""
        graph = FormulaDependencyGraph()
        graph.add_cell("A1", "of:=[.B1]")
        graph.add_cell("C1", "of:=[.B1]")
        graph.add_cell("D1", "of:=[.B1]+[.E1]")
        # B1 is depended on by A1, C1, and D1
        dependents = graph.get_dependents("B1")
        assert "Sheet1.A1" in dependents
        assert "Sheet1.C1" in dependents
        assert "Sheet1.D1" in dependents

    def test_circular_reference_error_formatting(self) -> None:
        """Test CircularReferenceError message formatting (lines 1692-1698)."""
        from spreadsheet_dl.builder import CircularReferenceError

        cycle = ["Sheet1.A1", "Sheet1.B1", "Sheet1.C1", "Sheet1.A1"]
        error = CircularReferenceError("Sheet1.A1", cycle)
        assert "Sheet1.A1" in str(error)
        assert "Sheet1.B1" in str(error)
        assert "->" in str(error)
        assert error.cell == "Sheet1.A1"
        assert error.cycle == cycle


class TestFormulaCoverageGaps:
    """Tests for untested formula methods to achieve 95% coverage."""

    def test_weekday_formula(self) -> None:
        """Test WEEKDAY formula (line 743)."""
        fb = FormulaBuilder()
        # Default type
        result = fb.weekday("A1")
        assert result == "of:=WEEKDAY([.A1];1)"
        # Custom type
        result = fb.weekday("B2", type=2)
        assert result == "of:=WEEKDAY([.B2];2)"

    def test_weeknum_formula(self) -> None:
        """Test WEEKNUM formula (line 747)."""
        fb = FormulaBuilder()
        result = fb.weeknum("A1")
        assert result == "of:=WEEKNUM([.A1];1)"
        result = fb.weeknum("B2", type=2)
        assert result == "of:=WEEKNUM([.B2];2)"

    def test_index_formula_without_col(self) -> None:
        """Test INDEX formula without col_num (line 816)."""
        fb = FormulaBuilder()
        result = fb.index(
            array=RangeRef(start="A1", end="A10"), row_num=5, col_num=None
        )
        assert result == "of:=INDEX([.A1:A10];5)"

    def test_index_match_with_prefix_strip(self) -> None:
        """Test INDEX/MATCH with prefix stripping (lines 855-857)."""
        fb = FormulaBuilder()
        # Test with prefix already in match formula
        match_with_prefix = fb.match("value", RangeRef(start="A1", end="A10"))
        result = fb.index_match(RangeRef(start="B1", end="B10"), match_with_prefix)
        assert "INDEX" in result
        assert "MATCH" in result

    def test_offset_with_height_width(self) -> None:
        """Test OFFSET formula with height and width (lines 868-876)."""
        fb = FormulaBuilder()
        # With height only
        result = fb.offset("A1", rows=2, cols=3, height=5)
        assert result == "of:=OFFSET([.A1];2;3;5)"
        # With height and width
        result = fb.offset("A1", rows=2, cols=3, height=5, width=10)
        assert result == "of:=OFFSET([.A1];2;3;5;10)"

    def test_indirect_formula(self) -> None:
        """Test INDIRECT formula (line 880)."""
        fb = FormulaBuilder()
        result = fb.indirect("A1")
        assert result == "of:=INDIRECT([.A1])"

    def test_left_formula(self) -> None:
        """Test LEFT formula (line 893)."""
        fb = FormulaBuilder()
        result = fb.left("A1", num_chars=5)
        assert result == "of:=LEFT([.A1];5)"

    def test_right_formula(self) -> None:
        """Test RIGHT formula (line 935)."""
        fb = FormulaBuilder()
        result = fb.right("A1", num_chars=3)
        assert result == "of:=RIGHT([.A1];3)"

    def test_mid_formula(self) -> None:
        """Test MID formula (line 941)."""
        fb = FormulaBuilder()
        result = fb.mid("A1", start_num=2, num_chars=5)
        assert result == "of:=MID([.A1];2;5)"

    def test_find_formula(self) -> None:
        """Test FIND formula (lines 935 with start_num)."""
        fb = FormulaBuilder()
        # With explicit start_num
        result = fb.find("text", "A1", start_num=5)
        assert result == 'of:=FIND("text";[.A1];5)'

    def test_search_formula(self) -> None:
        """Test SEARCH formula (line 941 with start_num)."""
        fb = FormulaBuilder()
        # With explicit start_num
        result = fb.search("pattern", "A1", start_num=2)
        assert result == 'of:=SEARCH("pattern";[.A1];2)'

    def test_substitute_with_instance(self) -> None:
        """Test SUBSTITUTE formula with instance_num (lines 951-954)."""
        fb = FormulaBuilder()
        result = fb.substitute("A1", old_text="old", new_text="new", instance_num=2)
        assert '"old"' in result
        assert '"new"' in result
        assert ";2)" in result

    def test_text_formula(self) -> None:
        """Test TEXT formula (line 895-897)."""
        fb = FormulaBuilder()
        result = fb.text("A1", format_text="0.00")
        assert result == 'of:=TEXT([.A1];"0.00")'

    def test_iferror_formula(self) -> None:
        """Test IFERROR formula (line 971-977)."""
        fb = FormulaBuilder()
        result = fb.iferror(value="A1", value_if_error="0")
        assert result == "of:=IFERROR([.A1];0)"

    def test_ifna_formula(self) -> None:
        """Test IFNA formula (line 985)."""
        fb = FormulaBuilder()
        result = fb.ifna(value="A1", value_if_na="NA")
        assert result == "of:=IFNA([.A1];[.NA])"

    def test_isblank_formula(self) -> None:
        """Test ISBLANK formula (line 999-1001)."""
        fb = FormulaBuilder()
        result = fb.isblank("A1")
        assert result == "of:=ISBLANK([.A1])"

    def test_iserror_formula(self) -> None:
        """Test ISERROR formula (line 1003-1005)."""
        fb = FormulaBuilder()
        result = fb.iserror("A1")
        assert result == "of:=ISERROR([.A1])"

    def test_isnumber_formula(self) -> None:
        """Test ISNUMBER formula (line 1007-1009)."""
        fb = FormulaBuilder()
        result = fb.isnumber("A1")
        assert result == "of:=ISNUMBER([.A1])"

    def test_istext_formula(self) -> None:
        """Test ISTEXT formula (line 1011-1013)."""
        fb = FormulaBuilder()
        result = fb.istext("A1")
        assert result == "of:=ISTEXT([.A1])"

    def test_concat_formula(self) -> None:
        """Test CONCAT formula (alias for CONCATENATE, line 893)."""
        fb = FormulaBuilder()
        result = fb.concat("A1", "B1", "C1")
        assert "CONCATENATE" in result
        assert result == "of:=CONCATENATE([.A1];[.B1];[.C1])"

    def test_array_formula(self) -> None:
        """Test array formula wrapping (lines 1032-1034)."""
        fb = FormulaBuilder()
        # Without prefix
        result = fb.array("SUM(A1:A10)")
        assert result == "of:={SUM(A1:A10)}"
        # With prefix - should strip it
        result = fb.array("of:=SUM(B1:B10)")
        assert result == "of:={SUM(B1:B10)}"
