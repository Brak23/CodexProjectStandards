# Conditional agent context loading

Agents should load enough context to act correctly without flooding the model with every repository document.

## Source of truth

`agent-context.yml` defines:

- Files required for every task.
- Additional context triggered by task characteristics.
- Rules for nested instructions and uncertain applicability.

The manifest is a routing aid. It does not override `AGENTS.md`, approved work artifacts, or a more specific nested `AGENTS.md`.

## Procedure

1. Read the `always` set.
2. Classify the task and select every applicable `when` group.
3. Read nested `AGENTS.md` files for paths considered for modification.
4. Read the active feature `state.yml`, brief, plan, and decisions for non-trivial work.
5. Prefer relevant sections and summaries before loading entire documentation trees.
6. Load more context when the task crosses boundaries or applicability is uncertain.
7. Record inaccessible or intentionally omitted material when it limits confidence.

## Anti-patterns

- Reading every document by default.
- Reading only the user prompt and skipping repository instructions.
- Treating a repository map or generated summary as authoritative over source files.
- Omitting a security, data, design, or operations standard because the change initially appeared small.
- Continuing when context conflicts cannot be resolved.

## Context refresh triggers

Reload applicable context when:

- The task scope changes.
- A new module or public contract enters the change surface.
- Risk classification increases.
- A session is compacted or restarted.
- Another agent or human changes the branch, brief, plan, or state file.
- The base branch advances materially.
