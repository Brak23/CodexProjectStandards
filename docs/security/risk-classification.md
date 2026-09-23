# Change risk classification

Risk determines verification and review strength. Governance mode determines how that evidence is organized.

In **delegated** mode, routine low-risk work may use author self-check plus relevant verification. Meaningful moderate work requires a fresh-context independent review; if one cannot be obtained, the work is not ready for release unless the product owner records an explicit exception under the project's exception process. High and critical work requires the named specialist reviews below and may not treat a missing required reviewer as a mere limitation.

In **formal** mode, use the same risk expectations through the formal planning, review, and approval records.

## Low

Examples: documentation, isolated style correction, mechanical refactor with strong coverage.

Required: short plan, targeted verification, CI, PR review.

## Moderate

Examples: normal feature, API endpoint, cross-module behavior, new external integration without sensitive data.

Required: a delegated `work.md` record or formal feature plan, full relevant verification, independent fresh-context review, rollout, and rollback.

## High

Examples: authentication, authorization, tenant isolation, payments, regulated data, destructive migration, infrastructure IAM, breaking public contract.

Required in addition:

- ADR when architectural
- Threat model
- Security and abuse-case tests
- Explicit migration and recovery plan
- Separate security review
- Staged rollout and production approval
- Post-deployment monitoring

## Critical

A change with broad irreversible data, financial, security, or availability impact. It requires named executive or system-owner approval, rehearsed recovery, constrained change window, and direct operational supervision.
