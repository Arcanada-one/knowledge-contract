# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Bounded start/resume/preflight around the unchanged offline Git observer.

Receipts describe file identities at one capture, not continuous availability,
producer authentication or effect permission. Inspecting an old receipt is
historical only. Every successful start/resume/preflight invocation acquires one
fresh capture; a preflight checks the predecessor context rather than silently
substituting a newly projected context after a relevant change.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile

try:
    from tools import repository_observer as observer
except ImportError:
    import repository_observer as observer


PROFILE_SCHEMA = "repository-session-profile/1"
RECEIPT_SCHEMA = "repository-session/1"
HEX = re.compile(r"[0-9a-f]{64}\Z")
PROFILE_KEYS = {"schema", "task_id", "scope", "repository_root_digest", "paths",
                "required_paths", "producer", "budget"}
RECEIPT_KEYS = {"schema", "operation", "sequence", "profile", "profile_digest",
                "predecessor", "ledger", "ledger_head", "capture_id", "observed_at",
                "implementation", "context", "context_id", "prior_validation",
                "result", "history_complete", "not_observed", "llm_calls",
                "readiness_grants_permission", "receipt_id"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member: " + key)
        result[key] = value
    return result


def _nonfinite(value):
    raise ValueError("non-finite JSON value: " + value)


def read_json(path):
    """Reject duplicate object members at every nesting level before interpretation."""
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=_unique_pairs, parse_constant=_nonfinite)


def _label(value, name):
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        raise ValueError(name + " must be nonempty text without control characters")
    return value


def _paths(values):
    if not isinstance(values, (list, tuple)) or not 1 <= len(values) <= 32:
        raise ValueError("select 1..32 explicit paths")
    for value in values:
        if not isinstance(value, str) or not value or "\\" in value or any(ord(c) < 32 for c in value):
            raise ValueError("invalid selected path")
        path = PurePosixPath(value)
        if (path.is_absolute() or not path.parts or str(path) != value
                or any(part.casefold() in {".", "..", ".git"} for part in path.parts)):
            raise ValueError("selected path is not normalized and relative")
    if len(set(values)) != len(values):
        raise ValueError("duplicate selected path")
    return sorted(values)


def _root_digest(repo):
    # A local address binding, not proof of repository identity or ownership.
    return digest({"resolved_local_root": str(Path(repo).resolve())})


def make_profile(repo, task_id, scope, paths, required_paths=None, *,
                 producer="local-git", budget=10000):
    profile = {"schema": PROFILE_SCHEMA, "task_id": task_id, "scope": scope,
               "repository_root_digest": _root_digest(repo), "paths": _paths(paths),
               "required_paths": _paths(paths if required_paths is None else required_paths),
               "producer": producer, "budget": budget}
    return validate_profile(profile)


def validate_profile(profile):
    if not isinstance(profile, dict) or set(profile) != PROFILE_KEYS or profile["schema"] != PROFILE_SCHEMA:
        raise ValueError("unsupported or incomplete task profile")
    for key in ("task_id", "scope", "producer"):
        _label(profile[key], key)
    if not isinstance(profile["repository_root_digest"], str) or not HEX.fullmatch(profile["repository_root_digest"]):
        raise ValueError("invalid local repository binding")
    if any(_paths(profile[key]) != profile[key] for key in ("paths", "required_paths")):
        raise ValueError("profile paths must be sorted and normalized")
    if not set(profile["required_paths"]) <= set(profile["paths"]):
        raise ValueError("required path is outside observation profile")
    if type(profile["budget"]) is not int or profile["budget"] < 0:
        raise ValueError("budget must be a nonnegative integer of abstract model units")
    return profile


def _implementation():
    root = Path(observer.__file__).resolve().parents[1]
    paths = {"session": Path(__file__), "observer": Path(observer.__file__),
             "model": root / "engineering/studies/agent-situation-controls/situation.py"}
    return {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in paths.items()}


def _context(step, profile):
    context = step["context"]
    # Omit process-local model identity, generation counters and source timestamps
    # from semantic identity. Full source records remain in the verified ledger.
    dependencies = {}
    for path in profile["required_paths"]:
        value = context["values"].get(observer.file_key(path))
        dependencies[path] = ({"state": value["state"], "value": value["value"]}
                              if value else {"state": "NOT_PROJECTED", "value": None})
    return {"status": context["status"], "required_paths": list(profile["required_paths"]),
            "required_cost": context["required_cost"], "cost": context["cost"],
            "budget": context["budget"], "dependencies": dependencies,
            "reasons": context["reasons"]}


