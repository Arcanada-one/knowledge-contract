#!/usr/bin/env python3
"""Build a book package (spec/BOOK_PACKAGE.md) around a source file and, when there is one, the Markdown a converter produced.

The builder wraps; it does not convert and it does not interpret. Rules:
- the source bytes are hashed and compared with an expected digest; a mismatch gives a blocked_integrity package;
- Markdown supplied by a converter becomes document.md unchanged; plain Markdown and text sources are copied as they are (identity);
- a format without converter output gives an adapter_required package with no document, never an empty or invented one;
- readable.md starts as a copy of document.md and the edit ledger starts empty;
- objects and relations start empty and the semantic block of the quality report says not_built.
It never reads the network, never runs the source, and writes only inside the output directory it is given.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_book_package as cbp  # noqa: E402

VERSION = "0.1.0"
FORMAT_BY_SUFFIX = {".pdf": "pdf", ".djvu": "djvu", ".ps": "ps", ".epub": "epub", ".html": "html", ".htm": "html", ".md": "md", ".txt": "txt",
                    ".json": "json", ".xlsx": "xlsx", ".ppt": "ppt", ".zip": "zip", ".7z": "sevenz", ".tar.gz": "tar_gz", ".tgz": "tar_gz", ".tex": "tex"}
TEXT_NATIVE = {"md", "txt"}


class BuildError(Exception):
    pass


SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")


def safe_component(value: str, what: str) -> str:
    """A single path component made of safe characters; never a separator, '.', '..' or an absolute path."""
    if not SAFE_NAME.fullmatch(value) or ".." in value:
        raise BuildError(f"unsafe {what}: {value[:60]!r}")
    return value


def remove_created(created: list[Path]) -> None:
    """Remove only the directories this call created, deepest first, and only while they are empty."""
    for directory in created:
        try:
            directory.rmdir()
        except OSError:
            break


def regular_file_inside(path: Path, root: Path, what: str) -> Path:
    try:
        mode = os.lstat(path).st_mode
        inside = path.resolve().is_relative_to(root.resolve())
    except OSError as exc:
        raise BuildError(f"{what} is not readable ({type(exc).__name__})") from exc
    if not stat.S_ISREG(mode) or not inside:
        raise BuildError(f"{what} is not a regular file inside {root.name}")
    return path


def detect_format(name: str) -> str:
    lower = name.lower()
    for suffix in sorted(FORMAT_BY_SUFFIX, key=len, reverse=True):
        if lower.endswith(suffix):
            return FORMAT_BY_SUFFIX[suffix]
    raise BuildError(f"unknown source format for {name}")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dumps(obj: object) -> bytes:
    return json.dumps(obj, indent=1, sort_keys=True).encode("utf-8") + b"\n"


def build(source: Path, out: Path, *, catalog_id: str, release: str = "r1", language: str = "en", title: str | None = None,
          converted_md: Path | None = None, converter: tuple[str, str] = ("none", "0"), expected_sha256: str | None = None,
          bibliography_only: bool = False, license_class: str = "unknown", license_spdx: str | None = None, holder: str | None = None,
          publishable_layers: list[str] | None = None, created_at: str | None = None, source_locator: str | None = None) -> dict:
    """Write a package into `out` (must not exist) and return its manifest."""
    if out.exists():
        raise BuildError("output directory already exists; refusing to overwrite")
    data = source.read_bytes()
    fmt = detect_format(source.name)
    digest = sha(data)
    pid = f"{catalog_id}.{release}"
    integrity = "unverified" if expected_sha256 is None else ("verified" if expected_sha256 == digest else "mismatch")
    completeness = "bibliography_only" if bibliography_only else "full"

    document: bytes | None = None
    tool, tool_version = converter
    checks: list[dict] = []
    if bibliography_only:
        status, extraction = "bibliography_only", "not_measured"
    elif integrity == "mismatch":
        status, extraction = "blocked_integrity", "failed"
        checks.append({"check_id": "chk.source_digest", "result": "fail", "method": "sha256 of the source compared with the expected digest"})
    else:
        if converted_md is not None:
            document = converted_md.read_bytes()
            tool_note = "converter output used unchanged"
        elif fmt in TEXT_NATIVE:
            document, tool, tool_version = data, "identity-copy", VERSION
            tool_note = "text-native source copied unchanged"
        else:
            tool_note = None
        if document is not None:
            try:
                text = document.decode("utf-8")
            except UnicodeDecodeError:
                text = None
            if text is None or not text.strip():
                document = None
                status, extraction = "adapter_required", "failed"
                checks.append({"check_id": "chk.document_usable", "result": "fail", "method": "document must decode as UTF-8 and not be empty"})
            else:
                status = "structure_only"
                checks.append({"check_id": "chk.document_usable", "result": "pass", "method": "document decodes as UTF-8 and is not empty"})
                if converted_md is None:
                    identical = document == data
                    checks.append({"check_id": "chk.identity", "result": "pass" if identical else "fail", "method": "document bytes compared with the source bytes"})
                    extraction = "pass" if identical else "failed"
                else:
                    extraction = "not_measured"
                    checks.append({"check_id": "chk.fidelity", "result": "unknown", "method": "no fidelity check was run on the converter output (" + tool_note + ")"})
        else:
            status, extraction = "adapter_required", "adapter_required"
            checks.append({"check_id": "chk.converter", "result": "fail", "method": f"no converter output was supplied for format {fmt}"})
    if document is None and not bibliography_only and status == "structure_only":
        raise BuildError("internal error: structure_only without a document")

    files: dict[str, bytes] = {}
    comps: dict[str, dict] = {}
    if document is not None:
        files["document.md"] = document
        files["readable.md"] = document
        comps["document_md"] = {"path": "document.md", "sha256": sha(document), "input_sha256": digest, "tool": tool, "tool_version": tool_version, "contains_generated_text": False}
        comps["readable_md"] = {"path": "readable.md", "sha256": sha(document), "contains_generated_text": False}
    for name, key in (("edits.jsonl", "edits"), ("objects.jsonl", "objects"), ("relations.jsonl", "relations")):
        files[name] = b""
        comps[key] = {"path": name, "sha256": sha(b""), "count": 0}
    quality = {"schema": "KCBookQuality/v1", "package_id": pid,
               "extraction": {"status": extraction, "checks": checks or [{"check_id": "chk.bibliography", "result": "not_applicable", "method": "bibliography-only record has no text to extract"}],
                              "cer": {"metric_status": "not_measured", "value": None}},
               "semantics": {"status": "not_built", "objects_count": 0, "relations_count": 0}, "kc2_admission": "not_measured"}
    files["quality.json"] = dumps(quality)
    comps["quality"] = {"path": "quality.json", "sha256": sha(files["quality.json"])}

    rights: dict = {"license_class": license_class, "publishable_layers": list(publishable_layers or [])}
    if holder:
        rights["holder"] = holder
    if license_spdx:
        rights["license"] = license_spdx
    representation = {"representation_id": f"rep.{catalog_id}.{digest[:12]}", "format": fmt, "source_sha256": digest, "size_bytes": len(data),
                      "integrity": integrity, "completeness": completeness}
    if source_locator:
        representation["locator"] = source_locator
    manifest = {"schema": "KCBookPackageManifest/v1", "package_id": pid, "release_id": release,
                "created_at": created_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "work": {"work_id": f"work.{catalog_id}", "title": title or catalog_id},
                "edition": {"edition_id": f"ed.{catalog_id}.{language}", "language": language, "kind": "original"},
                "representation": representation, "related_works": [], "rights": rights, "components": comps,
                "tooling": [{"tool": "build_book_package", "tool_version": VERSION}] + ([{"tool": tool, "tool_version": tool_version}] if tool != "none" else []),
                "package_status": status, "kc2_admission": "not_measured"}
    files["manifest.json"] = dumps(manifest)
    created: list[Path] = []
    missing = out.parent
    while not missing.exists():
        created.append(missing)
        missing = missing.parent
    out.parent.mkdir(parents=True, exist_ok=True)
    work = out.parent / f".{out.name}.building-{os.getpid()}"
    if work.exists():
        remove_created(created)
        raise BuildError("a stale build directory is in the way; refusing to continue")
    work.mkdir()
    try:
        for rel, content in files.items():
            (work / rel).write_bytes(content)
        problems = cbp.check_package(work)
        if problems:
            raise BuildError("the package built here does not pass its own validator: " + "; ".join(problems[:3]))
        if out.exists():
            raise BuildError("output directory already exists; refusing to overwrite")
        os.rename(work, out)
    except BaseException:
        shutil.rmtree(work, ignore_errors=True)
        remove_created(created)
        raise
    return manifest


def parse_sums(path: Path) -> dict[str, str]:
    out = {}
    for line in path.read_bytes().decode("utf-8").splitlines():
        parts = line.split(None, 1)
        if len(parts) == 2:
            out[parts[1].strip()] = parts[0]
    return out


def parse_matrix(path: Path) -> dict[str, tuple[str, str]]:
    """File name -> (catalog ids, manifest check result) from a tab-separated check list."""
    out = {}
    for line in path.read_bytes().decode("utf-8").splitlines():
        cells = line.split("\t")
        if len(cells) >= 5:
            out[cells[4]] = (cells[2], cells[0])
    return out


def build_samples(samples: Path, out_root: Path, created_at: str) -> list[dict]:
    sums = parse_sums(samples / "SHA256SUMS.samples")
    matrix = parse_matrix(samples / "MANIFEST_SHA_CHECK.tsv")
    results = []
    out_root.mkdir(parents=True, exist_ok=True)
    for name in sorted(sums):
        catalog = matrix.get(name, (name.split("_")[0], ""))[0].replace("+", "-")
        try:
            safe_component(name, "source file name")
            safe_component(catalog, "catalog id")
            regular_file_inside(samples / name, samples, "source file")
            target = out_root / catalog
            if not target.resolve().is_relative_to(out_root.resolve()):
                raise BuildError("output directory leaves --out")
            manifest = build(samples / name, target, catalog_id=catalog, expected_sha256=sums[name], created_at=created_at)
            results.append({"file": name, "catalog": catalog, "format": manifest["representation"]["format"], "integrity": manifest["representation"]["integrity"],
                            "package_status": manifest["package_status"]})
        except BuildError as exc:
            results.append({"file": name, "catalog": catalog, "error": str(exc)[:200]})
    return results


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    one = sub.add_parser("one")
    one.add_argument("--source", required=True, type=Path)
    one.add_argument("--out", required=True, type=Path)
    one.add_argument("--catalog-id", required=True)
    one.add_argument("--language", default="en")
    one.add_argument("--converted-md", type=Path)
    one.add_argument("--converter", nargs=2, metavar=("TOOL", "VERSION"), default=["none", "0"])
    one.add_argument("--expected-sha256")
    many = sub.add_parser("samples")
    many.add_argument("--samples-dir", required=True, type=Path)
    many.add_argument("--out", required=True, type=Path)
    many.add_argument("--created-at", default=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    args = ap.parse_args(argv[1:])
    try:
        if args.cmd == "one":
            m = build(args.source, args.out, catalog_id=args.catalog_id, language=args.language, converted_md=args.converted_md,
                      converter=tuple(args.converter), expected_sha256=args.expected_sha256)
            print(json.dumps({"package": m["package_id"], "status": m["package_status"]}))
        else:
            results = build_samples(args.samples_dir, args.out, args.created_at)
            print(json.dumps(results, indent=1))
            return 1 if any("error" in r for r in results) else 0
    except BuildError as exc:
        print(f"BUILD_FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
