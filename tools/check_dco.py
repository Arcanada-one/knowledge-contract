#!/usr/bin/env python3
"""Fail when a commit in BASE..HEAD lacks a valid Signed-off-by trailer (DCO 1.1).

Rules:
- The sign-off must be in the trailer block: the last paragraph of the message,
  which must not be the subject paragraph.
- Its name and email must match the commit author or the committer
  (case-insensitive), so a contributor cannot sign off for someone else.
- Merge commits are not checked. They carry no authored content; every
  non-merge commit they bring into BASE..HEAD is checked. History of this
  repository is linear (squash merges), so merge commits only appear when a
  contributor merges the base branch into a PR branch.
- Exception: commits whose author is in BOT_AUTHORS (automation that cannot sign
  off) are accepted without a sign-off. The list is exact-match on name and
  email and is part of the reviewed source; extend it only by pull request.
"""
from __future__ import annotations

import re
import subprocess
import sys

SIGNOFF_RE = re.compile(r"^Signed-off-by: (?P<name>.+?) <(?P<email>[^<>\s]+@[^<>\s]+)>[ \t]*$", re.I)

BOT_AUTHORS = {
    ("dependabot[bot]", "49699333+dependabot[bot]@users.noreply.github.com"),
    ("github-actions[bot]", "41898282+github-actions[bot]@users.noreply.github.com"),
}


def commits(base: str, head: str, repo: str = ".") -> list[dict]:
    fmt = "%H%x1f%P%x1f%an%x1f%ae%x1f%cn%x1f%ce%x1f%B%x1e"
    out = subprocess.run(
        ["git", "-C", repo, "log", f"--format={fmt}", f"{base}..{head}"],
        check=True, capture_output=True, text=True,
    ).stdout
    rows = []
    for record in out.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        sha, parents, an, ae, cn, ce, body = record.split("\x1f", 6)
        rows.append({"sha": sha, "parents": parents.split(), "author": (an, ae), "committer": (cn, ce), "body": body})
    return rows


def trailer_paragraph(body: str) -> list[str]:
    paragraphs = re.split(r"\n[ \t]*\n", body.strip("\n"))
    if len(paragraphs) < 2:
        return []
    return paragraphs[-1].splitlines()


def signed(commit: dict) -> bool:
    identities = {(n.casefold(), e.casefold()) for n, e in (commit["author"], commit["committer"])}
    for line in trailer_paragraph(commit["body"]):
        match = SIGNOFF_RE.match(line)
        if match and (match["name"].casefold(), match["email"].casefold()) in identities:
            return True
    return False


def unsigned(base: str, head: str, repo: str = ".") -> list[str]:
    bad = []
    for commit in commits(base, head, repo):
        if len(commit["parents"]) > 1:
            continue
        if commit["author"] in BOT_AUTHORS:
            continue
        if not signed(commit):
            bad.append(commit["sha"])
    return bad


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: check_dco.py BASE HEAD", file=sys.stderr)
        return 2
    bad = unsigned(argv[1], argv[2])
    for sha in bad:
        print(f"DCO_CHECK_FAIL {sha} has no Signed-off-by trailer matching its author or committer (use git commit -s)")
    if bad:
        return 1
    print("DCO_CHECK_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
