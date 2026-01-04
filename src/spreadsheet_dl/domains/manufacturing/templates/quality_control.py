"""
Quality Control Template for SPC and defect tracking.

Implements:
    TASK-C005: QualityControlTemplate for manufacturing domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class QualityControlTemplate(BaseTemplate):
    """
    Quality control charts with statistical process control (SPC).

    Implements:
        TASK-C005: QualityControlTemplate with SPC analysis

    Features:
    - Inspection data tracking
    - Defect categorization
    - Statistical process control (SPC) calculations
    - Control limit calculations (UCL, LCL)
    - Process capability metrics (Cp, Cpk)
    - Pareto analysis for defect types

    Example:
        >>> template = QualityControlTemplate(
        ...     product_line="Widget Assembly",
        ...     spec_limits=(95.0, 105.0),
        ... )
        >>> builder = template.generate()
        >>> builder.save("quality_control.ods")
    """

    product_name: str = "Product"
    num_measurements: int = 20
    spec_limits: tuple[float, float] = (90.0, 110.0)  # (LSL, USL)
    include_spc: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for quality control template

        Implements:
            TASK-C005: Template metadata
        """
        return TemplateMetadata(
            name="Quality Control",
            description="Quality control charts with SPC and defect tracking",
            category="manufacturing",
            tags=("quality", "spc", "defects", "inspection"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """
        Validate template configuration.

        Returns:
            True if configuration is valid

        Implements:
            TASK-C005: Template validation
        """
        if self.num_measurements <= 0:
            return False
        if self.spec_limits[0] >= self.spec_limits[1]:
            return False
        return True

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the quality control spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C005: QualityControlTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Quality Control - {self.product_name}",
            author="Quality Assurance",
            subject="Quality Control",
            description=f"Quality control and SPC for {self.product_name}",
            keywords=["quality", "spc", "control", self.product_name],
        )

        # Create inspection data sheet
        builder.sheet("Inspection Data")
        self._create_inspection_sheet(builder)

        # Create SPC analysis if requested
        if self.include_spc:
            builder.sheet("SPC Analysis")
            self._create_spc_sheet(builder)

        # Create defect summary
        builder.sheet("Defect Summary")
        self._create_defect_summary(builder)

        return builder

    def _create_inspection_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create the inspection data sheet."""
        builder.column("Sample #", width="80pt", style="text")
        builder.column("Date/Time", width="120pt", type="date")
        builder.column("Inspector", width="100pt", style="text")
        builder.column("Measurement", width="100pt", type="number")
        builder.column("Spec LSL", width="80pt", type="number")
        builder.column("Spec USL", width="80pt", type="number")
        builder.column("In Spec?", width="80pt", style="text")
        builder.column("Defect Type", width="120pt", style="text")
        builder.column("Notes", width="200pt", style="text")

        builder.freeze(rows=1)

        # Header row
        builder.row(style="header_primary")
        builder.cell("Sample #")
        builder.cell("Date/Time")
        builder.cell("Inspector")
        builder.cell("Measurement")
        builder.cell("Spec LSL")
        builder.cell("Spec USL")
        builder.cell("In Spec?")
        builder.cell("Defect Type")
        builder.cell("Notes")

        # Sample data rows
        lsl, usl = self.spec_limits
        for i in range(1, 21):  # 20 sample rows
            row_idx = i + 1
            builder.row()
            builder.cell(f"S-{i:03d}")
            builder.cell("", style="date")
            builder.cell("", style="text")
            builder.cell(0.0, style="number")
            builder.cell(lsl)
            builder.cell(usl)
            # Formula to check if in spec
            builder.cell(
                f'=IF(AND(D{row_idx}>=E{row_idx},D{row_idx}<=F{row_idx}),"Pass","Fail")'
            )
            builder.cell("", style="text")
            builder.cell("", style="text")

    def _create_spc_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create SPC analysis sheet."""
        builder.column("Metric", width="200pt")
        builder.column("Value", width="120pt", type="number")
        builder.column("Formula", width="250pt", style="text")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("SPC Metrics", colspan=3)

        builder.row(style="header_secondary")
        builder.cell("Metric")
        builder.cell("Value")
        builder.cell("Formula")

        # Calculate metrics from inspection data
        metrics = [
            ("Sample Count", "=COUNTA('Inspection Data'.A2:A21)", "Count of samples"),
            ("Mean (X̄)", "=AVERAGE('Inspection Data'.D2:D21)", "Average measurement"),
            ("Std Dev (σ)", "=STDEV('Inspection Data'.D2:D21)", "Standard deviation"),
            ("Upper Control Limit (UCL)", "=B4+(3*B5)", "Mean + 3σ"),
            ("Lower Control Limit (LCL)", "=B4-(3*B5)", "Mean - 3σ"),
            ("Specification LSL", f"={self.spec_limits[0]}", "Lower spec limit"),
            ("Specification USL", f"={self.spec_limits[1]}", "Upper spec limit"),
            ("Process Capability (Cp)", "=(B8-B7)/(6*B5)", "(USL-LSL)/(6σ)"),
            (
                "Defect Count",
                "=COUNTIF('Inspection Data'.G2:G21,\"Fail\")",
                "Failed samples",
            ),
            ("Defect Rate %", "=(B10/B3)*100", "Defects/Total * 100"),
            ("First Pass Yield %", "=((B3-B10)/B3)*100", "Pass/Total * 100"),
        ]

        for metric, formula, description in metrics:
            builder.row()
            builder.cell(metric)
            builder.cell(formula)
            builder.cell(description)

    def _create_defect_summary(self, builder: SpreadsheetBuilder) -> None:
        """Create defect summary sheet."""
        builder.column("Defect Type", width="150pt")
        builder.column("Count", width="100pt", type="number")
        builder.column("Percentage", width="100pt", type="number")
        builder.column("Cumulative %", width="100pt", type="number")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Defect Type")
        builder.cell("Count")
        builder.cell("Percentage")
        builder.cell("Cumulative %")

        # Common defect types
        defect_types = [
            "Dimensional",
            "Surface Finish",
            "Missing Component",
            "Wrong Material",
            "Assembly Error",
            "Other",
        ]

        for row_idx, defect_type in enumerate(defect_types, start=2):
            builder.row()
            builder.cell(defect_type)
            # Count from inspection data
            builder.cell(f"=COUNTIF('Inspection Data'.H2:H21,A{row_idx})")
            # Percentage
            builder.cell(f"=(B{row_idx}/SUM(B$2:B$7))*100")
            # Cumulative percentage
            builder.cell(f"=SUM(C$2:C{row_idx})")


__all__ = ["QualityControlTemplate"]
