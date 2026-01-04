"""
Biology Domain Plugin for SpreadsheetDL.

Implements:
    TASK-C006: Biology domain plugin
    PHASE-C: Domain plugin implementations

Provides biology-specific functionality including:
- Lab experiment protocols and plate reader data templates
- Gene expression and sequencing results templates
- Molecular biology, biochemistry, and ecology formulas
- FASTA, GenBank, and plate reader importers
"""

from __future__ import annotations

from spreadsheet_dl.domains.base import BaseDomainPlugin, PluginMetadata

# Import formulas
from spreadsheet_dl.domains.biology.formulas.biochemistry import (
    BradfordAssayFormula,
    DilutionFactorFormula,
    EnzymeActivityFormula,
    MichaelisMentenFormula,
)
from spreadsheet_dl.domains.biology.formulas.ecology import (
    PopulationGrowthFormula,
    ShannonDiversityFormula,
    SimpsonIndexFormula,
    SpeciesRichnessFormula,
)
from spreadsheet_dl.domains.biology.formulas.molecular import (
    ConcentrationFormula,
    FoldChangeFormula,
    GCContentFormula,
    MeltingTempFormula,
)

# Import importers
from spreadsheet_dl.domains.biology.importers.fasta import FASTAImporter
from spreadsheet_dl.domains.biology.importers.genbank import GenBankImporter
from spreadsheet_dl.domains.biology.importers.plate_reader import PlateReaderImporter

# Import templates
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


class BiologyDomainPlugin(BaseDomainPlugin):
    """
    Biology domain plugin.

    Implements:
        TASK-C006: Complete Biology domain plugin
        PHASE-C: Domain plugin implementations

    Provides comprehensive biology functionality for SpreadsheetDL
    with templates, formulas, and importers tailored for research workflows.

    Templates:
        - ExperimentProtocolTemplate: Lab experiment protocols
        - PlateReaderDataTemplate: Microplate reader data
        - GeneExpressionTemplate: Gene expression analysis (qPCR)
        - EcologyFieldDataTemplate: Field observations and diversity
        - SequencingResultsTemplate: DNA/RNA sequencing results

    Formulas (12 total):
        Molecular Biology (4):
        - CONCENTRATION: Nucleic acid concentration
        - FOLD_CHANGE: Gene expression fold change
        - GC_CONTENT: GC content percentage
        - MELTING_TEMP: DNA melting temperature

        Biochemistry (4):
        - BRADFORD_ASSAY: Protein concentration
        - ENZYME_ACTIVITY: Enzyme specific activity
        - MICHAELIS_MENTEN: Michaelis-Menten kinetics
        - DILUTION_FACTOR: Serial dilution calculations

        Ecology (4):
        - SHANNON_DIVERSITY: Shannon diversity index
        - SIMPSON_INDEX: Simpson's diversity index
        - SPECIES_RICHNESS: Species richness
        - POPULATION_GROWTH: Population growth rate

    Importers:
        - PlateReaderImporter: Plate reader data (CSV/XML)
        - FASTAImporter: FASTA sequence files
        - GenBankImporter: GenBank sequence files

    Example:
        >>> plugin = BiologyDomainPlugin()
        >>> plugin.initialize()
        >>> template_class = plugin.get_template("experiment_protocol")
        >>> template = template_class()
        >>> builder = template.generate()
        >>> builder.save("protocol.ods")
    """

    @property
    def metadata(self) -> PluginMetadata:
        """
        Get plugin metadata.

        Returns:
            PluginMetadata with biology plugin information

        Implements:
            TASK-C006: Plugin metadata requirements
        """
        return PluginMetadata(
            name="biology",
            version="4.0.0",
            description=(
                "Biology templates, formulas, and importers for research and analysis"
            ),
            author="SpreadsheetDL Team",
            license="MIT",
            homepage="https://github.com/spreadsheet-dl/spreadsheet-dl",
            tags=("biology", "research", "genetics", "ecology", "lab-notebook"),
            min_spreadsheet_dl_version="4.0.0",
        )

    def initialize(self) -> None:
        """
        Initialize plugin resources.

        Registers all templates, formulas, and importers.

        Implements:
            TASK-C006: Plugin initialization with all components

        Raises:
            Exception: If initialization fails
        """
        # Register templates (5 total)
        self.register_template("experiment_protocol", ExperimentProtocolTemplate)
        self.register_template("plate_reader_data", PlateReaderDataTemplate)
        self.register_template("gene_expression", GeneExpressionTemplate)
        self.register_template("ecology_field_data", EcologyFieldDataTemplate)
        self.register_template("sequencing_results", SequencingResultsTemplate)

        # Register molecular biology formulas (4 total)
        self.register_formula("CONCENTRATION", ConcentrationFormula)
        self.register_formula("FOLD_CHANGE", FoldChangeFormula)
        self.register_formula("GC_CONTENT", GCContentFormula)
        self.register_formula("MELTING_TEMP", MeltingTempFormula)

        # Register biochemistry formulas (4 total)
        self.register_formula("BRADFORD_ASSAY", BradfordAssayFormula)
        self.register_formula("ENZYME_ACTIVITY", EnzymeActivityFormula)
        self.register_formula("MICHAELIS_MENTEN", MichaelisMentenFormula)
        self.register_formula("DILUTION_FACTOR", DilutionFactorFormula)

        # Register ecology formulas (4 total)
        self.register_formula("SHANNON_DIVERSITY", ShannonDiversityFormula)
        self.register_formula("SIMPSON_INDEX", SimpsonIndexFormula)
        self.register_formula("SPECIES_RICHNESS", SpeciesRichnessFormula)
        self.register_formula("POPULATION_GROWTH", PopulationGrowthFormula)

        # Register importers (3 total)
        self.register_importer("plate_reader", PlateReaderImporter)
        self.register_importer("fasta", FASTAImporter)
        self.register_importer("genbank", GenBankImporter)

    def cleanup(self) -> None:
        """
        Cleanup plugin resources.

        No resources need explicit cleanup for this plugin.

        Implements:
            TASK-C006: Plugin cleanup method
        """
        # No cleanup needed for this plugin
        pass

    def validate(self) -> bool:
        """
        Validate plugin configuration.

        Returns:
            True if plugin has required templates and formulas registered

        Implements:
            TASK-C006: Plugin validation
        """
        # Verify we have all required components
        required_templates = 5
        required_formulas = 12  # 4 molecular + 4 biochemistry + 4 ecology
        required_importers = 3

        return (
            len(self._templates) >= required_templates
            and len(self._formulas) >= required_formulas
            and len(self._importers) >= required_importers
        )


__all__ = [
    "BiologyDomainPlugin",
]
