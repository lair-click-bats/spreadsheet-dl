"""Physics domain formulas.

Implements:
    Physics formula implementations (25 formulas)
    BATCH-5: Physics domain creation
"""

from __future__ import annotations

from spreadsheet_dl.domains.physics.formulas.electromagnetism import (
    CoulombLawFormula,
    ElectricFieldFormula,
    FaradayLawFormula,
    LorentzForceFormula,
    MagneticForceFormula,
    PoyntingVectorFormula,
)
from spreadsheet_dl.domains.physics.formulas.mechanics import (
    AngularMomentumFormula,
    CentripetalForceFormula,
    KineticEnergyFormula,
    MomentumFormula,
    NewtonSecondLawFormula,
    PotentialEnergyFormula,
    WorkEnergyFormula,
)
from spreadsheet_dl.domains.physics.formulas.optics import (
    BraggLawFormula,
    DiffractionGratingFormula,
    LensMakerEquationFormula,
    MagnificationLensFormula,
    SnellsLawFormula,
    ThinFilmInterferenceFormula,
)
from spreadsheet_dl.domains.physics.formulas.quantum import (
    BohrRadiusFormula,
    DeBroglieWavelengthFormula,
    HeisenbergUncertaintyFormula,
    PhotoelectricEffectFormula,
    PlanckEnergyFormula,
    RydbergFormulaFormula,
)

__all__ = [
    "AngularMomentumFormula",
    "BohrRadiusFormula",
    "BraggLawFormula",
    "CentripetalForceFormula",
    "CoulombLawFormula",
    "DeBroglieWavelengthFormula",
    "DiffractionGratingFormula",
    "ElectricFieldFormula",
    "FaradayLawFormula",
    "HeisenbergUncertaintyFormula",
    "KineticEnergyFormula",
    "LensMakerEquationFormula",
    "LorentzForceFormula",
    "MagneticForceFormula",
    "MagnificationLensFormula",
    "MomentumFormula",
    "NewtonSecondLawFormula",
    "PhotoelectricEffectFormula",
    "PlanckEnergyFormula",
    "PotentialEnergyFormula",
    "PoyntingVectorFormula",
    "RydbergFormulaFormula",
    "SnellsLawFormula",
    "ThinFilmInterferenceFormula",
    "WorkEnergyFormula",
]
