# Workflow decision tree

Use this page when you are unsure how much process a change needs.

```text
Are you creating a maintained repository?
├─ No → A throwaway script or experiment probably does not need this template.
└─ Yes → Adopt the template once for the whole repository.
          │
          What are you changing?
          │
          ├─ Typo, docs, tiny UI fix, or contained low-risk bug
          │  └─ LIGHT WORKFLOW
          │     Understand → smallest change → relevant tests → task verify → PR
          │
          ├─ New feature, API, integration, dependency, or multi-module change
          │  └─ FULL FEATURE WORKFLOW
          │     Brief → discovery → plan → implement → review → verify → PR
          │
          └─ Auth, payments, sensitive data, migration, infrastructure,
             secrets, or breaking public contract
             └─ HIGH-RISK WORKFLOW
                Full workflow + threat model/migration/rollback/security review
```

## Light workflow

Use when the behavior is already understood, the change is localized, and failure has a small blast radius.

Required:

1. Confirm current behavior.
2. Make the smallest coherent change.
3. Run focused tests and `task verify`.
4. Open a pull request with actual evidence.

A feature workspace or ExecPlan is normally unnecessary.

## Full feature workflow

Use when the change introduces meaningful behavior, spans boundaries, or is likely to require tradeoffs.

Required:

1. Create a feature workspace.
2. Approve the brief.
3. Perform read-only discovery.
4. Approve the plan.
5. Implement on a branch.
6. Conduct independent review.
7. Record verification evidence.
8. Human-control merge and release.

## High-risk workflow

Use the full feature workflow and add the applicable specialist controls:

- Threat model.
- Data migration and reconciliation plan.
- Rollback or disablement plan.
- Security review.
- Staged rollout and monitoring thresholds.
- Explicit human approval for consequential decisions.

## Fast command

Run:

```bash
task recommend
```

The interactive helper asks a few questions and recommends a workflow.
