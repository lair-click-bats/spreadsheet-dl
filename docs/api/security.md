# Security API Reference

Data encryption at rest, secure key management, and audit logging.

**Implements:** FR-SEC-001 (Data Encryption), NFR-SEC-001 (Credential Security)

## Overview

The security module provides:

- AES-256-GCM file encryption with PBKDF2-SHA256 key derivation
- Encrypted credential storage
- Security audit logging
- Password generation and strength checking

## Classes

### FileEncryptor

Encrypt and decrypt budget files with password-based encryption.

```python
from spreadsheet_dl.security import FileEncryptor

encryptor = FileEncryptor()

# Encrypt a file
metadata = encryptor.encrypt_file(
    "budget.ods",
    "budget.ods.enc",
    "my-secure-password"
)

# Decrypt a file
metadata = encryptor.decrypt_file(
    "budget.ods.enc",
    "budget.ods",
    "my-secure-password"
)
```

#### Constructor

```python
FileEncryptor(audit_log: SecurityAuditLog | None = None)
```

**Parameters:**

- `audit_log`: Optional audit log for tracking operations

#### Methods

##### `encrypt_file()`

Encrypt a file with password.

```python
metadata = encryptor.encrypt_file(
    input_path: str | Path,
    output_path: str | Path,
    password: str,
    *,
    delete_original: bool = False
)
```

**Parameters:**

- `input_path`: Path to file to encrypt
- `output_path`: Path for encrypted output
- `password`: Encryption password
- `delete_original`: Whether to securely delete original (3-pass overwrite)

**Returns:** `EncryptionMetadata` with encryption details

**Raises:**

- `FileError`: If file operations fail
- `EncryptionError`: If encryption fails

##### `decrypt_file()`

Decrypt a file with password.

```python
metadata = encryptor.decrypt_file(
    input_path: str | Path,
    output_path: str | Path,
    password: str,
    *,
    verify_hash: bool = True
)
```

**Parameters:**

- `input_path`: Path to encrypted file
- `output_path`: Path for decrypted output
- `password`: Decryption password
- `verify_hash`: Whether to verify content integrity

**Returns:** `EncryptionMetadata` from file

**Raises:**

- `FileError`: If file operations fail
- `DecryptionError`: If decryption fails or wrong password
- `IntegrityError`: If integrity check fails

---

### CredentialStore

Secure storage for credentials encrypted with a master password.

```python
from spreadsheet_dl.security import CredentialStore

store = CredentialStore()

# Store a credential
store.store_credential(
    "nextcloud_password",
    "my-secret-password",
    master_password="my-master-password"
)

# Retrieve a credential
password = store.get_credential(
    "nextcloud_password",
    master_password="my-master-password"
)

# List stored credentials
keys = store.list_credentials(master_password="my-master-password")
# ["nextcloud_password", "plaid_secret"]

# Delete a credential
deleted = store.delete_credential(
    "nextcloud_password",
    master_password="my-master-password"
)
```

#### Constructor

```python
CredentialStore(store_path: Path | None = None)
```

**Parameters:**

- `store_path`: Path to credential store file (default: `~/.config/spreadsheet-dl/credentials.enc`)

#### Methods

| Method                                          | Description                     |
| ----------------------------------------------- | ------------------------------- |
| `store_credential(key, value, master_password)` | Store a credential              |
| `get_credential(key, master_password)`          | Retrieve a credential           |
| `delete_credential(key, master_password)`       | Delete a credential             |
| `list_credentials(master_password)`             | List all stored credential keys |

---

### SecurityAuditLog

Security audit log for tracking file access and encryption operations.

```python
from spreadsheet_dl.security import SecurityAuditLog

audit_log = SecurityAuditLog()

# Log an action
audit_log.log_action(
    action="encrypt",
    file_path="/path/to/file.ods",
    success=True,
    details={"algorithm": "AES-256-GCM"}
)

# Retrieve log entries
entries = audit_log.get_entries(
    file_path="/path/to/file.ods",
    action="encrypt",
    limit=100
)
```

#### Constructor

```python
SecurityAuditLog(log_path: Path | None = None)
```

**Parameters:**

- `log_path`: Path to audit log file (default: `~/.config/spreadsheet-dl/security_audit.log`)

#### Methods

##### `log_action()`

Log a security action.

```python
audit_log.log_action(
    action: str,           # e.g., "encrypt", "decrypt", "access"
    file_path: str,
    success: bool = True,
    details: dict | None = None
)
```

