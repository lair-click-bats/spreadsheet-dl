"""
Comprehensive tests for financial statement templates.

Targets the financial_statements module which has very low coverage (12%).
"""

from __future__ import annotations

import pytest

from spreadsheet_dl.domains.finance.templates.financial_statements import (
    FINANCIAL_STATEMENT_TEMPLATES,
    BalanceSheetTemplate,
    CashFlowStatementTemplate,
    EquityStatementTemplate,
    IncomeStatementTemplate,
    get_financial_template,
    list_financial_templates,
)

pytestmark = [pytest.mark.unit, pytest.mark.finance]


class TestIncomeStatementTemplate:
    """Tests for IncomeStatementTemplate."""

    def test_create_income_statement_basic(self) -> None:
        """Test creating a basic income statement."""
        template = IncomeStatementTemplate()
        builder = template.generate()

        assert builder is not None
        # Verify the builder has sheets
        assert hasattr(builder, "_sheets")

    def test_create_income_statement_with_theme(self) -> None:
        """Test creating income statement with theme."""
        template = IncomeStatementTemplate(theme="corporate")
        builder = template.generate()

        assert builder is not None

    def test_create_income_statement_no_theme(self) -> None:
        """Test creating income statement without theme."""
        template = IncomeStatementTemplate(theme=None)
        builder = template.generate()

        assert builder is not None
        assert hasattr(builder, "_sheets")


class TestBalanceSheetTemplate:
    """Tests for BalanceSheetTemplate."""

    def test_create_balance_sheet_basic(self) -> None:
        """Test creating a basic balance sheet."""
        template = BalanceSheetTemplate()
        builder = template.generate()

        assert builder is not None
        assert hasattr(builder, "_sheets")

    def test_create_balance_sheet_with_theme(self) -> None:
        """Test creating balance sheet with theme."""
        template = BalanceSheetTemplate(theme="minimal")
        builder = template.generate()

        assert builder is not None

    def test_create_balance_sheet_no_theme(self) -> None:
        """Test creating balance sheet without theme."""
        template = BalanceSheetTemplate(theme=None)
        builder = template.generate()

        assert builder is not None


class TestCashFlowStatementTemplate:
    """Tests for CashFlowStatementTemplate."""

    def test_create_cash_flow_basic(self) -> None:
        """Test creating a basic cash flow statement."""
        template = CashFlowStatementTemplate()
        builder = template.generate()

        assert builder is not None
        assert hasattr(builder, "_sheets")

    def test_create_cash_flow_with_theme(self) -> None:
        """Test creating cash flow statement with theme."""
        template = CashFlowStatementTemplate(theme="dark")
        builder = template.generate()

        assert builder is not None

    def test_create_cash_flow_no_theme(self) -> None:
        """Test creating cash flow statement without theme."""
        template = CashFlowStatementTemplate(theme=None)
        builder = template.generate()

        assert builder is not None


class TestEquityStatementTemplate:
    """Tests for EquityStatementTemplate."""

    def test_create_equity_statement_basic(self) -> None:
        """Test creating a basic equity statement."""
        template = EquityStatementTemplate()
        builder = template.generate()

        assert builder is not None
        assert hasattr(builder, "_sheets")

    def test_create_equity_statement_with_theme(self) -> None:
        """Test creating equity statement with theme."""
        template = EquityStatementTemplate(theme="high_contrast")
        builder = template.generate()

        assert builder is not None

    def test_create_equity_statement_no_theme(self) -> None:
        """Test creating equity statement without theme."""
        template = EquityStatementTemplate(theme=None)
        builder = template.generate()

        assert builder is not None


class TestFinancialTemplatesRegistry:
    """Tests for financial template registry functions."""

    def test_list_financial_templates(self) -> None:
        """Test listing all financial templates."""
        templates = list_financial_templates()

        assert isinstance(templates, list)
        assert len(templates) > 0
        assert "income_statement" in templates
        assert "balance_sheet" in templates
        assert "cash_flow_statement" in templates
        assert "equity_statement" in templates

    def test_get_financial_template_income(self) -> None:
        """Test getting income statement template."""
        template_class = get_financial_template("income_statement")

        assert template_class is not None
        assert template_class == IncomeStatementTemplate

    def test_get_financial_template_balance(self) -> None:
        """Test getting balance sheet template."""
        template_class = get_financial_template("balance_sheet")

        assert template_class is not None
        assert template_class == BalanceSheetTemplate

    def test_get_financial_template_cash_flow(self) -> None:
        """Test getting cash flow template."""
        template_class = get_financial_template("cash_flow_statement")

        assert template_class is not None
        assert template_class == CashFlowStatementTemplate

    def test_get_financial_template_equity(self) -> None:
        """Test getting equity statement template."""
        template_class = get_financial_template("equity_statement")

        assert template_class is not None
        assert template_class == EquityStatementTemplate

    def test_get_financial_template_invalid(self) -> None:
        """Test getting invalid template returns None."""
        template_class = get_financial_template("nonexistent_template")

        assert template_class is None

    def test_financial_statement_templates_constant(self) -> None:
        """Test FINANCIAL_STATEMENT_TEMPLATES constant."""
        assert isinstance(FINANCIAL_STATEMENT_TEMPLATES, dict)
        assert len(FINANCIAL_STATEMENT_TEMPLATES) >= 4


class TestFinancialTemplatesIntegration:
    """Integration tests for all financial templates."""

    def test_all_templates_generate(self) -> None:
        """Test that all templates can generate builders."""
        templates = [
            IncomeStatementTemplate(),
            BalanceSheetTemplate(),
            CashFlowStatementTemplate(),
            EquityStatementTemplate(),
        ]

        for template in templates:
            builder = template.generate()
            assert builder is not None
            assert hasattr(builder, "_sheets")

    def test_templates_via_registry(self) -> None:
        """Test all templates via registry."""
        template_names = list_financial_templates()

        for name in template_names:
            template_class = get_financial_template(name)
            assert template_class is not None

            template = template_class()
            builder = template.generate()
            assert builder is not None
            assert hasattr(builder, "_sheets")

    def test_templates_with_themes(self) -> None:
        """Test all templates with different themes."""
        themes = ["default", "corporate", "minimal", "dark"]

        for theme in themes:
            income = IncomeStatementTemplate(theme=theme)
            balance = BalanceSheetTemplate(theme=theme)
            cash_flow = CashFlowStatementTemplate(theme=theme)
            equity = EquityStatementTemplate(theme=theme)

            assert income.generate() is not None
            assert balance.generate() is not None
            assert cash_flow.generate() is not None
            assert equity.generate() is not None

    def test_multiple_instances(self) -> None:
        """Test creating multiple instances of templates."""
        for _ in range(3):
            income = IncomeStatementTemplate()
            assert income.generate() is not None

        for _ in range(3):
            balance = BalanceSheetTemplate()
            assert balance.generate() is not None
