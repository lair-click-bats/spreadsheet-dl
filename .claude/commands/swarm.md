---
name: swarm
description: Execute complex tasks with parallel agent coordination
arguments: <task>
---

# Parallel Agent Swarm

Execute tasks requiring multiple independent agents working simultaneously.

## When to Use

| Command  | Pattern  | Use When                                        |
| -------- | -------- | ----------------------------------------------- |
| `/ai`    | Serial   | Tasks with dependencies, step-by-step workflows |
| `/swarm` | Parallel | Independent subtasks, multiple perspectives     |

## Parallel Detection Keywords

- **comprehensive** / **full** / **complete** - Needs broad coverage
- **multiple** / **various** / **diverse** - Different perspectives
- **all aspects** / **from different angles** - Multi-faceted analysis

## Process

1. Decompose task into independent subtasks
2. Identify agents via dynamic discovery
3. Spawn agents in parallel
4. Collect completion reports
5. Synthesize results into unified response

## Examples

```bash
# Comprehensive research
/swarm comprehensive research on Docker networking from academic, industry, and community sources

# Multi-perspective analysis
/swarm security review from multiple perspectives: threat modeling, code audit, compliance

# Full documentation suite
/swarm complete documentation: API reference, tutorial, and architecture diagram
```

## Synthesis Process

After all agents complete:

1. Read all completion reports
2. Identify overlapping findings
3. Note conflicting information
4. Synthesize into unified document
5. Cross-reference related sections

## Anti-patterns

- Using /swarm for tasks with dependencies (use /ai for serial)
- Spawning too many agents (3-5 is optimal)
- Not synthesizing results
- Parallel agents that need each other's output

## See Also

- `.claude/agents/orchestrator.md` - Handles parallel dispatch
- `/ai` - For serial workflows
