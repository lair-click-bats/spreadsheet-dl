"""Environmental domain formulas.

Implements:
    Environmental domain formula extensions

Provides 12 specialized formulas for environmental science:
- Air quality (AQI, emission rate, pollution index)
- Water quality (WQI, BOD)
- Ecology (Shannon diversity, Simpson index, species richness)
- Carbon/Sustainability (CO2 equivalent, footprint, impact score)
"""

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
from spreadsheet_dl.domains.environmental.formulas.lifecycle import (
    AcidificationPotential,
    EutrophicationPotential,
    GlobalWarmingPotential,
)
from spreadsheet_dl.domains.environmental.formulas.water_quality import (
    BODCalculationFormula,
    WaterQualityIndexFormula,
)

__all__ = [
    # Air Quality
    "AQICalculationFormula",
    "AcidificationPotential",
    # Water Quality
    "BODCalculationFormula",
    # Carbon/Sustainability
    "CarbonEquivalentFormula",
    "EcologicalFootprintFormula",
    "EmissionRateFormula",
    "EnvironmentalImpactScoreFormula",
    "EutrophicationPotential",
    "GlobalWarmingPotential",
    "PollutionIndexFormula",
    # Ecology
    "ShannonDiversityFormula",
    "SimpsonIndexFormula",
    "SpeciesRichnessFormula",
    "SustainabilityScoreFormula",
    "WaterQualityIndexFormula",
]
