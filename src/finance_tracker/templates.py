"""
Budget Templates - Pre-configured budget templates for different scenarios.

Provides ready-to-use budget templates for various household types
and financial situations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

from finance_tracker.ods_generator import BudgetAllocation, ExpenseCategory


@dataclass
class BudgetTemplate:
    """Budget template definition."""

    name: str
    description: str
    allocations: list[BudgetAllocation]
    # Target percentages of income (for scaling)
    income_percentages: dict[str, float] = field(default_factory=dict)
    # Notes and tips
    notes: list[str] = field(default_factory=list)
    # Recommended for
    recommended_for: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert template to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "allocations": [
                {
                    "category": a.category.value,
                    "amount": str(a.monthly_budget),
                    "notes": a.notes,
                }
                for a in self.allocations
            ],
            "income_percentages": self.income_percentages,
            "notes": self.notes,
            "recommended_for": self.recommended_for,
            "total_budget": str(self.total_budget),
        }

    @property
    def total_budget(self) -> Decimal:
        """Calculate total budget from allocations."""
        return sum((a.monthly_budget for a in self.allocations), Decimal("0"))

    def scale_to_income(self, monthly_income: Decimal) -> list[BudgetAllocation]:
        """
        Scale allocations to a specific monthly income.

        Args:
            monthly_income: Target monthly income.

        Returns:
            Scaled list of BudgetAllocation.
        """
        if not self.income_percentages:
            # Scale proportionally
            current_total = self.total_budget
            if current_total == 0:
                return self.allocations.copy()

            scale = monthly_income / current_total
            return [
                BudgetAllocation(
                    category=a.category,
                    monthly_budget=(a.monthly_budget * scale).quantize(Decimal("1")),
                    notes=a.notes,
                )
                for a in self.allocations
            ]

        # Use percentage-based scaling
        return [
            BudgetAllocation(
                category=a.category,
                monthly_budget=(
                    monthly_income
                    * Decimal(
                        str(self.income_percentages.get(a.category.value, 0) / 100)
                    )
                ).quantize(Decimal("1")),
                notes=a.notes,
            )
            for a in self.allocations
        ]


# ============================================================================
# Pre-built Budget Templates
# ============================================================================

TEMPLATE_50_30_20 = BudgetTemplate(
    name="50/30/20 Rule",
    description="Classic budgeting rule: 50% needs, 30% wants, 20% savings/debt",
    allocations=[
        # Needs (50%)
        BudgetAllocation(
            ExpenseCategory.HOUSING, Decimal("1500"), "Rent/mortgage - keep under 30%"
        ),
        BudgetAllocation(
            ExpenseCategory.UTILITIES, Decimal("200"), "Electric, water, gas"
        ),
        BudgetAllocation(ExpenseCategory.GROCERIES, Decimal("400"), "Food for home"),
        BudgetAllocation(
            ExpenseCategory.TRANSPORTATION, Decimal("300"), "Gas, maintenance, transit"
        ),
        BudgetAllocation(
            ExpenseCategory.HEALTHCARE, Decimal("150"), "Insurance, copays"
        ),
        BudgetAllocation(ExpenseCategory.INSURANCE, Decimal("200"), "Auto, life, etc."),
        # Wants (30%)
        BudgetAllocation(
            ExpenseCategory.ENTERTAINMENT, Decimal("200"), "Movies, hobbies"
        ),
        BudgetAllocation(
            ExpenseCategory.DINING_OUT, Decimal("250"), "Restaurants, takeout"
        ),
        BudgetAllocation(
            ExpenseCategory.CLOTHING, Decimal("100"), "Non-essential clothing"
        ),
        BudgetAllocation(ExpenseCategory.PERSONAL, Decimal("100"), "Self-care"),
        BudgetAllocation(
            ExpenseCategory.SUBSCRIPTIONS, Decimal("100"), "Streaming, apps"
        ),
        BudgetAllocation(ExpenseCategory.GIFTS, Decimal("50"), "Presents"),
        BudgetAllocation(ExpenseCategory.MISCELLANEOUS, Decimal("100"), "Buffer"),
        # Savings/Debt (20%)
        BudgetAllocation(
            ExpenseCategory.SAVINGS, Decimal("600"), "Emergency fund, retirement"
        ),
        BudgetAllocation(
            ExpenseCategory.DEBT_PAYMENT, Decimal("400"), "Extra debt payments"
        ),
        BudgetAllocation(ExpenseCategory.EDUCATION, Decimal("50"), "Learning, courses"),
    ],
    income_percentages={
        "Housing": 30,
        "Utilities": 4,
        "Groceries": 8,
        "Transportation": 6,
        "Healthcare": 3,
        "Insurance": 4,
        "Entertainment": 4,
        "Dining Out": 5,
        "Clothing": 2,
        "Personal Care": 2,
        "Subscriptions": 2,
        "Gifts": 1,
        "Miscellaneous": 2,
        "Savings": 13,
        "Debt Payment": 13,
        "Education": 1,
    },
    notes=[
        "Needs (housing, utilities, groceries, transport, healthcare) = 50%",
        "Wants (entertainment, dining, clothing, subscriptions) = 30%",
        "Savings and debt repayment = 20%",
        "Adjust housing down if possible to boost savings",
    ],
    recommended_for=["Beginners", "Single income", "Debt payoff focus"],
)

TEMPLATE_FAMILY_OF_FOUR = BudgetTemplate(
    name="Family of Four",
    description="Budget optimized for a family with two children",
    allocations=[
        BudgetAllocation(
            ExpenseCategory.HOUSING, Decimal("2200"), "Larger home for family"
        ),
        BudgetAllocation(ExpenseCategory.UTILITIES, Decimal("300"), "Higher usage"),
        BudgetAllocation(ExpenseCategory.GROCERIES, Decimal("800"), "4 people"),
        BudgetAllocation(
            ExpenseCategory.TRANSPORTATION, Decimal("500"), "Larger vehicle, more trips"
        ),
        BudgetAllocation(
            ExpenseCategory.HEALTHCARE, Decimal("300"), "Family health insurance"
        ),
        BudgetAllocation(
            ExpenseCategory.INSURANCE, Decimal("400"), "Life insurance important"
        ),
        BudgetAllocation(
            ExpenseCategory.ENTERTAINMENT, Decimal("200"), "Family activities"
        ),
        BudgetAllocation(
            ExpenseCategory.DINING_OUT, Decimal("250"), "Occasional family dinners"
        ),
        BudgetAllocation(ExpenseCategory.CLOTHING, Decimal("200"), "Kids grow fast"),
        BudgetAllocation(ExpenseCategory.PERSONAL, Decimal("100"), "Self-care"),
        BudgetAllocation(
            ExpenseCategory.EDUCATION, Decimal("200"), "School supplies, activities"
        ),
        BudgetAllocation(
            ExpenseCategory.SAVINGS, Decimal("800"), "Emergency + college fund"
        ),
        BudgetAllocation(
            ExpenseCategory.DEBT_PAYMENT, Decimal("400"), "Mortgage/loans"
        ),
        BudgetAllocation(
            ExpenseCategory.GIFTS, Decimal("150"), "Birthday parties, holidays"
        ),
        BudgetAllocation(ExpenseCategory.SUBSCRIPTIONS, Decimal("100"), "Family plans"),
        BudgetAllocation(
            ExpenseCategory.MISCELLANEOUS, Decimal("100"), "Unexpected kid expenses"
        ),
    ],
    notes=[
        "Account for school expenses in Education",
        "Kids clothing grows fast - buy slightly ahead",
        "Family activities can be free (parks, libraries)",
        "Consider term life insurance for parents",
    ],
    recommended_for=["Families with children", "Dual income households"],
)

TEMPLATE_SINGLE_MINIMALIST = BudgetTemplate(
    name="Single Minimalist",
    description="Lean budget for single person focused on savings",
    allocations=[
        BudgetAllocation(
            ExpenseCategory.HOUSING, Decimal("1200"), "Studio/1BR or roommate"
        ),
        BudgetAllocation(ExpenseCategory.UTILITIES, Decimal("100"), "Low usage"),
        BudgetAllocation(
            ExpenseCategory.GROCERIES, Decimal("300"), "Meal prep focused"
        ),
        BudgetAllocation(
            ExpenseCategory.TRANSPORTATION, Decimal("150"), "Public transit or bike"
        ),
        BudgetAllocation(ExpenseCategory.HEALTHCARE, Decimal("100"), "Basic coverage"),
        BudgetAllocation(ExpenseCategory.INSURANCE, Decimal("100"), "Renters + basic"),
        BudgetAllocation(
            ExpenseCategory.ENTERTAINMENT, Decimal("100"), "Free/low-cost activities"
        ),
        BudgetAllocation(
            ExpenseCategory.DINING_OUT, Decimal("100"), "Occasional treat"
        ),
        BudgetAllocation(ExpenseCategory.CLOTHING, Decimal("50"), "Capsule wardrobe"),
        BudgetAllocation(ExpenseCategory.PERSONAL, Decimal("50"), "Minimal"),
        BudgetAllocation(ExpenseCategory.EDUCATION, Decimal("100"), "Self-improvement"),
        BudgetAllocation(ExpenseCategory.SAVINGS, Decimal("700"), "High savings rate"),
        BudgetAllocation(
            ExpenseCategory.DEBT_PAYMENT, Decimal("200"), "Aggressive payoff"
        ),
        BudgetAllocation(
            ExpenseCategory.GIFTS, Decimal("30"), "Thoughtful, not expensive"
        ),
        BudgetAllocation(
            ExpenseCategory.SUBSCRIPTIONS, Decimal("50"), "Essential only"
        ),
        BudgetAllocation(ExpenseCategory.MISCELLANEOUS, Decimal("50"), "Buffer"),
    ],
    notes=[
        "Prioritize savings rate over lifestyle",
        "Use library for books, entertainment",
        "Meal prep to reduce food costs",
        "Consider biking or public transit",
    ],
    recommended_for=["Single person", "FIRE aspirants", "Debt elimination"],
)

TEMPLATE_ZERO_BASED = BudgetTemplate(
    name="Zero-Based Budget",
    description="Every dollar has a purpose - income minus expenses equals zero",
    allocations=[
        BudgetAllocation(ExpenseCategory.HOUSING, Decimal("1500"), "Shelter"),
        BudgetAllocation(ExpenseCategory.UTILITIES, Decimal("200"), "Basic services"),
        BudgetAllocation(ExpenseCategory.GROCERIES, Decimal("500"), "Food"),
        BudgetAllocation(
            ExpenseCategory.TRANSPORTATION, Decimal("350"), "Getting around"
        ),
        BudgetAllocation(ExpenseCategory.HEALTHCARE, Decimal("200"), "Health costs"),
        BudgetAllocation(ExpenseCategory.INSURANCE, Decimal("250"), "Protection"),
        BudgetAllocation(ExpenseCategory.ENTERTAINMENT, Decimal("150"), "Fun money"),
        BudgetAllocation(ExpenseCategory.DINING_OUT, Decimal("200"), "Eating out"),
        BudgetAllocation(ExpenseCategory.CLOTHING, Decimal("100"), "Clothes"),
        BudgetAllocation(ExpenseCategory.PERSONAL, Decimal("75"), "Personal care"),
        BudgetAllocation(ExpenseCategory.EDUCATION, Decimal("75"), "Learning"),
        BudgetAllocation(ExpenseCategory.SAVINGS, Decimal("600"), "Save first"),
        BudgetAllocation(ExpenseCategory.DEBT_PAYMENT, Decimal("300"), "Debt snowball"),
        BudgetAllocation(ExpenseCategory.GIFTS, Decimal("75"), "Giving"),
        BudgetAllocation(ExpenseCategory.SUBSCRIPTIONS, Decimal("75"), "Subscriptions"),
        BudgetAllocation(ExpenseCategory.MISCELLANEOUS, Decimal("100"), "Catch-all"),
    ],
    notes=[
        "Assign every dollar before the month starts",
        "Income - All expenses = $0",
        "Move unused funds to savings",
        "Review and adjust weekly",
    ],
    recommended_for=["Detail-oriented", "Dave Ramsey followers", "Tight budgets"],
)

TEMPLATE_FIRE = BudgetTemplate(
    name="FIRE (Financial Independence)",
    description="Extreme savings rate for early retirement",
    allocations=[
        BudgetAllocation(
            ExpenseCategory.HOUSING, Decimal("1000"), "House hacking or very low"
        ),
        BudgetAllocation(ExpenseCategory.UTILITIES, Decimal("100"), "Minimal usage"),
        BudgetAllocation(
            ExpenseCategory.GROCERIES, Decimal("250"), "Efficient meal planning"
        ),
        BudgetAllocation(
            ExpenseCategory.TRANSPORTATION, Decimal("100"), "Bike/walk when possible"
        ),
        BudgetAllocation(
            ExpenseCategory.HEALTHCARE, Decimal("150"), "High deductible + HSA"
        ),
        BudgetAllocation(ExpenseCategory.INSURANCE, Decimal("100"), "Essential only"),
        BudgetAllocation(
            ExpenseCategory.ENTERTAINMENT, Decimal("50"), "Free activities"
        ),
        BudgetAllocation(ExpenseCategory.DINING_OUT, Decimal("50"), "Rare treat"),
        BudgetAllocation(ExpenseCategory.CLOTHING, Decimal("30"), "Minimal, quality"),
        BudgetAllocation(ExpenseCategory.PERSONAL, Decimal("30"), "DIY when possible"),
        BudgetAllocation(ExpenseCategory.EDUCATION, Decimal("50"), "Free resources"),
        BudgetAllocation(ExpenseCategory.SAVINGS, Decimal("1500"), "50%+ savings rate"),
        BudgetAllocation(ExpenseCategory.DEBT_PAYMENT, Decimal("0"), "Debt-free"),
        BudgetAllocation(ExpenseCategory.GIFTS, Decimal("30"), "Homemade/experiences"),
        BudgetAllocation(ExpenseCategory.SUBSCRIPTIONS, Decimal("30"), "Minimal"),
        BudgetAllocation(ExpenseCategory.MISCELLANEOUS, Decimal("30"), "Tiny buffer"),
    ],
    notes=[
        "Target 50-70% savings rate",
        "Focus on expense reduction",
        "Maximize tax-advantaged accounts",
        "Track every expense meticulously",
    ],
    recommended_for=[
        "FIRE movement",
        "Extreme savers",
        "High income, low expense lifestyle",
    ],
)

TEMPLATE_HIGH_INCOME = BudgetTemplate(
    name="High Income ($200k+)",
    description="Budget for high earners with lifestyle balance",
    allocations=[
        BudgetAllocation(
            ExpenseCategory.HOUSING, Decimal("4000"), "Nice home/neighborhood"
        ),
        BudgetAllocation(ExpenseCategory.UTILITIES, Decimal("400"), "Full services"),
        BudgetAllocation(ExpenseCategory.GROCERIES, Decimal("1200"), "Quality food"),
        BudgetAllocation(
            ExpenseCategory.TRANSPORTATION, Decimal("800"), "Reliable vehicles"
        ),
        BudgetAllocation(
            ExpenseCategory.HEALTHCARE, Decimal("500"), "Comprehensive coverage"
        ),
        BudgetAllocation(ExpenseCategory.INSURANCE, Decimal("600"), "Full protection"),
        BudgetAllocation(
            ExpenseCategory.ENTERTAINMENT, Decimal("500"), "Travel, hobbies"
        ),
        BudgetAllocation(
            ExpenseCategory.DINING_OUT, Decimal("600"), "Nice restaurants"
        ),
        BudgetAllocation(
            ExpenseCategory.CLOTHING, Decimal("300"), "Professional wardrobe"
        ),
        BudgetAllocation(ExpenseCategory.PERSONAL, Decimal("200"), "Self-care"),
        BudgetAllocation(
            ExpenseCategory.EDUCATION, Decimal("300"), "Continuous learning"
        ),
        BudgetAllocation(
            ExpenseCategory.SAVINGS, Decimal("3000"), "Maxed retirement + taxable"
        ),
        BudgetAllocation(
            ExpenseCategory.DEBT_PAYMENT, Decimal("0"), "Should be minimal"
        ),
        BudgetAllocation(ExpenseCategory.GIFTS, Decimal("300"), "Generous giving"),
        BudgetAllocation(
            ExpenseCategory.SUBSCRIPTIONS, Decimal("200"), "Premium services"
        ),
        BudgetAllocation(ExpenseCategory.MISCELLANEOUS, Decimal("300"), "Flexibility"),
    ],
    notes=[
        "Max out all tax-advantaged accounts first",
        "Avoid lifestyle inflation - save raises",
        "Consider backdoor Roth, mega backdoor",
        "Charitable giving can be tax-efficient",
    ],
    recommended_for=["High earners", "Tech workers", "Executives"],
)

# Registry of all templates
BUDGET_TEMPLATES: dict[str, BudgetTemplate] = {
    "50_30_20": TEMPLATE_50_30_20,
    "family": TEMPLATE_FAMILY_OF_FOUR,
    "minimalist": TEMPLATE_SINGLE_MINIMALIST,
    "zero_based": TEMPLATE_ZERO_BASED,
    "fire": TEMPLATE_FIRE,
    "high_income": TEMPLATE_HIGH_INCOME,
}


def get_template(name: str) -> BudgetTemplate:
    """
    Get a budget template by name.

    Args:
        name: Template name.

    Returns:
        BudgetTemplate instance.

    Raises:
        ValueError: If template not found.
    """
    if name not in BUDGET_TEMPLATES:
        available = ", ".join(BUDGET_TEMPLATES.keys())
        raise ValueError(f"Unknown template: {name}. Available: {available}")
    return BUDGET_TEMPLATES[name]


def list_templates() -> list[dict[str, Any]]:
    """
    List all available templates with summaries.

    Returns:
        List of template info dictionaries.
    """
    return [
        {
            "name": name,
            "display_name": t.name,
            "description": t.description,
            "total_budget": str(t.total_budget),
            "recommended_for": t.recommended_for,
        }
        for name, t in BUDGET_TEMPLATES.items()
    ]


def create_custom_template(
    name: str,
    description: str,
    monthly_income: Decimal,
    savings_rate: float = 20.0,
    housing_percent: float = 28.0,
) -> BudgetTemplate:
    """
    Create a custom template based on income and goals.

    Args:
        name: Template name.
        description: Template description.
        monthly_income: Monthly income.
        savings_rate: Target savings rate (percent).
        housing_percent: Housing allocation (percent).

    Returns:
        Custom BudgetTemplate.
    """
    # Calculate major allocations
    savings = monthly_income * Decimal(str(savings_rate / 100))
    housing = monthly_income * Decimal(str(housing_percent / 100))
    remaining = monthly_income - savings - housing

    # Distribute remaining across categories (percentages must add to 100%)
    allocations = [
        BudgetAllocation(ExpenseCategory.HOUSING, housing.quantize(Decimal("1"))),
        BudgetAllocation(ExpenseCategory.SAVINGS, savings.quantize(Decimal("1"))),
        BudgetAllocation(
            ExpenseCategory.UTILITIES,
            (remaining * Decimal("0.06")).quantize(Decimal("1")),
        ),
        BudgetAllocation(
            ExpenseCategory.GROCERIES,
            (remaining * Decimal("0.16")).quantize(Decimal("1")),
        ),
        BudgetAllocation(
            ExpenseCategory.TRANSPORTATION,
            (remaining * Decimal("0.12")).quantize(Decimal("1")),
        ),
        BudgetAllocation(
            ExpenseCategory.HEALTHCARE,
            (remaining * Decimal("0.06")).quantize(Decimal("1")),
        ),
        BudgetAllocation(
            ExpenseCategory.INSURANCE,
            (remaining * Decimal("0.06")).quantize(Decimal("1")),
        ),
        BudgetAllocation(
            ExpenseCategory.ENTERTAINMENT,
            (remaining * Decimal("0.09")).quantize(Decimal("1")),
        ),
        BudgetAllocation(
            ExpenseCategory.DINING_OUT,
            (remaining * Decimal("0.09")).quantize(Decimal("1")),
        ),
        BudgetAllocation(
            ExpenseCategory.CLOTHING,
            (remaining * Decimal("0.05")).quantize(Decimal("1")),
        ),
        BudgetAllocation(
            ExpenseCategory.PERSONAL,
            (remaining * Decimal("0.04")).quantize(Decimal("1")),
        ),
        BudgetAllocation(
            ExpenseCategory.EDUCATION,
            (remaining * Decimal("0.03")).quantize(Decimal("1")),
        ),
        BudgetAllocation(
            ExpenseCategory.DEBT_PAYMENT,
            (remaining * Decimal("0.11")).quantize(Decimal("1")),
        ),
        BudgetAllocation(
            ExpenseCategory.GIFTS, (remaining * Decimal("0.04")).quantize(Decimal("1"))
        ),
        BudgetAllocation(
            ExpenseCategory.SUBSCRIPTIONS,
            (remaining * Decimal("0.04")).quantize(Decimal("1")),
        ),
        BudgetAllocation(
            ExpenseCategory.MISCELLANEOUS,
            (remaining * Decimal("0.05")).quantize(Decimal("1")),
        ),
    ]

    return BudgetTemplate(
        name=name,
        description=description,
        allocations=allocations,
        notes=[
            f"Based on ${monthly_income:,.2f} monthly income",
            f"Targeting {savings_rate:g}% savings rate",
            f"Housing allocation: {housing_percent:g}%",
        ],
    )
