"""Register Map Template for MCU/FPGA/IC documentation.

Implements:
    RegisterMapTemplate for embedded systems and hardware development
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class RegisterMapTemplate(BaseTemplate):
    """Register map template for documenting hardware registers.

    Implements:
        RegisterMapTemplate for MCU, FPGA, and IC register documentation

    Features:
    - Register address and offset tracking
    - Bit field definitions with position, width, access type
    - Reset/default values with hex/binary display
    - Read/Write/ReadWrite/WriteOnly access indicators
    - Reserved bit tracking
    - Auto-calculated bit masks
    - Register grouping by peripheral/module
    - Cross-reference between related registers

    Example:
        >>> template = RegisterMapTemplate(  # doctest: +SKIP
        ...     device_name="STM32F4xx",
        ...     peripheral_name="GPIO",
        ...     base_address=0x40020000,
        ... )
        >>> builder = template.generate()  # doctest: +SKIP
        >>> path = builder.save("gpio_registers.ods")  # doctest: +SKIP
    """

    device_name: str = "Device"
    peripheral_name: str = "Peripheral"
    base_address: int = 0x40000000
    register_width: int = 32  # 8, 16, 32, or 64 bit
    num_registers: int = 16
    include_bit_fields: bool = True
    bit_fields_per_register: int = 8
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Register Map",
            description="Hardware register documentation with bit fields",
            category="electrical_engineering",
            tags=("registers", "mcu", "fpga", "embedded", "bitfields"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """Validate template parameters."""
        return (
            self.num_registers > 0
            and self.register_width in (8, 16, 32, 64)
            and self.base_address >= 0
        )

    def generate(self) -> SpreadsheetBuilder:
        """Generate register map spreadsheet.

        Returns:
            SpreadsheetBuilder configured with register map template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Register Map - {self.device_name} {self.peripheral_name}",
            author="Hardware Engineering",
            subject="Register Documentation",
            description=f"Register map for {self.device_name} {self.peripheral_name}",
            keywords=["registers", "hardware", "embedded", self.device_name],
        )

        # Create register overview sheet
        self._create_register_sheet(builder)

        # Create bit field details sheet if enabled
        if self.include_bit_fields:
            self._create_bitfield_sheet(builder)

        # Create quick reference sheet
        self._create_quick_reference(builder)

        return builder

    def _create_register_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create the main register overview sheet."""
        builder.sheet("Registers")

        # Define columns
        builder.column("Offset", width="70pt", style="text")
        builder.column("Address", width="90pt", style="text")
        builder.column("Name", width="140pt", style="text")
        builder.column("Access", width="60pt", style="text")
        builder.column("Reset Value", width="90pt", style="text")
        builder.column("Description", width="250pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Register Map: {self.device_name} - {self.peripheral_name} "
            f"(Base: 0x{self.base_address:08X})",
            colspan=7,
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Offset")
        builder.cell("Address")
        builder.cell("Name")
        builder.cell("Access")
        builder.cell("Reset Value")
        builder.cell("Description")
        builder.cell("Notes")

        # Register rows
        bytes_per_reg = self.register_width // 8
        for i in range(self.num_registers):
            offset = i * bytes_per_reg
            address = self.base_address + offset
            builder.row()
            builder.cell(f"0x{offset:02X}", style="input")
            builder.cell(f"0x{address:08X}")
            builder.cell("", style="input")  # Register name
            builder.cell("RW", style="input")  # Access type
            builder.cell(f"0x{'0' * (self.register_width // 4)}", style="input")
            builder.cell("", style="input")  # Description
            builder.cell("", style="input")  # Notes

        # Summary section
        builder.row()
        builder.row(style="section_header")
        builder.cell("Register Summary", colspan=7)

        builder.row()
        builder.cell("Base Address:", colspan=2)
        builder.cell(f"0x{self.base_address:08X}")
        builder.cell("")
        builder.cell("Register Width:", colspan=2)
        builder.cell(f"{self.register_width} bits")

        builder.row()
        builder.cell("Total Registers:", colspan=2)
        builder.cell(self.num_registers)
        builder.cell("")
        builder.cell("Address Range:", colspan=2)
        end_addr = self.base_address + (self.num_registers * bytes_per_reg) - 1
        builder.cell(f"0x{self.base_address:08X} - 0x{end_addr:08X}")

        # Access type legend
        builder.row()
        builder.row(style="section_header")
        builder.cell("Access Type Legend", colspan=7)

        access_types = [
            ("RW", "Read/Write", "Register can be read and written"),
            ("RO", "Read Only", "Register can only be read"),
            ("WO", "Write Only", "Register can only be written"),
            ("W1C", "Write 1 to Clear", "Write 1 to clear bit, read returns status"),
            ("W1S", "Write 1 to Set", "Write 1 to set bit"),
            ("RC", "Read to Clear", "Reading clears the register"),
        ]

        for code, name, desc in access_types:
            builder.row()
            builder.cell(code)
            builder.cell(name, colspan=2)
            builder.cell(desc, colspan=4)

    def _create_bitfield_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create bit field details sheet."""
        builder.sheet("Bit Fields")

        # Define columns
        builder.column("Register", width="120pt", style="text")
        builder.column("Bit(s)", width="60pt", style="text")
        builder.column("Field Name", width="120pt", style="text")
        builder.column("Access", width="50pt", style="text")
        builder.column("Reset", width="50pt", style="text")
        builder.column("Mask", width="90pt", style="text")
        builder.column("Description", width="200pt", style="text")
        builder.column("Values/Encoding", width="180pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Bit Field Definitions: {self.device_name} - {self.peripheral_name}",
            colspan=8,
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Register")
        builder.cell("Bit(s)")
        builder.cell("Field Name")
        builder.cell("Access")
        builder.cell("Reset")
        builder.cell("Mask")
        builder.cell("Description")
        builder.cell("Values/Encoding")

        # Bit field rows for each register
        for reg in range(self.num_registers):
            for bf in range(self.bit_fields_per_register):
                row_num = reg * self.bit_fields_per_register + bf + 3
                builder.row()
                builder.cell("", style="input")  # Register name
                builder.cell("", style="input")  # Bit position (e.g., "7:4" or "3")
                builder.cell("", style="input")  # Field name
                builder.cell("RW", style="input")  # Access
                builder.cell("0", style="input")  # Reset value
                # Mask calculation from bit position
                builder.cell(
                    f'=IF(B{row_num}="";"";'
                    f'IF(ISERROR(FIND(":";B{row_num}));'
                    f'"0x"&DEC2HEX(POWER(2;VALUE(B{row_num})));'
                    f'"0x"&DEC2HEX(POWER(2;VALUE(LEFT(B{row_num};FIND(":";B{row_num})-1))+1)'
                    f'-POWER(2;VALUE(MID(B{row_num};FIND(":";B{row_num})+1;10))))))'
                )
                builder.cell("", style="input")  # Description
                builder.cell("", style="input")  # Values/Encoding

        # Common bit field patterns
        builder.row()
        builder.row(style="section_header")
        builder.cell("Common Bit Patterns", colspan=8)

        patterns = [
            ("Enable", "0 = Disabled, 1 = Enabled"),
            ("Status", "0 = Inactive, 1 = Active"),
            ("Mode[1:0]", "00 = Mode0, 01 = Mode1, 10 = Mode2, 11 = Mode3"),
            ("Priority[2:0]", "000 = Lowest ... 111 = Highest"),
            ("Prescaler[3:0]", "0000 = /1, 0001 = /2, ... 1111 = /32768"),
        ]

        for name, values in patterns:
            builder.row()
            builder.cell("")
            builder.cell("")
            builder.cell(name)
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell(values)

    def _create_quick_reference(self, builder: SpreadsheetBuilder) -> None:
        """Create quick reference sheet with common operations."""
        builder.sheet("Quick Reference")

        builder.column("Operation", width="150pt", style="text")
        builder.column("Register", width="100pt", style="text")
        builder.column("Value/Mask", width="100pt", style="text")
        builder.column("Code Example", width="300pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Quick Reference: {self.device_name} - {self.peripheral_name}",
            colspan=5,
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Operation")
        builder.cell("Register")
        builder.cell("Value/Mask")
        builder.cell("Code Example")
        builder.cell("Notes")

        # Common operations section
        builder.row(style="section_header")
        builder.cell("Common Operations", colspan=5)

        # Example operations (empty for user to fill)
        operations = [
            "Initialize peripheral",
            "Enable peripheral",
            "Disable peripheral",
            "Set mode",
            "Configure speed/baud",
            "Enable interrupts",
            "Clear interrupt flags",
            "Read status",
            "Start operation",
            "Stop operation",
        ]

        for op in operations:
            builder.row()
            builder.cell(op, style="input")
            builder.cell("", style="input")
            builder.cell("", style="input")
            builder.cell("", style="input")
            builder.cell("", style="input")

        # Code snippets section
        builder.row()
        builder.row(style="section_header")
        builder.cell("Bit Manipulation Examples", colspan=5)

        snippets = [
            ("Set bit", "REG |= (1 << BIT)", "Set single bit"),
            ("Clear bit", "REG &= ~(1 << BIT)", "Clear single bit"),
            ("Toggle bit", "REG ^= (1 << BIT)", "Toggle single bit"),
            ("Read bit", "(REG >> BIT) & 1", "Read single bit"),
            ("Set field", "REG = (REG & ~MASK) | (VAL << POS)", "Set multi-bit field"),
            ("Read field", "(REG & MASK) >> POS", "Read multi-bit field"),
        ]

        for name, code, note in snippets:
            builder.row()
            builder.cell(name)
            builder.cell("")
            builder.cell("")
            builder.cell(code)
            builder.cell(note)


__all__ = ["RegisterMapTemplate"]
