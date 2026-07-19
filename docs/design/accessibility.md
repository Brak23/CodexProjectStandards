# Accessibility standards

## Baseline

Target WCAG 2.2 AA for user-facing web applications unless a stricter legal, contractual, or product standard applies.

Accessibility is part of the acceptance criteria and definition of done, not a final audit step.

## Required implementation behavior

- Use semantic HTML and native controls whenever possible.
- Provide programmatic names, roles, values, descriptions, and relationships.
- Support complete keyboard operation without traps.
- Maintain visible focus indicators and logical focus order.
- Move or restore focus deliberately after navigation, dialogs, errors, and dynamic updates.
- Associate validation errors with fields and provide actionable recovery guidance.
- Announce important asynchronous status changes without excessive interruption.
- Preserve meaning at 200 percent zoom and browser text enlargement.
- Respect reduced-motion preferences.
- Provide alternatives for non-text content.
- Do not rely on color, position, sound, or motion alone to communicate meaning.
- Ensure pointer targets and spacing are usable on touch devices.

## Testing layers

For UI-changing work, use the applicable combination of:

1. Static analysis and linting.
2. Automated accessibility checks in component or end-to-end tests.
3. Keyboard-only testing.
4. Focus-order and focus-restoration testing.
5. Zoom and reflow testing.
6. Reduced-motion testing.
7. Screen-reader testing for critical or custom interactions.
8. Manual contrast and non-color-cue review.

Automated scanners cannot establish full accessibility compliance. Record what was tested manually and what remains unverified.

## Custom components

A custom widget must have a documented keyboard and accessibility contract before implementation. Prefer established accessible patterns rather than inventing interaction behavior.

Custom dialogs, menus, comboboxes, grids, tabs, trees, and drag-and-drop interactions require focused manual testing and should use well-maintained accessible primitives where appropriate.

## Blocking defects

Treat these as release-blocking for affected critical flows:

- Keyboard trap or inaccessible primary action.
- Missing accessible name on an essential control.
- Focus lost or hidden during a required task.
- Critical information available only through color or pointer hover.
- Unrecoverable form error for assistive-technology users.
- Content unusable at supported zoom or text size.
