# Responsive design standards

Responsive design means preserving task success and information hierarchy across available space, input methods, zoom, and content variation. It is not simply shrinking a desktop layout.

## Layout rules

- Use content-driven layout behavior and documented breakpoints.
- Prefer reflow, wrapping, progressive disclosure, and container-aware composition.
- Avoid fixed dimensions when content or localization can grow.
- Prevent unintended horizontal scrolling at supported viewport sizes and 200 percent zoom.
- Keep primary actions reachable without obscuring content.
- Preserve source order and reading order when the visual layout changes.
- Do not hide essential information or functionality only to make a smaller screen fit.

## Required scenarios

Verify the applicable surfaces at:

- Narrow mobile width.
- Common mobile and tablet widths.
- Desktop width.
- Narrow-height landscape or split-screen conditions.
- 200 percent browser zoom.
- Increased text size.
- Long labels, validation messages, names, numbers, and translated text.
- Touch and pointer input.

Exact breakpoint values are project-specific. Document them with the design system or layout primitives rather than scattering arbitrary media queries.

## Common patterns

### Navigation

Navigation must remain discoverable, keyboard operable, and stateful across layouts. Preserve the current location and return focus correctly when mobile navigation opens or closes.

### Tables and dense data

Choose deliberately among reflow, horizontal scrolling, column priority, cards, or alternate summaries. Do not silently remove important columns. Label scrollable regions and preserve headers and context.

### Dialogs, drawers, and overlays

On smaller screens, a dialog may become a full-screen surface or drawer when that improves usability. Maintain focus management, escape behavior, scroll containment, and accessible naming.

### Forms

Keep labels visible, error messages close to fields, controls comfortably sized, and related inputs grouped. Avoid multi-column layouts that create confusing reading or focus order on narrow screens.

### Media and charts

Provide responsive sizing, readable labels, and a textual or tabular alternative when visual interpretation is required for task completion.

## Evidence

UI-changing pull requests should show the most relevant narrow and wide layouts plus any breakpoint where hierarchy or interaction changes materially.
