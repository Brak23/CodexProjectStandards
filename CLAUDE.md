# Claude Code repository instructions

Read and follow `AGENTS.md` as the primary operating contract. Also read `agent-context.yml`, `agent-policy.yml`, the active feature `state.yml`, approved brief, approved execution plan, relevant architecture documents, and nested `AGENTS.md` files before editing.

Claude Code-specific expectations:

- Begin non-trivial work with read-only discovery and a written plan.
- Load only the applicable conditional context, then expand when scope or risk changes.
- Use `task` commands as the stable project interface.
- Maintain the feature workspace and `state.yml` under `docs/work/` during long-running work.
- Do not use broad shell commands when a narrower command is available.
- Do not modify tests, CI, security controls, evaluation files, or agent governance merely to pass.
- Work on a branch named `agent/<description>` and prepare a draft PR.
- Follow the session-recovery and multi-agent coordination protocols after handoff or interruption.
- Stop for human approval at specification, consequential technical decision, approval-required tool use, and release gates.

If this file conflicts with `AGENTS.md`, `agent-policy.yml`, or higher platform policy, the stricter applicable rule wins.
