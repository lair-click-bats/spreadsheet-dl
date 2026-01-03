# Serialization API Reference

Round-trip serialization for spreadsheet definitions.

**Implements:** TASK-402 (Round-trip serialization)

## Overview

The serialization module provides:

- JSON and YAML serialization for spreadsheet structures
- Full fidelity preservation of all data types
- Type reconstruction for dataclasses, enums, dates, decimals
- Complete spreadsheet definition format with versioning

## Classes

### Serializer

Main serialization interface for spreadsheet definitions.

```python
from spreadsheet_dl.serialization import Serializer
from spreadsheet_dl.builder import SpreadsheetBuilder

# Build a spreadsheet
builder = SpreadsheetBuilder()
builder.sheet("Data").column("Name").column("Amount")
sheets = builder.build()

# Serialize
serializer = Serializer()

# JSON operations
json_str = serializer.to_json(sheets)
restored = serializer.from_json(json_str)

serializer.save_json(sheets, "spreadsheet.json")
sheets = serializer.load_json("spreadsheet.json")

# YAML operations
yaml_str = serializer.to_yaml(sheets)
restored = serializer.from_yaml(yaml_str)

serializer.save_yaml(sheets, "spreadsheet.yaml")
sheets = serializer.load_yaml("spreadsheet.yaml")
```

#### Methods

##### JSON Serialization

| Method                                 | Description                  |
| -------------------------------------- | ---------------------------- |
| `to_json(data, indent=2)`              | Serialize to JSON string     |
| `from_json(json_str)`                  | Deserialize from JSON string |
| `save_json(data, file_path, indent=2)` | Save to JSON file            |
| `load_json(file_path)`                 | Load from JSON file          |

##### YAML Serialization

| Method                       | Description                  |
| ---------------------------- | ---------------------------- |
| `to_yaml(data)`              | Serialize to YAML string     |
| `from_yaml(yaml_str)`        | Deserialize from YAML string |
| `save_yaml(data, file_path)` | Save to YAML file            |
| `load_yaml(file_path)`       | Load from YAML file          |

---

### SpreadsheetEncoder

JSON encoder for spreadsheet data structures.

```python
import json
from spreadsheet_dl.serialization import SpreadsheetEncoder

# Use with json.dumps
json_str = json.dumps(data, cls=SpreadsheetEncoder, indent=2)
```

Handles:

- Dataclass instances (with `_type` marker)
- Enums (with `_enum` and `_value`)
- Decimal values (with `_decimal`)
- Date/datetime objects (with `_date`/`_datetime`)
- Path objects (with `_path`)

---

### SpreadsheetDecoder

Decoder for spreadsheet data structures.

```python
from spreadsheet_dl.serialization import SpreadsheetDecoder

# Decode a dictionary
decoded = SpreadsheetDecoder.decode(data_dict)

# Decode a list
decoded_list = SpreadsheetDecoder.decode_list(data_list)
```

Reconstructs:

- SheetSpec, RowSpec, CellSpec, ColumnSpec
- ChartSpec, ChartTitle, DataSeries, AxisConfig
- ChartType, LegendPosition enums
- Decimal, date, datetime, Path values

---

### DefinitionFormat

High-level spreadsheet definition format.

```python
from spreadsheet_dl.serialization import DefinitionFormat
from spreadsheet_dl.builder import SpreadsheetBuilder

# Build sheets
builder = SpreadsheetBuilder()
builder.sheet("Budget").column("Category").column("Amount")
sheets = builder.build()

# Create complete definition
definition = DefinitionFormat.create(
    sheets=sheets,
    charts=[],
    named_ranges=[],
    metadata={"author": "Finance Team", "version": "1.0"}
)

# Save to file
path = DefinitionFormat.save(
    "budget_definition.yaml",
    sheets=sheets,
    metadata={"author": "Finance Team"},
    format="yaml"  # or "json"
)

# Load from file
loaded = DefinitionFormat.load("budget_definition.yaml")
```

#### Definition Format Structure

```yaml
version: '4.0'
metadata:
  author: Finance Team
  version: '1.0'
  custom_field: value
sheets:
  - _type: SheetSpec
    name: Budget
    columns:
      - _type: ColumnSpec
        name: Category
        width: 2.5cm
    rows:
      - _type: RowSpec
        cells:
          - _type: CellSpec
            value: Housing
charts: []
named_ranges: []
```

---

## Module Functions

### `save_definition()`

Save spreadsheet definition to file.

