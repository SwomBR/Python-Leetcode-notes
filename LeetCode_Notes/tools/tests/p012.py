"""Tests for 012 Number of 1 Bits."""
import random

MIN_TESTED_BLOCKS = 3


def reference(n):
    count = 0
    for ch in format(n, "b"):
        if ch == "1":
            count += 1
    return count


def check(ns):
    solve = ns["Solution"]().hammingWeight
    # Official examples
    assert solve(11) == 3
    assert solve(128) == 1
    assert solve(2147483645) == 30
    # Edge cases
    assert solve(1) == 1
    assert solve(2 ** 31 - 1) == 31
    assert solve(85) == 4
    assert solve(3 << 29) == 2
    for k in range(31):
        assert solve(1 << k) == 1, k
        assert solve((1 << (k + 1)) - 1) == k + 1, k
    rng = random.Random(12)
    for _ in range(3000):
        n = rng.randint(1, 2 ** 31 - 1)
        assert solve(n) == reference(n), n
