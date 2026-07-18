# Testing strategy

## Test portfolio

- Unit tests protect domain rules, calculations, transformations, and edge conditions.
- Integration tests verify databases, queues, caches, frameworks, and provider adapters.
- Contract tests verify API, event, and schema compatibility.
- Component tests verify user interaction and state transitions.
- End-to-end tests protect only critical user journeys and production smoke paths.
- Security tests cover authorization, tenant isolation, abuse cases, and input boundaries.
- Nonfunctional tests cover accessibility, performance, load, resilience, and recovery.

## Rules

- Test observable behavior, not implementation trivia.
- Avoid excessive mocking. Use real boundaries for critical integration behavior.
- Existing acceptance tests are protected surfaces.
- Never delete, skip, weaken, or broaden mocks solely to make implementation pass.
- A flaky test is a defect.
- Coverage is a signal, not the definition of correctness.

## Default thresholds

Projects should set risk-appropriate thresholds. Initial defaults:

- Changed-line coverage at least 80 percent.
- Critical domain branch coverage at least 90 percent.
- Overall coverage may not decrease without justification.
- PR validation target under 10 minutes.
- Flaky test rate under 1 percent.

## Evidence

Record exact commands, counts, failures, skips, environment, and commit. Independent or held-out scenarios should verify composed behavior for consequential changes.
