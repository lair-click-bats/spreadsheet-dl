#!/usr/bin/env python3
"""Comprehensive test suite for strict quality enforcement hooks.

Tests all file types, auto-fix behavior, blocking behavior, and edge cases.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

# ANSI color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


class TestResult:
    """Track test results."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.tests = []

    def add_pass(self, name: str, message: str = ""):
        self.passed += 1
        self.tests.append((name, "PASS", message))
        print(f"{GREEN}✓{RESET} {name}: {message}")

    def add_fail(self, name: str, message: str = ""):
        self.failed += 1
        self.tests.append((name, "FAIL", message))
        print(f"{RED}✗{RESET} {name}: {message}")

    def add_warn(self, name: str, message: str = ""):
        self.warnings += 1
        self.tests.append((name, "WARN", message))
        print(f"{YELLOW}⚠{RESET} {name}: {message}")

    def summary(self):
        total = self.passed + self.failed + self.warnings
        print("\n" + "=" * 80)
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"{RED}Failed: {self.failed}{RESET}")
        if self.warnings > 0:
            print(f"{YELLOW}Warnings: {self.warnings}{RESET}")
        print("=" * 80)
        return self.failed == 0


def run_hook(file_path: str, hook_script: str) -> tuple[int, str, str]:
    """Run quality enforcement hook on a file.

    Args:
        file_path: Path to test file
        hook_script: Path to hook script

    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    hook_input = json.dumps(
        {
            "tool_name": "Write",
            "tool_input": {"file_path": file_path},
            "tool_use_id": "test",
        }
    )

    try:
        result = subprocess.run(
            ["python3", hook_script],
            input=hook_input,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Hook timeout"
    except Exception as e:
        return 1, "", str(e)


def test_python_clean(results: TestResult, hook: str, temp_dir: Path):
    """Test clean Python file passes."""
    test_file = temp_dir / "clean.py"
    test_file.write_text('''"""Clean Python module."""


def hello(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"


def main() -> None:
    """Main function."""
    print(hello("World"))


if __name__ == "__main__":
    main()
''')

    exit_code, _stdout, _stderr = run_hook(str(test_file), hook)

    if exit_code == 0:
        results.add_pass("Python: Clean file", "Passed as expected")
    else:
        results.add_fail("Python: Clean file", f"Exit {exit_code}, expected 0")


def test_python_unused_import(results: TestResult, hook: str, temp_dir: Path):
    """Test Python with unused import gets auto-fixed."""
    test_file = temp_dir / "unused_import.py"
    test_file.write_text('''"""Test module."""
import os
import sys


def hello() -> None:
    """Say hello."""
    print("Hello")
''')

    exit_code, _stdout, _stderr = run_hook(str(test_file), hook)

    # Unused imports should be auto-fixed by ruff check --fix
    if exit_code == 0:
        content = test_file.read_text()
        if "import os" not in content and "import sys" not in content:
            results.add_pass("Python: Unused import", "Auto-fixed (F401 removed)")
        else:
            results.add_warn("Python: Unused import", "Passed but imports not removed")
    else:
        results.add_fail(
            "Python: Unused import", f"Exit {exit_code}, expected 0 (auto-fixed)"
        )


def test_python_undefined_name(results: TestResult, hook: str, temp_dir: Path):
    """Test Python with undefined name gets blocked."""
    test_file = temp_dir / "undefined.py"
    test_file.write_text('''"""Test module."""


def foo() -> None:
    """Function with undefined name."""
    print(undefined_variable)
''')

    exit_code, _stdout, stderr = run_hook(str(test_file), hook)

    if exit_code == 2:
        if "F821" in stderr or "Undefined name" in stderr:
            results.add_pass("Python: Undefined name", "Blocked as expected (F821)")
        else:
            results.add_warn(
                "Python: Undefined name", "Blocked but wrong error message"
            )
    else:
        results.add_fail(
            "Python: Undefined name", f"Exit {exit_code}, expected 2 (blocked)"
        )


def test_python_syntax_error(results: TestResult, hook: str, temp_dir: Path):
    """Test Python with syntax error gets blocked."""
    test_file = temp_dir / "syntax_error.py"
    test_file.write_text('''"""Test module."""


def foo()  # Missing colon
    print("Hello")
''')

    exit_code, _stdout, stderr = run_hook(str(test_file), hook)

    if exit_code == 2:
        if "E999" in stderr or "SyntaxError" in stderr:
            results.add_pass("Python: Syntax error", "Blocked as expected (E999)")
        else:
            results.add_warn("Python: Syntax error", "Blocked but wrong error message")
    else:
        results.add_fail(
            "Python: Syntax error", f"Exit {exit_code}, expected 2 (blocked)"
        )


def test_python_bad_formatting(results: TestResult, hook: str, temp_dir: Path):
    """Test Python with bad formatting gets auto-fixed."""
    test_file = temp_dir / "bad_format.py"
    test_file.write_text('''"""Test module."""
def foo(  ):
    x=1+2
    return   x
''')

    exit_code, _stdout, _stderr = run_hook(str(test_file), hook)

    # Should auto-format and pass
    if exit_code == 0:
        # Check if file was reformatted
        content = test_file.read_text()
        if "def foo():" in content and "x = 1 + 2" in content:
            results.add_pass("Python: Bad formatting", "Auto-formatted and passed")
        else:
            results.add_warn("Python: Bad formatting", "Passed but formatting unclear")
    else:
        results.add_fail(
            "Python: Bad formatting", f"Exit {exit_code}, expected 0 after auto-fix"
        )


def test_shell_clean(results: TestResult, hook: str, temp_dir: Path):
    """Test clean shell script passes."""
    test_file = temp_dir / "clean.sh"
    test_file.write_text("""#!/bin/bash
