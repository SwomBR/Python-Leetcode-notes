"""Tests for 018 Non-overlapping Intervals."""
import copy
import random


def _reference(intervals):
    """Independent reference: O(n^2) DP for the largest non-overlapping set."""
    ordered = sorted(intervals, key=lambda x: (x[1], x[0]))
    n = len(ordered)
    best = [1] * n
    for i in range(n):
        for j in range(i):
            if ordered[j][1] <= ordered[i][0]:
                best[i] = max(best[i], best[j] + 1)
    return n - (max(best) if best else 0)


def check(ns):
    solve = ns["Solution"]().eraseOverlapIntervals

    def run(intervals):
        return solve(copy.deepcopy(intervals))

    assert run([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert run([[1, 2], [1, 2], [1, 2]]) == 2
    assert run([[1, 2], [2, 3]]) == 0
    assert run([[1, 5]]) == 0
    assert run([[1, 10], [2, 3], [4, 5]]) == 1
    assert run([[-3, -1], [-2, 0]]) == 1
    assert run([[1, 2], [2, 3], [3, 4], [4, 5]]) == 0
    assert run([[1, 100], [11, 22], [1, 11], [2, 12]]) == 2
    rng = random.Random(18)
    for _ in range(300):
        intervals = []
        for _ in range(rng.randint(1, 9)):
            a = rng.randint(-10, 10)
            intervals.append([a, a + rng.randint(1, 6)])
        assert run(intervals) == _reference(intervals), intervals
