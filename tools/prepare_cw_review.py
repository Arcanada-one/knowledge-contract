#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Bind a CW review packet to exact inputs; never authenticate or approve it.

The Python API accepts bytes, not caller-selected filesystem paths or trust flags.
The CLI reads an explicitly pinned local Git snapshot and reports missing paper
results. No network, credentials, native requests, merge or publication effects.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

try:
    from tools import check_contract_profile as exchange
    from tools import check_cw_programme as programme
except ModuleNotFoundError:
    import check_contract_profile as exchange
    import check_cw_programme as programme

ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = "roadmap/coordinated-work/plan/execution-graph.json"
CRITERION_PATH = ROOT / "roadmap/coordinated-work/review-binding/criterion.json"
PROFILE = "kc-cw-review-subject/1"
CRITERION_PROFILE = "kc-cw-review-binding-criterion/1"
LANGUAGES = {"en", "ru", "zh-Hans"}
PROPERTIES = {
    "paper_result": ("claim_coverage", "claim_support", "applicability",
                     "review_protocol", "publication_rights"),
    "programme_announcement": ("announcement_accuracy", "review_protocol",
                               "publication_rights"),
}
ORIGINS = {"original_result", "metadata_extraction", "reconstructed_view",
           "new_synthetic_example"}
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9:/._-]{0,199}\Z")


class Invalid(ValueError):
    """Preparation/representation failure, not a refutation of a scientific claim."""


def require(condition, message):
    if not condition:
        raise Invalid(message)


def decode(data):
    try:
        return exchange.decode_record(data)
    except (exchange.ProfileError, AttributeError, TypeError) as exc:
        raise Invalid(str(exc)) from exc


def encode(value):
    """Write one explicit representation; digests always cover the resulting bytes."""
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def nonblank(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label}: nonblank text required")
    require(not any(0xD800 <= ord(c) <= 0xDFFF for c in value), f"{label}: isolated surrogate")


@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    revision: str
    data: bytes
    hash_domain: str = "sha256/raw-bytes-v1"

    def __post_init__(self):
        require(isinstance(self.artifact_id, str) and ID.fullmatch(self.artifact_id), "invalid artifact ID")
        require(isinstance(self.revision, str) and ID.fullmatch(self.revision), "invalid revision")
        require(type(self.data) is bytes, "artifact data must be immutable bytes")
        require(self.hash_domain in {"sha256/raw-bytes-v1", "sha256/raw-utf8-json-v1"}, "unsupported hash domain")
        if self.hash_domain == "sha256/raw-utf8-json-v1":
            decode(self.data)

    @property
    def ref(self):
        return {"artifact_id": self.artifact_id, "revision": self.revision,
                "hash_domain": self.hash_domain, "sha256": hashlib.sha256(self.data).hexdigest()}


@dataclass(frozen=True)
class Evidence:
    artifact: Artifact
    locator: str
    origin: str

    def __post_init__(self):
        require(isinstance(self.artifact, Artifact), "evidence needs actual artifact bytes")
        require(bool(self.artifact.data), "evidence artifact is empty")
        nonblank(self.locator, "evidence location")
        require(self.origin in ORIGINS, "unsupported evidence origin; a plan is not an output")


@dataclass(frozen=True)
class BoundSubject:
    artifact: Artifact
    criterion: Artifact
    inputs: tuple[Artifact, ...]
    missing: tuple[str, ...]
    required_properties: tuple[str, ...]


def registry(artifacts):
    result = {}
    for artifact in artifacts:
        require(isinstance(artifact, Artifact), "expected an Artifact with actual bytes")
        key = (artifact.artifact_id, artifact.revision, artifact.hash_domain)
        require(key not in result or result[key].data == artifact.data,
                f"conflicting bytes for the same artifact identity: {artifact.artifact_id}")
        result[key] = artifact
    return result


def resolve(ref, entries):
    if not isinstance(ref, dict):
        return None
    artifact = entries.get((ref.get("artifact_id"), ref.get("revision"), ref.get("hash_domain")))
    return artifact if artifact is not None and artifact.ref == ref else None


