# Contributing to SpreadsheetDL

First off, thank you for considering contributing to SpreadsheetDL! It's people like you that make SpreadsheetDL such a great tool.

## Versioning and Compatibility

SpreadsheetDL follows [Semantic Versioning](https://semver.org/) (SemVer):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

**Stability Commitment:**

- Backwards compatibility - Maintained within major versions
- Deprecation warnings - Added before removing features
- Migration guides - Provided for major version upgrades
- Semantic versioning - Strictly followed for all releases

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

# Build and serve documentation locally
scripts/docs.sh serve
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
- Maintain or improve test coverage (currently 71%)
- Use descriptive test names that explain the scenario
- Follow the existing test structure

### Documentation

- Update documentation for any user-facing changes
- Add docstrings to all public functions
- Include code examples where helpful
- Keep README.md up to date

## Documentation Checklist

Before submitting a PR that includes new code, ensure:

- [ ] All new public functions have docstrings
- [ ] Docstrings follow Google style format
- [ ] Args section lists all parameters with descriptions
- [ ] Returns section describes the return value
- [ ] Raises section documents all exceptions (if applicable)
- [ ] Examples are included for complex functionality
- [ ] Doctests pass: `uv run pytest --doctest-modules src/spreadsheet_dl/`
- [ ] User-facing docs updated if behavior changes
- [ ] CHANGELOG.md updated for user-visible changes

### Docstring Format

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int = 0) -> bool:
    """Brief one-line description.

    Extended description if needed. Can span multiple lines
    and provide additional context.

    Args:
        param1: Description of first parameter.
        param2: Description of second parameter. Defaults to 0.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param1 is empty.
        TypeError: When param2 is not an integer.

    Examples:
        >>> example_function("value", 10)
        True
    """
```

For detailed templates, see `.claude/templates/docstring.md`.

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
│   ├── domains/            # Domain plugins
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
