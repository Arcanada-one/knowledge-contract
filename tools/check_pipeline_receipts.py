#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Validate a chain of PipelineStageReceipt/v1 receipts (engineering/specifications/pipeline).

A chain is a directory of `*.json` files, one receipt each, kept next to the artefacts of one document. The validator works from the chain
alone: no index, no registry, no network. It applies schemas/pipeline-receipt.schema.json to every receipt, then the rules a schema cannot
express. Every refusal carries a stable code (PIPE-...). It never claims that a stage did good work, only that the record of the stages is
complete, ordered, linked by digest, consistent about one document and one rights class, and honest about what was not measured.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_book_package as cbp  # noqa: E402  (strict JSON reader shared with the book-package validator)

REPO = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO / "schemas" / "pipeline-receipt.schema.json"
STAGES = ("intake", "classify", "convert", "recognise", "bundle", "kc-package", "library", "publish", "index")
# Permissiveness of a rights class; a stage may keep the class of its predecessor or narrow it, never widen it.
RIGHTS_RANK = {"third_party_restricted": 0, "unknown": 1, "public_domain": 2, "author_open": 2}
# Only these stages may end `skipped` (with a reason): the format needs no conversion, or no classification is wanted. Every other stage is essential.
SKIPPABLE = frozenset(("classify", "convert"))
# The stages that may take the ORIGINAL SOURCE as an input; every later stage works from what an earlier stage produced.
SOURCE_STAGES = frozenset(("intake", "classify", "convert", "recognise"))
IMPORT_SUFFIX = "-import"  # a tool that verifies existing outputs instead of running a stage names the import
MAX_RECEIPT_BYTES = 1 << 20
FORMAT_CHECKER = jsonschema.FormatChecker()


@FORMAT_CHECKER.checks("date-time", raises=(ValueError, TypeError))
def _utc_seconds(value):
    datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    return True


def _validator() -> jsonschema.Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=FORMAT_CHECKER)


