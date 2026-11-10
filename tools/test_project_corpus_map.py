# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Controls for the deterministic read-only corpus-map projection."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.project_corpus_map import (
    EXPECTED_NODES,
    EXPECTED_PLANNING_REQUIRES,
    EXPECTED_RELATIONS,
    PINNED_BLOB,
    REASON_AUTHORITY_CLAIM,
    REASON_DUPLICATE_ID,
    REASON_EXPECT_BLOB_MISMATCH,
    REASON_PLANNING_REQUIRES_COUNT,
    REASON_RELATION_FAMILY_COUNT,
    REASON_STATUS_RELABEL,
    REASON_UNKNOWN_ENDPOINT,
    REASON_UNSUPPORTED_EDGE_KIND,
    dumps_deterministic,
    git_blob_sha1,
    project_bytes,
    reading_link_sccs,
    render_html,
    render_text,
    write_outputs,
)

REPO = Path(__file__).resolve().parents[1]
MAP_PATH = REPO / "reference/foundations/corpus-map.json"
BASE = json.loads(MAP_PATH.read_text(encoding="utf-8"))
RAW = MAP_PATH.read_bytes()
INPUT_PATH = MAP_PATH.as_posix()


def mutate_raw(change) -> bytes:
    data = copy.deepcopy(BASE)
    change(data)
    return dumps_deterministic(data).encode("utf-8")


