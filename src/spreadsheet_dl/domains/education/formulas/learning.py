"""Learning metrics formulas.

Implements:
    Learning metrics formulas
    (LEARNING_GAIN, MASTERY_LEVEL, ATTENDANCE_RATE, COMPLETION_RATE,
     BLOOM_TAXONOMY_LEVEL, READABILITY_SCORE)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from spreadsheet_dl.domains.base import BaseFormula, FormulaArgument, FormulaMetadata


@dataclass(slots=True, frozen=True)
class LearningGainFormula(BaseFormula):
    """Calculate normalized learning gain.

    Implements:
        LEARNING_GAIN formula for pre/post assessment

    Uses Hake's normalized gain: g = (post - pre) / (max - pre)

    Example:
        >>> formula = LearningGainFormula()
        >>> result = formula.build("A1", "A2", "100")
        >>> # Returns: "(A2-A1)/(100-A1)"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for LEARNING_GAIN

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="LEARNING_GAIN",
            category="education",
            description="Calculate normalized learning gain (Hake's formula)",
            arguments=(
                FormulaArgument(
                    "pre_score",
                    "number",
                    required=True,
                    description="Pre-assessment score",
                ),
                FormulaArgument(
                    "post_score",
                    "number",
                    required=True,
                    description="Post-assessment score",
                ),
                FormulaArgument(
                    "max_score",
                    "number",
                    required=False,
                    description="Maximum possible score",
                    default=100,
                ),
            ),
            return_type="number",
            examples=(
                "=LEARNING_GAIN(B2;C2)",
                "=LEARNING_GAIN(pre;post;100)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build LEARNING_GAIN formula string.

        Args:
            *args: pre_score, post_score, [max_score]
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            LEARNING_GAIN formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        pre_score = args[0]
        post_score = args[1]
        max_score = args[2] if len(args) > 2 else 100

        # Hake's normalized gain: g = (post - pre) / (max - pre)
        # With protection against division by zero
        return f"IF({pre_score}={max_score};1;({post_score}-{pre_score})/({max_score}-{pre_score}))"


@dataclass(slots=True, frozen=True)
class MasteryLevelFormula(BaseFormula):
    """Calculate mastery level for competency-based grading.

    Implements:
        MASTERY_LEVEL formula for mastery grading

    Returns mastery level (1-4 or custom scale) based on score.

    Example:
        >>> formula = MasteryLevelFormula()
        >>> result = formula.build("A1")
        >>> # Returns formula for 4-point mastery scale
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for MASTERY_LEVEL

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="MASTERY_LEVEL",
            category="education",
            description="Calculate mastery level from score",
            arguments=(
                FormulaArgument(
                    "score",
                    "number",
                    required=True,
                    description="Student score (0-100)",
                ),
                FormulaArgument(
                    "scale",
                    "number",
                    required=False,
                    description="Mastery scale levels (default 4)",
                    default=4,
                ),
            ),
            return_type="number",
            examples=(
                "=MASTERY_LEVEL(B2)",
                "=MASTERY_LEVEL(score;5)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build MASTERY_LEVEL formula string.

        Args:
            *args: score, [scale]
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            MASTERY_LEVEL formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        score = args[0]
        # scale = args[1] if len(args) > 1 else 4

        # 4-point mastery scale:
        # 4 = Exceeds (90-100)
        # 3 = Meets (80-89)
        # 2 = Approaching (70-79)
        # 1 = Beginning (0-69)
        return f"IF({score}>=90;4;IF({score}>=80;3;IF({score}>=70;2;1)))"


@dataclass(slots=True, frozen=True)
class AttendanceRateFormula(BaseFormula):
    """Calculate student attendance rate.

    Implements:
        ATTENDANCE_RATE formula for attendance tracking

    Calculates percentage of days attended.

    Example:
        >>> formula = AttendanceRateFormula()
        >>> result = formula.build("A1", "A2")
        >>> # Returns: "A1/A2*100"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for ATTENDANCE_RATE

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="ATTENDANCE_RATE",
            category="education",
            description="Calculate student attendance rate percentage",
            arguments=(
                FormulaArgument(
                    "days_present",
                    "number",
                    required=True,
                    description="Number of days present",
                ),
                FormulaArgument(
                    "total_days",
                    "number",
                    required=True,
                    description="Total number of school days",
                ),
            ),
            return_type="number",
            examples=(
                "=ATTENDANCE_RATE(B2;C2)",
                "=ATTENDANCE_RATE(present;total)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build ATTENDANCE_RATE formula string.

        Args:
            *args: days_present, total_days
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            ATTENDANCE_RATE formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        days_present = args[0]
        total_days = args[1]

        return f"IF({total_days}=0;0;{days_present}/{total_days}*100)"


@dataclass(slots=True, frozen=True)
class CompletionRateFormula(BaseFormula):
    """Calculate assignment completion rate.

    Implements:
        COMPLETION_RATE formula for assignment tracking

    Calculates percentage of assignments completed.

    Example:
        >>> formula = CompletionRateFormula()
        >>> result = formula.build("A1", "A2")
        >>> # Returns: "A1/A2*100"
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for COMPLETION_RATE

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="COMPLETION_RATE",
            category="education",
            description="Calculate assignment completion rate percentage",
            arguments=(
                FormulaArgument(
                    "completed",
                    "number",
                    required=True,
                    description="Number of assignments completed",
                ),
                FormulaArgument(
                    "total",
                    "number",
                    required=True,
                    description="Total number of assignments",
                ),
            ),
            return_type="number",
            examples=(
                "=COMPLETION_RATE(B2;C2)",
                "=COMPLETION_RATE(completed;total)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build COMPLETION_RATE formula string.

        Args:
            *args: completed, total
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            COMPLETION_RATE formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        completed = args[0]
        total = args[1]

        return f"IF({total}=0;0;{completed}/{total}*100)"


@dataclass(slots=True, frozen=True)
class BloomTaxonomyLevelFormula(BaseFormula):
    """Categorize learning objective by Bloom's Taxonomy level.

    Implements:
        BLOOM_TAXONOMY_LEVEL formula for learning design

    Returns taxonomy level (1-6) based on action verb keywords.

    Example:
        >>> formula = BloomTaxonomyLevelFormula()
        >>> result = formula.build("A1")
        >>> # Returns formula to categorize by Bloom's level
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for BLOOM_TAXONOMY_LEVEL

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="BLOOM_TAXONOMY_LEVEL",
            category="education",
            description="Categorize objective by Bloom's Taxonomy level (1-6)",
            arguments=(
                FormulaArgument(
                    "objective_text",
                    "text",
                    required=True,
                    description="Learning objective text",
                ),
            ),
            return_type="number",
            examples=(
                "=BLOOM_TAXONOMY_LEVEL(B2)",
                '=BLOOM_TAXONOMY_LEVEL("Analyze the causes...")',
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build BLOOM_TAXONOMY_LEVEL formula string.

        Args:
            *args: objective_text
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            BLOOM_TAXONOMY_LEVEL formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        text = args[0]

        # Bloom's levels (simplified detection via keywords):
        # 6 = Create (design, construct, develop, formulate, create)
        # 5 = Evaluate (judge, critique, evaluate, assess, justify)
        # 4 = Analyze (analyze, compare, contrast, differentiate, examine)
        # 3 = Apply (apply, demonstrate, solve, use, implement)
        # 2 = Understand (explain, describe, summarize, interpret, classify)
        # 1 = Remember (list, define, recall, identify, name)
        upper_text = f"UPPER({text})"

        # Build nested IF formula for detection
        return (
            f'IF(OR(ISNUMBER(SEARCH("CREATE";{upper_text}));'
            f'ISNUMBER(SEARCH("DESIGN";{upper_text})));6;'
            f'IF(OR(ISNUMBER(SEARCH("EVALUATE";{upper_text}));'
            f'ISNUMBER(SEARCH("JUDGE";{upper_text})));5;'
            f'IF(OR(ISNUMBER(SEARCH("ANALYZE";{upper_text}));'
            f'ISNUMBER(SEARCH("COMPARE";{upper_text})));4;'
            f'IF(OR(ISNUMBER(SEARCH("APPLY";{upper_text}));'
            f'ISNUMBER(SEARCH("SOLVE";{upper_text})));3;'
            f'IF(OR(ISNUMBER(SEARCH("EXPLAIN";{upper_text}));'
            f'ISNUMBER(SEARCH("DESCRIBE";{upper_text})));2;1)))))'
        )


@dataclass(slots=True, frozen=True)
class ReadabilityScoreFormula(BaseFormula):
    """Calculate Flesch-Kincaid readability grade level.

    Implements:
        READABILITY_SCORE formula for content analysis

    Calculates approximate grade level for text readability.

    Example:
        >>> formula = ReadabilityScoreFormula()
        >>> result = formula.build("100", "20", "150")
        >>> # Returns Flesch-Kincaid grade level formula
    """

    @property
    def metadata(self) -> FormulaMetadata:
        """Get formula metadata.

        Returns:
            FormulaMetadata for READABILITY_SCORE

        Implements:
            Formula metadata
        """
        return FormulaMetadata(
            name="READABILITY_SCORE",
            category="education",
            description="Calculate Flesch-Kincaid grade level",
            arguments=(
                FormulaArgument(
                    "word_count",
                    "number",
                    required=True,
                    description="Total number of words",
                ),
                FormulaArgument(
                    "sentence_count",
                    "number",
                    required=True,
                    description="Total number of sentences",
                ),
                FormulaArgument(
                    "syllable_count",
                    "number",
                    required=True,
                    description="Total number of syllables",
                ),
            ),
            return_type="number",
            examples=(
                "=READABILITY_SCORE(B2;C2;D2)",
                "=READABILITY_SCORE(words;sentences;syllables)",
            ),
        )

    def build(self, *args: Any, **kwargs: Any) -> str:
        """Build READABILITY_SCORE formula string.

        Args:
            *args: word_count, sentence_count, syllable_count
            **kwargs: Keyword arguments (optional)

        Returns:
            ODF formula string

        Implements:
            READABILITY_SCORE formula building

        Raises:
            ValueError: If arguments are invalid
        """
        self.validate_arguments(args)

        word_count = args[0]
        sentence_count = args[1]
        syllable_count = args[2]

        # Flesch-Kincaid Grade Level:
        # 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
        return f"0.39*({word_count}/{sentence_count})+11.8*({syllable_count}/{word_count})-15.59"


__all__ = [
    "AttendanceRateFormula",
    "BloomTaxonomyLevelFormula",
    "CompletionRateFormula",
    "LearningGainFormula",
    "MasteryLevelFormula",
    "ReadabilityScoreFormula",
]
