# Contributing to SpreadsheetDL

First off, thank you for considering contributing to SpreadsheetDL! It's people like you that make SpreadsheetDL such a great tool.

## Pre-Release Status (IMPORTANT)

**SpreadsheetDL v4.0.0 is currently in alpha and has NOT been released to PyPI.**

This means:

- ✅ **Breaking changes are welcome** - We're perfecting the API before public release
- ✅ **Refactoring encouraged** - Improve code structure, naming, organization
- ✅ **No backwards compatibility needed** - We can change anything to make it better
- ✅ **Focus on quality** - Goal is the BEST possible v4.0.0, not backwards compatible alpha

**After v4.0.0 release:** We'll follow semantic versioning strictly.

## Code of Conduct

This project and everyone participating in it is governed by the [SpreadsheetDL Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, YAML templates, etc.)
- **Describe the behavior you observed and what you expected**
- **Include your environment details** (Python version, OS, SpreadsheetDL version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the test suite (`uv run pytest`)
5. Run linting (`uv run ruff check src/ tests/`)
6. Commit your changes using [conventional commits](https://www.conventionalcommits.org/)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone your fork
git clone https://github.com/lair-click-bats/spreadsheet-dl.git
cd spreadsheet-dl

# Install dependencies
uv sync --dev

# Run tests to verify setup
uv run pytest
```

### Development Commands

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=spreadsheet_dl --cov-report=term-missing

# Lint code
uv run ruff check src/ tests/

# Format code
uv run ruff format src/ tests/

# Type check
uv run mypy src/
```

## Coding Standards

### Style Guide

- Follow PEP 8 (enforced by ruff)
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and small

### Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, missing semi-colons, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(builder): add support for conditional formatting
fix(renderer): correct datetime serialization order
docs(api): add ChartBuilder examples
test(mcp): increase coverage to 95%
```

### Testing

- Write tests for all new features
- Maintain or improve test coverage (currently 97%)
- Use descriptive test names that explain the scenario
- Follow the existing test structure

### Documentation

- Update documentation for any user-facing changes
- Add docstrings to all public functions
- Include code examples where helpful
- Keep README.md up to date

### Branding & Naming

We have official branding guidelines to ensure consistency across all project materials. Please review [BRANDING.md](BRANDING.md) for:

- **Name usage**: When to use "SpreadsheetDL" vs "spreadsheet-dl" vs "spreadsheet_dl"
- **Taglines**: Official primary and secondary taglines
- **Terminology**: Preferred terms (e.g., "definition language" not "DSL", "domain plugin" not "extension")
- **Tone**: Brand voice guidelines for documentation, marketing, and community communication

**Quick Reference:**

- **In prose**: SpreadsheetDL (capitalized, no hyphen)
- **Package name**: spreadsheet-dl (lowercase, hyphenated)
- **Python imports**: spreadsheet_dl (lowercase, underscored)
- **Primary tagline**: "The Spreadsheet Definition Language for Python"

## Project Structure

```
spreadsheet-dl/
├── src/spreadsheet_dl/     # Source code
│   ├── builder.py          # Fluent builder API
│   ├── charts.py           # Chart builder
│   ├── renderer.py         # ODS renderer
│   ├── mcp_server.py       # MCP server
│   ├── schema/             # Data models
│   └── template_engine/    # Template system
├── tests/                  # Test suite
├── docs/                   # Documentation
├── examples/               # Usage examples
└── themes/                 # YAML theme files
```

## Getting Help

- **GitHub Discussions**: For questions and discussions
- **GitHub Issues**: For bugs and feature requests

## Recognition

Contributors are recognized in:

- The CHANGELOG.md for significant contributions
- The GitHub contributors page
- Special thanks in release notes for major features

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to SpreadsheetDL!
