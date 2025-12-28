"""
Custom exceptions for finance tracker.

Provides a hierarchy of exceptions for better error handling
and programmatic error recovery.
"""

from __future__ import annotations


class FinanceTrackerError(Exception):
    """Base exception for all finance tracker errors."""

    def __init__(self, message: str, error_code: str | None = None) -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error message.
            error_code: Optional machine-readable error code.
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self._default_error_code()

    def _default_error_code(self) -> str:
        """Return default error code based on class name."""
        return self.__class__.__name__.upper()


# File-related exceptions
class FileError(FinanceTrackerError):
    """Base exception for file-related errors."""

    pass


class FileNotFoundError(FileError):
    """Raised when a required file is not found."""

    pass


class InvalidFileFormatError(FileError):
    """Raised when a file has an invalid format."""

    pass


class FileWriteError(FileError):
    """Raised when writing to a file fails."""

    pass


# ODS-specific exceptions
class OdsError(FinanceTrackerError):
    """Base exception for ODS file errors."""

    pass


class OdsReadError(OdsError):
    """Raised when reading an ODS file fails."""

    pass


class OdsWriteError(OdsError):
    """Raised when writing an ODS file fails."""

    pass


class SheetNotFoundError(OdsError):
    """Raised when a required sheet is not found in ODS file."""

    def __init__(
        self, sheet_name: str, available_sheets: list[str] | None = None
    ) -> None:
        """
        Initialize the exception.

        Args:
            sheet_name: Name of the sheet that was not found.
            available_sheets: List of available sheet names.
        """
        self.sheet_name = sheet_name
        self.available_sheets = available_sheets or []

        message = f"Sheet '{sheet_name}' not found"
        if available_sheets:
            message += f". Available sheets: {', '.join(available_sheets)}"

        super().__init__(message, "SHEET_NOT_FOUND")


# Data validation exceptions
class ValidationError(FinanceTrackerError):
    """Base exception for data validation errors."""

    pass


class InvalidAmountError(ValidationError):
    """Raised when an amount value is invalid."""

    def __init__(self, value: str, reason: str = "Invalid format") -> None:
        """
        Initialize the exception.

        Args:
            value: The invalid amount value.
            reason: Reason why the value is invalid.
        """
        self.value = value
        self.reason = reason
        super().__init__(f"Invalid amount '{value}': {reason}", "INVALID_AMOUNT")


class InvalidDateError(ValidationError):
    """Raised when a date value is invalid."""

    def __init__(self, value: str, expected_format: str = "YYYY-MM-DD") -> None:
        """
        Initialize the exception.

        Args:
            value: The invalid date value.
            expected_format: Expected date format.
        """
        self.value = value
        self.expected_format = expected_format
        super().__init__(
            f"Invalid date '{value}'. Expected format: {expected_format}",
            "INVALID_DATE",
        )


class InvalidCategoryError(ValidationError):
    """Raised when a category is not recognized."""

    def __init__(
        self, category: str, valid_categories: list[str] | None = None
    ) -> None:
        """
        Initialize the exception.

        Args:
            category: The invalid category.
            valid_categories: List of valid category names.
        """
        self.category = category
        self.valid_categories = valid_categories or []

        message = f"Invalid category '{category}'"
        if valid_categories:
            message += f". Valid categories: {', '.join(valid_categories)}"

        super().__init__(message, "INVALID_CATEGORY")


# CSV import exceptions
class CSVImportError(FinanceTrackerError):
    """Base exception for CSV import errors."""

    pass


class UnsupportedBankFormatError(CSVImportError):
    """Raised when a bank format is not supported."""

    def __init__(self, bank: str, supported_banks: list[str] | None = None) -> None:
        """
        Initialize the exception.

        Args:
            bank: The unsupported bank name.
            supported_banks: List of supported bank names.
        """
        self.bank = bank
        self.supported_banks = supported_banks or []

        message = f"Unsupported bank format '{bank}'"
        if supported_banks:
            message += f". Supported: {', '.join(supported_banks)}"

        super().__init__(message, "UNSUPPORTED_BANK")


class CSVParseError(CSVImportError):
    """Raised when parsing a CSV file fails."""

    def __init__(self, message: str, line_number: int | None = None) -> None:
        """
        Initialize the exception.

        Args:
            message: Error message.
            line_number: Line number where the error occurred.
        """
        self.line_number = line_number

        if line_number:
            full_message = f"CSV parse error at line {line_number}: {message}"
        else:
            full_message = f"CSV parse error: {message}"

        super().__init__(full_message, "CSV_PARSE_ERROR")


# WebDAV/Nextcloud exceptions
class WebDAVError(FinanceTrackerError):
    """Base exception for WebDAV errors."""

    pass


class ConnectionError(WebDAVError):
    """Raised when connection to WebDAV server fails."""

    pass


class AuthenticationError(WebDAVError):
    """Raised when WebDAV authentication fails."""

    pass


class UploadError(WebDAVError):
    """Raised when uploading a file fails."""

    pass


class DownloadError(WebDAVError):
    """Raised when downloading a file fails."""

    pass


# Configuration exceptions
class ConfigurationError(FinanceTrackerError):
    """Base exception for configuration errors."""

    pass


class MissingConfigError(ConfigurationError):
    """Raised when required configuration is missing."""

    def __init__(self, config_key: str, config_source: str = "environment") -> None:
        """
        Initialize the exception.

        Args:
            config_key: Name of the missing configuration key.
            config_source: Where the configuration should be set.
        """
        self.config_key = config_key
        self.config_source = config_source
        super().__init__(
            f"Missing required configuration '{config_key}' in {config_source}",
            "MISSING_CONFIG",
        )


class InvalidConfigError(ConfigurationError):
    """Raised when configuration value is invalid."""

    pass


# Template exceptions
class TemplateError(FinanceTrackerError):
    """Base exception for template errors."""

    pass


class TemplateNotFoundError(TemplateError):
    """Raised when a template is not found."""

    def __init__(
        self, template_name: str, available_templates: list[str] | None = None
    ) -> None:
        """
        Initialize the exception.

        Args:
            template_name: Name of the template that was not found.
            available_templates: List of available template names.
        """
        self.template_name = template_name
        self.available_templates = available_templates or []

        message = f"Template '{template_name}' not found"
        if available_templates:
            message += f". Available: {', '.join(available_templates)}"

        super().__init__(message, "TEMPLATE_NOT_FOUND")
