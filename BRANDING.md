# SpreadsheetDL Brand Guidelines

**Version:** 1.0
**Last Updated:** 2026-01-03
**Status:** Official

---

## Overview

This document defines the official branding guidelines for SpreadsheetDL, ensuring consistent presentation across all documentation, code, marketing, and communication channels.

---

## Name & Capitalization

### Official Name

**SpreadsheetDL** (one word, capital S, capital D, capital L)

### Package & Import Names

```python
# PyPI package name (lowercase, hyphenated)
pip install spreadsheet-dl

# Python import (lowercase, underscored)
import spreadsheet_dl
from spreadsheet_dl import create_spreadsheet

# CLI command (lowercase, hyphenated)
spreadsheet-dl generate
```

### Usage Rules

✅ **CORRECT:**

- SpreadsheetDL is a universal spreadsheet definition language
- The SpreadsheetDL project
- Using SpreadsheetDL for finance
- Install `spreadsheet-dl` (in code blocks)
- Import `spreadsheet_dl` (in code)

❌ **INCORRECT:**

- spreadsheetdl (no capitals)
- Spreadsheet-DL (hyphen in prose)
- spreadsheet-DL (mixed case)
- Spreadsheet DL (two words)
- SDL (abbreviation conflicts with Simple DirectMedia Layer)

### When to Use Which Form

| Context                 | Form           | Example                                     |
| ----------------------- | -------------- | ------------------------------------------- |
| **Marketing copy**      | SpreadsheetDL  | "SpreadsheetDL is the..."                   |
| **Documentation prose** | SpreadsheetDL  | "Using SpreadsheetDL, you can..."           |
| **Package names**       | spreadsheet-dl | `pip install spreadsheet-dl`                |
| **Python imports**      | spreadsheet_dl | `import spreadsheet_dl`                     |
| **CLI commands**        | spreadsheet-dl | `spreadsheet-dl generate`                   |
| **File names**          | spreadsheet-dl | `spreadsheet-dl-guide.md`                   |
| **URLs**                | spreadsheet-dl | `github.com/lair-click-bats/spreadsheet-dl` |

---

## Taglines

### Primary Tagline (Short Form)

> **"The Spreadsheet Definition Language for Python"**

**Use:** Headers, social media, elevator pitches

**Why:** Establishes category ("The" = definitive), clarifies "DL" meaning, targets Python devs

---

### Secondary Tagline (Expanded Form)

> **"Define complex spreadsheets in Python or YAML, export to ODS/XLSX/PDF. Built-in domains for finance, science, and engineering. Native MCP server for Claude integration."**

**Use:** GitHub repo description, README intro, PyPI description

**Why:** Shows concrete value (formats, domains, features) in 155 characters

---

### Alternate Taglines (Context-Specific)

**For developer audiences:**

> "Declarative spreadsheet definition language with domain plugins"

**For data scientists:**

> "From pandas DataFrames to publication-ready spreadsheets"

**For AI/LLM developers:**

> "Built for the AI era with native MCP server"

**For finance professionals:**

> "Professional financial spreadsheets from Python code"

---

## Positioning Statement

### Full Positioning (Elevator Pitch - 30 seconds)

> **For** Python developers who need to generate complex spreadsheets programmatically,
>
> **SpreadsheetDL** is a **universal spreadsheet definition language**
>
> **That** lets you declare spreadsheet structure, formulas, and styling in code or YAML—then export to ODS, XLSX, or PDF.
>
> **Unlike** imperative libraries like openpyxl or xlsxwriter,
>
> **SpreadsheetDL** provides a **declarative, high-level API** with built-in theme support, formula validation, domain-specific templates for finance/science/engineering, and **native MCP integration for LLM agents**.

### Short Positioning (One-liner)

> "Declarative, multi-format, domain-aware spreadsheet language with native MCP server"

---

## Visual Identity

### Colors

**Primary Palette:**

