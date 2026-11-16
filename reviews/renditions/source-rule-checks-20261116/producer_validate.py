# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Bounded author checks for Source Rule Checks RU/zh-Hans renditions.

Uses the pinned site's actual Markdown parser and rendition parity check with
Pandoc 3.1.3. Writes only a JSON observation to stdout; no semantic verdict,
scientific experiment, review admission, site build or deployment is performed.
Adapted from reviews/renditions/context-controls-20261116/producer_validate.py.
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
SOURCE_PATH = "engineering/studies/semantic-bridge-conformance/STUDY.md"
SOURCE_BLOB = "a08166d551ca43c7e2e203d9408604ec43bd4799"
SOURCE_SHA256 = "4df280692b0fd5f591f4098f4f1fa68a837a4c606e6e9dc481b0b12ef2a3f612"
SOURCE_REVIEW_STATE = "internally-reviewed; external independence not verified"
SITE_COMMIT = "d3d17929f209612669f38db6a735d46bc9ec309c"
CHECKER_HASHES = {
    "renditions.py": "dca34612d0714cc40dc9001f2953a7c1f0b73af7a47ae2feb6b38d48d85c5d2f",
    "rendition_preamble.py": "163434ad6ba70de4773e4b672915b838b0b005bddc130f33fd08c4851bd7d073",
    "build_publication.py": "20ffe44a5d873bef16750a2eeca8fa0cd4dc4a7af62c01f2e55410da8a0e87e5",
}
# Independently recorded from the pinned English source, not from the targets.
HEADINGS = (
    "question-and-result", "materials-operation-and-assumptions",
    "independent-expected-result-method", "original-source-examples-and-actual-cli-use",
    "connection-to-algebra-and-geometry", "resolved-input-failure-and-review-boundary",
    "reproduction-and-interpretation",
)
BLOCKS = (
    "Header", "Header", "Para", "Para", "Para", "Header", "Para", "Para", "Para",
    "Header", "Para", "Para", "Table", "Para", "Header", "Para", "Para", "Table",
    "Para", "Header", "Para", "Para", "Para", "Para", "Para", "Header", "Para",
    "Para", "Para", "Header", "Para", "CodeBlock", "Para", "Para", "Para",
)
EXPECTED_COUNTS = {"sections": 7, "blocks": 35, "table_rows": [5, 5],
                   "table_cells": [[3] * 5, [3] * 5], "code_objects": 34,
                   "math_objects": 0, "references": 19, "distinct_references": 18,
                   "notes": 0}
MUTATIONS = (
    ("missing-section", "RENDITION_SECTION_UNRESOLVED"),
    ("missing-reference", "RENDITION_REFERENCE_DROPPED"),
    ("missing-table-row", "TABLE_SHAPE"),
    ("changed-command", "RENDITION_CODE_CHANGED"),
    ("changed-result-16384-to-16385", "NUMBERS_PER_BLOCK"),
    ("wrong-source-commit", "METADATA_SOURCE_COMMIT"),
    ("invented-review", "METADATA_REVIEW_STATE"),
)
# Only decimal digit tokens and three-digit comma/space grouping are compared.
# This accommodates "16,384" / "16 384"; it does not interpret written numerals.
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


def rows(table):
    c = table["c"]
    return c[3][1] + [row for group in c[4] for row in group[2] + group[3]] + c[5][1]


def table_signature(ast):
    return [[[(cell[2], cell[3]) for cell in row[1]] for row in rows(block)]
            for block in ast["blocks"] if block["t"] == "Table"]


def numbers(value):
    text = " ".join(n["c"] for n in walk(value) if n.get("t") == "Str")
    return Counter(re.sub(r"[, \u00a0\u202f]", "", token) for token in NUMBER.findall(text))


def counts(ast, facts, rendition):
    tables = [block for block in ast["blocks"] if block["t"] == "Table"]
    return {"sections": len(rendition.sections_of(ast)[0]), "blocks": len(ast["blocks"]),
            "table_rows": [len(rows(table)) for table in tables],
            "table_cells": [[len(row[1]) for row in rows(table)] for table in tables],
            "code_objects": len(facts["code"]), "math_objects": len(facts["formulas"]),
            "references": sum(facts["references"].values()),
            "distinct_references": len(facts["references"]), "notes": facts["notes"]}


