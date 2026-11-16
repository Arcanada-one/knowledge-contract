# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Evaluate captured rule bytes after explicit repository-context adoption.

Offline laboratory adapter: committed source and packet are the complete file
dependency profile. A fresh preflight precedes each new calculation. Working
tree contents, authority, external effects and continuous freshness are outside
this profile. A saved bundle is historical evidence, not a live permission.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys

try:
    from tools import repository_session as session
    from tools import semantic_bridge as bridge
except ImportError:
    import repository_session as session
    import semantic_bridge as bridge


SCHEMA = "repository-rule-consumption/1"
MAX_CAPTURES = 32
MAX_BUNDLE_BYTES = 32 * 1024 * 1024
OPERATIONS = {"START": "START", "RESUME": "RESUME", "EVALUATE": "PREFLIGHT"}
BUNDLE_KEYS = {"schema", "operation", "inputs", "session", "bindings", "analysis",
               "result", "predecessor", "implementation", "evidence_scope",
               "history_complete", "effects_authorized", "llm_calls", "receipt_id"}
EVIDENCE_SCOPE = "committed-files-at-capture"


def _implementation():
    return {name: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
            for name, module in (("consumer", sys.modules[__name__]), ("bridge", bridge))}


def _inputs(inputs, profile):
    if (type(inputs) is not dict or set(inputs) != {"source", "packet"}
            or any(type(value) is not str for value in inputs.values())):
        raise ValueError("source and packet must be explicit relative paths")
    paths = session._paths([inputs["source"], inputs["packet"]])
    if profile["paths"] != paths or profile["required_paths"] != paths:
        raise ValueError("both input files must be the complete required context")
    return inputs


def _analysis(source, packet):
    try:
        parsed = bridge.parse_packet_bytes(packet)
    except bridge.BridgeError as error:
        result = bridge._base_report()
        result.update(status=error.status,
                      errors=[{"code": error.code, "message": str(error), **error.details}])
        return result
    return bridge.analyze(source, parsed)


def _derive(operation, receipt, inputs):
    """Replay this bundle's result; this function never reads files from repo."""
    if operation != "EVALUATE":
        return receipt["result"], None, None
    if receipt["result"] != "VALID":
        return "BLOCKED", None, None
    if receipt["resume_required"] or receipt["context_id"] != receipt["adopted_context_id"]:
        raise ValueError("calculation requires the explicitly adopted context")
    capture = receipt["ledger"]["entries"][-1]["capture"]
    if capture["status"] != "OK":
        raise ValueError("calculation requires a completed stable-HEAD capture")
    raw, identities = {}, {}
    for role, path in inputs.items():
        entry = capture["files"][path]
        dependency = receipt["context"]["dependencies"][path]
        if entry["state"] != "PRESENT" or dependency["state"] != "KNOWN":
            raise ValueError("calculation requires known committed input bytes")
        identity = {key: entry[key] for key in ("blob", "mode", "size", "sha256")}
        if session.canonical(identity) != session.canonical(dependency["value"]):
            raise ValueError("captured bytes differ from adopted dependency identity")
        raw[role] = base64.b64decode(entry["content_b64"], validate=True)
        identities[role] = {"path": path, **identity}
    bindings = {"capture_id": capture["capture_id"], "context_id": receipt["context_id"],
                "head": capture["head_start"], "tree": capture["tree"], "files": identities}
    analysis = _analysis(raw["source"], raw["packet"])
    return analysis["status"], bindings, analysis


def validate_bundle(bundle):
    """Replay internal consistency, including historical calculation, not freshness.

The hash chain is unauthenticated and may be rewritten as a whole. The caller
selects a predecessor; this adapter does not enforce a unique global history.
"""
    if type(bundle) is not dict or set(bundle) != BUNDLE_KEYS or bundle["schema"] != SCHEMA:
        raise ValueError("unsupported or incomplete consumer bundle")
    if bundle["receipt_id"] != session.digest({k: v for k, v in bundle.items() if k != "receipt_id"}):
        raise ValueError("consumer bundle digest mismatch")
    operation = bundle["operation"]
    if type(operation) is not str or operation not in OPERATIONS:
        raise ValueError("unknown consumer operation")
    if bundle["implementation"] != _implementation():
        raise ValueError("consumer implementation changed; explicit migration required")
    receipt = session.validate_receipt(bundle["session"])
    if receipt["operation"] != OPERATIONS[operation]:
        raise ValueError("consumer operation differs from session operation")
    if receipt["sequence"] > MAX_CAPTURES:
        raise ValueError("consumer capture bound exceeded")
    inputs = _inputs(bundle["inputs"], receipt["profile"])
    predecessor = bundle["predecessor"]
    if operation == "START":
        if predecessor is not None:
            raise ValueError("start bundle has a predecessor")
    elif (type(predecessor) is not dict
          or set(predecessor) != {"receipt_id", "session_receipt_id"}
          or type(predecessor["receipt_id"]) is not str
          or not session.HEX.fullmatch(predecessor["receipt_id"])
          or predecessor["session_receipt_id"] != receipt["predecessor"]["receipt_id"]):
        raise ValueError("consumer predecessor differs from session predecessor")
    result, bindings, analysis = _derive(operation, receipt, inputs)
    for key, expected in (("result", result), ("bindings", bindings), ("analysis", analysis)):
        if session.canonical(bundle[key]) != session.canonical(expected):
            raise ValueError(key + " differs from captured-input replay")
    if (bundle["evidence_scope"] != EVIDENCE_SCOPE or bundle["history_complete"] is not False
            or bundle["effects_authorized"] is not False
            or type(bundle["llm_calls"]) is not int or bundle["llm_calls"] != 0):
        raise ValueError("unsupported consumer claim")
    return bundle


