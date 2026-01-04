# Config API Reference

Configuration management for SpreadsheetDL.

**Implements:** FR-CONFIG-001 (Configuration Management)

## Overview

The Config module provides a unified configuration system that supports multiple sources:

1. **YAML configuration files** (~/.config/spreadsheet-dl/config.yaml, ~/.spreadsheet-dl.yaml, etc.)
2. **Environment variables** (NEXTCLOUD_URL, NEXTCLOUD_USER, etc.)
3. **Program defaults** (sensible defaults for all settings)

Later sources override earlier ones, with environment variables having the highest priority.

## Configuration Classes

### NextcloudSettings

Nextcloud/WebDAV server configuration.

```python
from spreadsheet_dl.config import NextcloudSettings

settings = NextcloudSettings(
    url="https://nextcloud.example.com",
    username="user@example.com",
    password="app-password",
    remote_path="/Finance",
    verify_ssl=True
)

# Check if configured
if settings.is_configured():
    print("Ready for upload")
```

**Attributes:**

- `url: str` - Server base URL (e.g., "https://nextcloud.example.com")
- `username: str` - Nextcloud username
- `password: str` - Nextcloud password or app password
- `remote_path: str` - Remote directory path (default: "/Finance")
- `verify_ssl: bool` - Whether to verify SSL certificates (default: True)

**Methods:**

#### `is_configured() -> bool`

Check if Nextcloud is fully configured (all required fields present).

```python
if settings.is_configured():
    # Safe to use for uploads
```

---

### DefaultSettings

Default values for common operations.

```python
from spreadsheet_dl.config import DefaultSettings
from pathlib import Path

defaults = DefaultSettings(
    output_directory=Path.home() / "Documents" / "Budgets",
    template="50_30_20",
    empty_rows=100,
    date_format="%Y-%m-%d",
    currency_symbol="$",
    currency_decimal_places=2
)
```

**Attributes:**

- `output_directory: Path` - Default directory for generated files
- `template: str` - Default budget template name
- `empty_rows: int` - Number of empty rows to pre-allocate
- `date_format: str` - Default date format string
- `currency_symbol: str` - Currency symbol for formatting
- `currency_decimal_places: int` - Decimal places for currency values

---

### AlertSettings

Alert threshold configuration for budget monitoring.

```python
from spreadsheet_dl.config import AlertSettings

alerts = AlertSettings(
    warning_threshold=80.0,      # Warn at 80% of budget
    critical_threshold=95.0,     # Critical at 95%
    enable_notifications=True,
    notification_email="user@example.com"
)
```

**Attributes:**

- `warning_threshold: float` - Budget percentage for warning alerts (default: 80.0)
- `critical_threshold: float` - Budget percentage for critical alerts (default: 95.0)
- `enable_notifications: bool` - Enable email notifications
- `notification_email: str` - Email address for notifications

---

### DisplaySettings

Display and formatting settings for CLI output.

```python
from spreadsheet_dl.config import DisplaySettings

display = DisplaySettings(
    use_color=True,           # Colored CLI output
    show_progress=True,       # Progress bars
    compact_output=False,     # Verbose output
    json_pretty_print=True    # Formatted JSON
)
```

**Attributes:**

- `use_color: bool` - Use colored terminal output
- `show_progress: bool` - Show progress indicators
- `compact_output: bool` - Compact output format
- `json_pretty_print: bool` - Pretty-print JSON output

---

### Config

Main configuration container aggregating all settings.

```python
from spreadsheet_dl.config import Config

# Create with defaults
config = Config()

# Load from all sources (files + environment)
config = Config.load()

# Load from specific file
config = Config.load("~/.spreadsheet-dl.yaml")

# Save configuration
config.save("~/.config/spreadsheet-dl/config.yaml")

# Export as dictionary
data = config.to_dict()
```

**Attributes:**

- `nextcloud: NextcloudSettings` - Nextcloud configuration
- `defaults: DefaultSettings` - Default operation settings
- `alerts: AlertSettings` - Alert thresholds
- `display: DisplaySettings` - Display settings

**Methods:**

#### `load(config_path: Path | str | None = None) -> Config`

Load configuration from all available sources.

Configuration is loaded in this order (later overrides earlier):

1. Explicitly specified file (if provided)
2. Default file locations (XDG_CONFIG_HOME, ~/.config, ~/.spreadsheet-dl.yaml, etc.)
3. Environment variables
4. Program defaults (built-in)

```python
# Auto-detect configuration file location
config = Config.load()

# Load from specific file
config = Config.load("/etc/spreadsheet-dl/config.yaml")

# Then override from environment
import os
os.environ["NEXTCLOUD_URL"] = "https://example.com"
config = Config.load()  # Reloads with env var
```

**Parameters:**

- `config_path`: Optional explicit path to YAML config file

**Returns:** Merged Config instance

**Raises:** ImportError if PyYAML is not installed (handled gracefully)

#### `to_dict() -> dict[str, Any]`

Export configuration as a dictionary.

```python
data = config.to_dict()

# Output structure:
# {
#     "nextcloud": {...},
#     "defaults": {...},
#     "alerts": {...},
#     "display": {...}
# }
```

#### `save(path: Path | str) -> None`

