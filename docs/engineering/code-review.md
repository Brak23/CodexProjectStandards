# Code review standard

This document defines the operational procedure for independent code review. The governing principles are in [`../philosophy/02-review-philosophy.md`](../philosophy/02-review-philosophy.md).

## Mission

Determine whether the exact reviewed change improves overall code health and is merge-ready under approved intent, repository standards, required evidence, and applicable specialist review.

Merge-readiness is the derived verdict. Do not decide the verdict before completing findings and coverage.

## Preconditions

Before reviewing, obtain:

- Exact commit SHA and base comparison.
- Approved `brief.md` and acceptance criteria.
- Approved `plan.md` and recorded amendments.
- Applicable ADRs or `decisions.md`.
- Final diff and affected repository context.
- Verification evidence and exact commands run.
- Required review level and specialist surfaces.
- Applicable root and nested `AGENTS.md` files.

Return `INCOMPLETE_REVIEW` when required context or qualification is unavailable.

## Reviewer independence

- Reviewer agents are read-only by default.
- Author self-check is not independent review.
- Review the artifacts and evidence directly rather than relying on the implementer's summary.
- Record the exact reviewed commit.
- Any later unreviewed changes invalidate the verdict for those changes.
- Logic, control flow, interface, data, permission, and architecture fixes require a separate remediation invocation and separate commit.

An unapplied suggested diff is allowed only for a mechanical and unambiguous correction that does not change logic, control flow, interfaces, data meaning, permissions, or architecture.

## Review sequence

### 1. Establish scope and authority

Confirm:

- What outcome the change is approved to produce.
- What is explicitly out of scope.
- Which paths and modules are included.
- Which standards and decisions govern the change.
- Which review surfaces require specialists.

### 2. Take the broad view

Before line-level inspection, determine:

- Should this change exist under approved intent?
- Is it located in the correct system and modules?
- Does its overall design integrate with the existing architecture?
- Is the change a coherent and appropriately sized unit?
- Does it add behavior or machinery beyond the plan?

### 3. Inspect high-risk surfaces first

Prioritize applicable:

- Authentication and authorization.
- Tenant, user, or data boundaries.
- Destructive operations and migrations.
- Public contracts and compatibility.
- Concurrency, idempotency, retries, and partial failure.
- Secrets, dependencies, and external execution.
- Deployment, rollback, and production access.

### 4. Inspect every assigned human-written line

Review with surrounding file, module, contract, and call-path context. Do not assume unchanged nearby code remains valid when the new interaction changes its meaning.

Generated or large data artifacts may be sampled when appropriate, but sampling must be declared in coverage.

### 5. Challenge verification

Determine:

- Which acceptance criteria each test or command proves.
- Whether negative and edge cases are covered.
- Whether mocks hide required integration behavior.
- Whether tests, thresholds, scanners, or controls were weakened.
- Whether the tested environment and commit match the reviewed change.
- Whether migration, rollback, accessibility, performance, security, or production-like evidence is required.

Passing status is not sufficient when the evidence does not establish the claim.

### 6. Record findings

Use the required finding format below. Do not create findings solely to populate a category.

### 7. Route design and plan issues correctly

- Blocking implementation findings must trace to concrete authority or evidence.
- Advisory architecture concerns should become follow-up work or a proposed ADR when they do not block current authority.
- A defect in an approved plan must be recorded separately against the plan or decision artifact.

### 8. State coverage and verdict

Complete the coverage statement before deriving the verdict.

## Review dimensions

Silently inspect applicable dimensions:

- Product and requirement alignment.
- Correctness and edge cases.
- Security and privacy.
- Architecture and dependency direction.
- Structural and local maintainability.
- Reliability, concurrency, and failure behavior.
- Data integrity and migration.
- Operability, observability, support, and rollback.
- Performance, capacity, and cost.
- Accessibility, usability, and content.
- Tests and verification.
- Documentation and compatibility.
- Scope excess and speculative complexity.

Do not manufacture a finding for every dimension.

## Priority

When concerns compete, prioritize by consequence:

1. Correctness, security, privacy, safety, and critical data integrity.
2. Structural maintainability and architecture with material future consequence.
3. Reliability, operability, compatibility, performance, and migration risk.
4. Local maintainability, readability, and test quality.
5. Named conventions not already enforced automatically.
6. Nits and preference.

Severity, not category, determines blocking consequence.

## Finding authority

### Blocking

A blocking finding must trace to one or more of:

- Definite or strongly evidenced defect.
- Security, privacy, safety, or data-integrity issue.
- Missing, incorrect, or extra work relative to the approved brief or plan.
- Violation of a named standard, policy, ADR, schema, or contract.
- Missing evidence required for a consequential claim.

