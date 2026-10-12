"""Tests for 008 Search in Rotated Sorted Array."""
import random


def check(ns):
    solve = ns["Solution"]().search
    assert solve([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert solve([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert solve([1], 0) == -1
    assert solve([1], 1) == 0
    assert solve([3, 1], 1) == 1
    assert solve([3, 1], 3) == 0
    assert solve([1, 3], 3) == 1
    assert solve([5, 1, 3], 5) == 0
    assert solve([4, 5, 6, 7, 0, 1, 2], 4) == 0
    assert solve([4, 5, 6, 7, 0, 1, 2], 2) == 6
    rng = random.Random(8)
    for _ in range(400):
        n = rng.randint(1, 15)
        base = sorted(rng.sample(range(-30, 31), n))
        k = rng.randint(0, n - 1)                # 0 = not rotated
        nums = base[k:] + base[:k]
        for target in range(-32, 33, rng.randint(1, 4)):
            expected = nums.index(target) if target in nums else -1
            assert solve(list(nums), target) == expected, (nums, target)
