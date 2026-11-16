#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Check ten source-currency repairs and two scoped editorial follow-ups.

This is a bounded producer check of committed repository bytes, actual Pandoc
ASTs and rendered rendition records. It grants no translation review, scientific
acceptance, publication or runtime admission. The historical c135 producer and
receipt are deliberately unchanged and must be replayed at their own revision.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
from hashlib import sha256
import importlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch

BASELINE = "b00b42fb5ca4f32ca443812c980c13d4d5d53d81"
ENGLISH = "8c7cd3bc1247998cb9554c568da26949da31b749"
SITE = "d3d17929f209612669f38db6a735d46bc9ec309c"
REPOSITORY = "Arcanada-one/knowledge-contract"
LANGUAGES = ("ru", "zh-Hans")
WORKS = {
    "constrained-transformations": "papers/constrained-transformations/PAPER.md",
    "evidence-and-falsification": "papers/evidence-and-falsification/PAPER.md",
    "geometry-of-semantic-representations": "papers/geometry-of-semantic-representations/PAPER.md",
    "bibliography": "reference/bibliography/BIBLIOGRAPHY.md",
    "source-map": "appendices/source-map/APPENDIX.md",
}
UPDATED = {(work, language) for work in WORKS for language in LANGUAGES}
EDITORIAL = {("agent-situation", language) for language in LANGUAGES}
EDITORIAL_CONTENT = "98ae7046baf8dba41d77c7e1728f1321b2b71cf0"
ADDED_FORMULA_DOCUMENT = {
    "path": WORKS["constrained-transformations"],
    "source_sha256": "954101bf1c0f540648862b1ead5a8c6324817283e9e87284c81bbb1a19aed432",
    "annotations": [{
        "math_index": 89, "math_type": "DisplayMath",
        "tex_sha256": "88fee1d40bf85f7c9c453d05f191dd2d5cb869e05ecc5852ea7c244320b20b35",
        "mtext_index": 1, "source_text": "for all ",
        "translations": {"ru": "для всех ", "zh-Hans": "对于任意 "},
    }],
}
MISSING = {
    (work, language)
    for work in ("semantic-bridge", "semantic-verification")
    for language in LANGUAGES
}
RETAINED_DIRECTORIES = (
    "reviews/renditions/context-controls-20261116/",
    "reviews/renditions/source-rule-checks-20261116/",
    "reviews/renditions/agent-situation-20261116/",
)
REQUIRED_MODULES = (
    "build_publication", "renditions", "rendition_preamble",
    "catalogue_localization", "formula_localization", "review_localization",
)
MARKDOWN = "markdown+gfm_auto_identifiers+pipe_tables+tex_math_dollars+tex_math_single_backslash+autolink_bare_uris"


class Refusal(ValueError):
    pass


def require(condition, code, detail=""):
    if not condition:
        raise Refusal(code + (": " + detail if detail else ""))


def git(root, *arguments):
    result = subprocess.run(["git", "-C", str(root), *arguments], capture_output=True)
    require(result.returncode == 0, "GIT", " ".join(arguments) + ": " + result.stderr.decode(errors="replace").strip())
    return result.stdout


def at(root, revision, path):
    return git(root, "show", revision + ":" + path)


def ancestor(root, older, newer):
    git(root, "merge-base", "--is-ancestor", older, newer)


def read_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "DUPLICATE_JSON_KEY", key)
            result[key] = value
        return result

    def nonfinite(value):
        raise Refusal("NONFINITE_JSON: " + value)

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite)


def entry_bytes(raw, array_name):
    """Extract exact JSON object bytes, rather than comparing reserialized objects."""
    text = raw.decode("utf-8")
    decoder = json.JSONDecoder()

    def space(index):
        while index < len(text) and text[index].isspace():
            index += 1
        return index

    index = space(0)
    require(text[index] == "{", "JSON_OBJECT_EXPECTED")
    index = space(index + 1)
    while text[index] != "}":
        key, index = decoder.raw_decode(text, index)
        index = space(index)
        require(text[index] == ":", "JSON_COLON_EXPECTED")
        index = space(index + 1)
        if key == array_name:
            require(text[index] == "[", "JSON_ARRAY_EXPECTED", array_name)
            result, index = [], space(index + 1)
            while text[index] != "]":
                start = index
                _, index = decoder.raw_decode(text, index)
                result.append(text[start:index].encode("utf-8"))
                index = space(index)
                if text[index] == ",":
                    index = space(index + 1)
            return result
        _, index = decoder.raw_decode(text, index)
        index = space(index)
        if text[index] == ",":
            index = space(index + 1)
    raise Refusal("JSON_ARRAY_MISSING: " + array_name)


