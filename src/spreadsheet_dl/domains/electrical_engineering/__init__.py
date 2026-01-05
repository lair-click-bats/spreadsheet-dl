"""Electrical Engineering Domain Plugin for SpreadsheetDL.

Implements:
    Electrical Engineering domain plugin
    PHASE-C: Domain plugin implementations

Provides comprehensive electrical engineering functionality including:
- Bill of Materials (BOM) tracking and analysis
- Pin mapping for ICs and connectors
- Power budget analysis and monitoring
- Signal routing documentation
- Test procedure tracking
- Power, impedance, and signal calculation formulas
- KiCad, Eagle, and generic component importers

Example:
    >>> from spreadsheet_dl.domains.electrical_engineering import (
    ...     ElectricalEngineeringDomainPlugin,
    ...     BOMTemplate,
    ...     PowerDissipationFormula,
    ... )
    >>>
    >>> # Use plugin
    >>> plugin = ElectricalEngineeringDomainPlugin()
    >>> plugin.initialize()
    >>>
    >>> # Use template directly
    >>> bom = BOMTemplate(project_name="Widget Rev A")
    >>> builder = bom.generate()
    >>> path = builder.save("widget_bom.ods")
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

# Templates
from spreadsheet_dl.domains.electrical_engineering.templates.bom import BOMTemplate
from spreadsheet_dl.domains.electrical_engineering.templates.pin_mapping import (
    PinMappingTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.power_budget import (
    PowerBudgetTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.procedure_template import (
    ProcedureTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.signal_routing import (
    SignalRoutingTemplate,
)

__all__ = [
    "BOMTemplate",
    "BandwidthFormula",
    "CapacitanceFormula",
    "CurrentCalcFormula",
    "EagleBOMImporter",
    "ElectricalEngineeringDomainPlugin",
    "GenericComponentCSVImporter",
    "InductanceFormula",
    "KiCadBOMImporter",
    "KiCadComponent",
    "ParallelResistanceFormula",
    "PinMappingTemplate",
    "PowerBudgetTemplate",
    "PowerDissipationFormula",
    "ProcedureTemplate",
    "PropagationDelayFormula",
    "RiseTimeFormula",
    "SeriesResistanceFormula",
    "SignalRoutingTemplate",
    "SignalToNoiseRatioFormula",
    "ThermalResistanceFormula",
    "VoltageDropFormula",
]
