"""
OEE Tracking Template for Overall Equipment Effectiveness analysis.

Implements:
    TASK-C005: OEETrackingTemplate for manufacturing domain
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class OEETrackingTemplate(BaseTemplate):
    """
    Overall Equipment Effectiveness (OEE) tracking and analysis.

    Implements:
        TASK-C005: OEETrackingTemplate with availability, performance, and quality

    Features:
    - Availability calculation (uptime / planned time)
    - Performance calculation (actual / ideal cycle time)
    - Quality calculation (good units / total units)
    - Overall OEE (Availability × Performance × Quality)
    - Downtime tracking and categorization
    - Loss analysis (availability, performance, quality losses)

    Example:
        >>> template = OEETrackingTemplate(
        ...     equipment_name="CNC Machine #5",
        ...     shifts=["Day", "Night"],
        ... )
        >>> builder = template.generate()
        >>> builder.save("oee_tracking.ods")
    """

    equipment_name: str = "Equipment"
    shifts: list[str] = field(default_factory=lambda: ["Shift A", "Shift B"])
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for OEE tracking template

        Implements:
            TASK-C005: Template metadata
        """
        return TemplateMetadata(
            name="OEE Tracking",
            description="Overall Equipment Effectiveness tracking and analysis",
            category="manufacturing",
            tags=("oee", "equipment", "efficiency", "downtime"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the OEE tracking spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C005: OEETrackingTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"OEE Tracking - {self.equipment_name}",
            author="Production Engineering",
            subject="OEE Analysis",
            description=f"OEE tracking and analysis for {self.equipment_name}",
            keywords=["oee", "efficiency", "equipment", self.equipment_name],
        )

        # Create OEE data sheet
        builder.sheet("OEE Data")
        self._create_oee_sheet(builder)

        # Create downtime tracking
        builder.sheet("Downtime")
        self._create_downtime_sheet(builder)

        # Create summary dashboard
        builder.sheet("Summary")
        self._create_summary_sheet(builder)

        return builder

    def _create_oee_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create the OEE tracking sheet."""
        builder.column("Date", width="100pt", type="date")
        builder.column("Shift", width="80pt", style="text")
        builder.column("Planned Time (min)", width="120pt", type="number")
        builder.column("Downtime (min)", width="120pt", type="number")
        builder.column("Run Time (min)", width="120pt", type="number")
        builder.column("Ideal Cycle Time", width="120pt", type="number")
        builder.column("Total Units", width="100pt", type="number")
        builder.column("Good Units", width="100pt", type="number")
        builder.column("Availability %", width="100pt", type="number")
        builder.column("Performance %", width="100pt", type="number")
        builder.column("Quality %", width="100pt", type="number")
        builder.column("OEE %", width="100pt", type="number")

        builder.freeze(rows=1)

        # Header row
        builder.row(style="header_primary")
        builder.cell("Date")
        builder.cell("Shift")
        builder.cell("Planned Time (min)")
        builder.cell("Downtime (min)")
        builder.cell("Run Time (min)")
        builder.cell("Ideal Cycle Time")
        builder.cell("Total Units")
        builder.cell("Good Units")
        builder.cell("Availability %")
        builder.cell("Performance %")
        builder.cell("Quality %")
        builder.cell("OEE %")

        # Sample data rows
        for i in range(2, 16):  # 14 sample rows
            builder.row()
            builder.cell("", style="date")
            builder.cell("", style="text")
            builder.cell(480, style="number")  # 8-hour shift
            builder.cell(0, style="number")
            # Run Time = Planned - Downtime
            builder.cell(f"=C{i}-D{i}")
            builder.cell(1.0, style="number")  # 1 min ideal cycle
            builder.cell(0, style="number")
            builder.cell(0, style="number")
            # Availability = Run Time / Planned Time * 100
            builder.cell(f"=(E{i}/C{i})*100")
            # Performance = (Total Units * Ideal Cycle) / Run Time * 100
            builder.cell(f"=(G{i}*F{i})/E{i}*100")
            # Quality = Good Units / Total Units * 100
            builder.cell(f"=IF(G{i}=0,0,(H{i}/G{i})*100)")
            # OEE = Availability * Performance * Quality / 10000
            builder.cell(f"=(I{i}*J{i}*K{i})/10000")

    def _create_downtime_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create downtime tracking sheet."""
        builder.column("Date", width="100pt", type="date")
        builder.column("Shift", width="80pt", style="text")
        builder.column("Start Time", width="100pt", style="text")
        builder.column("End Time", width="100pt", style="text")
        builder.column("Duration (min)", width="100pt", type="number")
        builder.column("Category", width="120pt", style="text")
        builder.column("Reason", width="200pt", style="text")
        builder.column("Corrective Action", width="200pt", style="text")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Date")
        builder.cell("Shift")
        builder.cell("Start Time")
        builder.cell("End Time")
        builder.cell("Duration (min)")
        builder.cell("Category")
        builder.cell("Reason")
        builder.cell("Corrective Action")

        # Sample downtime rows
        for _ in range(20):
            builder.row()
            builder.cell("", style="date")
            builder.cell("", style="text")
            builder.cell("", style="text")
            builder.cell("", style="text")
            builder.cell(0, style="number")
            builder.cell("", style="text")
            builder.cell("", style="text")
            builder.cell("", style="text")

    def _create_summary_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create OEE summary dashboard."""
        builder.column("Metric", width="200pt")
        builder.column("Value", width="120pt", type="number")
        builder.column("Target", width="100pt", type="number")
        builder.column("Status", width="100pt", style="text")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("OEE Summary Dashboard", colspan=4)

        builder.row(style="header_secondary")
        builder.cell("Metric")
        builder.cell("Value")
        builder.cell("Target")
        builder.cell("Status")

        # Summary metrics
        metrics = [
            ("Average Availability %", "=AVERAGE('OEE Data'.I2:I15)", 90),
            ("Average Performance %", "=AVERAGE('OEE Data'.J2:J15)", 95),
            ("Average Quality %", "=AVERAGE('OEE Data'.K2:K15)", 99),
            ("Average OEE %", "=AVERAGE('OEE Data'.L2:L15)", 85),
            ("Total Planned Time (hrs)", "=SUM('OEE Data'.C2:C15)/60", 0),
            ("Total Downtime (hrs)", "=SUM('OEE Data'.D2:D15)/60", 0),
            ("Total Units Produced", "=SUM('OEE Data'.G2:G15)", 0),
            ("Total Good Units", "=SUM('OEE Data'.H2:H15)", 0),
        ]

        for row_idx, (metric, formula, target) in enumerate(metrics, start=3):
            builder.row()
            builder.cell(metric)
            builder.cell(formula)
            if target > 0:
                builder.cell(target)
                builder.cell(f'=IF(B{row_idx}>=C{row_idx},"On Target","Below Target")')
            else:
                builder.cell("", style="number")
                builder.cell("", style="text")


__all__ = ["OEETrackingTemplate"]
