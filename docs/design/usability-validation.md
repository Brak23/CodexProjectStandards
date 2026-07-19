# Usability validation

Accessibility asks whether people can operate the interface. Usability asks whether they can understand it and complete the intended task effectively.

## Choose validation by risk

### Lightweight review

Use for localized or familiar patterns:

- Heuristic review.
- Dogfooding with realistic data.
- Review against comparable existing flows.
- Support and analytics review after release.

### Task-based validation

Use when a flow is new, consequential, unfamiliar, or difficult to reverse:

- Prototype or implemented-flow testing with representative users.
- Scenario-based testing without coaching.
- Observation of completion, errors, hesitation, workarounds, and comprehension.
- Follow-up questions focused on reasoning rather than preference alone.

### Production learning

For meaningful flows, define how production behavior will be evaluated:

- Completion and abandonment.
- Time to complete when relevant.
- Error and retry patterns.
- Repeated backtracking or help usage.
- Support contacts and qualitative feedback.
- Accessibility-related feedback.

Metrics must be interpreted with user context. A higher click rate is not automatically a better outcome.

## Heuristic review areas

Review:

- Match between the product and users' language.
- Visibility of system status.
- Clear hierarchy and primary action.
- Consistency with established patterns.
- Error prevention and recovery.
- Recognition rather than memory burden.
- User control and reversibility.
- Progressive disclosure of complexity.
- Help and explanation at the moment of need.

## Evidence and privacy

Record:

- Research question.
- Participant or data source characteristics without unnecessary personal data.
- Tasks and environment.
- Observed findings separated from interpretation.
- Severity and affected users.
- Decisions and follow-up work.

Do not record sensitive participant information in the repository. Follow applicable privacy, consent, and research-governance requirements.

## Stop conditions

Do not treat preference disagreement as a defect by itself. Escalate when representative users cannot discover or complete a critical task, misunderstand a consequential outcome, repeatedly make the same error, or require undocumented assistance.
