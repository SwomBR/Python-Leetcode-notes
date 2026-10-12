"""Tests for 004 Product of Array Except Self."""
import math
import random


def check(ns):
    solve = ns["Solution"]().productExceptSelf
    assert solve([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert solve([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    assert solve([0, 0]) == [0, 0]
    assert solve([2, 3]) == [3, 2]
    assert solve([0, 4, 5]) == [20, 0, 0]
    rng = random.Random(4)
    for _ in range(300):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(2, 10))]
        expected = [math.prod(nums[:i] + nums[i + 1:]) for i in range(len(nums))]
        assert solve(list(nums)) == expected, nums
