# Module: exceptions

## Overview

Custom exceptions for SpreadsheetDL finance tracker. Provides a comprehensive hierarchy of exceptions with error codes, actionable guidance, and contextual information for better error handling and programmatic error recovery.

**Error Code Format:** `FT-<CATEGORY>-<NUMBER>`

**Categories:**

- GEN (001-099): General/uncategorized errors
- FILE (100-199): File system errors
- ODS (200-299): ODS file errors
- CSV (300-399): CSV import errors
- VAL (400-499): Validation errors
- CFG (500-599): Configuration errors
- NET (600-699): Network/WebDAV errors
- TMPL (700-799): Template errors
- FMT (800-899): Formatting errors
- EXT (900-999): Extension/plugin errors
- SEC (1000-1099): Security errors

## Key Classes

### SpreadsheetDLError

Base exception for all finance tracker errors. Provides structured error information including machine-readable error codes, human-readable summaries, detailed explanations, actionable suggestions, and contextual information.

**Attributes:**

- `error_code` (str): Machine-readable error code (default: "FT-GEN-001")
- `severity` (ErrorSeverity): Error severity level
- `message` (str): Human-readable summary (one line)
- `details` (str | None): Detailed explanation of the error
- `suggestion` (str | None): Actionable fix suggestion
- `context` (ErrorContext): Contextual information (file, line, value)
- `doc_url_base` (str): Base URL for documentation

**Methods:**

#### `__init__(message, error_code=None, details=None, suggestion=None, context=None, severity=None)`

Initialize the exception.

**Example:**

```python
from spreadsheet_dl.exceptions import SpreadsheetDLError, ErrorContext

raise SpreadsheetDLError(
    "Operation failed",
    details="Database connection could not be established",
    suggestion="Check your database configuration",
    context=ErrorContext(file_path="config.yaml", line_number=15)
)
```

#### `format_error(use_color=True, show_debug=False) -> str`

Format error for display with optional ANSI colors and debug information.

**Parameters:**

- `use_color` (bool): Whether to use ANSI colors (default: True)
- `show_debug` (bool): Whether to include debug information (default: False)

**Returns:**

- `str`: Formatted error string

#### `to_dict() -> dict[str, Any]`

Convert error to dictionary for JSON output.

**Returns:**

- `dict`: Error information including code, severity, message, details, suggestion, context, and doc_url

#### `doc_url -> str`

Property that returns documentation URL for this error.

**Example:**

```python
try:
    # Operation
    pass
except SpreadsheetDLError as e:
    print(e.format_error())
    print(f"See: {e.doc_url}")
    print(json.dumps(e.to_dict(), indent=2))
```

### ErrorContext

Context information for an error with file location, values, and extra metadata.

**Attributes:**

- `file_path` (str | None): File path where error occurred
- `line_number` (int | None): Line number in file
- `column` (int | None): Column number in file
- `value` (str | None): Actual value that caused error
- `expected` (str | None): Expected value/format
- `actual` (str | None): Actual value/format found
- `extra` (dict[str, Any]): Additional context information

**Methods:**

#### `to_dict() -> dict[str, Any]`

Convert context to dictionary.

**Example:**

```python
from spreadsheet_dl.exceptions import ErrorContext

context = ErrorContext(
    file_path="budget.ods",
    line_number=42,
    value="invalid_amount",
    expected="numeric value",
    extra={"sheet": "Expenses"}
)
```

### ErrorSeverity

Enum for error severity levels.

**Values:**

- `ERROR`: Critical error that prevents operation
- `WARNING`: Warning that operation may not complete correctly
- `INFO`: Informational message (e.g., operation cancelled)

## Exception Hierarchy

### General Errors (FT-GEN-001 to FT-GEN-099)

#### UnknownError (FT-GEN-001)

Unknown or unexpected error.

```python
from spreadsheet_dl.exceptions import UnknownError

raise UnknownError("Unexpected condition", original_error=exc)
```

#### OperationCancelledError (FT-GEN-002)

User cancelled the operation.

```python
from spreadsheet_dl.exceptions import OperationCancelledError

raise OperationCancelledError("File generation")
```

#### NotImplementedFeatureError (FT-GEN-003)

Feature is not yet implemented.

```python
from spreadsheet_dl.exceptions import NotImplementedFeatureError

raise NotImplementedFeatureError("PDF export")
```

### File Errors (FT-FILE-100 to FT-FILE-199)

#### FileNotFoundError (FT-FILE-101)

Required file is not found.

```python
from spreadsheet_dl.exceptions import FileNotFoundError

raise FileNotFoundError(file_path="budget.ods", file_type="ODS file")
```

#### FilePermissionError (FT-FILE-102)

File permission is denied.

```python
from spreadsheet_dl.exceptions import FilePermissionError

raise FilePermissionError(file_path="/etc/budget.ods", operation="write")
```

#### FileExistsError (FT-FILE-103)

File already exists.

```python
from spreadsheet_dl.exceptions import FileExistsError

raise FileExistsError(file_path="output.ods")
```

#### InvalidFileFormatError (FT-FILE-104)

File has an invalid format.

```python
from spreadsheet_dl.exceptions import InvalidFileFormatError

raise InvalidFileFormatError(
    file_path="data.txt",
    expected_format="ODS",
    actual_format="text"
)
```

### Validation Errors (FT-VAL-400 to FT-VAL-499)

#### InvalidAmountError (FT-VAL-401)

Amount value is invalid.

```python
from spreadsheet_dl.exceptions import InvalidAmountError

raise InvalidAmountError("abc", reason="Not a valid number")
```

#### InvalidDateError (FT-VAL-402)

Date value is invalid.

