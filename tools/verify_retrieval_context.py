#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov
# SPDX-License-Identifier: Apache-2.0
"""Finite abstract checks for retrieval-and-context-composition/PAPER.md.

Original project verification code, derived from the paper's stated model.
This is a bounded author-side control: not independent scientific review,
not production verification, not a semantic validator, empirical benchmark
or proof. Python standard library only. Prints deterministic JSON; no network
writes. Default mode binds PAPER_SHA256 and PROTECTED digests. Title-only
mode (--title-only-against) proves a candidate differs from pinned accepted
bytes only in the explicit title-field allowlist below; it does not judge the
new name (naming canon is separate).

Title-field allowlist (every other byte, including all PROTECTED sections
except these fields, must stay identical):
  - front-matter key `title`
  - front-matter key `subtitle`
  - the single H1 line

Usage:
  python3 tools/verify_retrieval_context.py --paper <candidate PAPER.md>
  python3 tools/verify_retrieval_context.py --paper <candidate PAPER.md> \\
    --title-only-against <git-blob-id-or-path>
"""
from __future__ import annotations
import argparse
import difflib
import hashlib
import itertools
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path

PAPER_SHA256 = 'e457fadcb17424e15083504a2babb2646aedc8aec7370048cd77854a8c7af64f'
# Exact immutable source: ea0c30575d56e793fb2875df47126ab3f6dc30ad.
SOURCE_BLOB = '1163fcb4223023919f63f26876d1702de359a1aa'
SOURCE_SHA256 = '6ebbb43bcdd09ba44b60d6b0e4fce9ec05dcd1550f1d8c43bf451379508b6773'
PROTECTED = {'front_matter': 'dd777ba4289802fda9698b4e2b2e56ebcf87887a78f6e664ac6f6b36104f5ac5', 'references': '45206a6b93e46346a9560133d549cf9958eef772d30f6285b7a0831645c646fa', 'proposition_1': '6ba06755c29874daa0247e4413f1624f2d844e383ab53e6cbb0a7140fd93bbdf', 'proposition_2': '577922c726193a0cfcddcbef8bfa66b20b0ed2e88608a38d0d082571c6f85274', 'proposition_3': '6d530a2b812948bfa82a735e40cc38056f026bafae3fd7aa980b949b9effa308', 'joint_ground_counterexample': '069bd939c2e56a9b1afc53b7b417622fee64d141a2d00a782e5b83b1ab2489e8'}

# Explicit allowlist for --title-only-against. Do not widen silently.
TITLE_FIELD_ALLOWLIST = ('title', 'subtitle', 'h1')
TITLE_ONLY_RECORD = 'retrieval-context-title-only-projection/1'
SUPPORTED_TITLE_ONLY_VERSIONS = frozenset({'1'})
ACCEPTED_PAPER_BLOB = '9311c0d157d5a926e3c08f6a087a53866064f4e0'


