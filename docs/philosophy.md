# Engineering philosophy

These documents define the shared engineering worldview used by repository standards, project-local skills, plans, implementation workflows, and reviews.

They are authoritative for interpretation but are loaded conditionally through `agent-context.yml` so routine tasks do not carry the entire philosophy into context.

## Canonical doctrines

1. [`philosophy/01-engineering-principles.md`](philosophy/01-engineering-principles.md)  
   Outcome hierarchy, code health, evidence, small changes, quality attributes, decision authority, and enforcement model.

2. [`philosophy/02-review-philosophy.md`](philosophy/02-review-philosophy.md)  
   Independent review mission, blocking and advisory authority, severity, confidence, evidence, coverage, findings, and merge-readiness verdicts.

3. [`philosophy/03-planning-philosophy.md`](philosophy/03-planning-philosophy.md)  
   Intent, decision, execution, and evidence contracts; discovery; decomposition; change budgets; amendments; and plan-defect handling.

4. [`philosophy/04-security-philosophy.md`](philosophy/04-security-philosophy.md)  
   Secure-by-design lifecycle, threat modeling, least privilege, safe defaults, supply-chain controls, realistic validation, and residual-risk ownership.

5. [`philosophy/05-agent-behavior.md`](philosophy/05-agent-behavior.md)  
   Agent authority, permissions, context routing, untrusted-content handling, uncertainty, scope discipline, specialist behavior, and independent review.

## Interpretation rules

- The doctrines define principles and decision logic. Operational standards and skills define the procedure for a specific task.
- A skill may specialize a doctrine but may not silently contradict or weaken it.
- Technically enforced policy outranks advisory prose.
- Approved product intent and accepted decisions govern the current change within legal, security, and organizational constraints.
- When principles conflict, record the conflict, evidence, decision owner, consequence, and rationale.
- These documents do not grant approvals, permissions, exceptions, or production authority.

## Source policy

The doctrines synthesize public primary guidance from Google Engineering Practices, DORA, NIST, CISA, Microsoft, AWS, the Agile Manifesto, and OpenAI. Each document lists its source basis. Repository requirements remain the project's own derived standards rather than claims that any source organization uses this exact combined process.
