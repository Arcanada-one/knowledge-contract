#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Finite semantic masks and source-bound consumer checks, separate from the API.

The oracle starts with Boolean truth masks, encodes them as controlled source,
and filters complete-world masks against evidence records. It does not import
the implementation's tokenizer, parser, AST traversal, or evaluator helpers.
Its complete finite families are not a natural-language fidelity benchmark.
"""
from __future__ import annotations

from collections import Counter
import copy
import hashlib
from itertools import product
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from tools import semantic_bridge as api


AVAILABILITY = ("known_false", "known_true", "unknown", "withheld")
UNASSESSED = ("source_semantic_fidelity", "attribution_authenticity",
              "current_authority", "real_world_truth")
ORIGINAL_NOTES = {
    "en": "Original test notice: membership, training and a check are required; suspension is an exception. Borrowing gives no copying authority.",
    "ru": "Авторский тестовый пример: нужны членство, обучение и проверка; приостановка — исключение. Выдача не даёт права копировать файлы.",
    "zh": "原创测试示例：需要成员资格、培训和检查；暂停借用属于例外。借用不授予复制文件的权限。",
}


def _check(condition, message):
    if not condition:
        raise AssertionError(message)


def _digest(source):
    return hashlib.sha256(source).hexdigest()


def _evidence(atoms, states):
    result = {}
    for atom, state in zip(atoms, states):
        record = {"referent": "synthetic observation " + atom, "type": "boolean",
                  "state": "known" if state.startswith("known_") else state}
        if state.startswith("known_"):
            record["value"] = state == "known_true"
        result["o_" + atom] = record
    return result


def _fixture(expressions, observations, *, notes=("Original controlled test source.",),
             newline=b"\n", final_newline=True, bindings=None, discourses=None):
    """Make literal source units independently of the implementation's parser."""
    units = [("r" + str(i + 1), expression) for i, expression in enumerate(expressions)]
    lines = [("NOTE " + note).encode("utf-8") for note in notes]
    rule_lines = [("RULE " + identity + ": " + expression).encode("utf-8")
                  for identity, expression in units]
    source = newline.join(lines + rule_lines) + (newline if final_newline else b"")
    readings = []
    for index, ((identity, expression), raw_line) in enumerate(zip(units, rule_lines)):
        start = source.index(raw_line)
        if bindings is None:
            names = set(re.findall(r"\b[a-z][a-z0-9_]*\b", expression))
            local = {name: "o_" + name for name in sorted(names) if "o_" + name in observations}
        else:
            local = bindings[index]
        readings.append({
            "id": identity, "start": start, "end": start + len(raw_line),
            "quote": raw_line.decode("utf-8"),
            "attribution": {"agent": "fixture_annotator_" + str(index + 1),
                            "discourse": "asserted" if discourses is None else discourses[index]},
            "bindings": dict(local),
        })
    packet = {"schema": "kc-semantic-bridge/1", "source_sha256": _digest(source),
              "source_media_type": "text/plain", "interpretation_set": "alternatives",
              "observations": copy.deepcopy(observations), "readings": readings}
    return source, packet


def _dnf(mask, atoms):
    """Encode a known truth mask without asking the consumer for its semantics."""
    worlds = 1 << len(atoms)
    if mask == 0:
        return "FALSE"
    if mask == (1 << worlds) - 1:
        return "TRUE"
    terms = []
    for world in range(worlds):
        if mask & (1 << world):
            literals = [atom if world & (1 << (len(atoms) - position - 1)) else "NOT " + atom
                        for position, atom in enumerate(atoms)]
            terms.append("(" + " AND ".join(literals) + ")")
    return "(" + " OR ".join(terms) + ")"


def _compatible_worlds(states):
    allowed = 0
    count = len(states)
    for world in range(1 << count):
        consistent = True
        for position, state in enumerate(states):
            bit = bool(world & (1 << (count - position - 1)))
            if state == "known_false" and bit:
                consistent = False
            if state == "known_true" and not bit:
                consistent = False
        if consistent:
            allowed |= 1 << world
    return allowed


