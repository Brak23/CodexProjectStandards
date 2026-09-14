# AI-assisted development workflow

## Operating model

The product owner owns outcomes, domain rules, priorities, consequential commitments, and product acceptance. The agent owns repository discovery, technical planning, implementation, tests, documentation, technical review, and allowed release execution. CI and protected environments enforce only the controls they are actually configured to enforce.

## Phases

### 1. Ideation and specification

No code changes. Convert the idea into a feature brief. Challenge flawed premises, identify missing journeys, permissions, failure states, data meaning, compatibility, security, and operational requirements.

In delegated mode, a clear product request authorizes ordinary engineering work. Formal mode retains its intent gate.

### 2. Read-only discovery

Inspect repository instructions, architecture, existing implementations, tests, contracts, history, dependencies, and deployment implications. Identify files considered but rejected.

### 3. Execution planning

Create a self-contained plan using `.agent/PLANS.md`. Map every acceptance criterion to implementation and verification. State the change budget and stop conditions.

Ask for a decision only when it changes the product outcome or introduces a material commitment, data boundary, irreversible effect, or unapproved production action.

### 4. Autonomous implementation

Work on an isolated `agent/*` branch. Implement milestone by milestone, update progress, and re-plan when scope or risk changes.

### 5. Independent review

Use fresh context or a separate reviewer. Review the approved brief, plan, final diff, tests, and evidence. Search for requirement mismatch, authorization bypass, data leakage, concurrency defects, evaluator manipulation, unnecessary scope, and rollback gaps.

### 6. Deterministic verification

Run the applicable verification ladder and create `verification.md`. A targeted test cannot support a repository-wide completion claim.

### 7. PR and release preparation

Generate the PR from the final diff. Document final behavior, deliberately unchanged behavior, migration, security, rollout, rollback, and limitations.

### 8. Merge and production release

The agent may execute a merge or deployment when the configured repository policy, integration, and scoped authorization permit it. A product owner decides consequential release authorization; editable repository records and PR authorship do not prove that decision.

### 9. Post-deployment verification

Verify health, critical user journeys, latency, errors, saturation, business events, and canary comparisons. Roll back when predefined thresholds fail.

## Agent completion statuses

- `COMPLETE`
- `COMPLETE_WITH_LIMITATIONS`
- `BLOCKED`
- `FAILED_VERIFICATION`

The system is designed to finish correctly or stop visibly, not to always produce a completion claim.
