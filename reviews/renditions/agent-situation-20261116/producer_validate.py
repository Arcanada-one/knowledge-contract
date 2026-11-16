# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Bounded author structural checks for the Agent Situation RU/zh-Hans drafts.

Adapted from the retained Context Controls and Source Rule Checks producer
validators. Reuses the exact site's Markdown parser and rendition parity code.
Outputs JSON only. No source changes, semantic acceptance, native full build,
publication, deployment or scientific experiment is performed.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

SOURCE_COMMIT = "8c7cd3bc1247998cb9554c568da26949da31b749"
SOURCE_PATH = "papers/agent-situation/PAPER.md"
SOURCE_BLOB = "93a11fb3ad161a5ed3ed817636035ed0556a46fd"
SOURCE_SHA256 = "f04471d2b66bbb0d2ac64e41325bbd9367fd2f5d49f40bb90235beae2ff81677"
SITE_COMMIT = "d3d17929f209612669f38db6a735d46bc9ec309c"
CHECKER_HASHES = {
    "renditions.py": "dca34612d0714cc40dc9001f2953a7c1f0b73af7a47ae2feb6b38d48d85c5d2f",
    "rendition_preamble.py": "163434ad6ba70de4773e4b672915b838b0b005bddc130f33fd08c4851bd7d073",
    "build_publication.py": "20ffe44a5d873bef16750a2eeca8fa0cd4dc4a7af62c01f2e55410da8a0e87e5",
}
# Recorded from exact EN bytes with the actual site's GFM reader, before targets.
HEADINGS = (
    (1, "agent-situation-initialization-change-and-bounded-context"),
    (2, "abstract"),
    (2, "1-question-method-and-contribution"),
    (2, "2-foundations-and-nearest-prior-work"),
    (3, "21-situation-and-uncertainty"),
    (3, "22-robot-capabilities-partial-startup-and-feedback"),
    (3, "23-agent-memory-and-bounded-context"),
    (2, "3-objects-and-state-distinctions"),
    (2, "4-initialization-as-bounded-readiness"),
    (2, "5-change-refresh-and-candidate-intentions"),
    (3, "51-reconcile-observations-before-recomputing-everything"),
    (3, "52-refresh-is-an-allocation-problem"),
    (3, "53-proactivity-remains-a-separate-decision"),
    (2, "6-bounded-model-facing-context"),
    (2, "7-conditional-properties-and-counterexamples"),
    (2, "8-evaluation-programme-and-evidence-boundary"),
    (2, "9-limitations-and-development-decision"),
    (2, "references-and-source-scope"),
)
EXPECTED_COUNTS = {
    "headings": 18, "mapped_sections": 17, "top_level_blocks": 79,
    "para_nodes": 57, "plain_nodes": 92, "bullet_items": 5,
    "tables": 3, "table_rows_including_headers": [7, 14, 8],
    "table_cells_per_row": [[3] * 7, [3] * 14, [3] * 8],
    "math_objects": 16, "inline_math": 15, "display_math": 1,
    "code_objects": 0, "references": 32, "distinct_references": 31,
    "notes": 0, "source_ids": 22,
}
MUTATIONS = (
    ("missing-section", "RENDITION_SECTION_UNRESOLVED"),
    ("missing-paragraph", "BLOCK_SEQUENCE"),
    ("missing-table-row", "TABLE_SHAPE"),
    ("changed-budget-formula", "RENDITION_FORMULA_CHANGED"),
    ("source-relative-link-not-rebased", "RENDITION_LINK_TRANSLATION"),
    ("swapped-inventory-row-numbers", "NUMBERS_PER_CELL"),
    ("wrong-source-commit", "METADATA_SOURCE_COMMIT"),
)
NUMBER = re.compile(r"(?<!\d)(?:\d{1,3}(?:(?:,|[ \u00a0\u202f])\d{3})+|\d+(?:[./–-]\d+)*)(?!\d)")


