"""Tests for 068 Pacific Atlantic Water Flow (LeetCode 417). Result order is free."""
import copy
import random


def _reference(h):
    """Fixed-point iteration: a cell reaches an ocean if it borders it or can step
    to an equal-or-lower neighbour that already reaches it."""
    m, n = len(h), len(h[0])
    pac = [[r == 0 or c == 0 for c in range(n)] for r in range(m)]
    atl = [[r == m - 1 or c == n - 1 for c in range(n)] for r in range(m)]
    changed = True
    while changed:
        changed = False
        for r in range(m):
            for c in range(n):
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and h[nr][nc] <= h[r][c]:
                        if pac[nr][nc] and not pac[r][c]:
                            pac[r][c] = changed = True
                        if atl[nr][nc] and not atl[r][c]:
                            atl[r][c] = changed = True
    return sorted([r, c] for r in range(m) for c in range(n) if pac[r][c] and atl[r][c])


def _norm(result):
    return sorted([list(x) for x in result])


def check(ns):
    def solve(h):
        return ns["Solution"]().pacificAtlantic(copy.deepcopy(h))

    ex1 = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
    assert _norm(solve(ex1)) == [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
    assert _norm(solve([[1]])) == [[0, 0]]
    assert _norm(solve([[1, 2, 3]])) == [[0, 0], [0, 1], [0, 2]]       # single row
    assert _norm(solve([[3], [2], [1]])) == [[0, 0], [1, 0], [2, 0]]   # single column
    assert _norm(solve([[5, 5], [5, 5]])) == [[0, 0], [0, 1], [1, 0], [1, 1]]
    assert _norm(solve([[1, 1, 1], [1, 0, 1], [1, 1, 1]])) == [
        [0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]
    rng = random.Random(68)
    for _ in range(300):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        h = [[rng.randint(0, 4) for _ in range(n)] for _ in range(m)]
        assert _norm(solve(h)) == _reference(h), h
