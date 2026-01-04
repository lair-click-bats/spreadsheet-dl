#!/usr/bin/env bash
# Cleanup script for preparing repository for public release
# Removes development artifacts from .coordination/ and .claude/agent-outputs/

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Pre-Release Cleanup Script ===${NC}"
echo ""

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Counter for removed files
REMOVED_COUNT=0

echo -e "${YELLOW}Phase 1: Cleaning .coordination/ directory${NC}"
echo "-------------------------------------------"

# Remove dated coordination files
echo "Removing dated coordination markdown files..."
find .coordination/ -type f -name "2025-*.md" -delete 2>/dev/null || true
find .coordination/ -type f -name "2026-*.md" -delete 2>/dev/null || true
REMOVED_COUNT=$((REMOVED_COUNT + $(find .coordination/ -type f -name "*.md" ! -name "README.md" 2>/dev/null | wc -l)))
find .coordination/ -type f -name "*.md" ! -name "README.md" -delete 2>/dev/null || true

# Remove implementation summaries
echo "Removing implementation summaries..."
find .coordination/ -type f -name "*IMPLEMENTATION*.md" -delete 2>/dev/null || true
find .coordination/ -type f -name "*SUMMARY*.md" -delete 2>/dev/null || true
find .coordination/ -type f -name "*COMPLETION*.md" -delete 2>/dev/null || true

# Reset state files
echo "Resetting state files..."
if [ -f ".coordination/active_work.json" ]; then
    echo '{"status": "idle", "task": null}' > .coordination/active_work.json
    echo "  - Reset active_work.json"
fi

if [ -f ".coordination/work_queue.json" ]; then
    echo '{"pending": [], "blocked": []}' > .coordination/work_queue.json
    echo "  - Reset work_queue.json"
fi

# Remove outdated task graph
if [ -f ".coordination/task-graph.json" ]; then
    rm -f .coordination/task-graph.json
    echo "  - Removed outdated task-graph.json"
    REMOVED_COUNT=$((REMOVED_COUNT + 1))
fi

# Remove completed.jsonl if it exists
if [ -f ".coordination/completed.jsonl" ]; then
    rm -f .coordination/completed.jsonl
    echo "  - Removed completed.jsonl"
    REMOVED_COUNT=$((REMOVED_COUNT + 1))
fi

echo ""
echo -e "${YELLOW}Phase 2: Cleaning .claude/agent-outputs/ directory${NC}"
echo "---------------------------------------------------"

# Remove all agent output files except .gitkeep
echo "Removing agent output files..."
find .claude/agent-outputs/ -type f ! -name ".gitkeep" -delete 2>/dev/null || true
AGENT_FILES=$(find .claude/agent-outputs/ -type f ! -name ".gitkeep" 2>/dev/null | wc -l)
REMOVED_COUNT=$((REMOVED_COUNT + AGENT_FILES))
echo "  - Removed all agent output files"

echo ""
echo -e "${YELLOW}Phase 3: Cleaning .coordination/checkpoints/ directory${NC}"
echo "--------------------------------------------------------"

# Remove checkpoint files except README.md
echo "Removing checkpoint files..."
find .coordination/checkpoints/ -type f ! -name "README.md" ! -name ".gitkeep" -delete 2>/dev/null || true
CHECKPOINT_FILES=$(find .coordination/checkpoints/ -type f ! -name "README.md" ! -name ".gitkeep" 2>/dev/null | wc -l)
REMOVED_COUNT=$((REMOVED_COUNT + CHECKPOINT_FILES))
echo "  - Removed checkpoint files"

echo ""
echo -e "${YELLOW}Phase 4: Verification${NC}"
echo "---------------------"

# Verify key files remain
echo "Verifying structure..."
ERRORS=0

if [ ! -f ".coordination/README.md" ]; then
    echo -e "${RED}  ✗ .coordination/README.md missing!${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}  ✓ .coordination/README.md present${NC}"
fi

if [ ! -f ".coordination/checkpoints/README.md" ]; then
    echo -e "${RED}  ✗ .coordination/checkpoints/README.md missing!${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}  ✓ .coordination/checkpoints/README.md present${NC}"
fi

if [ ! -f ".coordination/spec/incomplete-features.yaml" ]; then
    echo -e "${RED}  ✗ .coordination/spec/incomplete-features.yaml missing!${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}  ✓ .coordination/spec/incomplete-features.yaml present${NC}"
fi

echo ""
echo -e "${GREEN}=== Cleanup Complete ===${NC}"
echo ""
echo "Summary:"
echo "  - Removed development artifacts"
echo "  - Reset state files to empty/idle state"
echo "  - Preserved README and structure files"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}  ✓ All verification checks passed${NC}"
    exit 0
else
    echo -e "${RED}  ✗ $ERRORS verification check(s) failed${NC}"
    exit 1
fi
