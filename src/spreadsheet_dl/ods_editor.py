"""
ODS file editing module for appending expenses to existing spreadsheets.

Implements:
    - FR-CORE-003: Expense append functionality
    - G-02: Fix expense command to actually write to ODS files

Provides safe modification of existing ODS files while preserving
structure, formulas, and formatting.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from odf.opendocument import load
from odf.table import Table, TableCell, TableRow
from odf.text import P

from spreadsheet_dl.exceptions import OdsReadError, OdsWriteError, SheetNotFoundError

if TYPE_CHECKING:
    from odf.opendocument import OpenDocumentSpreadsheet

    from spreadsheet_dl.ods_generator import ExpenseEntry


class OdsEditor:
    """
    Edit existing ODS spreadsheets.

    Provides safe modification of ODS files for:
    - Appending expense entries
    - Updating cell values
    - Preserving existing formulas and formatting

    Implements:
        - FR-CORE-003: Expense append to existing ODS files
    """

    def __init__(self, file_path: Path | str) -> None:
        """
        Initialize editor with an existing ODS file.

        Args:
            file_path: Path to the ODS file to edit.

        Raises:
            OdsReadError: If file cannot be read or is invalid.
        """
        self.file_path = Path(file_path)
        self._doc: OpenDocumentSpreadsheet | None = None

        if not self.file_path.exists():
            raise OdsReadError(f"File not found: {self.file_path}", "FILE_NOT_FOUND")

        try:
            self._doc = load(str(self.file_path))
        except Exception as e:
            raise OdsReadError(
                f"Failed to load ODS file: {e}", "ODS_LOAD_FAILED"
            ) from e

    def get_sheet_names(self) -> list[str]:
        """
        Get list of sheet names in the document.

        Returns:
            List of sheet names.
        """
        if self._doc is None:
            return []

        sheets = self._doc.spreadsheet.getElementsByType(Table)
        return [sheet.getAttribute("name") for sheet in sheets]

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
        if self._doc is None:
            raise OdsReadError("Document not loaded", "DOC_NOT_LOADED")

        sheets = self._doc.spreadsheet.getElementsByType(Table)
        for sheet in sheets:
            if sheet.getAttribute("name") == name:
                return sheet

        available = self.get_sheet_names()
        raise SheetNotFoundError(name, available)

    def find_next_empty_row(self, sheet_name: str) -> int:
        """
        Find the index of the next empty row in a sheet.

        Scans from the beginning looking for the first row where
        the first cell is empty (excluding header row).

        Args:
            sheet_name: Name of the sheet to scan.

        Returns:
            Row index (0-based) of the next empty row.
        """
        sheet = self.get_sheet(sheet_name)
        rows = sheet.getElementsByType(TableRow)

        # Start from row 1 (skip header)
        for idx, row in enumerate(rows[1:], start=1):
            cells = row.getElementsByType(TableCell)
            if not cells:
                return idx

            # Check if first cell is empty
            first_cell = cells[0]
            text_content = ""
            for p in first_cell.getElementsByType(P):
                if hasattr(p, "firstChild") and p.firstChild:
                    text_content = str(p.firstChild)
                    break

            # Also check value attributes
            date_value = first_cell.getAttribute("datevalue")
            string_value = first_cell.getAttribute("stringvalue")

            if not text_content and not date_value and not string_value:
                return idx

        # All rows filled, return the count (append at end)
        return len(rows)

    def append_expense(self, expense: ExpenseEntry, sheet_name: str = "Expense Log") -> int:
        """
        Append an expense entry to the expense sheet.

        Args:
            expense: ExpenseEntry to append.
            sheet_name: Name of the expense sheet (default: "Expense Log").

        Returns:
            Row number where expense was added.

        Raises:
            SheetNotFoundError: If expense sheet not found.
            OdsWriteError: If append fails.

        Implements:
            - FR-CORE-003: Expense append functionality
        """
        try:
            sheet = self.get_sheet(sheet_name)
            rows = sheet.getElementsByType(TableRow)

            # Find insertion point
            insert_idx = self.find_next_empty_row(sheet_name)

            # Create the expense row
            row = self._create_expense_row(expense)

            # Insert or replace row
            if insert_idx < len(rows):
                # Replace existing empty row
                old_row = rows[insert_idx]
                sheet.insertBefore(row, old_row)
                sheet.removeChild(old_row)
            else:
                # Append new row
                sheet.addElement(row)

            return insert_idx + 1  # Return 1-based row number

        except SheetNotFoundError:
            raise
        except Exception as e:
            raise OdsWriteError(
                f"Failed to append expense: {e}", "EXPENSE_APPEND_FAILED"
            ) from e

    def _create_expense_row(self, expense: ExpenseEntry) -> TableRow:
        """
        Create a TableRow element from an ExpenseEntry.

        Args:
            expense: ExpenseEntry to convert.

        Returns:
            TableRow element ready for insertion.
        """
        row = TableRow()

        # Date cell
        date_cell = TableCell(
            valuetype="date",
            datevalue=expense.date.isoformat(),
        )
        date_cell.addElement(P(text=expense.date.strftime("%Y-%m-%d")))
        row.addElement(date_cell)

        # Category cell
        cat_cell = TableCell(valuetype="string")
        cat_cell.addElement(P(text=expense.category.value))
        row.addElement(cat_cell)

        # Description cell
        desc_cell = TableCell(valuetype="string")
        desc_cell.addElement(P(text=expense.description))
        row.addElement(desc_cell)

        # Amount cell
        amount_cell = TableCell(
            valuetype="currency",
            value=str(expense.amount),
        )
        amount_cell.addElement(P(text=f"${expense.amount:.2f}"))
        row.addElement(amount_cell)

        # Notes cell
        notes_cell = TableCell(valuetype="string")
        notes_cell.addElement(P(text=expense.notes))
        row.addElement(notes_cell)

        return row

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
        if self._doc is None:
            raise OdsWriteError("No document loaded", "NO_DOC")

        save_path = Path(output_path) if output_path else self.file_path

        try:
            self._doc.save(str(save_path))
            return save_path
        except Exception as e:
            raise OdsWriteError(
                f"Failed to save document: {e}", "SAVE_FAILED"
            ) from e


def append_expense_to_file(
    file_path: Path | str,
    expense: ExpenseEntry,
    sheet_name: str = "Expense Log",
) -> tuple[Path, int]:
    """
    Convenience function to append a single expense to an ODS file.

    Args:
        file_path: Path to the ODS file.
        expense: ExpenseEntry to append.
        sheet_name: Name of the expense sheet.

    Returns:
        Tuple of (file path, row number where added).

    Implements:
        - FR-CORE-003: Quick expense append
    """
    editor = OdsEditor(file_path)
    row_num = editor.append_expense(expense, sheet_name)
    saved_path = editor.save()
    return saved_path, row_num
