# Governance modes

The template separates collaboration mode from governance mode. **repository.mode** remains **solo** or **team** for GitHub ownership and review configuration. **options.governance_mode** selects how agents organize meaningful work.

## Delegated

**delegated** is the default for new projects. The product owner directs the outcome and accepts the product. AI owns ordinary engineering work: discovery, technical planning, implementation, tests, debugging, review, documentation, and authorized release execution.

A meaningful change uses one editable **docs/work/<id>-<slug>/work.md** record. It is working memory, not proof of approval. Technical steps can change as discovery improves. Ask the product owner only for unresolved consequential decisions, such as new recurring cost, altered data exposure, irreversible external effects, or production authorization outside an existing policy.

Delegated mode does not create formal planning approval roles or require separate intent, decision, plan, and implementation-authorization pull requests.

## Formal

**formal** retains the model-v2 planning records, immutable revisions, authority workflow, review ledger, and separate approval gates. Choose it when a project needs that evidence model because of organizational policy, many independent contributors, or materially regulated change control.

## Existing projects

Projects created before **options.governance_mode** existed resolve to **formal**. Add the setting deliberately after reviewing active workspaces and local GitHub requirements. Historical formal workspaces stay formal even after a project adopts delegated mode.

## Migration

1. Add **options.governance_mode: delegated** to **project.yml**.
2. Review local workflow requirements and branch protections before removing formal required checks. A formal-to-delegated transition is evaluated by the trusted base-branch authority workflow, so the PR cannot exempt itself by deleting that workflow.
3. Run bootstrap in a clean branch and inspect the generated-file diff.
4. Preserve existing formal workspaces; new delegated work uses **work.md**.
5. Add real application checks under **scripts/verify.d/** before claiming application verification.