def committed(root, revision, path):
    relative = Path(path)
    require(not relative.is_absolute() and ".." not in relative.parts, "REPOSITORY_PATH", path)
    file = (root / relative).resolve()
    require(file.is_relative_to(root), "REPOSITORY_PATH", path)
    raw = file.read_bytes()
    require(raw == at(root, revision, path), "UNCOMMITTED_INPUT", path)
    return raw


def walk(value):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


def rows(table):
    value = table["c"]
    return value[3][1] + [row for group in value[4] for row in group[2] + group[3]] + value[5][1]


def block_shape(block):
    """Preserve paragraph/list/cell boundaries without asserting prose equivalence."""
    kind, content = block["t"], block.get("c")
    if kind in {"Para", "Plain"}:
        return kind
    if kind == "Header":
        return [kind, content[0]]
    if kind in {"BulletList", "OrderedList"}:
        attributes, items = (None, content) if kind == "BulletList" else content
        return [kind, attributes, [[block_shape(child) for child in item] for item in items]]
    if kind == "Table":
        return [kind, len(content[2]), [block_shape(child) for child in content[1][1]],
                [[[cell[2], cell[3], [block_shape(child) for child in cell[4]]]
                  for cell in row[1]] for row in rows(block)]]
    if kind == "BlockQuote":
        return [kind, [block_shape(child) for child in content]]
    if kind in {"CodeBlock", "RawBlock", "HorizontalRule"}:
        return [kind, content]
    raise Refusal("UNEXPECTED_BLOCK_KIND: " + kind)


def parse_bytes(raw, build):
    return read_json(build.run(["pandoc", "--from=" + MARKDOWN, "--to=json"], raw.decode("utf-8")))


def structural_target_blocks(work, language, target, old_target, build):
    """Keep the two exact historical source-map link-language notices visible.

    These author disclosures already exist at BASELINE, immediately after the
    scientific-crosswalk heading. They are not English-source paragraphs. Only
    this declared, unchanged paragraph is excluded from the extra block-shape
    comparison; the real consumer still checks the full unmodified target AST.
    """
    if work != "source-map":
        return target["blocks"], None
    expected = {
        "ru": "Ссылки на текущие документы в таблицах ведут к закреплённому английскому оригиналу.",
        "zh-Hans": "下列表格中指向当前文档的链接均指向固定修订版的英文原文。",
    }[language]

    def locate(ast):
        candidates = [i + 1 for i, block in enumerate(ast["blocks"])
                      if block["t"] == "Header" and block["c"][1][0] == "2-scientific-crosswalk"]
        require(len(candidates) == 1 and candidates[0] < len(ast["blocks"]), "RETAINED_NOTICE_LOCATION")
        index = candidates[0]
        paragraph = ast["blocks"][index]
        require(paragraph["t"] == "Para" and build.plain(paragraph) == expected, "RETAINED_NOTICE_TEXT")
        return index, paragraph

    index, paragraph = locate(target)
    _, old_paragraph = locate(old_target)
    require(paragraph == old_paragraph, "RETAINED_NOTICE_CHANGED")
    return target["blocks"][:index] + target["blocks"][index + 1:], {
        "anchor": "2-scientific-crosswalk", "text": expected,
        "baseline_ast_identical": True,
    }


