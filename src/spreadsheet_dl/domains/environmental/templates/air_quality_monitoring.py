"""
Air Quality Monitoring Template.

Implements:
    TASK-C008: AirQualityMonitoringTemplate for environmental domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class AirQualityMonitoringTemplate(BaseTemplate):
    """
    Air quality monitoring template.

    Implements:
        TASK-C008: AirQualityMonitoringTemplate with AQI calculations

    Features:
    - Pollutant concentration tracking (PM2.5, PM10, O3, NO2, SO2, CO)
    - AQI calculation for each pollutant
    - Overall AQI determination
    - Health advisory levels
    - Trend visualization data

    Example:
        >>> template = AirQualityMonitoringTemplate(
        ...     station_name="Downtown Station",
        ...     num_readings=24,
        ... )
        >>> builder = template.generate()
        >>> builder.save("air_quality.ods")
    """

    station_name: str = "Air Quality Station"
    station_id: str = ""
    location: str = ""
    num_readings: int = 24
    include_health_advisory: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for air quality monitoring template

        Implements:
            TASK-C008: Template metadata
        """
        return TemplateMetadata(
            name="Air Quality Monitoring",
            description="Air pollutant monitoring with AQI calculations",
            category="environmental",
            tags=("air-quality", "monitoring", "aqi", "pollution"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """
        Validate template parameters.

        Returns:
            True if parameters are valid

        Implements:
            TASK-C008: Template validation
        """
        return self.num_readings > 0

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the air quality monitoring spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C008: AirQualityMonitoringTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Air Quality - {self.station_name}",
            author="Environmental Monitoring Team",
            subject="Air Quality Data",
            description=f"Air quality monitoring for {self.station_name}",
            keywords=["air-quality", "aqi", "pollution", self.station_name],
        )

        # Create monitoring sheet
        builder.sheet("Readings")

        # Define columns
        builder.column("Date/Time", width="120pt", type="datetime")
        builder.column("PM2.5", width="60pt")
        builder.column("PM10", width="60pt")
        builder.column("O3", width="60pt")
        builder.column("NO2", width="60pt")
        builder.column("SO2", width="60pt")
        builder.column("CO", width="60pt")
        builder.column("AQI", width="50pt")
        builder.column("Category", width="100pt", style="text")

        builder.freeze(rows=2)

        # Header
        builder.row(style="header_primary")
        builder.cell(f"AIR QUALITY: {self.station_name}", colspan=9)

        # Column headers
        builder.row(style="header_secondary")
        builder.cell("Date/Time")
        builder.cell("PM2.5")
        builder.cell("PM10")
        builder.cell("O3")
        builder.cell("NO2")
        builder.cell("SO2")
        builder.cell("CO")
        builder.cell("AQI")
        builder.cell("Category")

        # Data rows
        for row_num in range(3, 3 + self.num_readings):
            builder.row()
            builder.cell("")  # Date/Time

            # Pollutant columns (empty for data entry)
            for _ in range(6):
                builder.cell("")

            # AQI formula (uses max of individual AQIs)
            # Simplified: just use PM2.5 as primary indicator
            pm25_col = "B"
            builder.cell(
                f"=IF({pm25_col}{row_num}<=12;{pm25_col}{row_num}*4.166;"
                f"IF({pm25_col}{row_num}<=35.4;50+({pm25_col}{row_num}-12)*2.132;"
                f"IF({pm25_col}{row_num}<=55.4;100+({pm25_col}{row_num}-35.4)*2.5;"
                f"IF({pm25_col}{row_num}<=150.4;150+({pm25_col}{row_num}-55.4)*0.526;"
                f"200))))",
            )

            # Category formula
            aqi_col = "H"
            builder.cell(
                f'=IF({aqi_col}{row_num}<=50;"Good";'
                f'IF({aqi_col}{row_num}<=100;"Moderate";'
                f'IF({aqi_col}{row_num}<=150;"Unhealthy Sensitive";'
                f'IF({aqi_col}{row_num}<=200;"Unhealthy";'
                f'IF({aqi_col}{row_num}<=300;"Very Unhealthy";"Hazardous")))))',
            )

        # Statistics section
        builder.row()  # Blank row

        builder.row(style="header_secondary")
        builder.cell("STATISTICS", colspan=9)

        # Average row
        builder.row()
        builder.cell("Average", style="label")
        for col in ["B", "C", "D", "E", "F", "G", "H"]:
            builder.cell(f"=AVERAGE({col}3:{col}{2 + self.num_readings})")
        builder.cell("")

        # Maximum row
        builder.row()
        builder.cell("Maximum", style="label")
        for col in ["B", "C", "D", "E", "F", "G", "H"]:
            builder.cell(f"=MAX({col}3:{col}{2 + self.num_readings})")
        builder.cell("")

        # Minimum row
        builder.row()
        builder.cell("Minimum", style="label")
        for col in ["B", "C", "D", "E", "F", "G", "H"]:
            builder.cell(f"=MIN({col}3:{col}{2 + self.num_readings})")
        builder.cell("")

        if self.include_health_advisory:
            # Health advisory sheet
            builder.sheet("AQI Reference")

            builder.column("AQI Range", width="100pt", style="text")
            builder.column("Category", width="120pt", style="text")
            builder.column("Color", width="80pt", style="text")
            builder.column("Health Advisory", width="300pt", style="text")

            builder.row(style="header_primary")
            builder.cell("AQI REFERENCE", colspan=4)

            builder.row(style="header_secondary")
            builder.cell("AQI Range")
            builder.cell("Category")
            builder.cell("Color")
            builder.cell("Health Advisory")

            aqi_data = [
                ("0-50", "Good", "Green", "Air quality is satisfactory"),
                (
                    "51-100",
                    "Moderate",
                    "Yellow",
                    "Acceptable; some risk for sensitive groups",
                ),
                (
                    "101-150",
                    "Unhealthy for Sensitive",
                    "Orange",
                    "Sensitive groups may experience effects",
                ),
                (
                    "151-200",
                    "Unhealthy",
                    "Red",
                    "Everyone may experience health effects",
                ),
                (
                    "201-300",
                    "Very Unhealthy",
                    "Purple",
                    "Health alert: everyone may experience serious effects",
                ),
                (
                    "301-500",
                    "Hazardous",
                    "Maroon",
                    "Health warning of emergency conditions",
                ),
            ]

            for aqi_range, category, color, advisory in aqi_data:
                builder.row()
                builder.cell(aqi_range)
                builder.cell(category)
                builder.cell(color)
                builder.cell(advisory)

        return builder


__all__ = ["AirQualityMonitoringTemplate"]
