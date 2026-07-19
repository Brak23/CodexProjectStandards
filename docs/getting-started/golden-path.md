# Golden path: from idea to release

This is the default end-to-end path for a maintained app using an AI coding agent.

## 1. Create the repository

Create a repository from this GitHub template and clone it.

```bash
mise install
task bootstrap
```

Review and commit the generated `project.yml`, README, CODEOWNERS, LICENSE, and workflows.

## 2. Verify the base repository

```bash
task doctor
task verify
```

Complete the manual GitHub settings in `docs/security/github-hardening.md` before production work.

## 3. Classify the change

```bash
task recommend
```

For a normal feature, continue with the full feature workflow.

## 4. Create the feature workspace

```bash
task feature FEATURE=APP-001 NAME=user-authentication
```

This creates:

```text
docs/work/APP-001-user-authentication/
├── brief.md
├── plan.md
├── decisions.md
└── verification.md
```

## 5. Define the outcome

Complete `brief.md` before implementation. Focus on observable behavior, users, permissions, failure states, non-goals, and acceptance criteria.

Ask the agent to challenge ambiguity rather than guessing.

## 6. Discover before designing

Have the agent inspect the repository without modifying files. It should map relevant modules, tests, contracts, ownership, authorization, dependencies, and comparable patterns.

## 7. Approve the plan

Have the agent create `plan.md` using `.agent/PLANS.md`. Review consequential architecture, security, data, dependency, rollout, and rollback decisions before coding starts.

## 8. Implement on a branch

Use an `agent/*` branch. The agent should update progress and decisions as it works, keep the repository coherent after each milestone, and stop when scope or risk changes.

## 9. Verify and review

```bash
task verify
```

Then perform a fresh-context adversarial review. Record exact commands, results, test counts, limitations, and rollout evidence in `verification.md`.

## 10. Open and merge the pull request

Open a draft PR first. Required checks and human review must pass before squash merge.

## 11. Release and observe

Use the documented rollout path. Verify production behavior, logs, metrics, and rollback readiness. A successful deployment command is not the same as verified production behavior.

## What success looks like

At the end, another engineer or agent can understand:

- What problem was solved.
- What changed and what deliberately did not.
- Why key decisions were made.
- How correctness was established.
- How the change is released, observed, and reversed.