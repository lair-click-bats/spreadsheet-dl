# Budget Templates API Reference

## Overview

The `templates` module provides pre-configured budget templates for different household types and financial situations. Templates can be scaled to any income level and customized for specific needs.

**Key Features:**

- 6 pre-built budget templates
- Income-based scaling
- Percentage-based allocations
- Template customization
- Recommended use cases
- Notes and tips for each template

**Module Location:** `spreadsheet_dl.domains.finance.templates`

---

## Core Classes

### BudgetTemplate

Budget template definition with allocations and metadata.

```python
@dataclass
class BudgetTemplate:
    name: str
    description: str
    allocations: list[BudgetAllocation]
    income_percentages: dict[str, float] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    recommended_for: list[str] = field(default_factory=list)
```

#### Properties

##### `total_budget -> Decimal`

Calculate total budget from allocations.

```python
template = TEMPLATE_50_30_20
total = template.total_budget  # Sum of all allocations
```

#### Methods

##### `to_dict() -> dict[str, Any]`

Convert template to dictionary.

```python
data = template.to_dict()
print(data['name'])
print(data['total_budget'])
```

##### `scale_to_income(monthly_income: Decimal) -> list[BudgetAllocation]`

Scale allocations to a specific monthly income.

```python
from decimal import Decimal

template = TEMPLATE_50_30_20
monthly_income = Decimal("5000")

# Scale template to $5,000/month
scaled = template.scale_to_income(monthly_income)

for allocation in scaled:
    print(f"{allocation.category.value}: ${allocation.monthly_budget}")
```

---

## Pre-built Templates

### TEMPLATE_50_30_20

Classic 50/30/20 budgeting rule.

**Total:** $4,700/month (example)
**Breakdown:**

- 50% Needs (housing, utilities, groceries, transportation, healthcare, insurance)
- 30% Wants (entertainment, dining, clothing, subscriptions, gifts)
- 20% Savings & Debt (savings, debt payment, education)

**Recommended for:** Beginners, Single income, Debt payoff focus

```python
from spreadsheet_dl.domains.finance.templates import TEMPLATE_50_30_20

budget = TEMPLATE_50_30_20
print(f"Base budget: ${budget.total_budget}")

# Scale to your income
from decimal import Decimal
scaled = budget.scale_to_income(Decimal("6000"))
```

---

### TEMPLATE_FAMILY_OF_FOUR

Budget optimized for a family with two children.

**Total:** $6,800/month (example)
**Focus:** Family expenses, children's needs, education, larger home

**Recommended for:** Families with children, Dual income households

```python
from spreadsheet_dl.domains.finance.templates import TEMPLATE_FAMILY_OF_FOUR

budget = TEMPLATE_FAMILY_OF_FOUR
for allocation in budget.allocations:
    print(f"{allocation.category.value}: ${allocation.monthly_budget}")
```

---

### TEMPLATE_SINGLE_MINIMALIST

Lean budget for single person focused on savings.

**Total:** $3,380/month (example)
**Focus:** High savings rate, minimal lifestyle, debt elimination

**Recommended for:** Single person, FIRE aspirants, Debt elimination

```python
from spreadsheet_dl.domains.finance.templates import TEMPLATE_SINGLE_MINIMALIST

budget = TEMPLATE_SINGLE_MINIMALIST
print(f"Savings allocation: ${budget.allocations[11].monthly_budget}")
```

---

### TEMPLATE_ZERO_BASED

Every dollar has a purpose - income minus expenses equals zero.

**Total:** $4,750/month (example)
**Approach:** Assign every dollar before the month starts

**Recommended for:** Detail-oriented, Dave Ramsey followers, Tight budgets

```python
from spreadsheet_dl.domains.finance.templates import TEMPLATE_ZERO_BASED

budget = TEMPLATE_ZERO_BASED
print("\n".join(budget.notes))
```

---

### TEMPLATE_FIRE

Extreme savings rate for early retirement (Financial Independence, Retire Early).

**Total:** $3,500/month (example)
**Focus:** 50-70% savings rate, expense minimization, tax optimization

**Recommended for:** FIRE movement, Extreme savers, High income/low expense lifestyle

```python
from spreadsheet_dl.domains.finance.templates import TEMPLATE_FIRE

budget = TEMPLATE_FIRE
savings_allocation = next(a for a in budget.allocations if a.category.value == "Savings")
print(f"Savings: ${savings_allocation.monthly_budget}")
```

---

### TEMPLATE_HIGH_INCOME

Budget for high earners ($200k+) with lifestyle balance.

**Total:** $13,200/month (example)
**Focus:** Maxed retirement accounts, quality of life, generous giving

**Recommended for:** High earners, Tech workers, Executives

