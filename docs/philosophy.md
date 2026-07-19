# Engineering philosophy

These standards exist to make AI-assisted software development faster **without making uncertainty invisible**.

## Understand before changing

Repository discovery is required because plausible code written without context often violates existing architecture, duplicates functionality, or fixes the wrong problem.

## Separate intent from implementation

A brief defines the outcome. A plan defines the technical approach. Separating them makes misunderstandings and design mistakes cheaper to correct before code exists.

## Scale process to risk

A typo should not require the same ceremony as authentication or a database migration. The repository keeps permanent baseline rules while each change uses a light, full, or high-risk workflow.

## Verification must be deterministic

An agent saying “this looks correct” is not evidence. Stable commands, tests, scanners, builds, and observed behavior allow humans and future agents to reproduce the result.

## Passing tests is necessary, not sufficient

Tests can be incomplete, misconfigured, or weakened. Independent review checks requirement alignment, architecture, security, data behavior, operational safety, and whether the tests meaningfully prove the claim.

## Humans own consequential decisions

Agents can discover, propose, implement, and verify. Humans retain control of product intent, irreversible tradeoffs, exceptions, merge, and production release.

## Prefer visible uncertainty

A blocked agent is safer than an agent that silently guesses. Assumptions, unknowns, limitations, and confidence must be recorded where they affect correctness.

## Keep evidence with the code

Briefs, plans, decisions, verification, contracts, and operational guidance remain in the repository so the project does not depend on one chat session or one person's memory.

## Build for replacement

The standards are the durable layer. Individual AI tools are interchangeable adapters. A project should remain understandable and operable when the preferred agent changes.