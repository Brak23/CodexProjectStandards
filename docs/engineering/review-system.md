# Stateful code review system

This document defines the portable execution and storage architecture used by the project-local `code-review` skill.

## Core separation

The system separates five concerns:

1. **Target resolution** produces a diff, base, and immutable snapshot identity.
2. **Evidence resolution** computes required evidence from policy, plan, and changed content, then compares it with available evidence.
3. **Scoped review** produces dimension and seam verdicts only within assigned authority.
4. **Aggregation** preserves coverage, verdicts, evidence, finding state, and ownership without manufacturing one review approval.
5. **Merge gating** deterministically applies current repository policy to the exact reviewed snapshot.

## Review targets

Supported targets are:

- GitHub pull request
- Branch diff
- Commit
- Staged changes
- Explicit unstaged changes

Local review defaults to staged changes. Staging is an intentional candidate set; unstaged state may contain experiments and incomplete work. Every local coverage statement records whether unstaged and untracked files were excluded.

Target type does not determine verdict authority. Available, current, snapshot-matching evidence determines what can be concluded.

## Evidence requirements

Effective requirements are the union of:

- the current class-conditional repository policy floor,
- approved plan requirements from a controlled vocabulary,
- static or judgment-based content triggers from the actual change.

Plans may add requirements or tighten centrally defined parameters. They cannot restate, substitute, remove, or weaken baseline predicates.

Diff triggers remain active after plan approval. Changes to authentication, authorization, cryptography, sensitive data, concurrency, migrations, infrastructure, accessibility, or other consequential surfaces can add evidence and specialist-review requirements even when the plan did not anticipate them.

Current policy applies at review time. When policy changed after plan approval, the review reports the delta separately so new obligations are not misrepresented as an author omission.

## Scoped dimensions

A reviewer declares owned dimensions and emits verdicts only for those dimensions:

- `APPROVE`
- `APPROVE_WITH_COMMENTS`
- `CHANGES_REQUESTED`
- `CANNOT_ASSESS`

`CANNOT_ASSESS` means the assigned owner ran but could not evaluate owned scope. It does not mean another dimension was outside the reviewer's assignment. Missing required dimensions are reported as incomplete coverage by aggregation.

Specialist authority binds within specialist dimensions. General-engineering observations about possible specialist concerns are routed as non-binding observations to the qualified owner.

## Seams

Seams are interactions between dimensions in a specific context, not merely generic pairs.

General engineering owns seam detection because it sees the whole change. It does not automatically own specialist seam assessment. A seam owner must be qualified in at least one constituent dimension and must consume the results of every participant dimension.

General-plus-specialist seams may default to the specialist when policy explicitly says so. An unregistered specialist-to-specialist seam remains visibly unassigned and blocks coverage until a qualified owner is assigned. The assignment should be written back to the seam registry.

Seam triggers may fire directly from changed content and instantiate constituent dimensions that individual detectors missed. Reviewers may also request dimensions or seams through bounded dynamic escalation.

Review is two phase:

1. Dimension review
2. Seam review consuming constituent dimension results

A seam may request changes even when each constituent dimension approves in isolation.

## Typed records

The system distinguishes:

- dimension findings,
- seam findings,
- routed observations,
- plan defects,
- evidence gaps,
- escalation requests,
- strengths,
- coverage statements.

Different record types have different authority and aggregation effects. A routed observation cannot block. A binding finding can be issued only by the owner of its dimension or seam.

Every binding finding includes a written acceptance criterion sufficient for a fresh qualified reviewer to adjudicate without conversational memory.

## Binding-finding lifecycle

Implementers may:

- mark a finding `ADDRESSED`, or
- mark it `DISPUTED` with evidence and reasoning.

Qualified dimension or seam owners may:

- resolve,
- reaffirm as still open,
- withdraw as invalid,
- supersede with a materially different finding.

Authenticated humans may waive or delegate authority through a recorded, scoped, expiring exception with compensating controls and follow-up.

Closure verification evaluates both the acceptance criterion and the remediation delta. The implementer's explanation is navigation context, not evidence. A separate defect introduced by the fix becomes a new finding.

A resolved finding that reappears becomes `REGRESSED`, which may trigger stronger tests, root-cause analysis, or architectural remediation.

## Persistent ledger

Durable review state must not be committed to the reviewed feature branch. Doing so would mutate the reviewed diff, expose audit history to rebase and squash rewriting, create concurrent ledger conflicts, and allow the implementer to forge owner-only transitions.

The portable store uses synthetic Git commits:

- `refs/reviews/snapshots/<snapshot-id>` for immutable snapshot bundles
- `refs/reviews/ledgers/<work-id>` for append-only ledger history
- `refs/reviews/merges/<merge-commit>` for final-commit aliases

Ledger updates use atomic compare-and-swap. Snapshot and merge refs are immutable. Repository policy may require commit signing or signed attestations and must validate actor authority independently of storage location.

Arbitrary refs are not fetched by normal clone defaults. Run:

```bash
task review-store-init
```

and explicitly push or automate review refs:

```bash
git push origin 'refs/reviews/*:refs/reviews/*'
```

## Capture and retention

Capture review records uniformly. Vary retention by policy instead of deciding whether to capture based on the reviewer's initial risk classification.

Raw diffs, complete logs, and bulky artifacts may remain external. Durable records must inline the decision-bearing excerpt whenever a finding, closure decision, scoped verdict, or gate decision depends on that evidence. Record the artifact hash, run identity or locator, and explicit retention deadline.

A hash whose referent has expired proves only that an unidentified object once existed. It does not preserve why a decision was made.

## Merge aliases

Squash and rebase merges can orphan reviewed pre-merge commit identities. After merge, write an immutable alias at `refs/reviews/merges/<merge-commit>` that maps the shipped commit to all reviewed snapshot IDs, snapshot refs, reviewed head, base, and merge method.

The pre-merge refs remain valid historical aliases. The merge ref makes shipped history discoverable from the final commit.

## Aggregation

Aggregation produces separate facts:

- dimension coverage,
- seam coverage,
- each received verdict,
- unresolved binding findings,
- evidence sufficiency,
- open escalation and assignment gaps,
- blockers grouped by resolution owner.

Aggregation status is `COMPLETE`, `INCOMPLETE`, `STALE`, `CONTRADICTORY`, or `INVALID`. `COMPLETE` means the record set is coherent and fully evaluable, not that it contains approval verdicts.

## Merge gate

The merge gate returns only `ALLOW` or `BLOCK`. It is deterministic and runs against the exact reviewed snapshot and current base state.

The gate evaluates identity, freshness, policy validity, stabilized requirements, dimension and seam coverage, scoped verdicts, finding state, evidence, human approvals, CI, branch protection, dependencies, and release sequencing.

Emergency progression is represented as `ALLOW` with an explicit emergency or approved-exception decision basis, named bypasses, expiry, compensating controls, and post-merge obligations. It must never appear as normal compliance.
