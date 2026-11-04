import json
import tempfile
import unittest
from pathlib import Path

import build_book_package as bb
import check_book_package as cbp

AT = "2026-11-04T00:00:00Z"


class Env:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def src(self, name, data):
        p = self.root / name
        p.write_bytes(data)
        return p

    def out(self, n):
        return self.root / f"out{n}"


class BuilderTests(unittest.TestCase):
    def setUp(self):
        self.e = Env()
        self.addCleanup(self.e.tmp.cleanup)

    def test_markdown_source_is_copied_unchanged_and_validates(self):
        data = b"# Title\n\nText with | pipes |\n    indented code\n"
        m = bb.build(self.e.src("a.md", data), self.e.out(1), catalog_id="T1", created_at=AT)
        self.assertEqual(m["package_status"], "structure_only")
        self.assertEqual((self.e.out(1) / "document.md").read_bytes(), data)
        self.assertEqual((self.e.out(1) / "readable.md").read_bytes(), data)
        self.assertEqual(cbp.check_package(self.e.out(1)), [])
        q = json.loads((self.e.out(1) / "quality.json").read_text())
        self.assertEqual((q["extraction"]["status"], q["semantics"]["status"]), ("pass", "not_built"))

    def test_text_source_is_copied_and_not_typographically_corrected(self):
        data = "+--+--+\n| a| b|\nquote \"x\" -- dash...\n".encode()
        bb.build(self.e.src("a.txt", data), self.e.out(1), catalog_id="T2", created_at=AT)
        self.assertEqual((self.e.out(1) / "document.md").read_bytes(), data)

    def test_converter_output_is_used_unchanged_and_fidelity_stays_unmeasured(self):
        src, conv = self.e.src("a.pdf", b"%PDF-1.4 fake"), self.e.src("c.md", "# Converted\n\ntext\n".encode())
        m = bb.build(src, self.e.out(1), catalog_id="T3", converted_md=conv, converter=("doc-md-html", "1.2.3"), created_at=AT)
        self.assertEqual(m["package_status"], "structure_only")
        self.assertEqual(m["components"]["document_md"]["tool"], "doc-md-html")
        q = json.loads((self.e.out(1) / "quality.json").read_text())
        self.assertEqual(q["extraction"]["status"], "not_measured")
        self.assertTrue(any(c["result"] == "unknown" for c in q["extraction"]["checks"]))
        self.assertEqual(cbp.check_package(self.e.out(1)), [])

    def test_format_without_converter_gives_adapter_required_and_no_document(self):
        m = bb.build(self.e.src("a.djvu", b"AT&TFORM fake"), self.e.out(1), catalog_id="T4", created_at=AT)
        self.assertEqual(m["package_status"], "adapter_required")
        self.assertNotIn("document_md", m["components"])
        self.assertFalse((self.e.out(1) / "document.md").exists())
        self.assertEqual(cbp.check_package(self.e.out(1)), [])

    def test_digest_mismatch_blocks_and_never_replaces_the_expected_hash(self):
        m = bb.build(self.e.src("a.md", b"# x\n"), self.e.out(1), catalog_id="T5", expected_sha256="0" * 64, created_at=AT)
        self.assertEqual((m["package_status"], m["representation"]["integrity"]), ("blocked_integrity", "mismatch"))
        self.assertNotIn("document_md", m["components"])
        self.assertEqual(cbp.check_package(self.e.out(1)), [])

    def test_matching_digest_is_verified(self):
        data = b"# x\n"
        m = bb.build(self.e.src("a.md", data), self.e.out(1), catalog_id="T6", expected_sha256=bb.sha(data), created_at=AT)
        self.assertEqual(m["representation"]["integrity"], "verified")

    def test_non_utf8_or_empty_document_is_not_accepted(self):
        for n, data in enumerate((b"\xff\xfe\x00bad", b"   \n"), 1):
            m = bb.build(self.e.src(f"b{n}.txt", data), self.e.out(n), catalog_id=f"T7{n}", created_at=AT)
            self.assertEqual(m["package_status"], "adapter_required", data)

    def test_bibliography_only_has_no_document_and_is_never_queued_as_text(self):
        m = bb.build(self.e.src("a.pdf", b"x"), self.e.out(1), catalog_id="T8", bibliography_only=True, created_at=AT)
        self.assertEqual(m["package_status"], "bibliography_only")
        self.assertNotIn("document_md", m["components"])
        self.assertEqual(cbp.check_package(self.e.out(1)), [])

    def test_build_is_deterministic(self):
        src = self.e.src("a.md", b"# x\n")
        bb.build(src, self.e.out(1), catalog_id="T9", created_at=AT)
        bb.build(src, self.e.out(2), catalog_id="T9", created_at=AT)
        for p in sorted(self.e.out(1).rglob("*")):
            if p.is_file():
                self.assertEqual(p.read_bytes(), (self.e.out(2) / p.relative_to(self.e.out(1))).read_bytes())

    def test_existing_output_is_never_overwritten(self):
        src = self.e.src("a.md", b"# x\n")
        bb.build(src, self.e.out(1), catalog_id="T10", created_at=AT)
        with self.assertRaises(bb.BuildError):
            bb.build(src, self.e.out(1), catalog_id="T10", created_at=AT)

    def test_unknown_format_is_refused(self):
        with self.assertRaises(bb.BuildError):
            bb.build(self.e.src("a.xyz", b"x"), self.e.out(1), catalog_id="T11", created_at=AT)

    def test_rights_default_to_nothing_publishable(self):
        m = bb.build(self.e.src("a.md", b"# x\n"), self.e.out(1), catalog_id="T12", created_at=AT)
        self.assertEqual((m["rights"]["license_class"], m["rights"]["publishable_layers"]), ("unknown", []))

    def test_samples_mode_reads_sums_and_matrix(self):
        d = self.e.root / "samples"
        d.mkdir()
        data = b"# s\n"
        (d / "ENGR99_X.md").write_bytes(data)
        (d / "SHA256SUMS.samples").write_text(f"{bb.sha(data)}  ENGR99_X.md\n")
        (d / "MANIFEST_SHA_CHECK.tsv").write_text("SHA_OK\tmd\tENGR99\t4\tENGR99_X.md\n")
        res = bb.build_samples(d, self.e.root / "run", AT)
        self.assertEqual([(r["catalog"], r["package_status"], r["integrity"]) for r in res], [("ENGR99", "structure_only", "verified")])

    def test_validator_catches_tampering_of_a_built_package(self):
        bb.build(self.e.src("a.md", b"# x\n"), self.e.out(1), catalog_id="T13", created_at=AT)
        (self.e.out(1) / "readable.md").write_bytes(b"# changed\n")
        self.assertTrue(cbp.check_package(self.e.out(1)))


if __name__ == "__main__":
    unittest.main()
