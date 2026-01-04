#!/usr/bin/env python3
"""
Template Engine Usage Examples - v4.0 Feature Showcase

Demonstrates comprehensive usage of the SpreadsheetDL template engine including:
- Loading and rendering YAML templates
- Variable substitution with built-in functions
- Conditional rendering
- Component composition and reuse
- Custom template creation
- Template validation and error handling

The template engine enables creating reusable spreadsheet templates with
variable substitution, similar to Jinja2 but optimized for spreadsheets.
"""

import sys
from datetime import date

# ============================================================================
# Example 1: Basic Template Loading
# ============================================================================


def example_basic_template_loading() -> None:
    """
    Demonstrate basic template loading from YAML.

    Shows:
    - Loading templates by name
    - Loading from file path
    - Loading from YAML string
    - Listing available templates
    """
    from spreadsheet_dl.template_engine.loader import TemplateLoader

    print("=" * 70)
    print("Example 1: Basic Template Loading")
    print("=" * 70)

    # 1. Create template loader
    print("\n1. Creating template loader:")
    loader = TemplateLoader()
    print(f"   Template directory: {loader._template_dir}")

    # 2. List available templates
    print("\n2. Listing available templates:")
    templates = loader.list_templates()
    if templates:
        print(f"   Found {len(templates)} templates:")
        for tmpl in templates[:5]:  # Show first 5
            print(f"     • {tmpl['name']} v{tmpl['version']}")
            print(f"       {tmpl['description']}")
    else:
        print("   No templates found (this is a demonstration)")

    # 3. Load template from YAML string
    print("\n3. Loading template from YAML string:")
    yaml_content = """
meta:
  name: Simple Budget
  version: 1.0.0
  description: A simple budget template

variables:
  - name: month
    type: integer
    description: Month number (1-12)
    required: true
  - name: year
    type: integer
    description: Year
    required: true

sheets:
  - name: Budget
    columns:
      - name: Category
        width: 4cm
      - name: Budget
        width: 3cm
        type: currency
      - name: Actual
        width: 3cm
        type: currency

    header:
      cells:
        - value: Category
          style: header
        - value: Budget
          style: header
        - value: Actual
          style: header
"""

    template = loader.load_from_string(yaml_content)
    print(f"   Template loaded: {template.name}")
    print(f"   Version: {template.version}")
    print(f"   Variables: {len(template.variables)}")
    print(f"   Sheets: {len(template.sheets)}")

    print("\n✓ Template loading demonstrated")
    print()


# ============================================================================
# Example 2: Variable Substitution
# ============================================================================


def example_variable_substitution() -> None:
    """
    Demonstrate variable substitution in templates.

    Shows:
    - Simple variable substitution
    - Nested variable access
    - Function calls in templates
    - Filter expressions
    - Arithmetic expressions
    """
    from spreadsheet_dl.template_engine.renderer import ExpressionEvaluator

    print("=" * 70)
    print("Example 2: Variable Substitution")
    print("=" * 70)

    # Create evaluator with variables
    variables = {
        "month": 12,
        "year": 2025,
        "budget": 5000,
        "actual": 4250,
        "categories": ["Housing", "Food", "Transport"],
        "config": {"currency": "$", "locale": "en_US"},
    }

    evaluator = ExpressionEvaluator(variables)

    # 1. Simple variable substitution
    print("\n1. Simple variable substitution:")
    examples = [
        ("Budget for month ${month}", variables),
        ("Year: ${year}", variables),
        ("Total budget: ${budget}", variables),
    ]

    for template, _ in examples:
        result = evaluator.evaluate(template)
        print(f"   '{template}' → '{result}'")

    # 2. Nested variable access
    print("\n2. Nested variable access:")
    nested_examples = [
        "Currency: ${config.currency}",
        "Locale: ${config.locale}",
    ]

    for template in nested_examples:
        result = evaluator.evaluate(template)
        print(f"   '{template}' → '{result}'")

    # 3. Function calls
    print("\n3. Built-in function calls:")
    function_examples = [
        "Month name: ${month_name(month)}",
        "Month abbrev: ${month_abbrev(month)}",
        "Budget formatted: ${format_currency(budget)}",
        "Uppercase: ${upper('budget')}",
    ]

    for template in function_examples:
        result = evaluator.evaluate(template)
        print(f"   '{template}' → '{result}'")

    # 4. Filters
    print("\n4. Filter expressions:")
    filter_examples = [
        ("Title case: ${'budget report'|title}", "'budget report'|title"),
        ("Default value: ${missing|default:N/A}", "missing|default:N/A"),
        ("Currency: ${budget|currency:$}", "budget|currency:$"),
        ("Round: ${4250.753|round:2}", "4250.753|round:2"),
    ]

    for desc, template in filter_examples:
        result = evaluator.evaluate(template)
        print(f"   {desc}")
        print(f"     '{template}' → '{result}'")

    # 5. Arithmetic expressions
    print("\n5. Arithmetic expressions:")
    arithmetic_examples = [
        "Remaining: ${budget - actual}",
        "Percent used: ${actual * 100 / budget}",
    ]

    for template in arithmetic_examples:
        result = evaluator.evaluate(template)
        print(f"   '{template}' → '{result}'")

    print("\n✓ Variable substitution demonstrated")
    print()


