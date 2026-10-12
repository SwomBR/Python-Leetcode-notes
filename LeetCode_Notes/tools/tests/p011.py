"""Tests for 011 Sum of Two Integers."""
import random


def check(ns):
    solve = ns["Solution"]().getSum
    # Official examples
    assert solve(1, 2) == 3
    assert solve(2, 3) == 5
    # Edge cases
    assert solve(0, 0) == 0
    assert solve(-1, 1) == 0
    assert solve(-3, -2) == -5
    assert solve(5, -8) == -3
    assert solve(-5, 8) == 3
    assert solve(1000, 1000) == 2000
    assert solve(-1000, -1000) == -2000
    assert solve(-1000, 1000) == 0
    assert solve(-7, 0) == -7
    assert solve(0, -7) == -7
    # Systematic sweep across the full constraint range
    for a in range(-1000, 1001, 37):
        for b in range(-1000, 1001, 41):
            assert solve(a, b) == a + b, (a, b)
    # Random comparison against Python's own addition
    rng = random.Random(11)
    for _ in range(3000):
        a = rng.randint(-1000, 1000)
        b = rng.randint(-1000, 1000)
        assert solve(a, b) == a + b, (a, b)
