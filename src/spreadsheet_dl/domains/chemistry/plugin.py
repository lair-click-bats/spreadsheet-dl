"""Chemistry Domain Plugin for SpreadsheetDL.

    Chemistry domain plugin
    BATCH-4: Chemistry domain creation

Provides chemistry-specific functionality including:
- Thermodynamics, solutions, and kinetics formulas
"""

from __future__ import annotations

from spreadsheet_dl.domains.base import BaseDomainPlugin, PluginMetadata

# Import formulas - Kinetics (5 formulas)
from spreadsheet_dl.domains.chemistry.formulas.kinetics import (
    ActivationEnergyFormula,
    HalfLifeFirstOrderFormula,
    HalfLifeSecondOrderFormula,
    IntegratedRateLawFormula,
    RateConstantFormula,
)

# Import formulas - Solutions (7 formulas)
from spreadsheet_dl.domains.chemistry.formulas.solutions import (
    BufferCapacityFormula,
    MolalityFormula,
    MolarityFormula,
    MoleFractionFormula,
    OsmoticPressureFormula,
    RaoultsLawFormula,
    pHCalculationFormula,
)

# Import formulas - Thermodynamics (8 formulas)
from spreadsheet_dl.domains.chemistry.formulas.thermodynamics import (
    ClausiusClapeyronFormula,
    EnthalpyChangeFormula,
    EntropyChangeFormula,
    EquilibriumConstantFormula,
    GibbsFreeEnergyFormula,
    IdealGasLawFormula,
    RealGasVanDerWaalsFormula,
    VantHoffEquationFormula,
)


class ChemistryDomainPlugin(BaseDomainPlugin):
    """Chemistry domain plugin.

        Complete Chemistry domain plugin
        BATCH-4: Chemistry domain creation

    Provides comprehensive chemistry functionality for SpreadsheetDL
    with formulas for thermodynamics, solutions, and kinetics.

    Formulas (20 total):
        Thermodynamics (8):
        - GIBBS_FREE_ENERGY: Gibbs free energy change
        - ENTHALPY_CHANGE: Enthalpy change for reaction
        - ENTROPY_CHANGE: Entropy change for reaction
        - EQUILIBRIUM_CONSTANT: Equilibrium constant from Gibbs
        - VANT_HOFF_EQUATION: Temperature dependence of K
        - CLAUSIUS_CLAPEYRON: Vapor pressure
        - IDEAL_GAS_LAW: PV=nRT
        - REAL_GAS_VAN_DER_WAALS: Van der Waals equation

        Solutions (7):
        - MOLARITY: Moles per liter
        - MOLALITY: Moles per kg solvent
        - MOLE_FRACTION: Component ratio
        - RAOULTS_LAW: Vapor pressure lowering
        - OSMOTIC_PRESSURE: Colligative property
        - PH_CALCULATION: pH from H+ concentration
        - BUFFER_CAPACITY: Buffer capacity

        Kinetics (5):
        - RATE_CONSTANT: Arrhenius equation
        - HALF_LIFE_FIRST_ORDER: First-order half-life
        - HALF_LIFE_SECOND_ORDER: Second-order half-life
        - INTEGRATED_RATE_LAW: Concentration vs time
        - ACTIVATION_ENERGY: Activation energy from rate constants

    Example:
        >>> plugin = ChemistryDomainPlugin()
        >>> plugin.initialize()
        >>> formulas = plugin.list_formulas()
    """

    @property
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata.

        Returns:
            PluginMetadata with chemistry plugin information

            Plugin metadata requirements
            BATCH-4: Chemistry domain metadata
        """
        return PluginMetadata(
            name="chemistry",
            version="1.0.0",
            description=(
                "Chemistry formulas for thermodynamics, solutions, and kinetics"
            ),
            author="SpreadsheetDL",
            license="MIT",
            tags=("chemistry", "thermodynamics", "kinetics", "solutions"),
            min_spreadsheet_dl_version="4.0.0",
        )

    def initialize(self) -> None:
        """Initialize plugin resources.

        Registers all formulas.

            Plugin initialization with all components
            BATCH-4: Chemistry domain initialization

        Raises:
            Exception: If initialization fails
        """
        # Register thermodynamics formulas (8 total)
        self.register_formula("GIBBS_FREE_ENERGY", GibbsFreeEnergyFormula)
        self.register_formula("ENTHALPY_CHANGE", EnthalpyChangeFormula)
        self.register_formula("ENTROPY_CHANGE", EntropyChangeFormula)
        self.register_formula("EQUILIBRIUM_CONSTANT", EquilibriumConstantFormula)
        self.register_formula("VANT_HOFF_EQUATION", VantHoffEquationFormula)
        self.register_formula("CLAUSIUS_CLAPEYRON", ClausiusClapeyronFormula)
        self.register_formula("IDEAL_GAS_LAW", IdealGasLawFormula)
        self.register_formula("REAL_GAS_VAN_DER_WAALS", RealGasVanDerWaalsFormula)

        # Register solutions formulas (7 total)
        self.register_formula("MOLARITY", MolarityFormula)
        self.register_formula("MOLALITY", MolalityFormula)
        self.register_formula("MOLE_FRACTION", MoleFractionFormula)
        self.register_formula("RAOULTS_LAW", RaoultsLawFormula)
        self.register_formula("OSMOTIC_PRESSURE", OsmoticPressureFormula)
        self.register_formula("PH_CALCULATION", pHCalculationFormula)
        self.register_formula("BUFFER_CAPACITY", BufferCapacityFormula)

        # Register kinetics formulas (5 total)
        self.register_formula("RATE_CONSTANT", RateConstantFormula)
        self.register_formula("HALF_LIFE_FIRST_ORDER", HalfLifeFirstOrderFormula)
        self.register_formula("HALF_LIFE_SECOND_ORDER", HalfLifeSecondOrderFormula)
        self.register_formula("INTEGRATED_RATE_LAW", IntegratedRateLawFormula)
        self.register_formula("ACTIVATION_ENERGY", ActivationEnergyFormula)

    def cleanup(self) -> None:
        """Cleanup plugin resources.

        No resources need explicit cleanup for this plugin.

            Plugin cleanup method
            BATCH-4: Chemistry domain cleanup
        """
        # No cleanup needed for this plugin
        pass

    def validate(self) -> bool:
        """Validate plugin configuration.

        Returns:
            True if plugin has required formulas registered

            Plugin validation
            BATCH-4: Chemistry domain validation
        """
        # Verify we have all required components
        required_formulas = 20  # 8 thermodynamics + 7 solutions + 5 kinetics

        return len(self._formulas) >= required_formulas


__all__ = [
    "ChemistryDomainPlugin",
]
