"""Tests for 007 Find Minimum in Rotated Sorted Array."""
import random


def check(ns):
    solve = ns["Solution"]().findMin
    assert solve([3, 4, 5, 1, 2]) == 1
    assert solve([4, 5, 6, 7, 0, 1, 2]) == 0
    assert solve([11, 13, 15, 17]) == 11
    assert solve([1]) == 1
    assert solve([2, 1]) == 1
    assert solve([1, 2]) == 1
    assert solve([5, 1, 2, 3, 4]) == 1
    assert solve([2, 3, 4, 5, 1]) == 1
    rng = random.Random(7)
    for _ in range(400):
        n = rng.randint(1, 20)
        base = sorted(rng.sample(range(-50, 51), n))
        k = rng.randint(1, n)                    # rotated k times
        nums = base[-k:] + base[:-k] if k < n else list(base)
        assert solve(list(nums)) == min(base), nums
