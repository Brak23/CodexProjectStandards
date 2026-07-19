# UX and UI development

This directory defines the durable product-design and front-end experience standards for user-facing software.

Use these standards when a change creates or materially alters screens, flows, navigation, forms, interactive components, content, responsive behavior, or accessibility behavior.

## Required workflow

1. Define the user goal, context, and measurable outcome before choosing a visual solution.
2. Inventory the complete interaction states and responsive behavior.
3. Reuse established design-system components and tokens before creating new ones.
4. Implement semantic, accessible, resilient interfaces.
5. Verify behavior, accessibility, responsiveness, content, and visual fidelity with reproducible evidence.
6. Validate usability when the cost of user confusion is material.

## Documents

- [`ux-ui-development.md`](ux-ui-development.md): End-to-end UX/UI delivery workflow and design handoff rules.
- [`design-system.md`](design-system.md): Tokens, components, variants, theming, ownership, and reuse.
- [`accessibility.md`](accessibility.md): WCAG 2.2 AA baseline and testing expectations.
- [`responsive-design.md`](responsive-design.md): Reflow, breakpoints, touch, zoom, and dense-data behavior.
- [`content-design.md`](content-design.md): Labels, messages, terminology, recovery guidance, and localization.
- [`usability-validation.md`](usability-validation.md): Heuristic review, task testing, analytics, and post-launch learning.
- [`ui-review-checklist.md`](ui-review-checklist.md): Required evidence and review checklist for UI-changing pull requests.

## Source of truth

Design tools such as Figma may hold visual source material, but a design link or screenshot is not a complete implementation specification. The repository must retain durable behavior, states, accessibility requirements, tokens, content decisions, acceptance criteria, and intentional deviations.

Agents must not invent missing product or interaction decisions from a static mockup. Record blocking questions and obtain human direction.
