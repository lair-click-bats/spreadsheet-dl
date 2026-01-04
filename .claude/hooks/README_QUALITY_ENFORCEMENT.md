# Quality Enforcement Hooks - Complete Guide

## Overview

This project uses **strict quality enforcement** to ensure ALL code written by Claude meets quality standards immediately, preventing technical debt accumulation.

**Philosophy**: Block operations with ANY quality issues rather than accumulating technical debt.

---

## Hook Strategy

### Workflow for Every File Write/Edit

```
1. Auto-format (ruff format, prettier, shfmt, etc.)
   └─> Non-blocking, always attempts formatting

2. Auto-fix (ruff check --fix, etc.)
   └─> Non-blocking, fixes what can be auto-fixed

3. Validate (check for remaining issues)
   └─> Checks all remaining warnings/errors

4. BLOCK if ANY issues remain (exit code 2)
   └─> Shows errors to Claude, operation blocked until fixed
```

### Why Strict Blocking?

**Problem**: The project previously accumulated:

- 579 mypy errors
- 224 Unicode warnings
- 15 star import issues
- Broad exception handlers
- Inconsistent formatting

This required a massive bulk fix effort.

**Solution**: Block on **ALL** quality issues immediately:

- ✅ Zero technical debt accumulation
- ✅ Consistent code quality
- ✅ Claude learns correct patterns immediately
- ✅ No bulk fixes needed later

---

## File Type Coverage

### Python (`.py`)

**Tools**: ruff (format + lint), mypy (types)

**Enforced Standards**:

- ✅ Formatting (ruff format)
- ✅ Import sorting (ruff I)
- ✅ Code style (ruff E, W, etc.)
- ✅ Code smells (ruff F, B, etc.)
- ✅ Unused imports (ruff F401)
- ✅ Undefined names (ruff F821)
- ⚠️ Type hints (mypy - INFO mode, optional strict)

**Auto-fixed**:

- Import ordering
- Trailing whitespace
- Line length (when possible)
- Quote normalization
- Many code style issues

**Blocked**:

- Syntax errors
- Undefined variables
- Unused imports
- Any remaining warnings after auto-fix

### Shell Scripts (`.sh`)

**Tools**: shfmt (format), shellcheck (lint)

**Enforced Standards**:

- ✅ Consistent formatting (shfmt)
- ✅ Common pitfalls (shellcheck)
- ✅ Quoting issues
- ✅ Variable expansion
- ✅ Exit code handling

**Auto-fixed**:

- Indentation (2 spaces)
- Spacing consistency

**Blocked**:

- All shellcheck warnings
- Syntax errors
- Potential bugs

### YAML (`.yaml`, `.yml`)

**Tools**: prettier (format), yamllint (lint)

**Enforced Standards**:

- ✅ Consistent formatting
- ✅ Indentation (2 spaces)
- ✅ Key ordering (when configured)
- ✅ Line length
- ✅ Trailing spaces

**Auto-fixed**:

- Formatting (prettier)

**Blocked**:

- All yamllint warnings
- Syntax errors
- Indentation issues

### Markdown (`.md`)

**Tools**: prettier (format), markdownlint (lint)

**Enforced Standards**:

- ✅ Consistent formatting
- ✅ Heading hierarchy
- ✅ List formatting
- ✅ Link formatting
- ✅ Code block formatting

**Auto-fixed**:

- Formatting (prettier)

**Blocked**:

- All markdownlint warnings
- Broken links (if configured)
- Style violations

### JSON (`.json`)

**Tools**: prettier (format), Python json.loads (validate)

**Enforced Standards**:

- ✅ Syntax validation
- ✅ Consistent formatting
- ✅ Indentation (2 spaces)

**Auto-fixed**:

- Formatting (prettier)

**Blocked**:

- Syntax errors
- Invalid JSON

---

## Configuration

### Current Setup (`.claude/settings.json`)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/quality_enforce_strict.py\"",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Hook Execution Order

Hooks run **in parallel** by default, but we use a single hook that handles the full workflow internally:

1. **Auto-format** (always runs, non-blocking)
2. **Auto-fix** (always runs, non-blocking)
3. **Validate** (always runs, may block)

This ensures correct ordering while being efficient.

### Environment Variables

**Optional Configuration**:

```bash
# Enable strict mypy type checking (blocks on type errors)
export MYPY_STRICT=1

# Disable strict enforcement (fallback to warnings only)
export QUALITY_STRICT=0
```

---

## Hook Files

### `quality_enforce_strict.py`

**Primary hook** - Handles ALL file types with strict blocking.

**Features**:

- Multi-language support (Python, Shell, YAML, Markdown, JSON)
- Auto-format → Auto-fix → Validate workflow
- Blocks on ANY remaining issues
- Clear error messages with suggestions
- Timeout protection (60s max)

**Exit Codes**:

- `0` - Success (no issues)
- `2` - BLOCK (issues found, operation blocked)

### `python_quality_enforce.py`

**Python-specific** strict enforcement (alternative to strict multi-language).

**Features**:

- Categorizes errors (critical vs warnings)
- Can be configured for critical-only blocking
- More detailed Python-specific messaging

### `python_type_check.py`

**Mypy type checking** with INFO/STRICT modes.

**Features**:

- INFO mode: Show type errors but don't block
- STRICT mode: Block on type errors (set `MYPY_STRICT=1`)
- Skips test files in INFO mode
- 60s timeout for large files

### `auto_format.py`

