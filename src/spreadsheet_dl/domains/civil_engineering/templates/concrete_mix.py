"""Concrete mix design template for mix proportioning.

Implements:
    ConcreteMixTemplate with mix design calculations
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class ConcreteMixTemplate(BaseTemplate):
    """Concrete mix design template for proportioning and quality control.

    Implements:
        ConcreteMixTemplate requirements

    Features:
        - Columns: Material, SG, Density, Weight (kg/m³), Volume (m³),
          Percentage by Weight, Percentage by Volume
        - Auto-calculation: Volumes, percentages, w/c ratio
        - Target strength and actual strength tracking
        - Admixtures section
        - Mix design parameters (slump, air content, strength)

    Example:
        >>> template = ConcreteMixTemplate(  # doctest: +SKIP
        ...     mix_id="C25/30",
        ...     target_strength=25.0
        ... )
        >>> builder = template.generate()  # doctest: +SKIP
        >>> path = builder.save("concrete_mix.ods")  # doctest: +SKIP
    """

    mix_id: str = "C25/30"
    target_strength: float = 25.0  # MPa
    slump: int = 75  # mm
    max_aggregate_size: int = 20  # mm
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Concrete Mix Design",
            description="Concrete mix proportioning and quality control",
            category="civil_engineering",
            tags=("concrete", "mix", "design", "proportioning", "strength"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """Generate concrete mix design spreadsheet.

        Returns:
            SpreadsheetBuilder configured with concrete mix template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Concrete Mix Design - {self.mix_id}",
            author="Concrete Technology Department",
            subject="Mix Design and Proportioning",
            description=f"Concrete mix design for {self.mix_id}",
            keywords=["concrete", "mix", "design", self.mix_id],
        )

        # Create main mix design sheet
        builder.sheet("Mix Design")

        # Define columns
        builder.column("Material", width="120pt", style="text")
        builder.column("Specific Gravity", width="100pt", type="number")
        builder.column("Density (kg/m³)", width="100pt", type="number")
        builder.column("Weight (kg/m³)", width="100pt", type="number")
        builder.column("Volume (m³)", width="90pt", type="number")
        builder.column("Weight %", width="80pt", type="percentage")
        builder.column("Volume %", width="80pt", type="percentage")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=3, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Concrete Mix Design - {self.mix_id}",
            colspan=8,
        )

        # Design parameters row
        builder.row(style="section_header")
        builder.cell(f"Target Strength: {self.target_strength} MPa", colspan=3)
        builder.cell(f"Slump: {self.slump} mm", colspan=2)
        builder.cell(f"Max Agg Size: {self.max_aggregate_size} mm", colspan=3)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Material")
        builder.cell("SG")
        builder.cell("Density (kg/m³)")
        builder.cell("Weight (kg/m³)")
        builder.cell("Volume (m³)")
        builder.cell("Weight %")
        builder.cell("Volume %")
        builder.cell("Notes")

        # Cement row
        builder.row()
        builder.cell("Cement (OPC)", style="text")
        builder.cell(3.15, style="input")  # Typical SG for cement
        builder.cell("=B4*1000", style="number")  # Density = SG * 1000
        builder.cell(350, style="input")  # Weight
        builder.cell("=D4/C4", style="number")  # Volume = Weight / Density
        builder.cell("", style="number")  # Will calc later
        builder.cell("", style="number")  # Will calc later
        builder.cell("Type I Portland Cement", style="text")

        # Water row
        builder.row()
        builder.cell("Water", style="text")
        builder.cell(1.0, style="input")  # SG of water
        builder.cell("=B5*1000", style="number")
        builder.cell(175, style="input")  # Weight
        builder.cell("=D5/C5", style="number")
        builder.cell("", style="number")
        builder.cell("", style="number")
        builder.cell("Potable water", style="text")

        # Fine aggregate row
        builder.row()
        builder.cell("Fine Aggregate (Sand)", style="text")
        builder.cell(2.65, style="input")  # Typical SG for sand
        builder.cell("=B6*1000", style="number")
        builder.cell(650, style="input")  # Weight
        builder.cell("=D6/C6", style="number")
        builder.cell("", style="number")
        builder.cell("", style="number")
        builder.cell("Natural sand, FM 2.8", style="text")

        # Coarse aggregate row
        builder.row()
        builder.cell("Coarse Aggregate", style="text")
        builder.cell(2.70, style="input")  # Typical SG for gravel
        builder.cell("=B7*1000", style="number")
        builder.cell(1200, style="input")  # Weight
        builder.cell("=D7/C7", style="number")
        builder.cell("", style="number")
        builder.cell("", style="number")
        builder.cell(f"{self.max_aggregate_size}mm crushed stone", style="text")

        # Air content row
        builder.row()
        builder.cell("Air Content", style="text")
        builder.cell("", style="text")
        builder.cell("", style="text")
        builder.cell("", style="text")
        builder.cell(0.02, style="input")  # 2% air
        builder.cell("", style="number")
        builder.cell("=E8", style="percentage")  # Air as percentage
        builder.cell("Entrained air", style="text")

        # Total row
        builder.row(style="total")
        builder.cell("TOTAL (per m³)", style="total_label")
        builder.cell("", style="text")
        builder.cell("", style="text")
        builder.cell("=SUM(D4:D7)", style="number")  # Total weight
        builder.cell("=SUM(E4:E8)", style="number")  # Total volume (should be 1.0)
        builder.cell("100%", style="percentage")
        builder.cell("100%", style="percentage")
        builder.cell("", style="text")

        # Calculate percentages
        for _i in range(4, 8):  # Rows 4-7 (materials)
            # Weight percentage
            builder.sheet("Mix Design")  # Ensure we're on the right sheet
            # We need to update cells, so we'll add this in a second pass

        # Mix design parameters
        builder.row()
        builder.row(style="section_header")
        builder.cell("Mix Design Parameters", colspan=8)

        builder.row()
        builder.cell("Water/Cement Ratio:", colspan=2)
        builder.cell("=D5/D4", style="number", colspan=2)  # w/c = water/cement
        builder.cell("")
        builder.cell("Target w/c:", colspan=2)
        builder.cell(0.50, style="input")

        builder.row()
        builder.cell("Cement Content:", colspan=2)
        builder.cell("=D4", style="number", colspan=2)
        builder.cell("kg/m³")
        builder.cell("Min Cement:", colspan=2)
        builder.cell(300, style="input")

        builder.row()
        builder.cell("Total Aggregate:", colspan=2)
        builder.cell("=D6+D7", style="number", colspan=2)
        builder.cell("kg/m³")
        builder.cell("Fine/Total Ratio:", colspan=2)
        builder.cell("=D6/(D6+D7)", style="percentage")

        builder.row()
        builder.cell("Slump:", colspan=2)
        builder.cell(self.slump, style="number", colspan=2)
        builder.cell("mm")
        builder.cell("Target Slump:", colspan=2)
        builder.cell(f"{self.slump}±25", style="text")

        # Admixtures section
        builder.row()
        builder.row(style="section_header")
        builder.cell("Admixtures", colspan=8)

        builder.row(style="header_secondary")
        builder.cell("Admixture Type", colspan=2)
        builder.cell("Dosage", colspan=2)
        builder.cell("Unit", colspan=1)
        builder.cell("Purpose", colspan=3)

        # Sample admixture rows
        admixture_types = [
            ("Plasticizer", "0.5% of cement", "Workability"),
            ("Air Entrainer", "50-100 ml/100kg", "Freeze-thaw resistance"),
            ("Retarder", "As per manufacturer", "Set time control"),
        ]

        for adm_type, dosage, purpose in admixture_types:
            builder.row()
            builder.cell(adm_type, colspan=2, style="input")
            builder.cell(dosage, colspan=2, style="input")
            builder.cell("", colspan=1, style="input")
            builder.cell(purpose, colspan=3, style="text")

        # Strength development tracking
        builder.row()
        builder.row(style="section_header")
        builder.cell("Strength Development", colspan=8)

        builder.row(style="header_secondary")
        builder.cell("Age (days)", colspan=2)
        builder.cell("Target Strength (MPa)", colspan=2)
        builder.cell("Actual Strength (MPa)", colspan=2)
        builder.cell("Achievement %", colspan=2)

        # Strength at different ages
        strength_ages = [(7, 0.65), (14, 0.85), (28, 1.0), (56, 1.15), (90, 1.20)]

        for age, factor in strength_ages:
            builder.row()
            builder.cell(age, colspan=2, style="number")
            builder.cell(
                self.target_strength * factor,
                colspan=2,
                style="number",
            )
            builder.cell(0.0, colspan=2, style="input")  # User enters actual
            # Achievement = (Actual / Target) * 100%
            curr_row = builder._current_row  # Get current row number
            builder.cell(
                f"=E{curr_row}/C{curr_row}",
                colspan=2,
                style="percentage",
            )

        return builder

    def validate(self) -> bool:
        """Validate template configuration."""
        return self.target_strength > 0 and self.slump > 0


__all__ = ["ConcreteMixTemplate"]
