# AI agent compatibility

The project standards are the durable operating layer. Coding agents are replaceable interfaces to that layer.

## Required capabilities

An agent is compatible when it can:

- Read repository instructions and relevant files.
- Respect nested instructions and protected surfaces.
- Inspect the repository before modifying it.
- Work on a branch and produce reviewable changes.
- Run commands and report exact results.
- Stop when approval or missing information blocks correctness.
- Preserve human control of merge and release.

## Supported entry points

- `AGENTS.md` is authoritative for Codex and tools that support the convention.
- `CLAUDE.md` is the Claude Code entry point and delegates to `AGENTS.md`.
- Other agents should be configured to read `AGENTS.md`, `project.yml`, the approved work documents, and applicable nested instructions.

## Adapting another agent

For Cursor, Gemini CLI, Aider, or another future tool:

1. Add the smallest tool-specific entry file required by that agent.
2. Delegate to `AGENTS.md` rather than copying and drifting the rules.
3. Keep stable commands, work artifacts, approval gates, and verification unchanged.
4. Document tool-specific limitations without weakening repository controls.

## Compatibility rule

Do not redesign the engineering workflow around a vendor-specific feature unless the repository retains a portable fallback. Chats, proprietary memory, and tool-only plans are not substitutes for committed repository evidence.

## Confidence and escalation

All compatible agents should report evidence-based confidence and escalation conditions using `docs/engineering/confidence-and-escalation.md`.
