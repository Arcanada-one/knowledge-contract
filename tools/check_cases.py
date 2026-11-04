#!/usr/bin/env python3
"""Check the engineering cases under cases/.

Rules: required front matter and sections; every number in the prose carries a tag [Rn] that resolves, through the case's own
Receipts table, to a value in a file of this repository, and the value must match; planned cases carry no numbers; no secret,
host detail, address or personal identifier; every case is listed in cases/README.md.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import export_corpus as ec  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
CASES = REPO / "cases"
SECTIONS = ["Goal", "Setup", "What was checked and how", "Receipts", "Result", "Limits", "What failed on the way"]
STATUSES = {"written", "planned"}
NUMBER = re.compile(r"(?<![\w#./:\[-])\d+(?:\.\d+)?(?![\w\]-])")
TAG = re.compile(r"^\s*\[R(\d+)\]")
WORDS = re.compile(r"\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|hundred|thousand|dozen|dozens|hundreds)\b", re.I)
PERSONAL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+|\+\d[\d\s().-]{8,}\d|(?<!\d)\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)|(?<![\w`])@[A-Za-z][\w-]{2,}")
KINDS = {"count", "value", "lines", "table_rows", "text_contains"}
FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def front_matter(text: str) -> dict[str, str]:
    m = FRONT.match(text)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def sections(body: str) -> dict[str, str]:
    parts = re.split(r"^## (.+)$", body, flags=re.M)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def resolve_pointer(doc: object, pointer: str) -> object:
    node = doc
    for raw in [p for p in pointer.split("/") if p != ""]:
        key = raw.replace("~1", "/").replace("~0", "~")
        node = node[int(key)] if isinstance(node, list) else node[key]
    return node


def md_table_rows(text: str, heading: str) -> int:
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.lstrip("# ").strip() == heading and l.startswith("#")), None)
    if start is None:
        raise KeyError(heading)
    table = []
    for line in lines[start + 1:]:
        if line.startswith("|"):
            table.append(line)
        elif table:
            break
    return max(len([r for r in table if not set(r.replace("|", "").strip()) <= set("-: ")]) - 1, 0)


def measured(kind: str, rel: str, locator: str) -> object:
    path = (REPO / rel).resolve()
    if REPO.resolve() not in path.parents or not path.is_file():
        raise FileNotFoundError(rel)
    text = path.read_text(encoding="utf-8")
    if kind == "lines":
        return len([l for l in text.splitlines() if l.strip()])
    if kind == "table_rows":
        return md_table_rows(text, locator)
    doc = json.loads(text)
    node = resolve_pointer(doc, locator)
    if kind == "count":
        return len(node)
    return node


def receipts_table(section: str) -> dict[int, tuple[str, str, str, str]]:
    rows = {}
    for line in section.splitlines():
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and re.fullmatch(r"R\d+", cells[0]):
            rows[int(cells[0][1:])] = (cells[1], cells[2], cells[3], cells[4])
    return rows


def prose_of(section: str) -> str:
    text = re.sub(r"```.*?```", " ", section, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    return "\n".join(l for l in text.splitlines() if not l.startswith("|") and not l.startswith("#"))


def check_case_text(text: str, name: str = "case") -> list[str]:
    problems: list[str] = []
    fm = front_matter(text)
    for key in ("case_id", "title", "status", "work_items", "license", "language"):
        if key not in fm:
            problems.append(f"{name}: front matter lacks {key}")
    if problems:
        return problems
    if fm["status"] not in STATUSES:
        problems.append(f"{name}: status must be written or planned")
    if fm["license"] != "CC-BY-4.0" or fm["language"] != "en":
        problems.append(f"{name}: license must be CC-BY-4.0 and language en")
    body = text[FRONT.match(text).end():]
    secs = sections(body)
    for needed in SECTIONS:
        if needed not in secs or len(secs[needed].strip()) < 10:
            problems.append(f"{name}: section '{needed}' is missing or empty")
    if problems:
        return problems
    raw = text.encode("utf-8")
    if ec.DENY_SHAPE.search(raw) or ec.SECRET_SHAPE.search(raw):
        problems.append(f"{name}: host detail, private address or secret shape")
    if PERSONAL.search(body):
        problems.append(f"{name}: personal identifier shape (email, phone or handle)")
    table = receipts_table(secs["Receipts"])
    if fm["status"] == "planned":
        if table or "awaiting" not in fm:
            problems.append(f"{name}: a planned case lists no receipts and names what it awaits")
        for sec_name, sec in secs.items():
            prose = prose_of(sec)
            if NUMBER.search(prose) or WORDS.search(prose):
                problems.append(f"{name}: a planned case may not carry numbers ({sec_name})")
        return problems
    if not table:
        problems.append(f"{name}: a written case needs at least one receipt row")
    for rid, (rel, kind, locator, expected) in sorted(table.items()):
        if kind not in KINDS:
            problems.append(f"{name}: R{rid} has unknown kind {kind}")
            continue
        try:
            actual = measured(kind, rel, locator)
        except (OSError, KeyError, IndexError, ValueError, TypeError):
            problems.append(f"{name}: R{rid} cannot be resolved ({rel})")
            continue
        if kind == "text_contains":
            if not isinstance(actual, str) or expected not in actual:
                problems.append(f"{name}: R{rid} text does not contain the stated value")
        elif str(actual) != expected:
            problems.append(f"{name}: R{rid} states {expected} but the receipt gives {actual}")
    used: set[int] = set()
    for sec_name, sec in secs.items():
        if sec_name == "Receipts":
            continue
        prose = prose_of(sec)
        used |= {int(n) for n in re.findall(r"\[R(\d+)\]", prose)}
        if WORDS.search(prose):
            problems.append(f"{name}: a number word in '{sec_name}' ({WORDS.search(prose).group(0)}); write the digit with its receipt tag")
        for m in NUMBER.finditer(prose):
            tag = TAG.match(prose[m.end():])
            if not tag:
                problems.append(f"{name}: number {m.group(0)} in '{sec_name}' has no receipt tag")
                continue
            rid = int(tag.group(1))
            used.add(rid)
            if rid not in table:
                problems.append(f"{name}: tag R{rid} has no row in Receipts")
                continue
            rel, kind, locator, expected = table[rid]
            if kind == "text_contains":
                if m.group(0) not in re.findall(r"\d+(?:\.\d+)?", expected):
                    problems.append(f"{name}: number {m.group(0)} is not in the text of R{rid}")
            elif m.group(0) != expected:
                problems.append(f"{name}: number {m.group(0)} differs from R{rid} ({expected})")
    for rid in table:
        if rid not in used:
            problems.append(f"{name}: R{rid} is never used")
    return problems


def check_all(cases_dir: Path = CASES) -> list[str]:
    problems: list[str] = []
    files = sorted(p for p in cases_dir.glob("*.md") if p.name != "README.md" and not p.name.startswith("_"))
    index = (cases_dir / "README.md").read_text(encoding="utf-8") if (cases_dir / "README.md").is_file() else ""
    seen_ids = set()
    for path in files:
        text = path.read_text(encoding="utf-8")
        problems += check_case_text(text, path.name)
        fm = front_matter(text)
        cid = fm.get("case_id", "")
        if cid in seen_ids:
            problems.append(f"{path.name}: duplicate case_id")
        seen_ids.add(cid)
        if cid and f"`{cid}`" not in index:
            problems.append(f"{path.name}: case_id {cid} is not listed in cases/README.md")
        if cid and path.stem != cid:
            problems.append(f"{path.name}: file name must equal case_id")
    for listed in re.findall(r"\| `([a-z0-9-]+)` \|", index):
        if listed not in seen_ids:
            problems.append(f"cases/README.md lists {listed} but no such case exists")
    return problems


def main(argv: list[str]) -> int:
    problems = check_all()
    for p in problems:
        print(f"CASES_FAIL {p}")
    if problems:
        return 1
    print("CASES_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
