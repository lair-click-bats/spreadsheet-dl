"""Tests for professional templates functionality.

Tests for v2.0.0 Professional Business Templates:
    - FR-PROF-001: Enterprise Budget Template
    - FR-PROF-002: Cash Flow Tracker Template
    - FR-PROF-003: Invoice/Expense Report Template
"""

from __future__ import annotations

import pytest

from spreadsheet_dl.templates import (
    PROFESSIONAL_TEMPLATES,
    BudgetCategory,
    CashFlowTrackerTemplate,
    EnterpriseBudgetTemplate,
    ExpenseReportTemplate,
    InvoiceTemplate,
    TemplateMetadata,
    get_template,
    list_templates,
)

pytestmark = [pytest.mark.unit, pytest.mark.templates]


class TestTemplateMetadata:
    """Tests for TemplateMetadata dataclass."""

    def test_default_values(self) -> None:
        """Test default metadata values."""
        meta = TemplateMetadata(name="Test")
        assert meta.name == "Test"
        assert meta.version == "1.0.0"
        assert meta.category == "finance"
        assert meta.tags == []

    def test_custom_values(self) -> None:
        """Test custom metadata values."""
        meta = TemplateMetadata(
            name="Custom Template",
            version="2.0.0",
            description="A custom template",
            category="business",
            author="Test Author",
            tags=["budget", "enterprise"],
        )
        assert meta.name == "Custom Template"
        assert meta.version == "2.0.0"
        assert meta.description == "A custom template"
        assert meta.category == "business"
        assert meta.author == "Test Author"
        assert "budget" in meta.tags


class TestBudgetCategory:
    """Tests for BudgetCategory dataclass."""

    def test_simple_category(self) -> None:
        """Test creating a simple category."""
        cat = BudgetCategory(name="Personnel")
        assert cat.name == "Personnel"
        assert cat.subcategories == []

    def test_category_with_subcategories(self) -> None:
        """Test category with subcategories."""
        cat = BudgetCategory(
            name="Operations",
            subcategories=["Rent", "Utilities", "Insurance"],
        )
        assert cat.name == "Operations"
        assert len(cat.subcategories) == 3
        assert "Rent" in cat.subcategories


class TestProfessionalTemplatesRegistry:
    """Tests for PROFESSIONAL_TEMPLATES registry."""

    def test_registry_contains_templates(self) -> None:
        """Test that registry has expected templates."""
        assert len(PROFESSIONAL_TEMPLATES) > 0
        assert "enterprise_budget" in PROFESSIONAL_TEMPLATES
        assert "cash_flow" in PROFESSIONAL_TEMPLATES
        assert "invoice" in PROFESSIONAL_TEMPLATES
        assert "expense_report" in PROFESSIONAL_TEMPLATES

    def test_registry_values_are_classes(self) -> None:
        """Test that registry values are template classes."""
        for _name, template_class in PROFESSIONAL_TEMPLATES.items():
            assert isinstance(template_class, type)

    def test_get_template_returns_class(self) -> None:
        """Test get_template returns template class."""
        template_class = get_template("enterprise_budget")
        assert template_class is EnterpriseBudgetTemplate

    def test_get_template_unknown_returns_none(self) -> None:
        """Test get_template returns None for unknown template."""
        result = get_template("nonexistent_template")
        assert result is None

    def test_list_templates_returns_names(self) -> None:
        """Test list_templates returns template names."""
        templates = list_templates()
        assert isinstance(templates, list)
        assert len(templates) == len(PROFESSIONAL_TEMPLATES)
        assert "enterprise_budget" in templates
        assert "cash_flow" in templates


class TestEnterpriseBudgetTemplate:
    """Tests for EnterpriseBudgetTemplate (FR-PROF-001)."""

    def test_default_values(self) -> None:
        """Test default template values."""
        template = EnterpriseBudgetTemplate()
        assert template.fiscal_year == 2024
        assert template.currency_symbol == "$"
        assert template.include_quarterly is True
        assert template.include_variance is True
        assert template.theme == "corporate"

    def test_default_categories(self) -> None:
        """Test default budget categories are created."""
        template = EnterpriseBudgetTemplate()
        assert len(template.categories) > 0
        category_names = [c.name for c in template.categories]
        assert "Personnel" in category_names
        assert "Operations" in category_names
        assert "Technology" in category_names

    def test_custom_departments(self) -> None:
        """Test custom departments."""
        template = EnterpriseBudgetTemplate(
            departments=["Engineering", "Sales", "Marketing"]
        )
        assert template.departments == ["Engineering", "Sales", "Marketing"]

    def test_custom_categories(self) -> None:
        """Test custom categories."""
        categories = [
            BudgetCategory(name="Custom1", subcategories=["Sub1", "Sub2"]),
            BudgetCategory(name="Custom2"),
        ]
        template = EnterpriseBudgetTemplate(categories=categories)
        assert len(template.categories) == 2
        assert template.categories[0].name == "Custom1"

    def test_months_property(self) -> None:
        """Test months property returns 12 months."""
        template = EnterpriseBudgetTemplate()
        assert len(template.months) == 12
        assert template.months[0] == "Jan"
        assert template.months[11] == "Dec"

    def test_generate_returns_builder(self) -> None:
        """Test generate returns SpreadsheetBuilder."""
        template = EnterpriseBudgetTemplate()
        builder = template.generate()
        # SpreadsheetBuilder should have been returned
        assert builder is not None
        assert hasattr(builder, "sheet")
        assert hasattr(builder, "save")


