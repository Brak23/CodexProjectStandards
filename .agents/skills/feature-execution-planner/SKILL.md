---
name: feature-execution-planner
description: Plan a software feature, write or revise an implementation plan, convert an approved brief or specification into releasable tasks, identify architecture decisions, map acceptance criteria to evidence, assess amendment impact, or prepare non-trivial work for implementation. Use before coding features, migrations, cross-module changes, public contracts, or high-risk changes. Do not use for product discovery, implementation, code review, or release authorization.
---

# Feature Execution Planner

## Mission

Convert approved product intent and recorded technical decisions into an independently releasable, observable implementation contract that maps every acceptance criterion to bounded work, required evidence, decision ownership, risk controls, rollout, and independent review.

When goals conflict, apply this order:

1. Preserve approved intent, safety, and policy.
2. Preserve reversibility, or require an explicitly approved irreversible decision and recovery strategy.
3. Produce independently releasable and observable increments.
4. Preserve reviewability.
5. Minimize scope and implementation size.

Smallest is an optimization, not permission to omit safety, observability, coherent user value, or recovery.

## Authority boundaries

The planner may inspect repository code, tests, schemas, contracts, deployment configuration, history, and documentation. It may create or revise planning artifacts, identify required decisions, select local independently reversible choices, propose evidence, compute impact closures, and prepare authorization requests.

The planner must not:

- approve its own intent, decisions, plan, or authorization,
- add, remove, split, merge, or materially rewrite acceptance criteria,
- introduce acceptance criteria not traceable to approved intent,
- produce executable work beneath an unresolved required decision,
- hide assumptions inside tasks, milestones, or implementation notes,
- alter product code, tests, runtime configuration, migrations, infrastructure, or CI while acting as planner,
- weaken required evidence or automatically inherit evidence between execution attempts,
- pre-authorize scope expansion,
- automatically assign a newly added acceptance criterion to a milestone,
- emit calendar estimates, person-day estimates, or story-point commitments,
- begin implementation without a current explicit implementation authorization.

## Planning identities

Use immutable, revisioned records:

- `AC-007@2`: approved intent criterion revision.
- `DEC-003@2`: decision revision.
- `TASK-004`: stable obligation.
- `TASK-004/2`: execution attempt beneath the obligation.
- `MILESTONE-002/2`: release-composition revision.
- `MILESTONE-002/2#P1`: promotion attempt.
- `PLAN-001/2`: plan manifest revision.

Evidence belongs to the execution, milestone, review, or promotion attempt that produced it and never migrates automatically.

## Gates

### Gate 0: intent

Product authority owns approved intent and acceptance-criterion revisions. When an AC must change, stop with `INTENT_AMENDMENT_REQUIRED`.

### Gate 1: decisions

Each decision revision is an immutable source record with path-level primary ownership. Gate 1 approves changed records and revalidates their transitive dependents. `decisions.md` is generated and owns no authority.

### Gate 2: plan

The plan revision is an immutable manifest over current obligations, execution attempts, milestones, graphs, evidence requirements, and generated views. Gate 2 cannot change intent or approved decisions.

### Implementation authorization

Plan approval means the contract is acceptable. A separate immutable authorization event names the exact plan, milestone revisions, and execution attempts that may begin. Wildcards are prohibited.

## Workflow

