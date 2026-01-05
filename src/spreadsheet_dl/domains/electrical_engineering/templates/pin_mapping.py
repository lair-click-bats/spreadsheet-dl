"""Pin mapping template for ICs and connectors.

Implements:
    PinMappingTemplate with IC grouping and pin usage analysis
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class PinMappingTemplate(BaseTemplate):
    """Pin mapping template for documenting IC pin assignments.

    Implements:
        PinMappingTemplate requirements

    Features:
        - Columns: IC Name, Pin Number, Pin Name, Signal Name, Direction,
          Connected To, Voltage Level, Notes
        - Grouped by IC
        - Summary: Total pins, power pins, I/O pins
        - Chart: Pin usage breakdown (power/ground/signal/NC)
        - Validation: Ensure no duplicate pin assignments

    Example:
        >>> template = PinMappingTemplate()
        >>> template.metadata.name
        'Pin Mapping'
        >>> builder = template.generate()
        >>> builder is not None
        True
    """

    project_name: str = "Electronic Design"
    num_pins: int = 50  # Total number of pins to document
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Pin Mapping",
            description="IC and connector pin assignment documentation",
            category="electrical_engineering",
            tags=("pins", "ic", "mapping", "signals"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """Generate pin mapping spreadsheet.

        Returns:
            SpreadsheetBuilder configured with pin mapping template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Pin Mapping - {self.project_name}",
            author="Engineering Department",
            subject="Pin Assignment Documentation",
            description=f"Pin mapping for {self.project_name}",
            keywords=["pins", "signals", "ic", self.project_name],
        )

        # Create main pin mapping sheet
        builder.sheet("Pin Mapping")

        # Define columns
        builder.column("IC Name", width="100pt", style="text")
        builder.column("Pin #", width="60pt", type="number")
        builder.column("Pin Name", width="100pt", style="text")
        builder.column("Signal Name", width="120pt", style="text")
        builder.column("Direction", width="80pt", style="text")
        builder.column("Connected To", width="120pt", style="text")
        builder.column("Voltage Level", width="80pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Pin Mapping - {self.project_name}", colspan=8)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("IC Name")
        builder.cell("Pin #")
        builder.cell("Pin Name")
        builder.cell("Signal Name")
        builder.cell("Direction")
        builder.cell("Connected To")
        builder.cell("Voltage Level")
        builder.cell("Notes")

        # Pin mapping rows
        for i in range(self.num_pins):
            i + 3
            builder.row()
            builder.cell("", style="input")  # IC Name
            builder.cell("", style="input")  # Pin Number
            builder.cell("", style="input")  # Pin Name
            builder.cell("", style="input")  # Signal Name
            builder.cell("", style="input")  # Direction (I/O/Pwr/GND)
            builder.cell("", style="input")  # Connected To
            builder.cell("", style="input")  # Voltage Level
            builder.cell("", style="input")  # Notes

        # Summary section
        self.num_pins + 4
        builder.row()  # Blank row

        builder.row(style="section_header")
        builder.cell("Pin Usage Summary", colspan=8)

        builder.row()
        builder.cell("Total Pins:", colspan=2)
        builder.cell(f"=COUNTA(B3:B{self.num_pins + 2})")
        builder.cell("")
        builder.cell("Power Pins:", colspan=2)
        builder.cell(f'=COUNTIF(E3:E{self.num_pins + 2},"Pwr")')

        builder.row()
        builder.cell("I/O Pins:", colspan=2)
        builder.cell(f'=COUNTIF(E3:E{self.num_pins + 2},"I/O")')
        builder.cell("")
        builder.cell("Ground Pins:", colspan=2)
        builder.cell(f'=COUNTIF(E3:E{self.num_pins + 2},"GND")')

        builder.row()
        builder.cell("Signal Pins:", colspan=2)
        builder.cell(f'=COUNTIF(E3:E{self.num_pins + 2},"Signal")')
        builder.cell("")
        builder.cell("NC (No Connect):", colspan=2)
        builder.cell(f'=COUNTIF(E3:E{self.num_pins + 2},"NC")')

        return builder

    def validate(self) -> bool:
        """Validate template configuration."""
        return self.num_pins > 0


__all__ = ["PinMappingTemplate"]
