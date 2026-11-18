#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""New synthetic replay of the historical CW claim-scope gap, not c167 recovery.

Read pinned Git objects only; no checkout, fetch, network request or report write.
CI must provide the two commits locally (actions/checkout fetch-depth: 0).
The old inputs and validator are read from 9ba; the comparison validator is the
fixed 9cb revision, never the current working-tree implementation. Acceptance
here concerns finite validator behavior, not the truth of the synthetic prose.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_COMMIT = "9ba73c9971ceb0f02b91946d5061ef4f961df772"
CORRECTED_COMMIT = "9cbcd22fc215e8089363912dc531e42ef6845e29"
CHECKER_PATH = "tools/check_cw_programme.py"
GRAPH_PATH = "roadmap/coordinated-work/plan/execution-graph.json"
STEPS_PATH = "roadmap/coordinated-work/plan/roadmap_steps.json"
README_PATH = "roadmap/coordinated-work/README.md"
EXPERIMENTS_PATH = "roadmap/coordinated-work/EXPERIMENTS.md"
CHECKER_BLOBS = {
    HISTORICAL_COMMIT: "24adea75bd01aa07c9a46c3b837ef2779c2a69b7",
    CORRECTED_COMMIT: "2fa62c24e66d24eb0bc7dd716b56277817acac53",
}
INPUT_BLOBS = {
    GRAPH_PATH: "0471a791e329f2f0f38ad8645a6c99f7246558a1",
    STEPS_PATH: "dd7aa8f8d96717ae13f749fc364598a0c5e60519",
    README_PATH: "0588ec8910341d78fdd0ba4de6c9de52a70bf0ec",
    EXPERIMENTS_PATH: "75591312de806eeb6425ee04238d15ac01eabb7c",
}
MUTATIONS = (
    ("CW-P02", "domain_model", "Certified causal productivity increase of 99% in all workplaces."),
    ("CW-P01", "review", "This literature review proves universal real-world profit gains."),
)


class ReplayError(ValueError):
    """Required pinned input is unavailable or does not match its identity."""


