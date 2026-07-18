# Python profile

## Defaults

- Supported Python pinned through Mise.
- `pyproject.toml` as project configuration.
- Type checking for production modules.
- Ruff or equivalent for format and lint.
- Pytest or the standard test framework selected consistently.
- Virtual environment isolated from system Python.

## Rules

- Validate external data at boundaries.
- Do not catch broad exceptions without rethrow, translation, or explicit recovery.
- Use context managers for resources.
- Bound retries, concurrency, and memory use.
- Pin direct and transitive dependencies through a lockfile.
