"""
Lesson Plan Template.

Implements:
    TASK-C007: LessonPlanTemplate for education domain
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class LessonPlanTemplate(BaseTemplate):
    """
    Lesson plan template for curriculum design.

    Implements:
        TASK-C007: LessonPlanTemplate with structured planning

    Features:
    - Lesson information (title, date, duration)
    - Learning objectives with Bloom's taxonomy
    - Materials and resources list
    - Step-by-step lesson activities
    - Assessment strategies
    - Differentiation notes

    Example:
        >>> template = LessonPlanTemplate(
        ...     lesson_title="Introduction to Variables",
        ...     grade_level="Grade 9",
        ... )
        >>> builder = template.generate()
        >>> builder.save("lesson_plan.ods")
    """

    lesson_title: str = "Lesson Plan"
    subject: str = ""
    grade_level: str = ""
    duration: str = "50 minutes"
    date: str = ""
    teacher: str = ""
    objectives: list[str] = field(default_factory=list)
    materials: list[str] = field(default_factory=list)
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for lesson plan template

        Implements:
            TASK-C007: Template metadata
        """
        return TemplateMetadata(
            name="Lesson Plan",
            description="Structured lesson planning with objectives and activities",
            category="education",
            tags=("lesson", "planning", "curriculum", "teaching"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """
        Validate template parameters.

        Returns:
            True if parameters are valid

        Implements:
            TASK-C007: Template validation
        """
        return len(self.lesson_title) > 0

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the lesson plan spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C007: LessonPlanTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Lesson Plan - {self.lesson_title}",
            author=self.teacher or "Teacher",
            subject="Lesson Plan",
            description=f"Lesson plan for {self.lesson_title}",
            keywords=["lesson", "plan", "curriculum", self.lesson_title],
        )

        # Create lesson plan sheet
        builder.sheet("Lesson Plan")

        # Define columns
        builder.column("Section", width="150pt", style="text")
        builder.column("Content", width="400pt", style="text")
        builder.column("Time", width="80pt", style="text")
        builder.column("Notes", width="200pt", style="text")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("LESSON PLAN", colspan=4)

        # Lesson information
        builder.row()
        builder.cell("Lesson Title:", style="label")
        builder.cell(self.lesson_title or "[Enter Lesson Title]")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Subject:", style="label")
        builder.cell(self.subject or "[Enter Subject]")
        builder.cell("Date:", style="label")
        builder.cell(self.date or "[Enter Date]")

        builder.row()
        builder.cell("Grade Level:", style="label")
        builder.cell(self.grade_level or "[Enter Grade Level]")
        builder.cell("Duration:", style="label")
        builder.cell(self.duration)

        builder.row()
        builder.cell("Teacher:", style="label")
        builder.cell(self.teacher or "[Enter Teacher Name]")
        builder.cell("")
        builder.cell("")

        builder.row()  # Blank row

        # Learning Objectives
        builder.row(style="header_secondary")
        builder.cell("LEARNING OBJECTIVES", colspan=4)

        builder.row(style="header_secondary")
        builder.cell("Objective")
        builder.cell("Description")
        builder.cell("Bloom's Level")
        builder.cell("Assessment")

        default_objectives = self.objectives or [
            "Students will be able to...",
            "Students will understand...",
            "Students will apply...",
        ]

        for i, obj in enumerate(default_objectives, 1):
            builder.row()
            builder.cell(f"Objective {i}")
            builder.cell(obj)
            builder.cell("[1-6]")
            builder.cell("[How assessed]")

        # Add blank rows for more objectives
        for i in range(len(default_objectives) + 1, len(default_objectives) + 4):
            builder.row()
            builder.cell(f"Objective {i}")
            builder.cell("")
            builder.cell("")
            builder.cell("")

        builder.row()  # Blank row

        # Materials & Resources
        builder.row(style="header_secondary")
        builder.cell("MATERIALS & RESOURCES", colspan=4)

        default_materials = self.materials or [
            "Textbook/workbook",
            "Presentation slides",
            "Handouts",
        ]

        for material in default_materials:
            builder.row()
            builder.cell("")
            builder.cell(material, colspan=3)

        for _ in range(3):
            builder.row()
            builder.cell("")
            builder.cell("", colspan=3)

        builder.row()  # Blank row

        # Lesson Activities
        builder.row(style="header_secondary")
        builder.cell("LESSON ACTIVITIES", colspan=4)

        builder.row(style="header_secondary")
        builder.cell("Phase")
        builder.cell("Activity Description")
        builder.cell("Duration")
        builder.cell("Resources/Notes")

        activities = [
            (
                "Opening/Hook",
                "[Engage students, activate prior knowledge]",
                "5 min",
                "",
            ),
            ("Direct Instruction", "[Present new content]", "15 min", ""),
            ("Guided Practice", "[Work through examples together]", "10 min", ""),
            ("Independent Practice", "[Students work independently]", "15 min", ""),
            ("Closure", "[Summarize, check for understanding]", "5 min", ""),
        ]

        for phase, activity, duration, notes in activities:
            builder.row()
            builder.cell(phase)
            builder.cell(activity)
            builder.cell(duration)
            builder.cell(notes)

        builder.row()  # Blank row

        # Assessment
        builder.row(style="header_secondary")
        builder.cell("ASSESSMENT", colspan=4)

        builder.row()
        builder.cell("Formative:", style="label")
        builder.cell("[Describe ongoing assessment strategies]", colspan=3)

        builder.row()
        builder.cell("Summative:", style="label")
        builder.cell("[Describe final assessment]", colspan=3)

        builder.row()  # Blank row

        # Differentiation
        builder.row(style="header_secondary")
        builder.cell("DIFFERENTIATION", colspan=4)

        builder.row()
        builder.cell("For struggling:", style="label")
        builder.cell("[Scaffolding strategies]", colspan=3)

        builder.row()
        builder.cell("For advanced:", style="label")
        builder.cell("[Extension activities]", colspan=3)

        builder.row()
        builder.cell("ELL support:", style="label")
        builder.cell("[Language support strategies]", colspan=3)

        builder.row()  # Blank row

        # Reflection (to be filled after lesson)
        builder.row(style="header_secondary")
        builder.cell("POST-LESSON REFLECTION", colspan=4)

        builder.row()
        builder.cell("What worked:", style="label")
        builder.cell("", colspan=3)

        builder.row()
        builder.cell("What to improve:", style="label")
        builder.cell("", colspan=3)

        builder.row()
        builder.cell("Notes for next time:", style="label")
        builder.cell("", colspan=3)

        return builder


__all__ = ["LessonPlanTemplate"]
