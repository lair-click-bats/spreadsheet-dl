# Module: progress

## Overview

Progress indicators for long-running operations. Provides progress bars, spinners, and batch progress tracking using the `rich` library with NO_COLOR environment variable support.

**Implements:** FR-UX-002: Progress indicators for long-running operations

**Features:**

- Progress bars for determinate operations
- Spinners for indeterminate operations
- Batch progress tracking
- NO_COLOR environment variable support
- TTY detection for automatic disabling in non-interactive environments
- Graceful degradation when `rich` library is not installed

## Key Functions

### progress_bar(description, total=None)

Context manager for progress bar operations.

**Parameters:**

- `description` (str): Task description to display
- `total` (int | None): Total number of items (None for indeterminate progress)

**Yields:**

- `TaskID | None`: Progress task for updating (None if progress disabled)

**Example:**

```python
from spreadsheet_dl.progress import progress_bar

# Determinate progress
with progress_bar("Processing rows", total=100) as task:
    for i in range(100):
        # Do work
        process_row(i)
        # Update progress
        if task:
            progress.update(task, advance=1)

# Indeterminate progress
with progress_bar("Loading data") as task:
    load_large_dataset()
```

### spinner(description)

Show spinner for indeterminate operations.

**Parameters:**

- `description` (str): Operation description

**Yields:**

- `None`

**Example:**

```python
from spreadsheet_dl.progress import spinner

with spinner("Loading database..."):
    # Perform long operation
    connect_to_database()
    load_initial_data()
```

### is_progress_enabled() -> bool

Check if progress indicators are enabled.

**Returns:**

- `bool`: True if progress indicators will be displayed

**Example:**

```python
from spreadsheet_dl.progress import is_progress_enabled

if is_progress_enabled():
    # Use progress indicators
    with progress_bar("Processing", total=100) as task:
        # ...
else:
    # Fall back to simple logging
    print("Processing...")
    # ...
```

### require_rich() -> None

Raise ImportError if rich library is not available.

**Raises:**

- `ImportError`: If rich library is not installed

**Example:**

```python
from spreadsheet_dl.progress import require_rich

try:
    require_rich()
    # Use progress features
except ImportError as e:
    print(f"Install rich for progress indicators: {e}")
```

## Key Classes

### BatchProgress

Progress tracking for batch operations with built-in context manager support.

**Attributes:**

- `total` (int): Total number of items to process
- `description` (str): Progress description
- `current` (int): Current progress count
- `_progress` (Progress | None): Internal rich Progress instance
- `_task` (TaskID | None): Internal task ID

**Methods:**

#### `__init__(total: int, description: str = "Processing") -> None`

Initialize batch progress tracker.

**Parameters:**

- `total` (int): Total number of items
- `description` (str): Progress description (default: "Processing")

#### `update(n: int = 1) -> None`

Update progress by n items.

**Parameters:**

- `n` (int): Number of items completed (default: 1)

#### `set_description(description: str) -> None`

Update the progress description dynamically.

**Parameters:**

- `description` (str): New description

**Example:**

```python
from spreadsheet_dl.progress import BatchProgress

# Process items with batch progress
items = range(1000)

with BatchProgress(len(items), "Processing items") as bp:
    for i, item in enumerate(items):
        # Process item
        result = process_item(item)

        # Update progress
        bp.update()

        # Update description every 100 items
        if i % 100 == 0:
            bp.set_description(f"Processing batch {i//100 + 1}")
```

## Usage Examples

### Basic Progress Bar

```python
from spreadsheet_dl.progress import progress_bar

rows = load_rows()

with progress_bar("Processing rows", total=len(rows)) as task:
    for row in rows:
        process_row(row)
        if task:
            progress.update(task, advance=1)
```

### Spinner for Indeterminate Operations

```python
from spreadsheet_dl.progress import spinner

with spinner("Connecting to server..."):
    connection = establish_connection()
    authenticate(connection)
```

### Batch Progress with Dynamic Description

```python
from spreadsheet_dl.progress import BatchProgress

files = list_files_to_process()

with BatchProgress(len(files), "Processing files") as bp:
    for i, file_path in enumerate(files):
        bp.set_description(f"Processing {file_path.name}")
        process_file(file_path)
        bp.update()
```

### Conditional Progress Display

```python
from spreadsheet_dl.progress import is_progress_enabled, progress_bar

def process_data(data, show_progress=True):
    if show_progress and is_progress_enabled():
        with progress_bar("Processing", total=len(data)) as task:
            for item in data:
                process_item(item)
                if task:
                    progress.update(task, advance=1)
    else:
        # Simple processing without progress
        for item in data:
            process_item(item)
```

### Multi-Level Progress

```python
from spreadsheet_dl.progress import BatchProgress

categories = get_categories()

with BatchProgress(len(categories), "Processing categories") as cat_progress:
    for category in categories:
        cat_progress.set_description(f"Category: {category.name}")

        items = get_items(category)
        with BatchProgress(len(items), f"Items in {category.name}") as item_progress:
            for item in items:
                process_item(item)
                item_progress.update()

        cat_progress.update()
```

### Error Handling with Progress

```python
from spreadsheet_dl.progress import BatchProgress

tasks = get_tasks()

with BatchProgress(len(tasks), "Executing tasks") as bp:
    for task in tasks:
        try:
            bp.set_description(f"Executing {task.name}")
            execute_task(task)
            bp.update()
        except Exception as e:
            bp.set_description(f"Failed: {task.name}")
            print(f"Error in {task.name}: {e}")
            bp.update()  # Still update progress
```

## Environment Configuration

### NO_COLOR Support

The module respects the `NO_COLOR` environment variable:

```bash
# Disable colored progress output
export NO_COLOR=1
spreadsheet-dl generate -o output/

# Re-enable colors
unset NO_COLOR
spreadsheet-dl generate -o output/
```

### TTY Detection

Progress indicators are automatically disabled when output is not a TTY:

```bash
# Progress enabled (interactive terminal)
spreadsheet-dl import data.csv

# Progress disabled (redirected output)
spreadsheet-dl import data.csv > import.log

# Progress disabled (piped output)
spreadsheet-dl analyze budget.ods | grep Total
```

## Installation

Progress indicators require the `rich` library:

```bash
# Install with progress support
pip install 'spreadsheet-dl[ui]'

# Or install rich separately
pip install rich>=13.0.0
```

If `rich` is not installed, progress functions gracefully degrade to no-ops.

## Integration with CLI

The progress module is automatically integrated into CLI commands:

```python
from spreadsheet_dl.progress import BatchProgress

def _cmd_import(args):
    entries = load_csv(args.csv_file)

    with BatchProgress(len(entries), "Importing transactions") as bp:
        for entry in entries:
            add_to_budget(entry)
            bp.update()

    print(f"Imported {len(entries)} transactions")
```

## See Also

- [cli](cli.md) - CLI commands using progress indicators
- [export](export.md) - Export operations with progress tracking
- [domains/finance/csv_import](domains/finance/csv_import.md) - CSV import with progress
