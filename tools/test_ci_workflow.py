import ast
import re
import types
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

    def test_candidate_export_installs_a_pinned_gitleaks_with_a_verified_digest_before_the_exporter_runs(self):
        # the exporter refuses without gitleaks, so the job must install it; an unpinned or unverified download would not do
        job = self.jobs["candidate-export"]
        install = job.index("gitleaks")
        self.assertLess(install, job.index("test_export_corpus"))
        self.assertLess(install, job.index("export_corpus.py"))
        self.assertRegex(job, r"GITLEAKS_VERSION: \d+\.\d+\.\d+\n")
        self.assertRegex(job, r"GITLEAKS_SHA256: [0-9a-f]{64}\n")
        self.assertIn("sha256sum -c", job)
        self.assertIn("releases/download/v${GITLEAKS_VERSION}/", job)
        self.assertNotIn("releases/latest", job)
        self.assertIn("/gitleaks\" version", job)

    def test_every_job_that_runs_the_exporter_checks_out_full_history(self):
        # the exporter refuses a shallow clone
        runners = [name for name, block in self.jobs.items() if "export_corpus" in block or "test_export" in block]
        self.assertIn("candidate-export", runners)
        for name in runners:
            self.assertIn("fetch-depth: 0", self.jobs[name], name)

    def test_corpus_map_validator_runs_with_full_history_and_a_negative_control(self):
        job = self.jobs["corpus-map"]
        self.assertIn("fetch-depth: 0", job)
        self.assertIn("python3 -B -m unittest tools.test_verify_corpus_map -v", job)
        self.assertIn("python3 -B -m unittest tools.test_project_corpus_map -v", job)
        self.assertIn("tools/verify_corpus_map.py --repo .", job)
        self.assertIn("tools/project_corpus_map.py", job)
        self.assertIn("--expect-blob a7b2fb8cde305b8fe4145df1ee7d7179478fdd60", job)
        self.assertIn("reference/foundations/projections/corpus-map-a7b2fb8c", job)
        self.assertIn("--check", job)
        self.assertIn("REPRODUCIBILITY.json", job)
        self.assertIn("REPRODUCIBILITY_PIN_MISMATCH", job)
        self.assertIn("REPRODUCIBILITY_PIN_OK", job)
        self.assertIn("['commit'] = 'main'", job)
        self.assertIn('test "$status" -eq 1', job)
        self.assertIn("tools/build_corpus_map_v2_inventory.py --check", job)
        self.assertIn("python3 -B -m unittest tools.test_corpus_map_v2_inventory -v", job)
        self.assertIn("--map reviews/corpus-map-v2/corpus-map-v2.inventory-candidate.json --repo .", job)
        self.assertNotIn("|| true", job)
        self.assertNotIn("continue-on-error", job)

    def test_security_audit_keeps_its_filter(self):
        self.assertIn("head.repo.full_name == github.repository", self.jobs["security-audit"])

    def test_licensing_runs_cross_package_overlay_corpus(self):
        job = self.jobs["licensing"]
        self.assertIn("Cross-package overlay preparation corpus (G11)", job)
        self.assertIn("python3 -B -m unittest tools.test_cross_package_overlay -v", job)
        self.assertIn("tools/cross_package_overlay.py", job)

    def test_licensing_runs_assessed_coverage_oracle_corpus(self):
        job = self.jobs["licensing"]
        self.assertIn("Assessed-coverage finite oracle corpus (Layer S)", job)
        self.assertIn("python3 -B -m unittest tools.test_assessed_coverage_oracle -v", job)
        self.assertIn("tools/assessed_coverage_oracle.py", job)

    def test_licensing_runs_reconcile_workgraph_harness(self):
        job = self.jobs["licensing"]
        self.assertIn("RM-04 workgraph reconcile harness (synthetic dry-run)", job)
        self.assertIn("python3 -B -m unittest tools.test_reconcile_workgraph -v", job)
        self.assertIn("tools/reconcile_workgraph.py", job)

    def test_publication_integrity_runs_retrieval_context_checker_with_pins(self):
        job = self.jobs["publication-integrity"]
        self.assertIn("fetch-depth: 0", job)
        self.assertIn("python3 -B -m unittest tools.test_verify_retrieval_context -v", job)
        self.assertIn("Pin and run retrieval-context checker", job)
        self.assertIn("tools/verify_retrieval_context.py", job)
        self.assertIn("CHECKER_SHA256:", job)
        self.assertIn("PAPER_SHA256: e457fadcb17424e15083504a2babb2646aedc8aec7370048cd77854a8c7af64f", job)
        self.assertIn("sha256sum -c", job)
        self.assertIn("ACCEPTED_PAPER_BLOB: 9311c0d157d5a926e3c08f6a087a53866064f4e0", job)
        self.assertIn("--title-only-against", job)
        self.assertIn("retrieval-context-report.json", job)
        self.assertIn('test -s "$report"', job)
        self.assertNotIn("|| true", job)
        self.assertNotIn("continue-on-error", job)


