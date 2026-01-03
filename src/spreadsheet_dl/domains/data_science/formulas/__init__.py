"""
Data Science Formulas for SpreadsheetDL.

Implements:
    TASK-C001: Data Science domain formulas

Provides statistical and ML formula extensions:
- Statistical formulas: TTEST, FTEST, ZTEST, CHISQ_TEST
- ML metrics: ACCURACY, PRECISION, RECALL, F1SCORE, CONFUSION_MATRIX_METRIC
- Data functions: DS_AVERAGE, DS_MEDIAN, DS_STDEV, DS_VARIANCE, DS_CORRELATION
"""

# Statistical formulas
# Data function formulas
from spreadsheet_dl.domains.data_science.formulas.data_functions import (
    AverageFormula,
    CorrelationFormula,
    MedianFormula,
    StdevFormula,
    VarianceFormula,
)

# ML metrics formulas
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

__all__ = [
    # Statistical
    "ChiSquareTestFormula",
    "FTestFormula",
    "TTestFormula",
    "ZTestFormula",
    # ML Metrics
    "AccuracyFormula",
    "ConfusionMatrixMetricFormula",
    "F1ScoreFormula",
    "PrecisionFormula",
    "RecallFormula",
    # Data Functions
    "AverageFormula",
    "CorrelationFormula",
    "MedianFormula",
    "StdevFormula",
    "VarianceFormula",
]
