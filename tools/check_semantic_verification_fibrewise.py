"""Finite reference controls for Semantic Verification's fibrewise profile.

Run from the repository root:
    python3 -B tools/check_semantic_verification_fibrewise.py

This is a reconstruction of a reported candidate, not its recovered bytes.
Origin records are retained in reviews/semantic-verification-20261115/.
The program computes stipulated finite models; it is not a validator for the
whole specification, an empirical verdict, or an admission mechanism.
Only Python's standard library is used. Run without Python optimization.
"""

from datetime import datetime, timezone
from itertools import product
import hashlib
import json
from pathlib import Path
import platform
import shlex
import subprocess
import sys


if not __debug__:
    sys.stderr.write("Refused: optimized Python disables required assertions.\n")
    raise SystemExit(2)

STATUSES = ("pass", "fail", "unknown", "not_applicable")


def _validate(profile, verdicts, observed):
    """Deliberately narrow finite input interface, not a receipt parser."""
    if type(profile) is not tuple or type(verdicts) is not tuple:
        raise ValueError("profile and verdicts must be explicit tuples")
    if not profile or len(profile) != len(verdicts):
        raise ValueError("a nonempty, fully specified common carrier is required")
    if any(type(value) is not int or value < 0 for value in profile):
        raise ValueError("observation labels must be nonnegative integers")
    if type(observed) is not int or observed < 0:
        raise ValueError("queried observation must be a nonnegative integer")
    if any(type(value) is not str or value not in STATUSES for value in verdicts):
        raise ValueError("every assessment must use an exact declared result label")


def fibrewise_transfer(profile, verdicts, observed):
    """Return the unique assessment on this entire attained fibre or refuse.

The outcome describes a mathematical diagnostic, separately from the four
assessment labels. In particular, an unknown assessment may be determined
in the model; an ambiguous fibre must never manufacture that assessment.
"""
    _validate(profile, verdicts, observed)
    indices = tuple(i for i, value in enumerate(profile) if value == observed)
    if not indices:
        return {
            "outcome": "refused_unattained",
            "assessment": None,
            "fibre": indices,
            "witness": None,
        }
    first = indices[0]
    for other in indices[1:]:
        if verdicts[first] != verdicts[other]:
            return {
                "outcome": "refused_ambiguous",
                "assessment": None,
                "fibre": indices,
                "witness": (first, other),
            }
    return {
        "outcome": "determined_in_model",
        "assessment": verdicts[first],
        "fibre": indices,
        "witness": None,
    }


def enumerated_partial_map_oracle(profile, verdicts):
    """Enumerate all 5^2 partial maps, with None meaning undefined.

No fibre grouping, implementation witness, or diagnostic result is used.
Unattained observations must be undefined. A candidate is sound precisely
when it agrees pointwise with every state on which it is defined.
"""
    candidates = []
    examined = 0
    for candidate in product((None,) + STATUSES, repeat=2):
        examined += 1
        supported = all(candidate[a] is None or a in profile for a in (0, 1))
        sound = all(
            candidate[profile[i]] is None or candidate[profile[i]] == verdicts[i]
            for i in range(len(profile))
        )
        if supported and sound:
            candidates.append(candidate)
    maximal_size = max(sum(value is not None for value in c) for c in candidates)
    maxima = [c for c in candidates if sum(v is not None for v in c) == maximal_size]
    assert len(maxima) == 1, (profile, verdicts, maxima)
    maximal = maxima[0]
    # Check greatestness, not just a maximum-cardinality choice.
    assert all(
        all(c[a] is None or c[a] == maximal[a] for a in (0, 1))
        for c in candidates
    ), (profile, verdicts, maximal, candidates)
    return maximal, examined


