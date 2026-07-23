# Feature: [Name]

- Feature ID: [ID]
- Owner:
- Status: Draft
- Risk classification: Low / Moderate / High / Critical
- User-interface impact: None / Minor / Significant

## Problem

[What is wrong today?]

## Users and context

[Who encounters it and under what conditions?]

## Desired outcome

[What observable result should become possible or better?]

## Current behavior

[What happens today and how was it established?]

## User journeys

[Primary, secondary, empty, failure, recovery, and administrative paths.]

For significant user-interface work, complete [`ux-requirements.md`](ux-requirements.md). Define the user goal, information hierarchy, complete interaction-state inventory, responsive behavior, accessibility behavior, content, design-system reuse, design source, and usability validation before implementation.

## Acceptance criteria

Give every criterion a stable ID and revision. Example:

### AC-001@1: [Observable outcome]

- Given [precondition]
- When [event]
- Then [observable result]

User-facing criteria must cover applicable loading, empty, error, success, disabled, read-only, permission-denied, partial, and recovery behavior rather than only the ideal state.

The active criteria and their exact revisions must also appear in `intent-manifest.json`. The planner may reference them but may not create or rewrite them.

## Failure and edge cases

Include invalid input, duplicates, unauthorized users, concurrency, dependency failure, partial completion, retry, empty state, maximum supported size, long content, narrow layouts, zoom, and assistive-technology use where applicable.

## Permissions

[Who can read, create, change, delete, approve, and administer?]

## Data

[What is created, read, updated, deleted, retained, exported, and audited?]

## Nonfunctional requirements

- Performance:
- Accessibility:
- Reliability:
- Privacy:
- Observability:
- Browser or device support:
- Responsive and zoom behavior:
- Localization and text expansion:
- Visual-regression coverage:
- Usability validation:

## Non-goals

[What is deliberately excluded?]

## Constraints

[Business, technical, regulatory, cost, schedule, design-system, or compatibility constraints.]

## Assumptions

[List only low-risk reversible assumptions.]

## Blocking decisions

[Decisions requiring human authority. Static mockups and design links do not authorize the agent to invent missing interaction, content, accessibility, or responsive behavior.]

## Success measurement

[How production behavior will demonstrate success, including task completion or usability measures for important user flows.]

## Approval

- Approved by:
- Date:
