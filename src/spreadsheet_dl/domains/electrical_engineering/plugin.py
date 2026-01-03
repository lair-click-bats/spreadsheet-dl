"""
Electrical Engineering Domain Plugin for SpreadsheetDL.

Implements:
    TASK-C002: Electrical Engineering domain plugin
    PHASE-C: Domain plugin implementations

Provides electrical engineering-specific functionality including:
- BOM (Bill of Materials) tracking and cost analysis
- Pin mapping for ICs and connectors
- Power budget analysis and monitoring
- Signal routing documentation for PCB design
- Test procedure tracking with pass/fail analysis
- Power, impedance, and signal formulas
- KiCad, Eagle, and generic CSV importers

Features:
    - 5 professional templates for EE workflows
    - 12 electrical engineering formula extensions
    - 3 importers for CAD tool exports
    - Integration with KiCad, Eagle, and other EDA tools
"""

from __future__ import annotations

from spreadsheet_dl.domains.base import BaseDomainPlugin, PluginMetadata

# Import formulas
from spreadsheet_dl.domains.electrical_engineering.formulas.impedance import (
    CapacitanceFormula,
    InductanceFormula,
    ParallelResistanceFormula,
    SeriesResistanceFormula,
)
from spreadsheet_dl.domains.electrical_engineering.formulas.power import (
    CurrentCalcFormula,
    PowerDissipationFormula,
    ThermalResistanceFormula,
    VoltageDropFormula,
)
from spreadsheet_dl.domains.electrical_engineering.formulas.signal import (
    BandwidthFormula,
    PropagationDelayFormula,
    RiseTimeFormula,
    SignalToNoiseRatioFormula,
)

# Import importers
from spreadsheet_dl.domains.electrical_engineering.importers.component_csv import (
    GenericComponentCSVImporter,
)
from spreadsheet_dl.domains.electrical_engineering.importers.eagle_bom import (
    EagleBOMImporter,
)
from spreadsheet_dl.domains.electrical_engineering.importers.kicad_bom import (
    KiCadBOMImporter,
)

# Import templates
from spreadsheet_dl.domains.electrical_engineering.templates.bom import BOMTemplate
from spreadsheet_dl.domains.electrical_engineering.templates.pin_mapping import (
    PinMappingTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.power_budget import (
    PowerBudgetTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.signal_routing import (
    SignalRoutingTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.test_procedure import (
    TestProcedureTemplate,
)


class ElectricalEngineeringDomainPlugin(BaseDomainPlugin):
    """
    Electrical Engineering domain plugin.

    Implements:
        TASK-C002: Complete Electrical Engineering domain plugin
        PHASE-C: Domain plugin implementations

    Provides comprehensive electrical engineering functionality for SpreadsheetDL
    with templates, formulas, and importers tailored for hardware/PCB design.

    Example:
        >>> plugin = ElectricalEngineeringDomainPlugin()
        >>> plugin.initialize()
        >>> template_class = plugin.get_template("bom")
        >>> template = template_class(project_name="Widget Rev A")
        >>> builder = template.generate()
        >>> builder.save("widget_bom.ods")
    """

    @property
    def metadata(self) -> PluginMetadata:
        """
        Get plugin metadata.

        Returns:
            PluginMetadata with electrical engineering plugin information

        Implements:
            TASK-C002: Plugin metadata requirements
        """
        return PluginMetadata(
            name="electrical_engineering",
            version="4.0.0",
            description="Electrical engineering templates, formulas, and importers for hardware/PCB design",
            author="SpreadsheetDL Team",
            license="MIT",
            homepage="https://github.com/spreadsheet-dl/spreadsheet-dl",
            tags=(
                "electrical-engineering",
                "electronics",
                "pcb",
                "hardware",
                "bom",
                "power",
            ),
            min_spreadsheet_dl_version="4.0.0",
        )

    def initialize(self) -> None:
        """
        Initialize plugin resources.

        Registers all templates, formulas, and importers.

        Implements:
            TASK-C002: Plugin initialization with all components

        Raises:
            Exception: If initialization fails
        """
        # Register templates (5 total)
        self.register_template("bom", BOMTemplate)
        self.register_template("pin_mapping", PinMappingTemplate)
        self.register_template("power_budget", PowerBudgetTemplate)
        self.register_template("signal_routing", SignalRoutingTemplate)
        self.register_template("test_procedure", TestProcedureTemplate)

        # Register power formulas (4 total)
        self.register_formula("POWER_DISSIPATION", PowerDissipationFormula)
        self.register_formula("VOLTAGE_DROP", VoltageDropFormula)
        self.register_formula("CURRENT_CALC", CurrentCalcFormula)
        self.register_formula("THERMAL_RESISTANCE", ThermalResistanceFormula)

        # Register impedance formulas (4 total)
        self.register_formula("PARALLEL_RESISTANCE", ParallelResistanceFormula)
        self.register_formula("SERIES_RESISTANCE", SeriesResistanceFormula)
        self.register_formula("CAPACITANCE", CapacitanceFormula)
        self.register_formula("INDUCTANCE", InductanceFormula)

        # Register signal formulas (4 total)
        self.register_formula("SIGNAL_TO_NOISE_RATIO", SignalToNoiseRatioFormula)
        self.register_formula("BANDWIDTH", BandwidthFormula)
        self.register_formula("RISE_TIME", RiseTimeFormula)
        self.register_formula("PROPAGATION_DELAY", PropagationDelayFormula)

        # Register importers (3 total)
        self.register_importer("kicad_bom", KiCadBOMImporter)
        self.register_importer("eagle_bom", EagleBOMImporter)
        self.register_importer("component_csv", GenericComponentCSVImporter)

    def cleanup(self) -> None:
        """
        Cleanup plugin resources.

        No resources need explicit cleanup for this plugin.

        Implements:
            TASK-C002: Plugin cleanup method
        """
        # No cleanup needed for this plugin
        pass

    def validate(self) -> bool:
        """
        Validate plugin configuration.

        Returns:
            True if plugin has required templates and formulas registered

        Implements:
            TASK-C002: Plugin validation
        """
        # Verify we have all required components
        required_templates = 5
        required_formulas = 12  # 4 power + 4 impedance + 4 signal
        required_importers = 3

        return (
            len(self._templates) >= required_templates
            and len(self._formulas) >= required_formulas
            and len(self._importers) >= required_importers
        )


__all__ = [
    "ElectricalEngineeringDomainPlugin",
]
