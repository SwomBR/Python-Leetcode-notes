"""Tests for 060 Combination Sum IV (LeetCode 377)."""
import itertools
import random


def _reference(nums, target):
    # Independent check: count ordered sequences of each exact length k
    # by brute-force enumeration of all k-tuples (small inputs only).
    total = 0
    smallest = min(nums)
    for k in range(1, target // smallest + 1):
        for seq in itertools.product(nums, repeat=k):
            if sum(seq) == target:
                total += 1
    return total


def check(ns):
    solve = ns["Solution"]().combinationSum4
    # Official examples
    assert solve([1, 2, 3], 4) == 7
    assert solve([9], 3) == 0
    # Edge cases
    assert solve([1], 1) == 1
    assert solve([5], 10) == 1
    assert solve([2, 3], 7) == 3       # (2,2,3), (2,3,2), (3,2,2)
    assert solve([4, 2, 1], 5) == 10
    assert solve([1000], 1) == 0
    rng = random.Random(60)
    for _ in range(150):
        nums = rng.sample(range(1, 7), rng.randint(1, 3))
        target = rng.randint(1, 8)
        assert solve(list(nums), target) == _reference(nums, target), (nums, target)
