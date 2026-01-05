"""
Load calculations template for civil engineering.

Implements:
    LoadCalculationsTemplate with load combinations and safety factors
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class LoadCalculationsTemplate(BaseTemplate):
    """
    Load calculations template for structural design.

    Implements:
        LoadCalculationsTemplate requirements

    Features:
        - Columns: Load Type, Description, Dead Load (kN), Live Load (kN),
          Wind Load (kN), Seismic Load (kN), Total Load, Safety Factor,
          Design Load
        - Auto-calculation: Total = sum of all loads, Design = Total * SF
        - Load combinations per ASCE 7 / Eurocode
        - Summary section with governing load combination
        - Conditional formatting for critical loads

    Example:
        >>> template = LoadCalculationsTemplate(
        ...     project_name="Office Building",
        ...     num_load_cases=15
        ... )
        >>> builder = template.generate()
        >>> builder.save("load_calculations.ods")
    """

    project_name: str = "Structural Project"
    num_load_cases: int = 20
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Load Calculations",
            description="Structural load analysis with load combinations and safety factors",
            category="civil_engineering",
            tags=("loads", "structural", "safety", "design"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate load calculations spreadsheet.

        Returns:
            SpreadsheetBuilder configured with load calculations template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Load Calculations - {self.project_name}",
            author="Structural Engineering Department",
            subject="Structural Load Analysis",
            description=f"Load calculations and combinations for {self.project_name}",
            keywords=["loads", "structural", "design", self.project_name],
        )

        # Create main load calculations sheet
        builder.sheet("Load Calculations")

        # Define columns
        builder.column("Load ID", width="80pt", style="text")
        builder.column("Description", width="150pt", style="text")
        builder.column("Dead Load (kN)", width="100pt", type="number")
        builder.column("Live Load (kN)", width="100pt", type="number")
        builder.column("Wind Load (kN)", width="100pt", type="number")
        builder.column("Seismic Load (kN)", width="110pt", type="number")
        builder.column("Total Load (kN)", width="100pt", type="number")
        builder.column("Safety Factor", width="90pt", type="number")
        builder.column("Design Load (kN)", width="110pt", type="number")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Load Calculations - {self.project_name}",
            colspan=9,
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Load ID")
        builder.cell("Description")
        builder.cell("Dead (kN)")
        builder.cell("Live (kN)")
        builder.cell("Wind (kN)")
        builder.cell("Seismic (kN)")
        builder.cell("Total (kN)")
        builder.cell("Safety Factor")
        builder.cell("Design (kN)")

        # Load case rows
        for i in range(self.num_load_cases):
            row_num = i + 3
            builder.row()
            builder.cell(f"LC{i + 1:02d}", style="input")  # Load ID
            builder.cell("", style="input")  # Description
            builder.cell(0, style="input")  # Dead load
            builder.cell(0, style="input")  # Live load
            builder.cell(0, style="input")  # Wind load
            builder.cell(0, style="input")  # Seismic load
            # Total = sum of all loads
            builder.cell(f"=SUM(C{row_num}:F{row_num})", style="number")
            builder.cell(1.5, style="input")  # Default safety factor
            # Design load = Total * SF
            builder.cell(f"=G{row_num}*H{row_num}", style="number")

        # Summary section
        total_row = self.num_load_cases + 3
        builder.row()  # Blank row
        builder.row(style="total")
        builder.cell("TOTALS", style="total_label", colspan=2)
        builder.cell(f"=SUM(C3:C{total_row - 1})", style="number")  # Total dead
        builder.cell(f"=SUM(D3:D{total_row - 1})", style="number")  # Total live
        builder.cell(f"=SUM(E3:E{total_row - 1})", style="number")  # Total wind
        builder.cell(f"=SUM(F3:F{total_row - 1})", style="number")  # Total seismic
        builder.cell(f"=SUM(G3:G{total_row - 1})", style="number")  # Total load
        builder.cell("")
        builder.cell(f"=SUM(I3:I{total_row - 1})", style="number")  # Total design

        # Load combination analysis
        builder.row()
        builder.row(style="section_header")
        builder.cell("Load Combinations (ASCE 7-16)", colspan=9)

        # Combination 1: 1.4D
        combo_row = total_row + 3
        builder.row()
        builder.cell("Combo 1", colspan=2)
        builder.cell("1.4D", colspan=3)
        builder.cell("")
        builder.cell("")
        builder.cell("=", style="text")
        builder.cell(f"=1.4*C{total_row}", style="number")

        # Combination 2: 1.2D + 1.6L
        builder.row()
        builder.cell("Combo 2", colspan=2)
        builder.cell("1.2D + 1.6L", colspan=3)
        builder.cell("")
        builder.cell("")
        builder.cell("=", style="text")
        builder.cell(f"=1.2*C{total_row}+1.6*D{total_row}", style="number")

        # Combination 3: 1.2D + L + 1.0W
        builder.row()
        builder.cell("Combo 3", colspan=2)
        builder.cell("1.2D + L + 1.0W", colspan=3)
        builder.cell("")
        builder.cell("")
        builder.cell("=", style="text")
        builder.cell(f"=1.2*C{total_row}+D{total_row}+E{total_row}", style="number")

        # Combination 4: 1.2D + L + E (seismic)
        builder.row()
        builder.cell("Combo 4", colspan=2)
        builder.cell("1.2D + L + E", colspan=3)
        builder.cell("")
        builder.cell("")
        builder.cell("=", style="text")
        builder.cell(f"=1.2*C{total_row}+D{total_row}+F{total_row}", style="number")

        # Combination 5: 0.9D + 1.0W
        builder.row()
        builder.cell("Combo 5", colspan=2)
        builder.cell("0.9D + 1.0W", colspan=3)
        builder.cell("")
        builder.cell("")
        builder.cell("=", style="text")
        builder.cell(f"=0.9*C{total_row}+E{total_row}", style="number")

        # Governing combination
        builder.row()
        builder.row(style="section_header")
        builder.cell("Governing Load Combination", colspan=9)

        builder.row()
        builder.cell("Maximum Design Load:", colspan=3)
        builder.cell(
            f"=MAX(I{combo_row}:I{combo_row + 4})",
            style="number",
            colspan=2,
        )
        builder.cell("")
        builder.cell("Utilization Ratio:", colspan=2)
        builder.cell("", style="input")  # User enters capacity

        # Statistics
        builder.row()
        builder.row(style="section_header")
        builder.cell("Load Statistics", colspan=9)

        builder.row()
        builder.cell("Average Total Load:", colspan=2)
        builder.cell(f"=AVERAGE(G3:G{total_row - 1})", style="number")
        builder.cell("")
        builder.cell("Max Single Load:", colspan=2)
        builder.cell(f"=MAX(G3:G{total_row - 1})", style="number")

        builder.row()
        builder.cell("Dead/Total Ratio:", colspan=2)
        builder.cell(f"=C{total_row}/G{total_row}", style="percentage")
        builder.cell("")
        builder.cell("Live/Total Ratio:", colspan=2)
        builder.cell(f"=D{total_row}/G{total_row}", style="percentage")

        return builder

    def validate(self) -> bool:
        """Validate template configuration."""
        return self.num_load_cases > 0


__all__ = ["LoadCalculationsTemplate"]
