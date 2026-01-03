"""
Domain Plugins for SpreadsheetDL.

Domain-specific functionality organized as plugins.

Implements:
    PHASE0-001: Restructure package for domain plugins
    PHASE0-002: Create domain plugin base classes
"""

from spreadsheet_dl.domains.base import (
    BaseDomainPlugin,
    BaseFormula,
    BaseImporter,
    BaseTemplate,
    FormulaArgument,
    FormulaMetadata,
    ImporterMetadata,
    ImportResult,
    PluginDependency,
    PluginMetadata,
    PluginStatus,
    TemplateMetadata,
)

__all__ = [
    # Base Classes
    "BaseDomainPlugin",
    "BaseTemplate",
    "BaseFormula",
    "BaseImporter",
    # Metadata Classes
    "PluginMetadata",
    "PluginDependency",
    "PluginStatus",
    "TemplateMetadata",
    "FormulaMetadata",
    "FormulaArgument",
    "ImporterMetadata",
    "ImportResult",
    # Domain Subpackages
    "finance",
]
