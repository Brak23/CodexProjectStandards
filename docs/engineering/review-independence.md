# Technical review

Review should find failures, requirement mismatch, and recovery gaps. It is separate from product acceptance.

## Delegated mode

- Small changes require an author self-check and relevant verification.
- Meaningful changes use a fresh-context reviewer when available.
- Record the reviewed commit, reviewer identity or agent/context, scope, findings, disposition, and remaining limitations in the PR or **work.md**.
- Self-review cannot be presented as independent review.
- Changes after the reviewed commit require review of the changed surface.

A missing independent reviewer is a stated limitation. Do not invent reviewer independence or specialist qualifications.

## Formal mode

Formal projects retain the review levels and evidence mechanics in **docs/engineering/review-system.md**, including the project-local code-review skill and its durable records.

## Specialist review

Use a qualified specialist when the changed surface and available policy require one. General review may identify a specialist concern but must not claim specialist approval.
