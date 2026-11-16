"""Portable same-controller review of the pinned fibrewise reference checker.

Run from the repository root:
    python3 -B reviews/semantic-verification-20261115/review_fibrewise_reference.py

This reviewer does not call the checker oracle or run_checks. It constructs
all partial maps as graph sets and derives the greatest map by union of every
sound graph. Auxiliary examples are outside the exhaustive binary experiment.
Ordinary replay prints a fresh JSON receipt to stdout and writes no files.
Retained original review artifacts are separate historical evidence.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import platform
import subprocess
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPOSITORY_ROOT / "tools/check_semantic_verification_fibrewise.py"
NOTE = Path(__file__).resolve().parent / "evidence/originals/F05-FIBREWISE-TRANSFER-CANDIDATE.md"
EXPECTED_SOURCE = "6f591ea3c179f3fddc687f0b8adb358d79c4d74e18bd2760c113d3d73d448188"
EXPECTED_NOTE = "7973c754308447d7f5d45cf8d1c12df6ab963f991ab031bbd966daa050b20dc2"
LABELS = ("pass", "fail", "unknown", "not_applicable")

def require(condition, context):
    if not condition:
        raise AssertionError(context)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

require(digest(SOURCE) == EXPECTED_SOURCE, "candidate source changed before review")
require(digest(NOTE) == EXPECTED_NOTE, "candidate note changed before review")
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("f05_frozen_candidate", SOURCE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def reviewer_oracle(p, v):
    # Digits encode a graph: digit0 means undefined,1..4 assessment labels.
    # No candidate helper, fibre grouping, result, or witness is consulted.
    valid_graphs = set()
    proposed = 0
    attained = set(p)
    for code in range(25):
        proposed += 1
        digits = (code % 5, code // 5)
        graph = frozenset((label, LABELS[digit - 1])
                          for label, digit in enumerate(digits) if digit)
        partial = dict(graph)
        if any(label not in attained for label in partial):
            continue
        if any(p[i] in partial and partial[p[i]] != v[i] for i in range(len(p))):
            continue
        valid_graphs.add(graph)
    greatest_graph = frozenset().union(*valid_graphs)
    require(len(dict(greatest_graph)) == len(greatest_graph),
            ("union not functional", p, v, greatest_graph))
    require(greatest_graph in valid_graphs,
            ("union not a sound partial map", p, v, greatest_graph))
    require(all(graph <= greatest_graph for graph in valid_graphs),
            ("union not greatest by extension", p, v))
    return dict(greatest_graph), proposed, len(valid_graphs)

def require_decision(p, v, a, greatest, decision):
    attained = a in p
    expected = ("determined_in_model" if a in greatest
                else "refused_ambiguous" if attained else "refused_unattained")
    require(decision["outcome"] == expected,
            ("wrong diagnostic", p, v, a, greatest, decision))
    indices = tuple(i for i in range(len(p)) if p[i] == a)
    require(decision["fibre"] == indices, ("wrong returned fibre", decision, indices))
    if a in greatest:
        require(decision["assessment"] == greatest[a], ("wrong value", greatest, decision))
        require(decision["witness"] is None, ("spurious witness", decision))
    else:
        require(decision["assessment"] is None, ("manufactured assessment", decision))
        if not attained:
            require(decision["witness"] is None, ("spurious unattained witness", decision))
        else:
            witness = decision["witness"]
            require(type(witness) is tuple and len(witness) == 2,
                    ("malformed witness", witness))
            i, j = witness
            require(0 <= i < j < len(p) and p[i] == p[j] == a and v[i] != v[j],
                    ("not an obstruction witness", p, v, a, witness))
    return expected

counts = Counter()
rows = {}
queries = Counter()
profiles = proposals = valid_maps = 0
first_mutant_counterexample = None
for p in product((0, 1), repeat=4):
    shape = "+".join(str(n) for n in sorted(Counter(p).values()))
    rows.setdefault(shape, Counter())
    for v in product(LABELS, repeat=4):
        profiles += 1
        greatest, examined, valid = reviewer_oracle(p, v)
        proposals += examined
        valid_maps += valid
        category = ("global" if set(greatest) == set(p)
                    else "partial_only" if greatest else "none")
        counts[category] += 1
        rows[shape][category] += 1
        for a in (0, 1):
            decision = m.fibrewise_transfer(p, v, a)
            outcome = require_decision(p, v, a, greatest, decision)
            queries[outcome] += 1
        if first_mutant_counterexample is None:
            for a in (0, 1):
                unsafe = m._first_value_mutant(p, v, a)
                try:
                    require_decision(p, v, a, greatest, unsafe)
                except AssertionError as error:
                    first_mutant_counterexample = {
                        "profile": p, "assessments": v, "query": a,
                        "greatest_map": greatest, "observed_failure": repr(error),
                    }
                    break

# Closed-form combinatorics, derived separately from the diagnostic and loops.
formula_rows = {
    "4": {"global": 2 * 4, "partial_only": 0, "none": 2 * (4**4 - 4)},
    "1+3": {"global": 8 * 4 * 4, "partial_only": 8 * 4 * (4**3 - 4), "none": 0},
    "2+2": {"global": 6 * 4**2, "partial_only": 6 * 2 * 4 * (4**2 - 4),
            "none": 6 * (4**2 - 4)**2},
}
observed_rows = {key: dict(value) for key, value in rows.items()}
# Counter omits zeros: normalize all three categories before comparison.
observed_rows = {key: {c: value.get(c, 0) for c in ("global", "partial_only", "none")}
                 for key, value in observed_rows.items()}
require(observed_rows == formula_rows, ("shape count disagreement", observed_rows, formula_rows))
require(profiles == 4096 and proposals == 102400, ("inventory mismatch", profiles, proposals))
require(dict(counts) == {"global": 232, "none": 1368, "partial_only": 2496}, counts)
require(valid_maps == 7272, ("unexpected sound-map inventory", valid_maps))
require(dict(queries) == {
    "determined_in_model": 2952, "refused_unattained": 512, "refused_ambiguous": 4728
}, queries)
require(first_mutant_counterexample is not None, "first-value mutant survived")

# Targeted auxiliary examples. Their counts do not enlarge the exhaustive set.
auxiliary = []
for label in LABELS:
    decision = m.fibrewise_transfer((7, 7, 13), (label, label, "pass"), 7)
    require_decision((7, 7, 13), (label, label, "pass"), 7, {7: label, 13: "pass"}, decision)
    auxiliary.append({"kind": "generalized_label_preservation", "label": label})
p, v = (7, 13, 7, 42, 42), ("unknown", "pass", "not_applicable", "fail", "fail")
greatest = {13: "pass", 42: "fail"}
for a in (7, 13, 42, 99):
    require_decision(p, v, a, greatest, m.fibrewise_transfer(p, v, a))
    auxiliary.append({"kind": "generalized_five_state_partial_model", "query": a})
before = m.fibrewise_transfer((7,), ("pass",), 7)
after = m.fibrewise_transfer((7, 7), ("pass", "fail"), 7)
require(before["outcome"] == "determined_in_model" and after["outcome"] == "refused_ambiguous",
        ("domain-extension hold failed", before, after))
auxiliary.append({"kind": "relevant_domain_extension", "before": before, "after": after})
# An added state at a different retained observation leaves the original whole fibre unchanged.
outside = m.fibrewise_transfer((7, 13), ("pass", "fail"), 7)
require(outside == before, ("other-fibre extension changed original result", before, outside))
auxiliary.append({"kind": "other_fibre_domain_extension", "unchanged_result": outside})
# Independent relevant/irrelevant refinements on the same stipulated carrier.
v = ("pass", "fail", "pass", "fail")
base = m.fibrewise_transfer((0, 0, 0, 0), v, 0)
relevant = [m.fibrewise_transfer((0, 1, 0, 1), v, a) for a in (0, 1)]
irrelevant = [m.fibrewise_transfer((0, 0, 1, 1), v, a) for a in (0, 1)]
require(base["outcome"] == "refused_ambiguous", base)
require([x["assessment"] for x in relevant] == ["pass", "fail"], relevant)
require(all(x["outcome"] == "refused_ambiguous" for x in irrelevant), irrelevant)
auxiliary.append({"kind": "refinement_controls", "relevant": relevant, "irrelevant": irrelevant})

malformed = (
    ((), (), 0), ((0,), (), 0), ((0,), ("pass", "fail"), 0),
    ([0], ("pass",), 0), ((0,), ["pass"], 0), ((True,), ("pass",), 0),
    ((-1,), ("pass",), 0), (("0",), ("pass",), 0), ((0,), (None,), 0),
    ((0,), ("PASS",), 0), ((0,), ("pass",), True), ((0,), ("pass",), -1),
    ((0,), ("pass",), "0"),
)
rejected = 0
for args in malformed:
    try:
        m.fibrewise_transfer(*args)
    except ValueError:
        rejected += 1
    else:
        raise AssertionError(("malformed input accepted", args))
require(rejected == 13, rejected)

optimized = subprocess.run([sys.executable, "-O", "-B", str(SOURCE.relative_to(REPOSITORY_ROOT))],
                           cwd=REPOSITORY_ROOT, capture_output=True, text=True, timeout=10, check=False)
require(optimized.returncode == 2 and optimized.stdout == ""
        and optimized.stderr == "Refused: optimized Python disables required assertions.\n",
        ("optimization bypass not refused", optimized.returncode, optimized.stdout, optimized.stderr))

# Independently execute the advertised entrypoint once; preserve this as a separate rerun,
# not a replacement of the author's receipt and not the source of the counts above.
entry = subprocess.run([sys.executable, "-B", str(SOURCE.relative_to(REPOSITORY_ROOT))],
                       cwd=REPOSITORY_ROOT, capture_output=True, text=True, timeout=30, check=False)
require(entry.returncode == 0, ("entrypoint failed", entry.returncode, entry.stderr))
entry_receipt = json.loads(entry.stdout)
require(entry_receipt["execution"]["script_sha256"] == EXPECTED_SOURCE, "entrypoint hash mismatch")
require(entry_receipt["first_value_mutant_control"]["result"] == "killed", "entrypoint mutant escaped")
require(entry_receipt["first_value_mutant_control"]["original_diagnostic_restored"] is True,
        "entrypoint did not restore diagnostic")
require(entry_receipt["optimized_mode_control"]["exit_code"] == 2, "entrypoint optimization check failed")
require(digest(SOURCE) == EXPECTED_SOURCE and digest(NOTE) == EXPECTED_NOTE, "source drifted during review")
report = {
    "schema": "kc-brain-f05-partial-internal-review/2",
    "observed_utc": datetime.now(timezone.utc).isoformat(),
    "reviewer": "ci_acceptance subagent, non-author role, same controller",
    "verdict": "PASS for the declared mathematical corollary and pinned finite reference checker only",
    "source": {"path": SOURCE.relative_to(REPOSITORY_ROOT).as_posix(), "sha256": EXPECTED_SOURCE},
    "note": {"path": NOTE.relative_to(REPOSITORY_ROOT).as_posix(), "sha256": EXPECTED_NOTE},
    "review_script_sha256": digest(Path(__file__)),
    "independent_review_method": "all25 partial-map graphs per profile; pointwise soundness; greatest graph by union; no candidate oracle/run_checks used",
    "executed_profiles": profiles,
    "partial_map_candidates_checked": proposals,
    "sound_partial_maps_total": valid_maps,
    "profile_categories": dict(counts),
    "closed_form_rows": formula_rows,
    "observation_query_outcomes": dict(queries),
    "query_count": sum(queries.values()),
    "first_value_mutant": {"result": "killed", "counterexample": first_mutant_counterexample},
    "auxiliary_cases": auxiliary,
    "malformed_inputs_rejected": rejected,
    "optimized_mode": {"exit_code": optimized.returncode, "stdout": optimized.stdout,
                       "stderr": optimized.stderr},
    "advertised_entrypoint": {"exit_code": entry.returncode,
        "command": "python3 -B tools/check_semantic_verification_fibrewise.py",
        "receipt_sha256": hashlib.sha256(entry.stdout.encode("utf-8")).hexdigest(),
        "receipt": entry_receipt},
    "scope_notes": [
        "Generalized labels7/13/42/99 and five-state examples are auxiliary; exhaustive claim remains four states and observation labels0/1.",
        "Refinement and other-fibre change examples establish only model-relative invariance/refusal, not runtime consumption or target-closure evidence.",
        "Candidate oracle is specific to two observation labels; it is not a general oracle for every supported diagnostic input.",
        "The public observation diagnostic accepts finite explicit complete tuples; live coverage of actual fibres is not established.",
        "No remote source mutation; ordinary replay writes no files and does not overwrite retained receipts.",
        "This portable review pins the canonical reference checker; any later edit needs a new hash and review. It does not validate the whole normative specification."
    ],
    "not_verified": [
        "external scientific or controller independence",
        "truth or availability of supplied assessment labels",
        "real target, source authentication, whole relevant fibre coverage",
        "actual consumption, native KC2 admission, production runtime authorization",
        "locale acceptance, source merge, deployment or improved outcomes"
    ],
    "environment": {"python": sys.version, "platform": platform.platform()},
}
print(json.dumps(report, indent=2))