C03_WORKFLOW = CI.with_name("c03-finite-controls.yml")
C03_COMMAND = "python3 -B -m unittest tools.test_c03_initial_precondition -v"


def c03_workflow_errors(text: str) -> list[str]:
    """Narrow structural guard for this deliberately simple workflow, not a YAML validator.

    Runtime success still requires the exact-head job and its test log. The guard
    runs from the existing licensing job, so deleting this workflow is not silent.
    """
    errors = []
    live = "\n".join(line for line in text.splitlines()
                     if not line.lstrip().startswith("#")) + "\n"
    if "on:\n  pull_request:\n  push:\n    branches: [main]\n" not in live:
        errors.append("missing unfiltered pull-request and main-push triggers")
    if "permissions:\n  contents: read\n" not in live or "secrets." in live:
        errors.append("expected read-only token and no secrets")
    if re.search(r"^\s*(?:if|continue-on-error|paths|paths-ignore|branches-ignore):", live, re.M):
        errors.append("conditional or failure-masking configuration")
    try:
        job = job_blocks(live)["c03-finite-controls"]
    except (IndexError, KeyError):
        return errors + ["missing C03 job"]
    expected = "        run: " + C03_COMMAND
    if expected not in job.splitlines():
        errors.append("missing direct, unmasked C03 command")
    if "persist-credentials: false" not in job:
        errors.append("checkout must not persist credentials")
    return errors


class C03WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.text = C03_WORKFLOW.read_text(encoding="utf-8")

    def test_real_workflow_runs_c03_without_skips(self):
        self.assertEqual(c03_workflow_errors(self.text), [])

    def test_omitted_command_is_refused(self):
        self.assertTrue(c03_workflow_errors(self.text.replace(C03_COMMAND, "true")))

    def test_printed_command_is_not_execution(self):
        self.assertTrue(c03_workflow_errors(self.text.replace(C03_COMMAND, "echo " + C03_COMMAND)))

    def test_commented_command_is_not_execution(self):
        self.assertTrue(c03_workflow_errors(self.text.replace("        run: " + C03_COMMAND,
                                                              "        # run: " + C03_COMMAND)))

    def test_skipped_job_is_refused(self):
        changed = self.text.replace("    runs-on:", "    if: false\n    runs-on:")
        self.assertTrue(c03_workflow_errors(changed))

    def test_masked_failure_is_refused(self):
        for changed in (self.text.replace(C03_COMMAND, C03_COMMAND + " || true"),
                        self.text.replace("    steps:", "    continue-on-error: true\n    steps:")):
            with self.subTest(changed=changed):
                self.assertTrue(c03_workflow_errors(changed))

    def test_wrong_module_is_refused(self):
        self.assertTrue(c03_workflow_errors(self.text.replace("tools.test_c03_initial_precondition",
                                                              "tools.test_reviewed_formal_results")))

    def test_missing_job_is_refused(self):
        self.assertTrue(c03_workflow_errors(self.text.replace("  c03-finite-controls:", "  other:")))


