# AI Export API Reference

AI-friendly dual export (ODS + JSON) with semantic metadata.

**Implements:** FR-DUAL-001, FR-DUAL-002, FR-AI-001, FR-AI-003

## Overview

The AI Export module provides semantic-aware export of ODS spreadsheets to JSON format optimized for LLM consumption. It includes:

- Dual export (ODS + JSON simultaneously)
- Semantic cell type classification
- Natural language formula descriptions
- Cell relationship graphs (dependency mapping)
- Semantic tagging based on financial context
- Business context inference
- Consistency validation
- AI instructions and query examples

## Semantic Types

### SemanticCellType

Semantic type classification for cells.

```python
from spreadsheet_dl.ai_export import SemanticCellType

# Structural
SemanticCellType.HEADER          # Column/row header
SemanticCellType.LABEL           # Row label
SemanticCellType.EMPTY           # Empty cell

# Data types
SemanticCellType.CURRENCY        # Monetary value
SemanticCellType.PERCENTAGE      # Percentage
SemanticCellType.DATE            # Date value
SemanticCellType.NUMBER          # Numeric value

# Financial semantics
SemanticCellType.BUDGET_AMOUNT   # Allocated budget
SemanticCellType.EXPENSE_AMOUNT  # Actual spending
SemanticCellType.INCOME_AMOUNT   # Income/revenue
SemanticCellType.BALANCE         # Remaining balance
SemanticCellType.VARIANCE        # Budget variance

# Formula types
SemanticCellType.SUM_FORMULA     # Contains SUM
SemanticCellType.AVERAGE_FORMULA # Contains AVERAGE
SemanticCellType.VLOOKUP_FORMULA # Contains VLOOKUP
SemanticCellType.CALCULATED      # Calculated value
```

---

### SemanticTag

Additional semantic tags for business context.

```python
from spreadsheet_dl.ai_export import SemanticTag

# Budget tags
SemanticTag.MONTHLY_ALLOCATION
SemanticTag.BUDGET_LIMIT
SemanticTag.REMAINING_BUDGET

# Expense tags
SemanticTag.FIXED_EXPENSE
SemanticTag.VARIABLE_EXPENSE
SemanticTag.ESSENTIAL
SemanticTag.DISCRETIONARY
SemanticTag.RECURRING
SemanticTag.ONE_TIME

# Status tags
SemanticTag.NEEDS_ATTENTION
SemanticTag.ON_TRACK
SemanticTag.EXCEEDED
```

---

## Cell Relationships

### CellRelationship

Represents dependency between cells.

```python
from spreadsheet_dl.ai_export import CellRelationship

relationship = CellRelationship(
    source_ref="C2",
    target_ref="B2:B10",
    relationship_type="sums",
    description="Sums monthly expenses"
)

# Convert to dictionary
data = relationship.to_dict()
```

**Attributes:**

- `source_ref: str` - Source cell reference
- `target_ref: str` - Target cell reference
- `relationship_type: str` - Type (depends_on, sums, references, vlookup, etc.)
- `description: str` - Human-readable description

---

## Semantic Cells and Sheets

### SemanticCell

Cell with semantic metadata.

```python
from spreadsheet_dl.ai_export import SemanticCell, SemanticCellType, SemanticTag

cell = SemanticCell(
    row=2,
    column=3,
    column_letter="C",
    value=150.50,
    display_value="$150.50",
    semantic_type=SemanticCellType.EXPENSE_AMOUNT,
    formula=None,
    cell_reference="C2",
)

# Add semantic tag
cell.add_tag(SemanticTag.FIXED_EXPENSE)

# Add relationship
cell.add_relationship("D2", "depends_on", "Used in variance calculation")

# Convert to dict
data = cell.to_dict()
```

**Attributes:**

- `row: int` - Row number
- `column: int` - Column number
- `column_letter: str` - Letter(s) (A, B, C, ..., AA, etc.)
- `value: Any` - Actual value
- `display_value: str` - Formatted display value
- `semantic_type: SemanticCellType` - Semantic classification
- `formula: str | None` - Formula content
- `formula_description: str | None` - Natural language formula meaning
- `cell_reference: str` - Cell reference (e.g., "A1")
- `context: dict[str, Any]` - Row/column context
- `tags: list[SemanticTag]` - Semantic tags
- `relationships: list[CellRelationship]` - Cell relationships

**Methods:**

#### `add_tag(tag: SemanticTag)`

