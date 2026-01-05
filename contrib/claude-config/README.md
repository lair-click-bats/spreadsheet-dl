# Claude Code Configuration Templates

This directory contains the full Claude Code configuration used for SpreadsheetDL development.

## What's Included

The `.claude/` directory in the main repo contains a working configuration. This contrib directory provides documentation and setup utilities for customization.

## Quick Setup

The main `.claude/` directory is ready to use. If you want to reset or customize:

```bash
# View current configuration
ls -la .claude/

# Run the setup script to reset to defaults
./scripts/setup-claude-config.sh

# Reset with full hook infrastructure
./scripts/setup-claude-config.sh --full
```

## Configuration Files

### Core Files (Always Active)

| File            | Purpose                            |
| --------------- | ---------------------------------- |
| `settings.json` | Permissions, hooks, model settings |
| `agents/*.md`   | Agent definitions                  |
| `commands/*.md` | Slash command definitions          |

### Optional Files

| File                        | Purpose                      |
| --------------------------- | ---------------------------- |
| `orchestration-config.yaml` | Agent swarm coordination     |
| `coding-standards.yaml`     | Code quality standards       |
| `project-metadata.yaml`     | Project metadata             |
| `paths.yaml`                | Centralized path definitions |
| `hooks/*.py, *.sh`          | Lifecycle automation         |

## Customization

### Modifying Agents

Edit files in `.claude/agents/`:

```markdown
---
name: my_agent
description: 'What the agent does'
tools: Read, Write, Edit, Bash
model: sonnet
routing_keywords:
  - keyword1
  - keyword2
---

# Agent Name

Instructions for the agent...
```

### Modifying Commands

Edit files in `.claude/commands/`:

```markdown
---
name: mycommand
description: What the command does
arguments: <required> [optional]
---

# Command Name

Instructions that run when `/mycommand` is invoked...
```

### Modifying Hooks

Hooks are configured in `settings.json` and implemented in `.claude/hooks/`.

See `.claude/hooks/README.md` for documentation.

## Disabling Features

### Disable All Hooks

Set environment variable:

```bash
export CLAUDE_BYPASS_HOOKS=1
```

### Disable Specific Hooks

Edit `.claude/settings.json` and remove the hook from the appropriate section.

## Best Practices

1. **Keep agents focused** - One agent per domain
2. **Use frontmatter keywords** - Enables dynamic routing
3. **Write completion reports** - Enables agent handoffs
4. **Test hooks locally** - Before committing changes

## Troubleshooting

### Hooks not running

- Check file permissions: `chmod +x .claude/hooks/*.sh`
- Check Python availability: `python3 --version`
- Check logs: `cat .claude/hooks/errors.log`

### Agent not found

- Verify file exists in `.claude/agents/`
- Check frontmatter syntax (YAML between `---` markers)
- Verify `routing_keywords` match your intent

### Command not working

- Verify file exists in `.claude/commands/`
- Check frontmatter syntax
- Try `/help` to see available commands
