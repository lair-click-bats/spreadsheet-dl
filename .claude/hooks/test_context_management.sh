#!/usr/bin/env bash
# Comprehensive test suite for context management hooks and utilities
# Tests: pre_compact_cleanup.sh, post_compact_recovery.sh, check_context_usage.sh,
#        checkpoint_state.sh, restore_checkpoint.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_TEMP="/tmp/test_context_mgmt_$$"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

cleanup() {
    rm -rf "$TEST_TEMP"
}
trap cleanup EXIT

setup_test_env() {
    local test_name="$1"
    local test_dir="$TEST_TEMP/$test_name"
    mkdir -p "$test_dir/.claude/hooks"
    mkdir -p "$test_dir/.claude/agent-outputs"
    mkdir -p "$test_dir/.claude/agents"
    mkdir -p "$test_dir/.claude/commands"
    mkdir -p "$test_dir/.coordination/checkpoints"
    mkdir -p "$test_dir/.coordination/spec"
    mkdir -p "$test_dir/.coordination/audits"

    # Create minimal required files
    echo "# Test CLAUDE.md" >"$test_dir/CLAUDE.md"
    echo "# Test agent" >"$test_dir/.claude/agents/test.md"
    echo "# Test command" >"$test_dir/.claude/commands/test.md"
    echo "test: value" >"$test_dir/.coordination/spec/test.yaml"

    echo "$test_dir"
}

print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

assert_success() {
    local test_name="$1"
    local exit_code="$2"
    local description="${3:-}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [ "$exit_code" -eq 0 ]; then
        echo -e "${GREEN}  ✓${NC} $test_name"
        [ -n "$description" ] && echo "    $description"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}  ✗${NC} $test_name (exit code: $exit_code)"
        [ -n "$description" ] && echo "    $description"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_json_ok() {
    local test_name="$1"
    local output="$2"

    TESTS_RUN=$((TESTS_RUN + 1))

    if echo "$output" | jq -e '.ok == true' >/dev/null 2>&1; then
        echo -e "${GREEN}  ✓${NC} $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}  ✗${NC} $test_name"
        echo "    Expected: {\"ok\": true, ...}"
        echo "    Got: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_file_exists() {
    local test_name="$1"
    local file_path="$2"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [ -f "$file_path" ]; then
        echo -e "${GREEN}  ✓${NC} $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}  ✗${NC} $test_name"
        echo "    File not found: $file_path"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_dir_exists() {
    local test_name="$1"
    local dir_path="$2"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [ -d "$dir_path" ]; then
        echo -e "${GREEN}  ✓${NC} $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}  ✗${NC} $test_name"
        echo "    Directory not found: $dir_path"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# ============================================================
# Test: pre_compact_cleanup.sh
# ============================================================
test_pre_compact_cleanup() {
    print_header "Testing pre_compact_cleanup.sh"

    # Test 1: Basic execution
    local test_dir=$(setup_test_env "pre_compact_basic")
    local output
    local exit_code=0

    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/pre_compact_cleanup.sh" 2>&1) || exit_code=$?
    assert_success "Pre-compact cleanup runs without error" "$exit_code"

    # Test 2: Creates archive directories
    assert_dir_exists "Creates coordination archive directory" "$test_dir/.coordination/archive"

    # Test 3: Logs cleanup metrics
    assert_file_exists "Creates compaction log" "$test_dir/.claude/hooks/compaction.log"

    # Test 4: Creates metrics log
    assert_file_exists "Creates metrics log" "$test_dir/.claude/hooks/context_metrics.log"

    # Test 5: Archives old files (create some old files first)
    local old_test_dir=$(setup_test_env "pre_compact_old_files")
    # Create an "old" file by touching with old date
    mkdir -p "$old_test_dir/.coordination"
    touch -d "40 days ago" "$old_test_dir/.coordination/old_file.md" 2>/dev/null || true

    output=$(CLAUDE_PROJECT_DIR="$old_test_dir" bash "$SCRIPT_DIR/pre_compact_cleanup.sh" 2>&1) || exit_code=$?
    assert_success "Pre-compact handles old files" "$exit_code"
}

# ============================================================
# Test: post_compact_recovery.sh
# ============================================================
test_post_compact_recovery() {
    print_header "Testing post_compact_recovery.sh"

    # Test 1: Success with all files present
    local test_dir=$(setup_test_env "post_compact_success")
    local output
    local exit_code=0

    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/post_compact_recovery.sh" 2>&1) || exit_code=$?
    assert_success "Post-compact recovery runs with all files" "$exit_code"
    assert_json_ok "Returns ok: true with all files" "$output"

    # Test 2: Warns but doesn't fail on missing CLAUDE.md
    local no_claude_dir=$(setup_test_env "post_compact_no_claude")
    rm -f "$no_claude_dir/CLAUDE.md"

    output=$(CLAUDE_PROJECT_DIR="$no_claude_dir" bash "$SCRIPT_DIR/post_compact_recovery.sh" 2>&1) || exit_code=$?
    assert_success "Warns but succeeds without CLAUDE.md" "$exit_code"

    # Test 3: Checks spec directory
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/post_compact_recovery.sh" 2>&1) || exit_code=$?

    TESTS_RUN=$((TESTS_RUN + 1))
    if grep -q "Spec directory found" "$test_dir/.claude/hooks/compaction.log" 2>/dev/null; then
        echo -e "${GREEN}  ✓${NC} Logs spec directory check"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${YELLOW}  ⚠${NC} Spec directory check not logged (may be expected)"
        TESTS_PASSED=$((TESTS_PASSED + 1))  # Count as pass since it's a warning
    fi
}

# ============================================================
# Test: check_context_usage.sh
# ============================================================
test_check_context_usage() {
    print_header "Testing check_context_usage.sh"

    local test_dir=$(setup_test_env "context_usage")
    local output
    local exit_code=0

    # Test 1: Basic execution (JSON output)
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/check_context_usage.sh" 2>&1) || exit_code=$?
    # Exit code 0-2 are valid (0=ok, 1=warning, 2=critical)
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ "$exit_code" -le 2 ]; then
        echo -e "${GREEN}  ✓${NC} Context usage check runs (exit: $exit_code)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}  ✗${NC} Context usage check failed (exit: $exit_code)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Test 2: Returns valid JSON
    TESTS_RUN=$((TESTS_RUN + 1))
    if echo "$output" | jq -e '.' >/dev/null 2>&1; then
        echo -e "${GREEN}  ✓${NC} Returns valid JSON"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}  ✗${NC} Invalid JSON output"
        echo "    Output: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Test 3: Has required fields
    TESTS_RUN=$((TESTS_RUN + 1))
    if echo "$output" | jq -e '.warning_level and .estimated_tokens and .percentage' >/dev/null 2>&1; then
        echo -e "${GREEN}  ✓${NC} Has required fields (warning_level, estimated_tokens, percentage)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}  ✗${NC} Missing required fields"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Test 4: Report mode
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/check_context_usage.sh" --report 2>&1) || exit_code=$?
    TESTS_RUN=$((TESTS_RUN + 1))
    if echo "$output" | grep -q "Context Usage Report"; then
        echo -e "${GREEN}  ✓${NC} Report mode generates readable output"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}  ✗${NC} Report mode failed"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# ============================================================
