"""
Power calculation formulas for electrical engineering.

Implements:
    TASK-C002: Power formulas (POWER_DISSIPATION, VOLTAGE_DROP, CURRENT_CALC, THERMAL_RESISTANCE)
"""

from __future__ import annotations

from typing import Any

from spreadsheet_dl.domains.base import BaseFormula, FormulaArgument, FormulaMetadata


class PowerDissipationFormula(BaseFormula):
    """
    Power dissipation formula: P = V * I.

    Calculates power dissipation given voltage and current.

    Implements:
        TASK-C002: POWER_DISSIPATION formula

    Example:
        >>> formula = PowerDissipationFormula()
        >>> formula.build("5", "0.1")
        '5*0.1'
        # Result: 0.5 watts
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata."""
        return FormulaMetadata(
            name="POWER_DISSIPATION",
            category="electrical_engineering",
            description="Calculate power dissipation from voltage and current: P = V * I",
            arguments=(
                FormulaArgument(
                    name="voltage",
                    type="number",
                    required=True,
                    description="Voltage in volts (V)",
                ),
                FormulaArgument(
                    name="current",
                    type="number",
                    required=True,
                    description="Current in amperes (A)",
                ),
            ),
            return_type="number",
            examples=(
                "=POWER_DISSIPATION(5, 0.1)  # 0.5 watts",
                "=POWER_DISSIPATION(A2, B2)  # Using cell references",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build ODF formula string.

        Args:
            *args: voltage, current

        Returns:
            ODF formula string: voltage*current
        """
        self.validate_arguments(args)
        voltage, current = args
        return f"{voltage}*{current}"


class VoltageDropFormula(BaseFormula):
    """
    Voltage drop formula: V = I * R * (length/1000).

    Calculates voltage drop in a conductor given current, resistance, and length.

    Implements:
        TASK-C002: VOLTAGE_DROP formula

    Example:
        >>> formula = VoltageDropFormula()
        >>> formula.build("2", "0.05", "1000")
        '2*0.05*(1000/1000)'
        # Result: 0.1 volts
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata."""
        return FormulaMetadata(
            name="VOLTAGE_DROP",
            category="electrical_engineering",
            description="Calculate voltage drop: V = I * R * (length/1000)",
            arguments=(
                FormulaArgument(
                    name="current",
                    type="number",
                    required=True,
                    description="Current in amperes (A)",
                ),
                FormulaArgument(
                    name="resistance",
                    type="number",
                    required=True,
                    description="Resistance per meter (Ω/m)",
                ),
                FormulaArgument(
                    name="length",
                    type="number",
                    required=True,
                    description="Length in millimeters (mm)",
                ),
            ),
            return_type="number",
            examples=(
                "=VOLTAGE_DROP(2, 0.05, 1000)  # 0.1V drop over 1m at 2A",
                "=VOLTAGE_DROP(A2, B2, C2)  # Using cell references",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build ODF formula string.

        Args:
            *args: current, resistance, length

        Returns:
            ODF formula string: current*resistance*(length/1000)
        """
        self.validate_arguments(args)
        current, resistance, length = args
        return f"{current}*{resistance}*({length}/1000)"


class CurrentCalcFormula(BaseFormula):
    """
    Current calculation formula: I = P / V.

    Calculates current given power and voltage.

    Implements:
        TASK-C002: CURRENT_CALC formula

    Example:
        >>> formula = CurrentCalcFormula()
        >>> formula.build("10", "5")
        '10/5'
        # Result: 2 amperes
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata."""
        return FormulaMetadata(
            name="CURRENT_CALC",
            category="electrical_engineering",
            description="Calculate current from power and voltage: I = P / V",
            arguments=(
                FormulaArgument(
                    name="power",
                    type="number",
                    required=True,
                    description="Power in watts (W)",
                ),
                FormulaArgument(
                    name="voltage",
                    type="number",
                    required=True,
                    description="Voltage in volts (V)",
                ),
            ),
            return_type="number",
            examples=(
                "=CURRENT_CALC(10, 5)  # 2 amperes",
                "=CURRENT_CALC(A2, B2)  # Using cell references",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build ODF formula string.

        Args:
            *args: power, voltage

        Returns:
            ODF formula string: power/voltage
        """
        self.validate_arguments(args)
        power, voltage = args
        return f"{power}/{voltage}"


class ThermalResistanceFormula(BaseFormula):
    """
    Thermal resistance formula: θ = ΔT / P.

    Calculates thermal resistance given temperature rise and power.

    Implements:
        TASK-C002: THERMAL_RESISTANCE formula

    Example:
        >>> formula = ThermalResistanceFormula()
        >>> formula.build("50", "10")
        '50/10'
        # Result: 5 °C/W
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata."""
        return FormulaMetadata(
            name="THERMAL_RESISTANCE",
            category="electrical_engineering",
            description="Calculate thermal resistance: θ = ΔT / P",
            arguments=(
                FormulaArgument(
                    name="temp_rise",
                    type="number",
                    required=True,
                    description="Temperature rise in degrees Celsius (°C)",
                ),
                FormulaArgument(
                    name="power",
                    type="number",
                    required=True,
                    description="Power dissipation in watts (W)",
                ),
            ),
            return_type="number",
            examples=(
                "=THERMAL_RESISTANCE(50, 10)  # 5 °C/W",
                "=THERMAL_RESISTANCE(A2, B2)  # Using cell references",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build ODF formula string.

        Args:
            *args: temp_rise, power

        Returns:
            ODF formula string: temp_rise/power
        """
        self.validate_arguments(args)
        temp_rise, power = args
        return f"{temp_rise}/{power}"


__all__ = [
    "CurrentCalcFormula",
    "PowerDissipationFormula",
    "ThermalResistanceFormula",
    "VoltageDropFormula",
]
