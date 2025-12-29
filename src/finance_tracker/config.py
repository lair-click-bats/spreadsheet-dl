"""
Configuration management for finance tracker.

Supports configuration from:
1. YAML config file (~/.finance-tracker.yaml or ~/.config/finance-tracker/config.yaml)
2. Environment variables
3. Command-line arguments (highest priority)

Configuration is merged with later sources overriding earlier ones.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Try to import yaml, fall back gracefully
try:
    import yaml

    HAS_YAML = True
except ImportError:
    yaml = None  # type: ignore[assignment]
    HAS_YAML = False


@dataclass
class NextcloudSettings:
    """Nextcloud/WebDAV configuration."""

    url: str = ""
    username: str = ""
    password: str = ""
    remote_path: str = "/Finance"
    verify_ssl: bool = True

    def is_configured(self) -> bool:
        """Check if Nextcloud is fully configured."""
        return bool(self.url and self.username and self.password)


@dataclass
class DefaultSettings:
    """Default values for common operations."""

    output_directory: Path = field(default_factory=Path.cwd)
    template: str = ""
    empty_rows: int = 50
    date_format: str = "%Y-%m-%d"
    currency_symbol: str = "$"
    currency_decimal_places: int = 2


@dataclass
class AlertSettings:
    """Alert threshold configuration."""

    warning_threshold: float = 80.0
    critical_threshold: float = 95.0
    enable_notifications: bool = False
    notification_email: str = ""


@dataclass
class DisplaySettings:
    """Display and formatting settings."""

    use_color: bool = True
    show_progress: bool = True
    compact_output: bool = False
    json_pretty_print: bool = True


@dataclass
class Config:
    """
    Main configuration container.

    Aggregates all configuration settings with sensible defaults.
    """

    nextcloud: NextcloudSettings = field(default_factory=NextcloudSettings)
    defaults: DefaultSettings = field(default_factory=DefaultSettings)
    alerts: AlertSettings = field(default_factory=AlertSettings)
    display: DisplaySettings = field(default_factory=DisplaySettings)

    @classmethod
    def load(cls, config_path: Path | str | None = None) -> Config:
        """
        Load configuration from all sources.

        Args:
            config_path: Optional explicit config file path.

        Returns:
            Merged configuration from all sources.
        """
        config = cls()

        # Load from file
        file_config = cls._load_from_file(config_path)
        if file_config:
            config = cls._merge_dict_into_config(config, file_config)

        # Load from environment (overrides file)
        config = cls._load_from_env(config)

        return config

    @classmethod
    def _get_config_paths(cls) -> list[Path]:
        """Get list of possible config file paths in priority order."""
        paths = []

        # XDG config directory
        xdg_config = os.environ.get("XDG_CONFIG_HOME", "")
        if xdg_config:
            paths.append(Path(xdg_config) / "finance-tracker" / "config.yaml")

        # Home directory locations
        home = Path.home()
        paths.extend(
            [
                home / ".config" / "finance-tracker" / "config.yaml",
                home / ".config" / "finance-tracker" / "config.yml",
                home / ".finance-tracker.yaml",
                home / ".finance-tracker.yml",
            ]
        )

        # Current directory
        paths.extend(
            [
                Path.cwd() / ".finance-tracker.yaml",
                Path.cwd() / ".finance-tracker.yml",
                Path.cwd() / "finance-tracker.yaml",
            ]
        )

        return paths

    @classmethod
    def _load_from_file(cls, explicit_path: Path | str | None = None) -> dict[str, Any]:
        """Load configuration from YAML file."""
        if not HAS_YAML:
            return {}

        # Try explicit path first
        if explicit_path:
            path = Path(explicit_path)
            if path.exists():
                return cls._parse_yaml_file(path)
            return {}

        # Try default paths
        for path in cls._get_config_paths():
            if path.exists():
                return cls._parse_yaml_file(path)

        return {}

    @classmethod
    def _parse_yaml_file(cls, path: Path) -> dict[str, Any]:
        """Parse a YAML configuration file."""
        if yaml is None:
            return {}
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
                return data if isinstance(data, dict) else {}
        except (OSError, ValueError, yaml.YAMLError):
            return {}

    @classmethod
    def _load_from_env(cls, config: Config) -> Config:
        """Load configuration from environment variables."""
        # Nextcloud settings
        if url := os.environ.get("NEXTCLOUD_URL"):
            config.nextcloud.url = url
        if user := os.environ.get("NEXTCLOUD_USER"):
            config.nextcloud.username = user
        if password := os.environ.get("NEXTCLOUD_PASSWORD"):
            config.nextcloud.password = password
        if path := os.environ.get("NEXTCLOUD_PATH"):
            config.nextcloud.remote_path = path

        # Display settings
        if os.environ.get("NO_COLOR"):
            config.display.use_color = False
        if os.environ.get("FINANCE_TRACKER_NO_PROGRESS"):
            config.display.show_progress = False

        # Default output directory
        if output_dir := os.environ.get("FINANCE_TRACKER_OUTPUT_DIR"):
            config.defaults.output_directory = Path(output_dir)

        # Default template
        if template := os.environ.get("FINANCE_TRACKER_TEMPLATE"):
            config.defaults.template = template

        return config

    @classmethod
    def _merge_dict_into_config(cls, config: Config, data: dict[str, Any]) -> Config:
        """Merge a dictionary into the config object."""
        # Nextcloud settings
        if nc := data.get("nextcloud", {}):
            if url := nc.get("url"):
                config.nextcloud.url = url
            if user := nc.get("username"):
                config.nextcloud.username = user
            if password := nc.get("password"):
                config.nextcloud.password = password
            if path := nc.get("remote_path"):
                config.nextcloud.remote_path = path
            if "verify_ssl" in nc:
                config.nextcloud.verify_ssl = nc["verify_ssl"]

        # Default settings
        if defaults := data.get("defaults", {}):
            if output_dir := defaults.get("output_directory"):
                config.defaults.output_directory = Path(output_dir)
            if template := defaults.get("template"):
                config.defaults.template = template
            if rows := defaults.get("empty_rows"):
                config.defaults.empty_rows = int(rows)
            if date_fmt := defaults.get("date_format"):
                config.defaults.date_format = date_fmt
            if currency := defaults.get("currency_symbol"):
                config.defaults.currency_symbol = currency

        # Alert settings
        if alerts := data.get("alerts", {}):
            if warning := alerts.get("warning_threshold"):
                config.alerts.warning_threshold = float(warning)
            if critical := alerts.get("critical_threshold"):
                config.alerts.critical_threshold = float(critical)
            if "enable_notifications" in alerts:
                config.alerts.enable_notifications = alerts["enable_notifications"]
            if email := alerts.get("notification_email"):
                config.alerts.notification_email = email

        # Display settings
        if display := data.get("display", {}):
            if "use_color" in display:
                config.display.use_color = display["use_color"]
            if "show_progress" in display:
                config.display.show_progress = display["show_progress"]
            if "compact_output" in display:
                config.display.compact_output = display["compact_output"]
            if "json_pretty_print" in display:
                config.display.json_pretty_print = display["json_pretty_print"]

        return config

    def to_dict(self) -> dict[str, Any]:
        """Export configuration as dictionary."""
        return {
            "nextcloud": {
                "url": self.nextcloud.url,
                "username": self.nextcloud.username,
                "remote_path": self.nextcloud.remote_path,
                "verify_ssl": self.nextcloud.verify_ssl,
            },
            "defaults": {
                "output_directory": str(self.defaults.output_directory),
                "template": self.defaults.template,
                "empty_rows": self.defaults.empty_rows,
                "date_format": self.defaults.date_format,
                "currency_symbol": self.defaults.currency_symbol,
            },
            "alerts": {
                "warning_threshold": self.alerts.warning_threshold,
                "critical_threshold": self.alerts.critical_threshold,
                "enable_notifications": self.alerts.enable_notifications,
                "notification_email": self.alerts.notification_email,
            },
            "display": {
                "use_color": self.display.use_color,
                "show_progress": self.display.show_progress,
                "compact_output": self.display.compact_output,
                "json_pretty_print": self.display.json_pretty_print,
            },
        }

    def save(self, path: Path | str) -> None:
        """
        Save configuration to a YAML file.

        Args:
            path: Path to save the configuration file.
        """
        if not HAS_YAML or yaml is None:
            raise ImportError("PyYAML is required to save configuration files")

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Don't save password to file for security
        data = self.to_dict()
        data["nextcloud"]["password"] = ""

        with open(path, "w") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)


# Global configuration instance (lazy-loaded)
_config: Config | None = None


def get_config(reload: bool = False) -> Config:
    """
    Get the global configuration instance.

    Args:
        reload: Force reload configuration from sources.

    Returns:
        Global Config instance.
    """
    global _config
    if _config is None or reload:
        _config = Config.load()
    return _config


def init_config_file(path: Path | str | None = None) -> Path:
    """
    Initialize a new configuration file with defaults.

    Args:
        path: Path for the config file. Defaults to ~/.config/finance-tracker/config.yaml

    Returns:
        Path to the created configuration file.
    """
    if path is None:
        path = Path.home() / ".config" / "finance-tracker" / "config.yaml"
    else:
        path = Path(path)

    config = Config()
    config.save(path)
    return path
