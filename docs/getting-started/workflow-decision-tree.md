# Workflow decision guide

Use this guide after inspecting the requested behavior and the action environment. The recommender is advisory; words in a ticket are not a risk classification.

## Routine

Use for localized, well-understood, reversible work with low blast radius.

1. Confirm current behavior.
2. Make the coherent change.
3. Run focused checks and applicable application verification.
4. Report the changed behavior and how to inspect it.

## Meaningful

Use when behavior crosses a shared boundary, needs technical tradeoffs, is difficult to reverse, or has material unknowns.

1. In delegated mode, create or update **work.md** with outcome, constraints, technical plan, verification, and material decisions.
2. Inspect affected modules, contracts, dependencies, and operational effects.
3. Implement and obtain fresh-context review when available.
4. Demonstrate the result and record limitations.

Formal mode uses its existing planner for the same class of work.

## High risk

Use when executable behavior changes a trust boundary, sensitive or regulated data, production state, or an irreversible external effect.

Use the meaningful workflow and add applicable security, data, rollback, staged-release, and specialist evidence. Development and local testing may proceed within policy; production execution still needs a configured integration and scoped authorization.

## Fast command

Run:

```bash
task recommend
```

For noninteractive use, supply observed facts rather than relying on a description alone:

```bash
python3 scripts/recommend_workflow.py "Fix authorization bypass" --trust-or-sensitive
```
