"""
Backward compatibility shim for currency module.

This module has been moved to spreadsheet_dl.domains.finance.currency.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.currency import (
    Currency,
    CurrencyCode,
    CurrencyConverter,
    ExchangeRate,
    ExchangeRateProvider,
    MoneyAmount,
    convert,
    format_currency,
    get_currency,
    list_currencies,
    money,
)

__all__ = [
    "Currency",
    "CurrencyCode",
    "CurrencyConverter",
    "ExchangeRate",
    "ExchangeRateProvider",
    "MoneyAmount",
    "convert",
    "format_currency",
    "get_currency",
    "list_currencies",
    "money",
]