```python
from spreadsheet_dl.serialization import save_definition

path = save_definition(
    file_path="budget.yaml",
    sheets=sheets,
    charts=charts,
    named_ranges=ranges,
    metadata={"author": "Me"},
    format="yaml"  # or "json"
)
```

### `load_definition()`

Load spreadsheet definition from file.

```python
from spreadsheet_dl.serialization import load_definition

definition = load_definition("budget.yaml")
sheets = definition["sheets"]
charts = definition.get("charts", [])
metadata = definition.get("metadata", {})
```

---

## Type Markers

The serialization format uses special markers to preserve type information:

| Marker      | Type      | Example                                         |
| ----------- | --------- | ----------------------------------------------- |
| `_type`     | Dataclass | `{"_type": "SheetSpec", "name": "Budget", ...}` |
| `_enum`     | Enum      | `{"_enum": "ChartType", "_value": "bar"}`       |
| `_decimal`  | Decimal   | `{"_decimal": "123.45"}`                        |
| `_date`     | date      | `{"_date": "2024-01-15"}`                       |
| `_datetime` | datetime  | `{"_datetime": "2024-01-15T10:30:00"}`          |
| `_path`     | Path      | `{"_path": "/home/user/file.ods"}`              |

---

## Registered Types

### Dataclass Types

- `SheetSpec`
- `RowSpec`
- `CellSpec`
- `ColumnSpec`
- `NamedRange`
- `RangeRef`
- `ChartSpec`
- `ChartTitle`
- `DataSeries`
- `AxisConfig`
- `LegendConfig`
- `DataLabelConfig`
- `ChartPosition`
- `ChartSize`

### Enum Types

- `ChartType`
- `LegendPosition`

---

## Complete Example

```python
from spreadsheet_dl.serialization import Serializer, DefinitionFormat
from spreadsheet_dl.builder import SpreadsheetBuilder
from spreadsheet_dl.charts import ChartBuilder
from pathlib import Path

# Build a complete spreadsheet
builder = SpreadsheetBuilder(theme="professional")

builder.workbook_properties(
    title="Monthly Budget",
    author="Finance Team"
)

builder.sheet("Budget") \
    .column("Category", width="150pt") \
    .column("Budget", type="currency") \
    .column("Actual", type="currency") \
    .column("Variance", type="currency") \
    .header_row() \
    .row().cells("Housing", 1500, 1450, 50) \
    .row().cells("Groceries", 500, 480, 20) \
    .row().cells("Transport", 300, 320, -20)

sheets = builder.build()

# Add a chart
chart = ChartBuilder() \
    .column_chart() \
    .title("Budget vs Actual") \
    .series("Budget", "B2:B4") \
    .series("Actual", "C2:C4") \
    .build()

# Serialize to YAML (more readable)
serializer = Serializer()
yaml_content = serializer.to_yaml(sheets)
print("YAML Output:")
print(yaml_content[:500] + "...")

# Save complete definition
path = DefinitionFormat.save(
    "budget_definition.yaml",
    sheets=sheets,
    charts=[chart],
    metadata={
        "author": "Finance Team",
        "created": "2024-01-15",
        "department": "Accounting"
    },
    format="yaml"
)
print(f"\nSaved to: {path}")

# Load and reconstruct
loaded = DefinitionFormat.load(path)
print(f"\nLoaded {len(loaded['sheets'])} sheets")
print(f"Version: {loaded['version']}")
print(f"Metadata: {loaded['metadata']}")

# Round-trip verification
original_json = serializer.to_json(sheets)
restored = serializer.from_json(original_json)
restored_json = serializer.to_json(restored)

assert original_json == restored_json
print("\nRound-trip verification: PASSED")
```

### JSON Output Example

```json
[
  {
    "_type": "SheetSpec",
    "name": "Budget",
    "columns": [
      {
        "_type": "ColumnSpec",
        "name": "Category",
        "width": "150pt",
        "type": "string"
      },
      {
        "_type": "ColumnSpec",
        "name": "Budget",
        "width": "2.5cm",
        "type": "currency"
      }
    ],
    "rows": [
      {
        "_type": "RowSpec",
        "cells": [
          { "_type": "CellSpec", "value": "Housing" },
          { "_type": "CellSpec", "value": 1500, "value_type": "float" }
        ]
      }
    ]
  }
]
```

### YAML Output Example

```yaml
- _type: SheetSpec
  name: Budget
  columns:
    - _type: ColumnSpec
      name: Category
      width: 150pt
    - _type: ColumnSpec
      name: Budget
      type: currency
  rows:
    - _type: RowSpec
      cells:
        - _type: CellSpec
          value: Housing
        - _type: CellSpec
          value: 1500
```
