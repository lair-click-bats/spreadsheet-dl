"""
ODS Renderer - Converts builder specifications to ODS files.

This module bridges the builder API with odfpy, translating
theme-based styles and sheet specifications into actual ODS documents.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING, Any

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TableCellProperties, TableColumnProperties, TextProperties
from odf.table import Table, TableCell, TableColumn, TableRow
from odf.text import P

if TYPE_CHECKING:
    from finance_tracker.builder import CellSpec, ColumnSpec, RowSpec, SheetSpec
    from finance_tracker.schema.styles import CellStyle, Theme


class OdsRenderer:
    """
    Render sheet specifications to ODS files.

    Handles:
    - Theme-based style generation
    - Cell formatting (currency, date, percentage)
    - Formula rendering
    - Multi-sheet documents
    """

    def __init__(self, theme: Theme | None = None) -> None:
        """
        Initialize renderer with optional theme.

        Args:
            theme: Theme for styling (None for default styles)
        """
        self._theme = theme
        self._doc: OpenDocumentSpreadsheet | None = None
        self._styles: dict[str, Style] = {}
        self._style_counter = 0

    def render(self, sheets: list[SheetSpec], output_path: Path) -> Path:
        """
        Render sheets to ODS file.

        Args:
            sheets: List of sheet specifications
            output_path: Output file path

        Returns:
            Path to created file
        """
        self._doc = OpenDocumentSpreadsheet()
        self._styles.clear()
        self._style_counter = 0

        # Create default styles
        self._create_default_styles()

        # Create theme-based styles if theme provided
        if self._theme:
            self._create_theme_styles()

        # Render each sheet
        for sheet_spec in sheets:
            self._render_sheet(sheet_spec)

        # Save document
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self._doc.save(str(output_path))
        return output_path

    def _create_default_styles(self) -> None:
        """Create default cell styles."""
        if self._doc is None:
            return

        # Default header style
        header_style = Style(name="DefaultHeader", family="table-cell")
        header_style.addElement(
            TableCellProperties(backgroundcolor="#4472C4", padding="2pt")
        )
        header_style.addElement(TextProperties(fontweight="bold", color="#FFFFFF"))
        self._doc.automaticstyles.addElement(header_style)
        self._styles["header"] = header_style
        self._styles["header_primary"] = header_style

        # Currency style
        currency_style = Style(name="DefaultCurrency", family="table-cell")
        currency_style.addElement(TableCellProperties(padding="2pt"))
        self._doc.automaticstyles.addElement(currency_style)
        self._styles["currency"] = currency_style
        self._styles["cell_currency"] = currency_style

        # Date style
        date_style = Style(name="DefaultDate", family="table-cell")
        date_style.addElement(TableCellProperties(padding="2pt"))
        self._doc.automaticstyles.addElement(date_style)
        self._styles["date"] = date_style
        self._styles["cell_date"] = date_style

        # Warning style (over budget)
        warning_style = Style(name="DefaultWarning", family="table-cell")
        warning_style.addElement(
            TableCellProperties(backgroundcolor="#FFC7CE", padding="2pt")
        )
        warning_style.addElement(TextProperties(color="#9C0006"))
        self._doc.automaticstyles.addElement(warning_style)
        self._styles["warning"] = warning_style
        self._styles["cell_warning"] = warning_style
        self._styles["cell_danger"] = warning_style

        # Success style (under budget)
        good_style = Style(name="DefaultGood", family="table-cell")
        good_style.addElement(
            TableCellProperties(backgroundcolor="#C6EFCE", padding="2pt")
        )
        good_style.addElement(TextProperties(color="#006100"))
        self._doc.automaticstyles.addElement(good_style)
        self._styles["good"] = good_style
        self._styles["cell_success"] = good_style

        # Normal cell style
        normal_style = Style(name="DefaultNormal", family="table-cell")
        normal_style.addElement(TableCellProperties(padding="2pt"))
        self._doc.automaticstyles.addElement(normal_style)
        self._styles["normal"] = normal_style
        self._styles["cell_normal"] = normal_style
        self._styles["default"] = normal_style

        # Total row style
        total_style = Style(name="DefaultTotal", family="table-cell")
        total_style.addElement(
            TableCellProperties(backgroundcolor="#4472C4", padding="2pt")
        )
        total_style.addElement(
            TextProperties(fontweight="bold", color="#FFFFFF", fontsize="11pt")
        )
        self._doc.automaticstyles.addElement(total_style)
        self._styles["total"] = total_style
        self._styles["total_row"] = total_style

    def _create_theme_styles(self) -> None:
        """Create styles from theme definitions."""
        if self._doc is None or self._theme is None:
            return

        for style_name in self._theme.list_styles():
            try:
                cell_style = self._theme.get_style(style_name)
                odf_style = self._create_odf_style(style_name, cell_style)
                self._doc.automaticstyles.addElement(odf_style)
                self._styles[style_name] = odf_style
            except Exception:
                # Skip styles that fail to resolve
                pass

    def _create_odf_style(self, name: str, cell_style: CellStyle) -> Style:
        """
        Create ODF style from CellStyle.

        Args:
            name: Style name
            cell_style: CellStyle from theme

        Returns:
            ODF Style object
        """
        self._style_counter += 1
        style = Style(name=f"Theme_{name}_{self._style_counter}", family="table-cell")

        # Cell properties
        cell_props: dict[str, Any] = {}

        if cell_style.background_color:
            cell_props["backgroundcolor"] = str(cell_style.background_color)

        if cell_style.padding:
            cell_props["padding"] = cell_style.padding

        # Borders
        if cell_style.border_top:
            cell_props["bordertop"] = cell_style.border_top.to_odf()
        if cell_style.border_bottom:
            cell_props["borderbottom"] = cell_style.border_bottom.to_odf()
        if cell_style.border_left:
            cell_props["borderleft"] = cell_style.border_left.to_odf()
        if cell_style.border_right:
            cell_props["borderright"] = cell_style.border_right.to_odf()

        if cell_props:
            style.addElement(TableCellProperties(**cell_props))

        # Text properties
        text_props: dict[str, Any] = {}

        if cell_style.font.family:
            text_props["fontfamily"] = cell_style.font.family

        if cell_style.font.size:
            text_props["fontsize"] = cell_style.font.size

        if cell_style.font.weight.value == "bold":
            text_props["fontweight"] = "bold"

        if cell_style.font.color:
            text_props["color"] = str(cell_style.font.color)

        if cell_style.font.italic:
            text_props["fontstyle"] = "italic"

        if text_props:
            style.addElement(TextProperties(**text_props))

        return style

    def _render_sheet(self, sheet_spec: SheetSpec) -> None:
        """
        Render a single sheet.

        Args:
            sheet_spec: Sheet specification
        """
        if self._doc is None:
            return

        table = Table(name=sheet_spec.name)

        # Add columns with widths
        for col_spec in sheet_spec.columns:
            col_style = self._create_column_style(col_spec)
            table.addElement(TableColumn(stylename=col_style))

        # Add rows
        for row_spec in sheet_spec.rows:
            row = self._render_row(row_spec, sheet_spec.columns)
            table.addElement(row)

        self._doc.spreadsheet.addElement(table)

    def _create_column_style(self, col_spec: ColumnSpec) -> Style:
        """Create column style with width."""
        if self._doc is None:
            raise ValueError("Document not initialized")

        self._style_counter += 1
        col_style = Style(name=f"Col_{self._style_counter}", family="table-column")
        col_style.addElement(TableColumnProperties(columnwidth=col_spec.width))
        self._doc.automaticstyles.addElement(col_style)
        return col_style

    def _render_row(self, row_spec: RowSpec, columns: list[ColumnSpec]) -> TableRow:
        """
        Render a single row.

        Args:
            row_spec: Row specification
            columns: Column specifications for type info

        Returns:
            ODF TableRow
        """
        row = TableRow()

        for i, cell_spec in enumerate(row_spec.cells):
            col_spec = columns[i] if i < len(columns) else None
            cell = self._render_cell(cell_spec, row_spec.style, col_spec)
            row.addElement(cell)

        return row

    def _render_cell(
        self,
        cell_spec: CellSpec,
        row_style: str | None,
        col_spec: ColumnSpec | None,
    ) -> TableCell:
        """
        Render a single cell.

        Args:
            cell_spec: Cell specification
            row_style: Default row style
            col_spec: Column specification for type info

        Returns:
            ODF TableCell
        """
        # Determine style
        style_name = cell_spec.style or row_style
        if style_name and style_name in self._styles:
            style = self._styles[style_name]
        else:
            style = self._styles.get("default")

        # Determine value type
        value_type = cell_spec.value_type
        if not value_type and col_spec:
            value_type = col_spec.type

        # Create cell with appropriate type
        cell_kwargs: dict[str, Any] = {}

        if style:
            cell_kwargs["stylename"] = style

        if cell_spec.formula:
            cell_kwargs["formula"] = cell_spec.formula
            cell_kwargs["valuetype"] = self._get_odf_value_type(value_type)

        elif cell_spec.value is not None:
            cell_kwargs.update(self._get_value_attrs(cell_spec.value, value_type))

        cell = TableCell(**cell_kwargs)

        # Add display text
        display_text = self._get_display_text(cell_spec.value, value_type)
        if display_text:
            cell.addElement(P(text=display_text))

        return cell

    def _get_odf_value_type(self, type_hint: str | None) -> str:
        """Map type hint to ODF value type."""
        type_map = {
            "string": "string",
            "currency": "currency",
            "date": "date",
            "percentage": "percentage",
            "float": "float",
            "number": "float",
        }
        return type_map.get(type_hint or "", "string")

    def _get_value_attrs(
        self,
        value: Any,
        type_hint: str | None,
    ) -> dict[str, Any]:
        """Get ODF attributes for a cell value."""
        attrs: dict[str, Any] = {}

        if value is None:
            return attrs

        if isinstance(value, date):
            attrs["valuetype"] = "date"
            attrs["datevalue"] = value.isoformat()
        elif isinstance(value, datetime):
            attrs["valuetype"] = "date"
            attrs["datevalue"] = value.date().isoformat()
        elif isinstance(value, Decimal):
            attrs["valuetype"] = "currency" if type_hint == "currency" else "float"
            attrs["value"] = str(value)
        elif isinstance(value, (int, float)):
            if type_hint == "currency":
                attrs["valuetype"] = "currency"
            elif type_hint == "percentage":
                attrs["valuetype"] = "percentage"
            else:
                attrs["valuetype"] = "float"
            attrs["value"] = str(value)
        else:
            attrs["valuetype"] = "string"

        return attrs

    def _get_display_text(self, value: Any, type_hint: str | None) -> str:
        """Get display text for a cell value."""
        if value is None:
            return ""

        if isinstance(value, date):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, datetime):
            return value.date().strftime("%Y-%m-%d")
        elif isinstance(value, (Decimal, float)):
            if type_hint == "currency":
                return f"${value:,.2f}"
            elif type_hint == "percentage":
                return f"{value:.1%}"
            return str(value)
        elif isinstance(value, int):
            if type_hint == "currency":
                return f"${value:,}"
            return str(value)

        return str(value)


def render_sheets(
    sheets: list[SheetSpec],
    output_path: Path | str,
    theme: Theme | None = None,
) -> Path:
    """
    Convenience function to render sheets to ODS.

    Args:
        sheets: Sheet specifications
        output_path: Output file path
        theme: Optional theme

    Returns:
        Path to created file
    """
    renderer = OdsRenderer(theme)
    return renderer.render(sheets, Path(output_path))
