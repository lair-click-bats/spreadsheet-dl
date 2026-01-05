"""
Manufacturing Specifications template for mechanical engineering.

Implements:
    ManufacturingSpecsTemplate with part specifications
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class ManufacturingSpecsTemplate(BaseTemplate):
    """
    Manufacturing Specifications template for part production.

    Generates manufacturing specifications with dimensions, tolerances,
    surface finish, and material specifications.

    Implements:
        ManufacturingSpecsTemplate requirements

    Features:
        - Part identification and revision control
        - Dimensional specifications with tolerances
        - Surface finish requirements (Ra)
        - Material specifications and heat treatment
        - Manufacturing process notes
        - Critical characteristic flagging
        - Inspection requirements

    Example:
        >>> template = ManufacturingSpecsTemplate(part_name="Shaft Assembly")
        >>> builder = template.generate()
        >>> builder.save("manufacturing_specs.ods")
    """

    part_name: str = "Part Specification"
    part_number: str = "PN-001"
    revision: str = "A"
    num_features: int = 15
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Manufacturing Specifications",
            description="Part manufacturing specifications with dimensions and tolerances",
            category="mechanical_engineering",
            tags=("manufacturing", "specifications", "tolerances", "quality"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate manufacturing specifications spreadsheet.

        Returns:
            SpreadsheetBuilder configured with manufacturing specs template

        Implements:
            Manufacturing specs template generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Manufacturing Specs - {self.part_name} ({self.part_number})",
            author="Engineering Department",
            subject="Manufacturing Specifications",
            description=f"Manufacturing specifications for {self.part_name}",
            keywords=[
                "manufacturing",
                "specifications",
                "tolerances",
                self.part_name,
            ],
        )

        # Create main specs sheet
        builder.sheet("Manufacturing Specs")

        # Define columns
        builder.column("Feature", width="150pt", style="text")
        builder.column("Dimension", width="100pt", style="text")
        builder.column("Nominal (mm)", width="90pt", type="number")
        builder.column("Tolerance (±mm)", width="100pt", type="number")
        builder.column("Surface Finish (Ra μm)", width="140pt", type="number")
        builder.column("Material Spec", width="120pt", style="text")
        builder.column("Critical", width="70pt", style="text")
        builder.column("Inspection", width="100pt", style="text")
        builder.column("Notes", width="200pt", style="text")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Manufacturing Specifications - {self.part_name} ({self.part_number} Rev {self.revision})",
            colspan=9,
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Feature")
        builder.cell("Dimension")
        builder.cell("Nominal (mm)")
        builder.cell("Tolerance (±mm)")
        builder.cell("Surface Finish (Ra μm)")
        builder.cell("Material Spec")
        builder.cell("Critical")
        builder.cell("Inspection")
        builder.cell("Notes")

        # Feature specification rows
        for _i in range(self.num_features):
            builder.row()
            builder.cell("", style="input")  # Feature
            builder.cell("", style="input")  # Dimension type (OD, ID, Length, etc.)
            builder.cell(0, style="input")  # Nominal
            builder.cell(0, style="input")  # Tolerance
            builder.cell(0, style="input")  # Surface finish
            builder.cell("", style="input")  # Material spec
            builder.cell("", style="input")  # Critical (Yes/No)
            builder.cell("", style="input")  # Inspection method
            builder.cell("", style="input")  # Notes

        # Summary section
        data_end = self.num_features + 2
        builder.row()  # Blank row

        builder.row(style="section_header")
        builder.cell("Specification Summary", colspan=9)

        builder.row()
        builder.cell("Total Features:", colspan=2)
        builder.cell(f"=COUNTA(A3:A{data_end})", style="number")
        builder.cell("")
        builder.cell("Critical Features:", colspan=2)
        builder.cell(f'=COUNTIF(G3:G{data_end};"Yes")', style="number")

        builder.row()
        builder.cell("Tightest Tolerance:", colspan=2)
        builder.cell(
            f"=MIN(IF(D3:D{data_end}>0;D3:D{data_end};999))",
            style="number",
        )
        builder.cell("mm")
        builder.cell("Best Surface Finish:", colspan=2)
        builder.cell(
            f"=MIN(IF(E3:E{data_end}>0;E3:E{data_end};999))",
            style="number",
        )
        builder.cell("μm")

        builder.row()
        builder.cell("Average Tolerance:", colspan=2)
        builder.cell(f"=AVERAGE(D3:D{data_end})", style="number")
        builder.cell("mm")
        builder.cell("Average Surface Finish:", colspan=2)
        builder.cell(f"=AVERAGE(E3:E{data_end})", style="number")
        builder.cell("μm")

        # Part information section
        builder.row()
        builder.row(style="section_header")
        builder.cell("Part Information", colspan=9)

        builder.row()
        builder.cell("Part Name:", colspan=2)
        builder.cell(self.part_name, colspan=3)
        builder.cell("Part Number:", colspan=2)
        builder.cell(self.part_number, colspan=2)

        builder.row()
        builder.cell("Revision:", colspan=2)
        builder.cell(self.revision)
        builder.cell("")
        builder.cell("")
        builder.cell("Date:", colspan=2)
        builder.cell("=TODAY()", style="date")

        # Reference notes
        builder.row()
        builder.row(style="section_header")
        builder.cell("Reference Notes", colspan=9)

        builder.row()
        builder.cell(
            "Surface Finish: Ra (Roughness Average) measured in micrometers (μm)",
            colspan=9,
        )

        builder.row()
        builder.cell(
            "Typical Ra values: Rough machining 3.2-6.3, Finish machining 0.8-1.6, Grinding 0.2-0.8, Polishing <0.1",
            colspan=9,
        )

        builder.row()
        builder.cell(
            "Critical Features: Require 100% inspection and SPC monitoring",
            colspan=9,
        )

        builder.row()
        builder.cell(
            "Inspection Methods: CMM (Coordinate Measuring Machine), Micrometer, Caliper, Profilometer",
            colspan=9,
        )

        builder.row()
        builder.cell(
            "Tolerances: Unless otherwise specified, dimensions in millimeters (mm)",
            colspan=9,
        )

        return builder

    def validate(self) -> bool:
        """
        Validate template configuration.

        Returns:
            True if configuration is valid
        """
        return (
            self.num_features > 0
            and len(self.part_name) > 0
            and len(self.part_number) > 0
        )


__all__ = ["ManufacturingSpecsTemplate"]
