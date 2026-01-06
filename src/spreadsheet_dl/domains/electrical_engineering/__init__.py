"""Electrical Engineering Domain Plugin for SpreadsheetDL.

Implements:
    Electrical Engineering domain plugin
    PHASE-C: Domain plugin implementations

Provides comprehensive electrical engineering functionality including:
- Power, impedance, and signal calculation formulas
- KiCad, Eagle, and generic component importers

Example:
    >>> from spreadsheet_dl.domains.electrical_engineering import (
    ...     ElectricalEngineeringDomainPlugin,
    ...     PowerDissipationFormula,
    ... )
    >>>
    >>> plugin = ElectricalEngineeringDomainPlugin()
    >>> plugin.initialize()
"""

# Plugin
# Formulas - Impedance
from spreadsheet_dl.domains.electrical_engineering.formulas.impedance import (
    CapacitanceFormula,
    InductanceFormula,
    ParallelResistanceFormula,
    SeriesResistanceFormula,
)

# Formulas - Power
from spreadsheet_dl.domains.electrical_engineering.formulas.power import (
    CurrentCalcFormula,
    PowerDissipationFormula,
    ThermalResistanceFormula,
    VoltageDropFormula,
)

# Formulas - Signal
from spreadsheet_dl.domains.electrical_engineering.formulas.signal import (
    BandwidthFormula,
    PropagationDelayFormula,
    RiseTimeFormula,
    SignalToNoiseRatioFormula,
)

# Importers
from spreadsheet_dl.domains.electrical_engineering.importers.component_csv import (
    GenericComponentCSVImporter,
)
from spreadsheet_dl.domains.electrical_engineering.importers.eagle_bom import (
    EagleBOMImporter,
)
from spreadsheet_dl.domains.electrical_engineering.importers.kicad_bom import (
    KiCadBOMImporter,
    KiCadComponent,
)
from spreadsheet_dl.domains.electrical_engineering.plugin import (
    ElectricalEngineeringDomainPlugin,
)

__all__ = [
    # Formulas - Signal
    "BandwidthFormula",
    # Formulas - Impedance
    "CapacitanceFormula",
    # Formulas - Power
    "CurrentCalcFormula",
    # Importers
    "EagleBOMImporter",
    # Plugin
    "ElectricalEngineeringDomainPlugin",
    "GenericComponentCSVImporter",
    "InductanceFormula",
    "KiCadBOMImporter",
    "KiCadComponent",
    "ParallelResistanceFormula",
    "PowerDissipationFormula",
    "PropagationDelayFormula",
    "RiseTimeFormula",
    "SeriesResistanceFormula",
    "SignalToNoiseRatioFormula",
    "ThermalResistanceFormula",
    "VoltageDropFormula",
]
