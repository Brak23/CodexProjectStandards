#!/usr/bin/env python3
'''Read the small project configuration shared by bootstrap and validators.'''

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE_MODES = {'delegated', 'formal'}


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.lower() in {'true', 'false'}:
        return value.lower() == 'true'
    if value in {'', 'null', '~'}:
        return None
    if value.startswith('"') and value.endswith('"'):
        return json.loads(value)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def parse_simple_yaml(path: Path) -> dict[str, Any]:
    '''Parse the template's intentionally small YAML subset without dependencies.'''
    parsed: list[tuple[int, str]] = []
    for raw in path.read_text(encoding='utf-8').splitlines():
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue
        indent = len(raw) - len(raw.lstrip(' '))
        if indent % 2:
            raise ValueError(f'YAML indentation must use two spaces: {raw}')
        parsed.append((indent, raw.strip()))

    result: dict[str, Any] = {}
    stack: list[tuple[int, object]] = [(-1, result)]
    for index, (indent, line) in enumerate(parsed):
        while indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if line.startswith('- '):
            if not isinstance(parent, list):
                raise ValueError(f'List item has no list parent: {line}')
            parent.append(parse_scalar(line[2:]))
            continue
        if ':' not in line or not isinstance(parent, dict):
            raise ValueError(f'Unsupported YAML line: {line}')
        key, value = line.split(':', 1)
        key, value = key.strip(), value.strip()
        if value:
            parent[key] = parse_scalar(value)
            continue
        next_line = parsed[index + 1] if index + 1 < len(parsed) else None
        child: object = [] if next_line and next_line[0] > indent and next_line[1].startswith('- ') else {}
        parent[key] = child
        stack.append((indent, child))
    return result


def load_project(root: Path = ROOT) -> dict[str, Any] | None:
    path = root / 'project.yml'
    return parse_simple_yaml(path) if path.exists() else None


def governance_mode(project: dict[str, Any] | None) -> str:
    '''Return delegated/formal; existing projects without a setting stay formal.'''
    if project is None:
        return 'formal'
    options = project.get('options', {})
    mode = options.get('governance_mode', 'formal') if isinstance(options, dict) else 'formal'
    if mode not in GOVERNANCE_MODES:
        raise ValueError('options.governance_mode must be one of: ' + ', '.join(sorted(GOVERNANCE_MODES)))
    return mode