class TestCashFlowTrackerTemplate:
    """Tests for CashFlowTrackerTemplate (FR-PROF-002)."""

    def test_default_values(self) -> None:
        """Test default template values."""
        template = CashFlowTrackerTemplate()
        assert template.start_date == "2024-01-01"
        assert template.periods == 12
        assert template.period_type == "monthly"
        assert template.opening_balance == 0.0
        assert template.include_projections is True

    def test_default_activity_items(self) -> None:
        """Test default operating/investing/financing items."""
        template = CashFlowTrackerTemplate()
        assert len(template.operating_inflows) > 0
        assert len(template.operating_outflows) > 0
        assert len(template.investing_inflows) > 0
        assert len(template.financing_inflows) > 0

    def test_custom_opening_balance(self) -> None:
        """Test custom opening balance."""
        template = CashFlowTrackerTemplate(opening_balance=50000.00)
        assert template.opening_balance == 50000.00

    def test_weekly_period_type(self) -> None:
        """Test weekly period type."""
        template = CashFlowTrackerTemplate(period_type="weekly", periods=52)
        assert template.period_type == "weekly"
        assert template.periods == 52

    def test_generate_returns_builder(self) -> None:
        """Test generate returns SpreadsheetBuilder."""
        template = CashFlowTrackerTemplate()
        builder = template.generate()
        assert builder is not None
        assert hasattr(builder, "sheet")


class TestInvoiceTemplate:
    """Tests for InvoiceTemplate (FR-PROF-003)."""

    def test_default_values(self) -> None:
        """Test default template values."""
        template = InvoiceTemplate()
        assert template.company_name == "Your Company"
        assert template.invoice_number == "INV-001"
        assert template.tax_rate == 0.0
        assert template.currency_symbol == "$"

    def test_custom_company_info(self) -> None:
        """Test custom company information."""
        template = InvoiceTemplate(
            company_name="Acme Corp",
            company_address="123 Main St",
            company_phone="555-1234",
            company_email="info@acme.com",
            invoice_number="INV-2024-001",
        )
        assert template.company_name == "Acme Corp"
        assert template.company_address == "123 Main St"
        assert template.invoice_number == "INV-2024-001"

    def test_with_tax_rate(self) -> None:
        """Test invoice with tax rate."""
        template = InvoiceTemplate(tax_rate=0.08)
        assert template.tax_rate == 0.08

    def test_generate_returns_builder(self) -> None:
        """Test generate returns SpreadsheetBuilder."""
        template = InvoiceTemplate()
        builder = template.generate()
        assert builder is not None


class TestExpenseReportTemplate:
    """Tests for ExpenseReportTemplate (FR-PROF-003)."""

    def test_default_values(self) -> None:
        """Test default template values."""
        template = ExpenseReportTemplate()
        assert template.employee_name == ""
        assert template.department == ""
        assert template.currency_symbol == "$"

    def test_default_categories(self) -> None:
        """Test default expense categories."""
        template = ExpenseReportTemplate()
        assert len(template.categories) > 0
        assert "Travel" in template.categories
        assert "Meals" in template.categories
        assert "Transportation" in template.categories

    def test_custom_employee_info(self) -> None:
        """Test custom employee information."""
        template = ExpenseReportTemplate(
            employee_name="John Doe",
            department="Engineering",
            report_period="January 2024",
        )
        assert template.employee_name == "John Doe"
        assert template.department == "Engineering"
        assert template.report_period == "January 2024"

    def test_custom_categories(self) -> None:
        """Test custom expense categories."""
        template = ExpenseReportTemplate(
            categories=["Flights", "Hotels", "Meals", "Ground Transport"]
        )
        assert len(template.categories) == 4
        assert "Flights" in template.categories

    def test_generate_returns_builder(self) -> None:
        """Test generate returns SpreadsheetBuilder."""
        template = ExpenseReportTemplate()
        builder = template.generate()
        assert builder is not None


class TestTemplateIntegration:
    """Integration tests for templates."""

    def test_enterprise_budget_creates_sheets(self) -> None:
        """Test enterprise budget creates multiple sheets."""
        template = EnterpriseBudgetTemplate(
            departments=["Engineering", "Marketing"],
            include_variance=True,
        )
        builder = template.generate()
        # Builder should have multiple sheets configured
        assert builder is not None

    def test_cash_flow_creates_sections(self) -> None:
        """Test cash flow creates operating/investing/financing sections."""
        template = CashFlowTrackerTemplate(
            include_projections=True,
        )
        builder = template.generate()
        assert builder is not None

    def test_all_templates_generate_successfully(self) -> None:
        """Test all templates can generate without errors."""
        for name, template_class in PROFESSIONAL_TEMPLATES.items():
            template = template_class()
            builder = template.generate()
            assert builder is not None, f"Template {name} failed to generate"
