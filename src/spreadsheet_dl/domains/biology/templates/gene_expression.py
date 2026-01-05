"""
Gene Expression Analysis Template for qPCR data.

Implements:
    GeneExpressionTemplate for biology domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class GeneExpressionTemplate(BaseTemplate):
    """
    Gene expression analysis template (qPCR).

    Implements:
        GeneExpressionTemplate with fold change calculations

    Features:
    - Sample information tracking
    - Ct value data entry (target and reference genes)
    - ΔCt and ΔΔCt calculations
    - Fold change calculation (2^-ΔΔCt method)
    - Statistical analysis (replicates, SD, SEM)
    - Normalized expression values

    Example:
        >>> template = GeneExpressionTemplate(
        ...     experiment_name="Stress Response",
        ...     num_genes=20,
        ... )
        >>> builder = template.generate()
        >>> builder.save("gene_expression.ods")
    """

    experiment_name: str = "Gene Expression Analysis"
    num_genes: int = 10
    reference_gene: str = "GAPDH"
    control_sample: str = "Control"
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for gene expression template

        Implements:
            Template metadata
        """
        return TemplateMetadata(
            name="Gene Expression",
            description="Gene expression analysis with fold change calculations",
            category="biology",
            tags=("qpcr", "gene-expression", "rt-qpcr", "fold-change"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """
        Validate template parameters.

        Returns:
            True if parameters are valid, False otherwise
        """
        return self.num_genes > 0

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the gene expression spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            GeneExpressionTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Gene Expression - {self.experiment_name}",
            author="Research Team",
            subject="qPCR Gene Expression",
            description=f"Gene expression analysis for {self.experiment_name}",
            keywords=["qpcr", "gene-expression", "fold-change"],
        )

        # Create Ct values sheet
        builder.sheet("Ct Values")

        builder.column("Sample", width="120pt", style="text")
        builder.column("Gene", width="100pt", style="text")
        builder.column("Replicate", width="80pt", type="number")
        builder.column("Ct Value", width="100pt", type="number")
        builder.column("Mean Ct", width="100pt", type="number")
        builder.column("SD", width="80pt", type="number")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Sample")
        builder.cell("Gene")
        builder.cell("Replicate")
        builder.cell("Ct Value")
        builder.cell("Mean Ct")
        builder.cell("SD")

        # Add sample data rows
        samples = ["Control", "Treatment1", "Treatment2"]
        for sample in samples:
            # Reference gene
            for rep in range(1, 4):
                builder.row()
                builder.cell(sample)
                builder.cell(self.reference_gene)
                builder.cell(rep)
                builder.cell("")
                if rep == 1:
                    # Mean formula spans all replicates
                    row_start = len(samples) * 3 + 2
                    builder.cell(f"=AVERAGE(D{row_start}:D{row_start + 2})")
                    builder.cell(f"=STDEV(D{row_start}:D{row_start + 2})")
                else:
                    builder.cell("")
                    builder.cell("")

            # Target genes
            for gene_idx in range(self.num_genes):
                gene = f"Gene{gene_idx + 1}"
                for rep in range(1, 4):
                    builder.row()
                    builder.cell(sample)
                    builder.cell(gene)
                    builder.cell(rep)
                    builder.cell("")
                    if rep == 1:
                        row_start = len(samples) * 3 + 2
                        builder.cell(f"=AVERAGE(D{row_start}:D{row_start + 2})")
                        builder.cell(f"=STDEV(D{row_start}:D{row_start + 2})")
                    else:
                        builder.cell("")
                        builder.cell("")

        # Create analysis sheet
        builder.sheet("Analysis")

        builder.column("Sample", width="120pt", style="text")
        builder.column("Gene", width="100pt", style="text")
        builder.column("Ct Target", width="100pt", type="number")
        builder.column("Ct Reference", width="100pt", type="number")
        builder.column("ΔCt", width="100pt", type="number")
        builder.column("ΔΔCt", width="100pt", type="number")
        builder.column("Fold Change", width="120pt", type="number")
        builder.column("log2 FC", width="100pt", type="number")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Sample")
        builder.cell("Gene")
        builder.cell("Ct Target")
        builder.cell("Ct Reference")
        builder.cell("ΔCt")
        builder.cell("ΔΔCt")
        builder.cell("Fold Change (2^-ΔΔCt)")
        builder.cell("log2 FC")

        # Add analysis rows for each sample and gene
        for idx, sample in enumerate(samples, start=2):
            for gene_idx in range(self.num_genes):
                gene = f"Gene{gene_idx + 1}"
                builder.row()
                builder.cell(sample)
                builder.cell(gene)
                builder.cell("")  # Ct target - link to Ct Values sheet
                builder.cell("")  # Ct reference
                builder.cell(f"=C{idx}-D{idx}")  # ΔCt = Ct_target - Ct_ref
                # ΔΔCt = ΔCt - ΔCt_control
                if sample == self.control_sample:
                    builder.cell(0)  # Control ΔΔCt = 0
                else:
                    builder.cell(f"=E{idx}-E2")  # Subtract control ΔCt
                builder.cell(f"=POWER(2;-F{idx})")  # 2^-ΔΔCt
                builder.cell(f"=LOG(G{idx};2)")  # log2(FC)

        # Add summary statistics sheet
        builder.sheet("Summary")

        builder.column("Gene", width="120pt", style="text")
        builder.column("Sample", width="120pt", style="text")
        builder.column("Fold Change", width="120pt", type="number")
        builder.column("Regulation", width="100pt", style="text")
        builder.column("Significance", width="100pt", style="text")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Gene")
        builder.cell("Sample")
        builder.cell("Fold Change")
        builder.cell("Regulation")
        builder.cell("Significance")

        # Add summary rows
        for gene_idx in range(self.num_genes):
            gene = f"Gene{gene_idx + 1}"
            for sample in samples[1:]:  # Exclude control
                builder.row()
                builder.cell(gene)
                builder.cell(sample)
                builder.cell("")  # Link to Analysis sheet
                builder.cell('=IF(C2>2;"Up";IF(C2<0.5;"Down";"No Change"))')
                builder.cell("")

        return builder


__all__ = ["GeneExpressionTemplate"]
