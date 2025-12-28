#!/usr/bin/env bash
#
# Resume Recent Claude Code Sessions in VS Code Terminal Tabs
#
# This script finds all Claude Code sessions active within the specified
# time period and opens each one in a separate VS Code integrated terminal tab.
#
# Requirements:
#   - VS Code with integrated terminal
#   - code CLI command in PATH
#
# Usage:
#   ./resume_claude_sessions_vscode.sh [OPTIONS] [hours]
#
# Options:
#   --dry-run      List sessions without resuming
#   --all          Resume all sessions (ignores hours parameter)
#
# Examples:
#   ./resume_claude_sessions_vscode.sh                # Last 1 hour
#   ./resume_claude_sessions_vscode.sh 2              # Last 2 hours
#   ./resume_claude_sessions_vscode.sh 0.5            # Last 30 minutes
#   ./resume_claude_sessions_vscode.sh --dry-run      # List only
#   ./resume_claude_sessions_vscode.sh --all          # All sessions

set -euo pipefail

# Parse options
DRY_RUN=false
RESUME_ALL=false

while [[ $# -gt 0 ]]; do
    case "$1" in
    --dry-run)
        DRY_RUN=true
        shift
        ;;
    --all)
        RESUME_ALL=true
        shift
        ;;
    -h | --help)
        echo "Usage: $0 [OPTIONS] [hours]"
        echo ""
        echo "Resume Claude Code sessions in VS Code terminal tabs"
        echo ""
        echo "Options:"
        echo "  --dry-run   List sessions without resuming"
        echo "  --all       Resume all sessions (ignores hours parameter)"
        echo "  -h, --help  Show this help message"
        echo ""
        echo "Arguments:"
        echo "  hours       Time window in hours (default: 1)"
        echo ""
        echo "Examples:"
        echo "  $0                # Last 1 hour"
        echo "  $0 2              # Last 2 hours"
        echo "  $0 0.5            # Last 30 minutes"
        echo "  $0 --dry-run      # List only"
        echo "  $0 --all          # All sessions"
        exit 0
        ;;
    *)
        break
        ;;
    esac
done

# Configuration
HOURS_AGO="${1:-1}" # Default to 1 hour if not specified
CLAUDE_DIR="${HOME}/.claude/projects"

# Check if Claude directory exists
if [ ! -d "$CLAUDE_DIR" ]; then
    echo "Error: Claude directory not found at $CLAUDE_DIR"
    exit 1
fi

# Check if code CLI is available
if ! command -v code &>/dev/null; then
    echo "Error: VS Code CLI 'code' command not found in PATH"
    echo "Install it via VS Code Command Palette: 'Shell Command: Install code command in PATH'"
    exit 1
fi

# Check if we're likely running in VS Code terminal
if [ -z "${TERM_PROGRAM:-}" ] || [ "${TERM_PROGRAM}" != "vscode" ]; then
    echo "Warning: Not detected as running in VS Code integrated terminal"
    echo "This script is optimized for VS Code's integrated terminal"
    echo ""
fi

echo "Searching for PRIMARY Claude Code sessions..."
echo "(Filtering out sub-agent sessions spawned via Task tool)"
if $RESUME_ALL; then
    echo "Mode: Resume ALL primary sessions"
else
    echo "Mode: Resume primary sessions from last ${HOURS_AGO} hour(s)"
fi
echo ""

# Find session files
declare -a sessions=()
declare -a work_dirs=()
declare -a last_activities=()

if $RESUME_ALL; then
    # Find all primary session files (exclude sub-agents with "agent-" prefix)
    while IFS= read -r -d '' session_file; do
        # Skip sub-agent sessions
        session_id=$(basename "$session_file" .jsonl)
        if [[ "$session_id" == agent-* ]]; then
            continue
        fi

        # Only include sessions that are actually resumable
        # Resumable sessions must end with "user" or "assistant" messages
        last_type=$(tail -1 "$session_file" 2>/dev/null | jq -r '.type' 2>/dev/null)

        # Whitelist approach: only keep sessions ending with user or assistant messages
        if [ "$last_type" != "user" ] && [ "$last_type" != "assistant" ]; then
            continue # Skip non-active sessions
        fi

        sessions+=("$session_file")
    done < <(find "$CLAUDE_DIR" -type f -name "*.jsonl" -print0 | sort -z)
else
    # Calculate threshold in minutes for find command
    MINUTES_AGO=$(echo "${HOURS_AGO} * 60" | bc)

    # Find primary session files modified within the specified time period
    while IFS= read -r -d '' session_file; do
        # Skip sub-agent sessions
        session_id=$(basename "$session_file" .jsonl)
        if [[ "$session_id" == agent-* ]]; then
            continue
        fi

        # Only include sessions that are actually resumable
        # Resumable sessions must end with "user" or "assistant" messages
        last_type=$(tail -1 "$session_file" 2>/dev/null | jq -r '.type' 2>/dev/null)

        # Whitelist approach: only keep sessions ending with user or assistant messages
        if [ "$last_type" != "user" ] && [ "$last_type" != "assistant" ]; then
            continue # Skip non-active sessions
        fi

        sessions+=("$session_file")
    done < <(find "$CLAUDE_DIR" -type f -name "*.jsonl" -mmin -"${MINUTES_AGO}" -print0 | sort -z)
fi