```python
from spreadsheet_dl.domains.finance.templates import TEMPLATE_HIGH_INCOME

budget = TEMPLATE_HIGH_INCOME
print(f"Total monthly: ${budget.total_budget}")
```

---

## Functions

### `get_template(name: str) -> BudgetTemplate`

Get a budget template by name.

**Template Names:**

- `"50_30_20"` - 50/30/20 Rule
- `"family"` - Family of Four
- `"minimalist"` - Single Minimalist
- `"zero_based"` - Zero-Based Budget
- `"fire"` - FIRE (Financial Independence)
- `"high_income"` - High Income ($200k+)

```python
from spreadsheet_dl.domains.finance.templates import get_template

template = get_template("50_30_20")
print(template.name)  # "50/30/20 Rule"
```

**Raises:** `ValueError` if template not found.

---

### `list_templates() -> list[dict[str, Any]]`

List all available templates with summaries.

```python
from spreadsheet_dl.domains.finance.templates import list_templates

for template_info in list_templates():
    print(f"{template_info['name']}: ${template_info['total_budget']}")
    print(f"  Recommended for: {', '.join(template_info['recommended_for'])}")
```

**Returns:** List of dictionaries with:

- `name` - Template key
- `display_name` - Display name
- `description` - Description
- `total_budget` - Total budget amount
- `recommended_for` - List of recommendations

---

### `create_custom_template(name: str, description: str, monthly_income: Decimal, savings_rate: float = 20.0, housing_percent: float = 28.0) -> BudgetTemplate`

Create a custom template based on income and goals.

```python
from decimal import Decimal
from spreadsheet_dl.domains.finance.templates import create_custom_template

template = create_custom_template(
    name="My Custom Budget",
    description="Tailored to my situation",
    monthly_income=Decimal("5500"),
    savings_rate=25.0,  # 25% savings
    housing_percent=30.0,  # 30% housing
)

print(f"Total: ${template.total_budget}")
for allocation in template.allocations:
    print(f"{allocation.category.value}: ${allocation.monthly_budget}")
```

**Parameters:**

- `name` - Template name
- `description` - Template description
- `monthly_income` - Monthly income
- `savings_rate` - Target savings rate (percent, default: 20.0)
- `housing_percent` - Housing allocation (percent, default: 28.0)

---

## Registry

The `BUDGET_TEMPLATES` dictionary contains all pre-built templates:

```python
from spreadsheet_dl.domains.finance.templates import BUDGET_TEMPLATES

# Access directly
template = BUDGET_TEMPLATES["50_30_20"]

# List all
for key, template in BUDGET_TEMPLATES.items():
    print(f"{key}: {template.name}")
```

---

## Usage Examples

### Example 1: Browse Templates

```python
from spreadsheet_dl.domains.finance.templates import list_templates

print("Available Budget Templates:")
print("=" * 60)

for template_info in list_templates():
    print(f"\n{template_info['display_name']}")
    print(f"  {template_info['description']}")
    print(f"  Base Budget: ${template_info['total_budget']}")
    print(f"  Best for: {', '.join(template_info['recommended_for'])}")
```

### Example 2: Scale to Income

```python
from decimal import Decimal
from spreadsheet_dl.domains.finance.templates import get_template

# Get template
template = get_template("50_30_20")

# Scale to different incomes
incomes = [Decimal("3000"), Decimal("5000"), Decimal("8000")]

for income in incomes:
    scaled = template.scale_to_income(income)
    total = sum(a.monthly_budget for a in scaled)
    print(f"\nIncome: ${income}")
    print(f"Scaled Total: ${total}")

    # Show major categories
    for allocation in scaled[:5]:
        print(f"  {allocation.category.value}: ${allocation.monthly_budget}")
```

### Example 3: Create from Template

```python
from decimal import Decimal
from spreadsheet_dl.domains.finance.templates import get_template
from spreadsheet_dl.domains.finance.ods_generator import MonthlyBudget

# Get and scale template
template = get_template("family")
allocations = template.scale_to_income(Decimal("7000"))

# Create budget from template
budget = MonthlyBudget(month=1, year=2025)
for allocation in allocations:
    budget.add_budget_allocation(allocation)

# Save
budget.save_to_ods("family_budget_2025.ods")
```

### Example 4: Compare Templates

```python
from decimal import Decimal
from spreadsheet_dl.domains.finance.templates import BUDGET_TEMPLATES

monthly_income = Decimal("5000")

print(f"Comparing templates at ${monthly_income}/month:")
print("=" * 60)

for key, template in BUDGET_TEMPLATES.items():
    scaled = template.scale_to_income(monthly_income)

    # Find savings allocation
    savings = next(
        (a for a in scaled if a.category.value == "Savings"),
        None
    )

    if savings:
        savings_rate = (savings.monthly_budget / monthly_income) * 100
        print(f"\n{template.name}:")
        print(f"  Savings: ${savings.monthly_budget} ({savings_rate:.1f}%)")
```

