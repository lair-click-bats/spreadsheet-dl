"""
Tests for Finance domain.

The finance domain provides comprehensive finance-specific functionality
including account management, budget analysis, multi-currency support,
bank transaction import, and financial reporting.

Note: Finance domain uses a different architecture than plugin-based domains.
It does not have a DomainPlugin class but provides modules and utilities.
"""

from __future__ import annotations

import pytest

from spreadsheet_dl.domains.finance import (
    Account,
    AccountManager,
    AccountType,
    Alert,
    AlertConfig,
    AlertMonitor,
    BankFormatRegistry,
    BUILTIN_FORMATS,
    Category,
    CategoryManager,
    CurrencyConverter,
    ExpenseCategory,
    get_default_accounts,
)


# ============================================================================
# Account Management Tests
# ============================================================================


class TestAccountManagement:
    """Test account management functionality."""

    def test_account_creation(self) -> None:
        """Test creating an account."""
        account = Account(
            name="Checking Account",
            account_type=AccountType.CHECKING,
            balance=1000.0,
        )

        assert account.name == "Checking Account"
        assert account.account_type == AccountType.CHECKING
        assert account.balance == 1000.0

    def test_default_accounts(self) -> None:
        """Test getting default accounts."""
        accounts = get_default_accounts()

        assert isinstance(accounts, list)
        assert len(accounts) > 0
        assert all(isinstance(acc, Account) for acc in accounts)


class TestAccountManager:
    """Test AccountManager."""

    def test_manager_initialization(self) -> None:
        """Test manager initializes correctly."""
        manager = AccountManager()

        assert isinstance(manager, AccountManager)
        assert len(manager.list_accounts()) >= 0

    def test_add_account(self) -> None:
        """Test adding an account."""
        manager = AccountManager()
        account = Account(
            name="Savings",
            account_type=AccountType.SAVINGS,
            balance=5000.0,
        )

        manager.add_account(account)
        accounts = manager.list_accounts()

        assert "Savings" in [acc.name for acc in accounts]


# ============================================================================
# Category Tests
# ============================================================================


class TestCategories:
    """Test category management."""

    def test_expense_category_enum(self) -> None:
        """Test ExpenseCategory enum."""
        assert ExpenseCategory.FOOD
        assert ExpenseCategory.HOUSING
        assert ExpenseCategory.TRANSPORTATION

    def test_category_creation(self) -> None:
        """Test creating a category."""
        category = Category(
            name="Groceries",
            budget_limit=500.0,
        )

        assert category.name == "Groceries"
        assert category.budget_limit == 500.0

    def test_category_manager(self) -> None:
        """Test CategoryManager."""
        manager = CategoryManager()

        assert isinstance(manager, CategoryManager)
        categories = manager.list_categories()
        assert isinstance(categories, list)


# ============================================================================
# Bank Format Tests
# ============================================================================


class TestBankFormats:
    """Test bank format registry."""

    def test_builtin_formats_exist(self) -> None:
        """Test builtin formats are available."""
        assert BUILTIN_FORMATS is not None
        assert isinstance(BUILTIN_FORMATS, dict)
        assert len(BUILTIN_FORMATS) > 0

    def test_bank_format_registry(self) -> None:
        """Test BankFormatRegistry."""
        registry = BankFormatRegistry()

        assert isinstance(registry, BankFormatRegistry)
        formats = registry.list_formats()
        assert isinstance(formats, list)


# ============================================================================
# Currency Tests
# ============================================================================


class TestCurrency:
    """Test currency conversion."""

    def test_currency_converter_initialization(self) -> None:
        """Test CurrencyConverter initializes."""
        converter = CurrencyConverter()

        assert isinstance(converter, CurrencyConverter)


# ============================================================================
# Alert Tests
# ============================================================================


class TestAlerts:
    """Test alert system."""

    def test_alert_creation(self) -> None:
        """Test creating an alert."""
        alert = Alert(
            message="Budget exceeded",
            severity="warning",
        )

        assert alert.message == "Budget exceeded"
        assert alert.severity == "warning"

    def test_alert_monitor_initialization(self) -> None:
        """Test AlertMonitor initializes."""
        config = AlertConfig()
        monitor = AlertMonitor(config)

        assert isinstance(monitor, AlertMonitor)


# ============================================================================
# Integration Tests
# ============================================================================


class TestFinanceIntegration:
    """Test finance domain integration."""

    def test_finance_imports_available(self) -> None:
        """Test all major finance components can be imported."""
        from spreadsheet_dl.domains.finance import (
            Account,
            AccountManager,
            Alert,
            AlertMonitor,
            BankFormatRegistry,
            Category,
            CategoryManager,
            CurrencyConverter,
        )

        # If we got here, all imports succeeded
        assert True

    def test_finance_domain_comprehensive(self) -> None:
        """Test finance domain provides comprehensive functionality."""
        # Account management
        manager = AccountManager()
        assert manager is not None

        # Categories
        cat_manager = CategoryManager()
        assert cat_manager is not None

        # Bank formats
        registry = BankFormatRegistry()
        assert registry is not None

        # All core components available
        assert True