def sha(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def block(text: str, start: str, end: str | None) -> str:
    i = text.index(start)
    return text[i:text.index(end, i) if end else len(text)]


def protected_blocks(text: str) -> dict[str, str]:
    return {
        'front_matter': text[:text.index('\n---\n', 4) + 5],
        'references': block(text, '## References', None),
        'proposition_1': block(text, 'Let \\(Z\\) be a finite', 'This establishes neither'),
        'proposition_2': block(text, 'Consider unit-cost, independent packages', '### Proposition 3.'),
        'proposition_3': block(text, 'Let \\(f\\) be a nonnegative', 'The result does not cover'),
        'joint_ground_counterexample': block(text, 'Joint grounds need not be submodular.', 'Feasible root selections'),
    }


def document_checks(path: Path) -> dict:
    data = path.read_bytes()
    text = data.decode('utf-8', errors='strict')
    checks = {name + '_exact': sha(value) == PROTECTED[name]
              for name, value in protected_blocks(text).items()}
    inline = re.findall(r'\\\((.*?)\\\)', text, re.S)
    display = re.findall(r'\\\[(.*?)\\\]', text, re.S)
    links = re.findall(r'\]\(([^)]+)\)|<(https?://[^>]+)>', text)
    headings = re.findall(r'^#{1,6} .+$', text, re.M)
    def fingerprint(items):
        return sha(json.dumps(items, ensure_ascii=False))
    checks.update({
        'original_inline_math_exact_order': fingerprint([x for x in inline if x != r'\operatorname{DeliveredSupports}(r,z)']) == '4e80c69fbd01cc5148a57939560ab0535dc92f5e943ed6b74ee4cd93672d3f63',
        'display_math_exact_order': fingerprint(display) == 'eceffa36fdaf13ff731085b0d2200a60c90eecccf6b931675aa0a39ca8c76314',
        'original_links_exact_order': fingerprint([x for x in links if x[0] != '../../reviews/retrieval-context/REVIEW.md']) == 'beee79279dca07706d0c401a5ba460d1ed44bfed8831d912df41774c1905b803',
        'old_headings_preserved': fingerprint([x for x in headings if x != '## 8. Conclusion']) == '642f5a00aad61704e6414cccc3e7cfec5d85a898990936968d236d016c6f4201',
    })
    checks.update({
        'exact_candidate': hashlib.sha256(data).hexdigest() == PAPER_SHA256,
        'utf8_lf_final_newline': not data.startswith(b'\xef\xbb\xbf') and b'\r' not in data and data.endswith(b'\n'),
        'one_title': len(re.findall(r'^# ', text, re.M)) == 1,
        'original_title': '# Retrieval, Coverage, and Context Composition under Resource Limits' in text,
        'delivered_support_explicit': '\\operatorname{DeliveredSupports}(r,z)' in text,
        'vector_budget_componentwise': 'interpreted componentwise' in text,
        'no_incumbent_without_candidate': 'there is no established incumbent' in text,
        'greedy_finite_domain': 'the ground set is finite' in text,
        'classical_result_attribution': 'not a new theorem of the present model' in text,
        'conclusion_present': '## 8. Conclusion' in text,
        'separate_verification_note': '../../reviews/retrieval-context/REVIEW.md' in text,
        'no_placeholders': not re.search(r'\b(?:TODO|FIXME|TBD)\b', text),
    })
    return {'checks': checks, 'passed': sum(checks.values()),
            'total': len(checks), 'pass': all(checks.values())}


def closure(roots: int, dependencies: tuple[int, ...]) -> int:
    """Bitset reachability; every dependency is an in-universe revision."""
    full = (1 << len(dependencies)) - 1
    if roots & ~full or any(mask & ~full for mask in dependencies):
        raise ValueError('required revision outside the declared universe')
    out = roots
    while True:
        expanded = out
        for i, mask in enumerate(dependencies):
            if out & (1 << i):
                expanded |= mask
        if expanded == out:
            return out
        out = expanded


def support(delivered: int, groups: tuple[tuple[int, bool | None], ...]) -> bool:
    """Each group is conjunctive; groups are alternatives. Unknown is not True."""
    return any(valid is True and (delivered & group) == group
               for group, valid in groups)


def representation_cost(delivered: int, weights: tuple[int, ...], overhead: int) -> int:
    return overhead + sum(w for i, w in enumerate(weights) if delivered & (1 << i))


def delivery_ok(roots: int, delivered: int, dependencies: tuple[int, ...],
                requirements: tuple[tuple[tuple[int, bool | None], ...], ...],
                weights: tuple[int, ...], overhead: int, budget: int) -> bool:
    """No-transform exact-delivery profile: never re-inflate the actual output."""
    needed = closure(roots, dependencies)
    return ((needed & delivered) == needed
            and all(support(delivered, groups) for groups in requirements)
            and representation_cost(delivered, weights, overhead) <= budget)


def solve(dependencies: tuple[int, ...], groups: tuple[int, int], overhead: int,
          budget: int, limit: int | None = None) -> tuple[str, int | None]:
    """Minimize rendered cost in the explicitly finite, identity-rendered space."""
    size = 1 << len(dependencies)
    best = None
    for roots in range(size):
        if limit is not None and roots >= limit:
            return 'incomplete', best
        delivered = closure(roots, dependencies)
        cost = representation_cost(delivered, (1, 2, 3), overhead)
        if cost <= budget and all(delivered & group == group for group in groups):
            best = cost if best is None else min(best, cost)
    return ('infeasible_in_declared_space' if best is None else 'optimal_in_declared_space', best)


def exact_selection_model() -> dict:
    """Independent oracle enumerates closed delivered sets, not root closures."""
    edges = tuple((i, j) for i in range(3) for j in range(3) if i != j)
    cases = feasible = infeasible = 0
    for edge_bits in range(1 << len(edges)):
        deps = [0, 0, 0]
        for e, (i, j) in enumerate(edges):
            if edge_bits & (1 << e):
                deps[i] |= 1 << j
        deps = tuple(deps)
        closed = [d for d in range(8)
                  if all(not (d & (1 << i)) or d & deps[i] == deps[i] for i in range(3))]
        for g1, g2 in itertools.product(range(1, 8), repeat=2):
            for overhead, budget in itertools.product((0, 1), range(8)):
                status, value = solve(deps, (g1, g2), overhead, budget)
                oracle_values = [representation_cost(d, (1, 2, 3), overhead)
                                 for d in closed if d & g1 == g1 and d & g2 == g2]
                oracle_values = [c for c in oracle_values if c <= budget]
                expected = min(oracle_values) if oracle_values else None
                if value != expected or (status == 'optimal_in_declared_space') != bool(oracle_values):
                    raise AssertionError((deps, g1, g2, overhead, budget, value, expected))
                cases += 1
                feasible += bool(oracle_values)
                infeasible += not oracle_values
    return {'carrier': '3 revisions; 64 loop-free directed graphs (cycles allowed); two nonempty conjunctive groups',
            'cost_profile': 'revision costs (1,2,3); fixed overhead 0 or 1; scalar budget 0..7; identity render',
            'unit': 'graph/group-pair/overhead/budget instance', 'instances': cases,
            'feasible_instances': feasible, 'infeasible_instances': infeasible,
            'root_decisions_per_instance': 8, 'disagreements_with_closed_set_oracle': 0}


def all_greedy_values(masks: tuple[int, ...], weights: tuple[int, ...], k: int) -> set[int]:
    def value(roots: int) -> int:
        covered = 0
        for i, mask in enumerate(masks):
            if roots & (1 << i):
                covered |= mask
        return sum(w for j, w in enumerate(weights) if covered & (1 << j))
    states = {0}
    for _ in range(k):
        next_states = set()
        for roots in states:
            candidates = [i for i in range(3) if not roots & (1 << i)]
            gains = {i: value(roots | (1 << i)) - value(roots) for i in candidates}
            best = max(gains.values())
            next_states.update(roots | (1 << i) for i in candidates if gains[i] == best)
        states = next_states
    return {value(roots) for roots in states}


def greedy_model() -> dict:
    instances = tie_outcomes = 0
    for masks in itertools.product(range(8), repeat=3):
        for weights in ((1, 1, 1), (1, 2, 3)):
            def value(roots: int) -> int:
                union = 0
                for i, mask in enumerate(masks):
                    if roots & (1 << i):
                        union |= mask
                return sum(w for j, w in enumerate(weights) if union & (1 << j))
            for k in (1, 2, 3):
                optimum = max(value(s) for s in range(8) if s.bit_count() <= k)
                factor = 1 - Fraction(k - 1, k) ** k
                values = all_greedy_values(masks, weights, k)
                if not all(Fraction(v) >= factor * optimum for v in values):
                    raise AssertionError((masks, weights, k, values, optimum))
                instances += 1
                tie_outcomes += len(values)
    return {'carrier': '3 selectable sets over 3 features; all 512 incidence matrices; two nonnegative weight profiles',
            'unit': 'incidence/weight/cardinality instance', 'instances': instances,
            'all_tie_resolutions_checked': True, 'distinct_value_outcomes_across_instances': tie_outcomes,
            'arithmetic': 'exact rational cardinality bound', 'violations': 0,
            'limit': 'weighted coverage subclass only, not all submodular functions or knapsack policies'}


def boundary_controls() -> dict:
    deps = (2, 0, 0)  # root 0 needs condition 1
    req = (((3, True),),)
    w = (2, 3, 1)
    tests = {
        'full_delivery_passes': delivery_ok(1, 3, deps, req, w, 0, 5),
        'truncated_exception_rejected': not delivery_ok(1, 1, deps, req, w, 0, 5),
        'dependency_root_removal_not_delivery_removal': closure(1, deps) == closure(3, deps),
        'unknown_group_not_passed': not support(3, ((3, None),)),
        'invalid_group_not_passed': not support(3, ((3, False),)),
        'alternative_valid_group_suffices': support(4, ((3, True), (4, True))),
        'joint_group_needs_both': not support(1, ((3, True),)) and support(3, ((3, True),)),
        'cyclic_closure_terminates': closure(1, (2, 1, 0)) == 3,
        'shared_dependency_charged_once': representation_cost(7, (1, 1, 3), 0) == 5,
        'format_overhead_can_break_budget': not delivery_ok(1, 3, deps, req, w, 1, 5),
        'mandatory_coverage_not_downward_closed': support(1, ((1, True),)) and not support(0, ((1, True),)),
        'joint_support_violates_diminishing_returns': int(support(2, ((3, True),))) == 0 and int(support(3, ((3, True),))) == 1,
        'early_stop_without_incumbent_is_incomplete': solve((0, 0, 0), (1, 1), 0, 5, 1) == ('incomplete', None),
        'early_stop_with_incumbent_not_optimal': solve((0, 0, 0), (1, 1), 0, 5, 2) == ('incomplete', 1),
        'complete_infeasibility_has_declared_scope': solve((0, 0, 0), (1, 1), 0, 0) == ('infeasible_in_declared_space', None),
        'vector_budget_not_compensated_by_other_units': not all(x <= y for x, y in zip((4, 6), (5, 5))),
    }
    try:
        closure(1, (8, 0, 0))
    except ValueError:
        tests['missing_dependency_rejected'] = True
    else:
        tests['missing_dependency_rejected'] = False
    # Deliberate faulty alternatives, each evaluated on its discriminating fixture.
    mutants = {
        'closure_only_accepts_truncated_delivery': support(closure(1, deps), req[0]) != delivery_ok(1, 1, deps, req, w, 0, 5),
        'double_counts_shared_dependency': (4 + 4 <= 5) != (representation_cost(7, (1, 1, 3), 0) <= 5),
        'ignores_render_overhead': delivery_ok(1, 3, deps, req, w, 0, 5) != delivery_ok(1, 3, deps, req, w, 1, 5),
        'unknown_treated_as_valid': support(3, ((3, True),)) != support(3, ((3, None),)),
        'early_stop_called_infeasible': ('infeasible_in_declared_space', None) != solve((0, 0, 0), (1, 1), 0, 5, 1),
        'adds_incommensurate_budgets': (4 + 6 <= 5 + 5) != all(x <= y for x, y in zip((4, 6), (5, 5))),
    }
    if not all(tests.values()) or not all(mutants.values()):
        raise AssertionError((tests, mutants))
    return {'checks': tests, 'passed': len(tests), 'total': len(tests),
            'deliberate_faulty_alternatives_distinguished': mutants,
            'mutation_scope': 'six explicit faulty alternatives in this abstract harness, not production code mutations'}


def load_reference_bytes(spec: str) -> tuple[bytes | None, str | None]:
    """Load accepted bytes from a git blob id or a filesystem path."""
    path = Path(spec)
    if path.is_file():
        return path.read_bytes(), None
    try:
        data = subprocess.check_output(['git', 'cat-file', '-p', spec], stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        detail = exc.output.decode('utf-8', errors='replace') if isinstance(exc, subprocess.CalledProcessError) else str(exc)
        return None, detail.strip() or 'unknown source'
    return data, None


def split_document(text: str) -> tuple[str, str, str]:
    """Return (front_matter_inner, body_including_closing_fence_consumed, remainder_after_fm)."""
    if not text.startswith('---\n'):
        raise ValueError('missing front matter opening fence')
    end = text.index('\n---\n', 4)
    inner = text[4:end]
    remainder = text[end + 5:]
    return inner, text[: end + 5], remainder


def project_title_fields(text: str) -> tuple[str, dict[str, str | None]]:
    """Strip allowlisted title/subtitle keys and normalize H1; return projected text and values.

    Allowlisted front-matter keys are removed entirely so that adding, removing or
    changing `title` / `subtitle` does not affect the residual. Every other
    front-matter line and every non-H1 body byte must still match exactly.
    """
    inner, _fm, remainder = split_document(text)
    observed: dict[str, str | None] = {'title': None, 'subtitle': None, 'h1': None}
    projected_lines: list[str] = []
    for line in inner.splitlines(keepends=True):
        matched = re.match(r'^(title|subtitle):\s*(.*)$', line.rstrip('\n'))
        if matched:
            observed[matched.group(1)] = matched.group(2)
            continue
        projected_lines.append(line if line.endswith('\n') else line + '\n')
    body_lines: list[str] = []
    h1_seen = False
    for line in remainder.splitlines(keepends=True):
        if not h1_seen and re.match(r'^# ', line):
            observed['h1'] = line.rstrip('\n')
            body_lines.append('# __TITLE_ONLY_H1__\n')
            h1_seen = True
        else:
            body_lines.append(line if line.endswith('\n') else line + '\n')
    projected = '---\n' + ''.join(projected_lines) + '---\n' + ''.join(body_lines)
    return projected, observed


def section_name_for_line(text: str, line_no: int) -> str:
    lines = text.splitlines()
    if line_no <= 0 or line_no > len(lines):
        return 'out_of_range'
    # Front matter occupies lines until the closing --- after the opening fence.
    try:
        _inner, fm, _rem = split_document(text)
    except ValueError:
        fm = ''
    fm_line_count = fm.count('\n')
    if line_no <= fm_line_count:
        return 'front_matter'
    prefix = '\n'.join(lines[:line_no])
    heading = None
    for match in re.finditer(r'^(#{1,6}) (.+)$', prefix, re.M):
        heading = match.group(0)
    if heading is None:
        return 'preamble'
    if heading.startswith('# ') and not heading.startswith('## '):
        return 'h1'
    lowered = heading.lower()
    if 'references' in lowered:
        return 'references'
    if 'proposition 1' in lowered:
        return 'proposition_1'
    if 'proposition 2' in lowered:
        return 'proposition_2'
    if 'proposition 3' in lowered:
        return 'proposition_3'
    if 'joint' in lowered and 'ground' in lowered:
        return 'joint_ground_counterexample'
    return heading.lstrip('#').strip()


def differing_regions(accepted: str, candidate: str) -> list[dict]:
    """Line-oriented residual differences after title projection (not a semantic judgment)."""
    a_lines = accepted.splitlines()
    c_lines = candidate.splitlines()
    regions: list[dict] = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a_lines, b=c_lines).get_opcodes():
        if tag == 'equal':
            continue
        sections = sorted({
            *(section_name_for_line(accepted, i + 1) for i in range(i1, max(i1 + 1, i2))),
            *(section_name_for_line(candidate, j + 1) for j in range(j1, max(j1 + 1, j2))),
        })
        regions.append({
            'op': tag,
            'accepted_lines': [i1 + 1, i2],
            'candidate_lines': [j1 + 1, j2],
            'sections': sections,
        })
    return regions


def title_fields_changed(accepted_obs: dict[str, str | None],
                         candidate_obs: dict[str, str | None]) -> list[str]:
    changed = []
    for key in TITLE_FIELD_ALLOWLIST:
        if accepted_obs.get(key) != candidate_obs.get(key):
            changed.append(key)
    return changed


def protected_body_digests(text: str) -> dict[str, str]:
    """PROTECTED digests with allowlisted title fields projected out of front_matter."""
    projected, _ = project_title_fields(text)
    blocks = protected_blocks(projected)
    return {name: sha(value) for name, value in blocks.items()}


def title_only_report(candidate_path: Path, against: str, version: str) -> dict:
    record = {
        'record_type': TITLE_ONLY_RECORD,
        'title_field_allowlist': list(TITLE_FIELD_ALLOWLIST),
        'title_only_version': version,
        'against': against,
        'candidate_path': str(candidate_path),
        'accepted_paper_blob': ACCEPTED_PAPER_BLOB,
        'source_sha256': SOURCE_SHA256,
        'not_established': [
            'independent scientific review',
            'production verification',
            'naming-canon acceptance of the new title',
            'semantic annotation correctness',
            'site deployment',
        ],
    }
    if version not in SUPPORTED_TITLE_ONLY_VERSIONS:
        record.update({'pass': False, 'refusal_reason': 'unsupported_version'})
        return record
    accepted_raw, err = load_reference_bytes(against)
    if accepted_raw is None:
        record.update({'pass': False, 'refusal_reason': 'unknown_source', 'detail': err})
        return record
    try:
        candidate_raw = candidate_path.read_bytes()
        candidate_text = candidate_raw.decode('utf-8', errors='strict')
        accepted_text = accepted_raw.decode('utf-8', errors='strict')
    except (OSError, UnicodeDecodeError) as exc:
        record.update({'pass': False, 'refusal_reason': 'corrupted_candidate', 'detail': str(exc)})
        return record
    try:
        accepted_projected, accepted_obs = project_title_fields(accepted_text)
        candidate_projected, candidate_obs = project_title_fields(candidate_text)
    except (ValueError, IndexError) as exc:
        record.update({'pass': False, 'refusal_reason': 'corrupted_candidate', 'detail': str(exc)})
        return record
    record['candidate_sha256'] = hashlib.sha256(candidate_raw).hexdigest()
    record['accepted_sha256'] = hashlib.sha256(accepted_raw).hexdigest()
    record['title_fields_observed'] = {
        'accepted': accepted_obs,
        'candidate': candidate_obs,
    }
    record['title_fields_changed'] = title_fields_changed(accepted_obs, candidate_obs)
    # Body identity: projected documents must match exactly.
    if accepted_projected != candidate_projected:
        record.update({
            'pass': False,
            'refusal_reason': 'incomplete_mapping',
            'differing_regions': differing_regions(accepted_text, candidate_text),
            'protected_digests_after_title_projection': {
                'accepted': protected_body_digests(accepted_text),
                'candidate': protected_body_digests(candidate_text),
            },
        })
        return record
    # Finite harness still runs; it does not depend on manuscript title bytes.
    record.update({
        'pass': True,
        'refusal_reason': None,
        'differing_regions': [],
        'selection': exact_selection_model(),
        'greedy': greedy_model(),
        'boundaries': boundary_controls(),
    })
    return record


def full_report(paper: Path) -> dict:
    report = {'record_type': 'retrieval-context-finite-verification/1',
              'candidate_sha256': PAPER_SHA256, 'source_sha256': SOURCE_SHA256,
              'document': document_checks(paper),
              'selection': exact_selection_model(), 'greedy': greedy_model(),
              'boundaries': boundary_controls(),
              'not_established': ['general proofs by enumeration', 'semantic annotation correctness',
                                  'production selector conformance', 'human comprehension',
                                  'editorial superiority', 'repository-wide CI', 'site deployment',
                                  'independent scientific review', 'production verification']}
    report['pass'] = report['document']['pass']
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--paper', type=Path, default=Path(__file__).resolve().parents[1] / 'papers/retrieval-and-context-composition/PAPER.md')
    parser.add_argument('--title-only-against', default=None,
                        help='Git blob id or path of the pinned accepted paper bytes')
    parser.add_argument('--title-only-version', default='1',
                        help='Title-only projection schema version (supported: 1)')
    args = parser.parse_args()
    if args.title_only_against is not None:
        report = title_only_report(args.paper, args.title_only_against, args.title_only_version)
    else:
        report = full_report(args.paper)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report.get('pass') else 1


if __name__ == '__main__':
    raise SystemExit(main())
