#!/usr/bin/env python3
"""Check the pre-registered theory checks (evaluation/kc3-checks.json) and the receipts that cite them.

The registry must exist, be complete (every paper P00 to P13 either has a check or says why it has none) and be falsifiable
(prediction and refutation present and different, controls and gates named). A receipt is accepted only if it cites the exact
digest of the registry, passes the gates of its check, and states an outcome its own evidence supports.
"""

from __future__ import annotations

import functools
import hashlib
import json
import sys
from pathlib import Path

import jsonschema

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "evaluation" / "kc3-checks.json"
REGISTRY_SCHEMA = REPO / "schemas" / "kc3-check-registry.schema.json"
RECEIPT_SCHEMA = REPO / "schemas" / "kc3-check-receipt.schema.json"
PAPERS = [f"P{i:02d}" for i in range(14)]
NEEDS_DIRECTION = {"proportion_wilson", "paired_difference"}
NEEDS_THRESHOLD = {"proportion_wilson"}


@functools.lru_cache(maxsize=None)
def _validator(path: Path, definition: str | None = None) -> jsonschema.Draft202012Validator:
    schema = json.loads(path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    if definition:
        schema = {"$schema": schema["$schema"], "$ref": f"#/$defs/{definition}", "$defs": schema["$defs"]}
    return jsonschema.Draft202012Validator(schema)


def _errors(validator: jsonschema.Draft202012Validator, record: object) -> list[str]:
    out = []
    for e in sorted(validator.iter_errors(record), key=lambda e: list(e.absolute_path)):
        msg = e.message if len(e.message) < 160 else e.message[:80] + " ... " + e.message[-60:]
        out.append(f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {msg}")
    return out


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_registry(registry: dict) -> list[str]:
    problems = _errors(_validator(REGISTRY_SCHEMA), registry)
    if problems:
        return problems
    ids = [c["id"] for c in registry["checks"]]
    if len(set(ids)) != len(ids):
        problems.append("duplicate check id")
    rules, gates, data = set(registry["decision_rules"]), set(registry["gates"]), set(registry["data"])
    covered = {c["paper"] for c in registry["checks"]}
    declared_none = [n["paper"] for n in registry["no_testable_claim"]]
    if len(set(declared_none)) != len(declared_none):
        problems.append("a paper is declared without a testable claim twice")
    for paper in PAPERS:
        if paper not in covered and paper not in declared_none:
            problems.append(f"{paper}: neither a check nor a no_testable_claim entry")
        if paper in covered and paper in declared_none:
            problems.append(f"{paper}: has a check and also a no_testable_claim entry")
    for c in registry["checks"]:
        cid = c["id"]
        if not cid.startswith(f"KC3-{c['paper']}-"):
            problems.append(f"{cid}: id does not match paper {c['paper']}")
        if c["decision_rule"] != "composite" and c["decision_rule"] not in rules:
            problems.append(f"{cid}: unknown decision rule {c['decision_rule']}")
        if c["decision_rule"] in NEEDS_DIRECTION and "direction" not in c:
            problems.append(f"{cid}: rule {c['decision_rule']} needs a direction")
        if c["decision_rule"] in NEEDS_THRESHOLD and "threshold" not in c:
            problems.append(f"{cid}: rule {c['decision_rule']} needs a threshold")
        if c["decision_rule"] == "paired_difference_no_advantage" and "equivalence_margin_relative" not in c:
            problems.append(f"{cid}: no-advantage rule needs an equivalence margin")
        if c["decision_rule"] == "composite":
            parts = c.get("parts", {})
            if len(parts) < 2 or "composite_rule" not in c:
                problems.append(f"{cid}: composite check needs at least two parts and a composite rule")
            for name, part in parts.items():
                if part.get("decision_rule") not in rules - {"descriptive"}:
                    problems.append(f"{cid}: part {name} has an unknown or descriptive rule")
        if c["decision_rule"] == "descriptive":
            problems.append(f"{cid}: a descriptive check has no prediction to falsify and may not be a test")
        if c["decision_rule"] != "composite" and c["decision_rule"] in {"proportion_wilson", "exact_all", "permutation_test"} and "n_min" not in c:
            problems.append(f"{cid}: rule needs n_min")
        for g in c["gates"]:
            if g not in gates:
                problems.append(f"{cid}: unknown gate {g}")
        for d in c["data"]:
            if d not in data:
                problems.append(f"{cid}: unknown data set {d}")
        if "G-VALID" not in c["gates"]:
            problems.append(f"{cid}: every check needs the validity gate G-VALID")
        if c["paid_model_run"] and "G-CAP" not in c["gates"]:
            problems.append(f"{cid}: a paid model run needs the spend-cap gate G-CAP")
        if c["paid_model_run"] == (c["spend_cap"] == "not_applicable"):
            problems.append(f"{cid}: spend_cap contradicts paid_model_run")
        if " ".join(c["prediction"].split()).lower() == " ".join(c["refutation"].split()).lower():
            problems.append(f"{cid}: prediction and refutation are the same text")
        if "D-REF" in c["data"] or ("D-Q21" in c["data"] and "G-REF" not in c["gates"]):
            problems.append(f"{cid}: question data needs the frozen-reference gate G-REF")
        if "D-L70" in c["data"] and "G-L70" not in c["gates"]:
            problems.append(f"{cid}: D-L70 needs gate G-L70")
        if "D-PKG" in c["data"] and "G-PKG" not in c["gates"]:
            problems.append(f"{cid}: D-PKG needs gate G-PKG")
    return problems


def check_receipt(receipt: dict, registry: dict, registry_bytes: bytes) -> list[str]:
    """Validate a receipt against the registry it cites. Returns problems; empty means the receipt is internally honest."""
    problems = _errors(_validator(RECEIPT_SCHEMA, "Receipt"), receipt)
    if problems:
        return problems
    checks = {c["id"]: c for c in registry["checks"]}
    check = checks.get(receipt["check_id"])
    if check is None:
        return [f"unknown check {receipt['check_id']}"]
    if receipt["prereg"]["sha256"] != sha256_bytes(registry_bytes):
        problems.append("receipt cites a digest that is not the registered file")
    for gate in check["gates"]:
        if gate not in receipt["gates_met"]:
            problems.append(f"gate {gate} is not reported")
    outcome = receipt["outcome"]
    if outcome in ("supported", "refuted"):
        if not (receipt["controls"]["positive_passed"] and receipt["controls"]["negative_failed"]):
            problems.append("a supported or refuted outcome needs both controls to behave")
        unmet = [g for g in check["gates"] if not receipt["gates_met"].get(g)]
        if unmet:
            problems.append("a supported or refuted outcome needs every gate met; unmet: " + ", ".join(unmet))
        if receipt["n"] < check.get("n_min", 1):
            problems.append(f"n {receipt['n']} is below the registered n_min {check['n_min']}")
        if check["decision_rule"] == "descriptive":
            problems.append("a descriptive check cannot be supported or refuted")
    if check["paid_model_run"] and not receipt["spend"]["paid_calls"] and receipt["outcome"] != "not_measured":
        problems.append("a paid-run check reports no paid calls but an outcome")
    spend = receipt["spend"]
    if spend["paid_calls"] and not check["paid_model_run"]:
        problems.append("paid calls were made by a check registered as unpaid")
    if spend["paid_calls"] and spend.get("used_usd", 0) > spend.get("cap_usd", 0):
        problems.append("spend exceeds the recorded cap")
    if receipt["run"]["finished_at"] < receipt["run"]["started_at"]:
        problems.append("run finishes before it starts")
    if outcome == "refuted" and not receipt.get("revision_proposal_ref"):
        problems.append("a refuted outcome needs a revision proposal")
    return problems


def main(argv: list[str]) -> int:
    registry_bytes = REGISTRY.read_bytes()
    problems = check_registry(json.loads(registry_bytes))
    for problem in problems:
        print(f"KC3_REGISTRY_FAIL {problem}")
    if problems:
        return 1
    print("KC3_REGISTRY_PASS sha256=" + sha256_bytes(registry_bytes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