def criterion_artifact():
    raw = CRITERION_PATH.read_bytes()
    return Artifact("kc:cw-review-binding-criterion", "content-" + hashlib.sha256(raw).hexdigest(),
                    raw, "sha256/raw-utf8-json-v1")


def bind_subject(*, graph, expected_source_ref, criterion, purpose, paper_id=None, documents=None,
                 applicability=None, evidence=None, review_policy=None):
    """Freeze complete material inputs, including explicit absences, for a review.

    The criterion and Git source are selected by the caller independently of any
    supplied observation. Neither selection is an authenticated grant of authority.
    """
    require(isinstance(graph, Artifact) and isinstance(criterion, Artifact), "graph and criterion artifacts required")
    require(graph.ref == expected_source_ref, "source bytes do not match the independently selected expected reference")
    require(re.fullmatch(r"[0-9a-f]{40}", graph.revision), "source must name a full Git commit")
    require(purpose in PROPERTIES, "unsupported review purpose")
    rule = decode(criterion.data)
    require(set(rule) == {"schema", "scope", "properties"} and rule["schema"] == CRITERION_PROFILE
            and rule["scope"] == "offline_packet_preparation_and_binding_only"
            and rule["properties"] == {k: list(v) for k, v in PROPERTIES.items()},
            "unsupported criterion; mandatory properties cannot be weakened by the packet")
    source = decode(graph.data)
    try:
        programme.validate_release_contracts(source)
        require(source["status"] == "proposed", "source must remain a proposal")
    except (programme.InvalidProgramme, KeyError, TypeError) as exc:
        raise Invalid(f"invalid source release contracts: {exc}") from exc

    documents = {} if documents is None else dict(documents)
    evidence = {} if evidence is None else dict(evidence)
    require(set(documents) <= LANGUAGES, "unsupported document language")
    missing, inputs = [], [graph, criterion]
    if purpose == "paper_result":
        contracts = source["paper_release_contracts"]
        positions = [n for n, c in enumerate(contracts) if c["paper_id"] == paper_id]
        require(len(positions) == 1, "paper ID does not select exactly one release contract")
        position = positions[0]
        contract = contracts[position]
        claim = {"paper_id": paper_id, "class": contract["claim_class"],
                 "statement": contract["claim_scope"], "language": "en",
                 "selector": f"/paper_release_contracts/{position}"}
        required_outputs = sorted({output for gate in contract["required_gates"] for output in gate["consumes"]})
        if applicability is None:
            missing.append("applicability")
    else:
        require(paper_id is None, "an announcement cannot inherit a paper-result identity")
        required_outputs = []
        claim = {"programme_id": source["programme_id"], "class": "programme_announcement",
                 "status": source["status"], "epics": len(source["epics"]),
                 "work_packages": len(source["tasks"]), "paper_contracts": len(source["paper_release_contracts"]),
                 "scope": "Counts of proposed entries in this source snapshot; no research result or delivery claim."}
    require(set(evidence) <= set(required_outputs), "unknown output; evidence obligations come from the pinned source")
    if "en" not in documents:
        missing.append("complete_document:en")
    document_refs = []
    for language, artifact in sorted(documents.items()):
        require(isinstance(artifact, Artifact), "document artifact required")
        try:
            nonblank(artifact.data.decode("utf-8"), "complete document")
        except UnicodeError as exc:
            raise Invalid("document is not UTF-8") from exc
        inputs.append(artifact)
        document_refs.append({"language": language, "artifact": artifact.ref, "extent": "complete_file"})
    if applicability is not None:
        require(isinstance(applicability, Artifact), "applicability artifact required")
        domain = decode(applicability.data)
        required_domain = {"population_or_model", "conditions", "time_horizon", "comparison",
                           "quantifiers", "assumptions", "excluded_conclusions"}
        require(set(domain) == required_domain, "incomplete or unsupported applicability descriptor")
        for field in required_domain:
            nonblank(domain[field], f"applicability.{field}")
        inputs.append(applicability)
    if review_policy is None:
        missing.append("review_policy")
    else:
        require(isinstance(review_policy, Artifact) and bool(review_policy.data), "review policy bytes required")
        inputs.append(review_policy)
    evidence_refs = []
    for output in required_outputs:
        item = evidence.get(output)
        if item is None:
            missing.append("output:" + output)
            evidence_refs.append({"output_id": output, "artifact": None, "locator": None, "origin": "missing"})
        else:
            require(isinstance(item, Evidence), "an output ID or future path is not observed evidence")
            inputs.append(item.artifact)
            evidence_refs.append({"output_id": output, "artifact": item.artifact.ref,
                                  "locator": item.locator, "origin": item.origin})
    registry(inputs)
    properties = tuple(PROPERTIES[purpose]) + tuple("translation_fidelity:" + lang for lang in sorted(documents) if lang != "en")
    descriptor = {"schema": PROFILE, "purpose": purpose,
                  "source": {"repository": "Arcanada-one/knowledge-contract", "path": GRAPH_PATH,
                             "artifact": graph.ref, "git_blob": programme.git_blob(graph.data),
                             "revision_provenance": "caller_selected_expected_reference_not_authenticated"},
                  "criterion": criterion.ref, "claim": claim, "documents": document_refs,
                  "applicability": None if applicability is None else applicability.ref,
                  "evidence": evidence_refs, "review_policy": None if review_policy is None else review_policy.ref,
                  "required_properties": list(properties), "missing_inputs": missing}
    raw = encode(descriptor)
    subject = Artifact("kc:cw-review-subject:" + (paper_id or "programme-announcement"),
                       "content-" + hashlib.sha256(raw).hexdigest(), raw, "sha256/raw-utf8-json-v1")
    return BoundSubject(subject, criterion, tuple(inputs), tuple(missing), properties)