def _indices(mask, width):
    return tuple(i for i in range(width) if mask & (1 << i))


def _possible(function_mask, allowed):
    return ([False] if allowed & ~function_mask else []) + ([True] if allowed & function_mask else [])


def _table(function_mask, allowed, world_count):
    return "".join("1" if function_mask & (1 << i) else "0"
                   for i in _indices(allowed, world_count))


def _assignments(atoms, allowed):
    return [{"o_" + atom: bool(world & (1 << (len(atoms) - position - 1)))
             for position, atom in enumerate(atoms)}
            for world in _indices(allowed, 1 << len(atoms))]


def _truth(values):
    return "TRUE" if values == [True] else "FALSE" if values == [False] else "UNDETERMINED"


def _boundaries(report):
    _check(report["schema"] == "kc-semantic-bridge-report/1", "wrong report profile")
    _check(report["effects_authorized"] is False, "data analysis granted effect authority")
    for field in UNASSESSED:
        _check(report[field] == "NOT_ASSESSED", field + " was silently promoted")


def _evaluated(report, source):
    _boundaries(report)
    _check(report["status"] == "EVALUATED", "valid controlled input did not evaluate: " + str(report))
    _check(report["errors"] == [], "evaluated result retains an unhandled error")
    _check(report["source_binding"] == "VERIFIED", "evaluated result lacks source binding")
    _check(report["controlled_parsing"] == "VERIFIED", "evaluated result lacks complete parsing")
    _check(report["source_sha256"] == _digest(source), "result identifies different source bytes")


def audit_boolean_space():
    atoms = ("p", "q", "r")
    profiles = tuple(product(AVAILABILITY, repeat=3))
    worlds = {states: _compatible_worlds(states) for states in profiles}
    evidence = {states: _evidence(atoms, states) for states in profiles}
    counters = Counter()
    for mask in range(1 << (1 << len(atoms))):
        source, baseline = _fixture((_dnf(mask, atoms),), evidence[profiles[0]])
        counters["source_expressions"] += 1
        for states in profiles:
            packet = {**baseline, "observations": evidence[states]}
            report = api.analyze(source, packet)
            _evaluated(report, source)
            allowed = worlds[states]
            expected_values = _possible(mask, allowed)
            expected_table = _table(mask, allowed, 8)
            _check(report["observation_ids"] == ["o_p", "o_q", "o_r"], "wrong observation order")
            _check(report["observations"] == evidence[states], "observation availability was not preserved")
            _check(report["world_assignments"] == _assignments(atoms, allowed), "worlds differ from mask oracle")
            _check(report["valuation_count"] == allowed.bit_count(), "wrong world count")
            _check(len(report["readings"]) == 1 and report["readings"][0]["id"] == "r1", "reading inventory changed")
            reading = report["readings"][0]
            _check(reading["table_bits"] == expected_table, "DNF evaluation differs from its truth mask")
            _check(reading["possible_values"] == expected_values, "per-reading possibility set is wrong")
            _check(report["possible_values"] == expected_values, "aggregate possibility set is wrong")
            _check(report["truth"] == _truth(expected_values), "wrong scoped truth summary")
            _check(report["reading_disagreement"] is False, "one reading disagreed with itself")
            counters["evaluation_records"] += 1
            counters["completed_world_evaluations"] += allowed.bit_count()
            counters["truth_" + report["truth"].lower()] += 1
    _check(counters["source_expressions"] == 2 ** (2 ** 3), "expression inventory incomplete")
    _check(counters["evaluation_records"] == 2 ** (2 ** 3) * 4 ** 3, "evidence-grid inventory incomplete")
    _check(all(counters["truth_" + state] for state in ("true", "false", "undetermined")),
           "useful true/false/undetermined paths were not all exercised")
    return {"result": "pass", "observed_counts": dict(sorted(counters.items())),
            "evidence_profiles": len(profiles),
            "distinct_compatible_world_sets": len(set(worlds.values())),
            "space": "all 256 three-atom Boolean functions as canonical DNF; all 4^3 supplied availability/value records",
            "limits": "Finite formal evaluation, not all accepted ASTs, source interpretation or independent empirical trials."}


