"""Carbon Footprint Template.

Implements:
    CarbonFootprintTemplate for environmental domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class CarbonFootprintTemplate(BaseTemplate):
    """Carbon footprint tracking template.

    Implements:
        CarbonFootprintTemplate with emissions calculations

    Features:
    - Scope 1, 2, 3 emissions tracking
    - Activity-based emissions calculations
    - CO2 equivalent conversions
    - Reduction targets tracking
    - Offset calculations

    Example:
        >>> template = CarbonFootprintTemplate()
        >>> builder = template.generate()
        >>> builder is not None
        True
    """

    organization_name: str = "Organization"
    reporting_year: int = 2024
    include_offsets: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Carbon Footprint",
            description="Carbon emissions tracking with CO2e calculations",
            category="environmental",
            tags=("carbon", "emissions", "footprint", "sustainability"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """Validate template parameters."""
        return len(self.organization_name) > 0

    def generate(self) -> SpreadsheetBuilder:
        """Generate the carbon footprint spreadsheet."""
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Carbon Footprint - {self.organization_name}",
            author="Sustainability Team",
            subject="Carbon Emissions",
            description=f"Carbon footprint for {self.organization_name}",
            keywords=["carbon", "emissions", "sustainability"],
        )

        # Emissions sheet
        builder.sheet("Emissions")

        builder.column("Category", width="150pt", style="text")
        builder.column("Source", width="150pt", style="text")
        builder.column("Activity Data", width="100pt")
        builder.column("Unit", width="80pt", style="text")
        builder.column("Emission Factor", width="100pt")
        builder.column("CO2e (tonnes)", width="100pt")

        builder.freeze(rows=2)

        builder.row(style="header_primary")
        builder.cell(
            f"CARBON FOOTPRINT: {self.organization_name} ({self.reporting_year})",
            colspan=6,
        )

        builder.row(style="header_secondary")
        builder.cell("Category")
        builder.cell("Source")
        builder.cell("Activity")
        builder.cell("Unit")
        builder.cell("EF")
        builder.cell("CO2e")

        # Scope 1
        builder.row(style="header_secondary")
        builder.cell("SCOPE 1 - Direct Emissions", colspan=6)

        scope1_sources = [
            ("Stationary Combustion", "Natural Gas", "therms", "0.0053"),
            ("Mobile Combustion", "Fleet Vehicles", "gallons", "0.0089"),
            ("Fugitive Emissions", "Refrigerants", "kg", "1.43"),
        ]

        scope1_start = 4
        for source, detail, unit, ef in scope1_sources:
            builder.row()
            builder.cell(source)
            builder.cell(detail)
            builder.cell("")  # Activity data
            builder.cell(unit)
            builder.cell(ef)
            row_num = scope1_start + scope1_sources.index((source, detail, unit, ef))
            builder.cell(f"=C{row_num}*E{row_num}")

        scope1_end = scope1_start + len(scope1_sources) - 1

        # Scope 2
        builder.row(style="header_secondary")
        builder.cell("SCOPE 2 - Indirect Energy", colspan=6)

        scope2_start = scope1_end + 2
        scope2_sources = [
            ("Electricity", "Purchased Power", "kWh", "0.0004"),
            ("Steam/Heat", "Purchased Heat", "MMBtu", "0.053"),
        ]

        for source, detail, unit, ef in scope2_sources:
            builder.row()
            builder.cell(source)
            builder.cell(detail)
            builder.cell("")
            builder.cell(unit)
            builder.cell(ef)
            row_num = scope2_start + scope2_sources.index((source, detail, unit, ef))
            builder.cell(f"=C{row_num}*E{row_num}")

        scope2_end = scope2_start + len(scope2_sources) - 1

        # Scope 3
        builder.row(style="header_secondary")
        builder.cell("SCOPE 3 - Other Indirect", colspan=6)

        scope3_start = scope2_end + 2
        scope3_sources = [
            ("Business Travel", "Air Travel", "miles", "0.00022"),
            ("Employee Commute", "Commuting", "miles", "0.00035"),
            ("Waste", "Landfill", "tonnes", "0.5"),
        ]

        for source, detail, unit, ef in scope3_sources:
            builder.row()
            builder.cell(source)
            builder.cell(detail)
            builder.cell("")
            builder.cell(unit)
            builder.cell(ef)
            row_num = scope3_start + scope3_sources.index((source, detail, unit, ef))
            builder.cell(f"=C{row_num}*E{row_num}")

        scope3_end = scope3_start + len(scope3_sources) - 1

        # Totals
        builder.row()
        builder.row(style="header_secondary")
        builder.cell("SUMMARY", colspan=6)

        builder.row()
        builder.cell("Scope 1 Total", colspan=5, style="label")
        builder.cell(f"=SUM(F{scope1_start}:F{scope1_end})")

        builder.row()
        builder.cell("Scope 2 Total", colspan=5, style="label")
        builder.cell(f"=SUM(F{scope2_start}:F{scope2_end})")

        builder.row()
        builder.cell("Scope 3 Total", colspan=5, style="label")
        builder.cell(f"=SUM(F{scope3_start}:F{scope3_end})")

        summary_start = scope3_end + 3
        builder.row()
        builder.cell("TOTAL EMISSIONS", colspan=5, style="label")
        builder.cell(f"=SUM(F{summary_start}:F{summary_start + 2})")

        return builder


__all__ = ["CarbonFootprintTemplate"]
