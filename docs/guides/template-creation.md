# Template Creation Guide

A comprehensive guide to creating reusable spreadsheet templates.

**Implements:** DOC-PROF-003 (Template Creation Guide)

## Overview

Templates define the structure, layout, and logic of spreadsheets. They enable:

- **Reusability**: Create once, generate many times with different data
- **Consistency**: Ensure uniform formatting across documents
- **Automation**: Dynamic content based on variables and conditions
- **Modularity**: Compose complex documents from reusable components

## Template Structure

Templates are defined in YAML with this structure:

```yaml
name: monthly_budget
version: "1.0"
description: "Monthly budget tracking template"

# Theme to use
theme: corporate

# Variables that can be set when rendering
variables:
  month:
    type: number
    description: "Month number (1-12)"
    required: true

  year:
    type: number
    description: "Year"
    default: "${current_year}"

  title:
    type: string
    default: "Monthly Budget Report"

  categories:
    type: list
    description: "Budget categories"
    required: true

# Reusable components
components:
  document_header:
    # ... component definition

# Sheet definitions
sheets:
  - name: "Budget"
    components:
      - "document_header:title=${title}"
    columns:
      - name: "Category"
        width: "150pt"
      - name: "Budget"
        width: "100pt"
        type: currency
    rows:
      # ... row definitions
```

## Variables

### Variable Types

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text values | `"Monthly Report"` |
| `number` | Numeric values | `2024` |
| `currency` | Money amounts | `1500.00` |
| `date` | Date values | `"2024-12-31"` |
| `boolean` | True/false | `true` |
| `list` | Array of items | `["Housing", "Food"]` |

### Variable Definition

```yaml
variables:
  # Required variable with no default
  month:
    type: number
    description: "Month number (1-12)"
    required: true

  # Optional with default value
  year:
    type: number
    description: "Year"
    default: "${current_year}"

  # String with static default
  currency_symbol:
    type: string
    default: "$"

  # List variable
  expense_categories:
    type: list
    description: "List of expense category names"
    required: true
```

### Built-in Variables

These are automatically available:

| Variable | Description | Example |
|----------|-------------|---------|
| `${current_date}` | Today's date | `2024-12-28` |
| `${current_year}` | Current year | `2024` |
| `${current_month}` | Current month | `12` |
| `${current_day}` | Current day | `28` |

### Using Variables

In cells and content:

```yaml
cells:
  - value: "${title}"
    style: title

  - value: "Report for ${month_name(month)} ${year}"
    style: subtitle

  - value: "${sum(budget_amounts)}"
    style: currency
```

## Variable Substitution

### Simple Substitution

```yaml
value: "${variable_name}"
```

### Nested Access

For objects and lists:

```yaml
value: "${user.name}"
value: "${categories[0]}"
```

### Functions

Built-in functions for transformations:

| Function | Description | Example |
|----------|-------------|---------|
| `month_name(n)` | Month number to name | `${month_name(3)}` -> "March" |
| `month_abbrev(n)` | Month abbreviation | `${month_abbrev(3)}` -> "Mar" |
| `format_date(d, fmt)` | Format date | `${format_date(date, "MMM D, YYYY")}` |
| `format_currency(n)` | Format as currency | `${format_currency(1500)}` -> "$1,500.00" |
| `format_percentage(n)` | Format as percent | `${format_percentage(0.15)}` -> "15%" |
| `sum(list)` | Sum of numbers | `${sum(amounts)}` |
| `len(list)` | Length of list | `${len(categories)}` |
| `min(list)` | Minimum value | `${min(amounts)}` |
| `max(list)` | Maximum value | `${max(amounts)}` |
| `upper(s)` | Uppercase | `${upper(name)}` |
| `lower(s)` | Lowercase | `${lower(name)}` |

### Filters

Apply transformations with pipe syntax:

```yaml
value: "${amount|currency}"
value: "${name|upper}"
value: "${missing_value|default:0}"
value: "${percentage|round:2}"
```

Available filters:

| Filter | Description | Example |
|--------|-------------|---------|
| `default:val` | Default if empty | `${x\|default:0}` |
| `upper` | Uppercase | `${name\|upper}` |
| `lower` | Lowercase | `${name\|lower}` |
| `round:n` | Round to n decimals | `${amount\|round:2}` |
| `currency` | Format as currency | `${amount\|currency}` |
| `percentage` | Format as percentage | `${rate\|percentage}` |

