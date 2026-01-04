"""
Student Attendance Template.

Implements:
    TASK-C007: StudentAttendanceTemplate for education domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class StudentAttendanceTemplate(BaseTemplate):
    """
    Student attendance tracking template.

    Implements:
        TASK-C007: StudentAttendanceTemplate with attendance calculations

    Features:
    - Student roster with IDs
    - Daily attendance columns (P/A/T/E codes)
    - Automatic attendance rate calculation
    - Absence tracking and totals
    - Monthly/term summaries

    Example:
        >>> template = StudentAttendanceTemplate(
        ...     class_name="Period 1 - Algebra",
        ...     num_students=30,
        ...     num_days=20,
        ... )
        >>> builder = template.generate()
        >>> builder.save("attendance.ods")
    """

    class_name: str = "Class Attendance"
    teacher: str = ""
    term: str = ""
    num_students: int = 30
    num_days: int = 20
    start_date: str = ""
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for student attendance template

        Implements:
            TASK-C007: Template metadata
        """
        return TemplateMetadata(
            name="Student Attendance",
            description="Daily attendance tracking with automatic rate calculations",
            category="education",
            tags=("attendance", "tracking", "students", "daily"),
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
        return self.num_students > 0 and self.num_days > 0

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the student attendance spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C007: StudentAttendanceTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Attendance - {self.class_name}",
            author=self.teacher or "Teacher",
            subject="Attendance Record",
            description=f"Attendance tracking for {self.class_name}",
            keywords=["attendance", "tracking", self.class_name],
        )

        # Create attendance sheet
        builder.sheet("Attendance")

        # Define columns
        builder.column("ID", width="60pt", style="text")
        builder.column("Student Name", width="150pt", style="text")

        # Day columns
        for i in range(1, self.num_days + 1):
            builder.column(f"D{i}", width="30pt", style="text")

        builder.column("Present", width="50pt")
        builder.column("Absent", width="50pt")
        builder.column("Tardy", width="50pt")
        builder.column("Rate %", width="60pt")

        builder.freeze(rows=3, cols=2)

        # Header row 1
        builder.row(style="header_primary")
        builder.cell(f"ATTENDANCE: {self.class_name}", colspan=self.num_days + 6)

        # Header row 2 - Legend
        builder.row()
        builder.cell("Legend:", style="label")
        builder.cell(
            "P=Present, A=Absent, T=Tardy, E=Excused", colspan=self.num_days + 5
        )

        # Header row 3 - Column headers
        builder.row(style="header_secondary")
        builder.cell("ID")
        builder.cell("Student Name")

        for i in range(1, self.num_days + 1):
            builder.cell(f"{i}")

        builder.cell("Pres")
        builder.cell("Abs")
        builder.cell("Tard")
        builder.cell("Rate")

        # Student rows
        for row_num in range(4, 4 + self.num_students):
            builder.row()
            builder.cell(f"STU{row_num - 3:03d}")
            builder.cell("")  # Student name

            # Day columns (empty for teacher to fill)
            for _ in range(self.num_days):
                builder.cell("")

            # Calculate column letters for formulas
            first_day_col = "C"
            last_day_col = chr(ord("C") + self.num_days - 1)
            day_range = f"{first_day_col}{row_num}:{last_day_col}{row_num}"

            # Present count
            builder.cell(
                f'=COUNTIF({day_range};"P")+COUNTIF({day_range};"p")'
            )

            # Absent count
            builder.cell(
                f'=COUNTIF({day_range};"A")+COUNTIF({day_range};"a")'
            )

            # Tardy count
            builder.cell(
                f'=COUNTIF({day_range};"T")+COUNTIF({day_range};"t")'
            )

            # Attendance rate
            present_col = chr(ord("C") + self.num_days)
            builder.cell(
                f"=IF(COUNTA({day_range})=0;0;{present_col}{row_num}/COUNTA({day_range})*100)")

        # Summary section
        builder.row()  # Blank row

        builder.row(style="header_secondary")
        builder.cell("DAILY TOTALS", colspan=2)

        # Daily present counts
        builder.row()
        builder.cell("Present:", style="label")
        builder.cell("")

        for i in range(self.num_days):
            col = chr(ord("C") + i)
            builder.cell(
                f'=COUNTIF({col}4:{col}{3 + self.num_students};"P")+COUNTIF({col}4:{col}{3 + self.num_students};"p")')

        builder.row()
        builder.cell("Absent:", style="label")
        builder.cell("")

        for i in range(self.num_days):
            col = chr(ord("C") + i)
            builder.cell(
                f'=COUNTIF({col}4:{col}{3 + self.num_students};"A")+COUNTIF({col}4:{col}{3 + self.num_students};"a")')

        builder.row()
        builder.cell("Rate %:", style="label")
        builder.cell("")

        for i in range(self.num_days):
            col = chr(ord("C") + i)
            present_row = 5 + self.num_students
            total_students = self.num_students
            builder.cell(
                f"=IF(COUNTA({col}4:{col}{3 + self.num_students})=0;0;{col}{present_row}/{total_students}*100)")

        return builder


__all__ = ["StudentAttendanceTemplate"]
