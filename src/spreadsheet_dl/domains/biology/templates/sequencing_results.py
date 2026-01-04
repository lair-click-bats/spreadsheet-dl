"""
Sequencing Results Template for DNA/RNA sequencing.

Implements:
    TASK-C006: SequencingResultsTemplate for biology domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class SequencingResultsTemplate(BaseTemplate):
    """
    DNA/RNA sequencing results template.

    Implements:
        TASK-C006: SequencingResultsTemplate with quality metrics

    Features:
    - Sample information and metadata
    - Quality metrics (Q30, GC content, read counts)
    - Sequence statistics
    - Coverage analysis
    - Variant calling summary
    - Alignment statistics

    Example:
        >>> template = SequencingResultsTemplate(
        ...     project_name="Genome Sequencing Project",
        ...     sequencing_type="Illumina NextSeq",
        ... )
        >>> builder = template.generate()
        >>> builder.save("sequencing_results.ods")
    """

    project_name: str = "Sequencing Project"
    num_samples: int = 10
    sequencing_type: str = "Illumina"  # Illumina, Nanopore, PacBio, etc.
    analysis_date: str = ""
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for sequencing results template

        Implements:
            TASK-C006: Template metadata
        """
        return TemplateMetadata(
            name="Sequencing Results",
            description="DNA/RNA sequencing results with quality metrics",
            category="biology",
            tags=("sequencing", "ngs", "genomics", "quality-control"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the sequencing results spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C006: SequencingResultsTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Sequencing - {self.project_name}",
            author="Genomics Team",
            subject="Sequencing Results",
            description=f"Sequencing results and QC for {self.project_name}",
            keywords=["sequencing", "ngs", "quality-control"],
        )

        # Create sample info sheet
        builder.sheet("Sample Information")

        builder.column("Sample ID", width="120pt", style="text")
        builder.column("Sample Name", width="150pt", style="text")
        builder.column("Organism", width="150pt", style="text")
        builder.column("Library Prep", width="120pt", style="text")
        builder.column("Index", width="100pt", style="text")
        builder.column("Notes", width="250pt", style="text")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Sample ID")
        builder.cell("Sample Name")
        builder.cell("Organism")
        builder.cell("Library Prep")
        builder.cell("Index/Barcode")
        builder.cell("Notes")

        # Add sample rows
        for i in range(1, 21):
            builder.row()
            builder.cell(f"Sample_{i:02d}")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")

        # Create QC metrics sheet
        builder.sheet("QC Metrics")

        builder.column("Sample ID", width="120pt", style="text")
        builder.column("Total Reads", width="120pt", type="number")
        builder.column("Passed Filter (%)", width="100pt", type="percentage")
        builder.column("Q30 (%)", width="80pt", type="percentage")
        builder.column("GC Content (%)", width="100pt", type="percentage")
        builder.column("Mean Quality", width="100pt", type="number")
        builder.column("Read Length", width="100pt", type="number")
        builder.column("Status", width="100pt", style="text")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Sample ID")
        builder.cell("Total Reads")
        builder.cell("Passed Filter %")
        builder.cell("Q30 %")
        builder.cell("GC Content %")
        builder.cell("Mean Quality Score")
        builder.cell("Mean Read Length")
        builder.cell("QC Status")

        # Add QC rows with conditional formatting logic
        for i in range(2, 22):
            builder.row()
            builder.cell(f"='Sample Information'.A{i}")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell(f'=IF(D{i}>0.8;"PASS";"REVIEW")')

        # Create alignment stats sheet
        builder.sheet("Alignment Stats")

        builder.column("Sample ID", width="120pt", style="text")
        builder.column("Mapped Reads", width="120pt", type="number")
        builder.column("Mapping Rate (%)", width="100pt", type="percentage")
        builder.column("Properly Paired (%)", width="120pt", type="percentage")
        builder.column("Duplicates (%)", width="100pt", type="percentage")
        builder.column("Mean Coverage", width="100pt", type="number")
        builder.column("Coverage >10x (%)", width="120pt", type="percentage")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Sample ID")
        builder.cell("Mapped Reads")
        builder.cell("Mapping Rate %")
        builder.cell("Properly Paired %")
        builder.cell("Duplicates %")
        builder.cell("Mean Coverage")
        builder.cell("Coverage >10x %")

        # Add alignment rows
        for i in range(2, 22):
            builder.row()
            builder.cell(f"='Sample Information'.A{i}")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")

        # Create variant summary sheet
        builder.sheet("Variant Summary")

        builder.column("Sample ID", width="120pt", style="text")
        builder.column("Total Variants", width="120pt", type="number")
        builder.column("SNPs", width="100pt", type="number")
        builder.column("Indels", width="100pt", type="number")
        builder.column("High Impact", width="100pt", type="number")
        builder.column("Moderate Impact", width="100pt", type="number")
        builder.column("Low Impact", width="100pt", type="number")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Sample ID")
        builder.cell("Total Variants")
        builder.cell("SNPs")
        builder.cell("Indels")
        builder.cell("High Impact")
        builder.cell("Moderate Impact")
        builder.cell("Low Impact")

        # Add variant rows
        for i in range(2, 22):
            builder.row()
            builder.cell(f"='Sample Information'.A{i}")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")

        # Create summary dashboard
        builder.sheet("Summary")

        builder.column("Metric", width="200pt", style="text")
        builder.column("Value", width="150pt", style="text")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("PROJECT SUMMARY", colspan=2)

        builder.row()
        builder.cell("Project Name:")
        builder.cell(self.project_name)

        builder.row()
        builder.cell("Sequencing Platform:")
        builder.cell(self.sequencing_type)

        builder.row()
        builder.cell("Analysis Date:")
        builder.cell(self.analysis_date or "[Date]")

        builder.row()
        builder.cell("Total Samples:")
        builder.cell("=COUNTA('Sample Information'.A2:A21)")

        builder.row()
        builder.cell("Samples Passed QC:")
        builder.cell("=COUNTIF('QC Metrics'.H2:H21;\"PASS\")")

        builder.row()
        builder.cell("Average Q30:")
        builder.cell("=AVERAGE('QC Metrics'.D2:D21)")

        builder.row()
        builder.cell("Average Mapping Rate:")
        builder.cell("=AVERAGE('Alignment Stats'.C2:C21)")

        builder.row()
        builder.cell("Total Variants:")
        builder.cell("=SUM('Variant Summary'.B2:B21)")

        return builder


__all__ = ["SequencingResultsTemplate"]
