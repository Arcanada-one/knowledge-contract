#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Check the four added Semantic Bridge/Verification bodies and all 72 readers.

This producer check preserves the historical 68-body witness at its own input.
Exact structure and source bindings do not establish prose equivalence, an
independent review, a whole-site release or observed production delivery.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

BASELINE = "18684f073285a4fa20f299518bd8a3d75b0c76d6"
ENGLISH = "8c7cd3bc1247998cb9554c568da26949da31b749"
WORKS = {
    "semantic-bridge": "engineering/specifications/semantic-bridge/SPECIFICATION.md",
    "semantic-verification": "engineering/specifications/semantic-verification/SPECIFICATION.md",
}
ADDED = {(work, language) for work in WORKS for language in ("ru", "zh-Hans")}
HERE = Path(__file__).resolve().parent
PREDECESSOR = HERE.parent / "source-currency-20261116/check_source_currency.py"
spec = importlib.util.spec_from_file_location("kc_source_currency_helpers", PREDECESSOR)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
require, git, at = prior.require, prior.git, prior.at


def key(entry):
    return entry["work"], entry["language"]


def exact_pairs(entries, expected):
    keys = [key(entry) for entry in entries]
    require(len(keys) == len(set(keys)) and set(keys) == expected,
            "BODY_PAIR_COVERAGE", repr(sorted(expected - set(keys))))


def preserve(root, current, relative):
    raw = prior.committed(root, current, relative)
    require(raw == at(root, BASELINE, relative), "HISTORICAL_BYTES_CHANGED", relative)
    return raw


def inventory(root, current, modules):
    rendition, build = modules["renditions"], modules["build_publication"]
    manifest = {"schema_version": 1, "repository": prior.REPOSITORY, "commit": current,
                "edition": "1.1", "catalog": "publication-catalog.json"}
    catalog = prior.read_json(preserve(root, current, manifest["catalog"]))
    documents = copy.deepcopy(catalog["documents"])
    require(len(documents) == 36, "WORK_INVENTORY")
    for doc in documents:
        raw = prior.committed(root, current, doc["path"])
        require(raw == at(root, ENGLISH, doc["path"]), "ENGLISH_CHANGED", doc["path"])
        doc["sha256"] = sha256(raw).hexdigest()
        doc["route"] = build.KINDS[doc["type"]][1] + doc["slug"] + "/"
    expected = {(doc["slug"], lang) for doc in documents for lang in ("ru", "zh-Hans")}
    raw = prior.committed(root, current, catalog["renditions"])
    old_raw = at(root, BASELINE, catalog["renditions"])
    entries = rendition.validate_sidecar(prior.read_json(raw), manifest)
    old = rendition.validate_sidecar(prior.read_json(old_raw), manifest)
    exact_pairs(entries, expected)
    require(len(old) == 68 and {key(e) for e in entries} - {key(e) for e in old} == ADDED,
            "ADDED_PAIR_SET")
    require(prior.entry_bytes(raw, "renditions")[:68] == prior.entry_bytes(old_raw, "renditions"),
            "HISTORICAL_ENTRY_BYTES")
    require([key(e) for e in entries[:68]] == [key(e) for e in old], "HISTORICAL_ORDER")
    reviews = {key(e): e["review"] for e in entries if "review" in e}
    require(reviews == {key(e): e["review"] for e in old if "review" in e} and len(reviews) == 8,
            "HISTORICAL_REVIEWS_CHANGED")
    by_work = {doc["slug"]: doc for doc in documents}
    require({work: by_work[work]["path"] for work in WORKS} == WORKS, "SOURCE_PATHS")
    revisions = {e["rendition"]["revision"] for e in entries if key(e) in ADDED}
    require(len(revisions) == 1, "CONTENT_REVISION_NOT_COMMON")
    content = next(iter(revisions))
    prior.ancestor(root, BASELINE, content)
    prior.ancestor(root, ENGLISH, content)
    prior.ancestor(root, content, current)
    for entry in entries:
        label = "/".join(key(entry))
        for field, code in (("source", "RENDITION_SOURCE_PIN"), ("rendition", "RENDITION_REVISION_PIN")):
            rendition.verify_pin(root, manifest, label, entry[field], code)
        source = by_work[entry["work"]]
        require(entry["source"]["path"] == source["path"] and
                entry["source"]["sha256"] == source["sha256"], "SOURCE_CURRENCY", label)
        prior.ancestor(root, entry["source"]["revision"], entry["rendition"]["revision"])
        target = prior.committed(root, current, entry["rendition"]["path"])
        require(sha256(target).hexdigest() == entry["rendition"]["sha256"], "TARGET_DIGEST", label)
        if key(entry) in ADDED:
            require("review" not in entry and entry["author"]["identity"] == "KC-Brain", "UNEARNED_REVIEW")
            require(entry["source"]["revision"] == ENGLISH, "ADDED_SOURCE_REVISION")
            require(target == at(root, content, entry["rendition"]["path"]), "CONTENT_BYTES")
        else:
            require(target == at(root, BASELINE, entry["rendition"]["path"]), "RETAINED_BODY_CHANGED", label)
    preserve(root, current, "publication-localization.json")
    metadata = modules["catalogue_localization"].compile_localization(root, manifest, documents)
    require(len(metadata["provenance"]["entries"]) == 72, "METADATA_INVENTORY")
    preserve(root, current, "publication-formula-localizations.json")
    review_path = "publication-review-localizations.json"
    review_raw = prior.committed(root, current, review_path)
    old_review_raw = at(root, BASELINE, review_path)
    review, old_review = prior.read_json(review_raw), prior.read_json(old_review_raw)
    require(prior.entry_bytes(review_raw, "entries") == prior.entry_bytes(old_review_raw, "entries"),
            "REVIEW_PRESENTATION_BYTES")
    omit = {"source_revision", "source_sha256"}
    require({k: v for k, v in review.items() if k not in omit} ==
            {k: v for k, v in old_review.items() if k not in omit}, "REVIEW_PRESENTATION_SCOPE")
    prior.ancestor(root, review["source_revision"], current)
    require(at(root, review["source_revision"], review["source_path"]) == raw and
            review["source_sha256"] == sha256(raw).hexdigest(), "REVIEW_PRESENTATION_BINDING")
    retained = git(root, "ls-tree", "-r", "--name-only", BASELINE, "reviews/renditions").decode().splitlines()
    for path in retained:
        preserve(root, current, path)
    return manifest, documents, entries, expected, content, len(retained)