def load_checker(site, pandoc):
    executable = shutil.which(str(pandoc))
    require(executable is not None, "PANDOC_MISSING")
    executable = str(Path(executable).resolve())
    version = subprocess.check_output([executable, "--version"], text=True).splitlines()[0]
    require(version == "pandoc 3.1.3", "PANDOC_VERSION", version)
    os.environ["PATH"] = str(Path(executable).parent) + os.pathsep + os.environ.get("PATH", "")
    require(Path(shutil.which("pandoc")).resolve() == Path(executable), "PANDOC_SELECTION")
    require(git(site, "rev-parse", "HEAD").decode().strip() == SITE, "SITE_REVISION")
    scripts = site / "scripts"
    expected = {
        name for name in git(site, "ls-tree", "-r", "--name-only", SITE, "scripts").decode().splitlines()
        if name.endswith(".py")
    }
    actual = {path.relative_to(site).as_posix() for path in scripts.rglob("*.py")}
    require(actual == expected, "CHECKER_MODULE_INVENTORY")
    hashes = {}
    for relative in sorted(expected):
        raw = committed(site, SITE, relative)
        hashes[relative] = sha256(raw).hexdigest()
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(scripts))
    modules = {name: importlib.import_module(name) for name in REQUIRED_MODULES}
    for name, module in modules.items():
        require(Path(module.__file__).resolve() == scripts / (name + ".py"), "CHECKER_IMPORT", name)
    return modules, hashes, version


def preserve_history(root, current):
    paths = git(root, "ls-tree", "-r", "--name-only", BASELINE, *RETAINED_DIRECTORIES).decode().splitlines()
    require(paths and all(any(path.startswith(directory) for path in paths) for directory in RETAINED_DIRECTORIES),
            "RETAINED_PRODUCER_INVENTORY")
    for path in paths:
        require(committed(root, current, path) == at(root, BASELINE, path), "RETAINED_PRODUCER_CHANGED", path)
    return {path: sha256(at(root, BASELINE, path)).hexdigest() for path in paths}