Save configuration to a YAML file.

```python
config.save("~/.config/spreadsheet-dl/config.yaml")

# Auto-creates parent directories
# Note: Password is NOT saved to file for security
```

**Parameters:**

- `path`: Path to save YAML configuration file

**Raises:** ImportError if PyYAML not installed

---

## Global Functions

### get_config(reload: bool = False) -> Config

Get the global configuration instance (singleton).

```python
from spreadsheet_dl.config import get_config

# First call loads from all sources
config = get_config()

# Subsequent calls return cached instance
config = get_config()  # Returns same instance

# Force reload from sources
config = get_config(reload=True)
```

**Parameters:**

- `reload`: Force reload from all sources

**Returns:** Global Config instance

---

### init_config_file(path: Path | str | None = None) -> Path

Initialize a new configuration file with defaults.

```python
from spreadsheet_dl.config import init_config_file

# Create at default location
path = init_config_file()
# -> ~/.config/spreadsheet-dl/config.yaml

# Create at custom location
path = init_config_file("/etc/spreadsheet-dl/config.yaml")
```

**Parameters:**

- `path`: Optional explicit path for config file. Defaults to ~/.config/spreadsheet-dl/config.yaml

**Returns:** Path to created configuration file

**Raises:** OSError if directory creation fails

---

## Configuration File Format

YAML configuration file format:

```yaml
# Nextcloud/WebDAV configuration
nextcloud:
  url: 'https://nextcloud.example.com'
  username: 'user@example.com'
  password: 'app-password'
  remote_path: '/Finance'
  verify_ssl: true

# Default operation settings
defaults:
  output_directory: '/home/user/Documents/Budgets'
  template: '50_30_20'
  empty_rows: 50
  date_format: '%Y-%m-%d'
  currency_symbol: '$'
  currency_decimal_places: 2

# Alert thresholds
alerts:
  warning_threshold: 80.0
  critical_threshold: 95.0
  enable_notifications: false
  notification_email: ''

# Display settings
display:
  use_color: true
  show_progress: true
  compact_output: false
  json_pretty_print: true
```

---

## Environment Variables

Supported environment variables:

- `NEXTCLOUD_URL` - Nextcloud server URL
- `NEXTCLOUD_USER` - Nextcloud username
- `NEXTCLOUD_PASSWORD` - Nextcloud password/app password
- `NEXTCLOUD_PATH` - Remote path (default: /Finance)
- `SPREADSHEET_DL_OUTPUT_DIR` - Default output directory
- `SPREADSHEET_DL_TEMPLATE` - Default template name
- `SPREADSHEET_DL_NO_PROGRESS` - Disable progress indicators
- `NO_COLOR` - Disable colored output

Example:

```bash
export NEXTCLOUD_URL="https://nextcloud.example.com"
export NEXTCLOUD_USER="user@example.com"
export NEXTCLOUD_PASSWORD="app-password"
export SPREADSHEET_DL_OUTPUT_DIR="/home/user/budgets"

# Now use the tool with these settings
spreadsheet-dl generate
```

---

## Configuration Priority Order

When the same setting is provided in multiple places:

1. **Program defaults** (lowest priority)
2. **Configuration file** (YAML)
3. **Environment variables** (highest priority)

This means environment variables override config files, which override defaults.

```python
# Example with priority chain
import os
from spreadsheet_dl.config import Config

# 1. Start with defaults
config = Config()

# 2. Config file overrides defaults
config = Config.load("my_config.yaml")

# 3. Environment variable overrides both
os.environ["NEXTCLOUD_URL"] = "https://override.example.com"
config = Config.load()
```

---

## Complete Example

```python
from pathlib import Path
from spreadsheet_dl.config import (
    Config,
    NextcloudSettings,
    DefaultSettings,
    AlertSettings,
    DisplaySettings,
    get_config,
    init_config_file,
)

# Initialize default config file
config_path = init_config_file()
print(f"Config file created at: {config_path}")

# Load configuration from all sources
config = Config.load()

# Check Nextcloud connectivity
if config.nextcloud.is_configured():
    print("Nextcloud is configured")
    print(f"  URL: {config.nextcloud.url}")
    print(f"  Path: {config.nextcloud.remote_path}")

# Use defaults for file generation
output_dir = config.defaults.output_directory
template = config.defaults.template
print(f"Default output: {output_dir}")
print(f"Default template: {template}")

# Check alert settings
if config.alerts.enable_notifications:
    print(f"Alerts enabled, email: {config.alerts.notification_email}")

# Use display settings
if config.display.use_color:
    print("Using colored output")

# Export configuration
config_dict = config.to_dict()
print(config_dict)

# Get global config singleton
global_config = get_config()
```

---

## Environment Detection

The config module automatically detects configuration files in this order:

1. `$XDG_CONFIG_HOME/spreadsheet-dl/config.yaml`
2. `~/.config/spreadsheet-dl/config.yaml`
3. `~/.config/spreadsheet-dl/config.yml`
4. `~/.spreadsheet-dl.yaml`
5. `~/.spreadsheet-dl.yml`
6. `./.spreadsheet-dl.yaml` (project directory)
7. `./spreadsheet-dl.yaml` (project directory)

The first file found is used, or you can specify an explicit path.
