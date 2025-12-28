"""Tests for budget templates functionality."""

from __future__ import annotations

from decimal import Decimal

import pytest

from finance_tracker.templates import (
    BUDGET_TEMPLATES,
    create_custom_template,
    get_template,
    list_templates,
)


class TestBudgetTemplate:
    """Tests for BudgetTemplate dataclass."""

    def test_total_budget(self) -> None:
        """Test calculating total budget."""
        template = get_template("50_30_20")
        total = template.total_budget

        assert total > 0
        # Should equal sum of allocations
        expected = sum(a.monthly_budget for a in template.allocations)
        assert total == expected

    def test_to_dict(self) -> None:
        """Test converting template to dictionary."""
        template = get_template("family")
        data = template.to_dict()

        assert "name" in data
        assert "allocations" in data
        assert "total_budget" in data
        assert len(data["allocations"]) == len(template.allocations)

    def test_scale_to_income(self) -> None:
        """Test scaling template to specific income."""
        template = get_template("50_30_20")
        scaled = template.scale_to_income(Decimal("5000"))

        # Total should be close to income
        total = sum(a.monthly_budget for a in scaled)
        assert abs(total - Decimal("5000")) < Decimal("100")


class TestGetTemplate:
    """Tests for get_template function."""

    def test_get_existing_template(self) -> None:
        """Test getting an existing template."""
        template = get_template("50_30_20")
        assert template.name == "50/30/20 Rule"
        assert len(template.allocations) > 0

    def test_get_all_templates(self) -> None:
        """Test that all defined templates can be retrieved."""
        for name in BUDGET_TEMPLATES:
            template = get_template(name)
            assert template is not None

    def test_invalid_template(self) -> None:
        """Test that invalid template raises error."""
        with pytest.raises(ValueError):
            get_template("nonexistent_template")


class TestListTemplates:
    """Tests for list_templates function."""

    def test_list_templates(self) -> None:
        """Test listing all templates."""
        templates = list_templates()

        assert len(templates) > 0
        assert all("name" in t for t in templates)
        assert all("display_name" in t for t in templates)
        assert all("total_budget" in t for t in templates)

    def test_template_info_complete(self) -> None:
        """Test that template info is complete."""
        templates = list_templates()

        for t in templates:
            assert t["name"] in BUDGET_TEMPLATES
            assert t["description"] != ""


class TestPredefinedTemplates:
    """Tests for predefined budget templates."""

    def test_50_30_20_template(self) -> None:
        """Test 50/30/20 rule template."""
        template = get_template("50_30_20")

        assert template.name == "50/30/20 Rule"
        assert len(template.allocations) >= 10
        assert len(template.notes) > 0
        assert "Beginners" in template.recommended_for

    def test_family_template(self) -> None:
        """Test family template."""
        template = get_template("family")

        assert "Family" in template.name
        # Family budget should be higher
        assert template.total_budget > Decimal("4000")

    def test_minimalist_template(self) -> None:
        """Test minimalist template."""
        template = get_template("minimalist")

        assert "Minimalist" in template.name
        # Should have high savings rate
        savings = next(
            (a for a in template.allocations if a.category.value == "Savings"), None
        )
        assert savings is not None
        assert savings.monthly_budget > Decimal("500")

    def test_fire_template(self) -> None:
        """Test FIRE template."""
        template = get_template("fire")

        assert "FIRE" in template.name
        # FIRE should have very high savings
        savings = next(
            (a for a in template.allocations if a.category.value == "Savings"), None
        )
        assert savings is not None
        # Savings should be largest category
        max_alloc = max(template.allocations, key=lambda a: a.monthly_budget)
        assert max_alloc.category.value == "Savings"

    def test_high_income_template(self) -> None:
        """Test high income template."""
        template = get_template("high_income")

        assert "High Income" in template.name
        # Should have larger total budget
        assert template.total_budget > Decimal("10000")


class TestCreateCustomTemplate:
    """Tests for create_custom_template function."""

    def test_create_custom(self) -> None:
        """Test creating a custom template."""
        template = create_custom_template(
            name="My Budget",
            description="Custom budget",
            monthly_income=Decimal("6000"),
            savings_rate=25.0,
            housing_percent=25.0,
        )

        assert template.name == "My Budget"
        assert len(template.allocations) > 0

        # Check savings allocation
        savings = next(
            (a for a in template.allocations if a.category.value == "Savings"), None
        )
        assert savings is not None
        # 25% of $6000 = $1500
        assert abs(savings.monthly_budget - Decimal("1500")) < Decimal("10")

        # Check housing allocation
        housing = next(
            (a for a in template.allocations if a.category.value == "Housing"), None
        )
        assert housing is not None
        # 25% of $6000 = $1500
        assert abs(housing.monthly_budget - Decimal("1500")) < Decimal("10")

    def test_custom_template_total(self) -> None:
        """Test that custom template totals correctly."""
        income = Decimal("5000")
        template = create_custom_template(
            name="Test",
            description="Test",
            monthly_income=income,
        )

        # Total should be close to income
        total = template.total_budget
        assert abs(total - income) < Decimal("100")

    def test_custom_template_notes(self) -> None:
        """Test that custom template has appropriate notes."""
        template = create_custom_template(
            name="Test",
            description="Test",
            monthly_income=Decimal("5000"),
            savings_rate=30.0,
        )

        assert len(template.notes) > 0
        assert any("30%" in note for note in template.notes)
