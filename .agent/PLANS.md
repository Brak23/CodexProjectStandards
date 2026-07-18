# Execution plan standard

An ExecPlan is the approved execution contract for non-trivial work. It must be self-contained enough that another engineer or agent can continue using only the repository and the plan.

## When required

Use an ExecPlan for features, cross-module changes, migrations, public contracts, security-sensitive work, infrastructure, significant refactors, or work expected to exceed 60 minutes.

## Required sections

### Purpose

State the user-visible or operational outcome and why it matters.

### Current behavior

Describe current implementation and the evidence used to establish it.

### Acceptance criteria

Copy or link every observable criterion from the approved brief. Do not rewrite criteria into weaker technical proxies.

### Non-goals

State what is deliberately excluded.

### Assumptions and unknowns

Classify each item as:

- Confirmed
- Low-risk and reversible assumption
- Blocking human decision

### Repository context

Identify relevant modules, comparable patterns, tests, public contracts, persistence, deployment topology, and external dependencies.

### Proposed design

Describe component changes, data flow, error behavior, authorization, observability, and why the design fits existing architecture.

### Alternatives considered

Record materially different options and why they were rejected.

### Risk classification

State risk level and changed trust boundaries, sensitive data, authorization, dependencies, network access, migration impact, and operational blast radius.

### Expected change surface

List expected files and directories. Record explicit expectations for:

- New dependencies
- Public contract changes
- Database migrations
- Infrastructure changes
- Feature flags
- Documentation changes

### Implementation milestones

Each milestone must leave the repository coherent and independently verifiable.

### Verification matrix

Map each acceptance criterion to implementation locations, tests, scanners, and observed evidence.

### Rollout

Describe sequencing, flags, canary or cohort strategy, release metrics, and success thresholds.

### Rollback or disablement

Describe the fastest safe recovery path and any irreversible effects.

### Progress

After every milestone record:

- Work completed
- Files changed
- Commands executed
- Results
- Unexpected findings
- Failed approaches
- Remaining work
- Current blockers

### Decision log

Record consequential implementation decisions with date, decision, rationale, alternatives, and consequences.

### Final evidence

Record the final commit, exact validation commands, results, remaining limitations, deployment notes, and final completion status.

## Replanning triggers

Stop and revise the plan when scope expands materially, risk increases, an unplanned dependency or migration is required, a public contract changes, or two repair attempts fail for the same symptom.
