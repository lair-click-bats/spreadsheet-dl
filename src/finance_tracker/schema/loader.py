"""
Theme loader from YAML files.

Loads and parses theme definitions from YAML files,
handling inheritance and color reference resolution.
"""

from __future__ import annotations

import contextlib
from pathlib import Path
from typing import Any

from finance_tracker.schema.styles import (
    Border,
    BorderStyle,
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
    validate_yaml_data,
)

# Try to import yaml, with fallback for when it's not installed
try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class ThemeLoader:
    """
    Load themes from YAML files.

    Handles:
    - YAML parsing with validation
    - Theme inheritance (extends)
    - Color reference resolution
    - Style inheritance resolution
    - Theme caching
    """

    # Default theme directory (relative to this file)
    DEFAULT_THEME_DIR = Path(__file__).parent.parent / "themes"

    def __init__(self, theme_dir: Path | str | None = None) -> None:
        """
        Initialize theme loader.

        Args:
            theme_dir: Directory containing theme YAML files.
                      Defaults to package themes/ directory.
        """
        if theme_dir is None:
            self.theme_dir = self.DEFAULT_THEME_DIR
        else:
            self.theme_dir = Path(theme_dir)

        self._cache: dict[str, Theme] = {}

    def load(self, name: str) -> Theme:
        """
        Load theme by name.

        Args:
            name: Theme name (filename without .yaml extension)

        Returns:
            Loaded Theme

        Raises:
            FileNotFoundError: If theme file not found
            SchemaValidationError: If theme is invalid
        """
        if not YAML_AVAILABLE:
            raise ImportError(
                "PyYAML is required for theme loading. "
                "Install with: pip install 'finance-tracker[config]'"
            )

        # Check cache
        if name in self._cache:
            return self._cache[name]

        # Find theme file
        theme_path = self.theme_dir / f"{name}.yaml"
        if not theme_path.exists():
            # Try .yml extension
            theme_path = self.theme_dir / f"{name}.yml"
            if not theme_path.exists():
                raise FileNotFoundError(
                    f"Theme not found: {name} (looked in {self.theme_dir})"
                )

        # Load and parse
        with open(theme_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if data is None:
            raise SchemaValidationError(f"Theme file is empty: {theme_path}")

        # Validate raw data
        validate_yaml_data(data)

        # Parse theme
        theme = self._parse_theme(data)

        # Handle inheritance from parent theme
        if theme.meta.extends:
            parent = self.load(theme.meta.extends)
            theme = self._merge_themes(parent, theme)

        # Cache and return
        self._cache[name] = theme
        return theme

    def load_from_string(self, yaml_content: str) -> Theme:
        """
        Load theme from YAML string.

        Args:
            yaml_content: YAML content as string

        Returns:
            Loaded Theme
        """
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML is required for theme loading")

        data = yaml.safe_load(yaml_content)
        if data is None:
            raise SchemaValidationError("Theme content is empty")

        validate_yaml_data(data)
        return self._parse_theme(data)

    def load_from_dict(self, data: dict[str, Any]) -> Theme:
        """
        Load theme from dictionary.

        Useful for programmatic theme creation.

        Args:
            data: Theme data as dictionary

        Returns:
            Loaded Theme
        """
        validate_yaml_data(data)
        return self._parse_theme(data)

    def list_themes(self) -> list[str]:
        """
        List available theme names.

        Returns:
            List of theme names
        """
        if not self.theme_dir.exists():
            return []

        themes = []
        for path in self.theme_dir.glob("*.yaml"):
            themes.append(path.stem)
        for path in self.theme_dir.glob("*.yml"):
            if path.stem not in themes:
                themes.append(path.stem)

        return sorted(themes)

    def clear_cache(self) -> None:
        """Clear the theme cache."""
        self._cache.clear()

    def _parse_theme(self, data: dict[str, Any]) -> Theme:
        """
        Parse theme from YAML data.

        Args:
            data: Raw YAML data

        Returns:
            Parsed Theme
        """
        # Parse metadata
        meta_data = data.get("meta", {})
        meta = ThemeSchema(
            name=meta_data.get("name", "Unnamed"),
            version=meta_data.get("version", "1.0.0"),
            description=meta_data.get("description", ""),
            author=meta_data.get("author", ""),
            extends=meta_data.get("extends"),
        )

        # Parse colors
        colors = self._parse_colors(data.get("colors", {}))

        # Parse fonts
        fonts = self._parse_fonts(data.get("fonts", {}))

        # Parse base styles
        base_styles = self._parse_styles(
            data.get("base_styles", {}),
            colors,
            fonts,
        )

        # Parse semantic styles
        styles = self._parse_styles(
            data.get("styles", {}),
            colors,
            fonts,
        )

        # Parse conditional formats
        conditional_formats = data.get("conditional_formats", {})

        return Theme(
            meta=meta,
            colors=colors,
            fonts=fonts,
            base_styles=base_styles,
            styles=styles,
            conditional_formats=conditional_formats,
        )

    def _parse_colors(self, data: dict[str, str]) -> ColorPalette:
        """
        Parse color palette from YAML data.

        Args:
            data: Colors dictionary from YAML

        Returns:
            ColorPalette
        """
        palette = ColorPalette()

        # Standard color mappings
        standard_colors = {
            "primary": "primary",
            "primary_light": "primary_light",
            "primary_dark": "primary_dark",
            "secondary": "secondary",
            "success": "success",
            "success_bg": "success_bg",
            "warning": "warning",
            "warning_bg": "warning_bg",
            "danger": "danger",
            "danger_bg": "danger_bg",
            "neutral_100": "neutral_100",
            "neutral_200": "neutral_200",
            "neutral_300": "neutral_300",
            "neutral_800": "neutral_800",
            "neutral_900": "neutral_900",
        }

        for name, value in data.items():
            color = Color(value)
            if name in standard_colors:
                setattr(palette, standard_colors[name], color)
            else:
                palette.set(name, color)

        return palette

    def _parse_fonts(self, data: dict[str, Any]) -> dict[str, Font]:
        """
        Parse font definitions from YAML data.

        Args:
            data: Fonts dictionary from YAML

        Returns:
            Dictionary of Font objects
        """
        fonts: dict[str, Font] = {}

        for name, font_data in data.items():
            if isinstance(font_data, dict):
                fonts[name] = Font(
                    family=font_data.get("family", "Liberation Sans"),
                    fallback=font_data.get("fallback", "Arial, sans-serif"),
                    size=font_data.get("size", "10pt"),
                )
            else:
                # Simple case: just font family name
                fonts[name] = Font(family=str(font_data))

        return fonts

    def _parse_styles(
        self,
        data: dict[str, Any],
        colors: ColorPalette,
        fonts: dict[str, Font],
    ) -> dict[str, StyleDefinition]:
        """
        Parse style definitions from YAML data.

        Args:
            data: Styles dictionary from YAML
            colors: Color palette for reference resolution
            fonts: Font definitions for reference resolution

        Returns:
            Dictionary of StyleDefinition objects
        """
        styles: dict[str, StyleDefinition] = {}

        for name, style_data in data.items():
            if not isinstance(style_data, dict):
                continue

            style = StyleDefinition(name=name)

            # Handle extends
            if "extends" in style_data:
                style.extends = style_data["extends"]

            # Typography
            if "font_family" in style_data:
                ref = style_data["font_family"]
                if ref.startswith("{fonts."):
                    font_name = ref[7:-1]  # Extract from {fonts.name}
                    if font_name in fonts:
                        style.font_family = fonts[font_name].family
                else:
                    style.font_family = ref

            if "font_size" in style_data:
                style.font_size = style_data["font_size"]

            if "font_weight" in style_data:
                with contextlib.suppress(ValueError):
                    style.font_weight = FontWeight(style_data["font_weight"])

            if "color" in style_data:
                style.font_color = self._resolve_color(style_data["color"], colors)

            if "italic" in style_data:
                style.italic = bool(style_data["italic"])

            if "underline" in style_data:
                style.underline = bool(style_data["underline"])

            if "text_align" in style_data:
                with contextlib.suppress(ValueError):
                    style.text_align = TextAlign(style_data["text_align"])

            if "vertical_align" in style_data:
                with contextlib.suppress(ValueError):
                    style.vertical_align = VerticalAlign(style_data["vertical_align"])

            # Background
            if "background_color" in style_data:
                style.background_color = self._resolve_color(
                    style_data["background_color"], colors
                )

            # Borders
            for border_name in [
                "border_top",
                "border_bottom",
                "border_left",
                "border_right",
            ]:
                if border_name in style_data:
                    border = self._parse_border(style_data[border_name], colors)
                    setattr(style, border_name, border)

            # Spacing
            if "padding" in style_data:
                style.padding = style_data["padding"]

            # Number/date formatting
            if "number_format" in style_data:
                style.number_format = style_data["number_format"]

            if "date_format" in style_data:
                style.date_format = style_data["date_format"]

            styles[name] = style

        return styles

    def _resolve_color(self, value: str, colors: ColorPalette) -> Color:
        """
        Resolve color value or reference.

        Args:
            value: Color value or reference like "{colors.primary}"
            colors: Color palette for resolution

        Returns:
            Resolved Color
        """
        if value.startswith("{colors."):
            color_name = value[8:-1]  # Extract from {colors.name}
            resolved = colors.get(color_name)
            if resolved:
                return resolved
        return Color(value)

    def _parse_border(
        self, value: str | dict[str, Any], colors: ColorPalette
    ) -> Border:
        """
        Parse border from string or dict.

        Args:
            value: Border specification
            colors: Color palette for color resolution

        Returns:
            Border object
        """
        if isinstance(value, str):
            # Parse "1px solid {colors.primary}" format
            parts = value.split()
            width = parts[0] if len(parts) > 0 else "1px"

            style = BorderStyle.SOLID
            if len(parts) > 1:
                with contextlib.suppress(ValueError):
                    style = BorderStyle(parts[1])

            color = Color("#000000")
            if len(parts) > 2:
                color = self._resolve_color(parts[2], colors)

            return Border(width=width, style=style, color=color)

        elif isinstance(value, dict):
            return Border(
                width=value.get("width", "1px"),
                style=BorderStyle(value.get("style", "solid")),
                color=self._resolve_color(value.get("color", "#000000"), colors),
            )

        return Border()

    def _merge_themes(self, parent: Theme, child: Theme) -> Theme:
        """
        Merge child theme over parent (inheritance).

        Child values override parent values.

        Args:
            parent: Parent theme
            child: Child theme

        Returns:
            Merged theme
        """
        # Merge colors
        merged_colors = ColorPalette()
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
            parent_color = getattr(parent.colors, attr)
            child_color = getattr(child.colors, attr)
            # Use child if different from default
            default_palette = ColorPalette()
            if str(child_color) != str(getattr(default_palette, attr)):
                setattr(merged_colors, attr, child_color)
            else:
                setattr(merged_colors, attr, parent_color)

        # Merge custom colors
        merged_colors.custom = {**parent.colors.custom, **child.colors.custom}

        # Merge fonts
        merged_fonts = {**parent.fonts, **child.fonts}

        # Merge styles
        merged_base_styles = {**parent.base_styles, **child.base_styles}
        merged_styles = {**parent.styles, **child.styles}

        # Merge conditional formats
        merged_cond = {**parent.conditional_formats, **child.conditional_formats}

        return Theme(
            meta=child.meta,
            colors=merged_colors,
            fonts=merged_fonts,
            base_styles=merged_base_styles,
            styles=merged_styles,
            conditional_formats=merged_cond,
        )


# Default loader instance
_default_loader: ThemeLoader | None = None


def get_default_loader() -> ThemeLoader:
    """Get or create the default theme loader."""
    global _default_loader
    if _default_loader is None:
        _default_loader = ThemeLoader()
    return _default_loader


def load_theme(name: str) -> Theme:
    """
    Convenience function to load a theme.

    Args:
        name: Theme name

    Returns:
        Loaded Theme
    """
    return get_default_loader().load(name)


def list_available_themes() -> list[str]:
    """
    List available themes.

    Returns:
        List of theme names
    """
    return get_default_loader().list_themes()
