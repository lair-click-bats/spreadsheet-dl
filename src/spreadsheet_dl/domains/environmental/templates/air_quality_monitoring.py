"""Air Quality Monitoring Template.

Implements:
    AirQualityMonitoringTemplate for environmental domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class AirQualityMonitoringTemplate(BaseTemplate):
    """Air quality monitoring template.

    Implements:
        AirQualityMonitoringTemplate with AQI calculations

    Features:
    - Pollutant concentration tracking (PM2.5, PM10, O3, NO2, SO2, CO)
    - AQI calculation for each pollutant
    - Overall AQI determination
    - Health advisory levels
    - Trend visualization data

    Example:
        >>> template = AirQualityMonitoringTemplate(  # doctest: +SKIP
        ...     station_name="Downtown Station",
        ...     num_readings=24,
        ... )
        >>> builder = template.generate()  # doctest: +SKIP
        >>> path = builder.save("air_quality.ods")  # doctest: +SKIP
    """

    station_name: str = "Air Quality Station"
    station_id: str = ""
    location: str = ""
    num_readings: int = 24
    include_health_advisory: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata.

        Returns:
            TemplateMetadata for air quality monitoring template

        Implements:
            Template metadata
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
        """Validate template parameters.

        Returns:
            True if parameters are valid

        Implements:
            Template validation
        """
        return self.num_readings > 0

    def generate(self) -> SpreadsheetBuilder:
        """Generate the air quality monitoring spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            AirQualityMonitoringTemplate generation
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

        # Define columns - pollutant concentrations
        builder.column("Date/Time", width="120pt", type="datetime")
        builder.column("PM2.5", width="55pt")  # µg/m³
        builder.column("PM10", width="55pt")  # µg/m³
        builder.column("O3", width="55pt")  # ppb
        builder.column("NO2", width="55pt")  # ppb
        builder.column("SO2", width="55pt")  # ppb
        builder.column("CO", width="55pt")  # ppm
        # Individual AQI columns for each pollutant
        builder.column("AQI-PM2.5", width="60pt")
        builder.column("AQI-PM10", width="60pt")
        builder.column("AQI-O3", width="55pt")
        builder.column("AQI-NO2", width="55pt")
        builder.column("AQI-SO2", width="55pt")
        builder.column("AQI-CO", width="55pt")
        # Overall AQI = MAX of all individual AQIs
        builder.column("AQI", width="50pt")
        builder.column("Category", width="100pt", style="text")

        builder.freeze(rows=2)

        # Header
        builder.row(style="header_primary")
        builder.cell(f"AIR QUALITY: {self.station_name}", colspan=15)

        # Column headers
        builder.row(style="header_secondary")
        builder.cell("Date/Time")
        builder.cell("PM2.5")
        builder.cell("PM10")
        builder.cell("O3")
        builder.cell("NO2")
        builder.cell("SO2")
        builder.cell("CO")
        builder.cell("AQI-PM2.5")
        builder.cell("AQI-PM10")
        builder.cell("AQI-O3")
        builder.cell("AQI-NO2")
        builder.cell("AQI-SO2")
        builder.cell("AQI-CO")
        builder.cell("AQI")
        builder.cell("Category")

        # Data rows with EPA AQI breakpoint calculations
        for row_num in range(3, 3 + self.num_readings):
            builder.row()
            builder.cell("")  # Date/Time

            # Pollutant columns (empty for data entry)
            for _ in range(6):
                builder.cell("")

            # AQI-PM2.5 formula (EPA breakpoints: 0-12, 12.1-35.4, 35.5-55.4, 55.5-150.4, 150.5-250.4, 250.5-350.4, 350.5-500.4 µg/m³)
            builder.cell(
                f'=IF(B{row_num}="";"";IF(B{row_num}<=12;B{row_num}*4.166;'
                f"IF(B{row_num}<=35.4;50+(B{row_num}-12)*2.132;"
                f"IF(B{row_num}<=55.4;100+(B{row_num}-35.4)*2.5;"
                f"IF(B{row_num}<=150.4;150+(B{row_num}-55.4)*0.526;"
                f"IF(B{row_num}<=250.4;200+(B{row_num}-150.4)*0.5;"
                f"IF(B{row_num}<=350.4;300+(B{row_num}-250.4)*1;"
                f"400+(B{row_num}-350.4)*0.666)))))))",
            )

            # AQI-PM10 formula (EPA breakpoints: 0-54, 55-154, 155-254, 255-354, 355-424, 425-504, 505-604 µg/m³)
            builder.cell(
                f'=IF(C{row_num}="";"";IF(C{row_num}<=54;C{row_num}*0.926;'
                f"IF(C{row_num}<=154;50+(C{row_num}-54)*0.5;"
                f"IF(C{row_num}<=254;100+(C{row_num}-154)*0.5;"
                f"IF(C{row_num}<=354;150+(C{row_num}-254)*0.5;"
                f"IF(C{row_num}<=424;200+(C{row_num}-354)*1.428;"
                f"IF(C{row_num}<=504;300+(C{row_num}-424)*1.25;"
                f"400+(C{row_num}-504)*1)))))))",
            )

            # AQI-O3 formula (8-hour: 0-54, 55-70, 71-85, 86-105, 106-200 ppb)
            builder.cell(
                f'=IF(D{row_num}="";"";IF(D{row_num}<=54;D{row_num}*0.926;'
                f"IF(D{row_num}<=70;50+(D{row_num}-54)*3.125;"
                f"IF(D{row_num}<=85;100+(D{row_num}-70)*3.333;"
                f"IF(D{row_num}<=105;150+(D{row_num}-85)*2.5;"
                f"200+(D{row_num}-105)*1.053)))))",
            )

            # AQI-NO2 formula (1-hour: 0-53, 54-100, 101-360, 361-649, 650-1249, 1250-2049 ppb)
            builder.cell(
                f'=IF(E{row_num}="";"";IF(E{row_num}<=53;E{row_num}*0.943;'
                f"IF(E{row_num}<=100;50+(E{row_num}-53)*1.064;"
                f"IF(E{row_num}<=360;100+(E{row_num}-100)*0.192;"
                f"IF(E{row_num}<=649;150+(E{row_num}-360)*0.173;"
                f"IF(E{row_num}<=1249;200+(E{row_num}-649)*0.166;"
                f"300+(E{row_num}-1249)*0.125))))))",
            )

            # AQI-SO2 formula (1-hour: 0-35, 36-75, 76-185, 186-304, 305-604, 605-1004 ppb)
            builder.cell(
                f'=IF(F{row_num}="";"";IF(F{row_num}<=35;F{row_num}*1.429;'
                f"IF(F{row_num}<=75;50+(F{row_num}-35)*1.25;"
                f"IF(F{row_num}<=185;100+(F{row_num}-75)*0.455;"
                f"IF(F{row_num}<=304;150+(F{row_num}-185)*0.42;"
                f"IF(F{row_num}<=604;200+(F{row_num}-304)*0.333;"
                f"300+(F{row_num}-604)*0.25))))))",
            )

            # AQI-CO formula (8-hour: 0-4.4, 4.5-9.4, 9.5-12.4, 12.5-15.4, 15.5-30.4, 30.5-50.4 ppm)
            builder.cell(
                f'=IF(G{row_num}="";"";IF(G{row_num}<=4.4;G{row_num}*11.364;'
                f"IF(G{row_num}<=9.4;50+(G{row_num}-4.4)*10;"
                f"IF(G{row_num}<=12.4;100+(G{row_num}-9.4)*16.667;"
                f"IF(G{row_num}<=15.4;150+(G{row_num}-12.4)*16.667;"
                f"IF(G{row_num}<=30.4;200+(G{row_num}-15.4)*6.667;"
                f"300+(G{row_num}-30.4)*5))))))",
            )

            # Overall AQI = MAX of all individual AQIs
            builder.cell(
                f'=IF(COUNTA(H{row_num}:M{row_num})=0;"";MAX(H{row_num}:M{row_num}))',
            )

            # Category formula based on overall AQI
            builder.cell(
                f'=IF(N{row_num}="";"";IF(N{row_num}<=50;"Good";'
                f'IF(N{row_num}<=100;"Moderate";'
                f'IF(N{row_num}<=150;"Unhealthy Sensitive";'
                f'IF(N{row_num}<=200;"Unhealthy";'
                f'IF(N{row_num}<=300;"Very Unhealthy";"Hazardous"))))))',
            )

        # Statistics section
        builder.row()  # Blank row

        builder.row(style="header_secondary")
        builder.cell("STATISTICS", colspan=15)

        # Average row - pollutant concentrations and all AQI values
        builder.row()
        builder.cell("Average", style="label")
        # Columns: B-G (pollutants), H-M (individual AQIs), N (overall AQI)
        for col in ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]:
            builder.cell(f"=AVERAGE({col}3:{col}{2 + self.num_readings})")
        builder.cell("")  # Category column

        # Maximum row
        builder.row()
        builder.cell("Maximum", style="label")
        for col in ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]:
            builder.cell(f"=MAX({col}3:{col}{2 + self.num_readings})")
        builder.cell("")

        # Minimum row
        builder.row()
        builder.cell("Minimum", style="label")
        for col in ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]:
            builder.cell(f"=MIN({col}3:{col}{2 + self.num_readings})")
        builder.cell("")

        # Exceedance count - number of readings exceeding "Good" threshold (AQI > 50)
        builder.row()
        builder.cell("Exceedances (>50)", style="label")
        for _ in range(6):  # Skip pollutant columns
            builder.cell("")
        for col in ["H", "I", "J", "K", "L", "M", "N"]:
            builder.cell(f'=COUNTIF({col}3:{col}{2 + self.num_readings};">50")')
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
