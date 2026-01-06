"""Biology Domain Plugin for SpreadsheetDL.

Implements:
    Biology domain plugin
    PHASE-C: Domain plugin implementations

Provides biology-specific functionality including:
- Molecular biology and biochemistry formulas
- FASTA, GenBank, and plate reader importers
- Ecology statistics and population growth calculations

Features:
    - 12 specialized formulas for biology calculations
    - 3 importers for biological data formats
    - Integration with lab instruments and sequence databases
"""

from __future__ import annotations

# Formulas - Biochemistry
from spreadsheet_dl.domains.biology.formulas.biochemistry import (
    BradfordAssayFormula,
    DilutionFactorFormula,
    EnzymeActivityFormula,
    MichaelisMentenFormula,
)

# Formulas - Ecology
from spreadsheet_dl.domains.biology.formulas.ecology import (
    PopulationGrowthFormula,
    ShannonDiversityFormula,
    SimpsonIndexFormula,
    SpeciesRichnessFormula,
)

# Formulas - Molecular Biology
from spreadsheet_dl.domains.biology.formulas.molecular import (
    ConcentrationFormula,
    FoldChangeFormula,
    GCContentFormula,
    MeltingTempFormula,
)

# Importers
from spreadsheet_dl.domains.biology.importers.fasta import FASTAImporter
from spreadsheet_dl.domains.biology.importers.genbank import GenBankImporter
from spreadsheet_dl.domains.biology.importers.plate_reader import PlateReaderImporter

# Plugin
from spreadsheet_dl.domains.biology.plugin import BiologyDomainPlugin

# Utils
from spreadsheet_dl.domains.biology.utils import (
    calculate_dilution,
    calculate_gc_content,
    calculate_melting_temp,
    calculate_od_to_concentration,
    complement_dna,
    format_scientific_notation,
    is_valid_dna,
    is_valid_rna,
    normalize_sequence,
    reverse_complement,
)

__all__ = [
    # Plugin
    "BiologyDomainPlugin",
    # Formulas - Biochemistry
    "BradfordAssayFormula",
    # Formulas - Molecular Biology
    "ConcentrationFormula",
    "DilutionFactorFormula",
    "EnzymeActivityFormula",
    # Importers
    "FASTAImporter",
    "FoldChangeFormula",
    "GCContentFormula",
    "GenBankImporter",
    "MeltingTempFormula",
    "MichaelisMentenFormula",
    "PlateReaderImporter",
    # Formulas - Ecology
    "PopulationGrowthFormula",
    "ShannonDiversityFormula",
    "SimpsonIndexFormula",
    "SpeciesRichnessFormula",
    # Utils
    "calculate_dilution",
    "calculate_gc_content",
    "calculate_melting_temp",
    "calculate_od_to_concentration",
    "complement_dna",
    "format_scientific_notation",
    "is_valid_dna",
    "is_valid_rna",
    "normalize_sequence",
    "reverse_complement",
]
