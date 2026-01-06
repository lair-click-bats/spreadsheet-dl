"""Educational assessment and psychometric formulas.

Implements:
    Education formulas for test analysis and reliability
    (ItemDifficulty, ItemDiscrimination, CronbachAlpha)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from spreadsheet_dl.domains.base import BaseFormula, FormulaArgument, FormulaMetadata


@dataclass(slots=True, frozen=True)
class ItemDifficulty(BaseFormula):
    """Calculate test item difficulty index.

    Implements:
        Item difficulty calculation (proportion correct)

    Example:
        >>> formula = ItemDifficulty()
        >>> result = formula.build("25", "30")
        >>> # Returns: "25/30"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for ItemDifficulty

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="ITEM_DIFFICULTY",
            category="assessment",
            description="Calculate item difficulty index (p-value)",
            arguments=(
                FormulaArgument(
                    "correct_responses",
                    "number",
                    required=True,
                    description="Number of correct responses",
                ),
                FormulaArgument(
                    "total_responses",
                    "number",
                    required=True,
                    description="Total number of responses",
                ),
            ),
            return_type="number",
            examples=(
                "=ITEM_DIFFICULTY(25;30)",
                "=ITEM_DIFFICULTY(A1;A2)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build ItemDifficulty formula string.

        Args:
            *args: correct_responses, total_responses
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            ItemDifficulty formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        correct_responses = args[0]
        total_responses = args[1]

        # p = Correct / Total
        return f"{correct_responses}/{total_responses}"


@dataclass(slots=True, frozen=True)
class ItemDiscrimination(BaseFormula):
    """Calculate item discrimination power.

    Implements:
        Item discrimination index (upper-lower difference)

    Example:
        >>> formula = ItemDiscrimination()
        >>> result = formula.build("0.80", "0.40")
        >>> # Returns: "0.80-0.40"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for ItemDiscrimination

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="ITEM_DISCRIMINATION",
            category="assessment",
            description="Calculate item discrimination index (D)",
            arguments=(
                FormulaArgument(
                    "upper_group_p",
                    "number",
                    required=True,
                    description="Proportion correct in upper group",
                ),
                FormulaArgument(
                    "lower_group_p",
                    "number",
                    required=True,
                    description="Proportion correct in lower group",
                ),
            ),
            return_type="number",
            examples=(
                "=ITEM_DISCRIMINATION(0.80;0.40)",
                "=ITEM_DISCRIMINATION(A1;A2)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build ItemDiscrimination formula string.

        Args:
            *args: upper_group_p, lower_group_p
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            ItemDiscrimination formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        upper_group_p = args[0]
        lower_group_p = args[1]

        # D = PU - PL
        return f"{upper_group_p}-{lower_group_p}"


@dataclass(slots=True, frozen=True)
class CronbachAlpha(BaseFormula):
    """Calculate Cronbach's alpha reliability coefficient.

    Implements:
        Cronbach's alpha for test reliability

    Example:
        >>> formula = CronbachAlpha()
        >>> result = formula.build("10", "25", "100")
        >>> # Returns: "of:=(10/(10-1))*(1-25/100)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for CronbachAlpha

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="CRONBACH_ALPHA",
            category="assessment",
            description="Calculate Cronbach's alpha reliability coefficient",
            arguments=(
                FormulaArgument(
                    "k",
                    "number",
                    required=True,
                    description="Number of items",
                ),
                FormulaArgument(
                    "sum_item_variance",
                    "number",
                    required=True,
                    description="Sum of item variances",
                ),
                FormulaArgument(
                    "total_variance",
                    "number",
                    required=True,
                    description="Total test variance",
                ),
            ),
            return_type="number",
            examples=(
                "=CRONBACH_ALPHA(10;25;100)",
                "=CRONBACH_ALPHA(A1;A2;A3)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build CronbachAlpha formula string.

        Args:
            *args: k, sum_item_variance, total_variance
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            CronbachAlpha formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        k = args[0]
        sum_item_variance = args[1]
        total_variance = args[2]

        # alpha = (k/(k-1)) * (1 - (sum_variance/total_variance))
        return f"of:=({k}/({k}-1))*(1-{sum_item_variance}/{total_variance})"
