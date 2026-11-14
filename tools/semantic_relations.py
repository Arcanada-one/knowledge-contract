# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Finite observation quotients and geometry for set-valued transformations.

This module models successful relation edges on explicit finite carriers. An
empty image is not an observed refusal, unknown result, termination guarantee,
or permission. Quotient coherence and metric bounds establish only the supplied
mathematical profile; they do not authenticate observations or admit knowledge.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

MAX_STATES = 12


def _size(value):
    if type(value) is not int or not 1 <= value <= MAX_STATES:
        raise ValueError(f"carrier size must be an integer in 1..{MAX_STATES}")
    return value


def _states(values, size, *, nonempty=False):
    values = tuple(values)
    if any(type(x) is not int or not 0 <= x < size for x in values):
        raise ValueError("state outside its declared finite carrier")
    result = frozenset(values)
    if nonempty and not result:
        raise ValueError("a nonempty image is required for this metric profile")
    return result


@dataclass(frozen=True)
class Partition:
    size: int
    blocks: tuple[frozenset[int], ...]

    def __post_init__(self):
        _size(self.size)
        blocks = tuple(_states(b, self.size, nonempty=True) for b in self.blocks)
        covered = set()
        for block in blocks:
            if covered.intersection(block):
                raise ValueError("observation classes overlap")
            covered.update(block)
        if covered != set(range(self.size)):
            raise ValueError("observation classes must cover the whole carrier")
        object.__setattr__(self, "blocks", blocks)

    def class_of(self, state):
        if type(state) is not int or not 0 <= state < self.size:
            raise ValueError("state outside partition carrier")
        return next(i for i, block in enumerate(self.blocks) if state in block)


@dataclass(frozen=True)
class FiniteRelation:
    source_size: int
    target_size: int
    pairs: frozenset[tuple[int, int]]

    def __post_init__(self):
        _size(self.source_size)
        _size(self.target_size)
        pairs = tuple(tuple(pair) for pair in self.pairs)
        for pair in pairs:
            if len(pair) != 2:
                raise ValueError("a relation edge needs two endpoints")
            x, y = pair
            _states((x,), self.source_size)
            _states((y,), self.target_size)
        object.__setattr__(self, "pairs", frozenset(pairs))

    def image(self, state):
        _states((state,), self.source_size)
        return frozenset(y for x, y in self.pairs if x == state)


@dataclass(frozen=True)
class QuotientAnalysis:
    coherent: bool
    quotient: FiniteRelation | None
    witness: dict | None


def compose(first: FiniteRelation, second: FiniteRelation):
    """Successful-path composition: first followed by second."""
    if first.target_size != second.source_size:
        raise ValueError("intermediate relation carriers disagree")
    pairs = frozenset((x, z) for x, y in first.pairs
                      for other_y, z in second.pairs if y == other_y)
    return FiniteRelation(first.source_size, second.target_size, pairs)


def _profile(relation, source, target):
    if source.size != relation.source_size or target.size != relation.target_size:
        raise ValueError("relation and observation carriers disagree")


def existential_quotient(relation, source, target):
    """Coarse existential abstraction, which need not preserve composition.

    This is always a relation on classes. It is not a certificate of exact
    behavior for every representative of an input class.
    """
    _profile(relation, source, target)
    pairs = frozenset((source.class_of(x), target.class_of(y))
                      for x, y in relation.pairs)
    return FiniteRelation(len(source.blocks), len(target.blocks), pairs)


def analyze_quotient(relation, source, target):
    """Check equality of reachable output classes, including empty images."""
    _profile(relation, source, target)
    images = tuple(frozenset(target.class_of(y) for y in relation.image(x))
                   for x in range(source.size))
    for class_index, block in enumerate(source.blocks):
        representative = min(block)
        for other in sorted(block):
            if images[representative] != images[other]:
                return QuotientAnalysis(False, None, {
                    "input_class": class_index,
                    "representatives": [representative, other],
                    "reachable_classes": [sorted(images[representative]), sorted(images[other])],
                    "empty_images": [not images[representative], not images[other]],
                })
    return QuotientAnalysis(True, existential_quotient(relation, source, target), None)


def quotient_composition(first, second, source, middle, target):
    """Compose exact observation quotients under the stated coherence rule.

    Refusal says that this sufficient exact-profile obligation was not met.
    An incoherent pair can accidentally have the same coarse composite; this
    function does not claim to characterize every such accidental equality.
    """
    if first.target_size != second.source_size:
        raise ValueError("intermediate relation carriers disagree")
    left = analyze_quotient(first, source, middle)
    right = analyze_quotient(second, middle, target)
    if not left.coherent or not right.coherent:
        raise ValueError("reachable observation classes depend on representative")
    return compose(left.quotient, right.quotient)


def validate_metric(matrix):
    """Validate a finite exact rational metric, including separation."""
    matrix = tuple(tuple(row) for row in matrix)
    _size(len(matrix))
    if any(len(row) != len(matrix) for row in matrix):
        raise ValueError("metric matrix must be square")
    if any(type(value) is not int and not isinstance(value, Fraction)
           for row in matrix for value in row):
        raise ValueError("metric distances must be exact integers or Fractions")
    normalized = tuple(tuple(Fraction(value) for value in row) for row in matrix)
    return _checked_metric(normalized)


@lru_cache(maxsize=32)
def _checked_metric(matrix):
    size = len(matrix)
    for x in range(size):
        for y in range(size):
            distance = matrix[x][y]
            if distance < 0 or distance != matrix[y][x]:
                raise ValueError("metric needs nonnegative symmetric distances")
            if (distance == 0) != (x == y):
                raise ValueError("metric requires zero exactly on identical states")
            if any(distance > matrix[x][z] + matrix[z][y] for z in range(size)):
                raise ValueError("metric triangle inequality fails")
    return matrix


def hausdorff(left, right, metric):
    metric = validate_metric(metric)
    left = _states(left, len(metric), nonempty=True)
    right = _states(right, len(metric), nonempty=True)
    forward = max(min(metric[x][y] for y in right) for x in left)
    backward = max(min(metric[x][y] for x in left) for y in right)
    return max(forward, backward)


def _images(images, target_size):
    _size(len(images))
    return tuple(_states(image, target_size, nonempty=True) for image in images)


def lipschitz_constant(images, source_metric, target_metric):
    """Least finite bound for this fully supplied, nonempty-valued map."""
    source_metric = validate_metric(source_metric)
    target_metric = validate_metric(target_metric)
    images = _images(images, len(target_metric))
    if len(images) != len(source_metric):
        raise ValueError("source metric and image inventory disagree")
    ratios = (hausdorff(images[x], images[y], target_metric) / source_metric[x][y]
              for x in range(len(images)) for y in range(x + 1, len(images)))
    return max(ratios, default=Fraction(0))


def compose_images(first_images, second_images):
    """Union composition of two explicitly nonempty-valued finite maps.

    The target carrier of the second map is not supplied here. Endpoint
    integrality/nonnegativity and the global finite bound are checked; the
    caller's metric supplies and validates its exact target size later.
    """
    second_images = _images(second_images, MAX_STATES)
    first_images = _images(first_images, len(second_images))
    return tuple(frozenset(z for y in image for z in second_images[y])
                 for image in first_images)
