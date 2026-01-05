# Claude Code Lifecycle Hooks

Automated actions at specific points in Claude's workflow.

## Hook Types

| Type             | Purpose                   | Blocking |
| ---------------- | ------------------------- | -------- |
| **PreToolUse**   | Validate before execution | Yes      |
| **PostToolUse**  | Process after execution   | No       |
| **PreCompact**   | Cleanup before compaction | No       |
| **SessionStart** | Initialize/recover        | No       |
| **SessionEnd**   | Cleanup on exit           | No       |
| **Stop**         | Handle shutdown           | No       |
| **SubagentStop** | Handle agent completion   | No       |

## Active Hooks

### Security & Validation

| Hook                     | Trigger    | Purpose                                            |
| ------------------------ | ---------- | -------------------------------------------------- |
| `validate_path.py`       | Write/Edit | Block writes to sensitive files (.env, .key, etc.) |
| `enforce_agent_limit.py` | Task       | Limit parallel agents to 2                         |

### Quality Enforcement

| Hook                        | Trigger    | Purpose                                    |
| --------------------------- | ---------- | ------------------------------------------ |
| `quality_enforce_strict.py` | Write/Edit | Run linters, type checks on modified files |

### Context Management

| Hook                       | Trigger      | Purpose                             |
| -------------------------- | ------------ | ----------------------------------- |
| `pre_compact_cleanup.sh`   | PreCompact   | Archive old files before compaction |
| `post_compact_recovery.sh` | SessionStart | Verify state after compaction       |
| `cleanup_stale_agents.py`  | SessionStart | Mark stale agents as failed         |
| `session_cleanup.sh`       | SessionEnd   | Clean temporary files               |
| `check_subagent_stop.py`   | SubagentStop | Auto-summarize large outputs        |

## Configuration

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate_path.py\"",
            "timeout": 5
          }
        ],
        "matcher": "Write|Edit"
      }
    ]
  }
}
```

## Environment Variables

- `CLAUDE_PROJECT_DIR` - Project root directory
- `CLAUDE_BYPASS_HOOKS` - Set to `1` to bypass all hooks

## Testing Hooks

```bash
# Test validate_path.py
CLAUDE_PROJECT_DIR=$(pwd) python3 .claude/hooks/validate_path.py

# Test cleanup
CLAUDE_PROJECT_DIR=$(pwd) .claude/hooks/pre_compact_cleanup.sh
```

## Log Files

- `errors.log` - Hook errors (created at runtime)
- `context_metrics.log` - Context usage tracking

## Essential Files

| File                        | Purpose       | Required    |
| --------------------------- | ------------- | ----------- |
| `validate_path.py`          | Security      | Yes         |
| `quality_enforce_strict.py` | Quality gates | Yes         |
| `enforce_agent_limit.py`    | Agent limits  | Recommended |
| `pre_compact_cleanup.sh`    | Cleanup       | Recommended |
| `post_compact_recovery.sh`  | Recovery      | Recommended |
| `cleanup_stale_agents.py`   | Maintenance   | Optional    |
| `session_cleanup.sh`        | Cleanup       | Optional    |
| `check_subagent_stop.py`    | Summarization | Optional    |
| `check_stop.py`             | Shutdown      | Optional    |

## Utility Scripts

| Script                   | Purpose                        |
| ------------------------ | ------------------------------ |
| `checkpoint_state.sh`    | Create/manage task checkpoints |
| `restore_checkpoint.sh`  | Restore checkpoint state       |
| `check_context_usage.sh` | Monitor context usage          |
