#!/bin/bash
# Validation script for nextcloud-finance-ods
# Runs all quality checks and tests

set -e

cd "$(dirname "$0")/.."

echo "=== Validation Suite ==="
echo ""

# Track failures
FAILURES=0

# Ruff check
echo "1. Ruff Lint Check"
echo "-------------------"
if uv run ruff check src/ tests/; then
    echo "PASS: Linting passed"
else
    echo "FAIL: Linting issues found"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Ruff format
echo "2. Ruff Format Check"
echo "--------------------"
if uv run ruff format --check src/ tests/; then
    echo "PASS: Formatting correct"
else
    echo "FAIL: Formatting issues found"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Mypy
echo "3. Mypy Type Check"
echo "------------------"
if uv run mypy src/; then
    echo "PASS: Type checking passed"
else
    echo "FAIL: Type errors found"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Pytest
echo "4. Pytest"
echo "---------"
if uv run pytest -v; then
    echo "PASS: All tests passed"
else
    echo "FAIL: Test failures"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# ODS Generation Test
echo "5. ODS Generation Test"
echo "----------------------"
mkdir -p output
if uv run python -c "
from finance_tracker.ods_generator import create_monthly_budget
from pathlib import Path
path = create_monthly_budget('output')
assert path.exists(), 'File not created'
assert path.stat().st_size > 0, 'File is empty'
print(f'Generated: {path} ({path.stat().st_size} bytes)')
"; then
    echo "PASS: ODS generation works"
else
    echo "FAIL: ODS generation failed"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# ODS Analysis Test
echo "6. ODS Analysis Test"
echo "--------------------"
if uv run python -c "
from finance_tracker.budget_analyzer import analyze_budget
from pathlib import Path
ods_files = list(Path('output').glob('*.ods'))
if ods_files:
    result = analyze_budget(ods_files[0])
    assert 'total_budget' in result
    assert 'total_spent' in result
    print(f'Analysis complete: budget=\${result[\"total_budget\"]:,.2f}')
else:
    print('No ODS files to analyze')
"; then
    echo "PASS: ODS analysis works"
else
    echo "FAIL: ODS analysis failed"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Report Generation Test
echo "7. Report Generation Test"
echo "-------------------------"
if uv run python -c "
from finance_tracker.report_generator import generate_monthly_report
from pathlib import Path
ods_files = list(Path('output').glob('*.ods'))
if ods_files:
    report = generate_monthly_report(ods_files[0], format='text')
    assert 'BUDGET REPORT' in report
    print('Report generated successfully')
    print(report[:200] + '...')
else:
    print('No ODS files for report')
"; then
    echo "PASS: Report generation works"
else
    echo "FAIL: Report generation failed"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# Summary
echo "=== Summary ==="
if [ $FAILURES -eq 0 ]; then
    echo "All checks passed!"
    exit 0
else
    echo "$FAILURES check(s) failed"
    exit 1
fi