def mutate(target, name):
    changed = copy.deepcopy(target)
    if name == "missing-section":
        changed["blocks"] = [b for b in changed["blocks"] if not
                             (b["t"] == "Header" and b["c"][1][0] == HEADINGS[-1])]
    elif name == "missing-reference":
        node = next(n for n in walk(changed["blocks"]) if n.get("t") == "Link")
        node.clear()
        node.update({"t": "Str", "c": "removed"})
    elif name == "missing-table-row":
        next(b for b in changed["blocks"] if b["t"] == "Table")["c"][4][0][3].pop()
    elif name == "changed-command":
        node = next(b for b in changed["blocks"] if b["t"] == "CodeBlock")
        node["c"][1] = node["c"][1].replace("python3 -B", "python3 -O", 1)
    elif name == "changed-result-16384-to-16385":
        block = changed["blocks"][3]
        before = numbers(block)
        require(before["16384"] == 1, "NUMBER_MUTATION_SUBJECT")
        for node in walk(block):
            if node.get("t") == "Str":
                replaced = re.sub(r"(?<!\d)16384(?!\d)", "16385", node["c"], count=1)
                if replaced == node["c"]:
                    replaced = re.sub(r"(?<!\d)384(?!\d)", "385", node["c"], count=1)
                if replaced != node["c"]:
                    node["c"] = replaced
                    break
        require(numbers(block) == before - Counter({"16384": 1}) + Counter({"16385": 1}),
                "NUMBER_MUTATION_NOT_APPLIED")
    else:
        require(name in {"wrong-source-commit", "invented-review"}, "UNKNOWN_MUTATION")
        field, value = (("source_commit", "0" * 40) if name == "wrong-source-commit"
                        else ("review_state", "reviewed"))
        changed["meta"][field] = {"t": "MetaString", "c": value}
    require(changed != target, "MUTATION_NOT_APPLIED:" + name)
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--site-repository", type=Path, required=True)
    parser.add_argument("--pandoc", required=True)
    args = parser.parse_args()
    if not __debug__:
        parser.error("optimized Python is not a supported execution mode")
    repo, site = args.repository.resolve(), args.site_repository.resolve()
    # which handles both a PATH command name and an explicit executable path.
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
    for module in (rendition, publication):
        require(Path(module.__file__).resolve() == site / "scripts" / (module.__name__ + ".py"),
                "SITE_MODULE_PATH")

    source_bytes = (repo / SOURCE_PATH).read_bytes()
    retained_source = subprocess.check_output(["git", "show", f"{SOURCE_COMMIT}:{SOURCE_PATH}"], cwd=repo)
    require(source_bytes == retained_source, "SOURCE_BYTES")
    require(hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256, "SOURCE_SHA256")
    blob = hashlib.sha1(b"blob " + str(len(source_bytes)).encode() + b"\0" + source_bytes).hexdigest()
    require(blob == SOURCE_BLOB, "SOURCE_GIT_BLOB")
    source_ast = publication.parse_markdown(repo / SOURCE_PATH)
    require(rendition.meta_value(source_ast, "review_state") == SOURCE_REVIEW_STATE, "SOURCE_REVIEW_STATE")
    require(rendition.sections_of(source_ast)[0] == [(2, anchor) for anchor in HEADINGS], "SOURCE_HEADINGS")
    require(tuple(b["t"] for b in source_ast["blocks"]) == BLOCKS, "SOURCE_BLOCK_SEQUENCE")
    source_facts = rendition.facts(source_ast, SOURCE_PATH, {anchor: anchor for anchor in HEADINGS})
    require(counts(source_ast, source_facts, rendition) == EXPECTED_COUNTS, "SOURCE_INVENTORY")
    source_pin = {"path": SOURCE_PATH, "sha256": SOURCE_SHA256, "revision": SOURCE_COMMIT}
    repository_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    manifest = {"commit": repository_head}
    rendition.verify_pin(repo, manifest, "Source Rule Checks source", source_pin, "RENDITION_SOURCE_PIN")

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
    for language in ("ru", "zh-Hans"):
        path = f"translations/{language}/{SOURCE_PATH}"
        target = publication.parse_markdown(repo / path)
        entry = {"work": "semantic-bridge-conformance", "language": language,
                 "source": {"path": SOURCE_PATH}, "rendition": {"path": path},
                 "sections": [{"source": anchor, "rendition": anchor} for anchor in HEADINGS]}

        def check(candidate):
            required = {"name": "semantic-bridge-conformance", "artifact": "engineering-study",
                        "edition": "1.1", "study_type": "finite-implementation-evaluation",
                        "author": "Pavel Valentov", "license": "CC-BY-4.0", "language": language,
                        "translation_of": SOURCE_PATH, "source_commit": SOURCE_COMMIT,
                        "source_git_blob": SOURCE_BLOB, "translation_status": "author-draft",
                        "review_state": "unreviewed", "source_review_state": SOURCE_REVIEW_STATE}
            for field, expected in required.items():
                require(rendition.meta_value(candidate, field) == expected, "METADATA_" + field.upper())
            mapping = rendition.check_parity(entry, source_ast, candidate)
            require(tuple(b["t"] for b in candidate["blocks"]) == BLOCKS, "BLOCK_SEQUENCE")
            require(table_signature(candidate) == table_signature(source_ast), "TABLE_SHAPE")
            for first, second in zip(source_ast["blocks"], candidate["blocks"]):
                require(numbers(first) == numbers(second), "NUMBERS_PER_BLOCK")
                if first["t"] == "Table":
                    for source_row, target_row in zip(rows(first), rows(second)):
                        for source_cell, target_cell in zip(source_row[1], target_row[1]):
                            require(numbers(source_cell[4]) == numbers(target_cell[4]), "NUMBERS_PER_CELL")
            require(rendition.script_matches(language, rendition.body_text(candidate)), "TARGET_SCRIPT")
            facts = rendition.facts(candidate, path, mapping, language)
            require(counts(candidate, facts, rendition) == EXPECTED_COUNTS, "TARGET_INVENTORY")
            for kind, reference in facts["references"]:
                resolved = (repo / reference.split("#")[0]).resolve()
                require(kind == "Link" and resolved.is_relative_to(repo) and resolved.is_file(), "REFERENCE_PATH")
            return facts

        facts = check(target)
        require(len(MUTATIONS) == 7 and len({name for name, _ in MUTATIONS}) == 7, "MUTATION_INVENTORY")
        adverse = []
        for name, expected in MUTATIONS:
            candidate = mutate(target, name)
            adverse.append(expect_refusal(lambda: check(candidate), expected, name))
        data = (repo / path).read_bytes()
        results.append({"language": language, "path": path, "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest(),
                        "counts": counts(target, facts, rendition), "adverse_controls": adverse})
    negative_count = 1 + sum(len(result["adverse_controls"]) for result in results)
    require(len(results) == 2 and negative_count == 15, "ADVERSE_CONTROL_INVENTORY")
    print(json.dumps({"result": "AUTHOR_STRUCTURE_AND_BINDING_PASS", "pandoc": version,
                      "parser": "build_publication.parse_markdown", "source": source_pin,
                      "source_blob": SOURCE_BLOB, "source_review_state": SOURCE_REVIEW_STATE,
                      "repository_head": repository_head, "site_checker_commit": SITE_COMMIT,
                      "checker_hashes": CHECKER_HASHES, "expected_counts": EXPECTED_COUNTS,
                      "source_digest_negative": source_negative, "targets": results,
                      "negative_controls_detected": negative_count,
                      "limits": ["Producer structural parity is not semantic equivalence or independent review.",
                                 "Digit tokens preserve multiplicity per block/cell, not order or written numerals; comma/space thousands grouping is normalized.",
                                 "Source evidence counts are translated, not rerun as new scientific tests.",
                                 "No rendition registration, review admission, site build, deployment, index result or native KC2 authority."]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Refusal as error:
        print(json.dumps({"result": "AUTHOR_CHECK_REFUSED", "code": str(error)}), file=sys.stderr)
        raise SystemExit(1) from error
