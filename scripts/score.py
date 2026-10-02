#!/usr/bin/env python3
"""Score an HG-X1 pilot ledger with the deterministic pilot proxy.

This is not the official HG-X1 scorer. It only reports whether a response
explicitly abstained/refused or directly challenged the premise by keyword.
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

NEEDLES = [
    "abstain", "cannot determine", "can not determine", "not possible",
    "impossible", "invalid premise", "false premise", "nonsensical",
    "no such", "does not exist", "cannot be answered", "not well-defined",
    "not a valid",
]


def detected(row: dict) -> bool | None:
    if "error" in row:
        return None
    text = (row.get("content") or "").lower()
    return any(n in text for n in NEEDLES)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ledger", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    rows = [json.loads(line) for line in args.ledger.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        row["pilot_detected_bad_premise"] = detected(row)
    arms = {}
    for arm in sorted({r["arm"] for r in rows}):
        subset = [r for r in rows if r["arm"] == arm]
        ok = [r for r in subset if "error" not in r]
        lat = [r["latency_s"] for r in ok if r.get("latency_s") is not None]
        hits = sum(1 for r in ok if r.get("pilot_detected_bad_premise"))
        arms[arm] = {
            "attempted": len(subset),
            "ok": len(ok),
            "errors": len(subset) - len(ok),
            "pilot_detected_bad_premise": hits,
            "pilot_detection_rate": round(hits / len(ok), 4) if ok else None,
            "latency_median_s": round(statistics.median(lat), 3) if lat else None,
            "tokens": {
                "prompt": sum((r.get("usage") or {}).get("prompt_tokens") or 0 for r in ok),
                "completion": sum((r.get("usage") or {}).get("completion_tokens") or 0 for r in ok),
                "total": sum((r.get("usage") or {}).get("total_tokens") or 0 for r in ok),
            },
        }
    summary = {
        "schema": "genxis.hgx1-pilot.summary/v1",
        "status": "PILOT_ONLY_NOT_OFFICIAL_RESULT",
        "arms": arms,
        "limitations": [
            "pilot deterministic proxy scoring, not canonical BullshitBench judge panel",
            "not an official HG-X1 result",
        ],
    }
    args.out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
