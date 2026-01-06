# Changelog

All notable changes to SpreadsheetDL will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- towncrier release notes start -->

## [4.1.0] - 2026-01-06 - Formula Expansion Release

**Major Formula Expansion** - This release nearly doubles the formula library from 157 to 305+ formulas across all 11 domain plugins.

### Added

**Physics Domain Expansion (+25 formulas)**

- Thermodynamics (13 formulas): `IDEAL_GAS_LAW`, `HEAT_TRANSFER`, `CARNOT_EFFICIENCY`, `ENTROPY_CHANGE`, `STEFAN_BOLTZMANN`, `THERMAL_CONDUCTION`, `THERMAL_EXPANSION`, `LATENT_HEAT`, `ADIABATIC_PROCESS`, `WIENS_LAW`, `INTERNAL_ENERGY`, `MEAN_FREE_PATH`, `RMS_VELOCITY`
- Waves (12 formulas): `WAVE_VELOCITY`, `DOPPLER_EFFECT`, `SOUND_INTENSITY`, `STANDING_WAVE`, `BEAT_FREQUENCY`, `WAVE_ENERGY`, `WAVE_POWER`, `STRING_TENSION`, `REFLECTION_COEFFICIENT`, `WAVE_PERIOD`, `ANGULAR_FREQUENCY`, `WAVE_NUMBER`
- Total Physics formulas: 50

**Chemistry Domain Expansion (+20 formulas)**

- Electrochemistry (10 formulas): `NERNST_EQUATION`, `FARADAY_LAW`, `CELL_POTENTIAL`, `GIBBS_ELECTROCHEMICAL`, `ELECTRODE_POTENTIAL`, `MASS_DEPOSITED`, `OVERPOTENTIAL`, `TAFEL_EQUATION`, `CONDUCTIVITY`, `EQUIVALENT_WEIGHT`
- Stoichiometry (10 formulas): `LIMITING_REAGENT`, `PERCENT_YIELD`, `THEORETICAL_YIELD`, `MASS_PERCENT`, `EMPIRICAL_FORMULA`, `MOLECULAR_FORMULA`, `DILUTION`, `TITRATION`, `MOLARITY_DILUTION`, `SOLUTION_MIXING`
- Total Chemistry formulas: 40

**Manufacturing Domain Expansion (+25 formulas)**

- Lean Manufacturing (10 formulas): `VALUE_STREAM_EFFICIENCY`, `LEAN_LEAD_TIME`, `PROCESS_CYCLE_EFFICIENCY`, `LEAN_TAKT_TIME`, `LEAN_CYCLE_TIME`, `TPM_AVAILABILITY`, `SMED_CHANGEOVER`, `KANBAN_QUANTITY`, `LITTLES_LAW`, `FLOW_EFFICIENCY`
- Six Sigma (10 formulas): `DPMO`, `SIGMA_LEVEL`, `CPK`, `PPK`, `RTY`, `SIX_SIGMA_DEFECT_RATE`, `PROCESS_SIGMA`, `CONTROL_LIMIT`, `Z_SCORE`, `GAUGE_RNR`
- Supply Chain (5 formulas): `BULLWHIP_EFFECT`, `NEWSVENDOR_QUANTITY`, `ABC_SCORE`, `SERVICE_LEVEL`, `CASH_CONVERSION_CYCLE`
- Total Manufacturing formulas: 37

**Finance Domain Expansion (+20 formulas)**

- Risk Management (7 formulas): `VAR`, `CVAR`, `PORTFOLIO_VOLATILITY`, `ALPHA`, `TRACKING_ERROR`, `INFORMATION_RATIO`, `DOWNSIDE_DEVIATION`
- Options Pricing (8 formulas): `BS_CALL`, `BS_PUT`, `IMPLIED_VOL`, `OPTION_DELTA`, `OPTION_GAMMA`, `OPTION_THETA`, `OPTION_VEGA`, `OPTION_RHO`
- Bond Analytics (5 formulas): `BOND_PRICE`, `YTM`, `DURATION`, `MDURATION`, `CONVEXITY`
- Total Finance formulas: 35

**Data Science Domain Expansion (+15 formulas)**

- Time Series (5 formulas): `MOVING_AVERAGE`, `EXPONENTIAL_SMOOTHING`, `ACF`, `PACF`, `SEASONALITY`
- Advanced ML Metrics (4 formulas): `ROC_AUC`, `LOG_LOSS`, `COHEN_KAPPA`, `MCC`
- Clustering (3 formulas): `SILHOUETTE_SCORE`, `DAVIES_BOULDIN_INDEX`, `CALINSKI_HARABASZ_INDEX`
- Feature Engineering (3 formulas): `MIN_MAX_NORMALIZE`, `Z_SCORE_STANDARDIZE`, `LOG_TRANSFORM`
- Total Data Science formulas: 29

**Electrical Engineering Domain Expansion (+10 formulas)**

- Digital Logic (5 formulas): `LOGIC_NAND`, `LOGIC_NOR`, `LOGIC_XOR`, `BINARY_TO_DECIMAL`, `DECIMAL_TO_BINARY`
- Filters (5 formulas): `LOW_PASS_CUTOFF`, `HIGH_PASS_CUTOFF`, `BANDPASS_CENTER`, `Q_FACTOR`, `FILTER_ATTENUATION`
- Total Electrical Engineering formulas: 22

**Mechanical Engineering Domain Expansion (+12 formulas)**

