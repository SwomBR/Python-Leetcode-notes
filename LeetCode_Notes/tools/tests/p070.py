"""Tests for 070 Longest Consecutive Sequence (LeetCode 128)."""
import random


def _reference(nums):
    """Sort the distinct values and count runs."""
    vals = sorted(set(nums))
    best = run = 0
    for i, v in enumerate(vals):
        run = run + 1 if i > 0 and vals[i - 1] == v - 1 else 1
        best = max(best, run)
    return best


def check(ns):
    solve = ns["Solution"]().longestConsecutive
    assert solve([100, 4, 200, 1, 3, 2]) == 4
    assert solve([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert solve([1, 0, 1, 2]) == 3
    assert solve([]) == 0
    assert solve([5]) == 1
    assert solve([7, 7, 7]) == 1
    assert solve([-1, -2, -3, 10]) == 3
    assert solve([10 ** 9, -10 ** 9, 10 ** 9 - 1]) == 2
    rng = random.Random(70)
    for _ in range(400):
        nums = [rng.randint(-8, 8) for _ in range(rng.randint(0, 25))]
        assert solve(list(nums)) == _reference(nums), nums
