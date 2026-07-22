# Review storage and retention

## Why review records are outside the working tree

A reviewer must not mutate the branch it is reviewing. Tracked ledger files would change the reviewed diff, be vulnerable to rebase and squash rewriting, conflict under concurrent review, and allow the implementer to forge owner-only transitions.

The durable store therefore uses synthetic Git commits under a separate ref namespace.

## Ref layout

- `refs/reviews/snapshots/<snapshot-id>` points to one immutable bundle for the reviewed snapshot.
- `refs/reviews/ledgers/<work-id>` points to an append-only commit chain containing ledger events and materialized state.
- `refs/reviews/merges/<merge-commit>` points to a merge alias bundle that maps the shipped commit to all pre-merge snapshot IDs and refs.

A snapshot ref is immutable. A ledger update uses compare-and-swap against the previous ref value. A merge alias is immutable once written.

## Transport

Arbitrary refs are not fetched by ordinary clone defaults. `review_store.py init` adds:

`+refs/reviews/*:refs/reviews/*`

to the selected remote fetch configuration. Review refs must also be pushed explicitly or by repository automation.

## Authority and tamper resistance

Storage separation alone does not prove reviewer authority. Repositories should require signed synthetic commits or signed disposition attestations when risk warrants it, restrict who may push review refs, and validate actor role and authority during aggregation.

An implementer-controlled write to a review ref is invalid unless policy explicitly grants that transition. The event remains auditable but has no authority.

## Uniform capture, tiered retention

Capture dimension, seam, evidence-decision excerpts, finding events, and aggregation uniformly. Retention varies by repository policy, not by whether the reviewer initially thought the change was important.

Durable records must retain enough evidence to explain the decision after external artifacts expire. For any evidence on which a binding finding, closure decision, or gate decision turns, inline:

- the failed assertion or decisive test result,
- the relevant analyzer message,
- CI conclusion and run identity,
- a concise source excerpt when needed,
- provenance hash and external locator,
- explicit external retention deadline.

Hashes prove identity but do not replace retained decision evidence.

## Merge mapping

After merge, create `refs/reviews/merges/<merge-commit>` with aliases to reviewed pre-merge snapshots. For squash merges, the final commit is not expected to equal the reviewed head SHA, so the alias manifest records the merge method, base, reviewed head, snapshot IDs, and final merge commit.