### Arithmetic

Basic math in expressions:

```yaml
value: "${budget - actual}"
value: "${total * tax_rate}"
value: "${amount / 12}"
```

## Conditional Content

### Basic Conditions

Include content only when conditions are met:

```yaml
rows:
  - cells:
      - value: "Above Budget!"
        style: warning
    condition: "${actual > budget}"

  - cells:
      - value: "On Track"
        style: success
    condition: "${actual <= budget}"
```

### If/Else Blocks

```yaml
conditional:
  if: "${variance < 0}"
  then:
    cells:
      - value: "${variance}"
        style: negative
  else:
    cells:
      - value: "${variance}"
        style: positive
```

### Conditional Styling

Apply different styles based on conditions:

```yaml
cells:
  - value: "${variance}"
    style:
      if: "${variance < 0}"
      then: "negative_currency"
      else: "positive_currency"
```

## Components

### Component Definition

Reusable template sections:

```yaml
components:
  document_header:
    description: "Standard document header"
    variables:
      - name: title
        type: string
        default: "Document"
      - name: subtitle
        type: string
        default: ""
      - name: date
        type: string
        default: "${current_date}"

    rows:
      - cells:
          - value: "${title}"
            style: title
            colspan: 4
        height: "24pt"

      - cells:
          - value: "${subtitle}"
            style: subtitle
            colspan: 4
        condition: "${subtitle}"

      - cells:
          - value: "${date}"
            style: date
            type: date
```

### Using Components

Reference in sheets with optional variable overrides:

```yaml
sheets:
  - name: "Budget"
    components:
      # Basic usage
      - "document_header"

      # With variable overrides
      - "document_header:title=Monthly Budget,date=2024-12-01"
```

### Built-in Components

Pre-built components from the component library:

| Component | Description |
|-----------|-------------|
| `document_header` | Title, subtitle, date header |
| `month_header` | Month/year specific header |
| `income_summary` | Income total section |
| `expense_summary` | Expense total section |
| `balance_row` | Net balance (income - expenses) |
| `category_header` | Column headers for budget table |
| `category_row` | Single category with budget/actual |
| `category_total` | Category totals with formulas |
| `transaction_header` | Transaction table headers |
| `transaction_entry` | Single transaction row |

**Example:**
```yaml
sheets:
  - name: "Summary"
    components:
      - "document_header:title=Financial Summary"
      - "income_summary"
      - "expense_summary"
      - "balance_row:income_cell=B5,expense_cell=B8"
```

## Formula Templates

### Static Formulas

```yaml
cells:
  - formula: "=SUM(B2:B20)"
    style: total
```

### Dynamic Formulas

Using variables in formulas:

```yaml
cells:
  - formula: "=SUM(B2:B${row_count + 1})"
```

### Formula with Variable Ranges

```yaml
variables:
  data_start_row:
    type: number
    default: 2
  data_end_row:
    type: number
    default: 20

cells:
  - formula: "=AVERAGE(C${data_start_row}:C${data_end_row})"
```

## Sheet Definitions

### Basic Sheet

```yaml
sheets:
  - name: "Budget"
    columns:
      - name: "Category"
        width: "150pt"
      - name: "Budget"
        width: "100pt"
        type: currency
      - name: "Actual"
        width: "100pt"
        type: currency

    rows:
      - cells:
          - value: "Category"
          - value: "Budget"
          - value: "Actual"
        style: header

      - cells:
          - value: "Housing"
          - value: 2000
          - value: 1850
        style: data
```

### Sheet with Freeze Panes

```yaml
sheets:
  - name: "Data"
    freeze:
      rows: 1
      columns: 1
```

### Sheet with Print Settings

```yaml
sheets:
  - name: "Report"
    print:
      area: "A1:D50"
      orientation: landscape
      fit_to_page: true
```

## Iteration

### Iterating Over Lists

```yaml
variables:
  categories:
    type: list
    required: true

sheets:
  - name: "Budget"
    rows:
      # Header
      - cells:
          - value: "Category"
          - value: "Amount"
        style: header

      # Iterate over categories
      - for_each: category in categories
        cells:
          - value: "${category.name}"
          - value: "${category.budget}"
            type: currency
```

