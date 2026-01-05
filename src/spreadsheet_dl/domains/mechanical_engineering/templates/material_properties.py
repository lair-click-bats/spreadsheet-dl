"""Material Properties template for mechanical engineering.

Implements:
    MaterialPropertiesTemplate with material database
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class MaterialPropertiesTemplate(BaseTemplate):
    """Material Properties database template.

    Generates a material properties database with mechanical properties
    including yield strength, ultimate strength, Young's modulus, etc.

    Implements:
        MaterialPropertiesTemplate requirements

    Features:
        - Material name and specification
        - Yield strength (MPa)
        - Ultimate tensile strength (MPa)
        - Young's modulus (GPa)
        - Poisson's ratio
        - Density (kg/m³)
        - Coefficient of thermal expansion (10⁻⁶/°C)
        - Common material presets (steel, aluminum, titanium, etc.)

    Example:
        >>> template = MaterialPropertiesTemplate()
        >>> template.metadata.name
        'Material Properties Database'
        >>> builder = template.generate()
        >>> builder is not None
        True
    """

    num_materials: int = 20
    include_presets: bool = True
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Material Properties Database",
            description="Material properties database with mechanical and thermal properties",
            category="mechanical_engineering",
            tags=("materials", "properties", "database", "mechanics"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """Generate material properties spreadsheet.

        Returns:
            SpreadsheetBuilder configured with material properties template

        Implements:
            Material properties template generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title="Material Properties Database",
            author="Engineering Department",
            subject="Material Properties",
            description="Database of material mechanical and thermal properties",
            keywords=["materials", "properties", "database", "engineering"],
        )

        # Create main materials sheet
        builder.sheet("Materials")

        # Define columns
        builder.column("Material Name", width="150pt", style="text")
        builder.column("Specification", width="120pt", style="text")
        builder.column("Yield Strength (MPa)", width="120pt", type="number")
        builder.column("Ultimate Strength (MPa)", width="140pt", type="number")
        builder.column("Young's Modulus (GPa)", width="140pt", type="number")
        builder.column("Poisson's Ratio", width="110pt", type="number")
        builder.column("Density (kg/m³)", width="110pt", type="number")
        builder.column("CTE (10⁻⁶/°C)", width="110pt", type="number")
        builder.column("Notes", width="200pt", style="text")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell("Material Properties Database", colspan=9)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Material Name")
        builder.cell("Specification")
        builder.cell("Yield Strength (MPa)")
        builder.cell("Ultimate Strength (MPa)")
        builder.cell("Young's Modulus (GPa)")
        builder.cell("Poisson's Ratio")
        builder.cell("Density (kg/m³)")
        builder.cell("CTE (10⁻⁶/°C)")
        builder.cell("Notes")

        # Add preset materials if requested
        if self.include_presets:
            presets = [
                (
                    "Structural Steel",
                    "ASTM A36",
                    250,
                    400,
                    200,
                    0.30,
                    7850,
                    11.7,
                    "Common structural steel",
                ),
                (
                    "Stainless Steel 304",
                    "AISI 304",
                    215,
                    505,
                    193,
                    0.29,
                    8000,
                    17.3,
                    "Austenitic stainless steel",
                ),
                (
                    "Aluminum 6061-T6",
                    "AA 6061-T6",
                    276,
                    310,
                    68.9,
                    0.33,
                    2700,
                    23.6,
                    "Heat-treated aluminum alloy",
                ),
                (
                    "Titanium Grade 5",
                    "Ti-6Al-4V",
                    880,
                    950,
                    113.8,
                    0.342,
                    4430,
                    8.6,
                    "Most common titanium alloy",
                ),
                (
                    "Tool Steel",
                    "AISI D2",
                    1700,
                    2050,
                    210,
                    0.30,
                    7700,
                    11.0,
                    "High-carbon tool steel",
                ),
            ]

            for preset in presets:
                builder.row()
                for value in preset:
                    if isinstance(value, str):
                        builder.cell(value, style="text")
                    else:
                        builder.cell(value, style="number")

        # Add empty rows for user input
        remaining_rows = self.num_materials - (
            len(presets) if self.include_presets else 0
        )
        for _ in range(max(0, remaining_rows)):
            builder.row()
            builder.cell("", style="input")  # Material Name
            builder.cell("", style="input")  # Specification
            builder.cell(0, style="input")  # Yield Strength
            builder.cell(0, style="input")  # Ultimate Strength
            builder.cell(0, style="input")  # Young's Modulus
            builder.cell(0, style="input")  # Poisson's Ratio
            builder.cell(0, style="input")  # Density
            builder.cell(0, style="input")  # CTE
            builder.cell("", style="input")  # Notes

        # Summary section
        data_start = 3
        data_end = self.num_materials + 2
        builder.row()  # Blank row

        builder.row(style="section_header")
        builder.cell("Database Statistics", colspan=9)

        builder.row()
        builder.cell("Total Materials:", colspan=2)
        builder.cell(f"=COUNTA(A{data_start}:A{data_end})", style="number")
        builder.cell("")
        builder.cell("Average Young's Modulus:", colspan=2)
        builder.cell(f"=AVERAGE(E{data_start}:E{data_end})", style="number")
        builder.cell("GPa")

        builder.row()
        builder.cell("Highest Yield Strength:", colspan=2)
        builder.cell(f"=MAX(C{data_start}:C{data_end})", style="number")
        builder.cell("MPa")
        builder.cell("Lowest Density:", colspan=2)
        builder.cell(f"=MIN(G{data_start}:G{data_end})", style="number")
        builder.cell("kg/m³")

        # Add reference notes
        builder.row()
        builder.row(style="section_header")
        builder.cell("Reference Notes", colspan=9)

        builder.row()
        builder.cell(
            "Yield Strength: Stress at which material begins permanent deformation",
            colspan=9,
        )

        builder.row()
        builder.cell(
            "Ultimate Strength: Maximum stress material can withstand before failure",
            colspan=9,
        )

        builder.row()
        builder.cell(
            "Young's Modulus: Stiffness of material (stress/strain ratio)", colspan=9
        )

        builder.row()
        builder.cell("Poisson's Ratio: Ratio of transverse to axial strain", colspan=9)

        builder.row()
        builder.cell(
            "CTE: Coefficient of Thermal Expansion (length change per temperature change)",
            colspan=9,
        )

        return builder

    def validate(self) -> bool:
        """Validate template configuration.

        Returns:
            True if configuration is valid
        """
        return self.num_materials > 0


__all__ = ["MaterialPropertiesTemplate"]
