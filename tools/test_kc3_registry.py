import copy
import json
import unittest

import check_kc3_registry as k

RAW = k.REGISTRY.read_bytes()
REG = json.loads(RAW)
SHA = k.sha256_bytes(RAW)


def mutated(fn):
    reg = copy.deepcopy(REG)
    fn(reg)
    return k.check_registry(reg)


def first(reg, cid):
    return next(c for c in reg["checks"] if c["id"] == cid)


REGISTRY_MUTATIONS = {
    "invariant_check_marked_as_testing_the_claim": (lambda r: first(r, "KC3-P04-C2").update(evidence_kind="tests_the_claim", claim_origin="registrant_hypothesis", claim_basis_in_paper="authors-domain-assessment"), "cannot cite the paper's own assessment"),
    "registrant_hypothesis_citing_the_paper": (lambda r: first(r, "KC3-P11-C1").update(claim_basis_in_paper="finite-test"), "must say that the paper does not state it"),
    "composite_part_without_n_min": (lambda r: first(r, "KC3-P04-C1")["parts"]["definition"].pop("n_min"), "own n_min"),
    "paper_without_check_or_reason": (lambda r: r["no_testable_claim"].pop(0), "neither a check nor"),
    "paper_with_check_and_reason": (lambda r: r["no_testable_claim"].append({"paper": "P01", "reason": "x" * 50}), "has a check and also"),
    "duplicate_id": (lambda r: r["checks"].append(copy.deepcopy(r["checks"][0])), "duplicate check id"),
    "unknown_gate": (lambda r: first(r, "KC3-P01-C1")["gates"].append("G-NOPE"), "unknown gate"),
    "unknown_data": (lambda r: first(r, "KC3-P01-C1")["data"].append("D-NOPE"), "unknown data set"),
    "unknown_rule": (lambda r: first(r, "KC3-P01-C1").__setitem__("decision_rule", "vibes"), "unknown decision rule"),
    "missing_direction": (lambda r: first(r, "KC3-P01-C1").pop("direction"), "needs a direction"),
    "missing_threshold": (lambda r: first(r, "KC3-P01-C1").pop("threshold"), "needs a threshold"),
    "missing_advantage_sign": (lambda r: first(r, "KC3-P13-C1").pop("advantage_sign"), "advantage_sign"),
    "wilson_n_min_one": (lambda r: first(r, "KC3-P01-C1").__setitem__("n_min", 1), "at least 20"),
    "wilson_prediction_unreachable": (lambda r: first(r, "KC3-P02-C1").__setitem__("threshold", 0.9999), "prediction cannot be met"),
    "wilson_refutation_unreachable": (lambda r: first(r, "KC3-P01-C1").__setitem__("n_min", 100), "refutation cannot be reached"),
    "sampled_without_sample_gate": (lambda r: first(r, "KC3-P01-C1")["gates"].remove("G-SAMPLE"), "G-SAMPLE"),
    "cap_gate_on_unpaid": (lambda r: first(r, "KC3-P01-C1")["gates"].append("G-CAP"), "unpaid"),
    "tautological_refutation": (lambda r: first(r, "KC3-P01-C1").__setitem__("refutation", "Nothing can refute this claim whatever the data show."), "tautology"),
    "short_prediction": (lambda r: first(r, "KC3-P01-C1").__setitem__("prediction", "It holds."), "too short"),
    "missing_origin": (lambda r: first(r, "KC3-P01-C1").pop("claim_origin"), "claim_origin"),
    "descriptive_test": (lambda r: first(r, "KC3-P01-C1").__setitem__("decision_rule", "descriptive"), "may not be a test"),
    "no_validity_gate": (lambda r: first(r, "KC3-P01-C1")["gates"].remove("G-VALID"), "G-VALID"),
    "paid_without_cap_gate": (lambda r: first(r, "KC3-P11-C2")["gates"].remove("G-CAP"), "G-CAP"),
    "paid_flag_contradicts_cap": (lambda r: first(r, "KC3-P11-C2").__setitem__("spend_cap", "not_applicable"), "contradicts paid_model_run"),
    "same_prediction_and_refutation": (lambda r: first(r, "KC3-P01-C1").__setitem__("refutation", first(r, "KC3-P01-C1")["prediction"]), "same text"),
    "questions_without_reference_gate": (lambda r: first(r, "KC3-P04-C2")["gates"].remove("G-REF"), "G-REF"),
    "packages_without_package_gate": (lambda r: first(r, "KC3-P01-C1")["gates"].remove("G-PKG"), "G-PKG"),
    "id_paper_mismatch": (lambda r: first(r, "KC3-P01-C1").__setitem__("paper", "P02"), "does not match paper"),
    "composite_with_one_part": (lambda r: first(r, "KC3-P04-C1")["parts"].pop("definition"), "at least two parts"),
    "exact_without_n_min": (lambda r: first(r, "KC3-P00-C2").pop("n_min"), "needs n_min"),
    "run_status_set": (lambda r: first(r, "KC3-P01-C1").__setitem__("status", "supported"), "'unrun' was expected"),
    "outcome_smuggled_in": (lambda r: first(r, "KC3-P01-C1").__setitem__("outcome", "supported"), "Additional properties"),
}


