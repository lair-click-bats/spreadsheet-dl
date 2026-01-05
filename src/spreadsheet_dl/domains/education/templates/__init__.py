"""
Education domain templates.

Implements:
    Education domain templates

Provides 5 specialized templates:
- CourseGradebookTemplate: Course grades and student tracking
- LessonPlanTemplate: Lesson planning and curriculum design
- AssessmentRubricTemplate: Assessment criteria and scoring
- StudentAttendanceTemplate: Attendance tracking
- LearningObjectivesTemplate: Learning objectives mapping
"""

from spreadsheet_dl.domains.education.templates.assessment_rubric import (
    AssessmentRubricTemplate,
)
from spreadsheet_dl.domains.education.templates.course_gradebook import (
    CourseGradebookTemplate,
)
from spreadsheet_dl.domains.education.templates.learning_objectives import (
    LearningObjectivesTemplate,
)
from spreadsheet_dl.domains.education.templates.lesson_plan import LessonPlanTemplate
from spreadsheet_dl.domains.education.templates.student_attendance import (
    StudentAttendanceTemplate,
)

__all__ = [
    "AssessmentRubricTemplate",
    "CourseGradebookTemplate",
    "LearningObjectivesTemplate",
    "LessonPlanTemplate",
    "StudentAttendanceTemplate",
]
