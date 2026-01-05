"""Protocol Analysis Template for serial communication protocols.

Implements:
    ProtocolAnalysisTemplate for I2C, SPI, UART, CAN, and custom protocols
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class ProtocolAnalysisTemplate(BaseTemplate):
    """Protocol analysis template for serial communication documentation.

    Implements:
        ProtocolAnalysisTemplate for embedded communication protocols

    Features:
    - Protocol configuration parameters
    - Message/transaction format documentation
    - Command/response definitions
    - Timing requirements and constraints
    - Error handling specifications
    - Bus topology and addressing
    - Packet capture analysis format
    - Protocol state machine documentation

    Supports: I2C, SPI, UART, CAN, LIN, RS-485, custom protocols

    Example:
        >>> template = ProtocolAnalysisTemplate(  # doctest: +SKIP
        ...     protocol_name="I2C Sensor Bus",
        ...     protocol_type="I2C",
        ...     device_count=8,
        ... )
        >>> builder = template.generate()  # doctest: +SKIP
        >>> path = builder.save("i2c_protocol.ods")  # doctest: +SKIP
    """

    protocol_name: str = "Serial Protocol"
    protocol_type: str = "I2C"  # I2C, SPI, UART, CAN, LIN, RS485, Custom
    bus_speed: str = "100 kHz"  # Protocol-specific speed
    device_count: int = 8
    num_commands: int = 20
    include_captures: bool = True
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Protocol Analysis",
            description="Serial protocol documentation and analysis",
            category="electrical_engineering",
            tags=("protocol", "i2c", "spi", "uart", "can", "serial"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """Validate template parameters."""
        return self.device_count > 0 and self.num_commands > 0

    def generate(self) -> SpreadsheetBuilder:
        """Generate protocol analysis spreadsheet.

        Returns:
            SpreadsheetBuilder configured with protocol analysis template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Protocol Analysis - {self.protocol_name}",
            author="Embedded Systems Team",
            subject="Protocol Documentation",
            description=f"{self.protocol_type} protocol documentation for {self.protocol_name}",
            keywords=[
                "protocol",
                self.protocol_type.lower(),
                "serial",
                self.protocol_name,
            ],
        )

        # Create bus configuration sheet
        self._create_config_sheet(builder)

        # Create device registry sheet
        self._create_devices_sheet(builder)

        # Create command definitions sheet
        self._create_commands_sheet(builder)

        # Create packet capture sheet if enabled
        if self.include_captures:
            self._create_captures_sheet(builder)

        # Create protocol state machine documentation
        self._create_state_machine_sheet(builder)

        # Create protocol reference
        self._create_reference_sheet(builder)

        return builder

    def _create_config_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create bus configuration sheet."""
        builder.sheet("Configuration")

        builder.column("Parameter", width="160pt", style="text")
        builder.column("Value", width="120pt", style="text")
        builder.column("Unit", width="80pt", style="text")
        builder.column("Min", width="80pt", style="text")
        builder.column("Max", width="80pt", style="text")
        builder.column("Notes", width="200pt", style="text")

        builder.freeze(rows=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Bus Configuration: {self.protocol_name} ({self.protocol_type})",
            colspan=6,
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Parameter")
        builder.cell("Value")
        builder.cell("Unit")
        builder.cell("Min")
        builder.cell("Max")
        builder.cell("Notes")

        # Protocol-specific configuration based on type
        if self.protocol_type.upper() == "I2C":
            config_params = [
                (
                    "Bus Speed Mode",
                    "Standard",
                    "",
                    "Standard",
                    "High-Speed",
                    "Standard/Fast/Fast+/HS",
                ),
                ("Clock Frequency", "100", "kHz", "10", "3400", "Depends on mode"),
                ("Address Mode", "7-bit", "", "", "", "7-bit or 10-bit"),
                ("Pull-up Resistance", "4.7", "kΩ", "1", "10", "Bus-dependent"),
                ("VDD", "3.3", "V", "1.8", "5.0", "Logic level"),
                ("Bus Capacitance", "100", "pF", "", "400", "Maximum load"),
                ("Clock Stretching", "Enabled", "", "", "", "Slave can hold SCL low"),
                ("Multi-Master", "No", "", "", "", "Single or multi-master"),
            ]
        elif self.protocol_type.upper() == "SPI":
            config_params = [
                ("Clock Frequency", "1", "MHz", "0.1", "100", "SCLK frequency"),
                ("Clock Polarity (CPOL)", "0", "", "0", "1", "Idle state of SCLK"),
                ("Clock Phase (CPHA)", "0", "", "0", "1", "Sample edge"),
                ("SPI Mode", "0", "", "0", "3", "CPOL*2 + CPHA"),
                ("Bit Order", "MSB First", "", "", "", "MSB or LSB first"),
                ("Word Size", "8", "bits", "4", "32", "Bits per transfer"),
                ("CS Active", "Low", "", "", "", "Low or High active"),
                ("Full Duplex", "Yes", "", "", "", "Simultaneous TX/RX"),
            ]
        elif self.protocol_type.upper() == "UART":
            config_params = [
                ("Baud Rate", "115200", "bps", "300", "4000000", "Bits per second"),
                ("Data Bits", "8", "bits", "5", "9", "Bits per character"),
                ("Stop Bits", "1", "", "1", "2", "Stop bit count"),
                ("Parity", "None", "", "", "", "None/Even/Odd"),
                ("Flow Control", "None", "", "", "", "None/RTS-CTS/XON-XOFF"),
                ("Logic Level", "3.3", "V", "1.8", "5.0", "Signal voltage"),
                ("Inversion", "No", "", "", "", "Signal inversion"),
                ("Break Detection", "No", "", "", "", "Break signal support"),
            ]
        elif self.protocol_type.upper() == "CAN":
            config_params = [
                ("Bit Rate", "500", "kbps", "10", "1000", "Standard CAN rate"),
                ("Sample Point", "75", "%", "50", "90", "Bit sampling position"),
                ("SJW", "1", "TQ", "1", "4", "Synchronization jump width"),
                ("PROP_SEG", "1", "TQ", "1", "8", "Propagation segment"),
                ("PHASE_SEG1", "7", "TQ", "1", "8", "Phase segment 1"),
                ("PHASE_SEG2", "2", "TQ", "2", "8", "Phase segment 2"),
                ("Bus Length", "40", "m", "", "1000", "Maximum bus length"),
                ("Termination", "120", "Ω", "118", "122", "Bus termination"),
            ]
        else:
            config_params = [
                ("Clock/Baud Rate", self.bus_speed, "", "", "", "Communication speed"),
                ("Data Width", "8", "bits", "", "", "Bits per transfer"),
                ("Voltage Level", "3.3", "V", "", "", "Logic level"),
                ("Topology", "", "", "", "", "Point-to-point/Bus/Ring"),
                ("Encoding", "", "", "", "", "NRZ/Manchester/etc"),
                ("Error Detection", "", "", "", "", "CRC/Parity/Checksum"),
            ]

        for param, value, unit, min_val, max_val, notes in config_params:
            builder.row()
            builder.cell(param)
            builder.cell(value, style="input")
            builder.cell(unit)
            builder.cell(min_val)
            builder.cell(max_val)
            builder.cell(notes)

    def _create_devices_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create device registry sheet."""
        builder.sheet("Devices")

        builder.column("Device Name", width="140pt", style="text")
        builder.column("Address", width="80pt", style="text")
        builder.column("Role", width="80pt", style="text")
        builder.column("Part Number", width="120pt", style="text")
        builder.column("Description", width="180pt", style="text")
        builder.column("Data Sheet", width="120pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Device Registry: {self.protocol_name}", colspan=7)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Device Name")
        builder.cell("Address")
        builder.cell("Role")
        builder.cell("Part Number")
        builder.cell("Description")
        builder.cell("Data Sheet")
        builder.cell("Notes")

        # Device rows
        for i in range(self.device_count):
            builder.row()
            builder.cell("", style="input")  # Device name
            # Address format depends on protocol
            if self.protocol_type.upper() == "I2C":
                builder.cell(f"0x{0x20 + i:02X}", style="input")
            elif self.protocol_type.upper() == "CAN":
                builder.cell(f"0x{0x100 + i * 0x10:03X}", style="input")
            else:
                builder.cell(str(i), style="input")
            builder.cell("", style="input")  # Role (Master/Slave)
            builder.cell("", style="input")  # Part number
            builder.cell("", style="input")  # Description
            builder.cell("", style="input")  # Data sheet URL
            builder.cell("", style="input")  # Notes

        # Address summary
        builder.row()
        builder.row(style="section_header")
        builder.cell("Address Summary", colspan=7)

        builder.row()
        builder.cell("Total Devices:", colspan=2)
        builder.cell(f"=COUNTA(A3:A{self.device_count + 2})")
        builder.cell("")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        if self.protocol_type.upper() == "I2C":
            builder.row()
            builder.cell("Reserved Addresses:", colspan=2)
            builder.cell("0x00-0x07, 0x78-0x7F")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")

    def _create_commands_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create command definitions sheet."""
        builder.sheet("Commands")

        builder.column("Cmd ID", width="70pt", style="text")
        builder.column("Name", width="140pt", style="text")
        builder.column("Direction", width="80pt", style="text")
        builder.column("Request Format", width="180pt", style="text")
        builder.column("Response Format", width="180pt", style="text")
        builder.column("Timeout (ms)", width="80pt", type="number")
        builder.column("Description", width="200pt", style="text")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Command Definitions: {self.protocol_name}", colspan=7)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Cmd ID")
        builder.cell("Name")
        builder.cell("Direction")
        builder.cell("Request Format")
        builder.cell("Response Format")
        builder.cell("Timeout")
        builder.cell("Description")

        # Command rows
        for i in range(self.num_commands):
            builder.row()
            builder.cell(f"0x{i:02X}", style="input")  # Command ID
            builder.cell("", style="input")  # Command name
            builder.cell("Request", style="input")  # Direction
            builder.cell("", style="input")  # Request format
            builder.cell("", style="input")  # Response format
            builder.cell(100, style="input")  # Timeout
            builder.cell("", style="input")  # Description

        # Error codes section
        builder.row()
        builder.row(style="section_header")
        builder.cell("Error/Status Codes", colspan=7)

        builder.row(style="header_secondary")
        builder.cell("Code")
        builder.cell("Name")
        builder.cell("Severity")
        builder.cell("Description")
        builder.cell("Recovery")
        builder.cell("")
        builder.cell("")

        # Common error codes
        error_codes = [
            ("0x00", "Success", "Info", "Operation completed", "N/A"),
            (
                "0x01",
                "NAK",
                "Warning",
                "Device not acknowledging",
                "Retry/check address",
            ),
            ("0x02", "Timeout", "Error", "Response timeout", "Retry/reset"),
            ("0x03", "Bus Error", "Error", "Bus collision/arbitration", "Retry"),
            ("0x04", "CRC Error", "Error", "Data corruption", "Retry"),
            ("0x05", "Invalid Command", "Error", "Unknown command ID", "Check command"),
            ("0xFF", "Unknown", "Critical", "Unspecified error", "Reset device"),
        ]

        for code, name, severity, desc, recovery in error_codes:
            builder.row()
            builder.cell(code)
            builder.cell(name)
            builder.cell(severity)
            builder.cell(desc)
            builder.cell(recovery)
            builder.cell("")
            builder.cell("")

    def _create_captures_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create packet capture analysis sheet."""
        builder.sheet("Captures")

        builder.column("Timestamp", width="100pt", style="text")
        builder.column("Direction", width="60pt", style="text")
        builder.column("Address", width="80pt", style="text")
        builder.column("Command", width="80pt", style="text")
        builder.column("Data (Hex)", width="200pt", style="text")
        builder.column("Length", width="60pt", type="number")
        builder.column("Status", width="70pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Protocol Captures: {self.protocol_name}", colspan=8)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Timestamp")
        builder.cell("Dir")
        builder.cell("Address")
        builder.cell("Command")
        builder.cell("Data (Hex)")
        builder.cell("Length")
        builder.cell("Status")
        builder.cell("Notes")

        # Capture rows (empty for user to fill from logic analyzer)
        for _ in range(50):
            builder.row()
            builder.cell("", style="input")  # Timestamp
            builder.cell("", style="input")  # Direction (TX/RX)
            builder.cell("", style="input")  # Address
            builder.cell("", style="input")  # Command
            builder.cell("", style="input")  # Data bytes
            builder.cell("", style="input")  # Length
            builder.cell("", style="input")  # Status
            builder.cell("", style="input")  # Notes

        # Capture analysis
        builder.row()
        builder.row(style="section_header")
        builder.cell("Capture Analysis", colspan=8)

        builder.row()
        builder.cell("Total Packets:", colspan=2)
        builder.cell("=COUNTA(A3:A52)")
        builder.cell("")
        builder.cell("TX Packets:", colspan=2)
        builder.cell('=COUNTIF(B3:B52;"TX")')
        builder.cell("")

        builder.row()
        builder.cell("RX Packets:", colspan=2)
        builder.cell('=COUNTIF(B3:B52;"RX")')
        builder.cell("")
        builder.cell("Errors:", colspan=2)
        builder.cell('=COUNTIF(G3:G52;"Error")')
        builder.cell("")

    def _create_state_machine_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create protocol state machine documentation sheet."""
        builder.sheet("State Machine")

        builder.column("State ID", width="70pt", style="text")
        builder.column("State Name", width="120pt", style="text")
        builder.column("Entry Action", width="150pt", style="text")
        builder.column("Exit Action", width="150pt", style="text")
        builder.column("Timeout (ms)", width="80pt", type="number")
        builder.column("Description", width="200pt", style="text")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Protocol State Machine: {self.protocol_name}", colspan=6)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("State ID")
        builder.cell("State Name")
        builder.cell("Entry Action")
        builder.cell("Exit Action")
        builder.cell("Timeout")
        builder.cell("Description")

        # Protocol-specific default states based on type
        if self.protocol_type.upper() == "I2C":
            default_states = [
                ("S0", "IDLE", "Release bus", "", 0, "Bus idle, waiting for start"),
                ("S1", "START", "Drive SDA low", "", 0, "Generate start condition"),
                ("S2", "ADDR_TX", "Shift address", "", 0, "Transmitting address byte"),
                ("S3", "ADDR_ACK", "Sample SDA", "", 100, "Wait for address ACK"),
                ("S4", "DATA_TX", "Shift data", "", 0, "Transmitting data byte"),
                ("S5", "DATA_RX", "Sample SDA", "", 0, "Receiving data byte"),
                ("S6", "DATA_ACK", "Drive ACK/NAK", "", 100, "Send/receive ACK"),
                ("S7", "STOP", "Drive SDA high", "", 0, "Generate stop condition"),
                ("S8", "ERROR", "Log error", "Reset bus", 0, "Error recovery state"),
            ]
        elif self.protocol_type.upper() == "SPI":
            default_states = [
                ("S0", "IDLE", "CS high", "", 0, "Bus idle, CS inactive"),
                ("S1", "SELECT", "CS low", "", 0, "Device selected"),
                ("S2", "TX_BYTE", "Load shift reg", "", 0, "Transmitting byte"),
                ("S3", "RX_BYTE", "Read shift reg", "", 0, "Receiving byte"),
                ("S4", "WAIT", "", "", 100, "Inter-byte delay"),
                ("S5", "DESELECT", "CS high", "", 0, "Transaction complete"),
            ]
        elif self.protocol_type.upper() == "CAN":
            default_states = [
                ("S0", "BUS_OFF", "", "Reset CAN", 0, "Controller off"),
                ("S1", "INIT", "Configure CAN", "", 0, "Initialization"),
                ("S2", "IDLE", "", "", 0, "Bus idle, ready"),
                ("S3", "TX_PEND", "Load TX buffer", "", 0, "Transmission pending"),
                ("S4", "TX_ACTIVE", "", "", 100, "Transmitting frame"),
                ("S5", "TX_DONE", "Clear TX flag", "", 0, "Transmission complete"),
                ("S6", "RX_PENDING", "", "", 0, "Frame received"),
                ("S7", "RX_PROCESS", "Read RX buffer", "", 0, "Processing frame"),
                ("S8", "ERROR_ACT", "Inc error cnt", "", 0, "Error active"),
                ("S9", "ERROR_PAS", "Log warning", "", 0, "Error passive"),
            ]
        elif self.protocol_type.upper() == "UART":
            default_states = [
                ("S0", "IDLE", "Sample RX line", "", 0, "Line idle (high), waiting"),
                (
                    "S1",
                    "START_DETECT",
                    "Start bit timer",
                    "",
                    0,
                    "Start bit falling edge",
                ),
                (
                    "S2",
                    "START_VALID",
                    "Sample mid-bit",
                    "",
                    0,
                    "Validate start bit low",
                ),
                ("S3", "DATA_SHIFT", "Shift in bit", "", 0, "Receive data bits 0-7"),
                ("S4", "PARITY_CHECK", "Calculate parity", "", 0, "Check parity bit"),
                ("S5", "STOP_BIT", "Sample stop bit", "", 0, "Validate stop bit high"),
                ("S6", "FRAME_DONE", "Store byte", "Signal RX", 0, "Frame complete"),
                ("S7", "TX_IDLE", "TX line high", "", 0, "Transmitter idle"),
                ("S8", "TX_START", "TX line low", "", 0, "Send start bit"),
                ("S9", "TX_DATA", "Shift out bit", "", 0, "Transmit data bits"),
                ("S10", "TX_PARITY", "Send parity", "", 0, "Transmit parity bit"),
                ("S11", "TX_STOP", "TX line high", "", 0, "Send stop bit(s)"),
                ("S12", "TX_DONE", "Clear TX busy", "", 0, "Transmission complete"),
                ("S13", "FRAME_ERR", "Set error flag", "Log error", 0, "Framing error"),
                ("S14", "OVERRUN", "Set overrun flag", "", 0, "RX buffer overrun"),
                ("S15", "BREAK_DET", "Set break flag", "", 0, "Break condition"),
            ]
        else:
            default_states = [
                ("S0", "IDLE", "", "", 0, "Initial state"),
                ("S1", "INIT", "", "", 0, "Initialization"),
                ("S2", "READY", "", "", 0, "Ready for operation"),
                ("S3", "BUSY", "", "", 0, "Operation in progress"),
                ("S4", "COMPLETE", "", "", 0, "Operation complete"),
                ("S5", "ERROR", "", "", 0, "Error state"),
            ]

        for state_id, name, entry, exit_act, timeout, desc in default_states:
            builder.row()
            builder.cell(state_id, style="input")
            builder.cell(name, style="input")
            builder.cell(entry, style="input")
            builder.cell(exit_act, style="input")
            builder.cell(timeout if timeout else "", style="input")
            builder.cell(desc, style="input")

        # Add empty rows for custom states
        for i in range(6):
            builder.row()
            builder.cell(f"S{len(default_states) + i}", style="input")
            builder.cell("", style="input")
            builder.cell("", style="input")
            builder.cell("", style="input")
            builder.cell("", style="input")
            builder.cell("", style="input")

        # State transitions section
        builder.row()
        builder.row(style="section_header")
        builder.cell("State Transitions", colspan=6)

        builder.row(style="header_secondary")
        builder.cell("From")
        builder.cell("To")
        builder.cell("Trigger")
        builder.cell("Condition")
        builder.cell("Action")
        builder.cell("Notes")

        # Transition rows
        for _ in range(20):
            builder.row()
            builder.cell("", style="input")  # From state
            builder.cell("", style="input")  # To state
            builder.cell("", style="input")  # Trigger event
            builder.cell("", style="input")  # Guard condition
            builder.cell("", style="input")  # Transition action
            builder.cell("", style="input")  # Notes

        # State machine summary
        builder.row()
        builder.row(style="section_header")
        builder.cell("State Machine Summary", colspan=6)

        builder.row()
        builder.cell("Total States:", colspan=2)
        builder.cell(f"=COUNTA(B3:B{len(default_states) + 8})")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Initial State:", colspan=2)
        builder.cell("IDLE", style="input")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Error State:", colspan=2)
        builder.cell("ERROR", style="input")
        builder.cell("")
        builder.cell("")
        builder.cell("")

    def _create_reference_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create protocol reference sheet."""
        builder.sheet("Reference")

        builder.column("Topic", width="140pt", style="text")
        builder.column("Information", width="400pt", style="text")
        builder.column("Notes", width="200pt", style="text")

        builder.freeze(rows=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Protocol Reference: {self.protocol_type}", colspan=3)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Topic")
        builder.cell("Information")
        builder.cell("Notes")

        # Protocol-specific reference information
        if self.protocol_type.upper() == "I2C":
            ref_info = [
                ("Start Condition", "SDA goes LOW while SCL is HIGH", ""),
                ("Stop Condition", "SDA goes HIGH while SCL is HIGH", ""),
                ("ACK/NAK", "SDA LOW=ACK, SDA HIGH=NAK on 9th clock", ""),
                ("Write Address", "(device_addr << 1) | 0", "R/W bit = 0"),
                ("Read Address", "(device_addr << 1) | 1", "R/W bit = 1"),
                ("Standard Mode", "100 kHz clock", "Most compatible"),
                ("Fast Mode", "400 kHz clock", "Common for sensors"),
                ("Fast Mode Plus", "1 MHz clock", "Requires strong pull-ups"),
                ("High Speed Mode", "3.4 MHz clock", "Requires special procedure"),
                ("General Call", "Address 0x00", "Broadcast to all devices"),
            ]
        elif self.protocol_type.upper() == "SPI":
            ref_info = [
                (
                    "Mode 0 (CPOL=0, CPHA=0)",
                    "SCLK idle LOW, sample on rising edge",
                    "Most common",
                ),
                (
                    "Mode 1 (CPOL=0, CPHA=1)",
                    "SCLK idle LOW, sample on falling edge",
                    "",
                ),
                (
                    "Mode 2 (CPOL=1, CPHA=0)",
                    "SCLK idle HIGH, sample on falling edge",
                    "",
                ),
                (
                    "Mode 3 (CPOL=1, CPHA=1)",
                    "SCLK idle HIGH, sample on rising edge",
                    "",
                ),
                ("MOSI", "Master Out Slave In", "Master transmit line"),
                ("MISO", "Master In Slave Out", "Master receive line"),
                ("SCLK", "Serial Clock", "Master provides clock"),
                ("CS/SS", "Chip Select / Slave Select", "Active LOW typically"),
                (
                    "Full Duplex",
                    "Simultaneous transmit and receive",
                    "Data shifted both ways",
                ),
                ("Daisy Chain", "MOSI->MISO chained through devices", "Saves CS pins"),
            ]
        elif self.protocol_type.upper() == "CAN":
            ref_info = [
                ("Standard ID", "11-bit identifier (0x000-0x7FF)", "Most common"),
                ("Extended ID", "29-bit identifier", "CAN 2.0B"),
                ("Data Frame", "ID + 0-8 bytes data + CRC", "Normal message"),
                ("Remote Frame", "Request for data from another node", "RTR bit set"),
                ("Error Frame", "Signals bus error condition", "6 dominant bits"),
                ("Overload Frame", "Requests extra time between frames", ""),
                (
                    "Bit Stuffing",
                    "After 5 same bits, insert opposite bit",
                    "Ensures edge transitions",
                ),
                (
                    "Arbitration",
                    "Dominant (0) wins over recessive (1)",
                    "Lower ID = higher priority",
                ),
                (
                    "ACK Slot",
                    "Any receiver drives dominant to ACK",
                    "In-frame acknowledgment",
                ),
                (
                    "Termination",
                    "120Ω at each end of bus",
                    "Required for signal integrity",
                ),
            ]
        else:
            ref_info = [
                ("Protocol Type", self.protocol_type, "User-defined protocol"),
                ("Data Format", "[Document your protocol format]", ""),
                ("Timing", "[Document timing requirements]", ""),
                ("Error Handling", "[Document error detection/correction]", ""),
            ]

        for topic, info, notes in ref_info:
            builder.row()
            builder.cell(topic)
            builder.cell(info)
            builder.cell(notes)


__all__ = ["ProtocolAnalysisTemplate"]