def _context_id(context, profile):
    return digest({"profile_digest": digest(profile), "context": context})


def _replay(ledger, profile):
    replay = observer.replay_ledger(ledger, profile["required_paths"], profile["budget"])
    captures = [entry["capture"] for entry in ledger["entries"]]
    if len({capture["capture_id"] for capture in captures}) != len(captures):
        raise ValueError("session ledger repeats an old capture")
    for capture in captures:
        if (capture["scope"] != profile["scope"] or capture["paths"] != profile["paths"]
                or capture["producer"] != profile["producer"]):
            raise ValueError("capture differs from the frozen task profile")
    return replay, captures


def _result(operation, context, prior_validation):
    if context["status"] != "READY":
        return context["status"]
    if operation == "PREFLIGHT":
        return "VALID" if prior_validation and prior_validation["status"] == "VALID" else "INVALID"
    return "READY"


def validate_receipt(receipt):
    """Validate internal consistency with this implementation; authenticate nothing."""
    if not isinstance(receipt, dict) or set(receipt) != RECEIPT_KEYS or receipt["schema"] != RECEIPT_SCHEMA:
        raise ValueError("unsupported or incomplete session receipt")
    payload = {key: value for key, value in receipt.items() if key != "receipt_id"}
    if receipt["receipt_id"] != digest(payload):
        raise ValueError("session receipt digest mismatch")
    profile = validate_profile(receipt["profile"])
    if receipt["profile_digest"] != digest(profile):
        raise ValueError("task profile digest mismatch")
    if receipt["implementation"] != _implementation():
        raise ValueError("receipt belongs to another implementation; explicit migration required")
    operation = receipt["operation"]
    if operation not in {"START", "RESUME", "PREFLIGHT"}:
        raise ValueError("unknown session operation")
    replay, captures = _replay(receipt["ledger"], profile)
    count = len(captures)
    if type(receipt["sequence"]) is not int or receipt["sequence"] != count:
        raise ValueError("session capture inventory mismatch")
    if (operation == "START") != (count == 1):
        raise ValueError("session operation does not match its capture inventory")
    last = captures[-1]
    if (receipt["ledger_head"] != receipt["ledger"]["head_hash"]
            or receipt["capture_id"] != last["capture_id"]
            or receipt["observed_at"] != last["observed_at"]):
        raise ValueError("receipt is not bound to its final capture")
    context = _context(replay["steps"][-1], profile)
    if canonical(receipt["context"]) != canonical(context) or receipt["context_id"] != _context_id(context, profile):
        raise ValueError("context does not match verified observation replay")
    prior_validation = replay["steps"][-1]["prior_validation"] if count > 1 else None
    if receipt["prior_validation"] != prior_validation or receipt["result"] != _result(operation, context, prior_validation):
        raise ValueError("session result does not match revalidation")
    predecessor = receipt["predecessor"]
    if count == 1:
        if predecessor is not None:
            raise ValueError("start receipt has a predecessor")
    else:
        keys = {"receipt_id", "sequence", "profile_digest", "ledger_head", "context_id"}
        if not isinstance(predecessor, dict) or set(predecessor) != keys:
            raise ValueError("missing predecessor binding")
        if not isinstance(predecessor["receipt_id"], str) or not HEX.fullmatch(predecessor["receipt_id"]):
            raise ValueError("invalid predecessor receipt identity")
        old_context = _context(replay["steps"][-2], profile)
        if (type(predecessor["sequence"]) is not int or predecessor["sequence"] != count - 1
                or predecessor["profile_digest"] != digest(profile)
                or predecessor["ledger_head"] != receipt["ledger"]["entries"][-2]["hash"]
                or predecessor["context_id"] != _context_id(old_context, profile)):
            raise ValueError("predecessor disagrees with retained ledger prefix")
    if (receipt["history_complete"] is not False or receipt["readiness_grants_permission"] is not False
            or type(receipt["llm_calls"]) is not int or receipt["llm_calls"] != 0
            or receipt["not_observed"] != observer.NOT_OBSERVED):
        raise ValueError("unsupported session claim")
    return receipt


