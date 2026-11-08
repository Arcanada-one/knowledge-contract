#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""STUB: red-before placeholder. Real evaluator lands in the next commit."""
from __future__ import annotations

import sys

SUPPORTED_PROFILE = "cross-package-relations/0.1"
MAX_INPUT_BYTES = 256 * 1024


def permission_key(package_id: str, release_id: str) -> str:
    return f"{package_id}@{release_id}"


def main(argv: list[str] | None = None) -> int:
    print("stub: not implemented", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
