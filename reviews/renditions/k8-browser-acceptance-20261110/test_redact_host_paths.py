#!/usr/bin/env python3
"""Unit tests for redact_host_paths.py using only synthetic fixtures."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import redact_host_paths as rhp


class RedactHostPathsTests(unittest.TestCase):
    def test_synthetic_mapping_redacts_and_is_deterministic(self) -> None:
        before_r1 = "SYNTH_VENV_PREFIX_AAA"
        before_r2 = "SYNTH_WORKDIR_PREFIX_BBB/"
        published = [
            {
                "id": "R1",
                "after": "<local-venv>",
                "before_sha256": rhp.sha256_text(before_r1),
            },
            {
                "id": "R2",
                "after": "./",
                "before_sha256": rhp.sha256_text(before_r2),
            },
        ]
        original_rules = rhp.PUBLISHED_RULES
        rhp.PUBLISHED_RULES = published
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                mapping = {
                    "rules": [
                        {
                            "id": "R1",
                            "before": before_r1,
                            "after": "<local-venv>",
                            "before_sha256": rhp.sha256_text(before_r1),
                        },
                        {
                            "id": "R2",
                            "before": before_r2,
                            "after": "./",
                            "before_sha256": rhp.sha256_text(before_r2),
                        },
                    ]
                }
                mapping_path = root / "mapping.json"
                mapping_path.write_text(
                    json.dumps(mapping, indent=2) + "\n", encoding="utf-8"
                )
                src = root / "src"
                src.mkdir()
                body = (
                    f"tool={before_r1}\n"
                    f"shot={before_r2}screenshots/a.png\n"
                    f"again={before_r2}screenshots/b.png\n"
                )
                (src / "report.json").write_text(body, encoding="utf-8")
                (src / "REPORT.md").write_text(
                    f"venv {before_r1}\n", encoding="utf-8"
                )
                dst_a = root / "out-a"
                dst_b = root / "out-b"
                self.assertEqual(
                    rhp.main(
                        [
                            "--src",
                            str(src),
                            "--dst",
                            str(dst_a),
                            "--mapping",
                            str(mapping_path),
                        ]
                    ),
                    0,
                )
                self.assertEqual(
                    rhp.main(
                        [
                            "--src",
                            str(src),
                            "--dst",
                            str(dst_b),
                            "--mapping",
                            str(mapping_path),
                        ]
                    ),
                    0,
                )
                a_json = (dst_a / "report.json").read_bytes()
                b_json = (dst_b / "report.json").read_bytes()
                a_md = (dst_a / "REPORT.md").read_bytes()
                b_md = (dst_b / "REPORT.md").read_bytes()
                self.assertEqual(a_json, b_json)
                self.assertEqual(a_md, b_md)
                text = a_json.decode("utf-8")
                self.assertIn("<local-venv>", text)
                self.assertIn("./screenshots/a.png", text)
                self.assertNotIn(before_r1, text)
                self.assertNotIn(before_r2, text)
                self.assertIn("<local-venv>", a_md.decode("utf-8"))
        finally:
            rhp.PUBLISHED_RULES = original_rules

    def test_wrong_before_string_refused(self) -> None:
        before_r1 = "SYNTH_VENV_PREFIX_AAA"
        before_r2 = "SYNTH_WORKDIR_PREFIX_BBB/"
        published = [
            {
                "id": "R1",
                "after": "<local-venv>",
                "before_sha256": rhp.sha256_text(before_r1),
            },
            {
                "id": "R2",
                "after": "./",
                "before_sha256": rhp.sha256_text(before_r2),
            },
        ]
        original_rules = rhp.PUBLISHED_RULES
        rhp.PUBLISHED_RULES = published
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                mapping = {
                    "rules": [
                        {
                            "id": "R1",
                            "before": "WRONG_BEFORE_STRING",
                            "after": "<local-venv>",
                        },
                        {
                            "id": "R2",
                            "before": before_r2,
                            "after": "./",
                        },
                    ]
                }
                mapping_path = root / "mapping.json"
                mapping_path.write_text(json.dumps(mapping) + "\n", encoding="utf-8")
                with self.assertRaises(SystemExit) as ctx:
                    rhp.load_rules(mapping_path)
                self.assertIn("digest mismatch for R1", str(ctx.exception))
        finally:
            rhp.PUBLISHED_RULES = original_rules


if __name__ == "__main__":
    raise SystemExit(unittest.main())
