# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 4.0.x   | :white_check_mark: |
| < 4.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within SpreadsheetDL, please send an email to the maintainers. All security vulnerabilities will be promptly addressed.

**Please do not report security vulnerabilities through public GitHub issues.**

When reporting a vulnerability, please include:

- Type of vulnerability (e.g., SQL injection, XSS, authentication bypass)
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability, including how an attacker might exploit it

## Security Considerations

### File System Access

SpreadsheetDL reads and writes spreadsheet files to the local filesystem. Users should:

- Only process spreadsheet files from trusted sources
- Be cautious when using spreadsheet files from untrusted sources as they may contain malicious formulas
- Validate file paths when using the library programmatically to prevent path traversal attacks

### Formula Evaluation

SpreadsheetDL supports spreadsheet formulas, including:

- Mathematical formulas
- Text manipulation formulas
- Date/time formulas
- Conditional formulas

**Important**: Formulas are written to spreadsheet files and evaluated by the spreadsheet application (LibreOffice, Excel, etc.), not by SpreadsheetDL itself. Users should be aware that malicious formulas could potentially be executed by the spreadsheet application.

### External Integrations

SpreadsheetDL includes optional integrations with external services:

- **Plaid API**: Banking data integration requires API credentials
- **HTML Import**: Parses HTML tables using BeautifulSoup4

When using these integrations:

- Store API credentials securely (environment variables, secrets management)
- Never commit API keys or credentials to version control
- Use HTTPS for all external API communications
- Validate and sanitize HTML content before processing

### MCP Server

The Model Context Protocol (MCP) server provides programmatic access to spreadsheet operations. When deploying the MCP server:

- Restrict access to trusted clients only
- Implement appropriate authentication and authorization
- Validate all input from MCP clients
- Be cautious about exposing the MCP server to untrusted networks

## Security Best Practices

When using SpreadsheetDL in production:

1. **Input Validation**: Validate all user-provided data before creating spreadsheets
2. **Path Sanitization**: Sanitize file paths to prevent directory traversal
3. **Credential Management**: Use environment variables or secrets managers for API credentials
4. **Dependency Updates**: Keep SpreadsheetDL and its dependencies up to date
5. **Minimal Permissions**: Run with minimal filesystem permissions necessary
6. **Audit Logging**: Log spreadsheet operations for audit trails

## Disclosure Policy

- Security vulnerabilities will be disclosed publicly after a fix is released
- We aim to release security patches within 30 days of disclosure
- Credit will be given to security researchers who responsibly disclose vulnerabilities

## Contact

For security-related inquiries, please open a private security advisory on GitHub or contact the maintainers directly.

Thank you for helping keep SpreadsheetDL and its users secure!
