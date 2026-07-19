# Stack-specific verification hooks

Add deterministic project checks here so local `task verify` and GitHub Actions execute the same contract.

Supported hook types:

- `*.py`, run with the configured Python interpreter.
- `*.sh`, run with Bash.
- Other executable files.

Hooks run in lexical filename order after base repository validation, bootstrap/configuration checks, and the optional reference project tests. Use numeric prefixes when order matters, for example:

```text
10-format.sh
20-lint.sh
30-typecheck.sh
40-unit-tests.sh
50-integration-tests.sh
60-build.sh
70-security.sh
```

Every hook must fail with a nonzero exit code when its control fails. Do not hide or downgrade failures in the hook.
