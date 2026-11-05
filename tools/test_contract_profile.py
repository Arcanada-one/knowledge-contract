# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Interoperability subset and serialized-publication counterexamples; all inputs synthetic."""
import copy
import json
import threading
import unittest
from pathlib import Path

import check_contract_profile as cp

FIXTURES = Path(__file__).resolve().parents[1] / "schemas/fixtures/contract-observation/valid"


def fixture(name):
    return json.loads((FIXTURES / (name + ".json")).read_text())


class ExchangeTests(unittest.TestCase):
    def test_all_three_record_families_validate(self):
        families = set()
        for path in FIXTURES.glob("*.json"):
            data = path.read_bytes()
            record = cp.decode_record(data)
            families.add(record["schema"])
            self.assertEqual(cp.check_record(record), [], path.name)
            self.assertEqual(len(cp.record_digest(data)), 64)
        self.assertEqual(families, set(cp.DISPATCH))

    def test_record_hash_is_exact_bytes_not_implicit_canonical_value(self):
        record = fixture("observation-pass")
        first = json.dumps(record, separators=(",", ":")).encode()
        second = json.dumps(record, indent=2).encode()
        self.assertEqual(cp.decode_record(first), cp.decode_record(second))
        self.assertNotEqual(cp.record_digest(first), cp.record_digest(second))

    def test_duplicate_members_nonfinite_bom_and_isolated_surrogates_are_rejected(self):
        for data in (b'{"x":1,"x":2}', b'{"x":{"v":1,"v":2}}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":1e999}',
                     b'\xef\xbb\xbf{}', b'{"x":"\\ud800"}', b'[]', b'\xff'):
            with self.subTest(data=data), self.assertRaises(cp.ProfileError):
                cp.decode_record(data)

    def test_missing_binding_wrong_vocabulary_or_unknown_extension_is_rejected(self):
        for field in ("subject", "criterion", "method", "observer", "observed_at", "scope", "trust_assumptions", "limitations"):
            rec = fixture("observation-pass")
            del rec[field]
            self.assertTrue(cp.check_record(rec), field)
        for change in ({"result": "ready"}, {"result": "success"}, {"schema": "KCObservation/v9"}, {"extra": "extension not negotiated"}):
            rec = fixture("observation-pass")
            rec.update(change)
            self.assertTrue(cp.check_record(rec), change)

    def test_not_applicable_requires_a_pinned_inapplicability_rule(self):
        rec = fixture("observation-pass")
        rec["result"] = "not_applicable"
        self.assertTrue(cp.check_record(rec))
        rec["inapplicability_rule"] = copy.deepcopy(rec["criterion"])
        self.assertEqual(cp.check_record(rec), [])

    def test_invalid_dates_do_not_pass_a_shape_only_check(self):
        rec = fixture("observation-pass")
        rec["observed_at"] = "2026-02-31T25:00:00Z"
        self.assertTrue(cp.check_record(rec))

    def test_change_event_monotonicity_and_revocation(self):
        for epoch in (7, 6, -1, 9007199254740992):
            rec = fixture("change-revocation")
            rec["new_epoch"] = epoch
            self.assertTrue(cp.check_record(rec), epoch)
        rec = fixture("change-revocation")
        rec["impact"] = "compatible"
        self.assertTrue(cp.check_record(rec))

    def test_advertisement_is_explicit_and_rejects_unknown_profiles(self):
        rec = fixture("profile-advertisement")
        rec["read_profiles"].append("implicit-everything")
        self.assertTrue(cp.check_record(rec))


class PublicationRaceTests(unittest.TestCase):
    def model(self):
        return cp.PublicationGuardModel("test.head", {"source": 3, "authority": 5, "policy": 8})

    def test_late_worker_cannot_overwrite_newer_head(self):
        m = self.model()
        first, second = m.read(), m.read()
        self.assertTrue(m.publish(second, "new-output"))
        self.assertFalse(m.publish(first, "late-output"))
        self.assertEqual(m.head, "new-output")

    def test_revocation_between_read_and_publish_blocks_old_and_new_worker(self):
        m = self.model()
        read = m.read()
        m.change("authority", revoked=True)
        self.assertFalse(m.publish(read, "unauthorized-output"))
        self.assertFalse(m.publish(m.read(), "still-unauthorized"))
        self.assertIsNone(m.head)

    def test_dependency_epoch_comparison_is_part_of_same_decision(self):
        m = self.model()
        read = m.read()
        m.change("source")
        read["generation"] = m.generation  # even a current head counter cannot hide an old dependency observation
        self.assertFalse(m.publish(read, "old-source-output"))

    def test_omitted_authority_dependency_and_wrong_namespace_are_rejected(self):
        m = self.model()
        read = m.read()
        del read["dependencies"]["authority"]
        self.assertFalse(m.publish(read, "unscoped-output"))
        read = m.read()
        read["namespace"] = "different.head"
        self.assertFalse(m.publish(read, "wrong-head"))

    def test_rollback_uses_new_generation_and_cannot_create_aba(self):
        m = self.model()
        self.assertTrue(m.publish(m.read(), "older-content"))
        stale = m.read()
        self.assertTrue(m.publish(m.read(), "newer-content"))
        self.assertTrue(m.publish(m.read(), "older-content"))
        self.assertEqual(m.head, "older-content")
        self.assertFalse(m.publish(stale, "late-output"))
        self.assertEqual(m.generation, 3)

    def test_concurrent_publishers_have_exactly_one_winner(self):
        m = self.model()
        read = m.read()
        start = threading.Barrier(3)
        results = []
        def worker(value):
            start.wait()
            results.append(m.publish(read, value))
        threads = [threading.Thread(target=worker, args=(value,)) for value in ("a", "b")]
        for t in threads:
            t.start()
        start.wait()
        for t in threads:
            t.join()
        self.assertEqual(sorted(results), [False, True])
        self.assertEqual(m.generation, 1)

    def test_counter_never_wraps(self):
        m = cp.PublicationGuardModel("test.head", {"authority": 1}, cp.MAX_EPOCH)
        self.assertFalse(m.publish(m.read(), "output"))
        with self.assertRaises(cp.ProfileError):
            m.change("authority", revoked=True)

    def test_exhausted_dependency_blocks_publication_after_failed_revocation(self):
        m = cp.PublicationGuardModel("test.head", {"authority": cp.MAX_EPOCH}, 0)
        old_read = m.read()
        with self.assertRaises(cp.ProfileError):
            m.change("authority", revoked=True)
        self.assertFalse(m.publish(old_read, "late-output"))
        self.assertFalse(m.publish(m.read(), "fresh-output"))
        self.assertIsNone(m.head)
        self.assertEqual(m.generation, 0)

        last_change = cp.PublicationGuardModel("test.head", {"source": cp.MAX_EPOCH - 1}, 0)
        last_change.change("source")
        self.assertFalse(last_change.publish(last_change.read(), "output"))
        self.assertIsNone(last_change.head)


if __name__ == "__main__":
    unittest.main()
