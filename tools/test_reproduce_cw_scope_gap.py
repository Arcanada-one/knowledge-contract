#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Finite controls for a new replay, with no writes to historical evidence."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

try:
    from . import reproduce_cw_scope_gap as replay
except ImportError:
    import reproduce_cw_scope_gap as replay


class ScopeGapReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = replay.reproduce()

    def test_real_pinned_history_accepts_and_copies_both_mutants_then_refuses_them(self):
        self.assertEqual(self.report["status"], "REPRODUCED")
        self.assertEqual(self.report["artifact_kind"], "new_synthetic_replay")
        self.assertIs(self.report["original_c167_bytes_recovered"], False)
        self.assertEqual(self.report["native_requests_executed"], 0)
        self.assertEqual(self.report["provenance"]["inputs_from_commit"],
                         "9ba73c9971ceb0f02b91946d5061ef4f961df772")
        cases = {row["paper_id"]: row for row in self.report["cases"]}
        expected = {
            "CW-P02": ("domain_model", "Certified causal productivity increase of 99% in all workplaces."),
            "CW-P01": ("review", "This literature review proves universal real-world profit gains."),
        }
        self.assertEqual(set(cases), set(expected))
        for paper, (claim_class, scope) in expected.items():
            with self.subTest(paper=paper):
                case = cases[paper]
                self.assertTrue(case["only_claim_scope_changed"])
                self.assertEqual(case["claim_class_unchanged"], claim_class)
                self.assertEqual(case["synthetic_scope"], scope)
                old, new = case["observations"]["historical"], case["observations"]["corrected"]
                self.assertEqual((old["full_validation"], old["instantiation"], old["instance_validation"]),
                                 ("ACCEPTED", "ACCEPTED", "ACCEPTED"))
                self.assertEqual(old["generated_claim_scope"], scope)
                self.assertEqual((old["release_instance_count"], old["release_stage_count"]), (16, 96))
                self.assertEqual(new["outcome"], "REFUSED")
                self.assertEqual(new["refused_by"], "validate")
                self.assertEqual(new["reason"], "paper release claim scope changed without reviewed revision: " + paper)

    def test_unmodified_graph_passes_both_validators_with_exact_blob_provenance(self):
        self.assertTrue(all(row["outcome"] == "ACCEPTED" for row in self.report["baseline"].values()))
        sources = {row["label"]: row for row in self.report["provenance"]["sources"]}
        self.assertEqual(sources["corrected"]["commit"], "9cbcd22fc215e8089363912dc531e42ef6845e29")
        for label, checker_blob in (("historical", "24adea75bd01aa07c9a46c3b837ef2779c2a69b7"),
                                    ("corrected", "2fa62c24e66d24eb0bc7dd716b56277817acac53")):
            objects = {row["path"]: row for row in sources[label]["objects"]}
            self.assertEqual(objects[replay.CHECKER_PATH]["git_blob"], checker_blob)
            self.assertEqual(objects[replay.GRAPH_PATH]["git_blob"], "0471a791e329f2f0f38ad8645a6c99f7246558a1")
            self.assertEqual(objects[replay.GRAPH_PATH]["sha256"],
                             "8c7b7e6fb1f95df9f9c1c85ce083fa7ba3250ed6637ae7ce1a41d6cc1c49e3a6")
            self.assertEqual(set(objects), {replay.CHECKER_PATH, replay.GRAPH_PATH, replay.STEPS_PATH,
                                            replay.README_PATH, replay.EXPERIMENTS_PATH})

    def test_working_tree_input_reads_cannot_substitute_for_pinned_history(self):
        # Disallow Python input-file reads: all original data must still arrive
        # through Git. This also works when the checked-out input files differ.
        with patch.object(Path, "read_bytes", side_effect=AssertionError("working-tree read")), \
                patch.object(Path, "read_text", side_effect=AssertionError("working-tree read")):
            self.assertEqual(replay.reproduce()["status"], "REPRODUCED")

    def test_same_json_with_changed_blob_bytes_is_refused(self):
        actual_git = replay._git
        identity = replay.HISTORICAL_COMMIT + ":" + replay.GRAPH_PATH

        def changed_payload(repository, *arguments):
            raw = actual_git(repository, *arguments)
            return raw + b"\n" if arguments == ("show", identity) else raw

        with patch.object(replay, "_git", side_effect=changed_payload):
            with self.assertRaisesRegex(replay.ReplayError, "Pinned Git blob bytes differ"):
                replay.reproduce()

    def test_wrong_path_blob_is_refused_before_validator_execution(self):
        actual_git = replay._git
        identity = replay.HISTORICAL_COMMIT + ":" + replay.CHECKER_PATH

        def wrong_binding(repository, *arguments):
            if arguments == ("rev-parse", "--verify", identity):
                return (replay.CHECKER_BLOBS[replay.CORRECTED_COMMIT] + "\n").encode("ascii")
            return actual_git(repository, *arguments)

        with patch.object(replay, "_git", side_effect=wrong_binding), \
                patch.object(replay, "load_validator") as load:
            with self.assertRaisesRegex(replay.ReplayError, "Pinned Git path differs"):
                replay.reproduce()
            load.assert_not_called()

    def test_regressed_comparison_does_not_get_a_success_report(self):
        actual_load = replay.load_validator
        old = None

        def replace_comparison(raw, repository, commit):
            nonlocal old
            if commit == replay.HISTORICAL_COMMIT:
                old = actual_load(raw, repository, commit)
                return old
            return old

        with patch.object(replay, "load_validator", side_effect=replace_comparison):
            report = replay.reproduce()
        self.assertEqual(report["status"], "NOT_REPRODUCED")
        for case in report["cases"]:
            self.assertEqual(case["observations"]["corrected"]["outcome"], "ACCEPTED")
            self.assertFalse(case["expected_contrast_observed"])

    def test_missing_local_history_emits_json_error_without_fallback(self):
        with tempfile.TemporaryDirectory() as empty_repository, redirect_stdout(io.StringIO()) as output:
            code = replay.main(["--repo", empty_repository])
        self.assertEqual(code, 2)
        report = json.loads(output.getvalue())
        self.assertEqual(report["status"], "ERROR")
        self.assertIn("fetch-depth: 0", report["error"])
        self.assertIn("No fetch or fallback", report["error"])
        self.assertIs(report["original_c167_bytes_recovered"], False)

    def test_cli_produces_the_observed_report(self):
        result = subprocess.run([sys.executable, "-B", str(Path(replay.__file__)), "--repo", str(replay.ROOT)],
                                check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), self.report)


if __name__ == "__main__":
    unittest.main()
