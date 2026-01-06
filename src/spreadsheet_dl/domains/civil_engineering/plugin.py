"""Civil Engineering Domain Plugin for SpreadsheetDL.

Implements:
    Civil Engineering domain plugin
    PHASE-C: Domain plugin implementations

Provides civil engineering-specific functionality including:
- Beam, soil, concrete, and load formulas
- Survey data, structural results, and building code importers
"""

from __future__ import annotations

from spreadsheet_dl.domains.base import BaseDomainPlugin, PluginMetadata

# Import formulas
from spreadsheet_dl.domains.civil_engineering.formulas.beam import (
    BeamDeflectionFormula,
    MomentFormula,
    ShearStressFormula,
)
from spreadsheet_dl.domains.civil_engineering.formulas.concrete import (
    ConcreteStrengthFormula,
    CrackWidthFormula,
    ReinforcementRatioFormula,
)
from spreadsheet_dl.domains.civil_engineering.formulas.loads import (
    DeadLoadFormula,
    LiveLoadFormula,
    SeismicLoadFormula,
    WindLoadFormula,
)
from spreadsheet_dl.domains.civil_engineering.formulas.soil import (
    BearingCapacityFormula,
    SettlementFormula,
    SoilPressureFormula,
)

# Import importers
from spreadsheet_dl.domains.civil_engineering.importers.building_codes import (
    BuildingCodesImporter,
)
from spreadsheet_dl.domains.civil_engineering.importers.structural_results import (
    StructuralResultsImporter,
)
from spreadsheet_dl.domains.civil_engineering.importers.survey_data import (
    SurveyDataImporter,
)


class CivilEngineeringDomainPlugin(BaseDomainPlugin):
    """Civil Engineering domain plugin.

    Implements:
        Complete Civil Engineering domain plugin
        PHASE-C: Domain plugin implementations

    Provides comprehensive civil engineering functionality for SpreadsheetDL
    with formulas and importers tailored for structural design and construction.

    Formulas (13 total):
        Beam (3):
        - BEAM_DEFLECTION: Beam deflection calculation
        - SHEAR_STRESS: Shear stress calculation
        - MOMENT: Bending moment calculation

        Soil (3):
        - BEARING_CAPACITY: Bearing capacity
        - SETTLEMENT: Settlement calculation
        - SOIL_PRESSURE: Soil pressure

        Concrete (3):
        - CONCRETE_STRENGTH: Concrete strength
        - REINFORCEMENT_RATIO: Reinforcement ratio
        - CRACK_WIDTH: Crack width calculation

        Loads (4):
        - DEAD_LOAD: Dead load calculation
        - LIVE_LOAD: Live load calculation
        - WIND_LOAD: Wind load calculation
        - SEISMIC_LOAD: Seismic load calculation

    Importers:
        - SurveyDataImporter: Survey data files
        - StructuralResultsImporter: Structural analysis results
        - BuildingCodesImporter: Building code tables

    Example:
        >>> plugin = CivilEngineeringDomainPlugin()
        >>> plugin.initialize()
        >>> formulas = plugin.list_formulas()
    """

    @property
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata.

        Returns:
            PluginMetadata with civil engineering plugin information

        Implements:
            Plugin metadata requirements
        """
        return PluginMetadata(
            name="civil_engineering",
            version="4.0.0",
            description="Civil engineering formulas and importers for structural design and construction",
            author="SpreadsheetDL Team",
            license="MIT",
            homepage="https://github.com/lair-click-bats/spreadsheet-dl",
            tags=(
                "civil-engineering",
                "structural",
                "construction",
                "loads",
                "concrete",
                "survey",
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
        # Register beam formulas (3 total)
        self.register_formula("BEAM_DEFLECTION", BeamDeflectionFormula)
        self.register_formula("SHEAR_STRESS", ShearStressFormula)
        self.register_formula("MOMENT", MomentFormula)

        # Register soil formulas (3 total)
        self.register_formula("BEARING_CAPACITY", BearingCapacityFormula)
        self.register_formula("SETTLEMENT", SettlementFormula)
        self.register_formula("SOIL_PRESSURE", SoilPressureFormula)

        # Register concrete formulas (3 total)
        self.register_formula("CONCRETE_STRENGTH", ConcreteStrengthFormula)
        self.register_formula("REINFORCEMENT_RATIO", ReinforcementRatioFormula)
        self.register_formula("CRACK_WIDTH", CrackWidthFormula)

        # Register load formulas (4 total)
        self.register_formula("DEAD_LOAD", DeadLoadFormula)
        self.register_formula("LIVE_LOAD", LiveLoadFormula)
        self.register_formula("WIND_LOAD", WindLoadFormula)
        self.register_formula("SEISMIC_LOAD", SeismicLoadFormula)

        # Register importers (3 total)
        self.register_importer("survey_data", SurveyDataImporter)
        self.register_importer("structural_results", StructuralResultsImporter)
        self.register_importer("building_codes", BuildingCodesImporter)

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
        required_formulas = 12  # 3 beam + 3 soil + 3 concrete + 3 loads (minimum)
        required_importers = 3

        return (
            len(self._formulas) >= required_formulas
            and len(self._importers) >= required_importers
        )


__all__ = [
    "CivilEngineeringDomainPlugin",
]
