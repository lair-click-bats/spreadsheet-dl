"""
Formulas for mechanical engineering domain.

Implements:
    REQ-C003-007: Mechanical engineering formula modules
"""

from spreadsheet_dl.domains.mechanical_engineering.formulas.fatigue import (
    FatigueLifeFormula,
    SafetyFactorFormula,
    StressConcentrationFormula,
)
from spreadsheet_dl.domains.mechanical_engineering.formulas.moment import (
    BendingStressFormula,
    MomentOfInertiaFormula,
    TorsionalStressFormula,
)
from spreadsheet_dl.domains.mechanical_engineering.formulas.stress_strain import (
    StressFormula,
    StrainFormula,
    YoungsModulusFormula,
)
from spreadsheet_dl.domains.mechanical_engineering.formulas.thermal import (
    ThermalExpansionFormula,
    ThermalStressFormula,
)

__all__ = [
    # Stress/Strain
    "StressFormula",
    "StrainFormula",
    "YoungsModulusFormula",
    # Moment
    "MomentOfInertiaFormula",
    "BendingStressFormula",
    "TorsionalStressFormula",
    # Thermal
    "ThermalExpansionFormula",
    "ThermalStressFormula",
    # Fatigue
    "FatigueLifeFormula",
    "SafetyFactorFormula",
    "StressConcentrationFormula",
]
