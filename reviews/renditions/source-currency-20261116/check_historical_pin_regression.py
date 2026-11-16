#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Replay one restored c135 bug by executing the exact historical checker.

The only mutation is an in-memory replacement of the target-pin refusal code.
This is separate from the current source-currency checker and its 45 controls.
"""
import argparse
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import json

BASELINE = "b00b42fb5ca4f32ca443812c980c13d4d5d53d81"
RELATIVE = "reviews/renditions/agent-situation-20261116/check_catalogue_metadata.py"
CORRECT = 'PIN_CODES = {"source": "RENDITION_SOURCE_PIN", "rendition": "RENDITION_REVISION_PIN"}'
WRONG = CORRECT.replace('"RENDITION_REVISION_PIN"', '"RENDITION_RENDITION_PIN"')
PROBE = 'rendition.verify_pin(repo, manifest, "adverse:" + label, bad_pin, PIN_CODES[label])'


def require(condition, reason):
    if not condition:
        raise ValueError("C135_WRONG_PIN_REPLAY: " + reason)


def git(repo, *arguments):
    return subprocess.check_output(["git", "-C", str(repo), *arguments])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--site-repository", type=Path, required=True)
    args = parser.parse_args()
    if not __debug__:
        parser.error("the actual pinned consumer requires non-optimized Python")
    repo, site = args.repository.resolve(), args.site_repository.resolve()
    require(git(repo, "rev-parse", "HEAD").decode().strip() == BASELINE, "historical worktree must be at b00")
    original = repo / RELATIVE
    raw = git(repo, "show", BASELINE + ":" + RELATIVE)
    require(original.read_bytes() == raw, "historical checker bytes differ")
    text = raw.decode("utf-8")
    require(text.count(CORRECT) == text.count(PROBE) == 1, "mutation/probe is not unique")
    mutant = text.replace(CORRECT, WRONG, 1)
    require(mutant.replace(WRONG, CORRECT, 1) == text, "mutation changed unrelated bytes")
    probe_line = next(i for i, line in enumerate(text.splitlines(), 1) if PROBE in line)
    filename = str(original) + "::controlled-wrong-target-pin"
    sys.dont_write_bytecode = True
    sys.argv = [str(original), "--repository", str(repo), "--site-repository", str(site)]
    try:
        exec(compile(mutant, filename, "exec"), {"__name__": "__main__", "__file__": str(original)})
    except AssertionError as error:
        require(error.args == ("RENDITION_RENDITION_PIN",), "wrong AssertionError payload")
        frames, cursor = [], error.__traceback__
        while cursor is not None:
            frames.append(cursor)
            cursor = cursor.tb_next
        probe = [frame for frame in frames if frame.tb_frame.f_code.co_filename == filename
                 and frame.tb_frame.f_code.co_name == "main" and frame.tb_lineno == probe_line]
        require(len(probe) == 1, "assertion did not arise in the target adverse-pin probe")
        local = probe[0].tb_frame.f_locals
        require(local.get("label") == "rendition" and local.get("expected") == "RENDITION_REVISION_PIN"
                and local.get("bad_pin", {}).get("sha256") == "0" * 64, "wrong adverse input")
        tail = frames[-3:]
        require([frame.tb_frame.f_code.co_name for frame in tail] == ["verify_pin", "fail", "__init__"]
                and all(Path(frame.tb_frame.f_code.co_filename).resolve() == site / "scripts/renditions.py"
                        for frame in tail), "failure did not traverse the real pinned consumer")
    else:
        raise ValueError("C135_WRONG_PIN_REPLAY: restored wrong code was accepted")
    require(original.read_bytes() == raw, "historical checker was modified")
    print(json.dumps({"result": "PASS", "historical_revision": BASELINE,
                      "historical_checker_sha256": sha256(raw).hexdigest(),
                      "mutant_sha256": sha256(mutant.encode()).hexdigest(),
                      "mutation": "only target PIN_CODES value: RENDITION_REVISION_PIN -> RENDITION_RENDITION_PIN",
                      "observed": "AssertionError: RENDITION_RENDITION_PIN",
                      "verified_call_chain": ["historical c135 adverse rendition pin", "verify_pin", "fail", "RenditionError.__init__"],
                      "scope": "one historical code-regression replay; no current source-currency or semantic acceptance"}, indent=2))


if __name__ == "__main__":
    main()
