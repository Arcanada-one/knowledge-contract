# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Three bounded review probes; no edits to implementation or test sources."""
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))
from tools import semantic_relations as api

sources = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
           for p in [root/'tools/semantic_relations.py', root/'tools/test_semantic_relations.py']}
probes = []

# Distinct carrier sizes and a coherent intermediate dead end: exact algebraic
# successful-path composition must still hold, without a nonempty-path claim.
x = api.Partition(4, ({0, 1}, {2}, {3}))
y = api.Partition(5, ({0, 3}, {1}, {2, 4}))
z = api.Partition(3, ({0}, {1, 2}))
first = api.FiniteRelation(4, 5, {(0, 0), (1, 3), (2, 1), (2, 2), (2, 4)})
second = api.FiniteRelation(5, 3, {(0, 1), (3, 2), (1, 0)})
concrete = api.compose(first, second)
expected_concrete = frozenset({(0, 1), (1, 2), (2, 0)})
assert concrete.pairs == expected_concrete
actual_quotient = api.quotient_composition(first, second, x, y, z)
assert actual_quotient.pairs == frozenset({(0, 1), (1, 0)})
assert api.analyze_quotient(concrete, x, z).quotient == actual_quotient
probes.append({'name': 'different-carriers-with-coherent-dead-end', 'result': 'PASS',
               'carriers': [4, 5, 3], 'concrete_pairs': sorted(concrete.pairs),
               'quotient_pairs': sorted(actual_quotient.pairs),
               'all_branches_continue': False})

# Distinct exact metric scales and carrier sizes; the composition bound is
# analytically tight: L_F=3/5, L_G=35, L_composite=21.
def line_metric(points):
    return tuple(tuple(abs(a-b) for b in points) for a in points)
ma = line_metric((Fraction(0), Fraction(1, 3), Fraction(1)))
mb = line_metric((Fraction(0), Fraction(1, 5)))
mc = line_metric((Fraction(0), Fraction(2), Fraction(5), Fraction(9)))
f = ({0}, {0, 1}, {1})
g = ({0, 1}, {2, 3})
composed = api.compose_images(f, g)
assert composed == (frozenset({0, 1}), frozenset({0, 1, 2, 3}), frozenset({2, 3}))
lf = api.lipschitz_constant(f, ma, mb)
lg = api.lipschitz_constant(g, mb, mc)
lc = api.lipschitz_constant(composed, ma, mc)
assert (lf, lg, lc) == (Fraction(3, 5), Fraction(35), Fraction(21))
probes.append({'name': 'different-metric-scales-and-carriers', 'result': 'PASS',
               'carriers': [3, 2, 4], 'L_first': str(lf), 'L_second': str(lg),
               'L_composite': str(lc), 'bound_tight': lc == lf * lg})

# Stop the iterator ourselves after 13 already excessive rows. This avoids an
# unbounded reproduction: the sentinel shows whether the advertised carrier
# bound limits input consumption before materialization finishes.
class ReadBeyondCarrierBound(Exception):
    pass

consumed = 0
width = api.MAX_STATES + 1

def excessive_matrix_rows():
    global consumed
    for i in range(width):
        consumed += 1
        yield tuple(0 if i == j else 1 for j in range(width))
    consumed += 1
    raise ReadBeyondCarrierBound('validation requested another row after MAX_STATES+1 rows')

try:
    api.validate_metric(excessive_matrix_rows())
except Exception as error:
    outcome = type(error).__name__
else:
    outcome = 'ACCEPTED'
probes.append({'name': 'input-consumption-at-carrier-bound',
               'result': 'BOUND_NOT_ENFORCED' if outcome == 'ReadBeyondCarrierBound' else outcome,
               'maximum_carrier_states': api.MAX_STATES,
               'rows_or_sentinel_requested': consumed,
               'exception': outcome,
               'scope': 'MAX_STATES bounds accepted dimension, but does not bound iterable consumption before validation.'})
assert outcome == 'ReadBeyondCarrierBound'
assert consumed == api.MAX_STATES + 2

print(json.dumps({'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
                  'source_sha256': sources, 'probes': probes,
                  'limits': 'Three local review probes, same controller/model family/host. No claim of external independent review. The bounded sentinel is not a runtime safety proof.'},
                 indent=2, sort_keys=True))
