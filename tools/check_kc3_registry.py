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
import math
import sys
from pathlib import Path

import jsonschema

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "evaluation" / "kc3-checks.json"
REGISTRY_SCHEMA = REPO / "schemas" / "kc3-check-registry.schema.json"
RECEIPT_SCHEMA = REPO / "schemas" / "kc3-check-receipt.schema.json"
PIN = REPO / "evaluation" / "kc3-checks.sha256"
TAUTOLOGIES = ("nothing can refute", "cannot be refuted", "always true", "cannot fail")
KC3_RUN_CAP_USD = 1.00  # DEC-AUP-0174: USD 1.00 per run for KC-3 paid checks; reverse with the decision
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


def wilson(k: int, n: int) -> tuple[float, float]:
    z = 1.959964
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    a = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - a) / d, (c + a) / d


def check_registry(registry: dict) -> list[str]:
    problems = _errors(_validator(REGISTRY_SCHEMA), registry)
    if problems:
        return problems
    ids = [c["id"] for c in registry["checks"]]
    if registry["status"] != "registered_before_any_run":
        problems.append("registry status must stay registered_before_any_run")
    for c in registry["checks"]:
        if c["claim_origin"] != "stated_in_paper" and c["evidence_kind"] == "tests_the_claim" and c["claim_basis_in_paper"] == "authors-domain-assessment":
            problems.append(f"{c['id']}: a claim not stated in the paper cannot cite the paper's own assessment as its basis")
        if c["claim_origin"] == "registrant_hypothesis" and c["claim_basis_in_paper"] not in ("not-in-paper", "hypothesis", "limit"):
            problems.append(f"{c['id']}: a registrant hypothesis must say that the paper does not state it")
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
        if c["decision_rule"] == "paired_difference_no_advantage" and "advantage_sign" not in c:
            problems.append(f"{cid}: no-advantage rule needs advantage_sign")
        if c["decision_rule"] == "proportion_wilson" and "n_min" in c and "threshold" in c and "direction" in c:
            if c["n_min"] < 20:
                problems.append(f"{cid}: a proportion check needs n_min of at least 20")
            n, thr = c["n_min"], c["threshold"]
            best_low, worst_high = wilson(n, n)[0], wilson(0, n)[1]
            if c["direction"] == "at_least":
                reach_pred, reach_ref = best_low >= thr, worst_high < thr
            else:
                reach_pred, reach_ref = worst_high < thr, best_low >= thr
            if not reach_pred:
                problems.append(f"{cid}: the prediction cannot be met at n_min {n} and threshold {thr}")
            if not reach_ref:
                problems.append(f"{cid}: the refutation cannot be reached at n_min {n} and threshold {thr}")
        if c["decision_rule"] in ("proportion_wilson", "permutation_test") and "G-SAMPLE" not in c["gates"]:
            problems.append(f"{cid}: a sampled check needs the sample gate G-SAMPLE")
        if "G-CAP" in c["gates"] and not c["paid_model_run"]:
            problems.append(f"{cid}: gate G-CAP on a check registered as unpaid")
        for key in ("prediction", "refutation"):
            text = c[key].lower()
            if len(text) < 40 or any(t in text for t in TAUTOLOGIES):
                problems.append(f"{cid}: {key} is too short or states a tautology")
        if c["decision_rule"] == "composite":
            parts = c.get("parts", {})
            for name, part in parts.items():
                if part.get("n_min", 0) < 5:
                    problems.append(f"{cid}: part {name} needs its own n_min of at least 5")
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


def load_ref(ref: str) -> dict | None:
    path = (REPO / ref).resolve()
    if REPO.resolve() not in path.parents or not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def paper_digest(paper: str) -> str | None:
    """SHA-256 of the English entry page of a paper, the text the checks were registered against."""
    matches = sorted((REPO / "papers").glob(f"{paper}_*.md"))
    return sha256_bytes(matches[0].read_bytes()) if matches else None


