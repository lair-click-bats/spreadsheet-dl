# Backup API Reference

Backup and restore functionality with integrity verification.

**Implements:** DR-STORE-002 (Backup/Restore Functionality)

## Overview

The Backup module provides comprehensive backup and recovery capabilities:

- Automatic backups before destructive operations (edit, delete, import, overwrite)
- Manual backup creation
- Configurable retention policies
- Compressed backups (gzip)
- SHA-256 integrity verification
- Restore with validation
- Backup metadata tracking
- Statistics and cleanup

## Enumerations

### BackupReason

Reasons for creating backups.

```python
from spreadsheet_dl.backup import BackupReason

BackupReason.MANUAL                  # User-initiated backup
BackupReason.AUTO_BEFORE_EDIT        # Before modifying file
BackupReason.AUTO_BEFORE_DELETE      # Before deleting file
BackupReason.AUTO_BEFORE_IMPORT      # Before importing data
BackupReason.AUTO_BEFORE_OVERWRITE   # Before overwriting file
BackupReason.SCHEDULED               # Scheduled backup
```

---

### BackupCompression

Supported compression algorithms.

```python
from spreadsheet_dl.backup import BackupCompression

BackupCompression.NONE    # No compression
BackupCompression.GZIP    # gzip compression
```

---

## Backup Metadata

### BackupMetadata

Metadata stored with each backup.

```python
from spreadsheet_dl.backup import BackupMetadata
from datetime import datetime

metadata = BackupMetadata(
    version="1.0",
    original_path="/home/user/budget.ods",
    original_filename="budget.ods",
    backup_time=datetime.now().isoformat(),
    reason="auto_before_edit",
    compression="gzip",
    content_hash="abc123def456...",
    file_size=51200,
    user="john",
    extra={"note": "Before major edits"}
)

# Serialize/deserialize
json_str = metadata.to_json()
metadata = BackupMetadata.from_json(json_str)

# Load from file
metadata = BackupMetadata.from_file("/path/to/backup.meta.json")
```

**Attributes:**

- `version: str` - Metadata format version
- `original_path: str` - Absolute path to original file
- `original_filename: str` - Original filename
- `backup_time: str` - ISO format backup timestamp
- `reason: str` - BackupReason enum value
- `compression: str` - BackupCompression enum value
- `content_hash: str` - SHA-256 hash of original content
- `file_size: int` - Size of original file in bytes
- `user: str` - User who created backup
- `extra: dict[str, Any]` - Additional metadata

---

### BackupInfo

Information about a backup file.

```python
from spreadsheet_dl.backup import BackupInfo

backup_info = BackupInfo(
    backup_path=Path("/home/user/.spreadsheet-dl-backups/budget_20240115_103000_000001.bak.gz"),
    metadata_path=Path("/home/user/.spreadsheet-dl-backups/budget_20240115_103000_000001.bak.gz.meta.json"),
    metadata=metadata,
    created=datetime.now()
)

print(backup_info)
# BackupInfo(file=budget.ods, created=2024-01-15T10:30:00.000001, reason=auto_before_edit)
```

---

## Backup Manager

### BackupManager

Main class for backup management.

```python
from spreadsheet_dl.backup import BackupManager, BackupReason
from pathlib import Path

# Create manager with defaults
manager = BackupManager()

# Custom configuration
manager = BackupManager(
    backup_dir="/var/backups/spreadsheet-dl",
    retention_days=60,
    compression=BackupCompression.GZIP
)
```

**Configuration:**

- `DEFAULT_BACKUP_DIR = ".spreadsheet-dl-backups"`
- `DEFAULT_RETENTION_DAYS = 30`

**Methods:**

#### `create_backup(file_path, reason=BackupReason.MANUAL, extra_metadata=None) -> BackupInfo`

Create a backup of a file.

```python
from spreadsheet_dl.backup import BackupManager, BackupReason

manager = BackupManager()

backup = manager.create_backup(
    "budget.ods",
    reason=BackupReason.AUTO_BEFORE_EDIT,
    extra_metadata={"action": "user_edits"}
)

print(backup.backup_path)
print(backup.metadata.content_hash)
```

**Parameters:**

- `file_path: str | Path` - File to backup
- `reason: BackupReason` - Reason for backup
- `extra_metadata: dict[str, Any] | None` - Additional metadata to store

