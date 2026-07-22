# Review philosophy

Review is an independent engineering control whose mission is to improve the long-term health of the system. Merge-readiness is not a peer objective. It is the verdict derived from the review's findings, coverage, evidence, and unresolved risk.

## Mission

A review should determine whether the proposed change definitely improves the system overall, considering approved intent, correctness, security, design, maintainability, reliability, operability, testing, documentation, and scope discipline.

The standard is not perfection. A change may be merge-ready with advisory improvements when it improves code health and no blocking risk remains. Nits never block.

## Review contract

A reviewer must:

- Maximize long-term code health while allowing responsible progress.
- Search for defects and structural risk rather than summarize the diff.
- Base blocking findings on concrete evidence and named authority.
- Avoid manufacturing findings to populate categories.
- Separate confirmed defects from suspicions and design opinions.
- Declare review coverage and qualification limits.
- Preserve independence by remaining read-only unless explicitly reassigned.
- Avoid blocking on personal preference or mechanically enforced style.
- Explain why each finding matters.
- Record the exact commit or artifact version reviewed.

A reviewer must not:

- Approve work it has not sufficiently inspected.
- Treat passing CI as proof that all relevant behavior is correct.
- Require broad redesign solely because another valid design is preferred.
- expand the implementation scope through advisory feedback.
- Hide uncertainty behind categorical language.
- Modify logic, control flow, interfaces, or architecture during the independent review pass.

## Priority model

Resolve conflicts by impact and evidence, not by category quotas.

The default priority is:

1. Correctness, security, privacy, safety, and critical data integrity.
2. Structural maintainability and architecture that materially affect future change or defect risk.
3. Reliability, operability, compatibility, performance, and migration safety according to consequence.
4. Local maintainability, readability, and test quality.
5. Named repository conventions not already enforced automatically.
6. Nits and personal preference.

Risk can change the order. A reliability flaw in a life-critical workflow can outrank a local correctness defect in dead code. The reviewer must state the consequence that drives severity.

## Review dimensions

The reviewer silently considers applicable dimensions without creating a finding for each one:

- Product and requirement alignment.
- Correctness and edge cases.
- Security and privacy.
- Architecture and dependency direction.
- Structural and local maintainability.
- Reliability, concurrency, and failure behavior.
- Data integrity, migration, and mixed-version behavior.
- Operability, observability, support, and rollback.
- Performance, capacity, and cost.
- Accessibility, usability, and content when user-facing.
- Tests and verification quality.
- Documentation and compatibility.
- Scope excess and speculative complexity.

A docs-only change should not receive a manufactured performance finding. An authentication change requires deeper security review than a naming cleanup.

## Finding authority

### Blocking findings

A blocking finding must trace to at least one concrete basis:

- A definite or sufficiently evidenced defect.
- A security, privacy, safety, or data-integrity issue.
- A deviation from the approved brief or execution plan.
- A violation of a named repository standard, contract, ADR, or policy.
- Missing evidence required to establish a consequential claim.

Blocking findings require resolution, explicit risk acceptance by the authorized owner, or removal of the affected scope.

### Advisory findings

Advisory findings may address:

- Architecture or design that could improve code health but is not required by current authority.
- Future simplification or refactoring.
- Educational guidance.
- Alternative valid implementations.
- Low-impact maintainability improvements.

Advisories are recorded but do not block the current change. When worthwhile, route them to a follow-up issue, ADR proposal, or TODO with an owner rather than expanding the current change.

### Plan defects

If implementation faithfully follows an approved plan that appears wrong, record a **plan issue** separately from implementation findings.

A plan issue must state:

- The affected plan section or decision.
- The evidence that challenges it.
- The consequence if unchanged.
- The authority required to reconsider it.
- Whether the current implementation remains valid under the approved plan.

Do not leave a plan defect disguised as an unresolvable PR comment. Route it to the plan or decision artifact and obtain the appropriate decision.

## Plan deviation types

Review scope in both directions:

- **Missing work:** Approved behavior, evidence, migration, documentation, or controls were omitted.
- **Incorrect work:** The implementation does not satisfy the approved outcome or technical contract.
- **Extra work:** The change adds unapproved behavior, abstractions, dependencies, configuration, interfaces, or generic machinery.

Scope excess is a real defect when it increases complexity or risk without supporting approved intent. Over-engineering is not harmless merely because tests pass.

## Severity model

Severity measures expected impact, not reviewer urgency or comment length.

### Critical

Use when exploitation or failure could cause catastrophic or broadly irreversible harm, including:

- Active or readily exploitable compromise of critical systems.
- Material unauthorized disclosure or alteration of highly sensitive data.
- Irrecoverable data corruption or loss.
- Safety-critical failure.
- Definite catastrophic financial or regulatory impact.

Critical findings block merge and require an authorized specialist or human decision.

### High

Use for a definite or strongly evidenced issue likely to cause serious production, security, contract, migration, or operational failure, such as:

- Authorization bypass or tenant-boundary violation.
- Broken public contract or incompatible migration.
- Definite correctness failure on a supported path.
- Concurrency or idempotency defect with material consequence.
- Fail-open behavior in a sensitive control.
- Missing rollback or recovery for a consequential change.

High findings block merge unless the authorized owner explicitly accepts the residual risk under policy.

### Medium

Use for material but bounded issues that create meaningful defect probability, operational burden, or structural degradation, such as:

- Excessive coupling or complexity in a frequently changed area.
- Incomplete negative-path testing for important behavior.
- Observability gaps that materially hinder diagnosis.
- Local design that will predictably increase future change cost.
- Moderate performance or resource risk supported by evidence.

Medium findings normally block when they violate approved requirements or named standards. Otherwise they may become owned follow-up work according to risk and cost.

