#!/usr/bin/env python3
"""Conservatively reconcile candidate findings against a durable ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

RESOLVED_STATES = {"RESOLVED", "WITHDRAWN", "SUPERSEDED", "WAIVED"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(value: object) -> str:
    text = str(value or "").lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def fingerprint(record: dict) -> str:
    supplied = record.get("fingerprint")
    if isinstance(supplied, dict):
        material = supplied
    else:
        material = {
            "record_type": record.get("record_type"),
            "scope": record.get("dimension") or record.get("seam_id"),
            "defect_class": record.get("defect_class"),
            "affected_contract": record.get("affected_contract"),
            "path": record.get("location", {}).get("path") if isinstance(record.get("location"), dict) else None,
            "symbol": record.get("location", {}).get("symbol") if isinstance(record.get("location"), dict) else None,
            "criterion": record.get("acceptance_criterion", {}).get("statement") if isinstance(record.get("acceptance_criterion"), dict) else None,
        }
    canonical = json.dumps(material, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def similarity(candidate: dict, existing: dict) -> float:
    fields = [
        (candidate.get("dimension") or candidate.get("seam_id"), existing.get("dimension") or existing.get("seam_id"), 0.25),
        (candidate.get("defect_class"), existing.get("defect_class"), 0.25),
        (candidate.get("affected_contract"), existing.get("affected_contract"), 0.20),
        ((candidate.get("location") or {}).get("symbol"), (existing.get("location") or {}).get("symbol"), 0.15),
        ((candidate.get("location") or {}).get("path"), (existing.get("location") or {}).get("path"), 0.15),
    ]
    score = 0.0
    for left, right, weight in fields:
        left_n, right_n = normalize(left), normalize(right)
        if left_n and right_n and left_n == right_n:
            score += weight
    return score


def reconcile(candidates: list[dict], ledger: list[dict]) -> list[dict]:
    by_fingerprint: dict[str, list[dict]] = {}
    for record in ledger:
        by_fingerprint.setdefault(record.get("fingerprint_sha256") or fingerprint(record), []).append(record)

    output: list[dict] = []
    for candidate in candidates:
        fp = candidate.get("fingerprint_sha256") or fingerprint(candidate)
        candidate["fingerprint_sha256"] = fp
        exact = by_fingerprint.get(fp, [])
        if exact:
            latest = exact[-1]
            state = latest.get("status")
            outcome = "REGRESSION" if state in RESOLVED_STATES else "UNCHANGED_OPEN"
            output.append({"candidate": candidate, "outcome": outcome, "existing_record_id": latest.get("record_id")})
            continue

        possible = []
        for existing in ledger:
            score = similarity(candidate, existing)
            if score >= 0.60:
                possible.append({"record_id": existing.get("record_id"), "score": round(score, 2)})
        if possible:
            possible.sort(key=lambda item: item["score"], reverse=True)
            output.append({"candidate": candidate, "outcome": "POSSIBLE_DUPLICATE", "matches": possible[:3], "reviewer_confirmation_required": True})
        else:
            output.append({"candidate": candidate, "outcome": "NEW"})
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    candidates_payload = load(args.candidates)
    ledger_payload = load(args.ledger)
    result = {
        "schema_version": 1,
        "results": reconcile(candidates_payload.get("records", []), ledger_payload.get("findings", [])),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(result['results'])} reconciliation results to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