def _bundle(operation, receipt, inputs, previous=None):
    result, bindings, analysis = _derive(operation, receipt, inputs)
    bundle = {"schema": SCHEMA, "operation": operation, "inputs": dict(inputs),
              "session": receipt, "result": result, "bindings": bindings, "analysis": analysis,
              "predecessor": ({"receipt_id": previous["receipt_id"],
                               "session_receipt_id": previous["session"]["receipt_id"]}
                              if previous is not None else None),
              "implementation": _implementation(), "evidence_scope": EVIDENCE_SCOPE,
              "history_complete": False, "effects_authorized": False, "llm_calls": 0}
    bundle["receipt_id"] = session.digest(bundle)
    return bundle


def start(repo, source_path, packet_path, *, task_id, scope, producer="local-git", budget=10000):
    inputs = {"source": source_path, "packet": packet_path}
    profile = session.make_profile(repo, task_id, scope, [source_path, packet_path],
                                   producer=producer, budget=budget)
    _inputs(inputs, profile)
    return _bundle("START", session.start(repo, profile), inputs)


def advance(repo, previous, operation):
    if operation not in {"RESUME", "EVALUATE"}:
        raise ValueError("advance requires RESUME or EVALUATE")
    validate_bundle(previous)
    if previous["session"]["sequence"] >= MAX_CAPTURES:
        raise ValueError("consumer capture bound reached; no silent history truncation")
    method = session.resume if operation == "RESUME" else session.preflight
    fresh = method(repo, previous["session"]["profile"], previous["session"])
    return _bundle(operation, fresh, previous["inputs"], previous)


def inspect_bundle(bundle):
    validate_bundle(bundle)
    return {"view": "HISTORICAL_ONLY", "receipt_id": bundle["receipt_id"],
            "captured_result": bundle["result"], "evidence_scope": EVIDENCE_SCOPE,
            "adopted_context_id": bundle["session"]["adopted_context_id"],
            "resume_required": bundle["session"]["resume_required"],
            "requires_fresh_capture": True, "effects_authorized": False}


def read_bundle(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_BUNDLE_BYTES + 1)
    if len(raw) > MAX_BUNDLE_BYTES:
        raise ValueError("consumer bundle exceeds byte bound")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=session._unique_pairs,
                      parse_constant=session._nonfinite)


def _exit_code(bundle):
    if bundle["result"] in {"READY", "EVALUATED"}:
        return 0
    return 1 if bundle["result"] in {"BLOCKED", "NOT_READY", "NOT_FIT"} else 2


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("start")
    create.add_argument("--repo", required=True)
    create.add_argument("--source-path", required=True)
    create.add_argument("--packet-path", required=True)
    create.add_argument("--task-id", required=True)
    create.add_argument("--scope", required=True)
    create.add_argument("--producer", default="local-git")
    create.add_argument("--budget", type=int, default=10000)
    create.add_argument("--output", required=True)
    for name in ("resume", "evaluate"):
        command = commands.add_parser(name)
        command.add_argument("--repo", required=True)
        command.add_argument("--previous", required=True)
        command.add_argument("--output", required=True)
    inspect = commands.add_parser("inspect")
    inspect.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            print(json.dumps(inspect_bundle(read_bundle(args.input)), sort_keys=True))
            return 0
        target, repo = Path(args.output), Path(args.repo).resolve()
        if target.exists() or target.is_symlink():
            raise ValueError("output exists; previous evidence is never replaced")
        resolved = target.resolve()
        if resolved == repo or repo in resolved.parents:
            raise ValueError("consumer output must be outside the observed repository")
        if args.command == "start":
            bundle = start(repo, args.source_path, args.packet_path, task_id=args.task_id,
                           scope=args.scope, producer=args.producer, budget=args.budget)
        else:
            bundle = advance(repo, read_bundle(args.previous), args.command.upper())
        serialized = json.dumps(bundle, ensure_ascii=False, sort_keys=True, indent=2,
                                allow_nan=False).encode("utf-8") + b"\n"
        if len(serialized) > MAX_BUNDLE_BYTES:
            raise ValueError("consumer result exceeds byte bound; no result was published")
        session.write_new_json(target, bundle)
        print(json.dumps({"view": "OBSERVED_THIS_INVOCATION", "receipt_id": bundle["receipt_id"],
                          "result": bundle["result"], "session_result": bundle["session"]["result"],
                          "sequence": bundle["session"]["sequence"],
                          "effects_authorized": False}, sort_keys=True))
        return _exit_code(bundle)
    except (ValueError, OSError, KeyError, TypeError, UnicodeError, RecursionError) as error:
        print("repository rule consumer: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
