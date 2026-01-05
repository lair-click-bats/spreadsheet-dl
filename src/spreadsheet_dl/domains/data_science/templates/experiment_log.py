"""Experiment Log Template for ML experiment tracking.

Implements:
    ExperimentLogTemplate for data science domain
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class ExperimentLogTemplate(BaseTemplate):
    """ML experiment tracking template.

    Implements:
        ExperimentLogTemplate with auto-numbered IDs and metric trends

    Features:
    - Auto-numbered experiment IDs
    - Parameter tracking (JSON/dict format)
    - Hyperparameter columns
    - Multiple metrics (accuracy, loss, etc.)
    - Duration tracking
    - Status field (running, completed, failed)
    - Notes column
    - Chart showing metric trends over experiments

    Example:
        >>> template = ExperimentLogTemplate()
        >>> builder = template.generate()
        >>> builder is not None
        True
    """

    project_name: str = "ML Project"
    metrics: list[str] = field(default_factory=lambda: ["accuracy", "loss"])
    include_hyperparams: bool = True
    include_reproducibility: bool = True  # Random seed, version tracking
    include_chart: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata.

        Returns:
            TemplateMetadata for experiment log template

        Implements:
            Template metadata
        """
        return TemplateMetadata(
            name="Experiment Log",
            description="ML experiment tracking with metrics and hyperparameters",
            category="data_science",
            tags=("ml", "experiments", "tracking", "metrics"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """Generate the experiment log spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            ExperimentLogTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Experiment Log - {self.project_name}",
            author="Data Science Team",
            subject="ML Experiments",
            description=f"Machine learning experiment log for {self.project_name}",
            keywords=["ml", "experiments", "tracking", self.project_name],
        )

        # Create experiments sheet
        builder.sheet("Experiments")

        # Define columns
        builder.column("Exp ID", width="80pt", style="text")
        builder.column("Date", width="100pt", type="date")
        builder.column("Parameters", width="200pt", style="text")

        if self.include_hyperparams:
            builder.column("Learning Rate", width="100pt", type="number")
            builder.column("Batch Size", width="80pt", type="number")
            builder.column("Epochs", width="80pt", type="number")

        # Reproducibility columns
        if self.include_reproducibility:
            builder.column("Random Seed", width="90pt", type="number")
            builder.column("Dataset Ver", width="90pt", style="text")
            builder.column("Code Ver", width="90pt", style="text")

        # Add metric columns
        for metric in self.metrics:
            builder.column(
                metric.replace("_", " ").title(), width="100pt", type="number"
            )

        builder.column("Duration (s)", width="100pt", type="number")
        builder.column("Status", width="100pt", style="text")
        builder.column("Notes", width="250pt", style="text")

        # Freeze header row
        builder.freeze(rows=1)

        # Header row
        builder.row(style="header_primary")
        builder.cell("Exp ID")
        builder.cell("Date")
        builder.cell("Parameters")

        if self.include_hyperparams:
            builder.cell("Learning Rate")
            builder.cell("Batch Size")
            builder.cell("Epochs")

        if self.include_reproducibility:
            builder.cell("Random Seed")
            builder.cell("Dataset Ver")
            builder.cell("Code Ver")

        for metric in self.metrics:
            builder.cell(metric.replace("_", " ").title())

        builder.cell("Duration (s)")
        builder.cell("Status")
        builder.cell("Notes")

        # Add sample data rows
        self._add_sample_data(builder)

        # Add summary statistics
        builder.sheet("Summary")
        self._create_summary_sheet(builder)

        return builder

    def _add_sample_data(self, builder: SpreadsheetBuilder) -> None:
        """Add sample experiment data."""
        sample_experiments = [
            {
                "id": "EXP-001",
                "date": "2024-01-15",
                "params": '{"model": "ResNet50", "optimizer": "Adam"}',
                "lr": 0.001,
                "batch": 32,
                "epochs": 50,
                "seed": 42,
                "dataset_ver": "v1.0.0",
                "code_ver": "abc123",
                "metrics": [0.92, 0.15],
                "duration": 3600,
                "status": "completed",
                "notes": "Baseline model",
            },
            {
                "id": "EXP-002",
                "date": "2024-01-16",
                "params": '{"model": "ResNet50", "optimizer": "SGD"}',
                "lr": 0.01,
                "batch": 64,
                "epochs": 50,
                "seed": 42,
                "dataset_ver": "v1.0.0",
                "code_ver": "def456",
                "metrics": [0.89, 0.22],
                "duration": 1800,
                "status": "completed",
                "notes": "SGD optimizer test",
            },
            {
                "id": "EXP-003",
                "date": "2024-01-17",
                "params": '{"model": "VGG16", "optimizer": "Adam"}',
                "lr": 0.0005,
                "batch": 32,
                "epochs": 50,
                "seed": 123,
                "dataset_ver": "v1.1.0",
                "code_ver": "ghi789",
                "metrics": [0.94, 0.12],
                "duration": 4500,
                "status": "completed",
                "notes": "VGG architecture",
            },
        ]

        for exp in sample_experiments:
            builder.row()
            builder.cell(exp["id"])
            builder.cell(exp["date"])
            builder.cell(exp["params"])

            if self.include_hyperparams:
                builder.cell(exp["lr"])
                builder.cell(exp["batch"])
                builder.cell(exp["epochs"])

            if self.include_reproducibility:
                builder.cell(exp.get("seed", ""))
                builder.cell(exp.get("dataset_ver", ""))
                builder.cell(exp.get("code_ver", ""))

            metrics = exp["metrics"]
            if isinstance(metrics, list):
                for metric_value in metrics[: len(self.metrics)]:
                    builder.cell(metric_value)

            builder.cell(exp["duration"])
            builder.cell(exp["status"])
            builder.cell(exp["notes"])

    def _create_summary_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create summary statistics sheet."""
        builder.column("Metric", width="150pt", style="text")
        builder.column("Best Value", width="120pt", type="number")
        builder.column("Average", width="120pt", type="number")
        builder.column("Worst Value", width="120pt", type="number")

        builder.freeze(rows=1)

        builder.row(style="header_primary")
        builder.cell("Metric")
        builder.cell("Best Value")
        builder.cell("Average")
        builder.cell("Worst Value")

        # Add rows for each metric with formulas
        for idx, metric in enumerate(self.metrics):
            # Calculate column offset: D (base) + hyperparams (3) + reproducibility (3)
            offset = 0
            if self.include_hyperparams:
                offset += 3
            if self.include_reproducibility:
                offset += 3
            col_letter = chr(ord("D") + offset + idx)  # Column position
            builder.row()
            builder.cell(metric.replace("_", " ").title())
            builder.cell(f"=MAX(Experiments.{col_letter}:Experiments.{col_letter})")
            builder.cell(f"=AVERAGE(Experiments.{col_letter}:Experiments.{col_letter})")
            builder.cell(f"=MIN(Experiments.{col_letter}:Experiments.{col_letter})")


__all__ = ["ExperimentLogTemplate"]