def check_chain(root: Path) -> list[str]:
    """Problems of the chain in `root`, each as `CODE: text`; an empty list is a valid chain."""
    root = Path(root)
    problems: list[str] = []
    files = sorted(p for p in root.iterdir() if p.suffix == ".json" and (p.is_file() or p.is_symlink())) if root.is_dir() else []
    if not files:
        return ["PIPE-EMPTY: the directory holds no receipt file"]
    loaded: dict[str, tuple[dict, str]] = {}  # file name -> (receipt, sha256 of its bytes)
    validator = _validator()
    for path in files:
        if path.is_symlink() or path.stat().st_size > MAX_RECEIPT_BYTES:
            problems.append(f"PIPE-READ: {path.name}: a receipt is a regular file of at most {MAX_RECEIPT_BYTES} bytes, not a symbolic link")
            continue
        try:
            data = path.read_bytes()
            record = cbp.strict_json(cbp.read_text_strict(path), path.name)
        except (cbp.PackageError, json.JSONDecodeError, OSError) as exc:
            problems.append(f"PIPE-READ: {path.name}: {exc}")
            continue
        if not isinstance(record, dict):
            problems.append(f"PIPE-SCHEMA: {path.name}: not a JSON object")
            continue
        errors = sorted(validator.iter_errors(record), key=lambda e: list(map(str, e.absolute_path)))[:3]
        for err in errors:
            problems.append(f"PIPE-SCHEMA: {path.name}: {'/'.join(map(str, err.absolute_path)) or '<root>'}: {err.message[:160]}")
        if errors:
            continue
        loaded[path.name] = (record, hashlib.sha256(data).hexdigest())
    if problems:
        return problems

    # Order comes from the links, never from file names: exactly one head, every link resolves, no fork, no cycle, nothing left over.
    by_digest = {digest: name for name, (_, digest) in loaded.items()}
    heads = [name for name, (r, _) in loaded.items() if r["previous_receipt_sha256"] is None]
    if len(heads) != 1:
        return [f"PIPE-HEAD: exactly one receipt must have previous_receipt_sha256 null, found {len(heads)}"]
    children: dict[str, list[str]] = {}
    for name, (record, _) in loaded.items():
        prev = record["previous_receipt_sha256"]
        if prev is None:
            continue
        if prev not in by_digest:
            problems.append(f"PIPE-LINK: {name}: previous_receipt_sha256 names no receipt of this chain (a receipt was altered, removed or is not here)")
            continue
        children.setdefault(by_digest[prev], []).append(name)
    for parent, kids in children.items():
        if len(kids) > 1:
            problems.append(f"PIPE-FORK: {parent} is the predecessor of {len(kids)} receipts ({', '.join(sorted(kids))})")
    if problems:
        return problems
    order, seen, current = [], set(), heads[0]
    while current is not None and current not in seen:
        seen.add(current)
        order.append(current)
        nxt = children.get(current)
        current = nxt[0] if nxt else None
    chain = [loaded[name][0] for name in order]
    names = dict(zip(range(len(order)), order))
    if chain[0]["stage"] != "intake":
        problems.append(f"PIPE-STAGE-ORDER: {names[0]}: the chain must start at intake, it starts at {chain[0]['stage']}")
    document_id = chain[0]["document_id"]
    for i, record in enumerate(chain):
        where = names[i]
        if record["document_id"] != document_id:
            problems.append(f"PIPE-ID: {where}: document_id differs from the head's; a changed source is a new document, not an edit")
        if i and STAGES.index(record["stage"]) != STAGES.index(chain[i - 1]["stage"]) + 1:
            problems.append(f"PIPE-STAGE-ORDER: {where}: stage {record['stage']} follows {chain[i - 1]['stage']}; the stages run in order without a gap or a repeat")
        if i and chain[i - 1]["outcome"] in ("paused_safe", "refused", "failed"):
            problems.append(f"PIPE-AFTER-STOP: {where}: follows {names[i - 1]}, whose outcome is {chain[i - 1]['outcome']}; nothing consumes a stage that did not finish")
        if record["outcome"] == "skipped" and record["stage"] not in SKIPPABLE:
            problems.append(f"PIPE-SKIP: {where}: stage {record['stage']} is essential and cannot end skipped; only {', '.join(sorted(SKIPPABLE))} can")
        measured = {m["name"]: m for m in record.get("measurements", [])}
        executed = measured.get("recognition_executed")
        if record["tool"]["name"].endswith(IMPORT_SUFFIX):
            if record["stage"] != "recognise":
                problems.append(f"PIPE-IMPORT: {where}: the tool names an import but the stage is {record['stage']}; an import adapter exists for recognise only")
            elif record["outcome"] == "done":
                if not (executed and executed["status"] == "measured" and executed.get("value") is False):
                    problems.append(f"PIPE-IMPORT: {where}: an import that finished must carry the measurement recognition_executed as measured false")
                for name in ("original_run_id", "original_finished_at"):
                    if name not in measured:
                        problems.append(f"PIPE-IMPORT: {where}: an import that finished must carry the measurement {name} (measured, or not_measured with a reason)")
        elif executed and executed["status"] == "measured" and executed.get("value") is False:
            problems.append(f"PIPE-IMPORT: {where}: recognition_executed is false but the tool {record['tool']['name']} does not name an import")
        if record["finished_at"] < record["started_at"] or (i and record["started_at"] < chain[i - 1]["finished_at"]):
            problems.append(f"PIPE-TIME: {where}: a stage starts after its predecessor finished and does not finish before it started")
        if i and RIGHTS_RANK[record["rights_class"]] > RIGHTS_RANK[chain[i - 1]["rights_class"]]:
            problems.append(f"PIPE-RIGHTS: {where}: rights class {chain[i - 1]['rights_class']} became {record['rights_class']}; no stage widens rights")
        if i and record["outcome"] == "done":
            # what a finished stage may consume: the outputs of the nearest earlier stage that finished (a skipped stage passes nothing on), or the original source
            nearest = next((chain[j] for j in range(i - 1, -1, -1) if chain[j]["outcome"] == "done"), None)
            allowed = {a["sha256"] for a in (nearest["outputs"] if nearest else [])} | ({document_id[2:]} if record["stage"] in SOURCE_STAGES else set())
            if not allowed & {a["sha256"] for a in record["inputs"]}:
                problems.append(f"PIPE-INPUT: {where}: none of its inputs is an output of the nearest earlier finished stage (or, for {', '.join(sorted(SOURCE_STAGES))}, the original source); "
                                "a stage consumes what was produced")
        if record["stage"] not in SOURCE_STAGES and document_id[2:] in {a["sha256"] for a in record["inputs"]}:
            problems.append(f"PIPE-SOURCE: {where}: stage {record['stage']} lists the original source as an input; only {', '.join(sorted(SOURCE_STAGES))} work from the source")
    sources = [a["sha256"] for a in chain[0]["inputs"] if a["role"] == "source"]
    if len(sources) > 1 or (chain[0]["outcome"] == "done" and not sources) or (sources and sources[0] != document_id[2:]):
        problems.append(f"PIPE-IDENTITY: {names[0]}: document_id is the content address of the original bytes; intake must list exactly one `source` input, that digest "
                        "(a refused or failed intake that lists none is not judged)")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: check_pipeline_receipts.py CHAIN_DIR", file=sys.stderr)
        return 2
    problems = check_chain(Path(argv[1]))
    if problems:
        for p in problems:
            print(f"PIPELINE_CHAIN_FAIL {p}")
        return 1
    print("PIPELINE_CHAIN_PASS (the record of the stages only; no stage quality, no KC2 admission)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
