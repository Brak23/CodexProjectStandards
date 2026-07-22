# Engineering principles

These principles define the engineering values shared by repository standards, skills, plans, implementation workflows, and reviews. They are intentionally broader than any single tool, model, language, framework, or deployment environment.

## Purpose

Engineering exists to produce and sustain valuable outcomes for users and the organization. Code is one means of doing that. Delivery speed, design quality, reliability, security, operability, cost, accessibility, and maintainability are system qualities that must be balanced against the actual mission and risk of the change.

The repository optimizes for **continuous improvement under explicit evidence and bounded risk**, not theoretical perfection and not unchecked velocity.

## Authority hierarchy

When legitimate concerns conflict, reason in this order:

1. Applicable law, regulation, organizational policy, and platform security controls.
2. Approved product intent and real user or mission outcomes.
3. Correctness, security, privacy, safety, and preservation of critical data.
4. Reliability, recoverability, operability, and compatibility.
5. Structural code health and long-term maintainability.
6. Local readability, testability, and consistency.
7. Enforced repository conventions.
8. Personal preference.

This hierarchy does not mean lower items are unimportant. It means a preference cannot overrule evidence, a convention cannot justify a defect, and delivery pressure cannot silently authorize unacceptable risk.

## Core principles

### 1. Optimize for outcomes, not activity

Working software and observable customer or mission outcomes are stronger evidence of progress than plans, tickets, generated code, or agent activity.

Every meaningful change must identify:

- Who or what benefits.
- What behavior or outcome changes.
- How success will be observed.
- Which harms, regressions, and non-goals must be avoided.

A technically elegant change that does not support approved intent is not successful engineering.

### 2. Improve code health continuously

Each accepted change should leave the system healthier overall, considering design, correctness, understandability, testability, security, reliability, and operational burden.

Perfection is not the standard. A change may be approved when it definitely improves the system even though non-blocking improvements remain. Conversely, a sequence of individually small degradations is still unacceptable because systems usually decay incrementally.

Technical debt is a deliberate, owned tradeoff with scope, consequence, and remediation intent. It is not an unnamed residue of schedule pressure.

### 3. Prefer facts and reproducible evidence over opinion

Technical claims should be grounded in one or more of:

- Executed tests or observed behavior.
- Source code, schemas, contracts, types, or generated artifacts.
- Production or production-like telemetry.
- Benchmarks with documented methodology.
- Approved requirements and architecture decisions.
- Official versioned documentation.
- Reproducible analysis.

Confidence must reflect the strength of the evidence. An authoritative tone is not evidence.

### 4. Make the smallest coherent change

Changes should be small enough to understand, verify, review, deploy, and reverse, while remaining coherent and useful.

A coherent change:

- Addresses one primary outcome.
- Includes the tests and documentation needed to prove it.
- Leaves the repository and deployable system in a valid state.
- Avoids unrelated cleanup and speculative generalization.
- Can be rolled back without untangling unrelated behavior.

Line count is only a proxy. A focused 300-line change may be safer than a 50-line change scattered across unrelated trust boundaries.

### 5. Separate intent, decisions, execution, and evidence

These are different contracts:

- **Intent** states the problem, outcome, constraints, acceptance criteria, and non-goals.
- **Decisions** record consequential choices, alternatives, rationale, tradeoffs, confidence, and status.
- **Execution** describes the bounded implementation approach and ownership.
- **Evidence** records what was observed and which claims were verified.

Combining them makes it difficult to tell whether a defect came from misunderstood intent, a bad decision, incorrect execution, or inadequate verification.

### 6. Simplicity means avoiding unnecessary work and structure

Prefer the simplest design that satisfies current approved requirements and quality attributes.

Do not add abstractions, configuration, extension points, services, dependencies, or generic machinery for hypothetical future needs. Over-engineering increases the number of states, contracts, failure modes, and maintenance obligations the system must carry.

Simplicity does not mean ignoring known scale, security, reliability, or compatibility requirements. Those are current requirements when evidence establishes them.

### 7. Treat quality attributes as explicit requirements

Correctness alone does not make a system production-ready. Applicable quality attributes must be named and verified, including:

