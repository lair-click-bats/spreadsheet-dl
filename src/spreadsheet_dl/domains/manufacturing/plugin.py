"""Manufacturing Domain Plugin for SpreadsheetDL.

Implements:
    Manufacturing domain plugin
    PHASE-C: Domain plugin implementations

Provides manufacturing-specific functionality including:
- Production, quality, and inventory metrics formulas
- MES, ERP, and sensor data importers
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


class ManufacturingDomainPlugin(BaseDomainPlugin):
    """Manufacturing domain plugin.

    Implements:
        Complete Manufacturing domain plugin
        PHASE-C: Domain plugin implementations

    Provides comprehensive manufacturing functionality for SpreadsheetDL
    with formulas and importers tailored for production planning,
    quality control, and inventory management.

    Formulas (12 total):
        Production Metrics (4):
        - CYCLE_TIME: Production cycle time
        - TAKT_TIME: Takt time calculation
        - THROUGHPUT: Production throughput
        - CAPACITY_UTILIZATION: Capacity utilization rate

        Quality Metrics (4):
        - DEFECT_RATE: Defect rate calculation
        - FIRST_PASS_YIELD: First pass yield
        - PROCESS_CAPABILITY: Process capability index
        - CONTROL_LIMITS: SPC control limits

        Inventory Metrics (4):
        - EOQ: Economic order quantity
        - REORDER_POINT: Reorder point
        - SAFETY_STOCK: Safety stock level
        - INVENTORY_TURNOVER: Inventory turnover ratio

    Importers:
        - MESDataImporter: Manufacturing Execution System data
        - ERPDataImporter: Enterprise Resource Planning data
        - SensorDataImporter: IoT sensor data

    Example:
        >>> plugin = ManufacturingDomainPlugin()
        >>> plugin.initialize()
        >>> formulas = plugin.list_formulas()
    """

    @property
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata.

        Returns:
            PluginMetadata with manufacturing plugin information

        Implements:
            Plugin metadata requirements
        """
        return PluginMetadata(
            name="manufacturing",
            version="4.0.0",
            description="Manufacturing formulas and importers for production planning and quality control",
            author="SpreadsheetDL Team",
            license="MIT",
            homepage="https://github.com/lair-click-bats/spreadsheet-dl",
            tags=("manufacturing", "production", "quality-control", "inventory", "oee"),
            min_spreadsheet_dl_version="4.0.0",
        )

    def initialize(self) -> None:
        """Initialize plugin resources.

        Registers all formulas and importers.

        Implements:
            Plugin initialization with all components

        Raises:
            Exception: If initialization fails
        """
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
        """Cleanup plugin resources.

        No resources need explicit cleanup for this plugin.

        Implements:
            Plugin cleanup method
        """
        pass

    def validate(self) -> bool:
        """Validate plugin configuration.

        Returns:
            True if plugin has required formulas and importers registered

        Implements:
            Plugin validation
        """
        required_formulas = 12  # 4 production + 4 quality + 4 inventory
        required_importers = 3

        return (
            len(self._formulas) >= required_formulas
            and len(self._importers) >= required_importers
        )


__all__ = [
    "ManufacturingDomainPlugin",
]
