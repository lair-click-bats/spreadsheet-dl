# Changelog

All notable changes to SpreadsheetDL will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- towncrier release notes start -->

## [Unreleased]

### Added

- **Finance Domain Formulas** - Complete formulas library with 15 functions across 3 categories:
  - Time Value of Money: `PresentValue`, `FutureValue`, `NetPresentValue`, `InternalRateOfReturn`, `PaymentFormula`, `RateFormula`, `PeriodsFormula`
  - Investments: `ReturnOnInvestment`, `CompoundAnnualGrowthRate`, `CompoundInterest`, `SharpeRatio`, `PortfolioBeta`
  - Depreciation: `StraightLineDepreciation`, `DecliningBalanceDepreciation`, `SUMYearsDigitsDepreciation`

- **Data Science Domain Formulas** - Regression analysis metrics (5 formulas):
  - `MeanSquaredError`, `RootMeanSquaredError`, `RSquared`, `MeanAbsoluteError`, `MeanAbsolutePercentageError`

- **Electrical Engineering Domain Formulas** - AC circuit analysis (5 formulas):
  - `RMSValue`, `PowerFactor`, `ComplexImpedance`, `Reactance`, `ResonantFrequency`

- **Civil Engineering Domain Formulas** - Hydrology and drainage (4 formulas):
  - `RunoffCoefficient`, `RationalMethod`, `ManningEquation`, `TimeOfConcentration`

- **Mechanical Engineering Domain Formulas** - Dynamics and vibration (4 formulas):
  - `NaturalFrequency`, `CriticalDamping`, `SpringConstant`, `AngularVelocity`

- **Biology Domain Formulas** - Cell culture and growth analysis (4 formulas):
  - `CellDensity`, `ViabilityPercent`, `DoublingTime`, `SpecificGrowthRate`

- **Manufacturing Domain Formulas** - Production efficiency (1 formula):
  - `OverallEquipmentEffectiveness` (OEE)

- **Environmental Domain Formulas** - Life cycle assessment (3 formulas):
  - `GlobalWarmingPotential`, `AcidificationPotential`, `EutrophicationPotential`

- **Education Domain Formulas** - Educational assessment (3 formulas):
  - `ItemDifficulty`, `ItemDiscrimination`, `CronbachAlpha`

- **Examples Learning Path** - Reorganized examples into progressive structure:
  - `examples/01_basics/` - Getting started (4 examples)
  - `examples/02_formulas/` - Calculations and analysis (4 examples)
  - `examples/03_charts/` - Data visualization (4 examples)
  - `examples/04_advanced/` - Integration and extension (3 examples)
  - Comprehensive README.md files for each section with learning objectives, prerequisites, and estimated time

- **Philosophy Documentation** - Added "Universal Tools, Not Templates" section to README.md explaining:
  - Composable primitives vs. rigid templates
  - Declarative over imperative approach
  - Plugin extensibility model

**Formula Coverage**: Total of 157 formulas (113 existing + 44 new) across 9 domain plugins

### Changed

- **Template System Simplified** - Removed pre-built budget templates and domain templates
  - Domain plugins now focus on formulas, importers, and utilities (universal mathematical tools)
  - Template engine infrastructure retained for user-defined templates
  - Theme system unchanged (5 built-in visual themes)
  - See examples directory for canonical learning path

### Removed

- Budget templates (`50_30_20`, `family`, `minimalist`, `zero_based`, `fire`, `high_income`)
- Domain-specific templates (9 domains)
- CLI `--template` / `-t` flag from generate command
- `templates` CLI command (now shows deprecation message)
- `docs/api/templates/` documentation
- `docs/guides/template-creation.md` guide

### Migration

If you were using budget templates, create allocations programmatically:

```python
from spreadsheet_dl import OdsGenerator, BudgetAllocation, ExpenseCategory
from decimal import Decimal

# Create your own allocations instead of using templates
allocations = [
    BudgetAllocation(ExpenseCategory.HOUSING, Decimal("1500")),
    BudgetAllocation(ExpenseCategory.GROCERIES, Decimal("600")),
    # Add more as needed
]

generator = OdsGenerator(theme="default")
generator.create_budget_spreadsheet("budget.ods", budget_allocations=allocations)
```

---

## [4.0.1] - 2026-01-06 - Security Hardening Release

**Security Fixes:**

This release implements comprehensive security hardening with 5 critical vulnerability mitigations.

### Added

**Security Module Enhancements:**

