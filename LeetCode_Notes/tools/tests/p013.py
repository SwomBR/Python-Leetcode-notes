"""Tests for 013 Counting Bits."""
import random

MIN_TESTED_BLOCKS = 3


def reference(n):
    return [format(i, "b").count("1") for i in range(n + 1)]


def check(ns):
    solve = ns["Solution"]().countBits
    # Official examples
    assert solve(2) == [0, 1, 1]
    assert solve(5) == [0, 1, 1, 2, 1, 2]
    # Edge cases
    assert solve(0) == [0]
    assert solve(1) == [0, 1]
    assert solve(8) == [0, 1, 1, 2, 1, 2, 2, 3, 1]
    big = solve(100000)
    assert len(big) == 100001
    assert big[100000] == 6
    assert big == reference(100000)
    rng = random.Random(13)
    for _ in range(200):
        n = rng.randint(0, 2000)
        assert solve(n) == reference(n), n
