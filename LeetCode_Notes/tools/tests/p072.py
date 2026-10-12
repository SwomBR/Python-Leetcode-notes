"""Tests for 072 Graph Valid Tree (LeetCode 261, Premium)."""
import random


def _reference(n, edges):
    """Independent reference: label propagation + edge count."""
    if len(edges) != n - 1:
        return False
    label = list(range(n))
    changed = True
    while changed:
        changed = False
        for a, b in edges:
            low = min(label[a], label[b])
            if label[a] != low or label[b] != low:
                label[a] = label[b] = low
                changed = True
    return len(set(label)) == 1


def check(ns):
    solve = ns["Solution"]().validTree
    # Commonly published examples
    assert solve(5, [[0, 1], [0, 2], [0, 3], [1, 4]]) is True
    assert solve(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) is False
    # Edge cases
    assert solve(1, []) is True
    assert solve(2, []) is False
    assert solve(2, [[1, 0]]) is True
    assert solve(4, [[0, 1], [2, 3]]) is False            # forest, n-2 edges
    assert solve(4, [[0, 1], [1, 2], [2, 0]]) is False     # n-1 edges but cycle + isolated 3
    assert solve(3, [[0, 1], [1, 2], [2, 0]]) is False     # too many edges (cycle)
    assert solve(6, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]) is True  # path
    rng = random.Random(72)
    for _ in range(400):
        n = rng.randint(1, 8)
        pairs = [[a, b] for a in range(n) for b in range(a + 1, n)]
        rng.shuffle(pairs)
        if rng.random() < 0.5 and n > 1:
            # build a random tree, optionally perturb it
            edges = [[rng.randrange(i), i] for i in range(1, n)]
            perm = list(range(n))
            rng.shuffle(perm)
            edges = [[perm[a], perm[b]] for a, b in edges]
            if rng.random() < 0.4 and edges:
                edges.pop(rng.randrange(len(edges)))
        else:
            edges = pairs[: rng.randint(0, len(pairs))]
        edges = [e[::-1] if rng.random() < 0.5 else e for e in edges]
        assert solve(n, [list(e) for e in edges]) == _reference(n, edges), (n, edges)
