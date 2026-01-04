#!/usr/bin/env python3
"""Script to add pytest markers to all test files systematically."""

from pathlib import Path

# Marker mappings based on test file patterns and characteristics
MARKER_MAP: dict[str, list[str]] = {
    # Unit tests - core functionality
    "test_schema.py": ["unit", "validation"],
    "test_schema_units.py": ["unit", "validation"],
    "test_builder.py": ["unit", "builder"],
    "test_builders.py": ["unit", "builder"],
    "test_exceptions.py": ["unit"],
    "test_serialization.py": ["unit"],
    "test_categories.py": ["unit", "finance"],
    # Integration tests
    "test_integration.py": ["integration", "requires_files", "finance"],
    # Performance tests
    "test_performance.py": ["unit", "benchmark"],
    # CLI tests
    "test_cli.py": ["unit", "cli"],
    "test_cli_themes.py": ["unit", "cli"],
    "test_interactive.py": ["integration", "cli"],
    # MCP server tests
    "test_mcp_server.py": ["unit", "mcp"],
    "test_mcp_tools_extended.py": ["unit", "mcp"],
    "test_completions.py": ["unit", "mcp"],
    # Finance tests
    "test_accounts.py": ["unit", "finance"],
    "test_alerts.py": ["unit", "finance"],
    "test_analytics.py": ["unit", "finance"],
    "test_budget_analyzer.py": ["unit", "finance"],
    "test_currency.py": ["unit", "finance"],
    "test_bank_formats.py": ["unit", "finance"],
    "test_goals.py": ["unit", "finance"],
    "test_recurring.py": ["unit", "finance"],
    # File I/O and rendering tests
    "test_ods_generator.py": ["integration", "requires_files", "rendering"],
    "test_ods_editor.py": ["integration", "requires_files", "rendering"],
    "test_renderer.py": ["unit", "rendering"],
    "test_export.py": ["integration", "requires_files", "requires_export", "rendering"],
    "test_csv_import.py": ["unit", "requires_files"],
    "test_backup.py": ["integration", "requires_files"],
    # Configuration and templates
    "test_config.py": ["unit", "requires_yaml"],
    "test_templates.py": ["unit", "templates"],
    "test_template_engine.py": ["unit", "templates"],
    "test_professional_templates.py": ["unit", "templates"],
    "test_themes.py": ["unit", "validation"],
    # Charts and visualization
    "test_charts.py": ["unit", "visualization"],
    "test_visualization.py": ["unit", "visualization"],
    # Reports and output
    "test_report_generator.py": ["integration", "requires_files"],
    "test_print_layout.py": ["unit", "rendering"],
    "test_typography.py": ["unit", "rendering"],
    # Notifications and reminders
    "test_notifications.py": ["unit"],
    "test_reminders.py": ["unit"],
    "test_progress.py": ["unit"],
    # Plugins and adapters
    "test_plugins.py": ["unit", "domain"],
    "test_adapters.py": ["unit"],
    # Security
    "test_security.py": ["unit"],
    # Integrations
    "test_plaid_integration.py": ["integration", "finance"],
    "test_webdav.py": ["integration"],
    "test_streaming.py": ["integration"],
    # AI/Training
    "test_ai_export.py": ["unit", "mcp"],
    "test_ai_training.py": ["unit", "mcp"],
    # Validation
    "test_validation_v4.py": ["integration", "validation"],
    # Backward compatibility
    "test_backward_compatibility.py": ["integration"],
    # Domain tests
    "domains/test_base.py": ["unit", "domain"],
    "domains/test_finance.py": ["unit", "domain", "finance"],
    "domains/test_data_science.py": ["unit", "domain", "science"],
    "domains/test_biology.py": ["unit", "domain", "science"],
    "domains/test_education.py": ["unit", "domain"],
    "domains/test_environmental.py": ["unit", "domain", "science"],
    "domains/test_electrical_engineering.py": ["unit", "domain", "engineering"],
    "domains/test_mechanical_engineering.py": ["unit", "domain", "engineering"],
    "domains/test_civil_engineering.py": ["unit", "domain", "engineering"],
    "domains/test_manufacturing.py": ["unit", "domain", "manufacturing"],
    # Hook tests
    ".claude/hooks/test_hooks.py": ["unit"],
    ".claude/hooks/test_quality_enforcement.py": ["unit"],
}


def add_markers_to_file(file_path: Path, markers: list[str]) -> bool:
    """Add pytest markers to a test file if not already present."""
    content = file_path.read_text()

    # Check if markers already present
    if "pytestmark = " in content:
        print(f"⏭️  {file_path.name}: Already has markers")
        return False

    # Find the position after imports using a state machine
    lines = content.split("\n")
    insert_index = 0
    in_multiline_import = False
    in_type_checking = False
    paren_depth = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Track parentheses for multi-line imports
        paren_depth += stripped.count("(") - stripped.count(")")

        # Check for TYPE_CHECKING block
        if stripped.startswith("if TYPE_CHECKING:"):
            in_type_checking = True
            continue

        # End of TYPE_CHECKING block (dedent back to module level)
        if (
            in_type_checking
            and line
            and not line[0].isspace()
            and not stripped.startswith(("#", "if", "elif", "else"))
        ):
            in_type_checking = False
            insert_index = i
            break

        # Regular import tracking
        if not in_type_checking:
            if stripped.startswith(("from ", "import ")):
                in_multiline_import = paren_depth > 0
                if not in_multiline_import:
                    insert_index = i + 1
            elif in_multiline_import and paren_depth == 0:
                # End of multi-line import
                in_multiline_import = False
                insert_index = i + 1
            elif stripped.startswith(("class ", "def ", "@pytest")):
                # Reached first class/function
                break

    # Create marker line
    marker_str = f"pytestmark = [pytest.mark.{', pytest.mark.'.join(markers)}]"

    # Insert markers
    lines.insert(insert_index, "")
    lines.insert(insert_index + 1, marker_str)

    # Write back
    file_path.write_text("\n".join(lines))
    print(f"✅ {file_path.name}: Added markers {markers}")
    return True


def main() -> None:
    """Add markers to all test files."""
    project_root = Path(__file__).parent.parent
    tests_dir = project_root / "tests"

    updated = 0
    skipped = 0

    for rel_path, markers in MARKER_MAP.items():
        if rel_path.startswith(".claude"):
            file_path = project_root / rel_path
        elif "/" in rel_path:
            file_path = tests_dir / rel_path
        else:
            file_path = tests_dir / rel_path

        if not file_path.exists():
            print(f"⚠️  {rel_path}: File not found")
            continue

        if add_markers_to_file(file_path, markers):
            updated += 1
        else:
            skipped += 1

    print(f"\n📊 Summary: {updated} files updated, {skipped} files skipped")


if __name__ == "__main__":
    main()