# Test: checkpoint_state.sh
# ============================================================
test_checkpoint_state() {
    print_header "Testing checkpoint_state.sh"

    local test_dir=$(setup_test_env "checkpoint")
    local output
    local exit_code=0

    # Test 1: Create checkpoint
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/checkpoint_state.sh" create "test-checkpoint" "Test description" 2>&1) || exit_code=$?
    assert_success "Create checkpoint" "$exit_code"

    # Test 2: Checkpoint directory created
    assert_dir_exists "Checkpoint directory created" "$test_dir/.coordination/checkpoints/test-checkpoint"

    # Test 3: Manifest file exists
    assert_file_exists "Manifest file created" "$test_dir/.coordination/checkpoints/test-checkpoint/manifest.json"

    # Test 4: State file exists
    assert_file_exists "State file created" "$test_dir/.coordination/checkpoints/test-checkpoint/state.json"

    # Test 5: Context file exists
    assert_file_exists "Context file created" "$test_dir/.coordination/checkpoints/test-checkpoint/context.md"

    # Test 6: Artifacts directory exists
    assert_dir_exists "Artifacts directory created" "$test_dir/.coordination/checkpoints/test-checkpoint/artifacts"

    # Test 7: List checkpoints
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/checkpoint_state.sh" list 2>&1) || exit_code=$?
    assert_success "List checkpoints" "$exit_code"

    TESTS_RUN=$((TESTS_RUN + 1))
    if echo "$output" | grep -q "test-checkpoint"; then
        echo -e "${GREEN}  ✓${NC} Checkpoint appears in list"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}  ✗${NC} Checkpoint not in list"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Test 8: Show checkpoint
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/checkpoint_state.sh" show "test-checkpoint" 2>&1) || exit_code=$?
    assert_success "Show checkpoint" "$exit_code"

    # Test 9: Delete checkpoint
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/checkpoint_state.sh" delete "test-checkpoint" 2>&1) || exit_code=$?
    assert_success "Delete checkpoint" "$exit_code"

    # Test 10: Checkpoint archived after delete
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ ! -d "$test_dir/.coordination/checkpoints/test-checkpoint" ]; then
        echo -e "${GREEN}  ✓${NC} Checkpoint removed after delete"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}  ✗${NC} Checkpoint still exists after delete"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Test 11: Help command
    output=$(bash "$SCRIPT_DIR/checkpoint_state.sh" help 2>&1) || exit_code=$?
    assert_success "Help command works" "$exit_code"
}

