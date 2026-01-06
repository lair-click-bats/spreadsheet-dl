"""Physics Domain Plugin for SpreadsheetDL.

Implements:
    Physics domain plugin
    BATCH-5: Physics domain creation

Provides physics-specific functionality including:
- Classical mechanics, electromagnetism, optics, and quantum mechanics formulas
"""

from __future__ import annotations

from spreadsheet_dl.domains.base import BaseDomainPlugin, PluginMetadata

# Import formulas - Electromagnetism (6 formulas)
from spreadsheet_dl.domains.physics.formulas.electromagnetism import (
    CoulombLawFormula,
    ElectricFieldFormula,
    FaradayLawFormula,
    LorentzForceFormula,
    MagneticForceFormula,
    PoyntingVectorFormula,
)

# Import formulas - Mechanics (7 formulas)
from spreadsheet_dl.domains.physics.formulas.mechanics import (
    AngularMomentumFormula,
    CentripetalForceFormula,
    KineticEnergyFormula,
    MomentumFormula,
    NewtonSecondLawFormula,
    PotentialEnergyFormula,
    WorkEnergyFormula,
)

# Import formulas - Optics (6 formulas)
from spreadsheet_dl.domains.physics.formulas.optics import (
    BraggLawFormula,
    DiffractionGratingFormula,
    LensMakerEquationFormula,
    MagnificationLensFormula,
    SnellsLawFormula,
    ThinFilmInterferenceFormula,
)

# Import formulas - Quantum (6 formulas)
from spreadsheet_dl.domains.physics.formulas.quantum import (
    BohrRadiusFormula,
    DeBroglieWavelengthFormula,
    HeisenbergUncertaintyFormula,
    PhotoelectricEffectFormula,
    PlanckEnergyFormula,
    RydbergFormulaFormula,
)


