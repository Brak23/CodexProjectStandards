# Documentation standards

Documentation serves four distinct purposes:

- Tutorials teach by guided experience.
- How-to guides complete a task.
- Reference provides precise facts and contracts.
- Explanation records concepts, tradeoffs, and architecture.

## Rules

- Version documentation with code.
- Link source-of-truth schemas rather than duplicating them.
- Test commands and examples where practical.
- Record owners and last validation dates for runbooks.
- Label planned, experimental, deprecated, and implemented behavior.
- Document failure and recovery, not only happy paths.
- Delete obsolete content instead of leaving contradictions.
- Use ADRs for consequential decisions and feature workspaces for temporary execution state.

Documentation claims must trace to source code, schema, test, executed command, ADR, issue, or PR.
