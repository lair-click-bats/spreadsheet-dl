"""Electrical Engineering Domain Plugin for SpreadsheetDL.

Implements:
    Electrical Engineering domain plugin
    PHASE-C: Domain plugin implementations

Provides electrical engineering-specific functionality including:
- Power, impedance, and signal formulas
- KiCad, Eagle, and generic CSV importers
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


class ElectricalEngineeringDomainPlugin(BaseDomainPlugin):
    """Electrical Engineering domain plugin.

    Implements:
        Complete Electrical Engineering domain plugin
        PHASE-C: Domain plugin implementations

    Provides comprehensive electrical engineering functionality for SpreadsheetDL
    with formulas and importers tailored for hardware/PCB design.

    Formulas (12 total):
        Power (4):
        - POWER_DISSIPATION: Power dissipation calculation
        - VOLTAGE_DROP: Voltage drop calculation
        - CURRENT_CALC: Current calculation
        - THERMAL_RESISTANCE: Thermal resistance

        Impedance (4):
        - PARALLEL_RESISTANCE: Parallel resistance
        - SERIES_RESISTANCE: Series resistance
        - CAPACITANCE: Capacitance calculation
        - INDUCTANCE: Inductance calculation

        Signal (4):
        - SIGNAL_TO_NOISE_RATIO: SNR calculation
        - BANDWIDTH: Bandwidth calculation
        - RISE_TIME: Rise time calculation
        - PROPAGATION_DELAY: Propagation delay

    Importers:
        - KiCadBOMImporter: KiCad BOM exports
        - EagleBOMImporter: Eagle BOM exports
        - GenericComponentCSVImporter: Generic component CSV

    Example:
        >>> plugin = ElectricalEngineeringDomainPlugin()
        >>> plugin.initialize()
        >>> formulas = plugin.list_formulas()
    """

    @property
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata.

        Returns:
            PluginMetadata with electrical engineering plugin information

        Implements:
            Plugin metadata requirements
        """
        return PluginMetadata(
            name="electrical_engineering",
            version="4.0.0",
            description="Electrical engineering formulas and importers for hardware/PCB design",
            author="SpreadsheetDL Team",
            license="MIT",
            homepage="https://github.com/lair-click-bats/spreadsheet-dl",
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
        """Initialize plugin resources.

        Registers all formulas and importers.

        Implements:
            Plugin initialization with all components

        Raises:
            Exception: If initialization fails
        """
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
        required_formulas = 12  # 4 power + 4 impedance + 4 signal
        required_importers = 3

        return (
            len(self._formulas) >= required_formulas
            and len(self._importers) >= required_importers
        )


__all__ = [
    "ElectricalEngineeringDomainPlugin",
]
