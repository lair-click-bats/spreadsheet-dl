# Pytest Markers Guide

This document describes the pytest markers used in the SpreadsheetDL test suite for organizing and selectively running tests.

## Available Markers

### Test Level Markers

- **`unit`** - Fast, isolated unit tests with no I/O
- **`integration`** - Integration tests involving multiple components (slower)

### Performance Markers

- **`slow`** - Tests taking >1 second to run
- **`benchmark`** - Performance benchmark tests

### Dependency Markers

- **`requires_yaml`** - Tests requiring PyYAML library
- **`requires_export`** - Tests requiring export dependencies (openpyxl, reportlab)
- **`requires_files`** - Tests that create/read files

### Domain Markers

- **`domain`** - Domain-specific plugin tests
- **`finance`** - Finance domain tests
- **`science`** - Science domain tests (biology, chemistry, etc.)
- **`engineering`** - Engineering domain tests
- **`manufacturing`** - Manufacturing domain tests

### Feature Markers

- **`mcp`** - MCP server functionality tests
- **`cli`** - CLI interface tests
- **`validation`** - Schema and data validation tests
- **`rendering`** - ODS/XLSX/PDF rendering tests
- **`builder`** - Builder API tests
- **`templates`** - Template system tests
- **`visualization`** - Chart and visualization tests

## Usage Examples

### Run only fast unit tests

```bash
uv run pytest -m unit
```

### Run only integration tests

```bash
uv run pytest -m integration
```

### Run unit tests excluding slow ones

```bash
uv run pytest -m "unit and not slow"
```

### Run all finance-related tests

```bash
uv run pytest -m finance
```

### Run only finance unit tests (not integration)

```bash
uv run pytest -m "finance and not integration"
```

### Run domain plugin tests for engineering

```bash
uv run pytest -m "domain and engineering"
```

### Run MCP server tests

```bash
uv run pytest -m mcp
```

### Run tests that don't require external files

```bash
uv run pytest -m "not requires_files"
```

### Run visualization and chart tests

```bash
uv run pytest -m visualization
```

### Run builder API tests

```bash
uv run pytest -m builder
```

## Combining Markers

You can use boolean expressions to combine markers:

- **AND**: `pytest -m "unit and finance"`
- **OR**: `pytest -m "finance or science"`
- **NOT**: `pytest -m "not slow"`
- **Complex**: `pytest -m "(unit or integration) and not slow and finance"`

## Test Organization

Tests are organized with markers at the module level using `pytestmark`:

```python
# Single marker
pytestmark = pytest.mark.unit

# Multiple markers
pytestmark = [pytest.mark.unit, pytest.mark.finance]
```

Individual test classes or functions can also have additional markers:

```python
@pytest.mark.slow
def test_large_dataset():
    """This test takes a while..."""
    pass
```

## Statistics

Current test distribution (approximate):

- **Unit tests**: ~1,950 tests
- **Integration tests**: ~375 tests
- **Finance tests**: ~300+ tests
- **Domain tests**: ~625 tests
- **MCP tests**: ~465 tests

## CI/CD Integration

For continuous integration, you can run different marker groups:

```bash
# Fast checks (unit only)
uv run pytest -m unit

# Full test suite
uv run pytest

# Specific feature validation
uv run pytest -m "mcp or builder or validation"
```

## Adding New Markers

1. Define the marker in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "new_marker: Description of the new marker",
]
```

1. Apply to test files:

```python
pytestmark = [pytest.mark.unit, pytest.mark.new_marker]
```

## Best Practices

- Use `unit` for fast, isolated tests
- Use `integration` for tests involving multiple components or I/O
- Use `slow` for tests >1 second
- Add domain markers (`finance`, `science`, etc.) for domain-specific tests
- Add feature markers (`mcp`, `cli`, etc.) for feature-specific tests
- Combine markers thoughtfully - most tests should have 1-3 markers
