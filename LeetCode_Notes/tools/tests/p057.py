"""Tests for 057 Longest Increasing Subsequence (LeetCode 300)."""
import itertools
import random


def _reference(nums):
    # Independent check: try every subset of indices (small n only).
    best = 0
    n = len(nums)
    for mask in range(1, 1 << n):
        chosen = [nums[i] for i in range(n) if mask >> i & 1]
        if all(a < b for a, b in zip(chosen, chosen[1:])):
            best = max(best, len(chosen))
    return best


def check(ns):
    solve = ns["Solution"]().lengthOfLIS
    # Official examples
    assert solve([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert solve([0, 1, 0, 3, 2, 3]) == 4
    assert solve([7, 7, 7, 7, 7, 7, 7]) == 1
    # Edge cases
    assert solve([5]) == 1
    assert solve([1, 2, 3, 4, 5]) == 5
    assert solve([5, 4, 3, 2, 1]) == 1
    assert solve([3, 4, 5, 1]) == 3
    assert solve([-10000, 10000]) == 2
    assert solve([4, 10, 4, 3, 8, 9]) == 3
    rng = random.Random(57)
    for _ in range(200):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(1, 10))]
        assert solve(list(nums)) == _reference(nums), nums
