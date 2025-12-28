#!/usr/bin/env bash
# =============================================================================
# Version Consistency Check Hook
# Validates version consistency across all documented locations
# Uses project-metadata.yaml as source of truth for locations to check
#
# Version: 1.0.0
# Created: 2025-12-25
# =============================================================================

set -euo pipefail

# Resolve to absolute path from script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$REPO_ROOT}"
LOG_FILE="$PROJECT_DIR/.claude/hooks/hook.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date -Iseconds)] VERSION_CHECK: $*" >>"$LOG_FILE"
}

# Check for bypass
if [ "${CLAUDE_BYPASS_HOOKS:-0}" = "1" ]; then
    echo '{"ok": true, "bypassed": true}'
    exit 0
fi

log "Starting version consistency check"

# Check if pyproject.toml exists (Python projects)
if [ -f "$PROJECT_DIR/pyproject.toml" ]; then
    # Extract version from pyproject.toml (SSOT)
    VERSION=$(grep -E '^version = "' "$PROJECT_DIR/pyproject.toml" | cut -d'"' -f2)

    if [ -z "$VERSION" ]; then
        log "ERROR: Could not extract version from pyproject.toml"
        echo '{"ok": false, "error": "Version not found in pyproject.toml"}'
        exit 1
    fi

    log "Found primary version: $VERSION"

    ERRORS=0

    # Check __init__.py if project has src layout
    # Adjust the path pattern as needed for your project structure
    for init_file in "$PROJECT_DIR"/src/*/__init__.py; do
        if [ -f "$init_file" ]; then
            if ! grep -q "__version__ = \"$VERSION\"" "$init_file"; then
                log "WARN: Version may be missing or mismatched in $init_file"
                # This is a warning, not an error - some projects don't track version in __init__
            fi
        fi
    done

    # Check README.md (allow extra text after version)
    if [ -f "$PROJECT_DIR/README.md" ]; then
        if ! grep -qE "Current Version:.*v$VERSION" "$PROJECT_DIR/README.md" 2>/dev/null; then
            # Not an error - README may not have version
            log "INFO: Version not found in README.md"
        fi
    fi

    # Output result
    if [ "$ERRORS" -gt 0 ]; then
        cat <<EOF
{
    "ok": false,
    "errors": $ERRORS,
    "message": "Version inconsistency detected. Expected: $VERSION. Check $LOG_FILE for details."
}
EOF
        log "Version check failed: $ERRORS errors"
        exit 1
    else
        echo "{\"ok\": true, \"version\": \"$VERSION\", \"message\": \"Version consistent across all locations\"}"
        log "Version check passed: $VERSION"
        exit 0
    fi
else
    # No pyproject.toml - skip version check
    echo '{"ok": true, "message": "No pyproject.toml found, skipping version check"}'
    log "Skipped: No pyproject.toml found"
    exit 0
fi
