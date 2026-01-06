"""Education Domain Plugin for SpreadsheetDL.

Implements:
    Education domain plugin
    PHASE-C: Domain plugin implementations

Provides education-specific functionality including:
- Grade calculation formulas (average, weighted, curve)
- Statistical analysis formulas (standard deviation, percentile)
- Learning metrics (mastery level, learning gain, completion rate)
- LMS data, gradebook export, and assessment results importers

Example:
    >>> from spreadsheet_dl.domains.education import EducationDomainPlugin
    >>> plugin = EducationDomainPlugin()
    >>> plugin.initialize()
"""

# Plugin
# Formulas - Grade Calculations
from spreadsheet_dl.domains.education.formulas.grades import (
    GradeAverageFormula,
    GradeCurveFormula,
    WeightedGradeFormula,
)

# Formulas - Learning Metrics
from spreadsheet_dl.domains.education.formulas.learning import (
    AttendanceRateFormula,
    BloomTaxonomyLevelFormula,
    CompletionRateFormula,
    LearningGainFormula,
    MasteryLevelFormula,
    ReadabilityScoreFormula,
)

# Formulas - Statistics
from spreadsheet_dl.domains.education.formulas.statistics import (
    CorrelationFormula,
    PercentileRankFormula,
    StandardDeviationFormula,
)

# Importers
from spreadsheet_dl.domains.education.importers import (
    AssessmentResultsImporter,
    GradebookExportImporter,
    LMSDataImporter,
)
from spreadsheet_dl.domains.education.plugin import EducationDomainPlugin

# Utils
from spreadsheet_dl.domains.education.utils import (
    calculate_attendance_rate,
    calculate_gpa,
    calculate_grade_average,
    calculate_letter_grade,
    calculate_weighted_grade,
    format_percentage,
    grade_to_points,
    points_to_grade,
)

__all__ = [
    # Importers
    "AssessmentResultsImporter",
    # Formulas - Learning
    "AttendanceRateFormula",
    "BloomTaxonomyLevelFormula",
    "CompletionRateFormula",
    # Formulas - Statistics
    "CorrelationFormula",
    # Plugin
    "EducationDomainPlugin",
    # Formulas - Grades
    "GradeAverageFormula",
    "GradeCurveFormula",
    "GradebookExportImporter",
    "LMSDataImporter",
    "LearningGainFormula",
    "MasteryLevelFormula",
    "PercentileRankFormula",
    "ReadabilityScoreFormula",
    "StandardDeviationFormula",
    "WeightedGradeFormula",
    # Utils
    "calculate_attendance_rate",
    "calculate_gpa",
    "calculate_grade_average",
    "calculate_letter_grade",
    "calculate_weighted_grade",
    "format_percentage",
    "grade_to_points",
    "points_to_grade",
]
