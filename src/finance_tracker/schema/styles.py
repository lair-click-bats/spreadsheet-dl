"""
Style schema definitions with dataclass validation.

Provides type-safe style definitions for themes including:
- Color with hex/RGB support
- Font specifications
- Border definitions
- Complete cell styles with inheritance
- Theme with color palette and style registry
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FontWeight(Enum):
    """Font weight options."""

    NORMAL = "normal"
    BOLD = "bold"
    LIGHT = "light"


class TextAlign(Enum):
    """Horizontal text alignment options."""

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class VerticalAlign(Enum):
    """Vertical text alignment options."""

    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"


class BorderStyle(Enum):
    """Border style options."""

    NONE = "none"
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"
    DOUBLE = "double"


# Regex for hex color validation
HEX_COLOR_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")


@dataclass
class Color:
    """
    Color specification supporting hex and RGB values.

    Examples:
        Color("#4472C4")
        Color.from_hex("#4472C4")
        Color.from_rgb(68, 114, 196)
    """

    value: str

    def __post_init__(self) -> None:
        """Validate color value."""
        if self.value.startswith("#"):
            if not HEX_COLOR_PATTERN.match(self.value):
                raise ValueError(f"Invalid hex color: {self.value}")
            # Normalize to 6-character hex
            if len(self.value) == 4:
                self.value = (
                    f"#{self.value[1] * 2}{self.value[2] * 2}{self.value[3] * 2}"
                )

    @classmethod
    def from_hex(cls, hex_code: str) -> Color:
        """Create color from hex code."""
        if not hex_code.startswith("#"):
            hex_code = f"#{hex_code}"
        return cls(hex_code)

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> Color:
        """Create color from RGB values (0-255)."""
        if not all(0 <= x <= 255 for x in (r, g, b)):
            raise ValueError(f"RGB values must be 0-255: ({r}, {g}, {b})")
        return cls(f"#{r:02x}{g:02x}{b:02x}")

    def to_rgb(self) -> tuple[int, int, int]:
        """Convert to RGB tuple."""
        hex_val = self.value.lstrip("#")
        return (
            int(hex_val[0:2], 16),
            int(hex_val[2:4], 16),
            int(hex_val[4:6], 16),
        )

    def __str__(self) -> str:
        return self.value


@dataclass
class ColorPalette:
    """
    Named color palette for themes.

    Provides semantic color naming for consistent theming.
    """

    primary: Color = field(default_factory=lambda: Color("#4472C4"))
    primary_light: Color = field(default_factory=lambda: Color("#6B8DD6"))
    primary_dark: Color = field(default_factory=lambda: Color("#2F4A82"))

    secondary: Color = field(default_factory=lambda: Color("#ED7D31"))

    success: Color = field(default_factory=lambda: Color("#70AD47"))
    success_bg: Color = field(default_factory=lambda: Color("#C6EFCE"))

    warning: Color = field(default_factory=lambda: Color("#FFC000"))
    warning_bg: Color = field(default_factory=lambda: Color("#FFEB9C"))

    danger: Color = field(default_factory=lambda: Color("#C00000"))
    danger_bg: Color = field(default_factory=lambda: Color("#FFC7CE"))

    neutral_100: Color = field(default_factory=lambda: Color("#FFFFFF"))
    neutral_200: Color = field(default_factory=lambda: Color("#F5F5F5"))
    neutral_300: Color = field(default_factory=lambda: Color("#E0E0E0"))
    neutral_800: Color = field(default_factory=lambda: Color("#333333"))
    neutral_900: Color = field(default_factory=lambda: Color("#000000"))

    # Additional custom colors
    custom: dict[str, Color] = field(default_factory=dict)

    def get(self, name: str) -> Color | None:
        """Get color by name."""
        # Check standard attributes first
        if hasattr(self, name) and name != "custom":
            value = getattr(self, name)
            if isinstance(value, Color):
                return value
        # Check custom colors
        return self.custom.get(name)

    def set(self, name: str, color: Color) -> None:
        """Set a custom color."""
        self.custom[name] = color

    def to_dict(self) -> dict[str, str]:
        """Convert palette to dictionary."""
        result: dict[str, str] = {}
        for attr in [
            "primary",
            "primary_light",
            "primary_dark",
            "secondary",
            "success",
            "success_bg",
            "warning",
            "warning_bg",
            "danger",
            "danger_bg",
            "neutral_100",
            "neutral_200",
            "neutral_300",
            "neutral_800",
            "neutral_900",
        ]:
            result[attr] = str(getattr(self, attr))
        for name, color in self.custom.items():
            result[name] = str(color)
        return result


@dataclass
class Font:
    """
    Font specification.

    Examples:
        Font(family="Liberation Sans", size="10pt")
        Font(family="Arial", size="12pt", weight=FontWeight.BOLD)
    """

    family: str = "Liberation Sans"
    fallback: str = "Arial, sans-serif"
    size: str = "10pt"
    weight: FontWeight = FontWeight.NORMAL
    color: Color = field(default_factory=lambda: Color("#000000"))
    italic: bool = False
    underline: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "family": self.family,
            "fallback": self.fallback,
            "size": self.size,
            "weight": self.weight.value,
            "color": str(self.color),
            "italic": self.italic,
            "underline": self.underline,
        }


@dataclass
class Border:
    """
    Border specification.

    Examples:
        Border()  # 1px solid black
        Border(width="2px", style=BorderStyle.DASHED, color=Color("#FF0000"))
    """

    width: str = "1px"
    style: BorderStyle = BorderStyle.SOLID
    color: Color = field(default_factory=lambda: Color("#000000"))

    def to_odf(self) -> str:
        """Convert to ODF border attribute string."""
        return f"{self.width} {self.style.value} {self.color.value}"

    def __str__(self) -> str:
        return self.to_odf()

    @classmethod
    def from_string(cls, border_str: str) -> Border:
        """
        Parse border from string like "1px solid #000000".

        Args:
            border_str: Border specification string

        Returns:
            Border instance
        """
        parts = border_str.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid border string: {border_str}")

        width = parts[0]
        style_str = parts[1].upper()

        try:
            style = BorderStyle[style_str]
        except KeyError:
            style = BorderStyle.SOLID

        color = Color(parts[2]) if len(parts) > 2 else Color("#000000")

        return cls(width=width, style=style, color=color)


@dataclass
class StyleDefinition:
    """
    Base style definition that can be extended.

    Used as building blocks for CellStyle. Supports inheritance
    via the 'extends' field.
    """

    name: str
    extends: str | None = None

    # Typography
    font_family: str | None = None
    font_size: str | None = None
    font_weight: FontWeight | None = None
    font_color: Color | None = None
    italic: bool | None = None
    underline: bool | None = None
    text_align: TextAlign | None = None
    vertical_align: VerticalAlign | None = None

    # Background
    background_color: Color | None = None

    # Borders
    border_top: Border | None = None
    border_bottom: Border | None = None
    border_left: Border | None = None
    border_right: Border | None = None

    # Spacing
    padding: str | None = None

    # Formatting
    number_format: str | None = None
    date_format: str | None = None


@dataclass
class CellStyle:
    """
    Complete cell style definition with all properties resolved.

    This is the final style used for rendering, with inheritance
    already applied.
    """

    name: str

    # Typography
    font: Font = field(default_factory=Font)
    text_align: TextAlign = TextAlign.LEFT
    vertical_align: VerticalAlign = VerticalAlign.MIDDLE

    # Background
    background_color: Color | None = None

    # Borders
    border_top: Border | None = None
    border_bottom: Border | None = None
    border_left: Border | None = None
    border_right: Border | None = None

    # Spacing
    padding: str = "2pt"

    # Formatting
    number_format: str | None = None
    date_format: str | None = None

    def with_overrides(self, **kwargs: Any) -> CellStyle:
        """
        Create new style with overridden values.

        Args:
            **kwargs: Style properties to override

        Returns:
            New CellStyle with overrides applied
        """
        # Copy current values
        new_font = Font(
            family=self.font.family,
            fallback=self.font.fallback,
            size=self.font.size,
            weight=self.font.weight,
            color=self.font.color,
            italic=self.font.italic,
            underline=self.font.underline,
        )

        result = CellStyle(
            name=kwargs.get("name", f"{self.name}_override"),
            font=new_font,
            text_align=self.text_align,
            vertical_align=self.vertical_align,
            background_color=self.background_color,
            border_top=self.border_top,
            border_bottom=self.border_bottom,
            border_left=self.border_left,
            border_right=self.border_right,
            padding=self.padding,
            number_format=self.number_format,
            date_format=self.date_format,
        )

        # Apply overrides
        for key, value in kwargs.items():
            if key == "name":
                result.name = value
            elif key == "font_family":
                result.font.family = value
            elif key == "font_size":
                result.font.size = value
            elif key == "font_weight":
                result.font.weight = value
            elif key == "font_color":
                result.font.color = value
            elif key == "italic":
                result.font.italic = value
            elif key == "underline":
                result.font.underline = value
            elif hasattr(result, key):
                setattr(result, key, value)

        return result

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "font": self.font.to_dict(),
            "text_align": self.text_align.value,
            "vertical_align": self.vertical_align.value,
            "background_color": str(self.background_color)
            if self.background_color
            else None,
            "border_top": str(self.border_top) if self.border_top else None,
            "border_bottom": str(self.border_bottom) if self.border_bottom else None,
            "border_left": str(self.border_left) if self.border_left else None,
            "border_right": str(self.border_right) if self.border_right else None,
            "padding": self.padding,
            "number_format": self.number_format,
            "date_format": self.date_format,
        }


@dataclass
class ThemeSchema:
    """
    Theme metadata schema.

    Contains theme identification and inheritance information.
    """

    name: str
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    extends: str | None = None


@dataclass
class Theme:
    """
    Complete theme definition.

    A theme contains:
    - Metadata (name, version, etc.)
    - Color palette
    - Font definitions
    - Style definitions with inheritance
    - Conditional formatting rules
    """

    meta: ThemeSchema
    colors: ColorPalette = field(default_factory=ColorPalette)
    fonts: dict[str, Font] = field(default_factory=dict)
    base_styles: dict[str, StyleDefinition] = field(default_factory=dict)
    styles: dict[str, StyleDefinition] = field(default_factory=dict)
    conditional_formats: dict[str, Any] = field(default_factory=dict)

    # Cache for resolved styles
    _resolved_cache: dict[str, CellStyle] = field(default_factory=dict, repr=False)

    @property
    def name(self) -> str:
        """Theme name."""
        return self.meta.name

    @property
    def version(self) -> str:
        """Theme version."""
        return self.meta.version

    @property
    def description(self) -> str:
        """Theme description."""
        return self.meta.description

    def get_color(self, name: str) -> Color:
        """
        Get color by name.

        Args:
            name: Color name from palette

        Returns:
            Color instance

        Raises:
            KeyError: If color not found
        """
        color = self.colors.get(name)
        if color is None:
            raise KeyError(f"Unknown color: {name}")
        return color

    def resolve_color_ref(self, ref: str) -> Color:
        """
        Resolve color reference like "{colors.primary}".

        Args:
            ref: Color reference string

        Returns:
            Resolved Color
        """
        if ref.startswith("{") and ref.endswith("}"):
            path = ref[1:-1].split(".")
            if path[0] == "colors" and len(path) > 1:
                return self.get_color(path[1])
        # Treat as literal color value
        return Color(ref)

    def get_style(self, name: str) -> CellStyle:
        """
        Get fully resolved style by name.

        Handles inheritance by resolving parent styles first.

        Args:
            name: Style name

        Returns:
            Fully resolved CellStyle

        Raises:
            KeyError: If style not found
        """
        # Check cache first
        if name in self._resolved_cache:
            return self._resolved_cache[name]

        # Find style definition
        style_def = self.styles.get(name) or self.base_styles.get(name)
        if style_def is None:
            raise KeyError(f"Unknown style: {name}")

        # Resolve inheritance chain
        resolved = self._resolve_style(style_def, set())
        self._resolved_cache[name] = resolved
        return resolved

    def _resolve_style(
        self,
        style_def: StyleDefinition,
        visited: set[str],
    ) -> CellStyle:
        """
        Recursively resolve style with inheritance.

        Args:
            style_def: Style definition to resolve
            visited: Set of visited style names (for cycle detection)

        Returns:
            Resolved CellStyle
        """
        if style_def.name in visited:
            raise ValueError(
                f"Circular inheritance detected for style: {style_def.name}"
            )
        visited.add(style_def.name)

        # Get parent style if extending
        if style_def.extends:
            parent_def = self.styles.get(style_def.extends) or self.base_styles.get(
                style_def.extends
            )
            if parent_def is None:
                raise KeyError(f"Parent style not found: {style_def.extends}")
            parent = self._resolve_style(parent_def, visited)
        else:
            # Create default style
            parent = CellStyle(name=style_def.name)

        # Apply overrides from this style
        font = Font(
            family=style_def.font_family or parent.font.family,
            fallback=parent.font.fallback,
            size=style_def.font_size or parent.font.size,
            weight=style_def.font_weight or parent.font.weight,
            color=style_def.font_color or parent.font.color,
            italic=style_def.italic
            if style_def.italic is not None
            else parent.font.italic,
            underline=style_def.underline
            if style_def.underline is not None
            else parent.font.underline,
        )

        return CellStyle(
            name=style_def.name,
            font=font,
            text_align=style_def.text_align or parent.text_align,
            vertical_align=style_def.vertical_align or parent.vertical_align,
            background_color=style_def.background_color or parent.background_color,
            border_top=style_def.border_top or parent.border_top,
            border_bottom=style_def.border_bottom or parent.border_bottom,
            border_left=style_def.border_left or parent.border_left,
            border_right=style_def.border_right or parent.border_right,
            padding=style_def.padding or parent.padding,
            number_format=style_def.number_format or parent.number_format,
            date_format=style_def.date_format or parent.date_format,
        )

    def list_styles(self) -> list[str]:
        """List all available style names."""
        return list(set(self.base_styles.keys()) | set(self.styles.keys()))

    def to_dict(self) -> dict[str, Any]:
        """Convert theme to dictionary for serialization."""
        return {
            "meta": {
                "name": self.meta.name,
                "version": self.meta.version,
                "description": self.meta.description,
                "author": self.meta.author,
                "extends": self.meta.extends,
            },
            "colors": self.colors.to_dict(),
            "fonts": {name: font.to_dict() for name, font in self.fonts.items()},
            "base_styles": {
                name: {"name": s.name, "extends": s.extends}
                for name, s in self.base_styles.items()
            },
            "styles": {
                name: {"name": s.name, "extends": s.extends}
                for name, s in self.styles.items()
            },
        }
