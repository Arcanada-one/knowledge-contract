#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Retain one complete offline rule-consumption lifecycle in fresh processes."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

try:
    from tools import repository_rule_consumer as consumer
except ImportError:
    import repository_rule_consumer as consumer


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = "tools/fixtures/repository-rule-lab/cases.json"
CASE_IDS = ("start", "evaluate-unknown", "ignore-uncommitted-decoys", "packet-change-blocked",
            "repeat-requires-resume", "explicit-resume", "evaluate-true",
            "unrelated-commit-preserves-context", "source-change-blocked",
            "resume-unsupported-source", "unsupported-is-not-truth", "inspect-is-historical")
PREPARATIONS = {"initial", "none", "dirty-decoys", "packet-change", "unrelated", "unsupported-source"}
PROGRAMS = ("tools/repository_rule_consumer.py", "tools/semantic_bridge.py",
            "tools/repository_session.py", "tools/repository_observer.py",
            "engineering/studies/agent-situation-controls/situation.py",
            "tools/run_repository_rule_lab.py", INVENTORY)
SOURCE = b"NOTE Offline laboratory fixture.\nRULE lending: member AND trained UNLESS suspended\n"


def identity(path):
    raw = path.read_bytes()
    return {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def load_plan(path):
    plan = consumer.session.read_json(path)
    if (type(plan) is not dict or plan.get("schema") != "repository-rule-lab-cases/1"
            or type(plan.get("cases")) is not list
            or tuple(case.get("id") for case in plan["cases"] if type(case) is dict) != CASE_IDS
            or len(plan["cases"]) != len(CASE_IDS)):
        raise ValueError("lab case inventory is missing, duplicated, reordered or unsupported")
    for case in plan["cases"]:
        if (set(case) != {"id", "operation", "prepare", "expected"}
                or case["operation"] not in {"start", "resume", "evaluate", "inspect"}
                or case["prepare"] not in PREPARATIONS or type(case["expected"]) is not dict):
            raise ValueError("unsupported lab case")
    return plan


def packet(source, *, suspended=None, constant=False, unsupported=False):
    start = source.index(b"RULE ")
    quote = source[start:].rstrip(b"\n").decode("utf-8")
    observations = {} if constant else {"member": {"state": "known", "value": True},
                                        "trained": {"state": "known", "value": True},
                                        "suspended": {"state": "unknown"} if suspended is None
                                        else {"state": "known", "value": suspended}}
    for name, observation in observations.items():
        observation.update(referent="fixture:" + name, type="boolean")
    bindings = {} if constant else ({"member": "member"} if unsupported else
                                    {name: name for name in observations})
    return {"schema": consumer.bridge.SCHEMA, "source_sha256": hashlib.sha256(source).hexdigest(),
            "source_media_type": "text/plain", "interpretation_set": "alternatives",
            "observations": observations,
            "readings": [{"id": "lending", "start": start, "end": start + len(quote.encode("utf-8")),
                          "quote": quote, "attribution": {"agent": "laboratory fixture", "discourse": "hypothetical"},
                          "bindings": bindings}]}


def write_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def run_lab(output):
    plan = load_plan(ROOT / INVENTORY)
    programs_before = {path: identity(ROOT / path) for path in PROGRAMS}
    output = Path(output).resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError("run directory must be outside the source checkout")
    output.mkdir(parents=False, exist_ok=False)
    repo = output / "fixture-repository"
    repo.mkdir()
    commands, results = [], []
    started_at = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    write_json(output / "planned-cases.json", plan)

    def git(*args):
        argv = ["git", "-c", "core.hooksPath=/dev/null", *args]
        result = subprocess.run(argv, cwd=repo, env=consumer.session.observer._git_environment(),
                                capture_output=True, text=True, timeout=15)
        commands.append({"argv": argv, "returncode": result.returncode,
                         "stdout": result.stdout, "stderr": result.stderr})
        if result.returncode:
            raise RuntimeError("fixture Git command failed")
        return result.stdout.strip()

    def fixture(source, supplied):
        (repo / "source.txt").write_bytes(source)
        (repo / "packet.json").write_text(json.dumps(supplied, sort_keys=True) + "\n", encoding="utf-8")

    def commit(message):
        git("add", "--", "source.txt", "packet.json")
        git("commit", "-m", message)

    failure, previous, count = None, None, 0
    try:
        git("init", "--initial-branch=main")
        git("config", "user.name", "Knowledge Contract offline fixture")
        git("config", "user.email", "fixture@example.invalid")
        for index, case in enumerate(plan["cases"], 1):
            preparation = case["prepare"]
            if preparation == "initial":
                fixture(SOURCE, packet(SOURCE))
                commit("Initial synthetic inputs")
            elif preparation == "dirty-decoys":
                decoy = b"NOTE Uncommitted decoy.\nRULE lending: FALSE\n"
                fixture(decoy, packet(decoy, constant=True))
            elif preparation == "packet-change":
                fixture(SOURCE, packet(SOURCE, suspended=False))
                commit("Change required observation packet")
            elif preparation == "unrelated":
                (repo / "unrelated.txt").write_text("Outside the declared two-file profile.\n", encoding="utf-8")
                git("add", "--", "unrelated.txt")
                git("commit", "-m", "Unrelated fixture change")
            elif preparation == "unsupported-source":
                source = b"NOTE Unsupported formal input.\nRULE lending: EXISTS member\n"
                fixture(source, packet(source, unsupported=True))
                commit("Change source to unsupported grammar")
            name = f"{index:02d}-{case['id']}"
            path = output / (name + ".json")
            argv = [sys.executable, "-B", str(ROOT / PROGRAMS[0]), case["operation"]]
            if case["operation"] == "inspect":
                argv += ["--input", str(previous)]
            else:
                argv += ["--repo", str(repo), "--output", str(path)]
                if case["operation"] == "start":
                    argv += ["--source-path", "source.txt", "--packet-path", "packet.json",
                             "--task-id", "offline-rule-lifecycle", "--scope", "two-committed-inputs"]
                else:
                    argv += ["--previous", str(previous)]
            run = subprocess.run(argv, capture_output=True, text=True, timeout=60)
            (output / (name + ".stdout.txt")).write_text(run.stdout, encoding="utf-8")
            (output / (name + ".stderr.txt")).write_text(run.stderr, encoding="utf-8")
            record = {"id": case["id"], "argv": argv, "exit_code": run.returncode,
                      "expected": case["expected"], "output": path.name,
                      "stdout": name + ".stdout.txt", "stderr": name + ".stderr.txt"}
            results.append(record)
            if case["operation"] == "inspect":
                actual = json.loads(run.stdout)
                write_json(path, actual)
                observed = {"exit_code": run.returncode, **{key: actual.get(key) for key in case["expected"] if key != "exit_code"}}
                claims_valid = actual.get("effects_authorized") is False
            else:
                bundle = consumer.validate_bundle(consumer.read_bundle(path))
                count += 1
                analysis = bundle["analysis"]
                observed = {"exit_code": run.returncode, "result": bundle["result"],
                            "session_result": bundle["session"]["result"],
                            "truth": analysis.get("truth") if analysis else None}
                claims_valid = (bundle["effects_authorized"] is False and bundle["llm_calls"] == 0
                                and bundle["session"]["sequence"] == count
                                and (analysis is None or analysis["effects_authorized"] is False))
                previous = path
            record.update(observed=observed, output_identity=identity(path),
                          passed=observed == case["expected"] and claims_valid and run.stderr == "")
            if not record["passed"]:
                raise RuntimeError("case differs from its predeclared expected result: " + case["id"])
    except (ValueError, OSError, KeyError, TypeError, RuntimeError, subprocess.TimeoutExpired) as error:
        failure = {"class": type(error).__name__, "message": str(error)}
    after = {path: identity(ROOT / path) for path in PROGRAMS}
    actual_ids = tuple(record["id"] for record in results)
    complete = actual_ids == CASE_IDS and all(record.get("passed") is True for record in results)
    report = {"schema": "repository-rule-lab-run/1", "started_at": started_at,
              "completed_at": datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds": round(time.monotonic() - started, 6),
              "python": platform.python_version(), "programs_before": programs_before,
              "programs_after": after, "programs_unchanged": programs_before == after,
              "planned": len(CASE_IDS), "executed": len(results),
              "passed": sum(record.get("passed") is True for record in results),
              "not_executed": [name for name in CASE_IDS if name not in actual_ids],
              "complete": complete, "failure": failure, "cases": results,
              "result": "PASS" if complete and failure is None and programs_before == after else "FAIL",
              "llm_calls": 0, "cost": "NOT_MEASURED", "effects_authorized": False,
              "limits": "One authored offline lifecycle, not independent episodes or an LLM trial. Internal replay does not authenticate the producer. Committed files only; working tree, continuous history, native admission and authority are not established."}
    write_json(output / "fixture-git-commands.json", commands)
    write_json(output / "RUN.json", report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = run_lab(args.output)
    except (ValueError, OSError) as error:
        print("repository rule laboratory: " + str(error), file=sys.stderr)
        return 2
    print(json.dumps({key: report[key] for key in ("result", "planned", "executed", "passed", "complete", "failure")}, sort_keys=True))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
