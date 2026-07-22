# Agent instruction architecture

## Decision

Use one canonical, portable instruction system:

1. Root `AGENTS.md` contains universal authority, safety, lifecycle, and completion rules.
2. `agent-context.yml` routes task-specific standards only when applicable.
3. Nested `AGENTS.md` files define local commands, architecture boundaries, and verification for genuinely distinct subsystems.
4. Tool-specific files such as `CLAUDE.md` remain thin adapters and must not duplicate the canonical rules.
5. Deterministic tooling enforces formatting, lint, types, tests, schemas, and policy wherever possible.

## Instruction categories

Every normative rule should be identifiable as one of these categories:

- `ENFORCED`: A machine control prevents or rejects violations, such as CI, permissions, schemas, or branch protection.
- `VERIFIABLE`: An agent or reviewer can run a deterministic command and inspect the result.
- `REVIEWED`: A qualified human or independent reviewer must assess the result.
- `ADVISORY`: Guidance that cannot be reliably enforced and should not be represented as a hard guarantee.

Prefer `ENFORCED` over `VERIFIABLE`, `VERIFIABLE` over `REVIEWED`, and `REVIEWED` over `ADVISORY` when the control can reasonably be automated.

## Root instruction budget

The root contract should normally remain below:

- 250 lines.
- 4,000 approximate tokens.
- One copy of each universal rule.

A larger root file requires a documented reason. Move stack, subsystem, UX, security, operations, and workflow detail into routed sources instead of expanding the root contract.

## When to create nested instructions

Create a nested `AGENTS.md` only when a directory has at least one material difference in:

- Build, test, lint, or verification commands.
- Architecture or dependency boundaries.
- Data or security constraints.
- Framework conventions.
- Deployment or operational ownership.

Do not create nested files merely because a directory exists. Do not repeat root requirements. State only the delta.

The nearest nested file governs its subtree. Agents must still obey every non-overridable root control.

## Thin adapters

Tool-specific entry files should:

- Point to `AGENTS.md`, `agent-context.yml`, and `agent-policy.yml`.
- Explain only tool-specific loading behavior or limitations.
- Avoid copied policy prose.
- Remain mechanically comparable to detect drift.

## Specialist agents

Keep a small role set with distinct evidence contracts:

- Discovery: read-only repository and dependency evidence.
- Planner: requirements mapping, risk, sequencing, and verification design.
- Implementer: authorized code changes within explicit ownership.
- Reviewer: independent diff and evidence assessment.
- Security reviewer: specialist trust-boundary and abuse-case assessment.

Do not create persona-only agents that have the same permissions, inputs, outputs, and acceptance criteria under different titles.

## Multi-agent execution

Parallel execution is permitted only when agents have explicit, non-overlapping ownership. Each assignment must define:

- Owned paths or artifacts.
- Inputs and approved decisions.
- Expected output and evidence.
- Prohibited changes.
- Integration owner.

Parallel agents must not independently alter shared contracts or overlapping files. Shared-interface changes are serialized through the integration owner.

## Context quality checks

Standards validation should detect or warn on:

- Oversized root instructions.
- Duplicated policy across adapters and nested files.
- Broken referenced paths.
- Commands that do not exist.
- References to unselected stack profiles.
- Nested rules that weaken or conflict with root controls.
- Prose rules already enforced by deterministic tooling.
- Stale instructions whose commands or paths no longer match the repository.

## Evaluation

Compare instruction strategies using representative repository tasks. Measure outcomes, not whether the model repeats the rules:

- Task success and regression rate.
- Unnecessary files changed.
- Tests or controls weakened.
- Human corrections required.
- Policy violations.
- Tokens and elapsed execution time.
- Unnecessary clarification count.

The recommended experiment compares no custom instructions, minimal root instructions, the full standards set, and minimal root plus routed task context.