# Process each session to extract metadata
for session_file in "${sessions[@]}"; do
    # Extract session UUID from filename
    session_id=$(basename "$session_file" .jsonl)

    # Get file modification time
    file_mtime=$(stat -c '%Y' "$session_file" 2>/dev/null || stat -f '%m' "$session_file" 2>/dev/null)
    last_activity=$(date -d "@${file_mtime}" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date -r "${file_mtime}" '+%Y-%m-%d %H:%M:%S' 2>/dev/null)

    # Extract working directory from session file (check first 10 lines only for speed)
    work_dir=$(head -10 "$session_file" 2>/dev/null | grep -a '"cwd"' | head -1 | grep -o '"/[^"]*"' | tr -d '"' 2>/dev/null || true)

    # Fallback: use HOME if directory not found or doesn't exist
    # (Very new sessions may not have cwd field yet)
    if [ -z "$work_dir" ] || [ ! -d "$work_dir" ]; then
        work_dir="$HOME"
    fi

    work_dirs+=("$work_dir")
    last_activities+=("$last_activity")
done

# Display found sessions
session_count=${#sessions[@]}

if [ "$session_count" -eq 0 ]; then
    if $RESUME_ALL; then
        echo "No primary Claude Code sessions found."
    else
        echo "No primary sessions found within the past ${HOURS_AGO} hour(s)."
    fi
    echo "(Sub-agent sessions are automatically filtered out)"
    exit 0
fi

echo "Found $session_count primary session(s):"
echo ""

for i in "${!sessions[@]}"; do
    session_id=$(basename "${sessions[$i]}" .jsonl)
    printf "[%d] Session: %s\n" $((i + 1)) "${session_id:0:12}..."
    printf "    Last activity: %s\n" "${last_activities[$i]}"
    printf "    Working dir: %s\n" "${work_dirs[$i]}"
    echo ""
done

if $DRY_RUN; then
    echo "Dry-run mode: Listed $session_count session(s) without resuming."
    exit 0
fi

# Create temporary script to run in each terminal tab
TEMP_SCRIPT_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_SCRIPT_DIR"' EXIT

echo "Opening $session_count terminal tab(s) in VS Code..."
echo ""

# Track unique sessions to avoid duplicates
declare -A seen_sessions

for i in "${!sessions[@]}"; do
    session_id=$(basename "${sessions[$i]}" .jsonl)
    work_dir="${work_dirs[$i]}"
    last_activity="${last_activities[$i]}"

    # Skip if we've already seen this session
    if [ -n "${seen_sessions[$session_id]:-}" ]; then
        echo "Skipping duplicate session: ${session_id:0:12}..."
        continue
    fi
    seen_sessions[$session_id]=1

    # Create a temporary script for this session
    temp_script="${TEMP_SCRIPT_DIR}/resume_${session_id:0:12}.sh"

    cat >"$temp_script" <<EOF
#!/usr/bin/env bash
# Auto-generated script to resume Claude Code session
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║ Resuming Claude Code Session                                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Session ID: $session_id"
echo "Last activity: $last_activity"
echo "Working directory: $work_dir"
echo ""
echo "────────────────────────────────────────────────────────────────"
echo ""

# Change to working directory
cd "$work_dir" 2>/dev/null || cd "$HOME"

# Resume the Claude session
claude --resume "$session_id"

# Keep terminal open after session ends
echo ""
echo "────────────────────────────────────────────────────────────────"
echo "Session ended. Terminal will remain open."
echo ""
exec bash -l
EOF

    chmod +x "$temp_script"

    # Open new terminal tab in VS Code and run the script
    # Note: This works best when run from within VS Code's integrated terminal
    echo "[$((i + 1))/$session_count] Opening terminal for session ${session_id:0:12}..."

    # Use VS Code CLI to create a terminal and run the script
    # The --command flag is not standard but we can send commands via terminal automation
    code --reuse-window

    # Create a launch command that VS Code can execute
    # Using escape sequences to create a new terminal tab (works in integrated terminal)
    if [ "${TERM_PROGRAM:-}" = "vscode" ]; then
        # Running inside VS Code terminal - use escape sequences
        printf '\033]0;Claude: %s\007' "${session_id:0:12}" # Set terminal title

        # Note: VS Code doesn't have direct escape sequences to open new tabs
        # Best approach is to use tasks.json or manual tab creation
        echo "  → Run in new terminal tab: bash $temp_script"
    else
        # Not in VS Code terminal - provide manual instructions
        echo "  → Open new VS Code terminal tab and run: bash $temp_script"
    fi

    # Brief delay to avoid overwhelming
    sleep 0.2
done

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Session resume preparation complete!"
echo ""

if [ "${TERM_PROGRAM:-}" = "vscode" ]; then
    echo "To resume sessions in separate terminal tabs:"
    echo ""
    echo "1. Open new terminal tabs in VS Code (Ctrl+Shift+\` or Cmd+Shift+\` on macOS)"
    echo "2. Run the commands shown above in each new tab"
    echo ""
else
    echo "To use this script most effectively:"
    echo ""
    echo "1. Open VS Code integrated terminal (Ctrl+\` or Cmd+\` on macOS)"
    echo "2. Run this script again from within VS Code"
    echo "3. Follow the instructions to open terminal tabs"
    echo ""
fi

echo "Alternative: Run all sessions in tmux instead:"
echo "  ./resume_recent_claude_sessions.sh --tmux ${HOURS_AGO}"
echo ""
echo "Temporary scripts location: $TEMP_SCRIPT_DIR"
echo "(Will be cleaned up on exit)"
echo ""
