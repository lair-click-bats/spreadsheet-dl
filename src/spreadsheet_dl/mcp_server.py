"""
MCP (Model Context Protocol) server for SpreadsheetDL.

BACKWARD COMPATIBILITY WRAPPER
===============================

This module has been refactored into a modular package structure at
`spreadsheet_dl._mcp/`. This file now serves as a backward compatibility
wrapper, re-exporting all public APIs from the new modular implementation.

All functionality remains 100% compatible. Imports from this module will
continue to work without changes:

    from spreadsheet_dl.mcp_server import MCPServer, create_mcp_server, main

New code should import from the modular package:

    from spreadsheet_dl._mcp import MCPServer, create_mcp_server, main

Package Structure (spreadsheet_dl/_mcp/):
    - cli.py: Command-line interface and server creation helpers
    - config.py: Configuration classes
    - exceptions.py: MCP-specific exceptions
    - handlers.py: Common handler utilities
    - models.py: Data models
    - registry.py: Tool registry
    - server.py: Core MCPServer implementation
    - tools/: Tool handler implementations by category
        - budget.py: Budget analysis tools (9 handlers)
        - cell.py: Cell manipulation tools (11 handlers)
        - style.py: Style and formatting tools (24 handlers)
        - structure.py: Row/column/sheet structure tools (22 handlers)
        - chart.py: Chart creation tools (2 handlers)
        - advanced.py: Advanced features (77 handlers)

Requirements implemented:
    - IR-MCP-002: Native MCP Server (Gap G-AI-05)

Features:
    - Budget analysis tools
    - Natural language expense entry
    - Report generation on request
    - Spending trend analysis
    - Period comparison
    - Real-time budget queries
    - 145+ MCP tools across all categories

Security:
    - File access restrictions (configurable paths)
    - Rate limiting
    - Audit logging
"""

from __future__ import annotations

# Re-export all public APIs from modular implementation
from spreadsheet_dl._mcp import (
    MCPCapabilities,
    MCPConfig,
    MCPError,
    MCPSecurityError,
    MCPServer,
    MCPTool,
    MCPToolError,
    MCPToolParameter,
    MCPToolRegistry,
    MCPToolResult,
    MCPVersion,
    create_mcp_server,
    main,
)

__all__ = [
    "MCPCapabilities",
    "MCPConfig",
    "MCPError",
    "MCPSecurityError",
    "MCPServer",
    "MCPTool",
    "MCPToolError",
    "MCPToolParameter",
    "MCPToolRegistry",
    "MCPToolResult",
    "MCPVersion",
    "create_mcp_server",
    "main",
]

# Support direct execution: python -m spreadsheet_dl.mcp_server
if __name__ == "__main__":
    main()
