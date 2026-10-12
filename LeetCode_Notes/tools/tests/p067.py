"""Tests for 067 Course Schedule (LeetCode 207)."""
import random


def _reference(n, prereqs):
    """Transitive closure (Floyd-Warshall style): impossible iff some course reaches itself."""
    reach = [[False] * n for _ in range(n)]
    for a, b in prereqs:
        reach[b][a] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    return not any(reach[i][i] for i in range(n))


def check(ns):
    solve = ns["Solution"]().canFinish
    assert solve(2, [[1, 0]]) is True              # Example 1
    assert solve(2, [[1, 0], [0, 1]]) is False     # Example 2
    assert solve(1, []) is True
    assert solve(3, []) is True
    assert solve(1, [[0, 0]]) is False             # self-loop
    assert solve(3, [[1, 0], [2, 1], [0, 2]]) is False
    assert solve(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True   # diamond
    assert solve(5, [[1, 0], [0, 1], [3, 2], [4, 3]]) is False  # cycle in one component
    chain = [[i + 1, i] for i in range(1999)]
    assert solve(2000, [list(p) for p in chain]) is True        # long chain
    assert solve(2000, [list(p) for p in chain] + [[0, 1999]]) is False
    rng = random.Random(67)
    for _ in range(400):
        n = rng.randint(1, 8)
        pairs = {(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 12))}
        if rng.random() < 0.7:          # make self-loops rarer
            pairs = {p for p in pairs if p[0] != p[1]}
        prereqs = [list(p) for p in pairs]
        expected = _reference(n, prereqs)
        assert solve(n, [list(p) for p in prereqs]) is expected, (n, prereqs)