class PhysicsDomainPlugin(BaseDomainPlugin):
    """Physics domain plugin.

    Implements:
        Complete Physics domain plugin
        BATCH-5: Physics domain creation

    Provides comprehensive physics functionality for SpreadsheetDL
    with formulas for mechanics, electromagnetism, optics, and quantum mechanics.

    Formulas (25 total):
        Classical Mechanics (7):
        - NEWTON_SECOND_LAW: F = ma
        - KINETIC_ENERGY: KE = 0.5*m*v²
        - POTENTIAL_ENERGY: PE = mgh
        - WORK_ENERGY: W = F*d*cos(θ)
        - MOMENTUM: p = mv
        - ANGULAR_MOMENTUM: L = Iω
        - CENTRIPETAL_FORCE: Fc = mv²/r

        Electromagnetism (6):
        - COULOMB_LAW: F = k*q1*q2/r²
        - ELECTRIC_FIELD: E = F/q
        - MAGNETIC_FORCE: F = qvB*sin(θ)
        - FARADAY_LAW: EMF = N*ΔΦ/Δt
        - LORENTZ_FORCE: F = q*(E + v*B)
        - POYNTING_VECTOR: S = E*H

        Optics (6):
        - SNELLS_LAW: n1*sin(θ1) = n2*sin(θ2)
        - LENS_MAKER_EQUATION: 1/f = (n-1)*(1/R1 - 1/R2)
        - MAGNIFICATION_LENS: M = -di/do
        - BRAGG_LAW: nλ = 2d*sin(θ)
        - THIN_FILM_INTERFERENCE: 2nt*cos(θ) = mλ
        - DIFFRACTION_GRATING: d*sin(θ) = mλ

        Quantum Mechanics (6):
        - PLANCK_ENERGY: E = hf
        - DE_BROGLIE_WAVELENGTH: λ = h/p
        - HEISENBERG_UNCERTAINTY: Δx*Δp ≥ ℏ/2
        - PHOTOELECTRIC_EFFECT: KE = hf - W
        - BOHR_RADIUS: r_n = n²*a₀
        - RYDBERG_FORMULA: 1/λ = R*(1/n₁² - 1/n₂²)

    Example:
        >>> plugin = PhysicsDomainPlugin()
        >>> plugin.initialize()
        >>> formulas = plugin.list_formulas()
    """

    @property
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata.

        Returns:
            PluginMetadata with physics plugin information

        Implements:
            Plugin metadata requirements
            BATCH-5: Physics domain metadata
        """
        return PluginMetadata(
            name="physics",
            version="1.0.0",
            description=(
                "Physics formulas for mechanics, electromagnetism, optics, "
                "and quantum mechanics"
            ),
            author="SpreadsheetDL",
            license="MIT",
            tags=("physics", "mechanics", "electromagnetism", "optics", "quantum"),
            min_spreadsheet_dl_version="4.0.0",
        )

    def initialize(self) -> None:
        """Initialize plugin resources.

        Registers all formulas.

        Implements:
            Plugin initialization with all components
            BATCH-5: Physics domain initialization

        Raises:
            Exception: If initialization fails
        """
        # Register mechanics formulas (7 total)
        self.register_formula("NEWTON_SECOND_LAW", NewtonSecondLawFormula)
        self.register_formula("KINETIC_ENERGY", KineticEnergyFormula)
        self.register_formula("POTENTIAL_ENERGY", PotentialEnergyFormula)
        self.register_formula("WORK_ENERGY", WorkEnergyFormula)
        self.register_formula("MOMENTUM", MomentumFormula)
        self.register_formula("ANGULAR_MOMENTUM", AngularMomentumFormula)
        self.register_formula("CENTRIPETAL_FORCE", CentripetalForceFormula)

        # Register electromagnetism formulas (6 total)
        self.register_formula("COULOMB_LAW", CoulombLawFormula)
        self.register_formula("ELECTRIC_FIELD", ElectricFieldFormula)
        self.register_formula("MAGNETIC_FORCE", MagneticForceFormula)
        self.register_formula("FARADAY_LAW", FaradayLawFormula)
        self.register_formula("LORENTZ_FORCE", LorentzForceFormula)
        self.register_formula("POYNTING_VECTOR", PoyntingVectorFormula)

        # Register optics formulas (6 total)
        self.register_formula("SNELLS_LAW", SnellsLawFormula)
        self.register_formula("LENS_MAKER_EQUATION", LensMakerEquationFormula)
        self.register_formula("MAGNIFICATION_LENS", MagnificationLensFormula)
        self.register_formula("BRAGG_LAW", BraggLawFormula)
        self.register_formula("THIN_FILM_INTERFERENCE", ThinFilmInterferenceFormula)
        self.register_formula("DIFFRACTION_GRATING", DiffractionGratingFormula)

        # Register quantum formulas (6 total)
        self.register_formula("PLANCK_ENERGY", PlanckEnergyFormula)
        self.register_formula("DE_BROGLIE_WAVELENGTH", DeBroglieWavelengthFormula)
        self.register_formula("HEISENBERG_UNCERTAINTY", HeisenbergUncertaintyFormula)
        self.register_formula("PHOTOELECTRIC_EFFECT", PhotoelectricEffectFormula)
        self.register_formula("BOHR_RADIUS", BohrRadiusFormula)
        self.register_formula("RYDBERG_FORMULA", RydbergFormulaFormula)

    def cleanup(self) -> None:
        """Cleanup plugin resources.

        No resources need explicit cleanup for this plugin.

        Implements:
            Plugin cleanup method
            BATCH-5: Physics domain cleanup
        """
        # No cleanup needed for this plugin
        pass

    def validate(self) -> bool:
        """Validate plugin configuration.

        Returns:
            True if plugin has required formulas registered

        Implements:
            Plugin validation
            BATCH-5: Physics domain validation
        """
        # Verify we have all required components
        required_formulas = 25  # 7 mechanics + 6 EM + 6 optics + 6 quantum

        return len(self._formulas) >= required_formulas


__all__ = [
    "PhysicsDomainPlugin",
]
