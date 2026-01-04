# AI Training Data API Reference

Export anonymized data for AI/ML training with privacy preservation.

**Implements:** FR-AI-010 (AI Training Data Export with Anonymization)

## Overview

The AI Training module provides functionality to export budget data in AI training-friendly formats while protecting privacy through multiple anonymization levels.

Features:

- PII (Personally Identifiable Information) detection and removal
- Configurable anonymization levels (none, minimal, standard, strict)
- Statistical preservation (aggregate stats maintained)
- Multiple export formats (JSON, JSONL, CSV, Parquet)
- Data augmentation (noise addition)
- Schema versioning
- Tokenization of descriptions

## Enumerations

### AnonymizationLevel

Anonymization intensity levels.

```python
from spreadsheet_dl.ai_training import AnonymizationLevel

AnonymizationLevel.NONE       # No anonymization (testing only)
AnonymizationLevel.MINIMAL    # Hash IDs, keep amounts
AnonymizationLevel.STANDARD   # Generalize amounts, remove descriptions
AnonymizationLevel.STRICT     # Maximum: bucketize all values
```

---

### ExportFormat

Supported export formats.

```python
from spreadsheet_dl.ai_training import ExportFormat

ExportFormat.JSON      # Single JSON file
ExportFormat.JSONL     # JSON Lines (one record per line)
ExportFormat.CSV       # Comma-separated values
ExportFormat.PARQUET   # Apache Parquet (columnar format)
```

---

## Configuration

### PIIPattern

Pattern for detecting PII in text.

```python
from spreadsheet_dl.ai_training import PIIPattern
import re

pattern = PIIPattern(
    name="email",
    pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    replacement="[EMAIL]",
    flags=re.IGNORECASE
)

# Compile pattern for use
compiled = pattern.compile()
```

**Attributes:**

- `name: str` - Pattern name
- `pattern: str` - Regex pattern
- `replacement: str` - Replacement text
- `flags: int` - Regex flags

**Methods:**

#### `compile() -> re.Pattern[str]`

Compile the regex pattern.

---

### AnonymizationConfig

Configuration for anonymization process.

```python
from spreadsheet_dl.ai_training import AnonymizationConfig, AnonymizationLevel

config = AnonymizationConfig(
    level=AnonymizationLevel.STANDARD,
    hash_salt="random-salt-value",
    amount_buckets=[0, 10, 25, 50, 100, 250, 500, 1000, 5000],
    preserve_categories=True,
    preserve_dates=False,
    add_noise_percent=2.5,
    include_statistics=True
)
```

**Attributes:**

- `level: AnonymizationLevel` - Anonymization level
- `hash_salt: str` - Salt for hashing IDs
- `amount_buckets: list[float]` - Bucket boundaries for amount generalization
- `preserve_categories: bool` - Keep original category names
- `preserve_dates: bool` - Keep exact dates vs. relative dates
- `add_noise_percent: float` - Percentage of noise to add to amounts
- `include_statistics: bool` - Include aggregate statistics
- `pii_patterns: list[PIIPattern]` - Custom PII detection patterns

**Defaults:**

Built-in PII patterns detect:

- Email addresses
- Phone numbers
- Social Security numbers
- Credit card numbers
- Account numbers
- Physical addresses
- ZIP codes

---

## PII Detection

### PIIDetector

Detects and removes PII from text.

```python
from spreadsheet_dl.ai_training import PIIDetector, AnonymizationConfig

config = AnonymizationConfig()
detector = PIIDetector(config)

# Detect PII
findings = detector.detect_pii("Contact me at john@example.com or call 555-123-4567")
# -> [("email", "john@example.com", 17, 35), ("phone", "555-123-4567", 45, 57)]

# Remove PII
clean_text = detector.remove_pii("My account is 123456789")
# -> "My account is [ACCOUNT]"

# Tokenize description
tokens = detector.tokenize_description("Amazon purchase for household items")
# -> ["amazon", "purchase", "household", "items"]
```

**Methods:**

#### `detect_pii(text: str) -> list[tuple[str, str, int, int]]`

Detect PII in text.

**Returns:** List of (pattern_name, matched_text, start_pos, end_pos)

#### `remove_pii(text: str) -> str`

Remove PII from text.

#### `tokenize_description(description: str) -> list[str]`

Tokenize description while removing PII.

Returns safe tokens without PII indicators.

---

## Data Anonymization

### AnonymizedTransaction

Anonymized transaction record.

```python
from spreadsheet_dl.ai_training import AnonymizedTransaction

tx = AnonymizedTransaction(
    id="a3f9c2d1e5b4",
    date="day-45",
    category="groceries",
    amount_bucket="25-50",
    amount_normalized=0.35,
    day_of_week=3,
    day_of_month=15,
    month=1,
    is_weekend=False,
    description_tokens=["whole", "foods"]
)

# Convert to dict
data = tx.to_dict()
```

**Attributes:**