# ============================================================================
# Example 3: Conditional Rendering
# ============================================================================


def example_conditional_rendering() -> None:
    """
    Demonstrate conditional content rendering.

    Shows:
    - If/else conditionals
    - Comparison operators
    - Boolean logic
    - Conditional formatting
    """
    from spreadsheet_dl.template_engine.renderer import (
        ConditionalEvaluator,
        ExpressionEvaluator,
    )
    from spreadsheet_dl.template_engine.schema import ConditionalBlock

    print("=" * 70)
    print("Example 3: Conditional Rendering")
    print("=" * 70)

    # 1. Simple conditionals
    print("\n1. Simple conditional evaluation:")
    variables = {"budget": 5000, "actual": 5500, "month": 12}
    expr_eval = ExpressionEvaluator(variables)
    cond_eval = ConditionalEvaluator(expr_eval)

    conditions = [
        ("actual > budget", "Over budget"),
        ("actual < budget", "Under budget"),
        ("month == 12", "December"),
        ("budget > 0", "Budget exists"),
    ]

    for condition, description in conditions:
        result = cond_eval.evaluate(condition)
        print(f"   '{condition}' → {result} ({description})")

    # 2. Conditional blocks
    print("\n2. Conditional blocks with if/else:")

    # Over budget scenario
    over_budget_block = ConditionalBlock(
        condition="actual > budget",
        content=["⚠️ Over budget!", "Review spending"],
        else_content=["✓ On track", "Good job"],
    )

    selected_content = cond_eval.select_content(over_budget_block)
    print(
        f"   Condition: actual ({variables['actual']}) > budget ({variables['budget']})"
    )
    print(f"   Result: {selected_content}")

    # Under budget scenario
    variables_under = {"budget": 5000, "actual": 4500}
    expr_eval_under = ExpressionEvaluator(variables_under)
    cond_eval_under = ConditionalEvaluator(expr_eval_under)

    selected_content = cond_eval_under.select_content(over_budget_block)
    print(
        f"\n   Condition: actual ({variables_under['actual']}) > budget ({variables_under['budget']})"
    )
    print(f"   Result: {selected_content}")

    # 3. Complex conditionals
    print("\n3. Complex conditional expressions:")
    complex_conditions = [
        "actual > budget and month == 12",
        "actual > 0 and budget > 0",
    ]

    for condition in complex_conditions:
        result = cond_eval.evaluate(condition)
        print(f"   '{condition}' → {result}")

    print("\n✓ Conditional rendering demonstrated")
    print()


# ============================================================================
# Example 4: Component Composition
# ============================================================================