- Fluid Mechanics (6 formulas): `REYNOLDS_NUMBER`, `BERNOULLI_EQUATION`, `DARCY_WEISBACH`, `POISEUILLE_LAW`, `DRAG_FORCE`, `LIFT_FORCE`
- Heat Transfer (6 formulas): `CONVECTION_COEFFICIENT`, `RADIATION_HEAT_TRANSFER`, `THERMAL_RESISTANCE`, `LOG_MEAN_TEMP_DIFF`, `FIN_EFFICIENCY`, `NUSSELT_NUMBER`
- Total Mechanical Engineering formulas: 23

**Biology Domain Expansion (+10 formulas)**

- Pharmacokinetics (5 formulas): `CLEARANCE`, `VOLUME_OF_DISTRIBUTION`, `HALF_LIFE`, `LOADING_DOSE`, `MAINTENANCE_DOSE`
- Genetics (5 formulas): `HARDY_WEINBERG`, `LINKAGE_DISEQUILIBRIUM`, `RECOMBINATION_FREQUENCY`, `CHI2_GENETICS`, `INBREEDING_COEFFICIENT`
- Total Biology formulas: 22

**Civil Engineering Domain Expansion (+5 formulas)**

- Foundation (3 formulas): `BEARING_CAPACITY_TERZAGHI`, `SETTLEMENT_ELASTIC`, `CONSOLIDATION_SETTLEMENT`
- Transportation (2 formulas): `STOPPING_DISTANCE`, `TRAFFIC_FLOW`
- Total Civil Engineering formulas: 18

**Security Enhancements**

- Per-tool rate limiting with configurable limits per tool category
- Burst limit protection with automatic cooldown
- Audit log rotation with compression support
- Plugin signature verification design document (implementation in v4.2.0)

**Documentation**

- Consolidated formula reference documentation (docs/reference/formula-reference.md)
- MCP tools reference documentation (docs/reference/mcp-tools-reference.md)
- Examples index with categorized learning paths (docs/reference/examples-index.md)
- Architecture diagrams with Mermaid visualizations (docs/ARCHITECTURE.md)
- Physics and Chemistry domain API documentation
- Domain overview index page

**Test Coverage**

- XLSX chart rendering tests (~1038 lines)
- MCP advanced tools tests (~1170 lines)
- XLSX sparkline tests (~880 lines)
- Streaming large file tests (~700 lines)
- Multi-format roundtrip tests (~900 lines)
- Domain cross-validation tests (~580 lines)
- 5,200+ new lines of test code

### Changed

- MCP rate limiting now supports per-tool configuration
- Audit logging includes automatic rotation when files exceed 10MB
- Rate limit status API provides detailed per-tool statistics

### Security

**New Security Features:**

- Per-tool rate limits prevent resource exhaustion attacks
- Burst detection with automatic cooldown periods
- Configurable rate limits for sensitive operations (exports, imports)
- Audit log rotation prevents disk exhaustion

**Deferred to v4.2.0:**

- Plugin signature verification (design complete)
- PKI integration for plugin trust

### Formula Coverage Summary

| Domain         | v4.0.1  | v4.1.0  | Change   |
| -------------- | ------- | ------- | -------- |
| Physics        | 25      | 50      | +25      |
| Chemistry      | 20      | 40      | +20      |
| Manufacturing  | 12      | 37      | +25      |
| Finance        | 15      | 35      | +20      |
| Data Science   | 14      | 29      | +15      |
| Electrical Eng | 12      | 22      | +10      |
| Mechanical Eng | 11      | 23      | +12      |
| Biology        | 12      | 22      | +10      |
| Civil Eng      | 13      | 18      | +5       |
| Environmental  | 22      | 22      | -        |
| Education      | 27      | 27      | -        |
| **Total**      | **183** | **325** | **+142** |

---

## [Unreleased]

### Added

- Nothing yet

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
  - Install with: `uv pip install spreadsheet-dl[security]`

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

- Marked 5 vulnerabilities as FIXED in v4.0.1
- Updated mitigation code examples to use new security modules
- Added status badges for implemented fixes
- Clarified plugin RCE mitigation (user must disable auto-discovery)

### Security

**Vulnerabilities Addressed:**

- CVE-PENDING-003: XML Entity Expansion (XXE) - HIGH - FIXED
- CVE-PENDING-004: ZIP Bomb DoS - HIGH - FIXED
- CVE-PENDING-002: Path Traversal - CRITICAL - MITIGATED
- CVE-PENDING-005: Formula Injection - MEDIUM - FIXED
- CVE-PENDING-006: Weak Password Brute Force - MEDIUM - FIXED

**Breaking Changes:** None (all security features are backwards compatible)

**Upgrade Recommendations:**

1. Install security dependencies: `uv pip install spreadsheet-dl[security]`
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

### Breaking Changes (Enhanced Builder API)

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
- Chart rendering ODF attribute error
- Serialization module import errors
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

- Expense append functionality
- OdsEditor module for modifying existing ODS files
- `--dry-run` flag for preview mode
- Comprehensive error code system
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

[4.1.0]: https://github.com/lair-click-bats/spreadsheet-dl/releases/tag/v4.1.0
[4.0.1]: https://github.com/lair-click-bats/spreadsheet-dl/releases/tag/v4.0.1
[4.0.0]: https://github.com/lair-click-bats/spreadsheet-dl/releases/tag/v4.0.0
