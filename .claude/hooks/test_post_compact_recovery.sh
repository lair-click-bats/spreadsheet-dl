#!/usr/bin/env bash
# Test suite for post_compact_recovery.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RECOVERY_SCRIPT="$SCRIPT_DIR/post_compact_recovery.sh"
TEST_TEMP="/tmp/test_recovery_$$"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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
    echo "$test_dir"
}

assert_success() {
    local test_name="$1"
    local output="$2"

    TESTS_RUN=$((TESTS_RUN + 1))

    if echo "$output" | jq -e '.ok == true' >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $test_name"
        echo "  Expected: {\"ok\": true, ...}"
        echo "  Got: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_failure() {
    local test_name="$1"
    local output="$2"
    local expected_error="$3"

    TESTS_RUN=$((TESTS_RUN + 1))

    if echo "$output" | jq -e '.ok == false' >/dev/null 2>&1 &&
        echo "$output" | jq -e ".error == \"$expected_error\"" >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $test_name"
        echo "  Expected: {\"ok\": false, \"error\": \"$expected_error\", ...}"
        echo "  Got: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

test_recovery_succeeds_with_all_files() {
    local test_dir=$(setup_test_env "test_all_files")

    # Create all critical files
    echo "# Test CLAUDE.md" >"$test_dir/CLAUDE.md"
    mkdir -p "$test_dir/.claude/agents"
    mkdir -p "$test_dir/.claude/commands"
    echo "# Test agent" >"$test_dir/.claude/agents/test.md"
    echo "# Test command" >"$test_dir/.claude/commands/test.md"

    # Run recovery script
    local output
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$RECOVERY_SCRIPT" 2>&1)

    assert_success "test_recovery_succeeds_with_all_files" "$output"
}

test_recovery_detects_missing_claude_md() {
    local test_dir=$(setup_test_env "test_missing_claude_md")

    # Create only directories, no CLAUDE.md
    mkdir -p "$test_dir/.claude/agents"
    mkdir -p "$test_dir/.claude/commands"
    echo "# Test agent" >"$test_dir/.claude/agents/test.md"

    # Run recovery script
    local output
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$RECOVERY_SCRIPT" 2>&1 || true)

    assert_failure "test_recovery_detects_missing_claude_md" "$output" "critical_files_missing"
}

test_recovery_detects_empty_agents_dir() {
    local test_dir=$(setup_test_env "test_empty_agents")

    # Create CLAUDE.md and directories, but leave agents empty
    echo "# Test CLAUDE.md" >"$test_dir/CLAUDE.md"
    mkdir -p "$test_dir/.claude/agents"
    mkdir -p "$test_dir/.claude/commands"
    echo "# Test command" >"$test_dir/.claude/commands/test.md"

    # Run recovery script
    local output
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$RECOVERY_SCRIPT" 2>&1 || true)

    assert_failure "test_recovery_detects_empty_agents_dir" "$output" "critical_files_missing"
}

test_recovery_detects_missing_agents_dir() {
    local test_dir=$(setup_test_env "test_missing_agents_dir")

    # Create CLAUDE.md and commands, but no agents directory
    echo "# Test CLAUDE.md" >"$test_dir/CLAUDE.md"
    mkdir -p "$test_dir/.claude/commands"
    echo "# Test command" >"$test_dir/.claude/commands/test.md"

    # Run recovery script
    local output
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$RECOVERY_SCRIPT" 2>&1 || true)

    assert_failure "test_recovery_detects_missing_agents_dir" "$output" "critical_files_missing"
}

test_recovery_detects_missing_commands_dir() {
    local test_dir=$(setup_test_env "test_missing_commands_dir")

    # Create CLAUDE.md and agents, but no commands directory
    echo "# Test CLAUDE.md" >"$test_dir/CLAUDE.md"
    mkdir -p "$test_dir/.claude/agents"
    echo "# Test agent" >"$test_dir/.claude/agents/test.md"

    # Run recovery script
    local output
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$RECOVERY_SCRIPT" 2>&1 || true)

    assert_failure "test_recovery_detects_missing_commands_dir" "$output" "critical_files_missing"
}

test_recovery_counts_agents_and_commands() {
    local test_dir=$(setup_test_env "test_counts")

    # Create all critical files with multiple agents and commands
    echo "# Test CLAUDE.md" >"$test_dir/CLAUDE.md"
    mkdir -p "$test_dir/.claude/agents"
    mkdir -p "$test_dir/.claude/commands"

    # Create 3 agents
    echo "# Agent 1" >"$test_dir/.claude/agents/agent1.md"
    echo "# Agent 2" >"$test_dir/.claude/agents/agent2.md"
    echo "# Agent 3" >"$test_dir/.claude/agents/agent3.md"

    # Create 2 commands
    echo "# Command 1" >"$test_dir/.claude/commands/cmd1.md"
    echo "# Command 2" >"$test_dir/.claude/commands/cmd2.md"

    # Run recovery script
    local output
    output=$(CLAUDE_PROJECT_DIR="$test_dir" bash "$RECOVERY_SCRIPT" 2>&1)

    TESTS_RUN=$((TESTS_RUN + 1))
    if echo "$output" | jq -e '.ok == true and .agents == 3 and .commands == 2' >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} test_recovery_counts_agents_and_commands"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} test_recovery_counts_agents_and_commands"
        echo "  Expected: {\"ok\": true, \"agents\": 3, \"commands\": 2}"
        echo "  Got: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Run all tests
echo "Running post_compact_recovery.sh tests..."
echo ""

test_recovery_succeeds_with_all_files
test_recovery_detects_missing_claude_md
test_recovery_detects_empty_agents_dir
test_recovery_detects_missing_agents_dir
test_recovery_detects_missing_commands_dir
test_recovery_counts_agents_and_commands

# Print summary
echo ""
echo "========================================"
echo "Test Summary:"
echo "  Total:  $TESTS_RUN"
echo -e "  ${GREEN}Passed: $TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "  ${RED}Failed: $TESTS_FAILED${NC}"
    exit 1
else
    echo -e "  ${GREEN}All tests passed!${NC}"
    exit 0
fi
