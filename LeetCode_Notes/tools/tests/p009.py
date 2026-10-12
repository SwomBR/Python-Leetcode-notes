"""Tests for 009 3Sum. Any order of triplets / of values inside a triplet is accepted."""
import itertools
import random


def _normalize(result):
    triplets = [tuple(sorted(t)) for t in result]
    assert all(len(t) == 3 for t in triplets), result
    assert len(triplets) == len(set(triplets)), f"duplicate triplets: {result}"
    return sorted(triplets)


def _reference(nums):
    found = set()
    for a, b, c in itertools.combinations(nums, 3):
        if a + b + c == 0:
            found.add(tuple(sorted((a, b, c))))
    return sorted(found)


def check(ns):
    solve = ns["Solution"]().threeSum
    assert _normalize(solve([-1, 0, 1, 2, -1, -4])) == [(-1, -1, 2), (-1, 0, 1)]
    assert _normalize(solve([0, 1, 1])) == []
    assert _normalize(solve([0, 0, 0])) == [(0, 0, 0)]
    assert _normalize(solve([0, 0, 0, 0])) == [(0, 0, 0)]
    assert _normalize(solve([-2, 0, 1, 1, 2])) == [(-2, 0, 2), (-2, 1, 1)]
    assert _normalize(solve([1, 2, 3])) == []
    assert _normalize(solve([-100000, 0, 100000])) == [(-100000, 0, 100000)]
    rng = random.Random(9)
    for _ in range(300):
        nums = [rng.randint(-6, 6) for _ in range(rng.randint(3, 12))]
        assert _normalize(solve(list(nums))) == _reference(nums), nums
