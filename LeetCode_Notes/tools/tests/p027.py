"""Tests for 027 Set Matrix Zeroes (in place, returns None)."""
import copy
import random


def _reference(matrix):
    m, n = len(matrix), len(matrix[0])
    zero_rows = {i for i in range(m) for j in range(n) if matrix[i][j] == 0}
    zero_cols = {j for i in range(m) for j in range(n) if matrix[i][j] == 0}
    return [[0 if (i in zero_rows or j in zero_cols) else matrix[i][j]
             for j in range(n)] for i in range(m)]


def _run(ns, matrix):
    grid = copy.deepcopy(matrix)
    result = ns["Solution"]().setZeroes(grid)
    assert result is None, "setZeroes must return None"
    return grid


def check(ns):
    assert _run(ns, [[1, 1, 1], [1, 0, 1], [1, 1, 1]]) == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    assert _run(ns, [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]) == \
        [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
    assert _run(ns, [[5]]) == [[5]]
    assert _run(ns, [[0]]) == [[0]]
    assert _run(ns, [[1, 0, 3]]) == [[0, 0, 0]]
    assert _run(ns, [[1], [0], [3]]) == [[0], [0], [0]]
    assert _run(ns, [[1, 2], [3, 4]]) == [[1, 2], [3, 4]]
    assert _run(ns, [[1, 0], [1, 1], [0, 1]]) == [[0, 0], [0, 0], [0, 0]]
    assert _run(ns, [[1, 2, 3], [4, 0, 6], [7, 8, 9], [0, 1, 1]]) == \
        [[0, 0, 3], [0, 0, 0], [0, 0, 9], [0, 0, 0]]
    assert _run(ns, [[2**31 - 1, -2**31], [0, 7]]) == [[0, -2**31], [0, 0]]
    rng = random.Random(27)
    for _ in range(500):
        m, n = rng.randint(1, 7), rng.randint(1, 7)
        p = rng.choice([0.05, 0.15, 0.3])
        matrix = [[0 if rng.random() < p else rng.randint(-5, 5) for _ in range(n)]
                  for _ in range(m)]
        assert _run(ns, matrix) == _reference(matrix), matrix
