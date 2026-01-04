"""
Environmental domain templates.

Implements:
    TASK-C008: Environmental domain templates

Provides 5 specialized templates:
- AirQualityMonitoringTemplate: Air pollutant monitoring
- WaterQualityAnalysisTemplate: Water quality parameters
- CarbonFootprintTemplate: Carbon emissions tracking
- BiodiversityAssessmentTemplate: Species diversity assessment
- EnvironmentalImpactTemplate: Environmental impact assessment
"""

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

__all__ = [
    "AirQualityMonitoringTemplate",
    "BiodiversityAssessmentTemplate",
    "CarbonFootprintTemplate",
    "EnvironmentalImpactTemplate",
    "WaterQualityAnalysisTemplate",
]
