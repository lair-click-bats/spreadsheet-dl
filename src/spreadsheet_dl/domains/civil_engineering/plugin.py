"""
Civil Engineering Domain Plugin for SpreadsheetDL.

Implements:
    Civil Engineering domain plugin
    PHASE-C: Domain plugin implementations

Provides civil engineering-specific functionality including:
- Load calculations (dead, live, wind, seismic)
- Material takeoff (concrete, rebar, formwork)
- Structural analysis (forces, reactions, deflections)
- Site survey data management
- Concrete mix design
- Beam, soil, concrete, and load formulas
- Survey data, structural results, and building code importers

Features:
    - 5 professional templates for civil engineering workflows
    - 12 civil engineering formula extensions
    - 3 importers for survey data, analysis results, and code tables
    - Integration with structural analysis software and surveying tools
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

# Import templates
from spreadsheet_dl.domains.civil_engineering.templates.concrete_mix import (
    ConcreteMixTemplate,
)
from spreadsheet_dl.domains.civil_engineering.templates.load_calculations import (
    LoadCalculationsTemplate,
)
from spreadsheet_dl.domains.civil_engineering.templates.material_takeoff import (
    MaterialTakeoffTemplate,
)
from spreadsheet_dl.domains.civil_engineering.templates.site_survey import (
    SiteSurveyTemplate,
)
from spreadsheet_dl.domains.civil_engineering.templates.structural_analysis import (
    StructuralAnalysisTemplate,
)


class CivilEngineeringDomainPlugin(BaseDomainPlugin):
    """
    Civil Engineering domain plugin.

    Implements:
        Complete Civil Engineering domain plugin
        PHASE-C: Domain plugin implementations

    Provides comprehensive civil engineering functionality for SpreadsheetDL
    with templates, formulas, and importers tailored for structural design
    and construction.

    Example:
        >>> plugin = CivilEngineeringDomainPlugin()
        >>> plugin.initialize()
        >>> template_class = plugin.get_template("load_calculations")
        >>> template = template_class(project_name="Bridge Design")
        >>> builder = template.generate()
        >>> builder.save("bridge_loads.ods")
    """

    @property
    def metadata(self) -> PluginMetadata:
        """
        Get plugin metadata.

        Returns:
            PluginMetadata with civil engineering plugin information

        Implements:
            Plugin metadata requirements
        """
        return PluginMetadata(
            name="civil_engineering",
            version="4.0.0",
            description="Civil engineering templates, formulas, and importers for structural design and construction",
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
        """
        Initialize plugin resources.

        Registers all templates, formulas, and importers.

        Implements:
            Plugin initialization with all components

        Raises:
            Exception: If initialization fails
        """
        # Register templates (5 total)
        self.register_template("load_calculations", LoadCalculationsTemplate)
        self.register_template("material_takeoff", MaterialTakeoffTemplate)
        self.register_template("structural_analysis", StructuralAnalysisTemplate)
        self.register_template("site_survey", SiteSurveyTemplate)
        self.register_template("concrete_mix", ConcreteMixTemplate)

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

        # Register load formulas (4 total) - note: total is 13 formulas, exceeding requirement
        self.register_formula("DEAD_LOAD", DeadLoadFormula)
        self.register_formula("LIVE_LOAD", LiveLoadFormula)
        self.register_formula("WIND_LOAD", WindLoadFormula)
        self.register_formula("SEISMIC_LOAD", SeismicLoadFormula)

        # Register importers (3 total)
        self.register_importer("survey_data", SurveyDataImporter)
        self.register_importer("structural_results", StructuralResultsImporter)
        self.register_importer("building_codes", BuildingCodesImporter)

    def cleanup(self) -> None:
        """
        Cleanup plugin resources.

        No resources need explicit cleanup for this plugin.

        Implements:
            Plugin cleanup method
        """
        # No cleanup needed for this plugin
        pass

    def validate(self) -> bool:
        """
        Validate plugin configuration.

        Returns:
            True if plugin has required templates and formulas registered

        Implements:
            Plugin validation
        """
        # Verify we have all required components
        required_templates = 5
        required_formulas = 12  # 3 beam + 3 soil + 3 concrete + 3 loads (minimum)
        required_importers = 3

        return (
            len(self._templates) >= required_templates
            and len(self._formulas) >= required_formulas
            and len(self._importers) >= required_importers
        )


__all__ = [
    "CivilEngineeringDomainPlugin",
]
