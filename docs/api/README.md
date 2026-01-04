# SpreadsheetDL API Documentation

Complete API reference for all SpreadsheetDL modules.

## Documentation Status

### ✅ Completed Documentation (5/27)

#### Core Modules (Priority 1) - 5/5 COMPLETE

1. **[renderer.md](renderer.md)** - Core ODS rendering engine ✅
2. **[cli.md](cli.md)** - Command-line interface ✅
3. **[plugins.md](plugins.md)** - Plugin system framework (NEW in v4.0) ✅
4. **[progress.md](progress.md)** - Progress indicators (NEW in v4.0) ✅
5. **[exceptions.md](exceptions.md)** - Exception hierarchy ✅

### 🚧 Pending Documentation (22/27)

#### Finance Domain Modules (Priority 2) - 0/7

6. **alerts.md** - Budget alerts
7. **analytics.md** - Budget analytics
8. **budget_analyzer.md** - Budget analysis
9. **goals.md** - Financial goals
10. **recurring.md** - Recurring expenses
11. **reminders.md** - Payment reminders
12. **report_generator.md** - Report generation

#### Import/Export Modules (Priority 3) - 0/4

13. **export.md** - Export functionality
14. **csv_import.md** - CSV import
15. **bank_formats.md** - Bank format definitions
16. **plaid_integration.md** - Plaid API integration

#### Utility Modules (Priority 4) - 0/8

17. **config.md** - Configuration management
18. **completions.md** - Shell completions
19. **currency.md** - Currency handling
20. **notifications.md** - Notification system
21. **backup.md** - Backup functionality
22. **webdav_upload.md** - WebDAV upload
23. **interactive.md** - Interactive mode
24. **templates.md** - Template utilities

#### AI/ML Modules (Priority 5) - 0/2

25. **ai_export.md** - AI-friendly export
26. **ai_training.md** - AI training data

#### Template Module - 0/1

27. **ods_generator.md** - ODS generator (verify completeness)

## Quick Reference

### Module Categories

| Category          | Modules                                                                                     | Purpose                               |
| ----------------- | ------------------------------------------------------------------------------------------- | ------------------------------------- |
| **Core**          | renderer, cli, plugins, progress, exceptions                                                | Core functionality and infrastructure |
| **Finance**       | alerts, analytics, budget_analyzer, goals, recurring, reminders, report_generator           | Financial tracking and analysis       |
| **Import/Export** | export, csv_import, bank_formats, plaid_integration                                         | Data import/export                    |
| **Utility**       | config, completions, currency, notifications, backup, webdav_upload, interactive, templates | Supporting utilities                  |
| **AI/ML**         | ai_export, ai_training                                                                      | AI/LLM integration                    |
| **Template**      | ods_generator                                                                               | Template generation                   |

### Documentation Template

Each module documentation follows this structure:

```markdown
# Module: <module_name>

## Overview

[Brief description, new features, use cases]

## Key Classes

[Class documentation with attributes, methods, examples]

## Key Functions

[Function documentation with parameters, returns, examples]

## Constants/Enums

[If applicable]

## Usage Examples

[Comprehensive working examples]

## See Also

[Links to related modules]
```

## Next Steps for Complete Documentation

### Phase 1: Finance Domain (Priority 2)

Create comprehensive documentation for financial modules:

- alerts.py - AlertMonitor, AlertSeverity, budget alert checking
- analytics.py - Dashboard generation, spending analytics
- budget_analyzer.py - BudgetAnalyzer class, summary generation
- goals.py - Financial goal tracking
- recurring.py - Recurring transaction management
- reminders.py - Payment reminder system
- report_generator.py - ReportGenerator class, multiple formats

### Phase 2: Import/Export (Priority 3)

Document data interchange modules:

- export.py - MultiFormatExporter, xlsx/csv/pdf export
- csv_import.py - CSV parsing, TransactionCategorizer
- bank_formats.py - BankFormatRegistry, 50+ bank formats
- plaid_integration.py - Plaid API integration (if implemented)

