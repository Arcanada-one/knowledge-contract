"""Integration checks of actual local Git observations and the situation bridge.

The repository adapter is exercised through its public API and CLI. Fixtures are
real temporary Git repositories; neither Git output nor situation.Model is
mocked. These tests check the declared adapter boundary, not LLM performance.
"""

import base64
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest

try:
    from tools import repository_observer as observer
except ImportError:
    import repository_observer as observer


def without_model_ids(value):
    """Ignore only a fresh Model instance's opaque local identifier on replay."""
    if isinstance(value, dict):
        return {k: without_model_ids(v) for k, v in value.items() if k != "model_id"}
    if isinstance(value, list):
        return [without_model_ids(v) for v in value]
    return value


class RepositoryObserverTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.repo = self.root / "repository"
        self.repo.mkdir()
        self.git("init", "--initial-branch=main")
        self.git("config", "user.name", "Local adapter integration test")
        self.git("config", "user.email", "local-test@example.invalid")
        self.write("source.txt", b"Pinned source, revision one.\n")
        self.write("unrelated.txt", b"Unrelated revision one.\n")
        self.commit("Initial source", "source.txt", "unrelated.txt")
        self.scope = "offline-integration-sandbox"

    def git(self, *arguments):
        completed = subprocess.run(
            ["git", "-C", str(self.repo), *arguments],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        return completed.stdout

    def write(self, path, content):
        destination = self.repo / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)

    def commit(self, message, *paths):
        self.git("add", "--", *paths)
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD").decode().strip()

    def capture(self, paths=None, producer="local-git"):
        return observer.capture(
            self.repo, paths or ["source.txt"], self.scope, producer=producer,
        )

    def replay(self, captures, required=None):
        return observer.replay_ledger(
            observer.make_ledger(captures), required or ["source.txt"], budget=10000,
        )

    def test_cold_read_is_bound_to_real_commit_blobs_without_unselected_data(self):
        secret = "untracked-secret-must-not-enter-observation"
        self.write("untracked.env", secret.encode())
        self.git("config", "remote.origin.url", "https://example.invalid/" + secret)
        receipt = self.capture()
        head = self.git("rev-parse", "HEAD").decode().strip()
        blob = self.git("rev-parse", head + ":source.txt").decode().strip()
        committed = self.git("cat-file", "blob", blob)
        self.assertEqual(receipt["status"], "OK")
        self.assertEqual(receipt["head_start"], head)
        self.assertEqual(receipt["head_end"], head)
        self.assertEqual(receipt["clock_domain"], "unix-nanoseconds")
        self.assertIs(type(receipt["observed_at"]), int)
        file = receipt["files"]["source.txt"]
        self.assertEqual(file["state"], "PRESENT")
        self.assertEqual(file["blob"], blob)
        self.assertEqual(file["size"], len(committed))
        self.assertEqual(file["sha256"], hashlib.sha256(committed).hexdigest())
        self.assertEqual(base64.b64decode(file["content_b64"], validate=True), committed)
        self.assertNotIn(secret, json.dumps(receipt))
        replay = self.replay([receipt])
        self.assertEqual(replay["steps"][0]["context"]["status"], "READY")
        self.assertIsNone(replay["steps"][0]["prior_validation"])
        self.assertEqual(set(replay["not_observed"]), {"ci", "effect_outcome", "authority"})

    def test_relevant_blob_change_invalidates_but_unrelated_commit_does_not(self):
        first = self.capture()
        self.write("unrelated.txt", b"Unrelated revision two.\n")
        self.commit("Unrelated update", "unrelated.txt")
        unrelated = self.capture()
        difference = observer.compare_captures(first, unrelated)
        self.assertTrue(difference["head_changed"])
        self.assertEqual(difference["changed"], [])
        self.assertEqual(difference["unchanged"], ["source.txt"])
        self.write("source.txt", b"Pinned source, revision two.\n")
        self.commit("Source update", "source.txt")
        changed = self.capture()
        difference = observer.compare_captures(unrelated, changed)
        self.assertEqual(difference["changed"], ["source.txt"])
        replay = self.replay([first, unrelated, changed])
        self.assertEqual(replay["steps"][1]["prior_validation"]["status"], "VALID")
        self.assertEqual(replay["steps"][2]["prior_validation"]["status"], "INVALID")
        self.assertEqual(replay["steps"][2]["context"]["status"], "READY")

    def test_selected_index_reports_staging_without_rebinding_committed_content(self):
        clean = self.capture()
        self.write("source.txt", b"Uncommitted content must remain distinct.\n")
        dirty = self.capture()
        self.assertEqual(dirty["head_start"], clean["head_start"])
        self.assertEqual(dirty["files"]["source.txt"], clean["files"]["source.txt"])
        self.assertEqual(dirty["working_tree_state"], "NOT_OBSERVED")
        self.assertEqual(dirty["selected_index_b64"], clean["selected_index_b64"])
        self.assertEqual(observer.compare_captures(clean, dirty)["unchanged"], ["source.txt"])
        self.git("add", "--", "source.txt")
        staged = self.capture()
        stage_blob = self.git("rev-parse", ":source.txt").strip()
        index = base64.b64decode(staged["selected_index_b64"], validate=True)
        self.assertIn(stage_blob + b" 0\tsource.txt\0", index)
        self.assertNotEqual(staged["selected_index_b64"], clean["selected_index_b64"])
        self.assertEqual(staged["working_tree_state"], "NOT_OBSERVED")
        self.assertEqual(staged["files"]["source.txt"], clean["files"]["source.txt"])

    def test_read_only_capture_does_not_execute_configured_clean_filter(self):
        marker = self.root / "filter-executed.txt"
        script = self.root / "recording_filter.py"
        script.write_text(
            "from pathlib import Path\nimport sys\n"
            "Path(" + repr(str(marker)) + ").write_text('filter executed')\n"
            "sys.stdout.buffer.write(sys.stdin.buffer.read())\n",
            encoding="utf-8",
        )
        self.write(".gitattributes", b"source.txt filter=recording\n")
        command = shlex.quote(sys.executable) + " " + shlex.quote(str(script))
        self.git("config", "filter.recording.clean", command)
        self.commit("Configure a local content conversion filter", ".gitattributes")
        marker.unlink(missing_ok=True)
        old = (self.repo / "source.txt").read_bytes()
        # Equal size forces Git's status refresh to inspect content instead of
        # deciding solely from a size mismatch. A read-only observer must not
        # execute a repository-configured command along that path.
        self.write("source.txt", b"x" * len(old))
        receipt = self.capture()
        self.assertFalse(marker.exists(), "capture executed repository clean filter")
        if receipt["status"] == "OK":
            self.assertEqual(base64.b64decode(receipt["files"]["source.txt"]["content_b64"]), old)

    def test_replay_preserves_observation_times_and_rejects_altered_capture(self):
        first = self.capture()
        second = self.capture()
        ledger = observer.make_ledger([first, second])
        retained = json.loads(json.dumps(ledger))
        a = observer.replay_ledger(ledger, ["source.txt"], budget=10000)
        b = observer.replay_ledger(retained, ["source.txt"], budget=10000)
        self.assertEqual(without_model_ids(a["steps"]), without_model_ids(b["steps"]))
        self.assertEqual(sum(s["events_ingested"] for s in a["steps"]),
                         sum(s["events_ingested"] for s in b["steps"]))
        self.assertEqual([s["observed_at"] for s in a["steps"]],
                         [first["observed_at"], second["observed_at"]])
        self.assertEqual(sum(s["events_ingested"] for s in a["steps"]), 1)
        self.assertEqual(ledger, retained)
        altered = deepcopy(ledger)
        altered["entries"][0]["capture"]["files"]["source.txt"]["content_b64"] = base64.b64encode(b"altered").decode()
        with self.assertRaises(ValueError):
            observer.replay_ledger(altered, ["source.txt"], budget=10000)
        altered_receipt = deepcopy(first)
        altered_receipt["observed_at"] += 1
        with self.assertRaises(ValueError):
            observer.compare_captures(altered_receipt, second)

    def test_absent_required_path_blocks_then_actual_committed_creation_recovers(self):
        missing = self.capture(["missing.txt"])
        self.assertEqual(missing["files"]["missing.txt"]["state"], "ABSENT")
        self.assertEqual(self.replay([missing], ["missing.txt"])["steps"][0]["context"]["status"], "NOT_READY")
        self.write("missing.txt", b"Newly observed committed file.\n")
        self.commit("Create formerly missing file", "missing.txt")
        present = self.capture(["missing.txt"])
        self.assertEqual(self.replay([missing, present], ["missing.txt"])["steps"][-1]["context"]["status"], "READY")

    def test_different_producers_disagree_without_implicit_last_writer_precedence(self):
        source_a = self.capture(producer="reader-a")
        self.write("source.txt", b"A different observed value.\n")
        self.commit("Second producer's observation", "source.txt")
        source_b = self.capture(producer="reader-b")
        replay = self.replay([source_a, source_b])
        context = replay["steps"][-1]["context"]
        self.assertEqual(context["status"], "NOT_READY")
        self.assertTrue(any("CONFLICT" in reason for reason in context["reasons"]))
        with self.assertRaises(ValueError):
            observer.compare_captures(source_a, source_b)

    def test_snapshot_after_missed_commit_recovers_latest_without_claiming_complete_history(self):
        first = self.capture()
        self.write("source.txt", b"Intermediate value never observed by the adapter.\n")
        self.commit("Unobserved intermediate update", "source.txt")
        latest_bytes = b"Latest value actually observed.\n"
        self.write("source.txt", latest_bytes)
        head = self.commit("Latest update", "source.txt")
        latest = self.capture()
        self.assertEqual(latest["head_end"], head)
        self.assertEqual(base64.b64decode(latest["files"]["source.txt"]["content_b64"]), latest_bytes)
        replay = self.replay([first, latest])
        self.assertEqual(len(replay["steps"]), 2)
        self.assertEqual(replay["steps"][-1]["context"]["status"], "READY")
        self.assertEqual(replay["steps"][-1]["prior_validation"]["status"], "INVALID")
        self.assertIs(replay["history_complete"], False)

    def test_path_profile_rejects_escape_and_comparison_rejects_scope_mismatch(self):
        for invalid in (".", "../outside.txt", "/etc/passwd", ".git/config", "a/../source.txt", "bad\0name"):
            with self.subTest(path=invalid), self.assertRaises(ValueError):
                self.capture([invalid])
        first = self.capture()
        other_scope = observer.capture(self.repo, ["source.txt"], "different-explicit-scope")
        other_profile = self.capture(["unrelated.txt"])
        for incompatible in (other_scope, other_profile):
            with self.assertRaises(ValueError):
                observer.compare_captures(first, incompatible)

    @unittest.skipUnless(hasattr(os, "symlink"), "requires symlink support")
    def test_committed_symlink_is_unsupported_and_never_dereferenced(self):
        secret = b"External target must not be read.\n"
        outside = self.root / "outside.txt"
        outside.write_bytes(secret)
        os.symlink(outside, self.repo / "linked.txt")
        self.commit("Selected symlink", "linked.txt")
        receipt = self.capture(["linked.txt"])
        self.assertEqual(receipt["files"]["linked.txt"]["state"], "UNSUPPORTED")
        self.assertNotIn(base64.b64encode(secret).decode(), json.dumps(receipt))
        self.assertEqual(self.replay([receipt], ["linked.txt"])["steps"][0]["context"]["status"], "NOT_READY")

    def test_cli_successor_preserves_previous_ledger_and_replays_in_fresh_process(self):
        first_path = self.root / "first-ledger.json"
        second_path = self.root / "second-ledger.json"
        base = [sys.executable, "-B", str(Path(observer.__file__).resolve())]
        arguments = ["observe", "--repo", str(self.repo), "--scope", self.scope, "--path", "source.txt"]
        subprocess.run(base + arguments + ["--output", str(first_path)], check=True, capture_output=True)
        original_bytes = first_path.read_bytes()
        self.write("source.txt", b"Second process observes a newer revision.\n")
        self.commit("Update between observer processes", "source.txt")
        subprocess.run(base + arguments + ["--previous", str(first_path), "--output", str(second_path)], check=True, capture_output=True)
        self.assertEqual(first_path.read_bytes(), original_bytes)
        original = json.loads(original_bytes)
        successor_bytes = second_path.read_bytes()
        successor = json.loads(successor_bytes)
        self.assertEqual(successor["entries"][:len(original["entries"])], original["entries"])
        self.assertEqual(len(successor["entries"]), len(original["entries"]) + 1)
        self.assertEqual(successor["count"], len(successor["entries"]))
        refused = subprocess.run(base + arguments + ["--output", str(second_path)], capture_output=True)
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual(second_path.read_bytes(), successor_bytes)
        replay = subprocess.run(base + ["replay", "--input", str(second_path), "--path", "source.txt"], check=True, capture_output=True)
        result = json.loads(replay.stdout)
        self.assertEqual(result["steps"][-1]["context"]["status"], "READY")
        self.assertEqual(result["steps"][-1]["prior_validation"]["status"], "INVALID")


if __name__ == "__main__":
    unittest.main()
