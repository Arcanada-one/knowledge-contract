#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Public synthetic demonstration, not a replay of the three source books.

The four invented records expose the difference between reproducible base bytes
and explicit preservation of uncertainty. No model call or OCR is performed.
"""
import copy
import hashlib
import json


RECORDS = [
    {'id': 'invented-component', 'description': 'One component has a visible label.',
     'uncertain': 'The small suffix cannot be read.', 'generated': True, 'review_state': 'unreviewed'},
    {'id': 'invented-arrow', 'description': 'An arrow joins two boxes.',
     'uncertain': '', 'generated': True, 'review_state': 'unreviewed'},
    {'id': 'invented-scale', 'description': 'A scale contains three marks.',
     'uncertain': 'The unit of the scale is unknown.', 'generated': True, 'review_state': 'unreviewed'},
    {'id': 'invented-caption', 'description': 'The caption identifies one panel.',
     'uncertain': '', 'generated': True, 'review_state': 'unreviewed'},
]


def base_block(record):
    return ('## ' + record['id'] + '\n' + record['description'] + '\n\n').encode()


def project(records):
    output = bytearray()
    insertions = []
    for record in records:
        if not isinstance(record.get('uncertain'), str):
            raise ValueError('An explicit uncertainty string is required, including an empty one.')
        if record.get('generated') is not True or record.get('review_state') != 'unreviewed':
            raise ValueError('This demonstration covers generated, unreviewed inputs only.')
        output.extend(base_block(record))
        extra = b'Description status: generated; unreviewed.\n'
        if record['uncertain']:
            extra += ('Recorded uncertainty: ' + record['uncertain'] + '\n').encode()
        start = len(output)
        output.extend(extra)
        insertions.append({'id': record['id'], 'start_byte': start, 'end_byte': len(output)})
    return bytes(output), insertions


def main():
    original = copy.deepcopy(RECORDS)
    base = b''.join(map(base_block, RECORDS))
    output, trace = project(RECORDS)
    restored = bytearray(output)
    for insertion in reversed(trace):
        del restored[insertion['start_byte']:insertion['end_byte']]
    missing = copy.deepcopy(RECORDS)
    del missing[0]['uncertain']
    try:
        project(missing)
    except ValueError:
        missing_field_rejected = True
    else:
        missing_field_rejected = False
    nonempty = [r for r in RECORDS if r['uncertain']]
    checks = {
        'base_reconstruction_exact': base == b''.join(map(base_block, RECORDS)),
        'base_omits_both_recorded_uncertainties': all(r['uncertain'].encode() not in base for r in nonempty),
        'projection_preserves_both_exact_uncertainties': all(r['uncertain'].encode() in output for r in nonempty),
        'all_four_generated_unreviewed_markers_present': output.count(b'Description status: generated; unreviewed.') == 4,
        'inverse_removal_restores_base_bytes': bytes(restored) == base,
        'inputs_unchanged': RECORDS == original,
        'missing_uncertainty_field_rejected': missing_field_rejected,
    }
    report = {'schema': 'knowledge-contract.synthetic-uncertainty-projection/1',
              'records': 4, 'nonempty_uncertainties': 2, 'checks': checks,
              'passed': all(checks.values()), 'base_sha256': hashlib.sha256(base).hexdigest(),
              'projection_sha256': hashlib.sha256(output).hexdigest(), 'insertions': trace,
              'scope': 'New public synthetic illustration of a projection invariant; not a rerun of the historical three-book corpus and not an OCR or semantic-accuracy measurement.'}
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
