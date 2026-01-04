"""
Environmental Domain Plugin for SpreadsheetDL.

Implements:
    TASK-C008: Environmental domain plugin
    PHASE-C: Domain plugin implementations

Provides environmental science-specific functionality including:
- Air quality monitoring templates
- Water quality analysis templates
- Carbon footprint tracking
- Biodiversity assessment
- Environmental impact assessment
- Pollution and sustainability formulas
- Sensor network and satellite data importers
"""

from __future__ import annotations

from spreadsheet_dl.domains.base import BaseDomainPlugin, PluginMetadata

# Import formulas
from spreadsheet_dl.domains.environmental.formulas.air_quality import (
    AQICalculationFormula,
    EmissionRateFormula,
    PollutionIndexFormula,
)
from spreadsheet_dl.domains.environmental.formulas.carbon import (
    CarbonEquivalentFormula,
    EcologicalFootprintFormula,
    EnvironmentalImpactScoreFormula,
    SustainabilityScoreFormula,
)
from spreadsheet_dl.domains.environmental.formulas.ecology import (
    ShannonDiversityFormula,
    SimpsonIndexFormula,
    SpeciesRichnessFormula,
)
from spreadsheet_dl.domains.environmental.formulas.water_quality import (
    BODCalculationFormula,
    WaterQualityIndexFormula,
)

# Import importers
from spreadsheet_dl.domains.environmental.importers.lab_results import (
    LabResultsImporter,
)
from spreadsheet_dl.domains.environmental.importers.satellite_data import (
    SatelliteDataImporter,
)
from spreadsheet_dl.domains.environmental.importers.sensor_network import (
    SensorNetworkImporter,
)

# Import templates
from spreadsheet_dl.domains.environmental.templates.air_quality_monitoring import (
    AirQualityMonitoringTemplate,
)
from spreadsheet_dl.domains.environmental.templates.biodiversity_assessment import (
    BiodiversityAssessmentTemplate,
)
from spreadsheet_dl.domains.environmental.templates.carbon_footprint import (
    CarbonFootprintTemplate,
)
from spreadsheet_dl.domains.environmental.templates.environmental_impact import (
    EnvironmentalImpactTemplate,
)
from spreadsheet_dl.domains.environmental.templates.water_quality_analysis import (
    WaterQualityAnalysisTemplate,
)


