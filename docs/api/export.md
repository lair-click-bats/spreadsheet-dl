# export - Multi-Format Export

Multi-format export module for finance tracker, providing export functionality to Excel (XLSX), CSV, PDF, and JSON while preserving formatting where possible.

## Overview

The export module enables exporting ODS spreadsheets to multiple formats:

- **Excel (.xlsx)**: Full formatting preservation with styled headers, borders, and auto-sized columns
- **CSV**: Plain text data export with multi-sheet support
- **PDF**: Formatted reports with tables, headers, and summaries
- **JSON**: Structured data export with metadata

## Key Features

- Multi-format export (XLSX, CSV, PDF, JSON)
- Batch export to multiple formats simultaneously
- Theme and formatting preservation (where supported)
- Progress tracking for large files
- Flexible export options per format
- Sheet filtering and selection

## Classes

### ExportFormat

```python
class ExportFormat(Enum):
    """Supported export formats."""
    XLSX = "xlsx"
    CSV = "csv"
    PDF = "pdf"
    JSON = "json"
```

Enumeration of available export formats.

### ExportOptions

```python
@dataclass
class ExportOptions:
    """Options for export operations."""
    include_headers: bool = True
    include_formulas: bool = False
    preserve_formatting: bool = True
    sheet_names: list[str] | None = None
    active_sheet_only: bool = False
    csv_delimiter: str = ","
    csv_quoting: int = csv.QUOTE_MINIMAL
    csv_encoding: str = "utf-8"
    xlsx_date_format: str = "YYYY-MM-DD"
    xlsx_number_format: str = "#,##0.00"
    xlsx_currency_format: str = '"$"#,##0.00'
    pdf_page_size: str = "letter"
    pdf_orientation: str = "portrait"
    pdf_title: str = ""
    pdf_author: str = "SpreadsheetDL"
    pdf_include_summary: bool = True
```

Configuration options for export operations.

**Attributes:**

- `include_headers`: Include header row in export
- `include_formulas`: Export formula results instead of formulas
- `preserve_formatting`: Preserve styling where possible
- `sheet_names`: List of specific sheets to export (None = all)
- `active_sheet_only`: Export only the active sheet
- `csv_delimiter`: CSV field delimiter
- `csv_quoting`: CSV quoting style
- `csv_encoding`: CSV file encoding
- `xlsx_date_format`: Excel date format string
- `xlsx_number_format`: Excel number format string
- `xlsx_currency_format`: Excel currency format string
- `pdf_page_size`: PDF page size (letter, a4, legal)
- `pdf_orientation`: PDF orientation (portrait, landscape)
- `pdf_title`: PDF document title
- `pdf_author`: PDF author metadata
- `pdf_include_summary`: Include summary section in PDF

### SheetData

```python
@dataclass
class SheetData:
    """Data structure for a spreadsheet sheet."""
    name: str
    rows: list[list[Any]] = field(default_factory=list)
    column_widths: list[int] = field(default_factory=list)
    headers: list[str] = field(default_factory=list)
    styles: dict[str, Any] = field(default_factory=dict)

    @property
    def row_count(self) -> int:
        """Get number of rows."""

    @property
    def column_count(self) -> int:
        """Get number of columns."""
```

Internal representation of sheet data during export.

**Properties:**

- `row_count`: Total number of rows
- `column_count`: Maximum number of columns across all rows

### MultiFormatExporter

```python
class MultiFormatExporter:
    """Export ODS files to multiple formats."""

    def __init__(self, options: ExportOptions | None = None) -> None:
        """Initialize exporter with optional configuration."""

    def export(
        self,
        ods_path: str | Path,
        output_path: str | Path,
        format: ExportFormat | str,
    ) -> Path:
        """Export ODS file to specified format."""

    def export_batch(
        self,
        ods_path: str | Path,
        output_dir: str | Path,
        formats: list[ExportFormat | str],
    ) -> dict[str, Path | None]:
        """Export ODS file to multiple formats."""
```

