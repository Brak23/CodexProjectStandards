# Next.js and React profile

Apply the repository-wide standards in [`../design/README.md`](../design/README.md) to every user-facing React surface.

## Architecture

- Keep server-only code and secrets out of client bundles.
- Treat Server Actions and route handlers as untrusted network entry points.
- Centralize authorization in server-side use cases.
- Prefer accessible semantic HTML and user-observable tests.
- Document cache, revalidation, rendering, and runtime choices per route.
- Keep domain and authorization policy outside presentational components.
- Distinguish server state, form state, navigation state, and ephemeral UI state.
- Keep state with the narrowest owner that requires it.
- Use error boundaries and route-level failure handling deliberately.
- Avoid giant page components; compose around stable product responsibilities.
- Do not create generic components before a stable repeated interaction pattern exists.

## Components and design system

- Search the established component library before creating a new component or variant.
- Consume semantic design tokens instead of duplicating raw values.
- Document the states, accessibility contract, and responsive behavior of shared components.
- Prefer composition and explicit variants over large collections of boolean props.
- Keep component APIs aligned to product meaning rather than CSS implementation.

## Forms and asynchronous behavior

- Use one clear source of truth for validation rules where practical.
- Preserve valid user input after recoverable failures.
- Prevent duplicate submissions and show pending state without falsely implying completion.
- Associate field and form errors programmatically and provide recovery guidance.
- Make loading, empty, partial, stale, offline, error, and success states deliberate.

## Testing

- Component tests verify user interaction, state transitions, keyboard behavior, and accessible output.
- End-to-end tests protect critical user journeys rather than duplicating every component test.
- Add automated accessibility checks, but retain manual keyboard, focus, zoom, reduced-motion, and critical screen-reader testing.
- Use visual-regression testing for shared components and high-value screens when the project supports it.
- Test observable behavior rather than component internals or implementation trivia.

## Quality

Target WCAG 2.2 AA. Measure LCP, INP, and CLS in production at the 75th percentile. Verify supported browsers, responsive reflow, long content, localization expansion, and critical user journeys with realistic data.
