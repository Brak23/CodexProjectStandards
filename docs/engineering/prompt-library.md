# AI engineering prompt library

Use these specialist prompts with the repository files as the source of truth. For short copy-ready prompts organized by common starting situation, begin at [`../prompts/README.md`](../prompts/README.md). Replace bracketed values.

## Ideation and specification

```text
Read AGENTS.md and the product and architecture documentation. Do not modify code.

Turn the following idea into an implementation-ready feature brief:
[idea]

Restate the user problem, challenge premature technical assumptions, inspect current repository behavior, separate explicit requirements from assumptions, identify permissions, data meaning, failure states, compatibility, security, operations, and blocking decisions. Create docs/work/[FEATURE]/brief.md and stop before implementation.
```

## Read-only discovery

```text
Read the approved brief and repository instructions. Do not modify files.

Map the relevant modules, existing patterns, tests, contracts, data ownership, authorization boundaries, dependencies, recent related history, deployment impact, and files considered but rejected. Report any contradiction between the brief and current architecture.
```

## Execution plan

```text
Create or update docs/work/[FEATURE]/plan.md using .agent/PLANS.md. Map every acceptance criterion to implementation and independent verification. State the expected change surface, risk classification, stop conditions, rollout, and rollback. Do not implement until the plan is approved.
```

## Implementation

```text
Implement the approved plan on an agent/* branch. Keep the repository coherent after each milestone. Update progress and decisions. Do not change protected tests or controls to pass. Stop and re-plan if scope or risk changes materially.
```

## Adversarial review

```text
Review the approved brief, plan, final diff, tests, and verification evidence using fresh context. Search specifically for requirement mismatch, authorization bypass, tenant leakage, race conditions, fail-open behavior, migration risk, test gaming, unnecessary scope, documentation contradiction, and rollback gaps. Do not merely summarize the diff.
```

## Failed verification

```text
The implementation failed verification. Revert speculative repairs, reproduce from a clean state, identify the first incorrect state and causal chain, record rejected hypotheses, and gather new evidence before proposing another change. Do not weaken the verifier.
```

## PR preparation

```text
Generate the PR description from the final diff and actual verification results. Include user-visible behavior, deliberately unchanged behavior, architecture, security, data, exact checks, rollout, rollback, limitations, and evidence-based confidence. Do not claim secure, backward compatible, fully tested, or production ready without explicit evidence.
```
