"""
Education Domain Plugin for SpreadsheetDL.

Implements:
    TASK-C007: Education domain plugin
    PHASE-C: Domain plugin implementations

Provides education-specific functionality including:
- Course gradebook and grade management templates
- Lesson plan and curriculum planning templates
- Assessment rubric templates
- Student attendance tracking
- Learning objectives mapping
- Grade calculation formulas (average, weighted, curve)
- Statistical analysis formulas (standard deviation, percentile)
- Learning metrics (mastery level, learning gain, completion rate)
- LMS data, gradebook export, and assessment results importers

Example:
    >>> from spreadsheet_dl.domains.education import EducationDomainPlugin
    >>> plugin = EducationDomainPlugin()
    >>> plugin.initialize()
    >>> # Use templates
    >>> from spreadsheet_dl.domains.education import CourseGradebookTemplate
    >>> template = CourseGradebookTemplate(course_name="Introduction to Python")
    >>> builder = template.generate()
    >>> builder.save("gradebook.ods")
"""

# Plugin
from spreadsheet_dl.domains.education.plugin import EducationDomainPlugin

# Formulas - Grade Calculations
from spreadsheet_dl.domains.education.formulas.grades import (
    GradeAverageFormula,
    GradeCurveFormula,
    WeightedGradeFormula,
)

# Formulas - Statistics
from spreadsheet_dl.domains.education.formulas.statistics import (
    CorrelationFormula,
    PercentileRankFormula,
    StandardDeviationFormula,
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

# Importers
from spreadsheet_dl.domains.education.importers import (
    AssessmentResultsImporter,
    GradebookExportImporter,
    LMSDataImporter,
)

# Templates
from spreadsheet_dl.domains.education.templates import (
    AssessmentRubricTemplate,
    CourseGradebookTemplate,
    LearningObjectivesTemplate,
    LessonPlanTemplate,
    StudentAttendanceTemplate,
)

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
    # Plugin
    "EducationDomainPlugin",
    # Templates
    "AssessmentRubricTemplate",
    "CourseGradebookTemplate",
    "LearningObjectivesTemplate",
    "LessonPlanTemplate",
    "StudentAttendanceTemplate",
    # Formulas - Grades
    "GradeAverageFormula",
    "GradeCurveFormula",
    "WeightedGradeFormula",
    # Formulas - Statistics
    "CorrelationFormula",
    "PercentileRankFormula",
    "StandardDeviationFormula",
    # Formulas - Learning
    "AttendanceRateFormula",
    "BloomTaxonomyLevelFormula",
    "CompletionRateFormula",
    "LearningGainFormula",
    "MasteryLevelFormula",
    "ReadabilityScoreFormula",
    # Importers
    "AssessmentResultsImporter",
    "GradebookExportImporter",
    "LMSDataImporter",
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
