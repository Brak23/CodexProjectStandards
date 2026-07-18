# Claude Code repository instructions

Read and follow `AGENTS.md` as the primary operating contract. Also read the approved feature brief, execution plan, relevant architecture documents, and nested `AGENTS.md` files before editing.

Claude Code-specific expectations:

- Begin non-trivial work with read-only discovery and a written plan.
- Use `task` commands as the stable project interface.
- Maintain the feature workspace under `docs/work/` during long-running work.
- Do not use broad shell commands when a narrower command is available.
- Do not modify tests, CI, security controls, or evaluation files merely to pass.
- Work on a branch named `agent/<description>` and prepare a draft PR.
- Stop for human approval at specification, consequential technical decision, and release gates.

If this file conflicts with `AGENTS.md`, `AGENTS.md` wins.