def run_checks():
    """The unchanged positive suite is also run against the adverse mutant."""
    profiles = partial_map_candidates = 0
    globally_factorable = partial_only = no_determined_fibre = 0
    outcomes = {
        "determined_in_model": 0,
        "refused_ambiguous": 0,
        "refused_unattained": 0,
    }
    first_partial_example = None
    for profile in product((0, 1), repeat=4):
        for verdicts in product(STATUSES, repeat=4):
            profiles += 1
            maximal_map, oracle_examined = enumerated_partial_map_oracle(profile, verdicts)
            partial_map_candidates += oracle_examined
            determined = 0
            for observed in (0, 1):
                decision = fibrewise_transfer(profile, verdicts, observed)
                expected = (
                    "refused_unattained" if observed not in profile
                    else "refused_ambiguous" if maximal_map[observed] is None
                    else "determined_in_model"
                )
                assert decision["outcome"] == expected, (
                    "oracle disagreement", profile, verdicts, observed, decision, maximal_map
                )
                assert decision["fibre"] == tuple(
                    i for i in range(4) if profile[i] == observed
                ), ("wrong fibre", profile, observed, decision)
                outcomes[expected] += 1
                if expected == "determined_in_model":
                    determined += 1
                    assert decision["assessment"] == maximal_map[observed]
                    assert decision["witness"] is None
                elif expected == "refused_ambiguous":
                    assert decision["assessment"] is None
                    i, j = decision["witness"]
                    assert 0 <= i < j < 4
                    assert profile[i] == profile[j] == observed
                    assert verdicts[i] != verdicts[j]
                else:
                    assert decision["assessment"] is None
                    assert decision["witness"] is None
            if determined == len(set(profile)):
                globally_factorable += 1
            elif determined:
                partial_only += 1
                if first_partial_example is None:
                    first_partial_example = {
                        "profile": profile,
                        "verdicts": verdicts,
                        "maximal_partial_map": maximal_map,
                    }
            else:
                no_determined_fibre += 1

    # Independent combinatorics by fibre sizes: constant, 1+3, and 2+2.
    assert profiles == (2 ** 4) * (4 ** 4) == 4096
    assert partial_map_candidates == profiles * (5 ** 2) == 102400
    assert globally_factorable == 2 * 4 + 14 * 16 == 232
    assert partial_only == 8 * (256 - 16) + 6 * 2 * 4 * (16 - 4) == 2496
    assert no_determined_fibre == 2 * (256 - 4) + 6 * (16 - 4) ** 2 == 1368
    assert globally_factorable + partial_only + no_determined_fibre == profiles
    assert outcomes == {
        "determined_in_model": 2952,
        "refused_ambiguous": 4728,
        "refused_unattained": 512,
    }

    # Preserve every canonical label; none is inferred from a missing fibre.
    for assessment in STATUSES:
        decision = fibrewise_transfer((0, 0), (assessment, assessment), 0)
        assert decision["outcome"] == "determined_in_model"
        assert decision["assessment"] == assessment
    distinction_pairs = (
        ("pass", "fail"), ("pass", "unknown"), ("unknown", "not_applicable")
    )
    for verdicts in distinction_pairs:
        decision = fibrewise_transfer((0, 0), verdicts, 0)
        assert decision["outcome"] == "refused_ambiguous"
        assert decision["assessment"] is None
        assert decision["witness"] == (0, 1)

    # One useful fibre survives even though another prevents global transfer.
    profile = (0, 0, 1, 1)
    verdicts = ("pass", "pass", "fail", "unknown")
    assert fibrewise_transfer(profile, verdicts, 0)["assessment"] == "pass"
    assert fibrewise_transfer(profile, verdicts, 1)["outcome"] == "refused_ambiguous"

    # Refinement controls on a declared finite carrier. A relevant added
    # observation separates every conflicting pair in this model; an added
    # observation that leaves such a pair together does not repair it.
    base = (0, 0, 0, 0)
    outcomes_for_refinement = ("pass", "fail", "pass", "fail")
    assert fibrewise_transfer(base, outcomes_for_refinement, 0)["outcome"] == "refused_ambiguous"
    relevant_refinement = (0, 1, 0, 1)
    assert fibrewise_transfer(relevant_refinement, outcomes_for_refinement, 0)["assessment"] == "pass"
    assert fibrewise_transfer(relevant_refinement, outcomes_for_refinement, 1)["assessment"] == "fail"
    irrelevant_refinement = (0, 0, 1, 1)
    for observed in (0, 1):
        assert fibrewise_transfer(irrelevant_refinement, outcomes_for_refinement, observed)["outcome"] == "refused_ambiguous"

    # Domain extension can invalidate a formerly determined fibre.
    assert fibrewise_transfer((0,), ("pass",), 0)["assessment"] == "pass"
    assert fibrewise_transfer((0, 0), ("pass", "fail"), 0)["outcome"] == "refused_ambiguous"
    unattained = fibrewise_transfer((0,), ("pass",), 1)
    assert unattained == {
        "outcome": "refused_unattained", "assessment": None,
        "fibre": (), "witness": None,
    }

    invalid_inputs = (
        ((), (), 0),
        ((0,), (), 0),
        ((0,), ("pass", "fail"), 0),
        ([0], ("pass",), 0),
        ((0,), ["pass"], 0),
        ((True,), ("pass",), 0),
        ((-1,), ("pass",), 0),
        (("0",), ("pass",), 0),
        ((0,), (None,), 0),
        ((0,), ("PASS",), 0),
        ((0,), ("pass",), True),
        ((0,), ("pass",), -1),
        ((0,), ("pass",), "0"),
    )
    rejected = 0
    for args in invalid_inputs:
        try:
            fibrewise_transfer(*args)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError(("unsupported input accepted", args))
    assert rejected == len(invalid_inputs) == 13

    return {
        "schema": "kc-brain-fibrewise-transfer-finite-check/1",
        "provenance": "reconstructed from reported claim and pinned existing factorization criterion; hourly bytes unavailable",
        "scope": "all 2^4 observation maps and all 4^4 stipulated assessment maps on four labeled states",
        "declared_profiles": 4096,
        "executed_profiles": profiles,
        "unexecuted_profiles": 0,
        "globally_factorable_profiles": globally_factorable,
        "non_global_with_at_least_one_determined_fibre": partial_only,
        "profiles_without_any_determined_fibre": no_determined_fibre,
        "observation_queries": sum(outcomes.values()),
        "observation_query_outcomes": outcomes,
        "partial_map_candidates_checked": partial_map_candidates,
        "oracle": "enumerate all 5^2 partial maps; check support and statewise agreement; verify unique greatest map",
        "first_partial_example": first_partial_example,
        "separate_controls": {
            "canonical_label_preservations": len(STATUSES),
            "distinction_pairs": len(distinction_pairs),
            "partial_without_global_model": 1,
            "relevant_and_irrelevant_refinement_models": 2,
            "domain_extension_countermodel": 1,
            "unattained_observation_case": 1,
            "rejected_input_shapes": rejected,
        },
        "actual_claim": "finite agreement of full-fibre diagnostic with independent partial-map enumeration; every obstruction checked",
        "controller_independence": "same controller and shared inputs; structural oracle independence only",
        "runtime_authorized": False,
        "effects_authorized": False,
        "exclusions": [
            "new theorem or priority claim", "empirical frequency or success rate",
            "coverage beyond the declared finite carrier", "justification of supplied assessments",
            "source authentication or exact target identity", "current permission",
            "production checker execution", "native KC2 admission",
            "independent semantic or language acceptance",
        ],
    }


