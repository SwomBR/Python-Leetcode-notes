"""Tests for 001 Two Sum."""
import random


def _valid(nums, target, answer):
    i, j = answer
    return i != j and 0 <= i < len(nums) and 0 <= j < len(nums) and nums[i] + nums[j] == target


def check(ns):
    solve = ns["Solution"]().twoSum
    cases = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
        ([-3, 4, 3, 90], 0, [0, 2]),
        ([0, 4, 3, 0], 0, [0, 3]),
    ]
    for nums, target, expected in cases:
        assert sorted(solve(list(nums), target)) == expected, (nums, target)
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(2, 30)
        nums = rng.sample(range(-1000, 1000), n)
        i, j = rng.sample(range(n), 2)
        target = nums[i] + nums[j]
        # guarantee exactly one answer by checking uniqueness
        pairs = [(a, b) for a in range(n) for b in range(a + 1, n) if nums[a] + nums[b] == target]
        if len(pairs) != 1:
            continue
        assert _valid(nums, target, solve(list(nums), target))
