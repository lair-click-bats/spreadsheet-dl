#!/usr/bin/env bash
# =============================================================================
# cleanup.sh - Remove temporary/generated files
# =============================================================================
# Usage: ./scripts/cleanup.sh [-v] [--dry-run]
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Defaults
VERBOSE=false
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
    -v | --verbose)
        VERBOSE=true
        shift
        ;;
    --dry-run)
        DRY_RUN=true
        VERBOSE=true
        shift
        ;;
    -h | --help)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Remove temporary and generated files"
        echo ""
        echo "Options:"
        echo "  -v, --verbose  Show files being removed"
        echo "  --dry-run      Show what would be removed without actually deleting"
        echo "  -h, --help     Show this help message"
        echo ""
        echo "Files removed:"
        echo "  - latexindent backups (*.bak0, *.bak1, etc.)"
        echo "  - perltidy backups (*.bak)"
        echo "  - GHDL work files (work-obj*.cf)"
        exit 0
        ;;
    *)
        echo "Unknown option: $1" >&2
        exit 2
        ;;
    esac
done

echo "=== CLEANUP ==="
echo ""
echo "Repository: $REPO_ROOT"
echo ""

cleanup_count=0

remove_file() {
    local file="$1"
    if $DRY_RUN; then
        echo "  Would remove: $file"
    else
        if $VERBOSE; then
            echo "  Removing: $file"
        fi
        rm -f "$file"
    fi
    ((cleanup_count++)) || true
}

# Clean up latexindent backup files (*.bak0, *.bak1, etc.)
echo "Checking for latexindent backup files..."
while IFS= read -r -d '' file; do
    remove_file "$file"
done < <(find "$REPO_ROOT" -type f \( -name "*.bak[0-9]" -o -name "*.bak[0-9][0-9]" \) -not -path "*/.git/*" -not -path "*/.venv/*" -print0 2>/dev/null)

# Clean up perltidy backup files (*.bak)
echo "Checking for perltidy backup files..."
while IFS= read -r -d '' file; do
    remove_file "$file"
done < <(find "$REPO_ROOT" -type f -name "*.bak" -not -path "*/.git/*" -not -path "*/.venv/*" -print0 2>/dev/null)

# Clean up GHDL work files (work-obj*.cf)
echo "Checking for GHDL work files..."
while IFS= read -r -d '' file; do
    remove_file "$file"
done < <(find "$REPO_ROOT" -type f -name "work-obj*.cf" -not -path "*/.git/*" -not -path "*/.venv/*" -print0 2>/dev/null)

echo ""
if [[ $cleanup_count -gt 0 ]]; then
    if $DRY_RUN; then
        echo "Would remove $cleanup_count file(s)"
    else
        echo "Removed $cleanup_count file(s)"
    fi
else
    echo "No files to remove"
fi