def receipt(check_id="KC3-P12-C1", **over):
    known = {c["id"] for c in REG["checks"]}
    check = next(c for c in REG["checks"] if c["id"] == (check_id if check_id in known else "KC3-P12-C1"))
    rec = {"schema": "KC3CheckReceipt/v1", "receipt_id": "rcpt-test-0001", "check_id": check_id, "prereg": {"sha256": SHA, "commit": "a" * 40},
           "data_digests": {"D-PKG": "b" * 64}, "run": {"started_at": "2026-11-05T00:00:00Z", "finished_at": "2026-11-05T01:00:00Z", "harness_commit": "c" * 40, "seed": 7},
           "controls": {"positive_passed": True, "negative_failed": True}, "gates_met": {g: True for g in check["gates"]}, "n": check.get("n_min", 1),
           "result": {"violations": 0}, "outcome": "supported", "limits": ["fixture receipt used only by the unit tests"],
           "reviewer_independence_class": "not_applicable", "spend": {"paid_calls": False}, "qualifications": []}
    rec.update(over)
    return rec


def PAID(**over):
    spend = {"paid_calls": True, "cap_usd": 1.0, "used_usd": 0.5, "cap_recorded_at": "2026-11-04T00:00:00Z", "provider": "deepseek", "model": "deepseek-chat",
             "tokens_in": 1000, "tokens_out": 200, "decision_id": "DEC-AUP-0174"}
    spend.update(over)
    return spend


RECEIPT_MUTATIONS = {
    "cap_above_per_run": (dict(spend=PAID(cap_usd=2.0, used_usd=0.5), check_id="KC3-P11-C2"), "above the per-run cap"),
    "paid_without_decision_id": (dict(spend={k: v for k, v in PAID().items() if k != "decision_id"}, check_id="KC3-P11-C2"), "'decision_id' is a required property"),
    "wrong_digest": (dict(prereg={"sha256": "0" * 64, "commit": "a" * 40}), "not the registered file"),
    "unknown_check": (dict(check_id="KC3-P12-C9"), "unknown check"),
    "control_failed_but_supported": (dict(controls={"positive_passed": False, "negative_failed": True}), "both controls"),
    "negative_control_passed": (dict(controls={"positive_passed": True, "negative_failed": False}), "both controls"),
    "gate_unmet": (None, "gate"),
    "n_below_minimum": (dict(n=3), "below the registered n_min"),
    "refuted_without_proposal": (dict(outcome="refuted"), "'revision_proposal_ref' is a required property"),
    "not_measured_without_reason": (dict(outcome="not_measured"), "'reason' is a required property"),
    "finish_before_start": (dict(run={"started_at": "2026-11-05T02:00:00Z", "finished_at": "2026-11-05T01:00:00Z", "harness_commit": "c" * 40, "seed": 7}), "before it starts"),
    "paid_calls_in_unpaid_check": (dict(spend=PAID(cap_usd=1.0, used_usd=0.2, cap_recorded_at="2026-11-04T00:00:00Z")), "registered as unpaid"),
    "extra_field": (dict(confidence=0.99), "Additional properties"),
    "cap_recorded_after_start": (dict(spend=PAID(cap_recorded_at="2026-11-05T00:30:00Z"), check_id="KC3-P11-C2"), "after the run started"),
    "proposal_file_missing": (dict(outcome="refuted", revision_proposal_ref="receipts/theory-checks/nope.json"), "does not resolve"),
    "weakened_without_proposal": (dict(claim_weakened=True, weakening_reason="supported only on a subset of formats"), "revision_proposal_ref"),
    "cap_gate_without_paid_calls": (None, "G-CAP is reported met"),
    "weakened_on_not_measured": (dict(outcome="not_measured", reason="control_failed", claim_weakened=True, weakening_reason="x" * 12, qualifications=["a failed control"], revision_proposal_ref="receipts/theory-checks/p.json"), "only meaningful on a supported outcome"),
    "qualifications_without_weakened_flag": (dict(qualifications=["a sub-control failed on one format"]), "must set claim_weakened"),
    "zero_registry_commit": (dict(prereg={"sha256": SHA, "commit": "0" * 40}), "does not match"),
    "foreign_decision_id": (dict(spend=PAID(decision_id="DEC-AUP-0001"), check_id="KC3-P11-C2"), "DEC-AUP-0174"),
}


