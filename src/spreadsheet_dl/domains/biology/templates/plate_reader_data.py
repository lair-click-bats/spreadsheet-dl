"""
Plate Reader Data Template for microplate assays.

Implements:
    TASK-C006: PlateReaderDataTemplate for biology domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class PlateReaderDataTemplate(BaseTemplate):
    """
    Microplate reader data analysis template.

    Implements:
        TASK-C006: PlateReaderDataTemplate with absorbance/fluorescence analysis

    Features:
    - 96-well or 384-well plate layout
    - Absorbance or fluorescence data entry
    - Standard curve calculation
    - Sample concentration calculations
    - Statistical analysis (mean, SD, CV)
    - Visualization-ready format

    Example:
        >>> template = PlateReaderDataTemplate(
        ...     plate_type="96-well",
        ...     read_type="absorbance",
        ... )
        >>> builder = template.generate()
        >>> builder.save("plate_data.ods")
    """

    plate_type: str = "96-well"  # "96-well" or "384-well"
    read_type: str = "absorbance"  # "absorbance" or "fluorescence"
    wavelength: int = 450  # nm
    experiment_name: str = "Plate Reader Assay"
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for plate reader template

        Implements:
            TASK-C006: Template metadata
        """
        return TemplateMetadata(
            name="Plate Reader Data",
            description="Microplate reader data analysis (absorbance, fluorescence)",
            category="biology",
            tags=("plate-reader", "microplate", "assay", "elisa"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the plate reader data spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C006: PlateReaderDataTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Plate Data - {self.experiment_name}",
            author="Lab Team",
            subject="Microplate Assay",
            description=f"{self.read_type.title()} data from {self.plate_type} plate",
            keywords=["plate", "assay", self.read_type, self.plate_type],
        )

        # Create plate layout sheet
        builder.sheet("Plate Layout")

        # Determine plate dimensions
        rows = 8 if self.plate_type == "96-well" else 16
        cols = 12 if self.plate_type == "96-well" else 24

        # Header
        builder.column("", width="60pt")
        for col_num in range(1, cols + 1):
            builder.column(str(col_num), width="70pt", type="number")

        builder.freeze(rows=1, cols=1)

        # Column headers
        builder.row(style="header_primary")
        builder.cell("")
        for col_num in range(1, cols + 1):
            builder.cell(str(col_num))

        # Row data
        row_labels = "ABCDEFGHIJKLMNOP"[:rows]
        for row_label in row_labels:
            builder.row()
            builder.cell(row_label, style="header_secondary")
            for _ in range(cols):
                builder.cell(0, style="input")

        # Create analysis sheet
        builder.sheet("Analysis")

        builder.column("Well", width="80pt", style="text")
        builder.column("Sample ID", width="150pt", style="text")
        builder.column("Reading", width="100pt", type="number")
        builder.column("Blank Corrected", width="120pt", type="number")
        builder.column("Concentration", width="120pt", type="number")
        builder.column("Mean", width="100pt", type="number")
        builder.column("SD", width="100pt", type="number")
        builder.column("CV%", width="80pt", type="percentage")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Well")
        builder.cell("Sample ID")
        builder.cell(f"{self.read_type.title()} ({self.wavelength}nm)")
        builder.cell("Blank Corrected")
        builder.cell("Concentration")
        builder.cell("Mean")
        builder.cell("SD")
        builder.cell("CV%")

        # Add sample rows
        for i in range(20):
            builder.row()
            builder.cell(f"A{i + 1}")
            builder.cell("")
            builder.cell("")
            builder.cell("=C{}-blank_value".format(i + 2))
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")

        # Create standard curve sheet
        builder.sheet("Standard Curve")

        builder.column("Standard Conc", width="120pt", type="number")
        builder.column("Reading 1", width="100pt", type="number")
        builder.column("Reading 2", width="100pt", type="number")
        builder.column("Reading 3", width="100pt", type="number")
        builder.column("Mean", width="100pt", type="number")
        builder.column("SD", width="100pt", type="number")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Concentration")
        builder.cell("Reading 1")
        builder.cell("Reading 2")
        builder.cell("Reading 3")
        builder.cell("Mean")
        builder.cell("SD")

        # Standard concentrations
        standards = [0, 10, 25, 50, 100, 250, 500, 1000]
        for idx, conc in enumerate(standards, start=2):
            builder.row()
            builder.cell(conc)
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell(f"=AVERAGE(B{idx}:D{idx})")
            builder.cell(f"=STDEV(B{idx}:D{idx})")

        # Add curve statistics
        builder.row()
        builder.row()
        builder.row(style="header_secondary")
        builder.cell("Curve Statistics", colspan=6)

        builder.row()
        builder.cell("Slope:")
        builder.cell("=SLOPE(E2:E9;A2:A9)", colspan=2)

        builder.row()
        builder.cell("Intercept:")
        builder.cell("=INTERCEPT(E2:E9;A2:A9)", colspan=2)

        builder.row()
        builder.cell("R²:")
        builder.cell("=RSQ(E2:E9;A2:A9)", colspan=2)

        return builder


__all__ = ["PlateReaderDataTemplate"]
