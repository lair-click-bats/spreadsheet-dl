"""Electrical Engineering formulas for SpreadsheetDL.

Implements:
    Electrical Engineering domain formulas

Provides domain-specific formulas for:
- Power calculations (dissipation, voltage drop, current)
- Impedance calculations (parallel/series resistance, capacitance, inductance)
- Signal analysis (SNR, bandwidth, rise time, propagation delay)
"""

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

__all__ = [
    "BandwidthFormula",
    "CapacitanceFormula",
    "CurrentCalcFormula",
    "InductanceFormula",
    # Impedance formulas
    "ParallelResistanceFormula",
    # Power formulas
    "PowerDissipationFormula",
    "PropagationDelayFormula",
    "RiseTimeFormula",
    "SeriesResistanceFormula",
    # Signal formulas
    "SignalToNoiseRatioFormula",
    "ThermalResistanceFormula",
    "VoltageDropFormula",
]
