# Agent behavior evaluations

`scenarios.json` contains portable governance scenarios for testing coding agents and agent runtimes.

Run the structural contract check with:

```bash
task agent-evals
```

This command confirms that the scenario suite is complete and machine-readable. It does **not** invoke a model or certify that any model passed.

A live evaluation harness should provide each scenario to the target agent in an isolated test repository and record:

- Agent and model name/version.
- Runtime and tool configuration.
- Loaded repository instructions and adapters.
- Sandbox and permission configuration.
- Agent response and attempted tool actions.
- Pass/fail result for every required and prohibited behavior.
- Evaluator identity, date, and limitations.

Do not run destructive, secret-access, production, or external-communication scenarios against real resources. Use fixtures, denied tools, mocks, or disposable sandboxes.
