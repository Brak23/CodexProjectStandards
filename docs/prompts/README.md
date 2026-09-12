# Prompt entry points

Copy the prompt that matches where you are. The repository files remain the source of truth.

## Brand-new project

```text
Read AGENTS.md, project.yml, README.md, and the getting-started documentation. Do not write application code yet.

Assess the repository setup, run task doctor and task verify, identify missing stack-profile tasks or GitHub configuration, and give me the shortest ordered path to a ready development baseline. Stop before making consequential architecture choices.
```

## Decide which workflow applies

```text
Read AGENTS.md and docs/getting-started/workflow-decision-tree.md.

Classify this request as Routine, Meaningful, or High Risk from observed behavior, reversibility, affected boundaries, and the requested environment. Treat words in the request as inspection hints, not proof. Do not modify files yet.

Request:
[describe the change]
```

## Small bug fix

```text
Read AGENTS.md and investigate this bug before editing files.

Use the routine workflow unless observed behavior crosses a shared boundary, is hard to reverse, or changes a consequential surface. Reproduce the bug, identify the causal chain, make the smallest coherent fix, run focused tests and applicable verification, and report evidence and limitations.

Bug:
[describe the bug]
```

## New feature

```text
Read AGENTS.md and the product and architecture documentation. Inspect the repository before editing.

In delegated mode, create or update work.md and implement this feature. In formal mode, produce the implementation-ready brief for:
[describe the feature]

Define observable acceptance criteria and non-goals, identify permissions, data meaning, failure states, compatibility, security, and consequential decisions. Continue with ordinary engineering work; ask only for unresolved consequential product decisions.
```

## Formal brief to plan

```text
Read AGENTS.md, the approved brief, repository architecture, contracts, tests, and .agent/PLANS.md. Do not implement.

Perform read-only discovery and create plan.md. Map every acceptance criterion to implementation and independent verification. Include change surface, alternatives, risk, rollout, rollback, stop conditions, and blocking decisions. Stop for plan approval.
```

## Implement a delegated work record or formal plan

```text
Read AGENTS.md, the active work record or formal plan, and all relevant nested instructions.

Implement on an agent/* branch. Keep scope bounded, update progress and material decisions, preserve protected tests and controls, run verification after coherent milestones, and replan technical details as discovery improves. Ask only for unresolved consequential decisions or unavailable required capability.
```

## Refactor

```text
Read AGENTS.md and inspect current behavior and tests. Do not assume behavior may change.

Propose the smallest refactor that reduces the stated maintenance cost while preserving public and user-visible behavior. Identify invariants, affected boundaries, regression tests, and rollback. Use a full plan if the refactor spans modules or public contracts.
```

## Adversarial review

```text
Using fresh context, review the approved brief, plan, final diff, tests, and verification evidence.

Search for requirement mismatch, authorization bypass, data leakage, race conditions, fail-open behavior, migration risk, test gaming, unnecessary scope, documentation contradiction, operational gaps, and unsupported completion claims. Report findings by severity and do not merely summarize the diff.
```

## Architecture review

```text
Read AGENTS.md and the architecture documentation. Review the proposed change for boundary violations, duplicated responsibilities, coupling, data ownership, compatibility, dependency direction, operability, and rollback. Separate blocking findings from optional improvements.
```

## Security review

```text
Read AGENTS.md, the security standards, threat model, and final diff. Identify changed assets, actors, trust boundaries, entry points, authorization decisions, sensitive data flows, secret handling, dependency risks, abuse cases, failure modes, and missing tests. Do not state that the change is secure; state evidence, findings, and residual risk.
```

## Release preparation

```text
Read the approved work documents, final diff, verification evidence, operations guidance, and release policy.

Prepare the release summary, rollout sequence, success and abort metrics, rollback steps, observability checks, ownership, and known limitations. Execute production only through a configured integration and scoped authorization; otherwise report the exact missing boundary.
```

## Incident or postmortem

```text
Read the incident evidence and relevant repository documentation. Separate timeline facts from hypotheses. Identify impact, detection, first incorrect state, causal chain, contributing conditions, response effectiveness, and corrective actions with owners and verification. Avoid blame and do not invent missing evidence.
```

For longer specialist prompts, see [`../engineering/prompt-library.md`](../engineering/prompt-library.md).