def _first_value_mutant(profile, verdicts, observed):
    """Deliberately unsafe: choose one representative even on mixed fibres."""
    _validate(profile, verdicts, observed)
    indices = tuple(i for i, value in enumerate(profile) if value == observed)
    return {
        "outcome": "determined_in_model" if indices else "refused_unattained",
        "assessment": verdicts[indices[0]] if indices else None,
        "fibre": indices,
        "witness": None,
    }


def execution_receipt():
    global fibrewise_transfer
    result = run_checks()
    original = fibrewise_transfer
    mutant_failure = None
    try:
        fibrewise_transfer = _first_value_mutant
        try:
            run_checks()
        except AssertionError as error:
            mutant_failure = repr(error)
    finally:
        fibrewise_transfer = original
    if mutant_failure is None:
        raise RuntimeError("first-value mutant escaped the unchanged controls")

    script = Path(__file__).resolve()
    optimized_command = [sys.executable, "-O", "-B", str(script)]
    optimized = subprocess.run(
        optimized_command, capture_output=True, text=True, timeout=10, check=False
    )
    if (
        optimized.returncode != 2 or optimized.stdout
        or optimized.stderr != "Refused: optimized Python disables required assertions.\n"
    ):
        raise RuntimeError("optimized-mode refusal differed from its fixed expectation")

    result["execution"] = {
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "command": shlex.join(sys.orig_argv),
        "working_directory": str(Path.cwd()),
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "assertions_enabled": __debug__,
    }
    result["first_value_mutant_control"] = {
        "mutation": "replace fibrewise_transfer in memory with first-representative selection",
        "procedure": "execute unchanged run_checks() and retain its original failure",
        "result": "killed",
        "observed_failure": mutant_failure,
        "original_diagnostic_restored": fibrewise_transfer is original,
    }
    result["optimized_mode_control"] = {
        "command": shlex.join(optimized_command),
        "exit_code": optimized.returncode,
        "stdout": optimized.stdout,
        "stderr": optimized.stderr,
        "result": "refused_before_finite_run_or_receipt",
    }
    return result


if __name__ == "__main__":
    print(json.dumps(execution_receipt(), indent=2))
