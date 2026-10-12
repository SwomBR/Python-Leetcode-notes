"""Tests for 055 Climbing Stairs (LeetCode 70)."""
import random


def _reference(n):
    """Independent reference: count step sequences with a full DP table."""
    ways = [0] * (n + 1)
    ways[0] = 1
    for i in range(1, n + 1):
        ways[i] = ways[i - 1] + (ways[i - 2] if i >= 2 else 0)
    return ways[n]


def check(ns):
    solve = ns["Solution"]().climbStairs
    assert solve(2) == 2
    assert solve(3) == 3
    assert solve(1) == 1
    assert solve(4) == 5
    assert solve(5) == 8
    assert solve(10) == 89
    # the brute-force recursion is exponential, so these tests stay at n <= 25
    for n in range(1, 26):
        assert solve(n) == _reference(n), n
    rng = random.Random(55)
    for _ in range(20):
        n = rng.randint(1, 25)
        assert solve(n) == _reference(n), n