class ProjectCorpusMapControls(unittest.TestCase):
    def test_pinned_blob_matches_workspace_bytes(self):
        self.assertEqual(git_blob_sha1(RAW), PINNED_BLOB)

    def test_happy_path_counts_and_layers(self):
        projection, _text, _html = project_bytes(RAW, INPUT_PATH, PINNED_BLOB)
        self.assertEqual(projection["status"], "candidate")
        self.assertEqual(
            projection["counts"],
            {
                "nodes": EXPECTED_NODES,
                "relations": EXPECTED_RELATIONS,
                "planning_requires": EXPECTED_PLANNING_REQUIRES,
            },
        )
        self.assertEqual(len(projection["nodes"]), 65)
        self.assertEqual(len(projection["layers"]["relations"]), 99)
        self.assertEqual(len(projection["layers"]["planning_requires"]), 45)
        # Layers stay separate: never presented as one 144-edge family.
        self.assertNotIn("all_edges", projection)
        self.assertNotIn("edges", projection)
        merged = projection["layers"]["relations"] + projection["layers"]["planning_requires"]
        self.assertEqual(len(merged), 144)
        self.assertEqual(projection["counts"]["relations"] + projection["counts"]["planning_requires"], 144)
        self.assertNotEqual(projection["counts"]["relations"], 144)
        # No derived permission / ready / accepted flags on the projection root.
        self.assertEqual(projection["status"], "candidate")
        self.assertEqual(projection["input"]["map_status"], "proposed-reference-view")
        self.assertNotIn("runtime_permission", projection)
        self.assertNotIn("ready", projection)
        self.assertNotIn("accepted", projection)
        self.assertNotIn("permission", projection)

    def test_determinism_two_runs_byte_identical(self):
        a_json, a_text, a_html = project_bytes(RAW, INPUT_PATH, PINNED_BLOB)
        b_json, b_text, b_html = project_bytes(RAW, INPUT_PATH, PINNED_BLOB)
        self.assertEqual(dumps_deterministic(a_json), dumps_deterministic(b_json))
        self.assertEqual(a_text, b_text)
        self.assertEqual(a_html, b_html)
        with tempfile.TemporaryDirectory() as tmp:
            d1 = Path(tmp) / "a"
            d2 = Path(tmp) / "b"
            dig1 = write_outputs(d1, a_json, a_text, a_html)
            dig2 = write_outputs(d2, b_json, b_text, b_html)
            self.assertEqual(dig1, dig2)
            for name in dig1:
                self.assertEqual((d1 / name).read_bytes(), (d2 / name).read_bytes())

    def test_claim_premises_and_limits_verbatim(self):
        projection, _, _ = project_bytes(RAW, INPUT_PATH, PINNED_BLOB)
        src = next(c for c in BASE["claims"] if c["id"] == "C01")
        out = next(n for n in projection["nodes"] if n["id"] == "C01")
        self.assertEqual(out["premises"], src["premises"])
        self.assertEqual(out["limits"], src["limits"])

    def test_reading_link_cycles_reported_not_as_proofs(self):
        projection, text, page = project_bytes(RAW, INPUT_PATH, PINNED_BLOB)
        cycles = projection["reading_link_cycles"]
        self.assertTrue(cycles["components"])
        note = cycles["note"].lower()
        self.assertIn("not proofs", note)
        self.assertNotIn("proof of", note)
        self.assertIn("membership only; no implied edge", cycles["note"])
        self.assertIn("not proofs", text.lower())
        self.assertIn("not proofs", page.lower())
        self.assertIn("membership only; no implied edge", text)
        self.assertIn("membership only; no implied edge", page)
        # Reciprocal D01/D03 reading links form a reported component.
        self.assertTrue(any(set(c) >= {"D01", "D03"} for c in cycles["components"]))

    def test_scc_fixture_without_reverse_edges_does_not_invent_arrows(self):
        # Triangle SCC A->B->C->A has no reverse edges B->A, C->B, A->C.
        relations = [
            {"from": "A", "to": "B", "kind": "reading-interface", "directed": True},
            {"from": "B", "to": "C", "kind": "reading-interface", "directed": True},
            {"from": "C", "to": "A", "kind": "reading-interface", "directed": True},
        ]
        comps = reading_link_sccs(
            [{"from": e["from"], "to": e["to"], "kind": e["kind"]} for e in relations]
        )
        self.assertEqual(comps, [["A", "B", "C"]])
        projection = {
            "disclaimer": {
                "scope": "proposed-reference-view",
                "not_authority_for": ["runtime"],
            },
            "legend": {"reading_links": "fixture"},
            "counts": {"nodes": 0, "relations": 3, "planning_requires": 0},
            "nodes": [],
            "layers": {"relations": relations, "planning_requires": []},
            "reading_link_cycles": {
                "components": comps,
                "note": (
                    "Strongly connected reading-link components list member ids only "
                    "(membership only; no implied edge). Directed paths may exist among "
                    "members; actual edges stay only in the relations layer. Not proofs, "
                    "inference rules or semantic entailments."
                ),
            },
        }
        text = render_text(projection)
        page = render_html(projection)
        for output in (text, page, dumps_deterministic(projection)):
            self.assertNotIn("<->", output)
            self.assertNotIn("B -> A", output)
            self.assertNotIn("B->A", output)
            self.assertNotIn("C -> B", output)
            self.assertNotIn("C->B", output)
            self.assertNotIn("A -> C", output)
            self.assertNotIn("A->C", output)
            self.assertNotIn("B -[reading-interface]-> A", output)
            self.assertNotIn("C -[reading-interface]-> B", output)
            self.assertNotIn("A -[reading-interface]-> C", output)
        self.assertIn("strongly connected reading-link component: {A, B, C}", text)
        self.assertIn("membership only; no implied edge", text)
        self.assertIn("membership only; no implied edge", page)
        # Actual directed edges remain only in the relations layer.
        self.assertIn("A -[reading-interface]-> B", text)
        self.assertIn("B -[reading-interface]-> C", text)
        self.assertIn("C -[reading-interface]-> A", text)

    def test_real_input_scc_membership_without_non_edges(self):
        projection, text, page = project_bytes(RAW, INPUT_PATH, PINNED_BLOB)
        reading = [
            e for e in BASE["relations"] if e.get("kind") == "reading-interface"
        ]
        self.assertEqual(len(reading), 13)
        edge_pairs = {(e["from"], e["to"]) for e in reading}
        self.assertNotIn(("D03", "D05"), edge_pairs)
        self.assertNotIn(("D05", "D03"), edge_pairs)
        self.assertIn(("D05", "D06"), edge_pairs)
        self.assertNotIn(("D06", "D05"), edge_pairs)
        scc = next(
            c
            for c in projection["reading_link_cycles"]["components"]
            if set(c) >= {"D01", "D03", "D05", "D06", "D07", "D08"}
        )
        self.assertEqual(scc, ["D01", "D03", "D05", "D06", "D07", "D08"])
        forbidden_fragments = (
            "D03 <-> D05",
            "D05 <-> D03",
            "D03->D05",
            "D05->D03",
            "D03 -> D05",
            "D05 -> D03",
            "D03 -[reading-interface]-> D05",
            "D05 -[reading-interface]-> D03",
            "D06 -[reading-interface]-> D05",
            "D06->D05",
            "D06 -> D05",
            "<->",
        )
        for output in (text, page, dumps_deterministic(projection)):
            for fragment in forbidden_fragments:
                self.assertNotIn(fragment, output, fragment)
        self.assertIn(
            "strongly connected reading-link component: "
            "{D01, D03, D05, D06, D07, D08}",
            text,
        )
        self.assertIn("membership only; no implied edge", text)
        self.assertIn("membership only; no implied edge", page)
        # Real forward edge stays in the relations layer only.
        self.assertIn("D05 -[reading-interface]-> D06", text)

    def test_semantics_copied_from_map(self):
        projection, _, _ = project_bytes(RAW, INPUT_PATH, PINNED_BLOB)
        self.assertEqual(
            projection["semantics"]["required_output_semantics"],
            BASE["required_output_semantics"],
        )
        self.assertEqual(
            projection["semantics"]["preparation_order_semantics"],
            BASE["preparation_order_semantics"],
        )
        self.assertEqual(projection["semantics"]["relation_kinds"], BASE["relation_kinds"])
        self.assertEqual(projection["disclaimer"]["scope"], BASE["scope"])
        self.assertEqual(projection["disclaimer"]["not_authority_for"], BASE["not_authority_for"])

    def refuse(self, raw: bytes, expect_blob: str, reason: str):
        with self.assertRaises(Exception) as ctx:
            project_bytes(raw, INPUT_PATH, expect_blob)
        err = ctx.exception
        self.assertEqual(err.reason_code, reason, getattr(err, "message", err))
        return err

    def test_wrong_expect_blob_refused(self):
        self.refuse(RAW, "0" * 40, REASON_EXPECT_BLOB_MISMATCH)

    def test_unknown_endpoint_refused(self):
        raw = mutate_raw(lambda d: d["relations"][0].update(to="ABSENT-NODE"))
        self.refuse(raw, git_blob_sha1(raw), REASON_UNKNOWN_ENDPOINT)

    def test_duplicate_id_refused(self):
        raw = mutate_raw(lambda d: d["terms"].append(copy.deepcopy(d["terms"][0])))
        self.refuse(raw, git_blob_sha1(raw), REASON_DUPLICATE_ID)

    def test_unsupported_edge_kind_refused(self):
        raw = mutate_raw(
            lambda d: d["relations"].append(
                {"from": "D01", "kind": "proves-truth", "to": "D02", "basis": "fixture"}
            )
        )
        self.refuse(raw, git_blob_sha1(raw), REASON_UNSUPPORTED_EDGE_KIND)

    def test_altered_relation_family_count_refused(self):
        def change(d):
            # Drop one reading-interface edge while keeping the map otherwise coherent enough
            # that the family-count gate is what must fire after validation mapping.
            d["relations"] = [e for e in d["relations"] if not (
                e["from"] == "D01" and e["to"] == "D02" and e["kind"] == "reading-interface"
            )]

        raw = mutate_raw(change)
        # Validator still accepts a structurally valid map with fewer relations.
        from tools.verify_corpus_map import validate

        self.assertTrue(validate(json.loads(raw.decode("utf-8")))["structural_valid"])
        self.refuse(raw, git_blob_sha1(raw), REASON_RELATION_FAMILY_COUNT)

    def test_altered_planning_requires_count_refused(self):
        def change(d):
            node = next(n for n in d["roadmap_nodes"] if n.get("requires"))
            node["requires"] = list(node["requires"])[:-1]

        raw = mutate_raw(change)
        from tools.verify_corpus_map import validate

        self.assertTrue(validate(json.loads(raw.decode("utf-8")))["structural_valid"])
        self.refuse(raw, git_blob_sha1(raw), REASON_PLANNING_REQUIRES_COUNT)

    def test_authority_claim_field_refused(self):
        raw = mutate_raw(lambda d: d.update(runtime_permission={"grant": "deploy"}))
        self.refuse(raw, git_blob_sha1(raw), REASON_AUTHORITY_CLAIM)

    def test_status_relabelled_to_accepted_refused(self):
        raw = mutate_raw(lambda d: d.update(status="accepted"))
        self.refuse(raw, git_blob_sha1(raw), REASON_STATUS_RELABEL)

    def test_html_and_text_expose_layers_and_filters(self):
        _, text, page = project_bytes(RAW, INPUT_PATH, PINNED_BLOB)
        self.assertIn("Layers: relations", text)
        self.assertIn("Layers: planning_requires", text)
        self.assertIn('id="layer-relations"', page)
        self.assertIn('id="layer-planning"', page)
        self.assertIn('href="#kind-reading-interface"', page)
        self.assertIn('href="#group-claims"', page)
        self.assertNotIn("<script", page.lower())


if __name__ == "__main__":
    unittest.main()
