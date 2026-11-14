# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Bind and evaluate a finite, explicitly supplied interpretation profile.

The input is plain UTF-8 NOTE/RULE source, not unrestricted natural language.
Byte binding, controlled parsing and Boolean evaluation do not authenticate
attribution, establish real-world truth, or grant permission to an agent.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys

SCHEMA = "kc-semantic-bridge/1"
REPORT_SCHEMA = "kc-semantic-bridge-report/1"
MAX_SOURCE_BYTES = 65536
MAX_PACKET_BYTES = 131072
MAX_OBSERVATIONS = 8
MAX_READINGS = 4
MAX_NODES = 128
MAX_DEPTH = 16
MAX_NESTING = 32
MAX_EXPRESSION_CHARS = 4096
IDENTIFIER = re.compile(r"[a-z][a-z0-9_]{0,31}\Z")
RULE_LINE = re.compile(r"RULE ([a-z][a-z0-9_]{0,31}): (.+)\Z")
TOKEN = re.compile(r"[ \t]*(NOT\b|AND\b|OR\b|UNLESS\b|TRUE\b|FALSE\b|[a-z][a-z0-9_]{0,31}|[()])")


class BridgeError(ValueError):
    def __init__(self, code, message, status="INVALID", **details):
        super().__init__(message)
        self.code, self.status, self.details = code, status, details


def _require(condition, code, message, status="INVALID"):
    if not condition:
        raise BridgeError(code, message, status)


def _keys(value, required, label):
    _require(type(value) is dict and set(value) == set(required),
             "invalid_fields", label + " has missing, extra or unsupported fields")


def _identifier(value, label):
    _require(type(value) is str and IDENTIFIER.fullmatch(value) is not None,
             "invalid_identifier", label + " must be a bounded lowercase identifier")
    return value


def _text(value, label):
    _require(type(value) is str and 0 < len(value) <= 256
             and not any(ord(c) < 32 for c in value),
             "invalid_text", label + " must be nonempty bounded text")
    try:
        value.encode("utf-8")
    except UnicodeError as error:
        raise BridgeError("invalid_utf8", label + " is not valid Unicode text") from error
    return value


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise BridgeError("duplicate_json_member", "duplicate JSON object member")
        result[key] = value
    return result


def _constant(_value):
    raise BridgeError("nonfinite_json", "non-finite JSON values are unsupported")


def _read_bounded(path, limit):
    with Path(path).open("rb") as stream:
        data = stream.read(limit + 1)
    _require(len(data) <= limit, "input_size_bound", "input exceeds the declared byte bound", "UNSUPPORTED")
    return data


def read_packet(path):
    """Read bounded JSON, refusing duplicate keys before interpreting any field."""
    raw = _read_bounded(path, MAX_PACKET_BYTES)
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                          parse_constant=_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise BridgeError("malformed_json", "packet is not supported well-formed UTF-8 JSON") from error


