#!/usr/bin/env python3
"""Configure a repository created from CodexProjectStandards."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_scalar(value: str):
    value = value.strip()
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value in {"", "null", "~"}:
        return None
    return value.strip('"\'')


def parse_simple_yaml(path: Path) -> dict:
    """Parse this template's intentionally simple YAML subset without dependencies."""
    result: dict = {}
    stack: list[tuple[int, object]] = [(-1, result)]
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if line.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError(f"List item has no list parent: {raw}")
            parent.append(parse_scalar(line[2:]))
            continue
        if ":" not in line:
            raise ValueError(f"Unsupported YAML line: {raw}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            if not isinstance(parent, dict):
                raise ValueError(f"Mapping has no dict parent: {raw}")
            parent[key] = parse_scalar(value)
        else:
            # Detect a following list by peeking is deliberately avoided. Known list keys are explicit.
            child = [] if key in {"profiles", "deployment_targets"} else {}
            parent[key] = child
            stack.append((indent, child))
    return result


def prompt(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or (default or "")


def prompt_list(label: str, default: list[str]) -> list[str]:
    value = prompt(label + " (comma-separated)", ",".join(default))
    return [item.strip() for item in value.split(",") if item.strip()]


def interactive_config() -> dict:
    name = prompt("Project name", "My Project")
    slug_default = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return {
        "project": {
            "name": name,
            "slug": prompt("Repository slug", slug_default),
            "description": prompt("One-sentence project description", "Describe the user outcome this project delivers."),
            "github_owner": prompt("GitHub owner or organization", "Brak23"),
            "repository_mode": prompt("Repository mode (solo/team)", "solo"),
            "license": prompt("License", "MIT"),
        },
        "profiles": prompt_list(
            "Profiles",
            ["node-typescript", "docker", "postgresql"],
        ),
        "deployment_targets": prompt_list(
            "Deployment targets",
            ["github-container-registry", "docker-compose"],
        ),
        "options": {
            "keep_reference_project": prompt("Keep reference project? (true/false)", "false").lower() == "true",
            "preserve_template_readme": True,
            "enable_semantic_release": prompt("Enable semantic release? (true/false)", "true").lower() == "true",
        },
    }


def dump_yaml(data: dict) -> str:
    lines: list[str] = []
    for section, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{section}:")
            for key, item in value.items():
                text = str(item).lower() if isinstance(item, bool) else str(item)
                lines.append(f"  {key}: {text}")
        elif isinstance(value, list):
            lines.append(f"{section}:")
            lines.extend(f"  - {item}" for item in value)
        else:
            lines.append(f"{section}: {value}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def project_readme(config: dict) -> str:
    project = config["project"]
    profiles = config.get("profiles", [])
    deployments = config.get("deployment_targets", [])
    return f"""# {project['name']}

{project['description']}

## Project status

Initial project setup. Replace this section with lifecycle, ownership, and release status.

## Architecture

See [`docs/architecture/overview.md`](docs/architecture/overview.md) and [`docs/architecture/boundaries.md`](docs/architecture/boundaries.md).

## Selected profiles

{chr(10).join(f'- `{item}`' for item in profiles) or '- None selected'}

## Deployment targets

{chr(10).join(f'- `{item}`' for item in deployments) or '- Not yet selected'}

## Development

Use Task as the stable command interface:

```bash
task --list
task verify
```

Add stack-specific `setup`, `dev`, `test`, and `build` tasks before application development begins.

## AI-assisted workflow

- Codex and compatible agents follow [`AGENTS.md`](AGENTS.md).
- Claude Code follows [`CLAUDE.md`](CLAUDE.md), which delegates to `AGENTS.md`.
- Non-trivial features use [`docs/work/`](docs/work/README.md) and [`.agent/PLANS.md`](.agent/PLANS.md).
- Agents work on `agent/*` branches and open draft PRs.
- Humans approve specification, consequential technical decisions, merge, and production release.

## Documentation

Start at [`docs/README.md`](docs/README.md).

## Security

Report vulnerabilities according to [`SECURITY.md`](SECURITY.md). Configure repository protections using [`docs/security/github-hardening.md`](docs/security/github-hardening.md).

## License

{project['license']}
"""


def apply(config: dict, dry_run: bool) -> None:
    project = config.get("project", {})
    required = ["name", "slug", "description", "github_owner", "repository_mode", "license"]
    missing = [key for key in required if not project.get(key)]
    if missing:
        raise ValueError("Missing project fields: " + ", ".join(missing))
    if project["repository_mode"] not in {"solo", "team"}:
        raise ValueError("repository_mode must be solo or team")

    print(f"Project: {project['name']}")
    print(f"Profiles: {', '.join(config.get('profiles', [])) or 'none'}")
    print(f"Deployment targets: {', '.join(config.get('deployment_targets', [])) or 'none'}")
    if dry_run:
        print("Dry run complete. No files changed.")
        return

    project_file = ROOT / "project.yml"
    project_file.write_text(dump_yaml(config), encoding="utf-8")

    options = config.get("options", {})
    if options.get("preserve_template_readme", True):
        destination = ROOT / "docs/getting-started/template-origin.md"
        if not destination.exists():
            destination.write_text((ROOT / "README.md").read_text(encoding="utf-8"), encoding="utf-8")

    (ROOT / "README.md").write_text(project_readme(config), encoding="utf-8")

    owner = project["github_owner"]
    codeowners = (ROOT / "CODEOWNERS").read_text(encoding="utf-8").replace("@Brak23", f"@{owner}")
    (ROOT / "CODEOWNERS").write_text(codeowners, encoding="utf-8")

    issue_config = ROOT / ".github/ISSUE_TEMPLATE/config.yml"
    if issue_config.exists():
        text = issue_config.read_text(encoding="utf-8")
        text = text.replace("Brak23/CodexProjectStandards", f"{owner}/{project['slug']}")
        issue_config.write_text(text, encoding="utf-8")

    if not options.get("keep_reference_project", False):
        shutil.rmtree(ROOT / "examples/reference-project", ignore_errors=True)

    if not options.get("enable_semantic_release", True):
        release = ROOT / ".github/workflows/release.yml"
        if release.exists():
            release.rename(ROOT / ".github/workflows/release.yml.disabled")

    print("Bootstrap complete.")
    print("Next: review README.md and project.yml, implement stack tasks, then run task verify.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        config = parse_simple_yaml(args.config) if args.config else interactive_config()
        apply(config, args.dry_run)
    except (OSError, ValueError) as exc:
        print(f"bootstrap error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
