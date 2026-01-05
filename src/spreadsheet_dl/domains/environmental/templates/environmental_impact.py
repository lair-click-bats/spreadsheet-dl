"""Environmental Impact Assessment Template.

Implements:
    EnvironmentalImpactTemplate for environmental domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class EnvironmentalImpactTemplate(BaseTemplate):
    """Environmental impact assessment template.

    Implements:
        EnvironmentalImpactTemplate with impact scoring

    Features:
    - Impact identification matrix
    - Magnitude, duration, reversibility scoring
    - Impact significance calculation
    - Mitigation measures tracking
    - Cumulative impact assessment

    Example:
        >>> template = EnvironmentalImpactTemplate()
        >>> builder = template.generate()
        >>> builder is not None
        True
    """

    project_name: str = "Environmental Impact Assessment"
    project_phase: str = "Construction"
    num_impact_factors: int = 20
    include_mitigation: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Environmental Impact Assessment",
            description="EIA with impact significance scoring",
            category="environmental",
            tags=("eia", "impact", "assessment", "environmental"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """Validate template parameters."""
        return self.num_impact_factors > 0

    def generate(self) -> SpreadsheetBuilder:
        """Generate the environmental impact assessment spreadsheet."""
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"EIA - {self.project_name}",
            author="Environmental Team",
            subject="Environmental Impact Assessment",
            description=f"EIA for {self.project_name}",
            keywords=["eia", "impact", "environmental"],
        )

        # Impact matrix sheet
        builder.sheet("Impact Matrix")

        builder.column("ID", width="50pt", style="text")
        builder.column("Activity", width="150pt", style="text")
        builder.column("Receptor", width="120pt", style="text")
        builder.column("Impact Description", width="200pt", style="text")
        builder.column("Magnitude", width="70pt")
        builder.column("Duration", width="70pt")
        builder.column("Reversibility", width="80pt")
        builder.column("Probability", width="70pt")
        builder.column("Significance", width="80pt")
        builder.column("Rating", width="80pt", style="text")

        builder.freeze(rows=2)

        builder.row(style="header_primary")
        builder.cell(f"IMPACT MATRIX: {self.project_name}", colspan=10)

        builder.row(style="header_secondary")
        builder.cell("ID")
        builder.cell("Activity")
        builder.cell("Receptor")
        builder.cell("Impact")
        builder.cell("Mag (1-5)")
        builder.cell("Dur (1-5)")
        builder.cell("Rev (1-5)")
        builder.cell("Prob (0-1)")
        builder.cell("Score")
        builder.cell("Rating")

        # Impact rows
        for i in range(1, self.num_impact_factors + 1):
            row_num = i + 2
            builder.row()
            builder.cell(f"IMP-{i:03d}")
            builder.cell("")  # Activity
            builder.cell("")  # Receptor
            builder.cell("")  # Impact description
            builder.cell("")  # Magnitude
            builder.cell("")  # Duration
            builder.cell("")  # Reversibility
            builder.cell("1")  # Probability (default 1)

            # Significance score formula
            # Score = Magnitude * Duration * Reversibility * Probability / 1.25
            builder.cell(
                f"=IF(AND(E{row_num}>0;F{row_num}>0;G{row_num}>0);"
                f"E{row_num}*F{row_num}*G{row_num}*H{row_num}/1.25;0)",
            )

            # Rating formula
            builder.cell(
                f'=IF(I{row_num}>=80;"Critical";'
                f'IF(I{row_num}>=60;"Major";'
                f'IF(I{row_num}>=40;"Moderate";'
                f'IF(I{row_num}>=20;"Minor";"Negligible"))))',
            )

        # Summary section
        builder.row()
        builder.row(style="header_secondary")
        builder.cell("SUMMARY", colspan=10)

        3 + self.num_impact_factors + 2

        builder.row()
        builder.cell("Total Impacts Identified", colspan=4, style="label")
        builder.cell(f"=COUNTA(B3:B{2 + self.num_impact_factors})")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Critical Impacts", colspan=4, style="label")
        builder.cell(f'=COUNTIF(J3:J{2 + self.num_impact_factors};"Critical")')
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Major Impacts", colspan=4, style="label")
        builder.cell(f'=COUNTIF(J3:J{2 + self.num_impact_factors};"Major")')
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Average Significance Score", colspan=4, style="label")
        builder.cell(f"=AVERAGE(I3:I{2 + self.num_impact_factors})")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        if self.include_mitigation:
            # Mitigation sheet
            builder.sheet("Mitigation Measures")

            builder.column("Impact ID", width="80pt", style="text")
            builder.column("Mitigation Measure", width="250pt", style="text")
            builder.column("Responsibility", width="120pt", style="text")
            builder.column("Timeline", width="100pt", style="text")
            builder.column("Cost Est.", width="100pt")
            builder.column("Status", width="100pt", style="text")

            builder.row(style="header_primary")
            builder.cell("MITIGATION MEASURES", colspan=6)

            builder.row(style="header_secondary")
            builder.cell("Impact ID")
            builder.cell("Mitigation Measure")
            builder.cell("Responsibility")
            builder.cell("Timeline")
            builder.cell("Cost Est.")
            builder.cell("Status")

            # Placeholder rows
            for i in range(1, min(self.num_impact_factors + 1, 21)):
                builder.row()
                builder.cell(f"IMP-{i:03d}")
                builder.cell("")
                builder.cell("")
                builder.cell("")
                builder.cell("")
                builder.cell("")

        # Scoring reference sheet
        builder.sheet("Scoring Guide")

        builder.column("Score", width="50pt")
        builder.column("Magnitude", width="200pt", style="text")
        builder.column("Duration", width="200pt", style="text")
        builder.column("Reversibility", width="200pt", style="text")

        builder.row(style="header_primary")
        builder.cell("SCORING GUIDE", colspan=4)

        builder.row(style="header_secondary")
        builder.cell("Score")
        builder.cell("Magnitude")
        builder.cell("Duration")
        builder.cell("Reversibility")

        scores = [
            (1, "Minimal", "Temporary (<1 year)", "Fully reversible"),
            (2, "Low", "Short-term (1-3 years)", "Largely reversible"),
            (3, "Moderate", "Medium-term (3-10 years)", "Partially reversible"),
            (4, "High", "Long-term (10-50 years)", "Largely irreversible"),
            (5, "Very High", "Permanent (>50 years)", "Permanent"),
        ]

        for score, magnitude, duration, reversibility in scores:
            builder.row()
            builder.cell(score)
            builder.cell(magnitude)
            builder.cell(duration)
            builder.cell(reversibility)

        return builder


__all__ = ["EnvironmentalImpactTemplate"]
