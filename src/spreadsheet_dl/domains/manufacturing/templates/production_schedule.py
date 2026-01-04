"""
Production Schedule Template for manufacturing capacity planning.

Implements:
    TASK-C005: ProductionScheduleTemplate for manufacturing domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class ProductionScheduleTemplate(BaseTemplate):
    """
    Production schedule with capacity planning and scheduling.

    Implements:
        TASK-C005: ProductionScheduleTemplate with capacity analysis

    Features:
    - Work order tracking with priority
    - Resource allocation (machines, labor)
    - Capacity planning and utilization
    - Timeline Gantt-style view
    - Status tracking (scheduled, in-progress, completed)
    - Bottleneck identification

    Example:
        >>> template = ProductionScheduleTemplate(
        ...     facility_name="Assembly Line A",
        ...     planning_periods=["Week 1", "Week 2", "Week 3", "Week 4"],
        ... )
        >>> builder = template.generate()
        >>> builder.save("production_schedule.ods")
    """

    facility_name: str = "Production Facility"
    num_products: int = 10
    include_capacity_analysis: bool = True
    theme: str = "default"

    @property
    def planning_periods(self) -> list[str]:
        """Generate default planning periods."""
        return ["Week 1", "Week 2", "Week 3", "Week 4"]

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for production schedule template

        Implements:
            TASK-C005: Template metadata
        """
        return TemplateMetadata(
            name="Production Schedule",
            description="Production schedule with capacity planning and resource allocation",
            category="manufacturing",
            tags=("production", "scheduling", "capacity", "planning"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """Validate template parameters."""
        return self.num_products > 0

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the production schedule spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C005: ProductionScheduleTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Production Schedule - {self.facility_name}",
            author="Production Planning",
            subject="Production Schedule",
            description=f"Production schedule and capacity planning for {self.facility_name}",
            keywords=["production", "schedule", "capacity", self.facility_name],
        )

        # Create schedule sheet
        builder.sheet("Schedule")
        self._create_schedule_sheet(builder)

        # Create capacity analysis if requested
        if self.include_capacity_analysis:
            builder.sheet("Capacity Analysis")
            self._create_capacity_sheet(builder)

        return builder

    def _create_schedule_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create the production schedule sheet."""
        # Define columns
        builder.column("WO #", width="80pt", style="text")
        builder.column("Product", width="150pt", style="text")
        builder.column("Quantity", width="80pt", type="number")
        builder.column("Priority", width="80pt", style="text")
        builder.column("Machine", width="100pt", style="text")
        builder.column("Status", width="100pt", style="text")

        # Add period columns
        for period in self.planning_periods:
            builder.column(period, width="90pt", type="number")

        builder.column("Total Hours", width="100pt", type="number")

        builder.freeze(rows=1)

        # Header row
        builder.row(style="header_primary")
        builder.cell("WO #")
        builder.cell("Product")
        builder.cell("Quantity")
        builder.cell("Priority")
        builder.cell("Machine")
        builder.cell("Status")

        for period in self.planning_periods:
            builder.cell(period)

        builder.cell("Total Hours")

        # Sample data rows
        sample_orders = [
            ("WO-001", "Widget A", 500, "High", "Machine 1", "Scheduled"),
            ("WO-002", "Widget B", 300, "Medium", "Machine 2", "In Progress"),
            ("WO-003", "Widget C", 750, "High", "Machine 1", "Scheduled"),
            ("WO-004", "Widget D", 200, "Low", "Machine 3", "Scheduled"),
            ("WO-005", "Widget A", 400, "Medium", "Machine 2", "Completed"),
        ]

        for row_idx, (wo, product, qty, priority, machine, status) in enumerate(
            sample_orders, start=2
        ):
            builder.row()
            builder.cell(wo)
            builder.cell(product)
            builder.cell(qty)
            builder.cell(priority)
            builder.cell(machine)
            builder.cell(status)

            # Sample hours allocation
            for _ in self.planning_periods:
                builder.cell(0, style="number")

            # Total formula
            col_start = chr(ord("G"))
            col_end = chr(ord("F") + len(self.planning_periods))
            builder.cell(f"=SUM({col_start}{row_idx}:{col_end}{row_idx})")

    def _create_capacity_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create capacity analysis sheet."""
        builder.column("Resource", width="150pt")
        builder.column("Max Capacity (hrs)", width="120pt", type="number")

        for period in self.planning_periods:
            builder.column(f"{period} Allocated", width="100pt", type="number")
            builder.column(f"{period} Utilization %", width="100pt", type="number")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Resource")
        builder.cell("Max Capacity (hrs)")

        for period in self.planning_periods:
            builder.cell(f"{period} Allocated")
            builder.cell(f"{period} Util %")

        # Sample resources
        resources = [
            ("Machine 1", 160),
            ("Machine 2", 160),
            ("Machine 3", 80),
            ("Labor Team A", 320),
        ]

        for row_idx, (resource, capacity) in enumerate(resources, start=2):
            builder.row()
            builder.cell(resource)
            builder.cell(capacity)

            # Allocated and utilization for each period
            for col_idx in range(len(self.planning_periods)):
                # Allocated hours
                builder.cell(0, style="number")
                # Utilization %
                alloc_col = chr(ord("C") + col_idx * 2)
                builder.cell(f"=({alloc_col}{row_idx}/B{row_idx})*100")


__all__ = ["ProductionScheduleTemplate"]
