# WebDAV Upload API Reference

Upload ODS files to Nextcloud via WebDAV protocol.

**Implements:** FR-CLOUD-001 (Nextcloud Integration)

## Overview

The WebDAV Upload module provides secure file upload to Nextcloud servers using the WebDAV protocol. It supports directory creation, file listing, downloading, and deleting files on remote Nextcloud instances.

Features:

- Secure HTTPS connection with SSL verification
- Basic HTTP authentication
- Automatic parent directory creation
- File listing and management
- Download files from Nextcloud
- Connection testing

## Configuration

### NextcloudConfig

Configuration for Nextcloud WebDAV connection.

```python
from spreadsheet_dl.webdav_upload import NextcloudConfig

config = NextcloudConfig(
    server_url="https://nextcloud.example.com",
    username="user@example.com",
    password="app-password",  # Recommended: app password
    remote_path="/Finance"
)

# Load from environment variables
config = NextcloudConfig.from_env()
```

**Attributes:**

- `server_url: str` - Nextcloud server base URL
- `username: str` - Nextcloud username
- `password: str` - Password (app password recommended)
- `remote_path: str` - Default remote path (default: "/Finance")

**Methods:**

#### `from_env() -> NextcloudConfig`

Create configuration from environment variables.

```python
import os

# Set environment variables
os.environ["NEXTCLOUD_URL"] = "https://nextcloud.example.com"
os.environ["NEXTCLOUD_USER"] = "user@example.com"
os.environ["NEXTCLOUD_PASSWORD"] = "app-password"
os.environ["NEXTCLOUD_PATH"] = "/Finance"

# Load configuration
config = NextcloudConfig.from_env()
```

**Environment Variables:**

- `NEXTCLOUD_URL` - Server base URL (required)
- `NEXTCLOUD_USER` - Username (required)
- `NEXTCLOUD_PASSWORD` - Password (required)
- `NEXTCLOUD_PATH` - Remote path (optional, defaults to "/Finance")

**Raises:** ValueError if required env vars are missing

---

## WebDAV Client

### WebDAVClient

Client for Nextcloud WebDAV operations.

```python
from spreadsheet_dl.webdav_upload import WebDAVClient, NextcloudConfig

config = NextcloudConfig(
    server_url="https://nextcloud.example.com",
    username="user@example.com",
    password="app-password"
)

client = WebDAVClient(config)

# Test connection
if client.test_connection():
    print("Connected to Nextcloud")
```

**Properties:**

#### `webdav_url: str`

Get the WebDAV base URL.

```python
url = client.webdav_url
# -> "https://nextcloud.example.com/remote.php/dav/files/user@example.com"
```

**Methods:**

#### `upload_file(local_path, remote_path=None, create_dirs=True) -> str`

Upload a file to Nextcloud.

```python
from pathlib import Path

# Upload with default remote path
url = client.upload_file("budget.ods")
# -> "https://nextcloud.example.com/remote.php/dav/files/user@example.com/Finance/budget.ods"

# Upload to custom remote path
url = client.upload_file(
    Path("budget.ods"),
    remote_path="/MyFolder/budget_backup.ods",
    create_dirs=True  # Create parent directories
)

# Upload without creating directories
url = client.upload_file(
    "budget.ods",
    remote_path="/existing/folder/budget.ods",
    create_dirs=False
)
```

**Parameters:**

- `local_path: Path | str` - Local file path to upload
- `remote_path: str | None` - Remote path (defaults to config.remote_path + filename)
- `create_dirs: bool` - Create parent directories if needed (default: True)

**Returns:** Remote URL of uploaded file

**Raises:** FileNotFoundError, PermissionError, ConnectionError

---

#### `list_files(remote_path=None) -> list[str]`

List files in a remote directory.

```python
# List files in default remote path
files = client.list_files()
# -> ["budget.ods", "expenses.csv", "summary.xlsx"]

# List files in custom path
files = client.list_files("/Archive")

# Check if specific file exists
if "budget.ods" in client.list_files():
    print("File found on server")
```

**Parameters:**

- `remote_path: str | None` - Remote directory (defaults to config.remote_path)

**Returns:** List of filenames in directory

---

#### `file_exists(remote_path: str) -> bool`

Check if a file exists on the server.

```python
if client.file_exists("/Finance/budget.ods"):
    print("File already exists")
else:
    print("File not found")
```

**Parameters:**

- `remote_path: str` - Path to file to check

**Returns:** True if file exists, False otherwise

---

#### `delete_file(remote_path: str) -> bool`

Delete a file from the server.

```python
# Delete file
success = client.delete_file("/Finance/old_budget.ods")

if success:
    print("File deleted")
else:
    print("File not found or already deleted")
```

**Parameters:**

- `remote_path: str` - Path to file to delete

**Returns:** True if deleted, False if file didn't exist

---

#### `download_file(remote_path, local_path) -> Path`

Download a file from the server.

```python
from pathlib import Path

# Download file
local_path = client.download_file(
    "/Finance/backup.ods",
    "budget_backup.ods"
)

print(f"Downloaded to: {local_path}")

# Download with parent directory creation
local_path = client.download_file(
    "/Finance/2024/January.ods",
    "data/2024/January.ods"
)
```

