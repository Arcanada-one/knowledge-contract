#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check a synthetic projection against a separately stored expected byte fixture.

The preserved edition-1.0 module supplies its four invented records and projection;
this corrected harness removes its vacuous reconstruction-equals-itself claim.
"""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
LEGACY = HERE.parent / "evidence" / "replay_uncertainty_projection.py"
spec = importlib.util.spec_from_file_location("edition_one_projection", LEGACY)
projection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(projection)


def restore(data, trace):
    result = bytearray(data)
    for row in reversed(trace):
        del result[row["start_byte"]:row["end_byte"]]
    return bytes(result)


def main():
    expected_base = (HERE / "synthetic-base.txt").read_bytes()
    records = copy.deepcopy(projection.RECORDS)
    actual_base = b"".join(projection.base_block(r) for r in records)
    generated, trace = projection.project(records)
    nonempty = [r["uncertain"].encode() for r in records if r["uncertain"]]
    changed = copy.deepcopy(records)
    changed[0]["description"] += " A fabricated extra statement."
    changed_base = b"".join(projection.base_block(r) for r in changed)
    missing = copy.deepcopy(records)
    del missing[0]["uncertain"]
    try:
        projection.project(missing)
    except ValueError:
        missing_rejected = True
    else:
        missing_rejected = False
    damaged_trace = copy.deepcopy(trace)
    damaged_trace[0]["end_byte"] -= 1
    checks = {
        "base_matches_separate_literal_fixture": actual_base == expected_base,
        "changed_description_fails_fixture_comparison": changed_base != expected_base,
        "base_omits_two_recorded_uncertainties": all(u not in actual_base for u in nonempty),
        "corrected_projection_contains_two_exact_uncertainties": all(u in generated for u in nonempty),
        "four_generated_unreviewed_labels": generated.count(b"Description status: generated; unreviewed.") == 4,
        "declared_insertion_removal_restores_fixture": restore(generated, trace) == expected_base,
        "damaged_insertion_trace_fails_restoration": restore(generated, damaged_trace) != expected_base,
        "missing_uncertainty_field_rejected": missing_rejected,
        "input_records_unchanged": records == projection.RECORDS,
    }
    report = {
        "schema": "knowledge-contract.synthetic-uncertainty-projection/2",
        "records": 4, "nonempty_uncertainties": 2,
        "legacy_code_sha256": hashlib.sha256(LEGACY.read_bytes()).hexdigest(),
        "expected_base_sha256": hashlib.sha256(expected_base).hexdigest(),
        "projection_sha256": hashlib.sha256(generated).hexdigest(),
        "checks": checks, "passed": all(checks.values()),
        "scope": "Illustration and finite checks of the projection rule using four invented records and a separate literal target. Not a reconstruction of the historical source-plus-ledger pipeline and not an OCR or semantic-accuracy measurement.",
    }
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