### Generating Multiple Sheets

```yaml
variables:
  months:
    type: list
    default: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

sheets:
  - for_each: month in months
    name: "${month_name(month)}"
    components:
      - "month_header:month=${month}"
    # ... rest of sheet definition
```

## Step-by-Step Tutorial

### 1. Define the Template

Create `templates/monthly_budget.yaml`:

```yaml
name: monthly_budget
version: "1.0"
description: "Monthly budget tracking template"
theme: professional

variables:
  month:
    type: number
    required: true
    description: "Month (1-12)"

  year:
    type: number
    default: "${current_year}"

  categories:
    type: list
    required: true
    description: "Budget categories with name and budget amount"

components:
  budget_header:
    rows:
      - cells:
          - value: "${month_name(month)} ${year} Budget"
            style: title
            colspan: 4
        height: "24pt"
      - cells: []
        height: "12pt"
```

### 2. Define Sheets

```yaml
sheets:
  - name: "Budget"
    components:
      - "budget_header"

    columns:
      - name: "Category"
        width: "150pt"
        style: text
      - name: "Budget"
        width: "100pt"
        type: currency
      - name: "Actual"
        width: "100pt"
        type: currency
      - name: "Remaining"
        width: "100pt"
        type: currency

    freeze:
      rows: 3

    rows:
      # Column headers
      - cells:
          - value: "Category"
          - value: "Budget"
          - value: "Actual"
          - value: "Remaining"
        style: header

      # Data rows from categories
      - for_each: cat in categories
        cells:
          - value: "${cat.name}"
          - value: "${cat.budget}"
            type: currency
          - value: ""  # Actual - to be filled in
          - formula: "=B{row}-C{row}"
            type: currency
        style: data
```

### 3. Add Totals

```yaml
    rows:
      # ... data rows from above ...

      # Total row
      - cells:
          - value: "Total"
            style: total_label
          - formula: "=SUM(B4:B${3 + len(categories)})"
            style: total
          - formula: "=SUM(C4:C${3 + len(categories)})"
            style: total
          - formula: "=B${4 + len(categories)}-C${4 + len(categories)}"
            style: total
```

### 4. Add Conditional Formatting

```yaml
    conditional_formats:
      - name: "variance_color"
        range: "D4:D${3 + len(categories)}"
        rules:
          - condition: "cell_value < 0"
            style: negative
          - condition: "cell_value >= 0"
            style: positive
```

### 5. Render the Template

```python
from spreadsheet_dl.template_engine import TemplateLoader, TemplateRenderer

# Load template
loader = TemplateLoader("./templates")
template = loader.load("monthly_budget")

# Define variables
variables = {
    "month": 12,
    "year": 2024,
    "categories": [
        {"name": "Housing", "budget": 2000},
        {"name": "Food", "budget": 800},
        {"name": "Transportation", "budget": 400},
        {"name": "Utilities", "budget": 300},
        {"name": "Entertainment", "budget": 200},
    ]
}

# Render
renderer = TemplateRenderer()
result = renderer.render(template, variables)

# Save
result.save("december_budget.ods")
```

## Best Practices

### 1. Use Meaningful Variable Names

```yaml
# Good
variables:
  fiscal_year:
    type: number
  budget_categories:
    type: list

# Avoid
variables:
  y:
    type: number
  cats:
    type: list
```

### 2. Provide Defaults

```yaml
variables:
  currency_symbol:
    type: string
    default: "$"
    description: "Currency symbol for formatting"
```

### 3. Document Components

```yaml
components:
  expense_table:
    description: |
      Expense tracking table with category breakdown.
      Requires: expense_categories variable (list)
      Output: Table with category, budget, actual, variance columns
```

### 4. Use Components for Reuse

Extract repeated structures:

```yaml
# Instead of repeating...
sheets:
  - name: "Q1"
    rows:
      - cells: [...]  # Same structure
  - name: "Q2"
    rows:
      - cells: [...]  # Same structure

# Define a component
components:
  quarterly_summary:
    rows:
      - cells: [...]

sheets:
  - name: "Q1"
    components: ["quarterly_summary:quarter=1"]
  - name: "Q2"
    components: ["quarterly_summary:quarter=2"]
```