Main export class supporting multiple output formats.

#### Methods

##### `__init__(options=None)`

Initialize the exporter.

**Parameters:**

- `options` (ExportOptions | None): Export configuration. Uses defaults if None.

##### `export(ods_path, output_path, format)`

Export an ODS file to a specific format.

**Parameters:**

- `ods_path` (str | Path): Path to source ODS file
- `output_path` (str | Path): Path for output file
- `format` (ExportFormat | str): Target format (xlsx, csv, pdf, json)

**Returns:**

- `Path`: Path to the exported file

**Raises:**

- `FileError`: If source file doesn't exist
- `FormatNotSupportedError`: If format is invalid
- `MultiExportError`: If export fails

**Example:**

```python
from spreadsheet_dl.export import MultiFormatExporter, ExportFormat

exporter = MultiFormatExporter()

# Export to Excel
exporter.export("budget.ods", "budget.xlsx", ExportFormat.XLSX)

# Export to CSV
exporter.export("budget.ods", "budget.csv", "csv")

# Export to PDF
exporter.export("budget.ods", "report.pdf", ExportFormat.PDF)
```

##### `export_batch(ods_path, output_dir, formats)`

Export an ODS file to multiple formats simultaneously.

**Parameters:**

- `ods_path` (str | Path): Path to source ODS file
- `output_dir` (str | Path): Directory for output files
- `formats` (list[ExportFormat | str]): List of target formats

**Returns:**

- `dict[str, Path | None]`: Dictionary mapping format names to output paths (None if failed)

**Example:**

```python
results = exporter.export_batch(
    "budget.ods",
    "exports/",
    [ExportFormat.XLSX, ExportFormat.CSV, ExportFormat.PDF]
)

for fmt, path in results.items():
    if path:
        print(f"Exported {fmt}: {path}")
    else:
        print(f"Failed to export {fmt}")
```

## Exceptions

### MultiExportError

```python
class MultiExportError(FinanceTrackerError):
    """Base exception for multi-format export errors."""
    error_code = "FT-MXP-1300"
```

Base exception for all export-related errors.

### FormatNotSupportedError

```python
class FormatNotSupportedError(MultiExportError):
    """Raised when export format is not supported."""
    error_code = "FT-MXP-1301"
```

Raised when attempting to use an unsupported export format.

**Attributes:**

- `format_name`: The invalid format name
- `available_formats`: List of supported formats

### ExportDependencyError

```python
class ExportDependencyError(MultiExportError):
    """Raised when required library for export is not installed."""
    error_code = "FT-MXP-1302"
```

Raised when a required library is missing for a specific format.

**Attributes:**

- `format_name`: The format requiring the library
- `library`: The missing library name

## Convenience Functions

### export_to_xlsx

```python
def export_to_xlsx(
    ods_path: str | Path,
    output_path: str | Path,
    options: ExportOptions | None = None,
) -> Path:
    """Convenience function to export ODS to Excel."""
```

Quick export to Excel format.

**Example:**

```python
from spreadsheet_dl.export import export_to_xlsx

export_to_xlsx("budget.ods", "budget.xlsx")
```

### export_to_csv

```python
def export_to_csv(
    ods_path: str | Path,
    output_path: str | Path,
    options: ExportOptions | None = None,
) -> Path:
    """Convenience function to export ODS to CSV."""
```

Quick export to CSV format.

### export_to_pdf

```python
def export_to_pdf(
    ods_path: str | Path,
    output_path: str | Path,
    options: ExportOptions | None = None,
) -> Path:
    """Convenience function to export ODS to PDF."""
```

Quick export to PDF format.

## Usage Examples

### Basic Export

