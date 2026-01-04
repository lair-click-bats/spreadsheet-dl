"""
Stress Analysis template for mechanical engineering.

Implements:
    REQ-C003-002: StressAnalysisTemplate with load cases and stress calculations
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class StressAnalysisTemplate(BaseTemplate):
    """
    Stress Analysis template for structural components.

    Generates a stress analysis spreadsheet with load cases, stress components,
    principal stresses, and von Mises stress calculations.

    Implements:
        REQ-C003-002: StressAnalysisTemplate requirements

    Features:
        - Multiple load cases (axial, bending, torsion)
        - Stress components (sigmax, sigmay, tauxy)
        - Principal stress calculations (sigma1, sigma2)
        - von Mises equivalent stress
        - Safety factor calculations
        - Yield strength comparison

    Example:
        >>> template = StressAnalysisTemplate(analysis_name="Beam Analysis")
        >>> builder = template.generate()
        >>> builder.save("stress_analysis.ods")
    """

    analysis_name: str = "Stress Analysis"
    num_load_cases: int = 10
    yield_strength: float = 250.0  # MPa (typical steel)
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Stress Analysis",
            description="Structural stress analysis with principal and von Mises stress",
            category="mechanical_engineering",
            tags=("stress", "analysis", "structural", "mechanics"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate stress analysis spreadsheet.

        Returns:
            SpreadsheetBuilder configured with stress analysis template

        Implements:
            REQ-C003-002: Stress analysis template generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Stress Analysis - {self.analysis_name}",
            author="Engineering Department",
            subject="Structural Stress Analysis",
            description=f"Stress analysis for {self.analysis_name}",
            keywords=["stress", "analysis", "mechanics", self.analysis_name],
        )

        # Create main analysis sheet
        builder.sheet("Stress Analysis")

        # Define columns
        builder.column("Load Case", width="80pt", style="text")
        builder.column("sigmax (MPa)", width="80pt", type="number")
        builder.column("sigmay (MPa)", width="80pt", type="number")
        builder.column("tauxy (MPa)", width="80pt", type="number")
        builder.column("sigma1 (MPa)", width="90pt", type="number")
        builder.column("sigma2 (MPa)", width="90pt", type="number")
        builder.column("von Mises (MPa)", width="110pt", type="number")
        builder.column("Safety Factor", width="100pt", type="number")
        builder.column("Status", width="80pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Stress Analysis - {self.analysis_name}", colspan=9)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Load Case")
        builder.cell("sigmax (MPa)")
        builder.cell("sigmay (MPa)")
        builder.cell("tauxy (MPa)")
        builder.cell("sigma1 (MPa)")
        builder.cell("sigma2 (MPa)")
        builder.cell("von Mises (MPa)")
        builder.cell("Safety Factor")
        builder.cell("Status")

        # Load case rows
        for i in range(self.num_load_cases):
            row_num = i + 3
            builder.row()
            builder.cell(f"Case {i + 1}", style="input")
            builder.cell(0, style="input")  # sigmax
            builder.cell(0, style="input")  # sigmay
            builder.cell(0, style="input")  # tauxy

            # Principal stress sigma1 = (sigmax + sigmay)/2 + SQRT(((sigmax - sigmay)/2)^2 + tauxy^2)
            builder.cell(
                f"=(B{row_num}+C{row_num})/2+SQRT(POWER((B{row_num}-C{row_num})/2;2)+POWER(D{row_num};2))",
                style="number",
            )

            # Principal stress sigma2 = (sigmax + sigmay)/2 - SQRT(((sigmax - sigmay)/2)^2 + tauxy^2)
            builder.cell(
                f"=(B{row_num}+C{row_num})/2-SQRT(POWER((B{row_num}-C{row_num})/2;2)+POWER(D{row_num};2))",
                style="number",
            )

            # von Mises stress = SQRT(sigmax^2 + sigmay^2 - sigmax*sigmay + 3*tauxy^2)
            builder.cell(
                f"=SQRT(POWER(B{row_num};2)+POWER(C{row_num};2)-B{row_num}*C{row_num}+3*POWER(D{row_num};2))",
                style="number",
            )

            # Safety Factor = Yield Strength / von Mises
            builder.cell(
                f'=IF(G{row_num}>0;{self.yield_strength}/G{row_num};"N/A")',
                style="number",
            )

            # Status: OK if SF >= 1.0, FAIL otherwise
            builder.cell(
                f'=IF(H{row_num}="N/A";"N/A";IF(H{row_num}>=1.0;"OK";"FAIL"))',
                style="text",
            )

        # Summary section
        summary_row = self.num_load_cases + 3
        builder.row()  # Blank row

        builder.row(style="section_header")
        builder.cell("Analysis Summary", colspan=9)

        builder.row()
        builder.cell("Material Yield Strength:", colspan=2)
        builder.cell(self.yield_strength, style="number")
        builder.cell("MPa")
        builder.cell("")
        builder.cell("Max von Mises Stress:", colspan=2)
        builder.cell(f"=MAX(G3:G{summary_row - 2})", style="number")
        builder.cell("MPa")

        builder.row()
        builder.cell("Minimum Safety Factor:", colspan=2)
        builder.cell(
            f'=MIN(IF(H3:H{summary_row - 2}="N/A";999;H3:H{summary_row - 2}))',
            style="number",
        )
        builder.cell("")
        builder.cell("")
        builder.cell("Number of Failed Cases:", colspan=2)
        builder.cell(f'=COUNTIF(I3:I{summary_row - 2};"FAIL")', style="number")

        builder.row()
        builder.row(style="section_header")
        builder.cell("Notes", colspan=9)

        builder.row()
        builder.cell(
            "sigmax, sigmay = Normal stresses in x and y directions (tension positive)",
            colspan=9,
        )

        builder.row()
        builder.cell("tauxy = Shear stress in xy plane", colspan=9)

        builder.row()
        builder.cell(
            "sigma1, sigma2 = Principal stresses (maximum and minimum normal stresses)",
            colspan=9,
        )

        builder.row()
        builder.cell(
            "von Mises = Equivalent stress for failure prediction (yield criterion)",
            colspan=9,
        )

        return builder

    def validate(self) -> bool:
        """
        Validate template configuration.

        Returns:
            True if configuration is valid
        """
        return self.num_load_cases > 0 and self.yield_strength > 0


__all__ = ["StressAnalysisTemplate"]
