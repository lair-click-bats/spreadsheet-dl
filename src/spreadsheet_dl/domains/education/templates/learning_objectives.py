"""
Learning Objectives Template.

Implements:
    TASK-C007: LearningObjectivesTemplate for education domain
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class LearningObjectivesTemplate(BaseTemplate):
    """
    Learning objectives mapping template.

    Implements:
        TASK-C007: LearningObjectivesTemplate with curriculum mapping

    Features:
    - Learning objective statements
    - Bloom's taxonomy level classification
    - Standards alignment tracking
    - Assessment mapping
    - Progress tracking per objective

    Example:
        >>> template = LearningObjectivesTemplate(
        ...     course_name="Introduction to Programming",
        ...     num_objectives=15,
        ... )
        >>> builder = template.generate()
        >>> builder.save("learning_objectives.ods")
    """

    course_name: str = "Learning Objectives"
    subject: str = ""
    grade_level: str = ""
    num_objectives: int = 15
    standards_framework: str = "Common Core"
    objectives: list[str] = field(default_factory=list)
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for learning objectives template

        Implements:
            TASK-C007: Template metadata
        """
        return TemplateMetadata(
            name="Learning Objectives",
            description="Learning objectives mapping with standards alignment",
            category="education",
            tags=("objectives", "curriculum", "standards", "alignment"),
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
        return self.num_objectives > 0

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the learning objectives spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C007: LearningObjectivesTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Learning Objectives - {self.course_name}",
            author="Curriculum Designer",
            subject="Learning Objectives",
            description=f"Learning objectives for {self.course_name}",
            keywords=["objectives", "curriculum", "standards", self.course_name],
        )

        # Create objectives sheet
        builder.sheet("Objectives")

        # Define columns
        builder.column("ID", width="50pt", style="text")
        builder.column("Learning Objective", width="350pt", style="text")
        builder.column("Bloom's Level", width="80pt", style="text")
        builder.column("Standard", width="100pt", style="text")
        builder.column("Unit/Lesson", width="100pt", style="text")
        builder.column("Assessment", width="150pt", style="text")
        builder.column("Status", width="80pt", style="text")

        builder.freeze(rows=2)

        # Header row
        builder.row(style="header_primary")
        builder.cell(f"LEARNING OBJECTIVES: {self.course_name}", colspan=7)

        # Course info row
        builder.row()
        builder.cell("Subject:", style="label")
        builder.cell(self.subject or "[Subject]")
        builder.cell("Grade:", style="label")
        builder.cell(self.grade_level or "[Grade]")
        builder.cell("Framework:", style="label")
        builder.cell(self.standards_framework, colspan=2)

        builder.row()  # Blank row

        # Column headers
        builder.row(style="header_secondary")
        builder.cell("ID")
        builder.cell("Learning Objective")
        builder.cell("Bloom's")
        builder.cell("Standard")
        builder.cell("Unit/Lesson")
        builder.cell("Assessment")
        builder.cell("Status")

        # Bloom's taxonomy reference

        # Default objectives
        default_objectives = self.objectives or [
            "Students will be able to define key vocabulary terms",
            "Students will be able to explain core concepts",
            "Students will be able to apply principles to new situations",
            "Students will be able to analyze relationships between concepts",
            "Students will be able to evaluate solutions critically",
        ]

        # Objective rows
        for i in range(self.num_objectives):
            builder.row()
            builder.cell(f"LO-{i + 1:02d}")

            # Objective text
            if i < len(default_objectives):
                builder.cell(default_objectives[i])
            else:
                builder.cell("Students will be able to...")

            # Bloom's level (dropdown in real spreadsheet)
            builder.cell("")

            # Standard alignment
            builder.cell("")

            # Unit/Lesson mapping
            builder.cell("")

            # Assessment method
            builder.cell("")

            # Status (Not Started, In Progress, Covered, Assessed)
            builder.cell("")

        builder.row()  # Blank row

        # Summary section
        builder.row(style="header_secondary")
        builder.cell("SUMMARY", colspan=7)

        builder.row()
        builder.cell("Total Objectives:", style="label")
        builder.cell(f"={self.num_objectives}")
        builder.cell("Covered:", style="label")
        builder.cell(
            f'=COUNTIF(G5:G{4 + self.num_objectives};"Covered")+COUNTIF(G5:G{4 + self.num_objectives};"Assessed")'
        )
        builder.cell("Remaining:", style="label")
        builder.cell(f"=B{5 + self.num_objectives + 1}-D{5 + self.num_objectives + 1}")
        builder.cell("")

        builder.row()  # Blank row

        # Bloom's reference sheet
        builder.sheet("Bloom's Taxonomy Reference")

        builder.column("Level", width="50pt")
        builder.column("Category", width="100pt", style="text")
        builder.column("Description", width="300pt", style="text")
        builder.column("Action Verbs", width="300pt", style="text")

        builder.row(style="header_primary")
        builder.cell("BLOOM'S TAXONOMY REFERENCE", colspan=4)

        builder.row(style="header_secondary")
        builder.cell("Level")
        builder.cell("Category")
        builder.cell("Description")
        builder.cell("Action Verbs")

        bloom_data = [
            (
                6,
                "Create",
                "Produce new or original work",
                "Design, assemble, construct, develop, formulate, author",
            ),
            (
                5,
                "Evaluate",
                "Justify a decision or course of action",
                "Appraise, argue, defend, judge, select, support, critique",
            ),
            (
                4,
                "Analyze",
                "Draw connections among ideas",
                "Differentiate, organize, relate, compare, contrast, examine",
            ),
            (
                3,
                "Apply",
                "Use information in new situations",
                "Execute, implement, solve, use, demonstrate, operate",
            ),
            (
                2,
                "Understand",
                "Explain ideas or concepts",
                "Classify, describe, discuss, explain, identify, summarize",
            ),
            (
                1,
                "Remember",
                "Recall facts and basic concepts",
                "Define, duplicate, list, memorize, repeat, state",
            ),
        ]

        for level, category, description, verbs in bloom_data:
            builder.row()
            builder.cell(level)
            builder.cell(category)
            builder.cell(description)
            builder.cell(verbs)

        return builder


__all__ = ["LearningObjectivesTemplate"]
