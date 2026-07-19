## Problem

Describe the user, operational, or engineering problem.

## User-visible behavior

Describe observable behavior after this change.

## Implementation summary

Explain the final implementation, not the original plan.

## Deliberately unchanged

List adjacent behavior intentionally left out.

## Acceptance criteria evidence

Map each acceptance criterion to implementation and verification evidence.

## Architecture impact

- [ ] No architecture impact
- [ ] ADR added or updated
- [ ] Module boundaries changed
- [ ] Public contract changed

## Security and privacy impact

- [ ] No changed trust boundary or sensitive data
- [ ] Threat model updated
- [ ] Authorization tests added
- [ ] Security review required

## Data and migration impact

- [ ] No data or schema impact
- [ ] Backward-compatible migration
- [ ] Backfill and reconciliation documented
- [ ] Rollback or forward-fix validated

## UX and UI impact

- [ ] No user-interface impact
- [ ] Existing design-system components and semantic tokens reused
- [ ] New component or variant is documented and justified
- [ ] Loading, empty, error, success, disabled, read-only, and permission states handled where applicable
- [ ] Narrow and wide layouts verified
- [ ] Keyboard navigation, focus order, and focus restoration verified
- [ ] Relevant screen-reader, zoom, and reduced-motion behavior checked
- [ ] User-facing content and recovery messages reviewed in context
- [ ] Intentional deviations from approved designs documented
- [ ] Usability validation or post-launch measures defined where warranted

For significant UI work, link `ux-requirements.md`, `ui-verification.md`, and the applicable checklist from `docs/design/ui-review-checklist.md`.

## Verification performed

List exact commands, results, test counts, skips, scans, and build output. Link `verification.md` for non-trivial work.

## Visual evidence or demonstration

For UI-changing work, include applicable:

- Before-and-after evidence.
- Narrow/mobile and desktop layouts.
- Loading, empty, error, success, and permission states.
- Keyboard focus or interaction recording when useful.
- Visual-regression results when supported.

Mark items not applicable rather than omitting the evidence section.

## Rollout plan

Describe flags, sequencing, canary or cohort release, metrics, and approval requirements.

## Rollback plan

Describe the fastest safe disablement or reversal path.

## Known limitations

List remaining non-blocking limitations, including untested browser, device, accessibility, visual, or usability conditions.

## Documentation updated

- [ ] README or user guidance
- [ ] UX/UI requirements or design-system guidance
- [ ] Architecture or ADR
- [ ] API or event contracts
- [ ] Operations and runbooks
- [ ] Changelog or release notes
- [ ] No documentation change required
