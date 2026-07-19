# Project maturity model

Use the lowest level that matches the project today. Add controls as the cost of failure and number of contributors increase.

## Level 0: disposable

Good for:

- One-time scripts.
- Learning experiments.
- Short-lived proofs of concept.

Expected controls:

- Basic version control when useful.
- No requirement to adopt this full template.

## Level 1: maintained personal project

Good for:

- A project one person expects to revisit.
- A personal application with real users or data.

Expected controls:

- Root agent instructions.
- Stable verification command.
- Branches and pull requests.
- Basic dependency and secret scanning.
- Lightweight documentation.

## Level 2: professional solo project

Good for:

- Revenue-impacting or portfolio-quality software.
- A solo-maintained production application.

Add:

- Feature briefs and plans for meaningful work.
- Automated CI and releases.
- Rollback and observability guidance.
- Architecture and contract documentation.
- Repository rulesets and protected environments.

## Level 3: small team

Good for:

- Multiple regular contributors.
- Shared production responsibility.

Add:

- Required approval.
- CODEOWNER review for sensitive paths.
- Clear ownership and on-call expectations.
- Incident reviews and migration runbooks.
- Team-visible exceptions with expiration.

## Level 4: regulated or enterprise

Good for:

- High financial, safety, privacy, or compliance impact.
- Large teams and complex production environments.

Add organizationally appropriate controls such as:

- Separation of duties.
- Formal change and evidence retention.
- Central identity, audit, policy, and artifact controls.
- Required security and privacy reviews.
- Disaster-recovery exercises.
- Compliance-specific approvals and records.

## Important

The maturity level changes the strength of controls, not the underlying principles. Even a Level 1 project should avoid silent assumptions, weakened tests, unsupported completion claims, and unreviewed high-risk changes.