"""
Tests for professional templates.

Tests FR-PROF-001, FR-PROF-002, FR-PROF-003
"""

import pytest

from spreadsheet_dl.templates.professional import (
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


class TestTemplateMetadata:
    """Tests for TemplateMetadata."""

    def test_basic_metadata(self):
        """Test basic metadata creation."""
        meta = TemplateMetadata(
            name="test-template",
            version="1.0.0",
            description="Test template",
        )
        assert meta.name == "test-template"
        assert meta.version == "1.0.0"
        assert meta.category == "finance"

    def test_metadata_with_tags(self):
        """Test metadata with tags."""
        meta = TemplateMetadata(
            name="budget",
            tags=["budget", "finance", "annual"],
        )
        assert "budget" in meta.tags
        assert len(meta.tags) == 3


class TestBudgetCategory:
    """Tests for BudgetCategory."""

    def test_basic_category(self):
        """Test basic category."""
        category = BudgetCategory(name="Personnel")
        assert category.name == "Personnel"
        assert category.subcategories == []

    def test_category_with_subcategories(self):
        """Test category with subcategories."""
        category = BudgetCategory(
            name="Personnel",
            subcategories=["Salaries", "Benefits", "Training"],
        )
        assert len(category.subcategories) == 3
        assert "Salaries" in category.subcategories


class TestEnterpriseBudgetTemplate:
    """Tests for EnterpriseBudgetTemplate (FR-PROF-001)."""

    def test_default_initialization(self):
        """Test default initialization."""
        template = EnterpriseBudgetTemplate()
        assert template.fiscal_year == 2024
        assert len(template.departments) == 1
        assert template.departments[0] == "General"
        assert template.currency_symbol == "$"

    def test_custom_fiscal_year(self):
        """Test custom fiscal year."""
        template = EnterpriseBudgetTemplate(fiscal_year=2025)
        assert template.fiscal_year == 2025

    def test_custom_departments(self):
        """Test custom departments."""
        template = EnterpriseBudgetTemplate(
            departments=["Engineering", "Sales", "Marketing"]
        )
        assert len(template.departments) == 3
        assert "Engineering" in template.departments

    def test_default_categories(self):
        """Test default categories are created."""
        template = EnterpriseBudgetTemplate()
        assert len(template.categories) > 0
        category_names = [c.name for c in template.categories]
        assert "Personnel" in category_names
        assert "Operations" in category_names

    def test_custom_categories(self):
        """Test custom categories."""
        template = EnterpriseBudgetTemplate(
            categories=[
                BudgetCategory("Custom1", ["A", "B"]),
                BudgetCategory("Custom2", ["C", "D"]),
            ]
        )
        assert len(template.categories) == 2
        assert template.categories[0].name == "Custom1"

    def test_months_property(self):
        """Test months property."""
        template = EnterpriseBudgetTemplate()
        months = template.months
        assert len(months) == 12
        assert months[0] == "Jan"
        assert months[11] == "Dec"

    def test_include_quarterly_flag(self):
        """Test include_quarterly flag."""
        template = EnterpriseBudgetTemplate(include_quarterly=True)
        assert template.include_quarterly is True

    def test_include_variance_flag(self):
        """Test include_variance flag."""
        template = EnterpriseBudgetTemplate(include_variance=True)
        assert template.include_variance is True


class TestCashFlowTrackerTemplate:
    """Tests for CashFlowTrackerTemplate (FR-PROF-002)."""

    def test_default_initialization(self):
        """Test default initialization."""
        template = CashFlowTrackerTemplate()
        assert template.periods == 12
        assert template.period_type == "monthly"
        assert template.opening_balance == 0.0

    def test_custom_start_date(self):
        """Test custom start date."""
        template = CashFlowTrackerTemplate(start_date="2025-01-01")
        assert template.start_date == "2025-01-01"

    def test_weekly_periods(self):
        """Test weekly period type."""
        template = CashFlowTrackerTemplate(
            period_type="weekly",
            periods=52,
        )
        assert template.period_type == "weekly"
        assert template.periods == 52

    def test_opening_balance(self):
        """Test opening balance."""
        template = CashFlowTrackerTemplate(opening_balance=50000.00)
        assert template.opening_balance == 50000.00

    def test_default_operating_inflows(self):
        """Test default operating inflows."""
        template = CashFlowTrackerTemplate()
        assert "Sales Revenue" in template.operating_inflows

    def test_default_operating_outflows(self):
        """Test default operating outflows."""
        template = CashFlowTrackerTemplate()
        assert "Payroll" in template.operating_outflows
        assert "Rent/Lease" in template.operating_outflows

    def test_default_investing_activities(self):
        """Test default investing activities."""
        template = CashFlowTrackerTemplate()
        assert "Asset Sales" in template.investing_inflows
        assert "Equipment Purchases" in template.investing_outflows

    def test_default_financing_activities(self):
        """Test default financing activities."""
        template = CashFlowTrackerTemplate()
        assert "Loan Proceeds" in template.financing_inflows
        assert "Loan Payments" in template.financing_outflows

    def test_include_projections(self):
        """Test include projections flag."""
        template = CashFlowTrackerTemplate(include_projections=True)
        assert template.include_projections is True


class TestInvoiceTemplate:
    """Tests for InvoiceTemplate (FR-PROF-003)."""

    def test_default_initialization(self):
        """Test default initialization."""
        template = InvoiceTemplate()
        assert template.company_name == "Your Company"
        assert template.invoice_number == "INV-001"

    def test_custom_company_info(self):
        """Test custom company information."""
        template = InvoiceTemplate(
            company_name="ACME Corp",
            company_address="123 Main St",
            company_phone="555-1234",
            company_email="info@acme.com",
        )
        assert template.company_name == "ACME Corp"
        assert template.company_address == "123 Main St"

    def test_custom_invoice_number(self):
        """Test custom invoice number."""
        template = InvoiceTemplate(invoice_number="INV-2024-001")
        assert template.invoice_number == "INV-2024-001"

    def test_tax_rate(self):
        """Test tax rate."""
        template = InvoiceTemplate(tax_rate=0.08)
        assert template.tax_rate == 0.08


class TestExpenseReportTemplate:
    """Tests for ExpenseReportTemplate."""

    def test_default_initialization(self):
        """Test default initialization."""
        template = ExpenseReportTemplate()
        assert template.employee_name == ""
        assert template.department == ""

    def test_custom_employee_info(self):
        """Test custom employee information."""
        template = ExpenseReportTemplate(
            employee_name="John Doe",
            department="Engineering",
        )
        assert template.employee_name == "John Doe"
        assert template.department == "Engineering"

    def test_default_categories(self):
        """Test default expense categories."""
        template = ExpenseReportTemplate()
        assert "Travel" in template.categories
        assert "Meals" in template.categories
        assert "Lodging" in template.categories

    def test_custom_categories(self):
        """Test custom expense categories."""
        template = ExpenseReportTemplate(
            categories=["Travel", "Supplies", "Software"]
        )
        assert len(template.categories) == 3
        assert "Software" in template.categories


class TestTemplateRegistry:
    """Tests for template registry."""

    def test_list_templates(self):
        """Test listing available templates."""
        templates = list_templates()
        assert "enterprise_budget" in templates
        assert "cash_flow" in templates
        assert "invoice" in templates
        assert "expense_report" in templates

    def test_get_template(self):
        """Test getting template by name."""
        template_class = get_template("enterprise_budget")
        assert template_class is EnterpriseBudgetTemplate

    def test_get_nonexistent_template(self):
        """Test getting nonexistent template."""
        template_class = get_template("nonexistent")
        assert template_class is None

    def test_professional_templates_dict(self):
        """Test PROFESSIONAL_TEMPLATES dictionary."""
        assert len(PROFESSIONAL_TEMPLATES) >= 4
        assert "enterprise_budget" in PROFESSIONAL_TEMPLATES
        assert "cash_flow" in PROFESSIONAL_TEMPLATES


class TestTemplateIntegration:
    """Integration tests for templates with builder."""

    @pytest.mark.skip(reason="Requires full builder implementation")
    def test_enterprise_budget_generate(self):
        """Test generating enterprise budget spreadsheet."""
        template = EnterpriseBudgetTemplate(
            fiscal_year=2024,
            departments=["Engineering"],
        )
        template.generate()
        # Would verify builder state

    @pytest.mark.skip(reason="Requires full builder implementation")
    def test_cash_flow_generate(self):
        """Test generating cash flow spreadsheet."""
        template = CashFlowTrackerTemplate(
            start_date="2024-01-01",
            periods=12,
            opening_balance=10000,
        )
        template.generate()
        # Would verify builder state

    @pytest.mark.skip(reason="Requires full builder implementation")
    def test_invoice_generate(self):
        """Test generating invoice spreadsheet."""
        template = InvoiceTemplate(
            company_name="Test Corp",
            invoice_number="INV-100",
        )
        template.generate()
        # Would verify builder state