- **Deep Blue** (#1a365d) - Professional, data-oriented, trust
- **Accent Green** (#38a169) - Growth, success, "go", validation
- **Charcoal** (#2d3748) - Text, borders, code blocks

**Domain-Specific Accent Colors:**

- Finance: Gold (#d69e2e)
- Science: Purple (#805ad5)
- Engineering: Orange (#dd6b20)
- Manufacturing: Steel Gray (#718096)
- Biology: Lime (#84cc16)
- Education: Sky Blue (#4299e1)
- Environmental: Forest Green (#22543d)

**Usage:**

- Headers/titles: Deep Blue
- CTAs/buttons: Accent Green
- Code blocks: Charcoal background
- Domain tags: Domain-specific colors

### Typography

**Code & Technical:**

- Font: JetBrains Mono, Fira Code, or system monospace
- Use for: Code examples, CLI commands, package names

**Marketing & Documentation:**

- Font: System sans-serif (-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto)
- Use for: Body text, explanations

**Headings:**

- **H1**: Bold, 2.5em, Deep Blue
- **H2**: Bold, 2em, Deep Blue
- **H3**: Bold, 1.5em, Charcoal

### Logo & Branding Assets

**Text-Only Logo (Primary):**

```
╔═══════════════════════╗
║  SpreadsheetDL        ║
║  ───────────────────  ║
║  The Spreadsheet      ║
║  Definition Language  ║
╚═══════════════════════╝
```

**ASCII Art (CLI/Terminal):**

```
 ____                        _     _               _   ____  _
/ ___| _ __  _ __ ___  __ _| | __| |___| |__   ___| |_|  _ \| |
\___ \| '_ \| '__/ _ \/ _` | |/ _` / __| '_ \ / _ \ __| | | | |
 ___) | |_) | | |  __/ (_| | | (_| \__ \ | | |  __/ |_| |_| | |___
|____/| .__/|_|  \___|\__,_|_|\__,_|___/_| |_|\___|\__|____/|_____|
      |_|
```

**Icon/Favicon Concept:**

- Simple grid (3×3) representing spreadsheet cells
- Deep Blue background, white grid lines
- Optional: Single cell highlighted in Accent Green

---

## Brand Voice & Tone

### Personality Traits

- **Technical** but accessible (not intimidating)
- **Confident** without arrogance (proven, not boastful)
- **Developer-empathetic** (we understand your pain points)
- **Open source community-minded** (collaborative, welcoming)

### Tone by Context

#### Documentation

- **Style**: Clear, precise, example-rich
- **Focus**: Explain "why" not just "how"
- **Examples**: Every concept has code example
- **Assumption**: Reader is competent Python developer

**✅ Good:**

> "The Builder API uses method chaining for readability. Each method returns the builder instance, letting you write:"

**❌ Bad:**

> "Method chaining is implemented via the fluent interface pattern wherein..."

---

#### Marketing (README, website, announcements)

- **Style**: Benefit-focused, problem-solving
- **Focus**: Lead with pain points, show solutions
- **Examples**: Concrete over abstract
- **Voice**: "You can..." not "We provide..."

**✅ Good:**

> "Tired of writing cell-by-cell spreadsheet code? SpreadsheetDL lets you define the structure once and export to any format."

**❌ Bad:**

> "SpreadsheetDL leverages a domain-driven architecture paradigm to facilitate declarative instantiation of spreadsheet artifacts."

---

#### Community (GitHub, Discord, issues)

- **Style**: Welcoming, collaborative, patient
- **Focus**: Help, don't judge
- **Examples**: "Great question!" not "You should have..."
- **Celebrate**: Contributions, milestones

**✅ Good:**

> "Great question! The formula builder works like this... [example]. Let me know if that helps!"

**❌ Bad:**

> "This is clearly documented in the API reference."

---

#### Announcements

- **Style**: Excited but not hyperbolic
- **Focus**: User value, not our effort
- **Examples**: Concrete metrics over vague claims
- **Voice**: Understated confidence

**✅ Good:**

> "We're pleased to announce SpreadsheetDL v4.0 with domain plugins for finance, science, and engineering. You can now create BOMs, experiment logs, and budgets using the same declarative API."

**❌ Bad:**

> "Revolutionary breakthrough! SpreadsheetDL v4.0 will completely transform how you think about spreadsheets forever! 🚀🔥💯"

---

## Messaging Framework

### Core Messages (Rule of Three)

#### 1. Declarative, Not Imperative

**Message**: "Define what you want, not how to build it"

**Example:**

```python
# openpyxl (imperative - 10+ lines)
ws['A1'] = 'Category'
ws['A1'].font = Font(bold=True, size=14)
ws['A1'].fill = PatternFill(fgColor='366092')
ws.column_dimensions['A'].width = 20
# ... repeat for every cell

# SpreadsheetDL (declarative - 1 line)
builder.sheet("Budget").header_row(style="header_primary")
```

---

#### 2. Universal Language, Domain-Aware

**Message**: "One language, any technical domain"

**Examples:**

- Finance: Budgets, statements, invoices
- Science: Experiments, datasets, analysis
- Engineering: BOMs, calculations, schedules
- Manufacturing: OEE, quality charts
- And more...

---

#### 3. LLM-Native from Day One

**Message**: "Built for the AI era with native MCP server"

**Example:**

> You: "Create a budget spreadsheet for Q1 2026"
> Claude (via MCP): _generates ODS with formulas, charts, themes_

---

## Competitive Positioning

### vs openpyxl

> "openpyxl is imperative and Excel-only. SpreadsheetDL is declarative, multi-format, and domain-aware."

### vs xlsxwriter

> "xlsxwriter is write-only and imperative. SpreadsheetDL provides round-trip editing, declarative API, and domain templates."

### vs pandas.to_excel()

> "pandas exports data, but you lose formulas, charts, and styling. SpreadsheetDL preserves the full spreadsheet model."

### vs All

> "Existing libraries force cell-by-cell imperative code. SpreadsheetDL lets you define structure once, with domain expertise built-in. Only tool built for the LLM era."

---

## Domain Positioning

### Finance

- **Message**: "From budgets to financial statements, all from Python"
- **Pain Point**: Manual Excel work, error-prone formulas
- **Solution**: Type-safe formulas, pre-built templates, bank import

### Data Science

- **Message**: "From pandas to publication-ready spreadsheets"
- **Pain Point**: to_excel() loses formatting, formulas, charts
- **Solution**: Statistical formulas, experiment tracking, reproducible reports

### Engineering

- **Message**: "BOMs, calculations, and schedules from code"
- **Pain Point**: Manual updates to Excel BOMs, calculation errors
- **Solution**: Component databases, validated formulas, revision tracking

### Manufacturing

- **Message**: "Quality dashboards and OEE tracking automated"
- **Pain Point**: Manual data entry, outdated charts
- **Solution**: SCADA integration, SPC charts, real-time dashboards

---

## Usage Examples

### Social Media Posts

**Twitter/X (280 chars):**

> 🧮 SpreadsheetDL v4.0 is here! Define spreadsheets as code, export to ODS/XLSX/PDF. Built-in domains for finance, science, & engineering. Native MCP server for Claude integration. Try it: github.com/lair-click-bats/spreadsheet-dl

**LinkedIn (Professional):**

> We're excited to announce SpreadsheetDL v4.0 - a universal spreadsheet definition language for Python. Instead of writing cell-by-cell imperative code, you define the structure once using a declarative API, then export to ODS, XLSX, or PDF.
>
> Key features:
>
> - Type-safe formula builder
> - Domain-specific templates (finance, science, engineering)
> - YAML-based theme system
> - Native MCP server for AI integration
>
> Perfect for developers who generate financial reports, scientific data tables, engineering BOMs, or manufacturing dashboards from code.
>
> Open source (MIT), 97% test coverage, production-ready.
>
> Check it out: [link]

---

### GitHub README Badges

```markdown
[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](releases)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-3,206%20passing-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-71%25-brightgreen.svg)](tests/)
[![MCP](https://img.shields.io/badge/MCP-native%20server-purple.svg)](docs/api/mcp_server.md)
```

---

### GitHub Topics/Tags

**Required (SEO & Discovery):**

```
spreadsheet
python
definition-language
declarative
ods
xlsx
pdf
```

**Recommended:**

```
mcp-server
claude
llm
finance
data-science
engineering
template-engine
builder-pattern
formula
chart
yaml
```

---

## File Naming Conventions

### Documentation Files

- `README.md` (not readme.md or ReadMe.md)
- `BRANDING.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `LICENSE` (no extension)

### Code Files

- `spreadsheet_dl/` (directory name)
- `builder.py` (not Builder.py)
- `test_builder.py` (test files)

### Example Files

- `example-budget.py` (hyphenated)
- `example-bom.py`
- `tutorial-1-basic-api.md`

---

## Version Naming

### Format

`MAJOR.MINOR.PATCH[-PRERELEASE]`

### Examples

- `4.0.0` (stable release)
- `4.0.0-alpha.1` (alpha prerelease)
- `4.0.0-beta.2` (beta prerelease)
- `4.1.0` (minor feature release)
- `4.0.1` (bugfix patch)

### Naming Scheme

- **Major (4.x.x)**: Breaking changes, new architecture
- **Minor (x.1.x)**: New features, backward compatible
- **Patch (x.x.1)**: Bug fixes only

**No code names** - use version numbers only

---

## Common Phrases & Terminology

### Preferred Terms

| Use This            | Not This                           |
| ------------------- | ---------------------------------- |
| SpreadsheetDL       | Spreadsheet DL, spreadsheetdl, SDL |
| definition language | DSL, description language          |
| declarative         | high-level, abstract               |
| domain plugin       | domain package, extension          |
| Builder API         | fluent API, builder pattern        |
| formula builder     | formula generator                  |
| theme               | style, stylesheet, skin            |
| MCP server          | MCP integration, MCP support       |
| export to ODS       | save as ODS, generate ODS          |

### Terminology Guidelines

**Technical terms:**

- First use: Define it ("SpreadsheetDL is a definition language that...")
- Subsequent: Use directly
- Avoid: Excessive jargon without context

**Domain terms:**

- Finance: Use standard terminology (budget, invoice, P&L)
- Science: Use field-specific terms (experiment log, dataset catalog)
- Engineering: Use industry terms (BOM, pin map, design calculation)

---

## Legal & Disclaimers

### Copyright Notice

```
Copyright (c) 2024-2026 lair-click-bats
Licensed under the MIT License
```

### Disclaimer for Calculations

> SpreadsheetDL provides tools for creating spreadsheets with formulas. Users are responsible for validating calculations for their specific use case. For critical applications (financial reporting, engineering calculations, etc.), always verify results independently.

### Disclaimer for Healthcare

> SpreadsheetDL is not validated for use in healthcare or medical applications. Do not use for patient data, clinical trials, or medical calculations without appropriate regulatory compliance and validation.

---

## Review & Updates

This branding guide should be reviewed and updated:

- **Major releases**: Update examples, version numbers
- **Quarterly**: Ensure consistency with actual usage
- **On feedback**: Incorporate community suggestions

**Owner**: Project maintainer (lair-click-bats)
**Contributors**: Open to community input via GitHub issues

---

**Document Version:** 1.0
**Last Updated:** 2026-01-03
**Status:** Official - All project materials should follow these guidelines
