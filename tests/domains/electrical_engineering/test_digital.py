"""Tests for digital circuit formulas in electrical engineering.

Implements:
    Tests for digital logic and binary conversion formulas
"""

from __future__ import annotations

import pytest

from spreadsheet_dl.domains.electrical_engineering.formulas.digital import (
    BinaryToDecimalFormula,
    DecimalToBinaryFormula,
    LogicNANDFormula,
    LogicNORFormula,
    LogicXORFormula,
)

pytestmark = [pytest.mark.unit, pytest.mark.domain, pytest.mark.engineering]


# ============================================================================
# Logic Gate Formula Tests
# ============================================================================


def test_logic_nand_formula() -> None:
    """Test NAND gate logic formula."""
    formula = LogicNANDFormula()

    # Test metadata
    assert formula.metadata.name == "LOGIC_NAND"
    assert formula.metadata.category == "electrical_engineering"
    assert len(formula.metadata.arguments) == 2
    assert formula.metadata.return_type == "boolean"

    # Test formula building
    result = formula.build("TRUE", "FALSE")
    assert result == "NOT(AND(TRUE,FALSE))"

    # Test with cell references
    result = formula.build("A2", "B2")
    assert result == "NOT(AND(A2,B2))"


def test_logic_nor_formula() -> None:
    """Test NOR gate logic formula."""
    formula = LogicNORFormula()

    # Test metadata
    assert formula.metadata.name == "LOGIC_NOR"
    assert formula.metadata.category == "electrical_engineering"
    assert len(formula.metadata.arguments) == 2
    assert formula.metadata.return_type == "boolean"

    # Test formula building
    result = formula.build("FALSE", "FALSE")
    assert result == "NOT(OR(FALSE,FALSE))"

    # Test with cell references
    result = formula.build("A2", "B2")
    assert result == "NOT(OR(A2,B2))"


def test_logic_xor_formula() -> None:
    """Test XOR gate logic formula."""
    formula = LogicXORFormula()

    # Test metadata
    assert formula.metadata.name == "LOGIC_XOR"
    assert formula.metadata.category == "electrical_engineering"
    assert len(formula.metadata.arguments) == 2
    assert formula.metadata.return_type == "boolean"

    # Test formula building
    result = formula.build("TRUE", "FALSE")
    assert result == "OR(AND(TRUE,NOT(FALSE)),AND(NOT(TRUE),FALSE))"

    # Test with cell references
    result = formula.build("A2", "B2")
    assert result == "OR(AND(A2,NOT(B2)),AND(NOT(A2),B2))"


# ============================================================================
# Binary Conversion Formula Tests
# ============================================================================


def test_binary_to_decimal_formula() -> None:
    """Test binary to decimal conversion formula."""
    formula = BinaryToDecimalFormula()

    # Test metadata
    assert formula.metadata.name == "BINARY_TO_DECIMAL"
    assert formula.metadata.category == "electrical_engineering"
    assert len(formula.metadata.arguments) == 1
    assert formula.metadata.return_type == "number"

    # Test formula building
    result = formula.build('"1010"')
    assert result == 'BIN2DEC("1010")'

    # Test with cell reference
    result = formula.build("A2")
    assert result == "BIN2DEC(A2)"


def test_decimal_to_binary_formula() -> None:
    """Test decimal to binary conversion formula."""
    formula = DecimalToBinaryFormula()

    # Test metadata
    assert formula.metadata.name == "DECIMAL_TO_BINARY"
    assert formula.metadata.category == "electrical_engineering"
    assert len(formula.metadata.arguments) == 1
    assert formula.metadata.return_type == "text"

    # Test formula building
    result = formula.build("10")
    assert result == "DEC2BIN(10)"

    # Test with cell reference
    result = formula.build("A2")
    assert result == "DEC2BIN(A2)"


# ============================================================================
# Validation Tests
# ============================================================================


def test_logic_nand_validation() -> None:
    """Test NAND formula argument validation."""
    formula = LogicNANDFormula()

    # Too few arguments
    with pytest.raises(ValueError, match="at least 2 arguments"):
        formula.build("TRUE")

    # Too many arguments
    with pytest.raises(ValueError, match="at most 2 arguments"):
        formula.build("TRUE", "FALSE", "TRUE")


def test_logic_nor_validation() -> None:
    """Test NOR formula argument validation."""
    formula = LogicNORFormula()

    # Too few arguments
    with pytest.raises(ValueError, match="at least 2 arguments"):
        formula.build("FALSE")

    # Too many arguments
    with pytest.raises(ValueError, match="at most 2 arguments"):
        formula.build("FALSE", "FALSE", "TRUE")