def inventory(root, current, modules):
    rendition = modules["renditions"]
    manifest = {"schema_version": 1, "repository": REPOSITORY, "commit": current,
                "edition": "1.1", "catalog": "publication-catalog.json"}
    catalog_raw = committed(root, current, manifest["catalog"])
    require(catalog_raw == at(root, BASELINE, manifest["catalog"]), "CATALOGUE_CHANGED")
    catalog = read_json(catalog_raw)
    require(catalog["edition"] == manifest["edition"] and catalog["renditions"] == "publication-renditions.json",
            "CATALOGUE_BINDING")
    documents = copy.deepcopy(catalog["documents"])
    require(len(documents) == 36, "WORK_INVENTORY")
    for doc in documents:
        raw = committed(root, current, doc["path"])
        require(raw == at(root, ENGLISH, doc["path"]), "ENGLISH_SOURCE_CHANGED", doc["path"])
        doc["sha256"] = sha256(raw).hexdigest()
        # Deliberately compile the rendition consumer, not load_inputs/full site:
        # this pinned site's publication-status allowlist predates this catalog.
        doc["route"] = modules["build_publication"].KINDS[doc["type"]][1] + doc["slug"] + "/"
    by_work = {doc["slug"]: doc for doc in documents}
    require(len(by_work) == len(documents), "DUPLICATE_WORK")
    require({work: by_work[work]["path"] for work in WORKS} == WORKS, "UPDATED_WORK_PATHS")
    raw = committed(root, current, catalog["renditions"])
    baseline_raw = at(root, BASELINE, catalog["renditions"])
    entries = rendition.validate_sidecar(read_json(raw), manifest)
    baseline_entries = rendition.validate_sidecar(read_json(baseline_raw), manifest)
    key = lambda entry: (entry["work"], entry["language"])
    require(len(entries) == len(baseline_entries) == 68, "RENDITION_INVENTORY")
    require([key(e) for e in entries] == [key(e) for e in baseline_entries], "RENDITION_ORDER_OR_KEYS")
    previous = {key(e): e for e in baseline_entries}
    changed = {key(e) for e in entries if e != previous[key(e)]}
    require(changed == UPDATED | EDITORIAL, "UPDATED_PAIR_SET", repr(sorted(changed)))
    fragments, old_fragments = entry_bytes(raw, "renditions"), entry_bytes(baseline_raw, "renditions")
    for index, entry in enumerate(entries):
        if key(entry) not in UPDATED | EDITORIAL:
            require(fragments[index] == old_fragments[index], "UNCHANGED_ENTRY_BYTES", repr(key(entry)))
    reviews = {key(e): e["review"] for e in entries if "review" in e}
    old_reviews = {key(e): e["review"] for e in baseline_entries if "review" in e}
    require(reviews == old_reviews and len(reviews) == 8, "HISTORICAL_REVIEWS_CHANGED")
    content_revisions = {e["rendition"]["revision"] for e in entries if key(e) in UPDATED}
    require(len(content_revisions) == 1, "CONTENT_REVISION_NOT_COMMON")
    content_revision = next(iter(content_revisions))
    require(content_revision != BASELINE, "CONTENT_REVISION_NOT_UPDATED")
    ancestor(root, BASELINE, content_revision)
    ancestor(root, ENGLISH, content_revision)
    ancestor(root, content_revision, current)
    ancestor(root, BASELINE, EDITORIAL_CONTENT)
    ancestor(root, EDITORIAL_CONTENT, current)
    for entry in entries:
        identity = key(entry)
        old = previous[identity]
        doc = by_work[entry["work"]]
        for field, code in (("source", "RENDITION_SOURCE_PIN"), ("rendition", "RENDITION_REVISION_PIN")):
            rendition.verify_pin(root, manifest, "/".join(identity), entry[field], code)
        ancestor(root, entry["source"]["revision"], entry["rendition"]["revision"])
        target = committed(root, current, entry["rendition"]["path"])
        require(sha256(target).hexdigest() == entry["rendition"]["sha256"], "TARGET_BYTES", repr(identity))
        require(entry["source"]["path"] == doc["path"] and entry["source"]["sha256"] == doc["sha256"],
                "CURRENT_SOURCE_MISMATCH", repr(identity))
        if identity in UPDATED:
            require("review" not in entry and "review" not in old, "UNEARNED_REVIEW", repr(identity))
            require({k: v for k, v in entry.items() if k not in {"source", "rendition", "sections"}} ==
                    {k: v for k, v in old.items() if k not in {"source", "rendition", "sections"}},
                    "UPDATED_ENTRY_SCOPE", repr(identity))
            require(entry["source"]["revision"] == ENGLISH, "UPDATED_SOURCE_REVISION", repr(identity))
            require(target == at(root, content_revision, entry["rendition"]["path"]), "CONTENT_REVISION_BYTES")
            require(target != at(root, BASELINE, entry["rendition"]["path"]), "BODY_NOT_UPDATED", repr(identity))
        elif identity in EDITORIAL:
            require("review" not in entry and "review" not in old, "UNEARNED_EDITORIAL_REVIEW", repr(identity))
            require({k: v for k, v in entry.items() if k != "rendition"} ==
                    {k: v for k, v in old.items() if k != "rendition"},
                    "EDITORIAL_ENTRY_SCOPE", repr(identity))
            require(entry["source"] == old["source"], "EDITORIAL_SOURCE_CHANGED", repr(identity))
            require(entry["rendition"]["path"] == old["rendition"]["path"], "EDITORIAL_TARGET_PATH", repr(identity))
            require(entry["rendition"]["revision"] == EDITORIAL_CONTENT, "EDITORIAL_CONTENT_REVISION", repr(identity))
            require(target == at(root, EDITORIAL_CONTENT, entry["rendition"]["path"]), "EDITORIAL_CONTENT_BYTES", repr(identity))
            require(target != at(root, BASELINE, entry["rendition"]["path"]), "EDITORIAL_BODY_NOT_UPDATED", repr(identity))
        else:
            require(target == at(root, BASELINE, entry["rendition"]["path"]), "UNCHANGED_BODY_CHANGED", repr(identity))
    expected = {(work, language) for work in by_work for language in LANGUAGES}
    missing = expected - {key(e) for e in entries}
    require(missing == MISSING, "MISSING_BODY_SET", repr(sorted(missing)))
    metadata = committed(root, current, "publication-localization.json")
    require(metadata == at(root, BASELINE, "publication-localization.json"), "METADATA_CHANGED")
    compiled_metadata = modules["catalogue_localization"].compile_localization(root, manifest, documents)
    require(len(compiled_metadata["provenance"]["entries"]) == 72, "METADATA_INVENTORY")
    return manifest, documents, entries, previous, content_revision, compiled_metadata


