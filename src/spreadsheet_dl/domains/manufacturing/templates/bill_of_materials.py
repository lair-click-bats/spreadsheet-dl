"""
Bill of Materials Template for manufacturing BOM with cost rollups.

Implements:
    TASK-C005: BillOfMaterialsTemplate for manufacturing domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class BillOfMaterialsTemplate(BaseTemplate):
    """
    Manufacturing BOM with yield, scrap rates, and cost rollups.

    Implements:
        TASK-C005: BillOfMaterialsTemplate with multi-level BOM

    Features:
    - Multi-level BOM structure (parent-child)
    - Quantity per assembly
    - Unit cost and extended cost
    - Yield percentage
    - Scrap rate tracking
    - Cost rollup calculations
    - Supplier information
    - Lead time tracking

    Example:
        >>> template = BillOfMaterialsTemplate(
        ...     product_name="Widget Assembly XL",
        ...     include_cost_rollup=True,
        ... )
        >>> builder = template.generate()
        >>> builder.save("bom.ods")
    """

    product_name: str = "Product"
    include_cost_rollup: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for BOM template

        Implements:
            TASK-C005: Template metadata
        """
        return TemplateMetadata(
            name="Bill of Materials",
            description="Manufacturing BOM with yield, scrap rates, and cost rollups",
            category="manufacturing",
            tags=("bom", "materials", "cost", "assembly"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the BOM spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C005: BillOfMaterialsTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"BOM - {self.product_name}",
            author="Engineering",
            subject="Bill of Materials",
            description=f"Bill of Materials for {self.product_name}",
            keywords=["bom", "materials", "assembly", self.product_name],
        )

        # Create BOM sheet
        builder.sheet("BOM")
        self._create_bom_sheet(builder)

        # Create cost rollup if requested
        if self.include_cost_rollup:
            builder.sheet("Cost Rollup")
            self._create_cost_rollup(builder)

        return builder

    def _create_bom_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create the BOM sheet."""
        builder.column("Level", width="60pt", type="number")
        builder.column("Part #", width="120pt", style="text")
        builder.column("Description", width="200pt", style="text")
        builder.column("Qty per Assembly", width="120pt", type="number")
        builder.column("Unit", width="80pt", style="text")
        builder.column("Unit Cost ($)", width="100pt", type="number")
        builder.column("Extended Cost ($)", width="120pt", type="number")
        builder.column("Yield %", width="80pt", type="number")
        builder.column("Scrap %", width="80pt", type="number")
        builder.column("Supplier", width="150pt", style="text")
        builder.column("Lead Time (days)", width="100pt", type="number")

        builder.freeze(rows=1)

        # Header row
        builder.row(style="header_primary")
        builder.cell("Level")
        builder.cell("Part #")
        builder.cell("Description")
        builder.cell("Qty per Assembly")
        builder.cell("Unit")
        builder.cell("Unit Cost ($)")
        builder.cell("Extended Cost ($)")
        builder.cell("Yield %")
        builder.cell("Scrap %")
        builder.cell("Supplier")
        builder.cell("Lead Time (days)")

        # Sample BOM structure
        # Level 0 = Final assembly, Level 1 = Major components, Level 2 = Parts
        bom_items = [
            (0, "WA-1000", "Widget Assembly XL", 1, "EA", 0, None, 98, 2),
            (1, "SA-100", "  Main Subassembly", 1, "EA", 125.50, None, 99, 1),
            (2, "P-001", "    Steel Plate 10mm", 2, "EA", 15.00, None, 100, 0),
            (2, "P-002", "    Aluminum Rod 5cm", 4, "EA", 8.50, None, 100, 0),
            (2, "P-003", "    Bearing SKF-123", 2, "EA", 12.75, None, 100, 0),
            (1, "SA-200", "  Control Subassembly", 1, "EA", 85.00, None, 98, 2),
            (2, "P-005", "    Circuit Board", 1, "EA", 45.00, None, 99, 1),
            (2, "P-008", "    Sensor Module", 2, "EA", 18.50, None, 100, 0),
            (1, "P-004", "  Motor 5HP", 1, "EA", 250.00, None, 100, 0),
            (1, "P-006", "  Hydraulic Pump", 1, "EA", 180.00, None, 99, 1),
            (1, "P-007", "  Control Panel", 1, "EA", 95.00, None, 100, 0),
            (1, "HW-KIT", "  Hardware Kit", 1, "SET", 25.00, None, 100, 0),
        ]

        for row_idx, (
            level,
            part,
            desc,
            qty,
            unit,
            cost,
            _,
            yield_pct,
            scrap,
        ) in enumerate(bom_items, start=2):
            builder.row()
            builder.cell(level)
            builder.cell(part)
            builder.cell(desc)
            builder.cell(qty)
            builder.cell(unit)
            builder.cell(cost if cost > 0 else 0, style="number")
            # Extended cost = Qty * Unit Cost / (Yield % / 100)
            if level > 0:  # Don't calculate for top level
                builder.cell(f"=(D{row_idx}*F{row_idx})/(H{row_idx}/100)")
            else:
                builder.cell("", style="number")
            builder.cell(yield_pct)
            builder.cell(scrap)
            builder.cell("", style="text")
            builder.cell(0, style="number")

    def _create_cost_rollup(self, builder: SpreadsheetBuilder) -> None:
        """Create cost rollup analysis sheet."""
        builder.column("Category", width="200pt")
        builder.column("Total Cost ($)", width="120pt", type="number")
        builder.column("Percentage", width="100pt", type="number")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Cost Rollup Analysis", colspan=3)

        builder.row(style="header_secondary")
        builder.cell("Category")
        builder.cell("Total Cost ($)")
        builder.cell("Percentage")

        # Cost categories
        categories = [
            ("Raw Materials (Level 2)", "=SUMIF(BOM.A:A,2,BOM.G:G)"),
            ("Subassemblies (Level 1)", "=SUMIF(BOM.A:A,1,BOM.G:G)"),
            ("Total Material Cost", "=B3+B4"),
            ("Scrap Cost (est.)", "=B5*0.02"),  # 2% average scrap
            ("Total BOM Cost", "=B5+B6"),
        ]

        for row_idx, (category, formula) in enumerate(categories, start=3):
            builder.row()
            builder.cell(category)
            builder.cell(formula)
            if row_idx <= 6:  # Only for main categories
                builder.cell(f"=(B{row_idx}/B$7)*100")
            else:
                builder.cell("", style="number")

        # Add blank row
        builder.row()

        # Cost by supplier (if we had supplier data)
        builder.row(style="header_secondary")
        builder.cell("Cost Summary", colspan=3)

        builder.row()
        builder.cell("Number of Components")
        builder.cell("=COUNTA(BOM.B2:B13)")
        builder.cell("")

        builder.row()
        builder.cell("Average Unit Cost")
        builder.cell("=AVERAGE(BOM.F2:F13)")
        builder.cell("")

        builder.row()
        builder.cell("Highest Cost Item")
        builder.cell("=MAX(BOM.F2:F13)")
        builder.cell("")


__all__ = ["BillOfMaterialsTemplate"]
