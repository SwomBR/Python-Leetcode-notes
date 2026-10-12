"""Tests for 062 House Robber II."""
import random


def _reference(nums):
    """Every subset with no two neighbours on the circle."""
    n = len(nums)
    best = 0
    for mask in range(1 << n):
        ok = True
        for i in range(n):
            j = (i + 1) % n
            if j != i and mask >> i & 1 and mask >> j & 1:
                ok = False
                break
        if ok:
            best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best


def check(ns):
    solve = ns["Solution"]().rob
    assert solve([2, 3, 2]) == 3
    assert solve([1, 2, 3, 1]) == 4
    assert solve([1, 2, 3]) == 3
    assert solve([5]) == 5
    assert solve([0]) == 0
    assert solve([5, 9]) == 9
    assert solve([2, 1, 1, 2]) == 3
    assert solve([200, 3, 140, 20, 10]) == 340
    rng = random.Random(62)
    for _ in range(300):
        nums = [rng.randint(0, 1000) for _ in range(rng.randint(1, 13))]
        assert solve(list(nums)) == _reference(nums), nums