def test_logic_xor_validation() -> None:
    """Test XOR formula argument validation."""
    formula = LogicXORFormula()

    # Too few arguments
    with pytest.raises(ValueError, match="at least 2 arguments"):
        formula.build("TRUE")

    # Too many arguments
    with pytest.raises(ValueError, match="at most 2 arguments"):
        formula.build("TRUE", "FALSE", "TRUE")


def test_binary_to_decimal_validation() -> None:
    """Test binary to decimal formula argument validation."""
    formula = BinaryToDecimalFormula()

    # Too few arguments
    with pytest.raises(ValueError, match="at least 1 arguments"):
        formula.build()

    # Too many arguments
    with pytest.raises(ValueError, match="at most 1 arguments"):
        formula.build('"1010"', '"1111"')


def test_decimal_to_binary_validation() -> None:
    """Test decimal to binary formula argument validation."""
    formula = DecimalToBinaryFormula()

    # Too few arguments
    with pytest.raises(ValueError, match="at least 1 arguments"):
        formula.build()

    # Too many arguments
    with pytest.raises(ValueError, match="at most 1 arguments"):
        formula.build("10", "20")


# ============================================================================
# Metadata Completeness Tests
# ============================================================================


def test_all_digital_formulas_have_complete_metadata() -> None:
    """Ensure all digital formulas have proper metadata."""
    formulas = [
        LogicNANDFormula,
        LogicNORFormula,
        LogicXORFormula,
        BinaryToDecimalFormula,
        DecimalToBinaryFormula,
    ]

    for formula_class in formulas:
        formula = formula_class()
        metadata = formula.metadata

        # Check required metadata fields
        assert metadata.name
        assert metadata.category == "electrical_engineering"
        assert metadata.description
        assert len(metadata.arguments) > 0
        assert metadata.return_type
        assert len(metadata.examples) > 0

        # Check each argument has required fields
        for arg in metadata.arguments:
            assert arg.name
            assert arg.type
            assert isinstance(arg.required, bool)


# ============================================================================
# Formula Examples Tests
# ============================================================================


def test_logic_nand_examples() -> None:
    """Test NAND formula examples are valid."""
    formula = LogicNANDFormula()
    assert len(formula.metadata.examples) >= 1
    # Check examples contain formula name
    for example in formula.metadata.examples:
        assert "LOGIC_NAND" in example or "# " in example


def test_logic_nor_examples() -> None:
    """Test NOR formula examples are valid."""
    formula = LogicNORFormula()
    assert len(formula.metadata.examples) >= 1
    for example in formula.metadata.examples:
        assert "LOGIC_NOR" in example or "# " in example


def test_logic_xor_examples() -> None:
    """Test XOR formula examples are valid."""
    formula = LogicXORFormula()
    assert len(formula.metadata.examples) >= 1
    for example in formula.metadata.examples:
        assert "LOGIC_XOR" in example or "# " in example


def test_binary_to_decimal_examples() -> None:
    """Test binary to decimal formula examples are valid."""
    formula = BinaryToDecimalFormula()
    assert len(formula.metadata.examples) >= 1
    for example in formula.metadata.examples:
        assert "BINARY_TO_DECIMAL" in example or "# " in example


def test_decimal_to_binary_examples() -> None:
    """Test decimal to binary formula examples are valid."""
    formula = DecimalToBinaryFormula()
    assert len(formula.metadata.examples) >= 1
    for example in formula.metadata.examples:
        assert "DECIMAL_TO_BINARY" in example or "# " in example


# ============================================================================
# Edge Cases and Integration Tests
# ============================================================================


def test_logic_gates_with_numeric_values() -> None:
    """Test logic gate formulas with numeric boolean representations."""
    nand = LogicNANDFormula()
    nor = LogicNORFormula()
    xor = LogicXORFormula()

    # Using 1 and 0 (which can represent TRUE/FALSE in spreadsheets)
    assert nand.build("1", "0") == "NOT(AND(1,0))"
    assert nor.build("1", "0") == "NOT(OR(1,0))"
    assert xor.build("1", "0") == "OR(AND(1,NOT(0)),AND(NOT(1),0))"


def test_binary_conversions_with_various_formats() -> None:
    """Test binary conversion formulas with various input formats."""
    bin_to_dec = BinaryToDecimalFormula()
    dec_to_bin = DecimalToBinaryFormula()

    # Different binary string formats
    assert bin_to_dec.build('"00001010"') == 'BIN2DEC("00001010")'
    assert bin_to_dec.build('"1"') == 'BIN2DEC("1")'

    # Different decimal formats
    assert dec_to_bin.build("0") == "DEC2BIN(0)"
    assert dec_to_bin.build("255") == "DEC2BIN(255)"
    assert dec_to_bin.build("C5") == "DEC2BIN(C5)"  # Cell reference
