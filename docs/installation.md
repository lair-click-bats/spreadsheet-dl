# Installation Guide

This guide covers installing Finance Tracker for development and production use.

## Requirements

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

## Quick Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/allenjd1/finance-tracker.git
cd finance-tracker

# Install dependencies
uv sync

# Verify installation
uv run finance-tracker --version
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/allenjd1/finance-tracker.git
cd finance-tracker

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package
pip install -e .

# Verify installation
finance-tracker --version
```

## Optional Dependencies

### Theme Support

For YAML-based themes, install with the config extra:

```bash
uv sync --extra config
# or
pip install -e ".[config]"
```

### Development Dependencies

For development and testing:

```bash
uv sync --dev
# or
pip install -e ".[dev]"
```

This includes:
- pytest - Testing framework
- pytest-cov - Coverage reporting
- ruff - Linting and formatting
- mypy - Type checking

## Verification

After installation, verify everything works:

```bash
# Check version
uv run finance-tracker --version

# Run tests
uv run pytest

# Generate a test budget
uv run finance-tracker generate -o /tmp/test/
```

## Environment Configuration

### Nextcloud Integration

For WebDAV upload functionality, set these environment variables:

```bash
export NEXTCLOUD_URL=https://your-nextcloud.com
export NEXTCLOUD_USER=username
export NEXTCLOUD_PASSWORD=app-password
export NEXTCLOUD_PATH=/Finance  # Optional, default: /Finance
```

### Configuration File

Alternatively, create a configuration file:

```bash
uv run finance-tracker config --init
```

This creates `~/.config/finance-tracker/config.yaml`.

## Platform-Specific Notes

### Linux

No special requirements. Ensure Python 3.11+ is available:

```bash
python3 --version
```

### macOS

Install Python via Homebrew if needed:

```bash
brew install python@3.11
```

### Windows

Install Python from [python.org](https://www.python.org/downloads/) or via Windows Store.

Use PowerShell for commands:

```powershell
uv run finance-tracker --version
```

## Troubleshooting

### Import Errors

If you see import errors, ensure the package is installed in development mode:

```bash
pip install -e .
```

### Missing Dependencies

If optional features fail, install extras:

```bash
# For theme support
uv sync --extra config

# For development
uv sync --dev
```

### Permission Issues

On Linux/macOS, if you get permission errors:

```bash
# Use user installation
pip install --user -e .
```

### Path Issues

Ensure the installed scripts are in your PATH:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

## Next Steps

After installation:

1. Read the [User Guide](user-guide.md) for comprehensive usage
2. Check [Examples](examples/index.md) for practical use cases
3. Review the [API Reference](api/index.md) for programmatic access
