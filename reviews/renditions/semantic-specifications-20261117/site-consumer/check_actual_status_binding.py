#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Three temporary actual-page counterexamples for same-status work masking."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, required=True)
    args = parser.parse_args()
    site = args.site_dir.resolve()
    sys.path.insert(0, str(site / "scripts"))
    from publication_checks import check_status_labels, STATUS_LABELS
    records = json.loads((site / "src/content/catalog.json").read_text())["records"]
    owner = next(r for r in records if r["id"] == "semantic-verification")
    target = next(r for r in records if r["id"] == "geometry-of-semantic-representations")
    require(owner["status"] == target["status"] == "research-draft", "Actual same-status premise changed")
    results = []
    with tempfile.TemporaryDirectory(prefix="kc-actual-status-") as directory:
        output = Path(directory)
        originals = {}
        for locale in ("en", "ru", "zh-Hans"):
            route = owner["route"].replace("/en/", "/" + locale + "/", 1)
            relative = route.strip("/") + "/index.html"
            raw = (site / "public" / relative).read_bytes()
            target_file = output / relative
            target_file.parent.mkdir(parents=True)
            target_file.write_bytes(raw)
            originals[locale] = (relative, raw)
        require(check_status_labels(output, records) == 3, "Actual positive control must pass in all locales")
        for locale, (relative, original) in originals.items():
            text = original.decode("utf-8")
            label = STATUS_LABELS[target["status"]][locale]
            wrapper = f'<span lang="{locale}" data-work-status="{target["id"]}"><span class="status-badge">{label}</span></span>'
            require(text.count(wrapper) == 1, "Mutation must remove exactly one target binding")
            mutated = text.replace(wrapper, "", 1)
            require(f'data-work-status="{owner["id"]}"' in mutated, "Owner badge must remain")
            href = target["route"].replace("/en/", "/" + locale + "/", 1) + "#proposition-2-recoverability-requires-agreement-on-representation-fibres"
            require(f'href="{href}"' in mutated, "Actual fragment link must remain")
            (output / relative).write_text(mutated)
            try:
                check_status_labels(output, records)
            except ValueError as error:
                refusal = str(error)
                require("shows geometry-of-semantic-representations" in refusal and "without the label" in refusal, "Wrong refusal")
            else:
                raise ValueError("The actual same-status mutation survived")
            results.append({"locale": locale, "route": "/" + relative.removesuffix("index.html"), "original_sha256": sha256(original).hexdigest(), "mutant_sha256": sha256(mutated.encode()).hexdigest(), "target_wrappers_removed": 1, "own_same_status_badge_preserved": True, "fragment_link_preserved": True, "refusal": refusal})
            (output / relative).write_bytes(original)
            require((site / "public" / relative).read_bytes() == original, "Retained generated page changed")
    print(json.dumps({"schema": "kc-actual-status-binding-control/v1", "scope": "same-controller actual generated-page counterexamples; no release or review admission", "checked_at_utc": datetime.now(timezone.utc).isoformat(), "positive_pages": 3, "mutants_refused": len(results), "checker_sha256": sha256((site / "scripts/publication_checks.py").read_bytes()).hexdigest(), "cases": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
