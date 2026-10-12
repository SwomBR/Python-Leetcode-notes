"""Tests for 028 Spiral Matrix."""
import copy
import random


def _reference(matrix):
    # Independent method: take the top row, rotate the rest counter-clockwise, repeat.
    grid = [list(row) for row in matrix]
    out = []
    while grid:
        out.extend(grid.pop(0))
        grid = [list(row) for row in zip(*grid)][::-1]
    return out


def _run(ns, matrix):
    return ns["Solution"]().spiralOrder(copy.deepcopy(matrix))


def check(ns):
    assert _run(ns, [[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert _run(ns, [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == \
        [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    assert _run(ns, [[7]]) == [7]
    assert _run(ns, [[1, 2, 3]]) == [1, 2, 3]
    assert _run(ns, [[1], [2], [3]]) == [1, 2, 3]
    assert _run(ns, [[1, 2], [3, 4], [5, 6]]) == [1, 2, 4, 6, 5, 3]
    assert _run(ns, [[1, 2, 3], [4, 5, 6]]) == [1, 2, 3, 6, 5, 4]
    assert _run(ns, [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]) == \
        [1, 2, 3, 6, 9, 12, 11, 10, 7, 4, 5, 8]
    rng = random.Random(28)
    for _ in range(400):
        m, n = rng.randint(1, 10), rng.randint(1, 10)
        matrix = [[rng.randint(-100, 100) for _ in range(n)] for _ in range(m)]
        assert _run(ns, matrix) == _reference(matrix), matrix
