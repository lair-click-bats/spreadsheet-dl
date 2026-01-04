"""
Assessment Rubric Template.

Implements:
    TASK-C007: AssessmentRubricTemplate for education domain
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class AssessmentRubricTemplate(BaseTemplate):
    """
    Assessment rubric template for scoring criteria.

    Implements:
        TASK-C007: AssessmentRubricTemplate with scoring levels

    Features:
    - Multiple criteria rows
    - Customizable scoring levels (default 4-point scale)
    - Level descriptions for each criterion
    - Weight/points per criterion
    - Total score calculation

    Example:
        >>> template = AssessmentRubricTemplate(
        ...     assessment_name="Research Paper Rubric",
        ...     num_criteria=5,
        ... )
        >>> builder = template.generate()
        >>> builder.save("rubric.ods")
    """

    assessment_name: str = "Assessment Rubric"
    subject: str = ""
    grade_level: str = ""
    num_criteria: int = 5
    num_levels: int = 4
    max_points: int = 100
    criteria: list[str] = field(default_factory=list)
    level_names: list[str] = field(default_factory=list)
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for assessment rubric template

        Implements:
            TASK-C007: Template metadata
        """
        return TemplateMetadata(
            name="Assessment Rubric",
            description="Scoring rubric with criteria and performance levels",
            category="education",
            tags=("rubric", "assessment", "scoring", "criteria"),
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
        return self.num_criteria > 0 and self.num_levels >= 2 and self.max_points > 0

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the assessment rubric spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C007: AssessmentRubricTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Rubric - {self.assessment_name}",
            author="Instructor",
            subject="Assessment Rubric",
            description=f"Scoring rubric for {self.assessment_name}",
            keywords=["rubric", "assessment", "grading", self.assessment_name],
        )

        # Create rubric sheet
        builder.sheet("Rubric")

        # Define columns
        builder.column("Criteria", width="150pt", style="text")
        builder.column("Weight", width="60pt")

        # Level columns
        level_names = self.level_names or [
            "Excellent (4)",
            "Good (3)",
            "Satisfactory (2)",
            "Needs Improvement (1)",
        ]
        for i in range(self.num_levels):
            name = (
                level_names[i]
                if i < len(level_names)
                else f"Level {self.num_levels - i}"
            )
            builder.column(name, width="200pt", style="text")

        builder.column("Score", width="60pt")

        builder.freeze(rows=2)

        # Header
        builder.row(style="header_primary")
        builder.cell(f"RUBRIC: {self.assessment_name}", colspan=self.num_levels + 3)

        # Subheader with assessment info
        builder.row()
        builder.cell("Subject:", style="label")
        builder.cell(self.subject or "[Subject]", colspan=2)
        builder.cell("Grade Level:", style="label")
        builder.cell(self.grade_level or "[Grade]", colspan=self.num_levels - 2)
        builder.cell("")

        builder.row()  # Blank row

        # Column headers
        builder.row(style="header_secondary")
        builder.cell("Criteria")
        builder.cell("Weight")
        for i in range(self.num_levels):
            name = (
                level_names[i]
                if i < len(level_names)
                else f"Level {self.num_levels - i}"
            )
            builder.cell(name)
        builder.cell("Score")

        # Default criteria
        default_criteria = self.criteria or [
            "Content & Organization",
            "Evidence & Support",
            "Analysis & Critical Thinking",
            "Language & Style",
            "Mechanics & Format",
        ]

        # Criteria rows
        points_per_criterion = self.max_points // self.num_criteria

        for i in range(self.num_criteria):
            criterion = (
                default_criteria[i]
                if i < len(default_criteria)
                else f"Criterion {i + 1}"
            )

            builder.row()
            builder.cell(criterion)
            builder.cell(points_per_criterion)

            # Level descriptions (placeholders)
            for level in range(self.num_levels):
                points = self.num_levels - level
                builder.cell(f"[Description for level {points}]")

            # Score cell (empty for teacher to fill)
            builder.cell("")

        # Separator
        builder.row()  # Blank row

        # Total row
        builder.row(style="header_secondary")
        builder.cell("TOTAL", style="label")
        builder.cell(f"={self.max_points}")

        # Empty cells for levels
        for _ in range(self.num_levels):
            builder.cell("")

        # Total score formula
        score_col = chr(ord("B") + self.num_levels + 1)  # Score column
        builder.cell(
            f"=SUM({score_col}5:{score_col}{4 + self.num_criteria})"
        )

        builder.row()  # Blank row

        # Percentage row
        builder.row()
        builder.cell("Percentage:", style="label")
        for _ in range(self.num_levels + 1):
            builder.cell("")
        total_row = 5 + self.num_criteria
        builder.cell(f"={score_col}{total_row}/B{total_row}*100")

        # Letter grade row
        builder.row()
        builder.cell("Letter Grade:", style="label")
        for _ in range(self.num_levels + 1):
            builder.cell("")
        pct_row = total_row + 2
        builder.cell(
            f'=IF({score_col}{pct_row}>=90;"A";IF({score_col}{pct_row}>=80;"B";IF({score_col}{pct_row}>=70;"C";IF({score_col}{pct_row}>=60;"D";"F"))))')

        builder.row()  # Blank row

        # Comments section
        builder.row(style="header_secondary")
        builder.cell("COMMENTS", colspan=self.num_levels + 3)

        builder.row()
        builder.cell("Strengths:", style="label")
        builder.cell("", colspan=self.num_levels + 2)

        builder.row()
        builder.cell("Areas for Improvement:", style="label")
        builder.cell("", colspan=self.num_levels + 2)

        builder.row()
        builder.cell("Next Steps:", style="label")
        builder.cell("", colspan=self.num_levels + 2)

        return builder


__all__ = ["AssessmentRubricTemplate"]
