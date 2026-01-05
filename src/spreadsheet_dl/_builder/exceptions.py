"""
Builder-specific exceptions with actionable error messages.

All builder exceptions inherit from BuilderError which provides
enhanced error messages with actionable guidance for developers.
"""

from __future__ import annotations

from spreadsheet_dl.exceptions import SpreadsheetDLError


class BuilderError(SpreadsheetDLError):
    """Base exception for builder errors with actionable messages."""

    pass


class NoSheetSelectedError(BuilderError):
    """Raised when sheet operation attempted without active sheet."""

    def __init__(self, operation: str) -> None:
        """
        Initialize with operation context.

        Args:
            operation: The operation that was attempted
        """
        super().__init__(
            f"Cannot {operation}: no sheet is currently selected.\n"
            f"Fix: Call .sheet('SheetName') first to create or select a sheet."
        )


class NoRowSelectedError(BuilderError):
    """Raised when row operation attempted without active row."""

    def __init__(self, operation: str) -> None:
        """
        Initialize with operation context.

        Args:
            operation: The operation that was attempted
        """
        super().__init__(
            f"Cannot {operation}: no row is currently active.\n"
            f"Fix: Call .row() first to create a new row, or use .header_row() or .data_rows()."
        )


class InvalidRangeError(BuilderError):
    """Raised when an invalid range is provided."""

    def __init__(self, range_ref: str, reason: str) -> None:
        """
        Initialize with range and reason.

        Args:
            range_ref: The invalid range reference
            reason: Why it's invalid
        """
        super().__init__(
            f"Invalid range '{range_ref}': {reason}\n"
            f"Fix: Use a valid range format like 'A1:B10' or 'Sheet1.A1:B10'."
        )


class EmptySheetError(BuilderError):
    """Raised when attempting to build with empty/invalid sheet."""

    def __init__(self, sheet_name: str, reason: str) -> None:
        """
        Initialize with sheet context.

        Args:
            sheet_name: Name of the problematic sheet
            reason: What's wrong with the sheet
        """
        super().__init__(
            f"Sheet '{sheet_name}' cannot be built: {reason}\n"
            f"Fix: Add columns and rows to the sheet, or remove it from the builder."
        )


class CircularReferenceError(BuilderError):
    """
    Error raised when circular references are detected in formulas.

    Attributes:
        cell: The cell that contains the circular reference
        cycle: List of cells forming the circular dependency
    """

    def __init__(self, cell: str, cycle: list[str]) -> None:
        self.cell = cell
        self.cycle = cycle
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        cycle_str = " -> ".join(self.cycle)
        return (
            f"Circular reference detected at {self.cell}: {cycle_str}\n"
            f"Fix: Remove the circular dependency by breaking the reference chain."
        )
