"""Tests for 073 Number of Connected Components in an Undirected Graph
(LeetCode 323, Premium)."""
import random


def _reference(n, edges):
    """Independent reference: merge explicit sets of nodes."""
    groups = [{v} for v in range(n)]
    for a, b in edges:
        ga = next(g for g in groups if a in g)
        gb = next(g for g in groups if b in g)
        if ga is not gb:
            groups.remove(gb)
            ga |= gb
    return len(groups)


def check(ns):
    solve = ns["Solution"]().countComponents
    # Commonly published examples
    assert solve(5, [[0, 1], [1, 2], [3, 4]]) == 2
    assert solve(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1
    # Edge cases
    assert solve(1, []) == 1
    assert solve(4, []) == 4
    assert solve(3, [[0, 1], [1, 2], [0, 2]]) == 1       # cycle
    assert solve(6, [[0, 1], [2, 3], [4, 5]]) == 3
    assert solve(4, [[2, 3]]) == 3
    rng = random.Random(73)
    for _ in range(400):
        n = rng.randint(1, 10)
        pairs = [[a, b] for a in range(n) for b in range(a + 1, n)]
        rng.shuffle(pairs)
        edges = pairs[: rng.randint(0, min(len(pairs), n + 2))]
        assert solve(n, [list(e) for e in edges]) == _reference(n, edges), (n, edges)
    # A larger case (long chain) to catch recursion / efficiency problems
    n = 2000
    edges = [[i, i + 1] for i in range(0, n - 1) if i != 999]
    assert solve(n, edges) == 2