class EnvironmentalDomainPlugin(BaseDomainPlugin):
    """
    Environmental domain plugin.

    Implements:
        TASK-C008: Complete Environmental domain plugin
        PHASE-C: Domain plugin implementations

    Provides comprehensive environmental science functionality for SpreadsheetDL
    with templates, formulas, and importers tailored for environmental monitoring,
    assessment, and sustainability tracking.

    Templates:
        - AirQualityMonitoringTemplate: Air pollutant monitoring
        - WaterQualityAnalysisTemplate: Water quality parameters
        - CarbonFootprintTemplate: Carbon emissions tracking
        - BiodiversityAssessmentTemplate: Species diversity assessment
        - EnvironmentalImpactTemplate: Environmental impact assessment

    Formulas (12 total):
        Air Quality (3):
        - AQI_CALCULATION: Air Quality Index
        - EMISSION_RATE: Pollutant emission rate
        - POLLUTION_INDEX: Pollution severity index

        Water Quality (2):
        - WATER_QUALITY_INDEX: WQI calculation
        - BOD_CALCULATION: Biochemical oxygen demand

        Ecology (3):
        - SHANNON_DIVERSITY: Shannon diversity index
        - SIMPSON_INDEX: Simpson's diversity index
        - SPECIES_RICHNESS: Species count

        Carbon/Sustainability (4):
        - CARBON_EQUIVALENT: CO2 equivalent
        - ECOLOGICAL_FOOTPRINT: Ecological footprint
        - SUSTAINABILITY_SCORE: Sustainability metric
        - ENVIRONMENTAL_IMPACT_SCORE: Impact assessment

    Importers:
        - SensorNetworkImporter: IoT sensor data
        - LabResultsImporter: Laboratory analysis results
        - SatelliteDataImporter: Remote sensing data

    Example:
        >>> plugin = EnvironmentalDomainPlugin()
        >>> plugin.initialize()
        >>> template_class = plugin.get_template("air_quality_monitoring")
        >>> template = template_class(station_name="Station A")
        >>> builder = template.generate()
        >>> builder.save("air_quality.ods")
    """

    @property
    def metadata(self) -> PluginMetadata:
        """
        Get plugin metadata.

        Returns:
            PluginMetadata with environmental plugin information

        Implements:
            TASK-C008: Plugin metadata requirements
        """
        return PluginMetadata(
            name="environmental",
            version="4.0.0",
            description=("Environmental monitoring templates, formulas, and importers"),
            author="SpreadsheetDL Team",
            license="MIT",
            homepage="https://github.com/spreadsheet-dl/spreadsheet-dl",
            tags=(
                "environmental",
                "monitoring",
                "sustainability",
                "ecology",
                "pollution",
            ),
            min_spreadsheet_dl_version="4.0.0",
        )

    def initialize(self) -> None:
        """
        Initialize plugin resources.

        Registers all templates, formulas, and importers.

        Implements:
            TASK-C008: Plugin initialization with all components

        Raises:
            Exception: If initialization fails
        """
        # Register templates (5 total)
        self.register_template("air_quality_monitoring", AirQualityMonitoringTemplate)
        self.register_template("water_quality_analysis", WaterQualityAnalysisTemplate)
        self.register_template("carbon_footprint", CarbonFootprintTemplate)
        self.register_template(
            "biodiversity_assessment", BiodiversityAssessmentTemplate
        )
        self.register_template("environmental_impact", EnvironmentalImpactTemplate)

        # Register air quality formulas (3)
        self.register_formula("AQI_CALCULATION", AQICalculationFormula)
        self.register_formula("EMISSION_RATE", EmissionRateFormula)
        self.register_formula("POLLUTION_INDEX", PollutionIndexFormula)

        # Register water quality formulas (2)
        self.register_formula("WATER_QUALITY_INDEX", WaterQualityIndexFormula)
        self.register_formula("BOD_CALCULATION", BODCalculationFormula)

        # Register ecology formulas (3)
        self.register_formula("SHANNON_DIVERSITY", ShannonDiversityFormula)
        self.register_formula("SIMPSON_INDEX", SimpsonIndexFormula)
        self.register_formula("SPECIES_RICHNESS", SpeciesRichnessFormula)

        # Register carbon/sustainability formulas (4)
        self.register_formula("CARBON_EQUIVALENT", CarbonEquivalentFormula)
        self.register_formula("ECOLOGICAL_FOOTPRINT", EcologicalFootprintFormula)
        self.register_formula("SUSTAINABILITY_SCORE", SustainabilityScoreFormula)
        self.register_formula(
            "ENVIRONMENTAL_IMPACT_SCORE", EnvironmentalImpactScoreFormula
        )

        # Register importers (3 total)
        self.register_importer("sensor_network", SensorNetworkImporter)
        self.register_importer("lab_results", LabResultsImporter)
        self.register_importer("satellite_data", SatelliteDataImporter)

    def cleanup(self) -> None:
        """
        Cleanup plugin resources.

        No resources need explicit cleanup for this plugin.

        Implements:
            TASK-C008: Plugin cleanup method
        """
        # No cleanup needed for this plugin
        pass

    def validate(self) -> bool:
        """
        Validate plugin configuration.

        Returns:
            True if plugin has required templates and formulas registered

        Implements:
            TASK-C008: Plugin validation
        """
        # Verify we have all required components
        required_templates = 5
        required_formulas = 12  # 3 air + 2 water + 3 ecology + 4 carbon
        required_importers = 3

        return (
            len(self._templates) >= required_templates
            and len(self._formulas) >= required_formulas
            and len(self._importers) >= required_importers
        )


__all__ = [
    "EnvironmentalDomainPlugin",
]
