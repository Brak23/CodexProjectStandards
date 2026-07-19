# Content design standards

Interface content is part of product behavior. Write for task completion, comprehension, recovery, and trust.

## Core rules

- Use the user's language and the product glossary consistently.
- Lead with the information or action the user needs.
- Prefer specific verbs and concrete nouns over vague labels.
- Keep button labels aligned to the action they perform.
- Keep field labels visible; do not rely on placeholder text as the only label.
- Explain why sensitive or unusual information is requested.
- Avoid internal implementation language, codes, and unexplained jargon.
- Preserve meaning when text wraps, expands, or is translated.

## Errors and validation

Error content must:

- Identify what went wrong in user-understandable terms.
- Explain what the user can do next.
- Preserve valid input when recovery is possible.
- Avoid blame.
- Avoid exposing sensitive implementation detail.
- Distinguish field errors, page errors, service failures, and permission failures.

Do not use generic messages such as “Something went wrong” when a safe, actionable explanation is available.

## Empty and loading states

An empty state should distinguish among:

- No data exists yet.
- Filters produced no results.
- The user lacks permission.
- Data is still loading.
- A dependency failed.

Provide a useful next action when one exists. Loading indicators should describe meaningful progress when waiting is material and should not imply success before completion.

## Confirmation and destructive actions

- State the consequence, affected object, and reversibility.
- Use stronger confirmation only when accidental action has meaningful cost.
- Avoid routine confirmation dialogs that train users to dismiss warnings.
- Use undo when it is safer and simpler than confirmation.

## Localization readiness

- Do not concatenate translated sentence fragments.
- Allow for text expansion.
- Keep dates, numbers, currency, names, and addresses locale-aware.
- Avoid embedding text in images when it must be localized or read by assistive technology.

## Review

Meaningful user-facing copy should be reviewed in the implemented interface, not only in a document, because layout, timing, hierarchy, and surrounding controls change interpretation.
