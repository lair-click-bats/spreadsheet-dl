# Claude Code Configuration

This directory contains configuration for [Claude Code](https://claude.com/claude-code), Anthropic's official CLI tool for development assistance.

## What is Claude Code?

Claude Code is an AI-powered development assistant that integrates with your codebase to help with:

- Code implementation and refactoring
- Testing and debugging
- Documentation
- Architecture planning
- Git workflow management

## Directory Structure

```
.claude/
├── agents/              # Specialized agent definitions
│   ├── orchestrator.md
│   ├── git_commit_manager.md
│   ├── spec_implementer.md
│   └── spec_validator.md
├── commands/            # Custom slash commands
│   ├── ai.md
│   ├── git.md
│   ├── implement.md
│   ├── spec.md
│   └── swarm.md
├── hooks/               # Event hooks and automation
│   └── orchestration-metrics.json
├── agent-outputs/       # Completion reports from agents
├── settings.json        # Claude Code settings
├── project-metadata.yaml # Project configuration
└── README.md           # This file
```

## For Contributors

### If you use Claude Code:

These configurations will automatically enhance your development workflow with:

- **Custom commands** like `/ai`, `/git`, `/swarm` for common tasks
- **Specialized agents** for implementation, testing, and validation
- **Automated workflows** for quality checks and git operations

### If you don't use Claude Code:

You can safely ignore this directory. All configurations are optional and won't affect:

- Standard development workflows
- CI/CD pipelines
- Testing or linting
- Building or packaging

## Configuration Files

- **`.claude/settings.json`**: Claude Code behavior and tool permissions
- **`.claude/project-metadata.yaml`**: Project metadata and validation rules
- **`.claude/agents/*.md`**: Specialized agent definitions with capabilities
- **`.claude/commands/*.md`**: Slash command prompts and workflows

## Learn More

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Agent Development Guide](https://docs.anthropic.com/claude-code/agents)
- [Custom Commands](https://docs.anthropic.com/claude-code/commands)

---

**Note**: This directory is part of the project's development infrastructure. Changes to these files affect Claude Code behavior but not the production codebase.