```python
from spreadsheet_dl.exceptions import InvalidDateError

raise InvalidDateError("2024-13-45", expected_format="YYYY-MM-DD")
```

#### InvalidCategoryError (FT-VAL-403)

Category is not recognized.

```python
from spreadsheet_dl.exceptions import InvalidCategoryError

raise InvalidCategoryError(
    "InvalidCat",
    valid_categories=["Groceries", "Transport", "Utilities"]
)
```

### Plugin Errors (FT-EXT-900 to FT-EXT-999)

#### PluginNotFoundError (FT-EXT-901)

Plugin is not found.

```python
from spreadsheet_dl.exceptions import PluginNotFoundError

raise PluginNotFoundError("my_plugin")
```

#### PluginLoadError (FT-EXT-902)

Loading a plugin fails.

```python
from spreadsheet_dl.exceptions import PluginLoadError

raise PluginLoadError("my_plugin", reason="Missing dependency: requests")
```

#### HookError (FT-EXT-904)

Plugin hook fails.

```python
from spreadsheet_dl.exceptions import HookError

raise HookError(
    hook_name="before_render",
    plugin_name="analytics",
    reason="API timeout"
)
```

## Usage Examples

### Basic Exception Handling

```python
from spreadsheet_dl.exceptions import SpreadsheetDLError, FileNotFoundError

try:
    generate_budget("budget.ods")
except FileNotFoundError as e:
    print(f"Error: {e.message}")
    print(f"Suggestion: {e.suggestion}")
except SpreadsheetDLError as e:
    print(f"[{e.error_code}] {e.message}")
    if e.details:
        print(f"Details: {e.details}")
```

### Formatted Error Display

```python
from spreadsheet_dl.exceptions import InvalidAmountError

try:
    amount = parse_amount(user_input)
except InvalidAmountError as e:
    # Colored output for terminal
    print(e.format_error(use_color=True))

    # Plain text for logs
    with open("error.log", "a") as f:
        f.write(e.format_error(use_color=False))
```

### JSON Error Response

```python
from spreadsheet_dl.exceptions import SpreadsheetDLError
import json

try:
    process_budget()
except SpreadsheetDLError as e:
    error_response = {
        "success": False,
        "error": e.to_dict()
    }
    print(json.dumps(error_response, indent=2))
```

### Custom Exception with Context

```python
from spreadsheet_dl.exceptions import SpreadsheetDLError, ErrorContext

def validate_budget_file(file_path):
    if not file_path.exists():
        raise SpreadsheetDLError(
            f"Budget file not found: {file_path}",
            error_code="FT-VAL-410",
            details="The specified budget file does not exist",
            suggestion=f"Create a budget file first with: spreadsheet-dl generate",
            context=ErrorContext(file_path=str(file_path))
        )
```

### Exception Hierarchy Usage

```python
from spreadsheet_dl.exceptions import (
    SpreadsheetDLError,
    ValidationError,
    InvalidAmountError
)

try:
    process_transaction()
except InvalidAmountError as e:
    # Handle specific validation error
    print(f"Invalid amount: {e.value}")
except ValidationError as e:
    # Handle any validation error
    print(f"Validation failed: {e.message}")
except SpreadsheetDLError as e:
    # Handle any finance tracker error
    print(f"Operation failed: {e.message}")
```

## CLI Integration

The CLI automatically handles all exceptions:

```python
def main():
    try:
        result = execute_command(args)
        return 0
    except OperationCancelledError:
        print("Operation cancelled.", file=sys.stderr)
        return 1
    except SpreadsheetDLError as e:
        print(e.format_error(use_color=not args.no_color), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled.", file=sys.stderr)
        return 130
```

## Error Code Reference

| Code        | Exception                  | Description                 |
| ----------- | -------------------------- | --------------------------- |
| FT-GEN-001  | UnknownError               | Unknown or unexpected error |
| FT-GEN-002  | OperationCancelledError    | User cancelled operation    |
| FT-GEN-003  | NotImplementedFeatureError | Feature not yet implemented |
| FT-FILE-101 | FileNotFoundError          | Required file not found     |
| FT-FILE-102 | FilePermissionError        | File permission denied      |
| FT-FILE-103 | FileExistsError            | File already exists         |
| FT-FILE-104 | InvalidFileFormatError     | Invalid file format         |
| FT-ODS-201  | OdsReadError               | Cannot read ODS file        |
| FT-ODS-202  | OdsWriteError              | Cannot write ODS file       |
| FT-ODS-203  | SheetNotFoundError         | Sheet not found in ODS      |
| FT-CSV-301  | CSVParseError              | CSV parsing failed          |
| FT-CSV-302  | UnsupportedBankFormatError | Bank format not supported   |
| FT-VAL-401  | InvalidAmountError         | Invalid amount value        |
| FT-VAL-402  | InvalidDateError           | Invalid date value          |
| FT-VAL-403  | InvalidCategoryError       | Invalid category            |
| FT-CFG-501  | MissingConfigError         | Required config missing     |
| FT-NET-601  | ConnectionError            | Connection failed           |
| FT-NET-602  | AuthenticationError        | Authentication failed       |
| FT-TMPL-701 | TemplateNotFoundError      | Template not found          |
| FT-EXT-901  | PluginNotFoundError        | Plugin not found            |
| FT-EXT-902  | PluginLoadError            | Plugin load failed          |
| FT-EXT-904  | HookError                  | Plugin hook failed          |
| FT-SEC-1001 | EncryptionError            | Encryption failed           |
| FT-SEC-1002 | DecryptionError            | Decryption failed           |

## See Also

- [cli](cli.md) - CLI error handling
- [plugins](plugins.md) - Plugin exceptions
- [config](config.md) - Configuration exceptions