def observation_scope(subject, property_name):
    """Explicit representation profile; no natural-language equivalence inference."""
    descriptor = decode(subject.artifact.data)
    return (f"purpose={descriptor['purpose']}; property={property_name}; "
            f"subject-sha256={subject.artifact.ref['sha256']}; extent=complete-bound-descriptor")


def context_matches(artifact, observation):
    """Check supplied protocol context consistency, never authenticity or competence."""
    context = decode(artifact.data)
    fields = {"schema", "subject", "criterion", "property", "scope", "reviewer", "method", "review_kind",
              "reviewer_access", "shared_dependencies", "independence_boundary", "competence_basis"}
    if set(context) != fields or context.get("schema") != "kc-cw-review-context/1":
        return False
    if any(context[key] != observation[key] for key in ("subject", "criterion", "property", "scope", "method")):
        return False
    if context["reviewer"] != observation["observer"] or context["review_kind"] not in {
            "editorial", "internal_technical", "independent_agent", "external_peer"}:
        return False
    return all(isinstance(context[key], str) and bool(context[key].strip()) for key in
               ("reviewer_access", "shared_dependencies", "independence_boundary", "competence_basis"))


def inspect_subject(subject, *, observations=(), review_materials=(), previous_descriptor=None):
    """Assess mechanical bindings, preserving each supplied result and all unknowns."""
    require(isinstance(subject, BoundSubject), "use bind_subject to prepare the current subject")
    descriptor = decode(subject.artifact.data)
    # Reconstruct the contract from the current immutable bytes. A caller-created
    # dataclass or edited descriptor cannot delete a mandatory output/property.
    own_entries = registry(subject.inputs)
    try:
        require(descriptor.get("schema") == PROFILE, "unsupported subject descriptor")
        current = bind_subject(
            graph=resolve(descriptor["source"]["artifact"], own_entries),
            expected_source_ref=descriptor["source"]["artifact"],
            criterion=subject.criterion, purpose=descriptor["purpose"],
            paper_id=descriptor["claim"].get("paper_id"),
            documents={row["language"]: resolve(row["artifact"], own_entries) for row in descriptor["documents"]},
            applicability=None if descriptor["applicability"] is None else resolve(descriptor["applicability"], own_entries),
            evidence={row["output_id"]: Evidence(resolve(row["artifact"], own_entries), row["locator"], row["origin"])
                      for row in descriptor["evidence"] if row["artifact"] is not None},
            review_policy=None if descriptor["review_policy"] is None else resolve(descriptor["review_policy"], own_entries))
        require(current.artifact == subject.artifact and current.missing == subject.missing
                and current.required_properties == subject.required_properties,
                "subject does not match reconstructed mandatory inputs")
    except (KeyError, TypeError, AttributeError) as exc:
        raise Invalid("malformed subject descriptor") from exc
    entries = registry((*subject.inputs, subject.artifact, *review_materials))
    rows, ids, covered, changes = [], set(), set(), []
    if previous_descriptor is not None:
        previous = decode(previous_descriptor)
        require(previous.get("schema") == PROFILE, "unsupported predecessor descriptor")
        changes = sorted(key for key in set(previous) | set(descriptor) if previous.get(key) != descriptor.get(key))
        if previous_descriptor != subject.artifact.data and not changes:
            changes = ["descriptor_raw_bytes"]
    for raw in observations:
        observation = decode(raw)
        errors = exchange.check_record(observation)
        require(not errors and observation.get("schema") == "KCObservation/v1",
                "malformed observation: " + "; ".join(errors))
        oid = observation["observation_id"]
        require(oid not in ids, "duplicate observation ID: " + oid)
        ids.add(oid)
        problems = []
        prop = observation["property"]
        if observation["subject"] != subject.artifact.ref:
            problems.append("subject_mismatch")
        if observation["criterion"] != subject.criterion.ref:
            problems.append("criterion_mismatch")
        if prop not in subject.required_properties:
            problems.append("property_outside_current_purpose")
        if observation["scope"] != observation_scope(subject, prop):
            problems.append("scope_mismatch")
        resolved = [resolve(ref, entries) for ref in observation["evidence_refs"]]
        if any(item is None for item in resolved):
            problems.append("evidence_bytes_missing_or_changed")
        contexts = [item for item in resolved if item is not None
                    and item.hash_domain == "sha256/raw-utf8-json-v1"
                    and decode(item.data).get("schema") == "kc-cw-review-context/1"]
        if len(contexts) != 1 or not context_matches(contexts[0], observation):
            problems.append("review_context_missing_or_mismatched")
        needed = []
        if prop == "claim_support":
            needed = [row["artifact"] for row in descriptor["evidence"] if row["artifact"] is not None]
        elif prop in {"claim_coverage", "publication_rights"}:
            needed = [row["artifact"] for row in descriptor["documents"]]
        elif prop == "announcement_accuracy":
            needed = [descriptor["source"]["artifact"], *[row["artifact"] for row in descriptor["documents"]]]
        elif prop == "review_protocol" and descriptor["review_policy"] is not None:
            needed = [descriptor["review_policy"]]
        elif prop.startswith("translation_fidelity:"):
            language = prop.split(":", 1)[1]
            needed = [row["artifact"] for row in descriptor["documents"] if row["language"] in {"en", language}]
        elif prop == "applicability" and descriptor["applicability"] is not None:
            needed = [descriptor["applicability"]]
        if any(ref not in observation["evidence_refs"] for ref in needed):
            problems.append("required_material_not_referenced")
        if observation["result"] == "not_applicable":
            # Schema requires the rule reference; the rule's bytes are also needed.
            if resolve(observation["inapplicability_rule"], entries) is None:
                problems.append("inapplicability_rule_unresolved")
        if not problems:
            covered.add(prop)
        rows.append({"observation_id": oid, "sha256": hashlib.sha256(raw).hexdigest(),
                     "property": prop, "claimed_result": observation["result"],
                     "binding_result": "fail" if problems else "pass", "problems": problems,
                     "authenticity": "unknown", "competence": "unknown"})
    missing_properties = sorted(set(subject.required_properties) - covered)
    binding = ("fail" if any(row["problems"] for row in rows) else
               "unknown" if missing_properties else "pass")
    reasons = ["REVIEW_REQUIRED", "reviewer_authenticity_not_established", "competence_not_established"]
    if changes:
        reasons.append("successor_assessment_required")
    if subject.missing:
        reasons.append("required_inputs_missing")
    if missing_properties:
        reasons.append("required_observations_missing_or_unbound")
    for claimed, reason in (("fail", "supplied_negative_assessment_retained"),
                            ("unknown", "supplied_unknown_assessment_retained"),
                            ("not_applicable", "supplied_exemption_not_established")):
        if any(row["claimed_result"] == claimed for row in rows):
            reasons.append(reason)
    return {"schema": "kc-cw-offline-review-report/1", "scope": "offline_packet_preparation_and_binding_only",
            "subject": subject.artifact.ref, "criterion": subject.criterion.ref, "purpose": descriptor["purpose"],
            "descriptor": descriptor, "preparation_result": "unknown" if subject.missing else "pass",
            "binding_result": binding, "supplied_observations": rows,
            "missing_properties": missing_properties, "changed_material_fields": changes,
            "claim_support": "unknown", "qualified_review": "unknown", "reviewer_authenticity": "unknown",
            "result": "unknown", "impact": "requires_review", "eligibility": "unknown", "decision": "revalidate",
            "reason_codes": reasons, "effects_authorized": False,
            "limitations": ["Supplied observations and protocol context are not authenticated.",
                            "The pure API compares an independently selected expected source reference; it does not authenticate that reference's Git provenance.",
                            "Byte identity and complete references do not establish semantic support, source fidelity or rights.",
                            "Missing declared inputs do not prove that no artifact exists elsewhere.",
                            "No current-use resolver, publication, native admission or deployment is implemented."]}


