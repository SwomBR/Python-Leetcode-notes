"""Tests for 016 Insert Interval."""
import copy
import random


def _reference(intervals, new_interval):
    """Independent reference: paint doubled coordinates, then read off runs.

    Doubling keeps [1, 2] and [3, 4] apart (they share no point), while
    [1, 2] and [2, 3] become one run (they share the point 2).
    """
    covered = set()
    for start, end in intervals + [new_interval]:
        covered.update(range(2 * start, 2 * end + 1))
    result = []
    for p in sorted(covered):
        if result and p == result[-1][1] + 1:
            result[-1][1] = p
        else:
            result.append([p, p])
    return [[a // 2, b // 2] for a, b in result]


def _random_sorted_disjoint(rng):
    intervals = []
    cur = rng.randint(0, 3)
    for _ in range(rng.randint(0, 6)):
        start = cur
        end = start + rng.randint(0, 3)
        intervals.append([start, end])
        cur = end + rng.randint(1, 4)   # gap >= 1, so no shared point
    return intervals


def check(ns):
    solve = ns["Solution"]().insert

    def run(intervals, new_interval):
        return solve(copy.deepcopy(intervals), list(new_interval))

    assert run([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert run([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
    assert run([], [5, 7]) == [[5, 7]]
    assert run([[3, 5]], [1, 2]) == [[1, 2], [3, 5]]
    assert run([[1, 2]], [5, 6]) == [[1, 2], [5, 6]]
    assert run([[1, 2]], [2, 3]) == [[1, 3]]
    assert run([[1, 2], [3, 4]], [0, 10]) == [[0, 10]]
    assert run([[1, 5]], [3, 3]) == [[1, 5]]
    assert run([[1, 5]], [0, 0]) == [[0, 0], [1, 5]]
    assert run([[0, 0], [2, 2]], [1, 1]) == [[0, 0], [1, 1], [2, 2]]
    rng = random.Random(16)
    for _ in range(400):
        intervals = _random_sorted_disjoint(rng)
        a = rng.randint(0, 30)
        new_interval = [a, a + rng.randint(0, 6)]
        expected = _reference(intervals, new_interval)
        assert run(intervals, new_interval) == expected, (intervals, new_interval)