def check_bodies(root, manifest, documents, entries, modules):
    rendition, build = modules["renditions"], modules["build_publication"]
    by_path = {d["path"]: d for d in documents}
    tree = rendition.tree_paths(root, manifest["commit"])
    pinned, peer_maps = rendition.link_context(entries)
    records, controls = [], []

    def refused(name, code, operation):
        try:
            operation()
        except ValueError as error:
            require(str(error).split(":", 1)[0] == code, "WRONG_REFUSAL", name + ": " + str(error))
            controls.append({"name": name, "refusal": code})
        else:
            raise prior.Refusal("ADVERSE_CONTROL_NOT_DETECTED: " + name)

    for entry in entries:
        if key(entry) not in ADDED:
            continue
        work, language = key(entry)
        label = work + "/" + language
        source = build.parse_markdown(root / entry["source"]["path"])
        target = build.parse_markdown(root / entry["rendition"]["path"])
        for field in ("name", "artifact", "edition", "author", "license", "status"):
            require(rendition.meta_value(target, field) == rendition.meta_value(source, field),
                    "METADATA_INVARIANT", label + ": " + field)
        for field, value in (("language", language), ("translation_of", entry["source"]["path"]),
                             ("source_commit", ENGLISH), ("translation_status", "author-draft"),
                             ("source_git_blob", git(root, "rev-parse", ENGLISH + ":" + entry["source"]["path"]).decode().strip())):
            require(rendition.meta_value(target, field) == value, "METADATA_BINDING", label + ": " + field)
        require(target["meta"].get("sources") == source["meta"].get("sources"), "SOURCE_IDENTITIES", label)
        for field in ("title", "description"):
            require(rendition.script_matches(language, rendition.meta_value(target, field)), "METADATA_LANGUAGE", label)
        title = [b for b in target["blocks"] if b["t"] == "Header" and b["c"][0] == 1]
        require(len(title) == 1 and build.plain(title[0]["c"][2]) == rendition.meta_value(target, "title"), "TITLE_BINDING")
        mapping = {p["rendition"]: p["source"] for p in entry["sections"]}
        mapping[rendition.title_id(target)] = rendition.title_id(source)
        def links():
            return rendition.analyse_links(target, entry["rendition"]["path"], language, tree, by_path,
                                           pinned[language], mapping, rendition.anchors_of(target), rendition.anchors_of(source))
        rendition.check_parity(entry, source, target, before_references=links, peer_maps=peer_maps)
        effective = modules["rendition_preamble"].source_for_anchor_parity(source, target)
        require([prior.block_shape(b) for b in effective["blocks"]] ==
                [prior.block_shape(b) for b in target["blocks"]], "BLOCK_OR_CELL_BOUNDARIES", label)
        for field, code in (("source", "RENDITION_SOURCE_PIN"), ("rendition", "RENDITION_REVISION_PIN")):
            pin = dict(entry[field], sha256="0" * 64)
            refused(label + ": corrupt " + field + " digest", code,
                    lambda: rendition.verify_pin(root, manifest, label, pin, code))
        stale_doc = dict(by_path[entry["source"]["path"]], sha256="0" * 64)
        require(rendition.resolve_state(root, manifest, stale_doc, entry)[0] == "stale", "STALE_SOURCE_NOT_DETECTED")
        controls.append({"name": label + ": source bytes no longer match pinned body", "state": "stale"})
        for kind, code in (("Header", "RENDITION_SECTION_UNRESOLVED"), ("Math", "RENDITION_FORMULA_CHANGED"),
                           ("Code", "RENDITION_CODE_CHANGED"), ("Link", "RENDITION_REFERENCE_DROPPED")):
            mutant = copy.deepcopy(target)
            if kind == "Header":
                index = next(i for i, b in enumerate(mutant["blocks"]) if b["t"] == kind and b["c"][0] == 2)
                del mutant["blocks"][index]
            else:
                node = next(n for n in prior.walk(mutant["blocks"]) if n.get("t") == kind)
                if kind in {"Code", "Math"}:
                    node["c"][1] += " changed"
                else:
                    node["t"], node["c"] = "Span", [["", [], []], node["c"][1]]
            refused(label + ": alter " + kind, code,
                    lambda: rendition.check_parity(entry, source, mutant, peer_maps=peer_maps))
        facts = rendition.facts(source, entry["source"]["path"], {a: a for a in rendition.anchors_of(source)})
        records.append({"work": work, "language": language, "source_sha256": entry["source"]["sha256"],
                        "rendition_sha256": entry["rendition"]["sha256"], "sections": len(entry["sections"]),
                        "blocks": len(target["blocks"]), "math_objects": len(facts["formulas"]),
                        "code_objects": len(facts["code"]), "references": sum(facts["references"].values())})
    expected = {(doc["slug"], lang) for doc in documents for lang in ("ru", "zh-Hans")}
    for name, mutation in (("omit final body", entries[:-1]),
                           ("replace body with existing pair", entries[:-1] + [copy.deepcopy(entries[0])])):
        refused(name, "BODY_PAIR_COVERAGE", lambda: exact_pairs(mutation, expected))
    require(len(records) == 4, "CHECKED_BODY_INVENTORY")
    return records, controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--site-repository", type=Path, required=True)
    parser.add_argument("--pandoc", default="pandoc")
    parser.add_argument("--check-retained-result", action="store_true")
    args = parser.parse_args()
    if not __debug__:
        parser.error("optimized Python is unsupported: the pinned external consumer uses assertions")
    root, site = args.repository.resolve(), args.site_repository.resolve()
    current = git(root, "rev-parse", "HEAD").decode().strip()
    prior.ancestor(root, BASELINE, current)
    preserve(root, current, PREDECESSOR.relative_to(root).as_posix())
    prior.committed(root, current, Path(__file__).resolve().relative_to(root).as_posix())
    modules, checker_hashes, pandoc = prior.load_checker(site, args.pandoc)
    manifest, documents, entries, expected, content, retained = inventory(root, current, modules)
    records, controls = check_bodies(root, manifest, documents, entries, modules)
    with tempfile.TemporaryDirectory(prefix="kc-complete-renditions-") as directory:
        renderer = modules["build_publication"].Renderer(root, Path(directory), manifest, documents)
        compiled = modules["renditions"].compile_renditions(root, manifest, documents, renderer, modules["build_publication"].run)
        require(compiled is not None, "COMPILED_ABSENT")
        exact_pairs(compiled.entries, expected)
        states = Counter(e["state"] for e in compiled.entries)
        require(states == {"reviewed": 8, "unreviewed": 64}, "COMPILED_STATES", repr(states))
        # entries is the provenance inventory; reader HTML is held separately
        # by for_work(). Inspect the consumer's actual rendered-body surface.
        for work, language in sorted(expected):
            record = compiled.for_work(work)[language]
            require(bool(record.get("html")), "COMPILED_BODY_EMPTY", repr((work, language)))
        presentation = {"formula": renderer.formula_localizations.provenance(),
                        "review": renderer.review_localizations.provenance()}
        require(all(presentation.values()), "PRESENTATION_NOT_EXECUTED")
    report = {"schema_version": 1, "result": "PASS", "baseline_revision": BASELINE,
                     "english_revision": ENGLISH, "publication_revision": current, "content_revision": content,
                     "site_revision": prior.SITE, "pandoc": pandoc,
                     "scope": "author structural checks and actual complete rendition consumer",
                     "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
                     "site_script_sha256": checker_hashes, "catalogue_works": 36, "metadata_records": 72,
                     "rendition_entries": 72, "retained_entries": 68, "missing_pairs": [],
                     "current_source_mismatches": 0, "historical_review_objects_unchanged": 8,
                     "historical_producer_files_unchanged": retained, "compiled_states": dict(states),
                     "bodies": records, "adverse_controls_detected": len(controls), "adverse_controls": controls,
                     "actual_presentation": presentation,
                     "limitations": ["Structural parity does not prove prose equivalence or independent semantic acceptance.",
                                     "This runs the reader consumer, not the full site compiler or deployment.",
                                     "Historical reviews retain their own scope; four new manuscripts remain unreviewed."]}
    roadmap_tool = root / "tools/check_translation_roadmap_currency.py"
    preserve(root, current, roadmap_tool.relative_to(root).as_posix())
    roadmap_spec = importlib.util.spec_from_file_location("kc_roadmap_witness", roadmap_tool)
    roadmap = importlib.util.module_from_spec(roadmap_spec)
    roadmap_spec.loader.exec_module(roadmap)
    observed = roadmap.witness(prior.committed(root, current, "roadmap/TRANSLATIONS.md").decode("utf-8"))
    actual = {"catalogue_works": 36, "metadata_cards": 72, "registered_bodies": 72,
              "source_mismatches": 0, "missing_pairs": [], "historical_review_entries": 8}
    roadmap.match(observed, actual)
    roadmap.match(roadmap.inventory(root), actual)
    if args.check_retained_result:
        retained_result = prior.read_json(prior.committed(root, current,
            "reviews/renditions/semantic-specifications-20261117/producer-result.json"))
        prior.ancestor(root, retained_result["publication_revision"], current)
        # A later receipt-only commit must not change its protected test inputs.
        for field in report:
            if field not in {"publication_revision", "actual_presentation"}:
                require(retained_result[field] == report[field], "RETAINED_RESULT_CHANGED", field)
        # Presentation embeds the newer publication commit; bindings and bytes
        # themselves were verified above by the actual constructors/consumers.
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(json.dumps({"result": "FAIL", "reason": str(error)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
