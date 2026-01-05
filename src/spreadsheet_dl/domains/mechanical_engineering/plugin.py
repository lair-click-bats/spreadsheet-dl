"""Mechanical Engineering Domain Plugin for SpreadsheetDL.

Implements:
    Mechanical Engineering domain plugin
    PHASE-C: Domain plugin implementations

Provides mechanical engineering-specific functionality including:
- Stress analysis templates with principal stress calculations
- Material properties database and tracking
- Assembly instructions with torque specifications
- Tolerance stackup analysis with statistical methods
- Manufacturing specifications tracking
- Stress/strain, moment, thermal, and fatigue formulas
- CAD metadata, FEA results, and material database importers

Features:
    - 5 professional templates for mechanical engineering workflows
    - 12 mechanical engineering formula extensions
    - 3 importers for CAD/FEA tool exports
    - Integration with STEP/IGES, FEA tools, and material databases
"""

from __future__ import annotations

from spreadsheet_dl.domains.base import BaseDomainPlugin, PluginMetadata

# Import formulas
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
    StrainFormula,
    StressFormula,
    YoungsModulusFormula,
)
from spreadsheet_dl.domains.mechanical_engineering.formulas.thermal import (
    ThermalExpansionFormula,
    ThermalStressFormula,
)

# Import importers
from spreadsheet_dl.domains.mechanical_engineering.importers.cad_metadata import (
    CADMetadataImporter,
)
from spreadsheet_dl.domains.mechanical_engineering.importers.fea_results import (
    FEAResultsImporter,
)
from spreadsheet_dl.domains.mechanical_engineering.importers.material_db import (
    MaterialDatabaseImporter,
)

# Import templates
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


class MechanicalEngineeringDomainPlugin(BaseDomainPlugin):
    """Mechanical Engineering domain plugin.

    Implements:
        Complete Mechanical Engineering domain plugin
        PHASE-C: Domain plugin implementations

    Provides comprehensive mechanical engineering functionality for SpreadsheetDL
    with templates, formulas, and importers tailored for mechanical design and analysis.

    Example:
        >>> plugin = MechanicalEngineeringDomainPlugin()
        >>> plugin.initialize()
        >>> template_class = plugin.get_template("stress_analysis")
        >>> template = template_class(analysis_name="Beam Bending")
        >>> builder = template.generate()
        >>> path = builder.save("stress_analysis.ods")
    """

    @property
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata.

        Returns:
            PluginMetadata with mechanical engineering plugin information

        Implements:
            Plugin metadata requirements
        """
        return PluginMetadata(
            name="mechanical_engineering",
            version="4.0.0",
            description="Mechanical engineering templates, formulas, and importers for design and analysis",
            author="SpreadsheetDL Team",
            license="MIT",
            homepage="https://github.com/lair-click-bats/spreadsheet-dl",
            tags=(
                "mechanical-engineering",
                "stress-analysis",
                "materials",
                "manufacturing",
                "fea",
                "cad",
            ),
            min_spreadsheet_dl_version="4.0.0",
        )

    def initialize(self) -> None:
        """Initialize plugin resources.

        Registers all templates, formulas, and importers.

        Implements:
            Plugin initialization with all components

        Raises:
            Exception: If initialization fails
        """
        # Register templates (5 total)
        self.register_template("stress_analysis", StressAnalysisTemplate)
        self.register_template("material_properties", MaterialPropertiesTemplate)
        self.register_template("assembly_instructions", AssemblyInstructionsTemplate)
        self.register_template("tolerance_stackup", ToleranceStackupTemplate)
        self.register_template("manufacturing_specs", ManufacturingSpecsTemplate)

        # Register stress/strain formulas (3 total)
        self.register_formula("STRESS", StressFormula)
        self.register_formula("STRAIN", StrainFormula)
        self.register_formula("YOUNGS_MODULUS", YoungsModulusFormula)

        # Register moment formulas (3 total)
        self.register_formula("MOMENT_OF_INERTIA", MomentOfInertiaFormula)
        self.register_formula("BENDING_STRESS", BendingStressFormula)
        self.register_formula("TORSIONAL_STRESS", TorsionalStressFormula)

        # Register thermal formulas (2 total)
        self.register_formula("THERMAL_EXPANSION", ThermalExpansionFormula)
        self.register_formula("THERMAL_STRESS", ThermalStressFormula)

        # Register fatigue formulas (3 total)
        self.register_formula("FATIGUE_LIFE", FatigueLifeFormula)
        self.register_formula("SAFETY_FACTOR", SafetyFactorFormula)
        self.register_formula("STRESS_CONCENTRATION", StressConcentrationFormula)

        # Register importers (3 total)
        self.register_importer("cad_metadata", CADMetadataImporter)
        self.register_importer("fea_results", FEAResultsImporter)
        self.register_importer("material_db", MaterialDatabaseImporter)

    def cleanup(self) -> None:
        """Cleanup plugin resources.

        No resources need explicit cleanup for this plugin.

        Implements:
            Plugin cleanup method
        """
        # No cleanup needed for this plugin
        pass

    def validate(self) -> bool:
        """Validate plugin configuration.

        Returns:
            True if plugin has required templates and formulas registered

        Implements:
            Plugin validation
        """
        # Verify we have all required components
        required_templates = 5
        required_formulas = 11  # 3 stress/strain + 3 moment + 2 thermal + 3 fatigue
        required_importers = 3

        return (
            len(self._templates) >= required_templates
            and len(self._formulas) >= required_formulas
            and len(self._importers) >= required_importers
        )


__all__ = [
    "MechanicalEngineeringDomainPlugin",
]
