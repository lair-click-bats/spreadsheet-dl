"""
ODS file editing module for appending expenses to existing spreadsheets.

Implements:
    - FR-CORE-003: Expense append functionality
    - G-02: Fix expense command to actually write to ODS files
    - TASK-302: Cell operations for MCP server

Provides safe modification of existing ODS files while preserving
structure, formulas, and formatting.
"""

from __future__ import annotations

import contextlib
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

from odf.opendocument import load
from odf.table import Table, TableCell, TableRow
from odf.text import P

from spreadsheet_dl.exceptions import OdsReadError, OdsWriteError, SheetNotFoundError

if TYPE_CHECKING:
    from odf.opendocument import OpenDocumentSpreadsheet

    from spreadsheet_dl.domains.finance.ods_generator import ExpenseEntry


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
        except (OSError, ValueError, AttributeError, KeyError) as e:
            # OSError: File I/O, ValueError: malformed XML/ZIP, AttributeError: missing attrs, KeyError: missing elements
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

    def append_expense(
        self, expense: ExpenseEntry, sheet_name: str = "Expense Log"
    ) -> int:
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
        except (AttributeError, ValueError, TypeError) as e:
            # AttributeError: missing DOM methods, ValueError: invalid data, TypeError: type mismatches
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
        except (OSError, ValueError, AttributeError) as e:
            # OSError: File I/O, ValueError: serialization, AttributeError: missing methods
            raise OdsWriteError(f"Failed to save document: {e}", "SAVE_FAILED") from e

    # =========================================================================
    # Cell Operations (TASK-302)
    # =========================================================================

    @staticmethod
    def _parse_cell_reference(cell_ref: str) -> tuple[int, int]:
        """
        Parse A1-style cell reference to (row, col) indices.

        Args:
            cell_ref: Cell reference like 'A1', 'B5', 'AA10'.

        Returns:
            Tuple of (row_index, col_index) (0-based).

        Raises:
            ValueError: If cell reference is invalid.
        """
        match = re.match(r"^([A-Z]+)(\d+)$", cell_ref.upper())
        if not match:
            raise ValueError(f"Invalid cell reference: {cell_ref}")

        col_str, row_str = match.groups()
        row = int(row_str) - 1  # Convert to 0-based

        # Convert column letters to index (A=0, B=1, ..., Z=25, AA=26, etc.)
        col = 0
        for char in col_str:
            col = col * 26 + (ord(char) - ord("A") + 1)
        col -= 1  # Convert to 0-based

        return row, col

    @staticmethod
    def _parse_range(range_ref: str) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Parse A1-style range reference to start and end coordinates.

        Args:
            range_ref: Range like 'A1:B5'.

        Returns:
            Tuple of ((start_row, start_col), (end_row, end_col)).

        Raises:
            ValueError: If range reference is invalid.
        """
        if ":" not in range_ref:
            # Single cell, return as 1x1 range
            row, col = OdsEditor._parse_cell_reference(range_ref)
            return (row, col), (row, col)

        start_ref, end_ref = range_ref.split(":", 1)
        start = OdsEditor._parse_cell_reference(start_ref)
        end = OdsEditor._parse_cell_reference(end_ref)
        return start, end

    def _get_cell(self, sheet: Table, row: int, col: int) -> TableCell | None:
        """
        Get a cell from a sheet by row and column index.

        Args:
            sheet: Sheet table element.
            row: Row index (0-based).
            col: Column index (0-based).

        Returns:
            TableCell element or None if not found.
        """
        rows = sheet.getElementsByType(TableRow)
        if row >= len(rows):
            return None

        cells = rows[row].getElementsByType(TableCell)
        if col >= len(cells):
            return None

        return cells[col]

    def _get_cell_value(self, cell: TableCell) -> Any:
        """
        Extract the value from a cell.

        Args:
            cell: TableCell element.

        Returns:
            Cell value (str, int, float, or None).
        """
        if cell is None:
            return None

        # Check for value attributes first
        value_type = cell.getAttribute("valuetype")

        if value_type == "float" or value_type == "currency":
            value = cell.getAttribute("value")
            if value:
                return float(value)
        elif value_type == "date":
            return cell.getAttribute("datevalue")
        elif value_type == "boolean":
            value = cell.getAttribute("booleanvalue")
            return value == "true" if value else None
        elif value_type == "string":
            value = cell.getAttribute("stringvalue")
            if value:
                return value

        # Fall back to text content
        text_parts = []
        for p in cell.getElementsByType(P):
            if hasattr(p, "firstChild") and p.firstChild:
                text_parts.append(str(p.firstChild))

        return " ".join(text_parts) if text_parts else None

    def _set_cell_value(
        self, sheet: Table, row: int, col: int, value: Any
    ) -> TableCell:
        """
        Set the value of a cell, creating rows/cells as needed.

        Args:
            sheet: Sheet table element.
            row: Row index (0-based).
            col: Column index (0-based).
            value: Value to set.

        Returns:
            The modified or created TableCell.
        """
        # Ensure row exists
        rows = sheet.getElementsByType(TableRow)
        while len(rows) <= row:
            sheet.addElement(TableRow())
            rows = sheet.getElementsByType(TableRow)

        target_row = rows[row]

        # Ensure cell exists
        cells = target_row.getElementsByType(TableCell)
        while len(cells) <= col:
            target_row.addElement(TableCell())
            cells = target_row.getElementsByType(TableCell)

        cell = cells[col]

        # Clear existing content
        for child in list(cell.childNodes):
            cell.removeChild(child)

        # Set new value
        if isinstance(value, bool):
            cell.setAttribute("valuetype", "boolean")
            cell.setAttribute("booleanvalue", "true" if value else "false")
            cell.addElement(P(text=str(value)))
        elif isinstance(value, (int, float)):
            cell.setAttribute("valuetype", "float")
            cell.setAttribute("value", str(value))
            cell.addElement(P(text=str(value)))
        else:
            # String value
            cell.setAttribute("valuetype", "string")
            cell.addElement(P(text=str(value)))

        return cell

    def get_cell_value(self, sheet_name: str, cell_ref: str) -> Any:
        """
        Get the value of a specific cell.

        Args:
            sheet_name: Name of the sheet.
            cell_ref: Cell reference (e.g., 'A1', 'B5').

        Returns:
            Cell value.

        Raises:
            SheetNotFoundError: If sheet not found.
            ValueError: If cell reference is invalid.
        """
        sheet = self.get_sheet(sheet_name)
        row, col = self._parse_cell_reference(cell_ref)
        cell = self._get_cell(sheet, row, col)
        return self._get_cell_value(cell)

    def set_cell_value(self, sheet_name: str, cell_ref: str, value: Any) -> None:
        """
        Set the value of a specific cell.

        Args:
            sheet_name: Name of the sheet.
            cell_ref: Cell reference (e.g., 'A1', 'B5').
            value: Value to set.

        Raises:
            SheetNotFoundError: If sheet not found.
            ValueError: If cell reference is invalid.
        """
        sheet = self.get_sheet(sheet_name)
        row, col = self._parse_cell_reference(cell_ref)
        self._set_cell_value(sheet, row, col, value)

    def clear_cell(self, sheet_name: str, cell_ref: str) -> None:
        """
        Clear the value and formatting of a cell.

        Args:
            sheet_name: Name of the sheet.
            cell_ref: Cell reference (e.g., 'A1', 'B5').

        Raises:
            SheetNotFoundError: If sheet not found.
            ValueError: If cell reference is invalid.
        """
        sheet = self.get_sheet(sheet_name)
        row, col = self._parse_cell_reference(cell_ref)
        cell = self._get_cell(sheet, row, col)

        if cell is not None:
            # Clear all attributes and content
            for attr in [
                "valuetype",
                "value",
                "datevalue",
                "stringvalue",
                "booleanvalue",
            ]:
                # Attribute doesn't exist, continue
                with contextlib.suppress(Exception):
                    cell.removeAttribute(attr)

            for child in list(cell.childNodes):
                cell.removeChild(child)

    def copy_cells(self, sheet_name: str, source: str, destination: str) -> None:
        """
        Copy a cell or range to another location.

        Args:
            sheet_name: Name of the sheet.
            source: Source cell/range (e.g., 'A1' or 'A1:B5').
            destination: Destination cell (top-left of paste area).

        Raises:
            SheetNotFoundError: If sheet not found.
            ValueError: If cell references are invalid.
        """
        sheet = self.get_sheet(sheet_name)
        src_start, src_end = self._parse_range(source)
        dst_row, dst_col = self._parse_cell_reference(destination)

        # Copy each cell in the range
        for row_offset in range(src_end[0] - src_start[0] + 1):
            for col_offset in range(src_end[1] - src_start[1] + 1):
                src_row = src_start[0] + row_offset
                src_col = src_start[1] + col_offset
                dst_row_idx = dst_row + row_offset
                dst_col_idx = dst_col + col_offset

                src_cell = self._get_cell(sheet, src_row, src_col)
                value = self._get_cell_value(src_cell)
                self._set_cell_value(sheet, dst_row_idx, dst_col_idx, value)

    def move_cells(self, sheet_name: str, source: str, destination: str) -> None:
        """
        Move a cell or range to another location.

        Args:
            sheet_name: Name of the sheet.
            source: Source cell/range (e.g., 'A1' or 'A1:B5').
            destination: Destination cell (top-left of paste area).

        Raises:
            SheetNotFoundError: If sheet not found.
            ValueError: If cell references are invalid.
        """
        # Copy first
        self.copy_cells(sheet_name, source, destination)

        # Then clear source
        sheet = self.get_sheet(sheet_name)
        src_start, src_end = self._parse_range(source)

        for row in range(src_start[0], src_end[0] + 1):
            for col in range(src_start[1], src_end[1] + 1):
                cell = self._get_cell(sheet, row, col)
                if cell is not None:
                    for attr in [
                        "valuetype",
                        "value",
                        "datevalue",
                        "stringvalue",
                        "booleanvalue",
                    ]:
                        # Attribute doesn't exist, continue
                        with contextlib.suppress(Exception):
                            cell.removeAttribute(attr)
                    for child in list(cell.childNodes):
                        cell.removeChild(child)

    def find_cells(
        self, sheet_name: str, search_text: str, match_case: bool = False
    ) -> list[tuple[str, Any]]:
        """
        Find cells containing specific text.

        Args:
            sheet_name: Name of the sheet.
            search_text: Text to search for.
            match_case: Whether to match case.

        Returns:
            List of (cell_ref, value) tuples for matches.

        Raises:
            SheetNotFoundError: If sheet not found.
        """
        sheet = self.get_sheet(sheet_name)
        matches = []

        search = search_text if match_case else search_text.lower()

        rows = sheet.getElementsByType(TableRow)
        for row_idx, row in enumerate(rows):
            cells = row.getElementsByType(TableCell)
            for col_idx, cell in enumerate(cells):
                value = self._get_cell_value(cell)
                if value is None:
                    continue

                value_str = str(value) if match_case else str(value).lower()
                if search in value_str:
                    # Convert indices back to A1 notation
                    col_letter = self._col_index_to_letter(col_idx)
                    cell_ref = f"{col_letter}{row_idx + 1}"
                    matches.append((cell_ref, value))

        return matches

    def replace_cells(
        self,
        sheet_name: str,
        search_text: str,
        replace_text: str,
        match_case: bool = False,
    ) -> int:
        """
        Find and replace text in cells.

        Args:
            sheet_name: Name of the sheet.
            search_text: Text to search for.
            replace_text: Replacement text.
            match_case: Whether to match case.

        Returns:
            Number of replacements made.

        Raises:
            SheetNotFoundError: If sheet not found.
        """
        matches = self.find_cells(sheet_name, search_text, match_case)
        count = 0

        for cell_ref, old_value in matches:
            old_str = str(old_value)
            if match_case:
                new_value = old_str.replace(search_text, replace_text)
            else:
                # Case-insensitive replace
                import re

                pattern = re.compile(re.escape(search_text), re.IGNORECASE)
                new_value = pattern.sub(replace_text, old_str)

            if new_value != old_str:
                self.set_cell_value(sheet_name, cell_ref, new_value)
                count += 1

        return count

    @staticmethod
    def _col_index_to_letter(col: int) -> str:
        """
        Convert column index to letter (A, B, ..., Z, AA, AB, ...).

        Args:
            col: Column index (0-based).

        Returns:
            Column letter(s).
        """
        result = ""
        col += 1  # Convert to 1-based
        while col > 0:
            col -= 1
            result = chr(ord("A") + (col % 26)) + result
            col //= 26
        return result


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
