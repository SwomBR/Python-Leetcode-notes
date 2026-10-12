"""Tests for 010 Container With Most Water."""
import random


def _reference(height):
    n = len(height)
    return max((j - i) * min(height[i], height[j])
               for i in range(n) for j in range(i + 1, n))


def check(ns):
    solve = ns["Solution"]().maxArea
    assert solve([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert solve([1, 1]) == 1
    assert solve([0, 0]) == 0
    assert solve([0, 5]) == 0
    assert solve([4, 3, 2, 1, 4]) == 16
    assert solve([1, 2, 1]) == 2
    assert solve([10000, 10000]) == 10000
    rng = random.Random(10)
    for _ in range(400):
        height = [rng.randint(0, 10) for _ in range(rng.randint(2, 15))]
        assert solve(list(height)) == _reference(height), height
