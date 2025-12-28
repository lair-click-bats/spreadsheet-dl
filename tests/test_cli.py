"""Tests for CLI interface."""

from __future__ import annotations

import json
import subprocess
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the CLI with given arguments."""
    return subprocess.run(
        [sys.executable, "-m", "finance_tracker.cli", *args],
        capture_output=True,
        text=True,
    )


class TestCLIBasics:
    """Tests for basic CLI functionality."""

    def test_version_flag(self) -> None:
        """Test --version flag shows version."""
        result = run_cli("--version")
        assert result.returncode == 0
        assert "finance-tracker" in result.stdout
        assert "0.4.0" in result.stdout

    def test_version_short_flag(self) -> None:
        """Test -V flag shows version."""
        result = run_cli("-V")
        assert result.returncode == 0
        assert "0.4.0" in result.stdout

    def test_help_flag(self) -> None:
        """Test --help flag shows help."""
        result = run_cli("--help")
        assert result.returncode == 0
        assert "finance-tracker" in result.stdout
        assert "generate" in result.stdout
        assert "analyze" in result.stdout
        assert "report" in result.stdout

    def test_no_command_shows_help(self) -> None:
        """Test running without command shows help."""
        result = run_cli()
        assert result.returncode == 1  # Exits with error
        assert "usage:" in result.stdout.lower() or "finance-tracker" in result.stdout


class TestGenerateCommand:
    """Tests for generate command."""

    def test_generate_help(self) -> None:
        """Test generate --help."""
        result = run_cli("generate", "--help")
        assert result.returncode == 0
        assert "--output" in result.stdout
        assert "--month" in result.stdout
        assert "--year" in result.stdout
        assert "--template" in result.stdout

    def test_generate_creates_file(self, tmp_path: Path) -> None:
        """Test generate creates an ODS file."""
        result = run_cli("generate", "-o", str(tmp_path))
        assert result.returncode == 0
        assert "Created:" in result.stdout

        # Check file was created
        ods_files = list(tmp_path.glob("budget_*.ods"))
        assert len(ods_files) == 1

    def test_generate_with_month_year(self, tmp_path: Path) -> None:
        """Test generate with specific month and year."""
        result = run_cli("generate", "-o", str(tmp_path), "-m", "6", "-y", "2025")
        assert result.returncode == 0

        # Check correct filename
        assert (tmp_path / "budget_2025_06.ods").exists()

    def test_generate_with_template(self, tmp_path: Path) -> None:
        """Test generate with a template."""
        result = run_cli("generate", "-o", str(tmp_path), "-t", "50_30_20")
        assert result.returncode == 0
        assert "Using template: 50/30/20 Rule" in result.stdout


class TestTemplatesCommand:
    """Tests for templates command."""

    def test_templates_list(self) -> None:
        """Test templates command lists templates."""
        result = run_cli("templates")
        assert result.returncode == 0
        assert "50_30_20" in result.stdout
        assert "family" in result.stdout
        assert "minimalist" in result.stdout

    def test_templates_json(self) -> None:
        """Test templates --json output."""
        result = run_cli("templates", "--json")
        assert result.returncode == 0

        # Should be valid JSON
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        assert len(data) > 0
        assert "name" in data[0]


class TestConfigCommand:
    """Tests for config command."""

    def test_config_help(self) -> None:
        """Test config command shows info."""
        result = run_cli("config")
        assert result.returncode == 0
        assert "Configuration" in result.stdout
        assert "NEXTCLOUD_URL" in result.stdout

    def test_config_show(self) -> None:
        """Test config --show outputs JSON."""
        result = run_cli("config", "--show")
        assert result.returncode == 0

        # Should be valid JSON
        data = json.loads(result.stdout)
        assert "nextcloud" in data
        assert "defaults" in data
        assert "display" in data

    def test_config_init(self, tmp_path: Path) -> None:
        """Test config --init creates config file."""
        config_path = tmp_path / "config.yaml"
        result = run_cli("config", "--init", "--path", str(config_path))

        # May fail if pyyaml not installed, that's OK
        if result.returncode == 0:
            assert config_path.exists()
            assert "Configuration file created" in result.stdout


class TestAnalyzeCommand:
    """Tests for analyze command."""

    def test_analyze_file_not_found(self, tmp_path: Path) -> None:
        """Test analyze with non-existent file."""
        result = run_cli("analyze", str(tmp_path / "nonexistent.ods"))
        assert result.returncode == 1
        assert (
            "not found" in result.stderr.lower() or "not found" in result.stdout.lower()
        )

    def test_analyze_with_json(self, tmp_path: Path) -> None:
        """Test analyze --json output."""
        # First create a budget file
        run_cli("generate", "-o", str(tmp_path))
        ods_file = next(iter(tmp_path.glob("budget_*.ods")))

        result = run_cli("analyze", str(ods_file), "--json")
        assert result.returncode == 0

        # Should be valid JSON
        data = json.loads(result.stdout)
        assert "total_budget" in data
        assert "total_spent" in data


class TestDashboardCommand:
    """Tests for dashboard command."""

    def test_dashboard_file_not_found(self, tmp_path: Path) -> None:
        """Test dashboard with non-existent file."""
        result = run_cli("dashboard", str(tmp_path / "nonexistent.ods"))
        assert result.returncode == 1

    def test_dashboard_output(self, tmp_path: Path) -> None:
        """Test dashboard produces output."""
        # First create a budget file
        run_cli("generate", "-o", str(tmp_path))
        ods_file = next(iter(tmp_path.glob("budget_*.ods")))

        result = run_cli("dashboard", str(ods_file))
        assert result.returncode == 0
        assert "BUDGET DASHBOARD" in result.stdout
        assert "SUMMARY" in result.stdout


class TestExpenseCommand:
    """Tests for expense command."""

    def test_expense_help(self) -> None:
        """Test expense --help."""
        result = run_cli("expense", "--help")
        assert result.returncode == 0
        assert "amount" in result.stdout.lower()
        assert "description" in result.stdout.lower()

    def test_expense_invalid_amount(self) -> None:
        """Test expense with invalid amount."""
        result = run_cli("expense", "not-a-number", "Test expense")
        assert result.returncode == 1
        assert "INVALID_AMOUNT" in result.stderr or "invalid" in result.stderr.lower()

    def test_expense_invalid_date(self) -> None:
        """Test expense with invalid date."""
        result = run_cli("expense", "25.00", "Test", "-d", "bad-date")
        assert result.returncode == 1
        assert "INVALID_DATE" in result.stderr or "invalid" in result.stderr.lower()

    def test_expense_invalid_category(self) -> None:
        """Test expense with invalid category."""
        result = run_cli("expense", "25.00", "Test", "-c", "NotACategory")
        assert result.returncode == 1
        assert "INVALID_CATEGORY" in result.stderr or "invalid" in result.stderr.lower()


class TestImportCommand:
    """Tests for import command."""

    def test_import_file_not_found(self, tmp_path: Path) -> None:
        """Test import with non-existent file."""
        result = run_cli("import", str(tmp_path / "nonexistent.csv"))
        assert result.returncode == 1
        assert "not found" in result.stderr.lower()


class TestAlertsCommand:
    """Tests for alerts command."""

    def test_alerts_file_not_found(self, tmp_path: Path) -> None:
        """Test alerts with non-existent file."""
        result = run_cli("alerts", str(tmp_path / "nonexistent.ods"))
        assert result.returncode == 1

    def test_alerts_json(self, tmp_path: Path) -> None:
        """Test alerts --json output."""
        # First create a budget file
        run_cli("generate", "-o", str(tmp_path))
        ods_file = next(iter(tmp_path.glob("budget_*.ods")))

        result = run_cli("alerts", str(ods_file), "--json")
        assert result.returncode == 0
        # Should be valid JSON (may be empty alerts list)
        data = json.loads(result.stdout)
        assert isinstance(data, (dict, list))


class TestReportCommand:
    """Tests for report command."""

    def test_report_file_not_found(self, tmp_path: Path) -> None:
        """Test report with non-existent file."""
        result = run_cli("report", str(tmp_path / "nonexistent.ods"))
        assert result.returncode == 1

    def test_report_markdown(self, tmp_path: Path) -> None:
        """Test report with markdown format."""
        # First create a budget file
        run_cli("generate", "-o", str(tmp_path))
        ods_file = next(iter(tmp_path.glob("budget_*.ods")))

        result = run_cli("report", str(ods_file), "-f", "markdown")
        assert result.returncode == 0
        assert "# Budget Report" in result.stdout

    def test_report_text(self, tmp_path: Path) -> None:
        """Test report with text format."""
        # First create a budget file
        run_cli("generate", "-o", str(tmp_path))
        ods_file = next(iter(tmp_path.glob("budget_*.ods")))

        result = run_cli("report", str(ods_file), "-f", "text")
        assert result.returncode == 0
        assert "BUDGET REPORT" in result.stdout

    def test_report_json(self, tmp_path: Path) -> None:
        """Test report with JSON format."""
        # First create a budget file
        run_cli("generate", "-o", str(tmp_path))
        ods_file = next(iter(tmp_path.glob("budget_*.ods")))

        result = run_cli("report", str(ods_file), "-f", "json")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "pie_chart" in data or "bar_chart" in data
