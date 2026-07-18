# Change risk classification

## Low

Examples: documentation, isolated style correction, mechanical refactor with strong coverage.

Required: short plan, targeted verification, CI, PR review.

## Moderate

Examples: normal feature, API endpoint, cross-module behavior, new external integration without sensitive data.

Required: feature brief, ExecPlan, full relevant verification, independent review, rollout and rollback.

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
