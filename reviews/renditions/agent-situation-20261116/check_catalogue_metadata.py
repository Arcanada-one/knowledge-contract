# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Replay the actual catalogue-localization consumer on a pinned source update.

Checks metadata and retained byte/ancestry inventory only. A successful result
does not admit a manuscript, refresh an old rendition's source currency, build
a site, or establish serving.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

SOURCE = "8c7cd3bc1247998cb9554c568da26949da31b749"
BASE = "89382a5fa70d361ab906d44c7c4ea2b6ea28bc83"
SITE = "d3d17929f209612669f38db6a735d46bc9ec309c"
CHECKERS = {
    "catalogue_localization.py": "c706733199081cbe9d2781db783ab867d28c95a0f748cb0490b93cce3ac786fe",
    "renditions.py": "dca34612d0714cc40dc9001f2953a7c1f0b73af7a47ae2feb6b38d48d85c5d2f",
}
NEW_WORKS = {"agent-situation", "semantic-bridge", "semantic-verification",
             "agent-situation-controls", "semantic-bridge-conformance"}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--site-repository", type=Path, required=True)
    args = parser.parse_args()
    repo, site = args.repository.resolve(), args.site_repository.resolve()
    for filename, digest in CHECKERS.items():
        raw = (site / "scripts" / filename).read_bytes()
        require(raw == git(site, "show", SITE + ":scripts/" + filename), "CHECKER_BYTES")
        require(hashlib.sha256(raw).hexdigest() == digest, "CHECKER_HASH")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(site / "scripts"))
    consumer = importlib.import_module("catalogue_localization")
    require(Path(consumer.__file__).resolve() == site / "scripts/catalogue_localization.py",
            "CONSUMER_PATH")
    catalog_raw = (repo / "publication-catalog.json").read_bytes()
    require(catalog_raw == git(repo, "show", SOURCE + ":publication-catalog.json"), "CATALOGUE_PIN")
    catalog = json.loads(catalog_raw)
    documents = []
    for doc in catalog["documents"]:
        raw = (repo / doc["path"]).read_bytes()
        require(raw == git(repo, "show", SOURCE + ":" + doc["path"]), "SOURCE_PIN:" + doc["path"])
        documents.append(dict(doc, sha256=hashlib.sha256(raw).hexdigest()))
    path = repo / "publication-localization.json"
    raw = path.read_bytes()
    current = json.loads(raw)
    baseline = json.loads(git(repo, "show", BASE + ":publication-localization.json"))
    old_catalog = json.loads(git(repo, "show", baseline["source"]["revision"] + ":publication-catalog.json"))
    before = {d["slug"]: d for d in old_catalog["documents"]}
    after = {d["slug"]: d for d in documents}
    require(len(before) == 31 and len(after) == 36 and set(after) - set(before) == NEW_WORKS,
            "CATALOGUE_POPULATION")
    for work, old in before.items():
        require(old == {k: v for k, v in after[work].items() if k != "sha256"},
                "OLD_CATALOGUE_DESCRIPTION_CHANGED:" + work)
    require(len(baseline["entries"]) == 62 and len(current["entries"]) == 72,
            "METADATA_POPULATION")
    by_key = {(e["work"], e["language"]): e for e in current["entries"]}
    require(len(by_key) == 72, "METADATA_DUPLICATE")
    rebound = []
    for old in baseline["entries"]:
        key = old["work"], old["language"]
        now = by_key[key]
        require({k: v for k, v in old.items() if k != "source_sha256"} ==
                {k: v for k, v in now.items() if k != "source_sha256"},
                "HISTORICAL_METADATA_PROSE_OR_STATUS_CHANGED")
        if old["source_sha256"] != now["source_sha256"]:
            rebound.append({"work": key[0], "language": key[1]})
    require(len(rebound) == 10, "REBOUND_METADATA_POPULATION")
    manifest = {"commit": git(repo, "rev-parse", "HEAD").decode().strip(),
                "catalog": "publication-catalog.json"}
    positive = consumer.compile_localization(repo, manifest, documents)
    require(set(positive["records"]) == set(after), "COMPILED_WORK_POPULATION")
    require(sum(len(v) for v in positive["records"].values()) == 72, "COMPILED_LOCALE_POPULATION")

    # Registration, source currency and review are separate inventories. Retain
    # every old entry; a metadata rebind must not refresh an old body or review.
    rendition = importlib.import_module("renditions")
    registry = json.loads((repo / "publication-renditions.json").read_bytes())
    entries = rendition.validate_sidecar(registry, {"edition": catalog["edition"]})
    old_entries = json.loads(git(repo, "show", BASE + ":publication-renditions.json"))["renditions"]
    require(len(old_entries) == 66 and len(entries) == 68 and entries[:66] == old_entries,
            "RETAINED_RENDITION_ENTRIES_CHANGED")
    require({(e["work"], e["language"]) for e in entries[66:]} ==
            {("agent-situation", "ru"), ("agent-situation", "zh-Hans")}, "NEW_RENDITION_POPULATION")
    require(all("review" not in e for e in entries[66:]), "NEW_RENDITION_REVIEW_INVENTED")
    changed_source = []
    for entry in entries:
        for label in ("source", "rendition"):
            rendition.verify_pin(repo, manifest, entry["work"] + ":" + label,
                                 entry[label], "RENDITION_" + label.upper() + "_PIN")
        require(hashlib.sha256((repo / entry["rendition"]["path"]).read_bytes()).hexdigest() ==
                entry["rendition"]["sha256"], "RENDITION_CURRENT_BYTES")
        if entry["source"]["sha256"] != after[entry["work"]]["sha256"]:
            changed_source.append({"work": entry["work"], "language": entry["language"],
                                   "retained_source_sha256": entry["source"]["sha256"],
                                   "current_source_sha256": after[entry["work"]]["sha256"]})
    require(len(changed_source) == 10, "SOURCE_CURRENCY_POPULATION")
    missing = sorted({(work, lang) for work in after for lang in ("ru", "zh-Hans")} -
                     {(e["work"], e["language"]) for e in entries})
    require(len(missing) == 4, "MISSING_RENDITION_POPULATION")

    # Inject only the sidecar bytes into the real consumer. Git ancestry and all
    # English source reads stay real; the working tree is never rewritten.
    original_read = Path.read_bytes

    def expect_refusal(label, data, expected):
        payload = json.dumps(data, ensure_ascii=False).encode()
        def read(self):
            return payload if self.resolve() == path else original_read(self)
        with patch.object(Path, "read_bytes", read):
            try:
                consumer.compile_localization(repo, manifest, documents)
            except ValueError as error:
                require(str(error) == "LOCALIZATION_INVALID: " + expected,
                        "UNEXPECTED_REFUSAL:" + label + ":" + str(error))
                return {"case": label, "refusal": str(error)}
        raise ValueError("COUNTEREXAMPLE_ACCEPTED:" + label)

    observations = [expect_refusal("original-31-work-sidecar", baseline,
                                  "catalogue localization is stale for the current catalogue")]
    binding_only = copy.deepcopy(baseline)
    binding_only["source"] = current["source"]
    observations.append(expect_refusal("catalogue-pin-only-repair", binding_only,
                                      "metadata source bytes are stale or inconsistent"))
    no_new = copy.deepcopy(current)
    no_new["entries"] = [e for e in no_new["entries"] if e["work"] not in NEW_WORKS]
    observations.append(expect_refusal("missing-five-work-translations", no_new,
                                      "incomplete catalogue work/language inventory"))
    missing_one = copy.deepcopy(current)
    missing_one["entries"] = [e for e in missing_one["entries"]
                              if (e["work"], e["language"]) != ("agent-situation", "zh-Hans")]
    observations.append(expect_refusal("missing-agent-situation-chinese", missing_one,
                                      "incomplete catalogue work/language inventory"))
    for label, field, value, expected in (
        ("wrong-source-bytes", "source_sha256", "0" * 64, "metadata source bytes are stale or inconsistent"),
        ("english-title-fallback", "title", "Agent Situation", "title/summary does not match the declared language"),
        ("fabricated-review", "status", "reviewed", "schema 1 does not confer reviewed metadata status"),
    ):
        altered = copy.deepcopy(current)
        next(e for e in altered["entries"] if (e["work"], e["language"]) == ("agent-situation", "ru"))[field] = value
        observations.append(expect_refusal(label, altered, expected))
    duplicate = copy.deepcopy(current)
    duplicate["entries"].append(copy.deepcopy(duplicate["entries"][-1]))
    observations.append(expect_refusal("duplicate-work-language", duplicate,
                                      "duplicate work/language entry"))
    print(json.dumps({
        "source_commit": SOURCE, "baseline_candidate_commit": BASE, "site_checker_commit": SITE,
        "metadata_sha256": hashlib.sha256(raw).hexdigest(), "english_works": 36,
        "compiled_metadata_entries": 72, "new_metadata_entries": 10,
        "historical_prose_records_preserved": 62, "metadata_source_rebindings": rebound,
        "rendition_inventory": {
            "registered_bodies": 68, "retained_previous_entries": 66,
            "historical_review_objects_preserved": sum("review" in e for e in old_entries),
            "body_pins_and_current_bytes_verified": 68,
            "source_digest_matches_current": 58, "source_digest_differs": changed_source,
            "missing_work_language_pairs": missing,
            "scope": "byte/ancestry inventory; no renewed linguistic or scientific acceptance",
        },
        "refusal_observations": observations, "result": "PASS",
        "scope": "producer metadata integration only; manuscript fidelity, review, native admission and serving NOT_VERIFIED",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
