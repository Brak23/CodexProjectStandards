#!/usr/bin/env python3
"""Configure a repository created from CodexProjectStandards."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_REPOSITORY = "https://github.com/Brak23/CodexProjectStandards"
SUPPORTED_PROJECT_TYPES = {"web-app", "api", "service", "cli", "library", "monorepo", "other"}
SUPPORTED_LICENSES = {"MIT", "Apache-2.0", "Proprietary"}

LICENSE_TEMPLATE_DIR = ROOT / "templates/licenses"


def parse_scalar(value: str):
    value = value.strip()
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value in {"", "null", "~"}:
        return None
    if value.startswith('"') and value.endswith('"'):
        return json.loads(value)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def parse_simple_yaml(path: Path) -> dict:
    """Parse the template's constrained YAML subset without dependencies."""
    parsed_lines: list[tuple[int, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent % 2:
            raise ValueError(f"YAML indentation must use two spaces: {raw}")
        parsed_lines.append((indent, raw.strip()))

    result: dict = {}
    stack: list[tuple[int, object]] = [(-1, result)]
    for index, (indent, line) in enumerate(parsed_lines):
        while indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if line.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError(f"List item has no list parent: {line}")
            parent.append(parse_scalar(line[2:]))
            continue

        if ":" not in line or not isinstance(parent, dict):
            raise ValueError(f"Unsupported YAML line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            parent[key] = parse_scalar(value)
            continue

        next_line = parsed_lines[index + 1] if index + 1 < len(parsed_lines) else None
        child: object = [] if next_line and next_line[0] > indent and next_line[1].startswith("- ") else {}
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
    slug = prompt("Repository name", re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"))
    owner = prompt("GitHub repository owner or organization", "Brak23")
    return {
        "project": {
            "name": name,
            "type": prompt("Project type", "web-app"),
            "description": prompt("One-sentence project description", "Describe the user outcome this project delivers."),
            "license": prompt("License (MIT/Apache-2.0/Proprietary)", "MIT"),
            "license_holder": prompt("Copyright holder", owner),
            "license_year": prompt("Copyright year", "2026"),
        },
        "repository": {
            "owner": owner,
            "name": slug,
            "mode": prompt("Repository mode (solo/team)", "solo"),
            "codeowners": prompt_list("CODEOWNERS users or teams", [f"@{owner}"]),
        },
        "profiles": prompt_list("Profiles", ["node-typescript", "docker", "postgresql"]),
        "deployment_targets": prompt_list("Deployment targets", ["github-container-registry", "docker-compose"]),
        "options": {
            "keep_reference_project": prompt("Keep reference project? (true/false)", "false").lower() == "true",
            "enable_semantic_release": prompt("Enable semantic release? (true/false)", "true").lower() == "true",
        },
    }


def format_yaml_scalar(value: object) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def dump_yaml(data: dict, indent: int = 0) -> str:
    lines: list[str] = []
    prefix = " " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            lines.append(dump_yaml(value, indent + 2).rstrip())
        elif isinstance(value, list):
            lines.append(f"{prefix}{key}:")
            lines.extend(f"{prefix}  - {format_yaml_scalar(item)}" for item in value)
        else:
            lines.append(f"{prefix}{key}: {format_yaml_scalar(value)}")
    return "\n".join(lines) + "\n"


def normalize_config(config: dict) -> dict:
    """Accept the original schema while writing the improved canonical schema."""
    project = dict(config.get("project", {}))
    repository = dict(config.get("repository", {}))

    owner = repository.get("owner") or project.pop("github_owner", None)
    name = repository.get("name") or project.get("slug")
    mode = repository.get("mode") or project.pop("repository_mode", None)
    project.pop("slug", None)

    if not repository.get("codeowners"):
        legacy = project.pop("codeowner", None)
        repository["codeowners"] = [legacy] if legacy else ([f"@{owner}"] if owner else [])

    repository.update({"owner": owner, "name": name, "mode": mode})
    project.setdefault("type", "other")
    project.setdefault("license_holder", owner)
    project.setdefault("license_year", "2026")

    return {
        "project": project,
        "repository": repository,
        "profiles": list(config.get("profiles", [])),
        "deployment_targets": list(config.get("deployment_targets", [])),
        "options": {
            "keep_reference_project": bool(config.get("options", {}).get("keep_reference_project", False)),
            "enable_semantic_release": bool(config.get("options", {}).get("enable_semantic_release", True)),
        },
    }


def validate_config(config: dict) -> None:
    project = config["project"]
    repository = config["repository"]
    required_project = ["name", "type", "description", "license", "license_holder", "license_year"]
    required_repository = ["owner", "name", "mode", "codeowners"]
    missing = [f"project.{key}" for key in required_project if not project.get(key)]
    missing += [f"repository.{key}" for key in required_repository if not repository.get(key)]
    if missing:
        raise ValueError("Missing configuration fields: " + ", ".join(missing))
    if project["type"] not in SUPPORTED_PROJECT_TYPES:
        raise ValueError("Unsupported project.type: " + project["type"])
    if project["license"] not in SUPPORTED_LICENSES:
        raise ValueError("Unsupported project.license: " + project["license"])
    if repository["mode"] not in {"solo", "team"}:
        raise ValueError("repository.mode must be solo or team")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", repository["owner"]):
        raise ValueError("repository.owner contains unsupported characters")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", repository["name"]):
        raise ValueError("repository.name contains unsupported characters")
    invalid_owners = [owner for owner in repository["codeowners"] if not re.fullmatch(r"@[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)?", owner)]
    if invalid_owners:
        raise ValueError("Invalid CODEOWNERS entries: " + ", ".join(invalid_owners))


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def project_readme(config: dict) -> str:
    project = config["project"]
    repository = config["repository"]
    profiles = config.get("profiles", [])
    deployments = config.get("deployment_targets", [])
    return f"""# {project['name']}

{project['description']}

## Project status

Initial project setup. Replace this section with lifecycle, ownership, and release status.

- Project type: `{project['type']}`
- Repository: `{repository['owner']}/{repository['name']}`
- Repository mode: `{repository['mode']}`
- Canonical setup record: [`project.yml`](project.yml)

## Architecture

See [`docs/architecture/overview.md`](docs/architecture/overview.md) and [`docs/architecture/boundaries.md`](docs/architecture/boundaries.md).

## Selected standards profiles

{chr(10).join(f'- `{item}`' for item in profiles) or '- None selected'}

Profiles select standards and recommended controls. They do not generate application code automatically. Implement the applicable profile behind the stable Task commands before feature development begins.

## Deployment targets

{chr(10).join(f'- `{item}`' for item in deployments) or '- Not yet selected'}

## Development

Use Task as the stable command interface:

```bash
task --list
task verify
```

Add stack-specific `setup`, `dev`, `test`, and `build` tasks while keeping `task verify` authoritative.

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

{project['license']}. See [`LICENSE`](LICENSE).
"""


def render_codeowners(config: dict) -> str:
    owners = " ".join(config["repository"]["codeowners"])
    return f"""# Generated from project.yml by scripts/bootstrap_project.py.
* {owners}

# Sensitive paths require explicit owner review in team mode.
/.github/workflows/ {owners}
/infrastructure/ {owners}
/migrations/ {owners}
/docs/security/ {owners}
/SECURITY.md {owners}
/CODEOWNERS {owners}
"""


def render_issue_config(config: dict) -> str:
    repository = config["repository"]
    return f"""blank_issues_enabled: false
contact_links:
  - name: Private security report
    url: https://github.com/{repository['owner']}/{repository['name']}/security/advisories/new
    about: Report suspected vulnerabilities privately.
"""


def render_template_origin() -> str:
    return f"""# Template origin

This project was initialized from [AI-Assisted Full-Stack Project Standards]({TEMPLATE_REPOSITORY}).

The upstream repository is a reusable standards scaffold for Codex and Claude Code. This file records provenance only. The active project instructions are the root `README.md`, `AGENTS.md`, `CLAUDE.md`, `project.yml`, and the documents under `docs/`.

Review upstream releases periodically and adopt changes deliberately through normal pull requests. Do not overwrite project-specific standards automatically.
"""


def render_license(config: dict) -> str:
    project = config["project"]
    template_path = LICENSE_TEMPLATE_DIR / f"{project['license']}.txt"
    if not template_path.exists():
        raise ValueError(f"Missing license template: {template_path.relative_to(ROOT)}")
    return template_path.read_text(encoding="utf-8").format(
        year=project["license_year"],
        holder=project["license_holder"],
    )


def configure_workflows(config: dict) -> None:
    workflows = ROOT / ".github/workflows"
    workflows.mkdir(parents=True, exist_ok=True)
    template_validation = workflows / "template-validation.yml"
    if template_validation.exists():
        template_validation.unlink()

    project_validation_template = ROOT / "templates/github-actions/project-validation.yml"
    atomic_write(workflows / "project-validation.yml", project_validation_template.read_text(encoding="utf-8"))

    release = workflows / "release.yml"
    release_template = ROOT / "templates/github-actions/semantic-release.yml.example"
    if config["options"]["enable_semantic_release"]:
        atomic_write(release, release_template.read_text(encoding="utf-8"))
    elif release.exists():
        release.unlink()


def apply(config: dict, dry_run: bool) -> None:
    config = normalize_config(config)
    validate_config(config)
    project = config["project"]
    repository = config["repository"]

    print(f"Project: {project['name']}")
    print(f"Repository: {repository['owner']}/{repository['name']}")
    print(f"Profiles: {', '.join(config.get('profiles', [])) or 'none'}")
    print(f"Deployment targets: {', '.join(config.get('deployment_targets', [])) or 'none'}")
    if dry_run:
        print("Dry run complete. No files changed.")
        return

    atomic_write(ROOT / "project.yml", dump_yaml(config))
    atomic_write(ROOT / "docs/getting-started/template-origin.md", render_template_origin())
    atomic_write(ROOT / "README.md", project_readme(config))
    atomic_write(ROOT / "CODEOWNERS", render_codeowners(config))
    atomic_write(ROOT / ".github/ISSUE_TEMPLATE/config.yml", render_issue_config(config))
    atomic_write(ROOT / "LICENSE", render_license(config))

    if not config["options"]["keep_reference_project"]:
        shutil.rmtree(ROOT / "examples/reference-project", ignore_errors=True)

    configure_workflows(config)

    print("Bootstrap complete.")
    print("Next: commit project.yml, review generated files, implement stack tasks, and run task verify.")


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
