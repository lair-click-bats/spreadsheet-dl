"""
Data Science Templates for SpreadsheetDL.

Implements:
    TASK-C001: Data Science domain templates

Provides professional templates for common data science workflows:
- ExperimentLogTemplate: ML experiment tracking
- DatasetCatalogTemplate: Dataset inventory and statistics
- AnalysisReportTemplate: Statistical analysis reports
- ABTestResultsTemplate: A/B test analysis with significance testing
- ModelComparisonTemplate: ML model comparison and evaluation
"""

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

__all__ = [
    "ABTestResultsTemplate",
    "AnalysisReportTemplate",
    "DatasetCatalogTemplate",
    "ExperimentLogTemplate",
    "ModelComparisonTemplate",
]
