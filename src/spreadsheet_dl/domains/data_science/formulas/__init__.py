"""Data Science Formulas for SpreadsheetDL.

Implements:
    Data Science domain formulas

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

# Regression metrics formulas
from spreadsheet_dl.domains.data_science.formulas.regression import (
    MeanAbsoluteError,
    MeanAbsolutePercentageError,
    MeanSquaredError,
    RootMeanSquaredError,
    RSquared,
)
from spreadsheet_dl.domains.data_science.formulas.statistical import (
    ChiSquareTestFormula,
    FTestFormula,
    TTestFormula,
    ZTestFormula,
)

__all__ = [
    # ML Metrics
    "AccuracyFormula",
    # Data Functions
    "AverageFormula",
    # Statistical
    "ChiSquareTestFormula",
    "ConfusionMatrixMetricFormula",
    "CorrelationFormula",
    "F1ScoreFormula",
    "FTestFormula",
    # Regression Metrics
    "MeanAbsoluteError",
    "MeanAbsolutePercentageError",
    "MeanSquaredError",
    "MedianFormula",
    "PrecisionFormula",
    "RSquared",
    "RecallFormula",
    "RootMeanSquaredError",
    "StdevFormula",
    "TTestFormula",
    "VarianceFormula",
    "ZTestFormula",
]
