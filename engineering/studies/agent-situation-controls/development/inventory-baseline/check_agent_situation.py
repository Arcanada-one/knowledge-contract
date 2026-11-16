#!/usr/bin/env python3
"""Run authored finite controls and deliberately disabled-guard variants."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from situation import Model, Observation

def obs(key, value=None, *, scope="A", source=None, event=None, seq=1,
        at=0, receipt=None, ttl=None, state="KNOWN", deps=(), pins=None):
    return Observation(key, scope, source or key + "-sensor",
                       event or scope + ":" + key + ":" + str(seq), seq,
                       value, state, at, at if receipt is None else receipt,
                       ttl, tuple(deps), pins)

class Scenario:
    def __init__(self, model_type):
        self.model = model_type()
        self.trace = []

    def call(self, method, **arguments):
        value = getattr(self.model, method)(**arguments)
        self.trace.append({"operation": method, "input": arguments, "output": value})
        return value

    def add(self, observation):
        from dataclasses import asdict
        result = self.model.ingest(observation)
        self.trace.append({"operation": "ingest", "input": asdict(observation), "output": result})
        return result

    def state(self, key, now=0, scope="A"):
        return self.call("resolve", scope=scope, key=key, now=now)

    def project(self, required, *, optional=(), now=0, scope="A", budget=100, costs=None):
        return self.call("project", scope=scope, required=list(required),
                         optional=list(optional), now=now, budget=budget, costs=costs)

    def validate(self, snapshot, now=0, scope="A"):
        return self.call("validate", snapshot=snapshot, scope=scope, now=now)

def case01(s):
    s.add(obs("x", 1, ttl=10))
    states = [s.state("x", n)["state"] for n in (9, 10, 11)]
    s.add(obs("x", 2, seq=2, at=12, ttl=10))
    return {"ttl_states": states, "recovery": s.state("x", 12)["state"],
            "recovered_value": s.state("x", 12)["value"]}

def case02(s):
    s.add(obs("unknown", state="UNKNOWN"))
    s.add(obs("false", False))
    s.add(obs("zero", 0))
    values = {key: s.state(key) for key in ("unknown", "false", "zero")}
    return {"states": [values[k]["state"] for k in values],
            "false_type": type(values["false"]["value"]).__name__,
            "zero_type": type(values["zero"]["value"]).__name__,
            "unknown_value": values["unknown"]["value"]}

def case03(s):
    s.add(obs("x", 7, at=0, receipt=8, ttl=5))
    first = s.state("x", 8)["state"]
    duplicate = s.add(obs("x", 7, at=0, receipt=10, ttl=5))
    result = s.state("x", 10)
    return {"first": first, "duplicate": duplicate, "after": result["state"],
            "retained_observed_at": result["sources"][0]["observed_at"],
            "retained_received_at": result["sources"][0]["received_at"]}

def case04(s):
    s.add(obs("future", 1, at=20, receipt=0))
    future = s.project(["future"])["status"]
    # A separate normal key allows the same model to expose the clock rollback.
    s.add(obs("normal", 1))
    before = s.project(["normal"], now=10)["status"]
    backward = s.project(["normal"], now=9)
    return {"future": future, "before": before, "backward": backward["status"],
            "clock_invalid": "CLOCK_INVALID" in backward["reasons"]}

def case05(s):
    s.add(obs("x", "new", source="stream", seq=2))
    lower = s.add(obs("x", "old", source="stream", seq=1, receipt=1))
    equal = s.add(obs("x", "different", source="stream", seq=2,
                      event="equal-sequence-new-event", receipt=2))
    cross_key = s.add(obs("other", "old", source="stream", seq=1, receipt=3))
    return {"lower": lower, "equal": equal, "cross_key_lower": cross_key,
            "value": s.state("x", 3)["value"]}

def case06(s):
    s.add(obs("x", True, source="first", event="first"))
    s.add(obs("x", False, source="second", event="second"))
    result = s.state("x")
    projection = s.project(["x"])
    return {"state": result["state"], "source_count": len(result["sources"]),
            "projection": projection["status"], "chosen_value": result["value"]}

def case07(s):
    s.add(obs("x", 1, event="same"))
    duplicate = s.add(obs("x", 1, event="same", receipt=1))
    inconsistent = s.add(obs("x", 2, event="same", receipt=2))
    return {"duplicate": duplicate, "inconsistent": inconsistent,
            "generation": s.model.generation, "value": s.state("x", 2)["value"]}

def case08(s):
    s.add(obs("a", 1))
    s.add(obs("b", "derived", deps=("a",), pins=(("a", 1),)))
    s.add(obs("unrelated", 1))
    snapshot = s.project(["b"])["snapshot"]
    s.add(obs("unrelated", 2, seq=2, at=1))
    unrelated = s.validate(snapshot, 1)["status"]
    s.add(obs("a", 2, seq=2, at=2))
    relevant = s.call("refresh", scope="A", required=["b"], now=2, trigger="EVENT",
                      event_key="a", changed=True)
    return {"unrelated_snapshot": unrelated, "derived_state": s.state("b", 2)["state"],
            "relevant_snapshot": s.validate(snapshot, 2)["status"],
            "relevant_request": relevant["request_model_call"]}

def case09(s):
    s.add(obs("x", 1, ttl=10))
    heartbeat = s.call("refresh", scope="A", required=["x"], now=5, trigger="HEARTBEAT")
    unchanged = s.call("refresh", scope="A", required=["x"], now=5, trigger="EVENT",
                       event_key="x", changed=False)
    unrelated = s.call("refresh", scope="A", required=["x"], now=5, trigger="EVENT",
                       event_key="noise", changed=True)
    return {"heartbeat_request": heartbeat["request_model_call"],
            "unchanged_request": unchanged["request_model_call"],
            "unrelated_request": unrelated["request_model_call"],
            "observed_at": s.state("x", 5)["sources"][0]["observed_at"]}

def case10(s):
    s.add(obs("x", "account-A", scope="A"))
    s.add(obs("x", "account-B", scope="B"))
    snapshot = s.project(["x"], scope="A")["snapshot"]
    return {"cross_scope": s.validate(snapshot, scope="B")["status"],
            "own_scope": s.validate(snapshot, scope="A")["status"],
            "account_B_value": s.state("x", scope="B")["value"]}

def case11(s):
    s.add(obs("a", 1))
    s.add(obs("b", 2, deps=("a",), pins=(("a", 1),)))
    s.add(obs("c", 3, deps=("b",), pins=(("b", 1),)))
    s.add(obs("bonus", 4))
    costs = {"a": 2, "b": 3, "c": 1, "bonus": 1}
    exact = s.project(["c"], optional=["bonus"], budget=6, costs=costs)
    below = s.project(["c"], optional=["bonus"], budget=5, costs=costs)
    return {"exact_status": exact["status"], "exact_included": exact["included"],
            "exact_cost": exact["cost"], "optional_omitted": exact["omitted"],
            "below_status": below["status"], "below_included": below["included"],
            "below_closure": below["required_closure"], "below_required_cost": below["required_cost"]}

def case12(s):
    s.add(obs("known", 1))
    s.add(obs("unknown", state="UNKNOWN"))
    optional = s.project(["known"], optional=["unknown"])
    return {"missing": s.project(["missing"])["status"],
            "unknown": s.project(["unknown"])["status"],
            "optional_status": optional["status"], "optional_included": optional["included"],
            "optional_omission": optional["omitted"]}

def case13(s):
    for key in ("r", "a", "b", "z"):
        s.add(obs(key, key))
    first = s.project(["r"], optional=["z", "b", "a"], budget=3)
    second = s.project(["r"], optional=["z", "b", "a"], budget=3)
    return {"deterministic": first == second, "included": first["included"],
            "omitted": first["omitted"]}

def case14(s):
    s.add(obs("grant_fixture", True))
    s.add(obs("plan", "prepared", deps=("grant_fixture",), pins=(("grant_fixture", 1),)))
    snapshot = s.project(["plan"])["snapshot"]
    before = s.validate(snapshot)["status"]
    s.add(obs("grant_fixture", False, seq=2, at=1))
    false_fact = s.project(["grant_fixture"], now=1)
    return {"before": before, "after": s.validate(snapshot, 1)["status"],
            "plan_state": s.state("plan", 1)["state"],
            "false_fact_structural_status": false_fact["status"],
            "readiness_grants_permission": false_fact["readiness_grants_permission"]}

def case15(s):
    s.add(obs("critical", "same-value"))
    snapshot = s.project(["critical"])["snapshot"]
    before = s.validate(snapshot)["status"]
    s.add(obs("critical", "same-value", seq=2, at=1))
    after = s.validate(snapshot, 1)
    return {"unchanged": before, "changed": after["status"],
            "version_reason": "CRITICAL_GENERATION_CHANGED:critical" in after["reasons"]}

def case16(s):
    s.add(obs("sensor", 1, ttl=5))
    s.project(["sensor"])
    result = s.call("refresh", scope="A", required=["sensor"], now=5, trigger="EXPIRY")
    return result

def case17(s):
    s.add(obs("critical", 1, ttl=10))
    s.add(obs("plan", "prepared", deps=("critical",), pins=(("critical", 1),)))
    s.add(obs("unrelated", 0, ttl=1))
    snapshot = s.project(["plan"])["snapshot"]
    fresh = s.call("refresh", scope="A", required=["plan"], now=2,
                   trigger="PRE_ACTION", snapshot=snapshot)
    stale = s.call("refresh", scope="A", required=["plan"], now=10,
                   trigger="PRE_ACTION", snapshot=snapshot)
    return {"fresh_reason": fresh["reason"], "fresh_observe": fresh["observe"],
            "fresh_model_request": fresh["request_model_call"],
            "stale_reason": stale["reason"], "stale_observe": stale["observe"]}

def case18(s):
    s.add(obs("external_outcome", state="UNKNOWN"))
    result = s.project(["external_outcome"])
    return {"outcome": s.state("external_outcome")["state"],
            "projection": result["status"], "readiness_grants_permission":
            result["readiness_grants_permission"]}

def case19(s):
    s.add(obs("a", "old"))
    s.add(obs("a", "new", seq=2, at=5))
    s.add(obs("unbound", "derived from old a", at=0, receipt=10, ttl=20, deps=("a",)))
    s.add(obs("old_pin", "derived from old a", at=0, receipt=10, ttl=20,
              deps=("a",), pins=(("a", 1),)))
    s.add(obs("future_pin", "claims future premise", at=0, receipt=10, ttl=20,
              deps=("a",), pins=(("a", 2),)))
    return {"unbound": s.project(["unbound"], now=10)["status"],
            "old_pin": s.project(["old_pin"], now=10)["status"],
            "future_pin": s.project(["future_pin"], now=10)["status"],
            "unbound_state": s.state("unbound", 10)["state"],
            "old_pin_state": s.state("old_pin", 10)["state"],
            "future_pin_state": s.state("future_pin", 10)["state"]}

def case20(s):
    s.add(obs("a", "old"))
    s.add(obs("a", "new", seq=2, at=5))
    s.add(obs("b", "derived from new a", at=6, receipt=10, ttl=20,
              deps=("a",), pins=(("a", 2),)))
    result = s.project(["b"], now=10)
    return {"matching_pin": result["status"], "closure": result["required_closure"],
            "derived_value": result["values"]["b"]["value"],
            "observed_at": result["values"]["b"]["sources"][0]["observed_at"]}

def case21(s):
    s.add(obs("a", "old"))
    snapshot = s.project(["a"])["snapshot"]
    original = json.loads(json.dumps(snapshot))
    snapshot["versions"] = {}
    s.add(obs("a", "new", seq=2, at=1))
    damaged = s.validate(snapshot, 1)
    return {"damaged": damaged["status"], "original_changed": s.validate(original, 1)["status"],
            "modification_detected": "SNAPSHOT_NOT_ISSUED_OR_MODIFIED" in damaged["reasons"]}

CASES = [case01, case02, case03, case04, case05, case06, case07, case08, case09,
         case10, case11, case12, case13, case14, case15, case16, case17, case18,
         case19, case20, case21]

class NoFreshnessGuard(Model):
    def _temporal_state(self, observation, now):
        return "KNOWN"

class NoDependencyClosure(Model):
    def _closure(self, scope, keys):
        return sorted(set(keys)), []

class NoScopeBinding(Model):
    def _scope_matches(self, snapshot, scope):
        return True

def run_case(case, expected, model_type=Model):
    scenario = Scenario(model_type)
    try:
        actual = case(scenario)
        return {"id": expected["id"], "description": expected["description"],
                "expected": expected["expected"], "actual": actual,
                "passed": actual == expected["expected"], "trace": scenario.trace}
    except Exception as error:
        return {"id": expected["id"], "description": expected["description"],
                "expected": expected["expected"], "actual": None, "passed": False,
                "error": type(error).__name__ + ": " + str(error), "trace": scenario.trace}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, default=ROOT / "evidence/finite-run.json")
    args = parser.parse_args()
    expected = json.loads((ROOT / "checks/expected.json").read_text())
    if len(expected) != 21 or [e["id"] for e in expected] != list(range(1, 22)):
        raise ValueError("expected fixture must enumerate 18 declared and 3 review controls")
    results = [run_case(case, item) for case, item in zip(CASES, expected)]
    mutations = []
    for name, model_type, index in [
        ("disabled_freshness_guard", NoFreshnessGuard, 0),
        ("disabled_dependency_closure", NoDependencyClosure, 10),
        ("disabled_scope_binding", NoScopeBinding, 9),
    ]:
        result = run_case(CASES[index], expected[index], model_type)
        mutations.append({"mutation": name, "detected": not result["passed"],
                          "completed_without_exception": "error" not in result, "control": result})
    paths = [ROOT / "checks/DESIGN_INPUT.md", ROOT / "situation.py",
             ROOT / "checks/check_agent_situation.py", ROOT / "checks/expected.json",
             ROOT / "README.md"]
    digests = {str(path.relative_to(ROOT)):
               {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "bytes": len(path.read_bytes())} for path in paths}
    passed = sum(r["passed"] for r in results)
    detected = sum(m["detected"] and m["completed_without_exception"] for m in mutations)
    evidence = {
        "schema": "agent-situation-finite-evidence-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python3 " + str(Path(__file__).resolve()) + " --evidence " + str(args.evidence.resolve()),
        "python": platform.python_version(),
        "provenance": {
            "design": "author-designed predeclared finite contract, not independent preregistration",
            "fixtures": "hand-authored expected outcomes",
            "implementation_and_runner": "same implementing agent",
            "actual_independence": "NOT_VERIFIED",
            "source_identities_authenticated": False,
            "native_agent_runtime_observed": False,
            "native_admission": "NOT_VERIFIED",
            "external_effects_executed": False,
            "llm_calls": 0,
            "network_calls": 0,
            "grants_implemented": False,
        },
        "counts": {"declared_controls": 18, "review_added_controls": 3, "executed_controls": len(results),
                   "passed_controls": passed, "failed_controls": len(results) - passed,
                   "mutation_controls": len(mutations), "mutations_detected": detected,
                   "expected_fields_checked": sum(len(e["expected"]) for e in expected)},
        "result": "FINITE_CONTROLS_PASS" if passed == len(results) and detected == 3 else "FINITE_CONTROLS_FAIL",
        "development_history": {
            "initial_suite": "18/18 passed and 3/3 mutants detected, but missed a material delayed-derivation bug",
            "review": "same-controller non-author inspection; actual independence NOT_VERIFIED",
            "counterexample": "development/v1/delayed-derivation-counterexample.json",
            "correction": "explicit dependency version pins, derivation-time check, and issued-snapshot integrity check",
        },
        "unimplemented": [
            "real sensors, tools, permissions, effects, LLM context/token accounting",
            "distributed clock synchronization and restart recovery",
            "causal ordering across independent producer streams",
            "persistence, authenticated sources/snapshots, adversarial access control",
            "optimal refresh scheduling, calibrated uncertainty or value of information",
            "general autonomous intentions, empirical agent outcomes and native admission",
        ],
        "limitations": [
            "One synthetic integer clock domain; clock regression stays invalid until a new model.",
            "The finite authored cases are not exhaustive, independent, or an external benchmark.",
            "Abstract positive integer costs are not measured model tokens.",
            "All source conflicts are conservatively retained; there is no trust-ranking adjudication.",
            "Refresh flags request a hypothetical rebuild or observation; no external call is made.",
            "A false fixture can be structurally ready; readiness never grants permission.",
        ],
        "source_digests": digests, "controls": results, "negative_controls": mutations,
    }
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    summary = (
        evidence["command"] + "\n" + evidence["result"] + "\n" +
        f"Authored controls: {passed}/{len(results)} (18 declared + 3 review); disabled-guard mutations detected: {detected}/3.\n" +
        "Native admission: NOT_VERIFIED; no LLM, network, grant authority, or effects.\n"
    )
    (ROOT / "evidence/execution.txt").write_text(summary)
    print(summary, end="")
    for result in results:
        if not result["passed"]:
            print(json.dumps({k: v for k, v in result.items() if k != "trace"}, sort_keys=True))
    return 0 if evidence["result"] == "FINITE_CONTROLS_PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())

