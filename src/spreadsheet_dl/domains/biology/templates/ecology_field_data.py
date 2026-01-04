"""
Ecology Field Data Template for field observations.

Implements:
    TASK-C006: EcologyFieldDataTemplate for biology domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class EcologyFieldDataTemplate(BaseTemplate):
    """
    Ecology field observations template.

    Implements:
        TASK-C006: EcologyFieldDataTemplate with species diversity metrics

    Features:
    - Site and survey information
    - Species observation tracking
    - Abundance counts
    - Environmental data (temperature, humidity, etc.)
    - Diversity indices (Shannon, Simpson, species richness)
    - GPS coordinates and habitat description

    Example:
        >>> template = EcologyFieldDataTemplate(
        ...     survey_name="Forest Biodiversity Study",
        ...     location="Oak Ridge Trail",
        ... )
        >>> builder = template.generate()
        >>> builder.save("field_data.ods")
    """

    survey_name: str = "Ecological Survey"
    location: str = ""
    date: str = ""
    observers: str = ""
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for ecology field data template

        Implements:
            TASK-C006: Template metadata
        """
        return TemplateMetadata(
            name="Ecology Field Data",
            description="Field observations with species diversity metrics",
            category="biology",
            tags=("ecology", "field-data", "biodiversity", "survey"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the ecology field data spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C006: EcologyFieldDataTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Field Data - {self.survey_name}",
            author=self.observers or "Field Team",
            subject="Ecological Survey",
            description=f"Field observations for {self.survey_name}",
            keywords=["ecology", "field-data", "biodiversity"],
        )

        # Create survey info sheet
        builder.sheet("Survey Info")

        builder.column("Field", width="150pt", style="text")
        builder.column("Value", width="300pt", style="text")

        builder.row(style="header_primary")
        builder.cell("SURVEY INFORMATION", colspan=2)

        builder.row()
        builder.cell("Survey Name:")
        builder.cell(self.survey_name)

        builder.row()
        builder.cell("Location:")
        builder.cell(self.location or "[Enter location]")

        builder.row()
        builder.cell("Date:")
        builder.cell(self.date or "[Enter date]")

        builder.row()
        builder.cell("Observers:")
        builder.cell(self.observers or "[Enter observer names]")

        builder.row()
        builder.cell("GPS Coordinates:")
        builder.cell("[Latitude, Longitude]")

        builder.row()
        builder.cell("Habitat Type:")
        builder.cell("[Forest, Grassland, Wetland, etc.]")

        builder.row()
        builder.cell("Weather Conditions:")
        builder.cell("")

        builder.row()
        builder.cell("Temperature (°C):")
        builder.cell("")

        builder.row()
        builder.cell("Humidity (%):")
        builder.cell("")

        # Create species observations sheet
        builder.sheet("Observations")

        builder.column("Species Name", width="200pt", style="text")
        builder.column("Common Name", width="150pt", style="text")
        builder.column("Count", width="80pt", type="number")
        builder.column("Life Stage", width="100pt", style="text")
        builder.column("Behavior", width="150pt", style="text")
        builder.column("Location Notes", width="200pt", style="text")
        builder.column("Time", width="80pt", style="text")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Species Name")
        builder.cell("Common Name")
        builder.cell("Abundance")
        builder.cell("Life Stage")
        builder.cell("Behavior")
        builder.cell("Location Notes")
        builder.cell("Time")

        # Add blank rows for observations
        for _ in range(30):
            builder.row()
            builder.cell("")
            builder.cell("")
            builder.cell(0)
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")

        # Create diversity analysis sheet
        builder.sheet("Diversity Analysis")

        builder.column("Metric", width="200pt", style="text")
        builder.column("Value", width="120pt", type="number")
        builder.column("Description", width="300pt", style="text")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("DIVERSITY METRICS", colspan=3)

        builder.row()
        builder.cell("Total Individuals")
        builder.cell("=SUM(Observations.C:C)")
        builder.cell("Total count of all individuals observed")

        builder.row()
        builder.cell("Species Richness")
        builder.cell('=COUNTIF(Observations.C:C;">0")')
        builder.cell("Number of different species present")

        builder.row()
        builder.cell("Shannon Diversity Index (H')")
        builder.cell(
            "=SUMPRODUCT(IF(Observations.C:C=0;0;-(Observations.C:C/SUM(Observations.C:C))*LN(Observations.C:C/SUM(Observations.C:C))))"
        )
        builder.cell("Shannon-Wiener diversity index")

        builder.row()
        builder.cell("Simpson's Index (D)")
        builder.cell("=SUMPRODUCT((Observations.C:C/SUM(Observations.C:C))^2)")
        builder.cell("Simpson's diversity index (0-1, lower = more diverse)")

        builder.row()
        builder.cell("Simpson's Reciprocal Index")
        builder.cell("=1/B5")
        builder.cell("Inverse of Simpson's D")

        # Create species summary sheet
        builder.sheet("Species Summary")

        builder.column("Species", width="200pt", style="text")
        builder.column("Total Count", width="100pt", type="number")
        builder.column("Relative Abundance", width="120pt", type="percentage")
        builder.column("Frequency", width="100pt", type="number")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Species")
        builder.cell("Total Count")
        builder.cell("Relative Abundance")
        builder.cell("Frequency")

        # Will be populated from Observations sheet
        for i in range(2, 32):
            builder.row()
            builder.cell(f"=Observations.A{i}")
            builder.cell(f"=Observations.C{i}")
            builder.cell(f"=B{i}/SUM(Observations.C:C)")
            builder.cell("")

        return builder


__all__ = ["EcologyFieldDataTemplate"]