Add semantic tag.

#### `add_relationship(target_ref: str, relationship_type: str, description: str = "")`

Add dependency relationship.

---

### SemanticSheet

Sheet with semantic metadata.

```python
from spreadsheet_dl.ai_export import SemanticSheet

sheet = SemanticSheet(
    name="Budget",
    purpose="Monthly budget allocation and tracking",
    cells=[],  # Will be populated
    rows=30,
    columns=5
)

# Build relationship graph
sheet.build_relationship_graph()

# Get cell by reference
cell = sheet.get_cell("A1")
```

**Attributes:**

- `name: str` - Sheet name
- `purpose: str` - Sheet purpose/description
- `cells: list[SemanticCell]` - All cells in sheet
- `rows: int` - Number of rows
- `columns: int` - Number of columns
- `summary: dict[str, Any]` - Summary statistics
- `schema: dict[str, Any]` - Inferred schema
- `relationship_graph: list[CellRelationship]` - All relationships

---

## AI Exporter

### AIExporter

Export ODS files to AI-friendly JSON format.

```python
from spreadsheet_dl.ai_export import AIExporter
from pathlib import Path

exporter = AIExporter(
    include_empty_cells=False,
    include_formulas=True,
    include_context=True,
    include_relationships=True,
    include_tags=True
)

# Export to JSON
export_data = exporter.export_to_json(
    "budget.ods",
    output_path="budget.json",
    business_context={"domain": "personal_finance"}
)
```

**Methods:**

#### `export_to_json(ods_path, output_path=None, business_context=None) -> dict[str, Any]`

Export ODS to AI-friendly JSON.

```python
exporter = AIExporter()

export_data = exporter.export_to_json(
    Path("budget.ods"),
    output_path=Path("budget_export.json"),
    business_context={
        "domain": "personal_finance",
        "period": "Q1 2024"
    }
)

# Access exported data
metadata = export_data["metadata"]
sheets = export_data["sheets"]
instructions = export_data["ai_instructions"]
```

**Parameters:**

- `ods_path: Path | str` - ODS file path
- `output_path: Path | str | None` - Optional file to write JSON
- `business_context: dict[str, Any] | None` - Business context for inference

**Returns:** Dictionary with:

- `metadata` - Export metadata
- `sheets` - List of semantic sheets
- `ai_instructions` - Instructions for LLM processing
- `semantic_dictionary` - Semantic type descriptions
- `query_examples` - Example queries

**Raises:** FileError, DualExportError

---

#### `export_dual(ods_path, output_dir=None, *, validate=True) -> tuple[Path, Path]`

Export both ODS and JSON simultaneously.

```python
exporter = AIExporter()

ods_copy, json_file = exporter.export_dual(
    "budget.ods",
    output_dir="exports/",
    validate=True
)

print(f"ODS: {ods_copy}")
print(f"JSON: {json_file}")
```

Creates timestamped copies with both formats.

**Parameters:**

- `ods_path: Path | str` - Source ODS file
- `output_dir: Path | str | None` - Output directory
- `validate: bool` - Validate consistency between formats

**Returns:** Tuple of (ods_path, json_path)

**Raises:** ConsistencyError if validation fails

---

## Convenience Functions

### export_for_ai(ods_path, output_path=None) -> dict[str, Any]

Quick export to AI-friendly JSON.

```python
from spreadsheet_dl.ai_export import export_for_ai

export_data = export_for_ai("budget.ods", "budget.json")
```

---

### export_dual(ods_path, output_dir=None) -> tuple[Path, Path]

Quick dual export.

```python
from spreadsheet_dl.ai_export import export_dual

ods_copy, json_file = export_dual("budget.ods", "output/")
```

---

## Exported Data Structure

The JSON export has this structure:

