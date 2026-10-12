"""Tests for 014 Missing Number."""
import random

MIN_TESTED_BLOCKS = 3


def reference(nums):
    present = [False] * (len(nums) + 1)
    for v in nums:
        present[v] = True
    return present.index(False)


def check(ns):
    solve = ns["Solution"]().missingNumber
    # Official examples
    assert solve([3, 0, 1]) == 2
    assert solve([0, 1]) == 2
    assert solve([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
    # Edge cases
    assert solve([1]) == 0
    assert solve([0]) == 1
    assert solve([3, 1, 2]) == 0
    big = list(range(10001))
    big.remove(5000)
    random.Random(0).shuffle(big)
    assert solve(list(big)) == 5000
    big2 = list(range(10000))  # n = 10^4 missing
    assert solve(list(big2)) == 10000
    rng = random.Random(14)
    for _ in range(500):
        n = rng.randint(1, 60)
        values = list(range(n + 1))
        values.remove(rng.randint(0, n))
        rng.shuffle(values)
        assert solve(list(values)) == reference(values), values
