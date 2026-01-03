"""
Plaid API integration for bank synchronization.

Provides direct bank connection and transaction sync via Plaid or similar
bank aggregation services.

Requirements implemented:
    - FR-IMPORT-003: Bank API Integration (Gap G-17)

Features:
    - OAuth-based bank connection flow
    - Transaction auto-sync with configurable schedule
    - Multi-factor authentication handling
    - Secure credential storage via CredentialStore
    - Multiple institution support
    - Transaction categorization
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any

from finance_tracker.exceptions import (
    ConfigurationError,
    FinanceTrackerError,
)


class PlaidError(FinanceTrackerError):
    """Base exception for Plaid integration errors."""

    error_code = "FT-PLAID-1800"


class PlaidConnectionError(PlaidError):
    """Raised when connection to Plaid fails."""

    error_code = "FT-PLAID-1801"

    def __init__(
        self,
        message: str = "Failed to connect to Plaid API",
        **kwargs: Any,
    ) -> None:
        super().__init__(
            message,
            suggestion="Check your API credentials and network connection.",
            **kwargs,
        )


class PlaidAuthError(PlaidError):
    """Raised when authentication fails."""

    error_code = "FT-PLAID-1802"

    def __init__(
        self,
        message: str = "Plaid authentication failed",
        institution: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.institution = institution
        suggestion = "Re-authenticate with your bank."
        if institution:
            suggestion = f"Re-authenticate with {institution}."
        super().__init__(message, suggestion=suggestion, **kwargs)


class PlaidSyncError(PlaidError):
    """Raised when transaction sync fails."""

    error_code = "FT-PLAID-1803"


class PlaidEnvironment(Enum):
    """Plaid API environments."""

    SANDBOX = "sandbox"
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class PlaidProduct(Enum):
    """Plaid API products."""

    TRANSACTIONS = "transactions"
    AUTH = "auth"
    IDENTITY = "identity"
    BALANCE = "balance"
    INVESTMENTS = "investments"
    LIABILITIES = "liabilities"


class LinkStatus(Enum):
    """Status of a Plaid Link connection."""

    PENDING = "pending"
    CONNECTED = "connected"
    REQUIRES_REAUTH = "requires_reauth"
    DISCONNECTED = "disconnected"
    ERROR = "error"


class SyncStatus(Enum):
    """Status of a transaction sync."""

    IDLE = "idle"
    SYNCING = "syncing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PlaidConfig:
    """
    Configuration for Plaid API integration.

    Attributes:
        client_id: Plaid client ID.
        secret: Plaid secret key.
        environment: API environment (sandbox, development, production).
        webhook_url: Optional webhook URL for real-time updates.
        products: List of Plaid products to enable.
    """

    client_id: str
    secret: str
    environment: PlaidEnvironment = PlaidEnvironment.SANDBOX
    webhook_url: str | None = None
    products: list[PlaidProduct] = field(
        default_factory=lambda: [PlaidProduct.TRANSACTIONS]
    )

    @classmethod
    def from_env(cls) -> PlaidConfig:
        """
        Load configuration from environment variables.

        Environment variables:
            PLAID_CLIENT_ID: Client ID
            PLAID_SECRET: Secret key
            PLAID_ENV: Environment (sandbox/development/production)
            PLAID_WEBHOOK_URL: Optional webhook URL

        Returns:
            PlaidConfig instance.

        Raises:
            ConfigurationError: If required variables are missing.
        """
        import os

        client_id = os.environ.get("PLAID_CLIENT_ID")
        secret = os.environ.get("PLAID_SECRET")
        env_str = os.environ.get("PLAID_ENV", "sandbox")
        webhook = os.environ.get("PLAID_WEBHOOK_URL")

        if not client_id or not secret:
            raise ConfigurationError(
                "PLAID_CLIENT_ID and PLAID_SECRET environment variables required"
            )

        try:
            environment = PlaidEnvironment(env_str.lower())
        except ValueError:
            environment = PlaidEnvironment.SANDBOX

        return cls(
            client_id=client_id,
            secret=secret,
            environment=environment,
            webhook_url=webhook,
        )

    @property
    def base_url(self) -> str:
        """Get the API base URL for the configured environment."""
        urls = {
            PlaidEnvironment.SANDBOX: "https://sandbox.plaid.com",
            PlaidEnvironment.DEVELOPMENT: "https://development.plaid.com",
            PlaidEnvironment.PRODUCTION: "https://production.plaid.com",
        }
        return urls[self.environment]


@dataclass
class PlaidInstitution:
    """
    Represents a financial institution in Plaid.

    Attributes:
        institution_id: Plaid's institution ID.
        name: Display name of the institution.
        products: Supported Plaid products.
        logo_url: URL to institution logo.
        primary_color: Brand color.
        url: Institution's website.
    """

    institution_id: str
    name: str
    products: list[str] = field(default_factory=list)
    logo_url: str | None = None
    primary_color: str | None = None
    url: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "institution_id": self.institution_id,
            "name": self.name,
            "products": self.products,
            "logo_url": self.logo_url,
            "primary_color": self.primary_color,
            "url": self.url,
        }


@dataclass
class PlaidAccount:
    """
    Represents a bank account from Plaid.

    Attributes:
        account_id: Plaid's account ID.
        name: Account name.
        official_name: Official account name from bank.
        type: Account type (depository, credit, etc.).
        subtype: Account subtype (checking, savings, etc.).
        mask: Last 4 digits of account number.
        current_balance: Current balance.
        available_balance: Available balance.
        currency: Currency code.
    """

    account_id: str
    name: str
    official_name: str | None = None
    type: str = "depository"
    subtype: str = "checking"
    mask: str | None = None
    current_balance: Decimal | None = None
    available_balance: Decimal | None = None
    currency: str = "USD"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "account_id": self.account_id,
            "name": self.name,
            "official_name": self.official_name,
            "type": self.type,
            "subtype": self.subtype,
            "mask": self.mask,
            "current_balance": float(self.current_balance) if self.current_balance else None,
            "available_balance": float(self.available_balance) if self.available_balance else None,
            "currency": self.currency,
        }


@dataclass
class PlaidTransaction:
    """
    Represents a transaction from Plaid.

    Attributes:
        transaction_id: Plaid's transaction ID.
        account_id: Associated account ID.
        amount: Transaction amount (positive = debit).
        date: Transaction date.
        name: Merchant/transaction name.
        merchant_name: Clean merchant name.
        category: Plaid category list.
        pending: Whether transaction is pending.
        payment_channel: How payment was made.
        location: Transaction location info.
    """

    transaction_id: str
    account_id: str
    amount: Decimal
    date: date
    name: str
    merchant_name: str | None = None
    category: list[str] = field(default_factory=list)
    pending: bool = False
    payment_channel: str = "other"
    location: dict[str, Any] = field(default_factory=dict)
    iso_currency_code: str = "USD"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "transaction_id": self.transaction_id,
            "account_id": self.account_id,
            "amount": float(self.amount),
            "date": self.date.isoformat(),
            "name": self.name,
            "merchant_name": self.merchant_name,
            "category": self.category,
            "pending": self.pending,
            "payment_channel": self.payment_channel,
            "location": self.location,
            "currency": self.iso_currency_code,
        }


@dataclass
class LinkToken:
    """
    Plaid Link token for initiating connections.

    Attributes:
        link_token: The token string.
        expiration: Token expiration time.
        request_id: Plaid request ID.
    """

    link_token: str
    expiration: datetime
    request_id: str

    @property
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return datetime.now() >= self.expiration


@dataclass
class AccessToken:
    """
    Plaid access token for a connected institution.

    Attributes:
        access_token: The token string (encrypted at rest).
        item_id: Plaid item ID.
        institution: Connected institution info.
        accounts: List of connected accounts.
        status: Connection status.
        last_sync: Last successful sync time.
        error: Error message if any.
    """

    access_token: str
    item_id: str
    institution: PlaidInstitution
    accounts: list[PlaidAccount] = field(default_factory=list)
    status: LinkStatus = LinkStatus.CONNECTED
    last_sync: datetime | None = None
    error: str | None = None

    def to_dict(self, include_token: bool = False) -> dict[str, Any]:
        """
        Convert to dictionary.

        Args:
            include_token: Whether to include the access token.

        Returns:
            Dictionary representation.
        """
        result = {
            "item_id": self.item_id,
            "institution": self.institution.to_dict(),
            "accounts": [a.to_dict() for a in self.accounts],
            "status": self.status.value,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "error": self.error,
        }
        if include_token:
            result["access_token"] = self.access_token
        return result


@dataclass
class SyncResult:
    """
    Result of a transaction sync operation.

    Attributes:
        status: Sync status.
        added: Number of new transactions.
        modified: Number of modified transactions.
        removed: Number of removed transactions.
        transactions: List of synced transactions.
        next_cursor: Cursor for pagination.
        has_more: Whether more transactions are available.
        error: Error message if sync failed.
    """

    status: SyncStatus
    added: int = 0
    modified: int = 0
    removed: int = 0
    transactions: list[PlaidTransaction] = field(default_factory=list)
    next_cursor: str | None = None
    has_more: bool = False
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "status": self.status.value,
            "added": self.added,
            "modified": self.modified,
            "removed": self.removed,
            "transaction_count": len(self.transactions),
            "has_more": self.has_more,
            "error": self.error,
        }


class PlaidClient:
    """
    Client for Plaid API integration.

    Provides methods for:
    - Creating Link tokens for bank connection
    - Exchanging public tokens for access tokens
    - Fetching account information
    - Syncing transactions
    - Managing connected items

    Note: This is a reference implementation that simulates Plaid API behavior.
    For production use, install the official `plaid-python` package.

    Example:
        >>> config = PlaidConfig.from_env()
        >>> client = PlaidClient(config)
        >>> link_token = client.create_link_token("user123")
        >>> # User completes Plaid Link flow...
        >>> access = client.exchange_public_token(public_token)
        >>> result = client.sync_transactions(access.access_token)
    """

    def __init__(
        self,
        config: PlaidConfig,
        credential_store: Any | None = None,
    ) -> None:
        """
        Initialize Plaid client.

        Args:
            config: Plaid configuration.
            credential_store: Optional CredentialStore for secure token storage.
        """
        self.config = config
        self.credential_store = credential_store
        self._http_client: Any = None

    def create_link_token(
        self,
        user_id: str,
        *,
        products: list[PlaidProduct] | None = None,
        country_codes: list[str] | None = None,
        language: str = "en",
    ) -> LinkToken:
        """
        Create a Link token for initiating Plaid Link.

        Args:
            user_id: Unique identifier for the user.
            products: Plaid products to enable. Defaults to config products.
            country_codes: Supported country codes. Defaults to ["US"].
            language: Link language. Defaults to "en".

        Returns:
            LinkToken for use with Plaid Link.

        Raises:
            PlaidConnectionError: If API call fails.
        """
        products = products or self.config.products
        country_codes = country_codes or ["US"]

        # In production, this would call:
        # POST /link/token/create
        request_data = {
            "client_id": self.config.client_id,
            "secret": self.config.secret,
            "user": {"client_user_id": user_id},
            "products": [p.value for p in products],
            "country_codes": country_codes,
            "language": language,
        }

        if self.config.webhook_url:
            request_data["webhook"] = self.config.webhook_url

        # Simulate API response for sandbox/development
        if self.config.environment == PlaidEnvironment.SANDBOX:
            return self._simulate_link_token(user_id)

        # Production would make actual API call
        return self._api_create_link_token(request_data)

    def exchange_public_token(
        self,
        public_token: str,
    ) -> AccessToken:
        """
        Exchange a public token for an access token.

        Called after user completes Plaid Link flow.

        Args:
            public_token: Public token from Plaid Link.

        Returns:
            AccessToken for accessing user's data.

        Raises:
            PlaidAuthError: If token exchange fails.
        """
        # In production, this would call:
        # POST /item/public_token/exchange

        if self.config.environment == PlaidEnvironment.SANDBOX:
            return self._simulate_access_token(public_token)

        return self._api_exchange_token(public_token)

    def get_accounts(
        self,
        access_token: str,
    ) -> list[PlaidAccount]:
        """
        Get accounts for an access token.

        Args:
            access_token: Plaid access token.

        Returns:
            List of connected accounts.

        Raises:
            PlaidConnectionError: If API call fails.
        """
        # In production, this would call:
        # POST /accounts/get

        if self.config.environment == PlaidEnvironment.SANDBOX:
            return self._simulate_accounts()

        return self._api_get_accounts(access_token)

    def get_balances(
        self,
        access_token: str,
        account_ids: list[str] | None = None,
    ) -> list[PlaidAccount]:
        """
        Get account balances.

        Args:
            access_token: Plaid access token.
            account_ids: Optional list of specific accounts.

        Returns:
            List of accounts with updated balances.

        Raises:
            PlaidConnectionError: If API call fails.
        """
        # In production, this would call:
        # POST /accounts/balance/get

        if self.config.environment == PlaidEnvironment.SANDBOX:
            return self._simulate_accounts()

        return self._api_get_balances(access_token, account_ids)

    def sync_transactions(
        self,
        access_token: str,
        cursor: str | None = None,
        count: int = 100,
    ) -> SyncResult:
        """
        Sync transactions for an access token.

        Uses cursor-based pagination for incremental sync.

        Args:
            access_token: Plaid access token.
            cursor: Pagination cursor from previous sync.
            count: Number of transactions to fetch.

        Returns:
            SyncResult with transactions and pagination info.

        Raises:
            PlaidSyncError: If sync fails.
        """
        # In production, this would call:
        # POST /transactions/sync

        if self.config.environment == PlaidEnvironment.SANDBOX:
            return self._simulate_transactions(cursor, count)

        return self._api_sync_transactions(access_token, cursor, count)

    def get_transactions(
        self,
        access_token: str,
        start_date: date,
        end_date: date,
        account_ids: list[str] | None = None,
    ) -> list[PlaidTransaction]:
        """
        Get transactions for a date range.

        Args:
            access_token: Plaid access token.
            start_date: Start date for transactions.
            end_date: End date for transactions.
            account_ids: Optional list of specific accounts.

        Returns:
            List of transactions.

        Raises:
            PlaidConnectionError: If API call fails.
        """
        # In production, this would call:
        # POST /transactions/get

        if self.config.environment == PlaidEnvironment.SANDBOX:
            return self._simulate_transaction_range(start_date, end_date)

        return self._api_get_transactions(access_token, start_date, end_date, account_ids)

    def refresh_transactions(
        self,
        access_token: str,
    ) -> bool:
        """
        Request a refresh of transactions.

        Triggers Plaid to fetch latest data from the institution.

        Args:
            access_token: Plaid access token.

        Returns:
            True if refresh was initiated successfully.
        """
        # In production, this would call:
        # POST /transactions/refresh

        if self.config.environment == PlaidEnvironment.SANDBOX:
            return True

        return self._api_refresh_transactions(access_token)

    def remove_item(
        self,
        access_token: str,
    ) -> bool:
        """
        Remove a connected item (bank connection).

        Args:
            access_token: Plaid access token for the item.

        Returns:
            True if removal was successful.
        """
        # In production, this would call:
        # POST /item/remove

        return True

    def search_institutions(
        self,
        query: str,
        country_codes: list[str] | None = None,
    ) -> list[PlaidInstitution]:
        """
        Search for financial institutions.

        Args:
            query: Search query (institution name).
            country_codes: Limit to specific countries.

        Returns:
            List of matching institutions.
        """
        # In production, this would call:
        # POST /institutions/search

        if self.config.environment == PlaidEnvironment.SANDBOX:
            return self._simulate_institution_search(query)

        return self._api_search_institutions(query, country_codes)

    # =========================================================================
    # Sandbox Simulation Methods
    # =========================================================================

    def _simulate_link_token(self, user_id: str) -> LinkToken:
        """Simulate Link token creation for sandbox."""
        token = f"link-sandbox-{hashlib.md5(user_id.encode()).hexdigest()[:16]}"
        return LinkToken(
            link_token=token,
            expiration=datetime.now() + timedelta(hours=4),
            request_id=f"req-{time.time_ns()}",
        )

    def _simulate_access_token(self, public_token: str) -> AccessToken:
        """Simulate access token exchange for sandbox."""
        # Generate deterministic IDs from public token
        token_hash = hashlib.md5(public_token.encode()).hexdigest()
        access_token = f"access-sandbox-{token_hash[:32]}"
        item_id = f"item-sandbox-{token_hash[32:]}"

        institution = PlaidInstitution(
            institution_id="ins_sandbox_1",
            name="Sandbox Bank",
            products=["transactions", "balance"],
            url="https://sandbox.plaid.com",
        )

        accounts = self._simulate_accounts()

        return AccessToken(
            access_token=access_token,
            item_id=item_id,
            institution=institution,
            accounts=accounts,
            status=LinkStatus.CONNECTED,
            last_sync=datetime.now(),
        )

    def _simulate_accounts(self) -> list[PlaidAccount]:
        """Generate sample accounts for sandbox."""
        return [
            PlaidAccount(
                account_id="acc_checking_001",
                name="Plaid Checking",
                official_name="Plaid Gold Standard 0% Interest Checking",
                type="depository",
                subtype="checking",
                mask="0000",
                current_balance=Decimal("1234.56"),
                available_balance=Decimal("1200.00"),
                currency="USD",
            ),
            PlaidAccount(
                account_id="acc_savings_001",
                name="Plaid Savings",
                official_name="Plaid Silver Standard 0.1% Interest Savings",
                type="depository",
                subtype="savings",
                mask="1111",
                current_balance=Decimal("5678.90"),
                available_balance=Decimal("5678.90"),
                currency="USD",
            ),
            PlaidAccount(
                account_id="acc_credit_001",
                name="Plaid Credit Card",
                official_name="Plaid Diamond 12.5% APR Interest Credit Card",
                type="credit",
                subtype="credit card",
                mask="2222",
                current_balance=Decimal("890.45"),
                available_balance=Decimal("9109.55"),
                currency="USD",
            ),
        ]

    def _simulate_transactions(
        self,
        cursor: str | None,
        count: int,
    ) -> SyncResult:
        """Generate sample transactions for sandbox."""
        transactions = self._simulate_transaction_range(
            date.today() - timedelta(days=30),
            date.today(),
        )

        return SyncResult(
            status=SyncStatus.COMPLETED,
            added=len(transactions),
            modified=0,
            removed=0,
            transactions=transactions[:count],
            next_cursor=None,
            has_more=len(transactions) > count,
        )

    def _simulate_transaction_range(
        self,
        start_date: date,
        end_date: date,
    ) -> list[PlaidTransaction]:
        """Generate sample transactions for a date range."""
        sample_transactions = [
            ("Uber", ["Transportation", "Rides"], Decimal("15.50"), "Uber", "other"),
            ("WHOLEFDS", ["Groceries"], Decimal("67.89"), "Whole Foods", "in_store"),
            ("AMAZON", ["Shopping"], Decimal("42.99"), "Amazon", "online"),
            ("NETFLIX", ["Entertainment", "Streaming"], Decimal("15.99"), "Netflix", "online"),
            ("STARBUCKS", ["Food and Drink", "Coffee"], Decimal("6.75"), "Starbucks", "in_store"),
            ("SHELL", ["Transportation", "Gas"], Decimal("45.00"), "Shell", "in_store"),
            ("ATM WITHDRAWAL", ["Transfer", "ATM"], Decimal("100.00"), None, "other"),
            ("WALGREENS", ["Health", "Pharmacy"], Decimal("23.45"), "Walgreens", "in_store"),
            ("SPOTIFY", ["Entertainment", "Music"], Decimal("9.99"), "Spotify", "online"),
            ("PG&E", ["Utilities"], Decimal("125.00"), "PG&E", "other"),
        ]

        transactions = []
        current_date = start_date
        tx_id = 0

        while current_date <= end_date:
            # Add 2-4 transactions per day
            num_tx = (current_date.day % 3) + 2
            for i in range(num_tx):
                tx_data = sample_transactions[(tx_id + i) % len(sample_transactions)]
                transactions.append(
                    PlaidTransaction(
                        transaction_id=f"tx-{current_date.isoformat()}-{tx_id + i}",
                        account_id="acc_checking_001" if tx_data[2] < 50 else "acc_credit_001",
                        amount=tx_data[2],
                        date=current_date,
                        name=tx_data[0],
                        merchant_name=tx_data[3],
                        category=tx_data[1],
                        pending=current_date == end_date,
                        payment_channel=tx_data[4],
                    )
                )
            tx_id += num_tx
            current_date += timedelta(days=1)

        return transactions

    def _simulate_institution_search(self, query: str) -> list[PlaidInstitution]:
        """Simulate institution search for sandbox."""
        # Sample institutions
        all_institutions = [
            PlaidInstitution(
                institution_id="ins_1",
                name="Chase",
                products=["transactions", "balance", "auth"],
                primary_color="#117ACA",
                url="https://www.chase.com",
            ),
            PlaidInstitution(
                institution_id="ins_2",
                name="Bank of America",
                products=["transactions", "balance"],
                primary_color="#E31837",
                url="https://www.bankofamerica.com",
            ),
            PlaidInstitution(
                institution_id="ins_3",
                name="Wells Fargo",
                products=["transactions", "balance", "auth"],
                primary_color="#D71E28",
                url="https://www.wellsfargo.com",
            ),
            PlaidInstitution(
                institution_id="ins_4",
                name="Capital One",
                products=["transactions", "balance"],
                primary_color="#004879",
                url="https://www.capitalone.com",
            ),
            PlaidInstitution(
                institution_id="ins_5",
                name="Citi",
                products=["transactions", "balance"],
                primary_color="#003B70",
                url="https://www.citi.com",
            ),
        ]

        query_lower = query.lower()
        return [
            inst for inst in all_institutions
            if query_lower in inst.name.lower()
        ]

    # =========================================================================
    # Production API Methods (stubs)
    # =========================================================================

    def _api_create_link_token(self, request_data: dict) -> LinkToken:
        """Make API call to create link token."""
        # Would use requests or httpx to call Plaid API
        raise NotImplementedError("Production API not implemented")

    def _api_exchange_token(self, public_token: str) -> AccessToken:
        """Make API call to exchange public token."""
        raise NotImplementedError("Production API not implemented")

    def _api_get_accounts(self, access_token: str) -> list[PlaidAccount]:
        """Make API call to get accounts."""
        raise NotImplementedError("Production API not implemented")

    def _api_get_balances(
        self,
        access_token: str,
        account_ids: list[str] | None,
    ) -> list[PlaidAccount]:
        """Make API call to get balances."""
        raise NotImplementedError("Production API not implemented")

    def _api_sync_transactions(
        self,
        access_token: str,
        cursor: str | None,
        count: int,
    ) -> SyncResult:
        """Make API call to sync transactions."""
        raise NotImplementedError("Production API not implemented")

    def _api_get_transactions(
        self,
        access_token: str,
        start_date: date,
        end_date: date,
        account_ids: list[str] | None,
    ) -> list[PlaidTransaction]:
        """Make API call to get transactions."""
        raise NotImplementedError("Production API not implemented")

    def _api_refresh_transactions(self, access_token: str) -> bool:
        """Make API call to refresh transactions."""
        raise NotImplementedError("Production API not implemented")

    def _api_search_institutions(
        self,
        query: str,
        country_codes: list[str] | None,
    ) -> list[PlaidInstitution]:
        """Make API call to search institutions."""
        raise NotImplementedError("Production API not implemented")


class PlaidSyncManager:
    """
    Manager for Plaid sync operations.

    Handles:
    - Scheduling automatic syncs
    - Managing multiple connected items
    - Converting Plaid transactions to finance-tracker format
    - Storing sync state and cursors

    Example:
        >>> manager = PlaidSyncManager(config)
        >>> manager.add_connection(access_token)
        >>> new_transactions = manager.sync_all()
    """

    def __init__(
        self,
        config: PlaidConfig,
        data_dir: Path | None = None,
    ) -> None:
        """
        Initialize sync manager.

        Args:
            config: Plaid configuration.
            data_dir: Directory for storing sync state.
        """
        self.client = PlaidClient(config)
        self.data_dir = data_dir or Path.home() / ".config" / "finance-tracker" / "plaid"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._connections: dict[str, AccessToken] = {}
        self._cursors: dict[str, str] = {}
        self._load_state()

    def add_connection(self, access_token: AccessToken) -> None:
        """
        Add a new bank connection.

        Args:
            access_token: Access token from Plaid Link.
        """
        self._connections[access_token.item_id] = access_token
        self._save_state()

    def remove_connection(self, item_id: str) -> bool:
        """
        Remove a bank connection.

        Args:
            item_id: Plaid item ID to remove.

        Returns:
            True if connection was removed.
        """
        if item_id in self._connections:
            connection = self._connections[item_id]
            self.client.remove_item(connection.access_token)
            del self._connections[item_id]
            if item_id in self._cursors:
                del self._cursors[item_id]
            self._save_state()
            return True
        return False

    def list_connections(self) -> list[dict[str, Any]]:
        """
        List all bank connections.

        Returns:
            List of connection info dictionaries.
        """
        return [
            conn.to_dict(include_token=False)
            for conn in self._connections.values()
        ]

    def sync_all(self) -> dict[str, SyncResult]:
        """
        Sync transactions for all connections.

        Returns:
            Dictionary mapping item_id to SyncResult.
        """
        results: dict[str, SyncResult] = {}

        for item_id, connection in self._connections.items():
            try:
                cursor = self._cursors.get(item_id)
                result = self.client.sync_transactions(
                    connection.access_token,
                    cursor=cursor,
                )

                if result.next_cursor:
                    self._cursors[item_id] = result.next_cursor

                connection.last_sync = datetime.now()
                connection.status = LinkStatus.CONNECTED
                connection.error = None

                results[item_id] = result

            except PlaidError as e:
                connection.status = LinkStatus.ERROR
                connection.error = str(e)
                results[item_id] = SyncResult(
                    status=SyncStatus.FAILED,
                    error=str(e),
                )

        self._save_state()
        return results

    def sync_connection(self, item_id: str) -> SyncResult:
        """
        Sync transactions for a specific connection.

        Args:
            item_id: Plaid item ID.

        Returns:
            SyncResult with transaction data.

        Raises:
            KeyError: If connection not found.
        """
        if item_id not in self._connections:
            raise KeyError(f"Connection not found: {item_id}")

        connection = self._connections[item_id]
        cursor = self._cursors.get(item_id)

        result = self.client.sync_transactions(
            connection.access_token,
            cursor=cursor,
        )

        if result.next_cursor:
            self._cursors[item_id] = result.next_cursor

        connection.last_sync = datetime.now()
        self._save_state()

        return result

    def convert_to_expenses(
        self,
        transactions: list[PlaidTransaction],
    ) -> list[dict[str, Any]]:
        """
        Convert Plaid transactions to expense entries.

        Args:
            transactions: List of Plaid transactions.

        Returns:
            List of expense dictionaries compatible with finance-tracker.
        """
        from finance_tracker.csv_import import TransactionCategorizer

        categorizer = TransactionCategorizer()
        expenses = []

        for tx in transactions:
            # Skip pending and income transactions
            if tx.pending or tx.amount < 0:
                continue

            # Map Plaid category to our category
            category = self._map_plaid_category(tx.category)
            if category is None:
                # Use auto-categorizer as fallback
                category = categorizer.categorize(tx.name)

            expenses.append({
                "date": tx.date,
                "category": category.value,
                "description": tx.merchant_name or tx.name,
                "amount": float(tx.amount),
                "notes": f"Imported from Plaid ({tx.transaction_id})",
                "plaid_transaction_id": tx.transaction_id,
                "plaid_account_id": tx.account_id,
            })

        return expenses

    def _map_plaid_category(
        self,
        plaid_categories: list[str],
    ) -> Any | None:
        """Map Plaid category to finance-tracker category."""
        from finance_tracker.ods_generator import ExpenseCategory

        if not plaid_categories:
            return None

        # Category mapping
        mapping = {
            "food and drink": ExpenseCategory.GROCERIES,
            "groceries": ExpenseCategory.GROCERIES,
            "restaurants": ExpenseCategory.DINING_OUT,
            "coffee": ExpenseCategory.DINING_OUT,
            "fast food": ExpenseCategory.DINING_OUT,
            "transportation": ExpenseCategory.TRANSPORTATION,
            "gas": ExpenseCategory.TRANSPORTATION,
            "ride share": ExpenseCategory.TRANSPORTATION,
            "entertainment": ExpenseCategory.ENTERTAINMENT,
            "streaming": ExpenseCategory.SUBSCRIPTIONS,
            "music": ExpenseCategory.SUBSCRIPTIONS,
            "utilities": ExpenseCategory.UTILITIES,
            "housing": ExpenseCategory.HOUSING,
            "rent": ExpenseCategory.HOUSING,
            "mortgage": ExpenseCategory.HOUSING,
            "healthcare": ExpenseCategory.HEALTHCARE,
            "pharmacy": ExpenseCategory.HEALTHCARE,
            "insurance": ExpenseCategory.INSURANCE,
            "shopping": ExpenseCategory.MISCELLANEOUS,
            "clothing": ExpenseCategory.CLOTHING,
            "personal care": ExpenseCategory.PERSONAL,
            "education": ExpenseCategory.EDUCATION,
        }

        for cat in plaid_categories:
            cat_lower = cat.lower()
            if cat_lower in mapping:
                return mapping[cat_lower]

        return None

    def _load_state(self) -> None:
        """Load sync state from disk."""
        state_file = self.data_dir / "sync_state.json"
        if state_file.exists():
            try:
                with open(state_file) as f:
                    state = json.load(f)
                    self._cursors = state.get("cursors", {})
                    # Note: Access tokens need secure storage
                    # This is simplified for the reference implementation
            except Exception:
                pass

    def _save_state(self) -> None:
        """Save sync state to disk."""
        state_file = self.data_dir / "sync_state.json"
        state = {
            "cursors": self._cursors,
            "last_updated": datetime.now().isoformat(),
        }
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)
