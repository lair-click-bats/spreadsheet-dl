# SpreadsheetDL Test Suite

Comprehensive test suite for SpreadsheetDL with organized pytest markers for selective test execution.

## Test Statistics

- **Total Tests**: ~2,661 tests
- **Unit Tests**: ~2,370 tests (fast, isolated)
- **Integration Tests**: ~291 tests (slower, multi-component)
- **Finance Tests**: ~272 tests
- **MCP Tests**: ~346 tests
- **Domain Tests**: ~504 tests

## Quick Start

```bash
# Run all tests
uv run pytest

# Run only fast unit tests
uv run pytest -m unit

# Run integration tests
uv run pytest -m integration

# Run specific domain tests
uv run pytest -m finance
uv run pytest -m "domain and engineering"
```

## Test Organization

Tests are organized using pytest markers at the module level:

```python
pytestmark = [pytest.mark.unit, pytest.mark.builder]
```

### Available Markers

#### Test Level

- `unit` - Fast, isolated tests (no I/O)
- `integration` - Multi-component tests (slower)

#### Performance

- `slow` - Tests >1 second
- `benchmark` - Performance benchmarks

#### Dependencies

- `requires_yaml` - Needs PyYAML
- `requires_export` - Needs openpyxl/reportlab
- `requires_files` - Creates/reads files

#### Domains

- `domain` - Domain plugin tests
- `finance` - Finance domain
- `science` - Science domains
- `engineering` - Engineering domains
- `manufacturing` - Manufacturing domain

#### Features

- `mcp` - MCP server
- `cli` - CLI interface
- `validation` - Schema validation
- `rendering` - ODS/XLSX/PDF rendering
- `builder` - Builder API
- `templates` - Template system
- `visualization` - Charts/graphs

## Common Usage Patterns

### Run Fast Tests Only

```bash
# Unit tests only (fastest)
uv run pytest -m unit

# Exclude slow tests
uv run pytest -m "unit and not slow"
```

### Run Feature-Specific Tests

```bash
# MCP server tests
uv run pytest -m mcp

# Builder API tests
uv run pytest -m builder

# Validation tests
uv run pytest -m validation
```

### Run Domain Tests

```bash
# All domain tests
uv run pytest -m domain

# Specific domains
uv run pytest -m "domain and finance"
uv run pytest -m "domain and engineering"
uv run pytest -m "domain and science"
```

### Run Tests by Dependency

```bash
# Tests that don't need YAML
uv run pytest -m "not requires_yaml"

# Tests that don't need files
uv run pytest -m "not requires_files"

# Tests that need export dependencies
uv run pytest -m requires_export
```

### Complex Combinations

```bash
# Unit finance tests (not integration)
uv run pytest -m "unit and finance and not integration"

# All rendering tests
uv run pytest -m rendering

# Domain tests excluding slow ones
uv run pytest -m "domain and not slow"
```

## Test Structure

```
tests/
├── test_*.py              # Core functionality tests
├── domains/               # Domain-specific tests
│   ├── test_finance.py
│   ├── test_biology.py
│   ├── test_engineering.py
│   └── ...
└── conftest.py            # Shared fixtures

.claude/hooks/
├── test_hooks.py          # Hook system tests
└── test_quality_enforcement.py
```

## Writing Tests

### Adding Markers to New Tests

```python
"""Test module description."""

from __future__ import annotations

import pytest

# Module-level markers
pytestmark = [pytest.mark.unit, pytest.mark.feature_name]


class TestMyFeature:
    """Test class for my feature."""

    def test_something(self) -> None:
        """Test description."""
        assert True

    @pytest.mark.slow
    def test_slow_operation(self) -> None:
        """This test is marked as slow."""
        # Expensive operation
        pass
```

### Marker Guidelines

1. **Always include a test level marker**: `unit` or `integration`
2. **Add feature markers**: `mcp`, `builder`, `cli`, etc.
3. **Add domain markers**: `finance`, `science`, `engineering` for domain tests
4. **Add dependency markers**: `requires_yaml`, `requires_files` if needed
5. **Mark slow tests**: Use `@pytest.mark.slow` for tests >1 second

## CI/CD Integration

Markers enable efficient CI/CD workflows:

```yaml
# Fast feedback - unit tests only
- name: Fast Tests
  run: uv run pytest -m unit

# Feature validation
- name: MCP Tests
  run: uv run pytest -m mcp

# Full validation
- name: All Tests
  run: uv run pytest
```

## Debugging

### List Tests Without Running

```bash
# See what would run
uv run pytest -m unit --collect-only

# Count tests
uv run pytest -m "unit and finance" --co -q | wc -l
```

### Verbose Output

```bash
# Show test names
uv run pytest -m unit -v

# Show test details
uv run pytest -m unit -vv
```

### Stop on First Failure

```bash
uv run pytest -m unit -x
```

## Documentation

For detailed marker documentation, see:

- [Testing Markers Guide](../docs/testing-markers.md)
- [pytest Documentation](https://docs.pytest.org/en/stable/how-to/mark.html)

## Troubleshooting

### Marker Not Registered

If you see "Unknown pytest.mark.X", add it to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "your_marker: Description",
]
```

### Import Errors

Ensure `import pytest` is present in test files using `pytestmark`.

### Test Not Collected

Check that:

1. Test file starts with `test_`
2. Test function starts with `test_`
3. Markers are defined correctly
4. File is in the `tests/` directory
