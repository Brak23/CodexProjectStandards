# Optional GitHub Actions profiles

Copy and adapt these files into `.github/workflows/` only when the project uses the corresponding stack. Re-pin all actions to current verified full SHAs during adoption.

- `codeql.yml.example`: Static analysis profile.
- `dependency-review.yml.example`: Pull request dependency policy.
- `container-build.yml.example`: Immutable container build, SBOM, and provenance outline.

These templates are not active because a stack-agnostic repository cannot safely infer languages, package managers, registries, or cloud permissions.
