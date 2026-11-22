# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Captured Rule Consumer integration with real Git and fresh CLI processes.

The expected Boolean outcomes and lifecycle transitions were fixed separately
from the implementation before the first run. Git output and the model are not
mocked. A capture wrapper counts real acquisitions; acquisition failure guards
and one publication-link failure only test the stated boundary.
"""
import base64
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

try:
    from tools import repository_rule_consumer as consumer
    from tools import repository_session as session
    from tools import semantic_bridge as bridge
except ImportError:
    import repository_rule_consumer as consumer
    import repository_session as session
    import semantic_bridge as bridge


SOURCE_PATH = "rules/source.txt"
PACKET_PATH = "rules/packet.json"
OTHER_PATH = "notes/unrelated.txt"
RULE = "RULE lending: member UNLESS suspended"
SOURCE_A = ("NOTE Original offline consumer fixture; supplied conditions, no real permission.\n"
            + RULE + "\n").encode("utf-8")


def packet_for(source, *, suspended=False, state="known", rule=RULE):
    """Author the fixed interpretation packet; do not call a parser/oracle."""
    quote = rule.encode("utf-8")
    offset = source.index(quote)
    suspension = {"referent": "supplied suspension condition", "type": "boolean", "state": state}
    if state == "known":
        suspension["value"] = suspended
    return {"schema": "kc-semantic-bridge/1", "source_sha256": hashlib.sha256(source).hexdigest(),
            "source_media_type": "text/plain", "interpretation_set": "alternatives",
            "observations": {
                "member": {"referent": "supplied membership condition", "type": "boolean",
                           "state": "known", "value": True},
                "suspended": suspension},
            "readings": [{"id": "lending", "start": offset, "end": offset + len(quote),
                          "quote": rule,
                          "attribution": {"agent": "authored offline fixture", "discourse": "hypothetical"},
                          "bindings": {"member": "member", "suspended": "suspended"}}]}


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


class RepositoryRuleConsumerTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.repo = self.root / "repository"
        self.repo.mkdir()
        self.environment = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.environment.pop("GIT_CONFIG_COUNT", None)
        self.git("init", "--initial-branch=main")
        self.git("config", "user.name", "Offline consumer integration")
        self.git("config", "user.email", "consumer-test@example.invalid")
        self.packet_a = packet_for(SOURCE_A)
        self.write_pair(SOURCE_A, self.packet_a)
        self.write(OTHER_PATH, b"Unrelated public fixture A.\n")
        self.commit("Initial committed pair", SOURCE_PATH, PACKET_PATH, OTHER_PATH)
        self.cli = Path(consumer.__file__).resolve()

    def git(self, *arguments):
        return subprocess.run(["git", "-c", "core.hooksPath=" + os.devnull, "-C", str(self.repo), *arguments],
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=self.environment).stdout

    def write(self, path, raw):
        destination = self.repo / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)

    def write_pair(self, source, packet):
        self.write(SOURCE_PATH, source)
        self.write(PACKET_PATH, packet if type(packet) is bytes else json_bytes(packet))

    def commit(self, message, *paths):
        self.git("add", "--", *paths)
        self.git("commit", "-m", message)

    def start(self):
        return consumer.start(self.repo, SOURCE_PATH, PACKET_PATH,
                              task_id="evaluate-authored-rule", scope="offline-consumer-fixture")

    def command(self, *arguments, environment=None):
        return subprocess.run([sys.executable, "-B", str(self.cli), *map(str, arguments)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=self.environment if environment is None else environment)

    def cli_start(self, name="start.json"):
        output = self.root / name
        result = self.command("start", "--repo", self.repo, "--source-path", SOURCE_PATH,
                              "--packet-path", PACKET_PATH, "--task-id", "evaluate-authored-rule",
                              "--scope", "offline-consumer-fixture", "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        return output, json.loads(output.read_bytes())

    def cli_advance(self, previous, operation, name, expected_code):
        output = self.root / name
        result = self.command(operation, "--repo", self.repo, "--previous", previous, "--output", output)
        self.assertEqual(result.returncode, expected_code, result.stderr.decode())
        return output, json.loads(output.read_bytes())

    def seal(self, bundle):
        # Recompute transport integrity after an intentional false assertion.
        bundle["receipt_id"] = session.digest({k: v for k, v in bundle.items() if k != "receipt_id"})
        return bundle

    def assert_no_authority(self, bundle):
        self.assertIs(bundle["effects_authorized"], False)
        self.assertIs(bundle["history_complete"], False)
        self.assertEqual(bundle["llm_calls"], 0)
        self.assertEqual(bundle["session"]["not_observed"], ["ci", "effect_outcome", "authority"])
        if bundle["analysis"] is not None:
            self.assertIs(bundle["analysis"]["effects_authorized"], False)
            for key in ("source_semantic_fidelity", "attribution_authenticity", "real_world_truth", "current_authority"):
                self.assertEqual(bundle["analysis"][key], "NOT_ASSESSED")

    def test_cold_start_and_valid_evaluate_bind_both_committed_inputs(self):
        first = self.start()
        self.assertEqual(first["result"], "READY")
        self.assertIsNone(first["analysis"])
        self.assertIsNone(first["bindings"])
        before = session.canonical(first)
        with patch.object(session.observer, "capture", wraps=session.observer.capture) as acquisition:
            evaluated = consumer.advance(self.repo, first, "EVALUATE")
        self.assertEqual(acquisition.call_count, 1)
        self.assertEqual(session.canonical(first), before)
        self.assertEqual(evaluated["result"], "EVALUATED")
        self.assertEqual(evaluated["session"]["result"], "VALID")
        self.assertEqual(evaluated["session"]["sequence"], 2)
        self.assertEqual(evaluated["analysis"]["truth"], "TRUE")
        self.assertEqual(evaluated["analysis"]["valuation_count"], 1)
        self.assertEqual(evaluated["analysis"]["readings"][0]["table_bits"], "1")
        receipt = evaluated["session"]
        self.assertEqual(receipt["context_id"], receipt["adopted_context_id"])
        self.assertEqual(set(receipt["context"]["dependencies"]), {SOURCE_PATH, PACKET_PATH})
        for role, path, expected in (("source", SOURCE_PATH, SOURCE_A),
                                     ("packet", PACKET_PATH, json_bytes(self.packet_a))):
            captured = receipt["ledger"]["entries"][-1]["capture"]["files"][path]
            self.assertEqual(base64.b64decode(captured["content_b64"]), expected)
            binding = evaluated["bindings"]["files"][role]
            self.assertEqual(binding["path"], path)
            self.assertEqual(binding["sha256"], hashlib.sha256(expected).hexdigest())
            self.assertEqual(binding["blob"], self.git("rev-parse", "HEAD:" + path).decode().strip())
            self.assertEqual({k: v for k, v in binding.items() if k != "path"},
                             receipt["context"]["dependencies"][path]["value"])
        self.assertEqual(evaluated["bindings"]["context_id"], receipt["adopted_context_id"])
        self.assertEqual(evaluated["bindings"]["capture_id"], receipt["capture_id"])
        self.assert_no_authority(evaluated)
        consumer.validate_bundle(evaluated)

    def test_unrelated_commit_keeps_adopted_context(self):
        first = self.start()
        previous_head = first["session"]["ledger"]["entries"][-1]["capture"]["head_start"]
        self.write(OTHER_PATH, b"Unrelated public fixture B.\n")
        self.commit("Only unrelated content changed", OTHER_PATH)
        evaluated = consumer.advance(self.repo, first, "EVALUATE")
        self.assertEqual(evaluated["result"], "EVALUATED")
        self.assertEqual(evaluated["analysis"]["truth"], "TRUE")
        self.assertEqual(evaluated["session"]["context_id"], first["session"]["context_id"])
        self.assertNotEqual(evaluated["bindings"]["head"], previous_head)
        self.assertEqual(set(evaluated["session"]["profile"]["required_paths"]), {SOURCE_PATH, PACKET_PATH})

    def test_dirty_pair_is_not_calculation_input(self):
        first = self.start()
        source_b = SOURCE_A.replace(b"Original offline", b"Dirty alternate")
        packet_b = packet_for(source_b, suspended=True)
        self.write_pair(source_b, packet_b)
        decoy = subprocess.run([sys.executable, "-B", str(Path(bridge.__file__).resolve()),
                                "--source", str(self.repo / SOURCE_PATH),
                                "--packet", str(self.repo / PACKET_PATH)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=self.environment)
        self.assertEqual(decoy.returncode, 0, decoy.stderr.decode())
        self.assertEqual(json.loads(decoy.stdout)["truth"], "FALSE")
        evaluated = consumer.advance(self.repo, first, "EVALUATE")
        self.assertEqual(evaluated["analysis"]["truth"], "TRUE")
        self.assertEqual(evaluated["analysis"]["source_sha256"], hashlib.sha256(SOURCE_A).hexdigest())
        capture = evaluated["session"]["ledger"]["entries"][-1]["capture"]
        self.assertEqual(capture["working_tree_state"], "NOT_OBSERVED")
        self.assertEqual(base64.b64decode(capture["files"][SOURCE_PATH]["content_b64"]), SOURCE_A)
        self.assertEqual(base64.b64decode(capture["files"][PACKET_PATH]["content_b64"]), json_bytes(self.packet_a))

    def test_each_required_file_invalidates_then_explicit_resume(self):
        for changed in ("source", "packet"):
            with self.subTest(changed=changed):
                if changed == "packet":
                    self.write_pair(SOURCE_A, self.packet_a)
                    self.commit("Reset authored pair for second dependency", SOURCE_PATH, PACKET_PATH)
                first = self.start()
                source = SOURCE_A + b"NOTE New committed source revision.\n" if changed == "source" else SOURCE_A
                packet = self.packet_a if changed == "source" else packet_for(source, suspended=True)
                self.write_pair(source, packet)
                path = SOURCE_PATH if changed == "source" else PACKET_PATH
                self.commit("Change just one required dependency", path)
                with patch.object(bridge, "analyze", side_effect=AssertionError("blocked capture was analyzed")):
                    refused = consumer.advance(self.repo, first, "EVALUATE")
                    repeated = consumer.advance(self.repo, refused, "EVALUATE")
                self.assertEqual(refused["result"], "BLOCKED")
                self.assertEqual(refused["session"]["result"], "INVALID")
                self.assertEqual(refused["session"]["context"]["status"], "READY")
                self.assertEqual(repeated["session"]["result"], "RESUME_REQUIRED")
                for bundle in (refused, repeated):
                    self.assertTrue(bundle["session"]["resume_required"])
                    self.assertEqual(bundle["session"]["adopted_context_id"], first["session"]["context_id"])
                    self.assertIsNone(bundle["analysis"])
                    self.assertIsNone(bundle["bindings"])
                if changed == "source":
                    self.write(PACKET_PATH, json_bytes(packet_for(source)))
                    self.commit("Bind packet to changed source before explicit adoption", PACKET_PATH)
                resumed = consumer.advance(self.repo, repeated, "RESUME")
                self.assertEqual(resumed["result"], "READY")
                self.assertIsNone(resumed["analysis"])
                self.assertIsNone(resumed["bindings"])
                self.assertFalse(resumed["session"]["resume_required"])
                evaluated = consumer.advance(self.repo, resumed, "EVALUATE")
                self.assertEqual(evaluated["result"], "EVALUATED")
                self.assertEqual(evaluated["analysis"]["truth"], "TRUE" if changed == "source" else "FALSE")

    def test_missing_packet_latches_across_persisted_cli_chain(self):
        first_path, first = self.cli_start()
        self.git("rm", "--", PACKET_PATH)
        self.git("commit", "-m", "Delete required packet")
        blocked_path, blocked = self.cli_advance(first_path, "evaluate", "missing.json", 1)
        self.assertEqual(blocked["result"], "BLOCKED")
        self.assertEqual(blocked["session"]["result"], "NOT_READY")
        self.assertIsNone(blocked["analysis"])
        self.write(PACKET_PATH, json_bytes(self.packet_a))
        self.commit("Restore packet without adopting it", PACKET_PATH)
        still_path, still = self.cli_advance(blocked_path, "evaluate", "restored-blocked.json", 1)
        self.assertEqual(still["session"]["result"], "RESUME_REQUIRED")
        self.assertIsNone(still["analysis"])
        resumed_path, resumed = self.cli_advance(still_path, "resume", "resumed.json", 0)
        self.assertEqual(resumed["result"], "READY")
        self.assertIsNone(resumed["analysis"])
        _, evaluated = self.cli_advance(resumed_path, "evaluate", "after-resume.json", 0)
        self.assertEqual(evaluated["analysis"]["truth"], "TRUE")
        self.assertEqual(evaluated["session"]["sequence"], 5)
        self.assertEqual(evaluated["session"]["operations"], ["START", "PREFLIGHT", "PREFLIGHT", "RESUME", "PREFLIGHT"])
        self.assertEqual(first["session"]["sequence"], 1)

    def test_unknown_and_withheld_remain_distinct(self):
        for state in ("unknown", "withheld"):
            with self.subTest(state=state):
                self.write(PACKET_PATH, json_bytes(packet_for(SOURCE_A, state=state)))
                self.commit("Supplied availability " + state, PACKET_PATH)
                evaluated = consumer.advance(self.repo, self.start(), "EVALUATE")
                report = evaluated["analysis"]
                self.assertEqual(report["status"], "EVALUATED")
                self.assertEqual(report["truth"], "UNDETERMINED")
                self.assertEqual(report["valuation_count"], 2)
                self.assertEqual(report["possible_values"], [False, True])
                self.assertEqual(report["readings"][0]["table_bits"], "10")
                self.assertEqual(report["observations"]["suspended"]["state"], state)
                self.assertNotIn("value", report["observations"]["suspended"])
                self.assert_no_authority(evaluated)

    def test_unsupported_invalid_and_duplicate_packet_are_not_success(self):
        xor_rule = "RULE lending: member XOR suspended"
        xor_source = ("NOTE Unsupported authored connective.\n" + xor_rule + "\n").encode()
        mismatch = deepcopy(self.packet_a)
        mismatch["source_sha256"] = "0" * 64
        duplicate = json_bytes(self.packet_a).replace(b'"value": false', b'"value": true, "value": false')
        self.assertNotEqual(duplicate, json_bytes(self.packet_a))
        variants = (("xor", xor_source, packet_for(xor_source, rule=xor_rule), "UNSUPPORTED"),
                    ("digest", SOURCE_A, mismatch, "INVALID"),
                    ("duplicate", SOURCE_A, duplicate, "INVALID"))
        for name, source, packet, expected in variants:
            with self.subTest(input=name):
                self.write_pair(source, packet)
                self.commit("Supplied formal input " + name, SOURCE_PATH, PACKET_PATH)
                if name == "duplicate":
                    with self.assertRaises(bridge.BridgeError) as from_bytes:
                        bridge.parse_packet_bytes(duplicate)
                    with self.assertRaises(bridge.BridgeError) as from_file:
                        bridge.read_packet(self.repo / PACKET_PATH)
                    self.assertEqual(from_bytes.exception.code, from_file.exception.code)
                    self.assertEqual(from_bytes.exception.status, "INVALID")
                evaluated = consumer.advance(self.repo, self.start(), "EVALUATE")
                self.assertEqual(evaluated["session"]["result"], "VALID")
                self.assertEqual(evaluated["result"], expected)
                self.assertEqual(evaluated["analysis"]["status"], expected)
                self.assertNotIn("truth", evaluated["analysis"])
                self.assert_no_authority(evaluated)
        self.write_pair(SOURCE_A, self.packet_a)
        self.assertEqual(bridge.read_packet(self.repo / PACKET_PATH), self.packet_a)
        self.assertEqual(bridge.parse_packet_bytes(json_bytes(self.packet_a)), self.packet_a)

    def test_closed_paths_root_and_scope(self):
        for source, packet, scope in ((SOURCE_PATH, SOURCE_PATH, "scope"),
                                      ("../source.txt", PACKET_PATH, "scope"),
                                      ("./rules/source.txt", PACKET_PATH, "scope"),
                                      (SOURCE_PATH, PACKET_PATH, "")):
            with self.subTest(source=source, packet=packet, scope=scope):
                with patch.object(session.observer, "capture", side_effect=AssertionError("invalid profile acquired Git")):
                    with self.assertRaises(ValueError):
                        consumer.start(self.repo, source, packet, task_id="fixed-task", scope=scope)
        first = self.start()
        other_root = self.root / "other-local-address"
        other_root.mkdir()
        with patch.object(session.observer, "capture", side_effect=AssertionError("foreign root acquired Git")):
            with self.assertRaises(ValueError):
                consumer.advance(other_root, first, "EVALUATE")
        narrow_profile = session.make_profile(self.repo, "evaluate-authored-rule", "offline-consumer-fixture",
                                               [SOURCE_PATH, PACKET_PATH], [SOURCE_PATH])
        narrower = deepcopy(first)
        narrower["session"] = session.start(self.repo, narrow_profile)
        with self.assertRaises(ValueError):
            consumer.validate_bundle(self.seal(narrower))
        scope_mismatch = deepcopy(first)
        scope_mismatch["session"]["profile"]["scope"] = "different-supplied-scope"
        scope_mismatch["session"]["profile_digest"] = session.digest(scope_mismatch["session"]["profile"])
        nested = scope_mismatch["session"]
        nested["receipt_id"] = session.digest({k: v for k, v in nested.items() if k != "receipt_id"})
        with self.assertRaises(ValueError):
            consumer.validate_bundle(self.seal(scope_mismatch))

    def test_resealed_analysis_and_binding_forgery_rejected(self):
        evaluated = consumer.advance(self.repo, self.start(), "EVALUATE")
        false_analysis = deepcopy(evaluated)
        false_analysis["analysis"]["truth"] = "FALSE"
        false_analysis["analysis"]["possible_values"] = [False]
        false_analysis["analysis"]["readings"][0]["table_bits"] = "0"
        false_identity = deepcopy(evaluated)
        false_identity["bindings"]["files"]["source"]["sha256"] = "0" * 64
        false_context = deepcopy(evaluated)
        false_context["bindings"]["context_id"] = "0" * 64
        for name, changed in (("truth", false_analysis), ("identity", false_identity), ("context", false_context)):
            with self.subTest(assertion=name):
                with self.assertRaises(ValueError):
                    consumer.validate_bundle(self.seal(changed))
        self.assertEqual(consumer.inspect_bundle(evaluated)["captured_result"], "EVALUATED")

    def test_crossprocess_inspect_and_exclusive_publication(self):
        first_path, _ = self.cli_start()
        evaluated_path, evaluated = self.cli_advance(first_path, "evaluate", "evaluated.json", 0)
        original = evaluated_path.read_bytes()
        first_bytes = first_path.read_bytes()
        empty_path = self.root / "empty-executable-path"
        empty_path.mkdir()
        without_git = dict(self.environment, PATH=str(empty_path))
        inspected = self.command("inspect", "--input", evaluated_path, environment=without_git)
        self.assertEqual(inspected.returncode, 0, inspected.stderr.decode())
        view = json.loads(inspected.stdout)
        self.assertEqual(view["view"], "HISTORICAL_ONLY")
        self.assertIs(view["requires_fresh_capture"], True)
        self.assertIs(view["effects_authorized"], False)
        self.assertEqual(view["receipt_id"], evaluated["receipt_id"])
        overwrite = self.command("evaluate", "--repo", self.repo, "--previous", first_path,
                                  "--output", evaluated_path)
        self.assertEqual(overwrite.returncode, 2)
        self.assertEqual(evaluated_path.read_bytes(), original)
        inside = self.repo / "new-consumer-output.json"
        rejected = self.command("evaluate", "--repo", self.repo, "--previous", evaluated_path, "--output", inside)
        self.assertEqual(rejected.returncode, 2)
        self.assertFalse(inside.exists())
        target = self.root / "simulated-link-failure.json"
        args = ["evaluate", "--repo", str(self.repo), "--previous", str(evaluated_path), "--output", str(target)]
        with patch.object(session.os, "link", side_effect=OSError("simulated refusal before publication")):
            with patch("sys.stdout"), patch("sys.stderr"):
                self.assertEqual(consumer.main(args), 2)
        self.assertFalse(target.exists())
        self.assertEqual(evaluated_path.read_bytes(), original)
        self.assertEqual(first_path.read_bytes(), first_bytes)

    def test_source_and_packet_byte_bounds_remain_explicit(self):
        oversized_source = b"NOTE " + b"x" * 65536 + b"\n" + RULE.encode() + b"\n"
        oversized_packet = b" " * 131073 + json_bytes(self.packet_a)
        for name, source, packet, code in (
                ("source", oversized_source, packet_for(oversized_source), "source_size_bound"),
                ("packet", SOURCE_A, oversized_packet, "input_size_bound")):
            with self.subTest(input=name):
                self.write_pair(source, packet)
                self.commit("Above Bridge input bound " + name, SOURCE_PATH, PACKET_PATH)
                evaluated = consumer.advance(self.repo, self.start(), "EVALUATE")
                self.assertEqual(evaluated["session"]["result"], "VALID")
                self.assertEqual(evaluated["result"], "UNSUPPORTED")
                self.assertEqual(evaluated["analysis"]["errors"][0]["code"], code)
                self.assertNotIn("truth", evaluated["analysis"])

    def test_capture_limit_does_not_truncate_or_reset(self):
        bundle = self.start()
        for _ in range(31):
            bundle = consumer.advance(self.repo, bundle, "RESUME")
        self.assertEqual(bundle["session"]["sequence"], 32)
        self.assertEqual(bundle["session"]["ledger"]["count"], 32)
        self.assertEqual(len(bundle["session"]["ledger"]["entries"]), 32)
        consumer.validate_bundle(bundle)
        original = session.canonical(bundle)
        with patch.object(session.observer, "capture", side_effect=AssertionError("33rd capture attempted")):
            with self.assertRaises(ValueError):
                consumer.advance(self.repo, bundle, "EVALUATE")
        self.assertEqual(session.canonical(bundle), original)


if __name__ == "__main__":
    unittest.main()