def presentation_scope(root, current):
    formula_name = "publication-formula-localizations.json"
    formula = read_json(committed(root, current, formula_name))
    old_formula = read_json(at(root, BASELINE, formula_name))
    require(formula["source_revision"] == ENGLISH, "FORMULA_SOURCE_REVISION")
    allowed = copy.deepcopy(old_formula)
    allowed["source_revision"] = ENGLISH
    for doc in allowed["documents"]:
        if doc["path"] == WORKS["geometry-of-semantic-representations"]:
            doc["source_sha256"] = sha256(at(root, ENGLISH, doc["path"])).hexdigest()
    allowed["documents"].append(ADDED_FORMULA_DOCUMENT)
    require(formula == allowed, "FORMULA_PRESENTATION_SCOPE")
    review_name = "publication-review-localizations.json"
    review_raw, old_review_raw = committed(root, current, review_name), at(root, BASELINE, review_name)
    review, old_review = read_json(review_raw), read_json(old_review_raw)
    require(entry_bytes(review_raw, "entries") == entry_bytes(old_review_raw, "entries"), "REVIEW_PRESENTATION_BYTES")
    require({k: v for k, v in review.items() if k not in {"source_revision", "source_sha256"}} ==
            {k: v for k, v in old_review.items() if k not in {"source_revision", "source_sha256"}},
            "REVIEW_PRESENTATION_CHANGED")
    ancestor(root, review["source_revision"], current)
    require(at(root, review["source_revision"], review["source_path"]) ==
            committed(root, current, review["source_path"]), "REVIEW_DESCRIPTOR_BINDING")
    require(review["source_sha256"] == sha256(committed(root, current, review["source_path"])).hexdigest(),
            "REVIEW_DESCRIPTOR_DIGEST")
    return {"formula_source_revision": formula["source_revision"],
            "new_formula_text_annotations": 1,
            "review_source_revision": review["source_revision"],
            "review_source_sha256": review["source_sha256"],
            "unchanged_review_presentations": len(review["entries"])}


