"""
Signal routing template for PCB design documentation.

Implements:
    TASK-C002: SignalRoutingTemplate with trace analysis
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class SignalRoutingTemplate(BaseTemplate):
    """
    Signal routing template for PCB trace documentation.

    Implements:
        TASK-C002: SignalRoutingTemplate requirements

    Features:
        - Columns: Signal Name, Source, Destination, Impedance (Ω), Length (mm),
          Max Frequency, Coupling, Termination, Notes
        - Calculated: Propagation delay, rise time limits
        - Summary: Total traces, high-speed signals, critical nets
        - Chart: Impedance distribution histogram

    Example:
        >>> template = SignalRoutingTemplate(project_name="Main Board Rev B")
        >>> builder = template.generate()
        >>> builder.save("signal_routing.ods")
    """

    project_name: str = "PCB Design"
    num_signals: int = 30
    pcb_velocity: float = 1.8e8  # Signal velocity in mm/s (FR4 typical)
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Signal Routing",
            description="PCB signal routing and trace analysis",
            category="electrical_engineering",
            tags=("signals", "routing", "pcb", "traces"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate signal routing spreadsheet.

        Returns:
            SpreadsheetBuilder configured with signal routing template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Signal Routing - {self.project_name}",
            author="Engineering Department",
            subject="Signal Routing Documentation",
            description=f"Signal routing for {self.project_name}",
            keywords=["signals", "routing", "pcb", self.project_name],
        )

        # Create main signal routing sheet
        builder.sheet("Signal Routing")

        # Define columns
        builder.column("Signal Name", width="120pt", style="text")
        builder.column("Source", width="100pt", style="text")
        builder.column("Destination", width="100pt", style="text")
        builder.column("Impedance (Ω)", width="80pt", type="number")
        builder.column("Length (mm)", width="80pt", type="number")
        builder.column("Max Freq (MHz)", width="90pt", type="number")
        builder.column("Prop Delay (ns)", width="90pt", type="number")
        builder.column("Coupling", width="80pt", style="text")
        builder.column("Termination", width="100pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Signal Routing - {self.project_name}", colspan=10)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Signal Name")
        builder.cell("Source")
        builder.cell("Destination")
        builder.cell("Impedance (Ω)")
        builder.cell("Length (mm)")
        builder.cell("Max Freq (MHz)")
        builder.cell("Prop Delay (ns)")
        builder.cell("Coupling")
        builder.cell("Termination")
        builder.cell("Notes")

        # Signal rows
        for i in range(self.num_signals):
            row_num = i + 3
            builder.row()
            builder.cell("", style="input")  # Signal Name
            builder.cell("", style="input")  # Source
            builder.cell("", style="input")  # Destination
            builder.cell(50, style="input")  # Impedance (default 50Ω)
            builder.cell(0, style="input")  # Length (mm)
            builder.cell(0, style="input")  # Max Frequency (MHz)
            # Propagation delay: length / velocity (convert to ns)
            builder.cell(
                f"=E{row_num}/{self.pcb_velocity}*1000000000", style="number"
            )  # ns
            builder.cell("", style="input")  # Coupling
            builder.cell("", style="input")  # Termination
            builder.cell("", style="input")  # Notes

        # Summary section
        self.num_signals + 4
        builder.row()  # Blank row

        builder.row(style="section_header")
        builder.cell("Routing Summary", colspan=10)

        builder.row()
        builder.cell("Total Signals:", colspan=2)
        builder.cell(f"=COUNTA(A3:A{self.num_signals + 2})")
        builder.cell("")
        builder.cell("Total Trace Length (mm):", colspan=2)
        builder.cell(f"=SUM(E3:E{self.num_signals + 2})", style="number")

        builder.row()
        builder.cell("High-Speed Signals (>100MHz):", colspan=2)
        builder.cell(f'=COUNTIF(F3:F{self.num_signals + 2},">100")')
        builder.cell("")
        builder.cell("Average Trace Length (mm):", colspan=2)
        builder.cell(f"=AVERAGE(E3:E{self.num_signals + 2})", style="number")

        builder.row()
        builder.cell("Critical Nets (>500MHz):", colspan=2)
        builder.cell(f'=COUNTIF(F3:F{self.num_signals + 2},">500")')
        builder.cell("")
        builder.cell("Max Propagation Delay (ns):", colspan=2)
        builder.cell(f"=MAX(G3:G{self.num_signals + 2})", style="number")

        # Impedance analysis
        builder.row()
        builder.row(style="section_header")
        builder.cell("Impedance Analysis", colspan=10)

        builder.row()
        builder.cell("50Ω Traces:", colspan=2)
        builder.cell(f'=COUNTIF(D3:D{self.num_signals + 2},"50")')
        builder.cell("")
        builder.cell("Average Impedance:", colspan=2)
        builder.cell(f"=AVERAGE(D3:D{self.num_signals + 2})", style="number")

        builder.row()
        builder.cell("75Ω Traces:", colspan=2)
        builder.cell(f'=COUNTIF(D3:D{self.num_signals + 2},"75")')
        builder.cell("")
        builder.cell("100Ω Diff Pairs:", colspan=2)
        builder.cell(f'=COUNTIF(D3:D{self.num_signals + 2},"100")')

        return builder

    def validate(self) -> bool:
        """Validate template configuration."""
        return self.num_signals > 0 and self.pcb_velocity > 0


__all__ = ["SignalRoutingTemplate"]