**Returns:** BackupInfo with backup details

**Raises:** FileError if file doesn't exist, BackupError on failure

---

#### `restore_backup(backup, target_path=None, *, verify=True, overwrite=False) -> Path`

Restore a file from backup.

```python
manager = BackupManager()

# Restore to original path
restored_path = manager.restore_backup(backup_info)

# Restore to custom path
restored_path = manager.restore_backup(
    backup_info,
    target_path="budget_restored.ods",
    verify=True,
    overwrite=False
)

# Restore from backup path directly
restored_path = manager.restore_backup(
    "/path/to/backup.bak.gz",
    target_path="recovery.ods"
)
```

**Parameters:**

- `backup: BackupInfo | Path | str` - Backup to restore from
- `target_path: Path | str | None` - Path to restore to (defaults to original)
- `verify: bool` - Verify integrity after restore
- `overwrite: bool` - Overwrite existing file

**Returns:** Path to restored file

**Raises:** BackupNotFoundError, BackupCorruptError, RestoreError

---

#### `list_backups(file_path=None, *, include_expired=False) -> list[BackupInfo]`

List available backups.

```python
# List all backups
all_backups = manager.list_backups()

# List backups for specific file
file_backups = manager.list_backups("budget.ods")

# Include expired backups (older than retention period)
all_including_expired = manager.list_backups(include_expired=True)

# Sort by newest first (default)
for backup in all_backups:
    print(f"{backup.metadata.original_filename}: {backup.created}")
```

**Parameters:**

- `file_path: str | Path | None` - Filter by original file
- `include_expired: bool` - Include expired backups

**Returns:** List of BackupInfo (sorted newest first)

---

#### `verify_backup(backup) -> dict[str, Any]`

Verify backup integrity.

```python
result = manager.verify_backup(backup_info)

if result["valid"]:
    print("Backup is valid")
else:
    print(f"Issues found:")
    for issue in result["issues"]:
        print(f"  - {issue}")
```

**Returns:** Dictionary with verification results:

```python
{
    "valid": True,
    "backup_path": str,
    "file_exists": True,
    "metadata_exists": True,
    "hash_valid": True,
    "size_valid": True,
    "issues": []
}
```

---

#### `cleanup_old_backups(days=None, *, dry_run=False) -> list[BackupInfo]`

Remove backups older than retention period.

```python
# Clean using configured retention (default: 30 days)
deleted = manager.cleanup_old_backups()

# Clean older than 60 days
deleted = manager.cleanup_old_backups(days=60)

# Preview what would be deleted
preview = manager.cleanup_old_backups(dry_run=True)
print(f"Would delete {len(preview)} backups")

# Actually delete
deleted = manager.cleanup_old_backups()
print(f"Deleted {len(deleted)} backups")
```

**Parameters:**

- `days: int | None` - Override retention days
- `dry_run: bool` - Preview without deleting

**Returns:** List of deleted BackupInfo

---

#### `get_backup_stats() -> dict[str, Any]`

Get backup statistics.

```python
stats = manager.get_backup_stats()

print(f"Total backups: {stats['total_backups']}")
print(f"Total size: {stats['total_size_mb']} MB")
print(f"Oldest: {stats['oldest_backup']}")
print(f"Newest: {stats['newest_backup']}")
print(f"By reason: {stats['by_reason']}")
print(f"By file: {stats['by_file']}")
```

**Returns:** Dictionary with statistics:

```python
{
    "total_backups": 42,
    "total_size_bytes": 2156032,
    "total_size_mb": 2.06,
    "oldest_backup": "2024-01-01T10:30:00",
    "newest_backup": "2024-01-15T14:20:00",
    "by_reason": {
        "auto_before_edit": 15,
        "manual": 10,
        "auto_before_import": 8,
        "...": "..."
    },
    "by_file": {
        "budget.ods": 25,
        "expenses.ods": 17
    }
}
```

---

## Exception Classes

### BackupError

Base exception for backup-related errors.

```python
from spreadsheet_dl.backup import BackupError

try:
    manager.create_backup("nonexistent.ods")
except BackupError as e:
    print(f"Backup failed: {e}")
```

---

### BackupNotFoundError

Raised when a backup file is not found.