def check_receipt(receipt: dict, registry: dict, registry_bytes: bytes, read_ref=load_ref, receipt_path: str | None = None,
                  ancestry=None, paper_sha=paper_digest) -> list[str]:
    """Validate a receipt against the registry it cites. Returns problems; empty means the receipt is internally consistent.

    It does not recompute the outcome from `result`: that needs the data and the harness, which this tool does not have.
    """
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
    if spend["paid_calls"] and spend.get("cap_usd", 0) > KC3_RUN_CAP_USD:
        problems.append("the recorded cap is above the per-run cap of the spend decision")
    if spend["paid_calls"] and spend.get("used_usd", 0) > spend.get("cap_usd", 0):
        problems.append("spend exceeds the recorded cap")
    if receipt["run"]["finished_at"] < receipt["run"]["started_at"]:
        problems.append("run finishes before it starts")
    if outcome == "refuted" and not receipt.get("revision_proposal_ref"):
        problems.append("a refuted outcome needs a revision proposal")
    if receipt["gates_met"].get("G-CAP") and not spend["paid_calls"]:
        problems.append("gate G-CAP is reported met but no paid calls or cap are recorded")
    if spend["paid_calls"] and spend.get("cap_recorded_at", "9") > receipt["run"]["started_at"]:
        problems.append("the spend cap was recorded after the run started")
    quals = receipt["qualifications"]
    if receipt.get("claim_weakened") and outcome != "supported":
        problems.append("claim_weakened is only meaningful on a supported outcome; refuted needs a proposal and not_measured weakens nothing")
    if outcome == "supported" and bool(quals) != bool(receipt.get("claim_weakened")):
        problems.append("a supported outcome with qualifications must set claim_weakened, and claim_weakened needs qualifications")
    if ancestry is not None and not ancestry(receipt["prereg"]["commit"]):
        problems.append("the registry commit is not an ancestor of the commit that holds this receipt")
    ref = receipt.get("revision_proposal_ref")
    if ref:
        proposal = read_ref(ref)
        if proposal is None:
            problems.append("revision_proposal_ref does not resolve to a proposal file")
        else:
            problems += ["proposal: " + m for m in _errors(_validator(RECEIPT_SCHEMA, "Proposal"), proposal)]
            if not problems:
                if proposal["check_id"] != receipt["check_id"] or proposal["paper"] != check["paper"]:
                    problems.append("proposal names another check or paper")
                if receipt_path is not None and proposal["receipt_ref"] != receipt_path:
                    problems.append("proposal receipt_ref does not name this receipt")
                if proposal["paper_sha256_at_proposal"] != paper_sha(check["paper"]):
                    problems.append("proposal paper digest is not the digest of the paper file")
                if proposal["finding"] == "refuted" and outcome != "refuted":
                    problems.append("proposal finding refuted but the receipt outcome is not refuted")
                if proposal["finding"] == "weakened" and not receipt.get("claim_weakened"):
                    problems.append("proposal finding weakened but the receipt does not say claim_weakened")
    return problems


def check_pin(registry_bytes: bytes) -> list[str]:
    """The registry digest is pinned in a file of its own, so a change to the registry shows up as a second changed file in review."""
    try:
        pinned = PIN.read_text(encoding="utf-8").split()[0]
    except (OSError, IndexError):
        return ["evaluation/kc3-checks.sha256 is missing or empty"]
    return [] if pinned == sha256_bytes(registry_bytes) else ["the registry changed but its pin file was not updated"]


def main(argv: list[str]) -> int:
    registry_bytes = REGISTRY.read_bytes()
    registry = json.loads(registry_bytes)
    problems = check_registry(registry) + check_pin(registry_bytes)
    import subprocess

    def ancestor(commit: str) -> bool:
        return subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=REPO, capture_output=True).returncode == 0

    for path in sorted((REPO / "receipts" / "theory-checks").glob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        if rec.get("schema") == "KC3CheckReceipt/v1":
            problems += [f"{path.name}: {m}" for m in check_receipt(rec, registry, registry_bytes, receipt_path=path.relative_to(REPO).as_posix(), ancestry=ancestor)]
    for problem in problems:
        print(f"KC3_REGISTRY_FAIL {problem}")
    if problems:
        return 1
    print("KC3_REGISTRY_PASS sha256=" + sha256_bytes(registry_bytes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
