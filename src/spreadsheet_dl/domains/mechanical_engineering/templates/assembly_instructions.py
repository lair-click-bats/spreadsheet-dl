"""
Assembly Instructions template for mechanical engineering.

Implements:
    REQ-C003-004: AssemblyInstructionsTemplate with step-by-step assembly
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class AssemblyInstructionsTemplate(BaseTemplate):
    """
    Assembly Instructions template for mechanical assemblies.

    Generates step-by-step assembly instructions with torque specifications,
    sequence numbers, tools required, and time estimates.

    Implements:
        REQ-C003-004: AssemblyInstructionsTemplate requirements

    Features:
        - Sequential step numbering
        - Part/component references
        - Torque specifications (N·m)
        - Tool requirements
        - Time estimates per step
        - Total assembly time calculation
        - Critical step flagging

    Example:
        >>> template = AssemblyInstructionsTemplate(assembly_name="Motor Assembly")
        >>> builder = template.generate()
        >>> builder.save("assembly_instructions.ods")
    """

    assembly_name: str = "Mechanical Assembly"
    num_steps: int = 15
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Assembly Instructions",
            description="Step-by-step assembly instructions with torque specs and tooling",
            category="mechanical_engineering",
            tags=("assembly", "instructions", "manufacturing", "torque"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate assembly instructions spreadsheet.

        Returns:
            SpreadsheetBuilder configured with assembly instructions template

        Implements:
            REQ-C003-004: Assembly instructions template generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Assembly Instructions - {self.assembly_name}",
            author="Manufacturing Department",
            subject="Assembly Instructions",
            description=f"Step-by-step assembly instructions for {self.assembly_name}",
            keywords=["assembly", "instructions", "manufacturing", self.assembly_name],
        )

        # Create main assembly sheet
        builder.sheet("Assembly Steps")

        # Define columns
        builder.column("Step #", width="50pt", style="text")
        builder.column("Description", width="250pt", style="text")
        builder.column("Parts/Components", width="150pt", style="text")
        builder.column("Torque (N·m)", width="90pt", type="number")
        builder.column("Tools Required", width="150pt", style="text")
        builder.column("Time (min)", width="80pt", type="number")
        builder.column("Critical", width="70pt", style="text")
        builder.column("Notes", width="200pt", style="text")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Assembly Instructions - {self.assembly_name}", colspan=8)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Step #")
        builder.cell("Description")
        builder.cell("Parts/Components")
        builder.cell("Torque (N·m)")
        builder.cell("Tools Required")
        builder.cell("Time (min)")
        builder.cell("Critical")
        builder.cell("Notes")

        # Assembly step rows
        for i in range(self.num_steps):
            builder.row()
            builder.cell(i + 1)  # Auto-numbered step
            builder.cell("", style="input")  # Description
            builder.cell("", style="input")  # Parts/Components
            builder.cell(0, style="input")  # Torque
            builder.cell("", style="input")  # Tools Required
            builder.cell(0, style="input")  # Time estimate
            builder.cell("", style="input")  # Critical flag (Yes/No)
            builder.cell("", style="input")  # Notes

        # Summary section
        total_row = self.num_steps + 3
        builder.row()  # Blank row

        builder.row(style="total")
        builder.cell("TOTALS", colspan=5, style="total_label")
        builder.cell(f"=SUM(F3:F{total_row - 1})", style="number")  # Total time
        builder.cell("")
        builder.cell("")

        # Statistics section
        builder.row()
        builder.row(style="section_header")
        builder.cell("Assembly Summary", colspan=8)

        builder.row()
        builder.cell("Total Steps:", colspan=2)
        builder.cell(f"=COUNTA(B3:B{total_row - 1})", style="number")
        builder.cell("")
        builder.cell("Total Assembly Time:", colspan=2)
        builder.cell(f"=SUM(F3:F{total_row - 1})", style="number")
        builder.cell("minutes")

        builder.row()
        builder.cell("Critical Steps:", colspan=2)
        builder.cell(f'=COUNTIF(G3:G{total_row - 1};"Yes")', style="number")
        builder.cell("")
        builder.cell("Average Step Time:", colspan=2)
        builder.cell(f"=AVERAGE(F3:F{total_row - 1})", style="number")
        builder.cell("minutes")

        builder.row()
        builder.cell("Max Torque Required:", colspan=2)
        builder.cell(f"=MAX(D3:D{total_row - 1})", style="number")
        builder.cell("N·m")
        builder.cell("Estimated Labor Hours:", colspan=2)
        builder.cell(f"=SUM(F3:F{total_row - 1})/60", style="number")
        builder.cell("hours")

        # Reference notes
        builder.row()
        builder.row(style="section_header")
        builder.cell("Assembly Notes", colspan=8)

        builder.row()
        builder.cell(
            "Torque Specifications: Apply specified torque using calibrated torque wrench",
            colspan=8,
        )

        builder.row()
        builder.cell(
            "Critical Steps: Steps marked 'Yes' require additional verification and QC",
            colspan=8,
        )

        builder.row()
        builder.cell(
            "Time Estimates: Include handling, positioning, and fastening time",
            colspan=8,
        )

        builder.row()
        builder.cell(
            "Sequence: Follow steps in numerical order unless otherwise specified",
            colspan=8,
        )

        return builder

    def validate(self) -> bool:
        """
        Validate template configuration.

        Returns:
            True if configuration is valid
        """
        return self.num_steps > 0 and len(self.assembly_name) > 0


__all__ = ["AssemblyInstructionsTemplate"]
