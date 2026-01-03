"""
Data Science Domain Plugin for SpreadsheetDL.

Implements:
    TASK-C001: Complete Data Science domain plugin
    PHASE-C: Domain plugin implementations

Provides comprehensive data science-specific functionality including:
- ML experiment tracking templates
- Dataset catalog and inventory management
- Statistical analysis reports
- A/B test results with significance testing
- Model comparison and evaluation
- Statistical test formulas (T-test, F-test, Chi-square)
- ML metrics formulas (accuracy, precision, recall, F1)
- Scientific CSV import with type detection
- MLflow experiment import
- Jupyter notebook metadata extraction

Example:
    >>> from spreadsheet_dl.domains.data_science import DataScienceDomainPlugin
    >>> plugin = DataScienceDomainPlugin()
    >>> plugin.initialize()
    >>> # Use templates
    >>> from spreadsheet_dl.domains.data_science import ExperimentLogTemplate
    >>> template = ExperimentLogTemplate(project_name="Image Classification")
    >>> builder = template.generate()
    >>> builder.save("experiments.ods")
"""

# Plugin
# Formulas - Data Functions
from spreadsheet_dl.domains.data_science.formulas.data_functions import (
    AverageFormula,
    CorrelationFormula,
    MedianFormula,
    StdevFormula,
    VarianceFormula,
)

# Formulas - ML Metrics
from spreadsheet_dl.domains.data_science.formulas.ml_metrics import (
    AccuracyFormula,
    ConfusionMatrixMetricFormula,
    F1ScoreFormula,
    PrecisionFormula,
    RecallFormula,
)

# Formulas - Statistical
from spreadsheet_dl.domains.data_science.formulas.statistical import (
    ChiSquareTestFormula,
    FTestFormula,
    TTestFormula,
    ZTestFormula,
)

# Importers
from spreadsheet_dl.domains.data_science.importers import (
    JupyterMetadataImporter,
    MLflowImporter,
    ScientificCSVImporter,
)
from spreadsheet_dl.domains.data_science.plugin import DataScienceDomainPlugin

# Templates
from spreadsheet_dl.domains.data_science.templates import (
    ABTestResultsTemplate,
    AnalysisReportTemplate,
    DatasetCatalogTemplate,
    ExperimentLogTemplate,
    ModelComparisonTemplate,
)

# Utils
from spreadsheet_dl.domains.data_science.utils import (
    calculate_confusion_matrix_metrics,
    format_scientific_notation,
    infer_data_type,
    parse_scientific_notation,
)

__all__ = [
    # Plugin
    "DataScienceDomainPlugin",
    # Templates
    "ABTestResultsTemplate",
    "AnalysisReportTemplate",
    "DatasetCatalogTemplate",
    "ExperimentLogTemplate",
    "ModelComparisonTemplate",
    # Formulas - Statistical
    "ChiSquareTestFormula",
    "FTestFormula",
    "TTestFormula",
    "ZTestFormula",
    # Formulas - ML Metrics
    "AccuracyFormula",
    "ConfusionMatrixMetricFormula",
    "F1ScoreFormula",
    "PrecisionFormula",
    "RecallFormula",
    # Formulas - Data Functions
    "AverageFormula",
    "CorrelationFormula",
    "MedianFormula",
    "StdevFormula",
    "VarianceFormula",
    # Importers
    "JupyterMetadataImporter",
    "MLflowImporter",
    "ScientificCSVImporter",
    # Utils
    "calculate_confusion_matrix_metrics",
    "format_scientific_notation",
    "infer_data_type",
    "parse_scientific_notation",
]
