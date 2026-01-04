"""
Site survey template for surveying data management.

Implements:
    REQ-C004-033: SiteSurveyTemplate with survey points and benchmarks
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class SiteSurveyTemplate(BaseTemplate):
    """
    Site survey template for survey points and topographic data.

    Implements:
        REQ-C004-033: SiteSurveyTemplate requirements

    Features:
        - Columns: Station, Point ID, Northing, Easting, Elevation,
          Description, Benchmark, Notes
        - Coordinate system specification
        - Elevation analysis (min, max, average)
        - Benchmark reference points
        - Cut/fill calculations

    Example:
        >>> template = SiteSurveyTemplate(
        ...     project_name="Highway Survey",
        ...     num_points=100
        ... )
        >>> builder = template.generate()
        >>> builder.save("site_survey.ods")
    """

    project_name: str = "Site Survey"
    num_points: int = 50
    datum: str = "WGS84"
    coordinate_system: str = "UTM Zone 10N"
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Site Survey",
            description="Survey points, elevations, and topographic data",
            category="civil_engineering",
            tags=("survey", "topography", "elevation", "coordinates"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate site survey spreadsheet.

        Returns:
            SpreadsheetBuilder configured with site survey template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Site Survey - {self.project_name}",
            author="Survey Engineering Department",
            subject="Topographic Survey Data",
            description=f"Survey points and elevations for {self.project_name}",
            keywords=["survey", "topography", "coordinates", self.project_name],
        )

        # Create main survey data sheet
        builder.sheet("Survey Points")

        # Define columns
        builder.column("Station", width="80pt", style="text")
        builder.column("Point ID", width="80pt", style="text")
        builder.column("Northing (m)", width="100pt", type="number")
        builder.column("Easting (m)", width="100pt", type="number")
        builder.column("Elevation (m)", width="90pt", type="number")
        builder.column("Description", width="150pt", style="text")
        builder.column("Benchmark", width="80pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=3, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Site Survey - {self.project_name}",
            colspan=8,
        )

        # Coordinate system info row
        builder.row(style="section_header")
        builder.cell(f"Datum: {self.datum}", colspan=4)
        builder.cell(f"Coordinate System: {self.coordinate_system}", colspan=4)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Station")
        builder.cell("Point ID")
        builder.cell("Northing (m)")
        builder.cell("Easting (m)")
        builder.cell("Elevation (m)")
        builder.cell("Description")
        builder.cell("Benchmark")
        builder.cell("Notes")

        # Survey point rows
        for i in range(self.num_points):
            i + 4
            builder.row()
            builder.cell(f"STA{i:04d}", style="input")  # Station
            builder.cell(f"P{i + 1:04d}", style="input")  # Point ID
            builder.cell(0.0, style="input")  # Northing
            builder.cell(0.0, style="input")  # Easting
            builder.cell(0.0, style="input")  # Elevation
            builder.cell("", style="input")  # Description
            builder.cell("N", style="input")  # Benchmark (Y/N)
            builder.cell("", style="input")  # Notes

        # Summary statistics
        total_row = self.num_points + 4
        builder.row()  # Blank row
        builder.row(style="section_header")
        builder.cell("Survey Statistics", colspan=8)

        builder.row()
        builder.cell("Total Points:", colspan=2)
        builder.cell(self.num_points, style="number")
        builder.cell("")
        builder.cell("Benchmarks:", colspan=2)
        builder.cell(f'=COUNTIF(G4:G{total_row - 1},"Y")', style="number")

        builder.row()
        builder.cell("Min Elevation:", colspan=2)
        builder.cell(f"=MIN(E4:E{total_row - 1})", style="number")
        builder.cell("m")
        builder.cell("Max Elevation:", colspan=2)
        builder.cell(f"=MAX(E4:E{total_row - 1})", style="number")
        builder.cell("m")

        builder.row()
        builder.cell("Average Elevation:", colspan=2)
        builder.cell(f"=AVERAGE(E4:E{total_row - 1})", style="number")
        builder.cell("m")
        builder.cell("Elevation Range:", colspan=2)
        builder.cell(
            f"=MAX(E4:E{total_row - 1})-MIN(E4:E{total_row - 1})",
            style="number",
        )
        builder.cell("m")

        # Coordinate bounds
        builder.row()
        builder.row(style="section_header")
        builder.cell("Coordinate Bounds", colspan=8)

        builder.row()
        builder.cell("Min Northing:", colspan=2)
        builder.cell(f"=MIN(C4:C{total_row - 1})", style="number")
        builder.cell("m")
        builder.cell("Max Northing:", colspan=2)
        builder.cell(f"=MAX(C4:C{total_row - 1})", style="number")
        builder.cell("m")

        builder.row()
        builder.cell("Min Easting:", colspan=2)
        builder.cell(f"=MIN(D4:D{total_row - 1})", style="number")
        builder.cell("m")
        builder.cell("Max Easting:", colspan=2)
        builder.cell(f"=MAX(D4:D{total_row - 1})", style="number")
        builder.cell("m")

        builder.row()
        builder.cell("Site Extent N-S:", colspan=2)
        builder.cell(
            f"=MAX(C4:C{total_row - 1})-MIN(C4:C{total_row - 1})",
            style="number",
        )
        builder.cell("m")
        builder.cell("Site Extent E-W:", colspan=2)
        builder.cell(
            f"=MAX(D4:D{total_row - 1})-MIN(D4:D{total_row - 1})",
            style="number",
        )
        builder.cell("m")

        # Benchmark reference sheet
        builder.sheet("Benchmarks")

        builder.column("BM ID", width="80pt", style="text")
        builder.column("Description", width="150pt", style="text")
        builder.column("Northing (m)", width="100pt", type="number")
        builder.column("Easting (m)", width="100pt", type="number")
        builder.column("Elevation (m)", width="90pt", type="number")
        builder.column("Date Established", width="100pt", style="text")
        builder.column("Stability", width="80pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.row(style="header_primary")
        builder.cell("Benchmark Reference Points", colspan=8)

        builder.row(style="header_secondary")
        builder.cell("BM ID")
        builder.cell("Description")
        builder.cell("Northing (m)")
        builder.cell("Easting (m)")
        builder.cell("Elevation (m)")
        builder.cell("Date")
        builder.cell("Stability")
        builder.cell("Notes")

        # Benchmark rows
        for i in range(10):
            builder.row()
            builder.cell(f"BM{i + 1:02d}", style="input")
            builder.cell("", style="input")
            builder.cell(0.0, style="input")
            builder.cell(0.0, style="input")
            builder.cell(0.0, style="input")
            builder.cell("", style="input")
            builder.cell("", style="input")
            builder.cell("", style="input")

        return builder

    def validate(self) -> bool:
        """Validate template configuration."""
        return self.num_points > 0


__all__ = ["SiteSurveyTemplate"]
