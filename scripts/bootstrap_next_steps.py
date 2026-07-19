#!/usr/bin/env python3
"""Print a concise handoff after bootstrap completes."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    configured = (ROOT / "project.yml").exists()
    print("\nRepository configured" if configured else "\nRepository setup")
    print("\nNext steps")
    print("1. Run: task doctor")
    print("2. Run: task verify")
    print("3. Review agent-context.yml and agent-policy.yml")
    print("4. Confirm the agent adapter you use loads AGENTS.md")
    print("5. Complete docs/security/github-hardening.md")
    print("6. For your next change, run: task recommend")
    print("7. For a normal feature, create a workspace:")
    print("   task feature FEATURE=APP-001 NAME=my-feature")
    print("8. Review its state.yml before approving implementation")
    print("\nGolden path: docs/getting-started/golden-path.md")
    print("Agent evaluation contracts: task agent-evals")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
