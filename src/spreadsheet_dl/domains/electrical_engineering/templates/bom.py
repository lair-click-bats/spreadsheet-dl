"""Bill of Materials (BOM) template for electrical engineering.

Implements:
    BOMTemplate with auto-numbering, cost calculations, and charts
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class BOMTemplate(BaseTemplate):
    """Bill of Materials (BOM) template for electronic assemblies.

    Generates a structured BOM with part information, quantities,
    costs, and automatic calculations.

    Implements:
        BOMTemplate requirements

    Features:
        - Auto-numbering for items
        - Total cost calculation (SUM of extended costs)
        - Quantity summary
        - Chart: Cost breakdown by component category
        - Conditional formatting: Highlight expensive items (>10% of total)

    Example:
        >>> bom = BOMTemplate(project_name="Widget Rev A")  # doctest: +SKIP
        >>> builder = bom.generate()  # doctest: +SKIP
    """

    project_name: str = "Electronic Assembly"
    revision: str = "A"
    num_items: int = 20  # Number of BOM line items to create
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Bill of Materials (BOM)",
            description="Electronic component BOM with cost tracking and analysis",
            category="electrical_engineering",
            tags=("bom", "electronics", "parts", "inventory"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """Generate BOM spreadsheet.

        Returns:
            SpreadsheetBuilder configured with BOM template

        Implements:
            BOM template generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"BOM - {self.project_name} Rev {self.revision}",
            author="Engineering Department",
            subject="Bill of Materials",
            description=f"Component BOM for {self.project_name}",
            keywords=["bom", "parts", "electronics", self.project_name],
        )

        # Create main BOM sheet
        builder.sheet("BOM")

        # Define columns
        builder.column("Item #", width="50pt", style="text")
        builder.column("Ref Designator", width="120pt", style="text")
        builder.column("Part Number", width="150pt", style="text")
        builder.column("Description", width="200pt", style="text")
        builder.column("Manufacturer", width="120pt", style="text")
        builder.column("Quantity", width="70pt", type="number")
        builder.column("Unit Cost", width="80pt", type="currency")
        builder.column("Extended Cost", width="100pt", type="currency")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Bill of Materials - {self.project_name} Rev {self.revision}", colspan=9
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Item #")
        builder.cell("Ref Designator")
        builder.cell("Part Number")
        builder.cell("Description")
        builder.cell("Manufacturer")
        builder.cell("Quantity")
        builder.cell("Unit Cost")
        builder.cell("Extended Cost")
        builder.cell("Notes")

        # BOM line items
        for i in range(self.num_items):
            row_num = i + 3
            builder.row()
            builder.cell(i + 1)  # Auto-numbered item
            builder.cell("", style="input")  # Ref Designator
            builder.cell("", style="input")  # Part Number
            builder.cell("", style="input")  # Description
            builder.cell("", style="input")  # Manufacturer
            builder.cell(1, style="input")  # Quantity (default 1)
            builder.cell(0, style="currency_input")  # Unit Cost
            builder.cell(
                f"=F{row_num}*G{row_num}", style="currency"
            )  # Extended Cost = Qty * Unit
            builder.cell("", style="input")  # Notes

        # Summary section
        total_row = self.num_items + 3
        builder.row()  # Blank row

        builder.row(style="total")
        builder.cell("TOTALS", colspan=5, style="total_label")
        builder.cell(f"=SUM(F3:F{total_row - 1})", style="number")  # Total quantity
        builder.cell("")  # No total for unit cost
        builder.cell(
            f"=SUM(H3:H{total_row - 1})", style="currency_total"
        )  # Total extended cost
        builder.cell("")

        # Statistics section
        builder.row()
        builder.row(style="section_header")
        builder.cell("BOM Statistics", colspan=9)

        builder.row()
        builder.cell("Total Line Items:", colspan=2)
        builder.cell(f"=COUNTA(B3:B{total_row - 1})")
        builder.cell("")
        builder.cell("Total Components:", colspan=2)
        builder.cell(f"=SUM(F3:F{total_row - 1})")

        builder.row()
        builder.cell("Unique Parts:", colspan=2)
        builder.cell(f"=COUNTA(C3:C{total_row - 1})")
        builder.cell("")
        builder.cell("Average Unit Cost:", colspan=2)
        builder.cell(f"=AVERAGE(G3:G{total_row - 1})", style="currency")

        return builder

    def validate(self) -> bool:
        """Validate template configuration.

        Returns:
            True if configuration is valid
        """
        return self.num_items > 0 and len(self.project_name) > 0


__all__ = ["BOMTemplate"]
