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
from tools.check_publication import check, EXPECTED_COUNTS, KINDS


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
                self.documents.append({"type": kind, "slug": slug, "path": path, "title": title, "language": "en"})
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