```json
{
  "metadata": {
    "version": "2.0",
    "format": "spreadsheet-dl-ai-export",
    "schema_version": "2.0",
    "export_time": "2024-01-15T10:30:00",
    "source_file": "/path/to/budget.ods",
    "business_context": {
      "domain": "personal_finance",
      "document_type": "budget_spreadsheet"
    },
    "capabilities": [
      "semantic_cell_types",
      "formula_descriptions",
      "cell_relationships",
      "semantic_tags",
      "business_context"
    ]
  },
  "sheets": [
    {
      "name": "Budget",
      "purpose": "Monthly budget allocation and tracking",
      "dimensions": {"rows": 30, "columns": 5},
      "schema": {
        "columns": {
          "A": {"name": "Category", "type": "category_name"}
        },
        "has_headers": true,
        "data_start_row": 2
      },
      "summary": {
        "total_cells": 150,
        "data_cells": 145,
        "formula_cells": 12,
        "currency_cells": 50
      },
      "cells": [
        {
          "ref": "A1",
          "value": "Category",
          "display": "Category",
          "type": "header",
          "tags": []
        },
        {
          "ref": "B2",
          "value": 500.00,
          "display": "$500.00",
          "type": "budget_amount",
          "formula": null,
          "tags": ["monthly_allocation"],
          "context": {
            "column_header": "Budget",
            "row_label": "Groceries"
          }
        }
      ],
      "relationship_graph": [
        {
          "source": "E2",
          "target": "B2:B10",
          "type": "sums",
          "description": "Sums monthly budget allocations"
        }
      ]
    }
  ],
  "ai_instructions": {
    "purpose": "This JSON export contains financial data...",
    "semantic_types": {...},
    "analysis_suggestions": [...]
  },
  "semantic_dictionary": {
    "budget_amount": "Allocated budget for a category",
    "expense_amount": "Actual spending/expense"
  },
  "query_examples": [
    {
      "query": "What is my total spending this month?",
      "approach": "Sum all cells with semantic_type 'expense_amount'"
    }
  ]
}
```

---

## Complete Example

```python
from spreadsheet_dl.ai_export import (
    AIExporter,
    export_for_ai,
    export_dual,
)
from pathlib import Path

# Method 1: Quick export
export_data = export_for_ai("budget.ods", "budget_ai.json")

# Method 2: Custom configuration
exporter = AIExporter(
    include_empty_cells=False,
    include_formulas=True,
    include_context=True,
    include_relationships=True,
    include_tags=True
)

export_data = exporter.export_to_json(
    "budget.ods",
    output_path="budget_semantic.json",
    business_context={
        "domain": "personal_finance",
        "period": "January 2024",
        "currency": "USD"
    }
)

# Access semantic information
for sheet in export_data["sheets"]:
    print(f"Sheet: {sheet['name']}")
    print(f"  Purpose: {sheet['purpose']}")
    print(f"  Rows: {sheet['dimensions']['rows']}")
    print(f"  Data cells: {sheet['summary']['data_cells']}")
    print(f"  Formula cells: {sheet['summary']['formula_cells']}")

# Method 3: Dual export (ODS + JSON)
ods_copy, json_file = export_dual("budget.ods", output_dir="exports/")
print(f"ODS copy: {ods_copy}")
print(f"JSON export: {json_file}")

# Get AI instructions
instructions = export_data["ai_instructions"]
print(f"\nPurpose: {instructions['purpose']}")
print(f"Available semantic types: {list(instructions['semantic_types'].keys())}")

# Get query examples
examples = export_data["query_examples"]
for example in examples[:3]:
    print(f"\nQuery: {example['query']}")
    print(f"Approach: {example['approach']}")
```

---

## LLM Integration

Use the exported JSON with LLMs:

```python
import json
from pathlib import Path
import anthropic

# Export budget to JSON
from spreadsheet_dl.ai_export import export_for_ai

export_data = export_for_ai("budget.ods")
json_str = json.dumps(export_data, indent=2)

# Send to Claude
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": f"""Analyze this budget export and identify:
1. Top spending categories
2. Areas over budget
3. Recommendations for improvement

Budget data:
{json_str}"""
        }
    ]
)

print(message.content[0].text)
```

---

## Use Cases

### Financial Analysis

```python
# Export budget for AI analysis
export_data = export_for_ai("monthly_budget.ods")

# LLM can understand:
# - Which amounts are budget vs. actual
# - Which expenses are fixed vs. variable
# - Relationships between totals and line items
# - Budget status (on track, warning, exceeded)
```

### Data Documentation

```python
# Generate semantic documentation
exporter = AIExporter()
export_data = exporter.export_to_json("data.ods")

# Extract semantic dictionary for documentation
for type_name, description in export_data["semantic_dictionary"].items():
    print(f"- {type_name}: {description}")
```

### Schema Inference

```python
# Extract inferred schema
sheets = export_data["sheets"]
for sheet in sheets:
    schema = sheet["schema"]
    for col_letter, col_info in schema["columns"].items():
        print(f"Column {col_letter}: {col_info['name']} ({col_info['type']})")
```
