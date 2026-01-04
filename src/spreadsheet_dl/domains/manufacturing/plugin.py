"""
Manufacturing Domain Plugin for SpreadsheetDL.

Implements:
    TASK-C005: Manufacturing domain plugin
    PHASE-C: Domain plugin implementations

Provides manufacturing-specific functionality including:
- Production schedule and capacity planning templates
- Quality control with SPC charts
- Inventory management with safety stock
- OEE tracking templates
- Bill of materials with cost rollups
- Production and quality metrics formulas
- MES, ERP, and sensor data importers

Features:
    - 5 professional templates for manufacturing workflows
    - Production, quality, and inventory formula extensions
    - Import from MES, ERP, and IoT sensor data
    - Integration with manufacturing systems
"""

from __future__ import annotations

from spreadsheet_dl.domains.base import BaseDomainPlugin, PluginMetadata

# Import formulas
from spreadsheet_dl.domains.manufacturing.formulas.inventory import (
    EOQFormula,
    InventoryTurnoverFormula,
    ReorderPointFormula,
    SafetyStockFormula,
)
from spreadsheet_dl.domains.manufacturing.formulas.production import (
    CapacityUtilizationFormula,
    CycleTimeFormula,
    TaktTimeFormula,
    ThroughputFormula,
)
from spreadsheet_dl.domains.manufacturing.formulas.quality import (
    ControlLimitsFormula,
    DefectRateFormula,
    FirstPassYieldFormula,
    ProcessCapabilityFormula,
)

# Import importers
from spreadsheet_dl.domains.manufacturing.importers.erp_data import ERPDataImporter
from spreadsheet_dl.domains.manufacturing.importers.mes_data import MESDataImporter
from spreadsheet_dl.domains.manufacturing.importers.sensor_data import (
    SensorDataImporter,
)

# Import templates
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


class ManufacturingDomainPlugin(BaseDomainPlugin):
    """
    Manufacturing domain plugin.

    Implements:
        TASK-C005: Complete Manufacturing domain plugin
        PHASE-C: Domain plugin implementations

    Provides comprehensive manufacturing functionality for SpreadsheetDL
    with templates, formulas, and importers tailored for production planning,
    quality control, and inventory management.

    Example:
        >>> plugin = ManufacturingDomainPlugin()
        >>> plugin.initialize()
        >>> template_class = plugin.get_template("production_schedule")
        >>> template = template_class()
        >>> builder = template.generate()
        >>> builder.save("production_schedule.ods")
    """

    @property
    def metadata(self) -> PluginMetadata:
        """
        Get plugin metadata.

        Returns:
            PluginMetadata with manufacturing plugin information

        Implements:
            TASK-C005: Plugin metadata requirements
        """
        return PluginMetadata(
            name="manufacturing",
            version="4.0.0",
            description="Manufacturing templates, formulas, and importers for production planning and quality control",
            author="SpreadsheetDL Team",
            license="MIT",
            homepage="https://github.com/spreadsheet-dl/spreadsheet-dl",
            tags=("manufacturing", "production", "quality-control", "inventory", "oee"),
            min_spreadsheet_dl_version="4.0.0",
        )

    def initialize(self) -> None:
        """
        Initialize plugin resources.

        Registers all templates, formulas, and importers.

        Implements:
            TASK-C005: Plugin initialization with all components

        Raises:
            Exception: If initialization fails
        """
        # Register templates (5 total)
        self.register_template("production_schedule", ProductionScheduleTemplate)
        self.register_template("quality_control", QualityControlTemplate)
        self.register_template("inventory_management", InventoryManagementTemplate)
        self.register_template("oee_tracking", OEETrackingTemplate)
        self.register_template("bill_of_materials", BillOfMaterialsTemplate)

        # Register production metrics formulas (4)
        self.register_formula("CYCLE_TIME", CycleTimeFormula)
        self.register_formula("TAKT_TIME", TaktTimeFormula)
        self.register_formula("THROUGHPUT", ThroughputFormula)
        self.register_formula("CAPACITY_UTILIZATION", CapacityUtilizationFormula)

        # Register quality metrics formulas (4)
        self.register_formula("DEFECT_RATE", DefectRateFormula)
        self.register_formula("FIRST_PASS_YIELD", FirstPassYieldFormula)
        self.register_formula("PROCESS_CAPABILITY", ProcessCapabilityFormula)
        self.register_formula("CONTROL_LIMITS", ControlLimitsFormula)

        # Register inventory metrics formulas (4)
        self.register_formula("EOQ", EOQFormula)
        self.register_formula("REORDER_POINT", ReorderPointFormula)
        self.register_formula("SAFETY_STOCK", SafetyStockFormula)
        self.register_formula("INVENTORY_TURNOVER", InventoryTurnoverFormula)

        # Register importers (3 total)
        self.register_importer("mes_data", MESDataImporter)
        self.register_importer("erp_data", ERPDataImporter)
        self.register_importer("sensor_data", SensorDataImporter)

    def cleanup(self) -> None:
        """
        Cleanup plugin resources.

        No resources need explicit cleanup for this plugin.

        Implements:
            TASK-C005: Plugin cleanup method
        """
        # No cleanup needed for this plugin
        pass

    def validate(self) -> bool:
        """
        Validate plugin configuration.

        Returns:
            True if plugin has required templates and formulas registered

        Implements:
            TASK-C005: Plugin validation
        """
        # Verify we have all required components
        required_templates = 5
        required_formulas = 12  # 4 production + 4 quality + 4 inventory
        required_importers = 3

        return (
            len(self._templates) >= required_templates
            and len(self._formulas) >= required_formulas
            and len(self._importers) >= required_importers
        )


__all__ = [
    "ManufacturingDomainPlugin",
]
