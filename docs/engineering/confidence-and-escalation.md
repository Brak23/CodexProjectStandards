# Confidence and escalation

Confidence is a summary of evidence, not a probability invented by the agent.

## Required completion summary

For meaningful changes, report:

```text
Confidence: High | Moderate | Low

Evidence:
- Repository patterns inspected
- Relevant tests and verification commands
- Public contracts or migrations reviewed
- Independent review outcome

Limitations:
- Anything not tested or observed

Escalate if:
- Conditions that would invalidate the conclusion
```

## Confidence levels

### High

Use only when:

- Acceptance criteria are explicit.
- Relevant repository patterns and contracts were inspected.
- Deterministic verification passed.
- No material unknowns remain.
- Independent review found no blocking issue.

### Moderate

Use when the implementation is supported by evidence but one or more non-blocking limitations remain, such as incomplete environment parity, an external system that could not be exercised, or a reversible assumption.

### Low

Use when correctness depends on unresolved information, weak verification, unfamiliar behavior, inaccessible systems, or an assumption with meaningful blast radius. Low confidence normally requires a visible limitation or blocker rather than a completion claim.

## Mandatory escalation triggers

Escalate regardless of stated confidence when a change introduces or materially affects:

- Authentication or authorization.
- Sensitive or regulated data.
- Payments or financial calculations.
- Production migrations or destructive operations.
- Infrastructure permissions, secrets, or trust boundaries.
- Breaking public contracts.
- A new dependency with unclear provenance or licensing.
- Verification that cannot be reproduced.

## Prohibited behavior

- Do not manufacture numeric percentages.
- Do not use confidence to override failed checks.
- Do not claim high confidence because the diff is small.
- Do not hide limitations inside a long narrative.