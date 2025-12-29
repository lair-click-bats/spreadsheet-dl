"""
Schema validation utilities.

Provides validation functions for themes, styles, and colors
to catch configuration errors early.
"""

from __future__ import annotations

import re
from typing import Any

from finance_tracker.schema.styles import (
    BorderStyle,
    Color,
    FontWeight,
    StyleDefinition,
    TextAlign,
    Theme,
    VerticalAlign,
)


class SchemaValidationError(Exception):
    """
    Error raised when schema validation fails.

    Attributes:
        field: The field that failed validation
        message: Description of the validation failure
        value: The invalid value
    """

    def __init__(
        self,
        message: str,
        field: str | None = None,
        value: Any = None,
    ) -> None:
        self.field = field
        self.message = message
        self.value = value
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        parts = []
        if self.field:
            parts.append(f"Field '{self.field}'")
        parts.append(self.message)
        if self.value is not None:
            parts.append(f"(got: {self.value!r})")
        return ": ".join(parts) if len(parts) > 1 else parts[0]


# Regex patterns for validation
HEX_COLOR_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
SIZE_PATTERN = re.compile(r"^\d+(\.\d+)?(pt|px|cm|mm|in|em|%)$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def validate_color(value: str | Color, field: str = "color") -> Color:
    """
    Validate and return a Color object.

    Args:
        value: Color value (hex string or Color)
        field: Field name for error messages

    Returns:
        Validated Color

    Raises:
        SchemaValidationError: If color is invalid
    """
    if isinstance(value, Color):
        return value

    if not isinstance(value, str):
        raise SchemaValidationError(
            "must be a hex color string",
            field=field,
            value=value,
        )

    # Handle color references (will be resolved later)
    if value.startswith("{") and value.endswith("}"):
        # Return a placeholder - actual resolution happens in theme
        return Color("#000000")  # Placeholder

    if not HEX_COLOR_PATTERN.match(value):
        raise SchemaValidationError(
            "must be a valid hex color (e.g., #RRGGBB or #RGB)",
            field=field,
            value=value,
        )

    return Color(value)


def validate_size(value: str, field: str = "size") -> str:
    """
    Validate a size value (e.g., "10pt", "2.5cm").

    Args:
        value: Size string
        field: Field name for error messages

    Returns:
        Validated size string

    Raises:
        SchemaValidationError: If size is invalid
    """
    if not isinstance(value, str):
        raise SchemaValidationError(
            "must be a string",
            field=field,
            value=value,
        )

    if not SIZE_PATTERN.match(value):
        raise SchemaValidationError(
            "must be a valid size (e.g., '10pt', '2.5cm', '12px')",
            field=field,
            value=value,
        )

    return value


def validate_font_weight(
    value: str | FontWeight, field: str = "font_weight"
) -> FontWeight:
    """
    Validate and return a FontWeight.

    Args:
        value: Font weight value (numeric string like "700" or name like "bold")
        field: Field name for error messages

    Returns:
        Validated FontWeight

    Raises:
        SchemaValidationError: If font weight is invalid
    """
    if isinstance(value, FontWeight):
        return value

    if not isinstance(value, str):
        raise SchemaValidationError(
            "must be a string",
            field=field,
            value=value,
        )

    # First try numeric values like "700"
    try:
        return FontWeight(value)
    except ValueError:
        pass

    # Then try named values like "bold"
    try:
        return FontWeight.from_name(value)
    except (ValueError, KeyError):
        valid_names = ["thin", "light", "normal", "medium", "semibold", "bold", "extrabold", "black"]
        valid_values = [w.value for w in FontWeight]
        raise SchemaValidationError(  # noqa: B904
            f"must be one of: {', '.join(valid_names)} or numeric values: {', '.join(valid_values)}",
            field=field,
            value=value,
        )


def validate_text_align(value: str | TextAlign, field: str = "text_align") -> TextAlign:
    """
    Validate and return a TextAlign.

    Args:
        value: Text alignment value
        field: Field name for error messages

    Returns:
        Validated TextAlign

    Raises:
        SchemaValidationError: If alignment is invalid
    """
    if isinstance(value, TextAlign):
        return value

    if not isinstance(value, str):
        raise SchemaValidationError(
            "must be a string",
            field=field,
            value=value,
        )
    try:
        return TextAlign(value.lower())
    except ValueError:
        valid = [a.value for a in TextAlign]
        raise SchemaValidationError(  # noqa: B904
            f"must be one of: {', '.join(valid)}",
            field=field,
            value=value,
        )


def validate_vertical_align(
    value: str | VerticalAlign,
    field: str = "vertical_align",
) -> VerticalAlign:
    """
    Validate and return a VerticalAlign.

    Args:
        value: Vertical alignment value
        field: Field name for error messages

    Returns:
        Validated VerticalAlign

    Raises:
        SchemaValidationError: If alignment is invalid
    """
    if isinstance(value, VerticalAlign):
        return value

    if not isinstance(value, str):
        raise SchemaValidationError(
            "must be a string",
            field=field,
            value=value,
        )
    try:
        return VerticalAlign(value.lower())
    except ValueError:
        valid = [a.value for a in VerticalAlign]
        raise SchemaValidationError(  # noqa: B904
            f"must be one of: {', '.join(valid)}",
            field=field,
            value=value,
        )


def validate_border_style(
    value: str | BorderStyle,
    field: str = "border_style",
) -> BorderStyle:
    """
    Validate and return a BorderStyle.

    Args:
        value: Border style value
        field: Field name for error messages

    Returns:
        Validated BorderStyle

    Raises:
        SchemaValidationError: If style is invalid
    """
    if isinstance(value, BorderStyle):
        return value

    if not isinstance(value, str):
        raise SchemaValidationError(
            "must be a string",
            field=field,
            value=value,
        )
    try:
        return BorderStyle(value.lower())
    except ValueError:
        valid = [s.value for s in BorderStyle]
        raise SchemaValidationError(  # noqa: B904
            f"must be one of: {', '.join(valid)}",
            field=field,
            value=value,
        )


def validate_style(style: StyleDefinition) -> list[str]:
    """
    Validate a style definition.

    Args:
        style: Style definition to validate

    Returns:
        List of warning messages (empty if all valid)

    Raises:
        SchemaValidationError: If validation fails
    """
    warnings: list[str] = []

    if not style.name:
        raise SchemaValidationError("Style name is required", field="name")
    # Validate size fields
    if style.font_size:
        try:
            validate_size(style.font_size, "font_size")
        except SchemaValidationError:
            warnings.append(
                f"Style '{style.name}': Invalid font_size '{style.font_size}'"
            )

    if style.padding:
        try:
            validate_size(style.padding, "padding")
        except SchemaValidationError:
            warnings.append(f"Style '{style.name}': Invalid padding '{style.padding}'")

    return warnings


def validate_theme(theme: Theme, strict: bool = False) -> list[str]:
    """
    Validate a complete theme.

    Args:
        theme: Theme to validate
        strict: If True, raise on warnings

    Returns:
        List of warning messages

    Raises:
        SchemaValidationError: If validation fails (or strict mode with warnings)
    """
    warnings: list[str] = []

    # Validate metadata
    if not theme.meta.name:
        raise SchemaValidationError("Theme name is required", field="meta.name")

    if theme.meta.version and not VERSION_PATTERN.match(theme.meta.version):
        warnings.append(f"Theme version '{theme.meta.version}' is not semver format")

    # Validate base styles
    for name, style in theme.base_styles.items():
        if style.name != name:
            warnings.append(
                f"Base style key '{name}' doesn't match style.name '{style.name}'"
            )
        warnings.extend(validate_style(style))

    # Validate styles
    for name, style in theme.styles.items():
        if style.name != name:
            warnings.append(
                f"Style key '{name}' doesn't match style.name '{style.name}'"
            )
        warnings.extend(validate_style(style))

        # Check that extends references exist
        if style.extends and (
            style.extends not in theme.base_styles and style.extends not in theme.styles
        ):
            raise SchemaValidationError(
                f"Style '{name}' extends unknown style '{style.extends}'",
                field=f"styles.{name}.extends",
            )

    # Check for circular inheritance
    for name in theme.styles:
        try:
            theme.get_style(name)
        except ValueError as e:
            raise SchemaValidationError(str(e))  # noqa: B904

    if strict and warnings:
        raise SchemaValidationError(f"Validation warnings: {'; '.join(warnings)}")

    return warnings


def validate_yaml_data(data: dict[str, Any]) -> list[str]:
    """
    Validate raw YAML data before parsing into theme.

    Args:
        data: Raw YAML data dictionary

    Returns:
        List of warning messages

    Raises:
        SchemaValidationError: If required fields are missing
    """
    warnings: list[str] = []

    # Check required sections
    if "meta" not in data:
        raise SchemaValidationError("Theme must have 'meta' section")
    meta = data["meta"]
    if not isinstance(meta, dict):
        raise SchemaValidationError("'meta' must be a dictionary")

    if "name" not in meta:
        raise SchemaValidationError("Theme meta must have 'name'")

    # Validate color references in styles
    def check_color_refs(obj: Any, path: str = "") -> None:
        """Recursively check color references."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                check_color_refs(value, new_path)
        elif isinstance(obj, str) and obj.startswith("{colors."):
            # Extract color name
            match = re.match(r"\{colors\.(\w+)\}", obj)
            if match:
                color_name = match.group(1)
                colors = data.get("colors", {})
                if color_name not in colors:
                    # Check if it's a standard color
                    standard_colors = {
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
                    }
                    if color_name not in standard_colors:
                        warnings.append(
                            f"Reference to undefined color '{color_name}' at {path}"
                        )

    check_color_refs(data.get("base_styles", {}), "base_styles")
    check_color_refs(data.get("styles", {}), "styles")

    return warnings