def example_component_composition() -> None:
    """
    Demonstrate reusable component composition.

    Shows:
    - Defining components
    - Component variables
    - Component reuse
    - Inline variable assignment
    """
    from spreadsheet_dl.template_engine.loader import TemplateLoader

    print("=" * 70)
    print("Example 4: Component Composition")
    print("=" * 70)

    # Create template with components
    yaml_content = """
meta:
  name: Component Demo
  version: 1.0.0

variables:
  - name: title
    type: string
    required: true

components:
  header:
    description: Standard header component
    variables:
      - name: title
        type: string
        required: true
      - name: subtitle
        type: string
        default: ""
    rows:
      - cells:
          - value: ${title}
            style: header
            colspan: 3
      - cells:
          - value: ${subtitle}
            style: subheader
            colspan: 3

  footer:
    description: Standard footer component
    variables:
      - name: generated_date
        type: string
        default: Today
    rows:
      - cells:
          - value: "Generated: ${generated_date}"
            style: footer
            colspan: 3

sheets:
  - name: Report
    components:
      - "header:title=Monthly Budget,subtitle=December 2025"
      - "footer:generated_date=2025-12-01"

    header:
      cells:
        - value: Category
        - value: Budget
        - value: Actual
"""

    print("\n1. Loading template with components:")
    loader = TemplateLoader()
    template = loader.load_from_string(yaml_content)

    print(f"   Template: {template.name}")
    print(f"   Components defined: {len(template.components)}")
    for comp_name, comp in template.components.items():
        print(f"     • {comp_name}: {comp.description}")
        print(f"       Variables: {len(comp.variables)}")
        print(f"       Rows: {len(comp.rows)}")

    # 2. Render template with components
    print("\n2. Rendering template with components:")
    from spreadsheet_dl.template_engine.renderer import TemplateRenderer

    renderer = TemplateRenderer()
    try:
        result = renderer.render(template, {"title": "My Report"})
        print("   ✓ Template rendered successfully")
        print(f"   Sheets: {len(result.sheets)}")
        for sheet in result.sheets:
            print(f"     • {sheet.name}: {len(sheet.rows)} rows")
    except ValueError as e:
        print(f"   Error: {e}")

    # 3. Component inheritance and reuse
    print("\n3. Component reuse benefits:")
    print("   • Define once, use multiple times")
    print("   • Consistent styling across sheets")
    print("   • Easy maintenance and updates")
    print("   • Variable substitution per usage")

    print("\n✓ Component composition demonstrated")
    print()


# ============================================================================
# Example 5: Complete Template Example
# ============================================================================


def example_complete_template() -> None:
    """
    Demonstrate a complete budget template.

    Shows:
    - Full template structure
    - Variable validation
    - Sheet rendering
    - Formulas in templates
    - Styling
    """
    from spreadsheet_dl.template_engine.loader import TemplateLoader
    from spreadsheet_dl.template_engine.renderer import TemplateRenderer

    print("=" * 70)
    print("Example 5: Complete Budget Template")
    print("=" * 70)

    # Create comprehensive budget template
    yaml_content = """
meta:
  name: Monthly Budget Template
  version: 2.0.0
  description: Complete monthly budget with categories and analysis
  author: SpreadsheetDL
  theme: professional

variables:
  - name: month
    type: integer
    description: Month number (1-12)
    required: true
    validation: "1 <= value <= 12"

  - name: year
    type: integer
    description: Year
    required: true

  - name: categories
    type: list
    description: Budget categories
    default: ["Housing", "Food", "Transportation", "Entertainment"]

  - name: currency_symbol
    type: string
    description: Currency symbol
    default: "$"

styles:
  header:
    font_weight: bold
    background_color: "#4472C4"
    font_color: "#FFFFFF"

  total:
    font_weight: bold
    border_top: "2pt solid #000000"

  currency:
    format_code: "$#,##0.00"

sheets:
  - name: ${month_name(month)} ${year} Budget
    freeze_rows: 1
    freeze_cols: 1

    columns:
      - name: Category
        width: 5cm
      - name: Budgeted
        width: 3cm
        type: currency
      - name: Actual
        width: 3cm
        type: currency
      - name: Variance
        width: 3cm
        type: currency
      - name: "Percent of Budget"
        width: 3cm
        type: percentage

    header:
      style: header
      cells:
        - value: Category
        - value: Budgeted
        - value: Actual
        - value: Variance
        - value: Percent of Budget

    data_rows:
      repeat: 1
      cells:
        - value: ""
          type: string
        - value: ""
          type: currency
        - value: ""
          type: currency
        - formula: "=C2-B2"
          type: currency
        - formula: "=C2/B2"
          type: percentage

    total_row:
      style: total
      cells:
        - value: "TOTAL"
        - formula: "=SUM(B2:B10)"
          style: currency
        - formula: "=SUM(C2:C10)"
          style: currency
        - formula: "=SUM(D2:D10)"
          style: currency
        - formula: "=C11/B11"
          type: percentage
"""

    print("\n1. Loading complete budget template:")
    loader = TemplateLoader()
    template = loader.load_from_string(yaml_content)

    print(f"   Template: {template.name}")
    print(f"   Version: {template.version}")
    print(f"   Description: {template.description}")
    print(f"   Variables: {len(template.variables)}")
    print(f"   Sheets: {len(template.sheets)}")
    print(f"   Styles defined: {len(template.styles)}")

    # 2. Show template variables
    print("\n2. Template variables:")
    for var in template.variables:
        required_str = "required" if var.required else "optional"
        default_str = f", default={var.default}" if var.default else ""
        print(f"   • {var.name} ({var.type.value}, {required_str}{default_str})")
        print(f"     {var.description}")

    # 3. Validate and render template
    print("\n3. Rendering template with variables:")
    renderer = TemplateRenderer()

    variables = {
        "month": 12,
        "year": 2025,
        "categories": [
            "Housing",
            "Groceries",
            "Utilities",
            "Transportation",
            "Entertainment",
        ],
        "currency_symbol": "$",
    }

    try:
        result = renderer.render(template, variables)
        print("   ✓ Template rendered successfully")
        print("\n   Generated spreadsheet:")
        print(f"     Name: {result.name}")
        print(f"     Sheets: {len(result.sheets)}")

        for sheet in result.sheets:
            print(f"\n     Sheet: {sheet.name}")
            print(f"       Columns: {len(sheet.columns)}")
            for col in sheet.columns:
                print(f"         • {col['name']} ({col['width']})")
            print(f"       Rows: {len(sheet.rows)}")
            print(f"       Frozen: {sheet.freeze_rows} rows, {sheet.freeze_cols} cols")

    except ValueError as e:
        print(f"   ✗ Validation error: {e}")

    # 4. Test with missing required variable
    print("\n4. Testing variable validation:")
    try:
        result = renderer.render(template, {"year": 2025})  # Missing month
        print("   Template rendered (unexpected)")
    except ValueError as e:
        print(f"   ✓ Validation caught missing variable: {e}")

    print("\n✓ Complete template demonstrated")
    print()


