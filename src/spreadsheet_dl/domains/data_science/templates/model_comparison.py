"""Model Comparison Template for ML model evaluation.

Implements:
    ModelComparisonTemplate for data science domain
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class ModelComparisonTemplate(BaseTemplate):
    """ML model comparison and evaluation template.

    Implements:
        ModelComparisonTemplate with multi-metric evaluation

    Features:
    - Multiple model comparison
    - Performance metrics (accuracy, precision, recall, F1)
    - Training and inference time tracking
    - Model size tracking
    - Notes field
    - Best model highlighting (conditional formatting metadata)
    - Chart: Multi-metric radar chart (metadata)
    - Confusion matrix section for each model
    - Overall winner determination

    Example:
        >>> template = ModelComparisonTemplate()
        >>> builder = template.generate()
        >>> builder is not None
        True
    """

    project_name: str = "ML Model Comparison"
    models: list[str] = field(default_factory=lambda: ["Model A", "Model B"])
    metrics: list[str] = field(
        default_factory=lambda: ["accuracy", "precision", "recall", "f1"]
    )
    include_confusion_matrix: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata.

        Returns:
            TemplateMetadata for model comparison template

        Implements:
            Template metadata
        """
        return TemplateMetadata(
            name="Model Comparison",
            description="ML model comparison with performance metrics and evaluation",
            category="data_science",
            tags=("ml", "models", "comparison", "evaluation", "metrics"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """Generate the model comparison spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            ModelComparisonTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Model Comparison - {self.project_name}",
            author="ML Engineering Team",
            subject="Model Evaluation",
            description=f"Model comparison and evaluation for {self.project_name}",
            keywords=["ml", "models", "evaluation", self.project_name],
        )

        # Create comparison sheet
        builder.sheet("Model Comparison")
        self._create_comparison_sheet(builder)

        # Create confusion matrices sheet if requested
        if self.include_confusion_matrix:
            builder.sheet("Confusion Matrices")
            self._create_confusion_matrices_sheet(builder)

        # Create recommendations sheet
        builder.sheet("Recommendations")
        self._create_recommendations_sheet(builder)

        return builder

    def _create_comparison_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create model comparison table."""
        builder.column("Model", width="150pt", style="text")
        builder.column("Accuracy", width="100pt", type="percentage")
        builder.column("Precision", width="100pt", type="percentage")
        builder.column("Recall", width="100pt", type="percentage")
        builder.column("F1 Score", width="100pt", type="percentage")
        builder.column("Training Time (s)", width="120pt", type="number")
        builder.column("Inference Time (ms)", width="130pt", type="number")
        builder.column("Model Size (MB)", width="120pt", type="number")
        builder.column("Notes", width="250pt", style="text")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Model")
        builder.cell("Accuracy")
        builder.cell("Precision")
        builder.cell("Recall")
        builder.cell("F1 Score")
        builder.cell("Training Time (s)")
        builder.cell("Inference Time (ms)")
        builder.cell("Model Size (MB)")
        builder.cell("Notes")

        # Add rows for each model
        for model in self.models:
            builder.row()
            builder.cell(model)
            builder.cell("")  # Accuracy - to be filled
            builder.cell("")  # Precision - to be filled
            builder.cell("")  # Recall - to be filled
            builder.cell("")  # F1 - to be filled
            builder.cell("")  # Training time - to be filled
            builder.cell("")  # Inference time - to be filled
            builder.cell("")  # Model size - to be filled
            builder.cell("")  # Notes - to be filled

        # Add sample data
        self._add_sample_data(builder)

        # Add best model row
        builder.row()
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row(style="header_secondary")
        builder.cell("Best Model")
        builder.cell("=INDEX(A2:A100,MATCH(MAX(B2:B100),B2:B100,0))")
        builder.cell("=MAX(B2:B100)")
        builder.cell("=MAX(C2:C100)")
        builder.cell("=MAX(D2:D100)")
        builder.cell("=MAX(E2:E100)")
        builder.cell("=MIN(F2:F100)")  # Best = minimum time
        builder.cell("=MIN(G2:G100)")  # Best = minimum time
        builder.cell("=MIN(H2:H100)")  # Best = minimum size

    def _add_sample_data(self, builder: SpreadsheetBuilder) -> None:
        """Add sample model comparison data."""
        # Sample data structure (for reference - not added to template)
        # Users fill in their own model metrics
        # Sample format:
        # {
        #     "name": "ResNet50",
        #     "accuracy": 0.92,
        #     "precision": 0.91,
        #     "recall": 0.90,
        #     "f1": 0.905,
        #     "train_time": 3600,
        #     "inference_time": 25,
        #     "size": 98,
        #     "notes": "Good baseline model",
        # }
        pass  # Template provides structure only

    def _create_confusion_matrices_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create confusion matrix section for each model."""
        builder.column("Model", width="150pt", style="text")
        builder.column("", width="100pt", style="text")  # Spacer
        builder.column("Predicted Positive", width="120pt", type="number")
        builder.column("Predicted Negative", width="120pt", type="number")
        builder.column("", width="100pt", style="text")  # Spacer
        builder.column("Metrics", width="120pt", style="text")
        builder.column("Value", width="120pt", type="number")

        # Header
        builder.row(style="header_primary")
        builder.cell("Confusion Matrices")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        # Add confusion matrix for each model
        for idx, model in enumerate(self.models):
            start_row = 3 + (idx * 7)  # Space between models

            # Model name
            builder.row()
            builder.cell(f"Model: {model}")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")

            # Matrix header
            builder.row(style="header_secondary")
            builder.cell("Actual")
            builder.cell("")
            builder.cell("Predicted Positive")
            builder.cell("Predicted Negative")
            builder.cell("")
            builder.cell("Metric")
            builder.cell("Value")

            # True Positive / False Negative row
            builder.row()
            builder.cell("Positive")
            builder.cell("TP")
            builder.cell("")  # TP value
            builder.cell("")  # FN value
            builder.cell("")
            builder.cell("True Positives")
            builder.cell(f"=C{start_row + 2}")

            # False Positive / True Negative row
            builder.row()
            builder.cell("Negative")
            builder.cell("FP")
            builder.cell("")  # FP value
            builder.cell("")  # TN value
            builder.cell("")
            builder.cell("True Negatives")
            builder.cell(f"=D{start_row + 3}")

            # Calculated metrics
            builder.row()
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("Accuracy")
            tp_cell = f"C{start_row + 2}"
            tn_cell = f"D{start_row + 3}"
            fp_cell = f"C{start_row + 3}"
            fn_cell = f"D{start_row + 2}"
            builder.cell(
                f"=({tp_cell}+{tn_cell})/({tp_cell}+{tn_cell}+{fp_cell}+{fn_cell})"
            )

            builder.row()
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("Precision")
            builder.cell(f"={tp_cell}/({tp_cell}+{fp_cell})")

    def _create_recommendations_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create model selection recommendations."""
        builder.column("Criterion", width="200pt", style="text")
        builder.column("Recommended Model", width="200pt", style="text")
        builder.column("Reason", width="350pt", style="text")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Model Selection Recommendations")
        builder.cell("")
        builder.cell("")

        # Recommendations
        recommendations = [
            (
                "Best Accuracy",
                "=INDEX('Model Comparison'.A2:A100,MATCH(MAX('Model Comparison'.B2:B100),'Model Comparison'.B2:B100,0))",
                "Highest accuracy score",
            ),
            (
                "Fastest Inference",
                "=INDEX('Model Comparison'.A2:A100,MATCH(MIN('Model Comparison'.G2:G100),'Model Comparison'.G2:G100,0))",
                "Lowest inference time for real-time applications",
            ),
            (
                "Smallest Size",
                "=INDEX('Model Comparison'.A2:A100,MATCH(MIN('Model Comparison'.H2:H100),'Model Comparison'.H2:H100,0))",
                "Best for deployment with size constraints",
            ),
            (
                "Best F1 Score",
                "=INDEX('Model Comparison'.A2:A100,MATCH(MAX('Model Comparison'.E2:E100),'Model Comparison'.E2:E100,0))",
                "Best balance of precision and recall",
            ),
        ]

        for criterion, formula, reason in recommendations:
            builder.row()
            builder.cell(criterion)
            builder.cell(formula)
            builder.cell(reason)


__all__ = ["ModelComparisonTemplate"]
