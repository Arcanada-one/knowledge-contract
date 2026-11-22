# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Bounded author checks for two Context Controls renditions; no semantic verdict.

Run with the exact site checker from d3d17929f209612669f38db6a735d46bc9ec309c
and Pandoc 3.1.3. Prints a new JSON observation; does not rewrite retained evidence.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import importlib
import json
from pathlib import Path
import re
import subprocess
import sys

SOURCE_COMMIT = "8c7cd3bc1247998cb9554c568da26949da31b749"
SOURCE_PATH = "engineering/studies/agent-situation-controls/STUDY.md"
SOURCE_BLOB = "b875953c066fcbb99e1579f76dfcd29c5bc9ef9d"
SOURCE_SHA256 = "41b6fbf4392fa27be2269ccbfb73b1e9049aa9cb7784c7b295960e8336366e05"
SITE_COMMIT = "d3d17929f209612669f38db6a735d46bc9ec309c"
FORMAT = "markdown+gfm_auto_identifiers+pipe_tables+tex_math_dollars+tex_math_single_backslash+autolink_bare_uris"
CHECKER_HASHES = {
    "renditions.py": "dca34612d0714cc40dc9001f2953a7c1f0b73af7a47ae2feb6b38d48d85c5d2f",
    "rendition_preamble.py": "163434ad6ba70de4773e4b672915b838b0b005bddc130f33fd08c4851bd7d073",
}


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


def metadata(ast, field):
    node = ast.get("meta", {}).get(field, {})
    if node.get("t") == "MetaString":
        return node["c"]
    return " ".join(n["c"] for n in walk(node) if n.get("t") == "Str")


def rows(table):
    c = table["c"]
    return c[3][1] + [row for group in c[4] for row in group[2] + group[3]] + c[5][1]


def table_signature(ast):
    return [[[(cell[2], cell[3]) for cell in row[1]] for row in rows(block)]
            for block in ast["blocks"] if block["t"] == "Table"]


