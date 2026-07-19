# Design system standards

## Tokens

Use named semantic tokens for:

- Color and contrast roles.
- Typography.
- Spacing and sizing.
- Radius and border treatment.
- Elevation.
- Motion duration and easing.
- Focus indicators.
- Breakpoints or container behavior when centrally managed.

Components should consume semantic tokens such as `surface-danger` or `text-muted`, not duplicate raw color or spacing values. Raw values require a documented exception when an appropriate token exists.

## Component rules

Before creating a component:

1. Search the existing component library and comparable product patterns.
2. Determine whether composition or a supported variant solves the need.
3. Confirm the new behavior is reusable and not merely visually similar.
4. Define ownership, states, accessibility contract, and testing expectations.

Every interactive component must document applicable states:

- Default.
- Hover.
- Focus-visible.
- Active.
- Selected or expanded.
- Disabled.
- Loading.
- Empty.
- Error.
- Success.
- Read-only.
- Permission denied.

## Variants and APIs

- Prefer small explicit variants over large collections of boolean props.
- Keep component APIs aligned to user-visible meaning rather than styling implementation.
- Do not expose arbitrary styling escape hatches by default.
- Preserve semantic markup and accessible naming across variants.
- Document controlled and uncontrolled behavior when both are supported.

## Theming

- Light, dark, high-contrast, and branded themes must use the same semantic contract.
- Do not rely on color alone to communicate state.
- Verify contrast and state visibility in every supported theme.
- Images, illustrations, charts, and shadows must remain understandable across themes.

## Ownership and lifecycle

Shared components require:

- A documented owner.
- Usage guidance and examples.
- Automated behavior and accessibility tests.
- A deprecation path for breaking replacement.
- Migration notes when consumers must change.

One-off UI is acceptable when reuse is genuinely unlikely and extraction would create a misleading abstraction. Keep it local and use shared tokens and primitives.
