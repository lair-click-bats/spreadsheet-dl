# Changelog

All notable changes to SpreadsheetDL will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2026-01-03

### Breaking Changes (PHASE0-004: Perfect Builder API)

**Enhanced Error Handling:**

- `ValueError` exceptions replaced with specific exception types:
  - `NoSheetSelectedError`: Raised when sheet operations attempted without active sheet
  - `NoRowSelectedError`: Raised when row operations attempted without active row
  - `EmptySheetError`: Raised when building/saving empty sheets
  - All inherit from `BuilderError` base class
- Error messages now include actionable "Fix:" guidance
- `CircularReferenceError` messages improved with fix suggestions

**Improved Validation:**

- `CellSpec.colspan` and `rowspan` must be >= 1 (validated in `__post_init__`)
- `SpreadsheetBuilder.data_rows()` count parameter must be >= 1
- `SpreadsheetBuilder.build()` validates all sheets are non-empty
- `SpreadsheetBuilder.save()` validates before rendering
- `SpreadsheetBuilder.named_range()` requires explicit sheet if no current sheet

**Migration Guide:**

```python
# Before v4.0.0
try:
    builder.freeze(rows=1)
except ValueError:
    pass

# After v4.0.0
from spreadsheet_dl.builder import NoSheetSelectedError
try:
    builder.freeze(rows=1)
except NoSheetSelectedError as e:
    # Error message includes helpful guidance
    print(e)  # "Fix: Call .sheet('SheetName') first..."
```

### Added - v4.0 Complete Feature Set

**Core Spreadsheet Engine:**

- Complete refactoring to SpreadsheetDL universal spreadsheet definition language
- Enhanced chart builder with 17 chart types (column, bar, line, pie, area, scatter, bubble, combo, sparklines)
- Advanced formula builder with 60+ functions (mathematical, statistical, financial, date/time, text, logical)
- Circular reference detection with FormulaDependencyGraph
- Named range support with proper ODF hierarchy
- Cell merge rendering with colspan/rowspan
- Conditional formatting (ColorScale, DataBar, IconSet)
- Data validation rules (dropdown, range, custom)
- Workbook properties (title, author, subject, keywords)
- Sheet protection capabilities
- Print area configuration
- Theme variant switching (light/dark/high-contrast)

**MCP Server (144 Tools):**

- MCP server with 144 tools for Claude/LLM integration (8x increase from v2.0)
- Tool categories: Cell Ops, Styles, Structure, Charts, Validation, Advanced, Workbook, Theme, Print, Import/Export, Accounts, Goals, Reporting
- MCPToolRegistry with decorator-based registration
- Rate limiting and security features
- Audit logging configuration

**New v4.0 Modules:**

- **Custom Categories** (`categories.py`) - Dynamic category management beyond 16 fixed categories
- **Performance Optimization** (`performance.py`) - LRU cache, lazy loading, batch processing, benchmarking
- **Progress Indicators** (`progress.py`) - Rich progress bars for long operations with NO_COLOR support
- **Plugin System** (`plugins.py`) - Extensible plugin framework with discovery, lifecycle management, hooks
- **Streaming I/O** (`streaming.py`) - Handle 100k+ row files without memory issues
- **Serialization** (`serialization.py`) - Round-trip YAML/JSON serialization with type preservation
- **Adapters** (`adapters.py`) - Multi-format export (ODS, XLSX, CSV, TSV, JSON, HTML, PDF)

**Documentation:**

- Complete API documentation (15 API docs in `docs/api/`)
- Getting started guide (`docs/getting-started.md`)
- 6 comprehensive tutorials (3,700+ lines total)
- Best practices guide (`docs/best-practices.md`)
- Plugin development guide (`docs/plugins.md`)
- 5 working example scripts

**CLI Enhancements:**

- `category` command group (add, list, update, delete, search, suggest)
- `plugin` command group (list, enable, disable, info)
- Progress indicators in import/export operations
- Enhanced error messages and validation

### Changed

