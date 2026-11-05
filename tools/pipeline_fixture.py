#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Build the synthetic pipeline receipt chain and its negative variants (every byte invented for this repository).

`python3 tools/pipeline_fixture.py write` regenerates schemas/fixtures/pipeline/; the unit tests rebuild the same bytes in memory and fail if the
committed files drift. Each negative variant is a MUTANT of the valid chain: one change, one expected refusal code.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_pipeline_receipts as cpr  # noqa: E402

FIXTURE_ROOT = cpr.REPO / "schemas" / "fixtures" / "pipeline"
SOURCE_BYTES = b"Synthetic public-domain pamphlet, invented for this repository.\n"
SOURCE_SHA = hashlib.sha256(SOURCE_BYTES).hexdigest()
DOC = "d_" + SOURCE_SHA
TOOLS = {"intake": "doclab-intake", "classify": "doclab-classify", "convert": "conversion-arcana", "recognise": "doclab-ocr", "bundle": "doclab-bundle",
         "kc-package": "doclab-kc-export", "library": "library-submit", "publish": "contract-place-api", "index": "kb-feeder-kc-lane"}


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def artefact(stage: str, role: str) -> dict:
    return {"role": role, "sha256": sha(f"{DOC}:{stage}:{role}")}


OUT_ROLE = {"intake": "source_record", "classify": "classification", "convert": "converted_text", "recognise": "transcription", "bundle": "result_bundle",
            "kc-package": "book_package", "library": "library_entry", "publish": "allowlist_row", "index": "index_run"}


def valid_receipts() -> list[dict]:
    receipts, previous_out = [], None
    for n, stage in enumerate(cpr.STAGES):
        outputs = [artefact(stage, OUT_ROLE[stage])]
        inputs = [{"role": "source", "sha256": SOURCE_SHA}] if n == 0 else [dict(previous_out, role="previous_output")]
        receipts.append({
            "schema": "PipelineStageReceipt/v1", "document_id": DOC, "stage": stage, "run_id": f"run.{stage}.1", "previous_receipt_sha256": None,
            "tool": {"name": TOOLS[stage], "version": "0.0.0"}, "started_at": f"2026-11-05T10:{n:02d}:00Z", "finished_at": f"2026-11-05T10:{n:02d}:30Z",
            "outcome": "done", "rights_class": "unknown", "inputs": inputs, "outputs": outputs,
            "measurements": [{"name": "units_seen", "status": "measured", "value": 1}, {"name": "cer", "status": "not_measured", "reason": "no reference transcription"}],
            "kc2_admission": "not_measured"})
        previous_out = outputs[0]
    return receipts


