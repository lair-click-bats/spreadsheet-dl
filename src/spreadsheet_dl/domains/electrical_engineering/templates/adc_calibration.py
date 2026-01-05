"""ADC Calibration Template for data acquisition systems.

Implements:
    ADCCalibrationTemplate for ADC/DAC characterization and calibration
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class ADCCalibrationTemplate(BaseTemplate):
    """ADC calibration template for data acquisition characterization.

    Implements:
        ADCCalibrationTemplate for ADC and DAC testing and calibration

    Features:
    - Resolution and full-scale range tracking
    - INL/DNL measurement tables with formulas
    - Offset and gain error calculations
    - ENOB (Effective Number of Bits) tracking
    - SNR, SINAD, THD measurement recording (from external test equipment)
    - Transfer function characterization
    - Calibration coefficient generation
    - Multi-channel support

    Example:
        >>> template = ADCCalibrationTemplate(  # doctest: +SKIP
        ...     adc_name="ADS1256",
        ...     resolution_bits=24,
        ...     reference_voltage=2.5,
        ... )
        >>> builder = template.generate()  # doctest: +SKIP
        >>> path = builder.save("adc_calibration.ods")  # doctest: +SKIP
    """

    adc_name: str = "ADC"
    resolution_bits: int = 12
    reference_voltage: float = 3.3
    num_channels: int = 8
    num_test_points: int = 17  # Typically 2^N + 1 for full characterization
    include_dynamic: bool = True  # Include dynamic performance metrics
    theme: str = "corporate"

    @property
    def metadata(self) -> TemplateMetadata:
        """Get template metadata."""
        return TemplateMetadata(
            name="ADC Calibration",
            description="ADC/DAC characterization and calibration worksheet",
            category="electrical_engineering",
            tags=("adc", "dac", "calibration", "data-acquisition", "inl", "dnl"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def validate(self) -> bool:
        """Validate template parameters."""
        return (
            self.resolution_bits > 0
            and self.reference_voltage > 0
            and self.num_channels > 0
            and self.num_test_points > 1
        )

    def generate(self) -> SpreadsheetBuilder:
        """Generate ADC calibration spreadsheet.

        Returns:
            SpreadsheetBuilder configured with ADC calibration template
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        full_scale = 2**self.resolution_bits - 1
        lsb_voltage = self.reference_voltage / (2**self.resolution_bits)

        builder.workbook_properties(
            title=f"ADC Calibration - {self.adc_name}",
            author="Test Engineering",
            subject="ADC Characterization",
            description=f"Calibration data for {self.adc_name} {self.resolution_bits}-bit ADC",
            keywords=["adc", "calibration", "testing", self.adc_name],
        )

        # Create configuration sheet
        self._create_config_sheet(builder, full_scale, lsb_voltage)

        # Create transfer function sheet
        self._create_transfer_sheet(builder, full_scale, lsb_voltage)

        # Create INL/DNL analysis sheet
        self._create_inl_dnl_sheet(builder, full_scale)

        # Create dynamic performance sheet if enabled
        if self.include_dynamic:
            self._create_dynamic_sheet(builder)

        # Create calibration coefficients sheet
        self._create_calibration_sheet(builder)

        return builder

    def _create_config_sheet(
        self, builder: SpreadsheetBuilder, full_scale: int, lsb_voltage: float
    ) -> None:
        """Create ADC configuration sheet."""
        builder.sheet("Configuration")

        builder.column("Parameter", width="180pt", style="text")
        builder.column("Value", width="120pt", type="number")
        builder.column("Unit", width="80pt", style="text")
        builder.column("Notes", width="250pt", style="text")

        builder.freeze(rows=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"ADC Configuration: {self.adc_name}", colspan=4)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Parameter")
        builder.cell("Value")
        builder.cell("Unit")
        builder.cell("Notes")

        # ADC specifications
        config_data = [
            ("ADC Model", self.adc_name, "", "Device under test"),
            ("Resolution", self.resolution_bits, "bits", ""),
            ("Reference Voltage", self.reference_voltage, "V", "Full-scale reference"),
            ("Full Scale Code", full_scale, "LSB", f"2^{self.resolution_bits} - 1"),
            ("LSB Size", round(lsb_voltage * 1e6, 3), "µV", "Voltage per LSB"),
            ("Number of Channels", self.num_channels, "", ""),
            ("Input Range", f"0 to {self.reference_voltage}", "V", "Single-ended"),
            ("", "", "", ""),
            ("Test Equipment", "", "", ""),
            ("Voltage Reference", "", "", "Precision voltage source"),
            ("DMM Model", "", "", "For verification"),
            ("Temperature", 25, "°C", "Ambient during test"),
        ]

        for param, value, unit, notes in config_data:
            builder.row()
            if param:
                builder.cell(param)
                builder.cell(
                    value,
                    style="input" if isinstance(value, str) and not value else "number",
                )
                builder.cell(unit)
                builder.cell(notes)
            else:
                builder.cell("")
                builder.cell("")
                builder.cell("")
                builder.cell("")

    def _create_transfer_sheet(
        self, builder: SpreadsheetBuilder, full_scale: int, lsb_voltage: float
    ) -> None:
        """Create transfer function characterization sheet."""
        builder.sheet("Transfer Function")

        builder.column("Test Point", width="80pt", type="number")
        builder.column("Applied Voltage", width="110pt", type="number")
        builder.column("Ideal Code", width="90pt", type="number")
        builder.column("Measured Code", width="100pt", type="number")
        builder.column("Error (LSB)", width="90pt", type="number")
        builder.column("Error (mV)", width="90pt", type="number")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(
            f"Transfer Function: {self.adc_name} ({self.resolution_bits}-bit, Vref={self.reference_voltage}V)",
            colspan=7,
        )

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Test #")
        builder.cell("Applied (V)")
        builder.cell("Ideal Code")
        builder.cell("Measured")
        builder.cell("Error (LSB)")
        builder.cell("Error (mV)")
        builder.cell("Notes")

        # Test point rows
        for i in range(self.num_test_points):
            row_num = i + 3
            # Calculate ideal voltage for this test point
            fraction = i / (self.num_test_points - 1)
            ideal_voltage = fraction * self.reference_voltage
            ideal_code = round(fraction * full_scale)

            builder.row()
            builder.cell(i + 1)
            builder.cell(round(ideal_voltage, 6), style="input")  # Applied voltage
            builder.cell(ideal_code)  # Ideal code
            builder.cell("", style="input")  # Measured code
            # Error in LSB = Measured - Ideal
            builder.cell(f'=IF(D{row_num}="";"";D{row_num}-C{row_num})')
            # Error in mV = Error_LSB * LSB_voltage * 1000
            builder.cell(f'=IF(E{row_num}="";"";E{row_num}*{lsb_voltage * 1000})')
            builder.cell("", style="input")

        # Summary statistics
        builder.row()
        builder.row(style="section_header")
        builder.cell("Transfer Function Analysis", colspan=7)

        last_data_row = self.num_test_points + 2

        builder.row()
        builder.cell("Offset Error:", colspan=2)
        builder.cell("=D3-C3", style="number")
        builder.cell("LSB")
        builder.cell("First point deviation")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Gain Error:", colspan=2)
        # Gain error = (measured_span / ideal_span - 1) * 100%
        builder.cell(
            f"=(D{last_data_row}-D3)/(C{last_data_row}-C3)*100-100", style="number"
        )
        builder.cell("%")
        builder.cell("Deviation from ideal slope")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Max Positive Error:", colspan=2)
        builder.cell(f"=MAX(E3:E{last_data_row})", style="number")
        builder.cell("LSB")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Max Negative Error:", colspan=2)
        builder.cell(f"=MIN(E3:E{last_data_row})", style="number")
        builder.cell("LSB")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("RMS Error:", colspan=2)
        builder.cell(
            f"=SQRT(SUMSQ(E3:E{last_data_row})/{self.num_test_points})", style="number"
        )
        builder.cell("LSB")
        builder.cell("")
        builder.cell("")
        builder.cell("")

    def _create_inl_dnl_sheet(
        self, builder: SpreadsheetBuilder, full_scale: int
    ) -> None:
        """Create INL/DNL analysis sheet."""
        builder.sheet("INL-DNL")

        builder.column("Code", width="70pt", type="number")
        builder.column("Transition (V)", width="110pt", type="number")
        builder.column("Ideal Trans.", width="100pt", type="number")
        builder.column("Code Width", width="90pt", type="number")
        builder.column("DNL (LSB)", width="90pt", type="number")
        builder.column("INL (LSB)", width="90pt", type="number")
        builder.column("Notes", width="120pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"INL/DNL Analysis: {self.adc_name}", colspan=7)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Code")
        builder.cell("Trans. (V)")
        builder.cell("Ideal (V)")
        builder.cell("Width (LSB)")
        builder.cell("DNL (LSB)")
        builder.cell("INL (LSB)")
        builder.cell("Notes")

        lsb_voltage = self.reference_voltage / (2**self.resolution_bits)

        # Sample codes for analysis (reduce for large ADCs)
        sample_codes = min(32, 2**self.resolution_bits)
        step = max(1, (2**self.resolution_bits) // sample_codes)

        for i in range(sample_codes):
            code = i * step
            row_num = i + 3
            ideal_transition = code * lsb_voltage

            builder.row()
            builder.cell(code)
            builder.cell("", style="input")  # Measured transition voltage
            builder.cell(round(ideal_transition, 6))  # Ideal transition
            # Code width = this transition - previous transition (in LSBs)
            if i > 0:
                builder.cell(f"=(B{row_num}-B{row_num - 1})/{lsb_voltage}")
            else:
                builder.cell("")
            # DNL = Code width - 1
            if i > 0:
                builder.cell(f'=IF(D{row_num}="";"";D{row_num}-1)')
            else:
                builder.cell("")
            # INL = Cumulative sum of DNL
            if i > 0:
                builder.cell(f'=IF(E{row_num}="";"";F{row_num - 1}+E{row_num})')
            else:
                builder.cell(0)
            builder.cell("", style="input")

        # Summary
        builder.row()
        builder.row(style="section_header")
        builder.cell("INL/DNL Summary", colspan=7)

        last_row = sample_codes + 2

        builder.row()
        builder.cell("Max DNL:", colspan=2)
        builder.cell(f"=MAX(E3:E{last_row})", style="number")
        builder.cell("LSB")
        builder.cell("Should be < 1 LSB")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Min DNL:", colspan=2)
        builder.cell(f"=MIN(E3:E{last_row})", style="number")
        builder.cell("LSB")
        builder.cell("Should be > -1 LSB")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Max INL:", colspan=2)
        builder.cell(f"=MAX(F3:F{last_row})", style="number")
        builder.cell("LSB")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Min INL:", colspan=2)
        builder.cell(f"=MIN(F3:F{last_row})", style="number")
        builder.cell("LSB")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        # Definitions
        builder.row()
        builder.row(style="section_header")
        builder.cell("Definitions", colspan=7)

        defs = [
            (
                "DNL",
                "Differential Non-Linearity: Deviation of code width from ideal 1 LSB",
            ),
            (
                "INL",
                "Integral Non-Linearity: Cumulative deviation from ideal transfer function",
            ),
            ("Missing Code", "DNL < -1 LSB indicates a missing output code"),
            ("Monotonicity", "ADC is monotonic if DNL > -1 LSB for all codes"),
        ]

        for term, definition in defs:
            builder.row()
            builder.cell(term)
            builder.cell(definition, colspan=6)

    def _create_dynamic_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create dynamic performance analysis sheet."""
        builder.sheet("Dynamic Performance")

        builder.column("Parameter", width="160pt", style="text")
        builder.column("Value", width="100pt", type="number")
        builder.column("Unit", width="60pt", style="text")
        builder.column("Specification", width="100pt", style="text")
        builder.column("Status", width="70pt", style="text")
        builder.column("Notes", width="180pt", style="text")

        builder.freeze(rows=2)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Dynamic Performance: {self.adc_name}", colspan=6)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Parameter")
        builder.cell("Measured")
        builder.cell("Unit")
        builder.cell("Spec")
        builder.cell("Status")
        builder.cell("Notes")

        # Test conditions
        builder.row(style="section_header")
        builder.cell("Test Conditions", colspan=6)

        builder.row()
        builder.cell("Input Frequency")
        builder.cell("", style="input")
        builder.cell("Hz")
        builder.cell("")
        builder.cell("")
        builder.cell("Near Nyquist for FFT test")

        builder.row()
        builder.cell("Sampling Rate")
        builder.cell("", style="input")
        builder.cell("SPS")
        builder.cell("")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("Input Amplitude")
        builder.cell("", style="input")
        builder.cell("Vpp")
        builder.cell("")
        builder.cell("")
        builder.cell("-0.5 dBFS typically")

        builder.row()
        builder.cell("FFT Size")
        builder.cell(4096, style="input")
        builder.cell("points")
        builder.cell("")
        builder.cell("")
        builder.cell("Power of 2")

        # Performance metrics
        builder.row()
        builder.row(style="section_header")
        builder.cell("Performance Metrics", colspan=6)

        ideal_snr = 6.02 * self.resolution_bits + 1.76

        metrics = [
            ("SNR", "", "dB", f">{ideal_snr - 3:.1f}", "Signal-to-Noise Ratio"),
            ("SINAD", "", "dB", "", "Signal-to-Noise and Distortion"),
            ("THD", "", "dB", "", "Total Harmonic Distortion (negative is better)"),
            ("SFDR", "", "dB", "", "Spurious-Free Dynamic Range"),
            (
                "ENOB",
                "",
                "bits",
                f">{self.resolution_bits - 1}",
                "(SINAD - 1.76) / 6.02",
            ),
            ("Noise Floor", "", "dBFS", "", "RMS noise level"),
        ]

        for name, value, unit, spec, notes in metrics:
            builder.row()
            builder.cell(name)
            builder.cell(value if value else "", style="input")
            builder.cell(unit)
            builder.cell(spec)
            # Status comparison would need actual spec values
            builder.cell("", style="input")
            builder.cell(notes)

        # ENOB calculation helper
        builder.row()
        builder.row(style="section_header")
        builder.cell("Calculations", colspan=6)

        builder.row()
        builder.cell("Ideal SNR")
        builder.cell(round(ideal_snr, 2))
        builder.cell("dB")
        builder.cell(f"6.02 x {self.resolution_bits} + 1.76")
        builder.cell("")
        builder.cell("")

        builder.row()
        builder.cell("ENOB Formula")
        builder.cell("")
        builder.cell("")
        builder.cell("(SINAD - 1.76) / 6.02")
        builder.cell("")
        builder.cell("Effective Number of Bits")

    def _create_calibration_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create calibration coefficients sheet."""
        builder.sheet("Calibration")

        builder.column("Channel", width="80pt", type="number")
        builder.column("Offset (LSB)", width="100pt", type="number")
        builder.column("Gain Factor", width="100pt", type="number")
        builder.column("Offset (mV)", width="100pt", type="number")
        builder.column("Status", width="80pt", style="text")
        builder.column("Cal Date", width="100pt", type="date")
        builder.column("Notes", width="150pt", style="text")

        builder.freeze(rows=2, cols=1)

        # Title row
        builder.row(style="header_primary")
        builder.cell(f"Calibration Coefficients: {self.adc_name}", colspan=7)

        # Header row
        builder.row(style="header_secondary")
        builder.cell("Channel")
        builder.cell("Offset (LSB)")
        builder.cell("Gain Factor")
        builder.cell("Offset (mV)")
        builder.cell("Status")
        builder.cell("Cal Date")
        builder.cell("Notes")

        lsb_mv = (self.reference_voltage / (2**self.resolution_bits)) * 1000

        # Channel calibration rows
        for ch in range(self.num_channels):
            row_num = ch + 3
            builder.row()
            builder.cell(ch)
            builder.cell(0, style="input")  # Offset in LSB
            builder.cell(1.0, style="input")  # Gain factor
            # Offset in mV
            builder.cell(f"=B{row_num}*{lsb_mv:.6f}")
            builder.cell("", style="input")  # Status
            builder.cell("", style="input")  # Calibration date
            builder.cell("", style="input")

        # Calibration formulas
        builder.row()
        builder.row(style="section_header")
        builder.cell("Calibration Application", colspan=7)

        builder.row()
        builder.cell("Corrected = (Raw - Offset) * Gain", colspan=7)

        builder.row()
        builder.cell("Voltage = Corrected * LSB_voltage", colspan=7)

        builder.row()
        builder.cell(
            f"LSB Voltage = {self.reference_voltage}V / 2^{self.resolution_bits} = {lsb_mv:.6f} mV",
            colspan=7,
        )

        # Code example
        builder.row()
        builder.row(style="section_header")
        builder.cell("Implementation Example (C code)", colspan=7)

        code_lines = [
            "// Apply calibration",
            f"int16_t offset[{self.num_channels}] = {{0}};  // From column B",
            f"float gain[{self.num_channels}] = {{1.0f}};  // From column C",
            "",
            "float calibrate(int channel, int raw_code) {",
            "    float corrected = (raw_code - offset[channel]) * gain[channel];",
            f"    return corrected * {(self.reference_voltage / (2**self.resolution_bits)):.9f}f;  // Voltage",
            "}",
        ]

        for line in code_lines:
            builder.row()
            builder.cell(line, colspan=7)


__all__ = ["ADCCalibrationTemplate"]
