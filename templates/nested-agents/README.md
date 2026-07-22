# Nested AGENTS.md templates

Use these only for subsystems with materially different commands, boundaries, security constraints, or ownership.

Recommended generated-project layout:

```text
AGENTS.md
apps/
  web/AGENTS.md
  ios/AGENTS.md
services/
  api/AGENTS.md
infra/
  AGENTS.md
```

Do not create a nested instruction file for every directory. Copy the closest template into the subsystem root, remove irrelevant sections, and describe only differences from the root contract.

Each nested file should normally remain below 100 lines and include:

- Scope and applicable paths.
- Exact local commands.
- Local architecture and dependency boundaries.
- Local verification expectations.
- Ownership or integration constraints.

It must not repeat or weaken root security, approval, verification, protected-surface, or tool-permission rules.
