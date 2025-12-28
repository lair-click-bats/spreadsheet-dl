#!/usr/bin/env bash
# =============================================================================
# Markdown Formatter for Workspace Template
# =============================================================================
# Formats and lints markdown files using prettier and markdownlint
# Usage: ./scripts/format_markdown.sh [--check] [--fix] [--lint] [path]
# =============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Defaults
MODE="format" # format, check, lint, fix
TARGET=""

# =============================================================================
# Helper Functions
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    command -v "$1" &>/dev/null
}

show_help() {
    echo "Usage: $0 [OPTIONS] [path]"
    echo ""
    echo "Options:"
    echo "  --check     Check formatting without modifying files"
    echo "  --fix       Fix formatting and lint issues"
    echo "  --lint      Run linting only (markdownlint)"
    echo "  --format    Run formatting only (prettier)"
    echo "  -h, --help  Show this help message"
    echo ""
    echo "Path:"
    echo "  Optional path to file or directory (default: entire repo)"
    echo ""
    echo "Examples:"
    echo "  $0                     # Format all markdown files"
    echo "  $0 --check             # Check all files without modifying"
    echo "  $0 --fix README.md     # Fix specific file"
    echo "  $0 --lint base/        # Lint files in directory"
}

# =============================================================================
# Argument Parsing
# =============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
    --check)
        MODE="check"
        shift
        ;;
    --fix)
        MODE="fix"
        shift
        ;;
    --lint)
        MODE="lint"
        shift
        ;;
    --format)
        MODE="format"
        shift
        ;;
    -h | --help)
        show_help
        exit 0
        ;;
    -*)
        log_error "Unknown option: $1"
        show_help
        exit 1
        ;;
    *)
        TARGET="$1"
        shift
        ;;
    esac
done

# Default target
if [[ -z "$TARGET" ]]; then
    TARGET="$REPO_ROOT"
fi

# Make target absolute
if [[ ! "$TARGET" = /* ]]; then
    TARGET="$REPO_ROOT/$TARGET"
fi

# =============================================================================
# Dependency Check
# =============================================================================

HAS_PRETTIER=false
HAS_MARKDOWNLINT=false

if check_command prettier; then
    HAS_PRETTIER=true
fi

if check_command markdownlint-cli2; then
    HAS_MARKDOWNLINT=true
fi

if [[ "$HAS_PRETTIER" == "false" && "$HAS_MARKDOWNLINT" == "false" ]]; then
    log_error "No markdown tools found"
    echo ""
    echo "Install at least one of:"
    echo "  prettier:         npm install -g prettier"
    echo "  markdownlint:     npm install -g markdownlint-cli2"
    exit 1
fi

# =============================================================================
# Formatting Functions
# =============================================================================

run_prettier_check() {
    local target=$1
    log_info "Checking formatting with prettier..."

    if [[ -f "$target" ]]; then
        if prettier --check "$target" 2>/dev/null; then
            log_success "$(basename "$target") is formatted correctly"
            return 0
        else
            log_warning "$(basename "$target") needs formatting"
            return 1
        fi
    else
        if prettier --check "$target/**/*.md" 2>/dev/null; then
            log_success "All files formatted correctly"
            return 0
        else
            log_warning "Some files need formatting"
            return 1
        fi
    fi
}

run_prettier_format() {
    local target=$1
    log_info "Formatting with prettier..."

    local config_args=""
    if [[ -f "$REPO_ROOT/.prettierrc.yaml" ]]; then
        config_args="--config $REPO_ROOT/.prettierrc.yaml"
    fi

    local ignore_args=""
    if [[ -f "$REPO_ROOT/.prettierignore" ]]; then
        ignore_args="--ignore-path $REPO_ROOT/.prettierignore"
    fi

    if [[ -f "$target" ]]; then
        # shellcheck disable=SC2086 # Intentional word splitting for optional args
        prettier --write $config_args $ignore_args "$target" 2>/dev/null
        log_success "Formatted $(basename "$target")"
    else
        # shellcheck disable=SC2086 # Intentional word splitting for optional args
        prettier --write $config_args $ignore_args "$target/**/*.md" 2>/dev/null || true
        log_success "Formatting complete"
    fi
}

run_markdownlint_check() {
    local target=$1
    log_info "Linting with markdownlint..."

    local config_args=""
    if [[ -f "$REPO_ROOT/.markdownlint.yaml" ]]; then
        config_args="--config $REPO_ROOT/.markdownlint.yaml"
    fi

    if [[ -f "$target" ]]; then
        # shellcheck disable=SC2086 # Intentional word splitting for optional args
        if markdownlint-cli2 $config_args "$target" 2>/dev/null; then
            log_success "$(basename "$target") passes linting"
            return 0
        else
            log_warning "$(basename "$target") has lint issues"
            return 1
        fi
    else
        # shellcheck disable=SC2086 # Intentional word splitting for optional args
        if markdownlint-cli2 $config_args "$target/**/*.md" 2>/dev/null; then
            log_success "All files pass linting"
            return 0
        else
            log_warning "Some files have lint issues"
            return 1
        fi
    fi
}

run_markdownlint_fix() {
    local target=$1
    log_info "Fixing lint issues with markdownlint..."

    local config_args=""
    if [[ -f "$REPO_ROOT/.markdownlint.yaml" ]]; then
        config_args="--config $REPO_ROOT/.markdownlint.yaml"
    fi

    if [[ -f "$target" ]]; then
        # shellcheck disable=SC2086 # Intentional word splitting for optional args
        markdownlint-cli2 --fix $config_args "$target" 2>/dev/null || true
        log_success "Fixed $(basename "$target")"
    else
        # shellcheck disable=SC2086 # Intentional word splitting for optional args
        markdownlint-cli2 --fix $config_args "$target/**/*.md" 2>/dev/null || true
        log_success "Lint fixes applied"
    fi
}

# =============================================================================
# Main Execution
# =============================================================================

log_info "Target: $TARGET"
log_info "Mode: $MODE"
echo ""

EXIT_CODE=0

case $MODE in
check)
    if [[ "$HAS_PRETTIER" == "true" ]]; then
        run_prettier_check "$TARGET" || EXIT_CODE=1
    fi
    if [[ "$HAS_MARKDOWNLINT" == "true" ]]; then
        run_markdownlint_check "$TARGET" || EXIT_CODE=1
    fi
    ;;
format)
    if [[ "$HAS_PRETTIER" == "true" ]]; then
        run_prettier_format "$TARGET"
    else
        log_warning "prettier not available, skipping format"
    fi
    ;;
lint)
    if [[ "$HAS_MARKDOWNLINT" == "true" ]]; then
        run_markdownlint_check "$TARGET" || EXIT_CODE=1
    else
        log_error "markdownlint-cli2 not available"
        EXIT_CODE=1
    fi
    ;;
fix)
    if [[ "$HAS_PRETTIER" == "true" ]]; then
        run_prettier_format "$TARGET"
    fi
    if [[ "$HAS_MARKDOWNLINT" == "true" ]]; then
        run_markdownlint_fix "$TARGET"
    fi
    ;;
esac

echo ""
if [[ $EXIT_CODE -eq 0 ]]; then
    log_success "Done!"
else
    log_warning "Completed with warnings"
fi

exit $EXIT_CODE
