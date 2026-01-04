"""
Format adapters for spreadsheet export/import.

Implements:
    - TASK-403: Format adapters (FR-EXPORT-001)

Provides adapter interfaces for converting between SpreadsheetDL's
internal representation and various file formats.

**Known Limitations:**
    - HTML import: Not yet implemented (HTMLAdapter.from_format raises NotImplementedError)
      HTML export is fully supported. Import requires parsing HTML tables which is planned
      for a future release.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SheetSpec


class ExportFormat(Enum):
    """Supported export formats."""

    ODS = "ods"  # OpenDocument Spreadsheet (native)
    XLSX = "xlsx"  # Microsoft Excel (via openpyxl)
    CSV = "csv"  # Comma-Separated Values
    TSV = "tsv"  # Tab-Separated Values
    HTML = "html"  # HTML table
    JSON = "json"  # JSON data
    PDF = "pdf"  # PDF (future)


class ImportFormat(Enum):
    """Supported import formats."""

    ODS = "ods"  # OpenDocument Spreadsheet
    XLSX = "xlsx"  # Microsoft Excel
    CSV = "csv"  # Comma-Separated Values
    TSV = "tsv"  # Tab-Separated Values
    JSON = "json"  # JSON data


@dataclass
class AdapterOptions:
    """
    Configuration options for format adapters.

    Attributes:
        include_headers: Include column headers in export
        include_styles: Export style information
        include_formulas: Export formulas (vs computed values)
        include_charts: Export chart definitions
        encoding: Text encoding for CSV/TSV
        delimiter: Field delimiter for CSV/TSV
        quote_char: Quote character for CSV/TSV
        date_format: Date format string
        decimal_places: Number of decimal places for numbers
        sheet_names: Specific sheets to export (None for all)
    """

    include_headers: bool = True
    include_styles: bool = True
    include_formulas: bool = True
    include_charts: bool = True
    encoding: str = "utf-8"
    delimiter: str = ","
    quote_char: str = '"'
    date_format: str = "%Y-%m-%d"
    decimal_places: int = 2
    sheet_names: list[str] | None = None


class FormatAdapter(ABC):
    """
    Abstract base class for format adapters.

    Implements TASK-403: Format adapter interface (FR-EXPORT-001)

    Subclasses implement specific format conversions.
    """

    @property
    @abstractmethod
    def format_name(self) -> str:
        """Return the adapter's format name."""
        ...  # pragma: no cover

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """Return the file extension for this format."""
        ...  # pragma: no cover

    @abstractmethod
    def export(
        self,
        sheets: list[SheetSpec],
        output_path: Path,
        options: AdapterOptions | None = None,
    ) -> Path:
        """
        Export sheets to file.

        Args:
            sheets: Sheet specifications to export
            output_path: Output file path
            options: Export options

        Returns:
            Path to created file
        """
        ...  # pragma: no cover

    @abstractmethod
    def import_file(
        self,
        input_path: Path,
        options: AdapterOptions | None = None,
    ) -> list[SheetSpec]:
        """
        Import sheets from file.

        Args:
            input_path: Input file path
            options: Import options

        Returns:
            List of imported sheet specifications
        """
        ...  # pragma: no cover


class OdsAdapter(FormatAdapter):
    """
    ODS format adapter (native format).

    Uses odfpy for ODS file operations.
    """

    @property
    def format_name(self) -> str:
        """Return format name."""
        return "OpenDocument Spreadsheet"

    @property
    def file_extension(self) -> str:
        """Return file extension."""
        return ".ods"

    def export(
        self,
        sheets: list[SheetSpec],
        output_path: Path,
        options: AdapterOptions | None = None,
    ) -> Path:
        """Export to ODS format."""
        from spreadsheet_dl.renderer import render_sheets

        return render_sheets(sheets, output_path)

    def import_file(
        self,
        input_path: Path,
        options: AdapterOptions | None = None,
    ) -> list[SheetSpec]:
        """Import from ODS format."""
        from spreadsheet_dl.builder import CellSpec, ColumnSpec, RowSpec, SheetSpec
        from spreadsheet_dl.streaming import StreamingReader

        sheets = []
        with StreamingReader(input_path) as reader:
            for sheet_name in reader.sheet_names():
                rows = []
                col_count = reader.column_count(sheet_name)
                columns = [ColumnSpec(name=f"Col{i + 1}") for i in range(col_count)]

                for streaming_row in reader.rows(sheet_name):
                    cells = []
                    for cell in streaming_row.cells:
                        cells.append(
                            CellSpec(
                                value=cell.value,
                                value_type=cell.value_type,
                                formula=cell.formula,
                                style=cell.style,
                            )
                        )
                    rows.append(RowSpec(cells=cells, style=streaming_row.style))

                sheets.append(SheetSpec(name=sheet_name, columns=columns, rows=rows))

        return sheets


