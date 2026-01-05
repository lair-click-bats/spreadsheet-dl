"""Machine learning metrics formulas.

Implements:
    ML metrics formulas (ACCURACY, PRECISION, RECALL, F1SCORE, CONFUSION_MATRIX_METRIC)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from spreadsheet_dl.domains.base import BaseFormula, FormulaArgument, FormulaMetadata


@dataclass(slots=True, frozen=True)
class AccuracyFormula(BaseFormula):
    """Accuracy metric: (TP+TN)/(TP+TN+FP+FN).

    Implements:
        ACCURACY formula for ML evaluation

    Example:
        >>> formula = AccuracyFormula()
        >>> result = formula.build(85, 90, 10, 15)
        >>> # Returns: "(85+90)/(85+90+10+15)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for ACCURACY

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="ACCURACY",
            category="ml_metrics",
            description="Calculate classification accuracy from confusion matrix values",
            arguments=(
                FormulaArgument(
                    "tp",
                    "number",
                    required=True,
                    description="True Positives count or cell reference",
                ),
                FormulaArgument(
                    "tn",
                    "number",
                    required=True,
                    description="True Negatives count or cell reference",
                ),
                FormulaArgument(
                    "fp",
                    "number",
                    required=True,
                    description="False Positives count or cell reference",
                ),
                FormulaArgument(
                    "fn",
                    "number",
                    required=True,
                    description="False Negatives count or cell reference",
                ),
            ),
            return_type="number",
            examples=(
                "=ACCURACY(A1;A2;A3;A4)",
                "=(85+90)/(85+90+10+15)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build ACCURACY formula string.

        Args:
            *args: tp, tn, fp, fn
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            ACCURACY formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        tp, tn, fp, fn = args

        # Formula: (TP+TN)/(TP+TN+FP+FN)
        return f"({tp}+{tn})/({tp}+{tn}+{fp}+{fn})"


@dataclass(slots=True, frozen=True)
class PrecisionFormula(BaseFormula):
    """Precision metric: TP/(TP+FP).

    Implements:
        PRECISION formula for ML evaluation

    Example:
        >>> formula = PrecisionFormula()
        >>> result = formula.build(85, 10)
        >>> # Returns: "85/(85+10)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for PRECISION

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="PRECISION",
            category="ml_metrics",
            description="Calculate precision from true/false positives",
            arguments=(
                FormulaArgument(
                    "tp",
                    "number",
                    required=True,
                    description="True Positives count or cell reference",
                ),
                FormulaArgument(
                    "fp",
                    "number",
                    required=True,
                    description="False Positives count or cell reference",
                ),
            ),
            return_type="number",
            examples=(
                "=PRECISION(A1;A2)",
                "=85/(85+10)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build PRECISION formula string.

        Args:
            *args: tp, fp
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            PRECISION formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        tp, fp = args

        # Formula: TP/(TP+FP)
        return f"{tp}/({tp}+{fp})"


@dataclass(slots=True, frozen=True)
class RecallFormula(BaseFormula):
    """Recall metric: TP/(TP+FN).

    Implements:
        RECALL formula for ML evaluation

    Example:
        >>> formula = RecallFormula()
        >>> result = formula.build(85, 15)
        >>> # Returns: "85/(85+15)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for RECALL

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="RECALL",
            category="ml_metrics",
            description="Calculate recall from true positives and false negatives",
            arguments=(
                FormulaArgument(
                    "tp",
                    "number",
                    required=True,
                    description="True Positives count or cell reference",
                ),
                FormulaArgument(
                    "fn",
                    "number",
                    required=True,
                    description="False Negatives count or cell reference",
                ),
            ),
            return_type="number",
            examples=(
                "=RECALL(A1;A2)",
                "=85/(85+15)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build RECALL formula string.

        Args:
            *args: tp, fn
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            RECALL formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        tp, fn = args

        # Formula: TP/(TP+FN)
        return f"{tp}/({tp}+{fn})"


@dataclass(slots=True, frozen=True)
class F1ScoreFormula(BaseFormula):
    """F1 Score metric: 2*(Precision*Recall)/(Precision+Recall).

    Implements:
        F1SCORE formula for ML evaluation

    Example:
        >>> formula = F1ScoreFormula()
        >>> result = formula.build("A1", "A2")
        >>> # Returns: "2*(A1*A2)/(A1+A2)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for F1SCORE

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="F1SCORE",
            category="ml_metrics",
            description="Calculate F1 score from precision and recall",
            arguments=(
                FormulaArgument(
                    "precision",
                    "number",
                    required=True,
                    description="Precision value or cell reference",
                ),
                FormulaArgument(
                    "recall",
                    "number",
                    required=True,
                    description="Recall value or cell reference",
                ),
            ),
            return_type="number",
            examples=(
                "=F1SCORE(A1;A2)",
                "=2*(0.9*0.85)/(0.9+0.85)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build F1SCORE formula string.

        Args:
            *args: precision, recall
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            F1SCORE formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        precision, recall = args

        # Formula: 2*(P*R)/(P+R)
        return f"2*({precision}*{recall})/({precision}+{recall})"


@dataclass(slots=True, frozen=True)
class ConfusionMatrixMetricFormula(BaseFormula):
    """Extract metrics from confusion matrix.

    Implements:
        CONFUSION_MATRIX_METRIC formula for metric extraction

    Example:
        >>> formula = ConfusionMatrixMetricFormula()
        >>> result = formula.build("A1:B2", "accuracy")
        >>> # Returns formula to extract accuracy from confusion matrix
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for CONFUSION_MATRIX_METRIC

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="CONFUSION_MATRIX_METRIC",
            category="ml_metrics",
            description="Extract metric from confusion matrix",
            arguments=(
                FormulaArgument(
                    "matrix",
                    "range",
                    required=True,
                    description="Confusion matrix range (2x2)",
                ),
                FormulaArgument(
                    "metric_name",
                    "text",
                    required=True,
                    description="Metric to extract: accuracy, precision, recall, f1",
                ),
            ),
            return_type="number",
            examples=(
                '=CONFUSION_MATRIX_METRIC(A1:B2;"accuracy")',
                '=CONFUSION_MATRIX_METRIC(A1:B2;"precision")',
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build CONFUSION_MATRIX_METRIC formula string.

        Args:
            *args: matrix, metric_name
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            CONFUSION_MATRIX_METRIC formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        matrix = args[0]
        metric_name = str(args[1]).strip('"').lower()

        # Extract cell references from matrix (assumes A1:B2 format)
        # For a 2x2 confusion matrix:
        # [TP  FN]
        # [FP  TN]

        # This is a simplified version - assumes matrix range like "A1:B2"
        if ":" in str(matrix):
            # Parse range to get individual cells
            # For now, use INDEX to extract values
            tp = f"INDEX({matrix};1;1)"
            fn = f"INDEX({matrix};1;2)"
            fp = f"INDEX({matrix};2;1)"
            tn = f"INDEX({matrix};2;2)"

            if metric_name == "accuracy":
                return f"({tp}+{tn})/({tp}+{tn}+{fp}+{fn})"
            elif metric_name == "precision":
                return f"{tp}/({tp}+{fp})"
            elif metric_name == "recall":
                return f"{tp}/({tp}+{fn})"
            elif metric_name == "f1":
                precision = f"{tp}/({tp}+{fp})"
                recall = f"{tp}/({tp}+{fn})"
                return f"2*({precision})*({recall})/(({precision})+({recall}))"
            else:
                msg = f"Unknown metric: {metric_name}. Use: accuracy, precision, recall, or f1"
                raise ValueError(msg)
        else:
            msg = "Matrix must be a range reference (e.g., A1:B2)"
            raise ValueError(msg)


__all__ = [
    "AccuracyFormula",
    "ConfusionMatrixMetricFormula",
    "F1ScoreFormula",
    "PrecisionFormula",
    "RecallFormula",
]
