"""
Inventory Management Template for stock tracking and optimization.

Implements:
    TASK-C005: InventoryManagementTemplate for manufacturing domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class InventoryManagementTemplate(BaseTemplate):
    """
    Inventory tracking with reorder points and safety stock.

    Implements:
        TASK-C005: InventoryManagementTemplate with EOQ and safety stock

    Features:
    - Current stock levels
    - Reorder point calculations
    - Safety stock recommendations
    - Economic Order Quantity (EOQ)
    - Lead time tracking
    - Supplier information
    - Inventory turnover metrics

    Example:
        >>> template = InventoryManagementTemplate(
        ...     warehouse_name="Main Warehouse",
        ...     include_eoq: bool = True,
        ... )
        >>> builder = template.generate()
        >>> builder.save("inventory.ods")
    """

    warehouse_name: str = "Warehouse"
    include_eoq: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for inventory management template

        Implements:
            TASK-C005: Template metadata
        """
        return TemplateMetadata(
            name="Inventory Management",
            description="Inventory tracking with reorder points, safety stock, and EOQ",
            category="manufacturing",
            tags=("inventory", "stock", "reorder", "eoq"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the inventory management spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C005: InventoryManagementTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Inventory Management - {self.warehouse_name}",
            author="Inventory Control",
            subject="Inventory Management",
            description=f"Inventory tracking and optimization for {self.warehouse_name}",
            keywords=["inventory", "stock", "reorder", self.warehouse_name],
        )

        # Create inventory tracking sheet
        builder.sheet("Inventory")
        self._create_inventory_sheet(builder)

        # Create EOQ analysis if requested
        if self.include_eoq:
            builder.sheet("EOQ Analysis")
            self._create_eoq_sheet(builder)

        return builder

    def _create_inventory_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create the inventory tracking sheet."""
        builder.column("Part #", width="100pt", style="text")
        builder.column("Description", width="200pt", style="text")
        builder.column("Current Stock", width="100pt", type="number")
        builder.column("Reorder Point", width="100pt", type="number")
        builder.column("Safety Stock", width="100pt", type="number")
        builder.column("Lead Time (days)", width="100pt", type="number")
        builder.column("Daily Demand", width="100pt", type="number")
        builder.column("Status", width="100pt", style="text")
        builder.column("Supplier", width="150pt", style="text")

        builder.freeze(rows=1)

        # Header row
        builder.row(style="header_primary")
        builder.cell("Part #")
        builder.cell("Description")
        builder.cell("Current Stock")
        builder.cell("Reorder Point")
        builder.cell("Safety Stock")
        builder.cell("Lead Time (days)")
        builder.cell("Daily Demand")
        builder.cell("Status")
        builder.cell("Supplier")

        # Sample inventory items
        items = [
            ("P-001", "Steel Plate 10mm", 500, 200, 50, 7, 25),
            ("P-002", "Aluminum Rod 5cm", 1200, 400, 100, 5, 60),
            ("P-003", "Bearing SKF-123", 300, 150, 40, 14, 10),
            ("P-004", "Motor 5HP", 80, 30, 10, 21, 2),
            ("P-005", "Circuit Board", 450, 180, 50, 10, 15),
            ("P-006", "Hydraulic Pump", 65, 25, 8, 28, 1),
            ("P-007", "Control Panel", 120, 50, 15, 14, 3),
            ("P-008", "Sensor Module", 800, 300, 80, 7, 35),
        ]

        for row_idx, (
            part,
            desc,
            stock,
            reorder,
            safety,
            lead_time,
            demand,
        ) in enumerate(items, start=2):
            builder.row()
            builder.cell(part)
            builder.cell(desc)
            builder.cell(stock)
            builder.cell(reorder)
            builder.cell(safety)
            builder.cell(lead_time)
            builder.cell(demand)
            # Status based on stock level
            builder.cell(
                f'=IF(C{row_idx}<=D{row_idx},"REORDER",IF(C{row_idx}<=E{row_idx},"LOW","OK"))'
            )
            builder.cell("", style="text")

    def _create_eoq_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create EOQ analysis sheet."""
        builder.column("Part #", width="100pt", style="text")
        builder.column("Annual Demand", width="120pt", type="number")
        builder.column("Order Cost ($)", width="100pt", type="number")
        builder.column("Holding Cost ($/unit)", width="120pt", type="number")
        builder.column("EOQ", width="100pt", type="number")
        builder.column("Orders per Year", width="120pt", type="number")
        builder.column("Total Cost ($)", width="120pt", type="number")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Part #")
        builder.cell("Annual Demand")
        builder.cell("Order Cost ($)")
        builder.cell("Holding Cost ($/unit)")
        builder.cell("EOQ")
        builder.cell("Orders per Year")
        builder.cell("Total Cost ($)")

        # Sample EOQ calculations
        parts = [
            ("P-001", 9125, 50, 5),
            ("P-002", 21900, 50, 3),
            ("P-003", 3650, 75, 8),
            ("P-004", 730, 100, 25),
            ("P-005", 5475, 60, 12),
        ]

        for row_idx, (part, annual_demand, order_cost, holding_cost) in enumerate(
            parts, start=2
        ):
            builder.row()
            builder.cell(part)
            builder.cell(annual_demand)
            builder.cell(order_cost)
            builder.cell(holding_cost)
            # EOQ formula: SQRT((2 * D * S) / H)
            builder.cell(f"=SQRT((2*B{row_idx}*C{row_idx})/D{row_idx})")
            # Orders per year: D / EOQ
            builder.cell(f"=B{row_idx}/E{row_idx}")
            # Total cost: (D/EOQ)*S + (EOQ/2)*H
            builder.cell(
                f"=(B{row_idx}/E{row_idx})*C{row_idx}+(E{row_idx}/2)*D{row_idx}"
            )


__all__ = ["InventoryManagementTemplate"]
