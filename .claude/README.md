# Claude Code Configuration

This directory contains configuration for [Claude Code](https://docs.anthropic.com/claude-code), Anthropic's AI-powered CLI development assistant.

## Directory Structure

```
.claude/
├── agents/              # Specialized agent definitions
│   ├── orchestrator.md      # Task routing and coordination
│   ├── git_commit_manager.md # Git workflow automation
│   ├── spec_implementer.md  # Implementation from specs
│   └── spec_validator.md    # Validation and testing
├── commands/            # Custom slash commands
│   ├── ai.md                # /ai - Universal task routing
│   ├── git.md               # /git - Smart commits
│   ├── implement.md         # /implement - Spec implementation
│   ├── spec.md              # /spec - Spec workflow
│   └── swarm.md             # /swarm - Parallel agents
├── hooks/               # Lifecycle automation
│   └── README.md            # Hook documentation
├── templates/           # Schema templates
│   └── spec/                # Specification schemas
├── settings.json        # Claude Code settings
├── orchestration-config.yaml
├── coding-standards.yaml
├── project-metadata.yaml
├── paths.yaml
└── README.md            # This file
```

## Quick Start

If you use Claude Code, these configurations are automatically loaded:

```bash
# Route any task to the right agent
/ai implement the authentication feature

# Smart conventional commits
/git

# Parallel analysis
/swarm comprehensive security review
```

## For Non-Claude Code Users

You can safely ignore this directory. All configurations are optional and won't affect:

- Standard development workflows
- CI/CD pipelines
- Testing or linting
- Building or packaging

## Key Features

### Agents

Specialized AI agents for different tasks:

- **orchestrator** - Routes tasks, coordinates multi-agent workflows
- **git_commit_manager** - Conventional commits, atomic history
- **spec_implementer** - Implements from specifications
- **spec_validator** - Validates against acceptance criteria

### Commands

Custom slash commands for common workflows:

- `/ai` - Universal task routing
- `/git` - Smart commit automation
- `/implement` - Spec-driven implementation
- `/spec` - Specification management
- `/swarm` - Parallel agent coordination

### Hooks

Automated quality gates and lifecycle management:

- Security validation (blocks sensitive file writes)
- Quality enforcement (auto-linting, type checks)
- Context management (cleanup, checkpointing)

## Configuration Files

| File                        | Purpose                              |
| --------------------------- | ------------------------------------ |
| `settings.json`             | Claude Code behavior and permissions |
| `orchestration-config.yaml` | Agent swarm configuration            |
| `coding-standards.yaml`     | Code quality standards               |
| `project-metadata.yaml`     | Project metadata                     |
| `paths.yaml`                | Centralized path definitions         |

## Learn More

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Custom Commands](https://docs.anthropic.com/claude-code/commands)
- [Hooks Documentation](./hooks/README.md)
