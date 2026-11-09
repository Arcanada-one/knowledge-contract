#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Mutation tests for concrete publication-gate failures; no network access."""
import json
from hashlib import sha256
from pathlib import Path
import shutil
import tempfile
import unittest
from tools.check_publication import check, PublicationCheck, EXPECTED_COUNTS, KINDS


class PublicationMutations(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.documents = []
        for kind, count in EXPECTED_COUNTS.items():
            directory, filename, artifact = KINDS[kind]
            for i in range(count):
                slug = f"{kind}-{i}"
                title = f"{kind.title()} {i}"
                path = f"{directory}/{slug}/{filename}"
                self.documents.append({"type": kind, "slug": slug, "path": path, "title": title, "language": "en", "edition": "1.0"})
                target = self.root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f'---\nname: {slug}\ntitle: "{title}"\nartifact: {artifact}\nedition: "1.0"\nauthor: Test author\nlanguage: en\nlicense: CC-BY-4.0\ndescription: A test document.\n---\n\n# {title}\n\n## Scope\n\nFinite fixture content with $x^2$.\n', encoding="utf-8")
        self.catalog = {"schema_version": 1, "edition": "1.0", "documents": self.documents}
        self.write_catalog()
        studies, claims = [], []
        for doc in [d for d in self.documents if d["type"] == "study"]:
            slug = doc["slug"]
            directory = self.root / "engineering/studies" / slug / "evidence"
            directory.mkdir()
            (directory / "observation.json").write_text('{"result": true}')
            raw = (directory / "observation.json").read_bytes()
            (directory / "origin.json").write_text(json.dumps({"schema": "knowledge-contract.study-evidence-origin/1", "study": slug, "files": [{"file": "observation.json", "representation": "test_fixture", "published_sha256": sha256(raw).hexdigest(), "size_bytes": len(raw)}]}))
            studies.append({"name": slug, "report": slug + "/STUDY.md", "origin": slug + "/evidence/origin.json"})
            claims.append({"claim_id": slug + "-claim", "study": slug + "/STUDY.md", "statement": "A finite fixture statement.", "claim_kind": "recorded_observation", "model": "Fixture", "test_or_argument": "Fixture inspection", "evidence": [{"path": slug + "/evidence/observation.json", "json_pointer": "/result"}], "counterexample_or_rival": "An alternative interpretation", "result": True, "limits": ["Fixture only"], "scientific_context": ["../../papers/paper-0/PAPER.md"], "public_reproduction": "Fixture inspection"})
        self.index = {"schema": "knowledge-contract.claim-evidence-index/1", "edition": "1.0", "claim_count": len(claims), "studies": studies, "claims": claims}
        self.write_index()
        self.paper = self.root / "papers/paper-0/PAPER.md"

    def tearDown(self):
        self.temp.cleanup()

    def write_catalog(self):
        (self.root / "publication-catalog.json").write_text(json.dumps(self.catalog))

    def write_index(self):
        (self.root / "engineering/studies/evidence-index.json").write_text(json.dumps(self.index))

    def assert_rejected(self, fragment):
        errors = check(self.root)
        self.assertTrue(any(fragment in error for error in errors), '\n'.join(errors))

    def test_valid_connected_publication(self):
        with self.paper.open("a") as out:
            out.write('\n[Other scope](../paper-1/PAPER.md#scope).\n')
        self.assertEqual(check(self.root), [])

    def test_broken_link(self):
        with self.paper.open("a") as out:
            out.write('\n[Missing](missing.md).\n')
        self.assert_rejected("broken link")

    def test_broken_anchor(self):
        with self.paper.open("a") as out:
            out.write('\n[Missing scope](../paper-1/PAPER.md#absent).\n')
        self.assert_rejected("broken anchor")

    def test_path_escape(self):
        with self.paper.open("a") as out:
            out.write('\n[Outside](../../../outside.md).\n')
        self.assert_rejected("path escape")

    def test_duplicate_catalog_entry(self):
        self.catalog["documents"].append(dict(self.catalog["documents"][0]))
        self.write_catalog()
        self.assert_rejected("duplicate catalog path or slug")

    def test_new_tenth_paper_count_is_required(self):
        self.documents[:] = [doc for doc in self.documents if not (doc["type"] == "paper" and doc["slug"] == "paper-9")]
        self.write_catalog()
        self.assert_rejected("document counts differ")

    def test_extra_eleventh_paper_is_refused(self):
        extra = dict(next(doc for doc in self.documents if doc["type"] == "paper"))
        extra["slug"] = "paper-extra"
        extra["path"] = "papers/paper-extra/PAPER.md"
        extra["title"] = "Paper extra"
        self.documents.append(extra)
        self.write_catalog()
        self.assert_rejected("document counts differ")

    def test_opaque_numbered_names_cannot_enter_the_current_catalog(self):
        for slug in ("r1", "r10", "p09", "123"):
            with self.subTest(slug=slug):
                self.documents[0]["slug"] = slug
                self.write_catalog()
                checker = PublicationCheck(self.root)
                checker.check_catalog()
                self.assertTrue(any("opaque numbered canonical slug" in e for e in checker.errors), checker.errors)

    def test_opaque_numbered_title_is_rejected(self):
        self.documents[0]["title"] = "R10"
        self.write_catalog()
        self.assert_rejected("opaque numbered canonical title")

    def test_new_edition_requires_consistent_document_and_evidence_versions(self):
        self.catalog["edition"] = "1.1"
        self.write_catalog()
        self.assert_rejected("frontmatter edition differs")
        for doc in self.documents:
            path = self.root / doc["path"]
            path.write_text(path.read_text().replace('edition: "1.0"', 'edition: "1.1"'))
            doc["edition"] = "1.1"
        self.write_catalog()
        self.assert_rejected("unsupported evidence-index schema or edition")
        self.index["edition"] = "1.1"
        self.write_index()
        self.assertEqual(check(self.root), [])

    def test_per_document_catalog_edition_cannot_lag_the_publication(self):
        self.documents[0]["edition"] = "0.9"
        self.write_catalog()
        self.assert_rejected("document edition differs from catalogue")

    def test_malformed_or_unfinished_edition_is_rejected(self):
        for edition in ("1.1-draft.1", "01.1", "1", 1.1, None):
            with self.subTest(edition=edition):
                self.catalog["edition"] = edition
                self.write_catalog()
                checker = PublicationCheck(self.root)
                self.assertIsNone(checker.check_catalog())
                self.assertTrue(any("numeric publication edition" in e for e in checker.errors), checker.errors)

    def test_wrong_main_filename(self):
        self.documents[0]["path"] = "papers/paper-0/SKILL.md"
        shutil.copyfile(self.paper, self.root / self.documents[0]["path"])
        self.write_catalog()
        self.assert_rejected("wrong file type/path")

    def test_missing_metadata(self):
        self.paper.write_text(self.paper.read_text().replace("description: A test document.\n", ""))
        self.assert_rejected("missing frontmatter metadata: description")

    def test_broken_evidence_pointer(self):
        self.index["claims"][0]["evidence"][0]["json_pointer"] = "/nonexistent"
        self.write_index()
        self.assert_rejected("broken JSON pointer")

    def test_changed_evidence_cannot_keep_its_old_provenance(self):
        path = self.root / "engineering/studies/study-0/evidence/observation.json"
        path.write_text('{"result": null}')
        self.assert_rejected("evidence hash mismatch")

    def test_unlisted_evidence_cannot_bypass_origin_inventory(self):
        path = self.root / "engineering/studies/study-0/evidence/unlisted.json"
        path.write_text('{"result": true}')
        self.assert_rejected("origin must cover every evidence file")


if __name__ == "__main__":
    unittest.main()
