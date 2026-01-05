# Streaming API Reference

Stream-based I/O for large spreadsheet files.

## Overview

The streaming module provides memory-efficient reading and writing for large ODS files:

- Row-by-row reading without loading entire file
- Chunk-by-chunk writing with automatic buffering
- Handles 100k+ rows efficiently
- Context manager support for proper resource cleanup

## Classes

### StreamingReader

Stream-based ODS file reader for large files.

```python
from spreadsheet_dl.streaming import StreamingReader

# Context manager usage (recommended)
with StreamingReader("large_file.ods") as reader:
    # List all sheets
    for sheet_name in reader.sheet_names():
        print(f"Sheet: {sheet_name}")
        print(f"  Rows: {reader.row_count(sheet_name)}")
        print(f"  Columns: {reader.column_count(sheet_name)}")

    # Read rows one at a time
    for row in reader.rows("Data"):
        for cell in row.cells:
            print(cell.value, end="\t")
        print()

# Read specific range
reader = StreamingReader("file.ods")
reader.open()
for row in reader.rows("Sheet1", start_row=1000, limit=100):
    process_row(row)
reader.close()
```

#### Constructor

```python
StreamingReader(file_path: Path | str)
```

**Parameters:**

- `file_path`: Path to ODS file

#### Methods

##### `open()` / `close()`

Open/close the ODS file for reading.

```python
reader = StreamingReader("file.ods")
reader.open()
# ... read operations ...
reader.close()
```

##### `sheet_names()`

Get list of sheet names in the document.

```python
names = reader.sheet_names()
# ["Sheet1", "Data", "Summary"]
```

##### `row_count()`

Get row count for a sheet without loading all rows.

```python
count = reader.row_count("Sheet1")
```

##### `column_count()`

Get column count for a sheet.

```python
count = reader.column_count("Sheet1")
```

##### `rows()`

Iterate over rows in a sheet.

```python
for row in reader.rows(
    sheet_name: str,
    start_row: int = 0,      # Starting row index (0-based)
    limit: int | None = None  # Max rows to return
):
    # row is a StreamingRow
    for cell in row.cells:
        print(cell.value)
```

---

### StreamingWriter

Stream-based ODS file writer for large files.

```python
from spreadsheet_dl.streaming import StreamingWriter

# Context manager usage
with StreamingWriter("output.ods") as writer:
    # Start a sheet with headers
    writer.start_sheet("Data", columns=["Name", "Amount", "Date"])

    # Write rows one at a time
    for item in data_generator():
        writer.write_row([item.name, item.amount, item.date])

    # End sheet (automatic on context exit)
    writer.end_sheet()

# Multiple sheets
with StreamingWriter("multi_sheet.ods", chunk_size=500) as writer:
    writer.start_sheet("Summary")
    writer.write_rows(summary_data)
    writer.end_sheet()

    writer.start_sheet("Details")
    writer.write_rows(detail_data)
    writer.end_sheet()
```

#### Constructor

```python
StreamingWriter(
    file_path: Path | str,
    chunk_size: int = 1000  # Rows to buffer before flushing
)
```

**Parameters:**

- `file_path`: Path for output ODS file
- `chunk_size`: Number of rows to buffer before flushing (default: 1000)

#### Methods

##### `start_sheet()`

Start a new sheet.

```python
writer.start_sheet(
    name: str,
    columns: list[str] | None = None  # Optional column headers
)
```

Returns `self` for method chaining.

##### `end_sheet()`

End the current sheet.

```python
writer.end_sheet()
```

Returns `self` for method chaining.

##### `write_row()`

Write a single row.

```python
# From list of values
writer.write_row(["Value 1", 123, "2024-01-15"])

# From StreamingRow
writer.write_row(StreamingRow(cells=[...]))
```

Returns `self` for method chaining.

##### `write_rows()`

Write multiple rows.

```python
rows = [
    ["Alice", 100, "2024-01-01"],
    ["Bob", 200, "2024-01-02"],
    ["Carol", 150, "2024-01-03"],
]
writer.write_rows(rows)
```

Returns `self` for method chaining.

##### `close()`

Finalize and save the ODS file.

```python
path = writer.close()
print(f"Saved to: {path}")
```

Returns the path to the created file.

---

### StreamingCell

Lightweight cell representation for streaming.

```python
from spreadsheet_dl.streaming import StreamingCell

cell = StreamingCell(
    value="Hello",
    value_type="string",
    formula=None,
    style=None
)

# Check if empty
if cell.is_empty():
    print("Cell is empty")
```