class RegistryTests(unittest.TestCase):
    def test_registered_file_passes(self):
        self.assertEqual(k.check_registry(REG), [])

    def test_every_paper_is_covered_exactly_once(self):
        covered = {c["paper"] for c in REG["checks"]} | {n["paper"] for n in REG["no_testable_claim"]}
        self.assertEqual(covered, set(k.PAPERS))

    def test_every_registry_mutation_is_reported(self):
        for name, (fn, fragment) in REGISTRY_MUTATIONS.items():
            problems = mutated(fn)
            self.assertTrue(any(fragment in p for p in problems), f"{name}: {fragment!r} not in {problems}")

    def test_all_checks_are_unrun_and_every_stored_receipt_is_honest(self):
        for c in REG["checks"]:
            self.assertEqual(c["status"], "unrun")  # status lives in receipts, never in the registry
        for path in sorted((k.REPO / "receipts" / "theory-checks").glob("*.json")):
            rec = json.loads(path.read_text())
            if rec.get("schema") == "KC3CheckReceipt/v1":
                self.assertEqual(k.check_receipt(rec, REG, RAW), [], path.name)

    def test_every_check_names_a_positive_and_a_negative_control(self):
        for c in REG["checks"]:
            self.assertGreater(len(c["controls"]["positive"]), 9, c["id"])
            self.assertGreater(len(c["controls"]["negative"]), 9, c["id"])

    def test_checks_that_call_a_paid_model_say_so(self):
        self.assertEqual({c["id"] for c in REG["checks"] if c["paid_model_run"]}, {"KC3-P11-C2", "KC3-P13-C1"})

    def test_wilson_reachability_numbers(self):
        self.assertAlmostEqual(k.wilson(100, 100)[0], 0.963, places=3)
        self.assertGreaterEqual(k.wilson(200, 200)[0], 0.98)

    def test_known_regression_checks_are_marked_as_such(self):
        reg = {c["id"]: c for c in REG["checks"]}
        for cid in ("KC3-P04-C2", "KC3-P07-C1", "KC3-P07-C2", "KC3-P10-C1", "KC3-P11-C1", "KC3-P10-C2"):
            self.assertEqual(reg[cid]["evidence_kind"], "regression_of_our_implementation", cid)
        for cid in ("KC3-P11-C1", "KC3-P10-C2", "KC3-P13-C1", "KC3-P04-C1"):
            self.assertEqual(reg[cid]["claim_origin"], "registrant_hypothesis", cid)

    def test_registry_is_pinned(self):
        self.assertEqual(k.check_pin(RAW), [])
        self.assertTrue(k.check_pin(RAW + b" "))


class ReceiptTests(unittest.TestCase):
    def test_honest_receipt_passes(self):
        self.assertEqual(k.check_receipt(receipt(), REG, RAW), [])

    def test_receipt_mutations_are_reported(self):
        for name, (over, fragment) in RECEIPT_MUTATIONS.items():
            if name == "gate_unmet":
                rec = receipt()
                rec["gates_met"]["G-PKG"] = False
            elif name == "cap_gate_without_paid_calls":
                rec = receipt()
                rec["gates_met"]["G-CAP"] = True
            else:
                rec = receipt(**over)
            problems = k.check_receipt(rec, REG, RAW)
            self.assertTrue(any(fragment in p for p in problems), f"{name}: {fragment!r} not in {problems}")

    def test_not_measured_is_allowed_with_failed_controls(self):
        rec = receipt(outcome="not_measured", reason="control_failed", controls={"positive_passed": False, "negative_failed": True})
        self.assertEqual(k.check_receipt(rec, REG, RAW), [])

    def test_paid_receipt_within_cap_passes(self):
        self.assertEqual(k.check_receipt(receipt("KC3-P11-C2", spend=PAID()), REG, RAW), [])

    def test_paid_check_needs_cap_before_calls(self):
        rec = receipt("KC3-P11-C2", spend={"paid_calls": True, "used_usd": 1.0})
        self.assertTrue(k.check_receipt(rec, REG, RAW))
        rec = receipt("KC3-P11-C2", spend=PAID(cap_usd=1.0, used_usd=3.0))
        self.assertTrue(any("exceeds the recorded cap" in p for p in k.check_receipt(rec, REG, RAW)))

    def test_registry_commit_must_be_an_ancestor_when_ancestry_is_known(self):
        self.assertEqual(k.check_receipt(receipt(), REG, RAW, ancestry=lambda c: True), [])
        self.assertTrue(any("not an ancestor" in p for p in k.check_receipt(receipt(), REG, RAW, ancestry=lambda c: False)))

    def test_digest_changes_when_the_registry_changes(self):
        altered = RAW.replace(b"unrun", b"unrun ", 1)
        self.assertNotEqual(k.sha256_bytes(altered), SHA)
        self.assertTrue(any("not the registered file" in p for p in k.check_receipt(receipt(), REG, altered)))


