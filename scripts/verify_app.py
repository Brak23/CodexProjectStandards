#!/usr/bin/env python3
'''Run configured application checks and distinguish them from template checks.'''

from __future__ import annotations

import os
import subprocess
import sys

from project_settings import ROOT, load_project


def run(command: list[str]) -> int:
    print('+', ' '.join(command))
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def main() -> int:
    project = load_project()
    if project is None:
        print('Application verification: NOT_APPLICABLE (template source repository)')
        return 0
    project_type = project.get('project', {}).get('type', 'other')
    hooks = ROOT / 'scripts/verify.d'
    supported = [] if not hooks.exists() else sorted(
        path for path in hooks.iterdir()
        if path.is_file() and path.name != 'README.md'
    )
    if not supported:
        if project_type == 'other':
            print('Application verification: NOT_APPLICABLE (project.type is other and no checks are configured)')
            return 0
        print('Application verification: NOT_CONFIGURED (add an executable check under scripts/verify.d/)', file=sys.stderr)
        return 2
    for hook in supported:
        if hook.suffix == '.py':
            code = run([sys.executable, str(hook.relative_to(ROOT))])
        elif hook.suffix == '.sh':
            code = run(['bash', str(hook.relative_to(ROOT))])
        elif os.access(hook, os.X_OK):
            code = run([str(hook.relative_to(ROOT))])
        else:
            print(f'Application verification: invalid hook {hook.relative_to(ROOT)}', file=sys.stderr)
            return 2
        if code:
            return code
    print('Application verification: PASSED')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
