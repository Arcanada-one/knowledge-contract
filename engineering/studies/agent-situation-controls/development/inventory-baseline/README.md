---
title: "Control Inventory: Preserved Runner and Omission Probe"
status: "retained-development-evidence"
sources: none
license: "CC-BY-4.0"
---

# Control Inventory: Preserved Runner and Omission Probe

This directory retains the exact runner from source commit `535c557a1c6bf90e156a17ca6d340a5c6dcd0a1f` and a separately executed review probe. The runner SHA-256 is `b77eda085d9335f585a227fdfb4dc99d1abcca6590f52318d01c97922b324fdd`. It is the runner identified by the original study manifest and original 21-control evidence; it has not been rewritten to include the repair.

The probe copied the whole study to a temporary directory, imported the original runner, removed only its last registered callable (`case21`) from `CASES`, and called `main`. All 21 expected fixtures remained present. The resulting [raw probe report](missing-control-run.json) records 20 executed controls, 87 claimed checked fields, and `FINITE_CONTROLS_PASS`; exit code was 0. Only 84 expected top-level fields belonged to the 20 executed controls. This is intentionally defective reviewer-generated output, not a replacement for the original full 21-control result.

The archived runner is a source artifact, not a self-contained executable at this nested path. To reproduce the old behavior, copy the current study into a temporary directory, replace its `checks/check_agent_situation.py` with this archived file, then import that temporary runner and set `CASES = CASES[:-1]` before calling `main`. Never run the writing entry point against retained repository evidence.

The successor runner validates an explicit one-to-one correspondence between the 21 declared IDs, callable registrations and fixtures before execution. The new results and limits are in [the dated successor receipt](../../evidence/20261114-inventory-receipt.json). The original `MANIFEST.json`, `evidence/finite-run.json` and `evidence/execution.txt` remain unchanged. The exact original `evidence/origin.json` bytes are preserved here as [origin.json](origin.json); the current origin retains its original three entries and adds all successor records for complete publication coverage. The runtime model and expected control values were unchanged. This repair concerns completeness of the finite harness, not agent performance or independent scientific acceptance.