### Example 5: Custom Template

```python
from decimal import Decimal
from spreadsheet_dl.domains.finance.templates import create_custom_template

# Create custom high-savings template
template = create_custom_template(
    name="Aggressive Saver",
    description="40% savings for early retirement",
    monthly_income=Decimal("6000"),
    savings_rate=40.0,
    housing_percent=25.0,
)

print(template.notes)
print(f"\nTotal Budget: ${template.total_budget}")
```

### Example 6: View Template Details

```python
from spreadsheet_dl.domains.finance.templates import get_template

template = get_template("fire")

print(f"Template: {template.name}")
print(f"Description: {template.description}")
print(f"\nRecommended for:")
for rec in template.recommended_for:
    print(f"  - {rec}")

print(f"\nNotes:")
for note in template.notes:
    print(f"  - {note}")

print(f"\nAllocations:")
for allocation in template.allocations:
    print(f"  {allocation.category.value}: ${allocation.monthly_budget}")
    if allocation.notes:
        print(f"    ({allocation.notes})")
```

### Example 7: Export Template

```python
from spreadsheet_dl.domains.finance.templates import get_template
import json

template = get_template("50_30_20")
data = template.to_dict()

# Save as JSON
with open("budget_template.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Exported {template.name}")
```

### Example 8: Template with Adjustments

```python
from decimal import Decimal
from spreadsheet_dl.domains.finance.templates import get_template

template = get_template("minimalist")
allocations = template.scale_to_income(Decimal("4000"))

# Adjust specific category
for allocation in allocations:
    if allocation.category.value == "Savings":
        # Increase savings
        allocation.monthly_budget += Decimal("200")
    elif allocation.category.value == "Entertainment":
        # Decrease entertainment
        allocation.monthly_budget -= Decimal("50")

# Use adjusted allocations
total = sum(a.monthly_budget for a in allocations)
print(f"Adjusted total: ${total}")
```

### Example 9: Zero-Based Budgeting

```python
from decimal import Decimal
from spreadsheet_dl.domains.finance.templates import get_template

monthly_income = Decimal("5000")
template = get_template("zero_based")
allocations = template.scale_to_income(monthly_income)

# Verify zero-based (income = expenses)
total_allocated = sum(a.monthly_budget for a in allocations)
difference = monthly_income - total_allocated

print(f"Income: ${monthly_income}")
print(f"Allocated: ${total_allocated}")
print(f"Remaining: ${difference}")

if difference == 0:
    print("Perfect zero-based budget!")
```

### Example 10: Multi-Template Analysis

```python
from decimal import Decimal
from spreadsheet_dl.domains.finance.templates import list_templates

monthly_income = Decimal("6000")

print(f"Budget Analysis for ${monthly_income}/month")
print("=" * 70)

for template_info in list_templates():
    from spreadsheet_dl.domains.finance.templates import get_template
    template = get_template(template_info['name'])
    allocations = template.scale_to_income(monthly_income)

    # Calculate category totals
    needs = sum(
        a.monthly_budget for a in allocations
        if a.category.value in ["Housing", "Utilities", "Groceries",
                                "Transportation", "Healthcare", "Insurance"]
    )

    savings = sum(
        a.monthly_budget for a in allocations
        if a.category.value in ["Savings", "Debt Payment"]
    )

    print(f"\n{template.name}:")
    print(f"  Needs: ${needs} ({needs/monthly_income*100:.1f}%)")
    print(f"  Savings: ${savings} ({savings/monthly_income*100:.1f}%)")
```

---

## Template Comparison

| Template          | Focus                | Savings Rate | Housing % | Best For               |
| ----------------- | -------------------- | ------------ | --------- | ---------------------- |
| 50/30/20          | Balanced             | 20%          | 30%       | Beginners, general use |
| Family of Four    | Family needs         | ~12%         | 32%       | Families with children |
| Single Minimalist | High savings         | ~23%         | 30%       | Single, debt payoff    |
| Zero-Based        | Intentional spending | 20%          | 32%       | Detail-oriented        |
| FIRE              | Maximum savings      | 50-70%       | 29%       | Early retirement       |
| High Income       | Lifestyle + savings  | 23%          | 30%       | High earners ($200k+)  |

---

## Income Percentages

Templates with `income_percentages` defined scale proportionally to any income level while maintaining recommended allocation ratios.

Templates without percentages scale the base amounts proportionally.

---

## Notes

- **All amounts are in USD** (Decimal type for precision)
- **Templates are starting points** - customize to your situation
- **Percentages are guidelines** - actual needs vary by location and lifestyle
- **Housing percentage** follows the 28% rule (should not exceed 28-30% of income)
- **Savings include** both emergency fund building and retirement contributions
