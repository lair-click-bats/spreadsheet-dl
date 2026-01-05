"""Memory Map Template for embedded systems documentation.

Implements:
    MemoryMapTemplate for firmware and hardware development
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class MemoryMapTemplate(BaseTemplate):
    """Memory map template for documenting system memory layout.

    Implements:
        MemoryMapTemplate for embedded systems memory documentation

    Features:
    - Memory region tracking with start/end addresses
    - Size calculations (auto-computed from address range)
    - Memory type classification (Flash, RAM, EEPROM, Peripheral, etc.)
    - Access permissions (R/W/X)
    - Usage tracking (bootloader, application, data, stack, heap, etc.)
    - Gap detection between regions
    - Overlap detection warnings
    - Memory utilization statistics

    Example:
        >>> template = MemoryMapTemplate(  # doctest: +SKIP
        ...     device_name="STM32F407",
        ...     total_flash=1024*1024,
        ...     total_ram=192*1024,
        ... )
        >>> builder = template.generate()  # doctest: +SKIP
        >>> path = builder.save("memory_map.ods")  # doctest: +SKIP
    """

    device_name: str = "Microcontroller"
    total_flash: int = 512 * 1024  # Total flash in bytes
    total_ram: int = 64 * 1024  # Total RAM in bytes
    num_regions: int = 20
    include_linker_info: bool = True
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Memory Map",
            description="System memory layout documentation with utilization tracking",
            category="electrical_engineering",
            tags=("memory", "embedded", "firmware", "linker", "flash", "ram"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """Validate template parameters."""
        return self.num_regions > 0 and self.total_flash >= 0 and self.total_ram >= 0

    def generate(self) -> SpreadsheetBuilder:
        """Generate memory map spreadsheet.

        Returns:
            SpreadsheetBuilder configured with memory map template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Memory Map - {self.device_name}",
            author="Firmware Engineering",
            subject="Memory Layout Documentation",
            description=f"Memory map for {self.device_name}",
            keywords=["memory", "flash", "ram", "linker", self.device_name],
        )

        # Create main memory map sheet
        self._create_memory_regions_sheet(builder)

        # Create linker script reference if enabled
        if self.include_linker_info:
            self._create_linker_reference(builder)

        # Create utilization summary
        self._create_utilization_sheet(builder)

        return builder

    def _create_memory_regions_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create the main memory regions sheet."""
        builder.sheet("Memory Regions")

        # Define columns
        builder.column("Region Name", width="130pt", style="text")
        builder.column("Start Address", width="95pt", style="text")
        builder.column("End Address", width="95pt", style="text")
        builder.column("Size (Bytes)", width="85pt", type="number")
        builder.column("Size (KB)", width="65pt", type="number")
        builder.column("Gap (Bytes)", width="80pt", type="number")
        builder.column("Type", width="70pt", style="text")
        builder.column("Access", width="55pt", style="text")
        builder.column("Cache", width="50pt", style="text")
        builder.column("XN", width="40pt", style="text")
        builder.column("Valid", width="55pt", style="text")
        builder.column("Usage", width="100pt", style="text")
        builder.column("Notes", width="130pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Memory Map: {self.device_name} "
            f"(Flash: {self.total_flash // 1024}KB, RAM: {self.total_ram // 1024}KB)",
            colspan=13,
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Region Name")
        builder.cell("Start Address")
        builder.cell("End Address")
        builder.cell("Size (Bytes)")
        builder.cell("Size (KB)")
        builder.cell("Gap (Bytes)")
        builder.cell("Type")
        builder.cell("Access")
        builder.cell("Cache")
        builder.cell("XN")
        builder.cell("Valid")
        builder.cell("Usage")
        builder.cell("Notes")

        # Memory region rows
        for i in range(self.num_regions):
            row_num = i + 3
            builder.row()
            builder.cell("", style="input")  # Region name (A)
            builder.cell("", style="input")  # Start address hex (B)
            builder.cell("", style="input")  # End address hex (C)
            # Size = End - Start + 1 (if both provided) (D)
            builder.cell(
                f'=IF(OR(B{row_num}="";C{row_num}="");"";'
                f'HEX2DEC(SUBSTITUTE(C{row_num};"0x";""))'
                f'-HEX2DEC(SUBSTITUTE(B{row_num};"0x";""))+1)'
            )
            # Size in KB (E)
            builder.cell(f'=IF(D{row_num}="";"";D{row_num}/1024)', style="number")
            # Gap = Current Start - Previous End - 1 (F)
            if i == 0:
                builder.cell("")  # No gap for first row
            else:
                builder.cell(
                    f'=IF(OR(B{row_num}="";C{row_num - 1}="");"";'
                    f'HEX2DEC(SUBSTITUTE(B{row_num};"0x";""))'
                    f'-HEX2DEC(SUBSTITUTE(C{row_num - 1};"0x";""))-1)'
                )
            builder.cell("", style="input")  # Type (G)
            builder.cell("RWX", style="input")  # Access (H)
            builder.cell("Y", style="input")  # Cacheable (I)
            builder.cell("N", style="input")  # Execute Never (J)
            # Validation: check End >= Start and no overlap (K)
            if i == 0:
                # First row: just check End >= Start
                builder.cell(
                    f'=IF(OR(B{row_num}="";C{row_num}="");"";'
                    f'IF(HEX2DEC(SUBSTITUTE(C{row_num};"0x";""))'
                    f'>=HEX2DEC(SUBSTITUTE(B{row_num};"0x";""));"OK";"ERR"))'
                )
            else:
                # Subsequent rows: check End >= Start AND no overlap with prev
                builder.cell(
                    f'=IF(OR(B{row_num}="";C{row_num}="");"";'
                    f'IF(HEX2DEC(SUBSTITUTE(C{row_num};"0x";""))'
                    f'<HEX2DEC(SUBSTITUTE(B{row_num};"0x";""));"RANGE";'
                    f'IF(AND(C{row_num - 1}<>"";'
                    f'HEX2DEC(SUBSTITUTE(B{row_num};"0x";""))'
                    f'<=HEX2DEC(SUBSTITUTE(C{row_num - 1};"0x";"")));"OVERLAP";"OK")))'
                )
            builder.cell("", style="input")  # Usage (L)
            builder.cell("", style="input")  # Notes (M)

        # Summary section
        builder.row()
        builder.row(style="section_header")
        builder.cell("Memory Summary", colspan=13)

        # Flash usage row
        builder.row()
        builder.cell("Flash Regions:", colspan=2)
        builder.cell(f'=COUNTIF(G3:G{self.num_regions + 2};"Flash")')
        builder.cell("")
        builder.cell("Flash Used (Bytes):", colspan=2)
        builder.cell(
            f'=SUMIF(G3:G{self.num_regions + 2};"Flash";D3:D{self.num_regions + 2})'
        )
        builder.cell("")
        # Count specific errors, not empty cells
        builder.cell("Validation Errors:", colspan=2)
        builder.cell(
            f'=COUNTIF(K3:K{self.num_regions + 2};"ERR")'
            f'+COUNTIF(K3:K{self.num_regions + 2};"RANGE")'
            f'+COUNTIF(K3:K{self.num_regions + 2};"OVERLAP")'
        )
        builder.cell("")
        builder.cell("")

        # RAM usage row
        builder.row()
        builder.cell("RAM Regions:", colspan=2)
        builder.cell(f'=COUNTIF(G3:G{self.num_regions + 2};"RAM")')
        builder.cell("")
        builder.cell("RAM Used (Bytes):", colspan=2)
        builder.cell(
            f'=SUMIF(G3:G{self.num_regions + 2};"RAM";D3:D{self.num_regions + 2})'
        )
        builder.cell("")
        builder.cell("Overlaps:", colspan=2)
        builder.cell(f'=COUNTIF(K3:K{self.num_regions + 2};"OVERLAP")')
        builder.cell("")
        builder.cell("")

        # Gap statistics row
        builder.row()
        builder.cell("Total Regions:", colspan=2)
        builder.cell(f"=COUNTA(A3:A{self.num_regions + 2})")
        builder.cell("")
        builder.cell("Total Gaps (Bytes):", colspan=2)
        builder.cell(f"=SUM(F3:F{self.num_regions + 2})")
        builder.cell("")
        builder.cell("Negative Gaps:", colspan=2)
        builder.cell(f'=COUNTIF(F3:F{self.num_regions + 2};"<0")')
        builder.cell("")
        builder.cell("")

        # Type legend
        builder.row()
        builder.row(style="section_header")
        builder.cell("Memory Type Legend", colspan=13)

        types = [
            ("Flash", "Non-volatile program memory"),
            ("RAM", "Volatile data memory (SRAM)"),
            ("EEPROM", "Non-volatile data storage"),
            ("CCM", "Core-Coupled Memory (tightly coupled RAM)"),
            ("Peripheral", "Memory-mapped peripheral registers"),
            ("External", "External memory (SDRAM, PSRAM, etc.)"),
            ("Reserved", "Reserved/unavailable memory region"),
        ]

        for mem_type, desc in types:
            builder.row()
            builder.cell(mem_type)
            builder.cell(desc, colspan=12)

    def _create_linker_reference(self, builder: SpreadsheetBuilder) -> None:
        """Create linker script reference sheet."""
        builder.sheet("Linker Reference")

        builder.column("Section", width="120pt", style="text")
        builder.column("VMA (Load)", width="100pt", style="text")
        builder.column("LMA (Run)", width="100pt", style="text")
        builder.column("Size", width="80pt", style="text")
        builder.column("Alignment", width="80pt", style="text")
        builder.column("Flags", width="80pt", style="text")
        builder.column("Description", width="200pt", style="text")

        builder.freeze(rows=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Linker Script Reference: {self.device_name}", colspan=7)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Section")
        builder.cell("VMA (Load)")
        builder.cell("LMA (Run)")
        builder.cell("Size")
        builder.cell("Alignment")
        builder.cell("Flags")
        builder.cell("Description")

        # Standard sections
        sections = [
            (".isr_vector", "Interrupt vector table"),
            (".text", "Executable code"),
            (".rodata", "Read-only data (constants)"),
            (".ARM.extab", "ARM exception tables"),
            (".ARM.exidx", "ARM exception index"),
            (".preinit_array", "Pre-initialization functions"),
            (".init_array", "Initialization functions"),
            (".fini_array", "Finalization functions"),
            (".data", "Initialized data (copied from Flash to RAM)"),
            (".bss", "Uninitialized data (zero-filled)"),
            (".heap", "Dynamic memory allocation"),
            (".stack", "Program stack"),
            (".ccmram", "CCM RAM section"),
        ]

        for section, desc in sections:
            builder.row()
            builder.cell(section)
            builder.cell("", style="input")  # VMA
            builder.cell("", style="input")  # LMA
            builder.cell("", style="input")  # Size
            builder.cell("4", style="input")  # Alignment (default 4)
            builder.cell("", style="input")  # Flags
            builder.cell(desc)

        # Linker symbols
        builder.row()
        builder.row(style="section_header")
        builder.cell("Common Linker Symbols", colspan=7)

        symbols = [
            ("_etext", "End of .text section"),
            ("_sdata", "Start of .data section in RAM"),
            ("_edata", "End of .data section in RAM"),
            ("_sidata", "Start of .data initialization values in Flash"),
            ("_sbss", "Start of .bss section"),
            ("_ebss", "End of .bss section"),
            ("_estack", "Initial stack pointer (top of RAM)"),
            ("_Min_Heap_Size", "Minimum heap size"),
            ("_Min_Stack_Size", "Minimum stack size"),
        ]

        for symbol, desc in symbols:
            builder.row()
            builder.cell(symbol)
            builder.cell("", style="input")  # Value
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell(desc)

    def _create_utilization_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create memory utilization analysis sheet."""
        builder.sheet("Utilization")

        builder.column("Metric", width="180pt", style="text")
        builder.column("Value", width="100pt", type="number")
        builder.column("Unit", width="60pt", style="text")
        builder.column("Percentage", width="80pt", type="percentage")
        builder.column("Status", width="80pt", style="text")
        builder.column("Notes", width="200pt", style="text")

        builder.freeze(rows=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Memory Utilization: {self.device_name}", colspan=6)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Metric")
        builder.cell("Value")
        builder.cell("Unit")
        builder.cell("Percentage")
        builder.cell("Status")
        builder.cell("Notes")

        # Flash utilization
        builder.row(style="section_header")
        builder.cell("Flash Memory", colspan=6)

        builder.row()
        builder.cell("Total Flash")
        builder.cell(self.total_flash)
        builder.cell("Bytes")
        builder.cell("100%")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Flash Used")
        builder.cell(0, style="input")  # User fills in
        builder.cell("Bytes")
        builder.cell(f"=B5/{self.total_flash}")
        builder.cell('=IF(D5>0.9;"CRITICAL";IF(D5>0.75;"WARNING";"OK"))')
        builder.cell("")

        builder.row()
        builder.cell("Flash Available")
        builder.cell(f"={self.total_flash}-B5")
        builder.cell("Bytes")
        builder.cell(f"=B6/{self.total_flash}")
        builder.cell("")
        builder.cell("")

        # RAM utilization
        builder.row()
        builder.row(style="section_header")
        builder.cell("RAM Memory", colspan=6)

        builder.row()
        builder.cell("Total RAM")
        builder.cell(self.total_ram)
        builder.cell("Bytes")
        builder.cell("100%")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Static RAM (.data + .bss)")
        builder.cell(0, style="input")
        builder.cell("Bytes")
        builder.cell(f"=B10/{self.total_ram}")
        builder.cell('=IF(D10>0.8;"WARNING";"OK")')
        builder.cell("Compile-time allocated")

        builder.row()
        builder.cell("Stack Size")
        builder.cell(0, style="input")
        builder.cell("Bytes")
        builder.cell(f"=B11/{self.total_ram}")
        builder.cell("")
        builder.cell("Reserved for stack")

        builder.row()
        builder.cell("Heap Size")
        builder.cell(0, style="input")
        builder.cell("Bytes")
        builder.cell(f"=B12/{self.total_ram}")
        builder.cell("")
        builder.cell("Available for malloc")

        builder.row()
        builder.cell("RAM Available")
        builder.cell(f"={self.total_ram}-B10-B11-B12")
        builder.cell("Bytes")
        builder.cell(f"=B13/{self.total_ram}")
        builder.cell('=IF(B13<0;"OVERFLOW";IF(D13<0.1;"LOW";"OK"))')
        builder.cell("")

        # Recommendations
        builder.row()
        builder.row(style="section_header")
        builder.cell("Utilization Guidelines", colspan=6)

        guidelines = [
            ("Flash", "< 75%", "Good headroom for updates"),
            ("Flash", "75-90%", "Consider optimization"),
            ("Flash", "> 90%", "Critical - reduce code size"),
            ("RAM (static)", "< 50%", "Good headroom"),
            ("RAM (static)", "50-80%", "Monitor growth"),
            ("RAM (static)", "> 80%", "Risk of stack overflow"),
            ("Stack", "Minimum 1KB", "For interrupt nesting"),
            ("Heap", "Application dependent", "Consider static allocation"),
        ]

        for resource, threshold, note in guidelines:
            builder.row()
            builder.cell(resource)
            builder.cell("")
            builder.cell("")
            builder.cell(threshold)
            builder.cell("")
            builder.cell(note)


__all__ = ["MemoryMapTemplate"]