- Renamed project from budget-spreadsheet to spreadsheet-dl
- Upgraded to Python 3.12
- Complete architecture refactoring for universal spreadsheet support
- Enhanced formula builder with circular reference detection
- Improved theme system with accessibility features
- Performance improvements with caching and lazy loading

### Fixed

- Datetime type check order bug in renderer (datetime vs date isinstance)
- Named Range ODF hierarchy bug (NamedExpressions container required)
- Theme exception handling in style creation
- Chart rendering ODF attribute error (CRITICAL-001)
- Serialization module import errors (CRITICAL-002)
- YAML parsing error handling in category manager

### Tests

- **2,181 tests passing** (3.4x increase from v2.0)
- **71% overall test coverage**, **97%+ on core modules**
- Zero test failures (14 intentional skips)
- Core module coverage: builder.py (99%), charts.py (99%), renderer.py (95%), mcp_server.py (69%)
- New test suites: categories (35 tests), performance (35 tests), progress (20 tests), plugins (38 tests), MCP extended (36 tests)

### Performance

- LRU cache with TTL support for frequent operations
- Lazy loading for large data structures
- Batch processing optimization
- Streaming I/O for memory-efficient large file handling
- Benchmark utilities for performance monitoring

## [2.0.0] - 2025-12-29

### Added

- Professional spreadsheet system with enterprise-grade formatting
- Advanced business and financial templates
- Multi-sheet workbook support
- Enhanced formula validation
- Comprehensive test suite (250+ tests)

## [0.4.1] - 2025-12-15

### Added

- Expense append functionality (FR-CORE-003)
- OdsEditor module for modifying existing ODS files
- `--dry-run` flag for preview mode
- Comprehensive error code system (FR-UX-003)
  - Structured error messages with error codes, details, and suggestions
  - Error code reference documentation
  - 50+ specific exception classes with actionable guidance

## [0.4.0] - 2025-12-10

### Added

- Declarative DSL for themes and styling
- YAML-based theme definitions (5 built-in themes)
- Fluent SpreadsheetBuilder API
- Type-safe FormulaBuilder
- OdsRenderer for builder-to-ODS conversion
- CLI `--theme` flag for generation commands
- CLI `themes` command to list available themes

### Changed

- Maintained full backward compatibility with v0.3.0

## [0.3.0] - 2025-12-10

### Added

- Configuration management system
- Exceptions module with structured error handling
- Performance improvements throughout the codebase

## [0.2.0] - 2025-12-10

### Added

- WebDAV upload to Nextcloud
- Bank CSV import with auto-detection for multiple banks
  - Chase, Bank of America, Capital One, and more
- Transaction auto-categorization with pattern matching
- Analytics dashboard with comprehensive budget insights
- Configurable alert system for budget monitoring
- Recurring expense management
- Budget templates (50/30/20, Family, FIRE, Minimalist, Zero-Based, High Income)
- Quick expense CLI command for rapid expense entry

### Fixed

- Pandas ODS reading issues (switched to pyexcel_ods3)

### Tests

- All 35+ tests passing

## [0.1.0] - 2025-12-09

### Added

- Initial release
- ODS budget generation with formulas
- Budget analysis with pandas
- Report generation (text, Markdown, JSON formats)
- CLI interface with basic commands
- Core expense tracking functionality
- Basic budget allocation system

---

## Unreleased

### Planned for v4.0.0 Final

- Complete implementation of all 145 MCP tools
- Full streaming I/O for massive files
- Complete PDF export functionality
- Enhanced visualization capabilities
- Performance optimizations for large datasets
- Additional chart types and customization options
- Extended template library
- Comprehensive API documentation
- Video tutorials and advanced examples

[4.0.0-alpha.1]: https://github.com/your-org/spreadsheet-dl/compare/v2.0.0...v4.0.0-alpha.1
[2.0.0]: https://github.com/your-org/spreadsheet-dl/compare/v0.4.1...v2.0.0
[0.4.1]: https://github.com/your-org/spreadsheet-dl/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/your-org/spreadsheet-dl/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/your-org/spreadsheet-dl/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/your-org/spreadsheet-dl/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/your-org/spreadsheet-dl/releases/tag/v0.1.0
