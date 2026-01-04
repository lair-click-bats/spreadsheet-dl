# SpreadsheetDL - Comprehensive Requirements Specification

**Document Version:** 2.1.0
**Analysis Date:** 2025-12-28
**Project Version Analyzed:** 4.0.0
**Status:** Historical Reference (Pre-v4.0.0 Development)

---

## Executive Summary

This document provides historical requirements analysis for the SpreadsheetDL project during its development phase. The analysis was based on the codebase state during v0.4.0 development and guided the evolution toward v4.0.0.

SpreadsheetDL is now a universal spreadsheet definition language with LLM-optimized MCP server integration, supporting multiple output formats (ODS, XLSX, PDF) and domain-specific plugins (Finance, Data Science, Engineering).

**Version 2.0.0 Enhancements:** Added detailed requirements for UI/UX, Extensibility, Template/Config System, and Formatting based on comprehensive codebase audit.

---

## Table of Contents

1. [Current State Analysis](#1-current-state-analysis)
2. [Gap Analysis](#2-gap-analysis)
3. [Functional Requirements](#3-functional-requirements)
4. [Non-Functional Requirements](#4-non-functional-requirements)
5. [Data Requirements](#5-data-requirements)
6. [Integration Requirements](#6-integration-requirements)
7. [Quality Requirements](#7-quality-requirements)
8. [Documentation Requirements](#8-documentation-requirements)
9. [Automation Requirements](#9-automation-requirements)
10. [UI/UX Requirements](#10-uiux-requirements) **(NEW)**
11. [Extensibility Requirements](#11-extensibility-requirements) **(NEW)**
12. [Template/Config System Requirements](#12-templateconfig-system-requirements) **(NEW)**
13. [Formatting Requirements](#13-formatting-requirements) **(NEW)**
14. [Prioritization Framework](#14-prioritization-framework)
15. [Traceability Matrix](#15-traceability-matrix)

---

## 1. Current State Analysis

### 1.1 Project Overview

| Attribute       | Value          |
| --------------- | -------------- |
| Name            | spreadsheet-dl |
| Version         | 0.4.0          |
| Language        | Python 3.11+   |
| Package Manager | uv             |
| Build System    | hatchling      |
| License         | MIT            |

### 1.2 Architecture

```
src/spreadsheet_dl/
├── __init__.py              # Package exports (68 exports)
├── ods_generator.py         # ODS file creation with odfpy
├── budget_analyzer.py       # Pandas-based analysis with pyexcel_ods3
├── report_generator.py      # Text/Markdown/JSON reports
├── cli.py                   # Argparse CLI (12 commands)
├── csv_import.py            # Bank CSV import (8 bank formats)
├── webdav_upload.py         # Nextcloud WebDAV integration
├── analytics.py             # Dashboard analytics
├── alerts.py                # Budget monitoring system
├── recurring.py             # Recurring expense management
├── templates.py             # Budget templates (6 templates)
├── builder.py               # Fluent API for spreadsheet construction
├── renderer.py              # Builder to ODS rendering
├── config.py                # YAML/environment configuration
├── exceptions.py            # Exception hierarchy (20+ exceptions)
├── schema/                  # Theme system
│   ├── styles.py            # Style dataclasses
│   ├── loader.py            # YAML theme loader
│   └── validation.py        # Schema validation
└── themes/                  # 5 built-in themes
    ├── default.yaml
    ├── corporate.yaml
    ├── minimal.yaml
    ├── dark.yaml
    └── high_contrast.yaml
```

### 1.3 Current Features

#### Core Features (v0.1.0-v0.3.0)

- [x] ODS spreadsheet generation with formulas (SUM, SUMIF, VLOOKUP)
- [x] Budget analysis with pandas
- [x] Report generation (text, Markdown, JSON)
- [x] CLI interface with 12 commands
- [x] 16 expense categories
- [x] WebDAV upload to Nextcloud
- [x] Bank CSV import (8 formats: Chase, BoA, Capital One, etc.)
- [x] Auto-categorization with regex patterns
- [x] Analytics dashboard
- [x] Alert system with configurable thresholds
- [x] Recurring expense management
- [x] 6 budget templates (50/30/20, Family, FIRE, etc.)
- [x] Configuration management (YAML + environment)
- [x] Exception hierarchy

#### DSL Features (v0.4.0)

- [x] YAML-based theme definitions
- [x] 5 built-in visual themes
- [x] Fluent SpreadsheetBuilder API
- [x] Type-safe FormulaBuilder
- [x] Theme inheritance support
- [x] Color palette system
- [x] Style inheritance with `extends`

### 1.4 Technical Stack

| Component      | Technology          |
| -------------- | ------------------- |
| ODS Generation | odfpy 1.4.1+        |
| Data Analysis  | pandas 2.1.0+       |
| ODS Reading    | pyexcel-ods3 0.6.1+ |
| HTTP/WebDAV    | requests 2.31.0+    |
| Config         | PyYAML (optional)   |
| Testing        | pytest 8.0+         |
| Linting        | ruff 0.8+           |
| Type Checking  | mypy 1.13+          |
| CI/CD          | GitHub Actions      |

### 1.5 Test Coverage

- 3,206 tests across 19 test files
- Integration tests for CLI commands
- CI runs on Python 3.11 and 3.12
- Coverage reporting via Codecov

---

## 2. Gap Analysis

### 2.1 Critical Gaps

| ID   | Gap                                                | Severity | Impact                              |
| ---- | -------------------------------------------------- | -------- | ----------------------------------- |
| G-01 | No data encryption at rest                         | High     | Financial data security risk        |
| G-02 | Quick expense entry doesn't actually append to ODS | High     | Core functionality incomplete       |
| G-03 | No multi-currency support                          | Medium   | Limits international use            |
| G-04 | No data backup/restore functionality               | Medium   | Data loss risk                      |
| G-05 | No account/balance tracking                        | Medium   | Missing fundamental finance feature |

### 2.2 Feature Gaps

| ID   | Gap                      | Current State            | Ideal State                      |
| ---- | ------------------------ | ------------------------ | -------------------------------- |
| G-06 | No goal tracking         | None                     | Track savings goals, debt payoff |
| G-07 | No investment tracking   | None                     | Portfolio tracking, dividends    |
| G-08 | No budget forecasting    | None                     | ML-based spending predictions    |
| G-09 | Limited visualization    | JSON chart data only     | Interactive charts               |
| G-10 | No mobile app            | Nextcloud app dependency | Native mobile support            |
| G-11 | No transaction splitting | None                     | Split bills across categories    |
| G-12 | No receipt attachment    | None                     | Link receipts to transactions    |
| G-13 | No tax categorization    | None                     | Tax-deductible tracking          |
| G-14 | No shared budgets        | None                     | Multi-user household support     |
| G-15 | No notification system   | Alerts only              | Email/push notifications         |

### 2.3 Integration Gaps

| ID   | Gap                        | Current State   | Ideal State             |
| ---- | -------------------------- | --------------- | ----------------------- |
| G-16 | Limited bank formats       | 8 formats       | 50+ formats + Plaid     |
| G-17 | No direct bank sync        | CSV import only | API-based sync          |
| G-18 | No calendar integration    | None            | Bill due date reminders |
| G-19 | No export to other formats | ODS only        | Excel, PDF, CSV export  |
| G-20 | No cloud backup            | Nextcloud only  | Multi-cloud support     |

### 2.4 Technical Debt

| ID    | Issue                         | Location             | Severity |
| ----- | ----------------------------- | -------------------- | -------- |
| TD-01 | Some odfpy type ignores       | pyproject.toml       | Low      |
| TD-02 | Architecture doc outdated     | docs/ARCHITECTURE.md | Medium   |
| TD-03 | No API documentation          | None                 | Medium   |
| TD-04 | Limited error messages in CLI | cli.py               | Low      |
| TD-05 | Hardcoded USD currency        | Multiple files       | Medium   |

### 2.5 Documentation Gaps

| ID   | Gap                            | Priority |
| ---- | ------------------------------ | -------- |
| D-01 | No API reference documentation | High     |
| D-02 | No user guide/tutorial         | High     |
| D-03 | No contribution guidelines     | Medium   |
| D-04 | No security documentation      | High     |
| D-05 | No deployment guide            | Medium   |

### 2.6 UI/UX Gaps (NEW)

| ID      | Gap                         | Current State                   | Ideal State                   |
| ------- | --------------------------- | ------------------------------- | ----------------------------- |
| G-UX-01 | No progress indicators      | Silent operations               | Visual progress feedback      |
| G-UX-02 | Inconsistent error messages | Basic exception output          | Structured, actionable errors |
| G-UX-03 | No command discovery        | Manual help lookup              | Interactive discovery         |
| G-UX-04 | Limited help examples       | Static epilog examples          | Context-aware examples        |
| G-UX-05 | No color coding in output   | Monochrome except --no-color    | Semantic color output         |
| G-UX-06 | No confirmation prompts     | Destructive ops without confirm | Safe defaults                 |
| G-UX-07 | No shell completions        | Manual typing                   | Tab completion                |
| G-UX-08 | Limited accessibility       | High-contrast theme only        | Full a11y support             |

### 2.7 Extensibility Gaps (NEW)

| ID       | Gap                         | Current State       | Ideal State              |
| -------- | --------------------------- | ------------------- | ------------------------ |
| G-EXT-01 | No plugin system            | Hardcoded features  | Plugin architecture      |
| G-EXT-02 | No custom category support  | Fixed 16 categories | User-defined categories  |
| G-EXT-03 | No custom formula support   | Predefined formulas | User formula definitions |
| G-EXT-04 | No extension hooks          | No event system     | Pre/post operation hooks |
| G-EXT-05 | No third-party integrations | Nextcloud only      | Integration framework    |

### 2.8 Template/Config Gaps (NEW)

| ID       | Gap                        | Current State    | Ideal State             |
| -------- | -------------------------- | ---------------- | ----------------------- |
| G-CFG-01 | No config migration        | Manual updates   | Automatic migration     |
| G-CFG-02 | No config validation       | Silent failures  | Schema validation       |
| G-CFG-03 | No template versioning     | No versions      | Semver templates        |
| G-CFG-04 | No template sharing        | Local only       | Export/import templates |
| G-CFG-05 | Limited override hierarchy | File + env + CLI | Full cascade system     |

### 2.9 Formatting Gaps (NEW)

| ID       | Gap                       | Current State      | Ideal State              |
| -------- | ------------------------- | ------------------ | ------------------------ |
| G-FMT-01 | Hardcoded currency format | $#,##0.00 only     | Configurable per locale  |
| G-FMT-02 | Limited date formats      | YYYY-MM-DD only    | Multiple format support  |
| G-FMT-03 | No negative number styles | -$X.XX only        | (X.XX), red text options |
| G-FMT-04 | No print layout control   | Default page setup | Custom page/margins      |
| G-FMT-05 | Format loss on export     | ODS-specific       | Format preservation      |

---

## 3. Functional Requirements

### 3.1 Core Budget Management

#### FR-CORE-001: Budget Creation

**Priority:** P0 (Critical)
**Status:** Implemented

The system SHALL:

- Generate ODS spreadsheets with configurable month/year
- Support multiple sheets (Expense Log, Budget, Summary)
- Include working formulas (SUM, SUMIF, VLOOKUP)
- Apply visual themes to generated spreadsheets
- Pre-populate budget allocations from templates
- Support custom expense categories

**Acceptance Criteria:**

- AC1: Generated ODS files open in LibreOffice and Collabora
- AC2: Formulas calculate correctly when data is entered
- AC3: All 5 built-in themes apply correctly
- AC4: All 6 budget templates generate correct allocations

#### FR-CORE-002: Budget Analysis

**Priority:** P0 (Critical)
**Status:** Implemented

The system SHALL:

- Load and parse ODS budget files
- Calculate total spending vs budget
- Break down spending by category
- Generate alerts for over-budget categories
- Support date range filtering
- Export analysis as JSON

**Acceptance Criteria:**

- AC1: Parse expenses with 100% accuracy
- AC2: Handle empty budget files gracefully
- AC3: Category percentages sum to correct totals

#### FR-CORE-003: Expense Entry

**Priority:** P0 (Critical)
**Status:** Partial (CLI exists but doesn't append)

The system SHALL:

- Accept quick expense entries via CLI
- Auto-categorize based on description
- Append to existing ODS files
- Support bulk import from CSV
- Validate amounts and dates

**Acceptance Criteria:**

- AC1: CLI `expense` command appends to ODS file
- AC2: Auto-categorization accuracy > 80%
- AC3: Invalid inputs produce helpful error messages

#### FR-CORE-004: Account Management

**Priority:** P1 (High)
**Status:** Not Implemented

The system SHALL:

- Track multiple accounts (checking, savings, credit)
- Maintain running balances
- Support account transfers
- Link transactions to accounts
- Calculate net worth

**Acceptance Criteria:**

- AC1: Account balances reconcile with transactions
- AC2: Transfers appear in both accounts
- AC3: Net worth calculation includes all accounts

### 3.2 Import and Export

#### FR-IMPORT-001: Bank CSV Import

**Priority:** P0 (Critical)
**Status:** Implemented

The system SHALL:

- Auto-detect bank format from CSV headers
- Support 8+ bank formats (Chase, BoA, Capital One, etc.)
- Handle various date and amount formats
- Filter expenses from income
- Categorize transactions automatically

**Acceptance Criteria:**

- AC1: All 8 bank formats parse correctly
- AC2: Date parsing handles regional formats
- AC3: Currency symbols and commas handled

#### FR-IMPORT-002: Extended Bank Support

**Priority:** P2 (Medium)
**Status:** Not Implemented

The system SHALL:

- Support 50+ bank/credit card formats
- Provide format builder for custom banks
- Save custom formats for reuse
- Validate CSV structure before import

**Acceptance Criteria:**

- AC1: Custom format builder accessible via CLI
- AC2: Saved formats persist across sessions
- AC3: Clear error messages for incompatible CSVs

#### FR-IMPORT-003: Bank API Integration

**Priority:** P3 (Low)
**Status:** Not Implemented

The system SHALL:

- Integrate with Plaid or similar service
- Support direct bank connection
- Auto-sync transactions periodically
- Handle multi-factor authentication

**Acceptance Criteria:**

- AC1: OAuth flow for bank connection
- AC2: Automatic sync configurable
- AC3: Secure credential storage

#### FR-EXPORT-001: Multi-Format Export

**Priority:** P2 (Medium)
**Status:** Partial (ODS only)

The system SHALL:

- Export to ODS (current)
- Export to Excel (.xlsx)
- Export to CSV
- Export to PDF (reports)
- Maintain formatting in exports

**Acceptance Criteria:**

- AC1: Excel files open in Microsoft Excel
- AC2: PDF reports print correctly
- AC3: CSV exports reimportable

### 3.3 Reporting and Analytics

#### FR-REPORT-001: Standard Reports

**Priority:** P0 (Critical)
**Status:** Implemented

The system SHALL:

- Generate text, Markdown, and JSON reports
- Include spending summaries
- Show category breakdowns
- Display alerts and warnings
- Support output to file or stdout

**Acceptance Criteria:**

- AC1: All 3 formats generate correctly
- AC2: Markdown renders properly
- AC3: JSON is valid and parseable

#### FR-REPORT-002: Advanced Analytics

**Priority:** P1 (High)
**Status:** Partial

The system SHALL:

- Calculate spending trends over time
- Project end-of-month spending
- Compare month-over-month
- Identify spending anomalies
- Provide daily spending averages

**Acceptance Criteria:**

- AC1: Trend calculations accurate
- AC2: Projections update as data changes
- AC3: Anomaly detection triggers alerts

#### FR-REPORT-003: Interactive Visualization

**Priority:** P2 (Medium)
**Status:** Not Implemented

The system SHALL:

- Generate interactive HTML charts
- Support pie, bar, and line charts
- Allow drill-down by category
- Export charts as images
- Provide embedded dashboard

**Acceptance Criteria:**

- AC1: Charts render in modern browsers
- AC2: Touch-friendly for mobile
- AC3: PNG/SVG export works

### 3.4 Recurring Transactions

#### FR-RECUR-001: Recurring Expense Management

**Priority:** P0 (Critical)
**Status:** Implemented

The system SHALL:

- Define recurring expenses (name, amount, frequency)
- Support multiple frequencies (daily to yearly)
- Generate entries for date ranges
- Calculate monthly totals
- Provide common templates (Netflix, rent, etc.)

**Acceptance Criteria:**

- AC1: All frequencies work correctly
- AC2: Monthly totals match expected
- AC3: Templates cover common expenses

#### FR-RECUR-002: Bill Reminders

**Priority:** P2 (Medium)
**Status:** Not Implemented

The system SHALL:

- Track bill due dates
- Send reminder notifications
- Mark bills as paid
- Integrate with calendar
- Support auto-pay tracking

**Acceptance Criteria:**

- AC1: Reminders sent before due date
- AC2: Calendar events created
- AC3: Paid status updates correctly

### 3.5 Goal Tracking

#### FR-GOAL-001: Savings Goals

**Priority:** P2 (Medium)
**Status:** Not Implemented

The system SHALL:

- Create savings goals with targets
- Track progress toward goals
- Calculate projected completion
- Support multiple concurrent goals
- Provide goal suggestions

**Acceptance Criteria:**

- AC1: Progress percentage accurate
- AC2: Completion dates calculated
- AC3: Visual progress indicators

#### FR-GOAL-002: Debt Payoff

**Priority:** P2 (Medium)
**Status:** Not Implemented

The system SHALL:

- Track debts with balances and rates
- Calculate payoff timelines
- Support snowball/avalanche methods
- Show interest saved
- Generate payment schedules

**Acceptance Criteria:**

- AC1: Interest calculations accurate
- AC2: Both payoff methods work
- AC3: Schedules exportable

### 3.6 Multi-Currency Support

#### FR-CURR-001: Currency Handling

**Priority:** P2 (Medium)
**Status:** Not Implemented

The system SHALL:

- Support multiple currencies
- Configure default currency
- Convert between currencies
- Track exchange rates
- Display currency symbols correctly

**Acceptance Criteria:**

- AC1: All major currencies supported
- AC2: Conversions use current rates
- AC3: Reports show correct symbols

### 3.7 Security Features

#### FR-SEC-001: Data Encryption

**Priority:** P1 (High)
**Status:** Not Implemented

The system SHALL:

- Encrypt sensitive data at rest
- Use secure key management
- Support password-protected exports
- Secure credential storage
- Audit access to files

**Acceptance Criteria:**

- AC1: AES-256 encryption for files
- AC2: Keys stored securely
- AC3: Audit log maintained

---

## 4. Non-Functional Requirements

### 4.1 Performance

#### NFR-PERF-001: Response Time

The system SHALL:

- Generate ODS files in < 2 seconds for typical budgets
- Analyze 1000+ transactions in < 1 second
- Import CSVs with 10,000 rows in < 5 seconds

#### NFR-PERF-002: Resource Usage

The system SHALL:

- Use < 256MB RAM for typical operations
- Keep CPU usage < 50% during file generation
- Support budgets with 50,000+ transactions

### 4.2 Reliability

#### NFR-REL-001: Data Integrity

The system SHALL:

- Never lose user data during operations
- Validate data before writing
- Maintain transaction atomicity
- Support graceful degradation

#### NFR-REL-002: Error Recovery

The system SHALL:

- Recover from interrupted operations
- Provide clear error messages
- Log errors for debugging
- Support resume of failed imports

### 4.3 Usability

#### NFR-USE-001: CLI Interface

The system SHALL:

- Provide intuitive command structure
- Include helpful error messages
- Support --help on all commands
- Use consistent argument patterns
- Provide progress indicators

#### NFR-USE-002: API Usability

The system SHALL:

- Follow Python conventions (PEP 8)
- Provide type hints on all functions
- Include docstrings with examples
- Maintain backward compatibility

### 4.4 Security

#### NFR-SEC-001: Credential Security

The system SHALL:

- Never log credentials
- Use secure credential storage
- Support app passwords for Nextcloud
- Mask sensitive data in output

#### NFR-SEC-002: Input Validation

The system SHALL:

- Validate all user inputs
- Sanitize file paths
- Prevent path traversal attacks
- Handle malformed data gracefully

### 4.5 Maintainability

#### NFR-MAINT-001: Code Quality

The system SHALL:

- Maintain > 80% test coverage
- Pass all linting rules (ruff)
- Pass type checking (mypy strict)
- Follow Python best practices

#### NFR-MAINT-002: Modularity

The system SHALL:

- Maintain single responsibility principle
- Support plugin architecture
- Allow component replacement
- Document module dependencies

### 4.6 Compatibility

#### NFR-COMP-001: Platform Support

The system SHALL:

- Run on Linux, macOS, and Windows
- Support Python 3.11+
- Work with LibreOffice 7.0+
- Work with Collabora Office

#### NFR-COMP-002: File Compatibility

The system SHALL:

- Generate valid ODF 1.2 files
- Open in Microsoft Excel (view only)
- Support files from Collabora Office
- Handle file version migrations

### 4.7 Accessibility

#### NFR-ACC-001: Theme Accessibility

The system SHALL:

- Provide high-contrast theme
- Meet WCAG 2.1 AA standards
- Support screen readers
- Use colorblind-friendly palettes

---

## 5. Data Requirements

### 5.1 Data Models

#### DR-MODEL-001: Expense Entry

```python
@dataclass
class ExpenseEntry:
    id: str                    # Unique identifier (NEW)
    date: date
    category: ExpenseCategory
    description: str
    amount: Decimal
    notes: str = ""
    account_id: str | None = None  # (NEW)
    receipt_path: str | None = None  # (NEW)
    tags: list[str] = field(default_factory=list)  # (NEW)
    is_tax_deductible: bool = False  # (NEW)
    split_from: str | None = None  # (NEW)
```

#### DR-MODEL-002: Account

```python
@dataclass
class Account:
    id: str
    name: str
    type: AccountType  # CHECKING, SAVINGS, CREDIT, INVESTMENT
    institution: str
    balance: Decimal
    currency: str = "USD"
    is_active: bool = True
    last_synced: datetime | None = None
```

#### DR-MODEL-003: Goal

```python
@dataclass
class Goal:
    id: str
    name: str
    target_amount: Decimal
    current_amount: Decimal
    target_date: date | None
    category: GoalCategory  # SAVINGS, DEBT_PAYOFF, PURCHASE
    priority: int
    is_completed: bool = False
```

### 5.2 Storage Requirements

#### DR-STORE-001: Data Persistence

The system SHALL:

- Store primary data in ODS format
- Cache analysis in JSON files
- Store configuration in YAML
- Support SQLite for indexing (optional)

#### DR-STORE-002: Backup Requirements

The system SHALL:

- Auto-backup before destructive operations
- Maintain 30 days of backups
- Support manual backup triggers
- Compress backup files

### 5.3 Privacy Requirements

#### DR-PRIV-001: Data Minimization

The system SHALL:

- Collect only necessary data
- Not transmit data to third parties
- Run entirely locally (except Nextcloud sync)
- Allow data deletion on request

#### DR-PRIV-002: Compliance

The system SHOULD:

- Support GDPR export requirements
- Allow full data export in portable format
- Document data handling practices

---

## 6. Integration Requirements

### 6.1 Nextcloud Integration

#### IR-NC-001: WebDAV Upload

**Status:** Implemented

The system SHALL:

- Upload files via WebDAV
- Support app passwords
- Handle connection errors
- Verify upload success

#### IR-NC-002: Bidirectional Sync

**Status:** Not Implemented

The system SHALL:

- Download edited files from Nextcloud
- Detect file conflicts
- Merge changes where possible
- Support sync scheduling

### 6.2 Claude/MCP Integration

#### IR-MCP-001: LibreOffice MCP

**Status:** Documented

The system SHALL:

- Document MCP setup process
- Support natural language queries
- Restrict file access paths
- Provide analysis responses

#### IR-MCP-002: Native MCP Server

**Status:** Not Implemented

The system SHOULD:

- Provide native MCP server for finance operations
- Expose budget analysis as tools
- Support natural language expense entry
- Generate reports on request

### 6.3 Calendar Integration

#### IR-CAL-001: Bill Due Dates

**Status:** Not Implemented

The system SHALL:

- Export due dates to ICS format
- Support Google Calendar sync
- Create recurring calendar events
- Include payment details in events

### 6.4 Notification Integration

#### IR-NOTIF-001: Alert Notifications

**Status:** Not Implemented

The system SHALL:

- Send email notifications
- Support push notifications (optional)
- Integrate with ntfy.sh
- Provide notification templates

---

## 7. Quality Requirements

### 7.1 Testing Requirements

#### QR-TEST-001: Unit Test Coverage

The system SHALL:

- Maintain > 80% code coverage
- Test all public API functions
- Include negative test cases
- Test edge cases and boundaries

#### QR-TEST-002: Integration Testing

The system SHALL:

- Test CLI command workflows
- Test file I/O operations
- Test external integrations (mocked)
- Run in CI on every PR

#### QR-TEST-003: Performance Testing

The system SHALL:

- Benchmark file generation times
- Test with large datasets
- Monitor memory usage
- Track performance regressions

### 7.2 Validation Requirements

#### QR-VAL-001: Data Validation

The system SHALL:

- Validate all user inputs
- Check file formats before processing
- Verify configuration completeness
- Report validation errors clearly

#### QR-VAL-002: Schema Validation

The system SHALL:

- Validate theme YAML against schema
- Verify ODS file structure
- Check formula syntax
- Validate CSV column mappings

### 7.3 Error Handling

#### QR-ERR-001: Exception Handling

The system SHALL:

- Use typed exception hierarchy
- Include error codes for programmatic handling
- Provide user-friendly messages
- Log full tracebacks for debugging

---

## 8. Documentation Requirements

### 8.1 User Documentation

#### DOC-USER-001: User Guide

Create comprehensive user guide covering:

- Installation and setup
- Basic usage tutorials
- CLI command reference
- Template customization
- Troubleshooting guide

#### DOC-USER-002: Quick Start Guide

Create 5-minute quick start covering:

- Install with uv
- Generate first budget
- Add expenses
- Generate report

### 8.2 API Documentation

#### DOC-API-001: API Reference

Generate complete API documentation:

- All public classes and functions
- Type signatures and examples
- Module organization guide
- Version migration notes

#### DOC-API-002: Integration Guide

Document integration points:

- Nextcloud/WebDAV setup
- MCP server configuration
- Custom bank format creation
- Theme development guide

### 8.3 Developer Documentation

#### DOC-DEV-001: Contribution Guide

Create contributor documentation:

- Development environment setup
- Code style guidelines
- PR process and requirements
- Release process

#### DOC-DEV-002: Architecture Documentation

Maintain architecture documentation:

- System overview diagram
- Module dependency graph
- Data flow diagrams
- Decision log (ADRs)

### 8.4 Security Documentation

#### DOC-SEC-001: Security Guide

Document security practices:

- Credential handling
- Data encryption
- File permissions
- Audit logging

---

## 9. Automation Requirements

### 9.1 CI/CD Pipeline

#### AUTO-CI-001: Continuous Integration

**Status:** Implemented

The system SHALL:

- Run linting on all PRs (ruff)
- Run type checking (mypy)
- Run tests on Python 3.11 and 3.12
- Build package artifacts
- Upload coverage reports

#### AUTO-CI-002: Release Automation

**Status:** Not Implemented

The system SHALL:

- Auto-generate changelog
- Create GitHub releases
- Publish to PyPI
- Update documentation

### 9.2 Scripts

#### AUTO-SCRIPT-001: Quality Scripts

The system SHALL provide:

- `scripts/check.sh` - Quick quality check
- `scripts/lint.sh` - Run all linters
- `scripts/format.sh` - Format code
- `scripts/clean.sh` - Clean artifacts
- `scripts/doctor.sh` - Environment check

#### AUTO-SCRIPT-002: Maintenance Scripts

The system SHALL provide:

- `scripts/maintenance/archive_coordination.sh`
- Backup automation
- Database optimization (if applicable)
- Log rotation

### 9.3 Hooks

#### AUTO-HOOK-001: Pre-commit Hooks

**Status:** Implemented (.pre-commit-config.yaml)

The system SHALL:

- Run ruff check on commit
- Validate YAML files
- Check markdown formatting
- Verify shell scripts

---

## 10. UI/UX Requirements (NEW)

### 10.1 User Journey and Task Completion

#### FR-UX-001: Command Discoverability

**Priority:** P1 (High)
**Status:** Partial (--help exists, limited discovery)
**Dependencies:** None

The system SHALL:

- Provide interactive command discovery via `spreadsheet-dl` without args
- Show contextual help based on partial command input
- Suggest related commands after successful operations
- Display common workflows in help output
- Support fuzzy matching for command names

**Acceptance Criteria:**

- AC1: Running without args shows categorized command list
- AC2: Misspelled commands suggest corrections
- AC3: Each command shows 2-3 practical examples
- AC4: Help includes "See also" section for related commands
- AC5: New users complete first budget in < 5 minutes

**Example Implementation:**

```
$ spreadsheet-dl
SpreadsheetDL v0.4.0 - Family Budget Management

Getting Started:
  generate    Create a new budget spreadsheet
  templates   Browse available budget templates
  themes      Browse available visual themes

Daily Use:
  expense     Quick expense entry
  import      Import bank transactions
  analyze     View spending analysis

Reports:
  report      Generate detailed reports
  dashboard   View analytics dashboard
  alerts      Check budget alerts

Management:
  upload      Sync to Nextcloud
  config      Manage settings

Run 'spreadsheet-dl <command> --help' for command details.
Run 'spreadsheet-dl guide' for interactive tutorial.
```

#### FR-UX-002: Progress Indicators

**Priority:** P1 (High)
**Status:** Not Implemented
**Dependencies:** FR-UX-005 (Color Output)

The system SHALL:

- Display progress bars for operations > 1 second
- Show spinner for indeterminate operations
- Report estimated time remaining when calculable
- Allow progress suppression via `--quiet` flag
- Write progress to stderr, output to stdout

**Acceptance Criteria:**

- AC1: CSV import shows row count progress
- AC2: Upload shows transfer progress
- AC3: Generation shows phase completion
- AC4: `--quiet` suppresses all progress output
- AC5: Progress doesn't interfere with piped output

**Example Output:**

```
$ spreadsheet-dl import bank_export.csv
Detecting format... Chase Credit Card
Parsing transactions: [################----] 80% (800/1000)
Categorizing:        [####################] 100%
Created: imported_20251228.ods (1000 transactions, $12,345.67 total)
```

#### FR-UX-003: Error Message Quality

**Priority:** P0 (Critical)
**Status:** Partial (Basic exception messages)
**Dependencies:** None

The system SHALL:

- Provide structured error messages with:
  - Error code (machine-readable)
  - Summary (one-line description)
  - Details (full explanation)
  - Suggestion (how to fix)
  - Reference (documentation link)
- Color-code errors (red), warnings (yellow), info (blue)
- Include context (file, line, value) when applicable
- Never show raw stack traces to users (--debug for developers)

**Acceptance Criteria:**

- AC1: All errors have unique error codes (FT-xxx format)
- AC2: Suggestions are actionable and specific
- AC3: File errors include path and permission info
- AC4: Network errors include retry suggestions
- AC5: Validation errors show expected vs actual values

**Error Message Schema:**

```
Error [FT-CSV-001]: Cannot parse CSV file

  File:    /path/to/transactions.csv
  Line:    42
  Problem: Invalid date format "12/31/24"

  The date format doesn't match expected pattern.
  Expected: YYYY-MM-DD (e.g., 2024-12-31)
  Found:    MM/DD/YY (e.g., 12/31/24)

Suggestion: Specify the bank format explicitly:
  spreadsheet-dl import --bank=chase /path/to/transactions.csv

Documentation: https://docs.spreadsheet-dl.io/errors/FT-CSV-001
```

#### FR-UX-004: Confirmation Prompts

**Priority:** P1 (High)
**Status:** Not Implemented
**Dependencies:** None

The system SHALL:

- Prompt for confirmation on destructive operations
- Support `--yes` / `-y` flag to skip prompts (for scripts)
- Show preview of changes before confirmation
- Highlight irreversible actions in warnings
- Support `--dry-run` for all write operations

**Acceptance Criteria:**

- AC1: File overwrite prompts show diff preview
- AC2: Bulk operations show count before proceed
- AC3: Upload shows remote path before confirm
- AC4: `--yes` bypasses all prompts
- AC5: `--dry-run` shows changes without applying

**Operations Requiring Confirmation:**

- Overwriting existing files
- Bulk import (> 100 transactions)
- File deletion
- Configuration reset
- Cloud upload

#### FR-UX-005: Color Output System

**Priority:** P2 (Medium)
**Status:** Partial (NO_COLOR env var support)
**Dependencies:** None

The system SHALL:

- Use semantic colors consistently:
  - Success: Green
  - Warning: Yellow/Orange
  - Error: Red
  - Info: Blue
  - Muted: Gray
- Respect NO_COLOR environment variable
- Respect --no-color flag
- Auto-detect terminal capabilities
- Provide colorblind-safe mode

**Acceptance Criteria:**

- AC1: All commands use consistent color scheme
- AC2: Colors degrade gracefully to bold/underline
- AC3: NO_COLOR disables all color output
- AC4: Piped output auto-disables colors
- AC5: Colorblind mode uses patterns/symbols

**Color Semantic Table:**
| Context | Color | Alternative |
|---------|-------|-------------|
| Success | Green | [OK] prefix |
| Under budget | Green | + prefix |
| Warning | Yellow | [!] prefix |
| Near budget | Yellow | ~ prefix |
| Error | Red | [ERROR] prefix |
| Over budget | Red | - prefix |
| Info | Blue | [i] prefix |
| Muted | Gray | (parentheses) |

#### FR-UX-006: Interactive Mode

**Priority:** P3 (Low)
**Status:** Not Implemented
**Dependencies:** FR-UX-001

The system SHALL:

- Provide interactive guided workflows
- Support step-by-step budget creation wizard
- Allow incremental expense entry session
- Remember preferences within session
- Support undo within session

**Acceptance Criteria:**

- AC1: `spreadsheet-dl interactive` launches wizard
- AC2: Tab completion works in interactive mode
- AC3: History navigation with up/down arrows
- AC4: Ctrl+C exits cleanly with partial save option
- AC5: Session timeout with auto-save

### 10.2 Help System and Learning

#### FR-UX-007: Contextual Help

**Priority:** P2 (Medium)
**Status:** Partial (Static --help)
**Dependencies:** None

The system SHALL:

- Provide examples for every command
- Show command usage in context
- Include "common mistakes" section
- Link to full documentation
- Support `--help-full` for extended help

**Acceptance Criteria:**

- AC1: Every command has 2+ working examples
- AC2: Examples use realistic data
- AC3: Errors include relevant help excerpts
- AC4: Help mentions related commands
- AC5: Version shows what's new

#### FR-UX-008: Tutorial System

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** FR-UX-006

The system SHALL:

- Provide built-in interactive tutorial
- Guide first-time users through setup
- Teach core concepts progressively
- Track tutorial completion
- Allow skipping to specific sections

**Acceptance Criteria:**

- AC1: `spreadsheet-dl tutorial` starts guided tour
- AC2: Tutorial completes in < 10 minutes
- AC3: Each step validates before proceeding
- AC4: Progress persists across sessions
- AC5: Advanced tutorials available for power users

#### FR-UX-009: Shell Completions

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** None

The system SHALL:

- Provide tab completion for Bash
- Provide tab completion for Zsh
- Provide tab completion for Fish
- Complete commands, subcommands, options
- Complete file paths contextually

**Acceptance Criteria:**

- AC1: Completions install via `spreadsheet-dl completions install`
- AC2: Commands complete after typing 2+ chars
- AC3: File arguments complete with correct extensions
- AC4: Option values complete (e.g., --theme <TAB>)
- AC5: Completions update with new versions

### 10.3 Output Formatting and Readability

#### FR-UX-010: Table Formatting

**Priority:** P1 (High)
**Status:** Partial (Dashboard has tables)
**Dependencies:** None

The system SHALL:

- Format tabular output with aligned columns
- Support compact and expanded views
- Truncate long values with ellipsis
- Auto-detect terminal width
- Support --width override

**Acceptance Criteria:**

- AC1: Tables align in all terminal sizes
- AC2: Numbers right-align, text left-aligns
- AC3: Currency columns show consistent decimals
- AC4: Headers distinguish from data rows
- AC5: Empty cells show dash or placeholder

#### FR-UX-011: Output Modes

**Priority:** P1 (High)
**Status:** Partial (--json on some commands)
**Dependencies:** None

The system SHALL:

- Support human-readable output (default)
- Support JSON output (--json)
- Support CSV output (--csv) for tabular data
- Support quiet mode (--quiet) for scripts
- Support verbose mode (--verbose/-v)

**Acceptance Criteria:**

- AC1: All commands support --json
- AC2: JSON output is valid and complete
- AC3: CSV output importable to spreadsheets
- AC4: Quiet mode outputs only essential data
- AC5: Verbose mode shows timing and details

### 10.4 Accessibility

#### FR-UX-012: Screen Reader Support

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** FR-UX-010

The system SHALL:

- Provide text alternatives for visual elements
- Announce progress updates accessibly
- Support high-contrast output mode
- Avoid relying solely on color
- Structure output for screen reader navigation

**Acceptance Criteria:**

- AC1: Progress bars have text percentage
- AC2: Tables have row/column announcements
- AC3: Status uses text labels not just color
- AC4: Errors are clearly announced
- AC5: Output parses well with NVDA/VoiceOver

#### FR-UX-013: Keyboard Navigation

**Priority:** P3 (Low)
**Status:** Not Applicable (CLI, not TUI)
**Dependencies:** FR-UX-006

The system SHALL (for interactive mode):

- Support standard keyboard shortcuts
- Allow navigation without mouse
- Provide keyboard shortcut help
- Support Escape to cancel
- Support Enter to confirm

**Acceptance Criteria:**

- AC1: All actions accessible via keyboard
- AC2: Focus indicators visible
- AC3: Tab order is logical
- AC4: Shortcuts don't conflict with terminal
- AC5: Help shows keyboard shortcuts

---

## 11. Extensibility Requirements (NEW)

### 11.1 Plugin Architecture

#### FR-EXT-001: Plugin System Framework

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** NFR-MAINT-002

The system SHALL:

- Define plugin interface specification
- Support plugin discovery via entry points
- Manage plugin lifecycle (load, enable, disable)
- Isolate plugin failures from core system
- Version plugin API with semver

**Acceptance Criteria:**

- AC1: Plugins discoverable via `spreadsheet-dl plugins list`
- AC2: Plugins installable via `pip install spreadsheet-dl-plugin-*`
- AC3: Plugin errors don't crash main application
- AC4: API version checked at load time
- AC5: Plugin config merged with main config

**Plugin Interface:**

```python
from spreadsheet_dl.plugins import Plugin, hookimpl

class MyPlugin(Plugin):
    """Example plugin implementation."""

    name = "my-plugin"
    version = "1.0.0"
    api_version = "1.0"  # Required spreadsheet-dl plugin API

    @hookimpl
    def on_expense_added(self, expense: ExpenseEntry) -> None:
        """Called after expense is added."""
        pass

    @hookimpl
    def on_report_generated(self, report: Report) -> dict:
        """Modify report before output."""
        return {"custom_section": {...}}

    @hookimpl
    def register_commands(self) -> list[Command]:
        """Add CLI commands."""
        return [MyCustomCommand()]
```

#### FR-EXT-002: Plugin Discovery and Management

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** FR-EXT-001

The system SHALL:

- Discover plugins via Python entry points
- Support local plugin directories
- Provide plugin enable/disable commands
- Show plugin status and health
- Support plugin-specific configuration

**Acceptance Criteria:**

- AC1: `spreadsheet-dl plugins install <name>` works
- AC2: `spreadsheet-dl plugins enable/disable <name>` works
- AC3: Plugin config in ~/.config/spreadsheet-dl/plugins/
- AC4: Disabled plugins don't load
- AC5: Plugin health check on startup

#### FR-EXT-003: Plugin API Documentation

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** FR-EXT-001

The system SHALL:

- Document all plugin hooks
- Provide plugin development guide
- Include example plugin template
- Specify API stability guarantees
- Maintain API changelog

**Acceptance Criteria:**

- AC1: All hooks documented with signatures
- AC2: Example plugin in examples/plugins/
- AC3: Plugin API versioned separately
- AC4: Breaking changes in major versions only
- AC5: Deprecation warnings for removed hooks

### 11.2 Extension Points and Hooks

#### FR-EXT-004: Event Hook System

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** FR-EXT-001

The system SHALL provide hooks for:

- Pre/post expense entry
- Pre/post report generation
- Pre/post file save
- Pre/post import
- Pre/post analysis
- Configuration load
- Application startup/shutdown

**Acceptance Criteria:**

- AC1: All major operations have pre/post hooks
- AC2: Hooks can modify operation data
- AC3: Hooks can cancel operations (pre only)
- AC4: Hook execution order configurable
- AC5: Hook errors logged but don't fail operation

**Hook Specification:**

```python
# Available hooks
HOOKS = {
    "on_startup": [],           # App initialization
    "on_shutdown": [],          # App cleanup
    "on_config_loaded": [],     # After config merge

    "pre_expense_add": [],      # Before adding expense
    "post_expense_add": [],     # After expense added

    "pre_import": [],           # Before CSV import
    "post_import": [],          # After import complete

    "pre_generate": [],         # Before ODS generation
    "post_generate": [],        # After file created

    "pre_analyze": [],          # Before analysis
    "post_analyze": [],         # After analysis complete

    "pre_report": [],           # Before report generation
    "post_report": [],          # After report created

    "pre_upload": [],           # Before cloud sync
    "post_upload": [],          # After upload complete
}
```

#### FR-EXT-005: Custom Category Support

**Priority:** P1 (High)
**Status:** Not Implemented
**Dependencies:** None

The system SHALL:

- Allow user-defined expense categories
- Support category hierarchies (parent/child)
- Merge custom categories with built-in
- Persist custom categories in config
- Support category aliases

**Acceptance Criteria:**

- AC1: Custom categories via config file
- AC2: Category hierarchy (Utilities > Electric)
- AC3: Categories usable in CLI and templates
- AC4: Import maps to custom categories
- AC5: Reports include custom categories

**Category Configuration:**

```yaml
# ~/.config/spreadsheet-dl/categories.yaml
categories:
  # Add new top-level category
  - name: 'Pet Care'
    icon: 'pet'
    patterns:
      - 'petco'
      - 'veterinar'
      - 'pet food'

  # Add subcategory to existing
  - name: 'Electric'
    parent: 'Utilities'
    patterns:
      - 'electric'
      - 'power company'

  # Alias existing category
  - name: 'Food'
    alias_of: 'Groceries'
```

#### FR-EXT-006: Custom Formula Support

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** None

The system SHALL:

- Allow custom formula definitions
- Support formula templates with variables
- Validate formula syntax
- Include formula documentation
- Support formula libraries

**Acceptance Criteria:**

- AC1: Custom formulas in theme YAML
- AC2: Variables like {category}, {month}
- AC3: Syntax validation before generation
- AC4: Formula errors show clear messages
- AC5: Standard formula library included

**Formula Definition:**

```yaml
# In theme or config
formulas:
  monthly_average:
    description: 'Calculate monthly average for category'
    template: '=AVERAGE(SUMIF({expense_range};{category};{amount_range}))'
    variables:
      expense_range: "'Expense Log'.$B:$B"
      amount_range: "'Expense Log'.$D:$D"
      category: '[.A{row}]'

  year_to_date:
    description: 'Sum all expenses for category this year'
    template: '=SUMIFS({amount_range};{expense_range};{category};{date_range};">="&DATE({year};1;1))'
```

### 11.3 Third-Party Integration Framework

#### FR-EXT-007: Integration API

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** FR-EXT-001

The system SHALL:

- Define integration interface
- Support OAuth authentication
- Handle rate limiting gracefully
- Provide credential storage
- Support webhook callbacks

**Acceptance Criteria:**

- AC1: Integration interface documented
- AC2: OAuth flow helper methods
- AC3: Automatic retry with backoff
- AC4: Credentials in system keyring
- AC5: Webhook endpoint configurable

#### FR-EXT-008: Bank Format Extension

**Priority:** P1 (High)
**Status:** Partial (8 hardcoded formats)
**Dependencies:** None

The system SHALL:

- Support user-defined bank formats
- Provide format definition schema
- Include format validation
- Share formats via export/import
- Contribute formats to community

**Acceptance Criteria:**

- AC1: Bank format YAML schema defined
- AC2: `spreadsheet-dl bank-format create` wizard
- AC3: Format validation before save
- AC4: Export format as shareable YAML
- AC5: Community format repository linkable

**Bank Format Schema:**

```yaml
# ~/.config/spreadsheet-dl/banks/my_bank.yaml
bank_format:
  name: 'My Local Bank'
  version: '1.0.0'

  detection:
    # How to identify this bank's CSV
    headers:
      - 'Transaction Date'
      - 'Post Date'
      - 'Description'
      - 'Amount'
    filename_pattern: 'my_bank_*.csv'

  columns:
    date:
      name: 'Transaction Date'
      format: 'MM/DD/YYYY'
    description:
      name: 'Description'
    amount:
      name: 'Amount'
      # Negative = expense, positive = income
      negate: false

  preprocessing:
    # Skip header rows
    skip_rows: 1
    # Encoding
    encoding: 'utf-8'
    # Delimiter
    delimiter: ','
```

### 11.4 Backward Compatibility

#### FR-EXT-009: API Stability Guarantees

**Priority:** P1 (High)
**Status:** Partial (No formal policy)
**Dependencies:** None

The system SHALL:

- Follow semantic versioning strictly
- Maintain backward compatibility in minor versions
- Deprecate before removing
- Provide migration guides
- Support LTS versions

**Acceptance Criteria:**

- AC1: CHANGELOG follows Keep a Changelog
- AC2: Deprecation warnings for 2 minor versions
- AC3: Migration guide for each major version
- AC4: API stability documented per module
- AC5: LTS versions supported 12 months

**Stability Levels:**
| Module | Stability | Guarantee |
|--------|-----------|-----------|
| `spreadsheet_dl.ods_generator` | Stable | Minor version compatible |
| `spreadsheet_dl.budget_analyzer` | Stable | Minor version compatible |
| `spreadsheet_dl.cli` | Stable | Command names stable |
| `spreadsheet_dl.builder` | Beta | May change in minor versions |
| `spreadsheet_dl.plugins` | Experimental | May change anytime |

---

## 12. Template/Config System Requirements (NEW)

### 12.1 Configuration Management

#### FR-TMPL-001: Config Override Hierarchy

**Priority:** P1 (High)
**Status:** Partial (File, env, CLI - no full cascade)
**Dependencies:** None

The system SHALL implement configuration cascade:

1. Built-in defaults (lowest priority)
2. System-wide config (`/etc/spreadsheet-dl/config.yaml`)
3. User config (`~/.config/spreadsheet-dl/config.yaml`)
4. Project config (`./.spreadsheet-dl.yaml`)
5. Environment variables (`SPREADSHEET_DL_*`)
6. Command-line arguments (highest priority)

**Acceptance Criteria:**

- AC1: All 6 levels respected in order
- AC2: `config --show --resolved` shows final values
- AC3: `config --show --sources` shows value origins
- AC4: Partial configs merge correctly
- AC5: Invalid configs fail with clear errors

**Example Resolution:**

```
$ spreadsheet-dl config --show --sources

Configuration (resolved):
  defaults.template: "50_30_20"
    - Default: ""
    - User config (~/.config/spreadsheet-dl/config.yaml): "50_30_20"  <-- ACTIVE

  defaults.currency_symbol: "EUR"
    - Default: "$"
    - User config: "$"
    - Environment (SPREADSHEET_DL_CURRENCY): "EUR"  <-- ACTIVE

  nextcloud.url: "https://cloud.example.com"
    - Environment (NEXTCLOUD_URL): "https://cloud.example.com"  <-- ACTIVE
```

#### FR-TMPL-002: Config Schema Validation

**Priority:** P1 (High)
**Status:** Not Implemented
**Dependencies:** None

The system SHALL:

- Define JSON Schema for config files
- Validate config on load
- Report all validation errors (not just first)
- Suggest corrections for common mistakes
- Support schema versioning

**Acceptance Criteria:**

- AC1: JSON Schema in repository
- AC2: `config --validate` command
- AC3: All errors reported at once
- AC4: Unknown keys warn (not error)
- AC5: Type mismatches show expected type

**Config Schema (excerpt):**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "defaults": {
      "type": "object",
      "properties": {
        "template": {
          "type": "string",
          "enum": [
            "50_30_20",
            "family",
            "minimalist",
            "zero_based",
            "fire",
            "high_income",
            ""
          ]
        },
        "currency_symbol": {
          "type": "string",
          "maxLength": 3
        },
        "date_format": {
          "type": "string",
          "pattern": "^%[YymdHMSjUW%].*$"
        }
      }
    }
  }
}
```

#### FR-TMPL-003: Config Migration

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** FR-TMPL-002

The system SHALL:

- Detect config schema version
- Migrate configs automatically
- Backup before migration
- Support manual migration
- Log migration changes

**Acceptance Criteria:**

- AC1: Config version in file metadata
- AC2: Auto-migrate on startup with prompt
- AC3: Backup created as config.yaml.bak
- AC4: `config --migrate` for manual trigger
- AC5: Migration log shows changes

#### FR-TMPL-004: Environment Variable Mapping

**Priority:** P1 (High)
**Status:** Partial (Limited env vars)
**Dependencies:** FR-TMPL-001

The system SHALL:

- Map all config keys to env vars
- Use consistent naming convention
- Support nested key mapping
- Document all env vars
- Support .env files

**Acceptance Criteria:**

- AC1: Pattern: `SPREADSHEET_DL_<SECTION>_<KEY>`
- AC2: Nested: `SPREADSHEET_DL_ALERTS_WARNING_THRESHOLD`
- AC3: Boolean: `true/false/1/0/yes/no`
- AC4: `.env` file auto-loaded
- AC5: `config --env-template` generates template

**Environment Variable Mapping:**

```bash
# ~/.config/spreadsheet-dl/.env

# Nextcloud settings
NEXTCLOUD_URL=https://cloud.example.com
NEXTCLOUD_USER=myuser
NEXTCLOUD_PASSWORD=secret

# Defaults
SPREADSHEET_DL_DEFAULTS_TEMPLATE=family
SPREADSHEET_DL_DEFAULTS_CURRENCY_SYMBOL=$
SPREADSHEET_DL_DEFAULTS_DATE_FORMAT=%Y-%m-%d

# Alerts
SPREADSHEET_DL_ALERTS_WARNING_THRESHOLD=80
SPREADSHEET_DL_ALERTS_CRITICAL_THRESHOLD=95

# Display
SPREADSHEET_DL_DISPLAY_USE_COLOR=true
SPREADSHEET_DL_DISPLAY_SHOW_PROGRESS=true
```

### 12.2 Template Management

#### FR-TMPL-005: Budget Template Creation

**Priority:** P1 (High)
**Status:** Partial (6 built-in, no custom)
**Dependencies:** None

The system SHALL:

- Allow custom budget template creation
- Support template wizard via CLI
- Calculate allocations from income
- Validate allocation totals
- Save templates for reuse

**Acceptance Criteria:**

- AC1: `template create` wizard walks through categories
- AC2: Percentages auto-calculate from income
- AC3: Warning if allocations exceed 100%
- AC4: Templates saved to user config dir
- AC5: Custom templates appear in `templates` command

**Template Creation Flow:**

```
$ spreadsheet-dl template create

Budget Template Wizard
======================

Template name: My Custom Budget
Description: Budget for our family situation

Monthly income (optional, for percentage calculation): $8000

Category Allocations:
  Housing:       $2000 (25%)
  Utilities:     $300 (3.75%)
  Groceries:     $800 (10%)
  ...

Total allocated: $7200 (90%)
Remaining: $800 (10%)

Assign remaining to:
  [1] Savings
  [2] Miscellaneous
  [3] Leave unallocated
> 1

Template saved to: ~/.config/spreadsheet-dl/templates/my_custom_budget.yaml
Use with: spreadsheet-dl generate --template=my_custom_budget
```

#### FR-TMPL-006: Template Versioning

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** FR-TMPL-005

The system SHALL:

- Version templates with semver
- Track template changes
- Support template updates
- Migrate budgets to new template versions
- Show template changelog

**Acceptance Criteria:**

- AC1: Templates have version in metadata
- AC2: `template history <name>` shows versions
- AC3: `template upgrade` migrates to latest
- AC4: Breaking changes require confirmation
- AC5: Old versions remain accessible

#### FR-TMPL-007: Template Sharing

**Priority:** P3 (Low)
**Status:** Not Implemented
**Dependencies:** FR-TMPL-005

The system SHALL:

- Export templates as shareable files
- Import templates from files/URLs
- Support template marketplace (future)
- Validate imported templates
- Credit template authors

**Acceptance Criteria:**

- AC1: `template export <name>` creates YAML file
- AC2: `template import <file/url>` adds template
- AC3: Imported templates marked as external
- AC4: Author attribution preserved
- AC5: Security scan on import

### 12.3 Theme Management

#### FR-TMPL-008: Theme Creation Guide

**Priority:** P2 (Medium)
**Status:** Partial (Schema exists, no guide)
**Dependencies:** None

The system SHALL:

- Document theme YAML schema completely
- Provide theme creation wizard
- Support live preview (where possible)
- Validate themes before use
- Include theme examples

**Acceptance Criteria:**

- AC1: Theme schema documented in detail
- AC2: `theme create` wizard available
- AC3: Theme validation on load
- AC4: Error messages show line numbers
- AC5: Example themes in examples/themes/

**Theme Schema Documentation:**

```yaml
# Theme file structure
meta:
  name: string # Required: Display name
  version: string # Required: Semver version
  description: string # Optional: Theme description
  author: string # Optional: Author name/email
  extends: string # Optional: Parent theme name

colors:
  # Semantic colors (all optional, inherit from parent or default)
  primary: '#RRGGBB'
  primary_light: '#RRGGBB'
  primary_dark: '#RRGGBB'
  secondary: '#RRGGBB'
  success: '#RRGGBB'
  success_bg: '#RRGGBB'
  warning: '#RRGGBB'
  warning_bg: '#RRGGBB'
  danger: '#RRGGBB'
  danger_bg: '#RRGGBB'
  neutral_100: '#RRGGBB' # White/lightest
  neutral_200: '#RRGGBB'
  neutral_300: '#RRGGBB'
  neutral_800: '#RRGGBB'
  neutral_900: '#RRGGBB' # Black/darkest

fonts:
  primary:
    family: string # Font family name
    fallback: string # Fallback fonts
  monospace:
    family: string
    fallback: string

base_styles:
  # Building block styles
  <style_name>:
    extends: string # Optional: Parent style
    font_family: string|ref # Font or "{fonts.primary.family}"
    font_size: string # e.g., "10pt", "12px"
    font_weight: string # "normal", "bold", "light"
    color: string|ref # Color or "{colors.primary}"
    background_color: string|ref
    text_align: string # "left", "center", "right"
    vertical_align: string # "top", "middle", "bottom"
    border_top: string # "1px solid #000000"
    border_bottom: string
    border_left: string
    border_right: string
    padding: string # e.g., "2pt"
    number_format: string # e.g., "$#,##0.00"
    date_format: string # e.g., "YYYY-MM-DD"

styles:
  # Semantic styles used in sheets
  <style_name>:
    extends: string # Usually extends base_style
    # ... same properties as base_styles

conditional_formats:
  <format_name>:
    description: string
    rules:
      - condition: string # Expression like "value < 0"
        style: string # Style name to apply
      - default: string # Default style if no match
```

#### FR-TMPL-009: Theme Inheritance

**Priority:** P2 (Medium)
**Status:** Implemented
**Dependencies:** None

The system SHALL:

- Support theme inheritance via `extends`
- Merge child values over parent
- Support multiple inheritance levels
- Detect circular inheritance
- Document inheritance behavior

**Acceptance Criteria:**

- AC1: `extends: parent_theme` works
- AC2: Child values override parent
- AC3: Unspecified values inherit
- AC4: Circular reference errors clearly
- AC5: `theme show --resolved` shows merged

#### FR-TMPL-010: Theme Validation

**Priority:** P1 (High)
**Status:** Partial (Basic validation)
**Dependencies:** None

The system SHALL:

- Validate theme YAML syntax
- Validate color hex codes
- Validate style references
- Check for missing required fields
- Verify inheritance chain

**Acceptance Criteria:**

- AC1: Invalid YAML shows parse error
- AC2: Invalid colors show correction
- AC3: Missing styles show available options
- AC4: `theme validate <file>` command
- AC5: Validation runs before generation

### 12.4 Default Value Handling

#### FR-TMPL-011: Default Value Documentation

**Priority:** P1 (High)
**Status:** Partial (Defaults in code, not documented)
**Dependencies:** None

The system SHALL:

- Document all default values
- Show defaults in --help output
- Support "use default" placeholder
- Allow resetting to defaults
- Track when defaults change

**Acceptance Criteria:**

- AC1: All defaults listed in documentation
- AC2: --help shows "(default: X)" for all options
- AC3: `~` or `null` in config means "use default"
- AC4: `config --reset <key>` restores default
- AC5: CHANGELOG notes default changes

**Default Values Table:**
| Setting | Default | Notes |
|---------|---------|-------|
| `defaults.output_directory` | Current directory | `.` or `$PWD` |
| `defaults.template` | (none) | Empty, no template |
| `defaults.empty_rows` | 50 | Rows for data entry |
| `defaults.date_format` | `%Y-%m-%d` | ISO format |
| `defaults.currency_symbol` | `$` | USD |
| `defaults.currency_decimal_places` | 2 | Standard |
| `alerts.warning_threshold` | 80.0 | 80% of budget |
| `alerts.critical_threshold` | 95.0 | 95% of budget |
| `display.use_color` | true | Unless NO_COLOR |
| `display.show_progress` | true | Show progress bars |
| `display.json_pretty_print` | true | Indent JSON |

---

## 13. Formatting Requirements (NEW)

### 13.1 Number Formatting

#### FR-FMT-001: Currency Formatting

**Priority:** P1 (High)
**Status:** Partial (USD hardcoded)
**Dependencies:** FR-CURR-001

The system SHALL:

- Support configurable currency symbol
- Support symbol position (prefix/suffix)
- Support thousands separator
- Support decimal places configuration
- Support locale-based formatting

**Acceptance Criteria:**

- AC1: Currency symbol configurable in config
- AC2: Position: `$1,234.56` or `1.234,56 EUR`
- AC3: Separator: `,` or `.` or ` `
- AC4: Decimals: 0, 2, or custom
- AC5: Locale auto-detection option

**Currency Format Configuration:**

```yaml
formatting:
  currency:
    symbol: '$' # Currency symbol
    symbol_position: 'prefix' # "prefix" or "suffix"
    decimal_separator: '.' # Decimal point
    thousands_separator: ',' # Thousands grouping
    decimal_places: 2 # Digits after decimal
    negative_format: '-$X' # How to show negatives
    # Alternatives: "($X)", "$-X", "$X-", "- $X"
```

#### FR-FMT-002: Negative Number Formatting

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** FR-FMT-001

The system SHALL:

- Support multiple negative formats
- Support red color for negatives
- Support parentheses notation
- Support conditional formatting
- Maintain format in exports

**Acceptance Criteria:**

- AC1: Format options: `-$X`, `($X)`, `$-X`
- AC2: Red text option for negatives
- AC3: Works in ODS and exports
- AC4: Configurable per column type
- AC5: Preview in CLI output

**Negative Format Options:**
| Style | Example | Use Case |
|-------|---------|----------|
| Minus prefix | -$1,234.56 | Default, clear |
| Parentheses | ($1,234.56) | Accounting standard |
| Minus suffix | $1,234.56- | Rarely used |
| Red color | $1,234.56 (red) | Visual emphasis |
| Red + parens | ($1,234.56) (red) | Maximum clarity |

#### FR-FMT-003: Percentage Formatting

**Priority:** P2 (Medium)
**Status:** Partial (Basic 0.0%)
**Dependencies:** None

The system SHALL:

- Support decimal places in percentages
- Support symbol position
- Support conditional coloring
- Handle > 100% values
- Format in reports and exports

**Acceptance Criteria:**

- AC1: Decimal places: 0, 1, 2 configurable
- AC2: Format: `85%` or `85.5%` or `0.855`
- AC3: > 100% shows correctly
- AC4: Color coding for thresholds
- AC5: Consistent across output formats

### 13.2 Date and Time Formatting

#### FR-FMT-004: Date Format Configuration

**Priority:** P1 (High)
**Status:** Partial (Single format)
**Dependencies:** None

The system SHALL:

- Support multiple date format patterns
- Support locale-based formatting
- Support relative dates ("today", "yesterday")
- Parse multiple input formats
- Display in configured format

**Acceptance Criteria:**

- AC1: Format patterns: ISO, US, EU, custom
- AC2: Input parsing flexible
- AC3: Output in configured format
- AC4: Relative dates in CLI output
- AC5: Full date in exports

**Date Format Patterns:**

```yaml
formatting:
  date:
    # Display format
    format: '%Y-%m-%d' # ISO: 2024-12-28
    # Alternatives:
    # "%m/%d/%Y"                 # US: 12/28/2024
    # "%d/%m/%Y"                 # EU: 28/12/2024
    # "%d %b %Y"                 # Long: 28 Dec 2024

    # Input parsing (auto-detect from these)
    input_formats:
      - '%Y-%m-%d'
      - '%m/%d/%Y'
      - '%d/%m/%Y'
      - '%m/%d/%y'

    # Relative dates in output
    use_relative: true # "today", "yesterday", "3 days ago"
    relative_threshold_days: 7 # Use relative for dates within 7 days
```

#### FR-FMT-005: Time Zone Handling

**Priority:** P3 (Low)
**Status:** Not Implemented
**Dependencies:** FR-FMT-004

The system SHALL:

- Store dates in UTC internally
- Convert to local timezone for display
- Support explicit timezone config
- Handle DST transitions
- Include timezone in exports

**Acceptance Criteria:**

- AC1: Internal storage UTC
- AC2: Display in local or configured TZ
- AC3: DST transitions handled
- AC4: TZ info in JSON exports
- AC5: Import respects source TZ

### 13.3 Conditional Formatting

#### FR-FMT-006: Conditional Format Rules

**Priority:** P2 (Medium)
**Status:** Partial (Basic in themes)
**Dependencies:** None

The system SHALL:

- Support condition-based styling
- Support multiple conditions per cell
- Support condition priorities
- Include standard finance conditions
- Allow custom conditions

**Acceptance Criteria:**

- AC1: Conditions evaluated in order
- AC2: First match wins
- AC3: Default style if no match
- AC4: Conditions: <, >, =, between
- AC5: Reference other cells

**Conditional Format Schema:**

```yaml
conditional_formats:
  budget_remaining:
    description: 'Color code remaining budget'
    column_pattern: 'Remaining' # Apply to columns matching pattern
    rules:
      - condition: '< 0'
        style: cell_danger
        description: 'Over budget - red background'

      - condition: '< $budget * 0.1'
        style: cell_warning
        description: 'Less than 10% remaining - yellow'

      - condition: '>= 0'
        style: cell_success
        description: 'On track - green background'

  percentage_status:
    column_pattern: '%'
    rules:
      - condition: '>= 1.0' # 100% or more
        style: cell_danger

      - condition: '>= 0.85' # 85-99%
        style: cell_warning

      - default: cell_normal
```

#### FR-FMT-007: Data Bars and Icons

**Priority:** P3 (Low)
**Status:** Not Implemented
**Dependencies:** FR-FMT-006

The system SHALL:

- Support data bars in cells
- Support icon sets (arrows, flags)
- Support color scales
- Work in ODS format
- Degrade gracefully in unsupported apps

**Acceptance Criteria:**

- AC1: Data bars show value visually
- AC2: Icons: up/down arrows, check/x
- AC3: Color scales: red-yellow-green
- AC4: ODF data bar syntax correct
- AC5: Fallback to text if unsupported

### 13.4 Print and Export Layout

#### FR-FMT-008: Print Layout Configuration

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** None

The system SHALL:

- Configure page size (Letter, A4, etc.)
- Configure margins
- Configure orientation
- Support header/footer
- Support page breaks

**Acceptance Criteria:**

- AC1: Page size in config
- AC2: Margins: top, bottom, left, right
- AC3: Orientation: portrait/landscape
- AC4: Headers: date, page number, title
- AC5: Auto page breaks at categories

**Print Configuration:**

```yaml
formatting:
  print:
    page_size: 'letter' # "letter", "a4", "legal"
    orientation: 'portrait' # "portrait", "landscape"
    margins:
      top: '1in'
      bottom: '1in'
      left: '0.75in'
      right: '0.75in'
    header:
      left: '{title}'
      center: ''
      right: '{date}'
    footer:
      left: ''
      center: 'Page {page} of {pages}'
      right: ''
    fit_to_page: false # Scale to fit
    print_gridlines: false
    repeat_header_rows: 1 # Repeat top N rows on each page
```

#### FR-FMT-009: Export Format Preservation

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** FR-EXPORT-001

The system SHALL:

- Preserve formatting in Excel export
- Convert ODS styles to Excel equivalents
- Maintain formula compatibility
- Preserve conditional formatting
- Document format limitations

**Acceptance Criteria:**

- AC1: Colors match in Excel
- AC2: Fonts substitute correctly
- AC3: Formulas work in Excel
- AC4: Conditional formats convert
- AC5: Limitations documented

**Format Compatibility Matrix:**
| Feature | ODS | XLSX | CSV | PDF |
|---------|-----|------|-----|-----|
| Colors | Full | Full | N/A | Full |
| Fonts | Full | Full | N/A | Full |
| Formulas | Full | Convert | N/A | Static |
| Conditional | Full | Convert | N/A | Applied |
| Data bars | Full | Partial | N/A | Applied |
| Comments | Full | Full | N/A | Visible |

### 13.5 Locale and Internationalization

#### FR-FMT-010: Locale Support

**Priority:** P2 (Medium)
**Status:** Not Implemented
**Dependencies:** FR-FMT-001, FR-FMT-004

The system SHALL:

- Detect system locale
- Support explicit locale config
- Format numbers per locale
- Format dates per locale
- Support locale in exports

**Acceptance Criteria:**

- AC1: Auto-detect from LANG/LC\_\*
- AC2: Override via config
- AC3: Number format follows locale
- AC4: Date format follows locale
- AC5: Locale preserved in files

**Locale Configuration:**

```yaml
formatting:
  locale: 'auto' # Or explicit: "en_US", "de_DE", "ja_JP"

  # Locale-specific overrides
  locales:
    en_US:
      currency_symbol: '$'
      date_format: '%m/%d/%Y'
      number:
        decimal: '.'
        thousands: ','

    de_DE:
      currency_symbol: 'EUR'
      date_format: '%d.%m.%Y'
      number:
        decimal: ','
        thousands: '.'

    ja_JP:
      currency_symbol: 'JPY'
      date_format: '%Y/%m/%d'
      number:
        decimal: '.'
        thousands: ','
```

#### FR-FMT-011: Multi-Language Support

**Priority:** P3 (Low)
**Status:** Not Implemented
**Dependencies:** FR-FMT-010

The system SHALL:

- Support UI text translation
- Support template name translation
- Support category name translation
- Support error message translation
- Use gettext for i18n

**Acceptance Criteria:**

- AC1: Core UI in en, de, es, fr, ja
- AC2: Category names translatable
- AC3: Error messages translatable
- AC4: Translation files in repo
- AC5: Community contributions welcome

---

## 14. Prioritization Framework

### 14.1 Priority Levels

| Priority | Label    | Description                  | Timeline   |
| -------- | -------- | ---------------------------- | ---------- |
| P0       | Critical | Core functionality, blockers | Sprint 1   |
| P1       | High     | Important features, security | Sprint 2-3 |
| P2       | Medium   | Nice-to-have features        | Sprint 4-6 |
| P3       | Low      | Future enhancements          | Backlog    |

### 14.2 Implementation Phases

#### Phase 1: Foundation (Sprint 1-2)

- Fix quick expense append (G-02)
- Complete API documentation (D-01)
- Create user guide (DOC-USER-001)
- Improve error messages (TD-04)
- **NEW:** Error message quality (FR-UX-003)
- **NEW:** Config validation (FR-TMPL-002)

#### Phase 2: Security & Reliability (Sprint 3-4)

- Implement data encryption (G-01)
- Add backup/restore (G-04)
- Security documentation (D-04)
- Multi-format export (FR-EXPORT-001)
- **NEW:** Confirmation prompts (FR-UX-004)
- **NEW:** Config migration (FR-TMPL-003)

#### Phase 3: Enhanced Features (Sprint 5-8)

- Account management (FR-CORE-004)
- Multi-currency support (FR-CURR-001)
- Extended bank formats (FR-IMPORT-002)
- Interactive visualization (FR-REPORT-003)
- **NEW:** Progress indicators (FR-UX-002)
- **NEW:** Custom categories (FR-EXT-005)
- **NEW:** Currency formatting (FR-FMT-001)
- **NEW:** Custom templates (FR-TMPL-005)

#### Phase 4: Advanced Features (Sprint 9-12)

- Goal tracking (FR-GOAL-001, FR-GOAL-002)
- Bill reminders (FR-RECUR-002)
- Calendar integration (IR-CAL-001)
- Notification system (IR-NOTIF-001)
- **NEW:** Plugin system (FR-EXT-001)
- **NEW:** Conditional formatting (FR-FMT-006)
- **NEW:** Shell completions (FR-UX-009)

#### Phase 5: Future Enhancements (Backlog)

- Bank API integration (FR-IMPORT-003)
- Native MCP server (IR-MCP-002)
- Investment tracking (G-07)
- Mobile app (G-10)
- **NEW:** Interactive mode (FR-UX-006)
- **NEW:** Multi-language (FR-FMT-011)
- **NEW:** Template marketplace (FR-TMPL-007)

### 14.3 Effort Estimates

| Requirement                         | Effort | Dependencies   |
| ----------------------------------- | ------ | -------------- |
| FR-CORE-003 (fix append)            | S      | None           |
| FR-SEC-001 (encryption)             | L      | None           |
| FR-CORE-004 (accounts)              | XL     | Schema changes |
| FR-CURR-001 (currencies)            | M      | FR-CORE-004    |
| FR-EXPORT-001 (multi-format)        | M      | None           |
| FR-REPORT-003 (charts)              | L      | Chart library  |
| FR-GOAL-001 (goals)                 | M      | FR-CORE-004    |
| IR-NOTIF-001 (notifications)        | M      | None           |
| **FR-UX-003 (error messages)**      | S      | None           |
| **FR-UX-002 (progress)**            | S      | None           |
| **FR-EXT-001 (plugins)**            | XL     | Architecture   |
| **FR-EXT-005 (custom categories)**  | M      | Schema         |
| **FR-TMPL-002 (config validation)** | S      | None           |
| **FR-TMPL-005 (custom templates)**  | M      | None           |
| **FR-FMT-001 (currency format)**    | M      | None           |
| **FR-FMT-006 (conditional)**        | L      | Theme system   |

Effort Scale: S (1-2 days), M (3-5 days), L (1-2 weeks), XL (2-4 weeks)

---

## 15. Traceability Matrix

### 15.1 Requirements to Features

| Requirement ID  | Current Feature                 | Status      | Version |
| --------------- | ------------------------------- | ----------- | ------- |
| FR-CORE-001     | OdsGenerator                    | Complete    | 0.1.0   |
| FR-CORE-002     | BudgetAnalyzer                  | Complete    | 0.1.0   |
| FR-CORE-003     | CLI expense command             | Partial     | 0.2.0   |
| FR-CORE-004     | -                               | Not Started | -       |
| FR-IMPORT-001   | CSVImporter                     | Complete    | 0.2.0   |
| FR-IMPORT-002   | -                               | Not Started | -       |
| FR-IMPORT-003   | -                               | Not Started | -       |
| FR-EXPORT-001   | ODS only                        | Partial     | 0.1.0   |
| FR-REPORT-001   | ReportGenerator                 | Complete    | 0.1.0   |
| FR-REPORT-002   | AnalyticsDashboard              | Partial     | 0.2.0   |
| FR-REPORT-003   | -                               | Not Started | -       |
| FR-RECUR-001    | RecurringExpenseManager         | Complete    | 0.2.0   |
| FR-RECUR-002    | -                               | Not Started | -       |
| FR-GOAL-001     | -                               | Not Started | -       |
| FR-GOAL-002     | -                               | Not Started | -       |
| FR-CURR-001     | -                               | Not Started | -       |
| FR-SEC-001      | -                               | Not Started | -       |
| **FR-UX-001**   | CLI --help                      | Partial     | 0.1.0   |
| **FR-UX-002**   | -                               | Not Started | -       |
| **FR-UX-003**   | exceptions.py                   | Partial     | 0.2.0   |
| **FR-UX-004**   | -                               | Not Started | -       |
| **FR-UX-005**   | NO_COLOR support                | Partial     | 0.2.0   |
| **FR-EXT-001**  | -                               | Not Started | -       |
| **FR-EXT-005**  | ExpenseCategory enum            | Partial     | 0.1.0   |
| **FR-TMPL-001** | config.py                       | Partial     | 0.3.0   |
| **FR-TMPL-002** | -                               | Not Started | -       |
| **FR-TMPL-005** | templates.py                    | Partial     | 0.2.0   |
| **FR-TMPL-008** | schema/loader.py                | Partial     | 0.4.0   |
| **FR-FMT-001**  | DefaultSettings.currency_symbol | Partial     | 0.3.0   |
| **FR-FMT-004**  | DefaultSettings.date_format     | Partial     | 0.3.0   |
| **FR-FMT-006**  | conditional_formats in themes   | Partial     | 0.4.0   |

### 15.2 Gaps to Requirements

| Gap ID       | Related Requirements    | Priority |
| ------------ | ----------------------- | -------- |
| G-01         | FR-SEC-001, NFR-SEC-001 | P1       |
| G-02         | FR-CORE-003             | P0       |
| G-03         | FR-CURR-001             | P2       |
| G-04         | DR-STORE-002            | P1       |
| G-05         | FR-CORE-004             | P1       |
| G-06         | FR-GOAL-001             | P2       |
| G-07         | Future enhancement      | P3       |
| G-08         | FR-REPORT-002           | P2       |
| G-09         | FR-REPORT-003           | P2       |
| G-10         | Future enhancement      | P3       |
| **G-UX-01**  | FR-UX-002               | P1       |
| **G-UX-02**  | FR-UX-003               | P0       |
| **G-UX-03**  | FR-UX-001               | P1       |
| **G-EXT-01** | FR-EXT-001              | P2       |
| **G-EXT-02** | FR-EXT-005              | P1       |
| **G-CFG-01** | FR-TMPL-003             | P2       |
| **G-CFG-02** | FR-TMPL-002             | P1       |
| **G-FMT-01** | FR-FMT-001              | P1       |
| **G-FMT-02** | FR-FMT-004              | P1       |

### 15.3 Requirements to Tests

| Requirement     | Test File(s)                   | Coverage |
| --------------- | ------------------------------ | -------- |
| FR-CORE-001     | test_ods_generator.py          | High     |
| FR-CORE-002     | test_budget_analyzer.py        | High     |
| FR-CORE-003     | test_cli.py                    | Medium   |
| FR-IMPORT-001   | test_csv_import.py             | High     |
| FR-REPORT-001   | test_report_generator.py       | High     |
| FR-RECUR-001    | test_recurring.py              | High     |
| NFR-COMP-001    | test_backward_compatibility.py | Medium   |
| **FR-UX-001**   | test_cli.py                    | Low      |
| **FR-UX-003**   | test_exceptions.py             | Medium   |
| **FR-TMPL-001** | test_config.py                 | High     |
| **FR-TMPL-008** | test_schema.py, test_themes.py | High     |
| **FR-FMT-006**  | test_themes.py                 | Low      |

### 15.4 New Requirements Summary (v2.0.0)

| Section         | New Requirements    | Priority Distribution  |
| --------------- | ------------------- | ---------------------- |
| UI/UX           | 13 requirements     | 3 P1, 6 P2, 4 P3       |
| Extensibility   | 9 requirements      | 2 P1, 6 P2, 1 P3       |
| Template/Config | 11 requirements     | 5 P1, 4 P2, 2 P3       |
| Formatting      | 11 requirements     | 3 P1, 6 P2, 2 P3       |
| **Total New**   | **44 requirements** | **13 P1, 22 P2, 9 P3** |

---

## Appendix A: File Inventory

### Source Files (20 files)

- `src/spreadsheet_dl/__init__.py` - Package exports
- `src/spreadsheet_dl/ods_generator.py` - ODS generation
- `src/spreadsheet_dl/budget_analyzer.py` - Analysis
- `src/spreadsheet_dl/report_generator.py` - Reports
- `src/spreadsheet_dl/cli.py` - CLI interface
- `src/spreadsheet_dl/csv_import.py` - Bank imports
- `src/spreadsheet_dl/webdav_upload.py` - Nextcloud sync
- `src/spreadsheet_dl/analytics.py` - Dashboard
- `src/spreadsheet_dl/alerts.py` - Alert system
- `src/spreadsheet_dl/recurring.py` - Recurring expenses
- `src/spreadsheet_dl/templates.py` - Budget templates
- `src/spreadsheet_dl/builder.py` - Fluent API
- `src/spreadsheet_dl/renderer.py` - ODS renderer
- `src/spreadsheet_dl/config.py` - Configuration
- `src/spreadsheet_dl/exceptions.py` - Exceptions
- `src/spreadsheet_dl/schema/__init__.py`
- `src/spreadsheet_dl/schema/styles.py`
- `src/spreadsheet_dl/schema/loader.py`
- `src/spreadsheet_dl/schema/validation.py`
- `src/spreadsheet_dl/themes/__init__.py`

### Test Files (19 files)

- `tests/conftest.py`
- `tests/test_alerts.py`
- `tests/test_analytics.py`
- `tests/test_backward_compatibility.py`
- `tests/test_builder.py`
- `tests/test_budget_analyzer.py`
- `tests/test_cli.py`
- `tests/test_cli_themes.py`
- `tests/test_config.py`
- `tests/test_csv_import.py`
- `tests/test_exceptions.py`
- `tests/test_integration.py`
- `tests/test_ods_generator.py`
- `tests/test_recurring.py`
- `tests/test_renderer.py`
- `tests/test_report_generator.py`
- `tests/test_schema.py`
- `tests/test_templates.py`
- `tests/test_themes.py`
- `tests/test_webdav.py`

### Theme Files (5 files)

- `src/spreadsheet_dl/themes/default.yaml`
- `src/spreadsheet_dl/themes/corporate.yaml`
- `src/spreadsheet_dl/themes/minimal.yaml`
- `src/spreadsheet_dl/themes/dark.yaml`
- `src/spreadsheet_dl/themes/high_contrast.yaml`

---

## Appendix B: Expense Categories

Current categories (16):

1. Housing
2. Utilities
3. Groceries
4. Transportation
5. Healthcare
6. Insurance
7. Entertainment
8. Dining Out
9. Clothing
10. Personal Care
11. Education
12. Savings
13. Debt Payment
14. Gifts
15. Subscriptions
16. Miscellaneous

Proposed additions:

- Childcare
- Pet Care
- Home Improvement
- Business Expenses
- Charity/Donations
- Travel
- Investments (for tracking, not true expense)

---

## Appendix C: Bank Formats Supported

| Bank             | Format Key      | Date Format | Status  |
| ---------------- | --------------- | ----------- | ------- |
| Chase            | chase           | MM/DD/YYYY  | Tested  |
| Chase Credit     | chase_credit    | MM/DD/YYYY  | Tested  |
| Bank of America  | bank_of_america | MM/DD/YYYY  | Tested  |
| Wells Fargo      | wells_fargo     | MM/DD/YYYY  | Tested  |
| Capital One      | capital_one     | YYYY-MM-DD  | Tested  |
| Discover         | discover        | MM/DD/YYYY  | Tested  |
| American Express | amex            | MM/DD/YYYY  | Tested  |
| USAA             | usaa            | YYYY-MM-DD  | Tested  |
| Generic          | generic         | YYYY-MM-DD  | Default |

---

## Appendix D: Error Code Reference (NEW)

### Error Code Format

`FT-<CATEGORY>-<NUMBER>`

### Error Categories

| Category | Code Range | Description                  |
| -------- | ---------- | ---------------------------- |
| GEN      | 001-099    | General/uncategorized errors |
| FILE     | 100-199    | File system errors           |
| ODS      | 200-299    | ODS file errors              |
| CSV      | 300-399    | CSV import errors            |
| VAL      | 400-499    | Validation errors            |
| CFG      | 500-599    | Configuration errors         |
| NET      | 600-699    | Network/WebDAV errors        |
| TMPL     | 700-799    | Template errors              |
| FMT      | 800-899    | Formatting errors            |
| EXT      | 900-999    | Extension/plugin errors      |

### Example Error Codes

| Code        | Description           | Severity |
| ----------- | --------------------- | -------- |
| FT-GEN-001  | Unknown error         | Error    |
| FT-FILE-001 | File not found        | Error    |
| FT-FILE-002 | Permission denied     | Error    |
| FT-FILE-003 | File already exists   | Warning  |
| FT-ODS-001  | Invalid ODS format    | Error    |
| FT-ODS-002  | Sheet not found       | Error    |
| FT-CSV-001  | Cannot parse CSV      | Error    |
| FT-CSV-002  | Unknown bank format   | Warning  |
| FT-VAL-001  | Invalid amount        | Error    |
| FT-VAL-002  | Invalid date          | Error    |
| FT-VAL-003  | Invalid category      | Error    |
| FT-CFG-001  | Missing config key    | Error    |
| FT-CFG-002  | Invalid config value  | Error    |
| FT-NET-001  | Connection failed     | Error    |
| FT-NET-002  | Authentication failed | Error    |
| FT-TMPL-001 | Template not found    | Error    |
| FT-FMT-001  | Invalid color         | Error    |

---

## Appendix E: Configuration Reference (NEW)

### Complete Configuration Schema

```yaml
# spreadsheet-dl configuration file
# Location: ~/.config/spreadsheet-dl/config.yaml

# Schema version for migration
schema_version: '1.0'

# Nextcloud/WebDAV settings
nextcloud:
  url: '' # https://your-nextcloud.com
  username: '' # Nextcloud username
  # password via NEXTCLOUD_PASSWORD env var
  remote_path: '/Finance' # Remote directory
  verify_ssl: true # Verify SSL certificates

# Default settings
defaults:
  output_directory: '.' # Output directory
  template: '' # Default budget template
  empty_rows: 50 # Empty rows in expense log
  date_format: '%Y-%m-%d' # Date display format
  currency_symbol: '$' # Currency symbol
  currency_decimal_places: 2 # Decimal places

# Alert thresholds
alerts:
  warning_threshold: 80.0 # Warning at 80%
  critical_threshold: 95.0 # Critical at 95%
  enable_notifications: false # Email notifications
  notification_email: '' # Email address

# Display settings
display:
  use_color: true # Colored output
  show_progress: true # Progress indicators
  compact_output: false # Compact mode
  json_pretty_print: true # Pretty JSON

# Formatting settings (NEW)
formatting:
  locale: 'auto' # System locale or explicit
  currency:
    symbol: '$'
    symbol_position: 'prefix'
    decimal_separator: '.'
    thousands_separator: ','
    decimal_places: 2
    negative_format: '-$X'
  date:
    format: '%Y-%m-%d'
    input_formats:
      - '%Y-%m-%d'
      - '%m/%d/%Y'
    use_relative: true
    relative_threshold_days: 7
  print:
    page_size: 'letter'
    orientation: 'portrait'
    margins:
      top: '1in'
      bottom: '1in'
      left: '0.75in'
      right: '0.75in'

# Plugin settings (NEW)
plugins:
  enabled: [] # List of enabled plugins
  disabled: [] # Explicitly disabled
  auto_discover: true # Auto-discover installed
```

---

## See Also

### Related Documentation

- **[Dual-Audience Requirements](2025-12-28-dual-audience-requirements.md)** - Comprehensive requirements for human-readable AND AI/LLM-readable representations of budget data
  - 12 AI/LLM integration requirements
  - 3 human rendering requirements
  - 4 dual export requirements
  - 6 identified gaps in AI/LLM support
  - Implementation examples and MCP integration

This addendum ensures spreadsheet-dl serves both human users (visual ODS spreadsheets) and AI assistants (structured JSON with semantic metadata) optimally.

---

## Document Control

| Version | Date       | Author | Changes                                                                                    |
| ------- | ---------- | ------ | ------------------------------------------------------------------------------------------ |
| 1.0.0   | 2025-12-28 | Claude | Initial comprehensive analysis                                                             |
| 2.0.0   | 2025-12-28 | Claude | Added UI/UX, Extensibility, Template/Config, Formatting requirements (44 new requirements) |
| 2.1.0   | 2025-12-28 | Claude | Added reference to Dual-Audience Requirements addendum                                     |

---

_End of Requirements Specification_