def digits(value):
    text = " ".join(n["c"] for n in walk(value) if n.get("t") == "Str")
    return Counter(re.findall(r"\d+(?:[./–-]\d+)*", text))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--site-repository", type=Path, required=True)
    parser.add_argument("--pandoc", required=True)
    args = parser.parse_args()
    if not __debug__:
        parser.error("optimized Python is not a supported execution mode")
    repo, site = args.repository.resolve(), args.site_repository.resolve()
    version = subprocess.check_output([args.pandoc, "--version"], text=True).splitlines()[0]
    require(version == "pandoc 3.1.3", "PANDOC_VERSION")
    for filename, expected in CHECKER_HASHES.items():
        data = (site / "scripts" / filename).read_bytes()
        retained = subprocess.check_output(["git", "show", f"{SITE_COMMIT}:scripts/{filename}"], cwd=site)
        require(data == retained and hashlib.sha256(data).hexdigest() == expected, "SITE_CHECKER_PIN")
    sys.path.insert(0, str(site / "scripts"))
    rendition = importlib.import_module("renditions")

    source_bytes = (repo / SOURCE_PATH).read_bytes()
    retained_source = subprocess.check_output(["git", "show", f"{SOURCE_COMMIT}:{SOURCE_PATH}"], cwd=repo)
    require(source_bytes == retained_source, "SOURCE_BYTES")
    require(hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256, "SOURCE_SHA256")
    git_blob = hashlib.sha1(b"blob " + str(len(source_bytes)).encode() + b"\0" + source_bytes).hexdigest()
    require(git_blob == SOURCE_BLOB, "SOURCE_GIT_BLOB")

    def ast(path):
        return json.loads(subprocess.check_output(
            [args.pandoc, str(repo / path), "--from=" + FORMAT, "--to=json"]))

    source_ast = ast(SOURCE_PATH)
    headings = rendition.sections_of(source_ast)[0]
    source_pin = {"path": SOURCE_PATH, "sha256": SOURCE_SHA256, "revision": SOURCE_COMMIT}
    rendition.verify_pin(repo, {"commit": SOURCE_COMMIT}, "Context Controls source", source_pin,
                         "RENDITION_SOURCE_PIN")
    wrong_source = {**source_pin, "sha256": "0" * 64}
    try:
        rendition.verify_pin(repo, {"commit": SOURCE_COMMIT}, "wrong source digest", wrong_source,
                             "RENDITION_SOURCE_PIN")
    except rendition.RenditionError as exc:
        require(exc.code == "RENDITION_SOURCE_PIN", "UNEXPECTED_SOURCE_REFUSAL")
        source_negative = exc.code
    else:
        raise Refusal("WRONG_SOURCE_DIGEST_ACCEPTED")

    results = []
    for language in ("ru", "zh-Hans"):
        path = f"translations/{language}/{SOURCE_PATH}"
        target = ast(path)
        entry = {
            "work": "agent-situation-controls", "language": language,
            "source": {"path": SOURCE_PATH}, "rendition": {"path": path},
            "sections": [{"source": identity, "rendition": identity} for _, identity in headings],
        }

        def check(candidate):
            required = {"translation_of": SOURCE_PATH, "source_commit": SOURCE_COMMIT,
                        "source_git_blob": SOURCE_BLOB, "translation_status": "author-draft",
                        "status": "research-draft", "language": language,
                        "author": "Pavel Valentov", "license": "CC-BY-4.0"}
            for key, expected in required.items():
                require(metadata(candidate, key) == expected, "METADATA_" + key.upper())
            mapping = rendition.check_parity(entry, source_ast, candidate)
            require([b["t"] for b in source_ast["blocks"]] == [b["t"] for b in candidate["blocks"]],
                    "BLOCK_SEQUENCE")
            require(table_signature(source_ast) == table_signature(candidate), "TABLE_SHAPE")
            for first, second in zip(source_ast["blocks"], candidate["blocks"]):
                require(digits(first) == digits(second), "NUMBERS_PER_BLOCK")
                if first["t"] == "Table":
                    for source_row, target_row in zip(rows(first), rows(second)):
                        for source_cell, target_cell in zip(source_row[1], target_row[1]):
                            require(digits(source_cell[4]) == digits(target_cell[4]), "NUMBERS_PER_CELL")
            require(rendition.script_matches(language, rendition.body_text(candidate)), "TARGET_SCRIPT")
            facts = rendition.facts(candidate, path, mapping, language)
            for kind, reference in facts["references"]:
                require(kind == "Link" and (repo / reference.split("#")[0]).is_file(), "REFERENCE_PATH")
            return facts

        facts = check(target)
        mutations = [
            ("missing-section", "RENDITION_SECTION_UNRESOLVED"),
            ("changed-command", "RENDITION_CODE_CHANGED"),
            ("missing-reference", "RENDITION_REFERENCE_DROPPED"),
            ("missing-table-row", "TABLE_SHAPE"),
            ("changed-result-number", "NUMBERS_PER_BLOCK"),
            ("wrong-source-commit", "METADATA_SOURCE_COMMIT"),
            ("invented-reviewed-status", "METADATA_TRANSLATION_STATUS"),
        ]
        observed = []
        for mutation, expected in mutations:
            changed = copy.deepcopy(target)
            if mutation == "missing-section":
                changed["blocks"] = [b for b in changed["blocks"] if not
                                     (b["t"] == "Header" and b["c"][1][0] == "5-results")]
            elif mutation == "changed-command":
                node = next(b for b in changed["blocks"] if b["t"] == "CodeBlock")
                node["c"][1] = node["c"][1].replace("python3 -B", "python3 -O", 1)
            elif mutation == "missing-reference":
                node = next(n for n in walk(changed["blocks"]) if n.get("t") == "Link")
                node.clear()
                node.update({"t": "Str", "c": "removed"})
            elif mutation == "missing-table-row":
                next(b for b in changed["blocks"] if b["t"] == "Table")["c"][4][0][3].pop()
            elif mutation == "changed-result-number":
                node = next(n for n in walk(changed["blocks"]) if n.get("t") == "Str" and
                            re.search(r"21/21", n.get("c", "")))
                node["c"] = node["c"].replace("21/21", "22/21", 1)
            else:
                field = "source_commit" if mutation == "wrong-source-commit" else "translation_status"
                value = "0" * 40 if mutation == "wrong-source-commit" else "reviewed"
                changed["meta"][field] = {"t": "MetaString", "c": value}
            try:
                check(changed)
            except (Refusal, rendition.RenditionError) as exc:
                code = exc.code if isinstance(exc, rendition.RenditionError) else str(exc)
                require(code == expected, "UNEXPECTED_MUTATION_REFUSAL:" + mutation + ":" + code)
                observed.append({"mutation": mutation, "refusal": code})
            else:
                raise Refusal("MUTATION_ACCEPTED:" + mutation)
        data = (repo / path).read_bytes()
        results.append({"language": language, "path": path, "sha256": hashlib.sha256(data).hexdigest(),
                        "bytes": len(data), "sections": len(headings), "blocks": len(target["blocks"]),
                        "table_rows_with_headers": [len(rows(b)) for b in target["blocks"] if b["t"] == "Table"],
                        "code_objects": len(facts["code"]), "references": sum(facts["references"].values()),
                        "adverse_controls": observed})
    negative_count = 1 + sum(len(result["adverse_controls"]) for result in results)
    require(len(results) == 2 and negative_count == 15, "ADVERSE_CONTROL_INVENTORY")
    print(json.dumps({"result": "AUTHOR_STRUCTURE_AND_BINDING_PASS", "pandoc": version, "format": FORMAT,
                      "source": source_pin, "source_blob": SOURCE_BLOB, "site_checker_commit": SITE_COMMIT,
                      "checker_hashes": CHECKER_HASHES, "source_digest_negative": source_negative,
                      "targets": results, "negative_controls_detected": negative_count,
                      "limits": ["Structural parity is not semantic equivalence or independent acceptance.",
                                 "Numeric order may change within a paragraph or cell for target-language syntax.",
                                 "No new model experiment, native admission, deployment or index result."]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
