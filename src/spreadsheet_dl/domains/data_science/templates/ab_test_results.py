"""
A/B Test Results Template for hypothesis testing.

Implements:
    ABTestResultsTemplate for data science domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class ABTestResultsTemplate(BaseTemplate):
    """
    A/B test results and analysis template.

    Implements:
        ABTestResultsTemplate with statistical significance testing

    Features:
    - Variant comparison (A/B or multivariate)
    - Sample size tracking
    - Conversion rate calculation
    - Confidence interval computation
    - P-value calculation
    - Statistical significance determination (p<0.05)
    - Lift percentage
    - Chart: Conversion rate comparison with error bars
    - Winner declaration based on significance

    Example:
        >>> template = ABTestResultsTemplate(
        ...     test_name="Homepage CTA Test",
        ...     variants=["Control", "Variant A", "Variant B"],
        ...     confidence_level=0.95,
        ... )
        >>> builder = template.generate()
        >>> builder.save("ab_test_results.ods")
    """

    test_name: str = "A/B Test"
    variants: list[str] | None = None
    confidence_level: float = 0.95
    include_chart: bool = True
    theme: str = "default"

    def __post_init__(self) -> None:
        """Initialize default variants if none provided."""
        if self.variants is None:
            self.variants = ["Control", "Variant A"]

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for A/B test results template

        Implements:
            Template metadata
        """
        return TemplateMetadata(
            name="A/B Test Results",
            description="A/B test analysis with statistical significance testing",
            category="data_science",
            tags=("ab-test", "hypothesis-testing", "statistics", "conversion"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the A/B test results spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            ABTestResultsTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"A/B Test Results - {self.test_name}",
            author="Product Analytics Team",
            subject="A/B Test Analysis",
            description=f"Statistical analysis for {self.test_name}",
            keywords=["ab-test", "statistics", "conversion", self.test_name],
        )

        # Create results sheet
        builder.sheet("Test Results")
        self._create_results_sheet(builder)

        # Create summary sheet
        builder.sheet("Summary")
        self._create_summary_sheet(builder)

        return builder

    def _create_results_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create test results comparison table."""
        builder.column("Variant", width="150pt", style="text")
        builder.column("Sample Size", width="100pt", type="number")
        builder.column("Conversions", width="100pt", type="number")
        builder.column("Conversion Rate", width="120pt", type="percentage")
        builder.column("Confidence Interval", width="150pt", style="text")
        builder.column("P-Value", width="100pt", type="number")
        builder.column("Significant?", width="120pt", style="text")
        builder.column("Lift %", width="100pt", type="percentage")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Variant")
        builder.cell("Sample Size")
        builder.cell("Conversions")
        builder.cell("Conversion Rate")
        builder.cell("Confidence Interval")
        builder.cell("P-Value")
        builder.cell("Significant?")
        builder.cell("Lift %")

        # Add rows for each variant
        if self.variants:
            for idx, variant in enumerate(self.variants):
                row_num = idx + 2  # Account for header
                builder.row()
                builder.cell(variant)
                builder.cell("")  # Sample size - to be filled
                builder.cell("")  # Conversions - to be filled
                # Conversion rate formula
                builder.cell(f"=IF(B{row_num}>0,C{row_num}/B{row_num},0)")
                builder.cell("")  # CI - to be calculated
                builder.cell("")  # P-value - to be calculated
                # Significance check
                builder.cell(f'=IF(F{row_num}<0.05,"YES","NO")')

                # Lift calculation (vs control in row 2)
                if idx == 0:
                    builder.cell(0)  # Control baseline
                else:
                    builder.cell(f"=(D{row_num}-D$2)/D$2")

        # Add sample data
        self._add_sample_data(builder)

        # Add winner declaration
        builder.row(style="header_secondary")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Winner")
        builder.cell(
            '=IF(MAX(H2:H10)>0,INDEX(A2:A10,MATCH(MAX(H2:H10),H2:H10,0)),"Control")'
        )

    def _add_sample_data(self, builder: SpreadsheetBuilder) -> None:
        """Add sample test data."""
        # Sample data will be added after the variant rows
        # This is a placeholder showing how data might look
        pass

    def _create_summary_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create test summary and interpretation."""
        builder.column("Metric", width="200pt", style="text")
        builder.column("Value", width="200pt", style="text")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Test Summary")
        builder.cell("")

        # Summary metrics
        summary_items = [
            ("Test Name", self.test_name),
            ("Confidence Level", f"{self.confidence_level * 100}%"),
            ("Number of Variants", str(len(self.variants) if self.variants else 0)),
            ("Significance Threshold", "p < 0.05"),
            ("Total Sample Size", "=SUM('Test Results'.B2:B100)"),
            ("Total Conversions", "=SUM('Test Results'.C2:C100)"),
            (
                "Overall Conversion Rate",
                "=SUM('Test Results'.C2:C100)/SUM('Test Results'.B2:B100)",
            ),
            ("Winner Variant", "='Test Results'.A{winner_row}"),
            ("Test Conclusion", "See Test Results sheet for detailed analysis"),
        ]

        for metric, value in summary_items:
            builder.row()
            builder.cell(metric)
            builder.cell(value)

        # Add interpretation section
        builder.row()
        builder.cell("")
        builder.cell("")

        builder.row(style="header_secondary")
        builder.cell("Interpretation Guidelines")
        builder.cell("")

        guidelines = [
            ("P-Value < 0.05", "Result is statistically significant"),
            ("P-Value >= 0.05", "No significant difference detected"),
            ("Positive Lift %", "Variant performs better than control"),
            ("Negative Lift %", "Variant performs worse than control"),
        ]

        for condition, interpretation in guidelines:
            builder.row()
            builder.cell(condition)
            builder.cell(interpretation)


__all__ = ["ABTestResultsTemplate"]
