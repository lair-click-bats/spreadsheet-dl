"""Mechanical Engineering Domain Plugin for SpreadsheetDL.

Implements:
    Mechanical Engineering domain plugin
    PHASE-C: Domain plugin implementations

Provides mechanical engineering-specific functionality including:
- Stress/strain, moment, thermal, and fatigue formulas
- CAD metadata, FEA results, and material database importers
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


class MechanicalEngineeringDomainPlugin(BaseDomainPlugin):
    """Mechanical Engineering domain plugin.

    Implements:
        Complete Mechanical Engineering domain plugin
        PHASE-C: Domain plugin implementations

    Provides comprehensive mechanical engineering functionality for SpreadsheetDL
    with formulas and importers tailored for mechanical design and analysis.

    Formulas (11 total):
        Stress/Strain (3):
        - STRESS: Stress calculation
        - STRAIN: Strain calculation
        - YOUNGS_MODULUS: Young's modulus

        Moment (3):
        - MOMENT_OF_INERTIA: Moment of inertia
        - BENDING_STRESS: Bending stress
        - TORSIONAL_STRESS: Torsional stress

        Thermal (2):
        - THERMAL_EXPANSION: Thermal expansion
        - THERMAL_STRESS: Thermal stress

        Fatigue (3):
        - FATIGUE_LIFE: Fatigue life calculation
        - SAFETY_FACTOR: Safety factor
        - STRESS_CONCENTRATION: Stress concentration factor

    Importers:
        - CADMetadataImporter: CAD file metadata (STEP/IGES)
        - FEAResultsImporter: FEA results data
        - MaterialDatabaseImporter: Material properties database

    Example:
        >>> plugin = MechanicalEngineeringDomainPlugin()
        >>> plugin.initialize()
        >>> formulas = plugin.list_formulas()
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
            description="Mechanical engineering formulas and importers for design and analysis",
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

        Registers all formulas and importers.

        Implements:
            Plugin initialization with all components

        Raises:
            Exception: If initialization fails
        """
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
        pass

    def validate(self) -> bool:
        """Validate plugin configuration.

        Returns:
            True if plugin has required formulas and importers registered

        Implements:
            Plugin validation
        """
        required_formulas = 11  # 3 stress/strain + 3 moment + 2 thermal + 3 fatigue
        required_importers = 3

        return (
            len(self._formulas) >= required_formulas
            and len(self._importers) >= required_importers
        )


__all__ = [
    "MechanicalEngineeringDomainPlugin",
]
