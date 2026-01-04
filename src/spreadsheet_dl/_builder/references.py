"""
Cell and range reference classes for formula construction.

Implements:
    - FR-BUILDER-005: Formula Builder Enhancement
    - PHASE0-005: Complete FormulaBuilder with 100+ functions

Provides classes for constructing ODF-compliant cell and range references:
- CellRef: Single cell reference with absolute/relative support
- RangeRef: Range reference for contiguous cells
- SheetRef: Sheet reference for cross-sheet formulas
- NamedRange: Named range definition
"""

from __future__ import annotations

from dataclasses import dataclass


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