- Security and privacy.
- Reliability and graceful degradation.
- Recoverability and rollback.
- Operability and observability.
- Performance and capacity.
- Cost and resource efficiency.
- Accessibility and usability.
- Compatibility and evolvability.
- Sustainability when material.

The appropriate emphasis depends on user impact, reversibility, exposure, data sensitivity, and operational consequence.

### 8. Build security and operations into the design

Security, privacy, deployment, monitoring, support, and recovery are not final checklists added after implementation. They influence architecture, interfaces, data handling, permissions, and release strategy from the beginning.

A feature is incomplete when it works only in the ideal path but cannot be diagnosed, operated, disabled, recovered, or secured in its real environment.

### 9. Automate deterministic policy

Requirements that can be enforced mechanically should be implemented through compilers, type systems, linters, formatters, tests, schemas, scanners, branch protections, permission boundaries, or CI.

Do not spend scarce human or model attention repeatedly reviewing deterministic style and policy issues that tooling can reject consistently.

Prose remains necessary for judgment, context, exceptions, and responsibilities that cannot be fully automated.

### 10. Preserve independent challenge

The author or implementing agent is responsible for self-checking, but self-checking is not independent review.

Review strength increases with risk. Reviewers must be able to challenge the implementation, approved plan, evidence, and assumptions without becoming the untracked author of the same change.

An independent reviewer may identify a plan defect or architectural concern. Authority to identify an issue does not automatically grant permission to redesign or edit the implementation.

### 11. Design for reversibility and learning

Prefer decisions and releases that preserve options, limit blast radius, and produce feedback.

- Use small batches and progressive exposure where applicable.
- Define rollback or roll-forward behavior before release.
- Instrument meaningful outcomes and failure modes.
- Record decisions and supersede them explicitly when evidence changes.
- Analyze consequential failures for root causes and recurrence prevention.

A failed experiment with bounded impact and useful evidence can be successful engineering. An unobservable success claim cannot.

### 12. Humans retain consequential authority

Agents and automation may discover, propose, implement, test, and review. Authenticated humans or designated organizational authorities retain approval for:

- Product intent and material scope.
- Architecture or security tradeoffs with significant consequence.
- Standards exceptions.
- Irreversible or destructive operations.
- Merge and production release where policy requires it.
- Acceptance of residual high risk.

An artifact can record approval but cannot create approval by itself.

## Enforcement model

Each repository requirement should be classified as one of:

- **ENFORCED:** A technical control prevents or rejects noncompliance.
- **VERIFIABLE:** A command or observable check can establish compliance.
- **REVIEWED:** Qualified judgment is required and must be recorded.
- **ADVISORY:** Guidance informs decisions but does not independently block work.

Do not describe a reviewed or advisory expectation as guaranteed enforcement.

## Conflict resolution

When two valid principles conflict:

1. State the conflict and affected outcomes.
2. Gather the strongest available evidence.
3. Identify the authority that owns the decision.
4. Compare consequence, reversibility, blast radius, and uncertainty.
5. Prefer the smallest reversible option that preserves required outcomes.
6. Record the decision, rationale, confidence, and consequences.
7. Define what evidence would cause reconsideration.

Do not resolve technical disagreements through status, verbosity, or model confidence.

## Anti-patterns

- Optimizing ticket completion while degrading user outcomes or code health.
- Treating passing tests as proof when the tests do not cover the claim.
- Using broad architecture language without identifying concrete requirements.
- Adding future-proof abstractions without a current supported use case.
- Encoding enforceable rules only in prose.
- Treating security, operations, accessibility, or documentation as downstream cleanup.
- Allowing the same actor to define intent, implement, approve, and release consequential work without independent checks.
- Hiding uncertainty to maintain momentum.

## Source basis

These principles synthesize established public guidance rather than copy one organization's process:

- [Google Engineering Practices: The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)
- [Google Engineering Practices: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- [Principles behind the Agile Manifesto](https://agilemanifesto.org/principles.html)
- [DORA: Working in small batches](https://dora.dev/capabilities/working-in-small-batches/)
- [DORA: Continuous delivery](https://dora.dev/capabilities/continuous-delivery/)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html)
- [AWS Prescriptive Guidance: Architectural decision records](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/introduction.html)
- [Microsoft Azure Well-Architected: Architecture decision records](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