# ============================================================================
# Example 6: Built-in Functions
# ============================================================================


def example_builtin_functions() -> None:
    """
    Demonstrate built-in template functions.

    Shows:
    - Date/time functions
    - String functions
    - Math functions
    - Formatting functions
    """
    from spreadsheet_dl.template_engine.renderer import (
        BUILTIN_FUNCTIONS,
        ExpressionEvaluator,
    )

    print("=" * 70)
    print("Example 6: Built-in Template Functions")
    print("=" * 70)

    print("\n1. Available built-in functions:")
    print(f"   Total functions: {len(BUILTIN_FUNCTIONS)}")
    for func_name in sorted(BUILTIN_FUNCTIONS.keys()):
        print(f"     • {func_name}()")

    # 2. Date functions
    print("\n2. Date/time functions:")
    variables = {"month": 12, "date_obj": date(2025, 12, 25)}
    evaluator = ExpressionEvaluator(variables)

    date_examples = [
        ("Month name: ${month_name(month)}", "month_name(12) → December"),
        ("Month abbrev: ${month_abbrev(month)}", "month_abbrev(12) → Dec"),
    ]

    for template, description in date_examples:
        result = evaluator.evaluate(template)
        print(f"   {description}")
        print(f"     {result}")

    # 3. String functions
    print("\n3. String manipulation functions:")
    variables["text"] = "budget report"
    evaluator = ExpressionEvaluator(variables)

    string_examples = [
        ("${upper(text)}", "BUDGET REPORT"),
        ("${lower(text)}", "budget report"),
        ("${title(text)}", "Budget Report"),
    ]

    for template, _expected in string_examples:
        result = evaluator.evaluate(template)
        print(f"   {template} → {result}")

    # 4. Math functions
    print("\n4. Math functions:")
    variables = {"values": [100, 200, 300, 400, 500], "value": -42.7}
    evaluator = ExpressionEvaluator(variables)

    math_examples = [
        ("Sum: ${sum(values)}", "sum([100,200,300,400,500])"),
        ("Min: ${min(values)}", "min([100,200,300,400,500])"),
        ("Max: ${max(values)}", "max([100,200,300,400,500])"),
        ("Abs: ${abs(value)}", "abs(-42.7)"),
        ("Round: ${round(value)}", "round(-42.7)"),
    ]

    for template, description in math_examples:
        result = evaluator.evaluate(template)
        print(f"   {description}")
        print(f"     {result}")

    # 5. Formatting functions
    print("\n5. Formatting functions:")
    variables = {"amount": 1234.56, "percent": 0.125}
    evaluator = ExpressionEvaluator(variables)

    format_examples = [
        ("${format_currency(amount)}", "$1,234.56"),
        ("${format_currency(amount, '€')}", "€1,234.56"),
        ("${format_percentage(percent)}", "12.5%"),
        ("${format_percentage(percent, 2)}", "12.50%"),
    ]

    for template, _expected in format_examples:
        result = evaluator.evaluate(template)
        print(f"   {template} → {result}")

    print("\n✓ Built-in functions demonstrated")
    print()


