"""
Data models for spreadsheet specifications.

Implements:
    - FR-BUILDER-001: Extended SpreadsheetBuilder
    - GAP-002: Missing __slots__ declarations
    - PHASE0-004: Perfect Builder API (v4.0.0)

Provides dataclasses for specifying spreadsheet structure:
- CellSpec: Individual cell specification
- RowSpec: Row specification
- ColumnSpec: Column specification
- SheetSpec: Sheet specification
- WorkbookProperties: Workbook-level metadata
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CellSpec:
    """
    Specification for a single cell.

    Implements GAP-002: Missing __slots__ declarations
    Implements PHASE0-004: Enhanced validation and edge case handling

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

    def __post_init__(self) -> None:
        """Validate cell specification after initialization."""
        if self.colspan < 1:
            raise ValueError(
                f"colspan must be >= 1, got {self.colspan}. "
                "Fix: Use colspan=1 (default) or higher."
            )
        if self.rowspan < 1:
            raise ValueError(
                f"rowspan must be >= 1, got {self.rowspan}. "
                "Fix: Use rowspan=1 (default) or higher."
            )

    def is_empty(self) -> bool:
        """Check if cell has no content."""
        return self.value is None and self.formula is None


@dataclass(slots=True)
class RowSpec:
    """
    Specification for a row.

    Implements GAP-002: Missing __slots__ declarations

    Attributes:
        cells: List of cell specifications
        style: Default style for cells in this row
        height: Row height (optional)
    """

    cells: list[CellSpec] = field(default_factory=list)
    style: str | None = None
    height: str | None = None


@dataclass(slots=True)
class ColumnSpec:
    """
    Specification for a column.

    Implements GAP-002: Missing __slots__ declarations

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


@dataclass(slots=True)
class SheetSpec:
    """
    Specification for a sheet.

    Implements FR-BUILDER-001: Extended sheet properties
    Implements GAP-002: Missing __slots__ declarations

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
