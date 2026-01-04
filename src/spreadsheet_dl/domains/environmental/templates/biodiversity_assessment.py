"""
Biodiversity Assessment Template.

Implements:
    TASK-C008: BiodiversityAssessmentTemplate for environmental domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class BiodiversityAssessmentTemplate(BaseTemplate):
    """
    Biodiversity assessment template.

    Implements:
        TASK-C008: BiodiversityAssessmentTemplate with diversity indices

    Features:
    - Species inventory tracking
    - Abundance counts
    - Shannon and Simpson diversity indices
    - Species richness
    - Evenness calculations
    - Habitat assessment

    Example:
        >>> template = BiodiversityAssessmentTemplate(
        ...     site_name="Forest Plot A",
        ...     num_species=50,
        ... )
        >>> builder = template.generate()
        >>> builder.save("biodiversity.ods")
    """

    site_name: str = "Biodiversity Site"
    site_id: str = ""
    habitat_type: str = ""
    num_species: int = 50
    include_habitat_assessment: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Biodiversity Assessment",
            description="Species diversity assessment with ecological indices",
            category="environmental",
            tags=("biodiversity", "ecology", "species", "diversity"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """Validate template parameters."""
        return self.num_species > 0

    def generate(self) -> SpreadsheetBuilder:
        """Generate the biodiversity assessment spreadsheet."""
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Biodiversity - {self.site_name}",
            author="Ecology Team",
            subject="Biodiversity Assessment",
            description=f"Species diversity assessment for {self.site_name}",
            keywords=["biodiversity", "ecology", "species"],
        )

        # Species inventory sheet
        builder.sheet("Species Inventory")

        builder.column("Species ID", width="80pt", style="text")
        builder.column("Scientific Name", width="180pt", style="text")
        builder.column("Common Name", width="150pt", style="text")
        builder.column("Count", width="60pt")
        builder.column("Proportion", width="80pt")
        builder.column("Status", width="100pt", style="text")

        builder.freeze(rows=2)

        builder.row(style="header_primary")
        builder.cell(f"SPECIES INVENTORY: {self.site_name}", colspan=6)

        builder.row(style="header_secondary")
        builder.cell("ID")
        builder.cell("Scientific Name")
        builder.cell("Common Name")
        builder.cell("Count")
        builder.cell("Proportion")
        builder.cell("Status")

        # Species rows
        for i in range(1, self.num_species + 1):
            row_num = i + 2
            builder.row()
            builder.cell(f"SP-{i:03d}")
            builder.cell("")  # Scientific name
            builder.cell("")  # Common name
            builder.cell("")  # Count

            # Proportion formula
            builder.cell(
                f"=IF(SUM(D$3:D${2 + self.num_species})=0;0;D{row_num}/SUM(D$3:D${2 + self.num_species}))"
            )

            builder.cell("")  # Status

        # Statistics section
        builder.row()
        builder.row(style="header_secondary")
        builder.cell("DIVERSITY INDICES", colspan=6)

        stats_start = 3 + self.num_species + 2

        builder.row()
        builder.cell("Total Individuals", colspan=3, style="label")
        builder.cell(f"=SUM(D3:D{2 + self.num_species})")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Species Richness (S)", colspan=3, style="label")
        builder.cell(f'=COUNTIF(D3:D{2 + self.num_species};">0")')
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Shannon Index (H')", colspan=3, style="label")
        # Shannon: H' = -SUM(pi * ln(pi))
        builder.cell(
            f"=-SUMPRODUCT(IF(E3:E{2 + self.num_species}>0;E3:E{2 + self.num_species}*LN(E3:E{2 + self.num_species});0))"
        )
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Simpson Index (1-D)", colspan=3, style="label")
        # Simpson: 1 - SUM(pi^2)
        builder.cell(
            f"=1-SUMPRODUCT(E3:E{2 + self.num_species};E3:E{2 + self.num_species})"
        )
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Evenness (J)", colspan=3, style="label")
        # Evenness: H' / ln(S)
        richness_cell = f"D{stats_start + 1}"
        shannon_cell = f"D{stats_start + 2}"
        builder.cell(f"=IF({richness_cell}>1;{shannon_cell}/LN({richness_cell});0)")
        builder.cell("")
        builder.cell("")

        if self.include_habitat_assessment:
            # Habitat assessment sheet
            builder.sheet("Habitat Assessment")

            builder.column("Feature", width="150pt", style="text")
            builder.column("Present", width="80pt", style="text")
            builder.column("Condition", width="100pt", style="text")
            builder.column("Notes", width="250pt", style="text")

            builder.row(style="header_primary")
            builder.cell("HABITAT ASSESSMENT", colspan=4)

            builder.row(style="header_secondary")
            builder.cell("Feature")
            builder.cell("Present (Y/N)")
            builder.cell("Condition")
            builder.cell("Notes")

            features = [
                "Canopy Cover",
                "Understory Vegetation",
                "Ground Cover",
                "Dead Wood",
                "Water Features",
                "Rock Outcrops",
                "Edge Habitat",
                "Corridors",
                "Human Disturbance",
                "Invasive Species",
            ]

            for feature in features:
                builder.row()
                builder.cell(feature)
                builder.cell("")
                builder.cell("")
                builder.cell("")

        return builder


__all__ = ["BiodiversityAssessmentTemplate"]
