# Approved scope and plan amendments

Authenticated human direction may change project intent or implementation scope, but it does not silently bypass an approved brief, plan, risk classification, or release gate.

## Amendment procedure

When a human requests a material change after approval:

1. Stop implementation at a coherent point.
2. Record the requested change and its source in `decisions.md`.
3. Update the brief when user-visible outcome, acceptance criteria, permissions, data meaning, non-goals, or success measurement changes.
4. Update the plan when architecture, dependencies, contracts, migrations, rollout, rollback, verification, or expected change surface changes.
5. Reassess workflow and risk classification.
6. Update `state.yml` to show the affected approval as pending.
7. Obtain the applicable human reapproval.
8. Resume only after the work artifacts and state agree.

## Changes that normally require reapproval

- New or weakened acceptance criteria.
- Expanded users, permissions, data, or public behavior.
- New dependency, module, service, migration, or infrastructure change.
- Increased blast radius or risk classification.
- Changed rollout, rollback, or verification strategy.
- Scope growth beyond the approved change budget.

## Minor clarifications

A clarification that does not alter observable behavior, risk, architecture, data, contracts, rollout, or verification may be recorded without reopening approval. When uncertain, treat the change as material.

## Conflict rule

The latest authenticated direction does not directly override the approved artifacts. It authorizes the amendment process. Until that process is complete, the agent reports the affected work as blocked or paused.
