"""
Thermal formulas for mechanical engineering.

Implements:
    REQ-C003-009: Thermal formulas (THERMAL_EXPANSION, THERMAL_STRESS)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from spreadsheet_dl.domains.base import BaseFormula, FormulaArgument, FormulaMetadata


@dataclass(slots=True, frozen=True)
class ThermalExpansionFormula(BaseFormula):
    """
    Thermal Expansion formula: ΔL = α × L × ΔT.

    Calculates linear thermal expansion given coefficient of thermal expansion,
    original length, and temperature change.

    Implements:
        REQ-C003-009: THERMAL_EXPANSION formula

    Example:
        >>> formula = ThermalExpansionFormula()
        >>> formula.build("11.7e-6", "1000", "100")
        '11.7e-6*1000*100'
        # Result: 1.17 mm expansion
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata."""
        return FormulaMetadata(
            name="THERMAL_EXPANSION",
            category="mechanical_engineering",
            description="Calculate linear thermal expansion: ΔL = α × L × ΔT",
            arguments=(
                FormulaArgument(
                    name="cte",
                    type="number",
                    required=True,
                    description="Coefficient of thermal expansion (α) in 1/°C",
                ),
                FormulaArgument(
                    name="length",
                    type="number",
                    required=True,
                    description="Original length (L) in mm",
                ),
                FormulaArgument(
                    name="temp_change",
                    type="number",
                    required=True,
                    description="Temperature change (ΔT) in °C",
                ),
            ),
            return_type="number",
            examples=(
                "=THERMAL_EXPANSION(11.7E-6; 1000; 100)  # 1.17 mm",
                "=THERMAL_EXPANSION(A2; B2; C2)  # Using cell references",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build ODF formula string.

        Args:
            *args: cte, length, temp_change

        Returns:
            ODF formula string: cte*length*temp_change
        """
        self.validate_arguments(args)
        cte, length, temp_change = args
        return f"{cte}*{length}*{temp_change}"


@dataclass(slots=True, frozen=True)
class ThermalStressFormula(BaseFormula):
    """
    Thermal Stress formula: σ = E × α × ΔT.

    Calculates thermal stress in a constrained member given Young's modulus,
    coefficient of thermal expansion, and temperature change.

    Implements:
        REQ-C003-009: THERMAL_STRESS formula

    Example:
        >>> formula = ThermalStressFormula()
        >>> formula.build("200000", "11.7e-6", "100")
        '200000*11.7e-6*100'
        # Result: 234 MPa
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata."""
        return FormulaMetadata(
            name="THERMAL_STRESS",
            category="mechanical_engineering",
            description="Calculate thermal stress in constrained member: σ = E × α × ΔT",
            arguments=(
                FormulaArgument(
                    name="youngs_modulus",
                    type="number",
                    required=True,
                    description="Young's modulus (E) in MPa",
                ),
                FormulaArgument(
                    name="cte",
                    type="number",
                    required=True,
                    description="Coefficient of thermal expansion (α) in 1/°C",
                ),
                FormulaArgument(
                    name="temp_change",
                    type="number",
                    required=True,
                    description="Temperature change (ΔT) in °C",
                ),
            ),
            return_type="number",
            examples=(
                "=THERMAL_STRESS(200000; 11.7E-6; 100)  # 234 MPa",
                "=THERMAL_STRESS(A2; B2; C2)  # Using cell references",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build ODF formula string.

        Args:
            *args: youngs_modulus, cte, temp_change

        Returns:
            ODF formula string: youngs_modulus*cte*temp_change
        """
        self.validate_arguments(args)
        youngs_modulus, cte, temp_change = args
        return f"{youngs_modulus}*{cte}*{temp_change}"


__all__ = [
    "ThermalExpansionFormula",
    "ThermalStressFormula",
]
