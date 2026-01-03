"""
Templates for mechanical engineering domain.

Implements:
    REQ-C003-002: Mechanical engineering template modules
"""

from spreadsheet_dl.domains.mechanical_engineering.templates.assembly_instructions import (
    AssemblyInstructionsTemplate,
)
from spreadsheet_dl.domains.mechanical_engineering.templates.manufacturing_specs import (
    ManufacturingSpecsTemplate,
)
from spreadsheet_dl.domains.mechanical_engineering.templates.material_properties import (
    MaterialPropertiesTemplate,
)
from spreadsheet_dl.domains.mechanical_engineering.templates.stress_analysis import (
    StressAnalysisTemplate,
)
from spreadsheet_dl.domains.mechanical_engineering.templates.tolerance_stackup import (
    ToleranceStackupTemplate,
)

__all__ = [
    "AssemblyInstructionsTemplate",
    "ManufacturingSpecsTemplate",
    "MaterialPropertiesTemplate",
    "StressAnalysisTemplate",
    "ToleranceStackupTemplate",
]