class _Parser:
    def __init__(self, expression):
        _require(type(expression) is str, "expression_type", "expression must be text")
        _require(len(expression) <= MAX_EXPRESSION_CHARS, "expression_bound",
                 "expression exceeds the declared character bound", "UNSUPPORTED")
        self.tokens, offset = [], 0
        while offset < len(expression):
            if expression[offset:].strip(" \t") == "":
                break
            match = TOKEN.match(expression, offset)
            _require(match is not None, "unsupported_token",
                     "expression contains syntax outside the controlled grammar", "UNSUPPORTED")
            self.tokens.append(match[1])
            offset = match.end()
            _require(len(self.tokens) <= 4 * MAX_NODES, "token_bound",
                     "expression exceeds the declared token bound", "UNSUPPORTED")
        self.position, self.nodes = 0, 0

    def peek(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def take(self, token):
        if self.peek() == token:
            self.position += 1
            return True
        return False

    def node(self, op, **fields):
        self.nodes += 1
        _require(self.nodes <= MAX_NODES, "node_bound",
                 "expression exceeds the declared AST-node bound", "UNSUPPORTED")
        return {"op": op, **fields}

    def expression(self, nesting=0):
        left = self.disjunction(nesting)
        if self.take("UNLESS"):
            left = self.node("unless", left=left, right=self.disjunction(nesting))
        return left

    def disjunction(self, nesting):
        left = self.conjunction(nesting)
        while self.take("OR"):
            left = self.node("or", left=left, right=self.conjunction(nesting))
        return left

    def conjunction(self, nesting):
        left = self.unary(nesting)
        while self.take("AND"):
            left = self.node("and", left=left, right=self.unary(nesting))
        return left

    def unary(self, nesting):
        _require(nesting <= MAX_NESTING, "nesting_bound",
                 "expression exceeds the declared syntax-nesting bound", "UNSUPPORTED")
        if self.take("NOT"):
            return self.node("not", arg=self.unary(nesting + 1))
        if self.take("("):
            result = self.expression(nesting + 1)
            _require(self.take(")"), "unclosed_group", "parenthesized expression is incomplete", "UNSUPPORTED")
            return result
        token = self.peek()
        _require(token is not None, "incomplete_expression", "expression is incomplete", "UNSUPPORTED")
        self.position += 1
        if token in {"TRUE", "FALSE"}:
            return self.node("const", value=token == "TRUE")
        _require(IDENTIFIER.fullmatch(token) is not None, "unexpected_token",
                 "unexpected token in the controlled expression", "UNSUPPORTED")
        return self.node("atom", name=token)


def _walk(ast):
    pending = [(ast, 1)]
    while pending:
        node, depth = pending.pop()
        yield node, depth
        if node["op"] == "not":
            pending.append((node["arg"], depth + 1))
        elif node["op"] in {"and", "or", "unless"}:
            pending.extend(((node["left"], depth + 1), (node["right"], depth + 1)))


def compile_rule(expression):
    """Parse the complete controlled expression; UNLESS is conjunction with NOT."""
    parser = _Parser(expression)
    ast = parser.expression()
    _require(parser.peek() is None, "trailing_syntax",
             "the whole expression must parse; chain UNLESS only with parentheses", "UNSUPPORTED")
    _require(all(depth <= MAX_DEPTH for _node, depth in _walk(ast)), "depth_bound",
             "expression exceeds the declared AST-depth bound", "UNSUPPORTED")
    return ast


def _atoms(ast):
    return {node["name"] for node, _depth in _walk(ast) if node["op"] == "atom"}


def evaluate_ast(ast, values):
    """Evaluate a compiled AST on a complete Boolean assignment of local atoms."""
    _require(type(values) is dict and all(type(values.get(atom)) is bool for atom in _atoms(ast)),
             "incomplete_assignment", "all used local atoms require actual Boolean values")

    def evaluate(node):
        op = node["op"]
        if op == "atom":
            return values[node["name"]]
        if op == "const":
            return node["value"]
        if op == "not":
            return not evaluate(node["arg"])
        left, right = evaluate(node["left"]), evaluate(node["right"])
        if op == "and":
            return left and right
        if op == "or":
            return left or right
        if op == "unless":
            return left and not right
        raise BridgeError("unknown_operator", "AST is not from the controlled compiler")

    return evaluate(ast)


def _source_units(source):
    _require(type(source) is bytes, "source_type", "source must be exact bytes")
    _require(len(source) <= MAX_SOURCE_BYTES, "source_size_bound",
             "source exceeds the declared byte bound", "UNSUPPORTED")
    try:
        source.decode("utf-8")
    except UnicodeError as error:
        raise BridgeError("invalid_utf8", "source is not valid UTF-8") from error
    units, offset, note_count = [], 0, 0
    seen = set()
    for segment in source.split(b"\n"):
        has_lf = offset + len(segment) < len(source)
        line = segment[:-1] if has_lf and segment.endswith(b"\r") else segment
        _require(b"\r" not in line and b"\x00" not in line, "source_control_character",
                 "source uses an unsupported line ending or NUL", "UNSUPPORTED")
        text = line.decode("utf-8")
        if text == "":
            pass
        elif text.startswith("NOTE "):
            note_count += 1
        else:
            match = RULE_LINE.fullmatch(text)
            _require(match is not None, "unsupported_source_line",
                     "every nonempty source line must be an exact NOTE or RULE unit", "UNSUPPORTED")
            identity, expression = match.groups()
            _require(identity not in seen, "duplicate_rule_unit", "RULE identifiers must be unique")
            seen.add(identity)
            units.append({"id": identity, "start": offset, "end": offset + len(line),
                          "quote": text, "expression": expression})
            _require(len(units) <= MAX_READINGS, "reading_bound",
                     "source exceeds the declared alternative-reading bound", "UNSUPPORTED")
        offset += len(segment) + 1
    _require(bool(units), "no_rule_units", "source has no controlled RULE unit", "UNSUPPORTED")
    return units, note_count


def _observations(observations):
    _require(type(observations) is dict, "observation_type", "observations must be an object")
    _require(len(observations) <= MAX_OBSERVATIONS, "observation_bound",
             "too many declared Boolean observations", "UNSUPPORTED")
    for identity, observation in observations.items():
        _identifier(identity, "observation identity")
        _require(type(observation) is dict, "observation_fields", "observation must be an object")
        state = observation.get("state")
        _require(state in {"known", "unknown", "withheld"} if type(state) is str else False,
                 "observation_state", "unsupported observation state")
        required = {"referent", "type", "state"} | ({"value"} if state == "known" else set())
        _keys(observation, required, "observation")
        _text(observation["referent"], "declared referent")
        _require(observation["type"] == "boolean", "observation_semantic_type",
                 "only the declared Boolean observation type is supported", "UNSUPPORTED")
        if state == "known":
            _require(type(observation["value"]) is bool, "observation_value",
                     "known observations require actual Boolean values")
    return sorted(observations)


def _base_report():
    return {"schema": REPORT_SCHEMA, "status": "INVALID", "errors": [],
            "effects_authorized": False, "source_binding": "NOT_VERIFIED",
            "controlled_parsing": "NOT_VERIFIED", "source_semantic_fidelity": "NOT_ASSESSED",
            "attribution_authenticity": "NOT_ASSESSED", "real_world_truth": "NOT_ASSESSED",
            "current_authority": "NOT_ASSESSED"}


def analyze(source, packet):
    """Produce one complete bounded report, or an explicit invalid/unsupported result."""
    report = _base_report()
    try:
        units, note_count = _source_units(source)
        source_sha256 = hashlib.sha256(source).hexdigest()
        report["source_sha256"] = source_sha256
        _keys(packet, {"schema", "source_sha256", "source_media_type", "interpretation_set",
                       "observations", "readings"}, "packet")
        _require(packet["schema"] == SCHEMA, "unsupported_schema", "unsupported packet schema", "UNSUPPORTED")
        _require(packet["source_media_type"] == "text/plain", "source_media_type",
                 "this profile supports plain text only", "UNSUPPORTED")
        _require(packet["interpretation_set"] == "alternatives", "interpretation_set",
                 "RULE units must be declared alternative readings of one query", "UNSUPPORTED")
        _require(type(packet["source_sha256"]) is str and packet["source_sha256"] == source_sha256,
                 "source_digest_mismatch", "packet is not bound to the supplied source bytes")
        observation_ids = _observations(packet["observations"])
        readings = packet["readings"]
        _require(type(readings) is list and 1 <= len(readings) <= MAX_READINGS,
                 "reading_inventory", "provide a nonempty bounded list of alternative readings")
        by_id = {}
        for reading in readings:
            _keys(reading, {"id", "start", "end", "quote", "attribution", "bindings"}, "reading")
            identity = _identifier(reading["id"], "reading identity")
            _require(identity not in by_id, "duplicate_reading", "reading identity is repeated")
            _keys(reading["attribution"], {"agent", "discourse"}, "attribution")
            _text(reading["attribution"]["agent"], "attribution agent")
            discourse = reading["attribution"]["discourse"]
            _require(type(discourse) is str and discourse in {"asserted", "quoted", "hypothetical"},
                     "discourse_position", "unsupported declared discourse position", "UNSUPPORTED")
            _require(type(reading["bindings"]) is dict, "binding_fields", "atom bindings must be an object")
            for atom, target in reading["bindings"].items():
                _identifier(atom, "local atom")
                _identifier(target, "bound observation")
                _require(target in packet["observations"], "missing_observation", "binding has no declared observation")
            by_id[identity] = reading
        _require(set(by_id) == {unit["id"] for unit in units}, "incomplete_rule_inventory",
                 "every source RULE unit must be retained exactly once")
        report["reading_ids"] = [unit["id"] for unit in units]
        compiled = []
        for unit in units:
            reading = by_id[unit["id"]]
            _require(type(reading["start"]) is int and type(reading["end"]) is int
                     and (reading["start"], reading["end"]) == (unit["start"], unit["end"]),
                     "whole_unit_required", "selector must bind the entire physical RULE line")
            _require(type(reading["quote"]) is str and reading["quote"] == unit["quote"],
                     "quote_mismatch", "quote must equal the complete selected UTF-8 RULE line")
        report["source_binding"] = "VERIFIED"
        for unit in units:
            reading = by_id[unit["id"]]
            try:
                ast = compile_rule(unit["expression"])
            except BridgeError as error:
                error.details["reading_id"] = unit["id"]
                raise
            _require(set(reading["bindings"]) == _atoms(ast), "atom_binding_inventory",
                     "bindings must cover all and only the used local atoms")
            compiled.append((unit, reading, ast))
        report["controlled_parsing"] = "VERIFIED"
        observations = packet["observations"]
        domains = [(observations[name]["value"],) if observations[name]["state"] == "known"
                   else (False, True) for name in observation_ids]
        worlds = [dict(zip(observation_ids, values)) for values in itertools.product(*domains)]
        results, columns = [], []
        for unit, reading, ast in compiled:
            values = [evaluate_ast(ast, {atom: world[target] for atom, target in reading["bindings"].items()})
                      for world in worlds]
            columns.append(values)
            results.append({"id": unit["id"], "attribution": dict(reading["attribution"]),
                            "bindings": dict(sorted(reading["bindings"].items())),
                            "span": {"start": unit["start"], "end": unit["end"]}, "quote": unit["quote"],
                            "ast": ast, "table_bits": "".join("1" if x else "0" for x in values),
                            "possible_values": sorted(set(values))})
        possible = sorted({value for column in columns for value in column})
        report.update(status="EVALUATED", note_line_count=note_count,
                      observation_ids=observation_ids,
                      observations={name: dict(observations[name]) for name in observation_ids},
                      world_assignments=worlds, valuation_count=len(worlds), readings=results,
                      possible_values=possible,
                      truth="TRUE" if possible == [True] else "FALSE" if possible == [False] else "UNDETERMINED",
                      reading_disagreement=any(len({column[i] for column in columns}) > 1 for i in range(len(worlds))))
    except BridgeError as error:
        report.update(status=error.status, errors=[{"code": error.code, "message": str(error), **error.details}])
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source", required=True)
    parser.add_argument("--packet", required=True)
    args = parser.parse_args(argv)
    try:
        source = _read_bounded(args.source, MAX_SOURCE_BYTES)
        packet = read_packet(args.packet)
        result = analyze(source, packet)
    except (BridgeError, OSError) as error:
        result = _base_report()
        result["status"] = error.status if isinstance(error, BridgeError) else "INVALID"
        result["errors"] = [{"code": error.code if isinstance(error, BridgeError) else "input_read_failed",
                             "message": str(error)}]
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False))
    return 0 if result["status"] == "EVALUATED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
