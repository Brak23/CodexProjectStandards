# Agent behavior evaluations

Repository validation proves files and commands exist. Behavior evaluations test whether an AI completes authorized work, respects real boundaries, and reports evidence honestly.

## Scenario contract

Each scenario identifies its governance mode, stimulus, required behavior, prohibited behavior, expected workflow, status, and escalation. Structural validation checks the scenario definitions only. It does not call a model or certify that a model passed.

The suite covers both useful autonomy and restraint:

- Clear delegated product work, routine dependency use, technical replanning, product corrections, recovery, review, and demonstrable completion.
- Injection, secret exposure, fabricated dependencies or evidence, false completion, sensitive-data and authorization changes, destructive or production actions outside authority.

## Live evaluation

When an agent runner is available, record the model, version, tool configuration, date, transcript or durable result, scenario identifiers, observed completion, unnecessary interruptions, missed necessary escalations, verification evidence, and limitations. Label unavailable live evaluation **NOT_RUN**. Do not infer live-agent behavior from structurally valid JSON.

Run representative scenarios when changing root instructions, tool policy, workflow classification, completion rules, or granted autonomy.
