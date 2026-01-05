"""Timing Analysis Template for digital design and FPGA development.

Implements:
    TimingAnalysisTemplate for setup/hold analysis and clock domain crossing
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class TimingAnalysisTemplate(BaseTemplate):
    """Timing analysis template for digital circuit timing verification.

    Implements:
        TimingAnalysisTemplate for FPGA and ASIC timing analysis

    Features:
    - Setup and hold time calculations
    - Clock-to-Q delay tracking
    - Path delay analysis with slack calculation
    - Clock domain crossing documentation
    - Timing constraint generation
    - Multi-clock domain support
    - Timing margin analysis
    - Critical path identification

    Example:
        >>> template = TimingAnalysisTemplate()
        >>> builder = template.generate()
        >>> builder is not None
        True
    """

    design_name: str = "Digital Design"
    target_frequency_mhz: float = 100.0
    num_clocks: int = 4
    num_paths: int = 30
    include_cdc: bool = True  # Clock Domain Crossing analysis
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Timing Analysis",
            description="Digital timing analysis with setup/hold and CDC tracking",
            category="electrical_engineering",
            tags=("timing", "fpga", "asic", "setup", "hold", "clock"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """Validate template parameters."""
        return (
            self.target_frequency_mhz > 0 and self.num_clocks > 0 and self.num_paths > 0
        )

    def generate(self) -> SpreadsheetBuilder:
        """Generate timing analysis spreadsheet.

        Returns:
            SpreadsheetBuilder configured with timing analysis template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        period_ns = 1000.0 / self.target_frequency_mhz

        builder.workbook_properties(
            title=f"Timing Analysis - {self.design_name}",
            author="Digital Design Team",
            subject="Timing Analysis",
            description=f"Timing analysis for {self.design_name} @ {self.target_frequency_mhz}MHz",
            keywords=["timing", "fpga", "setup", "hold", self.design_name],
        )

        # Create clock definitions sheet
        self._create_clocks_sheet(builder)

        # Create timing paths sheet
        self._create_paths_sheet(builder, period_ns)

        # Create CDC analysis if enabled
        if self.include_cdc:
            self._create_cdc_sheet(builder)

        # Create timing constraints reference
        self._create_constraints_sheet(builder)

        return builder

    def _create_clocks_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create clock definitions sheet."""
        builder.sheet("Clocks")

        builder.column("Clock Name", width="120pt", style="text")
        builder.column("Frequency (MHz)", width="100pt", type="number")
        builder.column("Period (ns)", width="90pt", type="number")
        builder.column("Duty Cycle (%)", width="90pt", type="number")
        builder.column("Rise Time (ns)", width="90pt", type="number")
        builder.column("Fall Time (ns)", width="90pt", type="number")
        builder.column("Jitter (ps)", width="80pt", type="number")
        builder.column("Source", width="120pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Clock Definitions: {self.design_name}", colspan=9)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Clock Name")
        builder.cell("Freq (MHz)")
        builder.cell("Period (ns)")
        builder.cell("Duty (%)")
        builder.cell("Rise (ns)")
        builder.cell("Fall (ns)")
        builder.cell("Jitter (ps)")
        builder.cell("Source")
        builder.cell("Notes")

        # Clock rows
        for i in range(self.num_clocks):
            row_num = i + 3
            builder.row()
            builder.cell("", style="input")  # Clock name
            builder.cell(self.target_frequency_mhz, style="input")  # Frequency
            builder.cell(f"=1000/B{row_num}")  # Period auto-calculated
            builder.cell(50, style="input")  # Duty cycle
            builder.cell(0.5, style="input")  # Rise time
            builder.cell(0.5, style="input")  # Fall time
            builder.cell(100, style="input")  # Jitter
            builder.cell("", style="input")  # Source
            builder.cell("", style="input")  # Notes

        # Clock relationships
        builder.row()
        builder.row(style="section_header")
        builder.cell("Clock Relationships", colspan=9)

        builder.row()
        builder.cell("Source Clock")
        builder.cell("Generated Clock")
        builder.cell("Multiplier")
        builder.cell("Divider")
        builder.cell("Phase (deg)")
        builder.cell("Relationship")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        # Sample clock relationships
        for _ in range(4):
            builder.row()
            builder.cell("", style="input")
            builder.cell("", style="input")
            builder.cell("1", style="input")
            builder.cell("1", style="input")
            builder.cell("0", style="input")
            builder.cell("", style="input")
            builder.cell("")
            builder.cell("")
            builder.cell("")

    def _create_paths_sheet(
        self, builder: SpreadsheetBuilder, period_ns: float
    ) -> None:
        """Create timing paths analysis sheet."""
        builder.sheet("Timing Paths")

        builder.column("Path ID", width="70pt", style="text")
        builder.column("Source", width="140pt", style="text")
        builder.column("Destination", width="140pt", style="text")
        builder.column("Clock", width="80pt", style="text")
        builder.column("Tsu (ns)", width="70pt", type="number")
        builder.column("Th (ns)", width="70pt", type="number")
        builder.column("Tco (ns)", width="70pt", type="number")
        builder.column("Tpath (ns)", width="80pt", type="number")
        builder.column("Setup Slack", width="85pt", type="number")
        builder.column("Hold Slack", width="80pt", type="number")
        builder.column("Status", width="70pt", style="text")
        builder.column("Notes", width="120pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Timing Paths: {self.design_name} (Target: {self.target_frequency_mhz}MHz, Period: {period_ns:.2f}ns)",
            colspan=12,
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Path ID")
        builder.cell("Source (FF/Port)")
        builder.cell("Destination (FF/Port)")
        builder.cell("Clock")
        builder.cell("Tsu (ns)")
        builder.cell("Th (ns)")
        builder.cell("Tco (ns)")
        builder.cell("Tpath (ns)")
        builder.cell("Setup Slack")
        builder.cell("Hold Slack")
        builder.cell("Status")
        builder.cell("Notes")

        # Timing path rows
        for i in range(self.num_paths):
            row_num = i + 3
            builder.row()
            builder.cell(f"P{i + 1:03d}")  # Path ID (A)
            builder.cell("", style="input")  # Source (B)
            builder.cell("", style="input")  # Destination (C)
            builder.cell("", style="input")  # Clock (D)
            builder.cell(0.5, style="input")  # Setup time Tsu (E)
            builder.cell(0.1, style="input")  # Hold time Th (F)
            builder.cell(0.3, style="input")  # Clock-to-Q Tco (G)
            builder.cell(0, style="input")  # Path delay Tpath (H)
            # Setup Slack = Period - Tco - Tpath - Tsu (I)
            builder.cell(f"={period_ns}-G{row_num}-H{row_num}-E{row_num}")
            # Hold Slack = Tco + Tpath - Th (J)
            builder.cell(f"=G{row_num}+H{row_num}-F{row_num}")
            # Status based on both setup and hold slack (K)
            builder.cell(
                f'=IF(OR(I{row_num}<0;J{row_num}<0);"FAIL";'
                f'IF(OR(I{row_num}<1;J{row_num}<0.5);"TIGHT";"PASS"))'
            )
            builder.cell("", style="input")  # Notes (L)

        # Summary statistics
        builder.row()
        builder.row(style="section_header")
        builder.cell("Timing Summary", colspan=12)

        builder.row()
        builder.cell("Total Paths:", colspan=2)
        builder.cell(f"=COUNTA(A3:A{self.num_paths + 2})")
        builder.cell("")
        builder.cell("Worst Setup Slack:", colspan=2)
        builder.cell(f"=MIN(I3:I{self.num_paths + 2})")
        builder.cell("")
        builder.cell("Worst Hold Slack:", colspan=2)
        builder.cell(f"=MIN(J3:J{self.num_paths + 2})")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Passing Paths:", colspan=2)
        builder.cell(f'=COUNTIF(K3:K{self.num_paths + 2};"PASS")')
        builder.cell("")
        builder.cell("Tight Paths:", colspan=2)
        builder.cell(f'=COUNTIF(K3:K{self.num_paths + 2};"TIGHT")')
        builder.cell("")
        builder.cell("Failing Paths:", colspan=2)
        builder.cell(f'=COUNTIF(K3:K{self.num_paths + 2};"FAIL")')
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Avg Setup Slack:", colspan=2)
        builder.cell(f"=AVERAGE(I3:I{self.num_paths + 2})")
        builder.cell("")
        builder.cell("Avg Hold Slack:", colspan=2)
        builder.cell(f"=AVERAGE(J3:J{self.num_paths + 2})")
        builder.cell("")
        builder.cell("Max Path Delay:", colspan=2)
        builder.cell(f"=MAX(H3:H{self.num_paths + 2})")
        builder.cell("")
        builder.cell("")

        # Timing formulas reference
        builder.row()
        builder.row(style="section_header")
        builder.cell("Timing Formulas", colspan=12)

        formulas = [
            ("Setup Slack", "Tclk - Tco - Tpath - Tsu", "Must be > 0 for setup timing"),
            ("Hold Slack", "Tco + Tpath - Th", "Must be > 0 for hold timing"),
            (
                "Max Frequency",
                "1 / (Tco + Tpath + Tsu)",
                "Maximum achievable frequency",
            ),
            ("Critical Path", "Path with minimum slack", "Limits overall frequency"),
        ]

        for name, formula, desc in formulas:
            builder.row()
            builder.cell(name)
            builder.cell(formula, colspan=5)
            builder.cell(desc, colspan=6)

    def _create_cdc_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create clock domain crossing analysis sheet."""
        builder.sheet("CDC Analysis")

        builder.column("CDC ID", width="70pt", style="text")
        builder.column("Source Clock", width="100pt", style="text")
        builder.column("Dest Clock", width="100pt", style="text")
        builder.column("Signal/Bus", width="120pt", style="text")
        builder.column("Width", width="60pt", type="number")
        builder.column("Synchronizer", width="100pt", style="text")
        builder.column("Stages", width="60pt", type="number")
        builder.column("MTBF (years)", width="90pt", type="number")
        builder.column("Status", width="70pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Clock Domain Crossing Analysis: {self.design_name}", colspan=10)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("CDC ID")
        builder.cell("Source Clk")
        builder.cell("Dest Clk")
        builder.cell("Signal/Bus")
        builder.cell("Width")
        builder.cell("Sync Type")
        builder.cell("Stages")
        builder.cell("MTBF (yrs)")
        builder.cell("Status")
        builder.cell("Notes")

        # CDC rows
        num_cdc = min(20, self.num_paths // 2)
        for i in range(num_cdc):
            row_num = i + 3
            builder.row()
            builder.cell(f"CDC{i + 1:03d}")
            builder.cell("", style="input")  # Source clock
            builder.cell("", style="input")  # Destination clock
            builder.cell("", style="input")  # Signal name
            builder.cell(1, style="input")  # Width (1 for single bit)
            builder.cell("2FF", style="input")  # Synchronizer type
            builder.cell(2, style="input")  # Number of stages
            builder.cell("", style="input")  # MTBF (calculated externally)
            # Status based on synchronizer and width
            builder.cell(
                f'=IF(E{row_num}>1;IF(F{row_num}="FIFO";"OK";"CHECK");IF(G{row_num}>=2;"OK";"REVIEW"))'
            )
            builder.cell("", style="input")

        # Synchronizer types reference
        builder.row()
        builder.row(style="section_header")
        builder.cell("Synchronizer Types", colspan=10)

        sync_types = [
            ("2FF", "Two flip-flop synchronizer", "Single-bit signals only"),
            ("3FF", "Three flip-flop synchronizer", "Higher MTBF requirement"),
            ("FIFO", "Asynchronous FIFO", "Multi-bit data transfer"),
            ("Gray", "Gray code + 2FF", "Multi-bit counter values"),
            (
                "Handshake",
                "Request/Acknowledge handshake",
                "Control signals, low throughput",
            ),
            ("Pulse", "Pulse synchronizer", "Edge detection across domains"),
            ("MCP", "Multi-Cycle Path", "Slow signals with timing constraint"),
        ]

        for sync_type, name, use_case in sync_types:
            builder.row()
            builder.cell(sync_type)
            builder.cell(name, colspan=3)
            builder.cell(use_case, colspan=6)

        # CDC checklist
        builder.row()
        builder.row(style="section_header")
        builder.cell("CDC Verification Checklist", colspan=10)

        checklist = [
            "All single-bit CDC signals use 2FF or 3FF synchronizers",
            "Multi-bit buses use FIFO, Gray code, or MCP constraints",
            "Reset signals are properly synchronized",
            "No reconvergent paths after CDC",
            "MTBF meets reliability requirements",
            "All CDC paths are documented and reviewed",
        ]

        for item in checklist:
            builder.row()
            builder.cell("[ ]", style="input")
            builder.cell(item, colspan=9)

    def _create_constraints_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create timing constraints reference sheet."""
        builder.sheet("Constraints")

        builder.column("Constraint Type", width="140pt", style="text")
        builder.column("Target", width="120pt", style="text")
        builder.column("Value", width="100pt", style="text")
        builder.column("SDC Command", width="300pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Timing Constraints: {self.design_name}", colspan=5)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Constraint Type")
        builder.cell("Target")
        builder.cell("Value")
        builder.cell("SDC Command")
        builder.cell("Notes")

        # Clock constraints section
        builder.row(style="section_header")
        builder.cell("Clock Constraints", colspan=5)

        period = 1000.0 / self.target_frequency_mhz
        builder.row()
        builder.cell("Primary Clock")
        builder.cell("clk", style="input")
        builder.cell(f"{period:.2f} ns", style="input")
        builder.cell(f"create_clock -period {period:.2f} -name clk [get_ports clk]")
        builder.cell("")

        builder.row()
        builder.cell("Generated Clock")
        builder.cell("", style="input")
        builder.cell("", style="input")
        builder.cell("create_generated_clock -source [get_ports clk] -divide_by 2 ...")
        builder.cell("")

        # I/O constraints section
        builder.row()
        builder.row(style="section_header")
        builder.cell("I/O Constraints", colspan=5)

        builder.row()
        builder.cell("Input Delay (max)")
        builder.cell("all_inputs", style="input")
        builder.cell("2.0 ns", style="input")
        builder.cell("set_input_delay -max 2.0 -clock clk [all_inputs]")
        builder.cell("Setup analysis")

        builder.row()
        builder.cell("Input Delay (min)")
        builder.cell("all_inputs", style="input")
        builder.cell("0.5 ns", style="input")
        builder.cell("set_input_delay -min 0.5 -clock clk [all_inputs]")
        builder.cell("Hold analysis")

        builder.row()
        builder.cell("Output Delay (max)")
        builder.cell("all_outputs", style="input")
        builder.cell("2.0 ns", style="input")
        builder.cell("set_output_delay -max 2.0 -clock clk [all_outputs]")
        builder.cell("Setup analysis")

        builder.row()
        builder.cell("Output Delay (min)")
        builder.cell("all_outputs", style="input")
        builder.cell("0.5 ns", style="input")
        builder.cell("set_output_delay -min 0.5 -clock clk [all_outputs]")
        builder.cell("Hold analysis")

        # False path/multicycle section
        builder.row()
        builder.row(style="section_header")
        builder.cell("Exceptions", colspan=5)

        builder.row()
        builder.cell("False Path")
        builder.cell("", style="input")
        builder.cell("N/A")
        builder.cell("set_false_path -from [get_clocks clk1] -to [get_clocks clk2]")
        builder.cell("Async CDC")

        builder.row()
        builder.cell("Multicycle Path")
        builder.cell("", style="input")
        builder.cell("2 cycles", style="input")
        builder.cell("set_multicycle_path 2 -setup -from ... -to ...")
        builder.cell("Slow paths")

        builder.row()
        builder.cell("Max Delay")
        builder.cell("", style="input")
        builder.cell("5.0 ns", style="input")
        builder.cell("set_max_delay 5.0 -from ... -to ...")
        builder.cell("Async paths")


__all__ = ["TimingAnalysisTemplate"]
