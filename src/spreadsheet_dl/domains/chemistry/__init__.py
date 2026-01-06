"""Chemistry Domain Plugin for SpreadsheetDL.

    Chemistry domain plugin
    BATCH-4: Chemistry domain creation

Provides chemistry-specific functionality including:
- Thermodynamics, solutions, and kinetics formulas
- Utility functions for chemistry calculations

Features:
    - 20 specialized formulas for chemistry calculations
    - 8 thermodynamics formulas (Gibbs, enthalpy, entropy, equilibrium, etc.)
    - 7 solutions formulas (molarity, pH, osmotic pressure, etc.)
    - 5 kinetics formulas (rate constants, half-life, activation energy)
"""

from __future__ import annotations

# Formulas - Kinetics (5 formulas)
from spreadsheet_dl.domains.chemistry.formulas.kinetics import (
    ActivationEnergyFormula,
    HalfLifeFirstOrderFormula,
    HalfLifeSecondOrderFormula,
    IntegratedRateLawFormula,
    RateConstantFormula,
)

# Formulas - Solutions (7 formulas)
from spreadsheet_dl.domains.chemistry.formulas.solutions import (
    BufferCapacityFormula,
    MolalityFormula,
    MolarityFormula,
    MoleFractionFormula,
    OsmoticPressureFormula,
    RaoultsLawFormula,
    pHCalculationFormula,
)

# Formulas - Thermodynamics (8 formulas)
from spreadsheet_dl.domains.chemistry.formulas.thermodynamics import (
    ClausiusClapeyronFormula,
    EnthalpyChangeFormula,
    EntropyChangeFormula,
    EquilibriumConstantFormula,
    GibbsFreeEnergyFormula,
    IdealGasLawFormula,
    RealGasVanDerWaalsFormula,
    VantHoffEquationFormula,
)

# Plugin
from spreadsheet_dl.domains.chemistry.plugin import ChemistryDomainPlugin

# Utils
from spreadsheet_dl.domains.chemistry.utils import (
    calculate_concentration_from_absorbance,
    calculate_concentration_from_ph,
    calculate_dilution_factor,
    calculate_molecular_weight,
    calculate_ph_from_concentration,
    celsius_to_kelvin,
    format_scientific_notation,
    kelvin_to_celsius,
)

__all__ = [
    "ActivationEnergyFormula",
    "BufferCapacityFormula",
    "ChemistryDomainPlugin",
    "ClausiusClapeyronFormula",
    "EnthalpyChangeFormula",
    "EntropyChangeFormula",
    "EquilibriumConstantFormula",
    "GibbsFreeEnergyFormula",
    "HalfLifeFirstOrderFormula",
    "HalfLifeSecondOrderFormula",
    "IdealGasLawFormula",
    "IntegratedRateLawFormula",
    "MolalityFormula",
    "MolarityFormula",
    "MoleFractionFormula",
    "OsmoticPressureFormula",
    "RaoultsLawFormula",
    "RateConstantFormula",
    "RealGasVanDerWaalsFormula",
    "VantHoffEquationFormula",
    "calculate_concentration_from_absorbance",
    "calculate_concentration_from_ph",
    "calculate_dilution_factor",
    "calculate_molecular_weight",
    "calculate_ph_from_concentration",
    "celsius_to_kelvin",
    "format_scientific_notation",
    "kelvin_to_celsius",
    "pHCalculationFormula",
]
