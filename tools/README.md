# Tools

Bounded repository checks and fixtures. They are author-side engineering
controls: they are not independent scientific review, production verification,
or a substitute for manuscript peer review.

## Retrieval-context checker

`verify_retrieval_context.py` binds the accepted retrieval-and-context paper
bytes (`PAPER_SHA256` and `PROTECTED` digests) and runs finite abstract
selection/delivery controls. CI must invoke it explicitly; a green
publication-integrity job that never ran the checker is not a pass for this
control.

Title-only projection (`--title-only-against <git-blob-or-path>`) proves that a
candidate differs from pinned accepted bytes only in a constrained title shape:
front-matter `title` may change; `subtitle` / `short_title` may be added or
changed; `previous_title` may be added and must equal the accepted title;
before the H1 at most the MD033 markdownlint comment, an `<a id>` whose id is
the GitHub slug of the accepted H1, and one blank line; the H1 must equal
`# ` plus the new title. Every other byte must stay identical. It does not
judge the new name. Any other change refuses with a typed reason and a
non-zero exit.

```sh
python3 -B tools/verify_retrieval_context.py \
  --paper papers/retrieval-and-context-composition/PAPER.md
python3 -B tools/verify_retrieval_context.py \
  --paper papers/retrieval-and-context-composition/PAPER.md \
  --title-only-against 9311c0d157d5a926e3c08f6a087a53866064f4e0
python3 -B -m unittest tools.test_verify_retrieval_context -v
```
