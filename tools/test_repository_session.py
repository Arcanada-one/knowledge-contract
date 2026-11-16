# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Repository Session lifecycle checks with real Git and fresh CLI processes.

Git command output and the reference model are never mocked. One acquisition
counter wraps the actual observer to check the one-capture-per-resume contract.
"""
from copy import deepcopy
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

try:
    from tools import repository_session as session
except ImportError:
    import repository_session as session


class RepositorySessionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.repo = self.root / "repository"
        self.repo.mkdir()
        self.git("init", "--initial-branch=main")
        self.git("config", "user.name", "Local session integration test")
        self.git("config", "user.email", "session-test@example.invalid")
        self.write("source.txt", b"Required source, first revision.\n")
        self.write("other.txt", b"Other source, first revision.\n")
        self.commit("Initial files", "source.txt", "other.txt")
        self.profile = session.make_profile(self.repo, "review-source", "session-fixture",
                                            ["source.txt", "other.txt"], ["source.txt"])
        self.cli = Path(session.__file__).resolve()

    def git(self, *arguments):
        return subprocess.run(["git", "-C", str(self.repo), *arguments], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    def write(self, path, data):
        (self.repo / path).write_bytes(data)

    def commit(self, message, *paths):
        self.git("add", "--", *paths)
        self.git("commit", "-m", message)

    def command(self, *arguments):
        return subprocess.run([sys.executable, "-B", str(self.cli), *map(str, arguments)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def seal(self, receipt):
        receipt["receipt_id"] = session.digest({k: v for k, v in receipt.items() if k != "receipt_id"})
        return receipt

    def test_start_binds_actual_bytes_and_inspection_is_historical(self):
        receipt = session.start(self.repo, self.profile)
        self.assertEqual(receipt["result"], "READY")
        self.assertEqual(receipt["sequence"], 1)
        self.assertIsNone(receipt["predecessor"])
        blob = self.git("rev-parse", "HEAD:source.txt").decode().strip()
        self.assertEqual(receipt["context"]["dependencies"]["source.txt"]["value"]["blob"], blob)
        self.assertEqual(set(receipt["context"]["dependencies"]), {"source.txt"})
        self.assertNotIn("model_id", receipt["context"])
        view = session.inspect_receipt(receipt)
        self.assertEqual(view["view"], "HISTORICAL_ONLY")
        self.assertTrue(view["requires_fresh_capture"])
        self.assertFalse(view["readiness_grants_permission"])
        self.assertEqual(receipt["not_observed"], ["ci", "effect_outcome", "authority"])
        self.assertEqual(receipt["llm_calls"], 0)

    def test_required_change_invalidates_preflight_even_when_new_context_is_ready(self):
        first = session.start(self.repo, self.profile)
        self.write("source.txt", b"Required source, second revision.\n")
        self.commit("Relevant change", "source.txt")
        checked = session.preflight(self.repo, self.profile, first)
        self.assertEqual(checked["context"]["status"], "READY")
        self.assertEqual(checked["prior_validation"]["status"], "INVALID")
        self.assertEqual(checked["result"], "INVALID")
        self.assertNotEqual(checked["context_id"], first["context_id"])
        resumed = session.resume(self.repo, self.profile, first)
        self.assertEqual(resumed["result"], "READY")
        self.assertEqual(resumed["prior_validation"]["status"], "INVALID")
        self.assertEqual(resumed["context_id"], checked["context_id"])

    def test_repeated_failed_preflight_requires_explicit_resume_to_adopt(self):
        first = session.start(self.repo, self.profile)
        self.write("source.txt", b"New required content awaiting explicit adoption.\n")
        self.commit("Required change before preflight chain", "source.txt")
        refused = session.preflight(self.repo, self.profile, first)
        repeated = session.preflight(self.repo, self.profile, refused)
        repeated_again = session.preflight(self.repo, self.profile, repeated)
        self.assertEqual(refused["result"], "INVALID")
        for receipt in (refused, repeated, repeated_again):
            self.assertEqual(receipt["context"]["status"], "READY")
            self.assertEqual(receipt["adopted_context_id"], first["context_id"])
            self.assertNotEqual(receipt["context_id"], receipt["adopted_context_id"])
            self.assertTrue(receipt["resume_required"])
        self.assertEqual(repeated["result"], "RESUME_REQUIRED")
        self.assertEqual(repeated_again["result"], "RESUME_REQUIRED")
        adopted = session.resume(self.repo, self.profile, repeated_again)
        checked = session.preflight(self.repo, self.profile, adopted)
        self.assertEqual(adopted["result"], "READY")
        self.assertEqual(adopted["adopted_context_id"], repeated_again["context_id"])
        self.assertFalse(adopted["resume_required"])
        self.assertEqual(checked["result"], "VALID")
        self.assertEqual(checked["operations"], ["START", "PREFLIGHT", "PREFLIGHT", "PREFLIGHT", "RESUME", "PREFLIGHT"])
        broken = deepcopy(repeated)
        broken["resume_required"] = False
        broken["adopted_context_id"] = broken["context_id"]
        broken["result"] = "VALID"
        with self.assertRaises(ValueError):
            session.validate_receipt(self.seal(broken))

    def test_failed_resume_does_not_allow_preflight_to_adopt_recovered_content(self):
        first = session.start(self.repo, self.profile)
        self.git("rm", "source.txt")
        self.git("commit", "-m", "Remove required file")
        failed = session.resume(self.repo, self.profile, first)
        self.assertEqual(failed["result"], "NOT_READY")
        self.assertTrue(failed["resume_required"])
        self.assertIsNone(failed["adopted_context_id"])
        self.write("source.txt", b"Recovered required content.\n")
        self.commit("Restore file after failed resume", "source.txt")
        candidate = session.preflight(self.repo, self.profile, failed)
        self.assertEqual(candidate["context"]["status"], "READY")
        self.assertEqual(candidate["result"], "RESUME_REQUIRED")
        self.assertIsNone(candidate["adopted_context_id"])
        resumed = session.resume(self.repo, self.profile, candidate)
        self.assertEqual(resumed["result"], "READY")
        self.assertFalse(resumed["resume_required"])

    def test_unrelated_change_and_repeated_resume_keep_semantic_identity(self):
        first = session.start(self.repo, self.profile)
        original = session.canonical(first)
        self.write("other.txt", b"Other source, new revision.\n")
        self.commit("Unrelated required-file context", "other.txt")
        second = session.resume(self.repo, self.profile, first)
        third = session.resume(self.repo, self.profile, second)
        self.assertEqual(second["prior_validation"]["status"], "VALID")
        self.assertEqual(first["context_id"], second["context_id"])
        self.assertEqual(second["context_id"], third["context_id"])
        self.assertNotEqual(first["capture_id"], second["capture_id"])
        self.assertNotEqual(second["receipt_id"], third["receipt_id"])
        self.assertEqual(third["sequence"], 3)
        replay = session.observer.replay_ledger(third["ledger"], ["source.txt"])
        self.assertEqual(replay["steps"][-1]["events_ingested"], 0)
        self.assertEqual(session.canonical(first), original)
        second["ledger"]["entries"][0]["capture"]["scope"] = "modified-successor"
        self.assertEqual(session.canonical(first), original)

    def test_unavailable_repository_blocks_until_a_new_successful_capture(self):
        first = session.start(self.repo, self.profile)
        saved_git = self.root / "temporarily-unavailable-git"
        (self.repo / ".git").rename(saved_git)
        try:
            unavailable = session.resume(self.repo, self.profile, first)
        finally:
            saved_git.rename(self.repo / ".git")
        self.assertEqual(unavailable["result"], "NOT_READY")
        self.assertEqual(unavailable["ledger"]["entries"][-1]["capture"]["status"], "UNAVAILABLE")
        self.assertEqual(unavailable["prior_validation"]["status"], "INVALID")
        recovered = session.resume(self.repo, self.profile, unavailable)
        self.assertEqual(recovered["result"], "READY")
        self.assertEqual(recovered["sequence"], 3)
        self.assertEqual(recovered["context_id"], first["context_id"])

    def test_absent_required_file_denies_readiness_then_creation_recovers(self):
        profile = session.make_profile(self.repo, "missing-file", "session-fixture", ["missing.txt"])
        missing = session.start(self.repo, profile)
        self.assertEqual(missing["ledger"]["entries"][0]["capture"]["status"], "OK")
        self.assertEqual(missing["result"], "NOT_READY")
        self.write("missing.txt", b"Now committed.\n")
        self.commit("Create required file", "missing.txt")
        recovered = session.resume(self.repo, profile, missing)
        self.assertEqual(recovered["result"], "READY")

    def test_frozen_task_scope_profile_and_repository_are_checked_before_capture(self):
        first = session.start(self.repo, self.profile)
        for field, value in (("task_id", "another-task"), ("scope", "another-scope"),
                             ("producer", "another-producer"), ("required_paths", ["other.txt"]),
                             ("budget", 99)):
            with self.subTest(field=field):
                profile = deepcopy(self.profile)
                profile[field] = value
                with patch.object(session.observer, "capture", wraps=session.observer.capture) as capture:
                    with self.assertRaisesRegex(ValueError, "profile differs"):
                        session.resume(self.repo, profile, first)
                    capture.assert_not_called()
        with self.assertRaisesRegex(ValueError, "repository root differs"):
            session.resume(self.root, self.profile, first)
        for paths in (["."], ["../source.txt"], ["source.txt", "source.txt"], [f"p{i}" for i in range(33)]):
            with self.subTest(paths=paths), self.assertRaises(ValueError):
                session.make_profile(self.repo, "x", "x", paths)
        with self.assertRaises(ValueError):
            session.make_profile(self.repo, "x", "x", ["source.txt"], budget=True)

    def test_resume_performs_one_actual_capture_and_preserves_predecessor(self):
        first = session.start(self.repo, self.profile)
        before = session.canonical(first)
        with patch.object(session.observer, "capture", wraps=session.observer.capture) as capture:
            second = session.resume(self.repo, self.profile, first)
            capture.assert_called_once()
        self.assertEqual(second["sequence"], first["sequence"] + 1)
        self.assertEqual(second["ledger"]["entries"][:-1], first["ledger"]["entries"])
        self.assertEqual(second["predecessor"]["receipt_id"], first["receipt_id"])
        self.assertEqual(session.canonical(first), before)

    def test_tampered_and_rehashed_semantically_wrong_receipts_are_rejected(self):
        first = session.start(self.repo, self.profile)
        broken = deepcopy(first)
        broken["result"] = "INVALID"
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            session.validate_receipt(broken)
        with self.assertRaisesRegex(ValueError, "result does not match"):
            session.validate_receipt(self.seal(broken))
        broken = deepcopy(first)
        broken["context"]["cost"] = True
        with self.assertRaisesRegex(ValueError, "context does not match"):
            session.validate_receipt(self.seal(broken))
        broken = deepcopy(first)
        broken["ledger"]["entries"][0]["capture"]["files"]["source.txt"]["content_b64"] = "AA=="
        with self.assertRaises(ValueError):
            session.validate_receipt(self.seal(broken))

    def test_json_duplicate_keys_nested_escaped_and_torn_input_are_rejected(self):
        receipt = session.start(self.repo, self.profile)
        plain = json.dumps(receipt)
        cases = [
            plain.replace('"result": "READY"', '"result": "INVALID", "result": "READY"', 1),
            plain.replace('"task_id": "review-source"', '"task_id": "other", "task_id": "review-source"', 1),
            '{"nested": [{"key": 1, "key": 2}]}',
            r'{"nested": {"scope": "a", "\u0073cope": "b"}}',
        ]
        path = self.root / "untrusted.json"
        for value in cases:
            with self.subTest(value=value[:100]):
                path.write_text(value)
                with self.assertRaisesRegex(ValueError, "duplicate JSON member"):
                    session.read_json(path)
        for value in (plain[:-1], '{"x": NaN}', '{"x": Infinity}', '{"x": -Infinity}'):
            path.write_text(value)
            with self.assertRaises(ValueError):
                session.read_json(path)

    def test_fresh_process_lifecycle_and_exclusive_output(self):
        profile_path, first_path = self.root / "profile.json", self.root / "first.json"
        result = self.command("profile", "--repo", self.repo, "--task-id", "cli-task", "--scope", "cli-scope",
                              "--path", "source.txt", "--output", profile_path)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.command("start", "--repo", self.repo, "--profile", profile_path, "--output", first_path)
        self.assertEqual(result.returncode, 0, result.stderr)
        first_bytes = first_path.read_bytes()
        first = session.read_json(first_path)
        inspected = self.command("inspect", "--input", first_path)
        self.assertEqual(inspected.returncode, 0, inspected.stderr)
        self.assertEqual(json.loads(inspected.stdout)["view"], "HISTORICAL_ONLY")
        second_path = self.root / "second.json"
        result = self.command("resume", "--repo", self.repo, "--profile", profile_path,
                              "--previous", first_path, "--output", second_path)
        self.assertEqual(result.returncode, 0, result.stderr)
        second = session.read_json(second_path)
        self.assertEqual(first["context_id"], second["context_id"])
        self.write("source.txt", b"New source after process restart.\n")
        self.commit("Changed before preflight", "source.txt")
        third_path = self.root / "preflight.json"
        result = self.command("preflight", "--repo", self.repo, "--profile", profile_path,
                              "--previous", second_path, "--output", third_path)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(session.read_json(third_path)["result"], "INVALID")
        overwrite = self.command("resume", "--repo", self.repo, "--profile", profile_path,
                                 "--previous", second_path, "--output", first_path)
        self.assertEqual(overwrite.returncode, 2)
        self.assertEqual(first_path.read_bytes(), first_bytes)
        inside = self.command("start", "--repo", self.repo, "--profile", profile_path,
                              "--output", self.repo / "receipt.json")
        self.assertEqual(inside.returncode, 2)
        self.assertFalse((self.repo / "receipt.json").exists())

    def test_budget_refusal_remains_separate_from_file_presence(self):
        profile = deepcopy(self.profile)
        profile["budget"] = 0
        receipt = session.start(self.repo, profile)
        self.assertEqual(receipt["ledger"]["entries"][0]["capture"]["files"]["source.txt"]["state"], "PRESENT")
        self.assertEqual(receipt["result"], "NOT_FIT")
        self.assertEqual(receipt["context"]["required_cost"], 1)
        self.assertEqual(receipt["context"]["budget"], 0)

    def test_session_preserves_configured_clean_filter_boundary(self):
        self.write(".gitattributes", b"source.txt filter=session-marker\n")
        self.commit("Attributes without configured filter", ".gitattributes")
        marker = self.root / "filter-ran"
        program = ("import pathlib,sys; pathlib.Path(" + repr(str(marker)) +
                   ").write_text('executed'); sys.stdout.buffer.write(sys.stdin.buffer.read())")
        self.git("config", "filter.session-marker.clean", shlex.quote(sys.executable) + " -c " + shlex.quote(program))
        self.write("source.txt", b"Unstaged working-tree bytes.\n")
        first = session.start(self.repo, self.profile)
        second = session.preflight(self.repo, self.profile, first)
        self.assertEqual(first["result"], "READY")
        self.assertEqual(second["result"], "VALID")
        self.assertFalse(marker.exists())
        self.assertEqual(first["ledger"]["entries"][0]["capture"]["working_tree_state"], "NOT_OBSERVED")


if __name__ == "__main__":
    unittest.main()