def audit_alternative_space():
    atoms = ("p", "q")
    profiles = tuple(product(AVAILABILITY, repeat=2))
    counters = Counter()
    for left, right in product(range(16), repeat=2):
        source, baseline = _fixture((_dnf(left, atoms), _dnf(right, atoms)),
                                    _evidence(atoms, profiles[0]), discourses=("asserted", "quoted"))
        counters["ordered_reading_pairs"] += 1
        for states in profiles:
            packet = {**baseline, "observations": _evidence(atoms, states)}
            report = api.analyze(source, packet)
            _evaluated(report, source)
            allowed = _compatible_worlds(states)
            expected = [_possible(left, allowed), _possible(right, allowed)]
            aggregate = sorted(set(expected[0]) | set(expected[1]))
            disagreement = bool((left ^ right) & allowed)
            _check([r["id"] for r in report["readings"]] == ["r1", "r2"], "alternative inventory/order changed")
            for index, mask in enumerate((left, right)):
                reading = report["readings"][index]
                _check(reading["table_bits"] == _table(mask, allowed, 4), "alternative truth table is wrong")
                _check(reading["possible_values"] == expected[index], "alternative possibilities are wrong")
                _check(reading["attribution"] == baseline["readings"][index]["attribution"], "attribution lost")
            _check(report["possible_values"] == aggregate and report["truth"] == _truth(aggregate),
                   "alternative union or truth summary is wrong")
            _check(report["reading_disagreement"] is disagreement, "same-world disagreement is wrong")
            counters["evaluation_records"] += 1
            counters["same_world_disagreement"] += int(disagreement)
            counters["same_world_agreement"] += int(not disagreement)
            counters["equal_value_sets_but_disagreeing"] += int(expected[0] == expected[1] and disagreement)
            counters["completed_world_reading_evaluations"] += 2 * allowed.bit_count()
    _check(counters["ordered_reading_pairs"] == 16 ** 2, "alternative-pair inventory incomplete")
    _check(counters["evaluation_records"] == 16 ** 2 * 4 ** 2, "alternative evidence-grid inventory incomplete")
    _check(counters["equal_value_sets_but_disagreeing"] > 0, "the value-set versus pointwise distinction was not exercised")
    return {"result": "pass", "observed_counts": dict(sorted(counters.items())),
            "space": "all ordered pairs of two-atom truth functions; all 4^2 availability/value records",
            "limits": "Explicit supplied alternatives; no claim that all human readings were discovered."}


def audit_original_examples():
    observations = _evidence(("m", "t", "k", "s"),
                             ("known_true", "known_true", "known_true", "known_false"))
    examples = []
    for language, note in ORIGINAL_NOTES.items():
        source, packet = _fixture(("m AND t AND k UNLESS s",), observations, notes=(note,))
        report = api.analyze(source, packet)
        _evaluated(report, source)
        _check(report["truth"] == "TRUE", "positive rule example failed")
        examples.append({"language": language, "source_utf8": source.decode("utf-8"),
                         "source_sha256": _digest(source), "packet": packet, "report": report,
                         "language_scope": "Original prose wrapper and byte binding; translation fidelity not assessed."})
    return {"result": "pass", "examples": examples}


def run_finite_audit():
    return {"boolean_space": audit_boolean_space(), "alternative_space": audit_alternative_space(),
            "original_examples": audit_original_examples(),
            "independence": "Separately authored truth-mask oracle; same controller/model family/host; not external review."}


class FiniteSemanticOracleTests(unittest.TestCase):
    def test_all_three_atom_truth_functions_against_all_evidence_profiles(self):
        self.assertEqual(audit_boolean_space()["result"], "pass")

    def test_all_two_atom_alternative_pairs_use_one_shared_world_grid(self):
        self.assertEqual(audit_alternative_space()["result"], "pass")

    def test_original_language_wrappers_bind_actual_utf8_bytes(self):
        examples = audit_original_examples()["examples"]
        self.assertEqual(len({row["source_sha256"] for row in examples}), 3)
        for row in examples:
            source = row["source_utf8"].encode("utf-8")
            reading = row["packet"]["readings"][0]
            self.assertEqual(source[reading["start"]:reading["end"]].decode("utf-8"), reading["quote"])
        for row in examples[1:]:
            self.assertNotEqual(row["source_utf8"].index("RULE"), row["packet"]["readings"][0]["start"])