class CsvAdapter(FormatAdapter):
    """
    CSV format adapter.

    Handles comma-separated values export/import.
    """

    @property
    def format_name(self) -> str:
        """Return format name."""
        return "Comma-Separated Values"

    @property
    def file_extension(self) -> str:
        """Return file extension."""
        return ".csv"

    def export(
        self,
        sheets: list[SheetSpec],
        output_path: Path,
        options: AdapterOptions | None = None,
    ) -> Path:
        """Export to CSV format."""
        import csv

        options = options or AdapterOptions()
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # CSV only supports single sheet - use first sheet or specified
        sheet = sheets[0] if sheets else None
        if options.sheet_names and sheets:
            for s in sheets:
                if s.name in options.sheet_names:
                    sheet = s
                    break

        if sheet is None:
            # Create empty file
            output_path.write_text("")
            return output_path

        with output_path.open("w", encoding=options.encoding, newline="") as f:
            writer = csv.writer(
                f,
                delimiter=options.delimiter,
                quotechar=options.quote_char,
            )

            # Write header row if present
            if options.include_headers and sheet.columns:
                writer.writerow([col.name for col in sheet.columns])

            # Write data rows
            for row in sheet.rows:
                values = []
                for cell in row.cells:
                    value = self._format_value(cell.value, options)
                    values.append(value)
                writer.writerow(values)

        return output_path

    def import_file(
        self,
        input_path: Path,
        options: AdapterOptions | None = None,
    ) -> list[SheetSpec]:
        """Import from CSV format."""
        import csv

        from spreadsheet_dl.builder import CellSpec, ColumnSpec, RowSpec, SheetSpec

        options = options or AdapterOptions()
        input_path = Path(input_path)

        rows = []
        columns = []

        with input_path.open("r", encoding=options.encoding) as f:
            reader = csv.reader(
                f,
                delimiter=options.delimiter,
                quotechar=options.quote_char,
            )

            for row_idx, csv_row in enumerate(reader):
                if row_idx == 0 and options.include_headers:
                    # First row is headers
                    columns = [ColumnSpec(name=col) for col in csv_row]
                else:
                    cells = [CellSpec(value=val) for val in csv_row]
                    rows.append(RowSpec(cells=cells))

        # If no headers, create generic columns
        if not columns and rows:
            max_cols = max(len(row.cells) for row in rows)
            columns = [ColumnSpec(name=f"Column{i + 1}") for i in range(max_cols)]

        sheet_name = input_path.stem
        return [SheetSpec(name=sheet_name, columns=columns, rows=rows)]

    def _format_value(self, value: Any, options: AdapterOptions) -> str:
        """Format a cell value for CSV export."""
        if value is None:
            return ""
        if isinstance(value, (datetime, date)):
            return value.strftime(options.date_format)
        if isinstance(value, (float, Decimal)):
            return f"{value:.{options.decimal_places}f}"
        return str(value)


class TsvAdapter(CsvAdapter):
    """
    TSV format adapter.

    Handles tab-separated values export/import.
    """

    @property
    def format_name(self) -> str:
        """Return format name."""
        return "Tab-Separated Values"

    @property
    def file_extension(self) -> str:
        """Return file extension."""
        return ".tsv"

    def export(
        self,
        sheets: list[SheetSpec],
        output_path: Path,
        options: AdapterOptions | None = None,
    ) -> Path:
        """Export to TSV format."""
        options = options or AdapterOptions()
        options.delimiter = "\t"
        return super().export(sheets, output_path, options)

    def import_file(
        self,
        input_path: Path,
        options: AdapterOptions | None = None,
    ) -> list[SheetSpec]:
        """Import from TSV format."""
        options = options or AdapterOptions()
        options.delimiter = "\t"
        return super().import_file(input_path, options)


