#!/usr/bin/env python3
"""Bounded, separately authored input/status probes; not the arithmetic oracle."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
MODULE = HERE / "semantic_bridge_successor.py"
EXPECTED = "0b049720da90a0b53f190bc720b78f9bbf4bf9940313c4c65cb699d2ae5a0d6a"
assert hashlib.sha256(MODULE.read_bytes()).hexdigest() == EXPECTED
spec = importlib.util.spec_from_file_location("reviewed_bridge", MODULE)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)
RESULTS = []
FIXTURES = HERE / "input-fixtures"
FIXTURES.mkdir(exist_ok=True)

def observation(state="unknown", value=None):
    result = {"referent": "supplied condition", "type": "boolean", "state": state}
    if state == "known":
        result["value"] = value
    return result

def packet(source, declarations, observations):
    """The declarations specify exact whole-line byte strings independently."""
    readings = []
    for identity, quoted_line, bindings in declarations:
        encoded = quoted_line.encode("utf-8")
        assert source.count(encoded) == 1
        start = source.index(encoded)
        readings.append({"id": identity, "start": start, "end": start + len(encoded),
                         "quote": quoted_line, "attribution": {"agent": "review fixture", "discourse": "hypothetical"},
                         "bindings": bindings})
    return {"schema": "kc-semantic-bridge/1", "source_sha256": hashlib.sha256(source).hexdigest(),
            "source_media_type": "text/plain", "interpretation_set": "alternatives",
            "observations": observations, "readings": readings}

def analyzed(name, source, supplied, status, code=None, truth=None, extra=None):
    result = bridge.analyze(source, supplied)
    assert result["status"] == status, (name, result)
    assert result["effects_authorized"] is False, (name, result)
    for key in ("source_semantic_fidelity", "attribution_authenticity", "real_world_truth", "current_authority"):
        assert result[key] == "NOT_ASSESSED", (name, result)
    if status != "EVALUATED":
        assert "truth" not in result and "readings" not in result, (name, result)
    if code:
        assert result["errors"][0]["code"] == code, (name, result)
    if truth:
        assert result["truth"] == truth, (name, result)
    if extra:
        extra(result)
    RESULTS.append({"name": name, "source_sha256": hashlib.sha256(source).hexdigest(),
                    "packet_sha256": hashlib.sha256(json.dumps(supplied, sort_keys=True, ensure_ascii=True).encode()).hexdigest(),
                    "report": result})
    return result

def reader_refusal(name, raw, code):
    path = FIXTURES / (name + ".json")
    path.write_bytes(raw)
    try:
        bridge.read_packet(path)
    except bridge.BridgeError as error:
        assert error.code == code, (name, error.code)
        RESULTS.append({"name": name, "raw_sha256": hashlib.sha256(raw).hexdigest(),
                        "bytes": len(raw), "error_code": error.code, "status": error.status})
    else:
        raise AssertionError((name, "invalid JSON was accepted"))

line = "RULE r: p UNLESS q"
source = ("NOTE Проверка 字节\r\n" + line + "\r\n").encode()
supplied = packet(source, [("r", line, {"p": "p", "q": "q"})],
                  {"p": observation("known", True), "q": observation("known", False)})
result = analyzed("unicode_crlf_full_unit", source, supplied, "EVALUATED", truth="TRUE")
assert result["readings"][0]["span"]["start"] == len("NOTE Проверка 字节\r\n".encode())
changed = copy.deepcopy(supplied)
changed["readings"][0]["end"] = changed["readings"][0]["start"] + len("RULE r: p")
changed["readings"][0]["quote"] = "RULE r: p"
analyzed("clipped_exception", source, changed, "INVALID", "whole_unit_required")
analyzed("changed_source_digest", source.replace("字节".encode(), "符号".encode()), supplied, "INVALID", "source_digest_mismatch")
changed = copy.deepcopy(supplied); changed["readings"][0]["quote"] = line.replace("UNLESS", "AND")
analyzed("wrong_quote", source, changed, "INVALID", "quote_mismatch")
changed = copy.deepcopy(supplied); changed["readings"][0]["start"] = True
analyzed("boolean_byte_offset", source, changed, "INVALID", "whole_unit_required")
changed = copy.deepcopy(supplied); changed["readings"][0]["unsupported_member"] = 0
analyzed("unknown_reading_member", source, changed, "INVALID", "invalid_fields")
changed = copy.deepcopy(supplied); changed["observations"]["p"]["referent"] = "\ud800"
analyzed("unpaired_unicode_surrogate", source, changed, "INVALID", "invalid_utf8")

source2 = b"RULE a: p\nRULE b: NOT p\n"
alternatives = packet(source2, [("a", "RULE a: p", {"p": "x"}), ("b", "RULE b: NOT p", {"p": "x"})], {"x": observation()})
alternatives["readings"].reverse()
result = analyzed("alternatives_same_world_source_order", source2, alternatives, "EVALUATED", truth="UNDETERMINED")
assert result["reading_disagreement"] is True
assert [(r["id"], r["table_bits"]) for r in result["readings"]] == [("a", "01"), ("b", "10")]
assert result["valuation_count"] == 2
changed = copy.deepcopy(alternatives); changed["readings"].pop()
analyzed("missing_rule_reading", source2, changed, "INVALID", "incomplete_rule_inventory")
changed = copy.deepcopy(alternatives); changed["readings"][1] = copy.deepcopy(changed["readings"][0])
analyzed("duplicate_reading", source2, changed, "INVALID", "duplicate_reading")
changed = copy.deepcopy(alternatives); extra = copy.deepcopy(changed["readings"][0]); extra["id"] = "extra"; changed["readings"].append(extra)
analyzed("extra_reading", source2, changed, "INVALID", "incomplete_rule_inventory")
analyzed("duplicate_source_rule", b"RULE a: p\nRULE a: NOT p\n", alternatives, "INVALID", "duplicate_rule_unit")
badsource = b"RULE a: TRUE\nRULE b: p FORALL q\n"
badpacket = packet(badsource, [("a", "RULE a: TRUE", {}), ("b", "RULE b: p FORALL q", {"p": "x", "q": "x"})], {"x": observation()})
result = analyzed("required_unsupported_alternative", badsource, badpacket, "UNSUPPORTED", "unsupported_token")
assert result["source_binding"] == "VERIFIED" and result["controlled_parsing"] == "NOT_VERIFIED"
alias_source = b"RULE alias: p AND NOT q\n"
for state in ("unknown", "withheld"):
    aliases = packet(alias_source, [("alias", "RULE alias: p AND NOT q", {"p": "x", "q": "x"})], {"x": observation(state)})
    result = analyzed("correlation_" + state, alias_source, aliases, "EVALUATED", truth="FALSE")
    assert result["observations"]["x"]["state"] == state and result["readings"][0]["table_bits"] == "00"

reader_refusal("duplicate_root", b'{"x":1,"x":2}', "duplicate_json_member")
reader_refusal("duplicate_nested_escaped", b'{"outer":[{"state":"unknown","st\\u0061te":"known"}]}', "duplicate_json_member")
reader_refusal("nonfinite_nan", b'{"value":NaN}', "nonfinite_json")
reader_refusal("malformed_json", b'{"schema":', "malformed_json")

constant = b"RULE r: TRUE\n"
constant_packet = packet(constant, [("r", "RULE r: TRUE", {})], {})
result = analyzed("constant_empty_observation_domain", constant, constant_packet, "EVALUATED", truth="TRUE")
assert result["world_assignments"] == [{}] and result["valuation_count"] == 1
raw = json.dumps(constant_packet).encode()
at_limit = raw + b" " * (131072 - len(raw))
path = FIXTURES / "packet_at_byte_limit.json"; path.write_bytes(at_limit)
result = analyzed("packet_at_byte_limit", constant, bridge.read_packet(path), "EVALUATED", truth="TRUE")
reader_refusal("packet_over_byte_limit", at_limit + b" ", "input_size_bound")
large_source = b"NOTE " + b"x" * (65536 - 5 - 1 - len(constant)) + b"\n" + constant
assert len(large_source) == 65536
large_packet = packet(large_source, [("r", "RULE r: TRUE", {})], {})
analyzed("source_at_byte_limit", large_source, large_packet, "EVALUATED", truth="TRUE")
analyzed("source_over_byte_limit", large_source + b"\n", large_packet, "UNSUPPORTED", "source_size_bound")

def compile_limit(name, expression, error_code=None):
    try:
        bridge.compile_rule(expression)
    except bridge.BridgeError as error:
        assert error_code is not None and error.code == error_code, (name, error.code)
        RESULTS.append({"name": name, "expression_sha256": hashlib.sha256(expression.encode()).hexdigest(), "error_code": error.code})
    else:
        assert error_code is None, (name, "over-limit expression accepted")
        RESULTS.append({"name": name, "expression_sha256": hashlib.sha256(expression.encode()).hexdigest(), "compiled": True})

compile_limit("depth_at_16", "NOT " * 15 + "p")
compile_limit("depth_over_16", "NOT " * 16 + "p", "depth_bound")
balanced = "p"
for _ in range(6): balanced = "(" + balanced + " AND " + balanced + ")"
compile_limit("nodes_at_128", "NOT " + balanced)
compile_limit("nodes_over_128", "NOT NOT " + balanced, "node_bound")
compile_limit("chars_at_4096", "TRUE" + " " * 4092)
compile_limit("chars_over_4096", "TRUE" + " " * 4093, "expression_bound")

record = {"reviewed_module_sha256": EXPECTED, "python": sys.version, "probes": RESULTS,
          "probe_count": len(RESULTS), "outcome": "PASS", "scope": "bounded separately authored input/status checks; no exhaustive arithmetic or external scientific claim"}
(HERE / "bounded-review-results.json").write_text(json.dumps(record, ensure_ascii=True, indent=2) + "\n")
print(json.dumps({"module_sha256": EXPECTED, "probe_count": len(RESULTS), "outcome": "PASS", "names": [r["name"] for r in RESULTS]}, indent=2))
