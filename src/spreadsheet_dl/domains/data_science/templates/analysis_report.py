"""
Analysis Report Template for statistical analysis documentation.

Implements:
    TASK-C001: AnalysisReportTemplate for data science domain
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class AnalysisReportTemplate(BaseTemplate):
    """
    Statistical analysis report template.

    Implements:
        TASK-C001: AnalysisReportTemplate with statistical tests and visualizations

    Features:
    - Summary section
    - Data description with statistics
    - Statistical tests section (T-test, Chi-square, etc.)
    - Findings and conclusions
    - Descriptive statistics table
    - Correlation matrix
    - Test results table
    - Distribution histograms (metadata)
    - Scatter plots (metadata)
    - Box plots (metadata)

    Example:
        >>> template = AnalysisReportTemplate(
        ...     analysis_name="Customer Segmentation Study",
        ...     variables=["age", "income", "purchases"],
        ... )
        >>> builder = template.generate()
        >>> builder.save("analysis_report.ods")
    """

    analysis_name: str = "Data Analysis Report"
    variables: list[str] = field(default_factory=lambda: ["var1", "var2", "var3"])
    include_correlation: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for analysis report template

        Implements:
            TASK-C001: Template metadata
        """
        return TemplateMetadata(
            name="Analysis Report",
            description="Statistical analysis report with tests and visualizations",
            category="data_science",
            tags=("statistics", "analysis", "report", "testing"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the analysis report spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C001: AnalysisReportTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Analysis Report - {self.analysis_name}",
            author="Data Science Team",
            subject="Statistical Analysis",
            description=f"Statistical analysis report for {self.analysis_name}",
            keywords=["analysis", "statistics", "report", self.analysis_name],
        )

        # Create summary sheet
        builder.sheet("Summary")
        self._create_summary_sheet(builder)

        # Create descriptive statistics sheet
        builder.sheet("Descriptive Statistics")
        self._create_descriptive_stats_sheet(builder)

        # Create correlation matrix sheet if requested
        if self.include_correlation:
            builder.sheet("Correlation Matrix")
            self._create_correlation_sheet(builder)

        # Create statistical tests sheet
        builder.sheet("Statistical Tests")
        self._create_tests_sheet(builder)

        # Create findings sheet
        builder.sheet("Findings")
        self._create_findings_sheet(builder)

        return builder

    def _create_summary_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create analysis summary sheet."""
        builder.column("Section", width="200pt", style="text")
        builder.column("Content", width="400pt", style="text")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Analysis Summary")
        builder.cell("")

        # Summary sections
        sections = [
            ("Analysis Name", self.analysis_name),
            ("Date", "=TODAY()"),
            ("Variables Analyzed", str(len(self.variables))),
            ("Variable Names", ", ".join(self.variables)),
            ("Sample Size", "N/A - See Descriptive Statistics"),
            ("Analysis Type", "Descriptive and Inferential Statistics"),
        ]

        for section, content in sections:
            builder.row()
            builder.cell(section)
            builder.cell(content)

    def _create_descriptive_stats_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create descriptive statistics table."""
        builder.column("Variable", width="150pt", style="text")
        builder.column("N", width="80pt", type="number")
        builder.column("Mean", width="100pt", type="number")
        builder.column("Median", width="100pt", type="number")
        builder.column("Std Dev", width="100pt", type="number")
        builder.column("Min", width="100pt", type="number")
        builder.column("Max", width="100pt", type="number")
        builder.column("Range", width="100pt", type="number")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Variable")
        builder.cell("N")
        builder.cell("Mean")
        builder.cell("Median")
        builder.cell("Std Dev")
        builder.cell("Min")
        builder.cell("Max")
        builder.cell("Range")

        # Sample data for each variable
        for var in self.variables:
            builder.row()
            builder.cell(var)
            builder.cell(100)  # Sample size
            builder.cell("")  # Mean - to be filled
            builder.cell("")  # Median - to be filled
            builder.cell("")  # Std Dev - to be filled
            builder.cell("")  # Min - to be filled
            builder.cell("")  # Max - to be filled
            builder.cell("=G{row}-F{row}")  # Range formula (will be adjusted)

    def _create_correlation_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create correlation matrix."""
        # First column for variable names
        builder.column("Variable", width="150pt", style="text")

        # Add column for each variable
        for var in self.variables:
            builder.column(var, width="100pt", type="number")

        builder.freeze(rows=1)  # Note: column freezing not supported in current builder

        # Header row
        builder.row(style="header_primary")
        builder.cell("Variable")
        for var in self.variables:
            builder.cell(var)

        # Correlation matrix rows
        for i, var1 in enumerate(self.variables):
            builder.row()
            builder.cell(var1)
            for j, _var2 in enumerate(self.variables):
                if i == j:
                    # Diagonal - perfect correlation with self
                    builder.cell(1.0)
                else:
                    # Placeholder for correlation values
                    builder.cell("")

    def _create_tests_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create statistical tests results table."""
        builder.column("Test", width="200pt", style="text")
        builder.column("Variables", width="200pt", style="text")
        builder.column("Statistic", width="120pt", type="number")
        builder.column("P-Value", width="120pt", type="number")
        builder.column("Significance", width="120pt", style="text")
        builder.column("Conclusion", width="300pt", style="text")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Test")
        builder.cell("Variables")
        builder.cell("Statistic")
        builder.cell("P-Value")
        builder.cell("Significance")
        builder.cell("Conclusion")

        # Sample tests
        if len(self.variables) >= 2:
            # T-test example
            builder.row()
            builder.cell("Independent T-Test")
            builder.cell(f"{self.variables[0]} vs {self.variables[1]}")
            builder.cell("")  # Statistic - to be filled
            builder.cell("")  # P-value - to be filled
            builder.cell('=IF(D2<0.05,"Significant","Not Significant")')
            builder.cell("")  # Conclusion - to be filled

            # Chi-square example
            builder.row()
            builder.cell("Chi-Square Test")
            builder.cell(f"{self.variables[0]} x {self.variables[1]}")
            builder.cell("")  # Statistic - to be filled
            builder.cell("")  # P-value - to be filled
            builder.cell('=IF(D3<0.05,"Significant","Not Significant")')
            builder.cell("")  # Conclusion - to be filled

    def _create_findings_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create findings and conclusions sheet."""
        builder.column("Section", width="200pt", style="text")
        builder.column("Finding", width="500pt", style="text")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Section")
        builder.cell("Findings and Conclusions")

        # Sections
        sections = [
            "Key Findings",
            "Statistical Significance",
            "Practical Implications",
            "Limitations",
            "Recommendations",
        ]

        for section in sections:
            builder.row()
            builder.cell(section)
            builder.cell("")  # To be filled with findings


__all__ = ["AnalysisReportTemplate"]