def git_bytes(repository, revision, path):
    require(bool(re.fullmatch(r"[0-9a-f]{40}", revision)), "use a full immutable source commit")
    environment = os.environ.copy()
    environment.update(GIT_NO_LAZY_FETCH="1", GIT_NO_REPLACE_OBJECTS="1",
                       GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
    prefix = ["git", "--no-replace-objects", "--no-optional-locks", "-c", "core.fsmonitor=false",
              "-c", "protocol.allow=never", "-C", str(repository), "cat-file"]
    options = {"check": False, "stdout": subprocess.PIPE, "stderr": subprocess.PIPE,
               "stdin": subprocess.DEVNULL, "env": environment, "timeout": 30}
    kind = subprocess.run([*prefix, "-t", revision], **options)
    require(kind.returncode == 0 and kind.stdout == b"commit\n", "source revision is not an available Git commit")
    completed = subprocess.run([*prefix, "blob", revision + ":" + path], **options)
    require(completed.returncode == 0, "source snapshot unavailable in local Git: " + path)
    return completed.stdout


def pending_report(repository, revision):
    graph = Artifact("kc:cw-execution-graph", revision, git_bytes(repository, revision, GRAPH_PATH),
                     "sha256/raw-utf8-json-v1")
    criterion = criterion_artifact()
    source = decode(graph.data)
    reports = [inspect_subject(bind_subject(graph=graph, expected_source_ref=graph.ref, criterion=criterion,
                                           purpose="paper_result", paper_id=row["paper_id"]))
               for row in source["paper_release_contracts"]]
    return {"schema": "kc-cw-pending-reviews/1", "source": graph.ref,
            "source_readback": {"method": "local_git_cat_file", "commit_type_checked": True,
                                "repository_identity_authenticated": False},
            "method": {"id": "kc:cw-offline-review-bindings", "version": "1",
                       "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}, "papers": reports,
            "review_required": len(reports), "effects_authorized": False,
            "scope": "Inventory of missing inputs in these prepared packets; not a global search or publication decision."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=ROOT)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args(argv)
    try:
        report = pending_report(args.repository, args.source_commit)
    except (Invalid, OSError, ValueError, TypeError, KeyError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"error": str(exc), "scope": "packet_preparation", "effects_authorized": False}), file=sys.stderr)
        return 2
    sys.stdout.buffer.write(encode(report))
    # A successfully prepared report can honestly say REVIEW_REQUIRED for every paper.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