**Parameters:**

- `remote_path: str` - Path to remote file
- `local_path: Path | str` - Local path to save file

**Returns:** Path to downloaded file

**Raises:** FileNotFoundError, ConnectionError

---

#### `test_connection() -> bool`

Test connection to Nextcloud server.

```python
if client.test_connection():
    print("Successfully connected to Nextcloud")
else:
    print("Failed to connect")
```

**Returns:** True if connection successful, False otherwise

---

## Convenience Functions

### upload_budget(local_path, config=None) -> str

Upload a budget file to Nextcloud.

```python
from spreadsheet_dl.webdav_upload import upload_budget

# Upload with environment configuration
url = upload_budget("budget.ods")

# Upload with specific configuration
from spreadsheet_dl.webdav_upload import NextcloudConfig

config = NextcloudConfig(
    server_url="https://nextcloud.example.com",
    username="user@example.com",
    password="app-password",
    remote_path="/Finance/2024"
)

url = upload_budget("budget.ods", config=config)
print(f"Uploaded to: {url}")
```

**Parameters:**

- `local_path: Path | str` - Local file path
- `config: NextcloudConfig | None` - Configuration (defaults to environment)

**Returns:** Remote URL of uploaded file

**Raises:** ValueError if env vars missing, FileNotFoundError, PermissionError, ConnectionError

---

## Complete Example

```python
from spreadsheet_dl.webdav_upload import WebDAVClient, NextcloudConfig
from pathlib import Path

# Configure Nextcloud connection
config = NextcloudConfig(
    server_url="https://nextcloud.example.com",
    username="user@example.com",
    password="app-password",
    remote_path="/Finance"
)

# Create client
client = WebDAVClient(config)

# Test connection
if not client.test_connection():
    print("Cannot connect to Nextcloud")
    exit(1)

# Upload budget file
local_file = Path("budget.ods")
if local_file.exists():
    remote_url = client.upload_file(local_file)
    print(f"Uploaded to: {remote_url}")
else:
    print("Budget file not found")

# List uploaded files
files = client.list_files()
print(f"Files in /Finance: {files}")

# Download backup
download_path = client.download_file(
    "/Finance/budget.ods",
    "budget_backup.ods"
)
print(f"Downloaded to: {download_path}")

# Check if archive exists
if client.file_exists("/Finance/Archive"):
    print("Archive folder exists")
else:
    print("Archive folder doesn't exist")

# Upload with custom path
archive_url = client.upload_file(
    local_file,
    remote_path="/Finance/Archive/budget_2024.ods",
    create_dirs=True
)
print(f"Archived to: {archive_url}")
```

---

## Error Handling

```python
from spreadsheet_dl.webdav_upload import WebDAVClient, NextcloudConfig

client = WebDAVClient(NextcloudConfig(...))

try:
    # Attempt upload
    url = client.upload_file("budget.ods")
    print(f"Success: {url}")

except FileNotFoundError as e:
    print(f"Local file not found: {e}")

except PermissionError as e:
    print(f"Permission denied on server: {e}")
    print("Check your credentials and permissions")

except ConnectionError as e:
    print(f"Connection failed: {e}")
    print("Check server URL and network connection")

except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Nextcloud Setup

### Generating App Passwords

For security, use app passwords instead of your main Nextcloud password:

1. Log in to Nextcloud
2. Go to Settings → Security
3. Click "Create new app password"
4. Give it a name (e.g., "SpreadsheetDL")
5. Copy the generated password

Use this password in your configuration:

```python
config = NextcloudConfig(
    server_url="https://your-nextcloud.example.com",
    username="your-username",
    password="generated-app-password",  # Use app password here
    remote_path="/Finance"
)
```

### Supported Nextcloud Versions

- Nextcloud 13.0+
- NextCloud AIO (All-In-One)

---

## Environment Configuration

```bash
# Set environment variables for automatic configuration
export NEXTCLOUD_URL="https://nextcloud.example.com"
export NEXTCLOUD_USER="user@example.com"
export NEXTCLOUD_PASSWORD="app-password"
export NEXTCLOUD_PATH="/Finance"

# Now use the tool - it will use these settings automatically
spreadsheet-dl upload budget.ods
```

---

## Troubleshooting

### Connection Issues

```python
# Test connection and get detailed info
if not client.test_connection():
    print("Cannot connect. Check:")
    print("1. Server URL is correct")
    print("2. Network connectivity")
    print("3. SSL certificates are valid")
    print("4. Credentials are correct")
```

### Upload Failures

```python
try:
    url = client.upload_file("large_file.ods")
except PermissionError as e:
    print("Permission error - check:")
    print("1. Username and password")
    print("2. Remote directory permissions")
    print("3. Server disk space")
except Exception as e:
    print(f"Upload failed: {e}")
```

### File Not Found

```python
# Verify file exists before upload
from pathlib import Path

file = Path("budget.ods")
if not file.exists():
    print(f"File not found: {file.absolute()}")
else:
    url = client.upload_file(file)
```