def check_bodies(root, manifest, documents, entries, previous, modules):
    rendition, build, preamble = (modules[name] for name in ("renditions", "build_publication", "rendition_preamble"))
    by_path = {doc["path"]: doc for doc in documents}
    tree = rendition.tree_paths(root, manifest["commit"])
    pinned, peer_maps = rendition.link_context(entries)
    source_cache, old_source_cache = {}, {}
    records, controls = [], []

    def rejected(name, expected, operation):
        try:
            operation()
        except rendition.RenditionError as error:
            require(error.code == expected, "ADVERSE_CONTROL_WRONG_REASON", name + ": " + str(error))
            controls.append({"name": name, "refusal": expected})
        else:
            raise Refusal("ADVERSE_CONTROL_NOT_DETECTED: " + name)

    for entry in entries:
        identity = entry["work"], entry["language"]
        if identity not in UPDATED:
            continue
        work, language = identity
        label = work + "/" + language
        old = previous[identity]
        source_path = entry["source"]["path"]
        if work not in source_cache:
            source_cache[work] = build.parse_markdown(root / source_path)
            old_source_cache[work] = parse_bytes(at(root, old["source"]["revision"], source_path), build)
        source = source_cache[work]
        target = build.parse_markdown(root / entry["rendition"]["path"])
        old_target = parse_bytes(at(root, BASELINE, entry["rendition"]["path"]), build)
        effective_source = preamble.source_for_anchor_parity(source, target)
        for field in ("name", "artifact", "edition", "author", "license", "status"):
            require(rendition.meta_value(target, field) == rendition.meta_value(source, field),
                    "METADATA_INVARIANT", label + ": " + field)
        for field, expected in (("language", language), ("translation_of", source_path),
                                ("source_commit", ENGLISH), ("source_git_blob", git(root, "rev-parse", ENGLISH + ":" + source_path).decode().strip()),
                                ("translation_status", "author-draft")):
            require(rendition.meta_value(target, field) == expected, "METADATA_BINDING", label + ": " + field)
        require(target.get("meta", {}).get("sources") == source.get("meta", {}).get("sources"), "SOURCE_IDS_CHANGED", label)
        for field in ("title", "short_title", "subtitle", "description"):
            value = rendition.meta_value(target, field)
            if value is not None:
                require(rendition.script_matches(language, value), "METADATA_LANGUAGE", label + ": " + field)
        title = [b for b in target["blocks"] if b["t"] == "Header" and b["c"][0] == 1]
        require(len(title) == 1 and build.plain(title[0]["c"][2]) == rendition.meta_value(target, "title"), "TITLE_BINDING", label)
        source_heads, _ = rendition.sections_of(source)
        old_heads, _ = rendition.sections_of(old_source_cache[work])
        new_sections = [anchor for _, anchor in source_heads if anchor not in {value for _, value in old_heads}]
        mapping = {p["rendition"]: p["source"] for p in entry["sections"]}
        if rendition.title_id(source) and rendition.title_id(target):
            mapping[rendition.title_id(target)] = rendition.title_id(source)

        def links():
            return rendition.analyse_links(target, entry["rendition"]["path"], language, tree, by_path,
                                           pinned[language], mapping, rendition.anchors_of(target), rendition.anchors_of(source))

        rendition.check_parity(entry, source, target, before_references=links, peer_maps=peer_maps)
        structural_blocks, retained_notice = structural_target_blocks(work, language, target, old_target, build)
        require([block_shape(b) for b in effective_source["blocks"]] == [block_shape(b) for b in structural_blocks],
                "BLOCK_OR_CELL_BOUNDARIES", label)
        source_facts = rendition.facts(source, source_path, {anchor: anchor for anchor in rendition.anchors_of(source)})
        old_facts = rendition.facts(old_source_cache[work], source_path,
                                    {anchor: anchor for anchor in rendition.anchors_of(old_source_cache[work])})

        stale = copy.deepcopy(entry)
        stale["source"] = copy.deepcopy(old["source"])
        require(rendition.resolve_state(root, manifest, by_path[source_path], stale)[0] == "stale",
                "STALE_SOURCE_NOT_DETECTED", label)
        controls.append({"name": label + ": restore actual old source pin", "state": "stale"})

        expected_old_refusal = "RENDITION_SECTION_UNRESOLVED" if new_sections else "RENDITION_REFERENCE_DROPPED"
        rejected(label + ": retag actual old body", expected_old_refusal,
                 lambda: rendition.check_parity(entry, source, old_target, peer_maps=peer_maps))

        if new_sections:
            mutant = copy.deepcopy(target)
            anchor = next(p["rendition"] for p in entry["sections"] if p["source"] == new_sections[0])
            start = next(i for i, b in enumerate(mutant["blocks"]) if b["t"] == "Header" and b["c"][1][0] == anchor)
            level = mutant["blocks"][start]["c"][0]
            end = next((i for i in range(start + 1, len(mutant["blocks"]))
                        if mutant["blocks"][i]["t"] == "Header" and mutant["blocks"][i]["c"][0] <= level),
                       len(mutant["blocks"]))
            del mutant["blocks"][start:end]
            rejected(label + ": omit new section " + anchor, "RENDITION_SECTION_UNRESOLVED",
                     lambda: rendition.check_parity(entry, source, mutant, peer_maps=peer_maps))
        if source_facts["formulas"]:
            mutant = copy.deepcopy(target)
            formula = next(n for n in walk(mutant["blocks"]) if n.get("t") == "Math")
            formula["c"][1] += " + 0"
            rejected(label + ": change exact formula", "RENDITION_FORMULA_CHANGED",
                     lambda: rendition.check_parity(entry, source, mutant, peer_maps=peer_maps))
        new_links = source_facts["references"] - old_facts["references"]
        require(any(key[0] == "Link" for key in new_links), "NEW_REFERENCE_CONTROL_UNAVAILABLE", label)
        mutant = copy.deepcopy(target)
        selected = next((node for node in walk(mutant["blocks"]) if node.get("t") == "Link" and
                         ("Link", rendition.normalize_target(node["c"][2][0], entry["rendition"]["path"],
                                                              mapping, language, peer_maps)) in new_links), None)
        require(selected is not None, "NEW_REFERENCE_CONTROL_UNAVAILABLE", label)
        href = selected["c"][2][0]
        selected["t"], selected["c"] = "Span", [["", [], []], selected["c"][1]]
        rejected(label + ": omit new reference " + href, "RENDITION_REFERENCE_DROPPED",
                 lambda: rendition.check_parity(entry, source, mutant, peer_maps=peer_maps))
        records.append({
            "work": work, "language": language, "source_sha256": entry["source"]["sha256"],
            "source_git_blob": git(root, "rev-parse", ENGLISH + ":" + source_path).decode().strip(),
            "rendition_sha256": entry["rendition"]["sha256"],
            "rendition_git_blob": git(root, "rev-parse", entry["rendition"]["revision"] + ":" + entry["rendition"]["path"]).decode().strip(),
            "mapped_sections": len(entry["sections"]), "new_source_sections": new_sections,
            "top_level_blocks": len(target["blocks"]), "math_objects": len(source_facts["formulas"]),
            "retained_locale_notice": retained_notice,
            "code_objects": len(source_facts["code"]), "references": sum(source_facts["references"].values()),
            "distinct_references": len(source_facts["references"]), "notes": source_facts["notes"],
        })
    require(len(records) == 10, "CHECKED_BODY_INVENTORY")
    return records, controls


