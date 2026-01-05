"""Experiment Protocol Template for lab experiments.

Implements:
    ExperimentProtocolTemplate for biology domain
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class ExperimentProtocolTemplate(BaseTemplate):
    """Lab experiment protocol template.

    Implements:
        ExperimentProtocolTemplate with materials and procedures

    Features:
    - Protocol information (title, purpose, date)
    - Materials list with quantities and sources
    - Step-by-step procedures
    - Safety notes and precautions
    - Expected results section
    - Notes and observations tracking

    Example:
        >>> template = ExperimentProtocolTemplate()
        >>> builder = template.generate()
        >>> builder is not None
        True
    """

    protocol_name: str = "Lab Experiment Protocol"
    purpose: str = ""
    author: str = ""
    date: str = ""
    materials: list[str] = field(default_factory=list)
    procedures: list[str] = field(default_factory=list)
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata.

        Returns:
            TemplateMetadata for experiment protocol template

        Implements:
            Template metadata
        """
        return TemplateMetadata(
            name="Experiment Protocol",
            description="Lab experiment protocol with materials and procedures",
            category="biology",
            tags=("experiment", "protocol", "lab", "procedures"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """Generate the experiment protocol spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            ExperimentProtocolTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Protocol - {self.protocol_name}",
            author=self.author or "Lab Team",
            subject="Experimental Protocol",
            description=f"Laboratory protocol for {self.protocol_name}",
            keywords=["protocol", "experiment", "lab", self.protocol_name],
        )

        # Create protocol sheet
        builder.sheet("Protocol")

        # Define columns
        builder.column("Section", width="150pt", style="text")
        builder.column("Details", width="400pt", style="text")
        builder.column("Notes", width="200pt", style="text")

        builder.freeze(rows=1)

        # Header row
        builder.row(style="header_primary")
        builder.cell("LABORATORY PROTOCOL", colspan=3)

        # Protocol information
        builder.row()
        builder.cell("Protocol Name:", style="label")
        builder.cell(self.protocol_name or "[Enter Protocol Name]")
        builder.cell("")

        builder.row()
        builder.cell("Purpose:", style="label")
        builder.cell(self.purpose or "[Enter Purpose]")
        builder.cell("")

        builder.row()
        builder.cell("Date:", style="label")
        builder.cell(self.date or "[Enter Date]")
        builder.cell("")

        builder.row()
        builder.cell("Author:", style="label")
        builder.cell(self.author or "[Enter Author]")
        builder.cell("")

        # Blank row
        builder.row()

        # Materials section
        builder.row(style="header_secondary")
        builder.cell("MATERIALS & REAGENTS", colspan=3)

        builder.row(style="header_secondary")
        builder.cell("Item")
        builder.cell("Quantity / Concentration")
        builder.cell("Source / Catalog #")

        # Default materials or user-provided
        default_materials = [
            ("Reagent 1", "Amount", "Supplier"),
            ("Reagent 2", "Amount", "Supplier"),
            ("Equipment 1", "1 unit", "Model"),
        ]

        materials_list = self.materials if self.materials else default_materials

        for material in materials_list:
            builder.row()
            if isinstance(material, str):
                builder.cell(material)
                builder.cell("")
                builder.cell("")
            else:
                for item in material:
                    builder.cell(item)

        # Add extra blank rows for additional materials
        for _ in range(3):
            builder.row()
            builder.cell("")
            builder.cell("")
            builder.cell("")

        # Blank row
        builder.row()

        # Procedures section
        builder.row(style="header_secondary")
        builder.cell("PROCEDURE", colspan=3)

        builder.row(style="header_secondary")
        builder.cell("Step")
        builder.cell("Instruction")
        builder.cell("Notes / Time")

        # Default procedures or user-provided
        default_procedures = [
            "Prepare workspace and gather materials",
            "Step-by-step instructions here",
            "Record observations and results",
        ]

        procedures_list = self.procedures if self.procedures else default_procedures

        for idx, procedure in enumerate(procedures_list, start=1):
            builder.row()
            builder.cell(f"Step {idx}")
            builder.cell(procedure)
            builder.cell("")

        # Add extra blank rows for additional steps
        for idx in range(len(procedures_list) + 1, len(procedures_list) + 6):
            builder.row()
            builder.cell(f"Step {idx}")
            builder.cell("")
            builder.cell("")

        # Blank row
        builder.row()

        # Safety notes section
        builder.row(style="header_secondary")
        builder.cell("SAFETY NOTES", colspan=3)

        builder.row()
        builder.cell("Hazards:", style="label")
        builder.cell("[List potential hazards]", colspan=2)

        builder.row()
        builder.cell("PPE Required:", style="label")
        builder.cell("[Lab coat, gloves, safety glasses, etc.]", colspan=2)

        builder.row()
        builder.cell("Waste Disposal:", style="label")
        builder.cell("[Disposal procedures]", colspan=2)

        # Blank row
        builder.row()

        # Expected results section
        builder.row(style="header_secondary")
        builder.cell("EXPECTED RESULTS", colspan=3)

        builder.row()
        builder.cell("[Describe expected outcomes]", colspan=3)

        # Blank row
        builder.row()

        # Observations sheet
        builder.sheet("Observations")

        builder.column("Date", width="100pt", type="date")
        builder.column("Time", width="80pt", style="text")
        builder.column("Observation", width="350pt", style="text")
        builder.column("Measured Value", width="120pt", style="text")
        builder.column("Notes", width="200pt", style="text")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Date")
        builder.cell("Time")
        builder.cell("Observation")
        builder.cell("Measured Value")
        builder.cell("Notes")

        # Add blank rows for observations
        for _ in range(20):
            builder.row()
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")

        return builder


__all__ = ["ExperimentProtocolTemplate"]
