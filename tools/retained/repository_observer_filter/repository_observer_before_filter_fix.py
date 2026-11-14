"""Read committed local Git files and replay receipts into the situation model.

Repository-only research adapter. No fetch, network client, model call, effect,
grant, or runtime admission. Receipt hashes detect inconsistent records; they
do not authenticate a producer or prove that unobserved changes did not occur.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import time

CAPTURE_SCHEMA = "repository-observation/1"
LEDGER_SCHEMA = "repository-observation-ledger/1"
CLOCK_DOMAIN = "unix-nanoseconds"
NOT_OBSERVED = ["ci", "effect_outcome", "authority"]
GIT_OPTIONS = ["--no-pager", "--literal-pathspecs", "--no-optional-locks",
               "-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false",
               "-c", "submodule.recurse=false", "-c", "protocol.allow=never"]
OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def _encoded(value):
    return base64.b64encode(value).decode("ascii")


def _decoded(value):
    if not isinstance(value, str):
        raise ValueError("base64 content must be text")
    try:
        return base64.b64decode(value, validate=True)
    except (ValueError, TypeError) as exc:
        raise ValueError("invalid base64 content") from exc


def _paths(paths):
    if not isinstance(paths, (list, tuple)) or not 1 <= len(paths) <= 32:
        raise ValueError("select between 1 and 32 explicit file paths")
    result = []
    for value in paths:
        if (not isinstance(value, str) or not value or "\x00" in value
                or "\\" in value or any(ord(c) < 32 for c in value)):
            raise ValueError("file path must be normalized relative text")
        path = PurePosixPath(value)
        if (path.is_absolute() or str(path) != value
                or any(part in {".", "..", ".git"} for part in path.parts)):
            raise ValueError("path escapes or is not a normalized file path")
        result.append(value)
    if len(set(result)) != len(result):
        raise ValueError("duplicate selected path")
    return sorted(result)


def _label(value, label):
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        raise ValueError(label + " must be nonempty text without control characters")
    return value


def _git_environment():
    # Discard ambient repository/namespace overrides. No credentials/config
    # contents are read into the receipt. Per-command protocol policy also
    # prevents a partial clone from obtaining a missing object by lazy fetch.
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_TERMINAL_PROMPT="0", GIT_NO_LAZY_FETCH="1",
               GIT_NO_REPLACE_OBJECTS="1", GIT_OPTIONAL_LOCKS="0",
               LC_ALL="C")
    return env


class _ReadFailure(Exception):
    pass


def capture(repo, paths, scope, *, producer="local-git", max_blob_bytes=1048576):
    """Read only the selected committed blobs, preserving raw command outputs.

    Scope/producer are caller labels, not discovered identities or permissions.
    The adapter writes nothing in repo. Untracked file contents are not read.
    """
    paths = _paths(paths)
    _label(scope, "scope")
    _label(producer, "producer")
    if type(max_blob_bytes) is not int or not 0 < max_blob_bytes <= 1048576:
        raise ValueError("max_blob_bytes must be 1..1048576")
    repo = Path(repo).resolve()
    record = {
        "schema": CAPTURE_SCHEMA, "scope": scope, "producer": producer,
        "paths": paths, "clock_domain": CLOCK_DOMAIN,
        "started_at": time.time_ns(), "observed_at": None,
        "head_start": None, "head_end": None, "tree": None,
        "branch": None, "status": "UNAVAILABLE", "error": None,
        "files": {p: {"state": "UNAVAILABLE"} for p in paths},
        "tracked_selected_status_b64": None, "commands": [],
        "history_complete": False, "worktree_atomic": False,
        "untracked_observed": False, "not_observed": list(NOT_OBSERVED),
        "python_version": sys.version.split()[0],
    }

    def run(*args, allowed=(0,)):
        argv = ["git", *GIT_OPTIONS, *args]
        started = time.time_ns()
        try:
            completed = subprocess.run(argv, cwd=repo, env=_git_environment(),
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       timeout=10, check=False)
            code, out, err = completed.returncode, completed.stdout, completed.stderr
        except (OSError, subprocess.TimeoutExpired) as exc:
            code, out = None, b""
            # A stable exception class identifies failure without recording an
            # absolute local path or credential-bearing environment string.
            err = type(exc).__name__.encode("ascii")
        record["commands"].append({"argv": argv, "started_at": started,
                                   "finished_at": time.time_ns(), "returncode": code,
                                   "stdout_b64": _encoded(out), "stderr_b64": _encoded(err)})
        if code not in allowed:
            raise _ReadFailure("command failed: " + " ".join(args[:2]))
        return code, out

    try:
        run("--version")
        if run("rev-parse", "--show-prefix")[1] != b"\n":
            raise _ReadFailure("explicit repository root required")
        record["head_start"] = run("rev-parse", "--verify", "HEAD^{commit}")[1].strip().decode("ascii")
        if not OID.fullmatch(record["head_start"]):
            raise _ReadFailure("unsupported commit identity")
        record["tree"] = run("rev-parse", "--verify", record["head_start"] + "^{tree}")[1].strip().decode("ascii")
        code, branch = run("symbolic-ref", "--quiet", "HEAD", allowed=(0, 1))
        record["branch"] = branch.strip().decode("utf-8") if code == 0 else None
        for path in paths:
            listing = run("ls-tree", "-z", "--full-tree", record["head_start"], "--", path)[1]
            if not listing:
                record["files"][path] = {"state": "ABSENT"}
                continue
            entries = listing.rstrip(b"\0").split(b"\0")
            if len(entries) != 1:
                raise _ReadFailure("selection did not identify one tree entry")
            meta, found_path = entries[0].split(b"\t", 1)
            mode, kind, oid = meta.decode("ascii").split(" ")
            if found_path.decode("utf-8") != path:
                raise _ReadFailure("tree entry did not match selected path")
            if mode not in {"100644", "100755"} or kind != "blob":
                record["files"][path] = {"state": "UNSUPPORTED", "mode": mode, "object": oid}
                continue
            if not OID.fullmatch(oid):
                raise _ReadFailure("unsupported blob identity")
            size = int(run("cat-file", "-s", oid)[1])
            if size > max_blob_bytes:
                record["files"][path] = {"state": "UNAVAILABLE", "reason": "BLOB_SIZE_LIMIT", "size": size}
                continue
            data = run("cat-file", "blob", oid)[1]
            if len(data) != size:
                raise _ReadFailure("blob size changed or read was incomplete")
            algorithm = hashlib.sha1 if len(oid) == 40 else hashlib.sha256
            if algorithm(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest() != oid:
                raise _ReadFailure("blob content differs from object identity")
            record["files"][path] = {"state": "PRESENT", "blob": oid, "mode": mode,
                                      "size": size, "sha256": hashlib.sha256(data).hexdigest(),
                                      "content_b64": _encoded(data)}
        status = run("status", "--porcelain=v1", "-z", "--untracked-files=no",
                     "--ignore-submodules=all", "--no-renames", "--", *paths)[1]
        record["tracked_selected_status_b64"] = _encoded(status)
        record["head_end"] = run("rev-parse", "--verify", "HEAD^{commit}")[1].strip().decode("ascii")
        record["status"] = "OK" if record["head_start"] == record["head_end"] else "CHANGED_DURING_READ"
    except (_ReadFailure, ValueError, UnicodeError) as exc:
        record["error"] = str(exc)
    record["observed_at"] = time.time_ns()
    record["capture_id"] = digest(record)
    validate_capture(record)
    return record


def validate_capture(record):
    """Check internal receipt consistency, not producer authenticity."""
    if not isinstance(record, dict) or record.get("schema") != CAPTURE_SCHEMA:
        raise ValueError("unsupported capture schema")
    payload = {k: v for k, v in record.items() if k != "capture_id"}
    if record.get("capture_id") != digest(payload):
        raise ValueError("capture digest mismatch")
    _label(record.get("scope"), "scope")
    _label(record.get("producer"), "producer")
    paths = _paths(record.get("paths"))
    if paths != record["paths"] or set(record.get("files", {})) != set(paths):
        raise ValueError("capture file inventory mismatch")
    if record.get("clock_domain") != CLOCK_DOMAIN:
        raise ValueError("unsupported observation clock")
    if any(type(record.get(k)) is not int or record[k] < 0 for k in ("started_at", "observed_at")):
        raise ValueError("invalid capture timestamps")
    if record["observed_at"] < record["started_at"]:
        raise ValueError("clock moved backwards during capture")
    if record.get("status") not in {"OK", "CHANGED_DURING_READ", "UNAVAILABLE"}:
        raise ValueError("unsupported capture state")
    if record["status"] != "UNAVAILABLE":
        if not all(isinstance(record.get(k), str) and OID.fullmatch(record[k])
                   for k in ("head_start", "head_end", "tree")):
            raise ValueError("missing pinned Git identities")
        if (record["head_start"] == record["head_end"]) != (record["status"] == "OK"):
            raise ValueError("HEAD consistency state mismatch")
        _decoded(record["tracked_selected_status_b64"])
    if not isinstance(record.get("commands"), list) or not record["commands"]:
        raise ValueError("missing command evidence")
    for command in record["commands"]:
        if not isinstance(command.get("argv"), list) or command["argv"][:1] != ["git"]:
            raise ValueError("unsupported command evidence")
        _decoded(command.get("stdout_b64"))
        _decoded(command.get("stderr_b64"))
    for file in record["files"].values():
        if file.get("state") not in {"PRESENT", "ABSENT", "UNAVAILABLE", "UNSUPPORTED"}:
            raise ValueError("unsupported file state")
        if file["state"] == "PRESENT":
            data = _decoded(file.get("content_b64"))
            oid = file.get("blob", "")
            if not isinstance(oid, str) or not OID.fullmatch(oid):
                raise ValueError("invalid blob identity")
            algorithm = hashlib.sha1 if len(oid) == 40 else hashlib.sha256
            if (type(file.get("size")) is not int or file["size"] != len(data)
                    or file.get("mode") not in {"100644", "100755"}
                    or file.get("sha256") != hashlib.sha256(data).hexdigest()
                    or oid != algorithm(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()):
                raise ValueError("recorded blob bytes do not match their identities")
    if (record.get("history_complete") is not False or record.get("worktree_atomic") is not False
            or record.get("untracked_observed") is not False or record.get("not_observed") != NOT_OBSERVED):
        raise ValueError("unsupported observation claim")
    return record


def compare_captures(before, after):
    validate_capture(before)
    validate_capture(after)
    if any(before[k] != after[k] for k in ("scope", "producer", "paths")):
        raise ValueError("scope, producer or selected path profile changed")
    result = {"changed": [], "unchanged": [], "unavailable": [],
              "head_changed": before["head_start"] != after["head_start"],
              "history_complete": False, "not_observed": list(NOT_OBSERVED)}
    for path in before["paths"]:
        old, new = before["files"][path], after["files"][path]
        if before["status"] != "OK" or after["status"] != "OK" or any(
                v["state"] != "PRESENT" for v in (old, new)):
            result["unavailable"].append(path)
        else:
            key = "unchanged" if (old["blob"], old["mode"]) == (new["blob"], new["mode"]) else "changed"
            result[key].append(path)
    return result


def make_ledger(captures):
    if not isinstance(captures, list) or not captures:
        raise ValueError("a ledger needs at least one actual capture")
    entries, previous = [], None
    for index, record in enumerate(captures):
        validate_capture(record)
        if any(record[k] != captures[0][k] for k in ("scope", "paths", "clock_domain")):
            raise ValueError("ledger observation profile changed")
        entry = {"index": index, "previous": previous, "capture": record}
        entry["hash"] = digest(entry)
        entries.append(entry)
        previous = entry["hash"]
    return {"schema": LEDGER_SCHEMA, "count": len(entries), "entries": entries, "head_hash": previous}


def _read_ledger(ledger):
    if not isinstance(ledger, dict) or ledger.get("schema") != LEDGER_SCHEMA:
        raise ValueError("unsupported ledger schema")
    entries = ledger.get("entries")
    if not isinstance(entries, list) or not entries or type(ledger.get("count")) is not int or ledger["count"] != len(entries):
        raise ValueError("ledger inventory mismatch")
    expected = make_ledger([entry["capture"] for entry in entries])
    if canonical(expected) != canonical(ledger):
        raise ValueError("ledger chain mismatch")
    return [entry["capture"] for entry in entries]


def _reference_model():
    name = "kc_situation_reference_for_repository_observer"
    if name not in sys.modules:
        path = Path(__file__).resolve().parents[1] / "engineering/studies/agent-situation-controls/situation.py"
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise ValueError("Agent Situation reference model is unavailable")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def file_key(path):
    return "file:" + path


def replay_ledger(ledger, required_paths, budget=10000):
    """Rebuild a fresh reducer, retaining original observation times and scope.

    Context readiness concerns committed file identities. A file-only review
    does not depend on unrelated HEAD changes. No effect permission is issued.
    Budget units are model fields, not tokens or the byte size of a prompt.
    """
    captures = _read_ledger(ledger)
    required = _paths(required_paths)
    if not set(required) <= set(captures[0]["paths"]):
        raise ValueError("required path was not selected for observation")
    reference = _reference_model()
    model = reference.Model()
    scope = captures[0]["scope"]
    previous, sequence, seen, steps = {}, {}, set(), []
    snapshot = None
    for record in captures:
        if record["capture_id"] in seen:
            steps.append({"capture_id": record["capture_id"], "duplicate_capture": True,
                          "context": steps[-1]["context"], "prior_validation": None,
                          "observed_at": record["observed_at"], "events_ingested": 0})
            continue
        seen.add(record["capture_id"])
        producer, now, ingested = record["producer"], record["observed_at"], 0
        for path, file in record["files"].items():
            known = record["status"] == "OK" and file["state"] == "PRESENT"
            value = {k: file[k] for k in ("blob", "mode", "size", "sha256")} if known else None
            # Capture bytes remain in the ledger. Only identities enter this
            # narrow projector: it is not yet a serialized LLM context adapter.
            state = "KNOWN" if known else "UNKNOWN"
            slot = (producer, path)
            semantic = canonical({"state": state, "value": value})
            if previous.get(slot) == semantic:
                continue
            sequence[producer] = sequence.get(producer, 0) + 1
            result = model.ingest(reference.Observation(
                key=file_key(path), scope=scope, source=producer,
                event_id=record["capture_id"] + ":" + path, sequence=sequence[producer],
                value=value, state=state, observed_at=now, received_at=now, ttl=None))
            if result != "UPDATED":
                raise ValueError("reference model rejected a new observation: " + result)
            previous[slot] = semantic
            ingested += 1
        prior_validation = model.validate(snapshot, scope, now) if snapshot else None
        context = model.project(scope, [file_key(p) for p in required], [], now, budget)
        snapshot = context["snapshot"]
        steps.append({"capture_id": record["capture_id"], "duplicate_capture": False,
                      "observed_at": now, "context": context,
                      "prior_validation": prior_validation, "events_ingested": ingested})
    return {"scope": scope, "clock_domain": CLOCK_DOMAIN, "steps": steps,
            "not_observed": list(NOT_OBSERVED), "history_complete": False,
            "readiness_grants_permission": False, "llm_calls": 0,
            "model_source_sha256": hashlib.sha256(Path(reference.__file__).read_bytes()).hexdigest()}


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    observe = sub.add_parser("observe")
    observe.add_argument("--repo", required=True)
    observe.add_argument("--scope", required=True)
    observe.add_argument("--producer", default="local-git")
    observe.add_argument("--path", action="append", required=True)
    observe.add_argument("--previous")
    observe.add_argument("--output", required=True)
    replay = sub.add_parser("replay")
    replay.add_argument("--input", required=True)
    replay.add_argument("--path", action="append", required=True)
    replay.add_argument("--budget", type=int, default=10000)
    args = parser.parse_args(argv)
    try:
        if args.command == "observe":
            old = _read_ledger(_read_json(args.previous)) if args.previous else []
            record = capture(args.repo, args.path, args.scope, producer=args.producer)
            ledger = make_ledger(old + [record])
            with Path(args.output).open("x", encoding="utf-8") as out:
                json.dump(ledger, out, ensure_ascii=False, sort_keys=True, indent=2)
                out.write("\n")
            print(json.dumps({"status": record["status"], "capture_id": record["capture_id"],
                              "head": record["head_start"], "ledger_count": ledger["count"]}))
            return 0 if record["status"] == "OK" else 1
        print(json.dumps(replay_ledger(_read_json(args.input), args.path, args.budget),
                         ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("repository observer: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
