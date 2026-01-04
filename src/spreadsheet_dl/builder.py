"""
Fluent builder API for spreadsheet construction.

Implements:
    - FR-BUILDER-001: Extended SpreadsheetBuilder
    - FR-BUILDER-004: ChartBuilder (via charts module)
    - FR-BUILDER-005: Formula Builder Enhancement
    - GAP-FORMULA-001: Circular reference detection (TASK-204)
    - PHASE0-004: Perfect Builder API (v4.0.0)

Public API entry point for the builder functionality.
Implementation is modularized in the _builder package.

Provides a declarative, chainable API for building spreadsheets:
- SpreadsheetBuilder: Main builder for creating sheets
- SheetBuilder: Builder for individual sheets
- FormulaBuilder: Type-safe formula construction
- ChartBuilder: Fluent chart creation (from charts module)
- FormulaDependencyGraph: Circular reference detection

Features in v4.0.0:
- Enhanced error messages with actionable guidance
- Improved edge case handling (empty sheets, invalid ranges)
- Consistent method signatures across all builders
- Better type safety and validation
- Optimized developer experience
"""

from __future__ import annotations

# Public API: Re-export everything from the _builder package
from spreadsheet_dl._builder import (
    BuilderError,
    CellRef,
    CellSpec,
    CircularReferenceError,
    ColumnSpec,
    EmptySheetError,
    FormulaBuilder,
    FormulaDependencyGraph,
    InvalidRangeError,
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

__all__ = [
    "BuilderError",
    "CellRef",
    "CellSpec",
    "CircularReferenceError",
    "ColumnSpec",
    "EmptySheetError",
    "FormulaBuilder",
    "FormulaDependencyGraph",
    "InvalidRangeError",
    "NamedRange",
    "NoRowSelectedError",
    "NoSheetSelectedError",
    "RangeRef",
    "RowSpec",
    "SheetRef",
    "SheetSpec",
    "SpreadsheetBuilder",
    "WorkbookProperties",
    "create_spreadsheet",
    "formula",
]