# ============================================================================
# Example 7: Custom Template Creation
# ============================================================================


def example_custom_template() -> None:
    """
    Demonstrate creating custom templates programmatically.

    Shows:
    - Building template objects in code
    - Custom variables and validation
    - Dynamic sheet generation
    - Template export to YAML
    """
    from spreadsheet_dl.template_engine.schema import (
        CellTemplate,
        ColumnTemplate,
        RowTemplate,
        SheetTemplate,
        SpreadsheetTemplate,
        TemplateVariable,
        VariableType,
    )

    print("=" * 70)
    print("Example 7: Custom Template Creation")
    print("=" * 70)

    # 1. Create template programmatically
    print("\n1. Creating template programmatically:")

    # Define variables
    variables = [
        TemplateVariable(
            name="report_title",
            type=VariableType.STRING,
            description="Report title",
            required=True,
        ),
        TemplateVariable(
            name="num_rows",
            type=VariableType.NUMBER,
            description="Number of data rows",
            default=10,
        ),
    ]

    # Define columns
    columns = [
        ColumnTemplate(name="ID", width="2cm", type="integer"),
        ColumnTemplate(name="Description", width="6cm", type="string"),
        ColumnTemplate(name="Amount", width="3cm", type="currency"),
    ]

    # Define header row
    header_row = RowTemplate(
        cells=[
            CellTemplate(value="ID", style="header"),
            CellTemplate(value="Description", style="header"),
            CellTemplate(value="Amount", style="header"),
        ],
    )

    # Define data rows
    data_rows = RowTemplate(
        cells=[
            CellTemplate(value="", type="integer"),
            CellTemplate(value="", type="string"),
            CellTemplate(value="", type="currency"),
        ],
        repeat=10,
    )

    # Define total row
    total_row = RowTemplate(
        cells=[
            CellTemplate(value="TOTAL", style="total", colspan=2),
            CellTemplate(formula="=SUM(C2:C11)", style="total"),
        ],
    )

    # Create sheet
    sheet = SheetTemplate(
        name="${report_title}",
        columns=columns,
        header_row=header_row,
        data_rows=data_rows,
        total_row=total_row,
        freeze_rows=1,
    )

    # Create template
    template = SpreadsheetTemplate(
        name="Custom Report Template",
        version="1.0.0",
        description="Programmatically created template",
        variables=variables,
        sheets=[sheet],
        styles={
            "header": {
                "font_weight": "bold",
                "background_color": "#4472C4",
                "font_color": "#FFFFFF",
            },
            "total": {"font_weight": "bold", "border_top": "2pt solid #000000"},
        },
    )

    print(f"   Template created: {template.name}")
    print(f"   Variables: {len(template.variables)}")
    print(f"   Sheets: {len(template.sheets)}")
    print(f"   Columns: {len(template.sheets[0].columns)}")

    # 2. Validate template
    print("\n2. Validating template:")
    test_vars = {"report_title": "My Custom Report"}
    errors = template.validate_variables(test_vars)

    if errors:
        print(f"   ✗ Validation errors: {errors}")
    else:
        print("   ✓ Template validation passed")

    # 3. Render template
    print("\n3. Rendering custom template:")
    from spreadsheet_dl.template_engine.renderer import TemplateRenderer

    renderer = TemplateRenderer()
    result = renderer.render(template, test_vars)

    print("   ✓ Template rendered")
    print(f"   Sheet name: {result.sheets[0].name}")
    print(f"   Rows generated: {len(result.sheets[0].rows)}")

    print("\n✓ Custom template creation demonstrated")
    print()


