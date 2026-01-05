"""
Education domain formulas.

Implements:
    Education domain formula extensions

Provides 12 specialized formulas for education:
- Grade calculations (average, weighted, curve)
- Statistics (standard deviation, percentile, correlation)
- Learning metrics (mastery, gain, attendance, completion, etc.)
"""

from spreadsheet_dl.domains.education.formulas.grades import (
    GradeAverageFormula,
    GradeCurveFormula,
    WeightedGradeFormula,
)
from spreadsheet_dl.domains.education.formulas.learning import (
    AttendanceRateFormula,
    BloomTaxonomyLevelFormula,
    CompletionRateFormula,
    LearningGainFormula,
    MasteryLevelFormula,
    ReadabilityScoreFormula,
)
from spreadsheet_dl.domains.education.formulas.statistics import (
    CorrelationFormula,
    PercentileRankFormula,
    StandardDeviationFormula,
)

__all__ = [
    # Learning
    "AttendanceRateFormula",
    "BloomTaxonomyLevelFormula",
    "CompletionRateFormula",
    # Statistics
    "CorrelationFormula",
    # Grades
    "GradeAverageFormula",
    "GradeCurveFormula",
    "LearningGainFormula",
    "MasteryLevelFormula",
    "PercentileRankFormula",
    "ReadabilityScoreFormula",
    "StandardDeviationFormula",
    "WeightedGradeFormula",
]
