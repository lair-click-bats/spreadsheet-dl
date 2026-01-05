"""Course Gradebook Template.

Implements:
    CourseGradebookTemplate for education domain
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class CourseGradebookTemplate(BaseTemplate):
    """Course gradebook template for grade tracking.

    Implements:
        CourseGradebookTemplate with grade calculations

    Features:
    - Student roster with IDs
    - Multiple assignment columns
    - Weighted grade calculations
    - Letter grade conversion
    - Class statistics (average, median, std dev)
    - Grade distribution chart data

    Example:
        >>> template = CourseGradebookTemplate(  # doctest: +SKIP
        ...     course_name="Introduction to Python",
        ...     num_students=30,
        ...     num_assignments=10,
        ... )
        >>> builder = template.generate()  # doctest: +SKIP
        >>> path = builder.save("gradebook.ods")  # doctest: +SKIP
    """

    course_name: str = "Course Gradebook"
    instructor: str = ""
    semester: str = ""
    num_students: int = 30
    num_assignments: int = 10
    include_midterm: bool = True
    include_final: bool = True
    theme: str = "default"
    weights: dict[str, float] = field(
        default_factory=lambda: {
            "assignments": 0.40,
            "midterm": 0.25,
            "final": 0.35,
        }
    )

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata.

        Returns:
            TemplateMetadata for course gradebook template

        Implements:
            Template metadata
        """
        return TemplateMetadata(
            name="Course Gradebook",
            description="Course grades and student tracking with weighted calculations",
            category="education",
            tags=("gradebook", "grades", "students", "course"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """Validate template parameters.

        Returns:
            True if parameters are valid

        Implements:
            Template validation
        """
        return (
            self.num_students > 0
            and self.num_assignments > 0
            and sum(self.weights.values()) <= 1.01  # Allow small floating point error
        )

    def generate(self) -> SpreadsheetBuilder:
        """Generate the course gradebook spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            CourseGradebookTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Gradebook - {self.course_name}",
            author=self.instructor or "Instructor",
            subject="Course Gradebook",
            description=f"Grade tracking for {self.course_name}",
            keywords=["gradebook", "grades", "course", self.course_name],
        )

        # Create grades sheet
        builder.sheet("Grades")

        # Define columns
        builder.column("Student ID", width="80pt", style="text")
        builder.column("Last Name", width="100pt", style="text")
        builder.column("First Name", width="100pt", style="text")

        # Assignment columns
        for i in range(1, self.num_assignments + 1):
            builder.column(f"HW{i}", width="50pt")

        if self.include_midterm:
            builder.column("Midterm", width="60pt")
        if self.include_final:
            builder.column("Final", width="60pt")

        builder.column("Average", width="60pt")
        builder.column("Weighted", width="60pt")
        builder.column("Letter", width="50pt", style="text")

        builder.freeze(rows=2, cols=3)

        # Header row 1 - Course info
        builder.row(style="header_primary")
        builder.cell(f"GRADEBOOK: {self.course_name}", colspan=self.num_assignments + 7)

        # Header row 2 - Column headers
        builder.row(style="header_secondary")
        builder.cell("ID")
        builder.cell("Last Name")
        builder.cell("First Name")

        for i in range(1, self.num_assignments + 1):
            builder.cell(f"HW{i}")

        if self.include_midterm:
            builder.cell("Mid")
        if self.include_final:
            builder.cell("Final")

        builder.cell("Avg")
        builder.cell("Wtd")
        builder.cell("Grade")

        # Student rows
        hw_start_col = 4  # D column (1-indexed in formula)
        hw_start_col + self.num_assignments - 1

        for row_num in range(3, 3 + self.num_students):
            builder.row()
            builder.cell(f"STU{row_num - 2:03d}")
            builder.cell("")  # Last name
            builder.cell("")  # First name

            # Assignment placeholders
            for _ in range(self.num_assignments):
                builder.cell("")

            if self.include_midterm:
                builder.cell("")
            if self.include_final:
                builder.cell("")

            # Average formula (assignments only)
            hw_range = f"D{row_num}:{chr(ord('D') + self.num_assignments - 1)}{row_num}"
            builder.cell(f"=AVERAGE({hw_range})")

            # Weighted grade formula
            weighted_parts = []
            if self.weights.get("assignments", 0) > 0:
                weighted_parts.append(
                    f"AVERAGE({hw_range})*{self.weights['assignments']}"
                )
            if self.include_midterm and self.weights.get("midterm", 0) > 0:
                mid_col = chr(ord("D") + self.num_assignments)
                weighted_parts.append(f"{mid_col}{row_num}*{self.weights['midterm']}")
            if self.include_final and self.weights.get("final", 0) > 0:
                offset = self.num_assignments + (1 if self.include_midterm else 0)
                final_col = chr(ord("D") + offset)
                weighted_parts.append(f"{final_col}{row_num}*{self.weights['final']}")

            weighted_formula = "+".join(weighted_parts) if weighted_parts else "0"
            builder.cell(f"={weighted_formula}")

            # Letter grade formula
            wtd_col = chr(
                ord("D")
                + self.num_assignments
                + (1 if self.include_midterm else 0)
                + (1 if self.include_final else 0)
                + 1
            )
            builder.cell(
                f'=IF({wtd_col}{row_num}>=90;"A";IF({wtd_col}{row_num}>=80;"B";IF({wtd_col}{row_num}>=70;"C";IF({wtd_col}{row_num}>=60;"D";"F"))))'
            )

        # Statistics section
        builder.row()  # Blank row

        builder.row(style="header_secondary")
        builder.cell("STATISTICS", colspan=3)

        # Class average
        builder.row()
        builder.cell("Class Average", colspan=3, style="label")
        for i in range(self.num_assignments):
            col = chr(ord("D") + i)
            builder.cell(f"=AVERAGE({col}3:{col}{2 + self.num_students})")

        # Standard deviation
        builder.row()
        builder.cell("Std Deviation", colspan=3, style="label")
        for i in range(self.num_assignments):
            col = chr(ord("D") + i)
            builder.cell(f"=STDEV({col}3:{col}{2 + self.num_students})")

        return builder


__all__ = ["CourseGradebookTemplate"]
