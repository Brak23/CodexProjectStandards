# Repository utilities

- `bootstrap_project.py`: Interactive or config-driven, atomic, idempotent project initialization.
- `bootstrap_next_steps.py`: Concise post-bootstrap handoff and next commands.
- `doctor.py`: Standards adoption health report used by `task doctor`.
- `recommend_workflow.py`: Advisory Light, Full Feature, or High-Risk workflow recommendation using impact and reversibility.
- `validate_repository.py`: Dynamic template or generated-project structure, local-link, workflow, and safety validation.
- `validate_agent_governance.py`: Validates context, tool policy, feature state, agent adapters, and behavior-evaluation contracts.
- `verify_project.py`: Authoritative stack-agnostic verification contract used by `task verify` and CI.
- `test_bootstrap.py`: Two-pass end-to-end bootstrap integration test in an isolated repository copy.
- `verify.d/`: Ordered stack-specific checks shared by local and CI verification.
- `create_feature.py`: Creates a feature workspace, including machine-readable `state.yml`, from `docs/work/_template`.
- `archive_feature.py`: Moves completed work to `docs/work/archive`.

Scripts use only the Python standard library so the base template remains stack-agnostic.
