import re
import unittest
from pathlib import Path

CI = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "ci.yml"
MUST_RUN_FOR_FORKS = ("licensing", "dco", "decision-separation")


def job_blocks(text: str) -> dict[str, str]:
    jobs = text.split("\njobs:\n", 1)[1]
    parts = re.split(r"^  ([A-Za-z0-9_-]+):\n", jobs, flags=re.M)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


class CiWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.text = CI.read_text(encoding="utf-8")
        self.jobs = job_blocks(self.text)

    def test_jobs_exist(self):
        for name in MUST_RUN_FOR_FORKS:
            self.assertIn(name, self.jobs)

    def test_fork_pr_jobs_have_no_repository_filter(self):
        # A skipped required check counts as passed, so these must run for fork PRs.
        for name in MUST_RUN_FOR_FORKS:
            conditions = re.findall(r"^    if: (.*)$", self.jobs[name], flags=re.M)
            for condition in conditions:
                self.assertNotIn("head.repo", condition, f"{name}: {condition}")
                self.assertNotIn("github.repository", condition, f"{name}: {condition}")

    def test_dco_runs_on_every_pull_request(self):
        self.assertIn("if: github.event_name == 'pull_request'\n", self.jobs["dco"])

    def test_fork_pr_jobs_use_no_secrets_and_read_only_token(self):
        for name in MUST_RUN_FOR_FORKS:
            self.assertNotIn("secrets.", self.jobs[name])
        self.assertIn("permissions:\n  contents: read\n", self.text)
        self.assertNotIn("pull_request_target", self.text)

    def test_decision_separation_runs_on_every_pull_request_with_full_history(self):
        job = self.jobs["decision-separation"]
        self.assertIn("if: github.event_name == 'pull_request'\n", job)
        self.assertIn("fetch-depth: 0", job)
        self.assertIn("tools/check_separation.py", job)

    def test_candidate_export_asserts_v2_with_full_history_and_no_mutation_pass(self):
        job = self.jobs["candidate-export"]
        self.assertIn("KnowledgeContractCandidateExport/v2", job)
        self.assertNotIn("CandidateExport/v1", self.text)
        self.assertIn("fetch-depth: 0", job)
        # the mutation pass is an author-side tool (run before pushing), not a pull request check
        self.assertNotIn("test_export_check_mutations", self.text)

    def test_every_job_that_runs_the_exporter_checks_out_full_history(self):
        # the exporter refuses a shallow clone
        runners = [name for name, block in self.jobs.items() if "export_corpus" in block or "test_export" in block]
        self.assertIn("candidate-export", runners)
        for name in runners:
            self.assertIn("fetch-depth: 0", self.jobs[name], name)

    def test_security_audit_keeps_its_filter(self):
        self.assertIn("head.repo.full_name == github.repository", self.jobs["security-audit"])


if __name__ == "__main__":
    unittest.main()
