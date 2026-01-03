# Adapters API Reference

Format adapters for spreadsheet export/import.

**Implements:** TASK-403 (Format adapters)

## Overview

The adapters module provides:

- Unified interface for importing/exporting multiple formats
- Format adapters: ODS, CSV, TSV, JSON, HTML
- Auto-detection of file format from extension
- Configurable export/import options

## Classes

### AdapterRegistry

Registry of available format adapters.

```python
from spreadsheet_dl.adapters import AdapterRegistry, ExportFormat

# Get adapter by format
adapter = AdapterRegistry.get_adapter(ExportFormat.CSV)
adapter.export(sheets, "output.csv")

# List available formats
formats = AdapterRegistry.list_formats()
# [ExportFormat.ODS, ExportFormat.CSV, ExportFormat.TSV, ...]

# Export to any format (auto-detect from extension)
AdapterRegistry.export(sheets, "output.xlsx")

# Import from any format
sheets = AdapterRegistry.import_file("data.csv")
```

#### Class Methods

##### `get_adapter()`

Get adapter instance for format.

```python
adapter = AdapterRegistry.get_adapter(format: ExportFormat)
```

**Raises:** `ValueError` if format not supported

##### `register_adapter()`

Register a new adapter.

```python
AdapterRegistry.register_adapter(
    format: ExportFormat,
    adapter_class: type[FormatAdapter]
)
```

##### `list_formats()`

List available export formats.

```python
formats = AdapterRegistry.list_formats()
# [ExportFormat.ODS, ExportFormat.CSV, ExportFormat.TSV, ...]
```

##### `export()`

Export sheets to file.

```python
path = AdapterRegistry.export(
    sheets: list[SheetSpec],
    output_path: Path | str,
    format: ExportFormat | None = None,  # Auto-detect if None
    options: AdapterOptions | None = None
)
```

##### `import_file()`

Import sheets from file.

```python
sheets = AdapterRegistry.import_file(
    input_path: Path | str,
    format: ImportFormat | None = None,  # Auto-detect if None
    options: AdapterOptions | None = None
)
```

---

### FormatAdapter

Abstract base class for format adapters.

```python
from spreadsheet_dl.adapters import FormatAdapter
from abc import abstractmethod

class CustomAdapter(FormatAdapter):
    @property
    def format_name(self) -> str:
        return "Custom Format"

    @property
    def file_extension(self) -> str:
        return ".custom"

    def export(self, sheets, output_path, options=None):
        # Implementation
        pass

    def import_file(self, input_path, options=None):
        # Implementation
        pass
```

#### Abstract Properties

| Property         | Type  | Description                   |
| ---------------- | ----- | ----------------------------- |
| `format_name`    | `str` | Human-readable format name    |
| `file_extension` | `str` | File extension (e.g., ".csv") |

#### Abstract Methods

| Method                                 | Description             |
| -------------------------------------- | ----------------------- |
| `export(sheets, output_path, options)` | Export sheets to file   |
| `import_file(input_path, options)`     | Import sheets from file |

---

### AdapterOptions

Configuration options for format adapters.

```python
from spreadsheet_dl.adapters import AdapterOptions

options = AdapterOptions(
    include_headers=True,
    include_styles=True,
    include_formulas=True,
    include_charts=True,
    encoding="utf-8",
    delimiter=",",
    quote_char='"',
    date_format="%Y-%m-%d",
    decimal_places=2,
    sheet_names=["Sheet1", "Sheet2"]  # None for all
)
```

#### Attributes

| Attribute          | Type       | Default    | Description                 |
| ------------------ | ---------- | ---------- | --------------------------- | ------------------------- |
| `include_headers`  | `bool`     | True       | Include column headers      |
| `include_styles`   | `bool`     | True       | Export style information    |
| `include_formulas` | `bool`     | True       | Export formulas vs values   |
| `include_charts`   | `bool`     | True       | Export chart definitions    |
| `encoding`         | `str`      | "utf-8"    | Text encoding for CSV/TSV   |
| `delimiter`        | `str`      | ","        | Field delimiter for CSV/TSV |
| `quote_char`       | `str`      | '"'        | Quote character for CSV/TSV |
| `date_format`      | `str`      | "%Y-%m-%d" | Date format string          |
| `decimal_places`   | `int`      | 2          | Decimal places for numbers  |
| `sheet_names`      | `list[str] | None`      | None                        | Specific sheets to export |

---

### Built-in Adapters

#### OdsAdapter

Native ODS format adapter.

```python
from spreadsheet_dl.adapters import OdsAdapter

adapter = OdsAdapter()
adapter.export(sheets, "output.ods")
sheets = adapter.import_file("input.ods")
```

#### CsvAdapter

CSV format adapter.

```python
from spreadsheet_dl.adapters import CsvAdapter, AdapterOptions

adapter = CsvAdapter()

# Custom options
options = AdapterOptions(
    delimiter=";",  # Semicolon-separated
    encoding="utf-8-sig"  # UTF-8 with BOM
)

adapter.export(sheets, "output.csv", options)
sheets = adapter.import_file("input.csv", options)
```

**Note:** CSV only supports single sheet. First sheet or specified sheet is exported.

#### TsvAdapter

Tab-separated values adapter.

```python
from spreadsheet_dl.adapters import TsvAdapter

adapter = TsvAdapter()
adapter.export(sheets, "output.tsv")
```

Inherits from CsvAdapter with tab delimiter.

#### JsonAdapter

JSON data format adapter.

```python
from spreadsheet_dl.adapters import JsonAdapter

adapter = JsonAdapter()
adapter.export(sheets, "output.json")
sheets = adapter.import_file("input.json")
```