class SourceAndReadingBoundaryTests(unittest.TestCase):
    def assertStatus(self, source, packet, status):
        result = api.analyze(source, packet)
        _boundaries(result)
        self.assertEqual(result["status"], status, result)
        if status != "EVALUATED":
            self.assertTrue(result["errors"])
            self.assertNotIn("truth", result)
        return result

    def test_complete_rule_unit_prevents_dropping_exception_with_valid_source_hash(self):
        observations = _evidence(("p", "q", "r"), ("known_true", "known_true", "known_true"))
        source, packet = _fixture(("(p AND q) UNLESS r",), observations)
        self.assertEqual(self.assertStatus(source, packet, "EVALUATED")["truth"], "FALSE")
        shortened = copy.deepcopy(packet)
        record = shortened["readings"][0]
        record["quote"] = record["quote"].split(" UNLESS")[0]
        record["end"] = record["start"] + len(record["quote"].encode("utf-8"))
        record["bindings"].pop("r")
        self.assertEqual(shortened["source_sha256"], _digest(source))
        self.assertStatus(source, shortened, "INVALID")

    def test_source_change_requires_new_identity_and_exact_selectors(self):
        source, packet = _fixture(("p",), _evidence(("p",), ("known_true",)), notes=("Alpha",))
        changed = source.replace(b"Alpha", b"Omega")
        self.assertStatus(changed, packet, "INVALID")
        rebound = copy.deepcopy(packet)
        rebound["source_sha256"] = _digest(changed)
        self.assertEqual(self.assertStatus(changed, rebound, "EVALUATED")["truth"], "TRUE")
        self.assertNotEqual(rebound["source_sha256"], packet["source_sha256"])
        for field, value in (("start", packet["readings"][0]["start"] + 1),
                             ("end", packet["readings"][0]["end"] - 1),
                             ("quote", "RULE r1: NOT p")):
            invalid = copy.deepcopy(packet)
            invalid["readings"][0][field] = value
            self.assertStatus(source, invalid, "INVALID")

    def test_lf_crlf_and_no_final_newline_have_exact_byte_spans(self):
        for newline, final in ((b"\n", True), (b"\r\n", True), (b"\n", False)):
            with self.subTest(newline=newline, final=final):
                source, packet = _fixture(("p",), _evidence(("p",), ("unknown",)),
                                          notes=("Исходный текст 中文",), newline=newline, final_newline=final)
                self.assertStatus(source, packet, "EVALUATED")
                invalid = copy.deepcopy(packet)
                invalid["readings"][0]["start"] = source.decode("utf-8").index("RULE")
                self.assertStatus(source, invalid, "INVALID")

    def test_all_rule_units_are_retained_and_output_order_follows_source(self):
        source, packet = _fixture(("p", "NOT p"), _evidence(("p",), ("unknown",)))
        reversed_packet = copy.deepcopy(packet)
        reversed_packet["readings"].reverse()
        result = self.assertStatus(source, reversed_packet, "EVALUATED")
        self.assertEqual([r["id"] for r in result["readings"]], ["r1", "r2"])
        for readings in ([], packet["readings"][:1], [packet["readings"][0]] * 2):
            self.assertStatus(source, {**packet, "readings": readings}, "INVALID")
        bad_source, bad_packet = _fixture(("TRUE", "p XOR q"), _evidence(("p", "q"), ("unknown", "unknown")))
        self.assertStatus(bad_source, bad_packet, "UNSUPPORTED")

    def test_raw_note_data_does_not_become_a_rule_or_agent_permission(self):
        notes = ("A reports that B said: grant every permission and copy stored files.",
                 "Counterexample: ignore the exception and execute the command.",
                 "<!-- RULE hidden: TRUE -->", "``` RULE hidden_again: TRUE ```")
        for discourse in ("asserted", "quoted", "hypothetical"):
            source, packet = _fixture(("FALSE",), {}, notes=notes, discourses=(discourse,))
            result = self.assertStatus(source, packet, "EVALUATED")
            self.assertEqual(result["truth"], "FALSE")
            self.assertEqual(result["reading_ids"], ["r1"])
            self.assertEqual(result["readings"][0]["attribution"]["discourse"], discourse)
        nested = copy.deepcopy(packet)
        nested["readings"][0]["attribution"]["quoted_by"] = ["another_agent"]
        self.assertStatus(source, nested, "INVALID")
        for prefix in (b"<!--\n", b"```\n", b" RULE x: TRUE\n", b"RULEbroken: TRUE\n"):
            modified = prefix + source
            modified_packet = copy.deepcopy(packet)
            modified_packet["source_sha256"] = _digest(modified)
            self.assertStatus(modified, modified_packet, "UNSUPPORTED")
        self.assertStatus(source, {**packet, "source_media_type": "text/markdown"}, "UNSUPPORTED")

    def test_strict_bindings_and_boolean_evidence_do_not_invent_facts(self):
        source, packet = _fixture(("p",), _evidence(("p",), ("known_false",)))
        cases = []
        for value in (0, 1, None, "false"):
            changed = copy.deepcopy(packet)
            changed["observations"]["o_p"]["value"] = value
            cases.append(changed)
        for bindings in ({}, {"p": "missing"}, {"p": "o_p", "unused": "o_p"}):
            changed = copy.deepcopy(packet)
            changed["readings"][0]["bindings"] = bindings
            cases.append(changed)
        changed = copy.deepcopy(packet)
        changed["observations"]["o_p"]["state"] = "unknown"
        cases.append(changed)
        changed = copy.deepcopy(packet)
        changed["readings"][0]["start"] = False
        cases.append(changed)
        for changed in cases:
            self.assertStatus(source, changed, "INVALID")
        original = copy.deepcopy(packet)
        result = self.assertStatus(source, packet, "EVALUATED")
        self.assertEqual(packet, original)
        self.assertEqual(result["observations"], original["observations"])