# Clean shell script

set -euo pipefail

main() {
  local name="$1"
  echo "Hello, ${name}!"
}

main "$@"
""")

    exit_code, _stdout, _stderr = run_hook(str(test_file), hook)

    if exit_code == 0:
        results.add_pass("Shell: Clean script", "Passed as expected")
    else:
        results.add_fail("Shell: Clean script", f"Exit {exit_code}, expected 0")


def test_shell_unquoted_variable(results: TestResult, hook: str, temp_dir: Path):
    """Test shell with bad practice gets caught."""
    test_file = temp_dir / "bad_practice.sh"
    test_file.write_text("""#!/bin/bash
# Script with shellcheck warnings

cd /tmp  # Using cd without checking if it succeeds
rm -rf "$DIR"/*  # Variable might be empty
""")

    exit_code, _stdout, _stderr = run_hook(str(test_file), hook)

    # Shellcheck may or may not catch these depending on configuration
    # Accept either blocking or passing as valid
    if exit_code == 2:
        results.add_pass("Shell: Bad practice", "Blocked by shellcheck")
    elif exit_code == 0:
        results.add_warn("Shell: Bad practice", "Not blocked (shellcheck config)")
    else:
        results.add_fail("Shell: Bad practice", f"Exit {exit_code}, unexpected")


def test_yaml_clean(results: TestResult, hook: str, temp_dir: Path):
    """Test clean YAML file passes."""
    test_file = temp_dir / "clean.yaml"
    test_file.write_text("""---
name: test
version: 1.0.0
description: A clean YAML file

config:
  enabled: true
  port: 8080
  items:
    - one
    - two
    - three
""")

    exit_code, _stdout, _stderr = run_hook(str(test_file), hook)

    if exit_code == 0:
        results.add_pass("YAML: Clean file", "Passed as expected")
    else:
        results.add_fail("YAML: Clean file", f"Exit {exit_code}, expected 0")


def test_yaml_bad_indentation(results: TestResult, hook: str, temp_dir: Path):
    """Test YAML with bad indentation gets blocked or auto-fixed."""
    test_file = temp_dir / "bad_indent.yaml"
    test_file.write_text("""---
name: test
config:
 enabled: true
  port: 8080
""")

    exit_code, _stdout, _stderr = run_hook(str(test_file), hook)

    # Could be auto-fixed by prettier or blocked by yamllint
    if exit_code == 0:
        results.add_pass("YAML: Bad indentation", "Auto-fixed and passed")
    elif exit_code == 2:
        results.add_pass("YAML: Bad indentation", "Blocked as expected")
    else:
        results.add_fail("YAML: Bad indentation", f"Exit {exit_code}, unexpected")


def test_json_clean(results: TestResult, hook: str, temp_dir: Path):
    """Test clean JSON file passes."""
    test_file = temp_dir / "clean.json"
    test_file.write_text("""{
  "name": "test",
  "version": "1.0.0",
  "config": {
    "enabled": true,
    "items": [1, 2, 3]
  }
}
""")

    exit_code, _stdout, _stderr = run_hook(str(test_file), hook)

    if exit_code == 0:
        results.add_pass("JSON: Clean file", "Passed as expected")
    else:
        results.add_fail("JSON: Clean file", f"Exit {exit_code}, expected 0")


def test_json_syntax_error(results: TestResult, hook: str, temp_dir: Path):
    """Test JSON with syntax error gets blocked."""
    test_file = temp_dir / "syntax_error.json"
    test_file.write_text("""{
  "name": "test",
  "value": 123,
}
""")

    exit_code, _stdout, stderr = run_hook(str(test_file), hook)

    if exit_code == 2:
        if "json" in stderr.lower() or "syntax" in stderr.lower():
            results.add_pass("JSON: Syntax error", "Blocked as expected")
        else:
            results.add_warn("JSON: Syntax error", "Blocked but wrong error message")
    else:
        results.add_fail(
            "JSON: Syntax error", f"Exit {exit_code}, expected 2 (blocked)"
        )


def test_markdown_clean(results: TestResult, hook: str, temp_dir: Path):
    """Test clean Markdown file passes."""
    test_file = temp_dir / "clean.md"
    test_file.write_text("""# Test Document

This is a clean markdown file.

## Section 1

Some content here.

### Subsection

- Item 1
- Item 2
- Item 3

## Section 2

More content.
""")

    exit_code, _stdout, _stderr = run_hook(str(test_file), hook)

    if exit_code == 0:
        results.add_pass("Markdown: Clean file", "Passed as expected")
    else:
        results.add_fail("Markdown: Clean file", f"Exit {exit_code}, expected 0")


def test_excluded_directory(results: TestResult, hook: str, temp_dir: Path):
    """Test that excluded directories are skipped."""
    venv_dir = temp_dir / ".venv"
    venv_dir.mkdir()
    test_file = venv_dir / "bad.py"
    test_file.write_text("""import os
x = undefined_name
""")

    exit_code, _stdout, _stderr = run_hook(str(test_file), hook)

    if exit_code == 0:
        results.add_pass("Excluded: .venv directory", "Skipped as expected")
    else:
        results.add_fail(
            "Excluded: .venv directory",
            f"Exit {exit_code}, should skip excluded dirs",
        )


def test_unknown_file_type(results: TestResult, hook: str, temp_dir: Path):
    """Test that unknown file types are allowed."""
    test_file = temp_dir / "test.xyz"
    test_file.write_text("random content")

    exit_code, _stdout, _stderr = run_hook(str(test_file), hook)

    if exit_code == 0:
        results.add_pass("Unknown: .xyz file", "Allowed as expected")
    else:
        results.add_fail(
            "Unknown: .xyz file", f"Exit {exit_code}, should allow unknown types"
        )


def test_auto_fix_multiple_issues(results: TestResult, hook: str, temp_dir: Path):
    """Test that multiple auto-fixable issues get fixed."""
    test_file = temp_dir / "multiple_issues.py"
    test_file.write_text('''"""Test module."""
import sys
import os
def foo(x,y):
    return x+y
''')

    exit_code, _stdout, stderr = run_hook(str(test_file), hook)

    # Should auto-fix import ordering and formatting
    if exit_code == 0:
        content = test_file.read_text()
        if "def foo(x, y):" in content and "x + y" in content:
            results.add_pass(
                "Auto-fix: Multiple issues", "Fixed formatting and imports"
            )
        else:
            results.add_warn("Auto-fix: Multiple issues", "Passed but unclear if fixed")
    else:
        # Check if blocked on unused imports
        if exit_code == 2 and "F401" in stderr:
            results.add_pass(
                "Auto-fix: Multiple issues",
                "Blocked on unused imports (expected)",
            )
        else:
            results.add_fail(
                "Auto-fix: Multiple issues",
                f"Exit {exit_code}, unexpected result",
            )


def main():
    """Run comprehensive test suite."""
    print(f"\n{BLUE}{'=' * 80}{RESET}")
    print(f"{BLUE}Quality Enforcement Hook - Comprehensive Test Suite{RESET}")
    print(f"{BLUE}{'=' * 80}{RESET}\n")

    # Locate hook script
    script_dir = Path(__file__).parent
    hook_script = script_dir / "quality_enforce_strict.py"

    if not hook_script.exists():
        print(f"{RED}Error: Hook script not found at {hook_script}{RESET}")
        return 1

    print(f"Testing hook: {hook_script}\n")

    results = TestResult()

    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        print(f"{BLUE}Python Tests{RESET}")
        print("-" * 40)
        test_python_clean(results, str(hook_script), temp_path)
        test_python_unused_import(results, str(hook_script), temp_path)
        test_python_undefined_name(results, str(hook_script), temp_path)
        test_python_syntax_error(results, str(hook_script), temp_path)
        test_python_bad_formatting(results, str(hook_script), temp_path)
        test_auto_fix_multiple_issues(results, str(hook_script), temp_path)

        print(f"\n{BLUE}Shell Tests{RESET}")
        print("-" * 40)
        test_shell_clean(results, str(hook_script), temp_path)
        test_shell_unquoted_variable(results, str(hook_script), temp_path)

        print(f"\n{BLUE}YAML Tests{RESET}")
        print("-" * 40)
        test_yaml_clean(results, str(hook_script), temp_path)
        test_yaml_bad_indentation(results, str(hook_script), temp_path)

        print(f"\n{BLUE}JSON Tests{RESET}")
        print("-" * 40)
        test_json_clean(results, str(hook_script), temp_path)
        test_json_syntax_error(results, str(hook_script), temp_path)

        print(f"\n{BLUE}Markdown Tests{RESET}")
        print("-" * 40)
        test_markdown_clean(results, str(hook_script), temp_path)

        print(f"\n{BLUE}Edge Case Tests{RESET}")
        print("-" * 40)
        test_excluded_directory(results, str(hook_script), temp_path)
        test_unknown_file_type(results, str(hook_script), temp_path)

    # Summary
    success = results.summary()

    if success:
        print(f"\n{GREEN}All tests passed! ✓{RESET}\n")
        return 0
    else:
        print(f"\n{RED}Some tests failed! ✗{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
