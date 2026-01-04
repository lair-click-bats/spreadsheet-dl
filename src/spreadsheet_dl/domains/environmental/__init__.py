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
- Pollution index and emissions calculations
- Water quality metrics (BOD, WQI)
- Ecological diversity indices (Shannon, Simpson)
- Sustainability scoring formulas
- Sensor network, lab results, and satellite data importers

Example:
    >>> from spreadsheet_dl.domains.environmental import EnvironmentalDomainPlugin
    >>> plugin = EnvironmentalDomainPlugin()
    >>> plugin.initialize()
    >>> # Use templates
    >>> from spreadsheet_dl.domains.environmental import AirQualityMonitoringTemplate
    >>> template = AirQualityMonitoringTemplate(station_name="Downtown Station")
    >>> builder = template.generate()
    >>> builder.save("air_quality.ods")
"""

# Plugin
from spreadsheet_dl.domains.environmental.plugin import EnvironmentalDomainPlugin

# Formulas - Air Quality
from spreadsheet_dl.domains.environmental.formulas.air_quality import (
    AQICalculationFormula,
    EmissionRateFormula,
    PollutionIndexFormula,
)

# Formulas - Water Quality
from spreadsheet_dl.domains.environmental.formulas.water_quality import (
    BODCalculationFormula,
    WaterQualityIndexFormula,
)

# Formulas - Ecology
from spreadsheet_dl.domains.environmental.formulas.ecology import (
    ShannonDiversityFormula,
    SimpsonIndexFormula,
    SpeciesRichnessFormula,
)

# Formulas - Carbon
from spreadsheet_dl.domains.environmental.formulas.carbon import (
    CarbonEquivalentFormula,
    EcologicalFootprintFormula,
    EnvironmentalImpactScoreFormula,
    SustainabilityScoreFormula,
)

# Importers
from spreadsheet_dl.domains.environmental.importers import (
    LabResultsImporter,
    SatelliteDataImporter,
    SensorNetworkImporter,
)

# Templates
from spreadsheet_dl.domains.environmental.templates import (
    AirQualityMonitoringTemplate,
    BiodiversityAssessmentTemplate,
    CarbonFootprintTemplate,
    EnvironmentalImpactTemplate,
    WaterQualityAnalysisTemplate,
)

# Utils
from spreadsheet_dl.domains.environmental.utils import (
    calculate_aqi,
    calculate_bod,
    calculate_carbon_equivalent,
    calculate_ecological_footprint,
    calculate_shannon_diversity,
    calculate_simpson_index,
    calculate_wqi,
    format_concentration,
    ppm_to_ugm3,
    ugm3_to_ppm,
)

__all__ = [
    # Plugin
    "EnvironmentalDomainPlugin",
    # Templates
    "AirQualityMonitoringTemplate",
    "BiodiversityAssessmentTemplate",
    "CarbonFootprintTemplate",
    "EnvironmentalImpactTemplate",
    "WaterQualityAnalysisTemplate",
    # Formulas - Air Quality
    "AQICalculationFormula",
    "EmissionRateFormula",
    "PollutionIndexFormula",
    # Formulas - Water Quality
    "BODCalculationFormula",
    "WaterQualityIndexFormula",
    # Formulas - Ecology
    "ShannonDiversityFormula",
    "SimpsonIndexFormula",
    "SpeciesRichnessFormula",
    # Formulas - Carbon
    "CarbonEquivalentFormula",
    "EcologicalFootprintFormula",
    "EnvironmentalImpactScoreFormula",
    "SustainabilityScoreFormula",
    # Importers
    "LabResultsImporter",
    "SatelliteDataImporter",
    "SensorNetworkImporter",
    # Utils
    "calculate_aqi",
    "calculate_bod",
    "calculate_carbon_equivalent",
    "calculate_ecological_footprint",
    "calculate_shannon_diversity",
    "calculate_simpson_index",
    "calculate_wqi",
    "format_concentration",
    "ppm_to_ugm3",
    "ugm3_to_ppm",
]