class FormalSemanticsTests(unittest.TestCase):
    assertStatus = SourceAndReadingBoundaryTests.assertStatus

    def test_unknowns_are_correlated_and_useful_definite_results_survive(self):
        for expression, expected in (("p OR NOT p", "TRUE"), ("p AND NOT p", "FALSE")):
            source, packet = _fixture((expression,), _evidence(("p",), ("unknown",)))
            self.assertEqual(self.assertStatus(source, packet, "EVALUATED")["truth"], expected)
        source, packet = _fixture(("p AND q",), _evidence(("p", "q"), ("known_false", "withheld")))
        result = self.assertStatus(source, packet, "EVALUATED")
        self.assertEqual(result["truth"], "FALSE")
        self.assertEqual(result["observations"]["o_q"]["state"], "withheld")
        self.assertNotIn("value", result["observations"]["o_q"])

    def test_aliases_share_an_observation_and_disagreement_is_pointwise(self):
        observation = _evidence(("shared",), ("unknown",))
        source, packet = _fixture(("p OR NOT q",), observation,
                                  bindings=({"p": "o_shared", "q": "o_shared"},))
        result = self.assertStatus(source, packet, "EVALUATED")
        self.assertEqual(result["valuation_count"], 2)
        self.assertEqual(result["readings"][0]["table_bits"], "11")
        source, packet = _fixture(("p", "NOT q"), observation,
                                  bindings=({"p": "o_shared"}, {"q": "o_shared"}))
        result = self.assertStatus(source, packet, "EVALUATED")
        self.assertEqual([r["possible_values"] for r in result["readings"]], [[False, True], [False, True]])
        self.assertEqual([r["table_bits"] for r in result["readings"]], ["01", "10"])
        self.assertTrue(result["reading_disagreement"])
        source, packet = _fixture(("p", "q"), observation,
                                  bindings=({"p": "o_shared"}, {"q": "o_shared"}))
        self.assertFalse(self.assertStatus(source, packet, "EVALUATED")["reading_disagreement"])

    def test_scope_precedence_and_explicit_unless_convention(self):
        cases = (("p OR q UNLESS r", 84), ("p UNLESS q OR r", 16),
                 ("NOT p AND q OR r", 174), ("p UNLESS (q UNLESS r)", 176),
                 ("(p UNLESS q) UNLESS r", 16))
        observations = _evidence(("p", "q", "r"), ("unknown",) * 3)
        for expression, truth_mask in cases:
            with self.subTest(expression=expression):
                source, packet = _fixture((expression,), observations)
                result = self.assertStatus(source, packet, "EVALUATED")
                self.assertEqual(result["readings"][0]["table_bits"], _table(truth_mask, 255, 8))
        for expression in ("p UNLESS q UNLESS r", "p; TRUE", "FORALL p", "1 meter", "p XOR q"):
            source, packet = _fixture((expression,), observations)
            self.assertStatus(source, packet, "UNSUPPORTED")

    def test_zero_observations_are_one_world_and_unused_observations_are_allowed(self):
        for expression, truth in (("TRUE", "TRUE"), ("FALSE", "FALSE")):
            source, packet = _fixture((expression,), {})
            result = self.assertStatus(source, packet, "EVALUATED")
            self.assertEqual(result["world_assignments"], [{}])
            self.assertEqual(result["valuation_count"], 1)
            self.assertEqual(result["truth"], truth)
            packet["observations"] = _evidence(("unused",), ("unknown",))
            result = self.assertStatus(source, packet, "EVALUATED")
            self.assertEqual(result["valuation_count"], 2)
            self.assertEqual(result["truth"], truth)

    def test_declared_bounds_keep_valid_maximum_and_reject_the_next_input(self):
        atoms = tuple("abcdefgh")
        observations = _evidence(atoms, ("unknown",) * 8)
        source, packet = _fixture((" AND ".join(atoms),) * 4, observations)
        result = self.assertStatus(source, packet, "EVALUATED")
        self.assertEqual(result["valuation_count"], 256)
        self.assertEqual(len(result["readings"]), 4)
        packet["observations"].update(_evidence(("extra",), ("unknown",)))
        self.assertStatus(source, packet, "UNSUPPORTED")
        source, packet = _fixture(("TRUE",) * 5, {})
        self.assertStatus(source, packet, "UNSUPPORTED")
        balanced = "p"
        for _ in range(6):
            balanced = "(" + balanced + " AND " + balanced + ")"
        observations = _evidence(("p",), ("unknown",))
        for expression, status in (("NOT " + balanced, "EVALUATED"),
                                   ("NOT NOT " + balanced, "UNSUPPORTED"),
                                   ("NOT " * 15 + "p", "EVALUATED"),
                                   ("NOT " * 16 + "p", "UNSUPPORTED"),
                                   ("(" * 33 + "p" + ")" * 33, "UNSUPPORTED")):
            source, packet = _fixture((expression,), observations)
            self.assertStatus(source, packet, status)
        source, packet = _fixture(("TRUE",), {}, notes=("x",))
        padding = b"x" * (65536 - len(source))
        enlarged = source.replace(b"NOTE x", b"NOTE x" + padding)
        start = enlarged.index(b"RULE")
        packet["source_sha256"] = _digest(enlarged)
        packet["readings"][0].update(start=start, end=start + len(b"RULE r1: TRUE"))
        self.assertEqual(len(enlarged), 65536)
        self.assertStatus(enlarged, packet, "EVALUATED")
        self.assertStatus(enlarged + b"\n", packet, "UNSUPPORTED")


