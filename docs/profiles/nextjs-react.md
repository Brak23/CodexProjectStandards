# Next.js and React profile

## Architecture

- Keep server-only code and secrets out of client bundles.
- Treat Server Actions and route handlers as untrusted network entry points.
- Centralize authorization in server-side use cases.
- Prefer accessible semantic HTML and user-observable tests.
- Document cache, revalidation, rendering, and runtime choices per route.

## Quality

Target WCAG 2.2 AA. Measure LCP, INP, and CLS in production at the 75th percentile. Test keyboard navigation, focus, zoom, reduced motion, and critical screen-reader behavior.
