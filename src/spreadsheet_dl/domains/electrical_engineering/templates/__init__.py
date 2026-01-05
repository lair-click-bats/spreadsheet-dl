"""Electrical Engineering templates for SpreadsheetDL.

Implements:
    Electrical Engineering domain templates

Provides professional templates for:
- Bill of Materials (BOM) tracking
- Pin mapping for ICs and connectors
- Power budget analysis
- Signal routing documentation
- Test procedure tracking
"""

from spreadsheet_dl.domains.electrical_engineering.templates.bom import BOMTemplate
from spreadsheet_dl.domains.electrical_engineering.templates.pin_mapping import (
    PinMappingTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.power_budget import (
    PowerBudgetTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.procedure_template import (
    ProcedureTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.signal_routing import (
    SignalRoutingTemplate,
)

__all__ = [
    "BOMTemplate",
    "PinMappingTemplate",
    "PowerBudgetTemplate",
    "ProcedureTemplate",
    "SignalRoutingTemplate",
]
