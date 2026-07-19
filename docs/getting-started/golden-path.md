# Golden path: from idea to release

This is the default end-to-end path for a maintained app using an AI coding agent.

## 1. Create the repository

Create a repository from this GitHub template and clone it.

```bash
mise install
task bootstrap
```

Review and commit the generated `project.yml`, README, CODEOWNERS, LICENSE, and workflows. Review `agent-context.yml` and tighten `agent-policy.yml` when the project requires stricter permissions.

## 2. Verify the base repository

```bash
task doctor
task verify
task agent-evals
```

`task doctor` measures standards adoption. `task agent-evals` validates evaluation contracts but does not run a model.

Complete the manual GitHub settings in `docs/security/github-hardening.md` before production work.

## 3. Confirm the agent adapter

Confirm the agent runtime loads the repository contract:

- Codex: `AGENTS.md`
- Claude Code: `CLAUDE.md`
- Gemini CLI: `GEMINI.md`
- Cursor: `.cursor/rules/project-standards.mdc`
- Aider: `.aider.conf.yml`

## 4. Classify the change

```bash
task recommend
```

Treat the result as advisory and classify upward when discovery reveals greater impact, lower reversibility, new trust boundaries, public contracts, or material unknowns.

## 5. Create the feature workspace

```bash
task feature FEATURE=APP-001 NAME=user-authentication
```

This creates:

```text
docs/work/APP-001-user-authentication/
├── state.yml
├── brief.md
├── plan.md
├── ux-requirements.md
├── decisions.md
├── verification.md
└── ui-verification.md
```

## 6. Define the outcome

Complete `brief.md` before implementation. Focus on observable behavior, users, permissions, failure states, non-goals, acceptance criteria, and applicable UX/UI requirements.

Keep `state.yml` in the specification phase until an authenticated human approves the brief and authorizes planning.

## 7. Discover before designing

Have the agent load the applicable groups from `agent-context.yml` and inspect the repository without modifying files. It should map relevant modules, tests, contracts, ownership, authorization, dependencies, environments, design patterns, and comparable implementations.

## 8. Approve the plan

Have the agent create `plan.md` using `.agent/PLANS.md`. Review architecture, security, data, dependency, tool permissions, rollout, rollback, verification, and independent-review level before coding starts.

Set implementation authorization in `state.yml` only from authenticated human approval.

## 9. Implement on the recorded branch

Use the `agent/*` branch and ownership fields recorded in `state.yml`. The agent should update phase, milestones, progress, decisions, blockers, and ownership lease as it works.

When scope changes materially, follow the amendment process and obtain reapproval before continuing.

## 10. Verify and independently review

```bash
task verify
```

Apply the required level in `docs/engineering/review-independence.md`. Record exact commands, results, test counts, limitations, reviewer, review level, reviewed commit, and rollout evidence.

## 11. Open and merge the pull request

Open a draft PR first. Required checks and human review must pass before squash merge. An agent cannot set release authorization, merge its own work, or perform prohibited production actions.

## 12. Release and observe

Use the documented rollout path and `agent-policy.yml`. Verify production behavior, logs, metrics, user journeys, and rollback readiness. A successful deployment command is not the same as verified production behavior.

## Recovery and handoff

After interruption, context compaction, model change, or reassignment, follow `docs/engineering/session-recovery.md`. Multiple active agents must follow `docs/engineering/multi-agent-coordination.md`.

## What success looks like

At the end, another engineer or agent can understand:

- What problem was solved.
- What changed and what deliberately did not.
- Which approvals and tool permissions applied.
- Why key decisions were made.
- How correctness was established and independently reviewed.
- How the change is released, observed, and reversed.