class ProposalLinkTests(unittest.TestCase):
    def reader(self, **over):
        prop = {"schema": "KC3RevisionProposal/v1", "proposal_id": "prop-0001", "paper": "P12", "check_id": "KC3-P12-C1", "receipt_ref": "receipts/theory-checks/r.json",
                "finding": "refuted", "claim_affected": "If the dependency set contains every input, reuse preserves checked properties.",
                "proposed_change": "State the measured counterexample as a limit of the conditional lemma.", "paper_sha256_at_proposal": "d" * 64,
                "status": "proposed", "route": "P10 revision and canon"}
        prop.update(over)
        return lambda ref: prop

    def call(self, rec, reader, **kw):
        return k.check_receipt(rec, REG, RAW, read_ref=reader, paper_sha=lambda paper: "d" * 64, **kw)

    def test_proposal_linked_and_consistent(self):
        rec = receipt(outcome="refuted", revision_proposal_ref="receipts/theory-checks/p.json")
        self.assertEqual(self.call(rec, self.reader(), receipt_path="receipts/theory-checks/r.json"), [])

    def test_proposal_must_name_this_receipt_and_the_real_paper_digest(self):
        rec = receipt(outcome="refuted", revision_proposal_ref="receipts/theory-checks/p.json")
        out = self.call(rec, self.reader(receipt_ref="receipts/theory-checks/other.json"), receipt_path="receipts/theory-checks/r.json")
        self.assertTrue(any("does not name this receipt" in p for p in out), out)
        out = self.call(rec, self.reader(paper_sha256_at_proposal="e" * 64))
        self.assertTrue(any("paper digest" in p for p in out), out)

    def test_real_paper_digest_function_reads_the_entry_page(self):
        self.assertEqual(k.paper_digest("P12"), k.sha256_bytes(next((k.REPO / "papers").glob("P12_*.md")).read_bytes()))
        self.assertIsNone(k.paper_digest("P99"))

    def test_proposal_for_another_check_or_paper_is_refused(self):
        rec = receipt(outcome="refuted", revision_proposal_ref="receipts/theory-checks/p.json")
        for over in ({"check_id": "KC3-P12-C2"}, {"paper": "P01"}):
            self.assertTrue(any("another check or paper" in p for p in self.call(rec, self.reader(**over))), over)

    def test_finding_must_match_receipt(self):
        rec = receipt(outcome="refuted", revision_proposal_ref="receipts/theory-checks/p.json")
        self.assertTrue(any("claim_weakened" in p for p in self.call(rec, self.reader(finding="weakened"))))
        rec = receipt(outcome="supported", claim_weakened=True, weakening_reason="supported only on text formats", qualifications=["holds only on text-native formats"], revision_proposal_ref="receipts/theory-checks/p.json")
        self.assertEqual(self.call(rec, self.reader(finding="weakened")), [])
        self.assertTrue(any("finding refuted" in p for p in self.call(rec, self.reader(finding="refuted"))))


class ProposalTests(unittest.TestCase):
    def proposal(self, **over):
        p = {"schema": "KC3RevisionProposal/v1", "proposal_id": "prop-0001", "paper": "P01", "check_id": "KC3-P01-C1", "receipt_ref": "receipts/theory-checks/rcpt-test-0001.json",
             "finding": "refuted", "claim_affected": "A structural validator checks pinned references, not whether an image was read.", "proposed_change": "Restate the limit with the measured support rate and its interval.",
             "paper_sha256_at_proposal": "d" * 64, "status": "proposed", "route": "P10 revision and canon"}
        p.update(over)
        return p

    def test_proposal_is_valid_and_is_not_an_edit(self):
        self.assertEqual(k._errors(k._validator(k.RECEIPT_SCHEMA, "Proposal"), self.proposal()), [])
        for over in ({"status": "applied"}, {"route": "direct edit"}, {"finding": "supported"}, {"paper": "P14"}, {"paper_sha256_at_proposal": "xyz"}):
            self.assertTrue(k._errors(k._validator(k.RECEIPT_SCHEMA, "Proposal"), self.proposal(**over)), over)


if __name__ == "__main__":
    unittest.main()