- Password strength enforcement in `CredentialStore.store_credential()`
  - Automatically rejects weak passwords (< 12 chars, no mixed case/symbols)
  - Provides actionable feedback for password improvement
  - Can be disabled with `enforce_password_strength=False` for testing
- Path traversal prevention utilities (`path_security.py`)
  - `validate_path()` - Validate user paths against base directory
  - `safe_join()` - Securely join path components
  - `is_safe_path()` - Non-throwing path validator
  - `PathSecurityError` exception for security violations

- Formula injection protection (`formulas.py`)
  - `sanitize_cell_ref()` - Validate cell references (A1, $A$1, A1:B10)
  - `sanitize_sheet_name()` - Validate sheet names
  - `FormulaError` exception for invalid/malicious references
  - Automatic validation in FormulaBuilder methods

- XML Entity Expansion (XXE) protection (`streaming.py`)
  - Auto-detect and use defusedxml if available
  - Fallback to stdlib with security warning
  - Protects against Billion Laughs attacks

- ZIP bomb detection (`streaming.py`)
  - Max uncompressed size: 100MB
  - Max compression ratio: 100:1
  - Max file count: 10,000 files
  - Prevents DoS via malicious ODS files

**Security Dependencies:**

- Added `security` optional dependency group in pyproject.toml
  - `defusedxml>=0.7.0` - XXE/XML bomb protection
  - `cryptography>=42.0.0` - Hardware-accelerated encryption
  - Install with: `pip install spreadsheet-dl[security]`

**Security Infrastructure:**

- GitHub Dependabot configuration (`.github/dependabot.yml`)
  - Weekly automated dependency updates
  - Security-critical package grouping
- Comprehensive security scanning workflow (`.github/workflows/security.yml`)
  - dependency-scan: safety + pip-audit for CVE detection
  - code-scan: bandit static security analysis
  - secret-scan: gitleaks for credential exposure
  - codeql: Advanced security code analysis
  - Runs weekly + on every push/PR

**Security Test Suite:**

- `tests/security/test_path_security.py` - 50+ path traversal tests
- `tests/security/test_formula_sanitization.py` - 40+ injection tests
- `tests/security/test_zip_bomb_detection.py` - 20+ DoS tests
- `tests/security/test_password_strength.py` - 30+ password tests
- Total: 140+ new security-focused tests

### Changed

**SECURITY.md Updates:**

- Marked 5 vulnerabilities as ✅ FIXED in v4.0.1
- Updated mitigation code examples to use new security modules
- Added status badges for implemented fixes
- Clarified plugin RCE mitigation (user must disable auto-discovery)

### Security

**Vulnerabilities Addressed:**

- CVE-PENDING-003: XML Entity Expansion (XXE) - HIGH → ✅ FIXED
- CVE-PENDING-004: ZIP Bomb DoS - HIGH → ✅ FIXED
- CVE-PENDING-002: Path Traversal - CRITICAL → ✅ MITIGATED
- CVE-PENDING-005: Formula Injection - MEDIUM → ✅ FIXED
- CVE-PENDING-006: Weak Password Brute Force - MEDIUM → ✅ FIXED

**Breaking Changes:** None (all security features are backwards compatible)

**Upgrade Recommendations:**

1. Install security dependencies: `pip install spreadsheet-dl[security]`
2. Review and apply path validation in file operations
3. Update master passwords if using CredentialStore
4. Enable security scanning in CI/CD pipelines

---

## [4.0.0] - 2026-01-04 - First Public Release

**First Public Release** - Starting at v4.0.0 following extensive internal development (v0.x through v3.x were internal iterations). This version represents a mature, production-ready codebase with comprehensive testing and complete documentation.

**Highlights:**

- Universal spreadsheet definition language for Python
- 9 production-ready domain plugins (Finance, Data Science, Engineering, etc.)
- 18 MCP tools for seamless LLM integration
- Complete API documentation with 6 comprehensive tutorials
- Multi-format export (ODS, XLSX, PDF, CSV, JSON, HTML)
- Enterprise features: streaming I/O, plugins, performance optimization

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

**MCP Server (18 Tools):**

- MCP server with 18 tools for Claude/LLM integration
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

- **3,206 tests passing** (5.0x increase from v2.0)
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

---

## Pre-Public Release Development History

The following versions (v0.1.0 through v2.0.0) represent internal development iterations prior to the first public release (v4.0.0). These entries are preserved for historical reference.

---

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

[4.0.0]: https://github.com/lair-click-bats/spreadsheet-dl/releases/tag/v4.0.0
