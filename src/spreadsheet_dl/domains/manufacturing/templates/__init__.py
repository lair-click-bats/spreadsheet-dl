"""
Manufacturing templates module.

Implements:
    TASK-C005: Manufacturing template exports
"""

from spreadsheet_dl.domains.manufacturing.templates.bill_of_materials import (
    BillOfMaterialsTemplate,
)
from spreadsheet_dl.domains.manufacturing.templates.inventory_management import (
    InventoryManagementTemplate,
)
from spreadsheet_dl.domains.manufacturing.templates.oee_tracking import (
    OEETrackingTemplate,
)
from spreadsheet_dl.domains.manufacturing.templates.production_schedule import (
    ProductionScheduleTemplate,
)
from spreadsheet_dl.domains.manufacturing.templates.quality_control import (
    QualityControlTemplate,
)

__all__ = [
    "BillOfMaterialsTemplate",
    "InventoryManagementTemplate",
    "OEETrackingTemplate",
    "ProductionScheduleTemplate",
    "QualityControlTemplate",
]
