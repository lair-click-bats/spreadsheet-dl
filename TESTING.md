# Testing Quick Reference

## Run Tests

```bash
# All tests
uv run pytest

# Fast unit tests only
uv run pytest -m unit

# Integration tests
uv run pytest -m integration

# Specific feature
uv run pytest -m mcp
uv run pytest -m finance
uv run pytest -m builder
```

## Common Patterns

```bash
# Fast tests without slow ones
uv run pytest -m "unit and not slow"

# Finance unit tests
uv run pytest -m "unit and finance"

# Domain-specific
uv run pytest -m "domain and engineering"
uv run pytest -m "domain and science"

# Tests not requiring files
uv run pytest -m "not requires_files"
```

## Available Markers

### Test Level

- `unit` - Fast, isolated
- `integration` - Multi-component

### Domains

- `finance` - Finance domain
- `science` - Science domains
- `engineering` - Engineering
- `manufacturing` - Manufacturing
- `domain` - Domain plugins

### Features

- `mcp` - MCP server
- `cli` - CLI interface
- `builder` - Builder API
- `validation` - Schema validation
- `rendering` - ODS/XLSX/PDF
- `templates` - Templates
- `visualization` - Charts

### Other

- `slow` - Tests >1 second
- `benchmark` - Performance tests
- `requires_yaml` - Needs PyYAML
- `requires_export` - Needs export libs
- `requires_files` - File I/O

## Documentation

- [Full Testing Guide](./tests/README.md)
- [Marker Reference](./docs/testing-markers.md)

## Statistics

- Total: 2,661 tests
- Unit: 2,370 tests (89%)
- Integration: 291 tests (11%)
