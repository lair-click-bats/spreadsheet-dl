# Changelog

All notable changes to SpreadsheetDL will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0-alpha.1] - 2026-01-03

### Added

- Complete refactoring to SpreadsheetDL universal spreadsheet definition language
- MCP server with 145+ planned tools for Claude integration
- Streaming I/O capability for 100k+ row files
- Round-trip import/export workflows
- Multi-format adapter system (XLSX, CSV, PDF)
- Theme variant switching (light/dark/high-contrast)
- Enhanced chart builder with comprehensive chart types
- Advanced template engine with YAML-based definitions
- Chart embedding infrastructure in OdsRenderer
- Named range support with proper ODF hierarchy
- Workbook properties (title, author, subject, keywords)
- Conditional formatting support
- Data validation rules
- Print area configuration
- Sheet protection capabilities

### Changed

- Renamed project from budget-spreadsheet to spreadsheet-dl
- Upgraded to Python 3.12
- Complete architecture refactoring for universal spreadsheet support
- Enhanced formula builder with 60+ functions
- Improved theme system with accessibility features

### Fixed

- Datetime type check order bug in renderer (datetime vs date isinstance)
- Named Range ODF hierarchy bug (NamedExpressions container required)
- Theme exception handling in style creation

### Tests

- Achieved 97% test coverage across all core modules
- 649 tests passing, 7 skipped (intentional)
- Zero test failures
- Core module coverage: builder.py (99%), charts.py (99%), renderer.py (96%), mcp_server.py (96%)
- Added comprehensive test suites for budget analysis, MCP protocol, and CLI operations

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
