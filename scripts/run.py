#!/usr/bin/env python3
"""HG-X1 pilot runner.

This script runs a small pilot only. It does not produce an official HG-X1
measurement. Required inputs:

- --questions-json: BullshitBench v2 questions.json
- CEREBRAS_API_KEY: for Arm A raw gpt-oss-120b
- GAVEL_API_KEY: for Arm C genxis/gavel-answer

The official experiment still requires a frozen protocol, model pins, controls,
k=3 repeats, and the official scoring/binding path.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import urllib.request
from pathlib import Path

CEREBRAS_ENDPOINT = "https://api.cerebras.ai/v1/chat/completions"
GAVEL_ENDPOINT = "https://gavel.genxis.com/v1/chat/completions"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def load_items(path: Path, limit: int):
    raw = path.read_text(encoding="utf-8")
    doc = json.loads(raw)
    flat = []
    for technique in doc["techniques"]:
        for q in technique["questions"]:
            flat.append({
                "id": q["id"],
                "question": q["question"],
                "nonsensical_element": q.get("nonsensical_element"),
                "domain": q.get("domain"),
                "domain_group": q.get("domain_group"),
                "technique": technique.get("technique"),
            })
    return flat[:limit], hashlib.sha256(raw.encode("utf-8")).hexdigest()


def post_json(url: str, body: dict, key: str, idem: str, user_agent: str) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "Idempotency-Key": idem,
            "User-Agent": user_agent,
        },
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return {
                "ok": True,
                "status": resp.status,
                "doc": json.loads(resp.read().decode("utf-8")),
                "latency_s": round(time.perf_counter() - started, 3),
            }
    except Exception as exc:  # noqa: BLE001 - pilot ledger records errors
        return {"ok": False, "error": f"{type(exc).__name__}: {str(exc)[:200]}", "latency_s": round(time.perf_counter() - started, 3)}


def normalize(arm: str, model: str, item: dict, response: dict, idem: str) -> dict:
    row = {
        "arm": arm,
        "model": model,
        "id": item["id"],
        "question_sha256": sha256_text(item["question"]),
        "domain_group": item.get("domain_group"),
        "technique": item.get("technique"),
        "idempotency_key": idem,
        "latency_s": response.get("latency_s"),
    }
    if not response.get("ok"):
        row["error"] = response.get("error")
        return row
    doc = response["doc"]
    content = ((doc.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
    row.update({"http": response.get("status"), "content": content, "content_sha256": sha256_text(content)})
    usage = doc.get("usage") or {}
    row["usage"] = {k: usage.get(k) for k in ("prompt_tokens", "completion_tokens", "total_tokens") if k in usage}
    if arm == "C_gavel_answer":
        gavel = doc.get("gavel") or {}
        row["gavel_abstain"] = bool(gavel.get("abstain"))
        row["gavel_abstain_reason"] = gavel.get("abstain_reason")
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions-json", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--raw-model", default="gpt-oss-120b")
    ap.add_argument("--gavel-model", default="genxis/gavel-answer")
    args = ap.parse_args()

    cerebras_key = os.environ.get("CEREBRAS_API_KEY")
    gavel_key = os.environ.get("GAVEL_API_KEY")
    if not cerebras_key or not gavel_key:
        raise SystemExit("Set CEREBRAS_API_KEY and GAVEL_API_KEY in the environment; do not commit keys.")

    args.out.mkdir(parents=True, exist_ok=True)
    items, dataset_sha = load_items(args.questions_json, args.limit)
    rows = []
    packet = {
        "schema": "genxis.hgx1-pilot.packet/v1",
        "status": "PILOT_ONLY_NOT_OFFICIAL_HGX1_RESULT",
        "limit": args.limit,
        "k": 1,
        "dataset_sha256": dataset_sha,
        "arms": [
            {"arm": "A_raw_cerebras", "model": args.raw_model, "provider": "cerebras", "temperature": 0},
            {"arm": "C_gavel_answer", "model": args.gavel_model, "provider": "gavel", "temperature": 0},
        ],
    }
    (args.out / "packet.json").write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")

    for index, item in enumerate(items):
        raw_body = {
            "model": args.raw_model,
            "messages": [
                {"role": "system", "content": "Answer the user question directly and concisely."},
                {"role": "user", "content": item["question"]},
            ],
            "temperature": 0,
            "max_tokens": 512,
        }
        raw_idem = sha256_text(canonical({"arm": "A_raw_cerebras", "model": args.raw_model, "id": item["id"], "i": index}))
        rows.append(normalize("A_raw_cerebras", args.raw_model, item, post_json(CEREBRAS_ENDPOINT, raw_body, cerebras_key, raw_idem, "genxis-hgx1-pilot-raw/1.0"), raw_idem))

        gavel_body = {"model": args.gavel_model, "messages": [{"role": "user", "content": item["question"]}], "temperature": 0, "max_tokens": 512}
        gavel_idem = sha256_text(canonical({"arm": "C_gavel_answer", "model": args.gavel_model, "id": item["id"], "i": index}))
        rows.append(normalize("C_gavel_answer", args.gavel_model, item, post_json(GAVEL_ENDPOINT, gavel_body, gavel_key, gavel_idem, "genxis-hgx1-pilot-gavel/1.0"), gavel_idem))

    with (args.out / "ledger.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
