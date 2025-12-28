"""
Enhanced template engine for professional spreadsheet generation.

Implements:
    - FR-TEMPLATE-001: Template Definition Schema
    - FR-TEMPLATE-002: Variable Substitution
    - FR-TEMPLATE-003: Conditional Content
    - FR-TEMPLATE-004: Reusable Components
    - FR-TEMPLATE-005: Component Library

Provides a YAML-based template system with:
- Variable substitution
- Conditional content
- Reusable components
- Sheet templates with styling
"""

from finance_tracker.template_engine.schema import (
    CellTemplate,
    ColumnTemplate,
    ComponentDefinition,
    ConditionalBlock,
    RowTemplate,
    SheetTemplate,
    SpreadsheetTemplate,
    TemplateVariable,
    VariableType,
)
from finance_tracker.template_engine.loader import (
    TemplateLoader,
    load_template,
    load_template_from_yaml,
)
from finance_tracker.template_engine.renderer import (
    ExpressionEvaluator,
    ConditionalEvaluator,
    TemplateRenderer,
    RenderedCell,
    RenderedRow,
    RenderedSheet,
    RenderedSpreadsheet,
    render_template,
)

__all__ = [
    # Schema
    "SpreadsheetTemplate",
    "SheetTemplate",
    "RowTemplate",
    "ColumnTemplate",
    "CellTemplate",
    "TemplateVariable",
    "VariableType",
    "ComponentDefinition",
    "ConditionalBlock",
    # Loader
    "TemplateLoader",
    "load_template",
    "load_template_from_yaml",
    # Renderer
    "TemplateRenderer",
    "render_template",
    "ExpressionEvaluator",
    "ConditionalEvaluator",
    "RenderedCell",
    "RenderedRow",
    "RenderedSheet",
    "RenderedSpreadsheet",
]