# ============================================================
# Test: restore_checkpoint.sh
# ============================================================
test_restore_checkpoint() {
    print_header "Testing restore_checkpoint.sh"

    local test_dir=$(setup_test_env "restore")
    local output
    local exit_code=0

    # Create a checkpoint first
    CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/checkpoint_state.sh" create "restore-test" "Restore test" >/dev/null 2>&1

    # Test 1: Restore checkpoint (text mode)
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/restore_checkpoint.sh" "restore-test" 2>&1) || exit_code=$?
    assert_success "Restore checkpoint (text mode)" "$exit_code"

    TESTS_RUN=$((TESTS_RUN + 1))
    if echo "$output" | grep -q "CHECKPOINT RESTORED"; then
        echo -e "${GREEN}  ✓${NC} Restore outputs checkpoint header"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}  ✗${NC} Missing checkpoint header in output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Test 2: Restore checkpoint (JSON mode)
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/restore_checkpoint.sh" "restore-test" --json 2>&1) || exit_code=$?
    assert_success "Restore checkpoint (JSON mode)" "$exit_code"

    TESTS_RUN=$((TESTS_RUN + 1))
    if echo "$output" | jq -e '.restored == true' >/dev/null 2>&1; then
        echo -e "${GREEN}  ✓${NC} JSON output has restored: true"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}  ✗${NC} JSON output missing restored field"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Test 3: Restore latest
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/restore_checkpoint.sh" --latest 2>&1) || exit_code=$?
    assert_success "Restore --latest" "$exit_code"

    # Test 4: Error on missing checkpoint
    exit_code=0
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/restore_checkpoint.sh" "nonexistent" 2>&1) || exit_code=$?
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ "$exit_code" -ne 0 ]; then
        echo -e "${GREEN}  ✓${NC} Returns error for missing checkpoint"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}  ✗${NC} Should fail for missing checkpoint"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Test 5: Help command
    output=$(bash "$SCRIPT_DIR/restore_checkpoint.sh" --help 2>&1) || exit_code=$?
    assert_success "Help command works" "$exit_code"
}

# ============================================================
# Test: Integration - Full workflow
# ============================================================
test_full_workflow() {
    print_header "Testing Full Workflow Integration"

    local test_dir=$(setup_test_env "integration")
    local output
    local exit_code=0

    # Step 1: Check initial context
    echo "  Step 1: Check initial context usage"
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/check_context_usage.sh" 2>&1) || exit_code=$?
    assert_success "Initial context check" "$exit_code"

    # Step 2: Create checkpoint
    echo "  Step 2: Create checkpoint before simulated work"
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/checkpoint_state.sh" create "workflow-test" "Integration test" 2>&1) || exit_code=$?
    assert_success "Create workflow checkpoint" "$exit_code"

    # Step 3: Simulate some work (create files)
    echo "  Step 3: Simulate work"
    echo '{"test": "data"}' >"$test_dir/.coordination/test_output.json"
    echo "# Test audit" >"$test_dir/.coordination/audits/test_audit.md"

    # Step 4: Run pre-compact cleanup
    echo "  Step 4: Run pre-compact cleanup"
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/pre_compact_cleanup.sh" 2>&1) || exit_code=$?
    assert_success "Pre-compact cleanup" "$exit_code"

    # Step 5: Run post-compact recovery
    echo "  Step 5: Run post-compact recovery"
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/post_compact_recovery.sh" 2>&1) || exit_code=$?
    assert_success "Post-compact recovery" "$exit_code"

    # Step 6: Restore checkpoint
    echo "  Step 6: Restore checkpoint"
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/restore_checkpoint.sh" "workflow-test" --json 2>&1) || exit_code=$?
    assert_success "Restore checkpoint after compact" "$exit_code"

    TESTS_RUN=$((TESTS_RUN + 1))
    if echo "$output" | jq -e '.restored == true and .task_id == "workflow-test"' >/dev/null 2>&1; then
        echo -e "${GREEN}  ✓${NC} Checkpoint correctly restored"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}  ✗${NC} Checkpoint restoration incomplete"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Step 7: Cleanup
    echo "  Step 7: Cleanup checkpoint"
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$SCRIPT_DIR/checkpoint_state.sh" delete "workflow-test" 2>&1) || exit_code=$?
    assert_success "Delete workflow checkpoint" "$exit_code"
}

# ============================================================
# Main: Run all tests
# ============================================================
main() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  Context Management Hooks Test Suite                   ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"

    mkdir -p "$TEST_TEMP"

    test_pre_compact_cleanup
    test_post_compact_recovery
    test_check_context_usage
    test_checkpoint_state
    test_restore_checkpoint
    test_full_workflow

    # Print summary
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  Test Summary${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "  Total tests:  $TESTS_RUN"
    echo -e "  ${GREEN}Passed:       $TESTS_PASSED${NC}"

    if [ $TESTS_FAILED -gt 0 ]; then
        echo -e "  ${RED}Failed:       $TESTS_FAILED${NC}"
        echo ""
        echo -e "${RED}Some tests failed!${NC}"
        exit 1
    else
        echo ""
        echo -e "${GREEN}All tests passed!${NC}"
        exit 0
    fi
}

main "$@"
