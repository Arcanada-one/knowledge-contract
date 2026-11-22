#!/usr/bin/env python3
"""Reproduce work-before-cap on a retained baseline or its successor.

One actual local Git capture supplies valid byte records. Larger histories below
are deliberately synthetic input mutations, not claims of 32/33 real captures.
The observer replay wrapper records calls while executing the unchanged replay.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--module-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(args.module_root))
    from tools import repository_rule_consumer as consumer
    session = consumer.session
    observer = session.observer

    expectation = {
        "scope": "synthetic oversized-input rejection order; one actual Git seed capture",
        "valid_32": "accept with real replay",
        "over_33": "refuse before any ledger replay",
        "false_sequence_with_33_entries": "refuse before any ledger replay",
        "independence": "non-author role, same controller and workspace",
    }
    write_json(args.output / "expectations.json", expectation)
    with tempfile.TemporaryDirectory(prefix="consumer-review-") as temp:
        repo = Path(temp) / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        source = b"RULE r1: TRUE\n"
        packet = {
            "schema": "kc-semantic-bridge/1",
            "source_sha256": hashlib.sha256(source).hexdigest(),
            "source_media_type": "text/plain", "interpretation_set": "alternatives",
            "observations": {},
            "readings": [{"id": "r1", "start": 0, "end": len(source) - 1,
                          "quote": source[:-1].decode(),
                          "attribution": {"agent": "review_fixture", "discourse": "hypothetical"},
                          "bindings": {}}],
        }
        (repo / "source.txt").write_bytes(source)
        write_json(repo / "packet.json", packet)
        subprocess.run(["git", "-C", str(repo), "add", "source.txt", "packet.json"], check=True)
        subprocess.run(["git", "-C", str(repo), "-c", "user.name=Review Fixture",
                        "-c", "user.email=review@example.invalid", "-c", "commit.gpgsign=false",
                        "commit", "-qm", "Controlled local review fixture"], check=True)
        seed = consumer.start(repo, "source.txt", "packet.json", task_id="review", scope="review")
        write_json(args.output / "actual-seed-start.json", seed)
        captures = []
        initial = seed["session"]["ledger"]["entries"][0]["capture"]
        for index in range(33):
            capture = copy.deepcopy(initial)
            capture["started_at"] += index
            capture["observed_at"] += index
            capture["capture_id"] = observer.digest({k: v for k, v in capture.items() if k != "capture_id"})
            captures.append(capture)

        def synthetic_bundle(count):
            receipt = copy.deepcopy(seed["session"])
            ledger = observer.make_ledger(captures[:count])
            replay, _ = session._replay(ledger, receipt["profile"])
            operations = ["START"] + ["PREFLIGHT"] * (count - 1)
            states = session._states(replay, receipt["profile"], operations)
            predecessor = {
                "receipt_id": "a" * 64, "sequence": count - 1,
                "profile_digest": receipt["profile_digest"],
                "ledger_head": ledger["entries"][-2]["hash"],
                "context_id": states[-2]["context_id"],
                "adopted_context_id": states[-2]["adopted_context_id"],
                "resume_required": states[-2]["resume_required"],
                "operations_digest": session.digest(operations[:-1]),
            }
            receipt.update(operation="PREFLIGHT", sequence=count,
                           predecessor=predecessor, ledger=ledger, ledger_head=ledger["head_hash"],
                           capture_id=captures[count - 1]["capture_id"],
                           observed_at=captures[count - 1]["observed_at"], operations=operations,
                           **states[-1])
            receipt["receipt_id"] = session.digest({k: v for k, v in receipt.items() if k != "receipt_id"})
            return consumer._bundle("EVALUATE", receipt, seed["inputs"],
                                    previous={"receipt_id": "b" * 64,
                                              "session": {"receipt_id": "a" * 64}})

        inputs = {"valid_32": synthetic_bundle(32), "over_33": synthetic_bundle(33)}
        wrong = copy.deepcopy(inputs["over_33"])
        wrong["session"]["sequence"] = 2
        wrong["session"]["receipt_id"] = session.digest({k: v for k, v in wrong["session"].items() if k != "receipt_id"})
        wrong["receipt_id"] = session.digest({k: v for k, v in wrong.items() if k != "receipt_id"})
        inputs["false_sequence_with_33_entries"] = wrong
        rows = {}
        for name, bundle in inputs.items():
            write_json(args.output / (name + ".json"), bundle)
            calls = []
            original = observer.replay_ledger

            def counted(*positional, **keywords):
                ledger = positional[0]
                calls.append(len(ledger["entries"]))
                return original(*positional, **keywords)

            observer.replay_ledger = counted
            try:
                consumer.validate_bundle(bundle)
                outcome, error = "ACCEPTED", None
            except (ValueError, TypeError, KeyError, RecursionError) as exc:
                outcome, error = "REFUSED", str(exc)
            finally:
                observer.replay_ledger = original
            rows[name] = {"outcome": outcome, "error": error,
                          "actual_replay_entry_counts": calls,
                          "input_bytes": (args.output / (name + ".json")).stat().st_size}
        result = {"expectation": expectation,
                  "module_sha256": hashlib.sha256(Path(consumer.__file__).read_bytes()).hexdigest(),
                  "bridge_sha256": hashlib.sha256(Path(consumer.bridge.__file__).read_bytes()).hexdigest(),
                  "results": rows}
        result["pass"] = (rows["valid_32"]["outcome"] == "ACCEPTED"
                          and rows["valid_32"]["actual_replay_entry_counts"] == [32]
                          and all(rows[name]["outcome"] == "REFUSED"
                                  and rows[name]["actual_replay_entry_counts"] == []
                                  for name in ("over_33", "false_sequence_with_33_entries")))
        write_json(args.output / "RESULT.json", result)
        print(json.dumps(result, indent=2))
        return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
