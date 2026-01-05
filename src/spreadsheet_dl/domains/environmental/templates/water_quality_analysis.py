"""Water Quality Analysis Template.

Implements:
    WaterQualityAnalysisTemplate for environmental domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class WaterQualityAnalysisTemplate(BaseTemplate):
    """Water quality analysis template.

    Implements:
        WaterQualityAnalysisTemplate with WQI calculations

    Features:
    - Physical parameters (temperature, turbidity, conductivity)
    - Chemical parameters (pH, DO, BOD, COD, nutrients)
    - WQI calculation
    - Standards compliance checking
    - Trend analysis data

    Example:
        >>> template = WaterQualityAnalysisTemplate()
        >>> builder = template.generate()
        >>> builder is not None
        True
    """

    site_name: str = "Water Quality Site"
    site_id: str = ""
    water_body: str = ""
    num_samples: int = 12
    include_standards: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata.

        Returns:
            TemplateMetadata for water quality analysis template

        Implements:
            Template metadata
        """
        return TemplateMetadata(
            name="Water Quality Analysis",
            description="Water quality parameters with WQI calculations",
            category="environmental",
            tags=("water-quality", "analysis", "wqi", "monitoring"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """Validate template parameters.

        Returns:
            True if parameters are valid

        Implements:
            Template validation
        """
        return self.num_samples > 0

    def generate(self) -> SpreadsheetBuilder:
        """Generate the water quality analysis spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            WaterQualityAnalysisTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Water Quality - {self.site_name}",
            author="Environmental Lab",
            subject="Water Quality Data",
            description=f"Water quality analysis for {self.site_name}",
            keywords=["water-quality", "wqi", "analysis", self.site_name],
        )

        # Create analysis sheet
        builder.sheet("Samples")

        # Define columns
        builder.column("Sample ID", width="80pt", style="text")
        builder.column("Date", width="80pt", type="date")
        builder.column("Temp (C)", width="60pt")
        builder.column("pH", width="50pt")
        builder.column("DO (mg/L)", width="70pt")
        builder.column("BOD (mg/L)", width="70pt")
        builder.column("Turbidity", width="70pt")
        builder.column("Conductivity", width="80pt")
        builder.column("WQI", width="50pt")
        builder.column("Status", width="80pt", style="text")

        builder.freeze(rows=2)

        # Header
        builder.row(style="header_primary")
        builder.cell(f"WATER QUALITY: {self.site_name}", colspan=10)

        # Column headers
        builder.row(style="header_secondary")
        builder.cell("Sample ID")
        builder.cell("Date")
        builder.cell("Temp")
        builder.cell("pH")
        builder.cell("DO")
        builder.cell("BOD")
        builder.cell("Turbidity")
        builder.cell("Conductivity")
        builder.cell("WQI")
        builder.cell("Status")

        # Data rows
        for row_num in range(3, 3 + self.num_samples):
            builder.row()
            builder.cell(f"WQ-{row_num - 2:03d}")
            builder.cell("")  # Date

            # Parameter columns (empty for data entry)
            for _ in range(6):
                builder.cell("")

            # WQI formula (simplified calculation)
            # Uses DO%, BOD, and pH
            do_col = "E"
            bod_col = "F"
            ph_col = "D"

            builder.cell(
                f"=("
                f"MIN({do_col}{row_num}/9*100;100)+"  # DO sub-index
                f"MAX(0;100-{bod_col}{row_num}*10)+"  # BOD sub-index
                f"100-ABS({ph_col}{row_num}-7)*15"  # pH sub-index
                f")/3",
            )

            # Status formula
            wqi_col = "I"
            builder.cell(
                f'=IF({wqi_col}{row_num}>=90;"Excellent";'
                f'IF({wqi_col}{row_num}>=70;"Good";'
                f'IF({wqi_col}{row_num}>=50;"Fair";'
                f'IF({wqi_col}{row_num}>=25;"Poor";"Very Poor"))))',
            )

        # Statistics section
        builder.row()  # Blank row

        builder.row(style="header_secondary")
        builder.cell("STATISTICS", colspan=10)

        # Average row
        builder.row()
        builder.cell("Average", colspan=2, style="label")
        for col in ["C", "D", "E", "F", "G", "H", "I"]:
            builder.cell(f"=AVERAGE({col}3:{col}{2 + self.num_samples})")
        builder.cell("")

        if self.include_standards:
            # Standards reference sheet
            builder.sheet("Standards")

            builder.column("Parameter", width="120pt", style="text")
            builder.column("Unit", width="80pt", style="text")
            builder.column("Standard", width="100pt", style="text")
            builder.column("Source", width="150pt", style="text")

            builder.row(style="header_primary")
            builder.cell("WATER QUALITY STANDARDS", colspan=4)

            builder.row(style="header_secondary")
            builder.cell("Parameter")
            builder.cell("Unit")
            builder.cell("Standard Value")
            builder.cell("Regulatory Source")

            standards = [
                ("pH", "-", "6.5 - 8.5", "EPA/WHO"),
                ("Dissolved Oxygen", "mg/L", ">= 5.0", "EPA"),
                ("BOD", "mg/L", "<= 3.0 (Class I)", "EPA"),
                ("Turbidity", "NTU", "<= 1.0 (drinking)", "WHO"),
                ("Temperature", "C", "< 32 (aquatic life)", "EPA"),
                ("Conductivity", "uS/cm", "< 1500", "General"),
                ("Ammonia", "mg/L", "<= 0.5", "EPA"),
                ("Nitrate", "mg/L", "<= 10", "WHO"),
            ]

            for param, unit, standard, source in standards:
                builder.row()
                builder.cell(param)
                builder.cell(unit)
                builder.cell(standard)
                builder.cell(source)

        return builder


__all__ = ["WaterQualityAnalysisTemplate"]