class JsonAdapter(FormatAdapter):
    """
    JSON format adapter.

    Exports spreadsheet data as JSON for programmatic access.
    """

    @property
    def format_name(self) -> str:
        """Return format name."""
        return "JSON Data"

    @property
    def file_extension(self) -> str:
        """Return file extension."""
        return ".json"

    def export(
        self,
        sheets: list[SheetSpec],
        output_path: Path,
        options: AdapterOptions | None = None,
    ) -> Path:
        """Export to JSON format."""
        from spreadsheet_dl.serialization import Serializer

        serializer = Serializer()
        return serializer.save_json(sheets, output_path)

    def import_file(
        self,
        input_path: Path,
        options: AdapterOptions | None = None,
    ) -> list[SheetSpec]:
        """Import from JSON format."""
        from spreadsheet_dl.serialization import Serializer

        serializer = Serializer()
        data = serializer.load_json(input_path)

        if isinstance(data, list):
            return data
        return [data] if data else []


class HtmlAdapter(FormatAdapter):
    """
    HTML format adapter.

    Exports spreadsheet as HTML table(s).
    """

    @property
    def format_name(self) -> str:
        """Return format name."""
        return "HTML Table"

    @property
    def file_extension(self) -> str:
        """Return file extension."""
        return ".html"

    def export(
        self,
        sheets: list[SheetSpec],
        output_path: Path,
        options: AdapterOptions | None = None,
    ) -> Path:
        """Export to HTML format."""
        options = options or AdapterOptions()
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        html_parts = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            '<meta charset="utf-8">',
            "<title>Spreadsheet Export</title>",
            "<style>",
            "table { border-collapse: collapse; margin: 20px 0; }",
            "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
            "th { background-color: #4472C4; color: white; }",
            "tr:nth-child(even) { background-color: #f2f2f2; }",
            "</style>",
            "</head>",
            "<body>",
        ]

        for sheet in sheets:
            if options.sheet_names and sheet.name not in options.sheet_names:
                continue

            html_parts.append(f"<h2>{self._escape_html(sheet.name)}</h2>")
            html_parts.append("<table>")

            # Header row
            if options.include_headers and sheet.columns:
                html_parts.append("<thead><tr>")
                for col in sheet.columns:
                    html_parts.append(f"<th>{self._escape_html(col.name)}</th>")
                html_parts.append("</tr></thead>")

            # Data rows
            html_parts.append("<tbody>")
            for row in sheet.rows:
                html_parts.append("<tr>")
                for cell in row.cells:
                    value = self._format_value(cell.value, options)
                    html_parts.append(f"<td>{self._escape_html(value)}</td>")
                html_parts.append("</tr>")
            html_parts.append("</tbody>")

            html_parts.append("</table>")

        html_parts.extend(["</body>", "</html>"])

        output_path.write_text("\n".join(html_parts), encoding="utf-8")
        return output_path

    def import_file(
        self,
        input_path: Path,
        options: AdapterOptions | None = None,
    ) -> list[SheetSpec]:
        """Import from HTML format (not implemented)."""
        raise NotImplementedError("HTML import is not yet supported")

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (
            str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def _format_value(self, value: Any, options: AdapterOptions) -> str:
        """Format a cell value for HTML export."""
        if value is None:
            return ""
        if isinstance(value, (datetime, date)):
            return value.strftime(options.date_format)
        if isinstance(value, (float, Decimal)):
            return f"{value:.{options.decimal_places}f}"
        return str(value)


class AdapterRegistry:
    """
    Registry of available format adapters.

    Implements TASK-403: Format adapter registry (FR-EXPORT-001)

    Provides discovery and instantiation of format adapters.

    Examples:
        # Get adapter by format
        adapter = AdapterRegistry.get_adapter(ExportFormat.CSV)
        adapter.export(sheets, "output.csv")

        # List available formats
        formats = AdapterRegistry.list_formats()

        # Export to any format
        AdapterRegistry.export(sheets, "output.xlsx", ExportFormat.XLSX)
    """

    _adapters: ClassVar[dict[ExportFormat, type[FormatAdapter]]] = {
        ExportFormat.ODS: OdsAdapter,
        ExportFormat.CSV: CsvAdapter,
        ExportFormat.TSV: TsvAdapter,
        ExportFormat.JSON: JsonAdapter,
        ExportFormat.HTML: HtmlAdapter,
    }

    @classmethod
    def get_adapter(cls, format: ExportFormat) -> FormatAdapter:
        """
        Get adapter instance for format.

        Args:
            format: Export format

        Returns:
            FormatAdapter instance

        Raises:
            ValueError: If format not supported
        """
        adapter_class = cls._adapters.get(format)
        if adapter_class is None:
            raise ValueError(f"Unsupported format: {format}")
        return adapter_class()

    @classmethod
    def register_adapter(
        cls,
        format: ExportFormat,
        adapter_class: type[FormatAdapter],
    ) -> None:
        """
        Register a new adapter.

        Args:
            format: Format to register
            adapter_class: Adapter class
        """
        cls._adapters[format] = adapter_class

    @classmethod
    def list_formats(cls) -> list[ExportFormat]:
        """List available export formats."""
        return list(cls._adapters.keys())

    @classmethod
    def export(
        cls,
        sheets: list[SheetSpec],
        output_path: Path | str,
        format: ExportFormat | None = None,
        options: AdapterOptions | None = None,
    ) -> Path:
        """
        Export sheets to file.

        Args:
            sheets: Sheet specifications
            output_path: Output file path
            format: Export format (auto-detect from extension if None)
            options: Export options

        Returns:
            Path to created file
        """
        path = Path(output_path)

        if format is None:
            # Auto-detect from extension
            ext = path.suffix.lower()
            format_map = {
                ".ods": ExportFormat.ODS,
                ".csv": ExportFormat.CSV,
                ".tsv": ExportFormat.TSV,
                ".json": ExportFormat.JSON,
                ".html": ExportFormat.HTML,
                ".htm": ExportFormat.HTML,
            }
            format = format_map.get(ext, ExportFormat.ODS)

        adapter = cls.get_adapter(format)
        return adapter.export(sheets, path, options)

    @classmethod
    def import_file(
        cls,
        input_path: Path | str,
        format: ImportFormat | None = None,
        options: AdapterOptions | None = None,
    ) -> list[SheetSpec]:
        """
        Import sheets from file.

        Args:
            input_path: Input file path
            format: Import format (auto-detect from extension if None)
            options: Import options

        Returns:
            List of imported sheet specifications
        """
        path = Path(input_path)

        if format is None:
            # Auto-detect from extension
            ext = path.suffix.lower()
            format_map = {
                ".ods": ExportFormat.ODS,
                ".csv": ExportFormat.CSV,
                ".tsv": ExportFormat.TSV,
                ".json": ExportFormat.JSON,
            }
            export_format = format_map.get(ext, ExportFormat.ODS)
        else:
            export_format = ExportFormat(format.value)

        adapter = cls.get_adapter(export_format)
        return adapter.import_file(path, options)


# Convenience functions


def export_to(
    sheets: list[SheetSpec],
    output_path: Path | str,
    format: ExportFormat | str | None = None,
    **kwargs: Any,
) -> Path:
    """
    Export sheets to file.

    Convenience function for AdapterRegistry.export().

    Args:
        sheets: Sheet specifications
        output_path: Output file path
        format: Export format (string or enum)
        **kwargs: Additional options for AdapterOptions

    Returns:
        Path to created file
    """
    if isinstance(format, str):
        format = ExportFormat(format)

    options = AdapterOptions(**kwargs) if kwargs else None
    return AdapterRegistry.export(sheets, output_path, format, options)


def import_from(
    input_path: Path | str,
    format: ImportFormat | str | None = None,
    **kwargs: Any,
) -> list[SheetSpec]:
    """
    Import sheets from file.

    Convenience function for AdapterRegistry.import_file().

    Args:
        input_path: Input file path
        format: Import format (string or enum)
        **kwargs: Additional options for AdapterOptions

    Returns:
        List of imported sheet specifications
    """
    if isinstance(format, str):
        format = ImportFormat(format)

    options = AdapterOptions(**kwargs) if kwargs else None
    return AdapterRegistry.import_file(input_path, format, options)
