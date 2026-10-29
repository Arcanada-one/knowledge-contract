---
mirror_of: https://github.com/Arcanada-one/knowledge-contract/blob/39e05969728ea7a51f162cdbefac32fd8f54dbb6/SOURCES.md
mirror_source_commit: 39e05969728ea7a51f162cdbefac32fd8f54dbb6
author: Pavel Valentov and Knowledge Contract Arcana contributors
license: CC-BY-4.0
mirror_note: "Mirror of `SOURCES.md` at the source commit above, filed under `articles/` so the corpus exporter can index it. The text after this front matter is unchanged except that relative link targets are rewritten to absolute URLs at the source commit (2 rewritten). Credit: Knowledge Contract Arcana, https://contract.place. Statements in the text about the present state of the project (for example that the corpus has no approved entries) are as of the source commit."
---

# Third-party source register

Knowledge Contract Arcana credits everything it builds on. Our synthesis is ours and is licensed as described in [README.md](https://github.com/Arcanada-one/knowledge-contract/blob/39e05969728ea7a51f162cdbefac32fd8f54dbb6/README.md); third-party works keep their own license and authors and are credited here. We cannot relicense others' work. Quote or reproduce third-party text only where its license allows, otherwise link to it.

## Rule

Every file added under `papers/` or `spec/` must be covered in one of two ways:

1. A row in the table below whose **Where** column contains the file path in backticks, or
2. A `sources:` key in the file's front matter (Markdown only): either a non-empty list in which every entry equals the **Source** cell of a row below, or the literal `sources: none` when the file uses no external source. `sources: []`, `sources: ""` and an empty key do not count.

CI (`tools/check_sources.py`) fails a `papers/**` or `spec/**` file with neither. A file that credits sources in its text must still keep them credited in every derivative (see [ATTRIBUTION.md](https://github.com/Arcanada-one/knowledge-contract/blob/39e05969728ea7a51f162cdbefac32fd8f54dbb6/ATTRIBUTION.md)).

## Table schema

| Source | Author | URI | License | What was used | Where |
| --- | --- | --- | --- | --- | --- |

No third-party source is registered yet: `papers/` and `spec/` contain no published file.
