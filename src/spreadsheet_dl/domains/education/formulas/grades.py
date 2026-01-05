"""
Grade calculation formulas.

Implements:
    Grade calculation formulas
    (GRADE_AVERAGE, WEIGHTED_GRADE, GRADE_CURVE)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from spreadsheet_dl.domains.base import BaseFormula, FormulaArgument, FormulaMetadata


@dataclass(slots=True, frozen=True)
class GradeAverageFormula(BaseFormula):
    """
    Calculate simple grade average.

    Implements:
        GRADE_AVERAGE formula for grade calculation

    Calculates the arithmetic mean of a range of grades.

    Example:
        >>> formula = GradeAverageFormula()
        >>> result = formula.build("A1:A10")
        >>> # Returns: "AVERAGE(A1:A10)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """
        Get formula metadata.

        Returns:
            FormulaMetadata for GRADE_AVERAGE

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="GRADE_AVERAGE",
            category="education",
            description="Calculate simple grade average from a range",
            arguments=(
                FormulaArgument(
                    "grades_range",
                    "range",
                    required=True,
                    description="Range of grade values",
                ),
                FormulaArgument(
                    "exclude_zeros",
                    "boolean",
                    required=False,
                    description="Exclude zero values from average",
                    default=False,
                ),
            ),
            return_type="number",
            examples=(
                "=GRADE_AVERAGE(B2:B30)",
                "=GRADE_AVERAGE(grades;TRUE)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build GRADE_AVERAGE formula string.

        Args:
            *args: grades_range, [exclude_zeros]
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            GRADE_AVERAGE formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        grades_range = args[0]
        exclude_zeros = args[1] if len(args) > 1 else False

        if exclude_zeros and str(exclude_zeros).upper() in ("TRUE", "1", "YES"):
            # Use AVERAGEIF to exclude zeros
            return f'AVERAGEIF({grades_range};"<>0")'
        else:
            return f"AVERAGE({grades_range})"


@dataclass(slots=True, frozen=True)
class WeightedGradeFormula(BaseFormula):
    """
    Calculate weighted grade average.

    Implements:
        WEIGHTED_GRADE formula for weighted calculations

    Calculates weighted average using grades and corresponding weights.

    Example:
        >>> formula = WeightedGradeFormula()
        >>> result = formula.build("A1:A5", "B1:B5")
        >>> # Returns: "SUMPRODUCT(A1:A5;B1:B5)/SUM(B1:B5)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """
        Get formula metadata.

        Returns:
            FormulaMetadata for WEIGHTED_GRADE

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="WEIGHTED_GRADE",
            category="education",
            description="Calculate weighted grade average",
            arguments=(
                FormulaArgument(
                    "grades_range",
                    "range",
                    required=True,
                    description="Range of grade values",
                ),
                FormulaArgument(
                    "weights_range",
                    "range",
                    required=True,
                    description="Range of weight values (must match grades range)",
                ),
            ),
            return_type="number",
            examples=(
                "=WEIGHTED_GRADE(B2:B10;C2:C10)",
                "=WEIGHTED_GRADE(grades;weights)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build WEIGHTED_GRADE formula string.

        Args:
            *args: grades_range, weights_range
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            WEIGHTED_GRADE formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        grades_range = args[0]
        weights_range = args[1]

        # Weighted average = SUMPRODUCT(grades, weights) / SUM(weights)
        return f"SUMPRODUCT({grades_range};{weights_range})/SUM({weights_range})"


@dataclass(slots=True, frozen=True)
class GradeCurveFormula(BaseFormula):
    """
    Apply grade curve adjustment.

    Implements:
        GRADE_CURVE formula for curve adjustments

    Adjusts grades based on various curving methods.

    Example:
        >>> formula = GradeCurveFormula()
        >>> result = formula.build("A1", "A1:A30", "linear", "10")
        >>> # Returns formula for linear curve adjustment
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """
        Get formula metadata.

        Returns:
            FormulaMetadata for GRADE_CURVE

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="GRADE_CURVE",
            category="education",
            description="Apply grade curve adjustment",
            arguments=(
                FormulaArgument(
                    "grade",
                    "number",
                    required=True,
                    description="Individual grade to curve",
                ),
                FormulaArgument(
                    "all_grades",
                    "range",
                    required=True,
                    description="Range of all grades for curve calculation",
                ),
                FormulaArgument(
                    "method",
                    "text",
                    required=False,
                    description="Curve method: linear, sqrt, or bell",
                    default="linear",
                ),
                FormulaArgument(
                    "adjustment",
                    "number",
                    required=False,
                    description="Adjustment factor (points to add or percentage)",
                    default=0,
                ),
            ),
            return_type="number",
            examples=(
                "=GRADE_CURVE(B2;B$2:B$30;linear;10)",
                "=GRADE_CURVE(grade;all_grades;sqrt)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build GRADE_CURVE formula string.

        Args:
            *args: grade, all_grades, [method], [adjustment]
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            GRADE_CURVE formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        grade = args[0]
        all_grades = args[1]
        method = str(args[2]).lower() if len(args) > 2 else "linear"
        adjustment = args[3] if len(args) > 3 else 0

        if method == "sqrt":
            # Square root curve: scaled to 100
            return f"SQRT({grade})*10"
        elif method == "bell":
            # Bell curve: normalize to mean=75, sd=10
            return f"75+10*({grade}-AVERAGE({all_grades}))/STDEV({all_grades})"
        else:
            # Linear: add fixed points
            return f"MIN({grade}+{adjustment};100)"


__all__ = [
    "GradeAverageFormula",
    "GradeCurveFormula",
    "WeightedGradeFormula",
]
