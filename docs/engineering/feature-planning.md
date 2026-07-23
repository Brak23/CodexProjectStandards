# Feature execution planning system

The Feature Execution Planner converts approved intent and approved technical decisions into a reviewable release contract. It does not perform product discovery, implementation, code review, or release authorization.

## Priority order

When planning targets conflict, preserve them in this order:

1. Approved intent, safety, and policy.
2. Reversibility or explicitly approved forward recovery.
3. Independently releasable and observable increments.
4. Reviewability.
5. Minimum implementation scope.

## Gates

- Gate 0 owns approved intent and acceptance-criterion revisions.
- Gate 1 owns immutable decision revisions and their dependency closure.
- Gate 2 owns obligations, execution attempts, milestone compositions, evidence design, and the plan manifest.
- A separate implementation authorization names the exact work that may begin.

Each gate uses a separate PR. Mixed authority gates fail validation.

## Record model

Normative records are strict JSON with `planning-canonical-json-v1` content hashes. Generated `decisions.md`, `plan.md`, and graph files are review views and must never be edited manually.

Approval is derived from authenticated GitHub review over the exact head and protected merge. Records do not contain author-editable approval claims.

## Decisions

A decision has a stable ID and immutable revisions. Amendments create a new revision rather than rewriting the selected option. Every record declares reversal cost, two or three options, what each option forecloses, a recommendation, owner roles, deadline, default, and explicit dependencies.

Changed decisions and their transitive dependents require revalidation.

## Obligations and execution attempts

An obligation is the stable piece of approved intent that must become true. Execution attempts are immutable approaches beneath it. Evidence and code references stay with the attempt that produced them. Evidence reuse requires an item-level carry claim naming the amendment and arguing specific non-impact.

Every active obligation has one current execution. Displaced executions are terminal and name their successor.

## Milestones

A milestone is a validated release composition over borrowed criteria. It owns no acceptance criteria. Behavioral milestones claim active AC revisions, enabling milestones support later releases, and maintenance milestones claim approved maintenance objectives.

Every current execution belongs to one current milestone. Every active AC is claimed by one behavioral milestone. A milestone owns joint evidence, observability, rollout, rollback or forward recovery, guarantees, dependencies, and release accountability.

## Plan approval and authorization

A plan revision is an immutable manifest over the current normative records and generated graphs. Structural validation makes it eligible for human approval; it does not judge architecture or authorize implementation.

After Gate 2 approval, a separate immutable authorization event names exact plan, milestone, and execution revisions. Wildcard authorization is prohibited. `state.yml` is an operational projection and not the source of authority.

## Independent review

A separate planner reviewer evaluates intent fidelity, architecture, release composition, reversibility, observability, evidence adequacy, and scope realism. Planning review reuses the Code Review skill's durable snapshot, finding lifecycle, and closure authority.

## Legacy workspaces

Existing model-v1 workspaces remain legacy until explicitly migrated. Migration preserves prior artifacts and creates draft model-v2 records with no approval or authorization claims.
