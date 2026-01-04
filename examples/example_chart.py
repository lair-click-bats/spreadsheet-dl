#!/usr/bin/env python3
"""
Example: Create charts programmatically.

This demonstrates using the chart builder API to create
spreadsheets with embedded charts.
"""

from decimal import Decimal
from pathlib import Path

from spreadsheet_dl import ChartType, chart, create_spreadsheet


def main() -> None:
    """Create budget with charts."""

    # Create spreadsheet
    builder = create_spreadsheet(theme="default")

    # Add expense data
    builder.sheet("Monthly Expenses").column("Category", width="3cm").column(
        "Budget", width="2.5cm", type="currency"
    ).column("Actual", width="2.5cm", type="currency").column(
        "Difference", width="2.5cm", type="currency"
    ).header_row(style="header_primary").row().cell("Housing").cell(
        Decimal("1800")
    ).cell(Decimal("1800")).cell(Decimal("0")).row().cell("Groceries").cell(
        Decimal("600")
    ).cell(Decimal("645")).cell(Decimal("-45")).row().cell("Dining Out").cell(
        Decimal("200")
    ).cell(Decimal("328")).cell(Decimal("-128")).row().cell("Transportation").cell(
        Decimal("400")
    ).cell(Decimal("245")).cell(Decimal("155")).row().cell("Entertainment").cell(
        Decimal("150")
    ).cell(Decimal("98")).cell(Decimal("52")).row().cell("Utilities").cell(
        Decimal("250")
    ).cell(Decimal("286")).cell(Decimal("-36")).row().cell("Healthcare").cell(
        Decimal("200")
    ).cell(Decimal("125")).cell(Decimal("75"))

    # Create spending chart
    spending_chart = (
        chart()
        .title("Budget vs Actual Spending")
        .type(ChartType.COLUMN)
        .data_range("B2:C8")
        .categories_range("A2:A8")
        .legend_position("bottom")
        .size(width="15cm", height="10cm")
        .position(row=10, col=0)
    )

    # Add chart to sheet
    builder.sheet("Monthly Expenses").add_chart(spending_chart)

    # Create pie chart for spending breakdown
    builder.sheet("Category Breakdown").column("Category", width="3cm").column(
        "Amount", width="2.5cm", type="currency"
    ).header_row(style="header_primary").row().cell("Housing").cell(
        Decimal("1800")
    ).row().cell("Groceries").cell(Decimal("645")).row().cell("Dining Out").cell(
        Decimal("328")
    ).row().cell("Transportation").cell(Decimal("245")).row().cell(
        "Entertainment"
    ).cell(Decimal("98")).row().cell("Utilities").cell(Decimal("286")).row().cell(
        "Healthcare"
    ).cell(Decimal("125"))

    pie_chart = (
        chart()
        .title("Spending Distribution")
        .type(ChartType.PIE)
        .data_range("B2:B8")
        .categories_range("A2:A8")
        .show_legend(True)
        .size(width="12cm", height="10cm")
        .position(row=2, col=3)
    )

    builder.sheet("Category Breakdown").add_chart(pie_chart)

    # Save
    output_file = Path("output/budget_with_charts.ods")
    output_file.parent.mkdir(exist_ok=True)
    builder.save(output_file)

    print(f"Created budget with charts: {output_file}")
    print("\nCharts included:")
    print("  1. Column chart: Budget vs Actual (Monthly Expenses sheet)")
    print("  2. Pie chart: Spending Distribution (Category Breakdown sheet)")
    print("\nOpen in LibreOffice Calc to view the charts!")


if __name__ == "__main__":
    main()
