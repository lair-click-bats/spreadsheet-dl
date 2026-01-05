"""
Environmental Domain Plugin for SpreadsheetDL.

Implements:
    Environmental domain plugin
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
# Formulas - Air Quality
from spreadsheet_dl.domains.environmental.formulas.air_quality import (
    AQICalculationFormula,
    EmissionRateFormula,
    PollutionIndexFormula,
)

# Formulas - Carbon
from spreadsheet_dl.domains.environmental.formulas.carbon import (
    CarbonEquivalentFormula,
    EcologicalFootprintFormula,
    EnvironmentalImpactScoreFormula,
    SustainabilityScoreFormula,
)

# Formulas - Ecology
from spreadsheet_dl.domains.environmental.formulas.ecology import (
    ShannonDiversityFormula,
    SimpsonIndexFormula,
    SpeciesRichnessFormula,
)

# Formulas - Water Quality
from spreadsheet_dl.domains.environmental.formulas.water_quality import (
    BODCalculationFormula,
    WaterQualityIndexFormula,
)

# Importers
from spreadsheet_dl.domains.environmental.importers import (
    LabResultsImporter,
    SatelliteDataImporter,
    SensorNetworkImporter,
)
from spreadsheet_dl.domains.environmental.plugin import EnvironmentalDomainPlugin

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
    # Formulas - Air Quality
    "AQICalculationFormula",
    # Templates
    "AirQualityMonitoringTemplate",
    # Formulas - Water Quality
    "BODCalculationFormula",
    "BiodiversityAssessmentTemplate",
    # Formulas - Carbon
    "CarbonEquivalentFormula",
    "CarbonFootprintTemplate",
    "EcologicalFootprintFormula",
    "EmissionRateFormula",
    # Plugin
    "EnvironmentalDomainPlugin",
    "EnvironmentalImpactScoreFormula",
    "EnvironmentalImpactTemplate",
    # Importers
    "LabResultsImporter",
    "PollutionIndexFormula",
    "SatelliteDataImporter",
    "SensorNetworkImporter",
    # Formulas - Ecology
    "ShannonDiversityFormula",
    "SimpsonIndexFormula",
    "SpeciesRichnessFormula",
    "SustainabilityScoreFormula",
    "WaterQualityAnalysisTemplate",
    "WaterQualityIndexFormula",
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
