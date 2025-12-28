"""Tests for builder module - SpreadsheetBuilder and FormulaBuilder."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from finance_tracker.builder import (
    CellRef,
    CellSpec,
    ColumnSpec,
    FormulaBuilder,
    RangeRef,
    RowSpec,
    SheetRef,
    SheetSpec,
    SpreadsheetBuilder,
    create_spreadsheet,
    formula,
)

if TYPE_CHECKING:
    from pathlib import Path

    pass


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

    def test_divide_formula(self) -> None:
        """Test division formula with zero check."""
        f = FormulaBuilder()
        formula_str = f.divide("B2", "C2")
        assert "IF" in formula_str
        assert ">0" in formula_str

    def test_average_formula(self) -> None:
        """Test AVERAGE formula."""
        f = FormulaBuilder()
        formula_str = f.average(f.range("A1", "A10"))
        assert formula_str == "of:=AVERAGE([.A1:A10])"

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


class TestSheetSpec:
    """Tests for SheetSpec class."""

    def test_empty_sheet(self) -> None:
        """Test empty sheet specification."""
        sheet = SheetSpec(name="Test")
        assert sheet.name == "Test"
        assert len(sheet.columns) == 0
        assert len(sheet.rows) == 0


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

    def test_add_sheet(self) -> None:
        """Test adding a sheet."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test Sheet")
        assert len(builder._sheets) == 1
        assert builder._sheets[0].name == "Test Sheet"

    def test_add_column(self) -> None:
        """Test adding columns."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("Date", width="2.5cm", type="date")
        assert len(builder._current_sheet.columns) == 1
        assert builder._current_sheet.columns[0].name == "Date"

    def test_add_column_without_sheet_raises(self) -> None:
        """Test adding column without sheet raises error."""
        builder = SpreadsheetBuilder(theme=None)
        with pytest.raises(ValueError, match="No sheet selected"):
            builder.column("Test")

    def test_header_row(self) -> None:
        """Test adding header row."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").column("B").header_row()
        assert len(builder._current_sheet.rows) == 1
        assert len(builder._current_sheet.rows[0].cells) == 2

    def test_data_rows(self) -> None:
        """Test adding empty data rows."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").column("A").column("B").data_rows(5)
        assert len(builder._current_sheet.rows) == 5

    def test_add_row(self) -> None:
        """Test adding a row."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").row()
        assert len(builder._current_sheet.rows) == 1

    def test_add_cell(self) -> None:
        """Test adding a cell."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").row().cell("Value")
        assert len(builder._current_row.cells) == 1
        assert builder._current_row.cells[0].value == "Value"

    def test_add_cell_without_row_raises(self) -> None:
        """Test adding cell without row raises error."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test")
        with pytest.raises(ValueError, match="No row selected"):
            builder.cell("Value")

    def test_add_cells(self) -> None:
        """Test adding multiple cells."""
        builder = SpreadsheetBuilder(theme=None)
        builder.sheet("Test").row().cells("A", "B", "C")
        assert len(builder._current_row.cells) == 3

    def test_formula_row(self) -> None:
        """Test adding formula row."""
        builder = SpreadsheetBuilder(theme=None)
        formulas = ["of:=SUM([.A1:A10])", None, "of:=COUNT([.C1:C10])"]
        builder.sheet("Test").column("A").column("B").column("C").formula_row(formulas)
        assert len(builder._current_sheet.rows) == 1
        assert builder._current_sheet.rows[0].cells[0].formula == formulas[0]

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


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_create_spreadsheet(self) -> None:
        """Test create_spreadsheet function."""
        builder = create_spreadsheet(theme="default")
        assert isinstance(builder, SpreadsheetBuilder)
        assert builder._theme_name == "default"

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
