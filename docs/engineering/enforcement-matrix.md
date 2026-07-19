# Engineering enforcement matrix

Written policy is not the same as enforced control. Every project should maintain this matrix and update it when tooling, agent permissions, or GitHub settings change.

| Control | Enforcement | Default owner | Evidence |
| --- | --- | --- | --- |
| Required repository structure and local links | Enforced by CI through `scripts/validate_repository.py` | Engineering | Required validation check |
| Agent context, policy, adapters, state template, and evaluation contracts | Enforced by CI through `scripts/validate_agent_governance.py` | AI platform or engineering | `task verify` output |
| Live model behavior against evaluation scenarios | Manually reviewed or project-specific automated harness | AI platform owner | Model/version/tool-config evaluation report |
| Authoritative verification command | Enforced locally and by CI through `scripts/verify_project.py` | Engineering | `task verify` output |
| Full-SHA GitHub Action pinning | Enforced by CI validator | Platform or repository owner | Required validation check |
| Feature phase, approval, ownership, and reviewed commit state | Manually reviewed; machine-readable in `state.yml` | Feature owner | Work state and approval record |
| Tool and environment permission compliance | Agent runtime where supported plus manual review | AI platform and environment owner | Tool logs, approvals, and verification evidence |
| Context routing and refresh | Agent runtime behavior plus review | Implementer and reviewer | Context manifest and work evidence |
| Pull requests before merge | Enforced by GitHub settings | Repository administrator | Ruleset configuration |
| Required approvals | Enforced by GitHub settings in team mode | Repository administrator | Ruleset configuration |
| CODEOWNER review for sensitive paths | Enforced by GitHub settings and CODEOWNERS | Security or platform owner | Review record |
| Secret scanning and push protection | Enforced by GitHub settings | Security | Security settings |
| Dependency review | Enforced by workflow and required check when configured | Engineering | Workflow result |
| Code scanning | Enforced by CodeQL workflow and required check when configured | Security | Code scanning result |
| Acceptance-criteria evidence | PR template and human review | Product and reviewer | PR body and verification document |
| Architecture compliance | Tests where possible, otherwise review | Technical owner | Architecture tests or review |
| Independent review level | Manually reviewed and recorded in `state.yml` | Feature owner | Reviewer, level, findings, and reviewed commit |
| Production approval | Enforced by protected environment | Release owner | Deployment approval record |
| Rollback readiness | Plan and release review | Service owner | Runbook and release evidence |
| Standards exceptions | Exception record and human approval | Named approver | Exception document or issue |

## Status vocabulary

Use one of:

- **Enforced by CI**
- **Enforced by GitHub settings**
- **Enforced by agent runtime**
- **Manually reviewed**
- **Recommended only**
- **Not applicable**

Do not claim a control or model behavior is enforced unless the repository can point to the mechanism and evidence. A structurally valid evaluation suite does not prove that a model passed it.
