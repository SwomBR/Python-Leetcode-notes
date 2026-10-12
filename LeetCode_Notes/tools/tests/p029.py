"""Tests for 029 Rotate Image (in place, returns None)."""
import copy
import random


def _reference(matrix):
    n = len(matrix)
    # Clockwise rotation: new[i][j] = old[n - 1 - j][i]
    return [[matrix[n - 1 - j][i] for j in range(n)] for i in range(n)]


def _run(ns, matrix):
    grid = copy.deepcopy(matrix)
    result = ns["Solution"]().rotate(grid)
    assert result is None, "rotate must return None"
    return grid


def check(ns):
    assert _run(ns, [[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    assert _run(ns, [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]) == \
        [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]
    assert _run(ns, [[42]]) == [[42]]
    assert _run(ns, [[1, 2], [3, 4]]) == [[3, 1], [4, 2]]
    assert _run(ns, [[-1000, 1000], [0, -1000]]) == [[0, -1000], [-1000, 1000]]
    rng = random.Random(29)
    for _ in range(300):
        n = rng.randint(1, 20)
        matrix = [[rng.randint(-1000, 1000) for _ in range(n)] for _ in range(n)]
        assert _run(ns, matrix) == _reference(matrix), matrix
    # Four clockwise rotations bring the matrix back to the start.
    matrix = [[rng.randint(-1000, 1000) for _ in range(5)] for _ in range(5)]
    grid = copy.deepcopy(matrix)
    for _ in range(4):
        ns["Solution"]().rotate(grid)
    assert grid == matrix
