# Reference project

This dependency-free Node.js application demonstrates the repository workflow without forcing a production stack.

## Capability

- `GET /health` returns a structured health response.
- Unknown routes return a structured `404`.
- The server handles shutdown signals.
- Tests verify user-visible HTTP behavior.

## Run

```bash
node src/server.mjs
```

## Test

```bash
node --test
```

The example is intentionally small. Its purpose is to show that code, tests, Task commands, agent instructions, and verification evidence should agree.
