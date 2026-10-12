"""Tests for 064 Unique Paths."""
import itertools
import random


def _reference(m, n):
    """Count distinct arrangements of (m-1) 'D' moves among m+n-2 moves by enumeration."""
    moves = m + n - 2
    return sum(1 for _ in itertools.combinations(range(moves), m - 1))


def check(ns):
    solve = ns["Solution"]().uniquePaths
    assert solve(3, 7) == 28
    assert solve(3, 2) == 3
    assert solve(1, 1) == 1
    assert solve(1, 9) == 1
    assert solve(9, 1) == 1
    assert solve(2, 2) == 2
    assert solve(3, 3) == 6
    assert solve(7, 3) == 28
    rng = random.Random(64)
    for _ in range(80):
        m, n = rng.randint(1, 8), rng.randint(1, 8)
        assert solve(m, n) == _reference(m, n), (m, n)