#### Attributes

| Attribute    | Type  | Description                              |
| ------------ | ----- | ---------------------------------------- | ------------------- |
| `value`      | `Any` | Cell value (string, number, date)        |
| `value_type` | `str` | ODF type (string, float, date, currency) |
| `formula`    | `str  | None`                                    | Optional formula    |
| `style`      | `str  | None`                                    | Optional style name |

---

### StreamingRow

Lightweight row representation for streaming.

```python
from spreadsheet_dl.streaming import StreamingRow, StreamingCell

row = StreamingRow(
    cells=[
        StreamingCell(value="Name"),
        StreamingCell(value=100, value_type="float"),
    ],
    style="header",
    row_index=0
)

# Iterate over cells
for cell in row:
    print(cell.value)

# Get cell count
print(len(row))  # 2
```

#### Attributes

| Attribute   | Type                  | Description         |
| ----------- | --------------------- | ------------------- | -------------- |
| `cells`     | `list[StreamingCell]` | List of cells       |
| `style`     | `str                  | None`               | Row style name |
| `row_index` | `int`                 | Row index (0-based) |

---

## Module Functions

### `stream_read()`

Create a streaming reader for an ODS file.

```python
from spreadsheet_dl.streaming import stream_read

reader = stream_read("large_file.ods")
with reader:
    for row in reader.rows("Sheet1"):
        process(row)
```

### `stream_write()`

Create a streaming writer for an ODS file.

```python
from spreadsheet_dl.streaming import stream_write

writer = stream_write("output.ods", chunk_size=500)
with writer:
    writer.start_sheet("Data", columns=["A", "B", "C"])
    writer.write_rows(data)
```

---

## Performance Tips

### Memory Efficiency

The streaming API maintains constant memory usage regardless of file size:

```python
# Processing 100,000 rows
with StreamingReader("huge_file.ods") as reader:
    total = 0
    for row in reader.rows("Data"):
        # Only one row in memory at a time
        if len(row.cells) > 1 and row.cells[1].value:
            total += float(row.cells[1].value)
    print(f"Total: {total}")
```

### Chunk Size Tuning

Adjust `chunk_size` based on your workload:

```python
# Large rows: smaller chunks
writer = StreamingWriter("output.ods", chunk_size=100)

# Small rows: larger chunks for better performance
writer = StreamingWriter("output.ods", chunk_size=5000)
```

### Pagination

Read data in pages for batch processing:

```python
PAGE_SIZE = 1000

with StreamingReader("file.ods") as reader:
    total_rows = reader.row_count("Data")

    for offset in range(0, total_rows, PAGE_SIZE):
        page = list(reader.rows("Data", start_row=offset, limit=PAGE_SIZE))
        process_batch(page)
```

---

## Complete Example

```python
from spreadsheet_dl.streaming import StreamingReader, StreamingWriter, StreamingCell

# Transform a large file
with StreamingReader("input.ods") as reader:
    with StreamingWriter("output.ods") as writer:
        for sheet_name in reader.sheet_names():
            # Get column count for headers
            col_count = reader.column_count(sheet_name)
            columns = [f"Column{i+1}" for i in range(col_count)]

            writer.start_sheet(f"{sheet_name}_transformed", columns=columns)

            for row in reader.rows(sheet_name):
                # Transform each row
                transformed_cells = []
                for cell in row.cells:
                    value = cell.value
                    # Apply transformation
                    if isinstance(value, (int, float)) and value > 0:
                        value = value * 1.1  # 10% increase
                    transformed_cells.append(value)

                writer.write_row(transformed_cells)

            writer.end_sheet()

print("Transformation complete!")
```

### Large File Generation

```python
from spreadsheet_dl.streaming import StreamingWriter
import random
from datetime import date, timedelta

# Generate 100,000 rows of sample data
with StreamingWriter("large_dataset.ods", chunk_size=2000) as writer:
    writer.start_sheet("Transactions", columns=[
        "ID", "Date", "Amount", "Category", "Description"
    ])

    base_date = date(2024, 1, 1)
    categories = ["Food", "Transport", "Housing", "Utilities", "Entertainment"]

    for i in range(100_000):
        writer.write_row([
            f"TX{i:06d}",
            (base_date + timedelta(days=i % 365)).isoformat(),
            round(random.uniform(10, 500), 2),
            random.choice(categories),
            f"Transaction {i}"
        ])

        # Progress indicator
        if i % 10000 == 0:
            print(f"Generated {i:,} rows...")

    writer.end_sheet()

print("Generated 100,000 rows!")
```