Uses Serializer for type-preserving JSON.

#### HtmlAdapter

HTML table format adapter.

```python
from spreadsheet_dl.adapters import HtmlAdapter, AdapterOptions

adapter = HtmlAdapter()

options = AdapterOptions(
    sheet_names=["Summary"]  # Export specific sheet
)

adapter.export(sheets, "output.html", options)
```

**Note:** HTML import is not supported.

---

## Enums

### ExportFormat

Supported export formats.

```python
from spreadsheet_dl.adapters import ExportFormat

ExportFormat.ODS   # OpenDocument Spreadsheet
ExportFormat.XLSX  # Microsoft Excel (future)
ExportFormat.CSV   # Comma-Separated Values
ExportFormat.TSV   # Tab-Separated Values
ExportFormat.HTML  # HTML table
ExportFormat.JSON  # JSON data
ExportFormat.PDF   # PDF (future)
```

### ImportFormat

Supported import formats.

```python
from spreadsheet_dl.adapters import ImportFormat

ImportFormat.ODS   # OpenDocument Spreadsheet
ImportFormat.XLSX  # Microsoft Excel (future)
ImportFormat.CSV   # Comma-Separated Values
ImportFormat.TSV   # Tab-Separated Values
ImportFormat.JSON  # JSON data
```

---

## Module Functions

### `export_to()`

Export sheets to file.

```python
from spreadsheet_dl.adapters import export_to

# Auto-detect format from extension
path = export_to(sheets, "output.csv")

# Explicit format
path = export_to(sheets, "output.dat", format="csv")

# With options
path = export_to(
    sheets,
    "output.csv",
    delimiter=";",
    encoding="utf-8-sig"
)
```

### `import_from()`

Import sheets from file.

```python
from spreadsheet_dl.adapters import import_from

# Auto-detect format from extension
sheets = import_from("data.csv")

# Explicit format
sheets = import_from("data.txt", format="csv")

# With options
sheets = import_from(
    "data.csv",
    include_headers=True,
    delimiter=","
)
```

---

## Auto-Detection

Extension to format mapping:

| Extension       | Format |
| --------------- | ------ |
| `.ods`          | ODS    |
| `.csv`          | CSV    |
| `.tsv`          | TSV    |
| `.json`         | JSON   |
| `.html`, `.htm` | HTML   |

---

## Complete Example

```python
from spreadsheet_dl.adapters import (
    AdapterRegistry,
    AdapterOptions,
    ExportFormat,
    export_to,
    import_from,
    CsvAdapter,
)
from spreadsheet_dl.builder import SpreadsheetBuilder
from pathlib import Path

# Build sample data
builder = SpreadsheetBuilder()
builder.sheet("Sales") \
    .column("Product") \
    .column("Q1", type="currency") \
    .column("Q2", type="currency") \
    .column("Q3", type="currency") \
    .header_row() \
    .row().cells("Widget A", 1500, 1800, 2100) \
    .row().cells("Widget B", 2200, 2400, 2600) \
    .row().cells("Widget C", 800, 900, 1100)

sheets = builder.build()

# Export to multiple formats
output_dir = Path("./exports")
output_dir.mkdir(exist_ok=True)

# 1. ODS (native format)
export_to(sheets, output_dir / "sales.ods")

# 2. CSV with custom options
export_to(
    sheets,
    output_dir / "sales.csv",
    delimiter=",",
    decimal_places=2
)

# 3. TSV
export_to(sheets, output_dir / "sales.tsv")

# 4. JSON (type-preserving)
export_to(sheets, output_dir / "sales.json")

# 5. HTML table
export_to(sheets, output_dir / "sales.html")

print(f"Exported to: {output_dir}")

# Import and transform
csv_sheets = import_from(output_dir / "sales.csv")
print(f"Imported {len(csv_sheets)} sheet(s)")

# Import with custom options
european_csv = import_from(
    "european_data.csv",
    delimiter=";",
    encoding="iso-8859-1"
)

# Round-trip test
json_sheets = import_from(output_dir / "sales.json")
print(f"JSON round-trip: {len(json_sheets)} sheet(s)")

# List all supported formats
print("\nSupported formats:")
for fmt in AdapterRegistry.list_formats():
    adapter = AdapterRegistry.get_adapter(fmt)
    print(f"  {fmt.value}: {adapter.format_name} ({adapter.file_extension})")
```

### Custom Adapter

```python
from spreadsheet_dl.adapters import FormatAdapter, AdapterOptions, AdapterRegistry, ExportFormat
from pathlib import Path

class MarkdownAdapter(FormatAdapter):
    """Export spreadsheet as Markdown table."""

    @property
    def format_name(self) -> str:
        return "Markdown Table"

    @property
    def file_extension(self) -> str:
        return ".md"

    def export(self, sheets, output_path, options=None):
        options = options or AdapterOptions()
        output_path = Path(output_path)

        lines = []
        for sheet in sheets:
            lines.append(f"## {sheet.name}\n")

            # Header row
            if sheet.columns:
                headers = [col.name for col in sheet.columns]
                lines.append("| " + " | ".join(headers) + " |")
                lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

            # Data rows
            for row in sheet.rows:
                cells = [str(c.value or "") for c in row.cells]
                lines.append("| " + " | ".join(cells) + " |")

            lines.append("")

        output_path.write_text("\n".join(lines))
        return output_path

    def import_file(self, input_path, options=None):
        raise NotImplementedError("Markdown import not supported")

# Register custom adapter
# AdapterRegistry.register_adapter(ExportFormat.MARKDOWN, MarkdownAdapter)
```
