"""Mechanical Engineering Domain Plugin for SpreadsheetDL.

Provides comprehensive mechanical engineering functionality including:
- Stress/strain, moment, thermal, and fatigue formulas
- CAD metadata, FEA results, and material database importers

Implements:
    Mechanical Engineering domain plugin
"""

# Plugin
# Formulas
from spreadsheet_dl.domains.mechanical_engineering.formulas import (
    BendingStressFormula,
    FatigueLifeFormula,
    MomentOfInertiaFormula,
    SafetyFactorFormula,
    StrainFormula,
    StressConcentrationFormula,
    StressFormula,
    ThermalExpansionFormula,
    ThermalStressFormula,
    TorsionalStressFormula,
    YoungsModulusFormula,
)

# Importers
from spreadsheet_dl.domains.mechanical_engineering.importers import (
    CADMetadataImporter,
    FEAResultsImporter,
    MaterialDatabaseImporter,
)
from spreadsheet_dl.domains.mechanical_engineering.plugin import (
    MechanicalEngineeringDomainPlugin,
)

# Utilities
from spreadsheet_dl.domains.mechanical_engineering.utils import (
    inch_to_mm,
    kg_to_lb,
    lb_to_kg,
    mm_to_inch,
    moment_of_inertia_circle,
    moment_of_inertia_rectangle,
    mpa_to_psi,
    polar_moment_of_inertia_circle,
    principal_stresses_2d,
    principal_stresses_3d,
    psi_to_mpa,
    section_modulus_circle,
    section_modulus_rectangle,
    von_mises_stress,
)

__all__ = [
    # Formulas
    "BendingStressFormula",
    # Importers
    "CADMetadataImporter",
    "FEAResultsImporter",
    "FatigueLifeFormula",
    "MaterialDatabaseImporter",
    # Plugin
    "MechanicalEngineeringDomainPlugin",
    "MomentOfInertiaFormula",
    "SafetyFactorFormula",
    "StrainFormula",
    "StressConcentrationFormula",
    "StressFormula",
    "ThermalExpansionFormula",
    "ThermalStressFormula",
    "TorsionalStressFormula",
    "YoungsModulusFormula",
    # Utilities
    "inch_to_mm",
    "kg_to_lb",
    "lb_to_kg",
    "mm_to_inch",
    "moment_of_inertia_circle",
    "moment_of_inertia_rectangle",
    "mpa_to_psi",
    "polar_moment_of_inertia_circle",
    "principal_stresses_2d",
    "principal_stresses_3d",
    "psi_to_mpa",
    "section_modulus_circle",
    "section_modulus_rectangle",
    "von_mises_stress",
]
