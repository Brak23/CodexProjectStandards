# UI review checklist

Use this checklist for pull requests that add or materially change a user-facing interface. Mark non-applicable items explicitly.

## Product and interaction

- [ ] Primary user goal and success outcome are clear.
- [ ] Entry, completion, cancellation, and recovery paths are covered.
- [ ] Loading, empty, error, success, disabled, read-only, and permission states are handled where applicable.
- [ ] Destructive actions communicate consequence and reversibility.
- [ ] Existing interaction patterns are reused or the deviation is explained.

## Design system

- [ ] Existing components and tokens were inspected before creating new ones.
- [ ] Raw styling values are not duplicated where semantic tokens exist.
- [ ] New component variants and states are documented.
- [ ] Supported themes were checked.

## Responsive behavior

- [ ] Relevant narrow and wide layouts were verified.
- [ ] 200 percent zoom and increased text size remain usable.
- [ ] Long content and validation messages do not break the layout.
- [ ] Touch targets and mobile navigation are usable.
- [ ] No unintended horizontal scrolling exists.

## Accessibility

- [ ] Semantic HTML and accessible names are correct.
- [ ] Keyboard operation and focus order were verified.
- [ ] Focus restoration and dynamic announcements were checked where applicable.
- [ ] Reduced-motion behavior was verified where motion exists.
- [ ] Critical custom interactions received screen-reader testing.
- [ ] Automated checks passed and manual limitations are recorded.

## Content

- [ ] Labels and actions use consistent user-facing terminology.
- [ ] Errors explain recovery without blame or sensitive detail.
- [ ] Empty states distinguish no data, no results, no access, loading, and failure.
- [ ] Copy was reviewed in the implemented layout.
- [ ] Localization and text expansion were considered.

## Evidence

- [ ] Before-and-after evidence is attached when changing existing UI.
- [ ] Desktop and mobile evidence is included when layout differs.
- [ ] Important loading, empty, error, and success states are demonstrated.
- [ ] Visual-regression results are included when supported.
- [ ] Intentional differences from approved designs are documented.
- [ ] Usability validation or post-launch success measures are defined when warranted.
