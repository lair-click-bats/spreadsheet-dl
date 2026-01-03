"""
Power budget template for power consumption analysis.

Implements:
    TASK-C002: PowerBudgetTemplate with power calculations and status indicators
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class PowerBudgetTemplate(BaseTemplate):
    """
    Power budget template for analyzing power consumption.

    Implements:
        TASK-C002: PowerBudgetTemplate requirements

    Features:
        - Columns: Component, Supply Voltage, Current (mA), Power (mW),
          % of Total, Status (OK/Warning/Critical), Notes
        - Auto-calculation: Power = Voltage × Current
        - Total power consumption
        - Chart: Power distribution pie chart
        - Conditional formatting: Red for >80% budget, yellow for >60%

    Example:
        >>> template = PowerBudgetTemplate(
        ...     project_name="IoT Device",
        ...     total_budget_mw=5000
        ... )
        >>> builder = template.generate()
        >>> builder.save("power_budget.ods")
    """

    project_name: str = "Electronic System"
    total_budget_mw: float = 10000.0  # Total power budget in milliwatts
    num_components: int = 20
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Power Budget",
            description="Power consumption analysis and budget tracking",
            category="electrical_engineering",
            tags=("power", "budget", "consumption", "analysis"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate power budget spreadsheet.

        Returns:
            SpreadsheetBuilder configured with power budget template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Power Budget - {self.project_name}",
            author="Engineering Department",
            subject="Power Budget Analysis",
            description=f"Power consumption budget for {self.project_name}",
            keywords=["power", "budget", "consumption", self.project_name],
        )

        # Create main power budget sheet
        builder.sheet("Power Budget")

        # Define columns
        builder.column("Component", width="150pt", style="text")
        builder.column("Supply Voltage (V)", width="100pt", type="number")
        builder.column("Current (mA)", width="80pt", type="number")
        builder.column("Power (mW)", width="80pt", type="number")
        builder.column("% of Total", width="80pt", type="percentage")
        builder.column("Status", width="80pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Power Budget - {self.project_name} (Budget: {self.total_budget_mw}mW)",
            colspan=7,
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Component")
        builder.cell("Voltage (V)")
        builder.cell("Current (mA)")
        builder.cell("Power (mW)")
        builder.cell("% of Total")
        builder.cell("Status")
        builder.cell("Notes")

        # Component rows
        for i in range(self.num_components):
            row_num = i + 3
            total_row = self.num_components + 3
            builder.row()
            builder.cell("", style="input")  # Component name
            builder.cell(0, style="input")  # Supply Voltage
            builder.cell(0, style="input")  # Current (mA)
            builder.cell(
                f"=B{row_num}*C{row_num}", style="number"
            )  # Power = V × I (mW)
            builder.cell(f"=D{row_num}/D{total_row}", style="percentage")  # % of total
            # Status: OK if <60%, Warning if 60-80%, Critical if >80%
            builder.cell(
                f'=IF(E{row_num}<0.6,"OK",IF(E{row_num}<0.8,"Warning","Critical"))',
                style="input",
            )
            builder.cell("", style="input")  # Notes

        # Total row
        total_row = self.num_components + 3
        builder.row(style="total")
        builder.cell("TOTAL POWER", style="total_label")
        builder.cell("")  # No voltage total
        builder.cell("")  # No current total
        builder.cell(f"=SUM(D3:D{total_row - 1})", style="number")  # Total power
        builder.cell("100%", style="percentage")  # Always 100%
        builder.cell("")
        builder.cell("")

        # Budget analysis section
        builder.row()  # Blank row
        builder.row(style="section_header")
        builder.cell("Budget Analysis", colspan=7)

        builder.row()
        builder.cell("Total Budget (mW):", colspan=2)
        builder.cell(self.total_budget_mw, style="number")
        builder.cell("")
        builder.cell("Budget Used:", colspan=2)
        builder.cell(f"=D{total_row}/{self.total_budget_mw}", style="percentage")

        builder.row()
        builder.cell("Total Consumption (mW):", colspan=2)
        builder.cell(f"=D{total_row}", style="number")
        builder.cell("")
        builder.cell("Remaining Budget (mW):", colspan=2)
        builder.cell(f"={self.total_budget_mw}-D{total_row}", style="number")

        builder.row()
        builder.cell("Average Power per Component:", colspan=2)
        builder.cell(f"=D{total_row}/{self.num_components}", style="number")
        builder.cell("")
        builder.cell("Budget Status:", colspan=2)
        builder.cell(
            f'=IF(D{total_row}>{self.total_budget_mw}*0.8,"CRITICAL",IF(D{total_row}>{self.total_budget_mw}*0.6,"WARNING","OK"))'
        )

        # Component count by status
        builder.row()
        builder.row(style="section_header")
        builder.cell("Status Summary", colspan=7)

        builder.row()
        builder.cell("Components OK:", colspan=2)
        builder.cell(f'=COUNTIF(F3:F{total_row - 1},"OK")')
        builder.cell("")
        builder.cell("Components at Warning:", colspan=2)
        builder.cell(f'=COUNTIF(F3:F{total_row - 1},"Warning")')

        builder.row()
        builder.cell("Components Critical:", colspan=2)
        builder.cell(f'=COUNTIF(F3:F{total_row - 1},"Critical")')

        return builder

    def validate(self) -> bool:
        """Validate template configuration."""
        return self.total_budget_mw > 0 and self.num_components > 0


__all__ = ["PowerBudgetTemplate"]
