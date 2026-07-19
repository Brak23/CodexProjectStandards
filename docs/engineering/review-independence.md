# Independent review levels

Review strength should increase with risk and consequence.

## Levels

### Level 0: author self-check

The implementing agent reviews its own diff and evidence in the same context. This is useful but is not independent review.

### Level 1: fresh-context review

The same model family reviews the work in a new context without relying on the implementation conversation.

### Level 2: separate agent review

A separate agent instance reviews the approved brief, plan, final diff, tests, and evidence. The reviewer is read-only by default.

### Level 3: diverse reviewer

A different model family or qualified human performs the review. Use this when model-correlated blind spots would be consequential.

### Level 4: specialist review

A qualified security, privacy, accessibility, data, infrastructure, legal, or domain specialist reviews the applicable surface.

## Minimum defaults

- Light workflow: Level 0, with Level 1 when behavior is user-visible or verification is weak.
- Full feature workflow: Level 2.
- High-risk workflow: Level 3 plus applicable Level 4 specialist review.
- Critical or regulated work: Human and specialist review as required by organizational policy.

## Independence requirements

- Reviewer context must include the approved intent, execution plan, final diff, and evidence.
- The reviewer must search for failures, not merely summarize the implementation.
- Reviewer agents must not edit implementation unless explicitly reassigned to a remediation task.
- Findings, disposition, reviewer identity or agent identifier, level, and reviewed commit must be recorded in `state.yml` and verification evidence.
- A review performed against an outdated commit is invalid for later unreviewed changes.
