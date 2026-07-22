---
name: code-review
description: >
  Perform an independent, read-only review of staged, unstaged, commit, branch,
  or pull-request changes. Capture an immutable snapshot, resolve evidence
  requirements, issue scoped dimension and seam verdicts, reconcile binding
  findings through the review ledger, aggregate coverage, and optionally run
  the deterministic merge gate. Use for initial review, specialist review,
  seam review, finding closure, or merge-policy evaluation. Do not use to
  implement fixes or to approve product, release, or exception decisions.
---

# Code review

## Mission

Improve code health over time. Merge readiness is not a reviewer verdict. Reviewers issue scoped verdicts; a deterministic policy gate separately decides whether an exact snapshot may merge.

## Invariants

- Remain read-only. Write only review artifacts or unapplied mechanical suggestions allowed by policy.
- Review an immutable snapshot and record its hash.
- Default local review to staged changes. Unstaged review must be explicit.
- Issue verdicts only for dimensions or seams assigned to this reviewer.
- A missing reviewer is incomplete coverage, not `CANNOT_ASSESS`.
- `CANNOT_ASSESS` means the assigned owner ran but lacked evidence, access, context, expertise, or comprehensibility.
- Every binding finding includes a written acceptance criterion.
- Implementers may mark binding findings addressed or disputed. Only a qualified owner may resolve, withdraw, supersede, or reaffirm them.
- General engineering detects seams. Qualified specialists assess them after constituent dimension reviews complete.
- Preserve findings and decisions outside the reviewed branch under `refs/reviews/*`.
- Never manufacture findings to fill categories.

## Modes

- `DISCOVERY`: resolve target, capture snapshot, classify risk, derive evidence, dimensions, and seams.
- `DIMENSION_REVIEW`: review assigned dimensions and route observations outside owned authority.
- `SEAM_REVIEW`: assess a registered interaction after all required participant reviews exist.
- `CLOSURE_REVIEW`: adjudicate addressed or disputed binding findings against a new snapshot.
- `AGGREGATION`: combine coverage, verdicts, evidence, ledger state, escalations, and exceptions.
- `MERGE_GATE`: run only the deterministic gate evaluator.
- `FULL_REVIEW`: coordinate all applicable phases except merge authorization unless explicitly requested.

## Required context

Always read:

1. `AGENTS.md` and `agent-policy.yml`.
2. `docs/philosophy/01-engineering-principles.md`.
3. `docs/philosophy/02-review-philosophy.md`.
4. `docs/engineering/code-review.md`.
5. `docs/engineering/review-independence.md`.
6. `docs/engineering/review-system.md`.

Also load the approved brief, plan, state, decisions, verification evidence, nearest nested `AGENTS.md`, affected contracts, ADRs, tests, and dimension-specific standards when applicable.

## Execution

1. Resolve one target: `github_pr`, `branch_diff`, `commit`, `staged`, or explicit `unstaged`.
2. Capture an immutable snapshot and record included and excluded local state.
3. Resolve effective evidence requirements as the union of:
   - current policy for the effective change class,
   - approved plan requirements from the controlled vocabulary,
   - static and judgment-based content triggers.
4. Derive required dimensions and context-specific seams. Seam triggers may instantiate dimensions.
5. Collect evidence and inline the decision-bearing excerpt for evidence on which a finding or verdict depends.
6. Run assigned dimension reviews. Route out-of-scope observations to the owning specialist.
7. Process bounded dynamic escalation. Open specialist-to-specialist seams require explicit owner assignment.
8. Run seam reviews after constituent dimension results are available.
9. Reconcile candidate findings against the persistent ledger before publishing them.
10. Aggregate without producing a scalar review approval.
11. Run the deterministic merge gate only when requested and required external state is available.

## Binding finding contract

A binding finding must contain severity, confidence, owned dimension or seam, location, problem, impact, evidence, authority basis, acceptance criterion, resolution owner, and estimated fix cost.

Lifecycle:

`OPEN -> ADDRESSED | DISPUTED -> RESOLVED | STILL_OPEN | WITHDRAWN | SUPERSEDED | WAIVED`

`REGRESSED` is used when a resolved finding reappears. `WAIVED` requires authenticated human authority, scope, expiry, compensating controls, and follow-up.

## Storage

Use `capture_review_snapshot.py` to create the target-neutral snapshot, `compose_requirements.py` to build the effective requirement set, and `review_store.py` for durable Git-ref storage.

- Immutable snapshot bundle: `refs/reviews/snapshots/<snapshot-id>`
- Append-only work ledger: `refs/reviews/ledgers/<work-id>`
- Merge mapping: `refs/reviews/merges/<merge-commit>`

Ordinary clones do not fetch arbitrary refs automatically. Run `task review-store-init` to configure the review refspec and verify it.

## Stop statuses

Report one of these when the workflow cannot continue safely:

- `BLOCKED_TARGET`
- `INVALID_REVIEW_REQUEST`
- `INCOMPLETE_CONTEXT`
- `REVIEW_ASSIGNMENT_REQUIRED`
- `EVIDENCE_REQUIRED`
- `REQUIREMENTS_UNSTABLE`
- `ARTIFACT_CONTRADICTION`
- `POLICY_EXCEPTION_REQUIRED`

Do not convert a blocked or incomplete result into approval because the code appears reasonable.
