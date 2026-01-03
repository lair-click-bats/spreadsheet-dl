#!/usr/bin/env python3
"""
Example: Use MCP server from Python.

This demonstrates starting and using the MCP server
programmatically for AI-powered spreadsheet operations.
"""

from pathlib import Path

from spreadsheet_dl import MCPConfig, MCPServer


def main():
    """Start MCP server and demonstrate basic usage."""

    print("SpreadsheetDL MCP Server Example")
    print("=" * 50)

    # Configure MCP server
    config = MCPConfig(
        port=3000,
        host="localhost",
        enable_write=True,
        enable_ai_analysis=True,
        spreadsheet_dir=Path("output").absolute(),
    )

    print("\nConfiguration:")
    print(f"  Port: {config.port}")
    print(f"  Host: {config.host}")
    print(f"  Write enabled: {config.enable_write}")
    print(f"  AI analysis: {config.enable_ai_analysis}")
    print(f"  Spreadsheet directory: {config.spreadsheet_dir}")

    # Create server
    server = MCPServer(config)

    print("\nAvailable tools:")
    for tool in server.get_available_tools():
        print(f"  - {tool.name}: {tool.description}")

    print("\n" + "=" * 50)
    print("MCP Server Setup Complete!")
    print("=" * 50)

    print("\nTo use with Claude Desktop:")
    print("1. Add this to Claude Desktop's config:")
    print("""
    {
      "mcpServers": {
        "spreadsheet-dl": {
          "command": "spreadsheet-dl",
          "args": ["mcp-server"],
          "env": {
            "SPREADSHEET_DIR": "/path/to/budgets"
          }
        }
      }
    }
    """)

    print("\n2. Restart Claude Desktop")

    print("\n3. Try these prompts:")
    print('   - "Create a monthly budget for January 2026"')
    print('   - "Add these expenses to my budget: groceries $125, gas $45"')
    print('   - "Analyze my spending and show me where I can save"')
    print('   - "Generate a report for this month"')

    print("\nTo start server manually:")
    print("  spreadsheet-dl mcp-server")

    print("\nServer is configured but not started (run manually)")
    print("See docs/tutorials/05-use-mcp-tools.md for detailed guide")


if __name__ == "__main__":
    main()
