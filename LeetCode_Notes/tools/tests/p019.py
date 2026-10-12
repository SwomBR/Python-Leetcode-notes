"""Tests for 019 Meeting Rooms (LeetCode 252, Premium; commonly published examples)."""
import copy
import random


def _reference(intervals):
    """Independent reference: count meetings covering each unit slot [t, t+1)."""
    if not intervals:
        return True
    lo = min(s for s, _ in intervals)
    hi = max(e for _, e in intervals)
    for t in range(lo, hi):
        if sum(1 for s, e in intervals if s <= t < e) > 1:
            return False
    return True


def check(ns):
    solve = ns["Solution"]().canAttendMeetings

    def run(intervals):
        return solve(copy.deepcopy(intervals))

    assert run([[0, 30], [5, 10], [15, 20]]) is False
    assert run([[7, 10], [2, 4]]) is True
    assert run([]) is True
    assert run([[1, 5]]) is True
    assert run([[1, 5], [5, 10]]) is True
    assert run([[1, 5], [1, 5]]) is False
    assert run([[1, 10], [2, 3]]) is False
    assert run([[5, 8], [1, 3], [3, 5]]) is True
    rng = random.Random(19)
    for _ in range(400):
        intervals = []
        for _ in range(rng.randint(0, 6)):
            a = rng.randint(0, 25)
            intervals.append([a, a + rng.randint(1, 5)])
        assert run(intervals) == _reference(intervals), intervals