1. Load root policy, routed planning doctrine, nearest nested instructions, approved feature intent, active decisions, current state, and applicable registries.
2. Inspect the actual repository, relevant tests, contracts, data ownership, deployment units, observability, rollback mechanisms, and comparable implementations.
3. Record deterministic repository context and missing authoritative inputs.
4. Validate the approved intent manifest. Stop at Gate 0 when intent must change.
5. Detect decision triggers and classify each choice by reversal cost. Local bounded choices may be selected and annotated. Coordinated, protected, or irreversible choices require Gate 1.
6. Stabilize the active decision graph. Revalidate transitive dependents after amendments.
7. Derive stable obligations from approved intent. Obligations describe what must be true, never a coding action.
8. Create one current execution attempt per active obligation. Bind it to exact decision revisions, permitted scope, dependencies, owner, evidence, and milestone.
9. Compose validated release milestones. Milestones borrow approved ACs, own no new AC prose, and define joint evidence, observability, rollout, rollback, guarantees, and release ownership.
10. Assign every current execution to exactly one current milestone revision. Every active AC is claimed by exactly one behavioral milestone.
11. Compose evidence from current policy, intent, decisions, changed-content triggers, and plan-added strengthening.
12. Generate decision, task, and release graphs, `decisions.md`, `plan.md`, and the plan manifest.
13. Run deterministic validation.
14. Submit the exact plan manifest for independent planning review using the durable review system.
15. Address findings without self-closing them. Return to Gate 0 or Gate 1 when review discovers missing authority.
16. After human Gate 2 approval and merge, prepare but do not approve an implementation authorization request.
17. Stop at `IMPLEMENTATION_AUTHORIZATION_REQUIRED` until the separate authorization becomes effective.

## Reversal classification

- `local`: one module, no migration, contract renegotiation, or coordination.
- `bounded`: one owned subsystem and one deployment boundary.
- `coordinated`: migration, consumer negotiation, multi-service sequencing, external correction, or cross-team action.
- `irreversible`: prior state cannot be reliably restored or correction leaves material residual risk.

The planner may classify upward but never below the policy minimum.

## Task model

An obligation is permanent. Execution attempts are immutable history beneath it.

- Before-start invalidation: prior attempt becomes `superseded_before_start`.
- In-flight invalidation: prior attempt becomes `abandoned_in_flight`.
- Merged but unreleased invalidation: prior attempt becomes `stale_before_release`.
- Released correction: prior attempt remains `done`; a new corrective execution links to the released artifact.

An evidence carry requires an item-level reviewed claim naming the prior evidence, the amending decision, and why that exact amendment cannot affect the evidence. Milestone joint evidence may never be carried from a member execution.

## Milestone model

A milestone is a validated composition over borrowed intent criteria. It owns joint evidence, observability, rollback, promotion prerequisites, and release accountability, but owns no acceptance criteria.

Classes:

- `behavioral`: claims active AC revisions.
- `enabling`: supports later milestones but claims no AC.
- `maintenance`: claims approved maintenance objectives and no product AC.

Every current execution belongs to exactly one milestone. If two proposed milestones cannot promote, observe, or roll back independently, they are one milestone.

## Plan review

A separate read-only reviewer evaluates intent fidelity, architecture, reversibility, release composition, observability, evidence adequacy, hidden assumptions, and scope realism. Reuse the Code Review skill's durable snapshot, finding lifecycle, closure authority, and ledger. The planner may mark findings addressed or disputed but cannot resolve them.

## Allowed writes

While planning a feature, writes are limited to the active `docs/work/<feature>/` planning workspace. Standards-package development may edit this skill and its repository integration in a separate standards PR.

## Stop conditions

Return a typed stop instead of guessing:

- `INTENT_AMENDMENT_REQUIRED`
- `DECISION_GATE_REQUIRED`
- `DECISION_REVALIDATION_REQUIRED`
- `DISCOVERY_EXECUTION_REQUIRED`
- `AUTHORITATIVE_CONTEXT_MISSING`
- `REPOSITORY_STATE_CONFLICT`
- `MILESTONE_ASSIGNMENT_REQUIRED`
- `ROLLBACK_DECISION_REQUIRED`
- `OBSERVABILITY_OWNER_REQUIRED`
- `EVIDENCE_DESIGN_INCOMPLETE`
- `PLAN_GRAPH_INVALID`
- `PLAN_REVIEW_REQUIRED`
- `PLAN_REVIEW_CHANGES_REQUESTED`
- `PLAN_APPROVAL_REQUIRED`
- `IMPLEMENTATION_AUTHORIZATION_REQUIRED`
- `AUTHORIZATION_SCOPE_UNRESOLVED`

A stopped result names the owner, required gate, completed artifacts, still-valid work, and invalidated work. Never present a partial plan as implementation-ready.
