"""Binary Analysis Template for reverse engineering.

Implements:
    BinaryAnalysisTemplate for firmware and binary reverse engineering
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class BinaryAnalysisTemplate(BaseTemplate):
    """Binary analysis template for reverse engineering documentation.

    Implements:
        BinaryAnalysisTemplate for firmware and software reverse engineering

    Features:
    - Function/symbol table documentation
    - Memory region mapping
    - Data structure definitions
    - String references
    - Cross-reference tables
    - API/syscall documentation
    - Vulnerability tracking
    - Analysis notes and findings

    Example:
        >>> template = BinaryAnalysisTemplate(  # doctest: +SKIP
        ...     binary_name="firmware.bin",
        ...     architecture="ARM Cortex-M4",
        ...     base_address=0x08000000,
        ... )
        >>> builder = template.generate()  # doctest: +SKIP
        >>> path = builder.save("firmware_analysis.ods")  # doctest: +SKIP
    """

    binary_name: str = "binary.bin"
    architecture: str = "x86_64"
    base_address: int = 0x00400000
    num_functions: int = 50
    num_structures: int = 20
    include_strings: bool = True
    include_vulns: bool = True
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="Binary Analysis",
            description="Reverse engineering documentation and analysis",
            category="electrical_engineering",
            tags=("reverse-engineering", "binary", "firmware", "analysis", "security"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """Validate template parameters."""
        return self.num_functions > 0 and self.base_address >= 0

    def generate(self) -> SpreadsheetBuilder:
        """Generate binary analysis spreadsheet.

        Returns:
            SpreadsheetBuilder configured with binary analysis template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        builder.workbook_properties(
            title=f"Binary Analysis - {self.binary_name}",
            author="Security Research",
            subject="Reverse Engineering",
            description=f"Analysis documentation for {self.binary_name}",
            keywords=["reverse-engineering", "binary", "analysis", self.binary_name],
        )

        # Create overview sheet
        self._create_overview_sheet(builder)

        # Create functions sheet
        self._create_functions_sheet(builder)

        # Create structures sheet
        self._create_structures_sheet(builder)

        # Create strings sheet if enabled
        if self.include_strings:
            self._create_strings_sheet(builder)

        # Create vulnerability tracking if enabled
        if self.include_vulns:
            self._create_vulns_sheet(builder)

        # Create cross-references sheet
        self._create_xrefs_sheet(builder)

        # Create notes sheet
        self._create_notes_sheet(builder)

        return builder

    def _create_overview_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create binary overview sheet."""
        builder.sheet("Overview")

        builder.column("Property", width="160pt", style="text")
        builder.column("Value", width="200pt", style="text")
        builder.column("Notes", width="300pt", style="text")

        builder.freeze(rows=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Binary Analysis: {self.binary_name}", colspan=3)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Property")
        builder.cell("Value")
        builder.cell("Notes")

        # File information
        builder.row(style="section_header")
        builder.cell("File Information", colspan=3)

        file_info = [
            ("File Name", self.binary_name, ""),
            ("File Size", "", "bytes"),
            ("MD5 Hash", "", ""),
            ("SHA256 Hash", "", ""),
            ("File Type", "", "ELF/PE/Mach-O/Raw"),
            ("Creation Date", "", "If available"),
        ]

        for prop, value, notes in file_info:
            builder.row()
            builder.cell(prop)
            builder.cell(value if value else "", style="input")
            builder.cell(notes)

        # Architecture information
        builder.row()
        builder.row(style="section_header")
        builder.cell("Architecture", colspan=3)

        arch_info = [
            ("Architecture", self.architecture, ""),
            (
                "Bit Width",
                "32" if "32" in self.architecture or "M" in self.architecture else "64",
                "bits",
            ),
            ("Endianness", "Little", "Little/Big"),
            ("Base Address", f"0x{self.base_address:08X}", "Load address"),
            ("Entry Point", "", "Program entry"),
            ("Compiler", "", "If identifiable"),
        ]

        for prop, value, notes in arch_info:
            builder.row()
            builder.cell(prop)
            builder.cell(value if value else "", style="input")
            builder.cell(notes)

        # Analysis statistics
        builder.row()
        builder.row(style="section_header")
        builder.cell("Analysis Statistics", colspan=3)

        stats = [
            ("Functions Identified", "=COUNTA(Functions.A3:A1000)", ""),
            ("Named Functions", "", "With symbols"),
            ("Structures Defined", "=COUNTA(Structures.A3:A1000)", ""),
            (
                "Strings Found",
                "=COUNTA(Strings.A3:A1000)" if self.include_strings else "N/A",
                "",
            ),
            ("Analysis Progress", "", "%"),
        ]

        for prop, value, notes in stats:
            builder.row()
            builder.cell(prop)
            builder.cell(
                value if value else "",
                style="input" if not value.startswith("=") else "number",
            )
            builder.cell(notes)

    def _create_functions_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create functions/symbols sheet."""
        builder.sheet("Functions")

        builder.column("Address", width="100pt", style="text")
        builder.column("Name", width="160pt", style="text")
        builder.column("Size", width="70pt", type="number")
        builder.column("Type", width="70pt", style="text")
        builder.column("Call Conv", width="80pt", style="text")
        builder.column("Parameters", width="130pt", style="text")
        builder.column("Returns", width="80pt", style="text")
        builder.column("Complexity", width="70pt", type="number")
        builder.column("Basic Blks", width="70pt", type="number")
        builder.column("Loops", width="50pt", type="number")
        builder.column("Calls", width="100pt", style="text")
        builder.column("Called By", width="100pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Functions: {self.binary_name}", colspan=13)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Address")
        builder.cell("Name")
        builder.cell("Size")
        builder.cell("Type")
        builder.cell("Call Conv")
        builder.cell("Parameters")
        builder.cell("Returns")
        builder.cell("CC")
        builder.cell("BBs")
        builder.cell("Loops")
        builder.cell("Calls")
        builder.cell("Called By")
        builder.cell("Notes")

        # Function rows
        for i in range(self.num_functions):
            builder.row()
            builder.cell("", style="input")  # Address
            builder.cell(f"sub_{i:04X}" if i > 0 else "main", style="input")  # Name
            builder.cell("", style="input")  # Size
            builder.cell("func", style="input")  # Type (func/thunk/import)
            builder.cell("", style="input")  # Calling convention
            builder.cell("", style="input")  # Parameters
            builder.cell("", style="input")  # Return type
            builder.cell("", style="input")  # Cyclomatic complexity
            builder.cell("", style="input")  # Basic blocks count
            builder.cell("", style="input")  # Loop count
            builder.cell("", style="input")  # Functions it calls
            builder.cell("", style="input")  # Functions that call it
            builder.cell("", style="input")  # Notes

        # Summary
        builder.row()
        builder.row(style="section_header")
        builder.cell("Function Analysis Summary", colspan=13)

        builder.row()
        builder.cell("Total Functions:", colspan=2)
        builder.cell(f"=COUNTA(A3:A{self.num_functions + 2})")
        builder.cell("")
        builder.cell("Named:", colspan=2)
        builder.cell(f'=COUNTIF(B3:B{self.num_functions + 2};"<>sub_*")')
        builder.cell("")
        builder.cell("Avg Complexity:", colspan=2)
        builder.cell(f"=AVERAGE(H3:H{self.num_functions + 2})")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Imports:", colspan=2)
        builder.cell(f'=COUNTIF(D3:D{self.num_functions + 2};"import")')
        builder.cell("")
        builder.cell("Thunks:", colspan=2)
        builder.cell(f'=COUNTIF(D3:D{self.num_functions + 2};"thunk")')
        builder.cell("")
        builder.cell("High Complexity (>10):", colspan=2)
        builder.cell(f'=COUNTIF(H3:H{self.num_functions + 2};">10")')
        builder.cell("")
        builder.cell("")
        builder.cell("")

    def _create_structures_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create data structures sheet."""
        builder.sheet("Structures")

        builder.column("Structure", width="140pt", style="text")
        builder.column("Offset", width="70pt", style="text")
        builder.column("Field Name", width="120pt", style="text")
        builder.column("Type", width="100pt", style="text")
        builder.column("Size", width="60pt", type="number")
        builder.column("Array", width="60pt", style="text")
        builder.column("Description", width="200pt", style="text")
        builder.column("References", width="120pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Data Structures: {self.binary_name}", colspan=8)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Structure")
        builder.cell("Offset")
        builder.cell("Field")
        builder.cell("Type")
        builder.cell("Size")
        builder.cell("Array")
        builder.cell("Description")
        builder.cell("References")

        # Structure/field rows
        for i in range(self.num_structures * 5):  # ~5 fields per structure
            builder.row()
            # Only put structure name on first field
            if i % 5 == 0:
                builder.cell(f"struct_{i // 5:02X}", style="input")
            else:
                builder.cell("")
            builder.cell("", style="input")  # Offset
            builder.cell("", style="input")  # Field name
            builder.cell("", style="input")  # Type
            builder.cell("", style="input")  # Size
            builder.cell("", style="input")  # Array count
            builder.cell("", style="input")  # Description
            builder.cell("", style="input")  # References

        # Common types reference
        builder.row()
        builder.row(style="section_header")
        builder.cell("Common Types Reference", colspan=8)

        types = [
            ("uint8_t / BYTE", "1 byte unsigned"),
            ("uint16_t / WORD", "2 bytes unsigned"),
            ("uint32_t / DWORD", "4 bytes unsigned"),
            ("uint64_t / QWORD", "8 bytes unsigned"),
            ("char*", "Pointer to string"),
            ("void*", "Generic pointer"),
            ("func_ptr", "Function pointer"),
        ]

        for type_name, desc in types:
            builder.row()
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell(type_name)
            builder.cell("")
            builder.cell("")
            builder.cell(desc)
            builder.cell("")

    def _create_strings_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create strings reference sheet."""
        builder.sheet("Strings")

        builder.column("Address", width="100pt", style="text")
        builder.column("String", width="300pt", style="text")
        builder.column("Length", width="60pt", type="number")
        builder.column("Encoding", width="80pt", style="text")
        builder.column("Entropy", width="70pt", type="number")
        builder.column("XRefs", width="100pt", style="text")
        builder.column("Context", width="150pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Strings: {self.binary_name}", colspan=7)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Address")
        builder.cell("String")
        builder.cell("Length")
        builder.cell("Encoding")
        builder.cell("Entropy")
        builder.cell("XRefs")
        builder.cell("Context")

        # String rows (50 entries)
        for _ in range(50):
            builder.row()
            builder.cell("", style="input")  # Address
            builder.cell("", style="input")  # String content
            builder.cell("", style="input")  # Length
            builder.cell("", style="input")  # Encoding (ASCII/UTF-8/UTF-16/Base64)
            builder.cell("", style="input")  # Entropy (0.0-8.0 bits)
            builder.cell("", style="input")  # Cross-references
            builder.cell("", style="input")  # Context/usage

        # String categories
        builder.row()
        builder.row(style="section_header")
        builder.cell("String Categories", colspan=7)

        categories = [
            ("Error Messages", 'Contains "error", "fail", "invalid"'),
            ("Debug Strings", 'Contains "debug", "log", "trace"'),
            ("URLs/Paths", 'Contains "http", "/", "\\\\"'),
            ("Format Strings", 'Contains "%s", "%d", "%x"'),
            ("Crypto Indicators", 'Contains "key", "encrypt", "hash", "aes", "rsa"'),
            ("Credentials", 'Contains "password", "token", "api_key", "secret"'),
            ("Shell/Commands", 'Contains "cmd", "exec", "system", "shell"'),
            ("High Entropy", "Entropy > 6.0 (possibly encoded/encrypted)"),
        ]

        for cat, desc in categories:
            builder.row()
            builder.cell(cat)
            builder.cell(desc, colspan=6)

    def _create_vulns_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create vulnerability tracking sheet."""
        builder.sheet("Vulnerabilities")

        builder.column("ID", width="80pt", style="text")
        builder.column("Type", width="110pt", style="text")
        builder.column("CWE", width="80pt", style="text")
        builder.column("Location", width="100pt", style="text")
        builder.column("Function", width="120pt", style="text")
        builder.column("CVSS", width="50pt", type="number")
        builder.column("Severity", width="70pt", style="text")
        builder.column("Exploitable", width="70pt", style="text")
        builder.column("Description", width="200pt", style="text")
        builder.column("Status", width="70pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Vulnerability Analysis: {self.binary_name}", colspan=10)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("ID")
        builder.cell("Type")
        builder.cell("CWE")
        builder.cell("Location")
        builder.cell("Function")
        builder.cell("CVSS")
        builder.cell("Severity")
        builder.cell("Exploit?")
        builder.cell("Description")
        builder.cell("Status")

        # Vulnerability rows
        for i in range(20):
            row_num = i + 3
            builder.row()
            builder.cell(f"VULN-{i + 1:03d}", style="input")
            builder.cell("", style="input")  # Type
            builder.cell("", style="input")  # CWE ID (e.g., CWE-119)
            builder.cell("", style="input")  # Address/location
            builder.cell("", style="input")  # Function name
            builder.cell("", style="input")  # CVSS score (0.0-10.0)
            # Auto-calculate severity from CVSS
            builder.cell(
                f'=IF(F{row_num}="";"";'
                f'IF(F{row_num}>=9;"Critical";'
                f'IF(F{row_num}>=7;"High";'
                f'IF(F{row_num}>=4;"Medium";'
                f'IF(F{row_num}>=0.1;"Low";"Info")))))'
            )
            builder.cell("", style="input")  # Exploitable (Yes/No/Unknown)
            builder.cell("", style="input")  # Description
            builder.cell("Open", style="input")  # Status

        # Vulnerability types reference with CWE mapping
        builder.row()
        builder.row(style="section_header")
        builder.cell("Common Vulnerability Types with CWE Mapping", colspan=10)

        vuln_types = [
            ("Buffer Overflow", "CWE-119", "Stack/heap buffer overrun", "High"),
            ("Format String", "CWE-134", "Uncontrolled format string", "High"),
            ("Integer Overflow", "CWE-190", "Arithmetic overflow/underflow", "Medium"),
            ("Use After Free", "CWE-416", "Dangling pointer dereference", "High"),
            ("Null Dereference", "CWE-476", "Null pointer dereference", "Medium"),
            ("Race Condition", "CWE-362", "TOCTOU or threading issue", "Medium"),
            ("Command Injection", "CWE-78", "Shell command injection", "Critical"),
            ("Path Traversal", "CWE-22", "Directory traversal", "Medium"),
            ("Hardcoded Creds", "CWE-798", "Embedded credentials", "High"),
            ("Weak Crypto", "CWE-327", "Weak or broken cryptography", "Medium"),
        ]

        for vuln_type, cwe, desc, default_sev in vuln_types:
            builder.row()
            builder.cell("")
            builder.cell(vuln_type)
            builder.cell(cwe)
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell(default_sev)
            builder.cell("")
            builder.cell(desc)
            builder.cell("")

    def _create_xrefs_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create cross-references sheet for tracking code/data references."""
        builder.sheet("XReferences")

        builder.column("Address", width="100pt", style="text")
        builder.column("Type", width="80pt", style="text")
        builder.column("Source", width="140pt", style="text")
        builder.column("Target", width="140pt", style="text")
        builder.column("Target Type", width="90pt", style="text")
        builder.column("Context", width="200pt", style="text")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Cross-References: {self.binary_name}", colspan=7)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Address")
        builder.cell("Type")
        builder.cell("Source")
        builder.cell("Target")
        builder.cell("Target Type")
        builder.cell("Context")
        builder.cell("Notes")

        # XRef rows
        for _ in range(50):
            builder.row()
            builder.cell("", style="input")  # Address of reference
            builder.cell("", style="input")  # Type (Call/Jump/Data/Import)
            builder.cell("", style="input")  # Source function/location
            builder.cell("", style="input")  # Target address/name
            builder.cell("", style="input")  # Target type (func/data/string/import)
            builder.cell("", style="input")  # Instruction/context
            builder.cell("", style="input")  # Notes

        # Summary statistics
        builder.row()
        builder.row(style="section_header")
        builder.cell("Reference Statistics", colspan=7)

        builder.row()
        builder.cell("Total References:", colspan=2)
        builder.cell("=COUNTA(A3:A52)")
        builder.cell("")
        builder.cell("Call References:", colspan=2)
        builder.cell('=COUNTIF(B3:B52;"Call")')

        builder.row()
        builder.cell("Jump References:", colspan=2)
        builder.cell('=COUNTIF(B3:B52;"Jump")')
        builder.cell("")
        builder.cell("Data References:", colspan=2)
        builder.cell('=COUNTIF(B3:B52;"Data")')

        builder.row()
        builder.cell("Import References:", colspan=2)
        builder.cell('=COUNTIF(B3:B52;"Import")')
        builder.cell("")
        builder.cell("String References:", colspan=2)
        builder.cell('=COUNTIF(E3:E52;"string")')

        # Reference type legend
        builder.row()
        builder.row(style="section_header")
        builder.cell("Reference Types", colspan=7)

        ref_types = [
            ("Call", "Function call (CALL, BL, etc.)", "Direct/indirect call"),
            (
                "Jump",
                "Control flow transfer (JMP, B, etc.)",
                "Conditional/unconditional",
            ),
            ("Data", "Data read/write reference", "Global/static data"),
            ("Import", "External library function", "DLL/shared library"),
            ("String", "String literal reference", "ASCII/Unicode"),
            ("Vtable", "Virtual function table entry", "C++/OOP"),
        ]

        for ref_type, desc, notes in ref_types:
            builder.row()
            builder.cell("")
            builder.cell(ref_type)
            builder.cell("")
            builder.cell("")
            builder.cell("")
            builder.cell(desc)
            builder.cell(notes)

    def _create_notes_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create analysis notes sheet."""
        builder.sheet("Notes")

        builder.column("Date", width="100pt", type="date")
        builder.column("Category", width="100pt", style="text")
        builder.column("Topic", width="150pt", style="text")
        builder.column("Notes", width="500pt", style="text")

        builder.freeze(rows=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Analysis Notes: {self.binary_name}", colspan=4)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Date")
        builder.cell("Category")
        builder.cell("Topic")
        builder.cell("Notes")

        # Note entry rows
        for _ in range(30):
            builder.row()
            builder.cell("", style="input")  # Date
            builder.cell("", style="input")  # Category
            builder.cell("", style="input")  # Topic
            builder.cell("", style="input")  # Notes

        # Categories reference
        builder.row()
        builder.row(style="section_header")
        builder.cell("Note Categories", colspan=4)

        categories = [
            "Initial Analysis",
            "Function Analysis",
            "Data Structure",
            "Algorithm",
            "Security",
            "Behavior",
            "Environment",
            "Question",
            "TODO",
        ]

        for cat in categories:
            builder.row()
            builder.cell("")
            builder.cell(cat)
            builder.cell("")
            builder.cell("")


__all__ = ["BinaryAnalysisTemplate"]