##### `get_entries()`

Get audit log entries with filtering.

```python
entries = audit_log.get_entries(
    file_path: str | None = None,
    action: str | None = None,
    limit: int = 100
)
```

---

### EncryptionMetadata

Metadata stored with encrypted files.

```python
from spreadsheet_dl.security import EncryptionMetadata

metadata = EncryptionMetadata(
    version="1.0",
    algorithm="AES-256-GCM",
    kdf="PBKDF2-SHA256",
    iterations=600000,
    salt=b"...",
    nonce=b"...",
    created_at="2024-01-15T10:30:00Z",
    original_filename="budget.ods",
    content_hash="sha256..."
)

# Serialize to JSON
json_str = metadata.to_json()

# Deserialize from JSON
restored = EncryptionMetadata.from_json(json_str)
```

---

## Module Functions

### `generate_password()`

Generate a cryptographically secure random password.

```python
from spreadsheet_dl.security import generate_password

# Default: 20 characters with symbols
password = generate_password()

# Custom length, no symbols
password = generate_password(length=16, include_symbols=False)
```

**Parameters:**

- `length`: Password length (minimum 12)
- `include_symbols`: Whether to include special characters

**Returns:** Random password string

### `check_password_strength()`

Check password strength.

```python
from spreadsheet_dl.security import check_password_strength

result = check_password_strength("MyPassword123!")
# {
#     "score": 85,
#     "level": "strong",
#     "feedback": [],
#     "requirements_met": {
#         "min_length": True,
#         "lowercase": True,
#         "uppercase": True,
#         "digit": True,
#         "symbol": True
#     }
# }
```

**Returns:** Dictionary with:

- `score`: 0-100 strength score
- `level`: "weak", "fair", "good", or "strong"
- `feedback`: List of improvement suggestions
- `requirements_met`: Which requirements are satisfied

---

## Enums

### EncryptionAlgorithm

```python
from spreadsheet_dl.security import EncryptionAlgorithm

EncryptionAlgorithm.AES_256_GCM  # Default
EncryptionAlgorithm.AES_256_CBC
```

### KeyDerivationFunction

```python
from spreadsheet_dl.security import KeyDerivationFunction

KeyDerivationFunction.PBKDF2_SHA256  # Default
KeyDerivationFunction.SCRYPT
```

---

## Security Parameters

| Parameter            | Value    | Description                    |
| -------------------- | -------- | ------------------------------ |
| `DEFAULT_ITERATIONS` | 600,000  | PBKDF2 iterations (OWASP 2023) |
| `SALT_SIZE`          | 32 bytes | Salt size (256 bits)           |
| `NONCE_SIZE`         | 12 bytes | GCM nonce (96 bits)            |
| `TAG_SIZE`           | 16 bytes | Authentication tag (128 bits)  |

---

## Encrypted File Format

Encrypted files use a custom binary format:

```
[Magic Bytes: 6B "SDLENC"]
[Version: 2B]
[Metadata Length: 4B]
[Metadata JSON: Variable]
[Authentication Tag: 16B]
[Ciphertext: Variable]
```

---

## Complete Example

```python
from pathlib import Path
from spreadsheet_dl.security import (
    FileEncryptor,
    CredentialStore,
    SecurityAuditLog,
    generate_password,
    check_password_strength,
)

# Create secure password
password = generate_password(length=24)
strength = check_password_strength(password)
print(f"Password strength: {strength['level']} ({strength['score']}/100)")

# Set up audit logging
audit_log = SecurityAuditLog(Path("./security.log"))

# Create encryptor with audit logging
encryptor = FileEncryptor(audit_log=audit_log)

# Encrypt budget file
metadata = encryptor.encrypt_file(
    "budget.ods",
    "budget.ods.enc",
    password,
    delete_original=True  # Secure delete original
)
print(f"Encrypted with {metadata.algorithm}")
print(f"Content hash: {metadata.content_hash[:16]}...")

# Store the password securely
store = CredentialStore()
master_password = "my-master-key"

store.store_credential(
    "budget_encryption_key",
    password,
    master_password
)

# Later, retrieve and decrypt
stored_password = store.get_credential(
    "budget_encryption_key",
    master_password
)

encryptor.decrypt_file(
    "budget.ods.enc",
    "budget_decrypted.ods",
    stored_password
)

# Review audit log
entries = audit_log.get_entries(action="encrypt")
for entry in entries:
    print(f"{entry.timestamp}: {entry.action} - {entry.success}")
```
