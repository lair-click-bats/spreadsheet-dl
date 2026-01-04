"""
Tests for MCP server finance/budget tools.

Tests IR-MCP-002: Native MCP Server - Finance Tools.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from spreadsheet_dl.mcp_server import (
    MCPConfig,
    MCPServer,
)

pytestmark = [pytest.mark.unit, pytest.mark.mcp]


class TestMCPServerAnalyzeBudgetHandlers:
    """Tests for analyze_budget handler with different analysis types."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_analyze_budget_summary_type(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test analyze_budget with summary type."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_analyze_budget(
            file_path=str(test_file),
            analysis_type="summary",
        )

        # Should return error (no real budget file) but not raise
        assert result is not None

    def test_analyze_budget_detailed_type(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test analyze_budget with detailed type."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_analyze_budget(
            file_path=str(test_file),
            analysis_type="detailed",
        )

        assert result is not None

    def test_analyze_budget_categories_type(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test analyze_budget with categories type."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_analyze_budget(
            file_path=str(test_file),
            analysis_type="categories",
        )

        assert result is not None

    def test_analyze_budget_trends_type(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test analyze_budget with trends type."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_analyze_budget(
            file_path=str(test_file),
            analysis_type="trends",
        )

        assert result is not None


class TestMCPServerQueryBudgetHandlers:
    """Tests for query_budget natural language processing."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_query_budget_total_spent_keyword(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget with total spent keywords."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_query_budget(
            question="How much have I spent in total?",
            file_path=str(test_file),
        )

        assert result is not None

    def test_query_budget_remaining_keyword(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget with remaining keywords."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_query_budget(
            question="How much budget is remaining?",
            file_path=str(test_file),
        )

        assert result is not None

    def test_query_budget_over_budget_keyword(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget with over budget keywords."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_query_budget(
            question="Am I over budget?",
            file_path=str(test_file),
        )

        assert result is not None

    def test_query_budget_default_response(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget with unrecognized question."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_query_budget(
            question="What is the meaning of life?",
            file_path=str(test_file),
        )

        assert result is not None


class TestMCPServerQueryBudgetCategoryMatching:
    """Tests for query_budget category matching logic."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_query_budget_with_category_match(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget with category name in question."""
        from decimal import Decimal

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            mock_summary = MagicMock()
            mock_summary.total_spent = Decimal("500")
            mock_summary.total_budget = Decimal("1000")
            mock_summary.total_remaining = Decimal("500")
            mock_summary.percent_used = Decimal("50")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("200"),
                "Transport": Decimal("150"),
                "Entertainment": Decimal("150"),
            }

            # Question with category name (avoid other keywords)
            result = server._handle_query_budget(
                question="Tell me about groceries category?",
                file_path=str(test_file),
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "Groceries" in data["answer"]
            assert data["data"]["category"] == "Groceries"
            assert data["data"]["amount"] == 200.0

    def test_query_budget_total_spent_path(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget total spent code path."""
        from decimal import Decimal

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            mock_summary = MagicMock()
            mock_summary.total_spent = Decimal("500")
            mock_summary.total_budget = Decimal("1000")
            mock_summary.total_remaining = Decimal("500")
            mock_summary.percent_used = Decimal("50")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("200")
            }

            # Test "spend" keyword
            result = server._handle_query_budget(
                question="How much did I spend?",
                file_path=str(test_file),
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "total_spent" in data["data"]
            assert data["data"]["total_spent"] == 500.0

    def test_query_budget_remaining_path(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget remaining budget code path."""
        from decimal import Decimal

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            mock_summary = MagicMock()
            mock_summary.total_spent = Decimal("500")
            mock_summary.total_budget = Decimal("1000")
            mock_summary.total_remaining = Decimal("500")
            mock_summary.percent_used = Decimal("50")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("200")
            }

            # Test "left" keyword
            result = server._handle_query_budget(
                question="How much budget is left?",
                file_path=str(test_file),
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "remaining" in data["data"]
            assert data["data"]["remaining"] == 500.0

    def test_query_budget_over_budget_path(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test query_budget over budget code path."""
        from decimal import Decimal

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            mock_summary = MagicMock()
            mock_summary.total_spent = Decimal("1100")
            mock_summary.total_budget = Decimal("1000")
            mock_summary.total_remaining = Decimal("-100")
            mock_summary.percent_used = Decimal("110")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("600"),
                "Transport": Decimal("500"),
            }

            # Test "overspent" keyword
            result = server._handle_query_budget(
                question="Did I overspent?",
                file_path=str(test_file),
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "percent_used" in data["data"]
            assert "is_over" in data["data"]
            assert data["data"]["is_over"] is True


class TestMCPServerSpendingTrends:
    """Tests for spending_trends with date grouping."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    @pytest.mark.skip(
        reason="Coverage+mock interaction issue - test passes without cov"
    )
    def test_spending_trends_with_category_filter(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test spending_trends with category filtering."""
        import pandas as pd

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            # Create mock expenses DataFrame
            mock_expenses = pd.DataFrame(
                {
                    "Date": ["2025-01-01", "2025-01-02", "2025-01-03"],
                    "Category": ["Groceries", "Transport", "Groceries"],
                    "Amount": [100.0, 50.0, 75.0],
                }
            )

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.expenses = mock_expenses

            result = server._handle_spending_trends(
                file_path=str(test_file),
                period="month",
                category="Groceries",
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "daily_spending" in data
            assert "statistics" in data
            assert data["category"] == "Groceries"
            assert "average_daily" in data["statistics"]

    def test_spending_trends_date_grouping(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test spending_trends date grouping logic."""
        import pandas as pd

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            # Create mock expenses DataFrame with Date column
            mock_expenses = pd.DataFrame(
                {
                    "Date": ["2025-01-01", "2025-01-01", "2025-01-02"],
                    "Category": ["Groceries", "Transport", "Groceries"],
                    "Amount": [100.0, 50.0, 75.0],
                }
            )

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.expenses = mock_expenses

            result = server._handle_spending_trends(
                file_path=str(test_file),
                period="week",
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "daily_spending" in data
            assert "2025-01-01" in data["daily_spending"]
            assert data["daily_spending"]["2025-01-01"] == 150.0
            assert data["statistics"]["total_days"] == 2
            assert data["statistics"]["highest_amount"] > 0


class TestMCPServerComparePeriods:
    """Tests for compare_periods calculations."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    @pytest.mark.skip(
        reason="Coverage+mock interaction issue - test passes without cov"
    )
    def test_compare_periods_calculations(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test compare_periods with date filtering and calculations."""
        import pandas as pd

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            # Create mock DataFrames for two periods
            p1_expenses = pd.DataFrame({"Amount": [100.0, 50.0, 75.0]})
            p2_expenses = pd.DataFrame({"Amount": [150.0, 100.0, 50.0]})

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.filter_by_date_range.side_effect = [p1_expenses, p2_expenses]

            result = server._handle_compare_periods(
                file_path=str(test_file),
                period1_start="2025-01-01",
                period1_end="2025-01-15",
                period2_start="2025-01-16",
                period2_end="2025-01-31",
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "period1" in data
            assert "period2" in data
            assert "comparison" in data
            assert data["period1"]["total"] == 225.0
            assert data["period2"]["total"] == 300.0
            assert "percent_change" in data["comparison"]

    @pytest.mark.skip(
        reason="Coverage+mock interaction issue - test passes without cov"
    )
    def test_compare_periods_zero_first_period(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test compare_periods when first period has zero spending."""
        import pandas as pd

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            # Empty first period, non-empty second
            p1_expenses = pd.DataFrame({"Amount": []})
            p2_expenses = pd.DataFrame({"Amount": [100.0, 50.0]})

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.filter_by_date_range.side_effect = [p1_expenses, p2_expenses]

            result = server._handle_compare_periods(
                file_path=str(test_file),
                period1_start="2025-01-01",
                period1_end="2025-01-15",
                period2_start="2025-01-16",
                period2_end="2025-01-31",
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert data["period1"]["total"] == 0.0
            assert data["period2"]["total"] == 150.0
            assert data["comparison"]["percent_change"] == 100


class TestMCPServerReportGeneration:
    """Tests for report generation with recommendations."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_generate_report_json_with_recommendations(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test JSON report format with recommendations."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with (
            patch(
                "spreadsheet_dl.domains.finance.report_generator.ReportGenerator"
            ) as MockReportGen,
            patch(
                "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
            ) as MockAnalyzer,
        ):
            mock_gen = MockReportGen.return_value
            mock_gen.generate_visualization_data.return_value = {
                "data": "test",
                "charts": [],
            }

            from decimal import Decimal

            mock_summary = MagicMock()
            mock_summary.total_remaining = Decimal("-100")
            mock_summary.percent_used = Decimal("110")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("500")
            }

            result = server._handle_generate_report(
                file_path=str(test_file),
                format="json",
                include_recommendations=True,
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "recommendations" in data
            assert len(data["recommendations"]) > 0

    def test_generate_report_markdown_with_recommendations(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test markdown report format with recommendations."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with (
            patch(
                "spreadsheet_dl.domains.finance.report_generator.ReportGenerator"
            ) as MockReportGen,
            patch(
                "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
            ) as MockAnalyzer,
        ):
            mock_gen = MockReportGen.return_value
            mock_gen.generate_markdown_report.return_value = "# Budget Report"

            from decimal import Decimal

            mock_summary = MagicMock()
            mock_summary.total_remaining = Decimal("100")
            mock_summary.percent_used = Decimal("85")

            mock_analyzer = MockAnalyzer.return_value
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("300")
            }

            result = server._handle_generate_report(
                file_path=str(test_file),
                format="markdown",
                include_recommendations=True,
            )

            assert result.is_error is False
            assert "Budget Report" in result.content[0]["text"]
            assert "## Recommendations" in result.content[0]["text"]

    def test_generate_report_text_format(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test text report format."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.report_generator.ReportGenerator"
        ) as MockReportGen:
            mock_gen = MockReportGen.return_value
            mock_gen.generate_text_report.return_value = "Budget Report Text"

            result = server._handle_generate_report(
                file_path=str(test_file),
                format="text",
                include_recommendations=False,
            )

            assert result.is_error is False
            assert "Budget Report Text" in result.content[0]["text"]

    def test_generate_recommendations_all_scenarios(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test _generate_recommendations with all logic paths."""
        from decimal import Decimal

        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"
        ) as MockAnalyzer:
            mock_analyzer = MockAnalyzer.return_value

            # Scenario 1: Over budget
            mock_summary = MagicMock()
            mock_summary.total_remaining = Decimal("-50")
            mock_summary.percent_used = Decimal("105")
            mock_analyzer.get_summary.return_value = mock_summary
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("200")
            }

            recommendations = server._generate_recommendations(test_file)
            assert any("over budget" in r.lower() for r in recommendations)

            # Scenario 2: High percentage (>80%)
            mock_summary.total_remaining = Decimal("50")
            mock_summary.percent_used = Decimal("85")

            recommendations = server._generate_recommendations(test_file)
            assert any("85" in r and "%" in r for r in recommendations)

            # Scenario 3: High category spending (>30%)
            mock_summary.percent_used = Decimal("50")
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("700"),
                "Transport": Decimal("100"),
                "Entertainment": Decimal("200"),
            }

            recommendations = server._generate_recommendations(test_file)
            assert any("Groceries" in r and "70.0%" in r for r in recommendations)

            # Scenario 4: All good
            mock_summary.percent_used = Decimal("50")
            mock_analyzer.get_category_breakdown.return_value = {
                "Groceries": Decimal("250"),
                "Transport": Decimal("250"),
                "Entertainment": Decimal("250"),
                "Utilities": Decimal("250"),
            }

            recommendations = server._generate_recommendations(test_file)
            assert any("on track" in r.lower() for r in recommendations)

    def test_generate_recommendations_exception_handling(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test _generate_recommendations handles exceptions."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with patch(
            "spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer",
            side_effect=Exception("Test error"),
        ):
            recommendations = server._generate_recommendations(test_file)
            assert recommendations == []

    def test_list_categories_handler(self, server: MCPServer) -> None:
        """Test list_categories handler."""
        result = server._handle_list_categories()

        assert result.is_error is False
        data = json.loads(result.content[0]["text"])
        assert "categories" in data
        assert len(data["categories"]) > 0
        assert all("name" in cat and "id" in cat for cat in data["categories"])

    def test_get_alerts_handler(self, server: MCPServer, tmp_path: Path) -> None:
        """Test get_alerts handler with severity filtering."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        with (
            patch("spreadsheet_dl.domains.finance.budget_analyzer.BudgetAnalyzer"),
            patch("spreadsheet_dl.domains.finance.alerts.AlertMonitor") as MockMonitor,
        ):
            mock_alert = MagicMock()
            mock_alert.message = "Over budget"
            mock_alert.category = "Groceries"
            mock_alert.severity.value = "critical"
            mock_alert.amount = 100
            mock_alert.threshold = 80

            mock_monitor = MockMonitor.return_value
            mock_monitor.check_all.return_value = [mock_alert]

            result = server._handle_get_alerts(
                file_path=str(test_file),
                severity="warning",
            )

            assert result.is_error is False
            data = json.loads(result.content[0]["text"])
            assert "total_alerts" in data
            assert "alerts" in data


class TestMCPServerGenerateReportFormats:
    """Tests for generate_report with different formats."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        """Create a test server."""
        config = MCPConfig(allowed_paths=[tmp_path, Path.cwd()])
        return MCPServer(config)

    def test_generate_report_json_format(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test generate_report with JSON format."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_generate_report(
            file_path=str(test_file),
            format="json",
            include_recommendations=True,
        )

        assert result is not None

    def test_generate_report_markdown_format(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test generate_report with markdown format."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_generate_report(
            file_path=str(test_file),
            format="markdown",
            include_recommendations=True,
        )

        assert result is not None

    def test_generate_report_text_format(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test generate_report with text format."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_generate_report(
            file_path=str(test_file),
            format="text",
            include_recommendations=False,
        )

        assert result is not None

    def test_generate_report_without_recommendations(
        self, server: MCPServer, tmp_path: Path
    ) -> None:
        """Test generate_report without recommendations."""
        test_file = tmp_path / "budget.ods"
        test_file.write_bytes(b"test")

        result = server._handle_generate_report(
            file_path=str(test_file),
            format="markdown",
            include_recommendations=False,
        )

        assert result is not None