- `id: str` - Hashed transaction ID
- `date: str` - Date (absolute or relative)
- `category: str` - Expense category
- `amount_bucket: str` - Amount range bucket
- `amount_normalized: float | None` - Normalized amount (0-1)
- `day_of_week: int | None` - 0=Monday, 6=Sunday
- `day_of_month: int | None` - Day number (1-31)
- `month: int | None` - Month number (1-12)
- `is_weekend: bool | None` - Weekend flag
- `description_tokens: list[str]` - Safe description tokens

---

### TrainingDataStatistics

Statistics about the training dataset.

```python
from spreadsheet_dl.ai_training import TrainingDataStatistics

stats = TrainingDataStatistics(
    total_records=1500,
    categories={"groceries": 420, "utilities": 300},
    amount_distribution={"0-10": 50, "10-25": 120},
    date_range=("2024-01-01", "2024-03-31"),
    monthly_totals={"2024-01": 3500.50},
    category_averages={"groceries": 12.50}
)

# Convert to dict
data = stats.to_dict()
```

---

### TrainingDataset

Container for anonymized training data.

```python
from spreadsheet_dl.ai_training import TrainingDataset, AnonymizationLevel

dataset = TrainingDataset(
    version="1.0",
    schema_version="1.0",
    anonymization_level=AnonymizationLevel.STANDARD.value,
    records=[...],
    statistics=stats,
    metadata={"source": "personal_budget"}
)

# Convert to dict
data = dataset.to_dict()
```

**Attributes:**

- `version: str` - Dataset version
- `schema_version: str` - Schema version
- `created_at: str` - ISO timestamp
- `anonymization_level: str` - Level applied
- `records: list[AnonymizedTransaction]` - Anonymized records
- `statistics: TrainingDataStatistics | None` - Aggregate stats
- `metadata: dict[str, Any]` - Additional metadata

---

## Data Anonymizer

### DataAnonymizer

Anonymizes financial data for AI training.

```python
from spreadsheet_dl.ai_training import DataAnonymizer, AnonymizationConfig, AnonymizationLevel

config = AnonymizationConfig(
    level=AnonymizationLevel.STANDARD,
    preserve_categories=True,
    preserve_dates=False,
    add_noise_percent=1.0,
    include_statistics=True
)

anonymizer = DataAnonymizer(config)

# Anonymize single transaction
transaction = {
    "date": "2024-01-15",
    "category": "Groceries",
    "description": "Whole Foods Market",
    "amount": 125.50
}

anon_tx = anonymizer.anonymize_transaction(transaction, index=0)
print(f"ID: {anon_tx.id}")
print(f"Category: {anon_tx.category}")
print(f"Bucket: {anon_tx.amount_bucket}")

# Anonymize dataset of transactions
transactions = [...]
dataset = anonymizer.anonymize_dataset(transactions)

print(f"Total records: {dataset.statistics.total_records}")
print(f"Categories: {dataset.statistics.categories}")
```

**Methods:**

#### `anonymize_transaction(tx: dict[str, Any], index: int = 0) -> AnonymizedTransaction`

Anonymize single transaction.

**Parameters:**

- `tx`: Dictionary with date, category, description, amount
- `index`: Transaction index for ID generation

**Returns:** AnonymizedTransaction

#### `anonymize_dataset(transactions: list[dict[str, Any]]) -> TrainingDataset`

Anonymize dataset of transactions.

**Returns:** TrainingDataset with statistics

---

## Export

### TrainingDataExporter

Export anonymized data in various formats.

```python
from spreadsheet_dl.ai_training import (
    TrainingDataExporter,
    AnonymizationConfig,
    AnonymizationLevel,
    ExportFormat
)
from pathlib import Path

config = AnonymizationConfig(
    level=AnonymizationLevel.STANDARD
)

exporter = TrainingDataExporter(config)

# Export from ODS file
output_path = exporter.export_from_ods(
    Path("budget.ods"),
    Path("training_data.json"),
    format=ExportFormat.JSON
)

# Export pre-anonymized dataset
output_path = exporter.export_dataset(
    dataset,
    Path("training.csv"),
    format=ExportFormat.CSV
)

# Stream records for processing
for record in exporter.stream_records(dataset):
    print(record)
```

**Methods:**

#### `export_from_ods(ods_path, output_path, format=ExportFormat.JSON) -> Path`

Export anonymized data from ODS file.

**Parameters:**

- `ods_path: Path` - ODS budget file
- `output_path: Path` - Output file path
- `format: ExportFormat` - Export format

**Returns:** Path to exported file

#### `export_dataset(dataset, output_path, format=ExportFormat.JSON) -> Path`

Export TrainingDataset to file.

#### `stream_records(dataset) -> Iterator[dict[str, Any]]`

Stream records for processing.

---

## Convenience Functions

### export_training_data(ods_path, output_path, \*, level="standard", format="json") -> Path

Quick export of anonymized training data.

