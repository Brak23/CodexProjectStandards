# Project-local agent skills

Skills in this directory are versioned with the repository and define repeatable professional workflows. They are procedures, not personas.

A skill should specify:

- when it applies and when it does not,
- required authoritative inputs,
- owned artifacts and authority boundaries,
- ordered workflow and stop conditions,
- deterministic validation where practical,
- evaluation scenarios for expected and prohibited behavior.

Repository-wide controls remain in `AGENTS.md`, `agent-policy.yml`, and routed standards. Nested `AGENTS.md` files define subsystem constraints. Skills must not weaken either layer.

## Included skills

- [`code-review`](code-review/SKILL.md): Stateful, scoped, evidence-driven independent review with Git-native review refs and deterministic aggregation and merge gating.