```python
from spreadsheet_dl.export import MultiFormatExporter, ExportFormat

# Create exporter
exporter = MultiFormatExporter()

# Export to different formats
exporter.export("budget.ods", "budget.xlsx", ExportFormat.XLSX)
exporter.export("budget.ods", "budget.csv", ExportFormat.CSV)
exporter.export("budget.ods", "report.pdf", ExportFormat.PDF)
```

### Custom Export Options

```python
from spreadsheet_dl.export import MultiFormatExporter, ExportOptions

# Configure export options
options = ExportOptions(
    preserve_formatting=True,
    xlsx_currency_format='"$"#,##0.00',
    pdf_orientation="landscape",
    pdf_title="Monthly Budget Report",
    csv_delimiter=";",
)

# Export with custom options
exporter = MultiFormatExporter(options)
exporter.export("budget.ods", "budget.xlsx", "xlsx")
```

### Sheet Selection

```python
# Export only specific sheets
options = ExportOptions(
    sheet_names=["Summary", "Expenses"],
)

exporter = MultiFormatExporter(options)
exporter.export("budget.ods", "summary.xlsx", "xlsx")
```

### Batch Export

```python
# Export to all formats at once
exporter = MultiFormatExporter()

results = exporter.export_batch(
    "budget.ods",
    "exports/",
    ["xlsx", "csv", "pdf", "json"]
)

# Check results
for format_name, path in results.items():
    if path:
        print(f"Successfully exported {format_name} to {path}")
```

### PDF Report Generation

```python
# Generate formatted PDF report
pdf_options = ExportOptions(
    pdf_title="Q4 2024 Financial Report",
    pdf_author="Finance Team",
    pdf_orientation="landscape",
    pdf_page_size="a4",
    pdf_include_summary=True,
)

exporter = MultiFormatExporter(pdf_options)
exporter.export("quarterly_report.ods", "Q4_report.pdf", "pdf")
```

### CSV Export with Custom Delimiter

```python
# Export CSV with semicolon delimiter (European format)
csv_options = ExportOptions(
    csv_delimiter=";",
    csv_encoding="utf-8",
    csv_quoting=csv.QUOTE_MINIMAL,
)

export_to_csv("data.ods", "data.csv", csv_options)
```

## Format-Specific Details

### XLSX Export

- Preserves cell formatting (fonts, colors, borders)
- Auto-adjusts column widths
- Applies styled headers with blue background
- Supports multiple sheets
- Formats currencies and dates properly
- Uses progress bar for large files (>100 rows)

**Dependencies:** Requires `openpyxl` package

### CSV Export

- Plain text format for maximum compatibility
- Multi-sheet files create separate CSVs in subdirectory
- Configurable delimiter and encoding
- Handles currency and date conversions to strings
- Creates combined file for multi-sheet exports

**Dependencies:** Built-in Python `csv` module

### PDF Export

- Creates formatted tables with headers
- Supports multiple sheets in one document
- Configurable page size and orientation
- Adds summary section with metadata
- Styled headers with alternating row colors
- Auto-adjusts table to page width

**Dependencies:** Requires `reportlab` package

### JSON Export

- Structured data with metadata
- Preserves column headers
- Includes sheet information
- ISO date formatting
- Timestamp of export
- Machine-readable format

**Dependencies:** Built-in Python `json` module

## Performance

- **Small files (<100 rows)**: Instant export
- **Medium files (100-1000 rows)**: Progress bar shown, ~1-5 seconds
- **Large files (>1000 rows)**: Progress bar shown, ~5-30 seconds

Progress tracking is automatically enabled for sheets with more than 100 rows.

## Related Modules

- [csv_import](csv_import.md) - Import transactions from CSV files
- [bank_formats](bank_formats.md) - Bank CSV format definitions
- [report_generator](report_generator.md) - Generate reports from data
- [ods_generator](ods_generator.md) - Generate ODS files

## Requirements Implemented

- **FR-EXPORT-001**: Multi-Format Export (Gap G-19)