def formula_coverage_regression(root, manifest, documents, formula_module):
    old_revision = "5827cd29b7833b4b4e4a1d1736effb81c76f36fa"
    relative = "papers/constrained-transformations/PAPER.md"
    descriptor = (root / "publication-formula-localizations.json").resolve()
    original_read = Path.read_bytes

    def committed(revision, path):
        return subprocess.check_output(["git", "-C", str(root), "show", revision + ":" + path])

    def require(condition, reason):
        if not condition:
            raise ValueError("FORMULA_COVERAGE_REGRESSION: " + reason)

    old_descriptor = committed(old_revision, descriptor.name)
    for doc in documents:
        raw = original_read(root / doc["path"])
        require(raw == committed(old_revision, doc["path"]), "canonical bytes changed: " + doc["path"])
        require(sha256(raw).hexdigest() == doc["sha256"], "document digest changed")

    def historical_descriptor_only(path):
        return old_descriptor if path.resolve() == descriptor else original_read(path)

    # Only this file read is injected; constructor Git reads still verify real C.
    with patch.object(Path, "read_bytes", historical_descriptor_only):
        historical = formula_module.FormulaLocalizations(root, dict(manifest, commit=old_revision), documents)
    require(relative not in historical.entries, "historical descriptor unexpectedly covers the source")
    current = formula_module.FormulaLocalizations(root, manifest, documents)
    require(relative in current.entries, "current descriptor does not cover the source")
    results = []
    for language in ("ru", "zh-Hans"):
        target = "translations/" + language + "/" + relative
        raw = original_read(root / target)
        require(raw == committed(old_revision, target) == committed(manifest["commit"], target), "target bytes changed")
        _, parts = formula_module.source_math(root, target)
        html = "".join(part["raw"] for part in parts)
        localized = current.localize(relative, language, html)
        current.validate_localized(relative, language, localized)
        require(localized != html, "positive control did not localize actual mtext")
        try:
            historical.localize(relative, language, html)
        except ValueError as error:
            expected = "FORMULA_LOCALIZATION_COVERAGE: localized reader has nonempty mtext without a source-bound descriptor: " + relative
            require(str(error) == expected, "wrong refusal: " + str(error))
        else:
            raise ValueError("FORMULA_COVERAGE_REGRESSION: missing descriptor was accepted")
        results.append({"language": language, "formula_objects": len(parts), "positive": "localized and validated",
                        "refusal": "FORMULA_LOCALIZATION_COVERAGE", "rendition_sha256": sha256(raw).hexdigest()})
    return {"name": "restore exact historical formula descriptor", "historical_commit": old_revision,
            "injection": "only descriptor Path.read_bytes; real Git/ancestry, canonical bytes and target bytes unchanged",
            "historical_descriptor_sha256": sha256(old_descriptor).hexdigest(), "locales": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--site-repository", type=Path, required=True)
    parser.add_argument("--pandoc", default="pandoc")
    args = parser.parse_args()
    if not __debug__:
        parser.error("optimized Python is unsupported: the pinned external consumer uses assertions")
    root, site = args.repository.resolve(), args.site_repository.resolve()
    modules, checker_hashes, pandoc = load_checker(site, args.pandoc)
    current = git(root, "rev-parse", "HEAD").decode().strip()
    ancestor(root, BASELINE, current)
    ancestor(root, ENGLISH, current)
    history = preserve_history(root, current)
    manifest, documents, entries, previous, content_revision, metadata = inventory(root, current, modules)
    presentation = presentation_scope(root, current)
    bodies, controls = check_bodies(root, manifest, documents, entries, previous, modules)
    with tempfile.TemporaryDirectory(prefix="kc-source-currency-render-") as directory:
        renderer = modules["build_publication"].Renderer(root, Path(directory), manifest, documents)
        compiled = modules["renditions"].compile_renditions(root, manifest, documents, renderer, modules["build_publication"].run)
        require(compiled is not None and len(compiled.entries) == 72, "COMPILED_INVENTORY")
        states = Counter(entry["state"] for entry in compiled.entries)
        require(states["missing"] == 4 and states["stale"] == 0, "COMPILED_SOURCE_CURRENCY", repr(states))
        for work, language in sorted(UPDATED | EDITORIAL):
            record = compiled.for_work(work)[language]
            require(record["state"] == "unreviewed" and record["review"] is None and bool(record.get("html")),
                    "COMPILED_UPDATED_BODY", work + "/" + language)
        formula_provenance = renderer.formula_localizations.provenance()
        review_provenance = renderer.review_localizations.provenance()
        require(formula_provenance is not None and review_provenance is not None, "PRESENTATION_NOT_EXECUTED")
    controls.append(formula_coverage_regression(root, manifest, documents, modules["formula_localization"]))
    print(json.dumps({
        "schema_version": 1, "result": "PASS", "scope": "bounded author structural and actual rendition-consumer validation",
        "baseline_revision": BASELINE, "english_revision": ENGLISH, "publication_revision": current,
        "content_revision_from_ten_entries": content_revision, "site_revision": SITE, "pandoc": pandoc,
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(), "site_script_sha256": checker_hashes,
        "rendition_entries": 68, "unchanged_entries": 56, "updated_pairs": 10,
        "editorial_pairs": 2, "editorial_work_language_pairs": [list(pair) for pair in sorted(EDITORIAL)],
        "editorial_content_revision": EDITORIAL_CONTENT,
        "current_source_mismatches": 0, "missing_pairs": [list(pair) for pair in sorted(MISSING)],
        "metadata_records": len(metadata["provenance"]["entries"]), "metadata_bytes_unchanged": True,
        "historical_review_objects_unchanged": 8, "compiled_states": dict(sorted(states.items())),
        "presentation_bindings": presentation, "actual_formula_localization": formula_provenance,
        "actual_review_localization": review_provenance, "bodies": bodies,
        "adverse_controls_detected": len(controls), "adverse_controls": controls,
        "retained_producer_files_unchanged": history,
        "limitations": [
            "No independent linguistic fidelity or scientific review is conferred.",
            "Structural completeness, exact formulas/code/links and source currency do not establish semantic equivalence of prose.",
            "This executes the real rendition and presentation consumers, not the full site build, release workflow or deployment.",
            "Historical producer files are verified unchanged; their execution remains separately reported at the appropriate revision.",
        ],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (Refusal, ValueError, OSError, subprocess.SubprocessError) as error:
        print(json.dumps({"result": "FAIL", "reason": str(error)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
