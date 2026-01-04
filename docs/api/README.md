# SpreadsheetDL API Documentation

Complete API reference for all SpreadsheetDL modules.

## Documentation Status

**100% Complete** - All 44 public API modules are fully documented.

See [API_DOCUMENTATION_STATUS.md](../API_DOCUMENTATION_STATUS.md) for detailed completion report.

## Quick Links

- [API Index](index.md) - Complete index of all APIs
- [Domain Plugin Development](domain-plugins.md) - Plugin development guide
- [Security Considerations](security.md) - Security best practices

## Core Infrastructure

### Spreadsheet Building

- **[builder.md](builder.md)** - Fluent spreadsheet builder API
- **[renderer.md](renderer.md)** - ODS rendering and styling engine
- **[template_engine.md](template_engine.md)** - Template engine system
- **[templates.md](templates.md)** - Template management utilities

### System Components

- **[cli.md](cli.md)** - Command-line interface
- **[plugins.md](plugins.md)** - Plugin system framework
- **[exceptions.md](exceptions.md)** - Exception hierarchy
- **[progress.md](progress.md)** - Progress indicators
- **[adapters.md](adapters.md)** - Plugin adapters

## Finance Domain

### Core Finance

- **[budget_analyzer.md](budget_analyzer.md)** - Core budget analysis engine
- **[analytics.md](analytics.md)** - Advanced analytics and dashboards
- **[accounts.md](accounts.md)** - Multi-account management
- **[categories.md](categories.md)** - Expense categories

### Finance Features

- **[alerts.md](alerts.md)** - Budget alert monitoring system
- **[goals.md](goals.md)** - Savings goals and debt payoff tracking
- **[recurring.md](recurring.md)** - Recurring expense management
- **[reminders.md](reminders.md)** - Bill reminders and calendar integration
- **[report_generator.md](report_generator.md)** - Multi-format report generation

### Finance Integration

- **[bank_formats.md](bank_formats.md)** - Extended bank format support (50+ institutions)
- **[plaid_integration.md](plaid_integration.md)** - Plaid API integration for bank sync
- **[csv_import.md](csv_import.md)** - CSV transaction import with auto-categorization

## Import/Export

- **[export.md](export.md)** - Multi-format export (XLSX, CSV, PDF, JSON)
- **[serialization.md](serialization.md)** - Data serialization
- **[streaming.md](streaming.md)** - Streaming operations

## Utilities

### Configuration & Integration

- **[config.md](config.md)** - Configuration management (YAML, env vars)
- **[completions.md](completions.md)** - Shell completion scripts
- **[backup.md](backup.md)** - Backup and versioning
- **[webdav_upload.md](webdav_upload.md)** - WebDAV/Nextcloud integration

### Runtime Features

- **[interactive.md](interactive.md)** - Interactive mode
- **[notifications.md](notifications.md)** - Notification system
- **[currency.md](currency.md)** - Multi-currency support and conversion

## AI/ML Integration

- **[ai_export.md](ai_export.md)** - LLM-friendly data export
- **[ai_training.md](ai_training.md)** - Training data generation for AI
- **[mcp_server.md](mcp_server.md)** - MCP server implementation

## Advanced Features

- **[charts.md](charts.md)** - Chart generation
- **[visualization.md](visualization.md)** - Data visualization
- **[ods_editor.md](ods_editor.md)** - ODS editing utilities
- **[ods_generator.md](ods_generator.md)** - ODS file generation
- **[performance.md](performance.md)** - Performance guidelines

## Documentation Quality

All documentation includes:

- Comprehensive overview with key features
- Complete API reference for all classes and methods
- Accurate type hints matching source code
- Working code examples for common use cases
- Cross-references to related modules
- Exception documentation
- Performance considerations

## Navigation Tips

1. **Start with [index.md](index.md)** for a complete overview
2. **Domain developers** should read [domain-plugins.md](domain-plugins.md)
3. **Security-conscious users** should review [security.md](security.md)
4. **Each module page** includes related modules and cross-references

## Contributing

When adding new features:

1. Update corresponding API documentation
2. Add working code examples
3. Update cross-references
4. Run documentation link checker
5. Update this README if adding new categories

## Version

Documentation version: 4.0.0
Last updated: 2026-01-04
