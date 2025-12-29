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
from finance_tracker.schema.print_layout import (
    # Headers and footers (FR-FORMAT-008)
    HeaderFooter,
    HeaderFooterContent,
    HeaderFooterSection,
    PageBreak,
    PageMargins,
    PageOrientation,
    # Page setup (FR-PRINT-001)
    PageSetup,
    PageSetupBuilder,
    PageSize,
    # Print area (FR-PRINT-002)
    PrintArea,
    # Presets
    PrintPresets,
    PrintQuality,
    PrintScale,
    RepeatConfig,
)
from finance_tracker.schema.styles import (
    CSS_NAMED_COLORS,
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
from finance_tracker.schema.typography import (
    FONT_PAIRINGS,
    TYPOGRAPHY_PRESETS,
    # Font pairing (FR-THEME-002)
    FontDefinition,
    FontPairing,
    FontRole,
    # Typography hierarchy (FR-THEME-003)
    HeadingStyle,
    TypeScaleRatio,
    TypeSize,
    Typography,
    get_font_pairing,
    get_typography,
    list_font_pairings,
    list_typography_presets,
)
from finance_tracker.schema.units import (
    Length,
    LengthUnit,
    cm,
    inches,
    mm,
    parse_length,
    pt,
)
from finance_tracker.schema.validation import (
    SchemaValidationError,
    validate_color,
    validate_style,
    validate_theme,
)

__all__ = [
    "CSS_NAMED_COLORS",
    "FONT_PAIRINGS",
    "TYPOGRAPHY_PRESETS",
    # Borders (FR-SCHEMA-004)
    "Border",
    "BorderEdge",
    "BorderStyle",
    "Borders",
    # Cell Fill (FR-SCHEMA-005)
    "CellFill",
    # Cell Style (FR-SCHEMA-007)
    "CellStyle",
    # Colors (FR-SCHEMA-001)
    "Color",
    "ColorPalette",
    # Fonts (FR-SCHEMA-003)
    "Font",
    # Font Pairing (FR-THEME-002)
    "FontDefinition",
    "FontPairing",
    "FontRole",
    "FontWeight",
    "GradientFill",
    "GradientStop",
    "GradientType",
    # Headers and Footers (FR-FORMAT-008)
    "HeaderFooter",
    "HeaderFooterContent",
    "HeaderFooterSection",
    # Typography Hierarchy (FR-THEME-003)
    "HeadingStyle",
    # Length (FR-SCHEMA-002)
    "Length",
    "LengthUnit",
    "NegativeFormat",
    # Number Format (FR-SCHEMA-006)
    "NumberFormat",
    "NumberFormatCategory",
    "PageBreak",
    "PageMargins",
    "PageOrientation",
    # Page Setup (FR-PRINT-001)
    "PageSetup",
    "PageSetupBuilder",
    "PageSize",
    "PatternFill",
    "PatternType",
    # Print Area (FR-PRINT-002)
    "PrintArea",
    # Print Presets
    "PrintPresets",
    "PrintQuality",
    "PrintScale",
    "RepeatConfig",
    # Validation
    "SchemaValidationError",
    "StrikethroughStyle",
    "StyleDefinition",
    # Alignment
    "TextAlign",
    # Theme (FR-THEME-*)
    "Theme",
    # Loader
    "ThemeLoader",
    "ThemeSchema",
    "TypeScaleRatio",
    "TypeSize",
    "Typography",
    "UnderlineStyle",
    "VerticalAlign",
    "cm",
    "get_font_pairing",
    "get_typography",
    "inches",
    "list_font_pairings",
    "list_typography_presets",
    "mm",
    "parse_length",
    "pt",
    "validate_color",
    "validate_style",
    "validate_theme",
]
