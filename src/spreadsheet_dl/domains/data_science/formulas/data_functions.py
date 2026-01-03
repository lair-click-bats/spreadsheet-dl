"""
Data function formulas (wrappers around ODF built-ins).

Implements:
    TASK-C001: Data function formulas (AVERAGE, MEDIAN, STDEV, VARIANCE, CORRELATION)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from spreadsheet_dl.domains.base import BaseFormula, FormulaArgument, FormulaMetadata


@dataclass(slots=True, frozen=True)
class AverageFormula(BaseFormula):
    """
    Average (mean) calculation using ODF AVERAGE function.

    Implements:
        TASK-C001: DS_AVERAGE formula wrapper

    Example:
        >>> formula = AverageFormula()
        >>> result = formula.build("A1:A10")
        >>> # Returns: "AVERAGE(A1:A10)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """
        Get formula metadata.

        Returns:
            FormulaMetadata for DS_AVERAGE

        Implements:
            TASK-C001: Formula metadata
        """
        return FormulaMetadata(
            name="DS_AVERAGE",
            category="data_functions",
            description="Calculate arithmetic mean of a dataset",
            arguments=(
                FormulaArgument(
                    "range",
                    "range",
                    required=True,
                    description="Data range or array",
                ),
            ),
            return_type="number",
            examples=(
                "=AVERAGE(A1:A10)",
                "=AVERAGE(data_range)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build AVERAGE formula string.

        Args:
            *args: range
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            TASK-C001: DS_AVERAGE formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        data_range = args[0]
        return f"AVERAGE({data_range})"


@dataclass(slots=True, frozen=True)
class MedianFormula(BaseFormula):
    """
    Median calculation using ODF MEDIAN function.

    Implements:
        TASK-C001: DS_MEDIAN formula wrapper

    Example:
        >>> formula = MedianFormula()
        >>> result = formula.build("A1:A10")
        >>> # Returns: "MEDIAN(A1:A10)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """
        Get formula metadata.

        Returns:
            FormulaMetadata for DS_MEDIAN

        Implements:
            TASK-C001: Formula metadata
        """
        return FormulaMetadata(
            name="DS_MEDIAN",
            category="data_functions",
            description="Calculate median of a dataset",
            arguments=(
                FormulaArgument(
                    "range",
                    "range",
                    required=True,
                    description="Data range or array",
                ),
            ),
            return_type="number",
            examples=(
                "=MEDIAN(A1:A10)",
                "=MEDIAN(data_range)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build MEDIAN formula string.

        Args:
            *args: range
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            TASK-C001: DS_MEDIAN formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        data_range = args[0]
        return f"MEDIAN({data_range})"


@dataclass(slots=True, frozen=True)
class StdevFormula(BaseFormula):
    """
    Standard deviation calculation using ODF STDEV function.

    Implements:
        TASK-C001: DS_STDEV formula wrapper

    Example:
        >>> formula = StdevFormula()
        >>> result = formula.build("A1:A10")
        >>> # Returns: "STDEV(A1:A10)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """
        Get formula metadata.

        Returns:
            FormulaMetadata for DS_STDEV

        Implements:
            TASK-C001: Formula metadata
        """
        return FormulaMetadata(
            name="DS_STDEV",
            category="data_functions",
            description="Calculate sample standard deviation",
            arguments=(
                FormulaArgument(
                    "range",
                    "range",
                    required=True,
                    description="Data range or array",
                ),
            ),
            return_type="number",
            examples=(
                "=STDEV(A1:A10)",
                "=STDEV(data_range)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build STDEV formula string.

        Args:
            *args: range
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            TASK-C001: DS_STDEV formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        data_range = args[0]
        return f"STDEV({data_range})"


@dataclass(slots=True, frozen=True)
class VarianceFormula(BaseFormula):
    """
    Variance calculation using ODF VAR function.

    Implements:
        TASK-C001: DS_VARIANCE formula wrapper

    Example:
        >>> formula = VarianceFormula()
        >>> result = formula.build("A1:A10")
        >>> # Returns: "VAR(A1:A10)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """
        Get formula metadata.

        Returns:
            FormulaMetadata for DS_VARIANCE

        Implements:
            TASK-C001: Formula metadata
        """
        return FormulaMetadata(
            name="DS_VARIANCE",
            category="data_functions",
            description="Calculate sample variance",
            arguments=(
                FormulaArgument(
                    "range",
                    "range",
                    required=True,
                    description="Data range or array",
                ),
            ),
            return_type="number",
            examples=(
                "=VAR(A1:A10)",
                "=VAR(data_range)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build VAR formula string.

        Args:
            *args: range
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            TASK-C001: DS_VARIANCE formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        data_range = args[0]
        return f"VAR({data_range})"


@dataclass(slots=True, frozen=True)
class CorrelationFormula(BaseFormula):
    """
    Correlation calculation using ODF CORREL function.

    Implements:
        TASK-C001: DS_CORRELATION formula wrapper

    Example:
        >>> formula = CorrelationFormula()
        >>> result = formula.build("A1:A10", "B1:B10")
        >>> # Returns: "CORREL(A1:A10;B1:B10)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """
        Get formula metadata.

        Returns:
            FormulaMetadata for DS_CORRELATION

        Implements:
            TASK-C001: Formula metadata
        """
        return FormulaMetadata(
            name="DS_CORRELATION",
            category="data_functions",
            description="Calculate Pearson correlation coefficient between two datasets",
            arguments=(
                FormulaArgument(
                    "array1",
                    "range",
                    required=True,
                    description="First data array or range",
                ),
                FormulaArgument(
                    "array2",
                    "range",
                    required=True,
                    description="Second data array or range",
                ),
            ),
            return_type="number",
            examples=(
                "=CORREL(A1:A10;B1:B10)",
                "=CORREL(x_values;y_values)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """
        Build CORREL formula string.

        Args:
            *args: array1, array2
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            TASK-C001: DS_CORRELATION formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        array1, array2 = args
        return f"CORREL({array1};{array2})"


__all__ = [
    "AverageFormula",
    "CorrelationFormula",
    "MedianFormula",
    "StdevFormula",
    "VarianceFormula",
]