class PublicConsumerTests(unittest.TestCase):
    def test_bounded_packet_with_huge_integer_returns_structured_cli_error(self):
        source, packet = _fixture(("TRUE",), {})
        payload = json.dumps(packet, separators=(",", ":"))
        start = packet["readings"][0]["start"]
        needle = '"start":' + str(start)
        self.assertEqual(payload.count(needle), 1)
        payload = payload.replace(needle, '"start":' + "9" * 5000, 1)
        self.assertLess(len(payload.encode("utf-8")), 131072)
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix="kc-semantic-bridge-integer-") as temporary:
            directory = Path(temporary)
            source_path, packet_path = directory / "source.txt", directory / "packet.json"
            source_path.write_bytes(source)
            packet_path.write_text(payload, encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-B", str(root / "tools/semantic_bridge.py"),
                 "--source", str(source_path), "--packet", str(packet_path)],
                text=True, capture_output=True, timeout=10, check=False,
                env={**os.environ, "PYTHONINTMAXSTRDIGITS": "4300"})
            self.assertEqual(completed.returncode, 2, completed.stderr)
            self.assertNotIn("Traceback", completed.stderr)
            report = json.loads(completed.stdout)
            _boundaries(report)
            self.assertEqual(report["status"], "INVALID")
            self.assertEqual(report["errors"][0]["code"], "malformed_json")

    def test_strict_json_and_fresh_process_cli_preserve_negative_results(self):
        source, packet = _fixture(("p",), _evidence(("p",), ("known_false",)),
                                  notes=(ORIGINAL_NOTES["ru"],))
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix="kc-semantic-bridge-") as temporary:
            directory = Path(temporary)
            source_path, packet_path = directory / "source.txt", directory / "packet.json"
            source_path.write_bytes(source)
            packet_path.write_text(json.dumps(packet, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(api.read_packet(packet_path), packet)
            before_files = sorted(path.name for path in directory.iterdir())
            command = [sys.executable, "-B", str(root / "tools/semantic_bridge.py"),
                       "--source", str(source_path), "--packet", str(packet_path)]
            completed = subprocess.run(command, text=True, capture_output=True, timeout=10, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = json.loads(completed.stdout)
            _evaluated(report, source)
            self.assertEqual(report["truth"], "FALSE")
            self.assertEqual(sorted(path.name for path in directory.iterdir()), before_files)
            serialized = json.dumps(packet, ensure_ascii=False, separators=(",", ":"))
            schema = '"schema":"kc-semantic-bridge/1"'
            state = '"state":"known"'
            referent = '"referent":"synthetic observation p"'
            file_cases = [
                ("top_level_duplicate", serialized.replace(schema, schema + "," + schema, 1).encode("utf-8"),
                 "duplicate_json_member", True),
                ("nested_duplicate", serialized.replace(state, state + "," + state, 1).encode("utf-8"),
                 "duplicate_json_member", True),
                ("escape_equivalent_duplicate",
                 serialized.replace(state, state + r',"\u0073tate":"known"', 1).encode("utf-8"),
                 "duplicate_json_member", True),
                ("nan", serialized.replace('"value":false', '"value":NaN', 1).encode("utf-8"),
                 "nonfinite_json", True),
                ("positive_infinity", serialized.replace('"value":false', '"value":Infinity', 1).encode("utf-8"),
                 "nonfinite_json", True),
                ("negative_infinity", serialized.replace('"value":false', '"value":-Infinity', 1).encode("utf-8"),
                 "nonfinite_json", True),
                ("invalid_utf8", serialized.encode("utf-8").replace(b"synthetic observation p", b"\xff", 1),
                 "malformed_json", True),
                ("unpaired_surrogate", serialized.replace(referent, r'"referent":"\ud800"', 1).encode("utf-8"),
                 "invalid_utf8", False),
            ]
            for label, payload, code, rejected_by_reader in file_cases:
                with self.subTest(case=label):
                    packet_path.write_bytes(payload)
                    if rejected_by_reader:
                        with self.assertRaises(ValueError) as raised:
                            api.read_packet(packet_path)
                        self.assertEqual(getattr(raised.exception, "code", None), code)
                    completed = subprocess.run(command, text=True, capture_output=True, timeout=10, check=False)
                    self.assertEqual(completed.returncode, 2, completed.stderr)
                    self.assertNotIn("Traceback", completed.stderr)
                    report = json.loads(completed.stdout)
                    _boundaries(report)
                    self.assertEqual(report["status"], "INVALID")
                    self.assertEqual(report["errors"][0]["code"], code)


if __name__ == "__main__":
    unittest.main()
