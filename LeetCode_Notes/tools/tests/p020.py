"""Tests for 020 Meeting Rooms II (LeetCode 253, Premium; commonly published examples)."""
import copy
import random


def _reference(intervals):
    """Independent reference: the most meetings running in any unit slot [t, t+1)."""
    lo = min(s for s, _ in intervals)
    hi = max(e for _, e in intervals)
    return max(sum(1 for s, e in intervals if s <= t < e) for t in range(lo, hi))


def check(ns):
    solve = ns["Solution"]().minMeetingRooms

    def run(intervals):
        return solve(copy.deepcopy(intervals))

    assert run([[0, 30], [5, 10], [15, 20]]) == 2
    assert run([[7, 10], [2, 4]]) == 1
    assert run([[1, 5]]) == 1
    assert run([[1, 5], [1, 5], [1, 5]]) == 3
    assert run([[1, 5], [5, 10], [10, 15]]) == 1
    assert run([[1, 10], [2, 3], [4, 5]]) == 2
    assert run([[1, 4], [2, 5], [4, 6], [5, 7]]) == 2
    assert run([[9, 10], [4, 9], [4, 17]]) == 2
    rng = random.Random(20)
    for _ in range(400):
        intervals = []
        for _ in range(rng.randint(1, 9)):
            a = rng.randint(0, 20)
            intervals.append([a, a + rng.randint(1, 6)])
        assert run(intervals) == _reference(intervals), intervals
