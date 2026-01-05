"""Electrical Engineering templates for SpreadsheetDL.

Implements:
    Electrical Engineering domain templates

Provides professional templates for:
- Bill of Materials (BOM) tracking
- Pin mapping for ICs and connectors
- Power budget analysis
- Signal routing documentation
- Test procedure tracking
- Register map documentation (MCU/FPGA)
- Memory map documentation
- Timing analysis (setup/hold, CDC)
- Protocol analysis (I2C, SPI, UART, CAN)
- ADC/DAC calibration
- Binary analysis for reverse engineering
"""

from spreadsheet_dl.domains.electrical_engineering.templates.adc_calibration import (
    ADCCalibrationTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.binary_analysis import (
    BinaryAnalysisTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.bom import BOMTemplate
from spreadsheet_dl.domains.electrical_engineering.templates.memory_map import (
    MemoryMapTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.pin_mapping import (
    PinMappingTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.power_budget import (
    PowerBudgetTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.procedure_template import (
    ProcedureTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.protocol_analysis import (
    ProtocolAnalysisTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.register_map import (
    RegisterMapTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.signal_routing import (
    SignalRoutingTemplate,
)
from spreadsheet_dl.domains.electrical_engineering.templates.timing_analysis import (
    TimingAnalysisTemplate,
)

__all__ = [
    "ADCCalibrationTemplate",
    "BOMTemplate",
    "BinaryAnalysisTemplate",
    "MemoryMapTemplate",
    "PinMappingTemplate",
    "PowerBudgetTemplate",
    "ProcedureTemplate",
    "ProtocolAnalysisTemplate",
    "RegisterMapTemplate",
    "SignalRoutingTemplate",
    "TimingAnalysisTemplate",
]
