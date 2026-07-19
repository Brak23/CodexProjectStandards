# Engineering enforcement matrix

Written policy is not the same as enforced control. Every project should maintain this matrix and update it when tooling or GitHub settings change.

| Control | Enforcement | Default owner | Evidence |
| --- | --- | --- | --- |
| Required repository structure and local links | CI through `scripts/validate_repository.py` | Engineering | Required validation check |
| Authoritative verification command | Local and CI through `scripts/verify_project.py` | Engineering | `task verify` output |
| Full-SHA GitHub Action pinning | CI validator | Platform or repository owner | Required validation check |
| Pull requests before merge | GitHub ruleset | Repository administrator | Ruleset configuration |
| Required approvals | GitHub ruleset in team mode | Repository administrator | Ruleset configuration |
| CODEOWNER review for sensitive paths | GitHub ruleset and CODEOWNERS | Security or platform owner | Review record |
| Secret scanning and push protection | GitHub repository setting | Security | Security settings |
| Dependency review | Optional workflow plus required check | Engineering | Workflow result |
| Code scanning | Optional CodeQL profile plus required check | Security | Code scanning result |
| Acceptance-criteria evidence | PR template and human review | Product and reviewer | PR body and verification document |
| Architecture compliance | Tests where possible, otherwise review | Technical owner | Architecture tests or review |
| Production approval | Protected environment | Release owner | Deployment approval record |
| Rollback readiness | Plan and release review | Service owner | Runbook and release evidence |
| Standards exceptions | Exception record and human approval | Named approver | Exception document or issue |

## Status vocabulary

Use one of:

- **Enforced by CI**
- **Enforced by GitHub settings**
- **Manually reviewed**
- **Recommended only**
- **Not applicable**

Do not claim a control is enforced unless the repository can point to the mechanism and evidence.
