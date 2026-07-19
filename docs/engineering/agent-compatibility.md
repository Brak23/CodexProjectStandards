# AI agent compatibility

The project standards are the durable operating layer. Coding agents are replaceable interfaces to that layer.

## Required capabilities

An agent is compatible when it can:

- Read repository instructions and relevant files.
- Respect nested instructions and protected surfaces.
- Use `agent-context.yml` to load applicable context.
- Apply `agent-policy.yml` before tool use.
- Read and maintain feature `state.yml` without self-approving gates.
- Inspect the repository before modifying it.
- Work on a branch and produce reviewable changes.
- Run commands and report exact results.
- Stop when approval, permission, ownership, or missing information blocks correctness.
- Preserve human control of merge and release.

## Included entry points

- `AGENTS.md`: Authoritative contract for Codex and tools supporting the convention.
- `CLAUDE.md`: Claude Code adapter delegating to the portable controls.
- `GEMINI.md`: Gemini CLI context file importing the root contract, context manifest, and tool policy.
- `.cursor/rules/project-standards.mdc`: Always-applied Cursor project rule referencing the portable controls.
- `.aider.conf.yml`: Loads the portable controls as read-only Aider context and preserves confirmation prompts.

Tool-specific adapters are deliberately thin. They must delegate to shared repository files rather than copy rules that can drift.

## Adapting another agent

1. Add the smallest tool-specific entry file required by that runtime.
2. Delegate to `AGENTS.md`, `agent-context.yml`, and `agent-policy.yml`.
3. Load the active feature state and approved work artifacts for non-trivial work.
4. Preserve stable commands, approval gates, review levels, and verification.
5. Document tool-specific limitations without weakening repository controls.
6. Add or update behavior-evaluation scenarios when the runtime introduces a new risk or capability.

## Compatibility rule

Do not redesign the engineering workflow around a vendor-specific feature unless the repository retains a portable fallback. Chats, proprietary memory, tool-only plans, and runtime-specific todo lists are not substitutes for committed repository state and evidence.

## Runtime verification

Before relying on an agent for unattended or high-risk work:

- Confirm its adapter is loaded.
- Confirm it can enforce or visibly honor tool permissions.
- Run the scenarios in `evals/agent-behavior/scenarios.json` through a model-specific harness.
- Record model, version, tool configuration, sandbox, date, results, and known limitations.

`task agent-evals` validates the scenario contracts only. It does not invoke or certify a model.

## Confidence and escalation

All compatible agents should report evidence-based confidence and escalation conditions using `docs/engineering/confidence-and-escalation.md`.
