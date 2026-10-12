"""Tests for 005 Maximum Subarray."""
import random


def check(ns):
    solve = ns["Solution"]().maxSubArray
    assert solve([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert solve([1]) == 1
    assert solve([5, 4, -1, 7, 8]) == 23
    assert solve([-3, -1, -2]) == -1
    assert solve([0, -1]) == 0
    rng = random.Random(5)
    for _ in range(300):
        nums = [rng.randint(-10, 10) for _ in range(rng.randint(1, 15))]
        expected = max(sum(nums[i:j + 1]) for i in range(len(nums)) for j in range(i, len(nums)))
        assert solve(list(nums)) == expected, nums