def _advance(repo, profile, previous, operation):
    validate_profile(profile)
    if _root_digest(repo) != profile["repository_root_digest"]:
        raise ValueError("repository root differs from the frozen profile")
    if previous is None:
        if operation != "START":
            raise ValueError("resume and preflight require a predecessor")
        captures, predecessor = [], None
    else:
        validate_receipt(previous)
        if previous["profile"] != profile:
            raise ValueError("task/scope/profile differs from the predecessor")
        # Return a successor without mutable aliases into the caller's predecessor.
        retained = json.loads(canonical(previous["ledger"]))
        captures = [entry["capture"] for entry in retained["entries"]]
        predecessor = {key: previous[key] for key in
                       ("receipt_id", "sequence", "profile_digest", "ledger_head", "context_id")}
    # This is the single acquisition call. Replay above and below does not run Git.
    fresh = observer.capture(repo, profile["paths"], profile["scope"], producer=profile["producer"])
    ledger = observer.make_ledger(captures + [fresh])
    replay, captures = _replay(ledger, profile)
    context = _context(replay["steps"][-1], profile)
    prior_validation = replay["steps"][-1]["prior_validation"] if previous else None
    receipt = {"schema": RECEIPT_SCHEMA, "operation": operation, "sequence": len(captures),
               "profile": json.loads(canonical(profile)), "profile_digest": digest(profile),
               "predecessor": predecessor, "ledger": ledger, "ledger_head": ledger["head_hash"],
               "capture_id": fresh["capture_id"], "observed_at": fresh["observed_at"],
               "implementation": _implementation(), "context": context,
               "context_id": _context_id(context, profile), "prior_validation": prior_validation,
               "result": _result(operation, context, prior_validation),
               "history_complete": False, "not_observed": list(observer.NOT_OBSERVED),
               "llm_calls": 0, "readiness_grants_permission": False}
    receipt["receipt_id"] = digest(receipt)
    return validate_receipt(receipt)


def start(repo, profile):
    return _advance(repo, profile, None, "START")


def resume(repo, profile, previous):
    return _advance(repo, profile, previous, "RESUME")


def preflight(repo, profile, previous):
    return _advance(repo, profile, previous, "PREFLIGHT")


def inspect_receipt(receipt):
    validate_receipt(receipt)
    return {"view": "HISTORICAL_ONLY", "receipt_id": receipt["receipt_id"],
            "context_id": receipt["context_id"], "captured_result": receipt["result"],
            "observed_at": receipt["observed_at"], "requires_fresh_capture": True,
            "readiness_grants_permission": False}


def write_new_json(path, value):
    """Publish one complete new JSON file without replacing any existing path."""
    target = Path(path)
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode("utf-8") + b"\n"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".session-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        # Same-directory hard-link publication is exclusive and does not expose
        # a partial destination. This is local evidence storage, not an effect API.
        os.link(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    profile = commands.add_parser("profile")
    profile.add_argument("--repo", required=True)
    profile.add_argument("--task-id", required=True)
    profile.add_argument("--scope", required=True)
    profile.add_argument("--path", action="append", required=True)
    profile.add_argument("--required-path", action="append")
    profile.add_argument("--producer", default="local-git")
    profile.add_argument("--budget", type=int, default=10000)
    profile.add_argument("--output", required=True)
    for name in ("start", "resume", "preflight"):
        command = commands.add_parser(name)
        command.add_argument("--repo", required=True)
        command.add_argument("--profile", required=True)
        if name != "start":
            command.add_argument("--previous", required=True)
        command.add_argument("--output", required=True)
    inspect = commands.add_parser("inspect")
    inspect.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            print(json.dumps(inspect_receipt(read_json(args.input)), sort_keys=True))
            return 0
        if Path(args.output).exists() or Path(args.output).is_symlink():
            raise ValueError("output already exists; predecessors are never overwritten")
        root, target = Path(args.repo).resolve(), Path(args.output).resolve()
        if target == root or root in target.parents:
            raise ValueError("session output must be outside the observed repository")
        if args.command == "profile":
            value = make_profile(args.repo, args.task_id, args.scope, args.path, args.required_path,
                                 producer=args.producer, budget=args.budget)
            write_new_json(args.output, value)
            print(json.dumps({"profile_digest": digest(value)}, sort_keys=True))
            return 0
        profile = validate_profile(read_json(args.profile))
        if args.command == "start":
            receipt = start(args.repo, profile)
        else:
            previous = read_json(args.previous)
            receipt = (resume if args.command == "resume" else preflight)(args.repo, profile, previous)
        write_new_json(args.output, receipt)
        print(json.dumps({"view": "OBSERVED_THIS_INVOCATION", "receipt_id": receipt["receipt_id"],
                          "context_id": receipt["context_id"], "result": receipt["result"],
                          "observed_at": receipt["observed_at"], "sequence": receipt["sequence"],
                          "readiness_grants_permission": False}, sort_keys=True))
        return 0 if receipt["result"] in {"READY", "VALID"} else 1
    except (ValueError, OSError, KeyError, TypeError, UnicodeError) as exc:
        print("repository session: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