```python
from spreadsheet_dl.ai_training import export_training_data
from pathlib import Path

# Export with defaults
output = export_training_data(
    "budget.ods",
    "training_data.json",
    level="standard",
    format="json"
)

# Strict anonymization
output = export_training_data(
    "budget.ods",
    "strict_training.csv",
    level="strict",
    format="csv"
)

# Parquet format (requires pandas/pyarrow)
output = export_training_data(
    "budget.ods",
    "training.parquet",
    level="standard",
    format="parquet"
)
```

**Parameters:**

- `ods_path: str | Path` - ODS file path
- `output_path: str | Path` - Output file path
- `level: str` - Anonymization level ("none", "minimal", "standard", "strict")
- `format: str` - Export format ("json", "jsonl", "csv", "parquet")

**Returns:** Path to exported file

---

## Anonymization Levels

### NONE

- No anonymization
- Use for testing only
- Contains all original data

### MINIMAL

- Hash transaction IDs
- Keep all amounts
- Keep exact dates
- Keep descriptions (tokenized, PII removed)

### STANDARD (Recommended)

- Hash transaction IDs
- Bucketize amounts
- Relative dates only
- Remove descriptions, keep tokens
- Keep category names
- Add optional noise

### STRICT

- Hash transaction IDs
- Maximum amount bucketization
- Relative dates only
- Remove all descriptions
- Generalize category names
- Maximum privacy

---

## Data Examples

### Input Transaction

```json
{
  "date": "2024-01-15",
  "category": "Groceries",
  "description": "Whole Foods Market - john@example.com",
  "amount": 125.5
}
```

### MINIMAL Anonymization

```json
{
  "id": "a3f9c2d1e5b4",
  "date": "2024-01-15",
  "category": "Groceries",
  "amount_bucket": "100-250",
  "amount_normalized": 0.415,
  "month": 1,
  "day_of_month": 15,
  "description_tokens": ["whole", "foods", "market"]
}
```

### STANDARD Anonymization

```json
{
  "id": "b5f2e1d9c3a8",
  "date": "day-45",
  "category": "Groceries",
  "amount_bucket": "100-250",
  "amount_normalized": 0.415,
  "month": 1,
  "day_of_month": 15,
  "is_weekend": false
}
```

### STRICT Anonymization

```json
{
  "id": "c7e3f2d0a9b6",
  "date": "day-45",
  "category": "food",
  "amount_bucket": "100-250"
}
```

---

## Complete Example

```python
from spreadsheet_dl.ai_training import (
    export_training_data,
    AnonymizationConfig,
    AnonymizationLevel,
    ExportFormat,
)
from pathlib import Path

# Method 1: Quick export
output = export_training_data(
    "budget.ods",
    "training_data.json",
    level="standard",
    format="json"
)
print(f"Exported to: {output}")

# Method 2: Custom configuration
config = AnonymizationConfig(
    level=AnonymizationLevel.STANDARD,
    preserve_categories=True,
    preserve_dates=False,
    add_noise_percent=2.0,
    include_statistics=True
)

from spreadsheet_dl.ai_training import TrainingDataExporter

exporter = TrainingDataExporter(config)
output = exporter.export_from_ods(
    Path("budget.ods"),
    Path("training.csv"),
    format=ExportFormat.CSV
)

# Load and inspect exported data
import json

with open("training_data.json") as f:
    data = json.load(f)

print(f"Records: {data['record_count']}")
print(f"Categories: {data['statistics']['categories']}")
print(f"Amount distribution: {data['statistics']['amount_distribution']}")

# Export for different use cases
# - Loose privacy: minimal anonymization, keep more data
export_training_data("budget.ods", "loose.json", level="minimal")

# - Strict privacy: maximum anonymization
export_training_data("budget.ods", "strict.parquet", level="strict", format="parquet")

# - ML-ready: standard format with statistics
export_training_data("budget.ods", "ml_ready.csv", level="standard", format="csv")
```

---

## Privacy Considerations

1. **Anonymization Level:** Choose based on sensitivity
   - MINIMAL: Research within organization
   - STANDARD: Sharing with trusted partners
   - STRICT: Public datasets or untrusted third parties

2. **Re-identification Risk:** Even with STRICT anonymization:
   - Avoid exporting small datasets (< 100 records)
   - Remove outliers that could be identifiable
   - Combine with differential privacy if available

3. **Data Retention:** Delete training data after use
   - Don't keep indefinitely
   - Clear temporary files
   - Use secure deletion

4. **Audit Trail:** Log data exports
   - Who exported
   - When
   - What anonymization level
   - Destination

---

## LLM Training

The exported data is suitable for fine-tuning financial analysis LLMs:

```python
import json
from pathlib import Path

# Export training data
from spreadsheet_dl.ai_training import export_training_data

export_training_data(
    "budget.ods",
    "training.jsonl",
    level="standard",
    format="jsonl"  # JSONL format preferred for ML
)

# Convert to training format (depends on your LLM framework)
# Each line in JSONL can be transformed to:
# {"input": "...", "output": "category: groceries, amount: $50-100"}
```
