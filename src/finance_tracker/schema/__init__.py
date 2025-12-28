"""
Schema package - Declarative style and theme definitions.

Implements:
    - FR-SCHEMA-001: Extended Color Dataclass
    - FR-SCHEMA-002: Length Value Object
    - FR-SCHEMA-003: Font Dataclass Enhancement
    - FR-SCHEMA-004: Border Edge and Borders Dataclass
    - FR-SCHEMA-005: Cell Fill Dataclass
    - FR-SCHEMA-006: Number Format Dataclass
    - FR-SCHEMA-007: Complete CellStyle Dataclass
    - FR-SCHEMA-010: Style Composition System
    - FR-THEME-002: Font Pairing System
    - FR-THEME-003: Typography Hierarchy
    - FR-FORMAT-007: Print Layout Control
    - FR-FORMAT-008: Headers and Footers
    - FR-PRINT-001: Page Setup Configuration
    - FR-PRINT-002: Print Area Management

This package provides:
- Style dataclasses for type-safe style definitions
- Length value objects for consistent dimension handling
- YAML theme loader with validation
- Style inheritance and color resolution
- Number and currency formatting
- Cell fill patterns and gradients
- Font pairing and typography hierarchy
- Print layout configuration
"""

from finance_tracker.schema.loader import ThemeLoader
from finance_tracker.schema.styles import (
    # Borders
    Border,
    BorderEdge,
    Borders,
    BorderStyle,
    # Cell fill
    CellFill,
    # Core styles
    CellStyle,
    # Colors
    Color,
    ColorPalette,
    CSS_NAMED_COLORS,
    # Fonts
    Font,
    FontWeight,
    GradientFill,
    GradientStop,
    GradientType,
    # Number formats
    NegativeFormat,
    NumberFormat,
    NumberFormatCategory,
    PatternFill,
    PatternType,
    StrikethroughStyle,
    # Styles
    StyleDefinition,
    # Alignment
    TextAlign,
    # Theme
    Theme,
    ThemeSchema,
    UnderlineStyle,
    VerticalAlign,
)
from finance_tracker.schema.units import (
    cm,
    inches,
    Length,
    LengthUnit,
    mm,
    parse_length,
    pt,
)
from finance_tracker.schema.typography import (
    # Font pairing (FR-THEME-002)
    FontDefinition,
    FontPairing,
    FontRole,
    FONT_PAIRINGS,
    get_font_pairing,
    list_font_pairings,
    # Typography hierarchy (FR-THEME-003)
    HeadingStyle,
    TypeScaleRatio,
    TypeSize,
    Typography,
    TYPOGRAPHY_PRESETS,
    get_typography,
    list_typography_presets,
)
from finance_tracker.schema.validation import (
    SchemaValidationError,
    validate_color,
    validate_style,
    validate_theme,
)
from finance_tracker.schema.print_layout import (
    # Page setup (FR-PRINT-001)
    PageSetup,
    PageSize,
    PageOrientation,
    PrintScale,
    PrintQuality,
    PageMargins,
    # Headers and footers (FR-FORMAT-008)
    HeaderFooter,
    HeaderFooterContent,
    HeaderFooterSection,
    # Print area (FR-PRINT-002)
    PrintArea,
    RepeatConfig,
    PageBreak,
    # Presets
    PrintPresets,
    PageSetupBuilder,
)

__all__ = [
    # Colors (FR-SCHEMA-001)
    "Color",
    "ColorPalette",
    "CSS_NAMED_COLORS",
    # Length (FR-SCHEMA-002)
    "Length",
    "LengthUnit",
    "pt",
    "cm",
    "mm",
    "inches",
    "parse_length",
    # Fonts (FR-SCHEMA-003)
    "Font",
    "FontWeight",
    "UnderlineStyle",
    "StrikethroughStyle",
    # Font Pairing (FR-THEME-002)
    "FontDefinition",
    "FontPairing",
    "FontRole",
    "FONT_PAIRINGS",
    "get_font_pairing",
    "list_font_pairings",
    # Typography Hierarchy (FR-THEME-003)
    "HeadingStyle",
    "TypeScaleRatio",
    "TypeSize",
    "Typography",
    "TYPOGRAPHY_PRESETS",
    "get_typography",
    "list_typography_presets",
    # Borders (FR-SCHEMA-004)
    "Border",
    "BorderEdge",
    "Borders",
    "BorderStyle",
    # Cell Fill (FR-SCHEMA-005)
    "CellFill",
    "PatternFill",
    "GradientFill",
    "GradientStop",
    "PatternType",
    "GradientType",
    # Number Format (FR-SCHEMA-006)
    "NumberFormat",
    "NumberFormatCategory",
    "NegativeFormat",
    # Cell Style (FR-SCHEMA-007)
    "CellStyle",
    "StyleDefinition",
    # Alignment
    "TextAlign",
    "VerticalAlign",
    # Theme (FR-THEME-*)
    "Theme",
    "ThemeSchema",
    # Loader
    "ThemeLoader",
    # Validation
    "SchemaValidationError",
    "validate_color",
    "validate_style",
    "validate_theme",
    # Page Setup (FR-PRINT-001)
    "PageSetup",
    "PageSize",
    "PageOrientation",
    "PrintScale",
    "PrintQuality",
    "PageMargins",
    # Headers and Footers (FR-FORMAT-008)
    "HeaderFooter",
    "HeaderFooterContent",
    "HeaderFooterSection",
    # Print Area (FR-PRINT-002)
    "PrintArea",
    "RepeatConfig",
    "PageBreak",
    # Print Presets
    "PrintPresets",
    "PageSetupBuilder",
]
