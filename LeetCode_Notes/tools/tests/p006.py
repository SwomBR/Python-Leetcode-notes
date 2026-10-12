"""Tests for 006 Maximum Product Subarray."""
import math
import random


def _reference(nums):
    return max(math.prod(nums[i:j + 1])
               for i in range(len(nums)) for j in range(i, len(nums)))


def check(ns):
    solve = ns["Solution"]().maxProduct
    assert solve([2, 3, -2, 4]) == 6
    assert solve([-2, 0, -1]) == 0
    assert solve([-2]) == -2
    assert solve([0]) == 0
    assert solve([-2, 3, -4]) == 24
    assert solve([-2, -3, 0, -4]) == 6
    assert solve([0, 2]) == 2
    assert solve([-1, -1]) == 1
    assert solve([3, -1, 4]) == 4
    assert solve([2, -5, -2, -4, 3]) == 24
    rng = random.Random(6)
    for _ in range(400):
        nums = [rng.randint(-4, 4) for _ in range(rng.randint(1, 12))]
        assert solve(list(nums)) == _reference(nums), nums
