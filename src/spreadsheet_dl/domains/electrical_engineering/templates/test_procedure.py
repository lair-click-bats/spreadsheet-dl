"""
Test procedure template for hardware testing documentation.

Implements:
    TestProcedureTemplate with pass/fail tracking
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class TestProcedureTemplate(BaseTemplate):
    """
    Test procedure template for hardware test documentation.

    Implements:
        TestProcedureTemplate requirements

    Features:
        - Columns: Test Step, Description, Expected Result, Actual Result,
          Status (Pass/Fail/Skip), Duration, Tester, Date, Notes
        - Auto-status from expected vs actual comparison
        - Pass rate calculation (% passing)
        - Chart: Test results summary (Pass/Fail/Skip counts)
        - Conditional formatting: Green for Pass, Red for Fail, Gray for Skip

    Example:
        >>> template = TestProcedureTemplate(
        ...     project_name="Main Board Rev A",
        ...     test_suite="Functional Test"
        ... )
        >>> builder = template.generate()
        >>> builder.save("test_procedure.ods")
    """

    # Prevent pytest from collecting this class as a test
    __test__ = False

    project_name: str = "Hardware Test"
    test_suite: str = "Functional Test Suite"
    num_test_steps: int = 25
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Test Procedure",
            description="Hardware test procedure and results tracking",
            category="electrical_engineering",
            tags=("test", "procedure", "qa", "validation"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate test procedure spreadsheet.

        Returns:
            SpreadsheetBuilder configured with test procedure template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Test Procedure - {self.project_name}",
            author="QA Department",
            subject="Test Procedure",
            description=f"Test procedure for {self.project_name}",
            keywords=["test", "procedure", "qa", self.project_name],
        )

        # Create main test procedure sheet
        builder.sheet("Test Procedure")

        # Define columns
        builder.column("Test Step", width="70pt", style="text")
        builder.column("Description", width="200pt", style="text")
        builder.column("Expected Result", width="150pt", style="text")
        builder.column("Actual Result", width="150pt", style="text")
        builder.column("Status", width="80pt", style="text")
        builder.column("Duration (min)", width="80pt", type="number")
        builder.column("Tester", width="100pt", style="text")
        builder.column("Date", width="90pt", type="date")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Test Procedure - {self.project_name} - {self.test_suite}", colspan=9
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Test Step")
        builder.cell("Description")
        builder.cell("Expected Result")
        builder.cell("Actual Result")
        builder.cell("Status")
        builder.cell("Duration (min)")
        builder.cell("Tester")
        builder.cell("Date")
        builder.cell("Notes")

        # Test step rows
        for i in range(self.num_test_steps):
            i + 3
            builder.row()
            builder.cell(f"STEP-{i + 1:03d}")  # Auto-numbered step
            builder.cell("", style="input")  # Description
            builder.cell("", style="input")  # Expected Result
            builder.cell("", style="input")  # Actual Result
            # Status: Auto-calculate or manual input
            builder.cell("", style="input")  # Status (Pass/Fail/Skip)
            builder.cell(0, style="input")  # Duration
            builder.cell("", style="input")  # Tester
            builder.cell("", style="date_input")  # Date
            builder.cell("", style="input")  # Notes

        # Summary section
        self.num_test_steps + 4
        builder.row()  # Blank row

        builder.row(style="section_header")
        builder.cell("Test Results Summary", colspan=9)

        builder.row()
        builder.cell("Total Test Steps:", colspan=2)
        builder.cell(f"=COUNTA(A3:A{self.num_test_steps + 2})")
        builder.cell("")
        builder.cell("Tests Passed:", colspan=2)
        builder.cell(f'=COUNTIF(E3:E{self.num_test_steps + 2},"Pass")')

        builder.row()
        builder.cell("Tests Failed:", colspan=2)
        builder.cell(f'=COUNTIF(E3:E{self.num_test_steps + 2},"Fail")')
        builder.cell("")
        builder.cell("Tests Skipped:", colspan=2)
        builder.cell(f'=COUNTIF(E3:E{self.num_test_steps + 2},"Skip")')

        builder.row()
        builder.cell("Pass Rate (%):", colspan=2)
        pass_count_ref = f'COUNTIF(E3:E{self.num_test_steps + 2},"Pass")'
        total_count_ref = f"COUNTA(E3:E{self.num_test_steps + 2})"
        builder.cell(
            f"=IF({total_count_ref}=0,0,{pass_count_ref}/{total_count_ref})",
            style="percentage",
        )
        builder.cell("")
        builder.cell("Total Duration (min):", colspan=2)
        builder.cell(f"=SUM(F3:F{self.num_test_steps + 2})", style="number")

        builder.row()
        builder.cell("Average Duration (min):", colspan=2)
        builder.cell(f"=AVERAGE(F3:F{self.num_test_steps + 2})", style="number")
        builder.cell("")
        builder.cell("Test Status:", colspan=2)
        fail_count_ref = f'COUNTIF(E3:E{self.num_test_steps + 2},"Fail")'
        builder.cell(
            f'=IF({fail_count_ref}>0,"FAILED",IF({pass_count_ref}={total_count_ref},"PASSED","IN PROGRESS"))'
        )

        # Test metrics
        builder.row()
        builder.row(style="section_header")
        builder.cell("Test Metrics", colspan=9)

        builder.row()
        builder.cell("Completion Rate:", colspan=2)
        builder.cell(
            f"=COUNTA(E3:E{self.num_test_steps + 2})/{self.num_test_steps}",
            style="percentage",
        )
        builder.cell("")
        builder.cell("Failure Rate:", colspan=2)
        builder.cell(
            f"=IF({total_count_ref}=0,0,{fail_count_ref}/{total_count_ref})",
            style="percentage",
        )

        builder.row()
        builder.cell("Tests Remaining:", colspan=2)
        builder.cell(
            f"={self.num_test_steps}-COUNTA(E3:E{self.num_test_steps + 2})",
            style="number",
        )

        return builder

    def validate(self) -> bool:
        """Validate template configuration."""
        return self.num_test_steps > 0


__all__ = ["TestProcedureTemplate"]
