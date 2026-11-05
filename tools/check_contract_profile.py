#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Validate the bounded KC observation/change-event exchange subset and exercise a local publication model.

The locked reference model is not a distributed implementation or an admission authority.
"""
from __future__ import annotations

import copy
import functools
import hashlib
import json
import math
import sys
import threading
from datetime import datetime
from pathlib import Path

import jsonschema

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas/contract-observation.schema.json"
MAX_EPOCH = 9007199254740991
DISPATCH = {"KCObservation/v1": "Observation", "KCDependencyChange/v1": "ChangeEvent", "KCProfileAdvertisement/v1": "Advertisement"}
FORMAT_CHECKER = jsonschema.FormatChecker()


@FORMAT_CHECKER.checks("date-time", raises=(ValueError, TypeError))
def utc_seconds(value):
    datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    return True


class ProfileError(ValueError):
    pass


def decode_record(data: bytes) -> dict:
    if data.startswith(b"\xef\xbb\xbf"):
        raise ProfileError("UTF-8 BOM is not permitted")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ProfileError(f"duplicate JSON member: {key}")
            result[key] = value
        return result

    def invalid_number(value):
        raise ProfileError(f"non-finite JSON number: {value}")

    try:
        record = json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=invalid_number)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProfileError(str(exc)) from exc
    if not isinstance(record, dict):
        raise ProfileError("record is not an object")
    # JSON permits escaped isolated surrogates; this profile requires Unicode scalar strings.
    def scalar_strings(value):
        if isinstance(value, str):
            if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
                raise ProfileError("isolated surrogate in JSON string")
        elif isinstance(value, dict):
            for k, v in value.items():
                scalar_strings(k)
                scalar_strings(v)
        elif isinstance(value, list):
            for v in value:
                scalar_strings(v)
        elif isinstance(value, float) and not math.isfinite(value):
            raise ProfileError("numeric value overflows the finite parser range")
    scalar_strings(record)
    return record


@functools.lru_cache(maxsize=None)
def validator(definition):
    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator({"$schema": schema["$schema"], "$ref": "#/$defs/" + definition, "$defs": schema["$defs"]}, format_checker=FORMAT_CHECKER)


def check_record(record: dict) -> list[str]:
    kind = DISPATCH.get(record.get("schema"))
    if kind is None:
        return ["unsupported record schema"]
    errors = [f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in validator(kind).iter_errors(record)]
    if errors:
        return errors
    if kind == "ChangeEvent":
        if record["new_epoch"] <= record["old_epoch"]:
            errors.append("new_epoch must strictly exceed old_epoch")
        if record["kind"] == "revoked" and record["impact"] != "blocked":
            errors.append("revocation impact must be blocked")
    return errors


def record_digest(data: bytes) -> str:
    record = decode_record(data)
    errors = check_record(record)
    if errors:
        raise ProfileError("; ".join(errors))
    return hashlib.sha256(data).hexdigest()


class PublicationGuardModel:
    """One namespace, serialized in memory, with explicit complete dependency epochs and revocations.

    A production implementation needs persistent non-reused counters and one linearizable transaction across the entire
    read set, including authority and policy. This finite model cannot certify those deployment properties.
    It models the epoch/revocation guard only; output-specific grants, semantic validity and build checks are outside it.
    """
    def __init__(self, namespace: str, dependencies: dict[str, int], generation: int = 0):
        if not namespace or type(generation) is not int or not 0 <= generation <= MAX_EPOCH:
            raise ProfileError("invalid namespace/generation")
        if any(type(v) is not int or not 0 <= v <= MAX_EPOCH for v in dependencies.values()):
            raise ProfileError("invalid dependency epoch")
        self.namespace = namespace
        self.generation = generation
        self.dependencies = dict(dependencies)
        self.revoked = set()
        self.head = None
        self._lock = threading.Lock()

    def read(self):
        with self._lock:
            return {"namespace": self.namespace, "generation": self.generation, "dependencies": copy.deepcopy(self.dependencies)}

    def change(self, dependency: str, *, revoked: bool = False):
        with self._lock:
            if dependency not in self.dependencies:
                raise ProfileError("unknown dependency")
            if max(self.generation, self.dependencies[dependency]) == MAX_EPOCH:
                raise ProfileError("counter exhausted; migrate to a new namespace, never wrap")
            self.dependencies[dependency] += 1
            self.generation += 1
            if revoked:
                self.revoked.add(dependency)
            # Clearing a revocation requires a distinct adopted authority decision, intentionally not modeled here.

    def publish(self, read_set: dict, output: str) -> bool:
        with self._lock:
            if (read_set.get("namespace") != self.namespace or read_set.get("generation") != self.generation
                    or read_set.get("dependencies") != self.dependencies or self.revoked or self.generation == MAX_EPOCH
                    or any(epoch == MAX_EPOCH for epoch in self.dependencies.values())):
                return False
            self.head = output
            self.generation += 1
            return True


def main(argv):
    if len(argv) != 2:
        print("usage: check_contract_profile.py RECORD.json", file=sys.stderr)
        return 2
    try:
        data = Path(argv[1]).read_bytes()
        digest = record_digest(data)
    except (OSError, ProfileError) as exc:
        print(f"CONTRACT_PROFILE_FAIL {exc}")
        return 1
    print(f"CONTRACT_PROFILE_PASS hash_domain=sha256/raw-utf8-json-v1 sha256={digest}; no evidence authenticity or runtime admission established")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
