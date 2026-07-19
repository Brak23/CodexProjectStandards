# Testing strategy

## Test portfolio

- Unit tests protect domain rules, calculations, transformations, and edge conditions.
- Integration tests verify databases, queues, caches, frameworks, and provider adapters.
- Contract tests verify API, event, and schema compatibility.
- Component tests verify user interaction, state transitions, keyboard behavior, focus behavior, and accessible output.
- End-to-end tests protect only critical user journeys and production smoke paths.
- Security tests cover authorization, tenant isolation, abuse cases, and input boundaries.
- Nonfunctional tests cover accessibility, performance, load, resilience, recovery, responsive behavior, and visual stability.

## UI verification portfolio

For user-facing changes, combine the applicable layers:

- Component behavior tests for interaction states and user-observable output.
- Automated accessibility checks.
- Manual keyboard, focus, zoom, reduced-motion, and critical screen-reader checks.
- Responsive verification using realistic content at relevant narrow and wide layouts.
- Visual-regression tests for shared components and high-value screens when supported.
- End-to-end tests for critical completion and recovery journeys.
- Content review in the implemented interface.
- Usability evaluation or production-success measures when user confusion has material cost.

Screenshots alone do not establish functional or accessible correctness. Automated accessibility scans alone do not establish WCAG conformance. Visual snapshots must be reviewed rather than blindly updated.

## Rules

- Test observable behavior, not implementation trivia.
- Avoid excessive mocking. Use real boundaries for critical integration behavior.
- Existing acceptance tests and approved visual baselines are protected surfaces.
- Never delete, skip, weaken, broadly update snapshots, or broaden mocks solely to make implementation pass.
- A flaky test is a defect.
- Coverage is a signal, not the definition of correctness.
- Test non-ideal UI states, not only the happy path.
- Use realistic long, empty, invalid, delayed, and permission-limited data.

## Default thresholds

Projects should set risk-appropriate thresholds. Initial defaults:

- Changed-line coverage at least 80 percent.
- Critical domain branch coverage at least 90 percent.
- Overall coverage may not decrease without justification.
- PR validation target under 10 minutes.
- Flaky test rate under 1 percent.
- No unresolved critical accessibility defect in a changed critical journey.

## Evidence

Record exact commands, counts, failures, skips, environment, browser and device coverage, commit, and artifact locations. Independent or held-out scenarios should verify composed behavior for consequential changes.

For significant UI work, use `docs/work/_template/ui-verification.md` and `docs/design/ui-review-checklist.md`.