class Refusal(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise Refusal(code)


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def headings(ast):
    return tuple((b["c"][0], b["c"][1][0]) for b in ast["blocks"] if b["t"] == "Header")


def rows(table):
    c = table["c"]
    return c[3][1] + [row for group in c[4] for row in group[2] + group[3]] + c[5][1]


def table_signature(ast):
    return [[[(cell[2], cell[3]) for cell in row[1]] for row in rows(block)]
            for block in ast["blocks"] if block["t"] == "Table"]


def block_shape(block):
    """Paragraph/list/cell boundaries; never infer equivalence from text length."""
    kind, content = block["t"], block.get("c")
    if kind in {"Para", "Plain"}:
        return kind
    if kind == "Header":
        return [kind, content[0]]
    if kind == "BulletList":
        return [kind, [[block_shape(b) for b in item] for item in content]]
    if kind == "Table":
        return [kind, len(content[2]), [block_shape(b) for b in content[1][1]],
                [[[cell[2], cell[3], [block_shape(b) for b in cell[4]]]
                  for cell in row[1]] for row in rows(block)]]
    raise Refusal("UNEXPECTED_BLOCK_KIND:" + kind)


def numbers(value):
    text = " ".join(n["c"] for n in walk(value) if n.get("t") == "Str")
    return Counter(re.sub(r"[, \u00a0\u202f]", "", token) for token in NUMBER.findall(text))


def counts(ast, facts, rendition):
    nodes = list(walk(ast["blocks"]))
    tables = [b for b in ast["blocks"] if b["t"] == "Table"]
    source_ids = ast.get("meta", {}).get("sources", {})
    return {
        "headings": len(headings(ast)), "mapped_sections": len(rendition.sections_of(ast)[0]),
        "top_level_blocks": len(ast["blocks"]),
        "para_nodes": sum(n.get("t") == "Para" for n in nodes),
        "plain_nodes": sum(n.get("t") == "Plain" for n in nodes),
        "bullet_items": sum(len(n["c"]) for n in nodes if n.get("t") == "BulletList"),
        "tables": len(tables), "table_rows_including_headers": [len(rows(t)) for t in tables],
        "table_cells_per_row": [[len(row[1]) for row in rows(t)] for t in tables],
        "math_objects": len(facts["formulas"]),
        "inline_math": sum(mode == "InlineMath" for mode, _ in facts["formulas"]),
        "display_math": sum(mode == "DisplayMath" for mode, _ in facts["formulas"]),
        "code_objects": len(facts["code"]), "references": sum(facts["references"].values()),
        "distinct_references": len(facts["references"]), "notes": facts["notes"],
        "source_ids": len(source_ids.get("c", [])) if source_ids.get("t") == "MetaList" else -1,
    }


def mutate(target, name):
    changed = copy.deepcopy(target)
    if name == "missing-section":
        changed["blocks"] = [b for b in changed["blocks"] if not
                             (b["t"] == "Header" and b["c"][1][0] == HEADINGS[-1][1])]
    elif name == "missing-paragraph":
        # First question-section paragraph contains no reference; the site allows
        # different text-block counts, so this probes the added paragraph guard.
        section = next(i for i, b in enumerate(changed["blocks"]) if b["t"] == "Header"
                       and b["c"][1][0] == "1-question-method-and-contribution")
        require(changed["blocks"][section + 1]["t"] == "Para", "PARAGRAPH_MUTATION_SUBJECT")
        changed["blocks"].pop(section + 1)
    elif name == "missing-table-row":
        next(b for b in changed["blocks"] if b["t"] == "Table")["c"][4][0][3].pop()
    elif name == "changed-budget-formula":
        node = next(n for n in walk(changed["blocks"]) if n.get("t") == "Math"
                    and n["c"][0]["t"] == "DisplayMath")
        require(r"+B_{\mathrm{margin}}" in node["c"][1], "FORMULA_MUTATION_SUBJECT")
        node["c"][1] = node["c"][1].replace(r"+B_{\mathrm{margin}}", "", 1)
    elif name == "source-relative-link-not-rebased":
        node = next(n for n in walk(changed["blocks"]) if n.get("t") == "Link"
                    and n["c"][2][0].endswith("LITERATURE.md"))
        node["c"][2][0] = "LITERATURE.md"
    elif name == "swapped-inventory-row-numbers":
        table = [b for b in changed["blocks"] if b["t"] == "Table"][1]
        first, second = rows(table)[1:3]
        a = next(n for n in walk(first[1][0][4]) if n.get("t") == "Str")
        b = next(n for n in walk(second[1][0][4]) if n.get("t") == "Str")
        require((a["c"], b["c"]) == ("1", "2"), "CELL_MUTATION_SUBJECT")
        a["c"], b["c"] = b["c"], a["c"]
    elif name == "wrong-source-commit":
        changed["meta"]["source_commit"] = {"t": "MetaString", "c": "0" * 40}
    else:
        raise Refusal("UNKNOWN_MUTATION:" + name)
    require(changed != target, "MUTATION_NOT_APPLIED:" + name)
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--site-repository", type=Path, required=True)
    parser.add_argument("--pandoc", required=True)
    parser.add_argument("--ru-path", type=Path, help="Optional staged candidate; logical path remains canonical")
    parser.add_argument("--zh-hans-path", type=Path, help="Optional staged candidate; logical path remains canonical")
    args = parser.parse_args()
    if not __debug__:
        parser.error("optimized Python is not a supported execution mode")
    repo, site = args.repository.resolve(), args.site_repository.resolve()
    selected = shutil.which(args.pandoc)
    require(selected is not None, "PANDOC_EXECUTABLE")
    pandoc = Path(selected).resolve()
    version = subprocess.check_output([str(pandoc), "--version"], text=True).splitlines()[0]
    require(version == "pandoc 3.1.3", "PANDOC_VERSION")
    os.environ["PATH"] = str(pandoc.parent) + os.pathsep + os.environ.get("PATH", "")
    require(Path(shutil.which("pandoc") or "").resolve() == pandoc, "PANDOC_EXECUTABLE")
    for filename, expected in CHECKER_HASHES.items():
        data = (site / "scripts" / filename).read_bytes()
        retained = subprocess.check_output(["git", "show", f"{SITE_COMMIT}:scripts/{filename}"], cwd=site)
        require(data == retained and hashlib.sha256(data).hexdigest() == expected, "SITE_CHECKER_PIN")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(site / "scripts"))
    rendition, publication = importlib.import_module("renditions"), importlib.import_module("build_publication")
    preamble = importlib.import_module("rendition_preamble")
    for module in (rendition, publication, preamble):
        require(Path(module.__file__).resolve() == site / "scripts" / (module.__name__ + ".py"), "SITE_MODULE_PATH")

    source_bytes = (repo / SOURCE_PATH).read_bytes()
    retained = subprocess.check_output(["git", "show", f"{SOURCE_COMMIT}:{SOURCE_PATH}"], cwd=repo)
    require(source_bytes == retained, "SOURCE_BYTES")
    require(hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256, "SOURCE_SHA256")
    source_blob = hashlib.sha1(b"blob " + str(len(source_bytes)).encode() + b"\0" + source_bytes).hexdigest()
    require(source_blob == SOURCE_BLOB, "SOURCE_GIT_BLOB")
    source_ast = publication.parse_markdown(repo / SOURCE_PATH)
    require(headings(source_ast) == HEADINGS, "SOURCE_HEADINGS")
    source_map = {anchor: anchor for _, anchor in HEADINGS}
    source_facts = rendition.facts(source_ast, SOURCE_PATH, source_map)
    require(counts(source_ast, source_facts, rendition) == EXPECTED_COUNTS, "SOURCE_INVENTORY")
    source_pin = {"path": SOURCE_PATH, "sha256": SOURCE_SHA256, "revision": SOURCE_COMMIT}
    repository_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    manifest = {"commit": repository_head}
    rendition.verify_pin(repo, manifest, "Agent Situation source", source_pin, "RENDITION_SOURCE_PIN")
    tree = rendition.tree_paths(repo, repository_head)
    documents = json.loads((repo / "publication-catalog.json").read_text())["documents"]
    by_path = {doc["path"]: doc for doc in documents}
    entries = json.loads((repo / "publication-renditions.json").read_text())["renditions"]
    peer_maps = {(e["language"], e["source"]["path"]):
                 {p["rendition"]: p["source"] for p in e["sections"]} for e in entries}

    def expect_refusal(operation, expected, label):
        try:
            operation()
        except (Refusal, rendition.RenditionError) as exc:
            code = exc.code if isinstance(exc, rendition.RenditionError) else str(exc)
            require(code == expected, "UNEXPECTED_REFUSAL:" + label + ":" + code)
            return {"mutation": label, "refusal": code}
        raise Refusal("MUTATION_ACCEPTED:" + label)

    source_negative = expect_refusal(
        lambda: rendition.verify_pin(repo, manifest, "wrong source digest",
                                     {**source_pin, "sha256": "0" * 64}, "RENDITION_SOURCE_PIN"),
        "RENDITION_SOURCE_PIN", "wrong-source-digest")
    results = []
    overrides = {"ru": args.ru_path, "zh-Hans": args.zh_hans_path}
    for language in ("ru", "zh-Hans"):
        logical_path = f"translations/{language}/{SOURCE_PATH}"
        physical = (overrides[language] or repo / logical_path).resolve()
        target = publication.parse_markdown(physical)
        pinned = frozenset(e["source"]["path"] for e in entries if e["language"] == language)
        entry = {"work": "agent-situation", "language": language,
                 "source": {"path": SOURCE_PATH}, "rendition": {"path": logical_path},
                 "sections": [{"source": anchor, "rendition": anchor}
                              for level, anchor in HEADINGS if level in {2, 3}]}

        def check(candidate):
            required = {"name": "agent-situation", "artifact": "scientific-paper", "edition": "1.1",
                        "author": "Pavel Valentov", "license": "CC-BY-4.0", "language": language,
                        "status": "research-draft", "translation_of": SOURCE_PATH,
                        "source_commit": SOURCE_COMMIT, "source_git_blob": SOURCE_BLOB,
                        "translation_status": "author-draft"}
            for field, expected in required.items():
                require(rendition.meta_value(candidate, field) == expected, "METADATA_" + field.upper())
            if "review_state" in candidate["meta"]:
                require(rendition.meta_value(candidate, "review_state") == "unreviewed", "METADATA_REVIEW_STATE")
            require(candidate["meta"].get("sources") == source_ast["meta"]["sources"], "SOURCE_IDS")
            for field in ("title", "short_title", "subtitle", "description"):
                value = rendition.meta_value(candidate, field)
                require(value and rendition.script_matches(language, value), "METADATA_" + field.upper())
            title = next(b for b in candidate["blocks"] if b["t"] == "Header" and b["c"][0] == 1)
            require(publication.plain(title["c"][2]) == rendition.meta_value(candidate, "title"), "TITLE_H1")

            link_results = []
            def link_check():
                link_results.extend(rendition.analyse_links(
                    candidate, logical_path, language, tree, by_path, pinned, source_map,
                    rendition.anchors_of(candidate), rendition.anchors_of(source_ast)))
            mapping = rendition.check_parity(entry, source_ast, candidate, before_references=link_check,
                                             peer_maps=peer_maps)
            require(headings(candidate) == HEADINGS, "EXACT_HEADING_ANCHORS")
            require([b["t"] for b in candidate["blocks"]] == [b["t"] for b in source_ast["blocks"]], "BLOCK_SEQUENCE")
            require(table_signature(candidate) == table_signature(source_ast), "TABLE_SHAPE")
            require([block_shape(b) for b in candidate["blocks"]] ==
                    [block_shape(b) for b in source_ast["blocks"]], "PARAGRAPH_LIST_CELL_SHAPE")
            for first, second in zip(source_ast["blocks"], candidate["blocks"]):
                require(numbers(first) == numbers(second), "NUMBERS_PER_BLOCK")
                if first["t"] == "Table":
                    for source_row, target_row in zip(rows(first), rows(second)):
                        for source_cell, target_cell in zip(source_row[1], target_row[1]):
                            require(numbers(source_cell[4]) == numbers(target_cell[4]), "NUMBERS_PER_CELL")
            require(rendition.script_matches(language, rendition.body_text(candidate)), "TARGET_SCRIPT")
            facts = rendition.facts(candidate, logical_path, mapping, language, peer_maps)
            require(counts(candidate, facts, rendition) == EXPECTED_COUNTS, "TARGET_INVENTORY")
            return facts, link_results

        facts, link_results = check(target)
        adverse = []
        for name, expected in MUTATIONS:
            candidate = mutate(target, name)
            adverse.append(expect_refusal(lambda: check(candidate), expected, name))
        data = physical.read_bytes()
        results.append({"language": language, "path": logical_path,
                        "input_mode": "staged-candidate" if overrides[language] else "repository-path",
                        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                        "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
                        "counts": counts(target, facts, rendition),
                        "link_classes": dict(Counter(kind for kind, _, _ in link_results)),
                        "adverse_controls": adverse})
    negative_count = 1 + sum(len(result["adverse_controls"]) for result in results)
    require(len(MUTATIONS) == 7 and len({name for name, _ in MUTATIONS}) == 7
            and len(results) == 2 and negative_count == 15, "ADVERSE_CONTROL_INVENTORY")
    print(json.dumps({"result": "AUTHOR_STRUCTURE_AND_BINDING_PASS", "pandoc": version,
                      "parser": "build_publication.parse_markdown (GFM identifiers)",
                      "source": source_pin, "source_blob": SOURCE_BLOB,
                      "source_status": "research-draft", "repository_head": repository_head,
                      "site_checker_commit": SITE_COMMIT, "checker_hashes": CHECKER_HASHES,
                      "expected_counts": EXPECTED_COUNTS, "source_digest_negative": source_negative,
                      "targets": results, "negative_controls_detected": negative_count,
                      "limits": [
                          "Producer structural parity is not semantic equivalence or independent review.",
                          "57 Pandoc Para nodes include one display-formula paragraph: 56 prose paragraphs; table row counts include headers.",
                          "Digit tokens preserve multiplicity per block/cell, not order or written numerals; grouping is normalized.",
                          "Matching paragraph boundaries cannot detect a lost negation, qualifier, clause or mistranslated claim.",
                          "Source bibliography and empirical claims are translated, not independently reverified or rerun.",
                          "No whole-sidecar validation, metadata migration, full site build, review admission, deployment or index admission.",
                      ]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(json.dumps({"result": "AUTHOR_CHECK_REFUSED", "code": getattr(error, "code", str(error))}), file=sys.stderr)
        raise SystemExit(1) from error