```python
from spreadsheet_dl.backup import BackupNotFoundError

try:
    manager.restore_backup("/nonexistent/backup.bak.gz")
except BackupNotFoundError as e:
    print(f"Backup not found: {e.backup_path}")
```

---

### BackupCorruptError

Raised when a backup file is corrupted.

```python
from spreadsheet_dl.backup import BackupCorruptError

try:
    manager.restore_backup(corrupted_backup, verify=True)
except BackupCorruptError as e:
    print(f"Backup corrupted: {e.reason}")
```

---

### RestoreError

Raised when restore operation fails.

```python
from spreadsheet_dl.backup import RestoreError

try:
    manager.restore_backup(backup_info, target_path="/read-only/file.ods")
except RestoreError as e:
    print(f"Restore failed: {e}")
```

---

## Convenience Functions

### auto_backup(file_path, reason, backup_manager=None) -> BackupInfo | None

Create automatic backup of a file.

```python
from spreadsheet_dl.backup import auto_backup, BackupReason

# Create backup with auto-detected manager
backup = auto_backup("budget.ods", BackupReason.AUTO_BEFORE_EDIT)

if backup:
    print(f"Backed up to: {backup.backup_path}")
else:
    print("File doesn't exist, no backup created")

# Use specific manager
manager = BackupManager(backup_dir="/custom/path")
backup = auto_backup("budget.ods", BackupReason.MANUAL, manager)
```

---

### backup_decorator(reason=BackupReason.AUTO_BEFORE_EDIT, file_arg="file_path")

Decorator to automatically backup files before operations.

```python
from spreadsheet_dl.backup import backup_decorator, BackupReason

@backup_decorator(
    reason=BackupReason.AUTO_BEFORE_EDIT,
    file_arg="ods_file"
)
def edit_budget(ods_file: Path, changes: dict) -> None:
    """Edit budget file. Automatically backed up first."""
    # Modifications here...
    pass

# Call the function - backup happens automatically
edit_budget(Path("budget.ods"), {"category": "Groceries", "amount": 500})
```

---

## Complete Example

```python
from spreadsheet_dl.backup import (
    BackupManager,
    BackupReason,
    auto_backup,
)
from pathlib import Path

# Initialize manager
manager = BackupManager(
    backup_dir=Path.home() / ".backups",
    retention_days=90
)

# Manual backup
budget_file = Path("budget.ods")
backup = manager.create_backup(
    budget_file,
    reason=BackupReason.MANUAL,
    extra_metadata={"comment": "Before major reorganization"}
)
print(f"Backup created: {backup.backup_path}")

# Verify backup integrity
result = manager.verify_backup(backup)
if result["valid"]:
    print("Backup verified OK")
else:
    print(f"Issues: {result['issues']}")

# List recent backups
recent = manager.list_backups(budget_file, include_expired=False)
print(f"Recent backups for {budget_file.name}:")
for b in recent[:5]:
    print(f"  - {b.created}: {b.metadata.reason}")

# Restore from backup
restored = manager.restore_backup(backup, target_path="budget_recovered.ods")
print(f"Restored to: {restored}")

# Cleanup old backups
deleted = manager.cleanup_old_backups()
print(f"Cleaned up {len(deleted)} old backups")

# Get statistics
stats = manager.get_backup_stats()
print(f"Total: {stats['total_backups']} backups, {stats['total_size_mb']} MB")
```

---

## Backup Storage

Default backup directory: `~/.spreadsheet-dl-backups/`

Files are stored with timestamp and reason:

```
budget_ods_20240115_103000_000001.bak.gz
budget_ods_20240115_103000_000001.bak.gz.meta.json
```

Metadata format (JSON):

```json
{
  "version": "1.0",
  "original_path": "/home/user/budget.ods",
  "original_filename": "budget.ods",
  "backup_time": "2024-01-15T10:30:00.000001+00:00",
  "reason": "auto_before_edit",
  "compression": "gzip",
  "content_hash": "5f6d9e8c7a...",
  "file_size": 51200,
  "user": "john",
  "extra": {}
}
```

---

## Security Considerations

1. **Password Protection:** Backups are stored unencrypted. Protect backup directory with file permissions.
2. **Retention:** Default 30-day retention. Adjust as needed for your compliance requirements.
3. **Verification:** Always verify backup integrity before relying on restore.
4. **Storage:** Consider backing up the backup directory itself for critical files.