# ============================================================================
# Example 8: Error Handling and Validation
# ============================================================================


def example_error_handling() -> None:
    """
    Demonstrate error handling and validation.

    Shows:
    - Variable validation
    - Type checking
    - Missing variable handling
    - Invalid template handling
    """
    from spreadsheet_dl.template_engine.loader import TemplateLoader
    from spreadsheet_dl.template_engine.renderer import TemplateRenderer

    print("=" * 70)
    print("Example 8: Error Handling and Validation")
    print("=" * 70)

    yaml_content = """
meta:
  name: Validation Demo
  version: 1.0.0

variables:
  - name: required_field
    type: string
    required: true

  - name: month
    type: integer
    validation: "1 <= value <= 12"

  - name: amount
    type: number
    validation: "value >= 0"

sheets:
  - name: Test
    header:
      cells:
        - value: ${required_field}
"""

    loader = TemplateLoader()
    template = loader.load_from_string(yaml_content)
    renderer = TemplateRenderer()

    # 1. Missing required variable
    print("\n1. Testing missing required variable:")
    try:
        result = renderer.render(template, {"month": 5})
        print("   Template rendered (unexpected)")
    except ValueError as e:
        print(f"   ✓ Caught error: {e}")

    # 2. Invalid variable type
    print("\n2. Testing invalid variable type:")
    try:
        result = renderer.render(
            template, {"required_field": "Test", "month": "not a number"}
        )
        print("   Template rendered (type coercion may occur)")
    except ValueError as e:
        print(f"   ✓ Caught error: {e}")

    # 3. Variable with validation
    print("\n3. Testing variable validation:")
    # Note: Validation is defined but not enforced in current implementation
    result = renderer.render(
        template, {"required_field": "Test", "month": 5, "amount": 100}
    )
    print("   ✓ Valid values accepted")

    # 4. Invalid YAML
    print("\n4. Testing invalid YAML:")
    invalid_yaml = """
meta:
  name: Invalid
sheets:
  - name: Test
    header:
      cells:
        - invalid syntax here
"""
    try:
        template = loader.load_from_string(invalid_yaml)
        print("   Template loaded (may have defaults)")
    except Exception as e:
        print(f"   ✓ Caught error: {type(e).__name__}")

    # 5. Successful validation
    print("\n5. Testing successful validation:")
    result = renderer.render(
        template, {"required_field": "Success", "month": 12, "amount": 1000}
    )
    print("   ✓ Template rendered successfully")
    print(f"   Sheet: {result.sheets[0].name}")

    print("\n✓ Error handling demonstrated")
    print()


# ============================================================================
# Main Example Runner
# ============================================================================


def main() -> None:
    """Run all template engine examples."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print(
        "║" + "  Template Engine Usage Examples - SpreadsheetDL v4.0".center(68) + "║"
    )
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    try:
        # Run all examples
        example_basic_template_loading()
        example_variable_substitution()
        example_conditional_rendering()
        example_component_composition()
        example_complete_template()
        example_builtin_functions()
        example_custom_template()
        example_error_handling()

        print("=" * 70)
        print("All Template Engine Examples Completed Successfully!")
        print("=" * 70)
        print()
        print("Key Features Demonstrated:")
        print("  • YAML-based template definition")
        print("  • Variable substitution with ${...} syntax")
        print("  • Built-in functions for dates, strings, math, formatting")
        print("  • Conditional rendering with if/else blocks")
        print("  • Reusable components for DRY templates")
        print("  • Template validation and error handling")
        print("  • Programmatic template creation")
        print()
        print("Template Engine Benefits:")
        print("  • Reusable spreadsheet templates")
        print("  • No code duplication")
        print("  • Type-safe variable system")
        print("  • Easy maintenance and updates")
        print("  • Version control friendly (YAML)")
        print()
        print("Common Use Cases:")
        print("  • Monthly budget templates")
        print("  • Invoice generators")
        print("  • Report templates")
        print("  • Data entry forms")
        print("  • Financial statements")
        print()

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