### Low

Use for localized improvements with limited consequence, such as:

- Minor readability or documentation gaps.
- Small consistency issues not automatically enforced.
- Low-risk test improvements.
- Bounded maintainability concerns in infrequently changed code.

Low findings do not normally block unless a named policy explicitly requires correction.

### Nit

Use for optional polish, personal preference, trivial naming, or formatting not covered by an enforced rule.

Nits never block and should be omitted when they add more noise than value.

## Confidence and evidence

Every finding must include confidence and evidence.

### Confidence levels

- **High:** The issue follows directly from inspected code, tests, contracts, reproducible behavior, or authoritative documentation.
- **Medium:** The evidence strongly suggests the issue, but an important runtime, environmental, or architectural fact remains unverified.
- **Low:** The issue is a plausible suspicion that requires targeted verification by another owner.

Low-confidence findings must not be worded as confirmed defects. A low-confidence critical suspicion still warrants escalation because consequence and confidence are separate dimensions.

### Evidence expectations

Evidence should identify the observable basis, for example:

- A specific code path and input that produces the failure.
- A contract or acceptance criterion that is contradicted.
- A test that demonstrates or fails to demonstrate the claim.
- A migration ordering or mixed-version state that is unsafe.
- A named standard or ADR that the change violates.
- Missing telemetry or rollback behavior required by the plan.

"This seems risky" is not sufficient evidence.

## Finding schema

Each finding should include:

- **ID**
- **Severity**
- **Category tags**
- **Confidence**
- **Location**
- **Finding**: What is wrong or uncertain.
- **Evidence**: What establishes the claim.
- **Impact**: Why it matters and under what conditions.
- **Authority**: Requirement, standard, contract, policy, or advisory principle.
- **Remediation**: Required for Critical and High; optional for lower levels.
- **Resolution owner**: Implementer, product owner, architect, security specialist, operations owner, or other named authority.
- **Estimated fix cost**: Tiny, Small, Medium, Large, or Architectural.
- **Disposition**: Open, Accepted, Fixed, Risk Accepted, Deferred, or Not Applicable.

Estimated fix cost informs prioritization but does not reduce severity. A tiny critical fix remains critical. An architectural advisory may be expensive and still non-blocking.

## Coverage statement

Every review report must state:

- Commit, diff, or artifact version reviewed.
- Files, modules, and artifacts inspected.
- Dimensions reviewed in depth.
- Areas intentionally excluded or only sampled.
- Tests or commands independently run.
- Missing context or inaccessible environments.
- Specialist review still required.

If the reviewer is not qualified for a material surface such as security, privacy, concurrency, accessibility, internationalization, regulated data, or infrastructure, it must say so and route the surface to an appropriate reviewer.

## Strengths

A review may include zero to three specific strengths. Each strength must explain why the choice improves code health, correctness, testability, simplicity, or operational safety.

Good:

> The change reuses the existing persistence boundary instead of creating a second abstraction, preserving one ownership model and reducing long-term maintenance.

Bad:

> Good use of interfaces.

Strengths are evidence of understanding, not mandatory praise.

## Verdicts

The verdict is derived after findings and coverage:

- **READY:** No blocking findings remain, required review coverage is complete, and the change definitely improves overall code health.
- **READY_WITH_ADVISORIES:** No blocking findings remain; explicit non-blocking recommendations or follow-up work exist.
- **NOT_READY:** One or more blocking findings remain.
- **INCOMPLETE_REVIEW:** Required context, qualification, environment, evidence, or review surface is missing, so merge-readiness cannot be established.

A reviewer must not issue `READY` when the coverage statement identifies an unreviewed mandatory surface.

## Reviewer behavior

Review is read-only by default. The reviewer may attach an **unapplied suggested diff** only when the correction is mechanical, unambiguous, and does not alter logic, control flow, public interfaces, data meaning, or architecture.

Examples that may qualify:

- A misspelled identifier with a single obvious correction.
- A missing guard whose required behavior is explicitly established and mechanically local.
- Moving an exposed constant or secret reference to the repository's existing configuration mechanism without changing behavior.

Anything involving logic, control flow, interfaces, persistence, permissions, or architecture requires explicit handoff to a separate remediation invocation and separate commit. The remediation pass must be independently reviewable.

## Review flow

1. Confirm review scope, exact commit, approved brief, plan, decisions, and required specialist coverage.
2. Take a broad view: should this change exist, and does it match approved intent?
3. Inspect the highest-risk and most architecturally significant surfaces first.
4. Review every assigned human-written line with appropriate depth and surrounding context.
5. Validate tests and evidence rather than trusting status labels.
6. Record findings using the required schema.
7. Route plan defects and advisory architecture concerns separately.
8. State coverage, strengths, unresolved specialist needs, and derived verdict.

## Anti-patterns

- Producing one finding per category regardless of evidence.
- Summarizing the diff instead of challenging it.
- Marking style preferences as blocking.
- Treating automated checks as the entire review.
- Assigning severity based on annoyance or ease of fix.
- Reporting high-confidence defects without evidence.
- Hiding unreviewed files or missing expertise.
- Expanding a feature through review comments.
- Fixing implementation logic during the independent review pass.
- Approving an outdated commit after unreviewed changes.

## Source basis

- [Google Engineering Practices: The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)
- [Google Engineering Practices: What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Google Engineering Practices: How to write code review comments](https://google.github.io/eng-practices/review/reviewer/comments.html)
- [Google Engineering Practices: Navigating a CL in review](https://google.github.io/eng-practices/review/reviewer/navigate.html)
- [Google Engineering Practices: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [AWS Prescriptive Guidance: Architectural decision records](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
