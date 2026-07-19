# UX and UI development workflow

## Before implementation

For a user-facing change, establish:

- Primary user and user goal.
- Entry point, completion point, and recovery path.
- Information hierarchy and primary action.
- Existing screens, patterns, and components to reuse.
- Happy path plus loading, empty, error, success, disabled, read-only, permission-denied, partial, offline, and delayed states when applicable.
- Desktop, tablet, mobile, narrow-height, zoomed, and long-content behavior.
- Keyboard sequence, focus order, focus restoration, and screen-reader meaning.
- Content, validation, confirmation, and destructive-action language.
- Design source, design owner, and unresolved product decisions.

Do not begin implementation from a single ideal-state mockup when material states or behavior remain undefined.

## Design handoff

A valid handoff should identify:

- Approved design or prototype reference.
- Target routes or surfaces.
- Reused and new components.
- Responsive behavior rather than only fixed-width screenshots.
- Interaction and animation behavior.
- Data assumptions and maximum realistic content.
- Accessibility annotations when behavior is not obvious.
- Copy source and terminology decisions.
- Known differences from existing patterns.

Static visual measurements are guidance, not permission to reproduce brittle absolute positioning. Implement the intended hierarchy and behavior using the project's design system.

## Implementation rules

- Prefer semantic HTML and native interaction behavior.
- Keep business and authorization policy outside presentational components.
- Keep state close to the narrowest owner that needs it.
- Distinguish server state, form state, navigation state, and ephemeral UI state.
- Reuse shared components before creating near-duplicates.
- Do not create a generic abstraction until a stable repeated pattern exists.
- Make asynchronous state visible and recoverable.
- Preserve user input after recoverable errors whenever safe.
- Prevent duplicate submissions and make destructive actions deliberate.
- Avoid layout shift and focus loss during updates.

## Definition of ready for UI implementation

A UI-significant change is ready when:

- The user goal and acceptance criteria are observable.
- Required states and responsive behavior are identified.
- Blocking copy and interaction decisions are resolved.
- Accessibility and browser/device expectations are stated.
- Existing components and patterns have been inspected.
- Any new design-system component has an explicit reason and owner.

## Definition of done

The implementation is not complete until:

- Functional and component tests pass.
- Keyboard and focus behavior are verified.
- Relevant screen-reader behavior is checked.
- Responsive layouts and 200 percent zoom are verified.
- Loading, empty, error, success, and permission states are demonstrated when applicable.
- Content is reviewed in context.
- Visual evidence is attached to the pull request.
- Intentional design deviations are documented.
- Usability or production-success measures are defined for consequential flows.
