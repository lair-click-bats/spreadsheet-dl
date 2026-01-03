"""
Tolerance Stackup template for mechanical engineering.

Implements:
    REQ-C003-005: ToleranceStackupTemplate with dimension chain analysis
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class ToleranceStackupTemplate(BaseTemplate):
    """
    Tolerance Stackup analysis template.

    Generates tolerance stackup analysis with worst-case and statistical methods,
    dimension chains, and stack-up calculations.

    Implements:
        REQ-C003-005: ToleranceStackupTemplate requirements

    Features:
        - Dimension chain components
        - Nominal dimensions
        - Upper and lower tolerances
        - Worst-case stackup (arithmetic sum)
        - Statistical stackup (RSS - Root Sum Square)
        - Contributing components analysis
        - Pass/fail against specification

    Example:
        >>> template = ToleranceStackupTemplate(analysis_name="Gap Analysis")
        >>> builder = template.generate()
        >>> builder.save("tolerance_stackup.ods")
    """

    analysis_name: str = "Tolerance Stackup"
    num_dimensions: int = 10
    target_dimension: float = 10.0  # mm
    tolerance_spec: float = 0.5  # mm (±)
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Tolerance Stackup Analysis",
            description="Tolerance stackup analysis with worst-case and statistical methods",
            category="mechanical_engineering",
            tags=("tolerance", "stackup", "analysis", "dimensions"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate tolerance stackup spreadsheet.

        Returns:
            SpreadsheetBuilder configured with tolerance stackup template

        Implements:
            REQ-C003-005: Tolerance stackup template generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Tolerance Stackup - {self.analysis_name}",
            author="Engineering Department",
            subject="Tolerance Stackup Analysis",
            description=f"Tolerance stackup analysis for {self.analysis_name}",
            keywords=["tolerance", "stackup", "analysis", self.analysis_name],
        )

        # Create main stackup sheet
        builder.sheet("Tolerance Stackup")

        # Define columns
        builder.column("Component", width="150pt", style="text")
        builder.column("Direction", width="70pt", style="text")
        builder.column("Nominal (mm)", width="90pt", type="number")
        builder.column("+ Tol (mm)", width="85pt", type="number")
        builder.column("- Tol (mm)", width="85pt", type="number")
        builder.column("Total Tol (mm)", width="95pt", type="number")
        builder.column("Variance", width="90pt", type="number")
        builder.column("Notes", width="200pt", style="text")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Tolerance Stackup Analysis - {self.analysis_name}", colspan=8)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Component")
        builder.cell("Direction")
        builder.cell("Nominal (mm)")
        builder.cell("+ Tol (mm)")
        builder.cell("- Tol (mm)")
        builder.cell("Total Tol (mm)")
        builder.cell("Variance")
        builder.cell("Notes")

        # Dimension rows
        for i in range(self.num_dimensions):
            row_num = i + 3
            builder.row()
            builder.cell("", style="input")  # Component
            builder.cell("+", style="input")  # Direction (+ or -)
            builder.cell(0, style="input")  # Nominal
            builder.cell(0, style="input")  # + Tolerance
            builder.cell(0, style="input")  # - Tolerance
            # Total tolerance = + Tol + - Tol (absolute values)
            builder.cell(
                f"=ABS(D{row_num})+ABS(E{row_num})",
                style="number",
            )
            # Variance = (Total Tol / 6)^2 for 6-sigma
            builder.cell(
                f"=POWER(F{row_num}/6;2)",
                style="number",
            )
            builder.cell("", style="input")  # Notes

        # Stackup calculations
        calc_row = self.num_dimensions + 3
        builder.row()  # Blank row

        builder.row(style="section_header")
        builder.cell("Stackup Results", colspan=8)

        # Worst-case stackup
        builder.row()
        builder.cell("Worst-Case Stackup:", colspan=2, style="total_label")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("  Nominal Result:", colspan=2)
        builder.cell(
            f'=SUMIF(B3:B{calc_row - 2};"+";C3:C{calc_row - 2})-SUMIF(B3:B{calc_row - 2};"-";C3:C{calc_row - 2})',
            style="number",
        )
        builder.cell("mm")
        builder.cell("Target:", colspan=2)
        builder.cell(self.target_dimension, style="number")
        builder.cell("mm")

        builder.row()
        builder.cell("  Maximum Result:", colspan=2)
        builder.cell(
            f'=SUMIF(B3:B{calc_row - 2};"+";C3:C{calc_row - 2}+D3:D{calc_row - 2})-SUMIF(B3:B{calc_row - 2};"-";C3:C{calc_row - 2}-E3:E{calc_row - 2})',
            style="number",
        )
        builder.cell("mm")
        builder.cell("Spec Tolerance:", colspan=2)
        builder.cell(self.tolerance_spec, style="number")
        builder.cell("mm")

        builder.row()
        builder.cell("  Minimum Result:", colspan=2)
        builder.cell(
            f'=SUMIF(B3:B{calc_row - 2};"+";C3:C{calc_row - 2}-E3:E{calc_row - 2})-SUMIF(B3:B{calc_row - 2};"-";C3:C{calc_row - 2}+D3:D{calc_row - 2})',
            style="number",
        )
        builder.cell("mm")
        builder.cell("Upper Limit:", colspan=2)
        builder.cell(
            f"={self.target_dimension}+{self.tolerance_spec}",
            style="number",
        )
        builder.cell("mm")

        builder.row()
        builder.cell("  Worst-Case Range:", colspan=2)
        builder.cell(
            f"=C{calc_row + 3}-C{calc_row + 4}",  # Max - Min
            style="number",
        )
        builder.cell("mm")
        builder.cell("Lower Limit:", colspan=2)
        builder.cell(
            f"={self.target_dimension}-{self.tolerance_spec}",
            style="number",
        )
        builder.cell("mm")

        # Statistical stackup (RSS)
        builder.row()
        builder.row(style="section_header")
        builder.cell("Statistical Stackup (RSS):", colspan=8)

        builder.row()
        builder.cell("  3-Sigma Range:", colspan=2)
        builder.cell(
            f"=3*SQRT(SUM(G3:G{calc_row - 2}))",
            style="number",
        )
        builder.cell("mm")
        builder.cell("Worst-Case Status:", colspan=2)
        builder.cell(
            f'=IF(C{calc_row + 5}<={self.tolerance_spec * 2};"PASS";"FAIL")',
            style="text",
        )

        builder.row()
        builder.cell("  6-Sigma Range:", colspan=2)
        builder.cell(
            f"=6*SQRT(SUM(G3:G{calc_row - 2}))",
            style="number",
        )
        builder.cell("mm")
        builder.cell("Statistical Status:", colspan=2)
        builder.cell(
            f'=IF(C{calc_row + 9}<={self.tolerance_spec * 2};"PASS";"FAIL")',
            style="text",
        )

        # Reference notes
        builder.row()
        builder.row(style="section_header")
        builder.cell("Analysis Notes", colspan=8)

        builder.row()
        builder.cell(
            "Direction: '+' adds to stackup, '-' subtracts from stackup",
            colspan=8,
        )

        builder.row()
        builder.cell(
            "Worst-Case: Arithmetic sum of all tolerances (pessimistic)",
            colspan=8,
        )

        builder.row()
        builder.cell(
            "Statistical (RSS): Root Sum Square method assuming normal distribution",
            colspan=8,
        )

        builder.row()
        builder.cell(
            "3-Sigma: 99.73% of parts within range; 6-Sigma: 99.9999998%",
            colspan=8,
        )

        return builder

    def validate(self) -> bool:
        """
        Validate template configuration.

        Returns:
            True if configuration is valid
        """
        return self.num_dimensions > 0 and self.tolerance_spec > 0


__all__ = ["ToleranceStackupTemplate"]
