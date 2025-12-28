"""Tests for custom exceptions."""

from __future__ import annotations

from finance_tracker.exceptions import (
    ConfigurationError,
    CSVImportError,
    CSVParseError,
    FileError,
    FinanceTrackerError,
    InvalidAmountError,
    InvalidCategoryError,
    InvalidDateError,
    MissingConfigError,
    OdsError,
    OdsReadError,
    SheetNotFoundError,
    TemplateError,
    TemplateNotFoundError,
    UnsupportedBankFormatError,
    ValidationError,
    WebDAVError,
)


class TestFinanceTrackerError:
    """Tests for base exception class."""

    def test_error_message(self) -> None:
        """Test error message is stored correctly."""
        error = FinanceTrackerError("Test error message")
        assert str(error) == "Test error message"
        assert error.message == "Test error message"

    def test_default_error_code(self) -> None:
        """Test default error code is class name."""
        error = FinanceTrackerError("Test")
        assert error.error_code == "FINANCETRACKERERROR"

    def test_custom_error_code(self) -> None:
        """Test custom error code."""
        error = FinanceTrackerError("Test", error_code="CUSTOM_CODE")
        assert error.error_code == "CUSTOM_CODE"


class TestValidationErrors:
    """Tests for validation exception classes."""

    def test_invalid_amount_error(self) -> None:
        """Test InvalidAmountError."""
        error = InvalidAmountError("abc123", "Not a valid number")
        assert "abc123" in str(error)
        assert "Not a valid number" in str(error)
        assert error.value == "abc123"
        assert error.reason == "Not a valid number"
        assert error.error_code == "INVALID_AMOUNT"

    def test_invalid_date_error(self) -> None:
        """Test InvalidDateError."""
        error = InvalidDateError("13-2025-01")
        assert "13-2025-01" in str(error)
        assert "YYYY-MM-DD" in str(error)
        assert error.value == "13-2025-01"
        assert error.error_code == "INVALID_DATE"

    def test_invalid_date_error_custom_format(self) -> None:
        """Test InvalidDateError with custom format."""
        error = InvalidDateError("bad-date", expected_format="DD/MM/YYYY")
        assert "DD/MM/YYYY" in str(error)
        assert error.expected_format == "DD/MM/YYYY"

    def test_invalid_category_error(self) -> None:
        """Test InvalidCategoryError."""
        error = InvalidCategoryError(
            "NotACategory", ["Groceries", "Housing", "Utilities"]
        )
        assert "NotACategory" in str(error)
        assert "Groceries" in str(error)
        assert error.category == "NotACategory"
        assert "Groceries" in error.valid_categories
        assert error.error_code == "INVALID_CATEGORY"


class TestOdsErrors:
    """Tests for ODS exception classes."""

    def test_sheet_not_found_error(self) -> None:
        """Test SheetNotFoundError."""
        error = SheetNotFoundError("Missing Sheet", ["Sheet1", "Sheet2"])
        assert "Missing Sheet" in str(error)
        assert "Sheet1" in str(error)
        assert error.sheet_name == "Missing Sheet"
        assert "Sheet1" in error.available_sheets
        assert error.error_code == "SHEET_NOT_FOUND"

    def test_sheet_not_found_error_no_available(self) -> None:
        """Test SheetNotFoundError without available sheets."""
        error = SheetNotFoundError("Missing Sheet")
        assert "Missing Sheet" in str(error)
        assert error.available_sheets == []


class TestCSVImportErrors:
    """Tests for CSV import exception classes."""

    def test_unsupported_bank_format_error(self) -> None:
        """Test UnsupportedBankFormatError."""
        error = UnsupportedBankFormatError(
            "MyBank", ["chase", "bank_of_america", "wells_fargo"]
        )
        assert "MyBank" in str(error)
        assert "chase" in str(error)
        assert error.bank == "MyBank"
        assert "chase" in error.supported_banks
        assert error.error_code == "UNSUPPORTED_BANK"

    def test_csv_parse_error(self) -> None:
        """Test CSVParseError."""
        error = CSVParseError("Missing column", line_number=42)
        assert "Missing column" in str(error)
        assert "line 42" in str(error)
        assert error.line_number == 42
        assert error.error_code == "CSV_PARSE_ERROR"

    def test_csv_parse_error_no_line(self) -> None:
        """Test CSVParseError without line number."""
        error = CSVParseError("General error")
        assert "General error" in str(error)
        assert error.line_number is None


class TestConfigurationErrors:
    """Tests for configuration exception classes."""

    def test_missing_config_error(self) -> None:
        """Test MissingConfigError."""
        error = MissingConfigError("NEXTCLOUD_URL", "environment")
        assert "NEXTCLOUD_URL" in str(error)
        assert "environment" in str(error)
        assert error.config_key == "NEXTCLOUD_URL"
        assert error.config_source == "environment"
        assert error.error_code == "MISSING_CONFIG"


class TestTemplateErrors:
    """Tests for template exception classes."""

    def test_template_not_found_error(self) -> None:
        """Test TemplateNotFoundError."""
        error = TemplateNotFoundError(
            "my_template", ["50_30_20", "family", "minimalist"]
        )
        assert "my_template" in str(error)
        assert "50_30_20" in str(error)
        assert error.template_name == "my_template"
        assert "50_30_20" in error.available_templates
        assert error.error_code == "TEMPLATE_NOT_FOUND"


class TestExceptionHierarchy:
    """Tests for exception class hierarchy."""

    def test_file_error_is_finance_tracker_error(self) -> None:
        """Test FileError inherits from FinanceTrackerError."""
        assert issubclass(FileError, FinanceTrackerError)

    def test_ods_error_is_finance_tracker_error(self) -> None:
        """Test OdsError inherits from FinanceTrackerError."""
        assert issubclass(OdsError, FinanceTrackerError)

    def test_validation_error_is_finance_tracker_error(self) -> None:
        """Test ValidationError inherits from FinanceTrackerError."""
        assert issubclass(ValidationError, FinanceTrackerError)

    def test_csv_import_error_is_finance_tracker_error(self) -> None:
        """Test CSVImportError inherits from FinanceTrackerError."""
        assert issubclass(CSVImportError, FinanceTrackerError)

    def test_webdav_error_is_finance_tracker_error(self) -> None:
        """Test WebDAVError inherits from FinanceTrackerError."""
        assert issubclass(WebDAVError, FinanceTrackerError)

    def test_configuration_error_is_finance_tracker_error(self) -> None:
        """Test ConfigurationError inherits from FinanceTrackerError."""
        assert issubclass(ConfigurationError, FinanceTrackerError)

    def test_template_error_is_finance_tracker_error(self) -> None:
        """Test TemplateError inherits from FinanceTrackerError."""
        assert issubclass(TemplateError, FinanceTrackerError)

    def test_ods_read_error_is_ods_error(self) -> None:
        """Test OdsReadError inherits from OdsError."""
        assert issubclass(OdsReadError, OdsError)

    def test_can_catch_base_exception(self) -> None:
        """Test catching FinanceTrackerError catches all subclasses."""
        errors = [
            FileError("test"),
            OdsError("test"),
            ValidationError("test"),
            CSVImportError("test"),
            WebDAVError("test"),
            ConfigurationError("test"),
            TemplateError("test"),
        ]

        for error in errors:
            try:
                raise error
            except FinanceTrackerError as e:
                assert e.message == "test"
