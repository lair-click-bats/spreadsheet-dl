"""Data Science Domain Plugin for SpreadsheetDL.

Implements:
    Data Science domain plugin
    PHASE-C: Domain plugin implementations

Provides data science-specific functionality including:
- Experiment tracking and model comparison templates
- Dataset cataloging and analysis templates
- Statistical testing formulas (T-test, F-test, Chi-square)
- ML metrics formulas (accuracy, precision, recall, F1)
- Scientific CSV and MLflow importers
- Jupyter notebook metadata extraction

Features:
    - 5 professional templates for data science workflows
    - Statistical and ML formula extensions
    - Import from scientific data formats
    - Integration with ML experiment tracking tools
"""

from __future__ import annotations

from spreadsheet_dl.domains.base import BaseDomainPlugin, PluginMetadata

# Import formulas
from spreadsheet_dl.domains.data_science.formulas.data_functions import (
    AverageFormula,
    CorrelationFormula,
    MedianFormula,
    StdevFormula,
    VarianceFormula,
)
from spreadsheet_dl.domains.data_science.formulas.ml_metrics import (
    AccuracyFormula,
    ConfusionMatrixMetricFormula,
    F1ScoreFormula,
    PrecisionFormula,
    RecallFormula,
)
from spreadsheet_dl.domains.data_science.formulas.statistical import (
    ChiSquareTestFormula,
    FTestFormula,
    TTestFormula,
    ZTestFormula,
)

# Import importers
from spreadsheet_dl.domains.data_science.importers.jupyter import (
    JupyterMetadataImporter,
)
from spreadsheet_dl.domains.data_science.importers.mlflow import MLflowImporter
from spreadsheet_dl.domains.data_science.importers.scientific_csv import (
    ScientificCSVImporter,
)

# Import templates
from spreadsheet_dl.domains.data_science.templates.ab_test_results import (
    ABTestResultsTemplate,
)
from spreadsheet_dl.domains.data_science.templates.analysis_report import (
    AnalysisReportTemplate,
)
from spreadsheet_dl.domains.data_science.templates.dataset_catalog import (
    DatasetCatalogTemplate,
)
from spreadsheet_dl.domains.data_science.templates.experiment_log import (
    ExperimentLogTemplate,
)
from spreadsheet_dl.domains.data_science.templates.model_comparison import (
    ModelComparisonTemplate,
)


class DataScienceDomainPlugin(BaseDomainPlugin):
    """Data Science domain plugin.

    Implements:
        Complete Data Science domain plugin
        PHASE-C: Domain plugin implementations

    Provides comprehensive data science functionality for SpreadsheetDL
    with templates, formulas, and importers tailored for ML/DS workflows.

    Example:
        >>> plugin = DataScienceDomainPlugin()
        >>> plugin.initialize()
        >>> template_class = plugin.get_template("experiment_log")
        >>> template = template_class()
        >>> builder = template.generate()
        >>> path = builder.save("experiments.ods")
    """

    @property
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata.

        Returns:
            PluginMetadata with data science plugin information

        Implements:
            Plugin metadata requirements
        """
        return PluginMetadata(
            name="data_science",
            version="4.0.0",
            description="Data science templates, formulas, and importers for ML/DS workflows",
            author="SpreadsheetDL Team",
            license="MIT",
            homepage="https://github.com/lair-click-bats/spreadsheet-dl",
            tags=("data-science", "machine-learning", "statistics", "analytics"),
            min_spreadsheet_dl_version="4.0.0",
        )

    def initialize(self) -> None:
        """Initialize plugin resources.

        Registers all templates, formulas, and importers.

        Implements:
            Plugin initialization with all components

        Raises:
            Exception: If initialization fails
        """
        # Register templates (5 total)
        self.register_template("experiment_log", ExperimentLogTemplate)
        self.register_template("dataset_catalog", DatasetCatalogTemplate)
        self.register_template("analysis_report", AnalysisReportTemplate)
        self.register_template("ab_test_results", ABTestResultsTemplate)
        self.register_template("model_comparison", ModelComparisonTemplate)

        # Register statistical formulas
        self.register_formula("TTEST", TTestFormula)
        self.register_formula("FTEST", FTestFormula)
        self.register_formula("ZTEST", ZTestFormula)
        self.register_formula("CHISQ_TEST", ChiSquareTestFormula)

        # Register ML metrics formulas
        self.register_formula("ACCURACY", AccuracyFormula)
        self.register_formula("PRECISION", PrecisionFormula)
        self.register_formula("RECALL", RecallFormula)
        self.register_formula("F1SCORE", F1ScoreFormula)
        self.register_formula("CONFUSION_MATRIX_METRIC", ConfusionMatrixMetricFormula)

        # Register data function formulas
        self.register_formula("DS_AVERAGE", AverageFormula)
        self.register_formula("DS_MEDIAN", MedianFormula)
        self.register_formula("DS_STDEV", StdevFormula)
        self.register_formula("DS_VARIANCE", VarianceFormula)
        self.register_formula("DS_CORRELATION", CorrelationFormula)

        # Register importers (3 total)
        self.register_importer("scientific_csv", ScientificCSVImporter)
        self.register_importer("mlflow", MLflowImporter)
        self.register_importer("jupyter", JupyterMetadataImporter)

    def cleanup(self) -> None:
        """Cleanup plugin resources.

        No resources need explicit cleanup for this plugin.

        Implements:
            Plugin cleanup method
        """
        # No cleanup needed for this plugin
        pass

    def validate(self) -> bool:
        """Validate plugin configuration.

        Returns:
            True if plugin has required templates and formulas registered

        Implements:
            Plugin validation
        """
        # Verify we have all required components
        required_templates = 5
        required_formulas = 14  # 4 statistical + 5 ML + 5 data functions
        required_importers = 3

        return (
            len(self._templates) >= required_templates
            and len(self._formulas) >= required_formulas
            and len(self._importers) >= required_importers
        )


__all__ = [
    "DataScienceDomainPlugin",
]