**Legacy hook** - Auto-formats files (non-blocking).

**Note**: Superseded by `quality_enforce_strict.py` which does formatting + validation.

### `auto_validate.py`

**Legacy hook** - Validates files (non-blocking, informational only).

**Note**: Superseded by `quality_enforce_strict.py` which blocks on issues.

---

## Testing Hooks

### Manual Testing

Test a hook directly:

```bash
# Create test input
cat << 'EOF' | python3 .claude/hooks/quality_enforce_strict.py
{
  "tool_name": "Write",
  "tool_input": {"file_path": "test.py"},
  "tool_use_id": "test"
}
EOF

# Check exit code
echo $?
# 0 = success, 2 = blocked
```

### Testing with Bad Code

Create a file with intentional issues:

```bash
# Create bad Python file
cat > test_bad.py << 'EOF'
import os  # unused import
def foo():
    x = 1  # unused variable
    print(y)  # undefined variable
EOF

# Test hook
cat << 'EOF' | python3 .claude/hooks/quality_enforce_strict.py
{
  "tool_name": "Write",
  "tool_input": {"file_path": "test_bad.py"},
  "tool_use_id": "test"
}
EOF

# Should block (exit 2) and show errors
```

### Integration Testing

```bash
# Use Claude to write a file and observe hook behavior
# Hook should auto-format, auto-fix, then block if issues remain

# Check hook logs
tail -f .claude/hooks/errors.log
tail -f .claude/hooks/enforcement.log
```

---

## Troubleshooting

### Hook Not Running

**Check**:

1. Is the hook file executable? (`chmod +x .claude/hooks/*.py`)
2. Is the hook configured in `.claude/settings.json`?
3. Check `.claude/hooks/errors.log` for errors

### Hook Timeout

**Symptoms**: Hook takes >60s, times out

**Solutions**:

- Increase timeout in settings.json: `"timeout": 120`
- Check for slow network (prettier, markdownlint use npx)
- Exclude large files or generated code

### Too Strict - Can't Write Anything

**Temporary Solutions**:

```bash
# Disable strict enforcement temporarily
export QUALITY_STRICT=0

# Or disable hook temporarily (edit .claude/settings.json)
# Comment out the PostToolUse hook, then restart session
```

**Permanent Solutions**:

- Configure tool ignore rules (`.ruff.toml`, `.yamllint`, etc.)
- Exclude files in hook (edit EXCLUDED_DIRS)
- Use critical-only mode instead of strict

### False Positives

**Configure tool ignore rules**:

**Ruff** (`.ruff.toml` or `pyproject.toml`):

```toml
[tool.ruff]
ignore = ["E501"]  # Ignore line length

[tool.ruff.per-file-ignores]
"tests/*.py" = ["F401"]  # Allow unused imports in tests
```

**Yamllint** (`.yamllint`):

```yaml
extends: default
rules:
  line-length:
    max: 120
  comments:
    min-spaces-from-content: 1
```

**Shellcheck** (in script):

```bash
# shellcheck disable=SC2086
echo $var  # Intentionally unquoted
```

**Markdownlint** (`.markdownlint.json`):

```json
{
  "MD013": false,
  "MD033": false
}
```

---

## Migration from Non-Strict

If migrating from non-strict enforcement:

1. **Run full quality check first**:

```bash
uv run ruff check src/ tests/
uv run mypy src/ tests/
yamllint .
shellcheck scripts/**/*.sh
```

2. **Fix all existing issues** (bulk fix):

```bash
uv run ruff format src/ tests/
uv run ruff check --fix src/ tests/
```

3. **Enable strict hooks** (update `.claude/settings.json`)

4. **All new code now enforced** - No more technical debt!

---

## Best Practices

### Do's ✅

- ✅ Fix issues immediately when Claude writes bad code
- ✅ Configure tool ignores for intentional violations
- ✅ Review auto-fixed changes in git diff
- ✅ Keep hooks fast (<10s per file)
- ✅ Use strict mode in production branches
- ✅ Commit hook configuration to git

### Don'ts ❌

- ❌ Don't disable hooks to "get around" quality issues
- ❌ Don't accumulate technical debt for "later"
- ❌ Don't ignore hook error messages
- ❌ Don't commit hook bypass workarounds
- ❌ Don't use `|| true` to silence hook failures

---

## Performance

### Hook Execution Time

Typical execution time per file:

| File Type | Format | Lint  | Total |
| --------- | ------ | ----- | ----- |
| Python    | ~0.3s  | ~0.5s | ~0.8s |
| Shell     | ~0.1s  | ~0.2s | ~0.3s |
| YAML      | ~0.5s  | ~0.3s | ~0.8s |
| Markdown  | ~0.5s  | ~0.4s | ~0.9s |
| JSON      | ~0.5s  | ~0.1s | ~0.6s |

**Total per write**: < 1 second for most files

### Optimization Tips

- Use `uv` for Python (faster than pip/conda)
- Cache tool installations (npx caches automatically)
- Exclude large generated files
- Set appropriate timeouts (30-60s)

---

## Summary

**Before Strict Enforcement**:

- Accumulated 579 mypy errors
- Inconsistent formatting
- Manual bulk fixes needed
- Technical debt grew over time

**After Strict Enforcement**:

- ✅ Zero tolerance for quality issues
- ✅ All code formatted on write
- ✅ All issues fixed immediately
- ✅ No technical debt accumulation
- ✅ Consistent high-quality codebase

**Result**: Every file written meets quality standards from day one.