def _git(repository, *arguments):
    environment = os.environ.copy()
    environment.update(GIT_NO_LAZY_FETCH="1", GIT_NO_REPLACE_OBJECTS="1",
                       GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
    command = ["git", "--no-replace-objects", "--no-optional-locks",
               "-c", "core.fsmonitor=false", "-c", "protocol.allow=never",
               "-C", str(repository), *arguments]
    try:
        result = subprocess.run(command, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env=environment, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ReplayError("Local Git read unavailable; no fetch or fallback was attempted.") from error
    if result.returncode:
        raise ReplayError("Required local Git object unavailable: " + " ".join(arguments)
                          + "; supply full local history (CI fetch-depth: 0). No fetch or fallback performed.")
    return result.stdout


def read_pinned_blob(repository, commit, path, expected_blob):
    """Check both the commit's path binding and the full returned blob bytes."""
    identity = commit + ":" + path
    actual_blob = _git(repository, "rev-parse", "--verify", identity).decode("ascii").strip()
    if actual_blob != expected_blob:
        raise ReplayError(f"Pinned Git path differs: {identity}; expected {expected_blob}, got {actual_blob}")
    raw = _git(repository, "show", identity)
    computed = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
    if computed != expected_blob:
        raise ReplayError(f"Pinned Git blob bytes differ: {identity}; expected {expected_blob}, got {computed}")
    return raw, {"path": path, "git_blob": computed, "sha256": hashlib.sha256(raw).hexdigest(),
                 "bytes": len(raw)}


def load_validator(raw, repository, commit):
    """Execute the completely read, verified historical module in isolation."""
    module = ModuleType("cw_scope_replay_" + commit)
    module.__file__ = str(Path(repository).resolve() / CHECKER_PATH)
    exec(compile(raw, "git:" + commit + ":" + CHECKER_PATH, "exec"), module.__dict__)
    return module


def _observe(validator, arguments, paper_id=None):
    # The original graph and all source records remain available for the next
    # control even if a future comparison implementation mutates an argument.
    arguments = deepcopy(arguments)
    graph = arguments[0]
    observed = {"full_validation": "NOT_RUN", "instantiation": "NOT_RUN",
                "instance_validation": "NOT_RUN"}
    stage = "validate"
    try:
        validator.validate(*arguments)
        observed["full_validation"] = "ACCEPTED"
        stage = "instantiate_release_instances"
        instances = validator.instantiate_release_instances(graph)
        observed["instantiation"] = "ACCEPTED"
        stage = "validate_release_instances"
        validator.validate_release_instances(graph, instances)
        observed["instance_validation"] = "ACCEPTED"
    except validator.InvalidProgramme as error:
        return {**observed, "outcome": "REFUSED", "refused_by": stage, "reason": str(error)}
    observed.update(outcome="ACCEPTED", release_instance_count=len(instances),
                    release_stage_count=sum(len(row["nodes"]) for row in instances))
    if paper_id is not None:
        matches = [row for row in instances if row["paper_id"] == paper_id]
        if len(matches) != 1:
            raise ReplayError("Replay instance does not identify exactly one paper: " + paper_id)
        observed["generated_claim_class"] = matches[0]["claim_class"]
        observed["generated_claim_scope"] = matches[0]["claim_scope"]
    return observed


def reproduce(repository=ROOT):
    validators, sources, retained_inputs = {}, [], None
    for label, commit in (("historical", HISTORICAL_COMMIT), ("corrected", CORRECTED_COMMIT)):
        resolved = _git(repository, "rev-parse", "--verify", commit + "^{commit}").decode("ascii").strip()
        if resolved != commit:
            raise ReplayError("Commit identity differs: " + commit)
        code, code_record = read_pinned_blob(repository, commit, CHECKER_PATH, CHECKER_BLOBS[commit])
        inputs, records = {}, [code_record]
        for path, expected in INPUT_BLOBS.items():
            inputs[path], record = read_pinned_blob(repository, commit, path, expected)
            records.append(record)
        if retained_inputs is None:
            retained_inputs = inputs
        elif inputs != retained_inputs:
            raise ReplayError("Comparison inputs differ from the historical input bytes")
        validators[label] = load_validator(code, repository, commit)
        sources.append({"label": label, "commit": commit, "objects": records})

    original = validators["historical"].strict_json(retained_inputs[GRAPH_PATH].decode("utf-8"))
    steps = retained_inputs[STEPS_PATH]
    arguments = (original, validators["historical"].strict_json(steps.decode("utf-8")), steps,
                 retained_inputs[README_PATH].decode("utf-8"), retained_inputs[EXPERIMENTS_PATH].decode("utf-8"))
    baseline = {label: _observe(validator, arguments) for label, validator in validators.items()}
    cases = []
    for paper_id, claim_class, synthetic_scope in MUTATIONS:
        graph = deepcopy(original)
        matches = [(index, row) for index, row in enumerate(graph["paper_release_contracts"])
                   if row["paper_id"] == paper_id]
        if len(matches) != 1 or matches[0][1]["claim_class"] != claim_class:
            raise ReplayError("Unexpected original paper/class identity: " + paper_id)
        index, contract = matches[0]
        original_scope = contract["claim_scope"]
        contract["claim_scope"] = synthetic_scope
        restored = deepcopy(graph)
        restored["paper_release_contracts"][index]["claim_scope"] = original_scope
        scope_only = restored == original and original_scope != synthetic_scope
        observations = {label: _observe(validator, (graph, *arguments[1:]), paper_id)
                        for label, validator in validators.items()}
        old, new = observations["historical"], observations["corrected"]
        copied = (old.get("generated_claim_scope") == synthetic_scope
                  and old.get("generated_claim_class") == claim_class)
        refused = (new["outcome"] == "REFUSED" and new["refused_by"] == "validate"
                   and new["reason"] == "paper release claim scope changed without reviewed revision: " + paper_id)
        cases.append({"paper_id": paper_id, "claim_class_unchanged": claim_class,
                      "original_scope": original_scope, "synthetic_scope": synthetic_scope,
                      "changed_json_pointer": f"/paper_release_contracts/{index}/claim_scope",
                      "only_claim_scope_changed": scope_only, "observations": observations,
                      "historical_template_copies_synthetic_scope": copied,
                      "expected_contrast_observed": scope_only and copied
                      and old["outcome"] == "ACCEPTED" and refused})
    reproduced = (all(row["outcome"] == "ACCEPTED" for row in baseline.values())
                  and all(row["expected_contrast_observed"] for row in cases))
    return {"schema": "kc-cw-claim-scope-replay/1",
            "artifact_kind": "new_synthetic_replay", "original_c167_bytes_recovered": False,
            "status": "REPRODUCED" if reproduced else "NOT_REPRODUCED",
            "provenance": {"inputs_from_commit": HISTORICAL_COMMIT, "sources": sources,
                           "working_tree_inputs_used": False, "identity_check": "local Git path and blob bytes"},
            "baseline": baseline, "cases": cases, "native_requests_executed": 0,
            "scope": "Finite behavior of two pinned validators on two new synthetic prose mutations; "
                     "not recovery of c167 raw reports, scientific acceptance, publication, or native authority."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT, help="Local repository with full pinned history")
    options = parser.parse_args(argv)
    try:
        report = reproduce(options.repo)
    except (ReplayError, ValueError, TypeError, KeyError, UnicodeError, OSError) as error:
        print(json.dumps({"schema": "kc-cw-claim-scope-replay/1", "status": "ERROR",
                          "artifact_kind": "new_synthetic_replay", "original_c167_bytes_recovered": False,
                          "historical_commit": HISTORICAL_COMMIT, "corrected_commit": CORRECTED_COMMIT,
                          "error": str(error), "native_requests_executed": 0}, sort_keys=True, indent=2))
        return 2
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if report["status"] == "REPRODUCED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
