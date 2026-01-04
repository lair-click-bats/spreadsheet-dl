"""
Mechanical Engineering Domain Plugin for SpreadsheetDL.

Provides comprehensive mechanical engineering functionality including:
- Stress analysis and material properties templates
- Assembly instructions and tolerance stackup
- Manufacturing specifications
- Stress/strain, moment, thermal, and fatigue formulas
- CAD metadata, FEA results, and material database importers

Implements:
    REQ-C003-001: Mechanical Engineering domain plugin
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

# Templates
from spreadsheet_dl.domains.mechanical_engineering.templates import (
    AssemblyInstructionsTemplate,
    ManufacturingSpecsTemplate,
    MaterialPropertiesTemplate,
    StressAnalysisTemplate,
    ToleranceStackupTemplate,
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
    "AssemblyInstructionsTemplate",
    "BendingStressFormula",
    "CADMetadataImporter",
    "FEAResultsImporter",
    "FatigueLifeFormula",
    "ManufacturingSpecsTemplate",
    "MaterialDatabaseImporter",
    "MaterialPropertiesTemplate",
    "MechanicalEngineeringDomainPlugin",
    "MomentOfInertiaFormula",
    "SafetyFactorFormula",
    "StrainFormula",
    "StressAnalysisTemplate",
    "StressConcentrationFormula",
    "StressFormula",
    "ThermalExpansionFormula",
    "ThermalStressFormula",
    "ToleranceStackupTemplate",
    "TorsionalStressFormula",
    "YoungsModulusFormula",
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
