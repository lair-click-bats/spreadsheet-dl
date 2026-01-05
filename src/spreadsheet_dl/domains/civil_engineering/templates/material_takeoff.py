"""Material takeoff template for construction quantity estimation.

Implements:
    MaterialTakeoffTemplate with quantity calculations
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class MaterialTakeoffTemplate(BaseTemplate):
    """Material takeoff template for quantity estimation.

    Implements:
        MaterialTakeoffTemplate requirements

    Features:
        - Columns: Item, Description, Material Type, Length/Area/Volume,
          Unit, Quantity, Unit Weight, Total Weight, Unit Cost, Total Cost
        - Auto-calculation: Total Weight, Total Cost
        - Separate sections for concrete, rebar, formwork
        - Summary totals by material type
        - Cost analysis

    Example:
        >>> template = MaterialTakeoffTemplate(  # doctest: +SKIP
        ...     project_name="Highway Bridge",
        ...     num_items=30
        ... )
        >>> builder = template.generate()  # doctest: +SKIP
        >>> path = builder.save("material_takeoff.ods")  # doctest: +SKIP
    """

    project_name: str = "Construction Project"
    num_items: int = 25
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Material Takeoff",
            description="Construction quantity estimation and material takeoff",
            category="civil_engineering",
            tags=("materials", "quantities", "concrete", "rebar", "cost"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """Generate material takeoff spreadsheet.

        Returns:
            SpreadsheetBuilder configured with material takeoff template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Material Takeoff - {self.project_name}",
            author="Construction Engineering Department",
            subject="Quantity Estimation",
            description=f"Material takeoff and quantities for {self.project_name}",
            keywords=["materials", "quantities", "takeoff", self.project_name],
        )

        # Create main takeoff sheet
        builder.sheet("Material Takeoff")

        # Define columns
        builder.column("Item #", width="60pt", style="text")
        builder.column("Description", width="150pt", style="text")
        builder.column("Material Type", width="100pt", style="text")
        builder.column("Dimensions", width="120pt", style="text")
        builder.column("Volume (m³)", width="80pt", type="number")
        builder.column("Area (m²)", width="80pt", type="number")
        builder.column("Quantity", width="80pt", type="number")
        builder.column("Unit Weight (kg)", width="90pt", type="number")
        builder.column("Total Weight (kg)", width="100pt", type="number")
        builder.column("Unit Cost ($)", width="80pt", type="number")
        builder.column("Total Cost ($)", width="100pt", type="number")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Material Takeoff - {self.project_name}",
            colspan=11,
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Item #")
        builder.cell("Description")
        builder.cell("Material")
        builder.cell("Dimensions")
        builder.cell("Volume (m³)")
        builder.cell("Area (m²)")
        builder.cell("Qty")
        builder.cell("Unit Wt (kg)")
        builder.cell("Total Wt (kg)")
        builder.cell("Unit Cost ($)")
        builder.cell("Total Cost ($)")

        # Item rows
        for i in range(self.num_items):
            row_num = i + 3
            builder.row()
            builder.cell(f"{i + 1:03d}", style="input")  # Item number
            builder.cell("", style="input")  # Description
            builder.cell("", style="input")  # Material type
            builder.cell("", style="input")  # Dimensions
            builder.cell(0, style="input")  # Volume
            builder.cell(0, style="input")  # Area
            builder.cell(1, style="input")  # Quantity
            builder.cell(0, style="input")  # Unit weight
            # Total weight = Quantity * Unit Weight
            builder.cell(f"=G{row_num}*H{row_num}", style="number")
            builder.cell(0, style="input")  # Unit cost
            # Total cost = Quantity * Unit Cost
            builder.cell(f"=G{row_num}*J{row_num}", style="number")

        # Summary totals
        total_row = self.num_items + 3
        builder.row()  # Blank row
        builder.row(style="total")
        builder.cell("TOTALS", style="total_label", colspan=4)
        builder.cell(f"=SUM(E3:E{total_row - 1})", style="number")  # Total volume
        builder.cell(f"=SUM(F3:F{total_row - 1})", style="number")  # Total area
        builder.cell(f"=SUM(G3:G{total_row - 1})", style="number")  # Total qty
        builder.cell("")
        builder.cell(f"=SUM(I3:I{total_row - 1})", style="number")  # Total weight
        builder.cell("")
        builder.cell(f"=SUM(K3:K{total_row - 1})", style="number")  # Total cost

        # Material breakdown section
        builder.row()
        builder.row(style="section_header")
        builder.cell("Material Summary", colspan=11)

        builder.row(style="header_secondary")
        builder.cell("Material Type", colspan=2)
        builder.cell("Volume (m³)", colspan=2)
        builder.cell("Area (m²)", colspan=2)
        builder.cell("Weight (kg)", colspan=2)
        builder.cell("Cost ($)", colspan=3)

        # Concrete summary
        builder.row()
        builder.cell("Concrete", colspan=2, style="text")
        builder.cell(
            f'=SUMIF(C3:C{total_row - 1},"Concrete",E3:E{total_row - 1})',
            colspan=2,
            style="number",
        )
        builder.cell(
            f'=SUMIF(C3:C{total_row - 1},"Concrete",F3:F{total_row - 1})',
            colspan=2,
            style="number",
        )
        builder.cell(
            f'=SUMIF(C3:C{total_row - 1},"Concrete",I3:I{total_row - 1})',
            colspan=2,
            style="number",
        )
        builder.cell(
            f'=SUMIF(C3:C{total_row - 1},"Concrete",K3:K{total_row - 1})',
            colspan=3,
            style="number",
        )

        # Rebar summary
        builder.row()
        builder.cell("Rebar", colspan=2, style="text")
        builder.cell(
            f'=SUMIF(C3:C{total_row - 1},"Rebar",E3:E{total_row - 1})',
            colspan=2,
            style="number",
        )
        builder.cell(
            f'=SUMIF(C3:C{total_row - 1},"Rebar",F3:F{total_row - 1})',
            colspan=2,
            style="number",
        )
        builder.cell(
            f'=SUMIF(C3:C{total_row - 1},"Rebar",I3:I{total_row - 1})',
            colspan=2,
            style="number",
        )
        builder.cell(
            f'=SUMIF(C3:C{total_row - 1},"Rebar",K3:K{total_row - 1})',
            colspan=3,
            style="number",
        )

        # Formwork summary
        builder.row()
        builder.cell("Formwork", colspan=2, style="text")
        builder.cell(
            f'=SUMIF(C3:C{total_row - 1},"Formwork",E3:E{total_row - 1})',
            colspan=2,
            style="number",
        )
        builder.cell(
            f'=SUMIF(C3:C{total_row - 1},"Formwork",F3:F{total_row - 1})',
            colspan=2,
            style="number",
        )
        builder.cell(
            f'=SUMIF(C3:C{total_row - 1},"Formwork",I3:I{total_row - 1})',
            colspan=2,
            style="number",
        )
        builder.cell(
            f'=SUMIF(C3:C{total_row - 1},"Formwork",K3:K{total_row - 1})',
            colspan=3,
            style="number",
        )

        # Cost analysis
        builder.row()
        builder.row(style="section_header")
        builder.cell("Cost Analysis", colspan=11)

        builder.row()
        builder.cell("Average Unit Cost:", colspan=2)
        builder.cell(
            f"=K{total_row}/G{total_row}",
            style="number",
            colspan=2,
        )
        builder.cell("")
        builder.cell("Cost per m³:", colspan=2)
        builder.cell(
            f"=K{total_row}/E{total_row}",
            style="number",
            colspan=2,
        )

        builder.row()
        builder.cell("Concrete Cost %:", colspan=2)
        concrete_cost_row = total_row + 5
        builder.cell(
            f"=K{concrete_cost_row}/K{total_row}",
            style="percentage",
            colspan=2,
        )
        builder.cell("")
        builder.cell("Rebar Cost %:", colspan=2)
        rebar_cost_row = total_row + 6
        builder.cell(
            f"=K{rebar_cost_row}/K{total_row}",
            style="percentage",
            colspan=2,
        )

        return builder

    def validate(self) -> bool:
        """Validate template configuration."""
        return self.num_items > 0


__all__ = ["MaterialTakeoffTemplate"]