# Keep the exact-head scientific review checklist aligned with the executable
# finite controls. Definition checks and bounded unittest execution below are
# distinct; neither establishes scientific proof or independent admission.
C03_NOTE = CI.parents[2] / "reviews" / "corpus-map-v2" / "C03_INITIAL_PRECONDITION.md"
C03_TESTS = CI.parents[2] / "tools" / "test_c03_initial_precondition.py"
C03_INVENTORY = re.compile(r"^C03 review-test inventory: ([0-9]+) executable tests$", re.M)


def c03_inventory_errors(note: str, test_source: str) -> list[str]:
    declared = C03_INVENTORY.findall(note)
    if len(declared) != 1:
        return ["expected exactly one review inventory"]
    if "recalculate the six finite checks" in note:
        return ["obsolete review requirement"]
    try:
        syntax = ast.parse(test_source)
    except SyntaxError:
        return ["unparseable test module"]
    suites = [node for node in syntax.body if isinstance(node, ast.ClassDef)]
    if len({suite.name for suite in suites}) != len(suites):
        return ["duplicate class name can shadow an earlier test suite"]
    methods = []
    for suite in suites:
        selected = [node for node in suite.body
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and node.name.startswith("test_")]
        if len({method.name for method in selected}) != len(selected):
            return [f"duplicate test method in {suite.name}"]
        if any(isinstance(method, ast.AsyncFunctionDef) for method in selected):
            return ["C03 requires synchronous tests; async bodies are not admitted"]
        methods.extend(selected)
    return [] if int(declared[0]) == len(methods) else [
        f"review inventory {declared[0]} differs from {len(methods)} test definitions"
    ]


def c03_execution_errors(note: str, test_source: str) -> list[str]:
    """Check this trusted repository fixture's actual unittest selection and result.

    This executes the C03 source, just like its dedicated CI invocation; it is
    NOT a sandbox for untrusted input or a general Python verifier. The caller's
    CI permissions and timeout still apply. The original named CI job and its
    log remain separate evidence. Repeated executions are not extra science cases.
    """
    errors = c03_inventory_errors(note, test_source)
    if errors:
        return errors
    declared = int(C03_INVENTORY.findall(note)[0])
    module = types.ModuleType("_c03_execution_probe")
    try:
        exec(compile(test_source, str(C03_TESTS), "exec"), module.__dict__)
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)

        def case_ids(group):
            for item in group:
                if isinstance(item, unittest.TestSuite):
                    yield from case_ids(item)
                else:
                    yield item.id()

        actual = list(case_ids(suite))
        syntax = ast.parse(test_source)
        expected = [f"{module.__name__}.{group.name}.{method.name}"
                    for group in syntax.body if isinstance(group, ast.ClassDef)
                    for method in group.body if isinstance(method, ast.FunctionDef)
                    and method.name.startswith("test_")]
        if loader.errors:
            return ["unittest loader reported errors"]
        if len(actual) != declared or sorted(actual) != sorted(expected):
            return [f"unittest selected {len(actual)} cases; expected {declared} exact test IDs"]
        result = unittest.TestResult()
        suite.run(result)
    except Exception as exc:
        return [f"C03 loading/execution raised {type(exc).__name__}: {exc}"]
    if result.testsRun != declared:
        errors.append(f"unittest ran {result.testsRun} cases; expected {declared}")
    if result.skipped:
        errors.append(f"C03 skipped {len(result.skipped)} cases")
    if result.expectedFailures:
        errors.append(f"C03 recorded {len(result.expectedFailures)} expected failures")
    if not result.wasSuccessful():
        errors.append("C03 did not pass without errors or unexpected outcomes")
    return errors