### Phase 3: Utilities (Priority 4)

Document supporting utilities:

- config.py - Configuration loading, validation
- completions.py - Shell completion generation
- currency.py - Multi-currency support, conversion
- notifications.py - Notification system
- backup.py - BackupManager, versioning
- webdav_upload.md - Nextcloud/WebDAV integration
- interactive.py - Interactive CLI mode
- templates.py - Template management utilities

### Phase 4: AI/ML (Priority 5)

Document AI integration:

- ai_export.py - AIExporter, semantic tagging
- ai_training.py - Training data generation

### Phase 5: Verification

- Verify ods_generator.py completeness
- Test all code examples
- Verify cross-references
- Ensure consistency

## Documentation Guidelines

### 1. Accuracy

- Read actual source code
- Document all public APIs
- Include correct type hints
- Match function signatures exactly

### 2. Completeness

- All classes documented
- All public methods documented
- All module-level functions documented
- Constants and enums included

### 3. Examples

- Working code examples
- Real-world use cases
- Integration examples
- Error handling patterns

### 4. Cross-References

- Link to related modules
- Reference prerequisite modules
- Link to CLI commands
- Reference exception types

### 5. Version Markers

- Mark new features (e.g., "NEW in v4.0.0")
- Note breaking changes
- Document deprecations
- Reference requirement IDs

## Contributing Documentation

When adding documentation:

1. **Read the source**: Always start by reading the actual module source code
2. **Follow the template**: Use the structure shown above
3. **Provide examples**: Include working, tested code examples
4. **Test examples**: Ensure all code examples actually work
5. **Cross-reference**: Link to related modules and exceptions
6. **Mark versions**: Note when features were added

## Tools for Documentation

### Generating Documentation Skeleton

```python
# Example script to generate documentation skeleton
from pathlib import Path

def create_module_doc_skeleton(module_name: str, module_path: Path):
    """Generate documentation skeleton from module inspection."""
    import ast
    import inspect

    # Read module source
    source = module_path.read_text()
    tree = ast.parse(source)

    # Extract classes and functions
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]

    # Generate skeleton
    doc = f"# Module: {module_name}\n\n"
    doc += "## Overview\n\n[TODO: Add overview]\n\n"

    if classes:
        doc += "## Key Classes\n\n"
        for cls in classes:
            doc += f"### {cls.name}\n\n"
            doc += "[TODO: Add class description]\n\n"

    if functions:
        doc += "## Key Functions\n\n"
        for func in functions:
            doc += f"### {func.name}\n\n"
            doc += "[TODO: Add function description]\n\n"

    doc += "## Usage Examples\n\n[TODO: Add examples]\n\n"
    doc += "## See Also\n\n[TODO: Add related modules]\n"

    return doc
```

### Verifying Documentation Coverage

```bash
# List all Python modules
find src/spreadsheet_dl -name "*.py" -type f | wc -l

# List documented modules
find docs/api -name "*.md" -type f | wc -l

# Find undocumented modules
comm -23 \
  <(find src/spreadsheet_dl -name "*.py" -exec basename {} .py \; | sort) \
  <(find docs/api -name "*.md" -exec basename {} .md \; | sort)
```

## Documentation Metrics

Target metrics for complete documentation:

- ✅ **Module Coverage**: 27/27 modules (currently 5/27 = 18.5%)
- ⏳ **Class Coverage**: All public classes
- ⏳ **Method Coverage**: All public methods
- ⏳ **Function Coverage**: All module-level functions
- ⏳ **Example Coverage**: At least 3 examples per module
- ⏳ **Cross-Reference Coverage**: All related modules linked

## See Also

- [User Guide](../user-guide.md) - High-level usage guide
- [Development Guide](../CONTRIBUTING.md) - Contributing guidelines
- [Changelog](../CHANGELOG.md) - Version history
- [Requirements](../../requirements/) - Feature requirements
