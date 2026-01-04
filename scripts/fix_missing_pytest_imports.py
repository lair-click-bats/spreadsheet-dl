#!/usr/bin/env python3
"""Fix missing pytest imports in test files with pytestmark."""

from pathlib import Path


def fix_file(file_path: Path) -> bool:
    """Add pytest import if pytestmark exists but import pytest doesn't."""
    content = file_path.read_text()

    # Check if file has pytestmark
    if "pytestmark = " not in content:
        return False

    # Check if pytest is already imported
    if "import pytest" in content:
        return False

    lines = content.split("\n")
    insert_index = 0

    # Find where to insert (after __future__ imports)
    for i, line in enumerate(lines):
        if line.strip().startswith("from __future__ import"):
            insert_index = i + 1
            break

    # Insert import pytest
    lines.insert(insert_index, "")
    lines.insert(insert_index + 1, "import pytest")

    file_path.write_text("\n".join(lines))
    print(f"✅ {file_path.name}: Added pytest import")
    return True


def main() -> None:
    """Fix all test files."""
    project_root = Path(__file__).parent.parent
    tests_dir = project_root / "tests"

    fixed = 0
    for test_file in tests_dir.rglob("test_*.py"):
        if fix_file(test_file):
            fixed += 1

    print(f"\n📊 Fixed {fixed} files")


if __name__ == "__main__":
    main()
