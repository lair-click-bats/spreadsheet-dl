"""
Structural analysis template for member forces and reactions.

Implements:
    StructuralAnalysisTemplate with force and stress calculations
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class StructuralAnalysisTemplate(BaseTemplate):
    """
    Structural analysis template for forces, reactions, and deflections.

    Implements:
        StructuralAnalysisTemplate requirements

    Features:
        - Columns: Member ID, Type, Length, Axial Force, Shear Force,
          Moment, Deflection, Stress, Unity Check, Status
        - Auto-calculation: Stress, Unity Check (demand/capacity)
        - Support reactions summary
        - Member capacity checks
        - Conditional formatting for overstressed members

    Example:
        >>> template = StructuralAnalysisTemplate(
        ...     project_name="Truss Bridge",
        ...     num_members=50
        ... )
        >>> builder = template.generate()
        >>> builder.save("structural_analysis.ods")
    """

    project_name: str = "Structural System"
    num_members: int = 30
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Structural Analysis",
            description="Member forces, reactions, deflections, and stress checks",
            category="civil_engineering",
            tags=("structural", "analysis", "forces", "stress", "deflection"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate structural analysis spreadsheet.

        Returns:
            SpreadsheetBuilder configured with structural analysis template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Structural Analysis - {self.project_name}",
            author="Structural Engineering Department",
            subject="Structural Analysis Results",
            description=f"Member forces and stress checks for {self.project_name}",
            keywords=["structural", "analysis", "forces", self.project_name],
        )

        # Create main analysis sheet
        builder.sheet("Member Forces")

        # Define columns
        builder.column("Member ID", width="80pt", style="text")
        builder.column("Type", width="80pt", style="text")
        builder.column("Length (m)", width="80pt", type="number")
        builder.column("Axial (kN)", width="90pt", type="number")
        builder.column("Shear (kN)", width="90pt", type="number")
        builder.column("Moment (kN·m)", width="100pt", type="number")
        builder.column("Deflection (mm)", width="100pt", type="number")
        builder.column("Stress (MPa)", width="90pt", type="number")
        builder.column("Capacity (MPa)", width="100pt", type="number")
        builder.column("Unity Check", width="90pt", type="number")
        builder.column("Status", width="80pt", style="text")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Structural Analysis - {self.project_name}",
            colspan=11,
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Member ID")
        builder.cell("Type")
        builder.cell("Length (m)")
        builder.cell("Axial (kN)")
        builder.cell("Shear (kN)")
        builder.cell("Moment (kN·m)")
        builder.cell("δ (mm)")
        builder.cell("Stress (MPa)")
        builder.cell("Capacity (MPa)")
        builder.cell("Unity Check")
        builder.cell("Status")

        # Member rows
        for i in range(self.num_members):
            row_num = i + 3
            builder.row()
            builder.cell(f"M{i + 1:03d}", style="input")  # Member ID
            builder.cell("", style="input")  # Type (beam, column, brace)
            builder.cell(0, style="input")  # Length
            builder.cell(0, style="input")  # Axial force
            builder.cell(0, style="input")  # Shear force
            builder.cell(0, style="input")  # Moment
            builder.cell(0, style="input")  # Deflection
            builder.cell(0, style="input")  # Stress
            builder.cell(250, style="input")  # Capacity (default steel fy=250 MPa)
            # Unity check = Stress / Capacity
            builder.cell(f"=H{row_num}/I{row_num}", style="number")
            # Status: OK if UC < 1.0, WARNING if UC < 1.1, FAIL if UC >= 1.1
            builder.cell(
                f'=IF(J{row_num}<1.0,"OK",IF(J{row_num}<1.1,"WARNING","FAIL"))',
                style="input",
            )

        # Summary section
        total_row = self.num_members + 3
        builder.row()  # Blank row
        builder.row(style="total")
        builder.cell("SUMMARY", style="total_label", colspan=3)
        builder.cell(f"=SUM(D3:D{total_row - 1})", style="number")  # Total axial
        builder.cell(f"=SUM(E3:E{total_row - 1})", style="number")  # Total shear
        builder.cell(f"=SUM(F3:F{total_row - 1})", style="number")  # Total moment
        builder.cell(f"=MAX(G3:G{total_row - 1})", style="number")  # Max deflection
        builder.cell(f"=MAX(H3:H{total_row - 1})", style="number")  # Max stress
        builder.cell("")
        builder.cell(f"=MAX(J3:J{total_row - 1})", style="number")  # Max unity
        builder.cell("")

        # Member statistics
        builder.row()
        builder.row(style="section_header")
        builder.cell("Member Statistics", colspan=11)

        builder.row()
        builder.cell("Total Members:", colspan=2)
        builder.cell(self.num_members, style="number")
        builder.cell("")
        builder.cell("Members OK:", colspan=2)
        builder.cell(f'=COUNTIF(K3:K{total_row - 1},"OK")', style="number")

        builder.row()
        builder.cell("Max Axial Force:", colspan=2)
        builder.cell(f"=MAX(ABS(D3:D{total_row - 1}))", style="number")
        builder.cell("")
        builder.cell("Members at Warning:", colspan=2)
        builder.cell(f'=COUNTIF(K3:K{total_row - 1},"WARNING")', style="number")

        builder.row()
        builder.cell("Max Moment:", colspan=2)
        builder.cell(f"=MAX(ABS(F3:F{total_row - 1}))", style="number")
        builder.cell("")
        builder.cell("Members Failed:", colspan=2)
        builder.cell(f'=COUNTIF(K3:K{total_row - 1},"FAIL")', style="number")

        builder.row()
        builder.cell("Average Unity Check:", colspan=2)
        builder.cell(f"=AVERAGE(J3:J{total_row - 1})", style="number")
        builder.cell("")
        builder.cell("System Utilization:", colspan=2)
        builder.cell(f"=AVERAGE(J3:J{total_row - 1})", style="percentage")

        # Support reactions
        builder.row()
        builder.row(style="section_header")
        builder.cell("Support Reactions", colspan=11)

        builder.row(style="header_secondary")
        builder.cell("Support ID", colspan=2)
        builder.cell("Type", colspan=2)
        builder.cell("Rx (kN)", colspan=2)
        builder.cell("Ry (kN)", colspan=2)
        builder.cell("M (kN·m)", colspan=3)

        # Sample support reactions (user fills in)
        for i in range(5):
            builder.row()
            builder.cell(f"S{i + 1}", colspan=2, style="input")
            builder.cell("", colspan=2, style="input")  # Type (fixed, pinned, roller)
            builder.cell(0, colspan=2, style="input")  # Rx
            builder.cell(0, colspan=2, style="input")  # Ry
            builder.cell(0, colspan=3, style="input")  # Moment

        # Reaction totals
        builder.row(style="total")
        builder.cell("TOTALS", colspan=4, style="total_label")
        react_total_row = total_row + 11
        builder.cell(
            f"=SUM(E{total_row + 7}:E{react_total_row - 1})",
            colspan=2,
            style="number",
        )
        builder.cell(
            f"=SUM(G{total_row + 7}:G{react_total_row - 1})",
            colspan=2,
            style="number",
        )
        builder.cell(
            f"=SUM(I{total_row + 7}:I{react_total_row - 1})",
            colspan=3,
            style="number",
        )

        return builder

    def validate(self) -> bool:
        """Validate template configuration."""
        return self.num_members > 0


__all__ = ["StructuralAnalysisTemplate"]