### Advisory

Architecture, simplification, refactoring, education, or alternative valid designs may be advisory when current approved authority does not require them.

Advisories do not block. Record useful follow-up work without expanding the current change.

## Plan deviations

Classify scope mismatch as:

- **Missing work**: Approved behavior, evidence, documentation, controls, or operations were omitted.
- **Incorrect work**: Implementation does not satisfy the approved contract.
- **Extra work**: Unapproved behavior, dependency, abstraction, configuration, interface, or generic machinery was added.

Over-engineering is extra work when it increases system complexity without a current approved requirement.

## Severity

- **Critical**: Catastrophic, broadly irreversible, or readily exploitable compromise, sensitive-data loss, data corruption, safety failure, or equivalent consequence.
- **High**: Definite serious production, security, contract, migration, authorization, tenant, concurrency, or recovery failure.
- **Medium**: Material but bounded defect risk, structural degradation, operational burden, incomplete important evidence, or predictable future change cost.
- **Low**: Localized limited-consequence readability, documentation, consistency, testing, or maintainability improvement.
- **Nit**: Optional polish or personal preference. Nits never block.

Severity measures impact, not urgency or estimated fix cost.

## Confidence

- **High**: Directly established by inspected code, contract, test, reproducible behavior, or authoritative documentation.
- **Medium**: Strongly suggested, but one material runtime, environmental, or architectural fact remains unverified.
- **Low**: Plausible suspicion requiring targeted verification.

Low-confidence findings must be written as hypotheses. Severity and confidence remain separate.

## Required finding format

```markdown
### [FINDING-ID] Concise title

- Severity: Critical | High | Medium | Low | Nit
- Categories: correctness, security, architecture, maintainability, reliability, data, operations, performance, accessibility, testing, documentation, scope
- Confidence: High | Medium | Low
- Location: path:line or affected artifact
- Authority: requirement, plan, standard, ADR, contract, policy, or Advisory
- Resolution owner: implementer | product | architecture | security | operations | other
- Estimated fix cost: Tiny | Small | Medium | Large | Architectural
- Disposition: Open | Fixed | Accepted | Risk Accepted | Deferred | Not Applicable

**Finding**
What is wrong or uncertain.

**Evidence**
What establishes the claim.

**Impact**
Why it matters and under which conditions.

**Remediation**
Required for Critical and High findings. Keep it concrete without taking over implementation design unnecessarily.
```

## Plan issue format

```markdown
### [PLAN-ID] Concise plan concern

- Plan location:
- Confidence:
- Decision owner:
- Current implementation faithful to approved plan: Yes | No | Unclear

**Evidence**

**Consequence**

**Required decision or amendment**
```

Do not use a plan issue to avoid reporting an implementation deviation.

## Coverage statement

Every report must include:

```markdown
## Coverage

- Reviewed commit:
- Base comparison:
- Files and modules inspected:
- Artifacts inspected:
- Dimensions reviewed in depth:
- Commands independently run:
- Sampled or excluded areas:
- Missing context or inaccessible environments:
- Specialist review still required:
```

Explicitly identify incomplete review of privacy, security, concurrency, accessibility, internationalization, regulated data, infrastructure, or other specialist surfaces.

## Strengths

Include zero to three strengths. Each must explain why the implementation improves code health or risk posture.

Do not include generic praise.

## Verdict

Return one:

- `READY`: No blocking findings remain, required coverage is complete, and the change definitely improves overall code health.
- `READY_WITH_ADVISORIES`: No blocking findings remain; explicit non-blocking recommendations or follow-up work exist.
- `NOT_READY`: One or more blocking findings remain.
- `INCOMPLETE_REVIEW`: Required context, evidence, environment, or qualified review is missing.

The verdict must follow findings and coverage, not precede them.

## Output order

1. Verdict and one-sentence rationale.
2. Blocking findings ordered by severity.
3. Advisory findings ordered by expected value.
4. Plan issues.
5. Coverage statement.
6. Strengths.
7. Required specialist or human decisions.

Omit empty finding sections. Never emit placeholder findings.

## Review completion checks

Before finishing:

- Every blocking finding has concrete evidence and authority.
- Critical and High findings include remediation and owner.
- Severity reflects consequence rather than ease of fix.
- Confidence accurately reflects missing facts.
- Extra scope and speculative abstraction were checked.
- No automated style issue was duplicated without additional consequence.
- Plan defects are routed separately.
- Coverage honestly identifies exclusions and qualification limits.
- The reviewed commit matches the report.
- The verdict follows logically from unresolved findings and coverage.
