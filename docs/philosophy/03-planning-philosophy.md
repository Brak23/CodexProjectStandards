# Planning philosophy

Planning converts approved intent into a bounded, testable execution contract. It is not a prediction that the future will unfold exactly as written, and it is not permission to implement unresolved product, architecture, security, or operational decisions.

## Mission

A good plan makes the next responsible action obvious while making uncertainty, consequence, ownership, and verification visible.

The plan should reduce the cost of discovering a misunderstanding before code exists, define how work can be delivered in small coherent increments, and identify when new evidence requires a decision or re-plan.

## Planning contract

A planner must:

- Start from approved intent, not an assumed solution.
- Inspect the existing system before proposing change.
- Separate facts, assumptions, decisions, and unknowns.
- Map every acceptance criterion to implementation and evidence.
- Identify quality attributes and operational consequences early.
- Decompose work into the smallest coherent, reversible increments.
- Record consequential decisions and alternatives.
- Define ownership, permissions, review level, and stop conditions.
- Treat the plan as amendable through explicit change control, not silent drift.

A planner must not:

- Begin implementation.
- Approve its own product intent, plan, architecture decision, risk exception, or release.
- Invent requirements to fill ambiguity.
- Hide unresolved decisions inside implementation steps.
- Produce a file-by-file task list without understanding behavior and architecture.
- Assume passing tests will prove requirements that the tests do not cover.

## The contracts

### Intent contract

The approved brief defines:

- The user or mission problem.
- Desired outcomes and success measures.
- Scope and non-goals.
- Constraints and policy requirements.
- Acceptance criteria.
- Product decisions already made.
- Open product decisions that block planning or implementation.

The planner may identify defects in the brief, but it cannot silently rewrite approved intent.

### Decision contract

Architecturally significant or difficult-to-reverse choices require an explicit decision record. A decision record should contain:

- Context and problem statement.
- Options considered.
- Decision and owner.
- Rationale and evidence.
- Tradeoffs and consequences.
- Confidence.
- Status such as Proposed, Accepted, Rejected, or Superseded.
- Conditions that would trigger reconsideration.

Accepted decisions are historical records. When evidence changes, create a superseding decision rather than rewriting history.

### Execution contract

The approved plan defines:

- Current-state findings.
- The smallest coherent technical approach.
- Expected modules, files, contracts, dependencies, and data changes.
- Milestones and ownership.
- Migration, release, rollback, and operational approach.
- Exact verification strategy.
- Review and approval requirements.
- Change budget and re-planning triggers.

The execution contract authorizes only the recorded scope, tools, environments, and ownership.

### Evidence contract

The plan must state how each consequential claim will be established through tests, observation, scans, builds, contract checks, benchmarks, or production-like validation.

"Verify it works" is not a verification strategy.

## Core principles

### 1. Understand the problem before prescribing the solution

Planning begins with the behavior and outcome that must change, then examines the current system, constraints, and existing patterns.

A plan that starts by selecting a framework, service, dependency, or abstraction before discovery has reversed the decision order.

### 2. Inspect before estimating or decomposing

The planner must inspect relevant:

- Source code and module boundaries.
- Tests and fixtures.
- Public contracts and schemas.
- Data ownership and migrations.
- Architecture decisions.
- Dependencies and runtime versions.
- Operational runbooks and deployment model.
- Recent related changes and known incidents.

Estimates and task boundaries created without repository discovery are low-confidence hypotheses and must be labeled accordingly.

### 3. Plan outcomes and milestones, not speculative keystrokes

Milestones should describe a coherent state that can be verified, reviewed, and handed off. They should not be an exhaustive prediction of every edit.

Good milestone:

> Add the versioned claim-analysis contract and compatibility tests without changing production routing.

Weak milestone:

> Edit controller.py, then edit schema.py, then add tests.

Files are evidence of expected scope, not the reason for the work.

### 4. Work in small coherent batches

Prefer slices that:

- Produce an independently understandable change.
- Keep the system valid after each merge.
- Include related tests and documentation.
- Limit the amount of unreviewed work.
- Can be reverted or disabled independently.
- Reduce overlapping ownership between agents or teams.

Use vertical slices when they deliver an end-to-end behavior safely. Use horizontal slices when a contract, migration, refactor, or layer boundary must precede parallel work.

Separate broad refactoring or formatting from functional change unless the local cleanup is essential to the change and remains easy to review.

### 5. Make acceptance criteria traceable

Every acceptance criterion must map to:

- One or more implementation milestones.
- Exact verification evidence.
- An owner.
- Any required specialist review.

Every milestone should map back to approved intent. Unmapped work is potential scope excess.

### 6. Treat assumptions as expiring liabilities

Each material assumption should state:

- What is assumed.
- Why the assumption is currently reasonable.
- Consequence if false.
- How and when it will be verified.
- Who owns verification.

An assumption that can materially alter architecture, security, data meaning, cost, or user behavior is a decision blocker, not implementation freedom.

### 7. Scale planning to risk and reversibility

Planning depth should increase with:

- Blast radius.
- Irreversibility.
- Trust-boundary or permission changes.
- Data sensitivity and migration complexity.
- Public contract impact.
- Operational consequence.
- Dependency and infrastructure change.
- Novelty and uncertainty.

A documentation typo should not require a feature workspace. Authentication, payment, regulated data, destructive migration, and production access require explicit high-risk planning.

### 8. Prefer reversible decisions and progressive commitment

When multiple valid options exist, prefer the approach that:

- Preserves future choices.
- Can be observed and validated early.
- Limits irreversible investment.
- Supports progressive exposure or feature control.
- Has a clear rollback or roll-forward path.

Do not defer a known critical decision merely to appear agile. Progressive commitment is not avoidance.

### 9. Include failure and operations from the beginning

A production plan must address applicable:

- Failure modes and safe defaults.
- Timeouts, retries, idempotency, concurrency, and partial failure.
- Telemetry, alerts, logs, and release markers.
- Capacity and performance limits.
- Deployment order and mixed-version behavior.
- Data migration, backfill, reconciliation, and recovery.
- Feature disablement, rollback, or roll-forward.
- Support ownership and runbook changes.

The happy path is only one state of the system.

### 10. Record significant decisions, not every implementation detail

Create or update an ADR when a choice materially affects:

- System structure or dependency direction.
- Public interfaces or data ownership.
- Security, privacy, reliability, or availability.
- Technology, framework, or production dependency selection.
- Deployment, migration, or operational model.
- A decision that is expensive or difficult to reverse.

Do not turn ADRs into broad design guides. Keep context, decision, rationale, alternatives, and consequences concise and durable.

### 11. Define a change budget

The plan should identify expected:

- Modules and paths.
- Public contracts.
- Dependencies.
- Migrations.
- Infrastructure and environments.
- Tool permissions.
- Review level.

Stop and re-plan when actual work materially exceeds the approved budget, including when:

- Changed files exceed the estimate by 50 percent.
- An unplanned module or trust boundary must change.
- A new production dependency or migration becomes necessary.
- A public interface or data meaning must change.
- Risk classification or required permissions increase.
- Repeated repair attempts indicate the plan or diagnosis may be wrong.

### 12. Plans evolve through explicit amendments

Discovery during implementation may invalidate part of an approved plan. The implementer should:

1. Stop before crossing the approved boundary.
2. Record the new evidence and affected assumptions.
3. Describe the proposed amendment and consequences.
4. Reassess risk, verification, ownership, and review.
5. Obtain the required approval.
6. Update the plan, decisions, and state before continuing.

Silent plan drift defeats the purpose of planning.

## Planning artifact responsibilities

### `brief.md`

Owns approved product intent, success, constraints, acceptance criteria, and non-goals.

### `plan.md`

Owns the approved implementation approach, milestones, traceability, verification, ownership, and operational strategy.

### `decisions.md` or ADRs

Own consequential choices, alternatives, rationale, confidence, consequences, and supersession history.

### `state.yml`

Records current phase, approvals, ownership, blockers, reviewed commit, and verification state. It reports authority but does not grant it.

### Verification evidence

Records commands, environments, results, artifacts, limitations, and the exact commit tested.

## Plan completeness test

Before approval, the plan should answer:

- What approved outcome changes?
- What is explicitly out of scope?
- What does the system do today?
- Which modules, contracts, data, and environments are affected?
- Which decisions are already approved, and which remain open?
- How is the work decomposed into safe increments?
- How does every acceptance criterion map to evidence?
- What can fail, and how does failure remain safe?
- How will the change be deployed, observed, supported, and reversed?
- Which permissions and tools are required?
- Who owns implementation, decisions, review, and release?
- What evidence would force a re-plan?

If consequential answers are unknown, the correct result is `BLOCKED`, not a more detailed fictional plan.

## Plan defect handling

A reviewer or implementer may identify that an approved plan is flawed even when implementation follows it faithfully.

Plan defects must be recorded against the plan or decision artifact, with evidence, consequence, decision owner, and effect on current work. Do not force the implementer to resolve a product or architecture decision through code review comments.

## Anti-patterns

- Planning from the requested solution without validating the problem.
- Treating a generated task list as architecture discovery.
- Creating one large feature branch because the feature is conceptually large.
- Listing tests without stating which claims they prove.
- Hiding product or security decisions in technical implementation steps.
- Assuming migration and rollback can be designed after coding.
- Recording architectural choices without alternatives or consequences.
- Updating an accepted ADR in place and erasing prior reasoning.
- Continuing after evidence invalidates scope, permissions, or risk assumptions.
- Treating the approved plan as infallible or treating it as optional.

## Source basis

- [Principles behind the Agile Manifesto](https://agilemanifesto.org/principles.html)
- [Google Engineering Practices: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [Google Engineering Practices: Writing good CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html)
- [DORA: Working in small batches](https://dora.dev/capabilities/working-in-small-batches/)
- [DORA: Trunk-based development](https://dora.dev/capabilities/trunk-based-development/)
- [DORA: Continuous delivery](https://dora.dev/capabilities/continuous-delivery/)
- [AWS Prescriptive Guidance: ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [Microsoft Azure Well-Architected: Maintain an ADR](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
