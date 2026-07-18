# Node.js and TypeScript profile

## Defaults

- Current supported LTS Node.js pinned through Mise and CI.
- Strict TypeScript.
- Lockfile committed with frozen installation.
- ESM unless ecosystem constraints require CommonJS.
- Runtime boundary validation for external data.
- Node test runner, Vitest, or Jest selected explicitly, not mixed casually.

## Task commands

Implement `task setup`, `task dev`, `task format`, `task lint`, `task typecheck`, `task test`, `task build`, and include all in `task verify`.

## Security

- Disable lifecycle scripts in untrusted install contexts where practical.
- Review package provenance, maintainers, licenses, and advisories.
- Avoid evaluating user-controlled JavaScript.
- Bound request bodies, concurrency, and timeouts.