def dump(record: dict) -> bytes:
    return (json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def link(receipts: list[dict]) -> dict[str, bytes]:
    """File name -> bytes, with every previous_receipt_sha256 set to the digest of the previous file's bytes."""
    out, previous = {}, None
    for n, record in enumerate(receipts):
        record = copy.deepcopy(record)
        record["previous_receipt_sha256"] = previous
        data = dump(record)
        out[f"{n + 1:02d}-{record['stage']}.json"] = data
        previous = hashlib.sha256(data).hexdigest()
    return out


def variants() -> dict[str, dict[str, bytes]]:
    base = valid_receipts()
    chains: dict[str, dict[str, bytes]] = {}

    def mutant(name: str, edit, relink: bool = True) -> None:
        rs = copy.deepcopy(base)
        edit(rs)
        chains[name] = link(rs) if relink else None  # type: ignore[assignment]
        if not relink:
            chains[name] = link(rs)

    chains["valid/synthetic-chain"] = link(base)

    native = copy.deepcopy(base)  # a format Doclab reads as it is: convert is skipped with its reason and recognise reads the source
    native[2].update(outcome="skipped", reason="the format is read as it is; no conversion is needed", inputs=[], outputs=[])
    native[3]["inputs"] = [{"role": "source", "sha256": SOURCE_SHA}]
    chains["valid/native-format-chain"] = link(native)

    both = copy.deepcopy(base)  # neither classified nor converted: recognise reads the source
    both[1].update(outcome="skipped", reason="no classification is wanted for this document", inputs=[], outputs=[])
    both[2].update(outcome="skipped", reason="the format is read as it is; no conversion is needed", inputs=[], outputs=[])
    both[3]["inputs"] = [{"role": "source", "sha256": SOURCE_SHA}]
    chains["valid/classify-and-convert-skipped"] = link(both)

    for n, stage in enumerate(cpr.STAGES):  # a chain may end at any stage with a refusal
        stopped = copy.deepcopy(base[: n + 1])
        stopped[n].update(outcome="refused", reason=f"{stage} refused this document", outputs=[])
        chains[f"valid/stopped-at-{stage}"] = link(stopped)
    mutant("invalid/id_changed", lambda rs: rs[4].update(document_id="d_" + "0" * 64))
    mutant("invalid/stage_missing", lambda rs: rs.pop(2))
    mutant("invalid/stage_repeated", lambda rs: rs.insert(3, copy.deepcopy(rs[2])))
    mutant("invalid/out_of_order", lambda rs: rs.__setitem__(slice(2, 4), [rs[3], rs[2]]))
    mutant("invalid/starts_at_classify", lambda rs: rs.pop(0))

    def widen(rs):
        rs[0]["rights_class"] = "third_party_restricted"
        rs[5]["rights_class"] = "author_open"
    mutant("invalid/rights_widened", widen)

    def consume_refused(rs):
        rs[3].update(outcome="refused", reason="conversion refused the file", outputs=[])
    mutant("invalid/consumed_after_refusal", consume_refused)

    def partial_output(rs):
        rs[3].update(outcome="failed", reason="stopped half way")
    mutant("invalid/partial_output_kept", partial_output)

    def input_unrelated(rs):
        rs[4]["inputs"] = [{"role": "previous_output", "sha256": sha("something else")}]
    mutant("invalid/input_not_from_predecessor", input_unrelated)

    def wrong_source(rs):
        rs[0]["inputs"] = [{"role": "source", "sha256": sha("another file")}]
    mutant("invalid/source_is_not_the_id", wrong_source)

    def backwards(rs):
        rs[3].update(started_at="2026-11-05T09:00:00Z", finished_at="2026-11-05T09:00:10Z")
    mutant("invalid/time_runs_backwards", backwards)

    def source_late(rs):
        rs[4]["inputs"] = [{"role": "source", "sha256": SOURCE_SHA}]
    mutant("invalid/source_as_input_of_a_later_stage", source_late)

    def source_beside_a_proper_input(rs):
        rs[4]["inputs"] = rs[4]["inputs"] + [{"role": "source", "sha256": SOURCE_SHA}]
    mutant("invalid/source_beside_a_proper_input", source_beside_a_proper_input)

    def skipped_with_input(rs):
        rs[2].update(outcome="skipped", reason="no conversion is needed", outputs=[])
    mutant("invalid/skipped_stage_with_an_input", skipped_with_input)

    def blank_reason(rs):
        rs[2].update(outcome="skipped", reason="   ", inputs=[], outputs=[])
    mutant("invalid/blank_reason", blank_reason)

    def essential_skipped(rs):
        rs[4].update(outcome="skipped", reason="not wanted", inputs=[], outputs=[])
    mutant("invalid/essential_stage_skipped", essential_skipped)

    def refused_wrong_id(rs):
        rs[0].update(outcome="refused", reason="not a document", outputs=[], inputs=[{"role": "source", "sha256": sha("another file")}])
        del rs[1:]
    mutant("invalid/refused_intake_with_a_foreign_source", refused_wrong_id)

    def two_sources(rs):
        rs[0]["inputs"] = [{"role": "source", "sha256": SOURCE_SHA}, {"role": "source", "sha256": sha("a second file")}]
    mutant("invalid/two_source_inputs", two_sources)

    def kc2(rs):
        rs[6]["kc2_admission"] = "admitted"
    mutant("invalid/kc2_admission_claimed", kc2)

    def unmeasured_with_value(rs):
        rs[1]["measurements"] = [{"name": "accuracy", "status": "not_measured", "reason": "no labelled set", "value": 0.97}]
    mutant("invalid/not_measured_with_a_value", unmeasured_with_value)

    def extra_field(rs):
        rs[2]["publishable"] = True
    mutant("invalid/unknown_field", extra_field)

    valid = chains["valid/synthetic-chain"]
    names = sorted(valid)
    broken = dict(valid)
    altered = bytearray(broken[names[2]])
    altered[altered.index(b"0.0.0")] = ord("9")  # a receipt changed after its successor was linked to it
    broken[names[2]] = bytes(altered)
    chains["invalid/link_broken_by_an_edit"] = broken
    chains["invalid/receipt_removed"] = {k: v for k, v in valid.items() if k != names[4]}
    forked = dict(valid)
    twin = json.loads(valid[names[3]])
    twin["run_id"] = "run.convert.2"
    forked["04-convert-retry.json"] = dump(twin)
    chains["invalid/fork"] = forked
    chains["invalid/duplicate_member"] = {**valid, names[0]: valid[names[0]].replace(b'"outcome": "done"', b'"outcome": "done",\n  "outcome": "done"', 1)}
    chains["invalid/not_json"] = {**valid, names[1]: b"not json\n"}
    chains["invalid/orphan_file"] = {**valid, "99-intake-copy.json": dump({**json.loads(valid[names[0]]), "run_id": "run.intake.2"})}
    return chains


EXPECTED = {
    "valid/synthetic-chain": None, "valid/native-format-chain": None, "valid/classify-and-convert-skipped": None,
    **{f"valid/stopped-at-{stage}": None for stage in cpr.STAGES}, "invalid/source_as_input_of_a_later_stage": "PIPE-SOURCE", "invalid/blank_reason": "PIPE-SCHEMA",
    "invalid/source_beside_a_proper_input": "PIPE-SOURCE", "invalid/skipped_stage_with_an_input": "PIPE-SCHEMA", "invalid/essential_stage_skipped": "PIPE-SKIP",
    "invalid/refused_intake_with_a_foreign_source": "PIPE-IDENTITY", "invalid/two_source_inputs": "PIPE-IDENTITY", "invalid/id_changed": "PIPE-ID", "invalid/stage_missing": "PIPE-STAGE-ORDER", "invalid/stage_repeated": "PIPE-STAGE-ORDER",
    "invalid/out_of_order": "PIPE-STAGE-ORDER", "invalid/starts_at_classify": "PIPE-STAGE-ORDER", "invalid/rights_widened": "PIPE-RIGHTS",
    "invalid/consumed_after_refusal": "PIPE-AFTER-STOP", "invalid/partial_output_kept": "PIPE-SCHEMA", "invalid/input_not_from_predecessor": "PIPE-INPUT",
    "invalid/source_is_not_the_id": "PIPE-IDENTITY", "invalid/time_runs_backwards": "PIPE-TIME", "invalid/kc2_admission_claimed": "PIPE-SCHEMA",
    "invalid/not_measured_with_a_value": "PIPE-SCHEMA", "invalid/unknown_field": "PIPE-SCHEMA", "invalid/link_broken_by_an_edit": "PIPE-LINK",
    "invalid/receipt_removed": "PIPE-LINK", "invalid/fork": "PIPE-FORK", "invalid/duplicate_member": "PIPE-READ", "invalid/not_json": "PIPE-READ",
    "invalid/orphan_file": "PIPE-HEAD",
}


def write() -> None:
    if FIXTURE_ROOT.exists():
        shutil.rmtree(FIXTURE_ROOT)
    for name, files in variants().items():
        target = FIXTURE_ROOT / name
        target.mkdir(parents=True)
        for fname, data in files.items():
            (target / fname).write_bytes(data)
    (FIXTURE_ROOT / "README.md").write_text(
        "# Synthetic pipeline receipt chains\n\nEvery receipt here is invented for this repository. `valid/` holds twelve chains: all nine stages, `convert` skipped, `classify` and `convert`\n"
        "skipped, and one that ends in a refusal at each of the nine stages. Each directory under `invalid/` is a mutant of the first valid chain with one defect and one expected refusal code\n"
        "(see `EXPECTED` in `tools/pipeline_fixture.py`). Regenerate with\n"
        "`python3 tools/pipeline_fixture.py write`; the unit tests fail if the committed files drift.\n", encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
    else:
        print("usage: pipeline_fixture.py write", file=sys.stderr)
        raise SystemExit(2)
