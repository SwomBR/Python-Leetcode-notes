"""Tests for 017 Merge Intervals."""
import copy
import random


def _reference(intervals):
    """Independent reference: paint doubled coordinates, then read off runs."""
    covered = set()
    for start, end in intervals:
        covered.update(range(2 * start, 2 * end + 1))
    result = []
    for p in sorted(covered):
        if result and p == result[-1][1] + 1:
            result[-1][1] = p
        else:
            result.append([p, p])
    return [[a // 2, b // 2] for a, b in result]


def check(ns):
    solve = ns["Solution"]().merge

    def run(intervals):
        return solve(copy.deepcopy(intervals))

    assert run([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert run([[1, 4], [4, 5]]) == [[1, 5]]
    assert run([[4, 7], [1, 4]]) == [[1, 7]]
    assert run([[1, 4]]) == [[1, 4]]
    assert run([[1, 10], [2, 3]]) == [[1, 10]]
    assert run([[1, 1], [1, 1]]) == [[1, 1]]
    assert run([[0, 0], [1, 1]]) == [[0, 0], [1, 1]]
    assert run([[1, 2], [2, 3], [3, 4]]) == [[1, 4]]
    assert run([[1, 2], [3, 4]]) == [[1, 2], [3, 4]]
    assert run([[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]]) == [[1, 10]]
    rng = random.Random(17)
    for _ in range(400):
        intervals = []
        for _ in range(rng.randint(1, 9)):
            a = rng.randint(0, 20)
            intervals.append([a, a + rng.randint(0, 5)])
        assert run(intervals) == _reference(intervals), intervals
