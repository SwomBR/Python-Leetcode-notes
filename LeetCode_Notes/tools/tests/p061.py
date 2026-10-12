"""Tests for 061 House Robber."""
import random


def _reference(nums):
    """Try every subset of houses; keep the ones with no two adjacent."""
    n = len(nums)
    best = 0
    for mask in range(1 << n):
        if mask & (mask >> 1):
            continue  # two neighbouring houses chosen
        best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best


def check(ns):
    solve = ns["Solution"]().rob
    assert solve([1, 2, 3, 1]) == 4
    assert solve([2, 7, 9, 3, 1]) == 12
    assert solve([5]) == 5
    assert solve([0]) == 0
    assert solve([1, 9]) == 9
    assert solve([2, 1, 1, 2]) == 4
    assert solve([0, 0, 0]) == 0
    assert solve([400, 400, 400]) == 800
    rng = random.Random(61)
    for _ in range(300):
        nums = [rng.randint(0, 400) for _ in range(rng.randint(1, 14))]
        assert solve(list(nums)) == _reference(nums), nums
