"""Biology Domain Plugin for SpreadsheetDL.

Implements:
    Biology domain plugin
    PHASE-C: Domain plugin implementations

Provides biology-specific functionality including:
- Lab experiment protocols and plate reader data templates
- Gene expression and sequencing results templates
- Molecular biology and biochemistry formulas
- FASTA, GenBank, and plate reader importers
- Ecology statistics and population growth calculations

Features:
    - 5 professional templates for research workflows
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

# Templates
from spreadsheet_dl.domains.biology.templates.ecology_field_data import (
    EcologyFieldDataTemplate,
)
from spreadsheet_dl.domains.biology.templates.experiment_protocol import (
    ExperimentProtocolTemplate,
)
from spreadsheet_dl.domains.biology.templates.gene_expression import (
    GeneExpressionTemplate,
)
from spreadsheet_dl.domains.biology.templates.plate_reader_data import (
    PlateReaderDataTemplate,
)
from spreadsheet_dl.domains.biology.templates.sequencing_results import (
    SequencingResultsTemplate,
)

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
    # Templates
    "EcologyFieldDataTemplate",
    "EnzymeActivityFormula",
    "ExperimentProtocolTemplate",
    # Importers
    "FASTAImporter",
    "FoldChangeFormula",
    "GCContentFormula",
    "GenBankImporter",
    "GeneExpressionTemplate",
    "MeltingTempFormula",
    "MichaelisMentenFormula",
    "PlateReaderDataTemplate",
    "PlateReaderImporter",
    # Formulas - Ecology
    "PopulationGrowthFormula",
    "SequencingResultsTemplate",
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
