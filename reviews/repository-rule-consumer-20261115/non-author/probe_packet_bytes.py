#!/usr/bin/env python3
"""Finite strict-byte-JSON controls; no semantic oracle or CLI lifecycle claim."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--module-root", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, str(args.module_root))
from tools import semantic_bridge as bridge

cases = [
    ("valid_object", b'{"a":{"b":true}}', None),
    ("duplicate_nested", b'{"a":{"b":0,"b":1}}', "duplicate_json_member"),
    ("nonfinite", b'{"a":NaN}', "nonfinite_json"),
    ("invalid_utf8", b'{"a":"\xff"}', "malformed_json"),
    ("integer_limit", b'{"a":' + b'1' * 5000 + b'}', "malformed_json"),
    ("too_large", b' ' * (bridge.MAX_PACKET_BYTES + 1), "input_size_bound"),
    ("not_bytes", '{"a":true}', "packet_type"),
]
rows = []
for name, raw, expected in cases:
    try:
        bridge.parse_packet_bytes(raw)
        actual = None
    except bridge.BridgeError as error:
        actual = error.code
    rows.append({"case": name, "expected": expected, "actual": actual,
                 "pass": actual == expected})
result = {"module_sha256": hashlib.sha256(Path(bridge.__file__).read_bytes()).hexdigest(),
          "integer_limit": sys.get_int_max_str_digits(), "cases": rows,
          "pass": all(row["pass"] for row in rows),
          "limit": "Strict byte API only; no natural-language fidelity, authentication, authority or native execution."}
args.output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["pass"] else 1)