class C03ReviewInventoryTests(unittest.TestCase):
    def setUp(self):
        self.note = C03_NOTE.read_text(encoding="utf-8")
        self.source = C03_TESTS.read_text(encoding="utf-8")

    def test_actual_review_inventory_matches_defined_tests(self):
        self.assertEqual(c03_inventory_errors(self.note, self.source), [])

    def test_stale_six_test_review_inventory_fails(self):
        mutant = self.note.replace("C03 review-test inventory: 10 executable tests",
                                   "C03 review-test inventory: 6 executable tests")
        self.assertTrue(c03_inventory_errors(mutant, self.source))

    def test_removed_test_method_fails_review_inventory(self):
        mutant = self.source.replace("def test_", "def disabled_", 1)
        self.assertNotEqual(mutant, self.source)
        self.assertTrue(c03_inventory_errors(self.note, mutant))

    def test_missing_or_duplicate_review_inventory_fails(self):
        marker = "C03 review-test inventory: 10 executable tests"
        for mutant in (self.note.replace(marker, ""), self.note + "\n" + marker + "\n"):
            with self.subTest():
                self.assertTrue(c03_inventory_errors(mutant, self.source))


    def test_actual_inventory_is_loaded_and_passes_without_skips(self):
        self.assertEqual(c03_execution_errors(self.note, self.source), [])

    def test_shadowed_method_fails_even_with_ten_definitions(self):
        mutant = self.source.replace(
            "def test_carriers_and_transitions_are_finite_and_well_typed",
            "def test_local_partial_correctness_for_all_admitted_transitions", 1)
        self.assertNotEqual(mutant, self.source)
        self.assertTrue(c03_inventory_errors(self.note, mutant))
        self.assertTrue(c03_execution_errors(self.note, mutant))

    def test_shadowed_class_fails_even_with_ten_definitions(self):
        mutant = self.source.replace("class C03TwoStepJunctionControls",
                                     "class C03InitialPreconditionTests", 1)
        self.assertNotEqual(mutant, self.source)
        self.assertTrue(c03_inventory_errors(self.note, mutant))
        self.assertTrue(c03_execution_errors(self.note, mutant))

    def test_skipped_method_or_class_is_not_a_passed_inventory(self):
        mutants = (
            self.source.replace("    def test_carriers_",
                                '    @unittest.skip("inventory control")\n    def test_carriers_', 1),
            self.source.replace("class C03TwoStepJunctionControls",
                                '@unittest.skip("inventory control")\nclass C03TwoStepJunctionControls', 1),
        )
        for mutant in mutants:
            with self.subTest(mutant=mutant[:60]):
                self.assertNotEqual(mutant, self.source)
                self.assertEqual(c03_inventory_errors(self.note, mutant), [])
                self.assertTrue(c03_execution_errors(self.note, mutant))

    def test_empty_load_tests_override_is_not_successful_coverage(self):
        mutant = self.source + ("\ndef load_tests(loader, tests, pattern):\n"
                                "    return unittest.TestSuite()\n")
        self.assertEqual(c03_inventory_errors(self.note, mutant), [])
        self.assertTrue(c03_execution_errors(self.note, mutant))

    def test_non_testcase_class_is_not_executable_inventory(self):
        mutant = self.source.replace("class C03InitialPreconditionTests(unittest.TestCase):",
                                     "class C03InitialPreconditionTests:", 1)
        self.assertNotEqual(mutant, self.source)
        self.assertEqual(c03_inventory_errors(self.note, mutant), [])
        self.assertTrue(c03_execution_errors(self.note, mutant))

    def test_unawaited_async_method_is_refused(self):
        mutant = self.source.replace("    def test_carriers_", "    async def test_carriers_", 1)
        self.assertNotEqual(mutant, self.source)
        self.assertTrue(c03_inventory_errors(self.note, mutant))
        self.assertTrue(c03_execution_errors(self.note, mutant))

    def test_expected_failure_is_not_a_passing_scientific_case(self):
        mutant = self.source.replace("    def test_carriers_",
                                     "    @unittest.expectedFailure\n    def test_carriers_", 1)
        mutant = mutant.replace("self.assertTrue(RELATION)", "self.assertFalse(RELATION)", 1)
        self.assertNotEqual(mutant, self.source)
        self.assertEqual(c03_inventory_errors(self.note, mutant), [])
        self.assertTrue(c03_execution_errors(self.note, mutant))


if __name__ == "__main__":
    unittest.main()