### 5. Validate Input

Use required and type constraints:

```yaml
variables:
  month:
    type: number
    required: true
    min: 1
    max: 12
    description: "Month number (1-12)"
```

### 6. Test with Different Data

Render with various inputs to ensure flexibility:

```python
# Test with minimal data
result = renderer.render(template, {
    "month": 1,
    "categories": [{"name": "Test", "budget": 100}]
})

# Test with many categories
result = renderer.render(template, {
    "month": 6,
    "categories": [{"name": f"Cat {i}", "budget": i * 100}
                   for i in range(1, 21)]
})
```

## Complete Example

```yaml
# templates/comprehensive_budget.yaml
name: comprehensive_budget
version: "1.0"
description: "Comprehensive monthly budget with summary and detail sheets"
theme: professional

variables:
  month:
    type: number
    required: true
    description: "Month (1-12)"

  year:
    type: number
    default: "${current_year}"

  income_items:
    type: list
    required: true
    description: "Income sources with name and amount"

  expense_categories:
    type: list
    required: true
    description: "Expense categories with name and budgeted amount"

components:
  report_header:
    variables:
      - name: title
        type: string
        required: true
    rows:
      - cells:
          - value: "${title}"
            style: title
            colspan: 4
        height: "28pt"
      - cells:
          - value: "${month_name(month)} ${year}"
            style: subtitle
            colspan: 4
        height: "20pt"
      - cells: []
        height: "10pt"

sheets:
  - name: "Summary"
    components:
      - "report_header:title=Budget Summary"

    columns:
      - name: "Description"
        width: "200pt"
      - name: "Amount"
        width: "120pt"
        type: currency

    rows:
      # Income Section
      - cells:
          - value: "INCOME"
            style: section_header
            colspan: 2
        height: "20pt"

      - for_each: item in income_items
        cells:
          - value: "${item.name}"
            style: data
          - value: "${item.amount}"
            style: currency

      - cells:
          - value: "Total Income"
            style: subtotal_label
          - formula: "=SUM(B3:B${2 + len(income_items)})"
            style: subtotal
        height: "20pt"

      # Spacer
      - cells: []
        height: "15pt"

      # Expense Section
      - cells:
          - value: "EXPENSES"
            style: section_header
            colspan: 2
        height: "20pt"

      - for_each: cat in expense_categories
        cells:
          - value: "${cat.name}"
            style: data
          - value: "${cat.budget}"
            style: currency

      - cells:
          - value: "Total Expenses"
            style: subtotal_label
          - formula: "=SUM(B${6 + len(income_items)}:B${5 + len(income_items) + len(expense_categories)})"
            style: subtotal
        height: "20pt"

      # Spacer
      - cells: []
        height: "15pt"

      # Net Balance
      - cells:
          - value: "NET BALANCE"
            style: total_label
          - formula: "=B${3 + len(income_items)}-B${7 + len(income_items) + len(expense_categories)}"
            style: total
        height: "24pt"

  - name: "Details"
    components:
      - "report_header:title=Budget Details"

    columns:
      - name: "Category"
        width: "150pt"
      - name: "Budget"
        width: "100pt"
        type: currency
      - name: "Actual"
        width: "100pt"
        type: currency
      - name: "Variance"
        width: "100pt"
        type: currency
      - name: "% Used"
        width: "80pt"
        type: percentage

    freeze:
      rows: 4

    rows:
      - cells:
          - value: "Category"
          - value: "Budget"
          - value: "Actual"
          - value: "Variance"
          - value: "% Used"
        style: header

      - for_each: cat in expense_categories
        cells:
          - value: "${cat.name}"
          - value: "${cat.budget}"
            type: currency
          - value: ""
          - formula: "=B{row}-C{row}"
            type: currency
          - formula: "=IF(B{row}>0,C{row}/B{row},0)"
            type: percentage
        style: data

    conditional_formats:
      - name: "over_budget"
        range: "D5:D${4 + len(expense_categories)}"
        rules:
          - condition: "cell_value < 0"
            style: negative

      - name: "percent_warning"
        range: "E5:E${4 + len(expense_categories)}"
        rules:
          - condition: "cell_value > 1"
            style: danger
          - condition: "cell_value > 0.9"
            style: warning
```
