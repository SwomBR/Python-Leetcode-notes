"""Tests for 003 Contains Duplicate."""
import random


def check(ns):
    solve = ns["Solution"]().containsDuplicate
    assert solve([1, 2, 3, 1]) is True
    assert solve([1, 2, 3, 4]) is False
    assert solve([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True
    assert solve([7]) is False
    assert solve([-1, -1]) is True
    assert solve([0, -0]) is True
    rng = random.Random(3)
    for _ in range(300):
        nums = [rng.randint(-20, 20) for _ in range(rng.randint(1, 15))]
        assert solve(list(nums)) == (len(set(nums)) != len(nums)), nums
