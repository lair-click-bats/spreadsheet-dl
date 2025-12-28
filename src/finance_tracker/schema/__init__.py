"""
Schema package - Declarative style and theme definitions.

This package provides:
- Style dataclasses for type-safe style definitions
- YAML theme loader with validation
- Style inheritance and color resolution
"""

from finance_tracker.schema.loader import ThemeLoader
from finance_tracker.schema.styles import (
    Border,
    BorderStyle,
    CellStyle,
    Color,
    ColorPalette,
    Font,
    FontWeight,
    StyleDefinition,
    TextAlign,
    Theme,
    ThemeSchema,
    VerticalAlign,
)
from finance_tracker.schema.validation import (
    SchemaValidationError,
    validate_color,
    validate_style,
    validate_theme,
)

__all__ = [
    # Styles
    "Border",
    "BorderStyle",
    "CellStyle",
    "Color",
    "ColorPalette",
    "Font",
    "FontWeight",
    # Validation
    "SchemaValidationError",
    "StyleDefinition",
    "TextAlign",
    "Theme",
    # Loader
    "ThemeLoader",
    "ThemeSchema",
    "VerticalAlign",
    "validate_color",
    "validate_style",
    "validate_theme",
]
